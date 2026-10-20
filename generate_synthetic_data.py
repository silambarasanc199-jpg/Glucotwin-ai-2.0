"""Generate deterministic synthetic multivariate glucose time-series for development."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260626


def generate(output: Path, patients: int = 36, days: int = 14) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    timestamps = pd.date_range("2025-01-01T00:00:00Z", periods=days * 96, freq="15min")
    records: list[dict] = []
    for index in range(patients):
        patient_id = f"SYN-{index + 1:03d}"
        age = int(rng.integers(25, 76))
        bmi = float(np.round(rng.normal(29, 4), 1))
        hba1c = float(np.round(np.clip(rng.normal(7.8, 1.1), 5.8, 11.5), 1))
        baseline = rng.normal(108 + (hba1c - 7) * 5, 8)
        sensitivity = rng.uniform(0.75, 1.3)
        meals: list[tuple[pd.Timestamp, float]] = []
        for day in range(days):
            midnight = timestamps[day * 96]
            for hour, probability in ((8, 0.95), (13, 0.9), (19, 0.95)):
                if rng.random() < probability:
                    meal_time = midnight + pd.Timedelta(hours=hour, minutes=int(rng.integers(-30, 31)))
                    meals.append((meal_time, float(rng.uniform(35, 95) * sensitivity)))
        sleep_by_day = rng.normal(7.1, 0.8, size=days + 1).clip(4.0, 10.0)
        for row_index, timestamp in enumerate(timestamps):
            hour = timestamp.hour + timestamp.minute / 60
            circadian = 4 * np.sin(2 * np.pi * (hour - 5) / 24)
            meal_response = 0.0
            for meal_time, magnitude in meals:
                elapsed = (timestamp - meal_time).total_seconds() / 3600
                if 0 <= elapsed <= 4:
                    peak_hours = 1.15
                    meal_response += magnitude * (elapsed / peak_hours) * np.exp(1 - elapsed / peak_hours)
            glucose = float(np.clip(baseline + circadian + meal_response + rng.normal(0, 5), 65, 360))
            asleep = hour >= 23 or hour < 7
            activity = int(rng.gamma(1.8, 24)) if not asleep else int(rng.gamma(0.3, 5))
            heart_rate = float(np.clip(rng.normal(62 + min(activity, 220) * 0.08, 5), 48, 145))
            records.append({
                "patient_id": patient_id,
                "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "age": age,
                "bmi": bmi,
                "hba1c": hba1c,
                "diabetes_duration_years": float(np.round(rng.uniform(0.2, 24), 1)),
                "glucose_mg_dl": round(glucose, 1),
                "heart_rate_bpm": round(heart_rate, 1),
                "sleep_hours": round(float(sleep_by_day[min(row_index // 96, days)]), 1),
                "steps": activity,
                "source": "synthetic-generator-v1",
                "is_synthetic": True,
            })
    frame = pd.DataFrame.from_records(records)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/synthetic_glucose.csv"))
    parser.add_argument("--patients", type=int, default=36)
    parser.add_argument("--days", type=int, default=14)
    args = parser.parse_args()
    frame = generate(args.output, args.patients, args.days)
    print(f"Generated {len(frame):,} synthetic readings for {frame.patient_id.nunique()} patients at {args.output} (seed={SEED}).")


if __name__ == "__main__":
    main()
