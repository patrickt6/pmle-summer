# Phase 2 — Question Consolidation Spec

**Date authored:** 2026-04-26 (immediately after Phase 1 finished)
**Estimated agent time:** 1.5–2.5 hours
**Depends on:** Phase 1 complete (✅ all 14 research reports landed)
**Unblocks:** Phase 3 MVP "Weekly homework view" (needs `exam_section`), Mock #1/#2 (Weeks 11–12)

---

## 1. Mission

Convert the existing **841-question Streamlit bank** into a properly-tagged consolidated bank that supports:

1. The **Phase 3 MVP "Weekly homework view"** — needs `exam_section` to scope per-week quizzes to the current week's blueprint section.
2. **Mock exam pools** held out from normal study so Mock #1 / #2 keep calibration value in Weeks 11–12.
3. **Rebrand-aware question display** — the Apr 22, 2026 Vertex AI → Gemini Enterprise Agent Platform rename + ten earlier renames documented in `CLAUDE.md`.

## 2. Why this matters

| Without | Consequence |
|---|---|
| `exam_section` field | Cannot filter the weekly quiz by current week's blueprint section — MVP unbuildable |
| Mock pool tags | Mock #1 / #2 questions leak into normal study, lose calibration value, mock score is biased upward |
| Rebrand JSON | Questions referencing 2024–2025 product names look outdated; learners second-guess correct answers because product was renamed |

## 3. Pre-flight (do BEFORE editing anything)

Read these files in order:

1. `CLAUDE.md` — full project context + rebrand alerts + April 2026 deprecations
2. `gcp-pmle-quiz/models/questions.py` — current Pydantic schema (you'll extend it)
3. First 5 lines of `gcp-pmle-quiz/data/quizzes.jsonl` (use `head -5`) — see actual record shape
4. `study_plan.md` Weeks 11–12 — the mock exam dependency on `mock_pool` tags
5. `research/genai/vertex-ai-overview.md` — full rename history (your source for `rebrands.json`)
6. `gcp-pmle-quiz/pages/` — list to find the quiz-mode page that will need a filter update

Verify the Python env is clean (one-time, no need to actually run the server):

```bash
cd gcp-pmle-quiz && uv sync
```

## 4. The four moves — execute in order

There are **dependencies**:
- Move 1 (schema) **must precede** Move 2 — pydantic validation will fail otherwise.
- Move 2 (sets `exam_section`) **must precede** Move 4 — mock pools are stratified by section.
- Move 3 (rebrands.json) is **independent** — can run any time after Move 1.

Suggested order: **1 → 2 → 3 → 4**.

---

## Move 1 — Schema enhancement

### What
Add three optional fields to the Pydantic Question model in `gcp-pmle-quiz/models/questions.py`:

```python
source: str | None = Field(
    default=None,
    description="Bank source: 'AndyTheFactory', 'Google Sample', 'Whizlabs', etc.",
)
exam_section: str | None = Field(
    default=None,
    description=(
        "PMLE v3.1 section. Allowed: §1.1, §1.2, §2.1, §2.2, §2.3, "
        "§3.1, §3.2, §3.3, §3.4, §4.1, §4.2, §4.3, §5.1, §5.2, §5.3, §6.1, §6.2."
    ),
)
mock_pool: list[str] | None = Field(
    default=None,
    description=(
        "Mock pool tags. Allowed values: 'mock1-pool', 'mock2-pool'. "
        "Default null = available for normal quiz mode."
    ),
)
```

All three are **optional with default `None`** so existing 841 records still validate without migration.

### Verification
- Existing JSONL still loads: from the `gcp-pmle-quiz` directory, run
  ```bash
  uv run python -c "from utils.loaders import load_questions; print(len(load_questions()))"
  ```
  (substitute the actual loader function — read `utils/` first to find it). Expected: `841`.
- A synthetic question with all three new fields validates without error.
- A synthetic question with none of the three new fields also validates (backwards compat).

---

## Move 2 — Migrate 841 Andy questions

### What
Write `gcp-pmle-quiz/scripts/migrate_phase2.py` that:

1. **Audit step (run first, print only):** dump unique values seen in `gcp_topics`, `ml_topics`, `gcp_products` across all 841 records. You'll use this to refine the heuristic rules below before applying them.
2. **Apply step:** for each record:
   - Set `source = "AndyTheFactory"` (we already know all 841 came from this bank — `CLAUDE.md` confirms it).
   - Infer `exam_section` from existing tags using the heuristic in `gcp-pmle-quiz/data/section-mapping.json` (you'll create this file too).
   - Leave `mock_pool` as `None` — Move 4 will set it.
3. Write back atomically: write to `quizzes.jsonl.tmp`, then `os.replace()` over the original.
4. Print a **summary** at the end:
   - Total records processed
   - Per-section counts
   - Number with `exam_section: null` (heuristic failures — keep < 10%)

### Heuristic mapping — `gcp-pmle-quiz/data/section-mapping.json`

Starting rules (refine after the audit step):

```json
{
  "as_of": "2026-04-26",
  "rules": [
    {"section": "§5.3", "match_any_in": "gcp_products", "patterns": ["Vertex AI Experiments", "Vertex ML Metadata"]},
    {"section": "§5.2", "match_any_in": "gcp_topics", "patterns": ["retraining", "CI/CD", "Cloud Build", "Jenkins"]},
    {"section": "§5.1", "match_any_in": "gcp_products", "patterns": ["Vertex AI Pipelines", "Kubeflow Pipelines", "Cloud Composer", "TFX", "MLFlow"]},
    {"section": "§6.2", "match_any_in": "ml_topics", "patterns": ["Model Monitoring", "drift", "skew", "training-serving"]},
    {"section": "§6.1", "match_any_in": "ml_topics", "patterns": ["Responsible AI", "fairness", "bias", "Explainable AI", "model security", "prompt injection"]},
    {"section": "§4.3", "match_any_in": "gcp_topics", "patterns": ["throughput", "latency", "private endpoint", "PSC", "Private Service Connect"]},
    {"section": "§4.2", "match_any_in": "gcp_topics", "patterns": ["Model Registry", "A/B testing", "Feature Store", "endpoint"]},
    {"section": "§4.1", "match_any_in": "gcp_topics", "patterns": ["batch prediction", "online prediction", "Dataflow inference", "BQML inference"]},
    {"section": "§3.3", "match_any_in": "gcp_topics", "patterns": ["GPU", "TPU", "Reduction Server", "Horovod", "compute selection", "edge"]},
    {"section": "§3.2", "match_any_in": "ml_topics", "patterns": ["hyperparameter tuning", "Vizier", "fine-tuning"]},
    {"section": "§3.1", "match_any_in": "ml_topics", "patterns": ["custom training", "Kubeflow on GKE", "AutoML training", "distributed training"]},
    {"section": "§2.3", "match_any_in": "ml_topics", "patterns": ["evaluation", "GenAI eval"]},
    {"section": "§2.2", "match_any_in": "gcp_products", "patterns": ["Vertex AI Workbench", "Colab Enterprise", "Dataproc"]},
    {"section": "§2.1", "match_any_in": "gcp_products", "patterns": ["Cloud Storage", "Spanner", "Cloud SQL", "Spark", "Hadoop"]},
    {"section": "§1.2", "match_any_in": "gcp_topics", "patterns": ["Model Garden", "ML APIs", "Document AI", "Retail API", "Agent Builder", "RAG"]},
    {"section": "§1.1", "match_any_in": "gcp_products", "patterns": ["BigQuery ML", "BQML", "AutoML"]}
  ],
  "match_semantics": "First rule that matches wins. Rules are listed in priority order — higher-weight or more-specific sections come first to break ties (e.g. §5.3 before §5.1)."
}
```

**Implementation note:** treat patterns as **case-insensitive substring** matches against any string in the named field, not exact equality. Many Andy-bank tags are lowercase or differently-capitalized.

### Verification
- Total records still **841** (no data loss).
- `exam_section: null` count **< 84** (10% threshold). If higher, refine rules using the audit output and re-run.
- Distribution roughly matches v3.1 weights (allow ±5 percentage-point slack):

  | Section | Target % | Target count (of 841) | Acceptable range |
  |---|---|---|---|
  | §1 | 13% | 109 | 67–151 |
  | §2 | 14% | 118 | 76–160 |
  | §3 | 18% | 151 | 109–193 |
  | §4 | 20% | 168 | 126–210 |
  | §5 | 22% | 185 | 143–227 |
  | §6 | 13% | 109 | 67–151 |

- **Manual spot-check:** open 10 random questions in the Streamlit app and read them. Does the inferred `exam_section` match what you'd assign by hand? Target: ≥7/10. If <7, refine rules and re-run.
- Idempotency: running the migration script twice on the same input should produce identical output the second time. Add an `if record.exam_section is None` guard before overwriting.

---

## Move 3 — Build `rebrands.json`

### What
Create `gcp-pmle-quiz/data/rebrands.json` from the rename history in `CLAUDE.md` "Specific renames worth memorizing" + `research/genai/vertex-ai-overview.md`.

### Schema

```json
{
  "as_of": "2026-04-26",
  "rebrands": [
    {
      "old": "Vertex AI Agent Builder",
      "new": "Gemini Enterprise Agent Platform",
      "rebranded_at": "2026-04-22",
      "context": "Announced at Cloud Next 2026 keynote. Function-first translate when answer choices use either name."
    },
    {
      "old": "AI Applications",
      "new": "Gemini Enterprise Agent Platform",
      "rebranded_at": "2026-04-22",
      "context": "Was already a re-rebrand from 'Vertex AI Agent Builder' (Apr 2025). Now renamed again."
    },
    {
      "old": "Vertex AI Search",
      "new": "Agent Search",
      "rebranded_at": "2026-04-22"
    },
    {
      "old": "Vertex AI Studio",
      "new": "Agent Platform Studio",
      "rebranded_at": "2026-04-22"
    },
    {
      "old": "Cloud Skills Boost",
      "new": "Google Skills",
      "rebranded_at": "2025-10-15",
      "context": "Domain cloudskillsboost.google → skills.google (308 redirects). Path /paths/17 unchanged."
    },
    {
      "old": "Reasoning Engine",
      "new": "Vertex AI Agent Engine",
      "rebranded_at": "2025-03-01",
      "context": "Was 'LangChain on Vertex AI' before that."
    },
    {
      "old": "LangChain on Vertex AI",
      "new": "Vertex AI Agent Engine",
      "rebranded_at": "2025-03-01"
    },
    {
      "old": "Dialogflow CX",
      "new": "Conversational Agents",
      "rebranded_at": "2024-11-01"
    },
    {
      "old": "Matching Engine",
      "new": "Vector Search",
      "rebranded_at": "2023-08-01"
    },
    {
      "old": "AI Platform",
      "new": "Vertex AI",
      "rebranded_at": "2022-05-15",
      "context": "Pre-2024 study material may still use 'AI Platform' — treat as outdated."
    },
    {
      "old": "Discovery Engine",
      "new": "Vertex AI Agent Builder",
      "rebranded_at": "2024-04-01",
      "note": "Subsequently rebranded twice — current name is 'Gemini Enterprise Agent Platform'."
    },
    {
      "old": "Gen App Builder",
      "new": "Vertex AI Agent Builder",
      "rebranded_at": "2024-04-01",
      "note": "Subsequently rebranded twice — current name is 'Gemini Enterprise Agent Platform'."
    }
  ]
}
```

### Verification
- File loads as valid JSON: `python -c "import json; print(len(json.load(open('gcp-pmle-quiz/data/rebrands.json'))['rebrands']))"`. Expected: ≥10.
- All entries from `CLAUDE.md` "Specific renames worth memorizing" are present.
- No duplicate `old` keys (the `Gen App Builder` and `Discovery Engine` entries are distinct olds → same intermediate new — that's fine, it's two different old names not a duplicate).

**Out of scope here:** wiring this into the Streamlit UI as an inline overlay. That's a Phase 3 task. We just produce the data file.

---

## Move 4 — Tag mock pools

### What
Stratified-sample 100 questions for `mock1-pool` and 100 for `mock2-pool` from non-overlapping sets. Tag in `quizzes.jsonl` via the `mock_pool` field.

### Strategy

1. Read all questions, group by `exam_section` (use the values from Move 2). Skip questions with `exam_section: null`.
2. Compute target counts per pool using v3.1 weights:

   | Section | Per-pool target |
   |---|---|
   | §1 | 13 |
   | §2 | 14 |
   | §3 | 18 |
   | §4 | 20 |
   | §5 | 22 |
   | §6 | 13 |
   | **Total** | **100** |

   (When a section has multiple sub-sections like §1.1/§1.2, distribute the target proportionally; if you can't, just sample within the parent section.)

3. For each section: shuffle with a **fixed seed** (`random.seed(42)`), take first N for `mock1-pool`, next N for `mock2-pool`. Sets are disjoint by construction.
4. Write `mock_pool: ["mock1-pool"]` or `mock_pool: ["mock2-pool"]` on the chosen records. Atomic write same as Move 2.

### Streamlit filter update — DO this same session

Find `gcp-pmle-quiz/pages/` quiz pages (use `Grep` for `mock_pool` to confirm none exist yet). The default quiz mode should **exclude** mock-pool questions so they stay held-out:

```python
# In the quiz page loader, BEFORE shuffling/serving:
questions = [q for q in questions if not q.mock_pool]
```

Add a TODO comment near the filter pointing to a future "Mock Exam" page (Phase 3) that will surface only `mock_pool == ["mock1-pool"]` or `["mock2-pool"]` in a timed mode.

### Verification
- `mock1-pool` has exactly **100** entries; `mock2-pool` has exactly **100** entries.
- `mock1-pool ∩ mock2-pool = ∅` — no question ID appears in both pools.
- Per-section distribution matches the table above ±2 questions per section.
- Streamlit quiz mode count: load `quizzes.jsonl` and filter out mock pools → expected `841 - 200 = 641` questions in normal-mode rotation.
- Reproducibility: re-run Move 4 with the same seed → same 200 IDs assigned to the same pools.

---

## 5. Out of scope this session

These are intentionally deferred:

- **MVP weekly homework view** — Phase 3, separate session. Phase 2 only delivers the schema dependency.
- **Google Sample form transcription** (~25 questions) — separate manual session.
- **Paid bank addition** (Whizlabs / Pluralsight / Udemy ~50 vetted questions) — Week 9 task.
- **Rebrand-translation overlay in Streamlit UI** — Phase 3 (reads the `rebrands.json` produced here).
- **Per-user progress isolation** — Phase 3.

## 6. End-of-session deliverables checklist

- [ ] `gcp-pmle-quiz/models/questions.py` — schema extended with 3 new optional fields
- [ ] `gcp-pmle-quiz/data/quizzes.jsonl` — all 841 records have `source = "AndyTheFactory"`, ≥90% have non-null `exam_section`, exactly 200 have `mock_pool` set
- [ ] `gcp-pmle-quiz/data/section-mapping.json` — heuristic rules used by the migration
- [ ] `gcp-pmle-quiz/data/rebrands.json` — ≥10 rebrand entries
- [ ] `gcp-pmle-quiz/scripts/migrate_phase2.py` — committed migration script (idempotent)
- [ ] Streamlit quiz mode default excludes mock-pool questions (one-line filter added)
- [ ] Final summary printed: per-section counts, mock pool sizes, rebrand entry count, any orphan questions with `exam_section: null`

## 7. Constraints (the agent MUST follow)

- **Do NOT change existing question records' content fields** (`question`, `options`, `answer`, `explanation`). Only ADD new fields.
- **Do NOT delete `gcp-pmle-quiz/data/progress.json`** — it has user state (current quiz progress).
- **Use a fixed random seed (42)** for mock pool sampling so the result is reproducible across re-runs.
- **Make the migration script idempotent** — running it twice should not change records the second time. Use `if record.field is None` guards.
- **Atomic writes only** — write to `.tmp` then `os.replace()`. Never partial-write `quizzes.jsonl` directly.
- **Stop and ask** if `exam_section` inference accuracy on a 10-question manual spot-check is below 70% — that means the heuristic needs more design work and shouldn't be applied to the whole bank yet.

---

## 8. Paste-ready prompt for fresh Claude Code session

Open a **fresh** Claude Code session in `/Users/patricktaylor/Documents/Google-PMLE/` (run `/clear` if continuing in an existing terminal). `CLAUDE.md` auto-loads. Paste the block below verbatim:

~~~
You're starting a fresh session in /Users/patricktaylor/Documents/Google-PMLE/. CLAUDE.md auto-loads and gives full project context — read it first if not already in your system reminder.

Single task this session: execute Phase 2 — question consolidation. The complete spec lives in `phase2-question-consolidation.md` at the repo root. Read it cover-to-cover before doing anything else; it defines goals, four moves (schema → migration → rebrands.json → mock pool tagging), heuristic mapping rules, exact file paths, and verification criteria.

Steps:

1. Read `phase2-question-consolidation.md` cover-to-cover.

2. Read the pre-flight files listed in §3 of that spec: CLAUDE.md, gcp-pmle-quiz/models/questions.py, first 5 lines of gcp-pmle-quiz/data/quizzes.jsonl (use `head -5` via Bash), study_plan.md (Week 11/12 mock exam context), research/genai/vertex-ai-overview.md (rebrand history source). List gcp-pmle-quiz/pages/ to find the quiz-mode page that needs a filter update.

3. Verify the Python env: `cd gcp-pmle-quiz && uv sync` (one-time; you do NOT need to run the Streamlit server).

4. Create 4 tasks via TaskCreate, one per Move (schema enhancement, migration, rebrands.json, mock pool tagging). Mark each in_progress when you start it; completed when its verification passes.

5. Execute moves in order: 1 → 2 → 3 → 4. Move 1 must precede Move 2 (otherwise pydantic validation fails). Move 2 must precede Move 4 (mock pools are stratified by exam_section). Move 3 is independent.

6. For Move 2, ALWAYS run the audit step first (dump unique values seen in gcp_topics / ml_topics / gcp_products across all 841 records) BEFORE applying the heuristic. Use the audit output to refine the rules in section-mapping.json if needed. Then apply.

7. After each move, run the verification steps described in the spec. Surface counts, distributions, and any anomalies in 3–5 sentences to the user before moving on.

8. STOP and ask the user if exam_section inference accuracy on a 10-question manual spot-check (Move 2 verification) is below 70%. Don't push through with a bad heuristic.

9. End-of-session: print a final summary table (per-section counts, mock pool sizes, rebrand entry count, orphan count with exam_section: null). Then surface Phase 3 MVP "Weekly homework view" as the natural next session.

Hard constraints:
- Do NOT change existing question records' content fields (question, options, answer, explanation). Only ADD new fields.
- Do NOT delete gcp-pmle-quiz/data/progress.json — it holds user state.
- Use random.seed(42) for mock pool sampling (reproducibility).
- Make the migration script idempotent — re-running it must not change records the second time.
- Atomic writes only (write to .tmp, then os.replace) when modifying quizzes.jsonl.

Estimated time: 1.5–2.5 hours of agent time.
~~~

---

## 9. Why this scope and not bigger

Phase 2 stops at **schema + tagging + reference data**. It deliberately doesn't include the MVP weekly homework view (Phase 3) or the rebrand-overlay UI (Phase 3) because:

1. The **MVP needs `exam_section` to exist first** — building both in one session risks scope creep and a half-finished UI.
2. **Mock pool tagging needs `exam_section` populated** — if Move 2 fails, Move 4 inherits the failure.
3. A **clean Phase 2 commit** = a clean baseline for Phase 3 to build on. The Phase 3 agent reads the result, doesn't have to debug it.

A focused 2-hour session beats a sprawling 6-hour one.
