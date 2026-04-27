# Phase 4 — Per-week Mock-Style Quizzes (todolist)

**Date authored:** 2026-04-27 (immediately after Phase 3 + the Mock Exam page shipped)
**Estimated agent time:** 2.5–4 hours
**Depends on:** Phase 2 ✓ (`exam_section` tags), Phase 3 ✓ (`weeks.json` + `utils/weekly.py`), Mock Exam page ✓ (scoring + UI patterns to reuse)
**Unblocks:** the "weekly mini-exam" cadence — Sunday retros become *timed quizzes scoped to the week's blueprint*, not open-ended Quiz Mode rounds

---

## 1. Mission

Per-week, **multiple** mock-style quizzes — same UX as the existing Mock Exam page (timed, no in-quiz explanations, score + per-section breakdown at end) — but each quiz is scoped to **only the current week's exam sections**, with **multiple distinct attempts per week** so we can drill the same week's content repeatedly without seeing identical questions in identical order.

Concretely: for Week 5 (§3.1, §3.2), surface "Quiz 5A · 20 Qs · 30 min", "Quiz 5B · 20 Qs · 30 min", "Quiz 5C · 20 Qs · 30 min", plus a **🔀 Remix** button that produces a fresh seeded attempt every click. For Week 11/12 (mock weeks), the existing Mock Exam page handles the held-out 200; this page handles everything else.

This is **distinct from** the Drill tab on Weekly Overview (untimed, open-ended, sends to Quiz Mode) and **distinct from** the Mock Exam page (50 Qs from held-out pools only). Same scoring infrastructure, different scope.

---

## 2. Why this matters

| Without | Consequence |
|---|---|
| Per-week timed quizzes | Sunday self-assessment is either an untimed Drill round (no calibration) or a Mock Exam attempt (burns held-out pool calibration value early). Neither works for weekly retros. |
| Multiple attempts per week | One quiz attempt per week → after one Sunday you've seen every order; no re-drill value within the same week. |
| Stratified sampling per attempt | Random shuffle ignores v3.1 sub-section weights → a Week 5 quiz might land 18 questions on §3.1 and 2 on §3.2, defeating the point of weekly focus. |
| Separate result tracking | Quiz scores spill into `progress.json` (which Quiz Mode already uses) → can't tell apart "drilled in Quiz Mode" from "took weekly quiz attempt." |

---

## 3. Pre-flight (read before editing)

1. `CLAUDE.md` — full project briefing
2. `phase3-weekly-overview.md` — understand the `weeks.json` schema you'll consume
3. `gcp-pmle-quiz/data/weeks.json` — actual content (each week's `exam_sections`)
4. `gcp-pmle-quiz/utils/weekly.py` — `quizzes_for_week()` is the building block
5. `gcp-pmle-quiz/pages/9_⏱️_Mock_Exam.py` — the scoring + render pattern to reuse
6. `gcp-pmle-quiz/pages/3_🤔_Quiz_Mode.py` — note that it already excludes mock pools by default
7. `gcp-pmle-quiz/data/quizzes.jsonl` — section distribution (most weeks have 30-150 questions in scope; Week 3 has only 24 — see §6 *Edge cases*)

Verify env: `python3 -c "import streamlit, pydantic, diskcache, plotly, pyvis"` — same stack as the rest of the app.

---

## 4. The four moves — execute in order

### Move 1 — Extract shared scoring/render helpers

**What.** Right now `pages/9_⏱️_Mock_Exam.py` defines `_score()`, `_format_clock()`, `_render_running()`, `_render_submitted()` privately. Move the reusable pieces into a new module so the per-week-quizzes page doesn't duplicate them.

**File.** `gcp-pmle-quiz/utils/quiz_runtime.py` (purely additive — does NOT modify Mock Exam page yet).

**Public API:**
```python
def score(questions: list[Question], responses: dict[int, set[int] | int | None]) -> ScoreResult: ...
def format_clock(seconds: int) -> str: ...
def render_running(state_prefix: str, questions: list[Question], duration_s: int) -> None: ...
def render_submitted(state_prefix: str, questions: list[Question],
                     responses: dict, threshold: float, started_at: float) -> None: ...
```

`state_prefix` parameterizes the session_state keys (e.g., `"mock_"` for the Mock Exam page, `"weekquiz_"` for the new page) so two timed quizzes never collide.

**Verify.** Mock Exam page still works after refactor; no behavior change. (Refactor in a later commit, not this Phase 4 commit, to keep blast radius small.)

---

### Move 2 — Stratified sampling helper

**What.** Add a function in `utils/weekly.py` that, given a week and an attempt seed, returns N questions drawn proportionally from the week's `exam_sections` according to v3.1 sub-section weights.

```python
def sample_quiz_for_week(
    week: Week,
    *,
    n_questions: int = 20,
    seed: int,
    exclude_mock: bool = True,
) -> list[Question]:
    """Stratified random sample of `n_questions` from this week's scope.

    For weeks with multiple sub-sections, distributes the count proportionally
    to the v3.1 blueprint weights. If a sub-section has fewer questions than
    its target, the shortfall spills to the next-highest-weighted sub-section.
    """
```

**Algorithm.**
1. Group all in-scope questions by `exam_section`.
2. Compute target counts per sub-section using the v3.1 weights table from CLAUDE.md (§1=13%, §2=14%, §3=18%, §4=20%, §5=22%, §6=13%); inside each parent, weight sub-sections evenly.
3. For each sub-section: shuffle with `random.Random(seed)` and take the target count.
4. If any sub-section runs out, top up from the largest remaining pool.
5. Final shuffle so questions aren't grouped by section in the quiz.

**Verify.**
- `len(sample_quiz_for_week(week_5, n_questions=20, seed=0)) == 20` for every week 1-12.
- Re-calling with the same seed → identical question IDs (reproducibility).
- Re-calling with a different seed → ≥80% different question IDs on weeks with ≥30 in-scope questions.
- Excludes `mock_pool` questions by default (so they stay held out).

**Edge case.** Week 3 has only 24 in-scope non-mock questions. With `n=20` that's fine but multiple disjoint attempts isn't possible — accept overlap on small weeks. See §6.

---

### Move 3 — New page `pages/10_📋_Week_Quizzes.py`

**What.** Per-week timed quiz launcher.

**Sidebar entry.** Numbered `10_` so it appears after Mock Exam.

**Page layout.**

1. **Week selector** — same default-to-current-week logic as Weekly Overview. Persist in `st.session_state.weekquiz_selected_week`.

2. **Header.** *"Week N — {title}"* + caption *"§{primary} focus · {n_in_scope} Qs in scope · {hours}h target."*

3. **Quiz cards.** A `st.columns(3)` with three preset attempts (A / B / C) for the selected week. Each card shows:
   - *"Quiz 5A · 20 Qs · 30 min"*
   - Status pill: 🟢 not yet attempted · 🟡 in progress · 🔵 completed (score X%)
   - **Start** button (or **Resume** / **Review**)

   Use deterministic seeds: `seed = week_num * 1000 + attempt_index` (1=A, 2=B, 3=C).

4. **🔀 Remix button.** Generates a fresh attempt with `seed = int(time.time())`. Useful for endless drilling once A/B/C are stale.

5. **Active quiz area** — when one of A/B/C/Remix is started, hide the cards and render via the shared `render_running` / `render_submitted` from Move 1. State prefix: `"weekquiz_"`.

6. **History list** at the bottom — read from `data/week_quiz_results.json` (Move 4) and show every prior attempt's score, date, weak sections.

**Quiz parameters per week** (defaults; override per-week in `weeks.json` if needed):
- Weeks 1-10: **20 questions, 30 minutes, pass ≥ 70%**
- Weeks 11-12: **30 questions, 45 minutes, pass ≥ 75%** (more intensive — they're the mock weeks)

**Verify.**
- Picking Week 5 → three cards render → Start Quiz 5A → timer starts at 30:00 → after answering and Submit → score with §3.1 / §3.2 breakdown.
- Quiz 5B uses different seed → different question IDs from 5A (cross-check: print sets of IDs).
- Remix produces yet another distinct attempt.
- Switching weeks mid-attempt warns: *"You have a quiz in progress for Week 5 — switch will lose progress"*.

---

### Move 4 — Persistent results store

**What.** Separate from `progress.json`. New file `gcp-pmle-quiz/data/week_quiz_results.json`.

**Schema.**
```json
{
  "as_of": "2026-04-27",
  "results": [
    {
      "week": 5,
      "attempt_id": "5A",          // "5A" / "5B" / "5C" / "remix-1714186800"
      "seed": 5001,
      "started_at": "2026-05-25T13:00:00",
      "finished_at": "2026-05-25T13:24:18",
      "duration_s": 1458,
      "n_questions": 20,
      "n_correct": 16,
      "pct": 0.80,
      "passed": true,
      "by_section": {"§3.1": [13, 16], "§3.2": [3, 4]},  // [correct, total]
      "wrong_question_ids": [356, 401, 482, 519]
    }
  ]
}
```

**Loader / writer in `utils/weekly.py`** (or a new `utils/week_results.py`):
```python
def load_week_quiz_results() -> list[WeekQuizResult]: ...
def append_week_quiz_result(r: WeekQuizResult) -> None: ...
def latest_attempt(week: int, attempt_id: str) -> WeekQuizResult | None: ...
```

**Atomic write** (same pattern as Phase 2 migration): write `.tmp`, then `os.replace`.

**Verify.**
- Submit Quiz 5A → file exists, 1 entry, schema validates.
- Submit Quiz 5B → 2 entries; existing entry untouched.
- Submit Quiz 5A again (different attempt) → 3 entries (we keep all attempts; "latest" filter at read time).
- File survives a server restart.

---

## 5. UI/UX nice-to-haves (skip if running long)

- **Wrong-answer drill from history.** Each row in the history list has a "🔁 Drill these" button → loads only the wrong question IDs from that attempt into a Quiz Mode round.
- **Per-week trend chart.** Plotly line chart of attempt scores over time per week. Show whether Week 5 is improving or stagnating.
- **Auto-skip already-passed weeks** in the selector (after passing all 3 attempts at ≥80%, mark week 🏆 done).
- **Email/iMessage share** of result card (post-MVP).

---

## 6. Edge cases and constraints

- **Small weeks.** Week 3 has only 24 non-mock questions in scope. Three 20-question attempts can't be disjoint. Accept ≤30% overlap between attempts on weeks where `n_in_scope < 60`. Surface a yellow caption on those weeks: *"Limited question pool — attempts will reuse some questions."*
- **§2.2 has only 7 questions** — Week 3 is the only week that includes §2.2. The stratified sampler should fall back to drawing extras from §1.2 (Week 3's other section) when §2.2 runs out.
- **Weeks 11/12 already have the held-out 200 mock-pool questions excluded.** That leaves 622 non-mock questions across all sections — plenty for multiple 30-question attempts. Don't bypass the `exclude_mock=True` default.
- **Don't double-count weeks 11/12 as "mock weeks" in two places.** Week 11/12 here = drilling whatever the learner needs across all sections. Week 11/12 in the Mock Exam page = the held-out calibrated 50 Qs. Two separate experiences, same week.
- **Mid-quiz week switch.** If `weekquiz_selected_week` changes while `weekquiz_in_progress=True`, prompt the user before discarding state.
- **Browser refresh during a quiz.** Streamlit session state is in-memory only. To survive refreshes, mirror the running state into `diskcache` (same pattern as `utils/session.py`). Keep this scoped to a key prefix to not collide with Quiz Mode's cache.

---

## 7. Constraints (the agent MUST follow)

- **Do NOT modify** `models/questions.py`, `data/quizzes.jsonl`, `data/section-mapping.json`, `data/rebrands.json`, `data/weeks.json`, or `utils/__init__.py`. Phase 4 is purely additive.
- **Do NOT delete** `data/progress.json` (regular Quiz Mode state) — `week_quiz_results.json` is a SEPARATE file.
- **Do NOT** lower the `mock_pool` exclusion. The Mock Exam pools must stay held out for Weeks 11/12 calibration even when the per-week page is used in those weeks.
- **Do NOT** auto-write any week_quiz_results entry on partial/abandoned attempts. Only on Submit (or on the timer hitting zero, which is functionally equivalent).
- **Reuse the Mock Exam scoring/render code** via Move 1's shared module — don't fork it.

---

## 8. End-of-session deliverables checklist

- [ ] `gcp-pmle-quiz/utils/quiz_runtime.py` — shared timed-quiz scoring + UI (Move 1)
- [ ] `gcp-pmle-quiz/pages/9_⏱️_Mock_Exam.py` refactored to use `utils.quiz_runtime` (no behavior change)
- [ ] `gcp-pmle-quiz/utils/weekly.py` extended with `sample_quiz_for_week()` (Move 2)
- [ ] `gcp-pmle-quiz/utils/week_results.py` (or extension of `weekly.py`) — load/append week_quiz_results
- [ ] `gcp-pmle-quiz/data/week_quiz_results.json` — bootstrap with `{"as_of": "...", "results": []}`
- [ ] `gcp-pmle-quiz/pages/10_📋_Week_Quizzes.py` — new page with selector / 3 attempts / Remix / history
- [ ] Streamlit dev server smoke-tested: pick Week 5 → Quiz 5A → 20 Qs render → submit → score appears + history row added → take Quiz 5B → different question IDs
- [ ] Final summary printed: per-week counts of available attempts, edge-case warnings (Week 3, §2.2)

---

## 9. Open design decisions for the agent

Pick the option that ships fastest:

- **Question count per quiz.** 20 Qs / 30 min for Weeks 1-10. Could go 25/40 to match exam-day pacing more closely. Default 20/30 — adjust later from real usage data.
- **Three attempts vs N attempts.** Three named attempts (A/B/C) keeps the UI simple. Power users hit Remix for more. Don't auto-generate D/E/F — clutter.
- **Pass threshold.** 70% per-week (lenient — the goal is exposure, not gating). Mock Exam keeps the stricter 70/80%.
- **History pruning.** Keep all attempts forever. The file is small (~1 KB per attempt).
- **Multi-user.** Same `progress.json` decision as everywhere else — both learners share `week_quiz_results.json`. Phase 5 if isolation is needed.
- **Resume in-progress quiz across browser refresh.** Yes — mirror to `diskcache` like the existing app does. Worth the ~30 lines of code.

---

## 10. Out of scope this session

- **Adaptive difficulty / spaced repetition.** Not now. Maybe Phase 5.
- **LLM-generated questions.** Way out of scope; we don't have the QA pipeline to verify generated questions against current Google docs.
- **Public sharing of quiz results.** Not now — this is a private 2-person study app.
- **Multi-section "themed" quizzes** that span weeks (e.g., "all of §5 across Weeks 7+8"). The Mock Exam page already covers all-section drilling. If we want themed quizzes, that's Phase 5.

---

## 11. Paste-ready prompt for fresh Claude Code session

Open a fresh Claude Code session in `/Users/patricktaylor/Documents/Google-PMLE/`. `CLAUDE.md` auto-loads. Paste verbatim:

~~~
You're starting a fresh session in /Users/patricktaylor/Documents/Google-PMLE/. CLAUDE.md auto-loads.

Single task this session: execute Phase 4 — per-week mock-style quizzes. The complete spec lives in `phase4-per-week-quizzes.md` at the repo root. Read it cover-to-cover before doing anything else; it defines four moves (extract shared scoring helpers → stratified sampling → new Week_Quizzes page → persistent results file), the data schema, the UI layout, and verification criteria including a mandatory dev-server click-through.

Steps:

1. Read `phase4-per-week-quizzes.md` cover-to-cover.

2. Read `gcp-pmle-quiz/pages/9_⏱️_Mock_Exam.py` and `gcp-pmle-quiz/utils/weekly.py` — these are the patterns you'll extend.

3. Verify the env: `python3 -c "import streamlit, pydantic, diskcache, plotly, pyvis"`.

4. Create 4 tasks via TaskCreate, one per Move. Mark each in_progress when starting; completed only after verification passes.

5. Execute moves strictly in order: 1 → 2 → 3 → 4. Move 1 must precede Move 3 (page imports the shared module).

6. For Move 2, the highest-leverage step is correctly stratifying the sample across the week's exam_sections proportional to v3.1 weights — handle the §2.2 fall-back case explicitly.

7. For Move 3, you MUST start the Streamlit dev server and click through Week 5 → Quiz 5A submit → Quiz 5B start (verify question IDs differ) → check history row appears.

8. End-of-session: print a summary table (12 weeks × 3 attempts each = 36 reproducible attempts; weeks with overlap warnings; total questions in scope per week).

Hard constraints:
- Phase 4 is purely additive. Do NOT modify the files listed in §7 of the spec.
- Atomic writes for week_quiz_results.json (write .tmp then os.replace).
- Reuse Mock Exam scoring via the new shared module — don't fork it.
- Excluded mock_pool stays excluded — those 200 questions are held out for Weeks 11/12.

Estimated time: 2.5-4 hours of agent time.
~~~

---

## 12. After Phase 4 ships

Likely Phase 5 candidates (don't commit until Phase 4 is in use):

1. **Adaptive sampling** — re-weight a learner's next attempt toward sub-sections they've scored < 70% on
2. **Cross-week themed quizzes** (all of §5 across Weeks 7-8; all of §6 across Week 9-12)
3. **Multi-user progress isolation** — both `progress.json` and `week_quiz_results.json` get a per-user split
4. **Auto-generated wrong-answer Anki-deck export** — wire Andy's existing NotebookLM-export pattern
5. **Question import pipeline** — when adding the Google sample form (~25 Qs) or a paid bank (~50 Qs)
