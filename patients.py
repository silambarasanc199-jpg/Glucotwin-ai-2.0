"""Patient profile and stored-history endpoints."""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.database import connect, transaction
from app.schemas import PatientCreate
from app.services.digital_twin import build_digital_twin

router = APIRouter(prefix="/api/patients", tags=["patients"])


def _patient(row) -> dict:
    result = dict(row)
    result["is_synthetic"] = bool(result["is_synthetic"])
    return result


def _readings(patient_id: str, limit: int = 500) -> list[dict]:
    with connect() as connection:
        rows = connection.execute(
            "SELECT * FROM readings WHERE patient_id = ? ORDER BY timestamp DESC LIMIT ?",
            (patient_id, limit),
        ).fetchall()
    result = [dict(row) for row in reversed(rows)]
    for item in result:
        item["is_synthetic"] = bool(item["is_synthetic"])
    return result


@router.get("")
def list_patients() -> list[dict]:
    with connect() as connection:
        rows = connection.execute("SELECT * FROM patients ORDER BY created_at DESC").fetchall()
    return [_patient(row) for row in rows]


@router.post("", status_code=201)
def create_patient(payload: PatientCreate) -> dict:
    patient_id = f"PT-{uuid4().hex[:10].upper()}"
    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with transaction() as connection:
        connection.execute(
            """INSERT INTO patients (patient_id, age, bmi, diabetes_duration_years, hba1c, is_synthetic, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (patient_id, payload.age, payload.bmi, payload.diabetes_duration_years, payload.hba1c,
             int(payload.is_synthetic), created_at),
        )
        row = connection.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,)).fetchone()
    return _patient(row)


@router.get("/{patient_id}")
def get_patient(patient_id: str) -> dict:
    with connect() as connection:
        row = connection.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,)).fetchone()
        summary = connection.execute(
            """SELECT COUNT(*) AS reading_count, MIN(timestamp) AS first_reading_at,
                      MAX(timestamp) AS latest_reading_at
               FROM readings WHERE patient_id = ?""",
            (patient_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Patient profile not found.")
    recent = _readings(patient_id, limit=200)
    twin = build_digital_twin(_patient(row), recent)
    twin["reading_count"] = summary["reading_count"]
    twin["first_reading_at"] = summary["first_reading_at"]
    twin["latest_reading_at"] = summary["latest_reading_at"]
    twin["latest_reading"] = recent[-1] if recent else None
    twin["historical_readings"] = recent
    twin["history_truncated"] = summary["reading_count"] > 200
    return twin


@router.get("/{patient_id}/history")
def patient_history(patient_id: str, limit: int = 5000) -> dict:
    with connect() as connection:
        exists = connection.execute("SELECT 1 FROM patients WHERE patient_id = ?", (patient_id,)).fetchone()
    if exists is None:
        raise HTTPException(status_code=404, detail="Patient profile not found.")
    if not 1 <= limit <= 10000:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 10000.")
    readings = _readings(patient_id, limit)
    return {"patient_id": patient_id, "readings": readings, "count": len(readings), "limit": limit}
