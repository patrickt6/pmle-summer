# PMLE Project TODO List

A phased checklist covering the full 12-week project: setup → research → web app → study → exam.
Phase 4 is the recurring weekly cadence — every other phase is one-time.

Check items off in this file (or surface them in the Streamlit app once Phase 3 ships).

---

## Next session — pick one (or stack in order)

These are the concrete moves at the start of any future Claude Code session in this directory:

**1. ~~Spawn the next research batch.~~ ✅ DONE 2026-04-26.** All 8 Phase 1 reports landed (~34,940 words). `study_plan.md` and `CLAUDE.md` patched. See git log / file list under `research/`.

**2. Execute Phase 2 question consolidation.** Full spec + paste-ready fresh-session prompt: **`phase2-question-consolidation.md`** at the repo root. Adds `source` / `exam_section` / `mock_pool` Pydantic fields, migrates the 841 Andy questions with a heuristic section-mapping, builds the rebrand-translation JSON, tags 200 questions into `mock1-pool` / `mock2-pool`. Estimated 1.5–2.5 agent-hours. Unblocks the MVP "Weekly homework view".

**3. Read `study_plan.md` and `TODOLIST.md` together with your friend.** Confirm the cadence (daily 45–60 min, Sat 90-min lab, Sun 60-min retro) fits both schedules. Lock the 12-week start date and book the real exam (Pearson VUE / OnVUE) for Saturday Week 12.

Recommendation: **#1 now** — 8 background agents spend wall-clock web-research time while you and your friend read docs and decide cadence.

### Paste-ready prompt for option 1 (fresh Claude Code session, zero prior context)

Open a fresh Claude Code session in `/Users/patricktaylor/Documents/Google-PMLE/`. `CLAUDE.md` auto-loads. Paste the block below:

~~~
You're starting a fresh session in /Users/patricktaylor/Documents/Google-PMLE/. CLAUDE.md auto-loads and gives full project context — read it first if not already in your system reminder.

Single task this session: execute Phase 1 of TODOLIST.md — spawn 8 background research sub-agents in parallel, each producing one focused .md report under research/.

Steps:

1. Read TODOLIST.md (Phase 1 section), PROMPTS.md (the "Post-research updates" header + "Constants" block), and ONE existing report (e.g. research/concepts/skew-vs-drift.md or research/decision-trees/compute-selection.md) so you internalize the report template: precise definitions, comparison tables, Mermaid decision trees where applicable, 5 sample exam questions in JSONL schema, References list, Confidence + Decay-risk notes at end.

2. Run `mkdir -p research/concepts research/decision-trees` (idempotent — they may already exist).

3. Create 8 tasks via TaskCreate (one per agent below), then mark each in_progress when you spawn its agent.

4. Spawn all 8 sub-agents in parallel — single message, 8 Agent tool calls, each with subagent_type: general-purpose, run_in_background: true. Each prompt MUST be self-contained because agents have zero memory of this session.

The 8 topics (full one-line scope in TODOLIST.md Phase 1):

A. HIGH PRIORITY — §5 Pipelines decision tree → research/decision-trees/pipelines-comparison.md
   Vertex AI Pipelines vs Kubeflow Pipelines vs Cloud Composer; TFX components mini-reference; CI/CD via Cloud Build vs Jenkins. §5 is 22% — highest exam weight.

B. HIGH PRIORITY — Tabular modeling decision tree → research/decision-trees/tabular-modeling.md
   BigQuery ML vs AutoML Tables vs Vertex AI custom training. Data sizes, model complexity, integration, cost, time-to-deploy. Decision flowchart in Mermaid.

C. §5.3 Metadata + lineage → research/concepts/metadata-lineage.md
   Vertex AI Experiments vs Vertex ML Metadata; dataset / model versioning; Pipeline lineage; MLflow-on-GCP if relevant.

D. §4 Serving deep dive → research/concepts/serving-deep-dive.md
   Batch vs online vs Dataflow vs BigQuery ML inference; A/B testing on Vertex AI endpoints; model registry patterns; throughput tuning; private endpoints.

E. §6.1 Responsible AI + model security → research/concepts/responsible-ai-security.md
   Fairness, bias, model exfiltration, prompt injection, Google's Responsible AI principles, security against unintended exploitation.

F. §3.2 Hyperparameter tuning → research/concepts/hyperparameter-tuning.md
   Vertex AI Vizier; grid / random / Bayesian; population-based training; parallel trials; trial budgeting.

G. Vertex AI Feature Store → research/concepts/feature-store.md
   Online + offline; ingestion patterns; point-in-time joins; batch vs streaming; cost-vs-ad-hoc-BigQuery-features tradeoff.

H. GCP IAM for ML → research/concepts/iam-for-ml.md
   Custom service accounts; predefined roles for ML; VPC-SC; private endpoints; Workload Identity.

Each agent prompt MUST include:
- Audience: two beginners, math-strong, no prior GCP/ML production experience, 10–12 week PMLE v3.1 prep.
- Rebrand alerts: Vertex AI rebranded to Gemini Enterprise Agent Platform on Apr 22 2026 at Cloud Next 2026; the v3.1 exam guide and Skills Boost still use old names. Translate function-first when answer-choice names look unfamiliar. Doc URLs prefer docs.cloud.google.com (Google migrated the host in 2026; cloud.google.com 301-redirects).
- Citation requirement: URL + access date for every non-trivial claim, prefer 2024–2026 sources, flag any pre-2023.
- Output spec: Markdown with H2/H3, tables for ≥3-way comparisons, Mermaid for decision trees, 5 sample exam questions in this exact JSONL schema (one valid JSON object per line):
  {"id": <int starting at 1>, "mode": "single_choice", "question": "...", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": <0-3>, "explanation": "...", "ml_topics": [...], "gcp_products": [...], "gcp_topics": [...]}
  Each explanation MUST explain why the right answer wins AND why each wrong answer is a trap.
- End with a Confidence section (High/Medium/Low per major claim) and a Decay-risk note.
- Target 1500–2500 words for narrow topics (B, C, F, G, H), up to 3000 for broader ones (A, D, E).

5. After spawning, end your turn with a clean table summarizing the 8 agents + their output paths. Do NOT poll or sleep — completion notifications arrive automatically.

6. As each completion notification arrives:
   - TaskUpdate that task to completed
   - Run `wc -l -w` on the output file to verify it landed
   - Surface 2–3 key findings in 3–5 sentences

7. When all 8 land, propose patches to study_plan.md (replace the `(TODO research/decision-trees/...)` markers with real links) and to CLAUDE.md (any new rebrands or contradictions discovered). Apply patches when approved.

8. End-of-session: surface Phase 2 (question consolidation) as the natural next move.
~~~

---

## Phase 0 — Setup (Week 0, before Day 1)

### Both partners
- [ ] Read `CLAUDE.md`, `PROMPTS.md`, `study_plan.md`, and all 6 `research/*.md` files (~2.5 hours)
- [ ] Create GCP account, claim **$300 free trial credit**. Note 90-day expiry on a calendar.
- [ ] Sign up for **Google Skills Starter** (free tier; 35 monthly credits at `skills.google`)
- [ ] Sign up for **Google Cloud Innovators** community (extra 35 monthly credits, free)
- [ ] Take Google's free official sample exam **cold** — record baseline score in `progress.json` notes
- [ ] Run `gcp-pmle-quiz` Streamlit app locally:
  ```bash
  cd gcp-pmle-quiz && uv sync && uv run streamlit run 🏠_Dashboard.py
  ```
- [ ] Confirm 841 questions load + dashboard renders

### Joint
- [ ] Lock 12-week start date (Day 1 = first Monday after setup completes)
- [ ] Calendar daily 45–60 min slots + Saturday 90-min lab + Sunday 60-min retro (12 weeks worth)
- [ ] Decide accountability cadence — daily 5-min text? Daily call?
- [ ] **Book real exam** for Saturday of Week 12 (Pearson VUE or OnVUE) — early booking locks slot
- [ ] Decide single shared shared notes location (Notion / Google Doc / shared markdown in repo)
- [ ] (Optional) Schedule a `/schedule` agent to nudge re: Pro trial start in 4 weeks

---

## Phase 1 — Research finalization (Week 1, parallel with study Week 1)

Spawn the next batch of focused research sub-agents. Each scoped narrowly, each saves to `research/<slug>/<file>.md`. Use `Agent` tool with `subagent_type: general-purpose` and `run_in_background: true`. Mirror the structure of the existing 6 (constants block + citation rules + JSONL sample Qs + confidence/decay notes).

### Highest priority — fills explicit gaps in the 12-week plan
- [ ] **§5 Pipelines decision tree** → `research/decision-trees/pipelines-comparison.md`
  *Vertex AI Pipelines vs Kubeflow Pipelines vs Cloud Composer; TFX components mini-reference; CI/CD with Cloud Build vs Jenkins. §5 is 22 % — highest exam weight.*
- [ ] **Tabular modeling decision tree** → `research/decision-trees/tabular-modeling.md`
  *BigQuery ML vs AutoML Tables vs Vertex AI custom training; data sizes, model complexity, integration, cost, time-to-deploy.*

### High priority — direct §-by-§ deep dives
- [ ] **§5.3 Metadata + lineage** → `research/concepts/metadata-lineage.md`
  *Vertex AI Experiments vs Vertex ML Metadata; dataset / model versioning; Pipeline lineage; MLflow on GCP.*
- [ ] **§4 Serving deep dive** → `research/concepts/serving-deep-dive.md`
  *Batch vs online vs Dataflow vs BigQuery ML inference; A/B testing on Vertex AI; model registry patterns; throughput tuning; private endpoints.*
- [ ] **§6.1 Responsible AI / model security** → `research/concepts/responsible-ai-security.md`
  *Fairness, bias, model exfiltration, prompt injection, Google's Responsible AI principles, security against unintended exploitation.*
- [ ] **§3.2 Hyperparameter tuning** → `research/concepts/hyperparameter-tuning.md`
  *Vertex AI Vizier; grid / random / Bayesian; population-based training; parallel trials; budgeting trials.*
- [ ] **Vertex AI Feature Store** → `research/concepts/feature-store.md`
  *Online + offline; ingestion patterns; PIT joins; batch vs streaming; cost vs ad-hoc BigQuery features.*
- [ ] **GCP IAM for ML** → `research/concepts/iam-for-ml.md`
  *Custom service accounts, predefined roles for ML, VPC-SC, private endpoints, Workload Identity.*

### After all complete
- [ ] Run reconciliation: read all 8 new reports + the original 6, update `study_plan.md` with new decision-tree references
- [ ] Update `CLAUDE.md` with any new rebrands or contradictions discovered
- [ ] Possibly add `research/_reconciled/canonical.md` if the 14 reports surface enough conflicts to need it

---

## Phase 2 — Question consolidation (Weeks 1–3, parallel with study)

### Schema enhancement
- [ ] Add optional `source` field to Question Pydantic model (`gcp-pmle-quiz/models/questions.py`)
- [ ] Add optional `exam_section` field tied to v3.1 (§1.1, §1.2, §2.1, …, §6.2)
- [ ] Migrate existing 841 records: set `source: "AndyTheFactory"`, infer `exam_section` from `gcp_topics` / `ml_topics` heuristically

### Andy bank quality verification
- [ ] Spot-check 30 random GenAI-flagged Andy questions against current Apr 2026 product names (rebrand-aware)
- [ ] Build `gcp-pmle-quiz/data/rebrands.json` — old → new product-name mapping
- [ ] Streamlit UI overlay: when a question references "Vertex AI Agent Builder", show "(now Gemini Enterprise Agent Platform)" inline (gracefully — don't break old questions)

### Add Google's official sample exam
- [ ] Manually transcribe ~25 Qs from Google's free sample form into JSONL with `source: "Google Sample"` and `exam_section` per item
- [ ] Re-take Google sample form periodically (every 4 weeks) to track delta vs baseline

### Plan paid bank addition for Week 9–10
- [ ] Decide: Pluralsight / A Cloud Guru subscription (if available) **OR** Whizlabs Premium (~$15) **OR** top-rated Udemy practice course (~$15)
- [ ] When Week 9 starts: add ~50 vetted Qs from chosen bank with `source: "<bank-name>"`, spot-check accuracy against official docs before commit

### Mock exam preparation (do during Phase 2 so the pools are ready by Week 11)
- [ ] Tag 100 Qs as `mock1-pool` (held out, never surfaced in normal quiz mode)
- [ ] Tag 100 Qs as `mock2-pool` (different held-out set)
- [ ] Build mock exam page in Streamlit: random 50 Qs from pool, 2-hour timer, no explanations until submit, score breakdown by §

---

## Phase 3 — Web app build (Weeks 1–3, parallel)

### Decision: extend Streamlit or rebuild Next.js?

**Recommendation:** extend Streamlit Weeks 1–2 (fast prototype with the 841 Qs already loaded). Re-evaluate end of Week 2.

| | Streamlit (extend) | Next.js (rebuild) |
|---|---|---|
| Speed | ✅ Already runs, 841 Qs loaded | ❌ Days of scaffolding |
| Multi-user | ❌ Single user | ✅ Auth via Clerk (Vercel Marketplace) |
| Mobile | ⚠️ Usable, ugly | ✅ Mobile-first |
| Sharing | ❌ Local only | ✅ Vercel deploy |
| Data | ✅ JSONL files | ⚠️ Migrate to Postgres / Neon |
| Analytics | ✅ Plotly already built | ❌ Rebuild from scratch |

- [ ] Decide approach end of Week 2 — default = stay on Streamlit, switch only if accountability features become critical

### Streamlit feature backlog (priority order)
- [ ] ⭐ **MVP — Weekly homework view** (explicitly requested by user, 2026-04-26). The partners' landing page: open the app, see "Week N — here's your homework". Reads `study_plan.md`, computes current week from the locked Day-1 date, renders for that week: theme, target hours, the Skills Boost item(s), the decision-tree refresher links, the weekend lab, the topic tags for self-assessment Qs. One-click "start this week's quiz" button that filters Qs by the week's topic tags. This is the smallest possible thing that lets you and your friend wake up and know what to study without rereading any markdown.
- [ ] **Per-user progress isolation** — currently `data/progress.json` is single-user; add user selector + per-user JSON files
- [ ] **Daily check-in / streak counter** — small persistent widget showing both partners' current streaks
- [ ] **Mock exam mode** — separate page, 50-Q timed quiz, no explanations until submit, results-by-section
- [ ] **Decision-tree pages** — render `research/decision-trees/*.md` files inline (`st.markdown`)
- [ ] **Rebrand-translation overlay** — read `data/rebrands.json`, annotate questions with old → new product names
- [ ] **Topic-of-week filter** — quiz mode filter by `exam_section` field (added in Phase 2)
- [ ] **Sunday retro form** — captures "1 learned / 1 stuck / 1 ahead" per partner, persists to disk (one JSON per week)
- [ ] **NotebookLM export refresh** — current export only does wrongs; add a "weekly digest" mode (this week's wrongs + topic summaries)
- [ ] **Cheatsheet view** — render decision-tree summaries + skew-vs-drift one-liner + Reduction Server fact + TPU naming as a single printable page

### Next.js port (only if decided to switch)
- [ ] Spawn `frontend-design:frontend-design` skill or `vercel:next-forge` skill for scaffolding
- [ ] Migrate JSONL → Postgres (Neon, via Vercel Marketplace)
- [ ] Auth via Clerk (Vercel Marketplace)
- [ ] Deploy to Vercel preview, then prod after Week 4
- [ ] Same backlog as Streamlit + shareable progress URL + push notifications for daily check-in

---

## Phase 4 — Study Weeks 1–12 (recurring; mirrors `study_plan.md`)

### Daily (Mon–Fri)
- [ ] 45–60 min focused study (alternate active learning vs active recall)
- [ ] 5-min sync with partner (text / Slack OK)

### Friday
- [ ] Paired quiz session, 30 min, week's topic-of-week tag

### Saturday
- [ ] 90-min paired lab session (one reads, one types — switch every 30 min)
- [ ] Push one "ohhh" insight per person to shared notes

### Sunday
- [ ] 60-min retro: weekly self-assessment quiz + wrong-answer review
- [ ] Each partner: 1 learned / 1 stuck / 1 ahead
- [ ] Set Monday's first 30-min focus
- [ ] Update `progress.json` (commit if Streamlit synced via git)

---

## Phase 5 — Mock exam phase (Weeks 11–12)

### Week 11
- [ ] **Saturday: Mock #1** — full 2 hours, 50 Qs from `mock1-pool`
- [ ] Same evening: review every wrong answer (do not skip!)
- [ ] Identify weakest 3 sections (compare against §1–§6 weights)
- [ ] Schedule Tue / Wed / Thu wrong-answer drilling on weak sections only

### Week 12
- [ ] **Wednesday: Mock #2** — full 2 hours, 50 Qs from `mock2-pool`
- [ ] Target ≥ 80 % (buffer above the 70 % real-exam threshold)
- [ ] Final personal-cheatsheet review (Friday before exam)
- [ ] Print or save the decision-tree summaries + Reduction Server fact + skew-vs-drift one-liner

### Exam-day prep (Friday before)
- [ ] Confirm exam booking 24 h before (Pearson VUE or OnVUE)
- [ ] ID, water, snack, biobreak rules clarified
- [ ] Pacing rule: 50 Qs / 120 min ≈ 2.4 min/Q. Flag-and-return for hard ones.
- [ ] **Translate function-first when product names look unfamiliar** (rebrand awareness)

---

## Phase 6 — Exam day + post-exam

- [ ] Take exam (Saturday Week 12)
- [ ] Same day: write debrief while fresh — top 5 surprises, top 5 traps, what helped most
- [ ] If both pass: celebrate. Optional give-back: post a 2026 passer writeup to r/googlecloud (we mined the community for ours).
- [ ] If either fails: 14-day waiting period before retake. Adjust plan based on debrief.

---

## Maintenance / calendar tasks (recurring during the 12 weeks)

- [ ] **Every 6 weeks**: re-run question-bank audit prompt (P3) — check if Tutorials Dojo / ExamPro launched a PMLE product, check if AndyTheFactory bank updated
- [ ] **Every 6 weeks**: re-run anecdotes audit (P4) — new passer reports, new traps
- [ ] **Every 6 weeks**: re-run resource audit (P2) — courses updated, prices changed
- [ ] **Watch** for v3.2 exam guide announcement — would invalidate parts of plan; check `cloud.google.com/learn/certification/machine-learning-engineer` monthly
- [ ] **Watch** for further rebrands as Vertex AI → Gemini Enterprise Agent Platform rolls through documentation
- [ ] Set a `ScheduleWakeup` or `/schedule` agent to remind: "Pro trial timing — Day 1 of Week 4" once Phase 0 setup completes

---

## Open decisions (TBD, decide as you go)

- [ ] **Auth + hosting model** for the web app (Streamlit Cloud / Vercel / local-only)
- [ ] **Sync mechanism** for two-person progress (git commits / shared filesystem / proper DB)
- [ ] **Anki?** No PMLE deck of usable quality exists; would have to build. Default = NO unless we have spare cycles in Week 12.
- [ ] **Public release**: open-source the consolidated bank + study app after passing? Default = YES, give back via PR to AndyTheFactory.
- [ ] **Streamlit vs Next.js** rebuild: defer until end of Week 2 (decided in Phase 3)

---

## Quick-reference: the seven cross-cutting findings to internalize

1. **Vertex AI → Gemini Enterprise Agent Platform** (Apr 22, 2026). Translate function-first.
2. **Cloud Skills Boost → Google Skills** (Oct 2025). New domain `skills.google`.
3. **Docs URL** `cloud.google.com` → `docs.cloud.google.com` (301).
4. **Tutorials Dojo + ExamPro + Anki decks don't exist for PMLE.** Stop looking.
5. **60–75 hour study budget** (not 200+). 25 / 25 / 50 split (path / docs / practice).
6. **GenAI weight = ~8–12 %** of exam. Don't over-weight.
7. **Real exam has near-zero multi-select** despite practice banks including them.
