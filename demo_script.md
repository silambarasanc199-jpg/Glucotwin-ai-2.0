# Demonstration Video Script — 21 Minutes

**Recording notes:** Record the actual local application, terminal, API docs, and included architecture/presentation. Start only after the setup steps below complete. Keep the `DEMO-*` label visible. No video has been uploaded. Replace the README's video placeholder only after uploading a real video as unlisted and verifying its URL.

## Before Recording

From the project directory run:

```bash
python -m pip install -r requirements.txt
python -m app.ml.generate_synthetic_data
python -m app.ml.train
python -m app.ml.evaluate
python -m app.seed_demo
python run.py
```

Open `http://127.0.0.1:8000` in a browser. Keep a second terminal ready in the project folder for commands/curl. Optionally open `http://127.0.0.1:8000/docs` in a second tab. Confirm that the patient selected is `DEMO-001` and that the dashboard marks synthetic data. Avoid real patient information.

## Timed Screen And Narration Plan

| Time | Show | Say / Do |
| --- | --- | --- |
| 00:00–01:00 | Title slide | “This is GlucoTwin AI, a diabetes digital-twin proof of concept prepared for the Happiest Health Digital Twin Challenge 2026 by SILAMBARASAN C at Muthayammal Engineering College.” State that all examples are synthetic and the system is not a medical device. |
| 01:00–02:30 | Problem slide | Explain that glucose varies and retrospective summaries may not express a near-term individualized pattern. Avoid claims about avoided events or improved outcomes. |
| 02:30–04:00 | Digital twin slide / dashboard overview | Define this project's twin narrowly: an anonymous profile linked to historical context and timestamped observations, recalculated from new stored readings. It is not a complete physiological simulation. |
| 04:00–05:30 | Dataset section and generator source | Show `app/ml/generate_synthetic_data.py`. State 36 generated profiles, 14 days, 15-minute observations, fixed seed 20260626, and list synthetic glucose, heart rate, steps, sleep, age, BMI, HbA1c, duration assumptions. Explain that no actual patient/public dataset was supplied. |
| 05:30–07:00 | Architecture PDF/SVG | Trace input sources → validation → SQLite digital twin → past-only features → saved model → FastAPI → dashboard. Point out the synthetic-only boundary and local prototype security limitation. |
| 07:00–08:30 | `app/ml/features.py` | Show that features use current/past readings and the label shifts forward eight observations. Describe the ≥180 mg/dL, next-120-minute target as a prototype definition only. Mention irregular training cadence is rejected and incomplete horizons are removed. |
| 08:30–10:00 | Training terminal | Run `python -m app.ml.train` if recording a live repeat, otherwise show its completed output. Explain 21/7/8 patient split, class weighting, imputation pipeline, candidate comparison, validation PR-AUC selection, and no test tuning. |
| 10:00–11:30 | `python -m app.ml.evaluate` and `models/evaluation.json` | Read actual test metrics: precision 0.7781, recall 0.5590, F1 0.6506, PR-AUC 0.7983, ROC-AUC 0.9339, confusion matrix `[[8106,355],[982,1245]]`. Immediately qualify that this is held-out synthetic data from the same generator, not clinical validation. |
| 11:30–13:00 | Swagger UI `/docs` | Expand health, patients, readings, and predict routes. Describe timezone/unit validation, duplicate handling, missing model response, and that the app has no authentication. Do not put personal identifiers into the API. |
| 13:00–14:00 | Terminal/API smoke test | Run `curl -fsS http://127.0.0.1:8000/health` and `curl -fsS http://127.0.0.1:8000/api/patients`. Show the returned `DEMO-001` identifier and `is_synthetic` flag. |
| 14:00–16:30 | Dashboard, desktop | Select `DEMO-001`; inspect available profile context, synthetic badge, measured-only glucose trend, and timeline. Explain that missing static values remain blank and that there is no live sensor connection. |
| 16:30–17:30 | Dashboard entry form | Add one clearly marked synthetic observation or explain its fields without submitting. State that a stored reading is an input, not a prediction. Show stale/missing data warnings if present. |
| 17:30–19:00 | Prediction control | Click “Run experimental prediction.” Read the actual returned raw score, 120-minute horizon, newest input timestamp, event wording, uncertainty note, and synthetic/model warnings. Say “This score is uncalibrated and is not a clinical probability or an alert.” Do not interpret a high/low score as a care action. |
| 19:00–20:00 | Evaluation and global feature area | Explain the metrics are retrieved from backend report, and the feature ranking is global association rather than a patient-specific causal explanation. Note that no confidence interval is available. |
| 20:00–21:00 | Limitations/conclusion slide | Recap no real dataset, no external validation, no calibration, no production security, no deployed live service, and no medical-device claim. Future work needs licensed representative data, ethics/clinical review, subgroup and calibration analysis, security, and external validation. Thank the technical jury. |

## Recording And Upload Instructions

1. Use a screen recorder on a computer or phone that can capture the browser and voice clearly. Keep the browser at readable zoom and hide unrelated notifications.
2. Record 1080p if available; use a quiet room and speak the safety disclaimers plainly. The script is 21 minutes; pause while pages load rather than claiming an action succeeded if it did not.
3. Watch the exported video once. Check sound, visible synthetic labels, privacy, and the final duration (20–22 minutes).
4. Upload to the team's YouTube account. Set visibility to **Unlisted**, not Public or Private, unless competition rules require another setting. Add a factual title/description and do not include personal health data.
5. Open the unlisted URL in a signed-out/private window to verify it plays. Then add that actual URL to `README.md` and the competition form. No upload is included or claimed by this bundle.
