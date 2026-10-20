# GlucoTwin AI 2.0 — Personalized Diabetes Digital Twin

**Happiest Health Digital Twin Challenge 2026** · **Muthayammal Engineering College, Tamil Nadu, India**

GlucoTwin AI 2.0 is a runnable research prototype that stores anonymous patient context and timestamped glucose/wearable observations, builds a transparent patient-specific data view, and serves an experimental estimate of whether glucose will reach a defined threshold within two hours. The project includes a FastAPI + SQLite backend, responsive browser dashboard, leakage-aware scikit-learn pipeline, tests, and submission materials.

> **Safety:** This is not a medical device. It is not clinically validated, does not provide diagnosis or treatment recommendations, and must not be used to make care decisions. The included dataset and demo records are synthetic. Model scores are uncalibrated.

## Team

- Project owner / team leader: **SILAMBARASAN C**
- College: **Muthayammal Engineering College, Tamil Nadu, India**
- Competition: **Happiest Health Digital Twin Challenge 2026**
- Team members: **[TEAM LEADER: add verified member names and roles, or state “Solo project”]**
- Faculty mentor: **[TEAM LEADER: add only if confirmed]**
- Contact details: **[TEAM LEADER: add an approved project contact; do not put private health data here]**

The existing public project README identifies the team leader and college above. Confirm team members, mentor, and contact details with the team before submission; do not invent competition outcomes, partnerships, patient users, or deployment links.

## Problem And Proposed Use Case

Glucose can change over time as meals, activity, sleep, and other factors vary. A retrospective report may not show a timely, person-specific estimate of what could happen next. This prototype links a patient profile to historical observations and a dynamic sensor timeline, then applies a supervised model to estimate a narrowly defined future event. It is designed for technical evaluation and education, not clinical use.

Expected research value is to demonstrate how a digital-twin data model, time-series feature engineering, and an inspectable API/dashboard could be assembled and evaluated. No improvement in patient outcomes is claimed.

## Architecture

![GlucoTwin AI architecture](docs/architecture_diagram.svg)

The diagram is available as editable SVG and `docs/architecture_diagram.pdf`. The dashboard is served by FastAPI at `/`; interactive API documentation is at `/docs`.

```text
Historical profile + timestamped readings + generated synthetic trajectories
                           │
                           ▼
               Validation and preprocessing
                           │
                           ▼
          Patient twin records in SQLite (local)
                           │
                           ▼
  Past-only feature engineering ──► FastAPI prediction service
                           │                    │
            offline patient split               ▼
       train / validation / test       Persisted experimental output
                │                                  │
                ▼                                  ▼
     Logistic / Random Forest                 Responsive dashboard
       selection by validation PR-AUC
```

## Technology

- Python 3.11–3.13; FastAPI, Pydantic, Uvicorn
- SQLite with parameterized SQL and foreign-key enforcement
- Pandas and NumPy for deterministic synthetic data and time-series processing
- scikit-learn pipelines, imputation, class weighting, patient-group holdout, and joblib artifacts
- HTML, CSS, JavaScript, and locally bundled Chart.js 4.4.7 (MIT) for the responsive dashboard
- Pytest and FastAPI TestClient for automated checks
- ReportLab and python-pptx to regenerate presentation assets

The dashboard defaults to same-origin API requests. For a separately hosted static frontend, set `apiBaseUrl` in `app/static/js/config.js` to the deployed FastAPI origin and set `GLUCOTWIN_CORS_ORIGINS` on the backend to the exact frontend origin. No deployment URL is currently configured or claimed.

## Data And Prediction Target

No public or patient dataset was present in the workspace, and no external dataset is included. The included generator creates **36 synthetic profiles × 14 days × 96 readings/day = 48,384 rows** at fixed 15-minute intervals using random seed `20260626`. The deterministic timeline begins at `2025-01-01T00:00:00Z`, so demo records are historical and should trigger freshness warnings rather than appear live. It produces synthetic age, BMI, HbA1c, diabetes duration, glucose, heart rate, sleep, and step-count values. Simplified meal-response pulses, circadian variation, random noise, activity patterns, and demographics are assumptions for software testing only; they are not a validated physiological simulator. All generated rows carry a synthetic marker. Do not present them as observed patient data.

The prototype event label is: **at least one glucose measurement ≥180 mg/dL among the next eight 15-minute measurements (the next 120 minutes)**. The threshold is an explicit project label, not a universal medical standard. The training pipeline rejects non-15-minute sampling intervals rather than silently calling eight irregular samples “two hours.” The API accepts timestamped readings and reports a cadence/freshness warning where the inference context is weak.

Features use only readings at or before prediction time: current glucose, 15-/60-minute glucose changes, 60-minute mean, 120-minute standard deviation, latest heart rate and sleep, 60-minute steps, available BMI/HbA1c, and time of day. Missing values are handled with training-fitted median imputation. Logistic Regression and Random Forest use `class_weight="balanced"` computed by fitting on the training partition only; no class resampling is applied to validation/test. Training labels use future glucose only; incomplete final horizons are removed. Patient identifiers are partitioned into train, validation, and test groups so a synthetic individual cannot appear in multiple partitions.

## Evaluation

The following are the **actual metrics generated by this repository's synthetic-data run** on 2026-10-20, not clinical validation. The model was chosen on validation PR-AUC, then evaluated once on held-out synthetic patients at the unadjusted 0.5 score threshold. `models/evaluation.json` is the generated report; rerunning the pipeline overwrites it with the current environment's run timestamp and results.

| Candidate | Validation PR-AUC | Selection role |
| --- | ---: | --- |
| Majority/prior baseline | 0.2630 | Reference baseline |
| Logistic Regression | 0.6577 | Candidate |
| Random Forest | 0.8548 | Selected by validation PR-AUC |

| Held-out test metric (Random Forest) | Result |
| --- | ---: |
| Precision | 0.7781 |
| Recall | 0.5590 |
| F1 | 0.6506 |
| PR-AUC | 0.7983 |
| ROC-AUC | 0.9339 |
| Confusion matrix `[[TN, FP], [FN, TP]]` | `[[8106, 355], [982, 1245]]` |
| Test samples | 10,688 rows from 8 held-out synthetic profiles |
| Positive / negative support | 2,227 / 8,461 |

These metrics describe a simulated dataset generated from one simplified process. The high ROC-AUC must not be interpreted as expected real-world performance. Synthetic class balance, shared generator assumptions, temporal autocorrelation, the chosen threshold, repeated observations per person, and the small number of held-out profiles limit interpretation. Precision/recall depend on the chosen 0.5 threshold; PR-AUC depends on event prevalence; ROC-AUC measures ranking and not calibration; none establishes utility, safety, or generalization. No clinical validation or probability calibration was performed.

## Installation And Run

From the repository folder:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell (use this instead of the line above)
.venv\Scripts\Activate.ps1
```

Copy `.env.example` to `.env` (optional if you prefer setting environment variables in your shell). The app loads local `.env` values without overriding values already set in the environment.

Install the pinned dependencies and generate the data, model, and explicit demo records:

```bash
python -m pip install -r requirements.txt
python -m app.ml.generate_synthetic_data
python -m app.ml.train
python -m app.ml.evaluate
python -m app.seed_demo
```

Start the application:

```bash
python run.py
```

Open `http://127.0.0.1:8000`. The dashboard loads records and evaluation from the API. Swagger docs: `http://127.0.0.1:8000/docs`; health check: `http://127.0.0.1:8000/health`. SQLite is created on startup. Synthetic records are added only by the separate `python -m app.seed_demo` command. To start with an empty database, remove the local database file after stopping the server; do not place sensitive health data in this prototype.

To reproduce the reported default synthetic run:

```bash
python -m app.ml.generate_synthetic_data --output data/synthetic_glucose.csv --patients 36 --days 14
python -m app.ml.train --data data/synthetic_glucose.csv
python -m app.ml.evaluate
python -m pytest -q
```

Random seed is fixed for data generation and patient-group partitioning. Scikit-learn/NumPy/library changes can still affect numeric results; record package versions with any submitted metric report.

## Dashboard

The browser UI includes backend-driven profile selection and counts, a measured-glucose-only chart, recent sensor rows, optional demographic context, manual reading entry, a prediction control, data freshness/quality notes, model file status, and metrics from `models/evaluation.json`. Empty, loading/error, and no-model states are explicit. No live sensor connection is claimed. Chart.js 4.4.7 is bundled locally under its MIT license; the optional Google font uses a CDN. API, ML, and database functions require no paid API or credential.

`docs/dashboard_synthetic.png` is a real rendered screenshot of the implemented dashboard using clearly synthetic demo records and this run's model evaluation/output. It is a prototype screenshot, not a deployed page or a real-patient result. Preserve its synthetic-data label if reusing it.

## API Routes

All JSON routes use FastAPI validation and clear status codes. Timestamps must include a timezone; glucose is in mg/dL, heart rate in beats/minute, sleep in hours, and steps are counts.

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | Health and database status; model file presence |
| GET | `/api/dashboard/summary` | Stored counts, model/evaluation status, safety notice |
| GET | `/api/patients` | List anonymous patient profiles |
| POST | `/api/patients` | Create profile; optional medical fields may be omitted |
| GET | `/api/patients/{patient_id}` | Profile, recent historical readings, digital-twin summary |
| GET | `/api/patients/{patient_id}/history?limit=5000` | Historical readings (limit 1–10,000) |
| POST | `/api/patients/{patient_id}/readings` | Add one timestamped observation |
| POST | `/api/patients/{patient_id}/readings/batch` | Atomic import of 1–1,000 observations |
| GET | `/api/patients/{patient_id}/readings?limit=500` | Retrieve recent time series |
| POST | `/api/patients/{patient_id}/predict` | Generate and persist experimental two-hour score |
| GET | `/api/patients/{patient_id}/predictions?limit=100` | Retrieve saved outputs |
| POST | `/api/readings` | Add a reading with `patient_id` in the JSON body |
| GET | `/api/predictions?patient_id=...` | List saved predictions, optionally for one patient |
| POST | `/api/predictions` | Generate and persist a prediction using `patient_id` in the JSON body |
| GET | `/docs` | Interactive OpenAPI/Swagger UI |

Duplicate records with the same patient/source timestamp or source record ID return HTTP 409. An unknown patient returns 404; invalid fields/timestamps return 422; prediction before training returns 503 with training instructions. Prediction response includes the event/horizon, raw score interpretation, uncertainty limitation, input timestamp, model version, observed signals, global (not individual causal) model feature ranking, quality warnings, and disclaimer.

Example API smoke test after starting the service and seeding demo records:

```bash
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/api/patients
# Copy a returned patient_id, then:
curl -fsS -X POST http://127.0.0.1:8000/api/patients/DEMO-001/predict
```

## Tests

Run: `python -m pytest -q`. Tests cover health, profile validation/retrieval, reading ingestion and duplicates, timezone/measurement validation, model-missing behavior, prediction response fields/history, top-level workflow routes, frontend assets/configuration, SQLite persistence across application restarts, missing optional features, forward-only labels, and rejection of irregular training cadence.

## Security, Privacy, And Limitations

- This prototype deliberately collects no name, address, email, phone, or medical record number. API-generated identifiers are anonymous IDs, not authentication credentials.
- Validate source data and use only data with permission to process. Never upload identifiable or confidential patient data to this student demonstration.
- `.env.example` contains placeholders only. Local `.env`, databases, generated CSVs, and model artifacts are excluded by `.gitignore`.
- CORS is disabled unless exact origins are set in `GLUCOTWIN_CORS_ORIGINS`; do not use wildcard origins for deployment.
- SQLite is for a local demonstration, not concurrent or regulated production workloads. The app has no user authentication, role-based access, audit logging, encryption-at-rest policy, clinical governance, regulatory review, or production-grade security controls.
- Synthetic observations are not physiological evidence. Model scores are not calibrated probabilities; feature rankings are global associations, not individual causal explanations. The application does not recommend insulin, medication, diet, or treatment action.
- See [`docs/limitations.md`](docs/limitations.md), [`docs/model_card.md`](docs/model_card.md), and [`docs/data_dictionary.md`](docs/data_dictionary.md).

## Deployment

The complete local application is the verified demo path. GitHub Pages can host static files but cannot run FastAPI, perform inference, or persist a SQLite database. A full hosted demo requires a Python-capable service and persistent writable storage. One deployment pattern is a small Render web service with a persistent disk mounted for the SQLite file and model artifact; current pricing, free-tier availability, disk policy, and sleep behavior can change, so check the provider's current plan before relying on it. Set `GLUCOTWIN_DATABASE_PATH`, `GLUCOTWIN_MODEL_PATH`, and `GLUCOTWIN_EVALUATION_PATH` to paths on that persistent disk. Build/start commands: `pip install -r requirements.txt` and `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Generate/train artifacts during a controlled build or upload the generated synthetic artifacts; do not generate demo users implicitly on service startup. Configure `app/static/js/config.js` with the actual API origin in a separately hosted frontend and set `GLUCOTWIN_CORS_ORIGINS` to the exact frontend origin. Confirm `/health`, `/docs`, prediction, and persistence after a restart before sharing any deployment URL. No service has been deployed by this project bundle.

## Submission Materials

- Editable presentation: [`docs/presentation.pptx`](docs/presentation.pptx)
- Presentation PDF: [`docs/presentation.pdf`](docs/presentation.pdf)
- Architecture: [`docs/architecture_diagram.pdf`](docs/architecture_diagram.pdf) and editable [`docs/architecture_diagram.svg`](docs/architecture_diagram.svg)
- 21-minute narration / screen plan (meets the official minimum 20-minute video requirement): [`docs/demo_script.md`](docs/demo_script.md)
- Slide-by-slide content: [`docs/presentation_outline.md`](docs/presentation_outline.md)
- Model card, data dictionary, limitations/ethics: `docs/`
- Video URL: **Not recorded or uploaded.** Follow the timed instructions in `docs/demo_script.md` and add only a real, verified video URL.
- Public repository URL: **Intended:** `https://github.com/silambarasanc199-jpg/GlucoTwin-AI-2.0`. Repository creation and access are not verified yet; do not submit this URL until it opens publicly and contains the checked commit.
- Official challenge rules: [Happiest Health Digital Twin Challenge 2026 on Unstop](https://unstop.com/hackathons/crp-digital-twin-challenge-2026-happiest-health-1757873). The page lists the public-repository, README, architecture PDF/PPT, presentation PDF/PPT, team, and minimum 20-minute prototype-video requirements. Recheck the page before submission in case it changes.

Regenerate the editable assets after modifying slides or the diagram with `python tools/build_submission_assets.py`. To reproduce the numeric synthetic example on slide 13 after a fresh extract, generate the dataset and train the model first; the builder intentionally omits a score if either artifact is missing. See [`docs/github_upload_and_submission.md`](docs/github_upload_and_submission.md) for safe repository creation/push instructions and the Unstop checklist.

## License

MIT License; see [`LICENSE`](LICENSE). The generated synthetic dataset is project-generated and contains no real people. There are no redistributed public dataset files. If you add a public dataset later, check its exact license, terms, and redistribution rules separately before packaging it.

## Future Work

Replace simulated data only with an appropriately licensed, de-identified dataset and independent review; validate timestamp quality and cohort definitions; compare temporal and patient-specific baselines; calibrate and externally validate outputs; quantify uncertainty; investigate subgroup performance and missingness; conduct clinical/ethics review; and add authentication, authorization, auditability, backup, secure deployment, and appropriate governance before any real-world use.
