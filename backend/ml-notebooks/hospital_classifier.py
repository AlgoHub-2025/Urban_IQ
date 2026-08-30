"""
Hospital/Clinic Facility Classifier - Lahore
===============================================
Trains a classification model to predict facility `type` (hospital vs
clinic) from its geographic location (lat/lon), using engineered
spatial features: distance from city center, bearing/quadrant, and
local point density.

Compares Logistic Regression, Random Forest, Gradient Boosting and
XGBoost with a stratified train/test split (since classes are
imbalanced: ~81% hospital / ~19% clinic), selects the best by F1-score,
refits on full data, and exports:
  1. test-set predictions (actual vs predicted) as JSON
  2. predictions for every facility in the dataset as JSON

Usage:
    python hospital_classifier.py --input hospitals_lahore.csv \
        --output hospitals_predictions.json
"""

import argparse
import json
import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import BallTree
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

# Lahore approximate city center (Data Darbar / city core)
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
        df["lat"], df["lon"], CITY_CENTER_LAT, CITY_CENTER_LON
    )
    df["north_of_center"] = (df["lat"] > CITY_CENTER_LAT).astype(int)
    df["east_of_center"] = (df["lon"] > CITY_CENTER_LON).astype(int)

    # local density: how many other facilities within ~1.5km (spatial context,
    # not the label itself, so it doesn't leak type info)
    coords_rad = np.radians(df[["lat", "lon"]].values)
    tree = BallTree(coords_rad, metric="haversine")
    radius = 1.5 / 6371.0  # 1.5 km in radians
    counts = tree.query_radius(coords_rad, r=radius, count_only=True)
    df["neighbors_within_1_5km"] = counts - 1  # exclude self

    return df


FEATURE_COLS = [
    "lat",
    "lon",
    "dist_to_center_km",
    "north_of_center",
    "east_of_center",
    "neighbors_within_1_5km",
]

CANDIDATE_MODELS = {
    "logistic_regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "random_forest": RandomForestClassifier(
        n_estimators=400, max_depth=8, class_weight="balanced", random_state=42, n_jobs=-1
    ),
    "gradient_boosting": GradientBoostingClassifier(
        n_estimators=300, max_depth=3, learning_rate=0.05, random_state=42
    ),
    "xgboost": XGBClassifier(
        n_estimators=400,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss",
    ),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="hospitals_lahore.csv")
    parser.add_argument("--output", default="hospitals_predictions.json")
    parser.add_argument("--model-dir", default="models/hospitals")
    args = parser.parse_args()

    raw = pd.read_csv(args.input)
    raw["type"] = raw["type"].str.lower().str.strip()
    feat_df = build_features(raw)

    X = feat_df[FEATURE_COLS]
    y_str = feat_df["type"]
    label_encoder = LabelEncoder()
    y = pd.Series(label_encoder.fit_transform(y_str), index=y_str.index)

    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=FEATURE_COLS, index=X.index)

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X_scaled, y, feat_df.index, test_size=0.2, random_state=42, stratify=y
    )

    os.makedirs(args.model_dir, exist_ok=True)

    results = {}
    fitted = {}
    for name, template in CANDIDATE_MODELS.items():
        model = clone(template)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="weighted")
        results[name] = {"accuracy": round(acc, 4), "f1_weighted": round(f1, 4)}
        fitted[name] = model
        print(f"  {name}: accuracy={acc:.4f} f1={f1:.4f}")

    best_name = max(results, key=lambda n: results[n]["f1_weighted"])
    best_model = fitted[best_name]
    print(f"\nBest model: {best_name}")
    print(classification_report(y_test, best_model.predict(X_test), target_names=label_encoder.classes_))

    # refit best model type on ALL data for deployment
    final_model = clone(CANDIDATE_MODELS[best_name])
    final_model.fit(X_scaled, y)
    joblib.dump(final_model, f"{args.model_dir}/hospital_type_model.joblib")
    joblib.dump(scaler, f"{args.model_dir}/scaler.joblib")
    joblib.dump(label_encoder, f"{args.model_dir}/label_encoder.joblib")

    metrics_report = {
        "best_model": best_name,
        "test_accuracy": results[best_name]["accuracy"],
        "test_f1_weighted": results[best_name]["f1_weighted"],
        "all_candidates": results,
        "class_distribution": y_str.value_counts().to_dict(),
    }

    # 1) Test-set predictions
    test_records = []
    test_preds_enc = best_model.predict(X_test)
    test_preds = label_encoder.inverse_transform(test_preds_enc)
    test_proba = best_model.predict_proba(X_test)
    for i, row_idx in enumerate(idx_test):
        row = raw.loc[row_idx]
        test_records.append(
            {
                "id": int(row["id"]),
                "name": row["name"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "actual_type": row["type"],
                "predicted_type": test_preds[i],
                "confidence": round(float(max(test_proba[i])), 4),
                "correct": bool(row["type"] == test_preds[i]),
            }
        )

    test_output = {
        "source": "hospital_classifier",
        "stage": "test_set_predictions",
        "num_test_rows": len(test_records),
        "model_metrics": metrics_report,
        "predictions": test_records,
    }
    test_path = args.output.replace(".json", "_test_predictions.json")
    with open(test_path, "w") as f:
        json.dump(test_output, f, indent=2, default=str)
    print(f"\nSaved TEST-SET predictions JSON -> {test_path}")

    # 2) Predictions for every facility (using the fully-trained deployment model)
    full_preds_enc = final_model.predict(X_scaled)
    full_preds = label_encoder.inverse_transform(full_preds_enc)
    full_proba = final_model.predict_proba(X_scaled)
    all_records = []
    for i, row_idx in enumerate(feat_df.index):
        row = raw.loc[row_idx]
        all_records.append(
            {
                "id": int(row["id"]),
                "name": row["name"],
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "actual_type": row["type"],
                "predicted_type": full_preds[i],
                "confidence": round(float(max(full_proba[i])), 4),
            }
        )

    output = {
        "source": "hospital_classifier",
        "stage": "full_dataset_predictions",
        "num_facilities": len(all_records),
        "model_metrics": metrics_report,
        "predictions": all_records,
    }
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Saved FULL-DATASET predictions JSON -> {args.output}")


if __name__ == "__main__":
    main()
