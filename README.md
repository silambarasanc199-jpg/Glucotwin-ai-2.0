GlucoTwin AI 2.0 — Personalized Diabetes Digital Twin

Happiest Health Digital Twin Challenge 2026
Institution: Muthayammal Engineering College (Autonomous), Tamil Nadu, India
Project Lead: SILAMBARASAN C
Project Type: Healthcare AI Research Prototype

GlucoTwin AI 2.0 is an experimental digital-twin research prototype that connects anonymous patient profiles with timestamped glucose and wearable observations. It demonstrates time-series feature engineering, a machine-learning pipeline, a FastAPI backend, SQLite persistence, and a browser-based dashboard to estimate whether glucose may cross a defined threshold within the next two hours.

«Important safety notice: GlucoTwin AI 2.0 is not a medical device and has not been clinically validated. It does not diagnose diabetes, recommend treatment, or support clinical decision-making. The included data is synthetic, and model scores are not calibrated probabilities.»

---

Table of Contents

- "Project Overview" (#project-overview)
- "Problem Statement" (#problem-statement)
- "Proposed Solution" (#proposed-solution)
- "Team Details" (#team-details)
- "Institutional Innovation and IIC" (#institutional-innovation-and-iic)
- "Key Features" (#key-features)
- "System Architecture" (#system-architecture)
- "Technology Stack" (#technology-stack)
- "Synthetic Dataset" (#synthetic-dataset)
- "Prediction Methodology" (#prediction-methodology)
- "Model Evaluation" (#model-evaluation)
- "Installation and Setup" (#installation-and-setup)
- "API Documentation" (#api-documentation)
- "Testing" (#testing)
- "Privacy, Security and Limitations" (#privacy-security-and-limitations)
- "Deployment" (#deployment)
- "Competition Submission Materials" (#competition-submission-materials)
- "Future Scope" (#future-scope)
- "License" (#license)

Project Overview

Glucose levels can vary over time in association with meals, physical activity, sleep, and other factors. This project explores how a software-based digital twin can organize historical observations and estimate a narrowly defined future glucose event.

GlucoTwin AI 2.0 combines:

1. Anonymous patient-profile management.
2. Timestamped glucose and wearable observations.
3. Historical time-series feature engineering.
4. A supervised machine-learning pipeline.
5. A FastAPI prediction service.
6. SQLite-based local persistence.
7. A responsive dashboard for exploring data and experimental outputs.

The project is intended for software demonstration, technical evaluation, and research exploration. It does not claim clinical effectiveness or improved patient outcomes.

Problem Statement

Traditional retrospective reports summarize historical measurements but may not demonstrate how an individual's data could be used in a forward-looking prediction workflow.

The challenge explored by this prototype is:

How can historical health context and timestamped glucose observations be organized into a transparent digital-twin workflow that estimates a defined future glucose event while making data quality, model limitations, and safety constraints visible?

Proposed Solution

GlucoTwin AI 2.0 demonstrates a workflow that:

- Stores anonymous profiles and timestamped observations.
- Validates incoming measurements and timestamps.
- Extracts features using information available at prediction time.
- Trains and evaluates machine-learning candidates using patient-grouped partitions.
- Exposes experimental predictions through a REST API.
- Displays historical observations, model status, quality warnings, and evaluation results through a browser dashboard.

All included demo observations are synthetic. The system does not connect to live glucose sensors or a clinical information system.

Team Details

Role| Details
Project Lead / Team Leader| SILAMBARASAN C
Team Member| M. Sri Haritha — Data Analyst
Institution| Muthayammal Engineering College (Autonomous)
Department / Programme| Artificial Intelligence and Data Science
Competition| Happiest Health Digital Twin Challenge 2026
Faculty Mentor| Not listed; add only after confirmation
Project Contact| Use an approved contact address or the project lead's public profile

Team note: Confirm each member's contribution and role before final submission. If M. Sri Haritha is not a member of this specific project team, remove that entry rather than publishing an inaccurate team list.

Institutional Innovation and IIC

GlucoTwin AI 2.0 is developed in the academic context of Muthayammal Engineering College (Autonomous), Kakkaveri, Rasipuram, Namakkal District, Tamil Nadu, India.

The college maintains an official Institution's Innovation Council (IIC) webpage:

- College website: https://mec.edu.in/
- Official IIC page: https://mec.edu.in/institutions-innovation-council/establishment-of-institutions-iic/
- College address: Kakkaveri, Rasipuram, Namakkal District, Tamil Nadu – 637408, India.

The college's published institutional information describes innovation, research, design thinking, entrepreneurship, and student project development as part of its broader academic activities.

This section identifies the institution's publicly documented innovation ecosystem. It does not claim that GlucoTwin AI 2.0 has received IIC incubation, funding, mentorship, approval, or endorsement. Add those details only if formally confirmed by the institution.

Key Features

- Digital-twin data model: Links anonymous profiles with timestamped observations.
- Time-series processing: Derives historical glucose and wearable features.
- Experimental risk estimation: Predicts a defined future glucose-threshold event.
- FastAPI backend: Provides validated REST endpoints and interactive API documentation.
- SQLite persistence: Stores profiles, readings, and prediction outputs locally.
- Responsive dashboard: Displays profile information, historical measurements, and model status.
- Data-quality warnings: Makes timestamp freshness and sampling-cadence limitations visible.
- Model evaluation: Reports validation and held-out test metrics.
- Automated tests: Covers API workflows, validation, persistence, and model-related behavior.
- Reproducible synthetic data: Uses a fixed generation seed for the documented example.

System Architecture

The prototype follows this high-level workflow:

Synthetic Patient Profiles and Time-Series Readings
                         |
                         v
              Input Validation
                         |
                         v
              SQLite Data Storage
                         |
                         v
          Historical Feature Engineering
                         |
                         v
           Trained ML Prediction Model
                         |
                         v
                FastAPI Service
                         |
                         v
             Responsive Web Dashboard
                         |
                         v
        Experimental Score and Quality Warnings

The model-training workflow is separate from the online prediction workflow. Patient identifiers are divided into training, validation, and test groups to reduce leakage between partitions.

Architecture diagram: "docs/architecture_diagram.pdf"
Editable architecture diagram: "docs/architecture_diagram.svg"

Technology Stack

Component| Technologies
Programming language| Python
Backend API| FastAPI, Pydantic, Uvicorn
Database| SQLite
Data processing| Pandas, NumPy
Machine learning| scikit-learn
Model artifacts| joblib
Frontend| HTML, CSS, JavaScript
Charts| Chart.js
Testing| pytest, FastAPI TestClient
Documentation| Markdown, OpenAPI / Swagger
Presentation generation| ReportLab, python-pptx

Synthetic Dataset

The project generator is configured to create:

- 36 synthetic profiles
- 14 days per profile
- 96 observations per day
- 48,384 total observations
- 15-minute sampling intervals
- Generation seed: "20260626"

The generated timeline begins at "2025-01-01T00:00:00Z". These records are historical synthetic examples, not live readings.

Generated variables include glucose, age, BMI, HbA1c, diabetes duration, heart rate, sleep duration, and step counts. The generator uses simplified assumptions for circadian patterns, meal-response pulses, activity, and noise. It is not a validated physiological simulator.

No real-patient dataset is included in the project.

Prediction Methodology

Prediction target

The model estimates whether at least one glucose observation is 180 mg/dL or higher among the next eight 15-minute measurements, representing a nominal 120-minute horizon when the sampling cadence is regular.

This is a project-defined experimental label, not a universal clinical threshold or a treatment recommendation.

Feature engineering

Features may include:

- Current glucose.
- Glucose change over 15 and 60 minutes.
- Mean glucose over the preceding 60 minutes.
- Glucose standard deviation over the preceding 120 minutes.
- Latest available heart rate and sleep duration.
- Steps recorded over the preceding 60 minutes.
- Available BMI and HbA1c context.
- Time of day.

Only information available at or before prediction time is intended to be used as a feature. Future observations are used to create training labels, not prediction-time inputs. Incomplete future horizons are excluded from training.

Model development

The documented pipeline compares:

- Majority/prior baseline.
- Logistic Regression.
- Random Forest.

The candidates use scikit-learn pipelines with training-fitted median imputation and balanced class weights. Model selection uses validation PR-AUC. The selected model is then evaluated on a held-out group of synthetic patients.

Irregular 15-minute sampling intervals are rejected by the documented training workflow rather than automatically being treated as a regular two-hour horizon.

Model Evaluation

The following values are reported by the project's documented synthetic-data run dated 20 October 2026. They are not evidence of real-world clinical performance.

Validation results

Candidate| Validation PR-AUC
Majority/prior baseline| 0.2630
Logistic Regression| 0.6577
Random Forest| 0.8548

Random Forest was selected using validation PR-AUC.

Held-out synthetic test results

Metric| Reported result
Precision| 0.7781
Recall| 0.5590
F1 score| 0.6506
PR-AUC| 0.7983
ROC-AUC| 0.9339
Test observations| 10,688
Held-out synthetic profiles| 8
Confusion matrix "[[TN, FP], [FN, TP]]"| "[[8106, 355], [982, 1245]]"

These figures must be checked against the actual generated evaluation report before they are used in a competition presentation.

Interpretation and limitations

- The results come from a simplified synthetic-data generator.
- The held-out group contains only eight synthetic profiles.
- Repeated measurements from the same individual are temporally correlated.
- Precision and recall depend on the chosen score threshold.
- PR-AUC depends on the prevalence of the defined event.
- ROC-AUC measures ranking performance, not probability calibration.
- No independent clinical validation, external-cohort validation, or probability calibration has been performed.

These metrics must not be described as clinically validated accuracy or expected patient outcomes.

Installation and Setup

Prerequisites

- Python 3.11–3.13, subject to the compatibility of the pinned dependencies.
- Git.
- A terminal or command prompt.

Clone the repository and enter its directory:

git clone https://github.com/silambarasanc199-jpg/Glucotwin-ai-2.0.git
cd Glucotwin-ai-2.0

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.venv\Scripts\Activate.ps1

On macOS or Linux:

source .venv/bin/activate

Install dependencies:

python -m pip install -r requirements.txt

Generate data and train the model

The commands below match the intended package structure. Run them only after confirming that the corresponding modules exist in the repository:

python -m app.ml.generate_synthetic_data
python -m app.ml.train
python -m app.ml.evaluate
python -m app.seed_demo

Start the server:

python run.py

Open the following local URLs:

- Dashboard: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

If the commands fail because the repository's actual files use a different structure, update this section to match the verified implementation before publishing the final README.

API Documentation

The intended API includes the following endpoints:

Method| Endpoint| Purpose
GET| "/health"| Health and model/database status
GET| "/api/dashboard/summary"| Dashboard summary
GET| "/api/patients"| List anonymous profiles
POST| "/api/patients"| Create a profile
GET| "/api/patients/{patient_id}"| Retrieve a profile and summary
GET| "/api/patients/{patient_id}/history"| Retrieve historical observations
POST| "/api/patients/{patient_id}/readings"| Add one observation
POST| "/api/patients/{patient_id}/readings/batch"| Import multiple observations
GET| "/api/patients/{patient_id}/readings"| Retrieve recent readings
POST| "/api/patients/{patient_id}/predict"| Generate an experimental prediction
GET| "/api/patients/{patient_id}/predictions"| Retrieve saved predictions
GET| "/docs"| Interactive OpenAPI / Swagger documentation

Confirm the implemented routes against the running API before treating this list as a verified API contract. FastAPI validation errors and prediction responses should be documented according to the actual implementation.

Testing

Run the test suite from the repository root:

python -m pytest -q

The intended test coverage includes:

- API health and endpoint workflows.
- Profile creation and retrieval.
- Reading validation and duplicate detection.
- Timestamp and measurement validation.
- Model-missing behavior.
- Prediction response fields and history.
- SQLite persistence.
- Missing optional features.
- Forward-only training labels.
- Rejection of irregular training cadence.

Record the actual test result before submission. Do not claim all tests pass unless the command completes successfully.

Privacy, Security and Limitations

- Demo records are synthetic and must be clearly labelled as such.
- Do not upload identifiable or confidential patient information.
- Anonymous identifiers are not authentication credentials.
- The prototype does not provide production-grade user authentication or role-based access control.
- SQLite is intended for a local demonstration, not a regulated or high-concurrency production service.
- Production deployment would require an appropriate security, privacy, access-control, audit, backup, and governance review.
- Model feature rankings indicate global model associations; they do not establish individual causality.
- Model scores are uncalibrated and must not be interpreted as clinical probabilities.
- The system does not recommend insulin, medication, diet, or other treatment actions.

Additional documentation, if present in the repository:

- "docs/limitations.md"
- "docs/model_card.md"
- "docs/data_dictionary.md"

Deployment

The verified intended demonstration path is local execution. GitHub Pages can host static frontend files but cannot run the FastAPI backend, perform server-side inference, or persist a SQLite database.

A hosted full-stack demo requires a Python-capable hosting service and appropriate persistent storage for the database and model artifacts.

Before sharing a hosted URL, verify:

1. The service starts successfully.
2. "/health" and "/docs" are accessible.
3. The dashboard can call the API.
4. A prediction request completes successfully.
5. Database and model files persist across service restarts.
6. CORS allows only the required frontend origin.
7. No secrets or private health information are exposed.

Deployment status: No hosted deployment is claimed here. Add a public demo URL only after deployment and testing have been completed.

Competition Submission Materials

The following materials are intended for the Happiest Health Digital Twin Challenge 2026. Confirm that each file exists and opens correctly before submission.

Material| Intended file / status
Project README| "README.md"
Architecture diagram| "docs/architecture_diagram.pdf"
Editable architecture diagram| "docs/architecture_diagram.svg"
Editable presentation| "docs/presentation.pptx"
Presentation PDF| "docs/presentation.pdf"
Timed demo and narration script| "docs/demo_script.md"
Slide-by-slide outline| "docs/presentation_outline.md"
Model card| "docs/model_card.md"
Data dictionary| "docs/data_dictionary.md"
Limitations and ethics| "docs/limitations.md"
Demo video| Not recorded or uploaded; add a verified link when available
Hosted application| Not verified; do not claim deployment
Repository| Confirm public access and exact URL before submission

Official challenge information: https://unstop.com/hackathons/crp-digital-twin-challenge-2026-happiest-health-1757873

Recheck the official challenge page for current submission rules and deadlines. A README or presentation does not replace any required video, repository, or submission form.

Future Scope

Potential research directions include:

- Evaluating appropriately licensed, de-identified datasets.
- Independent validation on external cohorts.
- Probability calibration and uncertainty analysis.
- Comparison with temporal and patient-specific baselines.
- Investigation of missingness and subgroup performance.
- Review of data quality and sampling assumptions.
- Appropriate clinical, ethics, and regulatory review.
- Secure authentication, authorization, audit logs, and production-grade data governance.

These are future goals, not completed capabilities.

License

This project is intended to use the MIT License. Confirm that the repository contains the actual "LICENSE" file before claiming that the license is in effect.

---

GlucoTwin AI 2.0
Exploring personalized glucose-risk estimation through digital-twin concepts, time-series data, and machine learning.

Built as a student research prototype at Muthayammal Engineering College for the Happiest Health Digital Twin Challenge 2026.
