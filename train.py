"""Train, select and evaluate the model using held-out patient groups."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.config import evaluation_path, model_path
from app.ml.features import FEATURE_COLUMNS, HORIZON_MINUTES, SPIKE_THRESHOLD_MG_DL, build_training_frame

SEED = 20260626


def split_patients(frame: pd.DataFrame) -> tuple[set[str], set[str], set[str]]:
    patients = np.array(sorted(frame.patient_id.unique()))
    rng = np.random.default_rng(SEED)
    rng.shuffle(patients)
    train_end = max(1, int(len(patients) * 0.6))
    validation_end = max(train_end + 1, int(len(patients) * 0.8))
    validation_end = min(validation_end, len(patients) - 1)
    return set(patients[:train_end]), set(patients[train_end:validation_end]), set(patients[validation_end:])


def pipeline_for(name: str) -> Pipeline:
    if name == "logistic_regression":
        estimator = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=SEED, solver="liblinear")
        return Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                         ("scaler", StandardScaler()), ("model", estimator)])
    if name == "random_forest":
        estimator = RandomForestClassifier(n_estimators=180, min_samples_leaf=4, class_weight="balanced",
                                           n_jobs=-1, random_state=SEED)
        return Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)), ("model", estimator)])
    if name == "majority_baseline":
        return Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                         ("model", DummyClassifier(strategy="prior"))])
    raise ValueError(f"Unknown model: {name}")


def metrics(y_true: pd.Series, scores: np.ndarray, predictions: np.ndarray) -> dict:
    matrix = confusion_matrix(y_true, predictions, labels=[0, 1])
    result = {
        "precision": float(precision_score(y_true, predictions, zero_division=0)),
        "recall": float(recall_score(y_true, predictions, zero_division=0)),
        "f1": float(f1_score(y_true, predictions, zero_division=0)),
        "pr_auc": float(average_precision_score(y_true, scores)),
        "roc_auc": float(roc_auc_score(y_true, scores)) if y_true.nunique() > 1 else None,
        "confusion_matrix_labels_0_1": matrix.tolist(),
        "class_distribution": {str(int(key)): int(value) for key, value in y_true.value_counts().sort_index().items()},
        "sample_count": int(len(y_true)),
    }
    return result


def train(data_path: Path, output_model: Path | None = None, output_report: Path | None = None) -> dict:
    raw = pd.read_csv(data_path)
    frame = build_training_frame(raw)
    if frame.patient_id.nunique() < 5 or frame.future_spike.nunique() < 2:
        raise ValueError("Training requires at least five patients and both target classes.")
    train_ids, validation_ids, test_ids = split_patients(frame)
    partitions = {"train": frame[frame.patient_id.isin(train_ids)],
                  "validation": frame[frame.patient_id.isin(validation_ids)],
                  "test": frame[frame.patient_id.isin(test_ids)]}
    if any(partitions[part].empty for part in partitions):
        raise ValueError("Patient-group split produced an empty partition.")
    candidates = ["majority_baseline", "logistic_regression", "random_forest"]
    validation_metrics = {}
    fitted = {}
    X_train = partitions["train"][FEATURE_COLUMNS]
    y_train = partitions["train"]["future_spike"]
    X_validation = partitions["validation"][FEATURE_COLUMNS]
    y_validation = partitions["validation"]["future_spike"]
    for name in candidates:
        candidate = pipeline_for(name)
        candidate.fit(X_train, y_train)
        scores = candidate.predict_proba(X_validation)[:, 1]
        predictions = (scores >= 0.5).astype(int)
        validation_metrics[name] = metrics(y_validation, scores, predictions)
        fitted[name] = candidate
    selected_name = max(candidates, key=lambda name: validation_metrics[name]["pr_auc"])
    selected = fitted[selected_name]
    X_test = partitions["test"][FEATURE_COLUMNS]
    y_test = partitions["test"]["future_spike"]
    test_scores = selected.predict_proba(X_test)[:, 1]
    test_predictions = (test_scores >= 0.5).astype(int)
    synthetic_values = raw["is_synthetic"].astype(str).str.strip().str.lower().isin({"true", "1", "yes"}) if "is_synthetic" in raw else None
    is_synthetic = bool(synthetic_values.all()) if synthetic_values is not None else False
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": {"path": str(data_path), "synthetic": is_synthetic,
                    "rows": int(len(raw)), "patients": int(raw.patient_id.nunique()), "seed": 20260626},
        "target": {"name": "future_spike", "definition": f"Any glucose measurement >= {SPIKE_THRESHOLD_MG_DL:g} mg/dL in the next {HORIZON_MINUTES} minutes (8 future 15-minute samples).",
                   "note": "Prototype research label only; not a universal clinical standard or diagnostic threshold."},
        "split": {"method": "patient-group holdout; no patient appears in more than one partition",
                  "patient_counts": {part: int(partitions[part].patient_id.nunique()) for part in partitions},
                  "row_counts": {part: int(len(partitions[part])) for part in partitions}},
        "feature_columns": FEATURE_COLUMNS,
        "validation_metrics_at_threshold_0_5": validation_metrics,
        "selected_model": selected_name,
        "selection_rule": "Highest validation PR-AUC; no test-set tuning.",
        "test_metrics_at_threshold_0_5": metrics(y_test, test_scores, test_predictions),
        "limitations": ["All generated observations are synthetic and generated from simplified assumptions.",
                        "Scores are uncalibrated model outputs and are not clinical probabilities.",
                        "Held-out patients come from the same synthetic generator, so results do not establish real-world performance.",
                        "Metrics depend on a prototype 180 mg/dL threshold and the simulated event prevalence."],
    }
    model_file = output_model or model_path()
    report_file = output_report or evaluation_path()
    model_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    bundle = {"pipeline": selected, "model_name": selected_name, "model_version": "2.0.0",
              "feature_columns": FEATURE_COLUMNS, "horizon_minutes": HORIZON_MINUTES,
              "target_threshold_mg_dl": SPIKE_THRESHOLD_MG_DL, "synthetic_training_data": report["dataset"]["synthetic"]}
    joblib.dump(bundle, model_file)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Selected {selected_name} using validation PR-AUC. Test report: {report_file}")
    print(json.dumps(report["test_metrics_at_threshold_0_5"], indent=2))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/synthetic_glucose.csv"))
    parser.add_argument("--model", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    train(args.data, args.model, args.report)


if __name__ == "__main__":
    main()
