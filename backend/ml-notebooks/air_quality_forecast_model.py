"""
Air Quality Forecasting Model - Lahore
========================================
Trains regression models to forecast next-day PM2.5 and PM10 from
historical daily air-quality data (pm25, pm10, temperature, humidity),
using lag/rolling/seasonal features. Compares Linear Regression, Random
Forest, Gradient Boosting and XGBoost with a chronological train/test
split, selects the best model per target by MAE, refits on full data,
then produces a multi-day forward forecast.

AQI category + health advisory are derived deterministically from the
forecast PM2.5 value using standard EPA PM2.5 breakpoints, so category
labels are always consistent with the numeric forecast.

Output: a single JSON object (also saved to disk) shaped for downstream
consumption by an LLM / alerting engine.

Usage:
    python air_quality_forecast_model.py --input air_quality_data.csv \
        --forecast-days 7 --output air_quality_forecast.json
"""

import argparse
import json
import os
import warnings
from datetime import timedelta

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")

TARGET_COLS = ["pm25", "pm10"]
FEATURE_BASE_COLS = ["pm25", "pm10", "temperature", "humidity"]
LAGS = [1, 2, 3, 7]
ROLL_WINDOW = 7

# EPA PM2.5 breakpoints: (low, high, category, health_advisory)
AQI_BREAKPOINTS = [
    (0.0, 12.0, "Good", "Air quality is satisfactory; enjoy normal activities."),
    (12.1, 35.4, "Moderate", "Unusually sensitive people should consider reducing prolonged outdoor exertion."),
    (35.5, 55.4, "Unhealthy for Sensitive Groups", "Children, elderly, and people with respiratory/heart conditions should limit outdoor exertion."),
    (55.5, 150.4, "Unhealthy", "Everyone may begin to experience health effects; sensitive groups should avoid outdoor exertion."),
    (150.5, 250.4, "Very Unhealthy", "Health alert: everyone should avoid prolonged outdoor exertion."),
    (250.5, 500.4, "Hazardous", "Health emergency: everyone should avoid all outdoor exertion."),
]


def aqi_category(pm25_value: float):
    for low, high, category, advisory in AQI_BREAKPOINTS:
        if low <= pm25_value <= high:
            return category, advisory
    return "Hazardous", AQI_BREAKPOINTS[-1][3]


# ----------------------------------------------------------------------
# Feature engineering
# ----------------------------------------------------------------------
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    for col in FEATURE_BASE_COLS:
        for lag in LAGS:
            df[f"{col}_lag{lag}"] = df[col].shift(lag)
        df[f"{col}_roll_mean{ROLL_WINDOW}"] = df[col].shift(1).rolling(ROLL_WINDOW).mean()
        df[f"{col}_roll_std{ROLL_WINDOW}"] = df[col].shift(1).rolling(ROLL_WINDOW).std()

    doy = df["date"].dt.dayofyear
    df["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)
    df["month"] = df["date"].dt.month
    # Lahore winter smog season (heavy crop burning + inversion): Oct-Feb
    df["is_smog_season"] = df["month"].isin([10, 11, 12, 1, 2]).astype(int)

    return df


def feature_columns(df: pd.DataFrame) -> list:
    non_features = set(TARGET_COLS + ["date", "temperature", "humidity"])
    return [c for c in df.columns if c not in non_features]


# ----------------------------------------------------------------------
# Model selection
# ----------------------------------------------------------------------
CANDIDATE_MODELS = {
    "linear_regression": LinearRegression(),
    "random_forest": RandomForestRegressor(
        n_estimators=400, max_depth=8, random_state=42, n_jobs=-1
    ),
    "gradient_boosting": GradientBoostingRegressor(
        n_estimators=300, max_depth=3, learning_rate=0.05, random_state=42
    ),
    "xgboost": XGBRegressor(
        n_estimators=400,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
    ),
}


def train_and_select_best(X_train, y_train, X_test, y_test):
    """Uses sklearn.clone() so each target gets its own fresh model instance —
    CANDIDATE_MODELS holds only unfitted templates, so one target's fit()
    never overwrites another's."""
    results = {}
    fitted = {}
    for name, template in CANDIDATE_MODELS.items():
        model = clone(template)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        r2 = r2_score(y_test, preds)
        results[name] = {"mae": mae, "rmse": rmse, "r2": r2}
        fitted[name] = model

    best_name = min(results, key=lambda n: results[n]["mae"])
    return best_name, fitted[best_name], results


# ----------------------------------------------------------------------
# Forecasting
# ----------------------------------------------------------------------
def export_test_predictions(test_df, models, feat_cols):
    """Run the TRAIN-fit models on the held-out TEST rows and return
    row-by-row {actual vs predicted} as JSON-ready records."""
    X_test = test_df[feat_cols]
    records = []
    preds_by_target = {t: models[t].predict(X_test) for t in TARGET_COLS}

    for i, (_, row) in enumerate(test_df.iterrows()):
        record = {"date": row["date"].strftime("%Y-%m-%d")}
        for target in TARGET_COLS:
            actual = float(row[target])
            predicted = round(float(preds_by_target[target][i]), 2)
            record[target] = {
                "actual": round(actual, 2),
                "predicted": predicted,
                "error": round(predicted - actual, 2),
            }
        category, advisory = aqi_category(record["pm25"]["predicted"])
        record["aqi_category_predicted"] = category
        record["health_advisory"] = advisory
        records.append(record)
    return records


def forecast_forward(df_feat, models, feat_cols, n_days):
    history = df_feat[["date"] + FEATURE_BASE_COLS].copy()
    forecasts = []

    # naive next-day temp/humidity assumption: persist seasonal rolling mean
    for step in range(n_days):
        last_date = history["date"].iloc[-1]
        next_date = last_date + timedelta(days=1)

        row = {"date": next_date}
        for col in FEATURE_BASE_COLS:
            series = history[col]
            for lag in LAGS:
                row[f"{col}_lag{lag}"] = series.iloc[-lag]
            row[f"{col}_roll_mean{ROLL_WINDOW}"] = series.iloc[-ROLL_WINDOW:].mean()
            row[f"{col}_roll_std{ROLL_WINDOW}"] = series.iloc[-ROLL_WINDOW:].std()

        doy = next_date.dayofyear
        row["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
        row["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)
        row["month"] = next_date.month
        row["is_smog_season"] = int(next_date.month in [10, 11, 12, 1, 2])

        x_row = pd.DataFrame([row])[feat_cols]

        pred = {}
        for col in TARGET_COLS:
            val = max(0.0, float(models[col].predict(x_row)[0]))
            pred[col] = round(val, 2)

        # carry forward temperature/humidity using recent rolling mean
        # (no dedicated weather model wired in here; keeps the pipeline self-contained)
        next_temp = round(float(history["temperature"].iloc[-ROLL_WINDOW:].mean()), 1)
        next_humidity = round(float(history["humidity"].iloc[-ROLL_WINDOW:].mean()), 1)

        category, advisory = aqi_category(pred["pm25"])

        forecasts.append(
            {
                "date": next_date.strftime("%Y-%m-%d"),
                "pm25": pred["pm25"],
                "pm10": pred["pm10"],
                "aqi_category": category,
                "health_advisory": advisory,
            }
        )

        history = pd.concat(
            [
                history,
                pd.DataFrame(
                    [
                        {
                            "date": next_date,
                            "pm25": pred["pm25"],
                            "pm10": pred["pm10"],
                            "temperature": next_temp,
                            "humidity": next_humidity,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    return forecasts


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="air_quality_data.csv")
    parser.add_argument("--forecast-days", type=int, default=7)
    parser.add_argument("--output", default="air_quality_forecast.json")
    parser.add_argument("--model-dir", default="models/air_quality")
    args = parser.parse_args()

    raw = pd.read_csv(args.input)
    feat_df = build_features(raw)
    feat_df_full = feat_df.copy()
    feat_df = feat_df.dropna().reset_index(drop=True)

    feat_cols = feature_columns(feat_df)

    split_idx = int(len(feat_df) * 0.85)
    train_df = feat_df.iloc[:split_idx]
    test_df = feat_df.iloc[split_idx:]

    X_train, X_test = train_df[feat_cols], test_df[feat_cols]

    os.makedirs(args.model_dir, exist_ok=True)

    best_models = {}       # fit on TRAIN split only -> used to score the TEST set honestly
    deploy_models = {}     # refit on FULL data -> used for forward forecasting
    metrics_report = {}

    for target in TARGET_COLS:
        y_train, y_test = train_df[target], test_df[target]
        best_name, best_model, all_results = train_and_select_best(
            X_train, y_train, X_test, y_test
        )
        best_models[target] = best_model  # already fit on X_train only

        final_model = clone(CANDIDATE_MODELS[best_name])
        final_model.fit(feat_df[feat_cols], feat_df[target])
        deploy_models[target] = final_model

        joblib.dump(best_model, f"{args.model_dir}/{target}_model_testfit.joblib")
        metrics_report[target] = {
            "best_model": best_name,
            "test_mae": round(all_results[best_name]["mae"], 4),
            "test_rmse": round(all_results[best_name]["rmse"], 4),
            "test_r2": round(all_results[best_name]["r2"], 4),
            "all_candidates": {
                n: {k: round(v, 4) for k, v in r.items()} for n, r in all_results.items()
            },
        }
        joblib.dump(final_model, f"{args.model_dir}/{target}_model.joblib")
        print(f"[{target}] best model = {best_name} | "
              f"MAE={metrics_report[target]['test_mae']} "
              f"R2={metrics_report[target]['test_r2']}")

    # 1) Predictions on the held-out TEST set (this is "test our model on testing data")
    test_predictions = export_test_predictions(test_df, best_models, feat_cols)
    test_output = {
        "source": "air_quality_forecast_model",
        "stage": "test_set_predictions",
        "location": "Lahore, Pakistan",
        "num_test_rows": len(test_predictions),
        "model_metrics": metrics_report,
        "predictions": test_predictions,
    }
    test_output_path = args.output.replace(".json", "_test_predictions.json")
    with open(test_output_path, "w") as f:
        json.dump(test_output, f, indent=2)
    print(f"\nSaved TEST-SET predictions JSON -> {test_output_path}")

    # 2) Forward forecast into the future (uses models refit on all data)
    forecasts = forecast_forward(feat_df_full, deploy_models, feat_cols, args.forecast_days)
    output = {
        "source": "air_quality_forecast_model",
        "stage": "future_forecast",
        "location": "Lahore, Pakistan",
        "generated_from_last_date": str(raw["date"].iloc[-1]),
        "forecast_horizon_days": args.forecast_days,
        "model_metrics": metrics_report,
        "forecast": forecasts,
    }
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved FUTURE forecast JSON -> {args.output}")


if __name__ == "__main__":
    main()
