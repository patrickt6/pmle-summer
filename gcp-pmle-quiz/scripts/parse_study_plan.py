"""Phase 6a — Parse ``study_plan.md`` → ``data/study_plan.json``.

Idempotent — run on every edit of ``study_plan.md``. Returns a non-zero
exit code if the parse looks wrong (week count off, malformed bullets,
etc.) so this can be wired into pre-commit or CI later.

Heuristic, not strict — the source markdown is hand-written and the
parser tolerates minor structural drift. New section conventions can be
added by extending ``SUBHEAD_PATTERNS``.

Usage::

    cd gcp-pmle-quiz
    uv run python scripts/parse_study_plan.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent  # gcp-pmle-quiz/
sys.path.insert(0, str(_APP_DIR))

from utils import DATA_DIR  # noqa: E402
from utils.study_plan import (  # noqa: E402
    STUDY_PLAN_FILE,
    Day,
    StudyPlan,
    Task,
    TaskLink,
    Week,
)

REPO_ROOT = _APP_DIR.parent
STUDY_PLAN_MD = REPO_ROOT / "study_plan.md"

# ---------- regex helpers ----------

WEEK_HEADER_RE = re.compile(r"^## Week (\d+) — (.+?)\s*$", re.MULTILINE)
SUBHEADING_RE = re.compile(r"^### (.+?)\s*$", re.MULTILINE)
DAY_BULLET_RE = re.compile(
    r"^-\s+\*\*(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b[^*]*\.\*\*\s*(.+?)$",
    re.MULTILINE,
)
TIME_PAREN_RE = re.compile(r"\((\d+)\s*min[^)]*\)")
HOURS_RE = re.compile(r"\*\*Hours\.\*\*\s*~?(\d+(?:\.\d+)?)")
EXAM_SECTIONS_RE = re.compile(r"\*\*§s\.\*\*\s*([^·]+?)(?:·|$)")
SAT_LAB_RE = re.compile(r"\*\*Sat lab\.\*\*\s*(.+?)(?:$|\n)")
DELIVERABLE_RE = re.compile(r"^- \[\s*\]\s*(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

DAY_INDEX = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

SUBHEAD_PATTERNS: dict[str, re.Pattern[str]] = {
    "deliverables": re.compile(r"📦.*deliverables", re.IGNORECASE),
    "anchors": re.compile(r"🧠.*concept", re.IGNORECASE),
    "daily": re.compile(r"📅.*daily", re.IGNORECASE),
    "saturday": re.compile(r"🧪.*saturday", re.IGNORECASE),
    "sunday": re.compile(r"📊.*sunday", re.IGNORECASE),
    "above": re.compile(r"🚀.*above", re.IGNORECASE),
}


def _extract_links(text: str) -> list[TaskLink]:
    return [TaskLink(label=m.group(1), url=m.group(2)) for m in LINK_RE.finditer(text)]


def _classify_task(description: str, links: list[TaskLink]) -> tuple[str, str | None]:
    """Return ``(type, primary_ref)`` heuristically based on text + links."""
    lower = description.lower()
    primary = links[0] if links else None
    primary_ref = primary.url if primary else None

    if primary:
        url = primary.url.lower()
        if "skills.google" in url or "skill_badges" in url:
            return ("lab", primary_ref)
        if url.endswith(".md") or "research/" in url:
            return ("read", primary_ref)
        if "youtube.com" in url or "youtu.be" in url:
            return ("video", primary_ref)
        if url.endswith(".pdf"):
            return ("read", primary_ref)
        if "pages/" in url and ".py" in url:
            return ("app", primary_ref)
        if url.startswith("http"):
            if any(kw in lower for kw in ("quiz mode", "drill", "wrong-answer", "quiz a")):
                return ("drill", primary_ref)
            # Public docs the plan now points at instead of local .md files —
            # treat as a read when the bullet's verb says so.
            if any(kw in lower for kw in ("read ", "skim ", "review ")):
                return ("read", primary_ref)
            return ("external", primary_ref)

    if any(kw in lower for kw in ("quiz mode", "drill", "wrong-answer", "quiz a", "quiz b", "quiz c")):
        return ("drill", primary_ref)
    if any(kw in lower for kw in ("read ", "skim ", "review ")):
        return ("read", primary_ref)
    if "lab" in lower:
        return ("lab", primary_ref)
    if "watch" in lower or "video" in lower:
        return ("video", primary_ref)
    return ("other", primary_ref)


def _parse_day_bullet(line: str) -> Day | None:
    m = DAY_BULLET_RE.match(line)
    if not m:
        return None
    day_label = m.group(1)
    description = m.group(2).strip()

    # Time hint sits inside the **Day (NN min).** prefix that we just consumed.
    prefix = line[: m.end(0)]
    time_m = TIME_PAREN_RE.search(prefix)
    estimated_min = int(time_m.group(1)) if time_m else None

    links = _extract_links(description)
    task_type, ref = _classify_task(description, links)
    task = Task(
        type=task_type,
        label=description,
        description=description,
        estimated_min=estimated_min,
        ref=ref,
        links=links,
    )
    return Day(
        day_label=day_label,
        day_index=DAY_INDEX[day_label],
        estimated_min=estimated_min,
        description=description,
        tasks=[task],
    )


def _split_subsections(week_body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(SUBHEADING_RE.finditer(week_body))
    for i, m in enumerate(matches):
        head = m.group(1).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(week_body)
        body = week_body[m.end() : end]
        for key, pat in SUBHEAD_PATTERNS.items():
            if pat.search(head):
                sections[key] = body
                break
    return sections


def _bullets(body: str) -> list[str]:
    out: list[str] = []
    for line in body.splitlines():
        ln = line.strip()
        if ln.startswith("- "):
            out.append(ln[2:].strip())
    return out


def _parse_week(num: int, header_match: re.Match[str], body: str) -> Week:
    theme = header_match.group(2).strip()

    # The subtitle metadata line lives on the first non-blank line of the body.
    subtitle_line = ""
    for line in body.splitlines():
        if line.strip():
            subtitle_line = line
            break

    exam_sections: list[str] = []
    es_match = EXAM_SECTIONS_RE.search(subtitle_line)
    if es_match:
        raw = es_match.group(1).strip().rstrip("·").strip()
        exam_sections = [p.strip() for p in raw.split(",") if p.strip()]

    estimated_hours = None
    h_match = HOURS_RE.search(subtitle_line)
    if h_match:
        estimated_hours = float(h_match.group(1))

    saturday_lab_label = None
    saturday_lab_url = None
    sl_match = SAT_LAB_RE.search(subtitle_line)
    if sl_match:
        sl_raw = sl_match.group(1).strip()
        sl_links = _extract_links(sl_raw)
        if sl_links:
            saturday_lab_label = sl_links[0].label
            saturday_lab_url = sl_links[0].url
        else:
            saturday_lab_label = sl_raw

    sections = _split_subsections(body)

    deliverables: list[Task] = []
    if "deliverables" in sections:
        for m in DELIVERABLE_RE.finditer(sections["deliverables"]):
            text = m.group(1).strip()
            links = _extract_links(text)
            ttype, ref = _classify_task(text, links)
            deliverables.append(
                Task(type=ttype, label=text, description=text, ref=ref, links=links)
            )

    concept_anchors: list[str] = (
        _bullets(sections["anchors"]) if "anchors" in sections else []
    )

    days: list[Day] = []
    if "daily" in sections:
        for line in sections["daily"].splitlines():
            day = _parse_day_bullet(line)
            if day is not None:
                days.append(day)

    saturday_day: Day | None = None
    if "saturday" in sections:
        text = sections["saturday"].strip()
        first_para = text.split("\n\n")[0]
        time_m = TIME_PAREN_RE.search(first_para)
        est_min = int(time_m.group(1)) if time_m else None
        links = _extract_links(first_para)
        ttype, ref = _classify_task(first_para, links)
        saturday_day = Day(
            day_label="Sat",
            day_index=5,
            estimated_min=est_min,
            description=first_para,
            tasks=[
                Task(
                    type="lab" if ttype == "other" else ttype,
                    label=first_para,
                    description=first_para,
                    estimated_min=est_min,
                    ref=ref,
                    links=links,
                )
            ],
        )

    sunday_day: Day | None = None
    sunday_quiz_target: float | None = None
    if "sunday" in sections:
        text = sections["sunday"].strip()
        # Strip markdown bold so `≥ **75 %**` matches the same regex as `≥ 70 %`.
        target_m = re.search(r"≥\s*(\d{1,3})\s*%", text.replace("**", ""))
        if target_m:
            sunday_quiz_target = int(target_m.group(1)) / 100.0
        sunday_tasks: list[Task] = []
        for raw in _bullets(text):
            links = _extract_links(raw)
            ttype, ref = _classify_task(raw, links)
            sunday_tasks.append(
                Task(
                    type="drill" if ttype == "other" else ttype,
                    label=raw,
                    description=raw,
                    ref=ref,
                    links=links,
                )
            )
        if sunday_tasks:
            first_line = text.splitlines()[0] if text else ""
            sunday_day = Day(
                day_label="Sun",
                day_index=6,
                description=first_line,
                tasks=sunday_tasks,
            )

    above: list[Task] = []
    if "above" in sections:
        for raw in _bullets(sections["above"]):
            links = _extract_links(raw)
            ttype, ref = _classify_task(raw, links)
            above.append(Task(type=ttype, label=raw, description=raw, ref=ref, links=links))

    return Week(
        num=num,
        theme=theme,
        exam_sections=exam_sections,
        estimated_hours=estimated_hours,
        saturday_lab_label=saturday_lab_label,
        saturday_lab_url=saturday_lab_url,
        deliverables=deliverables,
        concept_anchors=concept_anchors,
        days=days,
        saturday=saturday_day,
        sunday=sunday_day,
        above_and_beyond=above,
        sunday_quiz_target=sunday_quiz_target,
    )


def parse_study_plan(md_text: str) -> StudyPlan:
    headers = list(WEEK_HEADER_RE.finditer(md_text))
    if not headers:
        raise ValueError("No '## Week N — Theme' headers found in study_plan.md")

    weeks: list[Week] = []
    for i, m in enumerate(headers):
        num = int(m.group(1))
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(md_text)
        body = md_text[start:end]
        weeks.append(_parse_week(num, m, body))

    weeks.sort(key=lambda w: w.num)
    return StudyPlan(as_of=date.today().isoformat(), weeks=weeks)


def main() -> int:
    if not STUDY_PLAN_MD.exists():
        print(f"❌ {STUDY_PLAN_MD} not found")
        return 1
    md = STUDY_PLAN_MD.read_text(encoding="utf-8")
    plan = parse_study_plan(md)

    if len(plan.weeks) != 12:
        print(f"❌ Expected 12 weeks, parsed {len(plan.weeks)}")
        return 1
    issues: list[str] = []
    for w in plan.weeks:
        if not w.days:
            issues.append(f"week {w.num}: 0 daily breakdown bullets")
        if not w.exam_sections:
            issues.append(f"week {w.num}: no exam_sections")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STUDY_PLAN_FILE.write_text(
        json.dumps(plan.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"✓ parsed {len(plan.weeks)} weeks → {STUDY_PLAN_FILE.name}")
    for w in plan.weeks:
        print(
            f"   week {w.num:2d} │ {len(w.days)} days │ "
            f"{len(w.deliverables)} deliverables │ "
            f"{len(w.concept_anchors)} anchors │ "
            f"target={int(w.sunday_quiz_target * 100) if w.sunday_quiz_target else '—'}%"
        )
    if issues:
        print("\n⚠ parse warnings:")
        for it in issues:
            print(f"   - {it}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
