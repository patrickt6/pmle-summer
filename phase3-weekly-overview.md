# Phase 3 — Weekly Overview ("Catch-all" per-week study dashboard) Spec

**Date authored:** 2026-04-26 (immediately after Phase 2 finished)
**Estimated agent time:** 2.5–4 hours
**Depends on:** Phase 2 complete (✓ schema + section tagging + mock pools + rebrands.json)
**Unblocks:** the actual studying — first page the two learners open every day

---

## 1. Mission

Build a per-week dashboard inside the existing Streamlit app that, for each of the 12 study weeks, surfaces **everything available** on that week's exam section in one place:

1. **What Google offers** — the Skills Boost lab(s) scheduled for the week + a pointer to the relevant exam-guide section
2. **What research we did** — the relevant report(s) from `research/concepts/`, `research/decision-trees/`, `research/genai/`, etc.
3. **What questions to drill** — quiz subset filtered to the week's `exam_section`(s), excluding mock pools, with wrong-answer drill mode
4. **What rebrands to watch for** — entries from `rebrands.json` whose `old` or `new` name appears in this section's research/quiz content
5. **What other resources to read** — curated free + paid links from `study_plan.md` "Resources index" + `research/labs/`

This is a **read-only aggregator** — no editing, no auth, no progress tracking beyond what already exists in `progress.json`. The point is to eliminate "what should I do today?" decision fatigue.

## 2. Why this matters

| Without | Consequence |
|---|---|
| Per-week aggregator | Learner has to open `study_plan.md`, then `research/<topic>/<file>.md`, then Streamlit Quiz Mode, then re-find the rebrand alerts in CLAUDE.md every single day. Decision fatigue → skipped study days. |
| Quiz batch scoped to current week | Random shuffles drag the learner through unrelated sections; the spaced-repetition value of a focused week is lost. |
| In-app rebrand surface | Learner second-guesses correct answers because product was renamed since the question was authored. (Phase 2 produced `rebrands.json` for exactly this reason — wire it up here.) |

## 3. Pre-flight (do BEFORE editing anything)

Read these in order:

1. `CLAUDE.md` — full project context + April 2026 rebrand alerts + deprecation list
2. `phase2-question-consolidation.md` — the just-shipped Phase 2 spec, especially §1 mission and §6 deliverables; understand the schema you inherit
3. `study_plan.md` — the source of truth for the week-by-week schedule. Read the entire "Week-by-week" table; it has lab numbers, section focus, hours, and mock-exam dates per week
4. `gcp-pmle-quiz/models/questions.py` — the Pydantic schema (already extended in Phase 2)
5. `gcp-pmle-quiz/data/section-mapping.json` — how `exam_section` is derived (you don't need to touch it but should understand the priority order)
6. `gcp-pmle-quiz/data/rebrands.json` — 14 entries; this is your rebrand-alert data source
7. `gcp-pmle-quiz/utils/__init__.py` — existing loader (`load_quizzes`); do **not** break its contract
8. `gcp-pmle-quiz/pages/3_🤔_Quiz_Mode.py` — already filters mock pools out of default mode; reuse the same pattern
9. `ls research/` and `ls research/<each-subdir>/` to inventory available report files (don't read them all — just collect filenames)
10. `gcp-pmle-quiz/🏠_Dashboard.py` — existing dashboard page; understand the look-and-feel conventions before adding a new sidebar entry

Verify the env (one-time):
```bash
cd gcp-pmle-quiz && uv sync   # if uv is installed; otherwise system python3 + pydantic 2.10+ works
```

## 4. The three moves — execute in order

Dependencies: Move 1 (data model) **must precede** Move 2 (loader) **must precede** Move 3 (page). Do not parallelize.

---

## Move 1 — Build `weeks.json`

### What

Create `gcp-pmle-quiz/data/weeks.json` — the master mapping of each of the 12 weeks to its content. **You build this by reading `study_plan.md` "Week-by-week" table cell-by-cell** and translating prose into structured data. This is the single highest-leverage file in Phase 3 — get it right and the rest writes itself.

### Schema

```json
{
  "as_of": "2026-04-26",
  "source_doc": "study_plan.md",
  "weeks": [
    {
      "week": 1,
      "title": "ML lifecycle + GCP fundamentals",
      "exam_sections": ["§1.1", "§1.2"],
      "primary_section": "§1",
      "hours_target": 5.5,
      "labs": [
        {"id": 1, "name": "Introduction to AI and Machine Learning on Google Cloud", "platform": "Google Skills", "url": "https://www.skills.google/paths/17"}
      ],
      "research_files": [
        "research/concepts/ml-lifecycle.md",
        "research/decision-trees/tabular-modeling.md"
      ],
      "decision_trees": [],
      "rebrand_alerts": ["AI Platform", "Cloud Skills Boost"],
      "resources": [
        {"title": "PMLE v3.1 Exam Guide §1", "url": "https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf", "kind": "official"}
      ],
      "milestone": null
    }
  ]
}
```

Field definitions:

- `week` (int, 1..12) — week number
- `title` (str) — short focus line (paraphrase from study_plan.md)
- `exam_sections` (list[str]) — subsections covered (e.g., `["§3.1", "§3.2"]`); use the §X.Y form so it can be matched against `quizzes.jsonl` records' `exam_section` field
- `primary_section` (str) — parent section (`§1`–`§6`), used for the quiz query when fine-grained subsection filter is too narrow
- `hours_target` (float) — from study_plan.md hours column
- `labs` (list[dict]) — each lab has `id`, `name`, `platform`, `url`. **`url` may be an empty string** if you can't find a deep link; the lab id alone is enough to find it on skills.google
- `research_files` (list[str]) — relative paths from repo root to research markdown files relevant to this week. **Verify each file exists** before listing it
- `decision_trees` (list[str]) — subset of `research_files` that are decision trees (i.e., paths starting with `research/decision-trees/`). The page renders these in their own collapsed expander
- `rebrand_alerts` (list[str]) — `old` names from `rebrands.json` that the learner is likely to encounter in this week's content. Default to `[]` if nothing applies
- `resources` (list[dict]) — extra links pulled from `study_plan.md` "Resources index" or `research/labs/`. Each has `title`, `url`, `kind` (one of `"official"`, `"community"`, `"video"`, `"paid"`, `"book"`)
- `milestone` (str or null) — special event for this week. Examples: `"Mock #1 (Sat)"` for Week 11, `"REAL EXAM (Sat)"` for Week 12

### How to build it

1. Read the entire "Week-by-week" table in `study_plan.md`. Each row is one week.
2. For lab IDs: study_plan.md uses the `**#N** Lab Name` convention. Strip the bold + `#`, get id + name. Default `platform: "Google Skills"`, `url: ""` unless a clearer URL is in the row.
3. For `exam_sections`: each week's row mentions the section focus (often as "§3" or by topic). Map topic → section using the v3.1 blueprint table in CLAUDE.md. If the week spans two subsections, list both.
4. For `research_files`: walk `research/` once at the start, build a quick map of `<filename> → topic`, then for each week list the files whose topic aligns with the week's `exam_sections`. **Bias toward inclusion** — better to over-link than to under-link; the page collapses them by default anyway.
5. For `rebrand_alerts`: for each week, check whether any `old` or `new` name in `rebrands.json` is mentioned in the linked research files (cheap grep). List only the `old` names — the new name comes from the rebrand entry.
6. For `resources`: copy from study_plan.md "Resources index" + add anything in `research/labs/` that's specific to the week.
7. For `milestone`: only Weeks 11 and 12 have non-null milestones (Mock #1, Mock #2, REAL EXAM).

### Verification

- File loads as valid JSON: `python3 -c "import json; print(len(json.load(open('gcp-pmle-quiz/data/weeks.json'))['weeks']))"`. Expected: `12`.
- Every `research_files` path resolves to an existing file (no broken links).
- Every `exam_sections` entry matches at least one record in `quizzes.jsonl` (cross-check: load both, every section should have ≥1 question).
- `hours_target` per week sums to within 5% of 60–75 hours (the project budget from CLAUDE.md).
- Spot-check Week 1, Week 6, Week 11, Week 12 by hand against `study_plan.md` — does the structured row match the prose?

---

## Move 2 — Backend loader

### What

Add `gcp-pmle-quiz/utils/weekly.py` (a new module) with these functions:

```python
def load_weeks() -> list[Week]                     # parse weeks.json into typed objects
def load_rebrands() -> list[Rebrand]                # parse rebrands.json into typed objects
def get_week(week_num: int) -> Week                 # lookup by week number, raise if not found
def quizzes_for_week(week: Week, *, exclude_mock: bool = True) -> list[Question]   # filter quizzes.jsonl by week.exam_sections, optionally excluding mock_pool
def progress_for_week(week: Week, progress: dict) -> dict   # subset of progress.json scoped to week's quizzes; returns {answered_correctly, answered_incorrectly, not_answered}
```

Define `Week` and `Rebrand` as Pydantic models that mirror the JSON schemas above. This is purely additive — do not modify `models/questions.py` or `utils/__init__.py`.

### Verification

- `load_weeks()` returns 12 entries. Each has non-empty `title`, `exam_sections`, and `hours_target > 0`.
- `quizzes_for_week(weeks[0])` returns >0 questions, all with `exam_section` in `weeks[0].exam_sections` and all with `mock_pool` falsy.
- Calling `quizzes_for_week` with `exclude_mock=False` returns at least as many questions as the default call.
- `progress_for_week` keys are a strict subset of the input progress dict's keys.

---

## Move 3 — Streamlit page `pages/1_📅_Weekly_Overview.py`

### What

Add a new page numbered `1_` so it appears at the top of the sidebar (above the existing Dashboard at `🏠_Dashboard.py` and the other numbered pages). The page is the per-week catch-all the user described.

### Page layout (top to bottom)

1. **Week selector** at the top — `st.selectbox` populated from `load_weeks()`. Default to the current week (compute from a `STUDY_START_DATE` constant in `weekly.py`; if the constant isn't set, default to Week 1 and surface a warning). Persist the selection in `st.session_state` so it survives reruns.

2. **Week header** — `Week N — {title}` + a small caption with `hours_target h target · §{primary_section} focus · {len(quizzes_for_week(...))} questions · {milestone or ""}`.

3. **Tabs** (use `st.tabs`) inside the page, in this order:
   - **📚 Plan** — Lab list (each row: `#id · name · platform · url`), exam-guide section pointer, hours target, milestone (if any).
   - **🧠 Research** — Each `research_file` rendered inside a collapsed `st.expander(filename)`; expander body uses `st.markdown(file.read_text(), unsafe_allow_html=True)`. Decision trees go into a separate "Decision Trees" sub-section above the rest.
   - **🤔 Drill** — Embedded quiz mode scoped to this week. Two buttons: **"Start fresh round"** (filters to `not_answered` for this week) and **"Wrong-answer drill"** (filters to `answered_incorrectly` for this week). When clicked, set `st.session_state.quizzes` to the filtered list and switch to `pages/3_🤔_Quiz_Mode.py` via `st.switch_page`. The existing Quiz Mode page already handles the round logic — you just hand it a pre-filtered list.
   - **🪧 Rebrand alerts** — Render `rebrand_alerts` as a small table: `old → new (rebranded_at)` with the `context` field expanded inline. If empty, render "No rebrand alerts for this week."
   - **🔗 Resources** — Render `resources` as a markdown bullet list grouped by `kind` (official, community, video, paid, book).

4. **Footer** — small "Edit this week's plan in `data/weeks.json`" caption with a link to the file.

### Quiz handoff detail (the one tricky bit)

The existing Quiz Mode page reads `not_answered` from `load_quizzes()`. To pre-filter to a week, the Weekly Overview page should:

```python
# In the Drill tab handler:
qs = quizzes_for_week(current_week)
progress = load_progress()
filtered = [q for q in qs if q.id not in progress]   # or progress[q.id] is False for wrong-answer drill
st.session_state.quizzes = filtered
st.session_state.quiz_in_progress = True
st.session_state.quiz_mode_pos = 0
st.session_state.quiz_mode_round_progress = {}
cache_session()
st.switch_page("pages/3_🤔_Quiz_Mode.py")
```

The Quiz Mode page already handles a pre-populated `st.session_state.quizzes` because `load_session()` reads from cache.

### Verification

- Page loads at `http://localhost:8501` after `cd gcp-pmle-quiz && uv run streamlit run 🏠_Dashboard.py` (or `python3 -m streamlit run ...` if uv is unavailable). Sidebar shows "Weekly Overview" as the first page below the home dashboard.
- Selecting Week 1 / Week 6 / Week 12 changes the header and tab content correctly.
- The 📚 Plan tab shows lab rows. The 🧠 Research tab shows expanders for the listed files. The 🤔 Drill tab "Start fresh round" hands off a filtered quiz list to Quiz Mode and that round only contains week-relevant questions.
- The 🪧 Rebrand alerts tab shows entries when `rebrand_alerts` is non-empty.
- Selecting a week with `milestone == "REAL EXAM (Sat)"` (Week 12) renders the milestone in the header.
- No regressions in the existing Quiz Mode page when navigated to directly (full 641-question pool still works).

### Manual smoke test the agent must do before reporting done

Before claiming the page works, the agent **must** start the Streamlit dev server and click through:
1. Week selector → pick Week 5 → confirm header + all 5 tabs render
2. 🤔 Drill tab → "Start fresh round" → land on Quiz Mode → confirm only Week 5's section's questions appear in the round
3. Navigate back to home, then to Week 11 → confirm Mock #1 milestone appears in header
4. 🧠 Research tab on Week 5 → confirm expanders open and markdown renders (not raw text)

If any of these fail, fix and re-test. Do not ask the user to verify before the agent has clicked through.

---

## 5. Out of scope this session

- **Mock Exam page** (separate timed UI for `mock_pool == ["mock1-pool"]`). Worth adding in Week 9 once the learners are doing daily quizzes. Defer to its own session.
- **Auth / multi-user progress isolation**. Both learners share `progress.json` for now. If they want isolated progress, that's a Phase 4 task.
- **Rebrand-translation overlay inside Quiz Mode** (replacing or annotating product names mid-question). Defer — easier to surface alerts in the Weekly Overview tab than to mutate question text.
- **Next.js rewrite**. The MVP must ship in Streamlit. Decide on a rewrite only after using the Streamlit version for a full week.
- **Per-question "mark for review" / personal notes**. Out of scope; existing app already handles correct/incorrect tracking.
- **Spaced-repetition scheduling** beyond the "Wrong-answer drill" button. Out of scope.

## 6. End-of-session deliverables checklist

- [ ] `gcp-pmle-quiz/data/weeks.json` — 12 entries, all paths verified to exist
- [ ] `gcp-pmle-quiz/utils/weekly.py` — loaders + week/quiz lookup helpers
- [ ] `gcp-pmle-quiz/pages/1_📅_Weekly_Overview.py` — new page with 5 tabs (Plan / Research / Drill / Rebrand alerts / Resources)
- [ ] Streamlit dev server smoke-tested (4-step click-through above)
- [ ] Final summary printed: 12 weeks, total quizzes covered per week, total research files linked, total resources

## 7. Constraints (the agent MUST follow)

- **Do NOT modify** `models/questions.py`, `data/quizzes.jsonl`, `data/section-mapping.json`, `data/rebrands.json`, or `utils/__init__.py`. Phase 3 is purely additive.
- **Do NOT delete** `data/progress.json` — it has user state.
- **Do NOT add** auth, login, or multi-user features.
- **Do NOT** invent lab URLs you can't verify. Empty string is fine; the lab id alone is enough.
- **Render markdown safely** — `unsafe_allow_html=True` is fine for trusted research files (they're authored by the team) but do not pass user input through it.
- **Preserve existing pages** — Dashboard, GCP Products, Quiz Mode, Edit Questions, Export-for-LM must all still work after the new page is added.

## 8. Why this scope and not bigger

This phase deliberately stops at one read-only page because:

1. The page is the **first thing the learners need before any other Phase 3 enhancement** — without it, they're still flipping between markdown files and Streamlit tabs every day.
2. Building Mock Exam mode + rebrand overlay + auth + Next.js rewrite in one session = scope creep + half-finished features.
3. A focused 3-hour Streamlit page can be used Monday morning. A 12-hour Next.js rewrite can't.

## 9. Open design decisions for the agent to make (pick one and proceed)

These are not blockers — pick the option that ships fastest:

- **Streamlit vs Next.js**: ship in Streamlit. Period.
- **In-app markdown vs link-out**: in-app via `st.expander` + `st.markdown(file.read_text())`.
- **Week selector default**: `STUDY_START_DATE = date(2026, 4, 27)` constant + `(today - start).days // 7 + 1`, clamped to `[1, 12]`. If the user wants to override, the selectbox is right there.
- **Multi-user progress**: not yet. One shared `progress.json`. Plan Phase 4 if it becomes a problem.

---

## 10. Paste-ready prompt for fresh Claude Code session

Open a **fresh** Claude Code session in `/Users/patricktaylor/Documents/Google-PMLE/` (run `/clear` if continuing in an existing terminal). `CLAUDE.md` auto-loads. Paste the block below verbatim:

~~~
You're starting a fresh session in /Users/patricktaylor/Documents/Google-PMLE/. CLAUDE.md auto-loads and gives full project context — read it first if not already in your system reminder.

Single task this session: execute Phase 3 — the per-week "catch-all" study dashboard. The complete spec lives in `phase3-weekly-overview.md` at the repo root. Read it cover-to-cover before doing anything else; it defines goals, three moves (weeks.json → backend loader → Streamlit page), the data schema, the tab layout, and verification criteria including a mandatory dev-server click-through.

Steps:

1. Read `phase3-weekly-overview.md` cover-to-cover.

2. Read the pre-flight files listed in §3 of that spec (CLAUDE.md, phase2-question-consolidation.md, study_plan.md, the Phase 2 data files, existing Streamlit pages). List `research/` subdirectories to inventory available report files — do NOT read every report; just collect filenames so Move 1 can map them to weeks.

3. Verify the Python env. The system has python3 + pydantic 2.10.6 already; if `uv` is available use `uv sync`, otherwise system python is fine.

4. Create 3 tasks via TaskCreate, one per Move (weeks.json, backend loader, Streamlit page). Mark each in_progress when you start it; completed only after its verification passes.

5. Execute moves strictly in order: 1 → 2 → 3. Move 1 must precede Move 2 (loader needs the data file). Move 2 must precede Move 3 (page imports the loader).

6. For Move 1, the highest-leverage step is correctly reading study_plan.md's "Week-by-week" table and translating each row into a structured weeks.json entry. Verify EVERY research_files path exists before writing the file.

7. After each move, run the verification steps described in the spec. Surface counts and anomalies in 3–5 sentences before moving on.

8. For Move 3, you MUST start the Streamlit dev server and click through the 4-step manual smoke test described in the spec before reporting done. If the server can't start, say so explicitly — do NOT claim the page works based on type-checks alone.

9. End-of-session: print a final summary table (weeks tagged, quizzes per week, research files per week, total resources, any weeks with 0 questions or 0 research files). Then surface the natural next session: Mock Exam page (separate timed UI for the held-out 200 questions) — to be built in Week 9.

Hard constraints:
- Do NOT modify models/questions.py, data/quizzes.jsonl, data/section-mapping.json, data/rebrands.json, or utils/__init__.py. Phase 3 is purely additive.
- Do NOT delete data/progress.json — it holds user state.
- Do NOT invent lab URLs you cannot verify. Empty string is fine.
- Do NOT add auth or multi-user features.
- Ship in Streamlit, not Next.js. The Next.js decision can be revisited after a week of using the MVP.

Estimated time: 2.5–4 hours of agent time.
~~~

---

## 11. After Phase 3 ships, what's next

Likely Phase 4 candidates (don't decide until Phase 3 is in use):

1. **Mock Exam page** — timed UI surfacing only `mock_pool` questions. Trigger: Week 9 of study.
2. **Rebrand-translation overlay inside Quiz Mode** — annotate old product names with current names at render time.
3. **Multi-user progress isolation** — only if both learners want separate progress tracking.
4. **Next.js rewrite** — only if the Streamlit MVP gets used and needs a public-share URL.
5. **Question import pipeline** — when adding the Google sample form (~25 Qs) or a paid bank (~50 Qs) in Week 9.
