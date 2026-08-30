"""
Population Density Spatial Regression - Lahore
==================================================
Trains a regression model to predict `population_density` from
geographic coordinates (longitude, latitude), using engineered
spatial features (distance from city center, quadrant). This lets the
model estimate population density at ANY point in the city -- useful
for exposure/vulnerability scoring when combined with hazard layers
(flood risk, air quality) for the alert engine.

Compares Linear Regression, Random Forest, Gradient Boosting and
XGBoost with a random train/test split, selects the best by MAE,
refits on full data, and exports:
  1. test-set predictions (actual vs predicted) as JSON
  2. predictions for every grid point in the dataset as JSON

Usage:
    python population_density_regression.py --input population_data.csv \
        --output population_predictions.json
"""

import argparse
import json
import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")

CITY_CENTER_LAT = 31.5497
CITY_CENTER_LON = 74.3436


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["dist_to_center_km"] = haversine_km(
        df["latitude"], df["longitude"], CITY_CENTER_LAT, CITY_CENTER_LON
    )
    df["north_of_center"] = (df["latitude"] > CITY_CENTER_LAT).astype(int)
    df["east_of_center"] = (df["longitude"] > CITY_CENTER_LON).astype(int)
    df["lat_x_lon"] = df["latitude"] * df["longitude"]
    return df


FEATURE_COLS = [
    "longitude",
    "latitude",
    "dist_to_center_km",
    "north_of_center",
    "east_of_center",
    "lat_x_lon",
]

CANDIDATE_MODELS = {
    "linear_regression": LinearRegression(),
    "random_forest": RandomForestRegressor(
        n_estimators=400, max_depth=12, random_state=42, n_jobs=-1
    ),
    "gradient_boosting": GradientBoostingRegressor(
        n_estimators=300, max_depth=4, learning_rate=0.05, random_state=42
    ),
    "xgboost": XGBRegressor(
        n_estimators=400,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
    ),
}


def density_tier(value: float) -> str:
    if value >= 15000:
        return "Very High"
    if value >= 8000:
        return "High"
    if value >= 3000:
        return "Moderate"
    return "Low"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="population_data.csv")
    parser.add_argument("--output", default="population_predictions.json")
    parser.add_argument("--model-dir", default="models/population")
    args = parser.parse_args()

    raw = pd.read_csv(args.input)
    feat_df = build_features(raw)

    X = feat_df[FEATURE_COLS]
    y = feat_df["population_density"]

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, feat_df.index, test_size=0.2, random_state=42
    )

    os.makedirs(args.model_dir, exist_ok=True)

    results = {}
    fitted = {}
    for name, template in CANDIDATE_MODELS.items():
        model = clone(template)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        r2 = r2_score(y_test, preds)
        results[name] = {"mae": round(mae, 2), "rmse": round(rmse, 2), "r2": round(r2, 4)}
        fitted[name] = model
        print(f"  {name}: MAE={mae:.2f} RMSE={rmse:.2f} R2={r2:.4f}")

    best_name = min(results, key=lambda n: results[n]["mae"])
    best_model = fitted[best_name]
    print(f"\nBest model: {best_name}")

    final_model = clone(CANDIDATE_MODELS[best_name])
    final_model.fit(X, y)
    joblib.dump(final_model, f"{args.model_dir}/population_density_model.joblib")

    metrics_report = {
        "best_model": best_name,
        "test_mae": results[best_name]["mae"],
        "test_rmse": results[best_name]["rmse"],
        "test_r2": results[best_name]["r2"],
        "all_candidates": results,
    }

    # 1) Test-set predictions
    test_preds = best_model.predict(X_test)
    test_records = []
    for i, row_idx in enumerate(idx_test):
        row = raw.loc[row_idx]
        predicted = round(float(test_preds[i]), 1)
        test_records.append(
            {
                "longitude": float(row["longitude"]),
                "latitude": float(row["latitude"]),
                "actual_density": round(float(row["population_density"]), 1),
                "predicted_density": predicted,
                "error": round(predicted - row["population_density"], 1),
                "density_tier_predicted": density_tier(predicted),
            }
        )

    test_output = {
        "source": "population_density_regression",
        "stage": "test_set_predictions",
        "num_test_rows": len(test_records),
        "model_metrics": metrics_report,
        "predictions": test_records,
    }
    test_path = args.output.replace(".json", "_test_predictions.json")
    with open(test_path, "w") as f:
        json.dump(test_output, f, indent=2, default=str)
    print(f"\nSaved TEST-SET predictions JSON -> {test_path}")

    # 2) Predictions for every grid point (deployment model, fit on full data)
    full_preds = final_model.predict(X)
    all_records = []
    for i, row_idx in enumerate(feat_df.index):
        row = raw.loc[row_idx]
        predicted = round(float(full_preds[i]), 1)
        all_records.append(
            {
                "longitude": float(row["longitude"]),
                "latitude": float(row["latitude"]),
                "actual_density": round(float(row["population_density"]), 1),
                "predicted_density": predicted,
                "density_tier_predicted": density_tier(predicted),
            }
        )

    output = {
        "source": "population_density_regression",
        "stage": "full_dataset_predictions",
        "num_points": len(all_records),
        "model_metrics": metrics_report,
        "predictions": all_records,
    }
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Saved FULL-DATASET predictions JSON -> {args.output}")


if __name__ == "__main__":
    main()
