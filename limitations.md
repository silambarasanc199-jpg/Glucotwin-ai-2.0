# Limitations, Ethics, And Safety

## Intended Boundary

GlucoTwin AI is a student research/software prototype. The only included observations are generated synthetic data. It is not a medical device, has no clinical validation, and must not guide diagnosis, treatment, or health decisions. The prediction UI gives no treatment recommendation.

## Data And Label

No project dataset or uploaded records were available during implementation. The simulator approximates simple meal-related glucose pulses, time-of-day variation, noise, activity, and optional demographic context. It omits real physiology, medications, illness, sensor artefacts, nutrition detail, individual treatment response, device calibration, and many social/environmental factors. It must not be described as clinical simulation. The label uses ≥180 mg/dL at any one of the next eight 15-minute samples. This is a project-defined target only, not a universal clinical standard. It assumes exact 15-minute cadence; training rejects irregular intervals.

## Model And Metrics

Patient-group holdout limits direct identity leakage, but the same synthetic generator and assumptions populate all partitions. The high synthetic metrics therefore say little about a different population or a real sensor stream. The sample count is many autocorrelated time points from only 36 generated profiles, not 48,384 independent people. Precision, recall, F1 depend on a fixed 0.5 threshold and event prevalence; PR-AUC depends on prevalence; ROC-AUC evaluates ranking rather than calibration. No calibration, external validation, prospective study, uncertainty interval, subgroup validation, fairness analysis, or clinical utility study exists. Global model feature ranking is not an individual explanation and does not establish causality.

## Privacy And Security

Do not use personal identifiers or real identifiable health data. API IDs are anonymous but there is no authentication or access control. Local SQLite and joblib files are not encrypted. Logging/audit controls, backup/recovery, hardened deployment, and regulatory/privacy compliance are not implemented. CORS can be configured to exact origins but is not access control. Do not expose this app publicly with real health records. Treat joblib artifacts as trusted executable inputs.

## Ethical Next Steps

Obtain data rights and ethics approval before using any human data. De-identify/minimize fields, document provenance and missingness, pre-register a clinically reviewed event definition, independently validate on a representative cohort, assess subgroup performance and calibration, quantify uncertainty, run prospective safety/usability studies, and seek specialist regulatory/security review before any real-world clinical use.
