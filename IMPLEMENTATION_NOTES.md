# Implementation Notes — Phases 2–5 (Apr 27–28, 2026)

**Audience.** Future Claude Code sessions and any human picking up this repo cold.
**Purpose.** Document what got built, what architectural decisions were made, and the conventions you must follow if you extend this app. Read `CLAUDE.md` first for project context, then this file before touching code.

---

## 1. State at the start of this session

The repo already had:

- A working Streamlit app at `gcp-pmle-quiz/` with Dashboard, Weekly Overview, GCP Products, Quiz Mode, Edit Questions, Export-for-LM, Useful Videos, Resources, Study Guide, and Mock Exam pages.
- 841 tagged questions in `data/quizzes.jsonl` (`source` set on all, `exam_section` on 822/841 ≈ 97.7 %, mock pools at 100/100 each).
- `data/section-mapping.json` (16 rules, priority-ordered), `data/rebrands.json` (14 entries), `data/weeks.json` (12 weeks).
- `utils/__init__.py` (loaders), `utils/session.py` (diskcache mirror), `utils/weekly.py` (Phase 3 backend).
- A `models/questions.py` Pydantic schema with the three optional Phase 2 fields (`source`, `exam_section`, `mock_pool`).

In other words **Phases 2 and 3 were already shipped before this session** — they got verified and audited but not rebuilt. Phase 4, Phase 5, and the study_plan.md content overhaul were net-new.

---

## 2. What this session shipped

Three commits pushed to `https://github.com/patrickt6/pmle-summer.git`:

| Commit | Subject |
|---|---|
| `d70d5a9` | Expand study_plan.md with measurable goals, hyperlinks, bonus content |
| `71f0569` | Add Phase 4: per-week timed quizzes + shared scoring runtime + tests |
| `1b5d106` | Add Phase 5: knowledge graph + library + labs integration |

### 2.1 study_plan.md overhaul

The user asked for "more specific deliverables, more hyperlinks, measurable goals, and 'above and beyond' bonus content." The rewrite:

- **Per-week section template** with a fixed shape: `🎯 Theme + measurable success` → `📦 Hard deliverables` (checkboxes) → `🧠 Concept anchors` (3–5 memorize-or-explain items) → `📅 Daily breakdown (Mon–Fri)` → `🧪 Saturday lab` (paired protocol) → `📊 Sunday self-assessment` (explicit threshold) → `🚀 Above-and-beyond` (optional bonuses).
- Every Skills Boost lab is hyperlinked to its `skills.google/course_templates/<id>` URL.
- Every research file is linked to `research/...`.
- Every internal app page is referenced by its file path (e.g., `pages/10_📋_Week_Quizzes.py`) so the plan doubles as in-app navigation.

### 2.2 Phase 4 — per-week mock-style quizzes

Spec lives at `phase4-per-week-quizzes.md`. The four moves:

**Move 1 — `utils/quiz_runtime.py`.** Shared scoring + render helpers consumed by both the Mock Exam page (legacy `mock_` prefix, NOT refactored this session — see §3.1 below) and the new Week Quizzes page (`weekquiz_` prefix). Public API: `score()`, `format_clock()`, `seconds_remaining()`, `init_state()`, `reset_state()`, `start()`, `submit()`, `render_running()`, `render_submitted()`. Score returns a `ScoreResult` dataclass with per-section breakdown and wrong-item list. State is parameterized by a string `state_prefix` so two timed quizzes never collide in `st.session_state`.

**Move 2 — `sample_quiz_for_week()` in `utils/weekly.py`.** Stratified sample of N questions from a Week's `exam_sections`. Algorithm:

1. Group in-scope questions by sub-section (`§3.1`, `§3.2`, …).
2. Compute per-sub-section target counts: parent-section share = `SECTION_WEIGHTS[parent] / sum(SECTION_WEIGHTS[p] for p in parents_present)`. Within a parent, share = `len(by_sub[sub]) / parent_avail`.
3. Floor each `raw_target`, distribute the remainder to sub-sections with the largest fractional parts (deterministic tiebreak by name).
4. Shuffle each sub-section with `random.Random(seed)`, take the target count, push leftovers to a global pool.
5. If we're still short, pull from leftovers.
6. Final shuffle of selected.

This handles small weeks (Week 3 has only 24 in-scope) by capping at `min(n_questions, available)` and accepting that overlap between attempts is unavoidable when `n_in_scope < 60`.

**Move 3 — `pages/10_📋_Week_Quizzes.py`.** Week selector + three preset attempt cards (A/B/C) + 🔀 Remix button + history table. Deterministic seeds: `seed = week_num * 1000 + attempt_index` (1=A, 2=B, 3=C). Remix uses `seed = int(time.time())`. Mock weeks (11, 12) use `MOCK_WEEK_PARAMS` (30 Qs / 45 min / ≥ 75 %); other weeks use `DEFAULT_PARAMS` (20 Qs / 30 min / ≥ 70 %). When the user submits, the page calls `render_submitted(..., on_finalize=_persist_result)` which writes one row to `data/week_quiz_results.json`.

**Move 4 — `utils/week_results.py` + `data/week_quiz_results.json`.** Persistent results store, separate from `progress.json` so timed-quiz history doesn't pollute Quiz Mode round tracking. Atomic write: `.tmp` then `os.replace`. Append-only (we keep all attempts forever — the file is small). Public API: `load_week_quiz_results()`, `append_week_quiz_result()`, `latest_attempt(week, attempt_id)`, `attempts_for_week(week)`. Pydantic `WeekQuizResult` schema mirrors the JSON.

### 2.3 Phase 5 — knowledge graph + library + labs

Spec lives at `phase5-graph-library-labs.md`. The three moves are independent — each ships in its own page.

**Move 1 — `pages/11_🕸_Knowledge_Graph.py`.** Force-directed pyvis graph joining five node types (color-coded): exam sections (blue hex) ↔ products (green box) ↔ concepts (purple ellipse) ↔ decision trees (purple diamond) ↔ labs (orange dot) ↔ rebrand-old names (grey dot, dashed edge). Built fresh from `weeks.json`, `knowledge.json`, `labs.json`, `rebrands.json`, `section-mapping.json`. The whole graph is cached via `@st.cache_resource` because rebuilding pyvis HTML is expensive (~1 s) but the underlying data rarely changes.

**Move 2 — `pages/12_📖_Knowledge_Library.py` + `data/knowledge.json` + `utils/knowledge.py`.** 19 cards across three categories (`concepts`, `products`, `decision_trees`), 12 of them flagged `high_yield: true`. UI is four tabs (🧠 Concepts · 🏷 Products · 🌳 Decision Trees · 🏆 High-yield cross-cut), with a sidebar text-search and section multi-select. Each card expander reads the underlying `research/<file>.md` inline via `st.markdown(..., unsafe_allow_html=True)`.

**Move 3 — `pages/13_🧪_Labs.py` + `data/labs.json` + `data/lab_progress.json` + `utils/labs.py`.** The biggest move and the highest-leverage one per the Phase 5 spec. The 20 Skills Boost items become first-class study artifacts with:

- **Status tracking** — `not_started / in_progress / completed / skipped`. Buttons: `▶️ Mark started`, `✅ Mark complete`, `⏭ Skip`, `🔁 Reset`.
- **Shared notes** — markdown text area, paste-driven, `Patrick:` / `Matty Boy:` prefix convention.
- **"Ohhh" insights** — append-only bullet list with `➕ Append` button.
- **Post-lab drill** — 15-Q timed quiz (20 min, ≥ 70 % pass) sampled from this lab's `exam_sections` via `post_lab_quiz_questions()`. Reuses `utils/quiz_runtime.py` with state prefix `labquiz_`.
- **Saturday paired-session template** in a collapsed expander, ready to paste into chat.

Plus three cross-link integrations:
- `🏠_Dashboard.py` — "Labs done X / 14 must-rated · Yh logged" banner.
- `pages/1_📅_Weekly_Overview.py` Plan tab — lab status table with link to Labs page.
- `pages/9_⏱️_Mock_Exam.py` submit view — "Suggested labs for your weak sections" callout listing incomplete labs covering any of the user's weakest 3 §s.

### 2.4 Test infrastructure

`gcp-pmle-quiz/tests/` (new this session) contains 64 pytest tests across 5 files:

| File | Count | Coverage |
|---|---|---|
| `test_quiz_runtime.py` | 16 | `score()` for single/multi-choice + partial/extra answers, per-section breakdown, uncategorized fallback, `format_clock()` edge cases (zero, hour, negative). |
| `test_weekly_sampler.py` | 12 | All 12 weeks load, sampler size + capping, determinism (same seed = same IDs), seed divergence (different seeds → ≥ 1 differing ID), mock exclusion default, in-scope guarantee, no-duplicate IDs within an attempt. |
| `test_week_results.py` | 9 | Empty-load, append + reload, atomic write (no leftover `.tmp`), `latest_attempt()` picks newest, missing-week returns None, retains all attempts forever, round-trip preserves nested fields. Uses `monkeypatch` to point `WEEK_QUIZ_RESULTS_FILE` at a tmp path so tests don't pollute real data. |
| `test_labs.py` | 18 | 20 labs load, must-rated count = 14, `get_lab` lookup + missing-raises, `labs_for_week`, `post_lab_quiz_questions` size + section-scoping + mock-exclusion + seed determinism, atomic progress writes, `update_lab` create + merge, completion summary aggregation. Tmp-progress fixture isolates test runs. |
| `test_knowledge.py` | 9 | 19+ cards load, ≥ 5 high-yield, search case-insensitive, empty search returns all, `filter_by_section`, every `research_file` path resolves on disk. |

Run from `gcp-pmle-quiz/`:

```bash
.venv-test/bin/pytest tests/ -q
```

(See §3.4 below for the venv setup.)

---

## 3. Architectural decisions and conventions

### 3.1 Why Mock Exam wasn't refactored to use `quiz_runtime`

The Phase 4 spec explicitly said "Refactor in a later commit, not this Phase 4 commit, to keep blast radius small." The new Week Quizzes and Labs pages use `quiz_runtime` fresh; Mock Exam keeps its inline `_score`, `_format_clock`, `_render_running`, `_render_submitted`. They duplicate logic but the duplication is contained — both produce equivalent results. **If you refactor Mock Exam later**, preserve the `mock_` state prefix and the existing meta-keys (`mock_num`, `mock_phase`, etc.) so any cached session state survives the upgrade.

### 3.2 State-prefix convention

`utils/quiz_runtime.py` parameterizes session state by a string prefix. Established prefixes:

- `mock_` — Mock Exam page (held-out 50 questions; legacy inline implementation)
- `weekquiz_` — Week Quizzes page (sampled per-week 20–30 Qs)
- `labquiz_` — Labs post-lab drill (15 Qs sampled from a lab's sections)

If you add a new timed-quiz surface, **pick a fresh prefix** so two pages can be open in different tabs without trampling each other. Reset state via `reset_state(prefix)`; never delete keys by hand.

### 3.3 Why labs/week_results data lives in separate JSON files (not progress.json)

`progress.json` tracks "user got Q42 right last time" for Quiz Mode rounds. Mixing in mock-pool questions would leak calibration value (Phase 2 stratified-sampled the mock pools to be held-out for Mocks #1/#2 in Weeks 11–12). Mixing in week-quiz history would conflate "I drilled this once" with "I sat the timed Sunday quiz." Separating into:

- `data/progress.json` — Quiz Mode round results (gitignored — user state)
- `data/week_quiz_results.json` — Week Quizzes attempt history (committed; small, append-only)
- `data/lab_progress.json` — Lab status + notes + insights + post-lab drill scores (gitignored — contains shared notes that may include personal context)

…keeps each surface's persistence model clean. Atomic writes (`.tmp` + `os.replace`) for both new files.

### 3.4 Test environment (`.venv-test/`)

The system Anaconda Python's pytest install is broken (`ImportError: cannot import name 'Config' from 'pytest'` due to a stale `pytest_asyncio` against new pytest). Workaround used this session:

```bash
python3 -m venv .venv-test
.venv-test/bin/pip install pytest streamlit pydantic
.venv-test/bin/pytest tests/
```

The `.venv-test/` directory is in `.gitignore`. If you switch to `uv` (the project uses `pyproject.toml` for `uv sync`), use `uv run pytest` instead — the venv is then unnecessary.

### 3.5 Stratified sampler — why a two-phase floor + remainder

`sample_quiz_for_week()` and `post_lab_quiz_questions()` both use the same algorithm:

1. **Floors.** For each sub-section, compute `raw_target = N * parent_share * sub_share`, take the floor. Sum is ≤ N.
2. **Remainder.** Distribute the `N − sum(floors)` leftover slots to sub-sections with the largest fractional remainders, deterministic tiebreak by sub-section name.
3. **Spillover.** If a sub-section runs out (its `len(by_sub[sub]) < target`), the leftover from that bucket spills back into a global pool.
4. **Top-up.** If the final selected count is still < N, pull from the global pool.

This is reproducible (same seed → same output), stable (tiebreaks are deterministic), and graceful with small pools (Week 3 has 24 questions in scope and the 20-Q sample still works, just with overlap between attempts).

### 3.6 pyvis caching

`pages/11_🕸_Knowledge_Graph.py` builds the graph once and caches the HTML via `@st.cache_resource(show_spinner=False)`. The Rebuild button in the sidebar busts the cache via `_cached_graph_html.clear()`. **Do not** invalidate on every rerun — the build is ~1 s and the data only changes when JSON files are edited.

### 3.7 Page sidebar order

Streamlit orders pages by the leading number prefix in the filename. Conventions in this repo:

| Order | File | Purpose |
|---|---|---|
| Home | `🏠_Dashboard.py` | Overview + meme + Start button |
| 1 | `1_📅_Weekly_Overview.py` | Per-week catch-all (Plan / Research / Drill / Rebrand / Resources) |
| 2 | `2_☁️_GCP_Products.py` | Product-only graph (legacy, pre-Phase 5) |
| 3 | `3_🤔_Quiz_Mode.py` | Untimed drill rounds with explanations |
| 4 | `4_📝_Edit_Questions.py` | In-app question editor |
| 5 | `5_🇦🇮_Export_for_LM.py` | Export wrong-answers to NotebookLM-ready markdown |
| 6 | `6_📺_Useful_Videos.py` | Curated video index |
| 7 | `7_📚_Resources.py` | External resources index |
| 8 | `8_📝_Study_Guide.py` | Long-form synthesized guide |
| 9 | `9_⏱️_Mock_Exam.py` | 50-Q timed mocks from held-out pools |
| 10 | `10_📋_Week_Quizzes.py` | 20–30 Q timed per-week quizzes |
| 11 | `11_🕸_Knowledge_Graph.py` | Multi-type force-directed graph |
| 12 | `12_📖_Knowledge_Library.py` | Searchable concept/product/decision-tree cards |
| 13 | `13_🧪_Labs.py` | 20 Skills Boost items as first-class artifacts |

If you add a new page, **pick the next free integer**. Reordering existing pages would break user muscle memory.

### 3.8 Data file ownership map

| File | Owner | Read by | Notes |
|---|---|---|---|
| `data/quizzes.jsonl` | Phase 2 migration | Quiz Mode, Mock Exam, Week Quizzes, Labs post-lab drill, sampler | Idempotent migration script at `scripts/migrate_phase2.py`. **Do not modify question content fields**; only ADD optional fields. |
| `data/section-mapping.json` | Phase 2 author (manual) | `migrate_phase2.py` | First-rule-wins, priority-ordered. Most specific § first. |
| `data/rebrands.json` | Phase 2 author (manual) | Weekly Overview, Knowledge Graph | 14 entries; sourced from `CLAUDE.md` + `research/genai/vertex-ai-overview.md`. |
| `data/weeks.json` | Phase 3 author (manual) | Weekly Overview, Week Quizzes, Knowledge Graph, Labs page | 12 entries. `study_start_date` drives "current week" computation. |
| `data/week_quiz_results.json` | `utils/week_results.py` (append-only) | Week Quizzes history | Bootstrap committed empty; populated at runtime. |
| `data/labs.json` | Phase 5 author (manual) | Labs page, Knowledge Graph, Weekly Overview Plan tab, Mock Exam suggestions | 20 entries from `research/labs/skills-boost-path.md`. |
| `data/lab_progress.json` | `utils/labs.py` (atomic write) | Labs page, Dashboard banner, Weekly Overview Plan tab, Mock Exam suggestions | **Gitignored** because it holds shared notes. The loader auto-creates an empty bootstrap. |
| `data/knowledge.json` | Phase 5 author (manual) | Knowledge Library, Knowledge Graph | 19 entries; `high_yield` flag drives the cross-cut tab. |
| `data/progress.json` | `utils/__init__.py` save | Quiz Mode, Weekly Overview Drill tab | **Gitignored**. Per-question correct/wrong map (id → bool). |
| `data/gcp_products.jsonl` | pre-existing | GCP Products page | 104 product entries; powers the legacy single-type graph. |

### 3.9 Why `_persist_result` / `_persist_post_lab_attempt` callbacks fire exactly once

Streamlit reruns the entire page script on every interaction. Without a guard, "submit a quiz" would write the result to disk on every rerun. The pattern:

```python
finalize_flag = f"{state_prefix}finalized"
if on_finalize is not None and not st.session_state.get(finalize_flag):
    try:
        on_finalize(result, meta)
    finally:
        st.session_state[finalize_flag] = True
```

The flag is cleared when a new attempt starts (`_start_attempt` deletes it). Without this you'd see duplicate rows in `week_quiz_results.json` after every rerun.

### 3.10 Idempotency convention

Phase 2 migration scripts (`scripts/migrate_phase2.py`, `scripts/tag_mock_pools.py`) only write a field if it's currently `None`. Re-running them on already-migrated data is a no-op. **All future migrations must follow this convention** — re-running a script must never mutate existing values unless you pass an explicit `--force` flag.

---

## 4. What to do (and not do) when extending

### 4.1 Adding a new question

1. Conform to the Pydantic `Question` schema in `models/questions.py` (id, mode, question, options, answer, explanation, plus optional source/exam_section/mock_pool).
2. Dedupe by question-text hash against the existing 841.
3. Append to `data/quizzes.jsonl` with `id = max_existing_id + 1`.
4. Tag with `source` (e.g. `"Google Sample"`, `"Whizlabs"`).
5. Either set `exam_section` manually OR re-run `scripts/migrate_phase2.py` and let the heuristic infer it.
6. Do **NOT** modify or replace `mock_pool` tags — those are calibrated for Mocks #1/#2.

### 4.2 Adding a new lab

1. Append a record to `data/labs.json` with all required fields (`id`, `name`, `type`, `platform`, `url`, `duration_hours`, `rating`, `exam_sections`, `weeks`, `decay_risk`, `console_focus`, `exam_yield_note`).
2. The Labs page picks it up automatically; cross-link banners on Dashboard, Weekly Overview, and Mock Exam refresh next time their pages render.
3. If the new lab applies to a specific study week, also add its `id` + `name` to `weeks.json` for that week's `labs` array (the Weekly Overview Plan tab joins on this).

### 4.3 Adding a new knowledge card

Append to `data/knowledge.json` under `concepts`, `products`, or `decision_trees`. Required fields: `id` (kebab-case unique), `title`, `blurb` (one paragraph), `tags` (list of `§X.Y` and/or product names), `research_file` (path relative to repo root — verified to exist by `test_research_files_resolve`), `high_yield` (boolean). Knowledge Library and Knowledge Graph pick it up on next load.

### 4.4 Adding a new timed-quiz surface

1. Pick a unique `STATE_PREFIX` (e.g. `"sectiondrill_"`).
2. `init_state(STATE_PREFIX)` at the top of `main()`.
3. Branch on `st.session_state[f"{STATE_PREFIX}phase"]`: `idle` → render selector; `running` → `render_running(STATE_PREFIX, header_label=...)`; `submitted` → `render_submitted(STATE_PREFIX, threshold=..., on_finalize=...)`.
4. On Start, call `start(STATE_PREFIX, questions=..., duration_s=..., meta=...)`.
5. If you persist results, write the callback in your page module, not in `quiz_runtime.py` — the runtime stays storage-agnostic.

### 4.5 Adding a test

Pytest discovers anything matching `tests/test_*.py`. Use the `app_root` fixture from `conftest.py` for absolute paths. Use `monkeypatch` to redirect data file paths at `utils.<module>.FILE_CONST` to a `tmp_path` so tests don't pollute real data. Run via `.venv-test/bin/pytest tests/ -q` from `gcp-pmle-quiz/`.

### 4.6 Things to NOT do

- **Don't modify question content fields** (`question`, `options`, `answer`, `explanation`) — only ADD optional fields.
- **Don't delete `data/progress.json` or `data/lab_progress.json`** — they hold user state.
- **Don't lower the `mock_pool` exclusion default** in any sampler — those 200 questions stay held out for Mocks #1/#2 calibration.
- **Don't bypass atomic writes** when modifying `data/quizzes.jsonl`, `data/week_quiz_results.json`, or `data/lab_progress.json`. Always `.tmp` + `os.replace`.
- **Don't invent lab URLs** that aren't already in `research/labs/skills-boost-path.md`. Empty string is fine.
- **Don't re-fork the Mock Exam scoring code.** If you need to change scoring behavior, change it in `utils/quiz_runtime.py` and (eventually) refactor Mock Exam to use it. Forking creates two sources of truth.
- **Don't add auth or multi-user features** — both partners share progress.json / lab_progress.json / week_quiz_results.json. Multi-user isolation is deferred to Phase 6 if it ever becomes a problem.

---

## 5. Known caveats and follow-ups

- **pyvis console errors.** Knowledge Graph page emits 2–3 benign console errors on subpath URLs (the iframe's pyvis bundle calls `_stcore/health` relative to `/Knowledge_Graph/...` which 404s). Doesn't affect rendering. If you ever switch to a non-Streamlit-iframe pyvis embed, these go away.
- **Skipped Mock Exam refactor.** §3.1 above. Eventual cleanup, not load-bearing.
- **No browser-test harness.** The 4-step click-throughs from spec §3 (Phase 3) and §3 (Phase 4) were performed manually via Playwright MCP this session. There's no committed automated end-to-end test. If you add one, use `.venv-test` plus Playwright Python (or extend the existing MCP-driven flow).
- **Section distribution drift.** Parent `§1` is at 78 questions vs the v3.1 13 % target of ~109. Acceptable — within the ±5 pp slack the Phase 2 spec allows. If you import a paid bank in Week 9, prioritize §1 questions to balance.
- **Week 3 small-pool warning.** Only 24 in-scope non-mock questions. The Week Quizzes page surfaces a yellow caption when `n_in_scope < 60`; tests cover this case.
- **Skills Boost item #20 (Privacy & Safety) marked `skip`.** Long, low-yield. If you bump it to `should`, also add it to a week in `weeks.json`.

---

## 6. How to verify the app works (smoke test)

```bash
# From repo root:
cd gcp-pmle-quiz

# Run all tests
.venv-test/bin/pytest tests/ -q
# Expect: 64 passed

# Boot the server
python3 -m streamlit run 🏠_Dashboard.py
# Or with uv: uv run streamlit run 🏠_Dashboard.py
# Then open http://localhost:8501

# Programmatic page-by-page smoke test
python3 -m streamlit run 🏠_Dashboard.py --server.headless true --server.port 8501 &
sleep 8
for url in / /Weekly_Overview /GCP_Products /Quiz_Mode /Edit_Questions /Export_for_LM /Useful_Videos /Resources /Study_Guide /Mock_Exam /Week_Quizzes /Knowledge_Graph /Knowledge_Library /Labs; do
    curl -s -o /dev/null -w "%{http_code}  $url\n" "http://localhost:8501$url"
done
# Expect: 200 on all 14
```

---

## 7. File map — quick reference

```
gcp-pmle-quiz/
├── 🏠_Dashboard.py                  # Home; Phase 5 banners labs + has Start button
├── pages/
│   ├── 1_📅_Weekly_Overview.py     # Phase 3; Phase 5 lab table in Plan tab
│   ├── 2_☁️_GCP_Products.py        # Pre-Phase, single-type product graph
│   ├── 3_🤔_Quiz_Mode.py           # Pre-Phase + Phase 2 mock_pool filter
│   ├── 4_📝_Edit_Questions.py      # Pre-Phase
│   ├── 5_🇦🇮_Export_for_LM.py      # Pre-Phase
│   ├── 6_📺_Useful_Videos.py       # Pre-Phase
│   ├── 7_📚_Resources.py           # Pre-Phase
│   ├── 8_📝_Study_Guide.py         # Pre-Phase
│   ├── 9_⏱️_Mock_Exam.py           # Pre-this-session; Phase 5 weak-section lab callout
│   ├── 10_📋_Week_Quizzes.py       # Phase 4
│   ├── 11_🕸_Knowledge_Graph.py    # Phase 5
│   ├── 12_📖_Knowledge_Library.py  # Phase 5
│   └── 13_🧪_Labs.py               # Phase 5
├── utils/
│   ├── __init__.py                  # Pre-Phase; loaders + DATA_DIR + QUIZ_FILE
│   ├── session.py                   # Pre-Phase; diskcache mirror
│   ├── weekly.py                    # Phase 3 + Phase 4 sampler extension
│   ├── quiz_runtime.py              # Phase 4
│   ├── week_results.py              # Phase 4
│   ├── knowledge.py                 # Phase 5
│   └── labs.py                      # Phase 5
├── models/
│   └── questions.py                 # Pre-this-session; Pydantic schema with Phase 2 fields
├── data/
│   ├── quizzes.jsonl                # 841 Phase-2-migrated questions
│   ├── section-mapping.json         # 16 priority-ordered rules
│   ├── rebrands.json                # 14 entries
│   ├── weeks.json                   # 12 weeks
│   ├── labs.json                    # 20 labs (Phase 5)
│   ├── knowledge.json               # 19 cards (Phase 5)
│   ├── week_quiz_results.json       # Phase 4 results store (bootstrap empty)
│   ├── lab_progress.json            # Phase 5; gitignored
│   ├── progress.json                # Pre-Phase; gitignored
│   └── gcp_products.jsonl           # Pre-Phase; 104 products
├── scripts/
│   ├── migrate_phase2.py            # Phase 2 source + exam_section migration (idempotent)
│   └── tag_mock_pools.py            # Phase 2 mock pool stratified sampling (idempotent)
└── tests/
    ├── conftest.py
    ├── test_quiz_runtime.py         # 16 tests
    ├── test_weekly_sampler.py       # 12 tests
    ├── test_week_results.py         # 9 tests
    ├── test_labs.py                 # 18 tests
    └── test_knowledge.py            # 9 tests
```

Total: 14 Streamlit pages, 7 utility modules, 10 data files, 2 migration scripts, 5 test files / 64 tests.
