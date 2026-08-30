"""
Road Type (highway class) Classifier - Lahore
================================================
NOTE ON DATA: the `lat`/`lon` columns in roads_lahore.csv are all 0 for
every row (a data export issue), so no real geospatial features exist.
The only informative signal is the road `name` itself (many are in
Urdu/Arabic script, some in English), so this model predicts the
`highway` class (primary/secondary/tertiary) purely from the name text
using TF-IDF character n-grams (robust across scripts/languages) plus
a classifier.

Compares Logistic Regression, Linear SVM, Random Forest and
Multinomial Naive Bayes with a stratified train/test split, selects
the best by weighted F1, refits on full data, and exports:
  1. test-set predictions (actual vs predicted) as JSON
  2. predictions for every road in the dataset as JSON

Usage:
    python road_type_classifier.py --input roads_lahore.csv \
        --output roads_predictions.json
"""

import argparse
import json
import os
import warnings

import joblib
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

warnings.filterwarnings("ignore")


def make_vectorizer():
    # char n-grams handle multilingual (Urdu/English) short strings far
    # better than word-level tokenization
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=2, max_features=20000)


CANDIDATE_MODELS = {
    "logistic_regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "linear_svm": LinearSVC(class_weight="balanced", max_iter=5000),
    "random_forest": RandomForestClassifier(
        n_estimators=300, max_depth=25, class_weight="balanced", random_state=42, n_jobs=-1
    ),
    "naive_bayes": MultinomialNB(),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="roads_lahore.csv")
    parser.add_argument("--output", default="roads_predictions.json")
    parser.add_argument("--model-dir", default="models/roads")
    parser.add_argument("--label-col", default="highway")
    args = parser.parse_args()

    raw = pd.read_csv(args.input)
    raw["name"] = raw["name"].fillna("unknown")
    label_col = args.label_col

    X_text = raw["name"]
    y = raw[label_col]

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X_text, y, raw.index, test_size=0.2, random_state=42, stratify=y
    )

    os.makedirs(args.model_dir, exist_ok=True)

    results = {}
    fitted_pipelines = {}
    for name, clf_template in CANDIDATE_MODELS.items():
        pipe = Pipeline([("tfidf", make_vectorizer()), ("clf", clone(clf_template))])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="weighted")
        results[name] = {"accuracy": round(acc, 4), "f1_weighted": round(f1, 4)}
        fitted_pipelines[name] = pipe
        print(f"  {name}: accuracy={acc:.4f} f1={f1:.4f}")

    best_name = max(results, key=lambda n: results[n]["f1_weighted"])
    best_pipe = fitted_pipelines[best_name]
    print(f"\nBest model: {best_name}")
    print(classification_report(y_test, best_pipe.predict(X_test)))

    # refit best pipeline on ALL data for deployment
    final_pipe = Pipeline([("tfidf", make_vectorizer()), ("clf", clone(CANDIDATE_MODELS[best_name]))])
    final_pipe.fit(X_text, y)
    joblib.dump(final_pipe, f"{args.model_dir}/road_type_model.joblib")

    metrics_report = {
        "best_model": best_name,
        "test_accuracy": results[best_name]["accuracy"],
        "test_f1_weighted": results[best_name]["f1_weighted"],
        "all_candidates": results,
        "class_distribution": y.value_counts().to_dict(),
    }

    def has_proba(pipe):
        return hasattr(pipe.named_steps["clf"], "predict_proba")

    # 1) Test-set predictions
    test_preds = best_pipe.predict(X_test)
    test_conf = best_pipe.predict_proba(X_test).max(axis=1) if has_proba(best_pipe) else [None] * len(X_test)
    test_records = []
    for i, row_idx in enumerate(idx_test):
        row = raw.loc[row_idx]
        test_records.append(
            {
                "id": int(row["id"]),
                "name": row["name"],
                "actual_highway": row[label_col],
                "predicted_highway": test_preds[i],
                "confidence": round(float(test_conf[i]), 4) if test_conf[i] is not None else None,
                "correct": bool(row[label_col] == test_preds[i]),
            }
        )

    test_output = {
        "source": "road_type_classifier",
        "stage": "test_set_predictions",
        "num_test_rows": len(test_records),
        "model_metrics": metrics_report,
        "predictions": test_records,
    }
    test_path = args.output.replace(".json", "_test_predictions.json")
    with open(test_path, "w") as f:
        json.dump(test_output, f, indent=2, default=str)
    print(f"\nSaved TEST-SET predictions JSON -> {test_path}")

    # 2) Predictions for every road (sampled if huge; here we do the full set)
    full_preds = final_pipe.predict(X_text)
    full_conf = final_pipe.predict_proba(X_text).max(axis=1) if has_proba(final_pipe) else [None] * len(X_text)
    all_records = []
    for i, row_idx in enumerate(raw.index):
        row = raw.loc[row_idx]
        all_records.append(
            {
                "id": int(row["id"]),
                "name": row["name"],
                "actual_highway": row[label_col],
                "predicted_highway": full_preds[i],
                "confidence": round(float(full_conf[i]), 4) if full_conf[i] is not None else None,
            }
        )

    output = {
        "source": "road_type_classifier",
        "stage": "full_dataset_predictions",
        "num_roads": len(all_records),
        "model_metrics": metrics_report,
        "predictions": all_records,
    }
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Saved FULL-DATASET predictions JSON -> {args.output}")


if __name__ == "__main__":
    main()
