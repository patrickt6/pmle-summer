"""Phase 3 — Weekly Overview page.

Per-week catch-all dashboard: 5 tabs (Plan, Research, Drill, Rebrand alerts,
Resources). Read-only aggregator. Drill tab pre-filters quizzes to the week's
exam sections and switches to Quiz Mode.
"""

import random
from pathlib import Path

import streamlit as st

from utils import load_progress, set_css_style
from utils.profile_ui import render_sidebar
from utils.labs import LabProgress, load_lab_progress, load_labs
from utils.research_links import label_for
from utils.session import cache_session
from utils.weekly import (
    Rebrand,
    Week,
    current_week_number,
    load_rebrands,
    load_weeks,
    progress_for_week,
    quizzes_for_week,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _section_question_counts(week: Week) -> tuple[int, int]:
    """Return (n_excl_mock, n_incl_mock) for the week's scope."""
    return (
        len(quizzes_for_week(week, exclude_mock=True)),
        len(quizzes_for_week(week, exclude_mock=False)),
    )


def _render_plan_tab(week: Week) -> None:
    st.subheader("Skills Boost / Google Skills items")
    if week.labs:
        # Phase 5 cross-link: surface Labs page status alongside each lab
        all_labs = {l.id: l for l in load_labs()}
        lab_progress = load_lab_progress()
        status_emoji = {
            "not_started": "🟢",
            "in_progress": "🟡",
            "completed": "🔵",
            "skipped": "⚪",
        }
        rows = []
        for lab in week.labs:
            tracked = all_labs.get(lab.id)
            prog = lab_progress.get(lab.id) or LabProgress()
            status = status_emoji.get(prog.status, "🟢")
            rating = tracked.rating if tracked else "?"
            link = f"[#{lab.id}]({lab.url})" if lab.url else f"#{lab.id}"
            rows.append({
                "Status": status,
                "Lab": link,
                "Name": lab.name,
                "Rating": rating,
                "Hours": f"{tracked.duration_hours:g}" if tracked else "?",
            })
        st.dataframe(rows, hide_index=True, use_container_width=True)
        if st.button("🧪 Open Labs page", key="open_labs_from_plan"):
            st.switch_page("pages/13_🧪_Labs.py")
    else:
        st.info("No Skills Boost items scheduled this week.")

    st.subheader("Exam guide section pointer")
    st.markdown(
        f"Primary focus: **{week.primary_section}**. Subsections covered: "
        + ", ".join(f"`{s}`" for s in week.exam_sections)
    )

    st.subheader("Time and milestone")
    cols = st.columns(2)
    cols[0].metric("Hours target", f"{week.hours_target:g} h")
    if week.milestone:
        cols[1].metric("Milestone", week.milestone)
    else:
        cols[1].metric("Milestone", "—")


def _render_research_tab(week: Week) -> None:
    if not week.research_files:
        st.info("No canonical sources mapped to this week.")
        return

    decision_set = set(week.decision_trees)
    decision_urls = [f for f in week.research_files if f in decision_set]
    other_urls = [f for f in week.research_files if f not in decision_set]

    if decision_urls:
        st.subheader("⭐ Decision Trees")
        for url in decision_urls:
            st.markdown(f"- 📖 [{label_for(url)} ↗]({url})")
        st.divider()

    if other_urls:
        st.subheader("Reference docs")
        for url in other_urls:
            st.markdown(f"- 📖 [{label_for(url)} ↗]({url})")


def _render_drill_tab(week: Week) -> None:
    progress = load_progress()
    week_qs = quizzes_for_week(week)
    sliced = progress_for_week(week, progress)

    cols = st.columns(3)
    cols[0].metric("Total in scope", len(week_qs))
    cols[1].metric("Not answered", len(sliced["not_answered"]))
    cols[2].metric("Wrong last time", len(sliced["answered_incorrectly"]))

    st.markdown(
        "Both buttons start a Quiz Mode round filtered to **this week's exam "
        "sections only**. Mock-pool questions are excluded so they stay held "
        "out for Mock #1 / #2."
    )

    bcol1, bcol2 = st.columns(2)
    fresh_disabled = len(sliced["not_answered"]) == 0
    wrong_disabled = len(sliced["answered_incorrectly"]) == 0

    if bcol1.button(
        "🟢 Start fresh round",
        type="primary",
        disabled=fresh_disabled,
        help="Drill questions you haven't answered yet for this week's sections.",
    ):
        not_answered_ids = set(sliced["not_answered"])
        filtered = [q for q in week_qs if q.id in not_answered_ids]
        _hand_off_to_quiz_mode(filtered)

    if bcol2.button(
        "🔁 Wrong-answer drill",
        disabled=wrong_disabled,
        help="Re-drill questions you got wrong for this week's sections.",
    ):
        wrong_ids = set(sliced["answered_incorrectly"])
        filtered = [q for q in week_qs if q.id in wrong_ids]
        _hand_off_to_quiz_mode(filtered)

    if fresh_disabled:
        st.caption("All week-scoped questions already answered — try the wrong-answer drill.")


def _hand_off_to_quiz_mode(filtered_questions: list) -> None:
    if not filtered_questions:
        st.warning("No questions match this filter.")
        return
    random.shuffle(filtered_questions)
    st.session_state.quizzes = filtered_questions
    st.session_state.quiz_in_progress = True
    st.session_state.quiz_mode_pos = 0
    st.session_state.quiz_mode_round_progress = {}
    st.session_state.quiz_mode_answered = False
    cache_session()
    st.switch_page("pages/3_🤔_Quiz_Mode.py")


def _render_rebrand_tab(week: Week, all_rebrands: list[Rebrand]) -> None:
    if not week.rebrand_alerts:
        st.info("No rebrand alerts for this week.")
        return

    olds = set(week.rebrand_alerts)
    matched = [r for r in all_rebrands if r.old in olds]

    if not matched:
        st.warning(
            "Week lists rebrand alerts but none matched `rebrands.json`. "
            "Check the `old` strings in `data/weeks.json` for typos."
        )
        return

    rows = []
    for r in matched:
        ctx = r.context or r.note or ""
        rows.append(
            {
                "Old name": r.old,
                "Current name": r.new,
                "Renamed": r.rebranded_at,
                "Context": ctx,
            }
        )
    st.dataframe(rows, hide_index=True, use_container_width=True)


def _render_resources_tab(week: Week) -> None:
    if not week.resources:
        st.info("No extra resources for this week.")
        return

    by_kind: dict[str, list] = {}
    for r in week.resources:
        by_kind.setdefault(r.kind, []).append(r)

    order = ["official", "community", "video", "paid", "book"]
    seen = set()
    for kind in order:
        if kind not in by_kind:
            continue
        seen.add(kind)
        st.subheader(kind.capitalize())
        for r in by_kind[kind]:
            if r.url:
                st.markdown(f"- [{r.title}]({r.url})")
            else:
                st.markdown(f"- {r.title}")

    # Any unexpected kinds
    for kind, items in by_kind.items():
        if kind in seen:
            continue
        st.subheader(kind.capitalize())
        for r in items:
            if r.url:
                st.markdown(f"- [{r.title}]({r.url})")
            else:
                st.markdown(f"- {r.title}")


def main() -> None:
    st.set_page_config(page_title="Weekly Overview", layout="wide")
    set_css_style(Path("style.css"))
    render_sidebar()
    st.title("📅 Weekly Overview")

    weeks = load_weeks()
    if not weeks:
        st.error("`data/weeks.json` is missing or empty. Run Phase 3 Move 1 first.")
        return

    rebrands = load_rebrands()

    default_week = current_week_number()
    if "weekly_overview_selected_week" not in st.session_state:
        st.session_state.weekly_overview_selected_week = default_week

    week_options = [w.week for w in weeks]
    week_labels = {w.week: f"Week {w.week} — {w.title}" for w in weeks}
    try:
        default_idx = week_options.index(st.session_state.weekly_overview_selected_week)
    except ValueError:
        default_idx = 0

    selected = st.selectbox(
        "Pick a study week",
        options=week_options,
        index=default_idx,
        format_func=lambda x: week_labels[x],
        key="weekly_overview_selected_week",
    )
    week = next(w for w in weeks if w.week == selected)

    n_excl, n_incl = _section_question_counts(week)
    caption_parts = [
        f"{week.hours_target:g}h target",
        f"{week.primary_section} focus",
        f"{n_excl} questions in scope (mock excluded)",
    ]
    if week.milestone:
        caption_parts.append(f"🏁 {week.milestone}")
    st.header(f"Week {week.week} — {week.title}")
    st.caption(" · ".join(caption_parts))

    plan_tab, research_tab, drill_tab, rebrand_tab, resources_tab = st.tabs(
        ["📚 Plan", "🧠 Research", "🤔 Drill", "🪧 Rebrand alerts", "🔗 Resources"]
    )

    with plan_tab:
        _render_plan_tab(week)
    with research_tab:
        _render_research_tab(week)
    with drill_tab:
        _render_drill_tab(week)
    with rebrand_tab:
        _render_rebrand_tab(week, rebrands)
    with resources_tab:
        _render_resources_tab(week)

    st.divider()
    st.caption("Edit this week's plan in `data/weeks.json`.")


if __name__ == "__main__":
    main()
