# Architecture Notes

## Runtime Data Flow

1. An operator creates an anonymous profile and submits a timestamped observation through FastAPI. Request schemas enforce expected units/ranges and timezone-aware timestamps.
2. Parameterized SQLite writes persist profile, observation, and optional prediction history. A unique constraint prevents duplicate patient/source timestamps and source record IDs.
3. The patient digital-twin service returns a transparent view of stored static context and dynamic observations. Unknown optional context remains missing.
4. The prediction service loads a trusted joblib model, sorts the patient's latest readings, constructs features from current/past records, and produces an uncalibrated model score. The explanation service adds observed signals, global feature associations, data-quality warnings, and safety notes.
5. FastAPI returns the validated response and persists prediction history to SQLite. The dashboard requests profile, reading, prediction, summary, and evaluation data from the API. The chart plots observed measurements only; no forecast value is portrayed as measured glucose.

## Offline Training Flow

The deterministic generator writes 15-minute trajectories with `is_synthetic=true`. Feature engineering uses current and past records only. Labels look at the next eight observations and rows with incomplete forward windows are dropped. The pipeline rejects irregular sampling intervals. Unique patient IDs are shuffled with a fixed seed into train/validation/test groups. Median imputation and class balancing are fitted/used only within each model's training pipeline. Candidate models are selected by validation PR-AUC. The selected pipeline is evaluated once on the held-out patients at a predeclared 0.5 threshold and serialized with joblib; the report includes class distribution and limitations.

## Boundaries And Safeguards

- No external sensor integration or paid API is present.
- No personal identifiers are collected; anonymous IDs are not a substitute for authentication.
- CORS is off unless explicit origins are configured.
- SQLite, local artifacts, and this unauthenticated API are intended for local educational use.
- `architecture_diagram.svg` is editable source; `architecture_diagram.pdf` is the generated share/print artifact.
