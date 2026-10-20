"""Top-level convenience endpoints for reading and prediction workflows."""

import json

from fastapi import APIRouter, HTTPException, Query

from app.database import connect
from app.routes.predictions import predict as predict_patient
from app.routes.sensors import add_reading as add_patient_reading
from app.schemas import PredictionRequest, ReadingCreate, ReadingSubmission

router = APIRouter(prefix="/api", tags=["workflow"])


@router.post("/readings", status_code=201)
def create_reading(payload: ReadingSubmission) -> dict:
    reading = ReadingCreate(**payload.model_dump(exclude={"patient_id"}))
    return add_patient_reading(payload.patient_id, reading)


@router.get("/predictions")
def list_predictions(
    patient_id: str | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
) -> dict:
    with connect() as connection:
        if patient_id is not None:
            exists = connection.execute(
                "SELECT 1 FROM patients WHERE patient_id = ?", (patient_id,)
            ).fetchone()
            if exists is None:
                raise HTTPException(status_code=404, detail="Patient profile not found.")
            rows = connection.execute(
                "SELECT response_json FROM predictions WHERE patient_id = ? "
                "ORDER BY prediction_timestamp DESC LIMIT ?",
                (patient_id, limit),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT response_json FROM predictions "
                "ORDER BY prediction_timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()
    predictions = [json.loads(row["response_json"]) for row in rows]
    return {"predictions": predictions, "count": len(predictions), "limit": limit}


@router.post("/predictions")
def create_prediction(payload: PredictionRequest) -> dict:
    return predict_patient(payload.patient_id)
