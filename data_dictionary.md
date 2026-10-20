# Data Dictionary

All timestamps are timezone-aware ISO-8601; generated demo CSV uses UTC. API ingestion normalizes time to UTC. Glucose is mg/dL. Generated rows are synthetic and carry `is_synthetic=true`.

| Field | Type / unit | Required | Meaning / handling |
| --- | --- | --- | --- |
| `patient_id` | string | yes | Anonymous stable row grouping ID; generated for API profiles |
| `age` | integer, years | no | Synthetic age or user-provided optional context; range 1–120 |
| `bmi` | decimal, kg/m² | no | Optional static profile context; range 10–80 |
| `diabetes_duration_years` | decimal, years | no | Optional user-provided context; range 0–100 |
| `hba1c` | decimal, % | no | Optional profile context; range 3–20 |
| `timestamp` | ISO-8601 datetime | yes | Observation time; must include timezone |
| `glucose_mg_dl` | decimal, mg/dL | yes | Measured or synthetic glucose observation; range 20–600 in API |
| `heart_rate_bpm` | decimal, beats/minute | no | Optional dynamic wearable context; range 25–240 |
| `sleep_hours` | decimal, hours | no | Optional synthetic/observed daily sleep context; range 0–24 |
| `steps` | integer, count | no | Step count in the observation interval; range 0–100,000 |
| `source` | string | yes, API default | Source label such as `manual` or `synthetic-generator-v1`; not proof of provenance |
| `source_record_id` | string | no | Optional source-level duplicate prevention key |
| `is_synthetic` | boolean | API default false | Explicit marker for demo/synthetic records; never inferred from medical values |
| `glucose_now` | decimal, mg/dL | model feature | Current glucose at prediction time |
| `glucose_delta_15m` | decimal, mg/dL | model feature | Difference from previous 15-minute training row |
| `glucose_delta_60m` | decimal, mg/dL | model feature | Difference from four rows earlier |
| `glucose_mean_60m` | decimal, mg/dL | model feature | Current plus up to three prior rows, trailing mean |
| `glucose_std_120m` | decimal, mg/dL | model feature | Trailing standard deviation over up to eight recent rows |
| `steps_60m` | count | model feature | Trailing sum over current plus up to three prior rows |
| `future_spike` | 0/1 label | training only | Any of the next eight 15-minute values reaches ≥180 mg/dL; never used as an inference feature |
| `raw_model_score` | decimal [0,1] | prediction | Uncalibrated model output; not clinical probability or risk |

Synthetic simulator assumptions and prediction target interpretation are detailed in `README.md` and `limitations.md`.
