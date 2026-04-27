# Google PMLE Certification — Study Project

## Mission
Two learners are studying together for the **Google Cloud Professional Machine Learning Engineer (PMLE)** certification (exam version **v3.1**, current as of April 2025+, includes generative AI content) on a **10–12 week timeline**. Both are **mathematically strong** but have **zero prior GCP or production ML experience**. Standard advice on r/googlecloud / Medium is "8 weeks for someone with prior cloud or ML experience" — we deliberately add 2–4 weeks of slack to absorb GCP product taxonomy and ML lifecycle concepts from scratch.

**Realistic study budget** (post-research): **60–75 hours total per learner**, ≈5–6 hr/week × 12 weeks, derived from the closest-match recent passer profile (V. Narvaez, Feb 2026 — see `research/anecdotes/recent-passers.md`). The 25 / 25 / 50 split — learning path / official docs / practice questions — is the canonical pacing template. **GenAI weight on the v3.1 exam**: triangulated at **~8–12% of questions** across 10 recent passer anecdotes. Plan a single dedicated week, don't over-weight.

End deliverable is a single web app that consolidates:
- A weekly study schedule (10–12 weeks)
- Curated learning resources (free + paid, ranked + dated)
- Hands-on labs / Skills Boost path with credit-burn awareness
- A unified question bank (target ≥1,500 deduped questions across all reputable sources)
- Topic-level performance tracking & knowledge-gap analytics
- Notes, explanations, decision-tree cheatsheets for confusable products

## Live state and rebrand alerts (April 2026, post-research)

The first batch of research agents (see `research/`) surfaced rebrands and corrections. Treat these as authoritative over older content:

### Product rebrands
- **Vertex AI → Gemini Enterprise Agent Platform** — announced at Google Cloud Next 2026 on **April 22, 2026** (two days before this file was written). The PMLE v3.1 exam guide and Skills Boost courseware **still use 2025 names** ("Vertex AI Agent Builder", "Vertex AI Studio", "Vertex AI Search"). Fresh `cloud.google.com` blogs and product UIs use the new names ("Agent Platform Studio", "Agent Search"). **Rebrand scope confirmed (Apr 26, 2026 research): affects Agent Builder / Studio / Search only — Pipelines, Training, Model Registry, ML Metadata, Experiments names are intact.** **Study tactic: translate function-first, then map to whichever name appears in the answer choice.** Full rename history in `research/genai/vertex-ai-overview.md`.
- **Cloud Skills Boost → Google Skills** — Oct 2025. Domain `cloudskillsboost.google` → `skills.google` (308 redirects). Path `/paths/17` is unchanged.
- **Docs hostname** — `cloud.google.com/...` → `docs.cloud.google.com/...` (301 redirects). Both forms valid; prefer `docs.` for new fetches.

### Specific renames worth memorizing
- Matching Engine → **Vector Search** (Aug 2023)
- Gen App Builder / Discovery Engine → Vertex AI Agent Builder (Apr 2024) → AI Applications (Apr 2025) → Gemini Enterprise Agent Platform (Apr 2026)
- Dialogflow CX → **Conversational Agents** (late 2024)
- Reasoning Engine / LangChain on Vertex AI → **Vertex AI Agent Engine** (Mar 2025)
- Vertex AI Search → **Agent Search** (Apr 2026)

### Deprecations to know (post-Apr 26, 2026 research batch)
- **Vertex Explainable AI** officially deprecated **March 16, 2026**, shutdown **March 16, 2027**. v3.1 still tests Sampled Shapley / Integrated Gradients / XRAI — soak it up but expect retirement-era questions. Per `research/concepts/responsible-ai-security.md`.
- **Vertex AI Feature Store**: both **Legacy** and **Optimized online serving** sunset **Feb 17, 2027** (no new features after May 17, 2026). **Bigtable online serving** is the safe exam answer. A possible "Agent Platform Feature Store" rename is propagating in docs. Per `research/concepts/feature-store.md`.

### Question banks confirmed NOT to exist for PMLE
As of Apr 2026: **Tutorials Dojo / Jon Bonso, ExamPro / Andrew Brown, AnkiHub, AnkiWeb** have no PMLE-specific products. The `PROMPTS.md` P3 prompt was written assuming they did — ignore those entries when running it. The **AndyTheFactory bank** (already on disk at `gcp-pmle-quiz/data/quizzes.jsonl`) is unusually strong: **537 of 841 questions** hit v3.1 GenAI keywords (verified Apr 2026). The 3-bank stack is: official Google sample form (calibration only) + Andy bank (workhorse) + ONE paid bank in Weeks 9–10 (Pluralsight / Whizlabs / vetted Udemy).

### Vertex AI Model Monitoring v1 vs v2
v2 announced **Jun 11, 2024**, still **Pre-GA as of Apr 2026**. Both versions are exam-fair. Key v2 changes: attaches to Model Registry version (not endpoint), supports off-Vertex models (Cloud Run / GKE / multi-cloud), supports on-demand jobs, treats attribution drift as a first-class objective. v1 default drift threshold = **0.3**; v2 SDK examples use much smaller defaults — don't over-memorize 0.3.

### Real-exam format
Recent passers report **zero or near-zero multi-select questions** on the real exam, despite practice banks (incl. Andy) including them. Don't burn time strategy-optimizing for multi-select; practice them only for concept reinforcement.

### High-yield distinguishing topics surfaced by research
- **Reduction Server** — Vertex-AI-only algorithm with documented 75% throughput uplift on NCCL GPU training, no code changes. Single highest-yield distinguishing topic per `research/decision-trees/compute-selection.md`.
- **Skew vs drift one-liner** — *"Skew is training vs production. Drift is production vs production-yesterday."* Memorize this verbatim (per `research/concepts/skew-vs-drift.md`).
- **TPU machine-type naming on Vertex** — `ct5lp-hightpu-{1t,4t,8t}` (v5e), `ct6e-standard` (v6e). v5e/v5p/v6e are safe bets; B200/H200/GB200/A4/Ironwood may not be in v3.1 scope yet.
- **Gemini SFT is LoRA-based PEFT** under the hood. Adapter sizes 1/2/4/8/16. Only 2.5 Pro/Flash/Flash-Lite are tunable. Pro maxes at adapter size 8. Preference tuning (RLHF-style) is Flash and Flash-Lite only.
- **AutoML endpoint scale-to-zero trap** — AutoML endpoints cannot scale to zero; an idle classification endpoint costs **~$991/month**. Common §4 distractor: "deploy AutoML to a Vertex endpoint" when batch prediction would do. Per `research/decision-trees/tabular-modeling.md`.
- **§5 orchestrator cost lever** — Vertex AI Pipelines = **$0.03/run + compute**, no idle cost. Cloud Composer 3 = **$0.06/DCU-hr** with **~$400/month floor** on a small environment. Single biggest input to "which orchestrator?" exam questions. Per `research/decision-trees/pipelines-comparison.md`.

## Working directory
`/Users/patricktaylor/Documents/Google-PMLE/`

## Repo layout
```
.
├── CLAUDE.md                                         # This file (project briefing for Claude sessions)
├── PROMPTS.md                                        # Deep-research prompts (ChatGPT / Gemini / Claude)
├── reddit-advice.md                                  # First anecdotal source (1 Reddit post)
├── professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf   # OFFICIAL exam guide v3.1
├── T-GCPMLE-A-m1-l1-en-file-1.en.pdf                 # Google official course slides (Module 1 Lesson 1)
├── Copy Google Machine Learning Exam Experience.gdoc # Empty placeholder
├── Gmail - An Offer of Admission from Waterloo.pdf   # Unrelated personal doc — ignore
├── research/                                         # (To be created) Deep-research outputs by topic + tool
└── gcp-pmle-quiz/                                    # Cloned: AndyTheFactory/gcp-pmle-quiz (Streamlit, ~841 Qs)
    ├── 🏠_Dashboard.py
    ├── pages/                                        # Quiz Mode, GCP Products map, Edit Questions, Export-for-LM
    ├── data/
    │   ├── quizzes.jsonl                             # 841 questions
    │   ├── gcp_products.jsonl                        # 104 GCP product entries (graph nodes)
    │   └── progress.json                             # autogenerated user progress (correct/wrong per id)
    ├── models/questions.py                           # Pydantic Question schema
    ├── utils/                                        # Loaders, diskcache session
    ├── dashboard.py                                  # Plotly knowledge-gap charts (per gcp_topics / gcp_products / ml_topics)
    ├── pyproject.toml                                # streamlit, pandas, plotly, pyvis, diskcache, pydantic
    └── docker-compose.yaml
```

## Exam blueprint (v3.1, weights from the official guide)
| § | Weight | Domain | Key services |
|---|---|---|---|
| 1 | **13%** | Architecting low-code AI | BigQuery ML, Model Garden, ML APIs, Document AI / Retail API, Vertex AI Agent Builder (RAG), AutoML |
| 2 | **~14%** | Collaborating across teams (data + models) | Cloud Storage, BigQuery, Spanner, Cloud SQL, Spark/Hadoop, Dataflow, TFX, Vertex AI Workbench, Colab Enterprise, Dataproc, Vertex AI Experiments, Kubeflow Pipelines, TensorBoard |
| 3 | **~18%** | Scaling prototypes into ML models | Custom training, Kubeflow on GKE, AutoML, distributed training, hyperparameter tuning, fine-tuning foundation models, CPU/GPU/TPU/edge, Reduction Server, Horovod |
| 4 | **~20%** | Serving and scaling models | Vertex AI online + batch prediction, Dataflow, BigQuery ML, Dataproc, model registry, A/B testing, Feature Store, public/private endpoints, throughput tuning |
| 5 | **~22%** ⭐ | Pipelines + automation (highest weight) | Kubeflow Pipelines, Vertex AI Pipelines, Cloud Composer, MLFlow, TFX, Cloud Build, Jenkins, Vertex AI Experiments, Vertex ML Metadata, lineage |
| 6 | **~13%** | Monitoring AI solutions | Training-serving skew, feature attribution drift, Vertex AI Model Monitoring, Explainable AI, Responsible AI practices, model security |

The exam **does not test coding skill** — Python + SQL literacy is sufficient to read code snippets in questions. Don't waste time deep-diving TensorFlow/PyTorch authoring.

## Question schema (existing app — keep this contract when adding questions)
```json
{
  "id": 103,
  "mode": "single_choice" | "multiple_choice",
  "question": "<HTML or plain text>",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": 3,                       // single_choice: index of correct option
  "answer": [0, 2],                  // multiple_choice: list of indices
  "explanation": "<markdown / HTML>",
  "ml_topics":     ["Model training", "Retraining"],
  "gcp_products":  ["Vertex AI", "Pub/Sub"],
  "gcp_topics":    ["Model deployment", "Model monitoring"]
}
```
When ingesting external question banks: parse → conform to schema → dedupe by question-text hash → continue numbering from the current max `id`. Tag every imported item with `source` (a new optional field) so we can filter quality by origin later.

## Tech stack (starter quiz app)
- Python ≥ 3.10, Streamlit ≥ 1.52
- pandas, plotly, pyvis (graph), pydantic v2, diskcache (session persistence)
- Run: `cd gcp-pmle-quiz && uv sync && uv run streamlit run 🏠_Dashboard.py` (http://localhost:8501)
- Or: `cd gcp-pmle-quiz && docker compose up --build -d`

## Project phases
1. **Research (current)** — execute prompts in `PROMPTS.md` against ChatGPT Deep Research, Gemini Deep Research, and Claude Research. Save each report under `research/<slug>/<tool>.md`. Run every prompt on ≥2 tools for triangulation.
2. **Synthesis** — reconcile reports into:
   - `study_plan.md` — week-by-week 10–12 week roadmap with daily hours, lab assignments, milestones
   - `resources.md` — ranked free + paid resources with date-of-publication and consensus scores
   - `question_banks.md` — assessed banks + ingestion order + dump-site warnings
3. **Question consolidation** — ingest all vetted banks into `gcp-pmle-quiz/data/quizzes.jsonl` (dedupe + tag `source`). Verify each imported question's correct answer against current Google docs before keeping.
4. **Web app build** — decide: extend Streamlit vs rebuild as Next.js (Vercel skills available). Streamlit is fast for analytics dashboards; Next.js is better if we want public sharing or auth.
5. **Study + iterate** — daily quiz batches, weekly retros, gap-driven re-study, full mock exams in weeks 9–12.

## Conventions
- **Recency**: prefer 2024 / 2025 / 2026 sources. Flag anything older than 2023 as "may be stale" — v3.1 (April 2025) added Model Garden, Agent Builder, RAG, foundation-model fine-tuning. Pre-2024 prep guides will miss this.
- **Verification**: before treating any tip as canon, require ≥3 independent sources. Single-anecdote advice goes in a "rumor" bucket.
- **Citations**: every claim in research outputs must cite a URL **with a publication date**.
- **Question vetting**: dump-site banks (Skillcertpro, ExamDumps, parts of ExamTopics) often contain wrong/outdated answers — re-verify against official docs before importing.
- **GCP product names**: use current names only. The "AI Platform → Vertex AI" rename completed in 2022; older content using "AI Platform" terminology should be treated as outdated.

## Out of scope
- Coding-style questions (the exam doesn't test this).
- Deep-learning math from first principles — both partners are math-strong, can skim derivations.
- Other GCP certs (Data Engineer, Cloud Architect) unless cross-referenced as preparatory.
- Anything related to the Waterloo PDF or other unrelated files in the working directory.
- **Strategy-optimizing for multi-select questions** — recent passer reports indicate the real exam has near-zero multi-select even though practice banks include them. Practice MS questions for concept reinforcement only.
- Pre-built **Anki decks** — none of usable quality exist for PMLE as of Apr 2026. Build your own from wrong-answer NotebookLM exports, or skip Anki entirely.

## How future Claude sessions should help
- **Adding questions**: parse, dedupe by question-text hash, conform to the schema above, append to `gcp-pmle-quiz/data/quizzes.jsonl`, increment `id`. Tag with `source`.
- **Building the web app**: don't rebuild blind — first read this file, the latest research outputs, and the existing Streamlit app. Decide extend-vs-rebuild based on what already works.
- **Exam-content questions**: ground answers in the v3.1 exam guide PDF + current Google Cloud docs (use Context7 / WebFetch for fresh docs). Never rely on training-cutoff knowledge for product features — Vertex AI ships changes monthly.
- **Tutoring mode**: Socratic for math-strong learners — ask leading questions, draw analogies to linear algebra / optimization / statistics, verify with official docs at the end.
- **Research mode**: when the user asks "what's the best X", check `research/` first, then `PROMPTS.md` to see if a prompt already covers it.

## Key external links to know
- Official exam page: https://cloud.google.com/learn/certification/machine-learning-engineer
- Google Skills ML Engineer Learning Path: https://www.skills.google/paths/17 (formerly Cloud Skills Boost — renamed Oct 2025; old URL 308-redirects)
- Free Google practice exam: linked from the official cert page
- Existing community quiz app source: https://github.com/AndyTheFactory/gcp-pmle-quiz
