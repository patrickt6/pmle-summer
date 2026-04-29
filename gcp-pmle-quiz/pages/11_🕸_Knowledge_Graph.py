"""Phase 5 Move 1 — Knowledge Graph.

Multi-type force-directed graph: exam sections (blue) ↔ GCP products (green) ↔
concepts/decision-trees (purple) ↔ labs (orange) ↔ rebrand-old names (grey,
dashed). Click a node → see its 1-hop neighborhood; sidebar filters node
types.

Distinct from `pages/2_☁️_GCP_Products.py` which renders only the
product↔dependency graph from `gcp_products.jsonl`. This page joins on the
Phase-2 + Phase-3 + Phase-5 data files to surface cross-type connections.
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from pyvis.network import Network

from utils import DATA_DIR, set_css_style
from utils.profile_ui import render_sidebar
from utils.knowledge import load_knowledge
from utils.labs import load_labs
from utils.weekly import load_rebrands, load_weeks


COLORS = {
    "section": "#3b82f6",
    "product": "#22c55e",
    "concept": "#a855f7",
    "decision_tree": "#a855f7",
    "lab": "#f97316",
    "rebrand_old": "#9ca3af",
}


def _load_section_mapping() -> dict:
    with (DATA_DIR / "section-mapping.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_graph() -> Network:
    weeks = load_weeks()
    knowledge = load_knowledge()
    labs = load_labs()
    rebrands = load_rebrands()
    section_mapping = _load_section_mapping()

    net = Network(
        height="700px",
        width="100%",
        bgcolor="#0e1117",
        font_color="#e6e6e6",
        directed=False,
        notebook=False,
    )
    net.barnes_hut(gravity=-9000, central_gravity=0.25, spring_length=160, spring_strength=0.04, damping=0.09)
    net.toggle_physics(True)

    # Sections (from weeks.json)
    sections: set[str] = set()
    for w in weeks:
        for s in w.exam_sections:
            sections.add(s)
    for s in sorted(sections):
        net.add_node(
            f"section::{s}",
            label=s,
            title=f"Exam section {s}",
            color=COLORS["section"],
            shape="hexagon",
            value=30,
            group="section",
        )

    # Products (from section-mapping.json — every pattern that names a product is a node)
    product_nodes: set[str] = set()
    for rule in section_mapping.get("rules", []):
        section = rule["section"]
        for pattern in rule.get("patterns", []):
            # Heuristic: title-case product-like patterns become nodes
            if any(c.isupper() for c in pattern) or pattern in {"vertex ai pipelines", "vertex ai endpoint", "vertex ai endpoints"}:
                pname = pattern.title() if pattern.islower() else pattern
                product_nodes.add(pname)
                section_id = f"section::{section}"
                product_id = f"product::{pname}"
                if pname not in product_nodes or product_id not in [n["id"] for n in net.nodes]:
                    pass

    # Better: collect product nodes from knowledge.json product list (curated)
    for p in knowledge.products:
        pid = f"product::{p.title}"
        net.add_node(
            pid,
            label=p.title,
            title=f"<b>{p.title}</b><br/>{p.blurb}",
            color=COLORS["product"],
            shape="box",
            value=24,
            group="product",
        )
        for tag in p.tags:
            if tag.startswith("§") and f"section::{tag}" in [n["id"] for n in net.nodes]:
                net.add_edge(pid, f"section::{tag}", color="#22c55e88", width=1.5)

    # Concepts + decision trees (from knowledge.json)
    for c in knowledge.concepts:
        cid = f"concept::{c.id}"
        net.add_node(
            cid,
            label=c.title,
            title=f"<b>{c.title}</b><br/>{c.blurb}",
            color=COLORS["concept"],
            shape="ellipse",
            value=18 if c.high_yield else 14,
            group="concept",
        )
        for tag in c.tags:
            if tag.startswith("§") and f"section::{tag}" in [n["id"] for n in net.nodes]:
                net.add_edge(cid, f"section::{tag}", color="#a855f788", width=1.2)
    for dt in knowledge.decision_trees:
        did = f"decision::{dt.id}"
        net.add_node(
            did,
            label=f"⭐ {dt.title}",
            title=f"<b>Decision tree:</b> {dt.title}<br/>{dt.blurb}",
            color=COLORS["decision_tree"],
            shape="diamond",
            value=22,
            group="decision_tree",
        )
        for tag in dt.tags:
            if tag.startswith("§") and f"section::{tag}" in [n["id"] for n in net.nodes]:
                net.add_edge(did, f"section::{tag}", color="#a855f7cc", width=1.6)

    # Labs (from labs.json)
    for l in labs:
        if l.rating == "skip":
            continue
        lid = f"lab::{l.id}"
        rating_emoji = "🏆" if l.rating == "must" else "🟡"
        net.add_node(
            lid,
            label=f"{rating_emoji} #{l.id}",
            title=f"<b>#{l.id} {l.name}</b><br/>{l.duration_hours}h · {l.rating}<br/>{l.exam_yield_note}",
            color=COLORS["lab"],
            shape="dot",
            value=14 + (8 if l.rating == "must" else 0),
            group="lab",
        )
        for s in l.exam_sections:
            sid = f"section::{s}"
            if sid in [n["id"] for n in net.nodes]:
                net.add_edge(lid, sid, color="#f9731688", width=1)

    # Rebrands (old → new)
    for r in rebrands:
        oid = f"rebrand::{r.old}"
        net.add_node(
            oid,
            label=r.old,
            title=f"<b>OLD:</b> {r.old}<br/><b>NEW:</b> {r.new}<br/>Renamed: {r.rebranded_at}",
            color=COLORS["rebrand_old"],
            shape="dot",
            value=10,
            group="rebrand_old",
        )
        # Edge to current product if we have it
        for p in knowledge.products:
            if r.new.lower() in p.title.lower() or p.title.lower() in r.new.lower():
                net.add_edge(oid, f"product::{p.title}", color="#9ca3af", dashes=True, width=1)

    return net


@st.cache_resource(show_spinner=False)
def _cached_graph_html() -> str:
    net = _build_graph()
    return net.generate_html(notebook=False)


def main() -> None:
    st.set_page_config(page_title="Knowledge Graph", page_icon="🕸", layout="wide")
    set_css_style(Path("style.css"))
    render_sidebar()

    st.title("🕸 Knowledge Graph")
    st.caption(
        "Sections (blue hex) · products (green box) · concepts (purple ellipse) · "
        "decision trees (purple diamond) · labs (orange dot) · old rebrand names "
        "(grey dot, dashed edge)."
    )

    with st.sidebar:
        st.header("Legend & filters")
        st.markdown(
            "- 🟦 **Section** — exam blueprint (§1.1 … §6.2)\n"
            "- 🟩 **Product** — GCP service (curated from knowledge.json)\n"
            "- 🟪 **Concept** — exam-section concept card\n"
            "- 🔷 **Decision tree** — high-yield product-selection card\n"
            "- 🟧 **Lab** — Skills Boost item\n"
            "- ⚪ **Rebrand-old** — historical product name (grey, dashed edge to current name)"
        )
        st.markdown("---")
        st.caption(
            "Tip: hover a node for details. Drag the canvas. Use mouse wheel to zoom. "
            "Click a node to focus it; the surrounding force layout rebalances."
        )
        st.markdown("---")
        if st.button("🔄 Rebuild graph"):
            _cached_graph_html.clear()
            st.rerun()

    html = _cached_graph_html()
    st.components.v1.html(html, height=720, scrolling=True)

    st.divider()
    st.subheader("How to use this view")
    st.markdown(
        "**For a weak section.** Find the §X.Y blue hex, look at its connected products, "
        "labs, and concepts. Mark untouched labs as the next thing to do.\n\n"
        "**For an unfamiliar product name.** Search the rebrand-old grey dots — if it's there, "
        "follow the dashed edge to the current name.\n\n"
        "**For exam-day calibration.** Decision-tree diamonds are high-yield. If a decision "
        "tree's connected sections include any of your weak ones, drill that tree first."
    )


if __name__ == "__main__":
    main()
