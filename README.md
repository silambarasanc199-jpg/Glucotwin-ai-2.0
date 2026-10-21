GlucoTwin AI 2.0 — Personalized Diabetes Digital Twin

Happiest Health Digital Twin Challenge 2026
Institution: Muthayammal Engineering College (Autonomous), Tamil Nadu, India
Project Lead: SILAMBARASAN C
Project Category: Healthcare AI · Digital Twin · Machine Learning

<p align="center">
  <strong>Exploring Personalized Glucose-Risk Estimation Through Digital-Twin Concepts</strong>
</p>---

🎥 Project Demonstration Video

Video presentation: "Watch GlucoTwin AI 2.0 on Google Drive" (https://drive.google.com/file/d/170ai6QFzbJGbxn-ZhZommDHR4dnYxPFQ/view?usp=drivesdk)

The video presents the project concept, proposed system architecture, technology stack, synthetic-data workflow, machine-learning methodology, evaluation results, prototype interface, limitations, and future scope.

If the video does not open, check the Google Drive sharing permission. Set access to Anyone with the link — Viewer if permitted by the competition's submission rules.

«Video status: The link has been provided by the project owner. Confirm that the video plays, its duration satisfies the official minimum requirement, and reviewers can access it before final submission.»

---

⚠️ Safety Disclaimer

GlucoTwin AI 2.0 is an experimental research and educational software prototype. It is not a medical device and has not been clinically validated.

- It does not diagnose diabetes or other medical conditions.
- It does not provide treatment, medication, insulin, or dietary recommendations.
- Its model scores are not calibrated clinical probabilities.
- The included demonstration records are synthetic, not real-patient measurements.
- It must not be used to make healthcare decisions.

The reported machine-learning metrics describe experiments on synthetic data only. They do not establish clinical accuracy, patient benefit, or real-world generalisation.

---

📌 Table of Contents

1. "Project Overview" (#-project-overview)
2. "Problem Statement" (#-problem-statement)
3. "Proposed Solution" (#-proposed-solution)
4. "Objectives" (#-objectives)
5. "Team Details" (#-team-details)
6. "Institutional Innovation and IIC" (#-institutional-innovation-and-iic)
7. "Key Features" (#-key-features)
8. "System Architecture" (#-system-architecture)
9. "Technology Stack" (#-technology-stack)
10. "Synthetic Dataset" (#-synthetic-dataset)
11. "Prediction Methodology" (#-prediction-methodology)
12. "Model Evaluation" (#-model-evaluation)
13. "Repository Structure" (#-repository-structure)
14. "Installation and Setup" (#-installation-and-setup)
15. "API Documentation" (#-api-documentation)
16. "Testing" (#-testing)
17. "Privacy, Security and Limitations" (#-privacy-security-and-limitations)
18. "Deployment" (#-deployment)
19. "Competition Submission Materials" (#-competition-submission-materials)
20. "Future Scope" (#-future-scope)
21. "License" (#-license)
22. "Acknowledgements" (#-acknowledgements)

---

🚀 Project Overview

GlucoTwin AI 2.0 is a research-oriented digital-twin prototype that explores how anonymous patient profiles, historical glucose measurements, timestamped observations, and selected wearable-related data can be combined into a machine-learning workflow.

The prototype is designed to demonstrate the technical process of organising historical observations and estimating whether glucose may cross a defined threshold during a future two-hour period.

The system combines:

- A patient-profile and time-series data model.
- Synthetic glucose and wearable-observation generation.
- Historical feature engineering.
- A scikit-learn machine-learning pipeline.
- A FastAPI backend.
- SQLite local persistence.
- A responsive HTML, CSS, and JavaScript dashboard.
- API documentation and automated tests.
- Technical documentation and competition presentation materials.

The project focuses on software architecture, reproducibility, data quality, and responsible interpretation of experimental model outputs.

No improvement in patient outcomes is claimed.

🎯 Problem Statement

Glucose measurements can change over time in association with meals, physical activity, sleep, and other factors.

Historical measurements provide information about previous observations, but a software prototype can also explore how timestamped data and available context may be organised into a forward-looking prediction workflow.

The technical problem addressed by this project is:

How can historical glucose observations and selected health-context features be processed through a transparent digital-twin architecture to estimate a defined future glucose event while making data-quality and model limitations visible?

Important technical considerations include:

- Consistent timestamp handling.
- Missing and irregular observations.
- Prevention of future-data leakage.
- Separation of training, validation, and test data.
- Interpretation of precision, recall, and other evaluation metrics.
- Clear communication of synthetic-data and clinical-validation limitations.

💡 Proposed Solution

GlucoTwin AI 2.0 demonstrates a pipeline that:

1. Creates or receives an anonymous patient profile.
2. Stores timestamped observations.
3. Validates incoming data.
4. Processes historical observations into model features.
5. Uses a trained machine-learning model to estimate a defined future event.
6. Returns an experimental result through an API.
7. Displays available data and model information in a browser dashboard.
8. Communicates data-quality warnings and safety limitations.

The current research configuration uses generated synthetic observations. A live glucose-sensor integration or clinical data connection is not claimed.

🎯 Objectives

- Demonstrate a software-based healthcare digital-twin concept.
- Connect anonymous profiles with timestamped time-series observations.
- Explore historical feature engineering for a future-event prediction task.
- Compare machine-learning candidates using a documented evaluation workflow.
- Provide an API for profile, observation, and prediction operations.
- Visualise historical observations through a browser interface.
- Document synthetic-data assumptions, privacy limitations, and future research requirements.

---

👥 Team Details

Role| Details
Project Lead / Team Leader| SILAMBARASAN C
Team Member| M. Sri Haritha — Data Analyst
Institution| Muthayammal Engineering College (Autonomous)
Programme| Artificial Intelligence and Data Science
Competition| Happiest Health Digital Twin Challenge 2026
Faculty Mentor| Not listed; add only after confirmation
Project Contact| Use an approved public project contact

Team verification: Keep M. Sri Haritha listed only if they are a confirmed member of this specific project team. Ensure that each member's role accurately reflects their contribution. Do not invent mentors, advisors, partnerships, or team members.

---

🏫 Institutional Innovation and IIC

GlucoTwin AI 2.0 is developed in the academic context of Muthayammal Engineering College (Autonomous), located at Kakkaveri, Rasipuram, Namakkal District, Tamil Nadu, India.

Institutional links

- Official college website: https://mec.edu.in/
- Institution's Innovation Council (IIC) page: https://mec.edu.in/institutions-innovation-council/establishment-of-institutions-iic/

The Institution's Innovation Council is part of the college's publicly documented innovation-related institutional ecosystem.

This project is presented as a student research prototype associated with the academic institution. The inclusion of the IIC link provides institutional context; it does not imply that the council has incubated, funded, mentored, approved, or officially endorsed GlucoTwin AI 2.0.

Any formal incubation, mentorship, or institutional support should be added only when independently confirmed.

---

✨ Key Features

1. Anonymous Patient Profiles

Organises profile information under anonymous identifiers rather than requiring names or other direct personal identifiers in the demonstration.

2. Timestamped Observations

Supports the intended workflow for storing glucose readings and selected wearable-related measurements over time.

3. Historical Feature Engineering

Derives features from observations available at or before the prediction timestamp.

4. Experimental Prediction

Uses a trained machine-learning candidate to estimate whether a defined future glucose event occurs within the intended horizon.

5. FastAPI Backend

Provides REST endpoints for the intended profile, observation, dashboard, and prediction workflows.

6. SQLite Persistence

Stores demonstration profiles, readings, and prediction outputs locally.

7. Browser Dashboard

Uses HTML, CSS, JavaScript, and Chart.js to present historical measurements and available model information.

8. Data-Quality Awareness

The intended workflow includes timestamp freshness and sampling-cadence checks so that weak inference contexts can be identified.

9. Model Evaluation

Documents a baseline comparison, validation-based model selection, and held-out synthetic test metrics.

10. Technical Documentation

Includes intended architecture, evaluation, privacy, testing, and competition presentation materials.

---

🏗️ System Architecture

The high-level workflow is:

Synthetic Patient Profiles and Time-Series Observations
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
         Trained Machine-Learning Model
                         |
                         v
               FastAPI Prediction API
                         |
                         v
             Responsive Web Dashboard
                         |
                         v
       Experimental Output and Quality Warnings

Architecture components

Component| Responsibility
Data generator| Produces synthetic profiles and observations
Validation layer| Checks fields, values, and timestamps
SQLite database| Persists local demonstration records
Feature pipeline| Derives historical model inputs
Training pipeline| Trains and evaluates candidate models
Prediction service| Produces experimental model output
FastAPI| Exposes backend functionality through endpoints
Browser dashboard| Presents observations and available results

Architecture diagram

- PDF: "docs/architecture_diagram.pdf"
- Editable SVG: "docs/architecture_diagram.svg"

Confirm that these paths match the actual files in the repository before relying on the links.

---

🛠️ Technology Stack

Technology| Purpose
Python| Backend, data processing, and ML
FastAPI| REST API framework
Pydantic| Request and data validation
Uvicorn| ASGI application server
SQLite| Local relational data storage
Pandas| Tabular and time-series processing
NumPy| Numerical computation
scikit-learn| Model training and evaluation
joblib| Model artifact persistence
HTML| Dashboard structure
CSS| Styling and responsive layout
JavaScript| Frontend behaviour and API requests
Chart.js| Time-series visualisation
pytest| Automated testing
FastAPI TestClient| API testing
ReportLab| PDF asset generation, if configured
python-pptx| PowerPoint generation, if configured

The core local workflow does not require a paid AI API or external generative-AI credentials.

---

📊 Synthetic Dataset

The documented generator configuration is designed to produce:

Parameter| Value
Synthetic profiles| 36
Days per profile| 14
Observations per day| 96
Sampling interval| 15 minutes
Total observations| 48,384
Random seed| "20260626"
Timeline start| "2025-01-01T00:00:00Z"

The generated variables include:

- Glucose.
- Age.
- Body mass index.
- HbA1c.
- Diabetes duration.
- Heart rate.
- Sleep duration.
- Step counts.

The generator uses simplified assumptions for circadian variation, meal-response pulses, activity patterns, demographics, and random noise.

These assumptions exist for software development and testing. They are not a validated physiological simulator.

All generated records must be identified as synthetic. The timeline is historical and must not be presented as live sensor data.

No public or real-patient dataset is claimed as part of the included demonstration.

---

🧠 Prediction Methodology

Prediction target

The experimental target is:

«At least one glucose measurement is greater than or equal to 180 mg/dL among the next eight 15-minute measurements, representing a nominal 120-minute horizon when sampling is regular.»

This is a project-defined label for experimentation. It is not a universal clinical standard or a treatment recommendation.

Historical features

The documented feature set may include:

- Current glucose.
- Glucose change over 15 minutes.
- Glucose change over 60 minutes.
- Mean glucose over the previous 60 minutes.
- Glucose standard deviation over the previous 120 minutes.
- Latest available heart rate.
- Latest available sleep duration.
- Steps over the previous 60 minutes.
- Available BMI and HbA1c.
- Time of day.

Only information available at or before prediction time should be used as model input.

Future glucose observations are used to generate training labels rather than being supplied as prediction-time features. Incomplete future horizons are excluded from training.

The documented pipeline rejects irregular 15-minute training cadence instead of silently treating eight irregular observations as an exact two-hour interval.

Candidate models

- Majority/prior baseline.
- Logistic Regression.
- Random Forest.

The documented pipeline uses training-fitted median imputation and balanced class weights. Candidate selection is based on validation PR-AUC, followed by evaluation on a held-out group of synthetic profiles.

---

📈 Model Evaluation

The following metrics are reported in the project's supplied documentation for a synthetic-data run dated 20 October 2026. They must be checked against the actual generated evaluation report before being treated as verified results.

Validation results

Candidate| Validation PR-AUC| Role
Majority/prior baseline| 0.2630| Reference baseline
Logistic Regression| 0.6577| Candidate
Random Forest| 0.8548| Selected candidate

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

Interpretation

These results are specific to a synthetic dataset generated using one simplified process.

The results do not establish expected real-world performance because:

- Synthetic observations reflect assumptions embedded in the generator.
- Repeated measurements within a profile are temporally correlated.
- Only eight synthetic profiles are reported in the held-out test group.
- Precision and recall depend on the chosen decision threshold.
- PR-AUC depends on event prevalence.
- ROC-AUC evaluates ranking, not probability calibration.
- Independent clinical validation and external-cohort testing have not been performed.

The reported values must not be described as clinically validated accuracy or evidence of improved patient outcomes.

---

📁 Repository Structure

The intended project documentation refers to a structure similar to the following. The actual repository may differ; update this tree to match the committed files.

GlucoTwin-AI-2.0/
├── README.md
├── requirements.txt
├── run.py
├── app/
│   ├── main.py
│   ├── database.py
│   ├── patients.py
│   ├── readings.py
│   ├── predictions.py
│   ├── prediction_service.py
│   ├── schemas.py
│   ├── digital_twin.py
│   ├── data_processing.py
│   ├── features.py
│   ├── risk_explanations.py
│   ├── seed_demo.py
│   ├── ml/
│   │   ├── generate_synthetic_data.py
│   │   ├── train.py
│   │   └── evaluate.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── js/
│           ├── app.js
│           └── config.js
├── data/
├── models/
├── docs/
│   ├── architecture_diagram.pdf
│   ├── architecture_diagram.svg
│   ├── presentation.pdf
│   ├── presentation.pptx
│   ├── presentation_outline.md
│   ├── demo_script.md
│   ├── model_card.md
│   ├── data_dictionary.md
│   ├── limitations.md
│   └── dashboard_synthetic.png
├── tests/
└── LICENSE

Do not create empty folders merely to match this example. Keep the repository tree consistent with the implementation that actually exists.

---

💻 Installation and Setup

Prerequisites

- Python 3.11–3.13, subject to dependency compatibility.
- Git.
- A terminal or command prompt.

1. Clone the repository

Use the verified public repository URL. The URL below is the intended address and should be used only after confirming that the repository exists and is publicly accessible.

git clone https://github.com/silambarasanc199-jpg/Glucotwin-ai-2.0.git
cd Glucotwin-ai-2.0

2. Create a virtual environment

python -m venv .venv

Windows PowerShell:

.venv\Scripts\Activate.ps1

macOS or Linux:

source .venv/bin/activate

3. Install dependencies

python -m pip install -r requirements.txt

4. Generate synthetic data and train the model

The following commands match the documented intended package structure. Run them only if the corresponding modules exist in the actual repository.

python -m app.ml.generate_synthetic_data
python -m app.ml.train
python -m app.ml.evaluate
python -m app.seed_demo

5. Start the application

python run.py

6. Open the local application

- Dashboard: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

If the code uses a different package layout or entry point, update these commands based on the verified implementation.

Synthetic demo records should be created through the explicit seed process rather than being silently inserted on every application startup.

---

🔌 API Documentation

The documented API design includes the following routes. Verify each endpoint against the actual running application before presenting this list as a confirmed API contract.

Method| Endpoint| Purpose
GET| "/health"| Check application, database, and model status
GET| "/api/dashboard/summary"| Retrieve dashboard summary
GET| "/api/patients"| List anonymous profiles
POST| "/api/patients"| Create a profile
GET| "/api/patients/{patient_id}"| Retrieve a profile and summary
GET| "/api/patients/{patient_id}/history"| Retrieve historical observations
POST| "/api/patients/{patient_id}/readings"| Add one timestamped reading
POST| "/api/patients/{patient_id}/readings/batch"| Import a batch of readings
GET| "/api/patients/{patient_id}/readings"| Retrieve recent readings
POST| "/api/patients/{patient_id}/predict"| Generate an experimental prediction
GET| "/api/patients/{patient_id}/predictions"| Retrieve saved predictions
GET| "/docs"| Open interactive Swagger documentation

Expected validation behaviour

The documented design intends to:

- Reject invalid fields or timestamps.
- Return a not-found response for unknown profiles.
- Detect duplicate source records where supported.
- Report a model-unavailable condition when the model is missing.
- Include appropriate quality warnings and safety information in prediction responses.

These behaviours should be confirmed through actual tests before claiming they all work.

---

🧪 Testing

Run the test suite from the repository root:

python -m pytest -q

The documented test coverage includes:

- Health and API workflow checks.
- Profile creation and retrieval.
- Reading validation.
- Timestamp and measurement validation.
- Duplicate detection.
- Prediction response fields and history.
- Missing-model behaviour.
- SQLite persistence.
- Missing optional features.
- Future-label construction.
- Irregular training cadence checks.

Record the actual test result before submitting the project. Do not claim that all tests pass unless the test command 
