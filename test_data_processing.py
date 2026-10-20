import pandas as pd
import pytest
import numpy as np

from app.ml.features import FEATURE_COLUMNS, build_training_frame, feature_row
from app.services.data_processing import utc_iso


def test_utc_iso_requires_timezone_and_normalizes():
    assert utc_iso(pd.Timestamp("2026-01-01T10:00:00+02:00").to_pydatetime()) == "2026-01-01T08:00:00Z"
    with pytest.raises(ValueError):
        utc_iso(pd.Timestamp("2026-01-01T10:00:00").to_pydatetime())


def test_prediction_features_allow_missing_optional_sensors():
    readings = pd.DataFrame([{"timestamp": "2026-01-01T10:00:00Z", "glucose_mg_dl": 125}])
    row = feature_row(readings)
    assert list(row.columns) == FEATURE_COLUMNS
    assert row.loc[0, "glucose_now"] == 125
    assert pd.isna(row.loc[0, "heart_rate_bpm"])
    assert pd.isna(row.loc[0, "hba1c"])


def test_training_label_is_forward_horizon_and_features_are_not_future_values():
    times = pd.date_range("2026-01-01T00:00:00Z", periods=12, freq="15min")
    data = pd.DataFrame({"patient_id": "P1", "timestamp": times,
                         "glucose_mg_dl": [100.0] * 12, "steps": [0] * 12})
    baseline = build_training_frame(data)
    changed = data.copy()
    changed.loc[changed.index == 4, "glucose_mg_dl"] = 210
    with_event = build_training_frame(changed)
    assert baseline.loc[0, "future_spike"] == 0
    assert with_event.loc[0, "future_spike"] == 1
    assert np.allclose(baseline.loc[0, FEATURE_COLUMNS].to_numpy(dtype=float),
                       with_event.loc[0, FEATURE_COLUMNS].to_numpy(dtype=float), equal_nan=True)
    assert not any("future" in column for column in FEATURE_COLUMNS)


def test_training_labels_drop_rows_without_complete_future_window():
    times = pd.date_range("2026-01-01T00:00:00Z", periods=10, freq="15min")
    data = pd.DataFrame({"patient_id": "P1", "timestamp": times,
                         "glucose_mg_dl": [100.0] * 10, "steps": [0] * 10})
    result = build_training_frame(data)
    assert len(result) == 2


def test_training_rejects_irregular_intervals_for_two_hour_label():
    data = pd.DataFrame({"patient_id": ["P1", "P1"],
                         "timestamp": ["2026-01-01T00:00:00Z", "2026-01-01T00:20:00Z"],
                         "glucose_mg_dl": [100.0, 110.0]})
    with pytest.raises(ValueError, match="exactly 15-minute intervals"):
        build_training_frame(data)
