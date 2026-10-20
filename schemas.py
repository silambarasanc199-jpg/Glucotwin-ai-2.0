"""API request/response models and incoming-data validation."""

from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PatientCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age: int | None = Field(default=None, ge=1, le=120)
    bmi: float | None = Field(default=None, ge=10, le=80)
    diabetes_duration_years: float | None = Field(default=None, ge=0, le=100)
    hba1c: float | None = Field(default=None, ge=3, le=20)
    is_synthetic: bool = False


class PatientRead(PatientCreate):
    patient_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReadingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    glucose_mg_dl: float = Field(ge=20, le=600)
    heart_rate_bpm: float | None = Field(default=None, ge=25, le=240)
    sleep_hours: float | None = Field(default=None, ge=0, le=24)
    steps: int | None = Field(default=None, ge=0, le=100000)
    source: Annotated[str, Field(min_length=1, max_length=40)] = "manual"
    source_record_id: Annotated[str | None, Field(default=None, max_length=120)] = None
    is_synthetic: bool = False

    @field_validator("timestamp")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must include a timezone, for example 2026-01-01T09:00:00Z")
        return value.astimezone(timezone.utc)


class ReadingBatch(BaseModel):
    readings: list[ReadingCreate] = Field(min_length=1, max_length=1000)


class ReadingSubmission(ReadingCreate):
    patient_id: str = Field(min_length=1, max_length=100)


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    patient_id: str = Field(min_length=1, max_length=100)


class ReadingRead(ReadingCreate):
    reading_id: int


class PredictionRead(BaseModel):
    patient_id: str
    prediction_timestamp: datetime
    forecast_horizon_minutes: int
    raw_model_score: float
    score_interpretation: str
    uncertainty_note: str
    predicted_event: str
    model_version: str
    latest_input_timestamp: datetime
    synthetic_data: bool
    key_observed_signals: list[str]
    global_model_features: list[dict[str, str | float]]
    data_quality_warnings: list[str]
    explanation: str
    disclaimer: str
