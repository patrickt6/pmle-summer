# Training-Serving Skew vs. Feature Attribution Drift

**Audience:** PMLE v3.1 candidates (math-strong, no GCP production experience)
**Exam section:** Section 6 — Monitoring AI solutions (~13% weight)
**Last updated:** 2026-04-24

This is the most commonly conflated concept on the Section 6 portion of the PMLE. The exam loves to swap one for the other in distractors. The single most useful sentence to memorise is at the end of section 5; everything else exists to defend that sentence.

---

## 1. Training-Serving Skew — verbatim definition

> "Training-serving skew occurs when the feature data distribution in production deviates from the feature data distribution used to train the model."
> — Vertex AI Model Monitoring overview, https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview (fetched 2026-04-24)

A second, slightly broader Google framing — useful because the exam uses both:

> "Training-serving skew is a difference between model performance during training and performance during serving. This skew can be caused by: (1) a discrepancy between how you handle data in the training and serving pipelines, (2) a change in the data between when you train and when you serve, (3) a feedback loop between your model and your algorithm."
> — Google Cloud blog, "Monitor models for training-serving skew with Vertex AI", https://cloud.google.com/blog/topics/developers-practitioners/monitor-models-training-serving-skew-vertex-ai (fetched 2026-04-24)

For **feature-attribution skew** specifically:

> "Training-serving skew occurs when a feature's attribution score in production deviates from the feature's attribution score in the original training data."
> — "Monitor feature attribution skew and drift", https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/monitor-explainable-ai (fetched 2026-04-24)

**Key property:** skew is a *static* mismatch between training and production; it can manifest the moment the model is deployed because the reference baseline is the **training dataset**.

---

## 2. Feature Attribution Drift — verbatim definition

> "Inference drift occurs when feature data distribution in production changes significantly over time."
> — Vertex AI Model Monitoring overview, https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview (fetched 2026-04-24)

For attribution specifically:

> "Prediction drift occurs when a feature's attribution score in production changes significantly over time."
> — "Monitor feature attribution skew and drift", https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/monitor-explainable-ai (fetched 2026-04-24)

Why attribution drift exists as a separate concept (this is the answer to "why not just use feature drift?"):

> "Drift scores correspond to impact on predictions. A large change in attribution to a feature by definition means that the feature's contribution to the prediction has changed... large attribution drift is usually indicative of large drift in the model predictions."
> — Google Cloud blog, "Monitoring feature attributions: how Google saved one of the largest ML services in trouble", https://cloud.google.com/blog/topics/developers-practitioners/monitoring-feature-attributions-how-google-saved-one-largest-ml-services-trouble (fetched 2026-04-24)

Feature attribution drift uses Vertex Explainable AI under the hood (Sampled Shapley, Integrated Gradients, XRAI) — see https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/overview (fetched 2026-04-24).

**Key property:** drift is a *temporal* shift; it requires no training data — only a window of production data compared against an earlier window of production data.

---

## 3. Side-by-side comparison

| Aspect | Training-serving skew | Feature attribution drift |
|---|---|---|
| Definition | Production feature distribution (or attribution) deviates from the **training** distribution. | A feature's contribution (attribution score) to predictions changes **significantly over time** in production. |
| Cause | Pipeline mismatch (different code paths for training vs. serving), stale features, transformation bug, feedback loops. | Real-world change in feature/label relationship, upstream data source migration, seasonality, concept drift exposed via attribution shifts. |
| When detected | Can fire on day 1 of deployment — the model has never seen this distribution. | Requires temporal observation; only detectable after enough serving traffic has accumulated. |
| Reference / baseline | The **training dataset** (or a batch-explanation output of it) supplied to the monitoring job. | A **prior production window** (running statistics from earlier serving traffic). No training data needed. |
| Detection method on Vertex AI | Model Monitoring with `TrainingDatasetSpec`; **L-infinity distance** for categorical features, **Jensen-Shannon divergence** for numerical features. Default threshold 0.3 in v1. | Same statistical distances, but applied to **attribution scores** produced by Vertex Explainable AI (Sampled Shapley / Integrated Gradients). |
| Trigger for retraining | Often points to a **bug fix** first (fix the pipeline, rebuild features) before retraining. Retraining alone won't fix a code-path mismatch. | Strong signal for **retraining** with fresh data, because the world (or the feature pipeline output) has changed since training. |
| Example scenario | Training pipeline log-transformed `income` in BigQuery; the online prediction client forgot to apply `log()`. Distribution looks completely different from training on day 1. | A fraud model's `device_fingerprint` attribution silently halved over six weeks because an upstream provider changed its hashing scheme. Raw distribution still looks similar; attribution score collapsed. |

Sources for the comparison row values: Vertex Model Monitoring overview and using-model-monitoring docs (fetched 2026-04-24); Google Cloud blog on attribution drift (June 2024 attribution-drift article cited above).

---

## 4. Vertex AI Model Monitoring v1 vs v2 (2024–2026 changes)

### v1 (Generally Available, the original product)
- Monitoring is attached to a deployed **endpoint**.
- Supports both **training-serving skew** and **prediction drift** for input features.
- Default per-feature threshold is **0.3** (Jensen-Shannon / L-infinity).
- Email alerts on threshold breach. Logs land in BigQuery.
- Sampling rate and monitoring window (min 1 hour, default 24 hours) are configured per endpoint.
- Source: https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/using-model-monitoring (fetched 2026-04-24).

### v2 (announced June 11, 2024; Pre-GA as of April 2026)
- Monitoring attaches to a **specific model version in the Model Registry**, not the endpoint. This decouples monitoring from where the model serves.
- Supports models **outside Vertex AI** (GKE, Cloud Run, GCE, multi-cloud).
- Adds **on-demand jobs** (one-shot analysis against a GCS baseline) plus scheduled continuous jobs.
- Adds **feature attribution drift** as a first-class objective alongside input-feature drift and output-prediction drift. v1 did not have first-class feature attribution monitoring.
- Configured via the Vertex AI SDK class `DataDriftSpec` (categorical metric `l_infinity`, numeric metric `jensen_shannon_divergence`).
- Source: Google Cloud blog "Get to know Vertex AI Model Monitoring", https://cloud.google.com/blog/products/ai-machine-learning/get-to-know-vertex-ai-model-monitoring (June 11, 2024); Vertex AI Model Monitoring overview (fetched 2026-04-24).

**Exam-relevant takeaway:** if a question describes monitoring a model that runs **outside Vertex AI** or asks about **on-demand analysis against a GCS dataset**, the answer is Model Monitoring v2. If a question describes the endpoint-attached default-threshold-0.3 setup with email alerts, it's v1.

---

## 5. The skew-vs-drift mental model — exam cue words

Memorise this one sentence. It resolves ~90% of exam questions on this topic:

> **Skew is *training* vs *production*. Drift is *production* vs *production-yesterday*.**

Cue words that signal **training-serving skew**:

- "On day one after deployment…"
- "The feature transformation in the serving pipeline differs from…"
- "The training data was preprocessed in BigQuery, but the online server…"
- "Compared to the training dataset…"
- "Schema mismatch", "different codebases", "Java service vs Python notebook"
- The scenario provides a **training dataset** (CSV, BigQuery table, GCS path).

Cue words that signal **feature attribution drift** (or input drift):

- "Over the past six weeks…", "gradually degraded over months", "model performance has slowly declined"
- "No training data is available", "we no longer have access to training data"
- "We want to monitor the importance of features without comparing to training"
- "An upstream data provider changed their schema last quarter"
- "Raw feature distributions look similar but the model's accuracy has dropped" → strong signal for **attribution drift** (or concept drift), not raw feature drift.

Tie-breaker between attribution drift and concept drift: if the scenario mentions Vertex Explainable AI, Shapley values, or "feature contribution", it is **attribution drift**. If the scenario mentions only that "labels have changed meaning" or "the relationship between X and y has shifted", it is **concept drift** (which Vertex AI does not directly monitor — you detect it via output performance metrics or by inference from attribution drift).

---

## 6. Sample exam-style questions (JSONL)

```jsonl
{"id": 1, "mode": "single_choice", "question": "A retail forecasting model has just been deployed to a Vertex AI endpoint. The training pipeline applied a log transform to the 'revenue' feature in a BigQuery query, but the online prediction client sends raw revenue values. On day one, the team sees the model returning wildly inaccurate forecasts. Which Vertex AI Model Monitoring objective will most directly surface this issue, and what is the fundamental cause?", "options": ["A. Prediction drift detection; the world has changed since training", "B. Training-serving skew detection; the serving pipeline transforms features differently from the training pipeline", "C. Feature attribution drift detection; the importance of revenue has changed over time", "D. Concept drift detection; the relationship between revenue and forecast has shifted"], "answer": 1, "explanation": "B is correct. The mismatch is between training-time preprocessing (log transform applied) and serving-time preprocessing (raw values), which is the textbook definition of training-serving skew per the Vertex AI Model Monitoring overview. The baseline is the training dataset, and the issue manifests immediately at deployment. A is wrong because drift requires temporal change in production over time; the model is one day old. C is wrong because attribution drift also requires a temporal window and would not be the most direct surface for a pipeline-code mismatch. D is wrong because concept drift is about the X-to-y relationship changing in the world; here the world is unchanged but the code paths disagree.", "ml_topics": ["model monitoring", "training-serving skew", "feature engineering"], "gcp_products": ["Vertex AI Model Monitoring", "BigQuery"], "gcp_topics": ["MLOps", "monitoring"]}
{"id": 2, "mode": "single_choice", "question": "A fraud detection model deployed eight months ago has shown gradually declining precision. The team plots input feature distributions and finds them statistically indistinguishable from training. They suspect a feature provided by a third-party API has silently changed its semantics. Which Vertex AI capability is the BEST first diagnostic?", "options": ["A. Enable training-serving skew detection with the original training set as baseline", "B. Enable Vertex AI Model Monitoring v2 feature attribution drift, comparing recent serving windows", "C. Re-run hyperparameter tuning with Vertex AI Vizier", "D. Increase the monitoring sampling rate to 100% and re-check feature distributions"], "answer": 1, "explanation": "B is correct. Raw input distributions are stable, but model quality has degraded gradually over many months — this is the classic 'attribution drift indicates a change the raw distribution missed' scenario from Google's blog on monitoring feature attributions. v2 supports attribution drift as a first-class objective. A is a trap: skew compares to training data, but the team has already verified raw distributions match training, so skew detection on raw features will return nothing. C addresses model fitness, not data semantics, and burns weeks. D is a trap: increasing sampling on already-matching distributions yields the same null result.", "ml_topics": ["feature attribution drift", "explainable AI", "model monitoring"], "gcp_products": ["Vertex AI Model Monitoring v2", "Vertex Explainable AI"], "gcp_topics": ["MLOps", "monitoring"]}
{"id": 3, "mode": "single_choice", "question": "A Vertex AI Model Monitoring job for a classification endpoint uses default thresholds. Which two statistical distance metrics does Vertex AI use to compare distributions, and which feature type does each cover?", "options": ["A. KL divergence for numerical, chi-squared for categorical", "B. L-infinity distance for categorical, Jensen-Shannon divergence for numerical", "C. Wasserstein distance for both; threshold default 0.5", "D. Cosine similarity for embeddings, L2 norm for tabular"], "answer": 1, "explanation": "B is correct per the Vertex AI Model Monitoring overview and v2 DataDriftSpec: categorical features use L-infinity distance, numerical features use Jensen-Shannon divergence; default per-feature alert threshold is 0.3 in v1. A is a plausible distractor because chi-squared is common in textbooks but Vertex does not use it. C is wrong on both metric and threshold. D is wrong: Vertex Model Monitoring is for tabular features and does not use cosine similarity for input drift.", "ml_topics": ["statistical distance", "distribution drift"], "gcp_products": ["Vertex AI Model Monitoring"], "gcp_topics": ["monitoring"]}
{"id": 4, "mode": "single_choice", "question": "Your team needs to monitor a TensorFlow model that serves predictions from a Cloud Run service backed by GKE — it is NOT deployed to a Vertex AI endpoint. You also want on-demand analysis against a baseline dataset stored in GCS. Which option fits?", "options": ["A. Vertex AI Model Monitoring v1 attached to the GKE pod", "B. Vertex AI Model Monitoring v2 with a Model Monitor registered against the model version in Model Registry", "C. Cloud Monitoring uptime checks with a custom metric for drift", "D. Manually export request logs to BigQuery and run TFDV (TensorFlow Data Validation) nightly"], "answer": 1, "explanation": "B is correct. Vertex AI Model Monitoring v2 (announced June 11, 2024 on the Google Cloud blog) decouples monitoring from Vertex endpoints: a Model Monitor is registered against a model version in the Vertex AI Model Registry and supports on-demand jobs against GCS baselines, including models served outside Vertex AI. A is wrong: v1 monitoring attaches only to Vertex AI endpoints. C is wrong: uptime checks observe availability, not distribution drift. D is technically possible but is exactly the kind of self-managed solution v2 was designed to replace; on a 'best fit' exam question the managed option wins.", "ml_topics": ["model monitoring", "MLOps"], "gcp_products": ["Vertex AI Model Monitoring v2", "Vertex AI Model Registry", "Cloud Run", "GKE"], "gcp_topics": ["monitoring", "deployment"]}
{"id": 5, "mode": "single_choice", "question": "A model monitoring job alerts that the Jensen-Shannon divergence on the 'session_duration' feature has crossed 0.4 (your configured threshold). Investigation reveals the serving feature pipeline computes session_duration in milliseconds, but the training pipeline computed it in seconds. The team asks whether to retrain. What is the BEST next step?", "options": ["A. Immediately retrain on the most recent month of serving data", "B. Fix the unit mismatch in the serving feature pipeline; only retrain if performance does not recover", "C. Lower the threshold to 0.1 and continue monitoring", "D. Disable monitoring for session_duration to suppress the alert"], "answer": 1, "explanation": "B is correct. This is training-serving skew caused by a pipeline implementation discrepancy (units differ between code paths). The Google Cloud blog 'Monitor models for training-serving skew with Vertex AI' explicitly lists 'a discrepancy between how you handle data in the training and serving pipelines' as cause #1. Retraining a model on buggy serving data would bake in the bug. A is wrong because retraining cannot fix a code-path mismatch. C is wrong because lowering the threshold makes the alarm noisier without fixing anything. D is wrong because suppressing the alert hides a real bug.", "ml_topics": ["training-serving skew", "feature engineering", "MLOps"], "gcp_products": ["Vertex AI Model Monitoring"], "gcp_topics": ["monitoring", "retraining"]}
```

---

## 7. Top 5 confusion traps from recent passer writeups

1. **"Skew is over time" — wrong.** Skew is *training vs production*; drift is *production over time*. Several 2024–2026 passer notes call this the most-missed distinction. Source: tjwebb PMLE notes (2024-11-16), https://tjwebb.medium.com/google-professional-machine-learning-engineer-pmle-exam-notes-8948e7748313.

2. **Assuming raw-feature drift detects attribution drift.** A model can have stable input distributions while a feature's contribution to predictions collapses (e.g., upstream provider changes hashing). The Google Cloud blog on attribution drift (https://cloud.google.com/blog/topics/developers-practitioners/monitoring-feature-attributions-how-google-saved-one-largest-ml-services-trouble, fetched 2026-04-24) is the canonical war story.

3. **Confusing concept drift with prediction drift.** "Accuracy dropped but no data drift detected" is the canonical concept-drift trap. ExamCert 2026 study plan (https://www.examcert.app/blog/gcp-ml-engineer-study-plan-2026/, March 21, 2026) explicitly calls this out: "Model accuracy has dropped but there's no data drift detected. The answer? Concept drift — the relationship between features and target has changed, even though the features themselves haven't."

4. **Picking v1 when the scenario has off-Vertex serving.** Several test prep guides note candidates instinctively pick "Vertex AI Model Monitoring" without distinguishing v1 (endpoint-attached) from v2 (Model-Registry-attached, supports external models). If the model runs on Cloud Run, GKE, or another cloud, the answer is v2. Source: Google Cloud blog "Get to know Vertex AI Model Monitoring" (June 11, 2024), https://cloud.google.com/blog/products/ai-machine-learning/get-to-know-vertex-ai-model-monitoring.

5. **Recommending retraining when the real problem is a pipeline bug.** Training-serving skew rooted in code-path differences (units, encodings, transforms) is fixed by *fixing the pipeline*, not by retraining. Retraining on broken serving data propagates the bug. Source: Google Cloud blog "Monitor models for training-serving skew with Vertex AI" (https://cloud.google.com/blog/topics/developers-practitioners/monitor-models-training-serving-skew-vertex-ai, fetched 2026-04-24) — three causes listed; only causes 2 and 3 are addressable by retraining; cause 1 (pipeline discrepancy) is not.

---

## 8. Confidence + Decay risk

**Confidence (high):** The verbatim Google definitions of training-serving skew, prediction drift, and feature attribution skew/drift are stable across 2024–2026 docs. The L-infinity / Jensen-Shannon detection methods and the 0.3 default threshold have been consistent since Model Monitoring's GA. The skew-vs-drift mental model ("training vs production" vs "production over time") is exam-stable.

**Confidence (medium):** Model Monitoring v2 was announced June 11, 2024 and remains Pre-GA as of April 2026 per the Google Cloud documentation fetched today. The PMLE v3.1 exam guide treats both v1 and v2 as fair game; current passer notes confirm v2 questions are appearing.

**Decay risk (watch):**
- **Model Monitoring v2 GA:** if/when v2 reaches GA, exam questions may stop testing v1-specific defaults (the 0.3 threshold, endpoint-attachment). Re-check the Vertex AI release notes (https://docs.cloud.google.com/vertex-ai/docs/core-release-notes) before sitting the exam.
- **Default threshold:** the 0.3 default is a v1 quirk; v2 sample SDK code uses much smaller defaults (e.g., 0.001 / 0.002 in `DataDriftSpec`). Don't memorise 0.3 as universal.
- **Cloud documentation host:** as of April 2026, `cloud.google.com/vertex-ai/docs/...` 301-redirects to `docs.cloud.google.com/...`. Both URLs are cited above; either will serve the same content.
- **Naming churn:** Google has used "prediction drift", "inference drift", "data drift", and "covariate shift" semi-interchangeably across docs. Treat them as synonyms unless the question specifically contrasts them.

**Word count:** ~2,150.
