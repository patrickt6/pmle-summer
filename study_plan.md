# PMLE 12-Week Study Plan

**Source.** Synthesized from the official [v3.1 exam guide](https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf), the closest-match recent passer (V. Narvaez, Feb 2026), and the [Google Skills Professional ML Engineer learning path](https://www.skills.google/paths/17).
**Audience.** Two beginners, math-strong, no prior GCP/ML, studying together.
**Target exam.** PMLE v3.1.
**Total budget.** 60–75 hours per learner (≈58 hr Skills Boost + ~10 hr practice questions + ~5 hr docs/review).
**Time split.** 25 % learning path / 25 % official docs / 50 % practice questions — per V. Narvaez Feb 2026 ([Andrei Paraschiv's PMLE pass writeup (Feb 2026)](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4)).

---

## Constants and rules
- Both partners follow the same week's theme. Falling behind ≥ 2 days → catch-up Sunday.
- Real exam has near-zero multi-select (per recent passer reports). Practice MS questions for concept reinforcement only.
- GenAI weight: ~8–12 % of exam (triangulated). Don't over-weight.
- Vertex AI ↔ Gemini Enterprise Agent Platform: translate function-first when answer-choice names look unfamiliar.
- Exam fee $200 each. Schedule on [Pearson VUE / OnVUE](https://cloud.google.com/learn/certification/machine-learning-engineer) for **Saturday of Week 12** (book in Phase 0).
- Track every measurable goal in the Streamlit app (`pages/1_📅_Weekly_Overview.py` Drill tab + `pages/10_📋_Week_Quizzes.py`).

---

## Daily / weekly routine

### Daily (Mon–Fri)
- **45–60 min** focused study, split:
  - Active learning (video / docs / blog) — ≤ 30 min
  - Active recall (quiz / flashcard / explain-aloud) — ≥ 15 min
- **5-min sync** with partner (Slack / text): "what did you cover, what stuck, what blocked"

### Friday — paired quiz session (30 min)
- Topic-of-week, alternating reader/explainer
- 10–15 questions; both must give answer + reasoning before revealing
- Wrong = mark in Streamlit, drill again Sunday

### Saturday — paired lab session (90 min)
- **Pre-lab (5 min)**: Patrick reads lab description aloud; Matty Boy opens fresh GCP console; agree on success criterion.
- **During lab (90 min)**: switch driver every 30 min; if blocked > 5 min, post in chat and move on.
- **Post-lab (10 min)**: each names ONE "ohhh" insight, paste into the Labs page (`pages/13_🧪_Labs.py`). Run the post-lab 15-Q drill. Mark lab ✅.

### Sunday — retrospective (60 min)
1. Run **Quiz 5A / 5B / 5C** (or current week's letter) on `pages/10_📋_Week_Quizzes.py` — 20-Q timed, 30 min, target ≥ 70 %.
2. Review wrong answers together — explain WHY each correct answer wins.
3. Each partner names: 1 thing learned, 1 stuck-on, 1 ahead-of-plan.
4. Set Monday's first 30-min focus.

---

## Week-by-week summary table

Skills Boost item numbers reference [Google Skills ML Engineer learning path](https://www.skills.google/paths/17). Andy bank topic tags use the existing `gcp_topics` / `ml_topics` / `gcp_products` fields in `gcp-pmle-quiz/data/quizzes.jsonl`. Detailed week sections follow the table.

| Week | Theme | §s | Hours | Skills Boost | Decision-tree refresher | Sunday quiz target | Milestone |
|------|-------|-----|-------|--------------|-------------------------|---------------------|-----------|
| **[1](#week-1--orientation--gcp-fundamentals)** | Orientation + GCP fundamentals | §1.1, §1.2, §2.1 | ~5 | [#1](https://www.skills.google/course_templates/593) | — | Sample form ≥ 35 % cold | Baseline captured |
| **[2](#week-2--bigquery-ml-11)** | §1 BQML | §1.1 | ~3 | [#4](https://www.skills.google/course_templates/626), [#5](https://www.skills.google/course_templates/627) | [BigQuery ML introduction](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) ⭐ | 20 Qs §1.1 ≥ 70 % | First skill badge |
| **[3](#week-3--ml-apis--notebooks-1222)** | §1.2 ML APIs + §2.2 notebooks | §1.2, §2.2 | ~5.25 | [#2](https://www.skills.google/course_templates/631), [#3](https://www.skills.google/course_templates/923) | — | 20 Qs §1.2+§2.2 ≥ 65 % | Workbench notebook published |
| **[4](#week-4--feature-engineering--feature-store-2142)** | §2 Feature engineering + Feature Store | §2.1, §4.2 | ~7.25 | [#6](https://www.skills.google/course_templates/11) ⚠️ | [Vertex AI Feature Store overview](https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview) ⭐ | 20 Qs §2 ≥ 70 % | Pro $29/mo trial begins Day 1 |
| **[5](#week-5--keras-custom-training-3132)** | §3 Custom training (Keras) part 1 | §3.1, §3.2 | ~5.5 | [#7 first half](https://www.skills.google/course_templates/12) | [Vertex AI hyperparameter tuning overview](https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview) ⭐ | 15 Qs §3.1+§3.2 ≥ 65 % | Pair-programmed Keras training notebook |
| **[6](#week-6--keras-finish--hardware-3341)** | §3 finish + §4 hardware | §3.3, §4.1 | ~7 | [#7 finish](https://www.skills.google/course_templates/12), [#10](https://www.skills.google/course_templates/584) | [Vertex AI training compute config](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute) ⭐ | 20 Qs §3.3+§4.1 ≥ 70 % | Multi-worker training run captured |
| **[7](#week-7--production-ml-systems-414243)** | §3 + §4 + §5 production systems | §4.1, §4.2, §4.3 | ~11 | [#8](https://www.skills.google/course_templates/17) | [Vertex AI predictions overview](https://docs.cloud.google.com/vertex-ai/docs/predictions/overview) ⭐ + [IAM overview](https://docs.cloud.google.com/iam/docs/overview) | 25 Qs §4 ≥ 70 % | Endpoint deployed + traffic split |
| **[8](#week-8--pipelines-highest-weight-515253)** | §5 Pipelines (highest weight) | §5.1, §5.2, §5.3 | ~3 | [#15](https://www.skills.google/course_templates/191), [#9](https://www.skills.google/course_templates/158) | [Vertex AI Pipelines introduction](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction) ⭐ + [Vertex AI Experiments intro](https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments) | 25 Qs §5 ≥ 75 % | Vertex AI Pipeline runs end-to-end |
| **[9](#week-9--monitoring--responsible-ai-6162)** | §3+§4 capstone + §6 monitoring | §6.1, §6.2 | ~10.25 | [#16](https://www.skills.google/course_templates/684) | [Vertex AI Model Monitoring overview](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview) ⭐ + [Google AI Principles](https://ai.google/principles/) ⭐ | 20 Qs §6 ≥ 70 % | Capstone + Model Monitoring config |
| **[10](#week-10--genai-sweep-12-23-32)** | GenAI sweep | §1.2, §2.3, §3.2 | ~4.25 | [#11](https://www.skills.google/course_templates/536), [#12](https://www.skills.google/course_templates/539), [#13](https://www.skills.google/course_templates/927), [#14](https://www.skills.google/course_templates/1080) | [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) ⭐ | 25 Qs GenAI tag ≥ 70 % | RAG built in Vertex AI Studio |
| **[11](#week-11--rag-capstone--mock-1-all-sections)** | RAG capstone + **Mock #1** | All | ~6.75 | [#17](https://www.skills.google/course_templates/1120) | All decision trees — rapid review | **Mock #1 ≥ 70 %** (Sat) | Mock #1 score recorded |
| **[12](#week-12--final-review--mock-2--exam-day-all-sections)** | Final review + **Mock #2** + exam day | All | ~6 | [#18](https://www.skills.google/course_templates/985), [#19](https://www.skills.google/course_templates/989) | All decision trees — final review | **Mock #2 ≥ 80 %** (Wed) | **REAL EXAM (Sat)** |

⭐ = high-yield decision-tree refresher (link in the right-hand column). ⚠️ = lab last refreshed 9 mo ago (UI mismatch possible).

---

## How to read each week below

Each week section follows a fixed shape so you can scan it at the same speed every Sunday:

- **🎯 Theme + measurable success.** What you should be able to *do* by Sunday night.
- **📦 Hard deliverables.** The minimum bar for the week to count as "complete." Every item is checkable.
- **🧠 Concept anchors.** The 3–5 things to memorize or be able to explain aloud.
- **📅 Daily breakdown (Mon–Fri).** 45–60 min/day, split active learning + active recall.
- **🧪 Saturday lab.** Specific lab + the paired-session protocol (pre/during/post).
- **📊 Sunday self-assessment.** Specific quiz + score threshold + what to do if below threshold.
- **🚀 Above-and-beyond (optional).** Bonus tasks if you finish early, sorted by ROI.

---

## Week 1 — Orientation + GCP fundamentals
**§s.** §1.1, §1.2, §2.1 · **Hours.** ~5 · **Sat lab.** [#1 Intro to AI & ML on GCP](https://www.skills.google/course_templates/593)

### 🎯 Theme + measurable success
Establish a baseline. By Sunday you should be able to: (a) recite the six v3.1 sections + weights without looking, (b) name three things Vertex AI does, (c) have a *number* (cold sample-form score) you'll compare against in Week 12.

### 📦 Hard deliverables
- [ ] Read [PMLE v3.1 exam guide PDF](professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf) **cover-to-cover** (60 min).
- [ ] Take the [Google free sample form](https://docs.google.com/forms/d/e/1FAIpQLSeYmkCANE81qSBqLW0g2X7RoskBX9yGYQu-m1TtsjMvHabGqg/viewform) **cold** (no prep) — record score.
- [ ] Complete Skills Boost [#1 Intro to AI & ML on GCP](https://www.skills.google/course_templates/593) (~4h).
- [ ] Sign up for [Google Cloud Innovators](https://cloud.google.com/innovators) — confers extra 35 monthly credits.
- [ ] Mark lab #1 complete in `pages/13_🧪_Labs.py`; capture one "ohhh" insight per partner.
- [ ] Open `pages/1_📅_Weekly_Overview.py` and select Week 1 — verify all 5 tabs render.

### 🧠 Concept anchors
- The six v3.1 sections + weights: §1=13%, §2=14%, §3=18%, §4=20%, **§5=22% ⭐**, §6=13%.
- Vertex AI = umbrella for **Pipelines + Training + Model Registry + Endpoints + Feature Store + Experiments + Model Monitoring**. (Pipelines/Training/Registry/Metadata/Experiments names are intact post-rebrand; Agent Builder/Studio/Search were renamed Apr 2026 — see [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder).)
- AutoML vs BQML vs Custom Training: AutoML = no code, BQML = SQL, Custom Training = your TF/PyTorch code.
- Real exam = 60 Qs / 2h / pass ≥ 70%. Near-zero multi-select on the real thing (per [recent passers](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4)).

### 📅 Daily breakdown
- **Mon (60 min).** Read this plan end-to-end. Open the Streamlit app: `cd gcp-pmle-quiz && uv run streamlit run 🏠_Dashboard.py` and switch to **📍 Today** in the sidebar.
- **Tue (60 min).** Read v3.1 exam guide PDF §1–§3 (skim).
- **Wed (60 min).** Read v3.1 exam guide PDF §4–§6 (skim). Skim [Andrei Paraschiv's PMLE pass writeup (Feb 2026)](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4).
- **Thu (60 min).** Take the free sample form *cold*. Record score. Note 5 most-confused questions.
- **Fri (45 min).** Skills Boost [#1](https://www.skills.google/course_templates/593) modules 1–2 with partner.

### 🧪 Saturday lab (90 min paired)
[#1 Intro to AI & ML on GCP](https://www.skills.google/course_templates/593) — finish remaining modules. **Success criterion:** can explain in 2 sentences what each Vertex AI surface does.

### 📊 Sunday self-assessment
- Run **Week 1 Quiz A** (20 Qs from §1.1+§1.2+§2.1) on `pages/10_📋_Week_Quizzes.py`. Target: **≥ 35 %** (this is *baseline week* — low bar).
- If < 35 %: re-read v3.1 exam guide §1–§2 in detail before Week 2.
- Drill the 5 most-confused sample-form questions until you can explain WHY each answer wins.

### 🚀 Above-and-beyond
- 📺 Watch [Google Cloud Tech YouTube — "Decode the Professional ML Engineer Cert"](https://www.youtube.com/results?search_query=google+cloud+professional+machine+learning+engineer+certification) (1h, free, optional).
- 📖 Skim [AndyTheFactory gcp-pmle-quiz repo](https://github.com/AndyTheFactory/gcp-pmle-quiz) — understand the 3-bank stack you'll use.
- 🛠 Free-tier lab: create a Cloud Storage bucket + IAM role binding via console (5–10 min, burns 0 credits, builds GCP muscle memory).

---

## Week 2 — BigQuery ML (§1.1)
**§s.** §1.1 · **Hours.** ~3 · **Sat lab.** [#4 BQML skill badge](https://www.skills.google/course_templates/626)

### 🎯 Theme + measurable success
Internalize the BQML SQL pattern (`CREATE MODEL → ML.PREDICT → ML.EVALUATE`). By Sunday: ≥ 70 % on a 20-Q §1.1 quiz, can write a CREATE MODEL statement from memory for a binary classifier.

### 📦 Hard deliverables
- [ ] Skills Boost [#4 Create ML Models with BQML](https://www.skills.google/course_templates/626) (skill badge).
- [ ] Skills Boost [#5 Engineer Data for Predictive Modeling with BQML](https://www.skills.google/course_templates/627) (skill badge).
- [ ] Read [BigQuery ML introduction](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) ⭐ — focus on the **AutoML scale-to-zero trap** and the BQML vs AutoML decision tree.
- [ ] Mark labs #4 and #5 complete in `pages/13_🧪_Labs.py`.
- [ ] Sunday: 20-Q quiz §1.1 ≥ 70 % via `pages/10_📋_Week_Quizzes.py` Week 2A.

### 🧠 Concept anchors
- BQML model types: `LINEAR_REG`, `LOGISTIC_REG`, `BOOSTED_TREE_*`, `DNN_*`, `KMEANS`, `MATRIX_FACTORIZATION`, `ARIMA_PLUS`, `AUTOML_*`.
- BQML inference goes via **`ML.PREDICT(MODEL ..., (SELECT ...))`** — no model export needed for BQ-resident data.
- **AutoML endpoints cannot scale to zero** — idle classification endpoint ≈ **$991/month**. Common §4 distractor.
- BQML can call Vertex AI for AutoML training under the hood (`MODEL_TYPE='AUTOML_CLASSIFIER'`).
- BQML *exports* to Vertex AI Model Registry, then deploys to a Vertex endpoint for non-BQ inference. Question pattern: "low-latency online prediction outside BQ" → export + Vertex endpoint.

### 📅 Daily breakdown
- **Mon (45 min).** Skim BQML docs: [Introduction to BigQuery ML](https://cloud.google.com/bigquery/docs/bqml-introduction). Watch first SB #4 module.
- **Tue (60 min).** Finish [#4](https://www.skills.google/course_templates/626) videos + run the challenge lab.
- **Wed (45 min).** Read [BigQuery ML introduction](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) — first half.
- **Thu (45 min).** [#5](https://www.skills.google/course_templates/627) entirely.
- **Fri (30 min, paired).** Drill 10 §1.1 questions via Quiz Mode filtered to `BigQuery ML` / `BQML` topic tags.

### 🧪 Saturday lab (90 min paired)
[#4 Create ML Models with BQML](https://www.skills.google/course_templates/626) challenge lab. **Success criterion:** model trained, evaluated, and `ML.PREDICT` returns sane outputs. Capture "ohhh" insight (likely: *the SQL `LABEL` column rename*).

### 📊 Sunday self-assessment
- **Week 2 Quiz A** (20 Qs §1.1) ≥ 70 %.
- If < 70 %: re-watch SB #4 modules 2–3 + redo the lab. Run **Quiz 2B** Monday before bed.
- Wrong-answer drill on `pages/1_📅_Weekly_Overview.py` Drill tab.

### 🚀 Above-and-beyond
- 🛠 Build a toy Kaggle Titanic BQML model (15 min): `CREATE MODEL` with `LOGISTIC_REG`, examine `ML.EVALUATE` output. Public dataset: `bigquery-public-data.ml_datasets.titanic`.
- 📖 Read the [BQML feature engineering best practices](https://cloud.google.com/bigquery/docs/preprocess-overview) doc — preview of Week 4.
- ⭐ **High-yield bonus:** drill the [BigQuery ML introduction](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) decision tree until you can recite the AutoML / BQML / Vertex Custom Training selection rules in under 60 seconds.

---

## Week 3 — ML APIs + Notebooks (§1.2, §2.2)
**§s.** §1.2, §2.2 · **Hours.** ~5.25 · **Sat lab.** [#3 Working with Notebooks in Vertex AI](https://www.skills.google/course_templates/923)

### 🎯 Theme + measurable success
Recognize when "use the pre-trained ML API" beats "train your own." Know the Workbench/Colab Enterprise/Dataproc trio cold. By Sunday: ≥ 65 % on a 20-Q §1.2+§2.2 quiz.

### 📦 Hard deliverables
- [ ] Skills Boost [#2 Prepare Data for ML APIs](https://www.skills.google/course_templates/631) (skill badge, ~45 min).
- [ ] Skills Boost [#3 Working with Notebooks in Vertex AI](https://www.skills.google/course_templates/923) (~4.5h).
- [ ] Skim [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) — focus on the **Apr 22 2026 rebrand** (Vertex AI Search → Agent Search; Vertex AI Studio → Agent Platform Studio; Vertex AI Agent Builder → Gemini Enterprise Agent Platform).
- [ ] Mark labs #2 and #3 complete; capture one "ohhh" insight each.

### 🧠 Concept anchors
- **ML API picker:** Document AI (forms/contracts) · Vision API (general images) · Translation API · Speech-to-Text · Natural Language API · Retail API · Healthcare API · Recommendations AI.
- **Pre-trained API vs custom training:** if generic + you need it tomorrow → API. If domain-specific → AutoML or custom training.
- **Workbench** (managed Vertex notebooks, full IDE) vs **Colab Enterprise** (managed, free/fast) vs **Dataproc** (Spark/Hadoop).
- **Vector Search** (formerly Matching Engine, renamed Aug 2023) — ScaNN-based ANN store for embeddings, key §1.2 GenAI piece.
- The **Apr 22, 2026 rebrand** is *surface-only* — APIs and IDs unchanged. Function-first translation when reading questions.

### 📅 Daily breakdown
- **Mon (45 min).** Watch [#2](https://www.skills.google/course_templates/631) videos.
- **Tue (60 min).** Run the [#2](https://www.skills.google/course_templates/631) challenge lab.
- **Wed (60 min).** [#3](https://www.skills.google/course_templates/923) modules 1–3.
- **Thu (60 min).** [#3](https://www.skills.google/course_templates/923) modules 4–end + the lab.
- **Fri (30 min, paired).** Quiz Mode filtered to `ML APIs` / `Vertex AI Workbench` / `Colab Enterprise` topic tags — 10 Qs.

### 🧪 Saturday lab (90 min paired)
[#3 Working with Notebooks in Vertex AI](https://www.skills.google/course_templates/923) — finish if not done by Friday. **Success criterion:** Workbench instance running, can launch a kernel, can connect to BQ from a notebook cell.

### 📊 Sunday self-assessment
- **Week 3 Quiz A** (20 Qs §1.2+§2.2) ≥ 65 %.
- §2.2 has only 7 questions in scope so the sampler will fall back to §1.2; expect mostly ML-API + GenAI tags.
- Wrong-answer drill via Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Run a Vision API request from a Colab Enterprise notebook (free quota covers 1k req/mo).
- 📖 Read the [Vector Search overview](https://cloud.google.com/vertex-ai/docs/vector-search/overview) — the §1.2 GenAI bullet that question banks under-cover.
- ⭐ Quiz Mode on the **`Document AI`** tag — high-yield distractor in §1.2.

---

## Week 4 — Feature engineering + Feature Store (§2.1, §4.2)
**§s.** §2.1, §4.2 · **Hours.** ~7.25 · **Sat lab.** [#6 Feature Engineering](https://www.skills.google/course_templates/11) ⚠️

### 🎯 Theme + measurable success
Understand when Feature Store earns its keep vs plain Cloud Storage / BQ. Memorize the **Feb 17 2027 sunset** for Legacy + Optimized online serving. By Sunday: ≥ 70 % on a 20-Q §2 quiz.

**Trial timing.** Pro $29/mo subscription **starts Day 1** — covers Weeks 4–12 (3 months × $29 = $87). Set a calendar reminder on **Day 6** to decide cancel-or-keep before auto-renewal.

### 📦 Hard deliverables
- [ ] Skills Boost [#6 Feature Engineering](https://www.skills.google/course_templates/11) (~7.25h). UI may show legacy Vertex names — concepts are still correct.
- [ ] Read [Vertex AI Feature Store overview](https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview) ⭐ end-to-end — note the **Feb 17 2027** sunset and **Bigtable online serving** as the safe exam answer.
- [ ] Start Pro subscription at [skills.google/payments/new](https://www.skills.google/payments/new). Set Day 6 calendar reminder.
- [ ] Mark lab #6 complete; capture one "ohhh" insight.

### 🧠 Concept anchors
- **Feature Store decision tree.** Cloud Storage = static blobs. BQ = analytical features. Feature Store = online + offline serving with point-in-time correctness.
- **Sunset.** Legacy Feature Store + Optimized online serving sunset **Feb 17, 2027**. Bigtable online serving = the safe exam answer.
- **Point-in-time correctness** — joining feature values *as-of* event time, prevents training-serving skew on time-traveled features.
- **Streaming ingestion** — Pub/Sub → Dataflow → Feature Store streaming write API (use SDK, not BQ batch).
- §4.2 connection: Feature Store is queried from a Vertex Endpoint at inference time → online feature serving.

### 📅 Daily breakdown
- **Mon (60 min).** [#6](https://www.skills.google/course_templates/11) modules 1–2 (BigQuery feature ops).
- **Tue (75 min).** [#6](https://www.skills.google/course_templates/11) modules 3–4 (Dataflow + TFT).
- **Wed (75 min).** [#6](https://www.skills.google/course_templates/11) modules 5–6 (Feature Store).
- **Thu (75 min).** [#6](https://www.skills.google/course_templates/11) finish + read [Vertex AI Feature Store overview](https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview).
- **Fri (30 min, paired).** Quiz Mode filtered to `Feature Store` / `Dataflow` / `feature engineering` — 10 Qs.

### 🧪 Saturday lab (90 min paired)
[#6 Feature Engineering](https://www.skills.google/course_templates/11) capstone lab. **Success criterion:** feature created, written, served from Feature Store online endpoint.

### 📊 Sunday self-assessment
- **Week 4 Quiz A** (20 Qs §2) ≥ 70 %.
- Wrong-answer drill on Weekly Overview Week 4.
- 5-min recap aloud: "When would I pick Feature Store over BQ?" (Should answer: online + low-latency + point-in-time correctness.)

### 🚀 Above-and-beyond
- 🛠 Stand up a streaming feature pipeline: Pub/Sub → Dataflow → Feature Store. The [Feature Store streaming ingestion codelab](https://cloud.google.com/vertex-ai/docs/featurestore/serving-online) is the cheapest hands-on.
- 📖 Read [Vertex AI Feature Store: streaming ingestion](https://cloud.google.com/vertex-ai/docs/featurestore/setup) — directly tested in §2.1.
- ⭐ Quiz Mode on **`Dataflow`** + **`pub/sub`** tags — §2.1 ETL is heavily tested.

---

## Week 5 — Keras custom training (§3.1, §3.2)
**§s.** §3.1, §3.2 · **Hours.** ~5.5 · **Sat lab.** [#7 Build, Train, Deploy ML Models with Keras](https://www.skills.google/course_templates/12) (first half)

### 🎯 Theme + measurable success
Run a Keras custom training job on Vertex AI. Tune one hyperparameter via **Vizier**. By Sunday: ≥ 65 % on a 15-Q §3.1+§3.2 quiz.

### 📦 Hard deliverables
- [ ] Skills Boost [#7 Keras](https://www.skills.google/course_templates/12) **first half** (~5.5h).
- [ ] Read [Vertex AI hyperparameter tuning overview](https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview) ⭐ — focus on Vizier algorithms (Bayesian, Random, Grid) + budgeting (parallel vs sequential trials).
- [ ] Pair-program **one** custom training notebook from #7 — both partners type half each.
- [ ] Mark lab #7 (in_progress) in `pages/13_🧪_Labs.py`.

### 🧠 Concept anchors
- **`CustomTrainingJob`** vs **`HyperparameterTuningJob`**: latter wraps the former with a Vizier StudySpec.
- Vizier = the tuning service; **same StudySpec** for AutoML and custom training. Algorithm = Bayesian (default), Random, or Grid.
- **Trial parallelism** — `parallelTrialCount` × `maxTrialCount`; parallel trials don't share state, so high parallelism + Bayesian = degraded learning.
- **Reduction Server** (preview here, deep-dive Week 6) — Vertex-only NCCL all-reduce, **75% throughput uplift** on multi-GPU training.
- **Gemini SFT = LoRA-based PEFT** — adapter sizes 1/2/4/8/16; only 2.5 Pro/Flash/Flash-Lite tunable; Pro maxes at adapter 8.

### 📅 Daily breakdown
- **Mon (60 min).** [#7](https://www.skills.google/course_templates/12) modules 1–2 (TF/Keras refresh).
- **Tue (60 min).** [#7](https://www.skills.google/course_templates/12) module 3 (Vertex AI Training).
- **Wed (60 min).** [#7](https://www.skills.google/course_templates/12) module 4 (HyperparameterTuningJob) + read [Vertex AI hyperparameter tuning overview](https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview).
- **Thu (60 min).** Pair-program a custom training notebook — partner A types, partner B reads. Switch at 30 min.
- **Fri (30 min, paired).** Quiz Mode filtered to `custom training` / `hyperparameter tuning` / `vizier` — 10 Qs.

### 🧪 Saturday lab (90 min paired)
[#7 Keras](https://www.skills.google/course_templates/12) — first-half lab. **Success criterion:** custom training job submitted, completes, model artifact in GCS.

### 📊 Sunday self-assessment
- **Week 5 Quiz A** (15 Qs §3.1+§3.2) ≥ 65 %.
- Each partner: explain the Vizier StudySpec aloud in 60 seconds.
- Wrong-answer drill on Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Run a tiny `HyperparameterTuningJob` on a synthetic dataset (Iris) with `n_trials=4`, see Vizier in action.
- 📖 Read [Vertex AI Vizier overview](https://cloud.google.com/vertex-ai/docs/vizier/overview).
- ⭐ Skim [Vertex AI training compute config](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute) Week 6 prep — **Reduction Server** is the highest-yield distinguishing topic on the entire exam.

---

## Week 6 — Keras finish + hardware (§3.3, §4.1)
**§s.** §3.3, §4.1 · **Hours.** ~7 · **Sat lab.** [#7 Keras](https://www.skills.google/course_templates/12) (finish) + multi-worker training

### 🎯 Theme + measurable success
Pick the right compute (CPU/GPU/TPU/Reduction Server). Deploy a Keras model to a Vertex Endpoint and call it. By Sunday: ≥ 70 % on a 20-Q §3.3+§4.1 quiz.

### 📦 Hard deliverables
- [ ] Finish Skills Boost [#7 Keras](https://www.skills.google/course_templates/12).
- [ ] Skills Boost [#10 MLOps Manage Features](https://www.skills.google/course_templates/584) (~1.75h).
- [ ] Read [Vertex AI training compute config](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute) ⭐ end-to-end. **The Reduction Server one-liner = the single highest-yield exam fact.**
- [ ] Mark labs #7 and #10 complete; capture two "ohhh" insights.

### 🧠 Concept anchors
- **CPU** = small models, debugging, batch inference. **GPU** = >50M params, dense matmul. **TPU** = TF/JAX, dense, large batch. **Reduction Server** = NCCL all-reduce on Vertex GPUs only, **+75% throughput, no code changes**.
- TPU machine types on Vertex: `ct5lp-hightpu-{1t,4t,8t}` (v5e), `ct6e-standard` (v6e). v5e/v5p/v6e are safe bets.
- **Distributed training strategies.** `MirroredStrategy` (single host multi-GPU) · `MultiWorkerMirroredStrategy` (multi-host) · `TPUStrategy` · `ParameterServerStrategy` (legacy, avoid in answers).
- **Horovod** = open-source equivalent to `MultiWorkerMirroredStrategy`; on Vertex you can swap to Reduction Server for the +75% bump.
- §4.1 connection: a trained model → Vertex Endpoint → online prediction (or batch prediction job for offline scoring).

### 📅 Daily breakdown
- **Mon (60 min).** [#7](https://www.skills.google/course_templates/12) modules 5–6 (distributed training).
- **Tue (60 min).** [#7](https://www.skills.google/course_templates/12) modules 7–end + endpoint deployment.
- **Wed (60 min).** [#10](https://www.skills.google/course_templates/584) entirely.
- **Thu (60 min).** Read [Vertex AI training compute config](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute). Drill the GPU/TPU/RS selection rules.
- **Fri (30 min, paired).** Quiz Mode filtered to `GPU` / `TPU` / `Reduction Server` / `distributed training` / `endpoint` — 10 Qs.

### 🧪 Saturday lab (90 min paired)
[#7 Keras](https://www.skills.google/course_templates/12) finish — multi-worker training run. **Success criterion:** training job completes with `MultiWorkerMirroredStrategy`; can read training logs in Cloud Logging.

### 📊 Sunday self-assessment
- **Week 6 Quiz A** (20 Qs §3.3+§4.1) ≥ 70 %.
- Each partner: cold-quiz "When do I pick Reduction Server?" — answer should mention NCCL, GPU-only, no code changes, +75%.
- Wrong-answer drill via Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Modify the Saturday training job to add Reduction Server: declare `reducerReplicaCount` + `reducerMachineType` in the [training job spec](https://cloud.google.com/vertex-ai/docs/training/distributed-training#reduction-server). Verify throughput in logs.
- 📖 Read [Reduction Server algorithm overview](https://cloud.google.com/vertex-ai/docs/training/distributed-training#reduction-server) directly.
- ⭐ Drill **`Horovod`** tag — common §3.3 distractor (Horovod is OSS; Reduction Server is Vertex-only).

---

## Week 7 — Production ML systems (§4.1, §4.2, §4.3)
**§s.** §4.1, §4.2, §4.3 · **Hours.** ~11 · **Sat lab.** [#8 Production ML Systems](https://www.skills.google/course_templates/17) capstone

### 🎯 Theme + measurable success
Master batch vs online inference, A/B testing, traffic splitting, public vs private endpoints. By Sunday: ≥ 70 % on a 25-Q §4 quiz.

### 📦 Hard deliverables
- [ ] Skills Boost [#8 Production ML Systems](https://www.skills.google/course_templates/17) (~11h, the longest course of the path).
- [ ] Read [Vertex AI predictions overview](https://docs.cloud.google.com/vertex-ai/docs/predictions/overview) ⭐ + [IAM overview](https://docs.cloud.google.com/iam/docs/overview).
- [ ] Deploy a model to a Vertex Endpoint with **traffic split** (e.g., 80/20) — paired session.
- [ ] Mark lab #8 complete; capture two "ohhh" insights.

### 🧠 Concept anchors
- **Batch vs online prediction.** Batch = scheduled, BQ output, no endpoint. Online = HTTP, low latency, requires deployed endpoint.
- **A/B testing.** Deploy 2 models to *one* endpoint with a `trafficSplit`. Caveat: Vertex AI doesn't compare metrics for you — you wire that via Model Monitoring.
- **Public vs private endpoints.** Private = via PSC (Private Service Connect) inside your VPC; needed for VPC-SC compliance.
- **Throughput tuning.** `min_replica_count` + `max_replica_count` + `autoscaling_metric_specs`. AutoML endpoints **cannot scale to zero** — idle ≈ $991/mo.
- **Model Registry** is the canonical surface for model versions. Endpoints reference Registry version IDs.
- **IAM cross-cut.** Service accounts for training jobs vs prediction. Workload Identity for GKE-side training. VPC-SC perimeters around Vertex resources.

### 📅 Daily breakdown
- **Mon (90 min).** [#8](https://www.skills.google/course_templates/17) modules 1–2 (architecture).
- **Tue (90 min).** [#8](https://www.skills.google/course_templates/17) modules 3–4 (serving).
- **Wed (90 min).** [#8](https://www.skills.google/course_templates/17) modules 5–6 (batch vs online).
- **Thu (90 min).** [#8](https://www.skills.google/course_templates/17) modules 7–8 (security + monitoring intro).
- **Fri (60 min, paired).** Quiz Mode filtered to `endpoint` / `model registry` / `A/B testing` / `private endpoint` — 15 Qs.

### 🧪 Saturday lab (120 min paired — extra 30 min for capstone scope)
[#8 Production ML Systems](https://www.skills.google/course_templates/17) end-of-course lab. **Success criterion:** model deployed to endpoint with 80/20 traffic split, online prediction succeeds via curl.

### 📊 Sunday self-assessment
- **Week 7 Quiz A** (25 Qs §4) ≥ 70 %.
- Each partner: explain *out loud* the difference between Vertex AI Endpoint, Vertex Model Registry, and Cloud Run prediction. Why pick which?
- Wrong-answer drill via Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Set up a private endpoint with PSC — extra 30 min on top of the Saturday lab.
- 📖 Read [Vertex AI prediction overview](https://cloud.google.com/vertex-ai/docs/predictions/overview) + [private endpoints](https://cloud.google.com/vertex-ai/docs/predictions/using-private-endpoints).
- ⭐ Drill **`Private Service Connect`** + **`VPC service controls`** — §4.3 distractors that hide behind generic "make it private" question wording.

---

## Week 8 — Pipelines (highest weight, §5.1, §5.2, §5.3)
**§s.** §5.1, §5.2, §5.3 · **Hours.** ~3 (light reading week — pipelines is short on Skills Boost but **22 % of exam**) · **Sat lab.** [#15 ML Pipelines on GCP](https://www.skills.google/course_templates/191)

### 🎯 Theme + measurable success
Pick the right orchestrator (Vertex AI Pipelines vs Cloud Composer vs Kubeflow on GKE vs MLFlow vs TFX). Track an experiment with **Vertex AI Experiments** + **ML Metadata**. By Sunday: ≥ 75 % on a 25-Q §5 quiz (highest-weight section, push the threshold up).

### 📦 Hard deliverables
- [ ] Skills Boost [#15 ML Pipelines on GCP](https://www.skills.google/course_templates/191) (~2.25h).
- [ ] Skills Boost [#9 MLOps Getting Started](https://www.skills.google/course_templates/158) (~45 min).
- [ ] Read [Vertex AI Pipelines introduction](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction) ⭐ — **the orchestrator cost lever** (Vertex Pipelines $0.03/run vs Composer $400/mo floor) is the single biggest §5 question driver.
- [ ] Read [Vertex AI Experiments intro](https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments) — Experiments + ML Metadata are the §5.3 anchors.
- [ ] Run **one** end-to-end Vertex AI Pipeline (the SB lab covers it).
- [ ] Mark labs #9 and #15 complete; capture two "ohhh" insights.

### 🧠 Concept anchors
- **Vertex AI Pipelines** = serverless KFP runner. **$0.03/run + compute**, no idle cost. Default pick.
- **Cloud Composer 3** = managed Airflow. **$0.06/DCU-hr × ~$400/mo floor** on the smallest env. Pick when you need cron, multi-system orchestration, or heavy non-ML scheduling.
- **Kubeflow Pipelines on GKE** = self-managed, when you need exotic configs or multi-cloud.
- **MLFlow** = experiment tracking + model registry alternative. On GCP, default to Vertex AI Experiments + Model Registry instead.
- **TFX** = TF-only pipeline framework, components run on Vertex AI Pipelines or KFP. Heavy in [#15](https://www.skills.google/course_templates/191), still tested.
- **Vertex AI Experiments** tracks runs, metrics, params. **ML Metadata** tracks artifacts + lineage. Ask: "I want to compare 5 training runs" → Experiments.
- **CI/CD for ML.** Cloud Build → Vertex Pipeline trigger. Cloud Source Repos. Artifact Registry. Jenkins (legacy answer, avoid).

### 📅 Daily breakdown
- **Mon (45 min).** [#9](https://www.skills.google/course_templates/158) entirely (45 min).
- **Tue (60 min).** [#15](https://www.skills.google/course_templates/191) modules 1–2.
- **Wed (60 min).** [#15](https://www.skills.google/course_templates/191) modules 3–end + the lab.
- **Thu (60 min).** Read [Vertex AI Pipelines introduction](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction) + [Vertex AI Experiments intro](https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments).
- **Fri (30 min, paired).** Quiz Mode filtered to `Vertex AI Pipelines` / `Kubeflow Pipelines` / `Cloud Composer` / `TFX` / `Vertex AI Experiments` — 15 Qs.

### 🧪 Saturday lab (90 min paired)
[#15 ML Pipelines on GCP](https://www.skills.google/course_templates/191) end-to-end lab. **Success criterion:** KFP pipeline runs on Vertex AI Pipelines, output artifacts visible in ML Metadata.

### 📊 Sunday self-assessment
- **Week 8 Quiz A** (25 Qs §5) ≥ **75 %** (higher bar — §5 is the biggest weight).
- Each partner: explain "Vertex AI Pipelines vs Cloud Composer" in 60 seconds, citing the cost numbers.
- Wrong-answer drill via Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Add a `KFP @component` for data validation to the Saturday pipeline.
- 📖 Read [KFP v2 SDK reference](https://www.kubeflow.org/docs/components/pipelines/) — the v2 syntax shows up in `kfp.v2.dsl.component` answer choices.
- ⭐ **High-yield bonus:** drill the [Vertex AI Pipelines introduction](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction) cost numbers until you can recite them. Single biggest input to §5 question answers.
- ⭐ Add experiment runs in Vertex AI Experiments → compare metrics in the UI.

---

## Week 9 — Monitoring + Responsible AI (§6.1, §6.2)
**§s.** §6.1, §6.2 · **Hours.** ~10.25 · **Sat lab.** [#16 Build and Deploy ML Solutions on Vertex AI](https://www.skills.google/course_templates/684) (capstone)

### 🎯 Theme + measurable success
Memorize the **skew-vs-drift one-liner** verbatim. Configure a Model Monitoring v2 job. Cite the **Apr 2026 Explainable AI deprecation**. By Sunday: ≥ 70 % on a 20-Q §6 quiz.

### 📦 Hard deliverables
- [ ] Skills Boost [#16 Build and Deploy ML Solutions on Vertex AI](https://www.skills.google/course_templates/684) (~8.25h, capstone).
- [ ] Read [Vertex AI Model Monitoring overview](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview) ⭐ — memorize the one-liner: **"Skew is training vs production. Drift is production vs production-yesterday."**
- [ ] Read [Google AI Principles](https://ai.google/principles/) ⭐ — note Vertex Explainable AI **deprecated Mar 16 2026**, shutdown Mar 16 2027. Still tested in v3.1.
- [ ] Configure one Vertex AI Model Monitoring v2 job (in the SB lab).
- [ ] Mark lab #16 complete; capture two "ohhh" insights.

### 🧠 Concept anchors
- **Skew vs drift one-liner.** "Skew is training vs production. Drift is production vs production-yesterday." Memorize verbatim.
- **Model Monitoring v1 vs v2.** v2 announced Jun 11 2024, **still Pre-GA Apr 2026**. Both fair game on exam. v2 attaches to Model Registry version (not endpoint), supports off-Vertex models, on-demand jobs, attribution drift as first-class objective.
- **v1 default drift threshold = 0.3.** v2 examples use much smaller defaults — don't over-memorize 0.3.
- **Explainable AI methods.** Sampled Shapley (default for tabular), Integrated Gradients (NN), XRAI (image). Deprecated Mar 16 2026 but **still tested in v3.1**.
- **Responsible AI.** Fairness metrics (demographic parity, equal opportunity), bias mitigation, model cards, human-in-the-loop review.
- **Security.** DLP API for PII redaction. CMEK for encryption keys. Prompt injection mitigations. VPC-SC for data-exfil prevention.

### 📅 Daily breakdown
- **Mon (90 min).** [#16](https://www.skills.google/course_templates/684) modules 1–2.
- **Tue (90 min).** [#16](https://www.skills.google/course_templates/684) modules 3–4.
- **Wed (90 min).** [#16](https://www.skills.google/course_templates/684) modules 5–6 + read [Vertex AI Model Monitoring overview](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview).
- **Thu (90 min).** Read [Google AI Principles](https://ai.google/principles/). Drill the deprecation timeline.
- **Fri (60 min, paired).** Quiz Mode filtered to `Model Monitoring` / `drift` / `skew` / `Explainable AI` / `Responsible AI` — 15 Qs.

### 🧪 Saturday lab (120 min paired — capstone is heavy)
[#16 Build and Deploy ML Solutions on Vertex AI](https://www.skills.google/course_templates/684) capstone challenge lab. **Success criterion:** AutoML or custom-trained model deployed + Model Monitoring v2 job configured against it.

### 📊 Sunday self-assessment
- **Week 9 Quiz A** (20 Qs §6) ≥ 70 %.
- Each partner: recite the skew-vs-drift one-liner cold. If either misses, do it 5× before bed.
- Wrong-answer drill via Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Configure a Sampled Shapley explanation on the Saturday endpoint, get back attributions for one prediction.
- 📖 Read [Vertex AI Model Monitoring v2 overview](https://cloud.google.com/vertex-ai/docs/model-monitoring/overview-v2).
- ⭐ Drill the **`feature attribution drift`** tag — net-new in Model Monitoring v2 and a likely v3.1 question.
- ⭐ Skim **§4 + §3** wrong-answer drill — Weeks 5–7 content fades fast.

---

## Week 10 — GenAI sweep (§1.2, §2.3, §3.2)
**§s.** §1.2, §2.3, §3.2 · **Hours.** ~4.25 · **Sat lab.** RAG warm-up — preview of Week 11 [#17](https://www.skills.google/course_templates/1120)

### 🎯 Theme + measurable success
Cover the v3.1 GenAI surface in one focused week. Know Model Garden, Agent Builder (now Gemini Enterprise Agent Platform), RAG, fine-tuning paths, eval. By Sunday: ≥ 70 % on a 25-Q GenAI-tagged quiz.

### 📦 Hard deliverables
- [ ] Skills Boost [#11 Intro to GenAI](https://www.skills.google/course_templates/536) (~30 min).
- [ ] Skills Boost [#12 Intro to LLMs](https://www.skills.google/course_templates/539) (~10 min).
- [ ] Skills Boost [#13 MLOps for GenAI](https://www.skills.google/course_templates/927) (~30 min).
- [ ] Skills Boost [#14 Model Evaluation](https://www.skills.google/course_templates/1080) (~1h).
- [ ] Read [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) ⭐ — full rebrand history + GenAI surface map.
- [ ] Build **one** RAG demo in [Vertex AI Studio](https://cloud.google.com/vertex-ai-studio) (now Agent Platform Studio post-Apr 2026).

### 🧠 Concept anchors
- **GenAI weight on v3.1: ~8–12 %.** Don't over-weight; one focused week is right.
- **Model Garden** = the catalog. Pick first-party (Gemini, Imagen) or open (Llama, Mistral, Claude via Anthropic API).
- **Agent Builder / Gemini Enterprise Agent Platform** = end-to-end RAG + tool-use agents. Was renamed Apr 22, 2026 — exam may use either name.
- **RAG components.** Vector Search (formerly Matching Engine) + embeddings (Gemini text-embedding) + retrieval prompt. Vertex AI Agent Engine = managed agent runtime.
- **Fine-tuning paths.** **Gemini SFT = LoRA-based PEFT** (adapters 1/2/4/8/16; only 2.5 Pro/Flash/Flash-Lite). Pro maxes at adapter 8. **Preference tuning (RLHF-style)** = Flash + Flash-Lite only.
- **Eval.** AutoSxS = side-by-side judge model comparison. Pointwise / pairwise eval. Generative AI eval via Vertex AI Model Evaluation.

### 📅 Daily breakdown
- **Mon (45 min).** [#11](https://www.skills.google/course_templates/536) + [#12](https://www.skills.google/course_templates/539). Read [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) §1–2.
- **Tue (45 min).** [#13](https://www.skills.google/course_templates/927) entirely.
- **Wed (60 min).** [#14](https://www.skills.google/course_templates/1080) entirely + read [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) rebrand history.
- **Thu (60 min).** Build a tiny RAG demo in Vertex AI Studio: paste a Wikipedia page → ask 3 questions → see retrieved chunks.
- **Fri (45 min, paired).** Quiz Mode filtered to `Gemini` / `RAG` / `Model Garden` / `Agent Builder` / `fine-tuning` / `LoRA` — 15 Qs.

### 🧪 Saturday lab (60 min paired — light week)
RAG warm-up using [Vertex AI Studio](https://cloud.google.com/vertex-ai-studio): build a chatbot over a small corpus. Capture rebrand confusion ("is it Vertex AI Search or Agent Search?") in the Labs page.

### 📊 Sunday self-assessment
- **Week 10 Quiz A** (25 Qs GenAI tags) ≥ 70 %.
- Each partner: recite "Gemini SFT is LoRA-based PEFT, adapter sizes 1/2/4/8/16, only 2.5 Pro/Flash/Flash-Lite tunable" cold.
- Wrong-answer drill via Weekly Overview.

### 🚀 Above-and-beyond
- 🛠 Run a Gemini SFT job against a small dataset via the [Vertex AI Tuning API](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models).
- 📖 Read the full [Vertex AI generative-AI overview](https://cloud.google.com/vertex-ai/generative-ai/docs/overview).
- ⭐ Drill the **rebrand alerts** in `pages/1_📅_Weekly_Overview.py` Week 10 tab — 12 historical renames.
- ⭐ Read the [Generative AI for Developers Learning Path /journeys/183](https://www.skills.google/journeys/183) — supplements the v3.1 GenAI bullets.

---

## Week 11 — RAG capstone + Mock #1 (all sections)
**§s.** All · **Hours.** ~6.75 · **Sat.** **MOCK #1 (50 Qs, 2h, ≥ 70 %)**

### 🎯 Theme + measurable success
Real-exam dress rehearsal. By Sunday: **≥ 70 %** on Mock #1, weakest 3 sections identified, drill plan for Week 12 set.

### 📦 Hard deliverables
- [ ] Skills Boost [#17 Create Generative AI Apps on GCP](https://www.skills.google/course_templates/1120) (~4.75h, RAG capstone skill badge).
- [ ] Rapid-review all decision trees: [tabular-modeling](https://docs.cloud.google.com/bigquery/docs/bqml-introduction), [compute-selection](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute), [pipelines-comparison](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction). 30 min each.
- [ ] **Take Mock #1 on Saturday.** Use `pages/9_⏱️_Mock_Exam.py` → "Start Mock #1." 50 Qs, 2-hour timer, no explanations.
- [ ] Identify weakest 3 sections from Mock #1 result. Plan Week 12 drill.
- [ ] Mark lab #17 complete; capture two "ohhh" insights.

### 🧠 Concept anchors
- **Mock #1 protocol.** Sit in a quiet room. Phone face-down. No notes. 2-hour timer. No coffee breaks beyond bathroom. Submit only when timer hits zero or you've reviewed all 50.
- **Don't binge content this week** — the scoring signal from Mock #1 is more valuable than any new lab. Treat Wed–Fri as light consolidation.
- **Rebrand alerts** are dense this week — 4 in the app. Review them on `pages/1_📅_Weekly_Overview.py` Week 11 tab.

### 📅 Daily breakdown
- **Mon (60 min).** [#17](https://www.skills.google/course_templates/1120) modules 1–2.
- **Tue (60 min).** [#17](https://www.skills.google/course_templates/1120) modules 3–end.
- **Wed (60 min).** Decision-tree review: [tabular-modeling](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) + [compute-selection](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute).
- **Thu (60 min).** Decision-tree review: [pipelines-comparison](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction). Read [Andrei Paraschiv's PMLE pass writeup (Feb 2026)](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4) day-of-exam tips.
- **Fri (30 min).** Light review only — no new content. Set up Saturday environment (quiet room, headphones, water).

### 🧪 Saturday — MOCK #1 (120 min)
- Open `pages/9_⏱️_Mock_Exam.py` → click **"Start Mock #1"**.
- 50 questions, 2-hour countdown.
- After submit: review per-section breakdown. The page surfaces "Weakest 3 sections" — write them down.
- **Pass criterion: ≥ 70 %.** If < 70 %: flag exam reschedule risk; do extra Week 12 drill on weakest sections.
- Stagger if both partners are testing: A goes Friday, B goes Saturday — first taker debriefs second.

### 📊 Sunday self-assessment
- Mock #1 already done. Reflect together (60 min): for each wrong question, explain WHY the correct answer wins.
- Lock Week 12 plan: which 3 sections get the bulk of the wrong-answer drill?

### 🚀 Above-and-beyond (only if Mock #1 ≥ 80%)
- 🛠 Build a slightly more complex RAG: chunking strategy comparison (sentence vs paragraph), measure retrieval quality.
- 📖 Skim [Cloud Next 2026 keynote announcements](https://cloud.google.com/blog/topics/google-cloud-next/2026) for any post-rebrand context.
- ⭐ Take Mock #1 *again* with the same seed (the mock pool is deterministic) — see if you remember answers (you should). Note: this **doesn't** validate your knowledge for Mock #2 since the pools are disjoint.

---

## Week 12 — Final review + Mock #2 + exam day (all sections)
**§s.** All · **Hours.** ~6 · **Wed.** **MOCK #2 (50 Qs, 2h, ≥ 80 %)** · **Sat.** **REAL EXAM**

### 🎯 Theme + measurable success
Final calibration + real exam. **Mock #2 ≥ 80 %** is the go/no-go for Saturday. By Saturday night: PMLE certified.

### 📦 Hard deliverables
- [ ] Skills Boost [#18 Fairness & Bias](https://www.skills.google/course_templates/985) (~2.25h).
- [ ] Skills Boost [#19 Interpretability](https://www.skills.google/course_templates/989) (~2h).
- [ ] **Drop [#20 Privacy & Safety](https://www.skills.google/course_templates/1036)** — too long, too low question-yield for the time available.
- [ ] **Take Mock #2 on Wednesday.** ≥ 80 % to track on plan.
- [ ] Heavy wrong-answer drill on weakest 3 sections from Mocks #1 + #2.
- [ ] Confirm exam booking on [Pearson VUE / OnVUE](https://cloud.google.com/learn/certification/machine-learning-engineer). Test webcam Friday.
- [ ] **Saturday: REAL EXAM.**

### 🧠 Concept anchors
- **Day-of-exam logistics.** OnVUE proctoring requires: government ID, clean desk, no phones in room, webcam-visible 360° room scan. 60 Qs / 2 hours. Pass = ≥ 70 %.
- **Read all 4 answer choices before picking.** v3.1 distractors are designed to look right at first glance.
- **Function-first translation.** When you see "Vertex AI Agent Builder" or "Gemini Enterprise Agent Platform" — same product. "Matching Engine" / "Vector Search" — same product.
- **Time discipline.** 60 Qs / 120 min = 2 min/Q on average. Flag long-prose questions, return to them after sweeping the easy ones.

### 📅 Daily breakdown
- **Mon (60 min).** [#18](https://www.skills.google/course_templates/985) entirely.
- **Tue (60 min).** [#19](https://www.skills.google/course_templates/989) entirely.
- **Wed (120 min).** **MOCK #2.** Review breakdown immediately.
- **Thu (60 min).** Wrong-answer drill on Mock #2 wrong questions. Read [Andrei Paraschiv's PMLE pass writeup (Feb 2026)](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4) one more time.
- **Fri (45 min).** Light review only — top 5 high-yield items: skew-vs-drift one-liner, Reduction Server one-liner, Pipelines vs Composer cost numbers, AutoML scale-to-zero trap, Gemini SFT = LoRA. **Do not learn new content Friday.** Test webcam + ID + room.
- **Sat: REAL EXAM.** Sleep 8h. Hydrate. Eat protein. Log in 30 min early. **Pass.**

### 🧪 Wednesday — MOCK #2 (120 min)
- Open `pages/9_⏱️_Mock_Exam.py` → click **"Start Mock #2"**.
- 50 questions from `mock2-pool` (disjoint from Mock #1).
- **Pass criterion: ≥ 80 %.** If < 80 %: **strongly consider pushing the exam by 1 week.** Buffer matters.
- Per-section breakdown → drives Thursday drill.

### 📊 Friday — light review only
- Top 5 high-yield items reciation drill (5 min):
  1. "Skew is training vs production. Drift is production vs production-yesterday."
  2. "Reduction Server: Vertex-only NCCL all-reduce, +75 % throughput, no code changes."
  3. "Vertex AI Pipelines $0.03/run + compute. Cloud Composer $0.06/DCU-hr × ~$400/mo floor."
  4. "AutoML endpoints can't scale to zero. Idle classification endpoint ≈ $991/mo."
  5. "Gemini SFT = LoRA-based PEFT, adapters 1/2/4/8/16. Only 2.5 Pro/Flash/Flash-Lite tunable."

### 🚀 Above-and-beyond
- 📖 Re-skim the canonical references in the [Resources index](#resources-index) — first paragraph only (10 min total).
- ⭐ Don't take a 3rd full mock — diminishing returns. Sleep instead.
- 🎉 Celebrate Saturday with steak.

---

## 10-week compression option

If both partners are pacing **ahead by ≥ 2 days** at end of Week 4 (track via Sunday retros):

- Drop **#5** BQML data engineering (fold into Week 1)
- Skim-only **#12** Intro to LLMs (10 min)
- Drop **#18** + **#19** Responsible AI courses (cover the practice-Q tags in Sunday quizzes instead)
- Merge Weeks 10 + 11 (cap GenAI sweep at one combined week)

Hours saved: ~7. New cadence: 7–8 hr/week × 10 weeks.

---

## Mock exam schedule

| When | What | Pass criterion |
|------|------|-----------------|
| **Sat Week 11** | [Mock #1](gcp-pmle-quiz/pages/9_⏱️_Mock_Exam.py) — 50 Qs from `mock1-pool` (held out, never shown in regular quiz mode), full 2-hour timed | ≥ 70 % to track on plan; identify weakest 3 sections |
| **Wed Week 12** | [Mock #2](gcp-pmle-quiz/pages/9_⏱️_Mock_Exam.py) — 50 Qs from `mock2-pool` (different held-out set), full 2-hour timed | **≥ 80 %** (gives buffer above the 70 % real-exam threshold) |
| **Sat Week 12** | **REAL EXAM** | Pass = ≥ 70 % per Google |

Stagger if possible: partner A goes Friday, partner B goes Saturday — first taker debriefs second.

---

## "If you fall behind" rules

| Behind by | Action |
|-----------|--------|
| 1–2 days | Catch-up Sunday + skip the optional Should-tier Skills Boost item that week |
| 3–5 days | Drop the lowest-weight section's content for that week (per exam blueprint); keep self-assessment quiz |
| > 5 days | Rebudget — push exam date 1–2 weeks. Better than rushing into fail. |

---

## Trial timing

**Pro subscription ($29/mo) starts Day 1 of Week 4** (Feature Engineering — peak lab consumption). The 7-day trial covers ~half of Week 4. Set a calendar reminder for **Day 6 of Week 4** — cancel before Day 7 if you only want to test, otherwise auto-renews. **Three months total subscription = $87 per learner**, plus $200 exam = **$574 total project cost for two**.

---

## Resources index

### Official PDFs
- [PMLE v3.1 exam guide](https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf) — read Week 1 cover-to-cover

### Research reports (all 14)
- [Google Skills ML Engineer learning path](https://www.skills.google/paths/17) — full Skills Boost inventory + sequencing rationale
- [Andrei Paraschiv's PMLE pass writeup (Feb 2026)](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4) — passer themes + Narvaez template + day-of-exam surprises
- [AndyTheFactory gcp-pmle-quiz repo](https://github.com/AndyTheFactory/gcp-pmle-quiz) — 3-bank stack + ethical guidance
- [Vertex AI Model Monitoring overview](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview) — §6 critical concept (memorize the one-liner)
- [Vertex AI training compute config](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute) — §3.3 hardware (Reduction Server is the high-yield item)
- [Vertex AI Pipelines introduction](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction) — §5 orchestrator picks (highest exam weight, 22%)
- [BigQuery ML introduction](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) — §1.1 BQML vs AutoML vs custom training
- [Vertex AI predictions overview](https://docs.cloud.google.com/vertex-ai/docs/predictions/overview) — §4 online/batch/Dataflow/BQML serving paths
- [Vertex AI Experiments intro](https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments) — §5.3 Vertex AI Experiments + ML Metadata
- [Vertex AI Feature Store overview](https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview) — §2 Feature Store (Legacy + Optimized sunset Feb 17, 2027)
- [Vertex AI hyperparameter tuning overview](https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview) — §3.2 Vizier + algorithms + budgeting
- [Google AI Principles](https://ai.google/principles/) — §6.1 RAI + security (Explainable AI deprecated Mar 16, 2026)
- [IAM overview](https://docs.cloud.google.com/iam/docs/overview) — cross-cutting IAM, VPC-SC, private endpoints, Workload Identity
- [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) — v3.1 GenAI map + rename history

### App
- [`gcp-pmle-quiz/`](gcp-pmle-quiz/) — Streamlit quiz app (workhorse: 841 Qs, 537 GenAI-flagged)
- Run: `cd gcp-pmle-quiz && uv run streamlit run 🏠_Dashboard.py` → http://localhost:8501

### External
- [PMLE certification page](https://cloud.google.com/learn/certification/machine-learning-engineer)
- [Google Skills ML Engineer Learning Path 17](https://www.skills.google/paths/17)
- [Google free sample exam form](https://docs.google.com/forms/d/e/1FAIpQLSeYmkCANE81qSBqLW0g2X7RoskBX9yGYQu-m1TtsjMvHabGqg/viewform)
- [Skills Boost / Google Skills subscription page](https://www.skills.google/payments/new)
- [Google Cloud Innovators (free 35 monthly credits)](https://cloud.google.com/innovators)
