# Model Card — GlucoTwin AI 2.0.0

## Summary

- **Model type:** Scikit-learn Random Forest pipeline selected from majority/prior baseline, Logistic Regression, and Random Forest.
- **Selection:** Highest validation PR-AUC; no test-set threshold tuning.
- **Task:** Estimate whether any of the next eight regularly sampled 15-minute glucose readings reaches 180 mg/dL.
- **Intended use:** Demonstrate a reproducible ML pipeline and API/dashboard workflow on synthetic observations.
- **Out-of-scope:** Diagnosis, care decisions, alerts to patients/clinicians, treatment selection, glucose control, and medical-device use.

## Data And Evaluation

The reproducible run on 2026-10-20 uses 48,384 generated readings for 36 synthetic profiles over 14 days (seed 20260626). The patient-level split is 21 train / 7 validation / 8 test profiles. Validation PR-AUC was 0.2630 for the prior baseline, 0.6577 for Logistic Regression, and 0.8548 for Random Forest; Random Forest was selected by validation PR-AUC. On the held-out synthetic test profiles at threshold 0.5, precision was 0.7781, recall 0.5590, F1 0.6506, PR-AUC 0.7983, and ROC-AUC 0.9339; the confusion matrix was `[[8106,355],[982,1245]]` (10,688 rows). See `models/evaluation.json` for the full generated record. These values are synthetic-only and are not clinical performance estimates.

## Inputs

Past/current glucose and derived changes/rolling statistics; recent heart rate, sleep, steps; optional static BMI/HbA1c; encoded time-of-day. Optional fields are imputed using training-fitted medians. At inference, sparse history and stale or missing sensor context generate warnings.

## Limitations, Risks, And Fairness

The data generator is an intentionally simple assumed process, not a physiological simulator or public clinical dataset. Test patients share the same generator as training. There is no external validation, subgroup analysis, calibration, confidence interval, clinical review, prospective evaluation, or utility assessment. Class prevalence, temporal autocorrelation, and one prototype threshold influence reported scores. The UI's raw score is not calibrated risk. Global feature importance is associative and not a patient-level causal explanation. Missingness and device populations in real settings may differ; subgroup fairness is unknown.

## Safe Use

Use only to demonstrate software mechanics with synthetic records. Do not connect it to a real patient, make a clinical claim, or make a care decision. The software is not a medical device and is not clinically validated. Re-evaluate from the beginning with appropriately licensed de-identified data and expert oversight before proposing a clinical study.
