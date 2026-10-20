"""Experimental prediction and prediction-history endpoints."""

import json

from fastapi import APIRouter, HTTPException

from app.database import connect, transaction
from app.schemas import PredictionRead
from app.services.prediction_service import load_bundle, make_prediction

router = APIRouter(prefix="/api/patients/{patient_id}", tags=["predictions"])


@router.post("/predict", response_model=PredictionRead)
def predict(patient_id: str) -> dict:
    with connect() as connection:
        patient_row = connection.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,)).fetchone()
        rows = connection.execute(
            "SELECT * FROM readings WHERE patient_id = ? ORDER BY timestamp DESC LIMIT 32", (patient_id,)
        ).fetchall()
    if patient_row is None:
        raise HTTPException(status_code=404, detail="Patient profile not found.")
    if not rows:
        raise HTTPException(status_code=422, detail="Add at least one glucose reading before requesting a prediction.")
    try:
        bundle = load_bundle()
        response = make_prediction(dict(patient_row), [dict(row) for row in reversed(rows)], bundle)
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    with transaction() as connection:
        connection.execute(
            """INSERT INTO predictions
               (patient_id, prediction_timestamp, input_timestamp, horizon_minutes, score, event_definition, model_version, response_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (patient_id, response["prediction_timestamp"], response["latest_input_timestamp"],
             response["forecast_horizon_minutes"], response["raw_model_score"], response["predicted_event"],
             response["model_version"], json.dumps(response)),
        )
    return response


@router.get("/predictions")
def prediction_history(patient_id: str, limit: int = 100) -> dict:
    if not 1 <= limit <= 1000:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 1000.")
    with connect() as connection:
        exists = connection.execute("SELECT 1 FROM patients WHERE patient_id = ?", (patient_id,)).fetchone()
        if exists is None:
            raise HTTPException(status_code=404, detail="Patient profile not found.")
        rows = connection.execute(
            "SELECT response_json FROM predictions WHERE patient_id = ? ORDER BY prediction_timestamp DESC LIMIT ?",
            (patient_id, limit),
        ).fetchall()
    return {"patient_id": patient_id, "predictions": [json.loads(row["response_json"]) for row in rows], "count": len(rows)}
