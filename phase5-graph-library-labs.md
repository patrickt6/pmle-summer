# Phase 5 — Knowledge Graph + Knowledge Library + Labs Integration (todolist)

**Date authored:** 2026-04-27
**Estimated agent time:** 4–6 hours (or split across 2-3 sessions; each move is independent)
**Depends on:** Phase 2 ✓ (`exam_section` tags, `rebrands.json`), Phase 3 ✓ (`weeks.json`, `utils/weekly.py`), Phase 4 (per-week quizzes — optional dependency for cross-linking)
**Unblocks:** discoverable knowledge browsing, lab-driven study cadence, the "show me everything connected to X" use case

---

## 1. Mission

Three additions, each independent so they can be sequenced or parallelized:

1. **🕸 Knowledge Graph view** — interactive node-edge visualization linking exam sections, GCP products, ML concepts, decision trees, labs, and rebrand alerts. Click a node → see its neighborhood, drill into related questions/research/labs.
2. **📖 Knowledge Library** — structured browsable cards for every concept, decision tree, and product covered. Search bar at top. Each card links into the underlying research file and the relevant week.
3. **🧪 Labs Integration** ⭐ (the big one) — first-class treatment of the Skills Boost labs as study artifacts: tracked completion status, shared notes per lab, *"after this lab, drill these N questions"* auto-quizzes, paired-session debrief templates.

The existing `pages/2_☁️_GCP_Products.py` is a starting point for Move 1 (it already uses pyvis). The other two pages are new.

---

## 2. Why this matters

| Without | Consequence |
|---|---|
| Knowledge graph | "I'm weak on §6.2 — what concepts/products/labs cover this?" requires opening 5 different markdown files and cross-referencing manually. The connections that make GCP make sense (e.g. *Vector Search ↔ Matching Engine ↔ Vertex AI Search ↔ Agent Builder ↔ Gemini Enterprise*) live only in our heads. |
| Knowledge library | The 14 research reports are deep-dives. There's no quick-reference layer — *"give me a one-paragraph reminder of skew-vs-drift before I start this lab"*. Today the only fast-lookup path is the Study Guide page, which is one long article. |
| Labs integration | **Labs are the most-cited resource across all 10 recent passers.** The study plan budgets 58h on Skills Boost out of ~70h total — but our app currently treats labs as link-out URLs in a list. No tracking of which we've completed, no shared notes from the Sat 90-min paired sessions (which the study plan explicitly schedules), no *"after this lab, drill these"* loop. This is where most of the gain actually lives. |

---

## 3. Pre-flight (read before editing)

1. `CLAUDE.md` — project briefing
2. `research/labs/skills-boost-path.md` — full lab inventory (20 items, durations, ratings, sections covered). **This is your data source for Move 3.**
3. `study_plan.md` — Sat 90-min lab session protocol; the "ohhh insight" debrief
4. `gcp-pmle-quiz/pages/2_☁️_GCP_Products.py` — existing pyvis graph (you'll extend, not replace)
5. `gcp-pmle-quiz/data/gcp_products.jsonl` — 104 product nodes (already loaded)
6. `gcp-pmle-quiz/data/section-mapping.json` — section → product/topic patterns (drives some graph edges)
7. `gcp-pmle-quiz/data/weeks.json` — week → labs / research / sections (drives lab-week cross-links)
8. `gcp-pmle-quiz/data/rebrands.json` — old → new product names (use as colored alert nodes in the graph)

Verify env: `python3 -c "import streamlit, pyvis, networkx, plotly"` — same stack.

---

## 4. The three moves — execute in any order (each is independent)

### Move 1 — Knowledge Graph view

**What.** Extend (or fork) the existing `pages/2_☁️_GCP_Products.py` to render a multi-type graph, not just product-product edges.

**File.** Either modify in place or create `pages/11_🕸_Knowledge_Graph.py` (new sidebar entry, leaves the existing GCP Products page intact).

**Node types.**

| Type | Source | Color | Example |
|---|---|---|---|
| Exam section | `weeks.json` `exam_sections` (16 unique) | blue | `§5.1` |
| GCP product | `gcp_products.jsonl` (104) | green | `Vertex AI Pipelines` |
| Concept / decision tree | `research/concepts/*.md` + `research/decision-trees/*.md` (11 files) | purple | `skew-vs-drift` |
| Lab | `research/labs/skills-boost-path.md` (20) | orange | `#7 Keras on GCP` |
| Rebrand-old | `rebrands.json` `old` (14) | grey, dashed border | `Matching Engine` |

**Edge types.**

- `section ↔ product` — derived from `data/section-mapping.json` (every product pattern in a section's rule-list connects)
- `section ↔ lab` — derived from `weeks.json` (each lab in a week connects to that week's `exam_sections`)
- `concept ↔ section` — derived from filename + content (skew-vs-drift → §6.2; compute-selection → §3.3; pipelines-comparison → §5.1; etc.)
- `product ↔ product` — only for known relationships (rebrand chain, "uses" relationship like *Vertex AI Pipelines uses Cloud Storage*). Keep this edge set small to avoid hairball.
- `rebrand-old ↔ rebrand-new` — derived from `rebrands.json`; rendered as dashed grey edges so they read as historical rather than active.

**Layout.**

- Default: pyvis force-directed layout, ~400 nodes feasible.
- **Filter sidebar** to show/hide by node type (default: all on except rebrand-old).
- **Search box** to highlight a node + its 1-hop neighborhood, dim everything else.
- **Click a node** → right-side details panel:
  - Description (from research file or section-mapping comment)
  - Linked research files
  - Number of questions tagged with that section/product
  - Links: *"Drill questions for this section"* (deep-link to Weekly Overview Drill tab) / *"Read research file"* (in-app expander)

**Performance.**

- 16 sections + 104 products + 11 concepts + 20 labs + 14 rebrand-olds = **165 nodes**. Easily manageable.
- Edge density: probably 600-1200. Fine for pyvis.
- Pre-render the HTML once (cache to `cache/knowledge_graph.html`) so the page loads instantly on revisits. Invalidate on `weeks.json`/`section-mapping.json`/`rebrands.json` mtime change.

**Verification.**

- All 165 nodes appear; legend shows 5 colors.
- Clicking `§5.1` highlights its connected products (Vertex AI Pipelines, Kubeflow, Cloud Composer, TFX, MLFlow), labs (#15, #9), concepts (pipelines-comparison.md).
- Filtering "rebrand-old" off hides the 14 dashed grey nodes cleanly.
- Page loads in < 2s after first cache warm-up.

---

### Move 2 — Knowledge Library page

**What.** Browsable, searchable reference. Less narrative than the Study Guide; more like a glossary + cheat-sheet.

**File.** `pages/12_📖_Knowledge_Library.py`.

**Data source.** Build `gcp-pmle-quiz/data/knowledge.json` with three lists:

```json
{
  "as_of": "2026-04-27",
  "concepts": [
    {
      "id": "skew-vs-drift",
      "title": "Training-serving skew vs feature drift",
      "blurb": "Skew is training vs production. Drift is production vs production-yesterday.",
      "tags": ["§6.2", "Vertex AI Model Monitoring"],
      "research_file": "research/concepts/skew-vs-drift.md",
      "high_yield": true
    }
  ],
  "products": [
    {
      "id": "reduction-server",
      "title": "Vertex AI Reduction Server",
      "blurb": "Vertex-only all-reduce algorithm. 75% throughput uplift on NCCL GPU training, no code changes. Single highest-yield distinguishing topic per research/decision-trees/compute-selection.md.",
      "tags": ["§3.3", "GPU", "distributed training"],
      "research_file": "research/decision-trees/compute-selection.md",
      "high_yield": true
    }
  ],
  "decision_trees": [
    {
      "id": "compute-selection",
      "title": "Which compute? CPU / GPU / TPU / Reduction Server",
      "blurb": "...",
      "tags": ["§3.3"],
      "research_file": "research/decision-trees/compute-selection.md",
      "high_yield": true
    }
  ]
}
```

Bootstrap `knowledge.json` by hand from the existing research files + the 5 high-yield distinguishing topics named in `pages/8_📝_Study_Guide.py` (Skew vs drift / Reduction Server / Pipelines vs Composer / AutoML scale-to-zero trap / Gemini SFT = LoRA).

**UI.**

- **Search bar** at top (filters all three lists by `title`/`blurb`/`tags` substring, case-insensitive).
- **Tabs:** `🧠 Concepts` · `🏷 Products` · `🌳 Decision Trees` · `🏆 High-yield` (cross-cuts the others — only entries with `high_yield: true`).
- Each card: title, blurb, tag chips (clickable → filter), "📖 Read full research" expander.
- Sidebar filter: by exam section (multi-select chips). Picks any card whose `tags` include any selected section.

**Verification.**

- Type "skew" → finds the skew-vs-drift card.
- Click §5.1 chip → only pipelines-related cards remain.
- High-yield tab shows 5+ cards.
- Every `research_file` path resolves (cross-check at startup).

---

### Move 3 — Labs Integration ⭐ (the highest-leverage move)

**What.** Promote labs from link-out URLs to first-class study artifacts. Track completion, share notes, generate post-lab quizzes.

**File.** `pages/13_🧪_Labs.py` + supporting data files.

#### 3a · Data layer

Create `gcp-pmle-quiz/data/labs.json` (translated from `research/labs/skills-boost-path.md` table):

```json
{
  "as_of": "2026-04-27",
  "labs": [
    {
      "id": 7,
      "name": "Build, Train and Deploy ML Models with Keras on Google Cloud",
      "type": "course",
      "platform": "Google Skills",
      "url": "https://www.skills.google/course_templates/12",
      "duration_hours": 10.75,
      "rating": "must",
      "exam_sections": ["§3.1", "§3.2", "§4.1"],
      "weeks": [5, 6],
      "decay_risk": "low",
      "last_updated_estimate": "2026-02",
      "console_focus": ["Vertex AI Workbench", "Vertex AI Custom Training", "Vertex AI Endpoints"],
      "exam_yield_note": "TF/Keras + Vertex AI deployment hits §3.1, §3.2, §4.1 simultaneously. Longest course in the path; carries the most weight per hour."
    }
  ]
}
```

20 entries (one per Skills Boost item) — bootstrap by hand from the table in `research/labs/skills-boost-path.md`.

Create `gcp-pmle-quiz/data/lab_progress.json` (per-lab state, single-user shared like progress.json):

```json
{
  "as_of": "2026-04-27",
  "labs": {
    "7": {
      "status": "in_progress",        // "not_started" | "in_progress" | "completed" | "skipped"
      "started_at": "2026-05-25T14:00:00",
      "completed_at": null,
      "shared_notes": "Patrick: the `cloudml-hypertune` library...\nMatty Boy: lost 30 min on the lab queue, retry button works.",
      "ohhh_insights": [
        "Vertex AI HyperparameterTuningJob is just a thin wrapper around Vizier — same StudySpec.",
        "Reduction Server requires no code changes; you just declare a reducer pool in the training job spec."
      ],
      "post_lab_quiz_attempts": [
        {"timestamp": "2026-05-25T15:42:00", "score": 0.75, "wrong_ids": [356, 482]}
      ]
    }
  }
}
```

#### 3b · Loader (`utils/labs.py`)

```python
def load_labs() -> list[Lab]: ...
def load_lab_progress() -> dict[int, LabProgress]: ...
def save_lab_progress(progress: dict[int, LabProgress]) -> None: ...   # atomic write
def labs_for_week(week_num: int) -> list[Lab]: ...                     # join with weeks.json
def post_lab_quiz_questions(lab: Lab, n: int = 15) -> list[Question]:
    """Sample n questions from `quizzes_for_week` covering this lab's exam_sections."""
```

#### 3c · `pages/13_🧪_Labs.py` UI

**Top.** Stats strip: `X / 20 labs completed · Y h logged · Z h remaining (must-rated only)`.

**Filter row.**
- Sort: by Skills Boost order / by week / by rating (must/should/skip) / by status
- Filter: rating chips (must · should · skip), status chips (not started · in progress · completed)

**Lab card** (one per lab, expandable):
```
🧪 #7 · Build, Train and Deploy ML Models with Keras on Google Cloud   [must · 10.75h · §3.1, §3.2, §4.1]
[ Status: 🟡 in progress · Week 5/6 ]
> ▶️ Open lab on Google Skills
> 📝 Lab notes (markdown editor — shared between Patrick & Matty Boy)
> 💡 "Ohhh" insights (bullet list — append-only)
> ⏱️ Mark started · Mark complete · Skip
> 🎯 Post-lab drill (15 Qs from §3.1+§3.2+§4.1, scored, no in-quiz explanations) — reuses utils/quiz_runtime.py from Phase 4
> 📊 Past attempts: 75% (May 25), 90% (May 30)
```

**Sat lab session template** at the bottom of each card (collapsed by default):
```markdown
## Saturday paired session — Lab #{id}

Pre-lab (5 min)
- [ ] Patrick reads the lab description aloud
- [ ] Matty Boy opens a fresh GCP console window
- [ ] Both agree on the success criterion

During lab (90 min, switch every 30 min)
- [ ] 0:00–0:30 — Patrick types, Matty Boy reads steps
- [ ] 0:30–0:60 — switch
- [ ] 0:60–0:90 — switch
- [ ] If blocked > 5 min, post in shared chat, move on

Post-lab (10 min)
- [ ] Each names ONE "ohhh" insight (paste in 💡 field above)
- [ ] Run the post-lab drill (15 Qs)
- [ ] Mark this lab ✅ in the app
```

#### 3d · Cross-link integrations

- **Weekly Overview** — the existing 📚 Plan tab gains a *"📊 Lab status"* column showing each lab's completion. One-click jump to the Labs page anchored at this lab.
- **Mock Exam page** — at the end of a mock, *"Sections you scored < 70% on map to these labs you haven't completed"* (cross-reference `lab_progress` × `weeks.json` × the score breakdown). Only show if the suggestion is non-empty.
- **Knowledge Graph (Move 1)** — lab nodes click through to the lab card.
- **Home page** — small banner *"Labs done: 7 / 14 must-rated"* under the meme.

#### 3e · Verification

- All 20 labs render. Filter "must-only" leaves 14.
- Mark lab #4 complete → status changes; `lab_progress.json` updated atomically; surviving server restart.
- Click "Post-lab drill" on lab #7 → 15 questions all from §3.1/§3.2/§4.1 (no other sections); submit → score appended to `post_lab_quiz_attempts[]` for lab 7.
- Add a note → reload page → note persisted.
- Sat session template renders as markdown checkboxes that persist when checked.

---

## 5. Out of scope this phase

- **Per-user note attribution beyond `Patrick: ` / `Matty Boy: ` prefixes** — multi-user is still Phase 6 if anything.
- **Auto-importing notes from a Google Doc / Notion** — paste-driven for now.
- **Lab gating** ("you can't open Mock Exam #1 until you've done labs 1-7") — too prescriptive; we trust each other.
- **Video transcript search across the labs.** Out of scope; Skills Boost doesn't expose transcripts via API.
- **GitHub-style activity heatmap of lab completion.** Cute, not load-bearing. Maybe Phase 7.

---

## 6. Constraints

- **Do NOT modify** `models/questions.py`, `data/quizzes.jsonl`, `data/section-mapping.json`, `data/rebrands.json`, `data/weeks.json`, `data/gcp_products.jsonl`, `utils/__init__.py`. Phase 5 is purely additive.
- **Do NOT delete** `data/progress.json` (Quiz Mode state) or any existing lab data once written.
- **Atomic writes** for `lab_progress.json` (write `.tmp` then `os.replace`) — same pattern as Phase 2.
- **Respect the URL constraint from earlier phases** — invent NO lab URLs. Use only what's in `research/labs/skills-boost-path.md`.
- **Use absolute paths** (`Path(__file__).resolve()...`) for all data file references — Streamlit Cloud lesson learned.
- **Reuse `utils/quiz_runtime.py`** from Phase 4 for the post-lab drill — don't fork the timer/score code.

---

## 7. End-of-phase deliverables

- [ ] `gcp-pmle-quiz/data/labs.json` — 20 entries, all URLs verified to match `research/labs/skills-boost-path.md`
- [ ] `gcp-pmle-quiz/data/knowledge.json` — concepts + products + decision trees, ~25-30 entries total
- [ ] `gcp-pmle-quiz/data/lab_progress.json` — bootstrap with `{"as_of": "...", "labs": {}}`
- [ ] `gcp-pmle-quiz/utils/labs.py` — load/save + post-lab quiz sampler
- [ ] `gcp-pmle-quiz/utils/knowledge.py` (or extend `weekly.py`) — concept/product loader
- [ ] `gcp-pmle-quiz/pages/11_🕸_Knowledge_Graph.py` — Move 1
- [ ] `gcp-pmle-quiz/pages/12_📖_Knowledge_Library.py` — Move 2
- [ ] `gcp-pmle-quiz/pages/13_🧪_Labs.py` — Move 3 (the big one)
- [ ] Cross-link breadcrumbs in Weekly Overview, Mock Exam, Home page
- [ ] Streamlit dev server smoke-tested on each new page (open lab #7 → write a note → mark complete → take post-lab drill → confirm score persists)
- [ ] Final summary printed: # nodes/edges in graph, # cards in library, labs completion rate

---

## 8. Open design decisions for the agent

- **One labs page or three?** One page with collapsible cards is simplest. Three (must / should / skip) feels redundant. Default: one page, sortable.
- **Lab notes editor — markdown vs plain text?** Markdown via `st.text_area` and rendered preview side-by-side. The team already writes markdown for everything else.
- **Post-lab quiz size.** Default 15 Qs. Could go 20. Don't go above 25 — it stops being post-lab and becomes a mini-mock.
- **Persist `ohhh_insights` separately or inside `shared_notes`?** Separate — it's structured (one-line bullets) and we want to be able to surface it on the home page in a "recent insights" feed eventually.
- **Graph layout.** Stick with pyvis force-directed. If 165 nodes feels cluttered, group by section in concentric rings (cytoscape.js has built-in layouts; pyvis less so).

---

## 9. Why this scope and not bigger

Three independent moves, each shippable in a session:

- **Move 1 (Graph)** — 1.5-2h. Pretty + memorable. Less load-bearing than Move 3.
- **Move 2 (Library)** — 1-1.5h. Useful daily; the lookup-layer the Study Guide page can't be.
- **Move 3 (Labs)** — 2-3h. **The actual point.** Labs are 58 of our ~70 hours of study budget. Treating them as link-out URLs leaves 80% of the value unrealized. Tracked completion + paired-session debrief + post-lab drills turn each lab into a closed feedback loop.

If session time is short, **do Move 3 first.** Move 1 is the most fun but Move 3 is the most useful.

---

## 10. Paste-ready prompt for fresh Claude Code session

Open a fresh session in `/Users/patricktaylor/Documents/Google-PMLE/`. `CLAUDE.md` auto-loads. Paste:

~~~
You're starting a fresh session in /Users/patricktaylor/Documents/Google-PMLE/. CLAUDE.md auto-loads.

Single task this session: execute Phase 5 — knowledge graph + library + labs integration. The complete spec is at `phase5-graph-library-labs.md`. Read it cover-to-cover before doing anything.

The three moves are independent. If session time is short, do Move 3 (Labs Integration) FIRST — it's the highest-leverage. Move 1 (Graph) is the most fun but Move 3 is what unlocks the Sat 90-min paired-session protocol from study_plan.md.

Steps:

1. Read `phase5-graph-library-labs.md` cover-to-cover.

2. Read `research/labs/skills-boost-path.md` carefully — it's the source of truth for `data/labs.json` (Move 3a). Map every entry in the table to a structured JSON record by hand.

3. Create 3 tasks via TaskCreate, one per Move. The moves are independent — execute in whatever order fits the session.

4. For Move 3, the Sat-session-template + post-lab quiz are the load-bearing features. Don't skimp on them. Reuse `utils/quiz_runtime.py` from Phase 4 if it exists; otherwise build the quiz UI inline (don't fork Mock Exam state).

5. After each move, smoke-test in the browser (open the new page, click through, verify data persistence).

6. End-of-session: print a summary (# graph nodes/edges, # library cards, # labs tracked, labs completion rate after a manual test toggle).

Hard constraints:
- Phase 5 is purely additive. Do NOT modify the files listed in §6 of the spec.
- Atomic writes for lab_progress.json.
- Use absolute paths (Path(__file__).resolve()...) for all data file references — same lesson as Phase 4.
- Invent NO lab URLs. Only use what's in research/labs/skills-boost-path.md.

Estimated time: 4-6 hours, splittable across 2-3 sessions if needed.
~~~

---

## 11. After Phase 5 ships

Likely Phase 6 candidates:

1. **Multi-user progress isolation** — Patrick and Matty Boy each get their own `progress.json` / `lab_progress.json` / `week_quiz_results.json`. Sign-in via Google (or just a name dropdown).
2. **Notion / Google Doc note sync** — push `shared_notes` and `ohhh_insights` to a doc the team already uses.
3. **Question import pipeline** — when adding the Google sample form (~25 Qs) or a paid bank (~50 Qs).
4. **Public-share read-only mode** — a deploy variant that lets us share the Study Guide page + Resources page with friends without exposing progress data.
5. **Mobile layout pass** — Streamlit defaults are OK on desktop, cramped on phones. Targeted CSS tweaks for the Mock Exam timer + the Labs page card list.
