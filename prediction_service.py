"""Model artifact loading and prototype prediction response assembly."""

from datetime import datetime, timezone

import joblib
import pandas as pd

from app.config import model_path
from app.ml.features import FEATURE_COLUMNS, HORIZON_MINUTES, SPIKE_THRESHOLD_MG_DL, feature_row
from app.services.data_processing import freshness_warning
from app.services.risk_explanations import observed_signals

DISCLAIMER = "Experimental research prototype; not medical advice, diagnosis, treatment, or a clinically validated alert."
EVENT = f"At least one measured glucose value >= {SPIKE_THRESHOLD_MG_DL:g} mg/dL within the next {HORIZON_MINUTES} minutes."


def load_bundle() -> dict:
    path = model_path()
    if not path.exists():
        raise FileNotFoundError(f"Trained model not found at {path}. Generate data and run `python -m app.ml.train` first.")
    return joblib.load(path)


def _global_features(bundle: dict) -> list[dict[str, str | float]]:
    pipeline = bundle["pipeline"]
    model = pipeline.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
    elif hasattr(model, "coef_"):
        importance = abs(model.coef_[0])
    else:
        return []
    imputer = pipeline.named_steps.get("imputer")
    names = list(FEATURE_COLUMNS)
    if imputer is not None and getattr(imputer, "indicator_", None) is not None:
        names.extend(f"missing_{FEATURE_COLUMNS[index]}" for index in imputer.indicator_.features_)
    pairs = sorted(zip(names, importance, strict=False), key=lambda pair: float(pair[1]), reverse=True)[:5]
    return [{"feature": name, "importance": float(value)} for name, value in pairs]


def make_prediction(patient: dict, readings: list[dict], bundle: dict | None = None) -> dict:
    if not readings:
        raise ValueError("At least one glucose reading is required before a prediction can be created.")
    bundle = bundle or load_bundle()
    ordered = sorted(readings, key=lambda item: item["timestamp"])
    latest = ordered[-1]
    features = feature_row(pd.DataFrame(ordered), patient.get("bmi"), patient.get("hba1c"))
    score = float(bundle["pipeline"].predict_proba(features[FEATURE_COLUMNS])[:, 1][0])
    latest_time = datetime.fromisoformat(latest["timestamp"].replace("Z", "+00:00"))
    generated = datetime.now(timezone.utc)
    warnings = []
    if len(ordered) < 8:
        warnings.append(f"Only {len(ordered)} reading(s) are available; training features generally summarize up to 2 hours of history.")
    recent_times = [datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00")) for item in ordered[-8:]]
    if len(recent_times) > 1 and any(
        (right - left).total_seconds() != 15 * 60 for left, right in zip(recent_times, recent_times[1:])
    ):
        warnings.append("Recent reading cadence differs from the model's 15-minute training cadence; lag-derived features may not be comparable.")
    stale = freshness_warning(latest_time, generated)
    if stale:
        warnings.append(stale)
    if bundle.get("synthetic_training_data"):
        warnings.append("The loaded model was trained only on synthetic data; this output has no demonstrated clinical validity.")
    if any(value is None for value in (latest.get("heart_rate_bpm"), latest.get("sleep_hours"), latest.get("steps"))):
        warnings.append("One or more optional sensor fields are missing; the model's training-fitted imputer supplied values.")
    contains_synthetic = bool(patient.get("is_synthetic")) or any(bool(item.get("is_synthetic")) for item in ordered)
    return {
        "patient_id": patient["patient_id"],
        "prediction_timestamp": generated.isoformat().replace("+00:00", "Z"),
        "forecast_horizon_minutes": int(bundle.get("horizon_minutes", HORIZON_MINUTES)),
        "raw_model_score": score,
        "score_interpretation": "Uncalibrated model score, not a calibrated clinical risk or probability.",
        "uncertainty_note": "No calibrated confidence interval or individual-level uncertainty estimate is available.",
        "predicted_event": EVENT,
        "model_version": bundle.get("model_version", "unknown"),
        "latest_input_timestamp": latest["timestamp"],
        "synthetic_data": contains_synthetic,
        "key_observed_signals": observed_signals(ordered),
        "global_model_features": _global_features(bundle),
        "data_quality_warnings": warnings,
        "explanation": "Observed signals summarize the input record. Feature rankings are global model associations, not patient-specific causal explanations.",
        "disclaimer": DISCLAIMER,
    }
