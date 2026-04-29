"""Render a week's daily tasks as an interactive Graphviz tree.

The tree is hierarchical: Week → 5/6 days → tasks per day. Each task
node carries the task's primary URL as a Graphviz ``URL`` attribute,
which Streamlit's ``st.graphviz_chart`` preserves in the rendered SVG
so clicking the node opens the source.

Usage::

    from utils.week_tree import render_week_tree
    render_week_tree(week)            # current week
    render_week_tree(week, mini=True) # compact "next week" peek

Designed to be cheap — no extra dependencies beyond Streamlit's bundled
graphviz; the DOT string is short enough that we re-render on every
page load without caching.
"""

from __future__ import annotations

import html
import textwrap

import streamlit as st

from utils.study_plan import Day, Task, Week

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

TASK_ICONS = {
    "read": "📖",
    "drill": "🤔",
    "lab": "🧪",
    "video": "📺",
    "app": "🎯",
    "external": "🔗",
    "other": "•",
}

# Subtle palette so the tree reads at a glance without screaming.
DAY_COLORS = {
    0: "#dbeafe",  # Mon — blue
    1: "#dbeafe",
    2: "#dbeafe",
    3: "#dbeafe",
    4: "#dbeafe",
    5: "#fef3c7",  # Sat — amber (lab)
    6: "#dcfce7",  # Sun — green (retro)
}
TASK_COLOR = "#f5f5f5"
ROOT_COLOR = "#fde68a"


def _short(label: str, max_chars: int) -> str:
    """Compact a task label for the tree — strip markdown link syntax,
    collapse whitespace, truncate with an ellipsis."""
    # Keep the link's display text, drop the URL.
    import re

    label = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", label)
    label = re.sub(r"`([^`]+)`", r"\1", label)
    label = " ".join(label.split())
    if len(label) > max_chars:
        label = label[: max_chars - 1].rstrip() + "…"
    return label


def _wrap(text: str, width: int) -> str:
    """Word-wrap to ``width`` chars per line for the Graphviz label."""
    return "\n".join(textwrap.wrap(text, width=width)) or text


def _day_tasks(week: Week, day_index: int) -> list[Task]:
    if day_index < 5:
        for d in week.days:
            if d.day_index == day_index:
                return d.tasks
        return []
    if day_index == 5 and week.saturday:
        return week.saturday.tasks
    if day_index == 6 and week.sunday:
        return week.sunday.tasks
    return []


def _build_dot(week: Week, *, mini: bool) -> str:
    label_max = 28 if mini else 60
    wrap_w = 18 if mini else 36
    fontsize_root = 14 if mini else 18
    fontsize_day = 11 if mini else 13
    fontsize_task = 9 if mini else 11

    lines: list[str] = ["digraph WeekTree {"]
    lines.append('    rankdir=LR;')
    lines.append('    bgcolor="transparent";')
    lines.append('    node [style="filled,rounded", shape=box, fontname="Helvetica"];')
    lines.append('    edge [color="#94a3b8"];')

    root_id = f"w{week.num}"
    root_label = _wrap(f"Week {week.num} — {week.theme}", wrap_w + 4)
    lines.append(
        f'    "{root_id}" [label="{root_label}", '
        f'fillcolor="{ROOT_COLOR}", fontsize={fontsize_root}, '
        f'tooltip="§: {", ".join(week.exam_sections)}"];'
    )

    for d_idx in range(7):
        tasks = _day_tasks(week, d_idx)
        if not tasks and d_idx != 5:  # always show Sat lab even if empty
            continue
        day_id = f"w{week.num}d{d_idx}"
        d_color = DAY_COLORS[d_idx]
        day_name = DAY_NAMES[d_idx]
        day_label = day_name if not tasks else f"{day_name} ({len(tasks)})"
        lines.append(
            f'    "{day_id}" [label="{day_label}", fillcolor="{d_color}", '
            f'fontsize={fontsize_day}];'
        )
        lines.append(f'    "{root_id}" -> "{day_id}";')

        for t_idx, t in enumerate(tasks):
            task_id = f"{day_id}t{t_idx}"
            icon = TASK_ICONS.get(t.type, "•")
            short = _short(t.label, max_chars=label_max)
            wrapped = _wrap(f"{icon} {short}", wrap_w)
            tooltip = html.escape(t.label.replace('"', "'"), quote=True)
            url_attr = ""
            if t.ref and t.ref.startswith("http"):
                # Graphviz URL becomes <a> in the SVG output.
                url_attr = f', URL="{t.ref}", target="_blank"'
            lines.append(
                f'    "{task_id}" [label="{wrapped}", fillcolor="{TASK_COLOR}", '
                f'fontsize={fontsize_task}, tooltip="{tooltip}"{url_attr}];'
            )
            lines.append(f'    "{day_id}" -> "{task_id}";')

    lines.append("}")
    return "\n".join(lines)


def render_week_tree(week: Week, *, mini: bool = False) -> None:
    """Render the week tree as a clickable Graphviz chart plus a
    fallback flat list so the hyperlinks always work even on
    SVG-restricted environments."""
    if not week:
        st.info("No week to render.")
        return
    dot = _build_dot(week, mini=mini)
    st.graphviz_chart(dot, use_container_width=True)
    if mini:
        return

    # Fallback: every task with a URL, listed below — guarantees the
    # hyperlinks are reachable even if the SVG renderer suppresses them.
    with st.expander("🔗 All clickable tasks for the week", expanded=False):
        for d_idx in range(7):
            tasks = _day_tasks(week, d_idx)
            if not tasks:
                continue
            st.markdown(f"**{DAY_NAMES[d_idx]}**")
            for t in tasks:
                icon = TASK_ICONS.get(t.type, "•")
                if t.ref and t.ref.startswith("http"):
                    st.markdown(f"- {icon} [{_short(t.label, 90)}]({t.ref})")
                else:
                    st.markdown(f"- {icon} {_short(t.label, 90)}")
