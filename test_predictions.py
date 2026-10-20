import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from app.ml.features import FEATURE_COLUMNS
from app.services import prediction_service
from app.services.prediction_service import load_bundle


def test_missing_model_has_helpful_error(tmp_path, monkeypatch):
    monkeypatch.setenv("GLUCOTWIN_MODEL_PATH", str(tmp_path / "absent.joblib"))
    with pytest.raises(FileNotFoundError, match="python -m app.ml.train"):
        load_bundle()


def test_model_loader_reads_saved_bundle(tmp_path, monkeypatch):
    from joblib import dump

    path = tmp_path / "trained.joblib"
    dump({"model_version": "test-1"}, path)
    monkeypatch.setattr(prediction_service, "model_path", lambda: path)
    assert load_bundle()["model_version"] == "test-1"


def test_prediction_response_has_required_fields_and_uncalibrated_score(client, monkeypatch, tmp_path):
    from app.routes import predictions

    X = pd.DataFrame(np.tile(np.arange(len(FEATURE_COLUMNS), dtype=float), (8, 1)), columns=FEATURE_COLUMNS)
    y = np.array([0, 1] * 4)
    pipeline = Pipeline([("imputer", SimpleImputer(strategy="median", add_indicator=True)),
                         ("model", DummyClassifier(strategy="prior"))]).fit(X, y)
    bundle = {"pipeline": pipeline, "model_name": "test_baseline", "model_version": "test-1",
              "feature_columns": FEATURE_COLUMNS, "horizon_minutes": 120,
              "synthetic_training_data": True}
    monkeypatch.setattr(predictions, "load_bundle", lambda: bundle)
    patient_id = client.post("/api/patients", json={"is_synthetic": True}).json()["patient_id"]
    for index, glucose in enumerate((112, 115, 121, 130)):
        client.post(f"/api/patients/{patient_id}/readings", json={
            "timestamp": f"2026-01-10T12:{index * 15:02d}:00Z", "glucose_mg_dl": glucose,
            "is_synthetic": True,
        })
    response = client.post(f"/api/patients/{patient_id}/predict")
    assert response.status_code == 200
    body = response.json()
    assert body["patient_id"] == patient_id
    assert body["forecast_horizon_minutes"] == 120
    assert 0 <= body["raw_model_score"] <= 1
    assert "uncalibrated" in body["score_interpretation"].lower()
    assert "uncertainty" in body["uncertainty_note"].lower()
    assert body["synthetic_data"] is True
    assert body["disclaimer"]
    assert body["data_quality_warnings"]
    assert client.get(f"/api/patients/{patient_id}/predictions").json()["count"] == 1
