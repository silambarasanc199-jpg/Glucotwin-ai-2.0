"""Timestamped sensor-reading ingestion and retrieval endpoints."""

import sqlite3

from fastapi import APIRouter, HTTPException, Query

from app.database import connect, transaction
from app.schemas import ReadingBatch, ReadingCreate
from app.services.data_processing import utc_iso

router = APIRouter(prefix="/api/patients/{patient_id}/readings", tags=["sensor readings"])


def _ensure_patient(patient_id: str, connection: sqlite3.Connection) -> None:
    if connection.execute("SELECT 1 FROM patients WHERE patient_id = ?", (patient_id,)).fetchone() is None:
        raise HTTPException(status_code=404, detail="Patient profile not found.")


def _insert(connection: sqlite3.Connection, patient_id: str, reading: ReadingCreate) -> int:
    cursor = connection.execute(
        """INSERT INTO readings
           (patient_id, timestamp, glucose_mg_dl, heart_rate_bpm, sleep_hours, steps, source, source_record_id, is_synthetic)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (patient_id, utc_iso(reading.timestamp), reading.glucose_mg_dl, reading.heart_rate_bpm,
         reading.sleep_hours, reading.steps, reading.source, reading.source_record_id, int(reading.is_synthetic)),
    )
    return int(cursor.lastrowid)


@router.post("", status_code=201)
def add_reading(patient_id: str, payload: ReadingCreate) -> dict:
    try:
        with transaction() as connection:
            _ensure_patient(patient_id, connection)
            reading_id = _insert(connection, patient_id, payload)
            row = connection.execute("SELECT * FROM readings WHERE reading_id = ?", (reading_id,)).fetchone()
    except sqlite3.IntegrityError as error:
        raise HTTPException(status_code=409, detail="A reading with this timestamp/source or source record already exists.") from error
    result = dict(row)
    result["is_synthetic"] = bool(result["is_synthetic"])
    return result


@router.post("/batch", status_code=201)
def import_readings(patient_id: str, payload: ReadingBatch) -> dict:
    try:
        with transaction() as connection:
            _ensure_patient(patient_id, connection)
            ids = [_insert(connection, patient_id, reading) for reading in payload.readings]
            placeholders = ",".join("?" for _ in ids)
            rows = connection.execute(f"SELECT * FROM readings WHERE reading_id IN ({placeholders}) ORDER BY timestamp", ids).fetchall()
    except sqlite3.IntegrityError as error:
        raise HTTPException(status_code=409, detail="Import rejected: duplicate timestamp/source or source record; no rows were saved.") from error
    return {"patient_id": patient_id, "created_count": len(rows), "readings": [dict(row) for row in rows]}


@router.get("")
def list_readings(patient_id: str, limit: int = Query(default=500, ge=1, le=10000)) -> dict:
    with connect() as connection:
        _ensure_patient(patient_id, connection)
        rows = connection.execute(
            "SELECT * FROM readings WHERE patient_id = ? ORDER BY timestamp DESC LIMIT ?",
            (patient_id, limit),
        ).fetchall()
    readings = [dict(row) for row in reversed(rows)]
    for reading in readings:
        reading["is_synthetic"] = bool(reading["is_synthetic"])
    return {"patient_id": patient_id, "readings": readings, "count": len(readings), "limit": limit}
