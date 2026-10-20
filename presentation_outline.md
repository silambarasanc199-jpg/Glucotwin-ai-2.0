# Presentation Outline

The editable 15-slide presentation is `presentation.pptx`; PDF export is `presentation.pdf`. Rebuild assets with `python tools/build_submission_assets.py` after editing source text or metrics.

1. **Title and team** — GlucoTwin AI 2.0; team details verified from the existing public project; synthetic-data disclaimer.
2. **Healthcare problem** — glucose varies over time; explain the technical use case without efficacy claims.
3. **Proposed solution** — linked patient record, time-series context, bounded experimental estimate.
4. **Digital-twin workflow** — updateable data representation, not a complete physiological simulation.
5. **Two data streams** — static EHR-style context and timestamped wearable-style readings; all demo data synthetic.
6. **Architecture** — validation, SQLite, training pipeline, model, FastAPI, and responsive dashboard.
7. **Data provenance and ethics** — 36 synthetic profiles, 14 days, fixed seed, assumptions and no real/public data.
8. **Temporal features and target** — past-only inputs and the next-eight-sample, 120-minute event label.
9. **Model methodology** — patient-group split, baseline comparison, training-only preprocessing, validation selection.
10. **Verified evaluation** — latest generated test metrics and limitations from `models/evaluation.json`.
11. **API and persistence** — validated ingestion, stored twin state, prediction history, health and docs endpoints.
12. **Dashboard** — synthetic patient selector, measured trend, timeline, loading/error/empty states, and risk explanation.
13. **Synthetic prediction example** — real output from the current local model, with uncalibrated-score warning.
14. **Limitations and safety** — no clinical validation, calibration, external validation, or production security.
15. **Conclusion and references** — reproducible research prototype; include verified links only.
