# Verification Report

Verified locally on 20 October 2026. The project is a synthetic-data software prototype, not a clinical product.

## Build And Tests

- `python -m compileall -q app tests run.py` — passed.
- `python -m app.ml.generate_synthetic_data` — passed; 48,384 readings across 36 synthetic profiles.
- `python -m app.ml.train` and `python -m app.ml.evaluate` — passed; patient-group holdout (21 train / 7 validation / 8 test profiles).
- `python -m pytest -q` — 22 passed. One Starlette/AnyIO deprecation warning was emitted.
- `node --check app/static/js/app.js` — passed.
- `python -m pip check` — passed; no broken requirements.
- FastAPI smoke checks passed for health, dashboard summary, patient list, prediction creation, and prediction history using temporary SQLite storage.
- Presentation PDF has 15 pages; architecture PDF has 1 page; the editable presentation has 15 slides; the architecture SVG parses as valid XML.
- README local-link check found 12 links and no missing targets.
- High-confidence credential-pattern scan of project source and documentation found no matches. Generated files, caches, and `.venv` were excluded.
- The final ZIP archive passed its integrity check and excludes `.env`, local environments/caches, generated CSV/model files, and SQLite databases.

The workspace's mounted filesystem returned SQLite `database is locked` during direct default-path testing. The API smoke test therefore used temporary SQLite storage; normal persistence on a user's local filesystem is covered by the automated SQLite tests, but the mounted-workspace locking behavior is environment-specific.

## Synthetic Model Results

The selected Random Forest predicts the project-defined event: any of the next eight 15-minute readings reaches 180 mg/dL. At the fixed 0.5 threshold on 10,688 held-out rows from eight synthetic profiles: precision 0.7781, recall 0.5590, F1 0.6506, PR-AUC 0.7983, and ROC-AUC 0.9339. These results are generated from simplified synthetic assumptions and are not clinical performance estimates or individual probabilities.

## Not Completed

- The intended GitHub repository has not been created or pushed because authenticated GitHub access was unavailable. Follow `github_upload_and_submission.md` only after signing into the intended account and confirming the target repository does not already exist.
- No prototype video has been recorded, no deployment is configured, and no external challenge submission has been made.
