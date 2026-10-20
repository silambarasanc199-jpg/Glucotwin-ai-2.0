"""Leakage-aware retrospective features and future-horizon training labels."""

from __future__ import annotations

import numpy as np
import pandas as pd

HORIZON_STEPS = 8
HORIZON_MINUTES = 120
SPIKE_THRESHOLD_MG_DL = 180.0
FEATURE_COLUMNS = [
    "glucose_now",
    "glucose_delta_15m",
    "glucose_delta_60m",
    "glucose_mean_60m",
    "glucose_std_120m",
    "heart_rate_bpm",
    "sleep_hours",
    "steps_60m",
    "bmi",
    "hba1c",
    "hour_sin",
    "hour_cos",
]


def feature_row(readings: pd.DataFrame, bmi: float | None = None, hba1c: float | None = None) -> pd.DataFrame:
    """Compute features at the latest timestamp using current and past readings only."""
    if readings.empty:
        raise ValueError("At least one reading is required to create prediction features")
    frame = readings.sort_values("timestamp").reset_index(drop=True)
    glucose = pd.to_numeric(frame["glucose_mg_dl"], errors="coerce")
    if glucose.isna().all():
        raise ValueError("At least one valid glucose measurement is required")
    latest = frame.iloc[-1]
    timestamp = pd.Timestamp(latest["timestamp"])
    values = {
        "glucose_now": glucose.iloc[-1],
        "glucose_delta_15m": glucose.iloc[-1] - glucose.iloc[-2] if len(frame) > 1 else np.nan,
        "glucose_delta_60m": glucose.iloc[-1] - glucose.iloc[-5] if len(frame) > 4 else np.nan,
        "glucose_mean_60m": glucose.tail(4).mean(),
        "glucose_std_120m": glucose.tail(8).std(ddof=0),
        "heart_rate_bpm": pd.to_numeric(frame.get("heart_rate_bpm"), errors="coerce").iloc[-1]
        if "heart_rate_bpm" in frame else np.nan,
        "sleep_hours": pd.to_numeric(frame.get("sleep_hours"), errors="coerce").iloc[-1]
        if "sleep_hours" in frame else np.nan,
        "steps_60m": pd.to_numeric(frame.get("steps"), errors="coerce").tail(4).sum(min_count=1)
        if "steps" in frame else np.nan,
        "bmi": bmi,
        "hba1c": hba1c,
        "hour_sin": np.sin(2 * np.pi * (timestamp.hour + timestamp.minute / 60) / 24),
        "hour_cos": np.cos(2 * np.pi * (timestamp.hour + timestamp.minute / 60) / 24),
    }
    return pd.DataFrame([values], columns=FEATURE_COLUMNS)


def build_training_frame(data: pd.DataFrame) -> pd.DataFrame:
    """Create one row per time point; labels look strictly forward eight 15-min steps."""
    required = {"patient_id", "timestamp", "glucose_mg_dl"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    frame = data.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="raise")
    frame["glucose_mg_dl"] = pd.to_numeric(frame["glucose_mg_dl"], errors="coerce")
    if "steps" not in frame:
        frame["steps"] = np.nan
    for column in ("heart_rate_bpm", "sleep_hours", "bmi", "hba1c"):
        if column not in frame:
            frame[column] = np.nan
    frame = frame.sort_values(["patient_id", "timestamp"]).reset_index(drop=True)
    intervals = frame.groupby("patient_id", sort=False)["timestamp"].diff().dropna()
    if not intervals.eq(pd.Timedelta(minutes=15)).all():
        raise ValueError("Training data must have exactly 15-minute intervals per patient to support the 120-minute target.")
    grouped = frame.groupby("patient_id", sort=False)
    glucose = pd.to_numeric(frame["glucose_mg_dl"], errors="coerce")
    frame["glucose_now"] = glucose
    frame["glucose_delta_15m"] = grouped["glucose_mg_dl"].diff(1)
    frame["glucose_delta_60m"] = grouped["glucose_mg_dl"].diff(4)
    frame["glucose_mean_60m"] = grouped["glucose_mg_dl"].transform(
        lambda values: values.rolling(4, min_periods=1).mean()
    )
    frame["glucose_std_120m"] = grouped["glucose_mg_dl"].transform(
        lambda values: values.rolling(8, min_periods=2).std(ddof=0)
    )
    frame["steps_60m"] = grouped["steps"].transform(lambda values: values.rolling(4, min_periods=1).sum())
    hour = frame["timestamp"].dt.hour + frame["timestamp"].dt.minute / 60
    frame["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    frame["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    future = pd.concat(
        [grouped["glucose_mg_dl"].shift(-step).rename(f"future_{step}") for step in range(1, HORIZON_STEPS + 1)],
        axis=1,
    )
    complete_horizon = future.notna().all(axis=1)
    frame["future_spike"] = (future.max(axis=1) >= SPIKE_THRESHOLD_MG_DL).astype("int8")
    frame = frame.loc[complete_horizon].copy()
    frame[FEATURE_COLUMNS] = frame[FEATURE_COLUMNS].apply(pd.to_numeric, errors="coerce")
    return frame
