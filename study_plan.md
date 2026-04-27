# PMLE 12-Week Study Plan

**Source.** Synthesized from `research/` (6 reports), the official v3.1 exam guide, the closest-match recent passer (V. Narvaez, Feb 2026), and the Google Skills "Professional ML Engineer" learning path inventory.
**Audience.** Two beginners, math-strong, no prior GCP/ML, studying together.
**Target exam.** PMLE v3.1.
**Total budget.** 60–75 hours per learner (≈58 hr Skills Boost + ~10 hr practice questions + ~5 hr docs/review).
**Time split.** 25 % learning path / 25 % official docs / 50 % practice questions — per V. Narvaez Feb 2026 (`research/anecdotes/recent-passers.md`).

---

## Constants and rules
- Both partners follow the same week's theme. Falling behind ≥ 2 days → catch-up Sunday.
- Real exam has near-zero multi-select (per recent passer reports). Practice MS questions for concept reinforcement only.
- GenAI weight: ~8–12 % of exam (triangulated). Don't over-weight.
- Vertex AI ↔ Gemini Enterprise Agent Platform: translate function-first when answer-choice names look unfamiliar.
- Exam fee $200 each. Schedule on Pearson VUE / OnVUE for **Saturday of Week 12** (book in Phase 0).

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
- One partner reads lab steps aloud; the other types in console
- Switch every 30 min
- End-of-lab: each names one "ohhh" insight; push to shared notes

### Sunday — retrospective (60 min)
1. Run weekly self-assessment quiz in Streamlit (≥ 20 Qs, this week's topic tags)
2. Review wrong answers together — explain WHY each correct answer wins
3. Each partner names: 1 thing learned, 1 stuck-on, 1 ahead-of-plan
4. Set Monday's first 30-min focus

---

## Week-by-week

Skills Boost item numbers reference `research/labs/skills-boost-path.md` (Andy bank topic tags use the existing `gcp_topics` / `ml_topics` / `gcp_products` fields in `gcp-pmle-quiz/data/quizzes.jsonl`).

| Week | Theme | Hours | Skills Boost items | Decision-tree refresher | Practice-Q topic tags | Weekend lab | Self-assessment milestone |
|------|-------|-------|---------------------|-------------------------|------------------------|-------------|----------------------------|
| **1** | Orientation + GCP fundamentals | ~5 | **#1** Intro to AI & ML on GCP. Read v3.1 exam guide PDF cover-to-cover. Take Google's free sample form **cold**. | — | First 50 unanswered Qs (any topic) | Free-tier lab on Cloud Storage + IAM (Innovators credits) | Sample-form score = baseline |
| **2** | §1 BQML | ~1 + reading | **#4** Create ML Models with BQML; **#5** Engineer Data for BQML | `research/decision-trees/tabular-modeling.md` ⭐ | `BigQuery ML`, `BQML` | BQML challenge lab (#4) | 20 Qs §1.1, target ≥ 70 % |
| **3** | §1.2 ML APIs + §2.2 notebooks | ~5.25 | **#2** Prepare Data for ML APIs SB; **#3** Working with Notebooks in Vertex AI | — | `Vertex AI Workbench`, `Colab Enterprise`, `Dataproc`, `ML APIs` | Workbench notebook lab (#3) | 20 Qs §1.2 + §2.2 |
| **4** | §2 Feature engineering + Feature Store | ~7.25 | **#6** Feature Engineering ⚠️ (last refresh 9 mo ago — UI may mismatch but concepts current) | `research/concepts/feature-store.md` ⭐ | `Feature Store`, `feature engineering`, `Dataflow` | Feature Store lab (paired) | 20 Qs §2 |
| **5** | §3 Custom training (Keras), part 1 | ~5.5 | **#7** Build, Train, Deploy ML Models with Keras on GCP — first half | `research/concepts/hyperparameter-tuning.md` ⭐ | `custom training`, `hyperparameter tuning` | Pair-program one Keras notebook | 15 Qs §3.1 + §3.2 |
| **6** | §3 finish + §4 hardware | ~7 | **#7** Keras course finish; **#10** MLOps Manage Features | `research/decision-trees/compute-selection.md` ⭐ | `GPU`, `TPU`, `distributed training`, `Reduction Server` | Multi-worker training lab | 20 Qs §3.3 + §4.1 |
| **7** | §3 + §4 + §5 production systems | ~11 | **#8** Production Machine Learning Systems | `research/concepts/serving-deep-dive.md` ⭐ + `research/concepts/iam-for-ml.md` | `serving`, `batch`, `online`, `A/B testing`, `model registry` | Vertex AI deploy + endpoint lab | 25 Qs §4 |
| **8** | §5 Pipelines (highest weight) | ~3 | **#15** ML Pipelines on GCP; **#9** MLOps Getting Started | `research/decision-trees/pipelines-comparison.md` ⭐ + `research/concepts/metadata-lineage.md` | `Vertex AI Pipelines`, `Kubeflow`, `Cloud Composer`, `TFX`, `CI/CD` | Vertex AI Pipelines hands-on | 25 Qs §5 |
| **9** | §3+§4 capstone + §6 monitoring | ~8.25 + 2 | **#16** Build and Deploy ML Solutions on Vertex AI (capstone SB) | `research/concepts/skew-vs-drift.md` ⭐ + `research/concepts/responsible-ai-security.md` ⭐ | `Model Monitoring`, `drift`, `skew`, `Explainable AI` | Capstone challenge lab + monitoring config | 20 Qs §6 |
| **10** | GenAI sweep | ~2.25 + 2 | **#11** Intro to GenAI; **#12** Intro to LLMs; **#13** MLOps for GenAI; **#14** Model Evaluation | `research/genai/vertex-ai-overview.md` ⭐ (rename history) | `Model Garden`, `Agent Builder`, `RAG`, `fine-tuning`, `Gemini` | RAG lab in Vertex AI Studio | 25 Qs GenAI |
| **11** | RAG capstone + **Mock #1** | ~4.75 + 2 | **#17** Create Generative AI Apps on GCP (RAG SB) | All decision trees — rapid review | Wrong-answer drill on weakest 3 sections from Mock #1 | RAG challenge lab | **Mock exam #1 (Sat, full 2-hour timed)** |
| **12** | Final review + **Mock #2** + exam day | ~4 + 2 | **#18** Fairness & Bias; **#19** Interpretability (drop **#20** Privacy & Safety) | All decision trees — final review | Wrong-answer drill, all sections | — | **Mock #2 (Wed)** + **REAL EXAM (Sat)** |

⭐ = decision-tree refresher in `research/` (all 14 landed; 8 added in the Apr 26, 2026 batch).

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
| **Sat Week 11** | Mock #1 — 50 Qs from `mock1-pool` (held out, never shown in regular quiz mode), full 2-hour timed | ≥ 70 % to track on plan; identify weakest 3 sections |
| **Wed Week 12** | Mock #2 — 50 Qs from `mock2-pool` (different held-out set), full 2-hour timed | **≥ 80 %** (gives buffer above the 70 % real-exam threshold) |
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

- `CLAUDE.md` — project briefing + rebrand alerts (read first)
- `PROMPTS.md` — research prompts to re-run every 6 weeks
- `professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf` — official exam guide (READ Week 1)
- `research/labs/skills-boost-path.md` — full Skills Boost inventory + sequencing rationale
- `research/anecdotes/recent-passers.md` — passer themes + Narvaez template + day-of-exam surprises
- `research/question-banks/audit.md` — 3-bank stack + ethical guidance
- `research/concepts/skew-vs-drift.md` — §6 critical concept (memorize the one-liner)
- `research/decision-trees/compute-selection.md` — §3.3 hardware (Reduction Server is the high-yield item)
- `research/decision-trees/pipelines-comparison.md` — §5 orchestrator picks (highest exam weight, 22%)
- `research/decision-trees/tabular-modeling.md` — §1.1 BQML vs AutoML vs custom training
- `research/concepts/serving-deep-dive.md` — §4 online/batch/Dataflow/BQML serving paths
- `research/concepts/metadata-lineage.md` — §5.3 Vertex AI Experiments + ML Metadata
- `research/concepts/feature-store.md` — §2 Feature Store (Legacy + Optimized sunset Feb 17, 2027)
- `research/concepts/hyperparameter-tuning.md` — §3.2 Vizier + algorithms + budgeting
- `research/concepts/responsible-ai-security.md` — §6.1 RAI + security (Explainable AI deprecated Mar 16, 2026)
- `research/concepts/iam-for-ml.md` — cross-cutting IAM, VPC-SC, private endpoints, Workload Identity
- `research/genai/vertex-ai-overview.md` — v3.1 GenAI map + rename history
- `gcp-pmle-quiz/` — Streamlit quiz app (workhorse: 841 Qs, 537 GenAI-flagged)
- `TODOLIST.md` — phased project checklist (Phase 4 is the recurring weekly cadence above)
