"""SQLite schema and connection helpers for the demonstration prototype."""

import sqlite3
from contextlib import contextmanager

from app.config import database_path


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def connect() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10, factory=ClosingConnection)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                age INTEGER,
                bmi REAL,
                diabetes_duration_years REAL,
                hba1c REAL,
                is_synthetic INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS readings (
                reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
                timestamp TEXT NOT NULL,
                glucose_mg_dl REAL NOT NULL,
                heart_rate_bpm REAL,
                sleep_hours REAL,
                steps INTEGER,
                source TEXT NOT NULL DEFAULT 'manual',
                source_record_id TEXT,
                is_synthetic INTEGER NOT NULL DEFAULT 0,
                UNIQUE(patient_id, timestamp, source),
                UNIQUE(patient_id, source, source_record_id)
            );
            CREATE INDEX IF NOT EXISTS idx_readings_patient_time
                ON readings(patient_id, timestamp DESC);
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
                prediction_timestamp TEXT NOT NULL,
                input_timestamp TEXT NOT NULL,
                horizon_minutes INTEGER NOT NULL,
                score REAL NOT NULL,
                event_definition TEXT NOT NULL,
                model_version TEXT NOT NULL,
                response_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_predictions_patient_time
                ON predictions(patient_id, prediction_timestamp DESC);
            """
        )


@contextmanager
def transaction():
    connection = connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
