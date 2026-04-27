# Deep-Research Prompts for PMLE Study Plan

## ⚠️ Post-research updates (April 2026) — read first

The first batch of agents (see `research/`) surfaced these corrections. Apply across all prompts:

- **Vertex AI → Gemini Enterprise Agent Platform** rebranded **Apr 22, 2026** at Cloud Next 2026. v3.1 exam guide and Skills Boost still use old names. When running prompts, instruct the research tool to **translate function-first, then map to whichever name appears in answer choices**.
- **Cloud Skills Boost → Google Skills** (Oct 2025). New domain `skills.google`. Path `/paths/17` 308-redirects.
- **Doc URLs**: `cloud.google.com/...` → `docs.cloud.google.com/...` (301 redirects). Both forms valid; prefer `docs.` for new fetches.
- **Question banks confirmed NOT to exist for PMLE** (as of Apr 2026): Tutorials Dojo / Jon Bonso, ExamPro / Andrew Brown, AnkiHub / AnkiWeb decks. Drop these from P3 and P12 prompts (edits applied below).
- **Realistic study budget**: 60–75 hours total per learner (per V. Narvaez, Feb 2026). The plan P1 produces should target this, not 200+ hours.
- **Vertex AI Model Monitoring v2** announced Jun 11, 2024, still Pre-GA Apr 2026. Both v1 and v2 are exam-fair. v1 default drift threshold: 0.3.
- **Real exam has near-zero multi-select** despite practice banks including them.
- **GenAI weight**: triangulated at ~8–12% of exam questions. Don't over-weight.

---

Each prompt below is **paste-ready** for ChatGPT Deep Research, Gemini Deep Research, or Claude Research. They are designed to be run **in parallel across at least 2 tools** so we can triangulate findings before trusting any advice.

---

## How to use this file

1. Pick a prompt (P1–P13).
2. Paste the prompt **including the `## Constants` block at the top of this file** into the chosen research tool.
3. Save the resulting report as `research/<prompt-slug>/<tool>.md` (e.g. `research/study-plan/chatgpt.md`).
4. Run the same prompt on a second tool. Compare. Note disagreements in `research/<slug>/_diff.md`.
5. After all P1–P12 reports are collected, run **P13 (Reconciliation)** with those reports as inputs.
6. Re-run P2, P3, P4 every ~6 weeks while studying — Google ships changes monthly and community advice rotates.

### Tool routing (rough strengths)

| Tool | Best for |
|------|----------|
| **ChatGPT Deep Research** | Citation rigor, academic-style synthesis, comparing many sources, paid-content reviews |
| **Gemini Deep Research** | Fresh web grounding, Reddit/forum aggregation, official Google docs (Google's own model knows its own docs well) |
| **Claude Research** | Structured synthesis, decision trees, study-plan logic, reconciliation across noisy inputs |

For every prompt I've marked a **primary** tool, but always run on a second one to cross-check.

---

## Constants — paste this block at the top of every prompt

```
EXAM: Google Cloud Professional Machine Learning Engineer, exam version v3.1
       (current since April 2025; includes Vertex AI Model Garden, Vertex AI Agent
        Builder, RAG applications, fine-tuning of foundation models, evaluating
        generative AI solutions).

EXAM BLUEPRINT (from the official v3.1 guide):
  §1 (13%)  Architecting low-code AI: BigQuery ML; ML APIs / foundation models in
            Model Garden; industry APIs (Document AI, Retail); RAG via Vertex AI
            Agent Builder; AutoML (tabular, text, speech, image, video).
  §2 (~14%) Collaborating across teams: organization-wide data (Cloud Storage,
            BigQuery, Spanner, Cloud SQL, Spark, Hadoop); Vertex AI Workbench,
            Colab Enterprise, Dataproc; Vertex AI Feature Store; PII/PHI handling;
            Vertex AI Experiments, Kubeflow Pipelines, TensorBoard; evaluating GenAI.
  §3 (~18%) Scaling prototypes: framework choice; interpretability; custom
            training, Kubeflow on GKE, AutoML, distributed training; hyperparameter
            tuning; fine-tuning foundation models; CPU vs GPU vs TPU vs edge;
            Reduction Server; Horovod.
  §4 (~20%) Serving and scaling: batch + online inference (Vertex AI, Dataflow,
            BigQuery ML, Dataproc); multi-framework serving; model registry;
            A/B testing; Feature Store; public + private endpoints; throughput
            scaling; latency / memory / throughput tuning.
  §5 (~22%) Pipelines + automation (HIGHEST WEIGHT): end-to-end pipelines;
            Kubeflow Pipelines, Vertex AI Pipelines, Cloud Composer, MLFlow, TFX;
            Cloud Build, Jenkins, CI/CD; retraining policies; Vertex AI
            Experiments + Vertex ML Metadata; model + data lineage.
  §6 (~13%) Monitoring: training-serving skew; feature attribution drift; Vertex
            AI Model Monitoring; Explainable AI; Responsible AI practices;
            security against unintended exploitation; assessing fairness/bias.

AUDIENCE: Two learners studying together. Mathematically strong. Zero prior GCP
          or production-ML experience. 10–12 week timeline (deliberately longer
          than the typical 8-week recommendation because of zero ramp-up
          experience). The exam does NOT test coding skill — Python + SQL
          literacy is sufficient to read code snippets.

OUTPUT RULES:
  1. Cite every non-trivial claim with a URL AND a publication date.
  2. Prefer sources from 2024 onward. FLAG any cited source older than 2023.
  3. If a recommendation depends on a GCP product feature, verify it isn't
     deprecated/renamed in current cloud.google.com docs and cite the doc URL.
  4. When community sources disagree, present BOTH views and indicate which is
     more recent and which has more independent corroboration.
  5. Output in well-structured Markdown: H2/H3 headings, tables where comparing
     ≥3 things, footnote-style citations [1] [2] etc., a final "References"
     section with full URLs and dates.
  6. End every report with a "Confidence" section (High / Medium / Low for
     each major claim) and a "Decay risk" note (which findings are likely to
     go stale within 6 months).
```

---

# P1 — Twelve-week study plan for absolute GCP/ML beginners
**Primary tool:** Claude Research **|** **Cross-check:** Gemini Deep Research
**Save as:** `research/study-plan/<tool>.md`

```
[paste Constants block here]

You are a senior ML platform engineer who has personally tutored 10+ engineers
through the PMLE certification. Build a complete WEEK-BY-WEEK study plan for
the audience defined in the Constants.

Required output:

1. A 12-week schedule as a Markdown table with these columns:
     | Week | Theme | Daily hours (target) | Primary resource(s) | Hands-on lab(s) | End-of-week assessment | Notes |

2. Honor these constraints:
     - Weeks 1–2 must be PURE GCP fundamentals (IAM, projects, Cloud Storage,
       BigQuery basics, Cloud Run/Cloud Functions intuition) BEFORE touching
       Vertex AI. Justify why with sources.
     - Front-load the heavier-weight sections: §5 Pipelines (22%), §4 Serving
       (20%), §3 Scaling (18%) should occupy their proportional share of total
       hours, not the same time as §1 (13%) and §6 (13%).
     - Reserve weeks 11–12 entirely for: full mock exams + targeted re-study of
       weak topics + final review. No new content in the last 14 days.
     - Insert one "buffer / review" day per week (typically Sunday).
     - Account for the GenAI additions in v3.1 (Model Garden, Agent Builder,
       RAG, fine-tuning) — beginners often miss these because older 2022–2023
       guides predate them. Allocate ≥1 dedicated week.

3. For each week, give:
     - Specific Google Skills Boost course IDs / Coursera modules / YouTube
       videos with timestamps when relevant.
     - 1–3 hands-on labs (Qwiklabs / Skills Boost) with credit cost estimates.
     - 1 reflection question and 1 self-test (10 questions or one mock-section).

4. After the 12-week table, give:
     - A "compressed 10-week variant" if the learners are picking up faster
       than expected (state explicitly which weeks to merge and what to drop).
     - A "what to skip" list — content that historically doesn't appear on the
       exam at material weight, with sources backing the claim.
     - Daily-routine template: split into "active learning" (videos/reading)
       vs "active recall" (quizzes/labs/flashcards), with %-of-time guidance.

5. Cite recent (2024–2026) passers' study plans where the recommendations
   originate. Differentiate "what worked for someone with prior cloud
   experience" vs "what worked for someone starting from zero."
```

---

# P2 — Comprehensive resource ranking
**Primary tool:** ChatGPT Deep Research **|** **Cross-check:** Gemini Deep Research
**Save as:** `research/resources/<tool>.md`

```
[paste Constants block here]

Build a comprehensive RANKED inventory of every credible resource for PMLE
v3.1 prep. Return SEPARATE ranked tables for each category below; do not
merge them.

Categories (one table per category):

A) FREE official Google content
   (Skills Boost paths/courses, Coursera Google specialization free auditing,
   official sample questions, official whitepapers, Google Cloud blog posts,
   Vertex AI documentation tutorials, Codelabs)

B) PAID courses (full courses, not question banks)
   (Coursera ML Engineer Learning Path certificate track, A Cloud Guru,
   Pluralsight, Linux Academy archives, Udemy by-instructor — list ALL
   reputable instructors with course slugs, ExamPro, Cloud Academy, Whizlabs
   courses (separate from their question banks))

C) YouTube channels and playlists
   (full PMLE-focused playlists from 2024+ only; flag any older as stale)

D) Books (technical, not exam-dump compilations)
   (e.g. "Machine Learning Design Patterns" — Lakshmanan; "Introducing MLOps" —
   Treveil; specifics published in 2023+ preferred)

E) High-signal blog posts and Medium articles
   (recent passer write-ups with detailed advice, technical deep-dives on
   specific exam topics — group by topic if useful)

F) Podcasts / interviews / recorded conference talks (Google Cloud Next sessions
   on Vertex AI, MLOps, Agent Builder — list session IDs and dates)

For EACH entry in EACH table, provide these columns:
   | Title | Author/Channel | URL | Cost | Hours to consume | Last updated/published | Exam sections covered (use §1–§6 weights) | Strengths | Weaknesses | Reviewer consensus (cite ≥2 reviews) | Recommended order |

After the tables:
   - "Top 3 picks per category" with the rationale.
   - "Skip list": resources that look popular but underperform — be specific
     about why (outdated, paid for low signal, padded with filler).
   - "Bundle recommendation" — given a $0 budget, $50 budget, $200 budget, and
     unlimited budget, what's the optimal stack?
   - Note any free trials / first-month-free promos and how to time them.

Verify all listed resources still exist and are not deprecated as of today.
```

---

# P3 — Question bank audit and quality assessment
**Primary tool:** ChatGPT Deep Research **|** **Cross-check:** Gemini Deep Research
**Save as:** `research/question-banks/<tool>.md`

```
[paste Constants block here]

Audit every known PMLE practice-question source. Goal: decide which to ingest
into our consolidated question bank and which to avoid.

Sources to assess (find more if you know of any):
   - The official Google PMLE practice exam (free, ~25 questions)
   - Whizlabs PMLE practice tests
   - ExamTopics (community-discussed question dumps)
   - Skillcertpro (NOTE: prior audit confirmed as braindump source; verify
     status, flag as ethical violation if still selling real-exam-derived
     content)
   - A Cloud Guru / Pluralsight bundled practice questions
   - Udemy practice tests (list by instructor — at least Ranga Karanam,
     Ulises Gascon, others)
   - Cloud Academy practice exams
   - Github open-source community banks (AndyTheFactory/gcp-pmle-quiz has
     ~841 questions, 537 hit v3.1 GenAI keywords — verified locally Apr
     2026; find others)
   - PassQuestion, ITExams, AmazonAWS-cert dump aggregators (verify
     status; expect to flag as braindump)

   ⚠️ Banks confirmed NOT to exist for PMLE as of Apr 2026 (don't waste
   research-tool time on them, but flag if status changed):
   - Tutorials Dojo / Jon Bonso (no PMLE product as of Apr 2026)
   - ExamPro / Andrew Brown (no PMLE product as of Apr 2026)
   - AnkiHub / AnkiWeb (no shared PMLE deck of usable quality as of Apr
     2026)

For each source, assess:
   | Source | Question count | Free or $ | Last updated | Coverage of v3.1 GenAI content | Answer-accuracy reputation (cite specific Reddit threads/reviews) | Format (single/multiple choice, with explanations?) | Dump-site (ethically questionable) or legit | Recommended for our use? (Yes / Maybe / No) | Notes |

Then deliver:
   1. Recommended consumption order (which to use first vs save for the last
      two weeks).
   2. Deduplication / overlap analysis — which banks share questions verbatim?
   3. ETHICAL guidance: which sources are dumps of real exam content (against
      Google's NDA) vs original practice questions. The user wants to study
      ethically — flag any source that is verbatim leaked exam content.
   4. Specific examples of frequently-wrong answers from each source — Reddit
      and Medium often catch these.
   5. A spreadsheet-style "ingestion plan" for combining the legit sources
      into a single bank (target ≥1500 deduped questions): what order, what
      verification step per source.
```

---

# P4 — Recent passer anecdotes and themes (April 2025 — today)
**Primary tool:** Gemini Deep Research **|** **Cross-check:** ChatGPT Deep Research
**Save as:** `research/anecdotes/<tool>.md`

```
[paste Constants block here]

Aggregate recent first-hand PMLE passer write-ups, ONLY from April 2025 onward
(post-v3.1). Ignore anything older — pre-v3.1 advice predates the GenAI
content rollout.

Sources to search:
   - Reddit: r/googlecloud, r/learnmachinelearning, r/MachineLearning,
     r/cscareerquestions, r/sysadmin (some passers post there)
   - Medium tags: gcp-pmle, pmle, professional-machine-learning-engineer,
     google-cloud-certification
   - Dev.to and Hashnode posts with the same tags
   - LinkedIn posts (search "passed PMLE", "Professional Machine Learning
     Engineer certification")
   - YouTube post-exam debrief videos from 2025 onward
   - Personal blogs found via Google search "passed Google PMLE 2025"
   - Twitter/X posts from credible engineers
   - Cert-prep Discord server posts (if accessible via web index)

For each anecdote, capture:
   | Source URL | Date | Author background (years exp / prior GCP / prior ML) | Study duration | Total study hours (if disclosed) | Resources used (with rank) | Score (if disclosed; passing is 70%+) | Top 3 lessons | Top 3 surprises on exam day |

Then synthesize:
   1. Top 10 themes ranked by frequency (theme = a piece of advice that ≥3
      passers independently mentioned).
   2. Disagreements — places where passers contradict each other (e.g.,
      "GenAI was a small part" vs "GenAI was 25% of my exam"). Show both
      sides with citations.
   3. Background-stratified breakdowns:
        - "I had no prior ML/GCP" — what worked for them?
        - "I had ML experience but no GCP" — what worked?
        - "I had GCP experience but no production ML" — what worked?
   4. Time-allocation heatmap: for each of §1–§6, what % of total study time
      do recent passers report spending?
   5. Day-of-exam advice consensus — flag time, biobreaks, marking review,
     pacing per question.
   6. Updates to common advice that older guides got wrong (e.g., things that
      changed after April 2025).
```

---

# P5 — Hands-on lab strategy and GCP free-tier optimization
**Primary tool:** Gemini Deep Research **|** **Cross-check:** ChatGPT Deep Research
**Save as:** `research/labs/<tool>.md`

```
[paste Constants block here]

Build a hands-on lab strategy for two beginners with limited GCP credits.

Scope:
   1. Google Skills Boost paid subscription ($29/mo) — list every PMLE-relevant
      lab/quest/course with:
        | Item | Type (lab/course/quest) | Hours | Skill points | Exam sections | Priority (Must/Should/Skip) |
   2. Google Skills Boost free trial — what's in it, how long does it last,
      what's the maximum credit you can extract before it ends?
   3. The new $300 GCP free trial — how to allocate it across mandatory
      hands-on practice (Vertex AI custom training, Vertex AI Pipelines,
      AutoML, Model Monitoring, Feature Store, BigQuery ML).
   4. Free-tier resources that NEVER expire — list everything in the always-free
      tier that's relevant to ML practice (e.g. BigQuery 1TB queries/month,
      Cloud Storage 5GB).
   5. DIY local-first labs — what can be done in Colab (free) or local Jupyter
      that simulates the GCP-only experience close enough for exam purposes?
   6. Qwiklabs vs Skills Boost — are they the same now? Are there free
      Qwiklabs sessions still available?

Deliverable:
   - A "MUST do" lab list (≤15 labs) with total estimated hours, ordered
     by exam section weight.
   - A "NICE to do" extension list.
   - A "credit-burn schedule" — when in the 12-week plan to spin up which
     resource (and tear it down to avoid charges). Include warnings about
     GPUs/TPUs that bill per second and can drain credits in hours.
   - List of common $$$ traps (e.g., forgotten endpoints, persistent disks).
   - Cite the official pricing pages and free-tier terms.
```

---

# P6 — Generative AI section (v3.1's newest content) deep dive
**Primary tool:** Gemini Deep Research **|** **Cross-check:** Claude Research
**Save as:** `research/genai/<tool>.md`

```
[paste Constants block here]

The v3.1 exam guide (April 2025) added significant generative AI content.
Older study guides miss this. Build a focused deep dive.

Cover specifically (mapping to the official guide):
   §1.2 — Building applications with ML APIs from Model Garden,
          industry-specific APIs (Document AI, Retail), RAG with Vertex AI
          Agent Builder.
   §2.2 — Foundational + open-source models in Model Garden.
   §2.3 — Evaluating generative AI solutions (what metrics? Vertex AI
          eval pipeline?).
   §3.2 — Fine-tuning foundational models (Vertex AI fine-tuning, Model
          Garden tuning, parameter-efficient methods like LoRA on Vertex AI).
   §4 — Serving fine-tuned + foundation models (online prediction with
        prompt templates, throughput considerations).
   §5 — Orchestrating GenAI pipelines (RAG ingestion, eval pipelines).
   §6 — Monitoring GenAI solutions (hallucination, groundedness,
        prompt injection, output quality drift).

Required output:
   1. A "concept-to-product" map — for every GenAI concept on the exam, which
      Vertex AI product implements it and what alternatives exist.
   2. A FAQ for common confusions: e.g.
        - When use Model Garden's pre-trained model vs Agent Builder's
          managed RAG?
        - Vertex AI Studio vs Vertex AI Agent Builder vs Conversational
          Agents — pick the right one for a given scenario.
        - Prompt design vs few-shot vs supervised fine-tuning vs RLHF —
          when to use each on Vertex AI.
   3. A 30-question practice mini-bank in our schema (single_choice and
      multiple_choice, each with 4–5 options, an `answer` index, and a
      detailed `explanation`). Use this exact JSON-line schema:

      {"id": <int>, "mode": "single_choice", "question": "...",
       "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
       "answer": <0-3>, "explanation": "...",
       "ml_topics": [...], "gcp_products": [...], "gcp_topics": [...]}

   4. Cite the relevant cloud.google.com/vertex-ai/generative-ai docs for
      every claim. Highlight any Agent Builder / Model Garden feature renamed
      or restructured in the past 6 months — Google has been iterating fast.
```

---

# P7 — Confusable-products decision trees
**Primary tool:** Claude Research **|** **Cross-check:** Gemini Deep Research
**Save as:** `research/decision-trees/<tool>.md`

```
[paste Constants block here]

The PMLE exam tests product-selection judgment heavily. Build clear decision
trees / flowcharts for these commonly-confused pairs/triples. Each should be
presentable as a Markdown decision tree (nested bullet list) AND as a small
ASCII / Mermaid diagram. Each must end with a 1-line "if in doubt, default to
X because Y" rule.

The trees:

   1. Vertex AI Pipelines vs Kubeflow Pipelines vs Cloud Composer (Airflow) —
      when each wins.
   2. BigQuery ML vs AutoML Tables vs Vertex AI custom training — picking the
      right tool for tabular ML.
   3. Vertex AI Workbench vs Colab Enterprise vs Dataproc Jupyter — choosing
      a notebook backend.
   4. CPU vs GPU vs TPU vs Edge — training and inference compute selection.
      Include cost-per-hour orders of magnitude.
   5. Vertex AI batch prediction vs online prediction vs Dataflow vs
      BigQuery ML inference — choosing the serving path.
   6. Vertex AI Feature Store vs ad-hoc BigQuery features — when is Feature
      Store worth the operational cost?
   7. Cloud Storage vs BigQuery vs Spanner vs Cloud SQL for training data
      ingestion — pick the right primary store.
   8. Cloud Build vs Jenkins vs GitHub Actions for ML CI/CD on GCP.
   9. Vertex AI Model Monitoring vs custom monitoring with Cloud Monitoring +
      BigQuery — when each is appropriate.
  10. Vertex AI Agent Builder vs Dialogflow CX vs custom RAG — picking the
      right conversational/RAG stack.
  11. Distributed-training patterns: Vertex AI's MultiWorkerMirroredStrategy
      vs Reduction Server vs Horovod vs ParameterServerStrategy — when each.
  12. Fine-tuning foundation model vs prompt engineering vs RAG — given a
      business need, which to recommend.

Each decision tree must:
   - Cite official Google docs that justify the routing.
   - Note any cost / latency / lock-in tradeoffs.
   - Flag any choice that recently changed (i.e., a 2024 best practice that
     became a 2025 best practice).
```

---

# P8 — Section 6 (Monitoring, Responsible AI) deep dive — 13%
**Primary tool:** ChatGPT Deep Research **|** **Cross-check:** Gemini Deep Research
**Save as:** `research/monitoring/<tool>.md`

```
[paste Constants block here]

Build a focused study guide for §6 of the exam (~13%). Cover all sub-topics
explicitly listed in the official guide:

§6.1 Identifying risks
   - Building secure AI (against unintended exploitation, prompt injection,
     model exfiltration)
   - Google's Responsible AI practices (bias monitoring)
   - Assessing AI solution readiness (fairness, bias)
   - Model explainability on Vertex AI (Explainable AI, feature attribution)

§6.2 Monitoring, testing, troubleshooting
   - Continuous evaluation metrics (Vertex AI Model Monitoring, Explainable AI)
   - Training-serving skew (DEFINITION + how to detect on Vertex AI)
   - Feature attribution drift (DEFINITION + difference from training-serving
     skew)
   - Performance vs baselines, simpler models, time dimension
   - Common training and serving errors

Required output:
   1. Glossary — every concept above with a precise 1–2 sentence definition,
     ideally quoting the Vertex AI docs verbatim (with citation).
   2. A "training-serving skew vs feature drift" table that disambiguates
     them — this is a #1 confusion in exam writeups.
   3. Configuration walkthroughs (markdown pseudo-code, not actual code) for:
        - Setting up Vertex AI Model Monitoring on an endpoint
        - Configuring drift alerts to a Pub/Sub → Cloud Function retraining loop
        - Enabling feature attribution
   4. 30 practice questions in our JSONL schema (see P6 spec).
   5. The 10 most common §6 mistakes per recent passer reports.
```

---

# P9 — Section 5 (Pipelines + Automation) deep dive — 22% (highest weight)
**Primary tool:** ChatGPT Deep Research **|** **Cross-check:** Claude Research
**Save as:** `research/pipelines/<tool>.md`

```
[paste Constants block here]

Section 5 is the highest-weight on the exam (22%). Build the deepest possible
study guide.

Cover:
§5.1 — End-to-end pipelines: data + model validation, train/serve preprocessing
       parity, MLFlow-on-GCP hosting, components + parameters + triggers
       (Cloud Build, Cloud Run), orchestration (Kubeflow Pipelines, Vertex AI
       Pipelines, Cloud Composer), hybrid/multicloud, TFX components,
       Kubeflow DSL.
§5.2 — Auto-retraining: when to retrain (drift, schedule, performance), CI/CD
       deployment with Cloud Build / Jenkins.
§5.3 — Metadata: Vertex AI Experiments, Vertex ML Metadata, dataset/model
       versioning, lineage.

Deliverables:
   1. A reference architecture diagram (Mermaid) for a full Vertex AI
      Pipelines lifecycle from BigQuery ingestion through training, eval,
      registry, deployment, monitoring, retraining trigger.
   2. A side-by-side comparison: Vertex AI Pipelines vs Kubeflow Pipelines on
      GKE — feature parity, when to choose each, cost.
   3. TFX components mini-reference: ExampleGen, Transform, Trainer, Evaluator,
      Pusher — with one-sentence purpose + when on the exam.
   4. Retraining policy decision tree: drift-triggered vs schedule vs
      performance-triggered — each with a concrete config recipe.
   5. CI/CD reference flow: from `git push` to a deployed model on a Vertex AI
      endpoint — list every Google service and artifact.
   6. 50-question practice mini-bank (this section is highest weight) in our
      JSONL schema.
   7. The 15 most-cited §5 traps from recent passer writeups.
```

---

# P10 — Common exam-day mistakes and pacing strategy
**Primary tool:** Gemini Deep Research **|** **Cross-check:** ChatGPT Deep Research
**Save as:** `research/exam-day/<tool>.md`

```
[paste Constants block here]

Compile the top 25 mistakes recent (April 2025+) PMLE passers report making
on exam day, ranked by frequency across writeups. For each:

   | Rank | Mistake | How to spot the trap | How to avoid it | Example or paraphrased question if cited |

Then:
   - Pacing strategy: 50 questions in 2 hours (≈2.4 min/Q). What's the
     consensus on flag-and-return vs commit-and-move?
   - The "80% know-it answer" trap — option that's right in 80% of cases
     but wrong for the specific scenario.
   - "All of these are right, pick the BEST one" interpretation tactics.
   - Multiple-correct (multiple choice) vs single-correct — how to spot.
   - Test-center vs OnVUE online — which has fewer issues per recent passers,
     known proctor-related problems.
   - Pre-exam checklist: ID, biobreak rules, water, scratch paper allowance.
   - Post-exam: how scores are reported, retake policy / wait time, badge.

Cite specific Reddit threads / blog posts.
```

---

# P11 — Math-strong-but-cloud-noob study sequencing
**Primary tool:** Claude Research **|** **Cross-check:** ChatGPT Deep Research
**Save as:** `research/sequencing/<tool>.md`

```
[paste Constants block here]

Audience profile: two learners with strong undergraduate-level mathematics
(linear algebra, multivariable calculus, statistics, probability) but ZERO
prior GCP experience and ZERO production ML experience.

Question: given that profile, what to skip vs what to spend extra time on?

Required output:
   1. A "skip / skim / standard / extra-deep" classification for every major
      sub-topic in the exam blueprint. Justify each with reasoning grounded in
      cognitive efficiency (math intuition transfers, GCP product taxonomy
      doesn't).
   2. Specific concepts where math-strong learners can compress study time:
        - Gradient descent + variants
        - Loss functions (cross-entropy, hinge, MSE, quantile)
        - Regularization (L1, L2, dropout)
        - Hyperparameter tuning logic (search vs Bayesian)
        - Distributed training math (data parallelism vs model parallelism)
        - PCA / matrix factorization
   3. Specific concepts where math-strong learners must NOT shortcut, because
      the exam tests product behavior, not math:
        - Vertex AI product hierarchy (Workbench / Pipelines / Endpoints / etc.)
        - GCP IAM roles for ML (custom service accounts, predefined roles)
        - Logging / monitoring product split (Cloud Logging vs Cloud Monitoring
          vs Vertex AI Model Monitoring)
        - Data residency / VPC-SC / private endpoints
        - Pricing intuition (where costs balloon)
   4. Recommended weekly cadence: math-strong learners can do 25–30 hours/week
      vs typical 15–20 — verify or refute this against passer reports.
   5. Analogies that transfer well from math/CS for the trickiest concepts —
      e.g., "training-serving skew is like a covariate shift in your test
      distribution".
```

---

# P12 — Spaced repetition + retention workflow
**Primary tool:** Claude Research **|** **Cross-check:** Gemini Deep Research
**Save as:** `research/retention/<tool>.md`

```
[paste Constants block here]

Design the optimal retention workflow for a 12-week, two-person, daily study
cadence. We already have ~841 questions in a Streamlit quiz tool with topic
tagging and incorrect-answer replay; we plan to consolidate to 1500+.

Cover:
   1. Anki vs NotebookLM vs Streamlit-quiz-only vs combined — what's the
      consensus among recent PMLE passers? (Note: prior audit found NO
      pre-built PMLE Anki deck of usable quality on AnkiWeb/AnkiHub as of
      Apr 2026. Confirm status before recommending Anki at all.)
   2. If Anki: card schemas suitable for HAND-BUILDING from scratch (cloze
      vs Q-A vs image-occlusion). Recommended deck structures for the 6
      exam sections. How to bulk-generate cards from the AndyTheFactory
      quiz bank's wrong-answer NotebookLM markdown export.
   3. Cost-benefit: given no pre-built deck exists, is Anki worth the
      build-cost vs leaning entirely on the Streamlit quiz + NotebookLM
      workflow that we already have? Cite recent passer reports either way.
   4. NotebookLM workflow — best practices for sources, prompts to generate
      flashcards/quizzes from incorrect answers and from official docs.
      Include the suggested-source URL list:
        https://docs.cloud.google.com/vertex-ai/docs/training/neural-architecture-search/suggested-workflow
        https://docs.cloud.google.com/dataflow/docs/optimize-costs
        https://docs.cloud.google.com/vertex-ai/docs/tabular-data/bp-tabular
        https://docs.cloud.google.com/architecture/ml-on-gcp-best-practices
        https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api/best-practices
        https://docs.cloud.google.com/dataflow/docs/guides/pipeline-best-practices
        https://docs.cloud.google.com/tpu/docs/intro-to-tpu
        https://cloud.google.com/blog/products/ai-machine-learning/master-gemini-sft
        https://docs.cloud.google.com/vertex-ai/docs/training/code-requirements
        https://docs.cloud.google.com/dialogflow/cx/docs/concept/best-practices
        https://docs.cloud.google.com/spanner/docs/vector-index-best-practices
      Suggest additions or replacements based on §1–§6 weights.
   5. Recommended daily / weekly review schedule — number of new cards, number
      of review cards, time-per-session.
   6. Two-person accountability cadence — pair-quizzing rituals that real
      passers used (cite recent posts).
   7. The 10 hardest concepts to retain per passer reports, with mnemonic
      suggestions.
   8. How to use "wrong-answer-only" replay effectively — diminishing returns
      threshold.
```

---

# P13 — Reconciliation across all reports
**Primary tool:** Claude Research **|** **Cross-check:** ChatGPT Deep Research
**Save as:** `research/_reconciled/canonical.md`
**Run last**, after collecting outputs from P1–P12 in `research/<slug>/<tool>.md`.

```
[paste Constants block here]

You have access to all the deep-research reports listed below. Read them as
input and produce ONE canonical synthesis document. Treat the reports as
noisy signal — your job is to reconcile.

Input reports (paste the full text of each, or link to each, in the order
listed):
   - research/study-plan/{chatgpt,gemini,claude}.md
   - research/resources/{chatgpt,gemini,claude}.md
   - research/question-banks/{chatgpt,gemini,claude}.md
   - research/anecdotes/{chatgpt,gemini,claude}.md
   - research/labs/{chatgpt,gemini,claude}.md
   - research/genai/{chatgpt,gemini,claude}.md
   - research/decision-trees/{chatgpt,gemini,claude}.md
   - research/monitoring/{chatgpt,gemini,claude}.md
   - research/pipelines/{chatgpt,gemini,claude}.md
   - research/exam-day/{chatgpt,gemini,claude}.md
   - research/sequencing/{chatgpt,gemini,claude}.md
   - research/retention/{chatgpt,gemini,claude}.md

Reconciliation rules:
   1. CONFIRMED — recommendations corroborated by ≥3 independent reports
     (across tools or across reviewed sources within a single tool's report).
     Promote to canon.
   2. MAJORITY — corroborated by 2 reports. Include but tag "majority view".
   3. SOLO — appears in only 1 report. Include in an "uncorroborated leads"
      appendix, never in the main study plan.
   4. CONFLICT — when reports disagree directly, present BOTH with their
      sources, and pick a tentative winner with reasoning, but mark it as
      "decision pending verification".

Required output structure:
   1. **Canonical 12-week schedule** (the master plan we will execute).
   2. **Resource shortlist** — top picks per category, ranked.
   3. **Question-bank ingestion plan** — which banks, in which order, with
      verification checks.
   4. **Hands-on lab list** — the labs we will actually do, with a credit
     budget projection.
   5. **Confusable-products cheatsheet** — the canonical decision trees.
   6. **Section-weighted study targets** — hours per section.
   7. **Risk register** — items where reports disagreed, expected to change,
     or where recency is suspect.
   8. **References** — full URL + date list, deduplicated.

End with a "Next 7 days" action list — the very first concrete steps to begin
executing the plan immediately.
```

---

## Maintenance / re-running

- **After all P1–P13 land**: write `study_plan.md`, `resources.md`,
  `question_banks.md` at the repo root, derived from `research/_reconciled/canonical.md`.
- **Every 6 weeks during the study period**: re-run **P2** (resources), **P3**
  (question banks), **P4** (anecdotes) — these decay fastest.
- **If Google announces a v3.2 exam guide**: re-run everything; the GenAI
  area will get more weight every revision.

## Style guidance for any deep-research tool that asks
- **Length**: aim for 3,000–8,000 words per report. Truncate filler, not
  citations.
- **Tables**: use Markdown tables for any comparison of ≥3 items.
- **Code/JSON blocks**: triple-fenced with language hint.
- **No filler intro/outro paragraphs** — start with the substantive content.
- **No marketing language** — flag it when found in cited sources.
