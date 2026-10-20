"""Explicitly seed SQLite with two clearly synthetic demo twins from the generated CSV."""

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from app.config import ROOT_DIR
from app.database import init_db, transaction


def seed(data_path: Path) -> int:
    if not data_path.exists():
        raise FileNotFoundError(f"Synthetic dataset missing at {data_path}. Run the synthetic-data generator first.")
    frame = pd.read_csv(data_path)
    if "is_synthetic" not in frame or not frame["is_synthetic"].astype(str).str.lower().isin(["true", "1"]).all():
        raise ValueError("Demo initialization only accepts a dataset explicitly marked synthetic.")
    init_db()
    selected = sorted(frame.patient_id.unique())[:2]
    inserted = 0
    try:
        with transaction() as connection:
            for index, source_patient in enumerate(selected, start=1):
                demo_id = f"DEMO-{index:03d}"
                profile = frame.loc[frame.patient_id == source_patient].iloc[0]
                connection.execute(
                    """INSERT OR IGNORE INTO patients
                       (patient_id, age, bmi, diabetes_duration_years, hba1c, is_synthetic, created_at)
                       VALUES (?, ?, ?, ?, ?, 1, strftime('%Y-%m-%dT%H:%M:%fZ','now'))""",
                    (demo_id, int(profile.age), float(profile.bmi), float(profile.diabetes_duration_years), float(profile.hba1c)),
                )
                patient_rows = frame.loc[frame.patient_id == source_patient]
                for row in patient_rows.itertuples(index=False):
                    cursor = connection.execute(
                        """INSERT OR IGNORE INTO readings
                           (patient_id, timestamp, glucose_mg_dl, heart_rate_bpm, sleep_hours, steps,
                            source, source_record_id, is_synthetic)
                           VALUES (?, ?, ?, ?, ?, ?, 'synthetic-generator-v1', ?, 1)""",
                        (demo_id, row.timestamp, float(row.glucose_mg_dl), float(row.heart_rate_bpm),
                         float(row.sleep_hours), int(row.steps), f"{source_patient}:{row.timestamp}"),
                    )
                    inserted += cursor.rowcount
    except sqlite3.Error:
        raise
    print(f"Demo initialization complete: {len(selected)} synthetic profiles; {inserted} new readings inserted. Safe to rerun.")
    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT_DIR / "data" / "synthetic_glucose.csv")
    args = parser.parse_args()
    seed(args.data)


if __name__ == "__main__":
    main()
