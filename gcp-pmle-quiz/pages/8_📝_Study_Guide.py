"""Study Guide — long-form synthesis of every research conclusion.

Source files: CLAUDE.md, study_plan.md, research/anecdotes/recent-passers.md,
research/question-banks/audit.md, research/labs/skills-boost-path.md, and
all eight research/concepts + research/decision-trees + research/genai files.
"""

from pathlib import Path

import streamlit as st

from utils import set_css_style


def main():
    st.set_page_config(page_title="Study Guide", page_icon="📝", layout="wide")
    set_css_style(Path("style.css"))

    # ---- Substack-style header ----
    st.markdown(
        "<h1 style='margin-bottom:0;'>How to actually study for the PMLE in 12 weeks</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#666;margin-top:4px;font-size:1.05em;'>"
        "Everything our research says about passing v3.1 — distilled into a single read. "
        "</p>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Synthesis of 14 research reports + 10 post-April-2025 passer writeups. "
        "By Patrick & Matty Boy · 2026-04-27 · ~12 min read."
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.markdown(
        """
> **TL;DR.** Plan **60-75 hours over 10-12 weeks**. Spend 25% of your time on the
> Skills Boost path, 25% on official Google docs, 50% on tagged practice questions.
> The exam tests **MLOps and Vertex AI** more than ML theory — §5 (Pipelines) is
> the heaviest section at 22%, and §3+§4 together are another 38%. GenAI is real
> but bounded at **~8-12% of questions**. Don't memorize the AndyTheFactory bank;
> drill it, then go read the actual Google docs the questions came from.
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("1 · The single most useful number: 60-75 hours")
    st.markdown(
        """
The closest behavioral match in our 10-passer corpus is **V. Narvaez (Feb 2026)** —
a "cloud newcomer" who passed in 12-15 weeks at ~1 hour weekdays + heavier weekends,
totalling **60-75 hours**. Two beginners studying together over 10-12 weeks should
plan **≥80 hours per person** (extra slack for GCP product taxonomy you've never
seen before).

Three other passers triangulate this number:

- **Andrei Paraschiv** (Feb 2026, NLP background): 30 days, "60+ days minimum if
  you lack ML AND GCP."
- **ExamCert practitioner** (Mar 2026, 2yr ML + ACE): 10 weeks, ~100-120 hours.
- **Alex Nyambura** (Jan 2026, SWE+GenAI Leader cert): 1 month nominal but
  1 *week* effective — *strongly does not recommend her own pace.*

The standard r/googlecloud and Medium recommendation is *"8 weeks for someone with
prior cloud or ML experience."* We deliberately add **2-4 weeks of slack** because
this is our first GCP cert and our first time in a serious ML lifecycle context.
"""
    )

    st.info(
        "**Action.** Block 5-6 hours/week on the calendar starting Week 1. "
        "Friday evenings = paired quiz session (30 min). Saturdays = paired lab "
        "session (90 min). Sundays = retro + weekly self-assessment quiz (60 min).",
        icon="✅",
    )

    # ---------------------------------------------------------------------
    st.header("2 · The 25 / 25 / 50 split is the canonical pacing")
    st.markdown(
        """
Narvaez's split is the only one in our corpus that gives concrete proportions:

| Activity | % of time | Approx hours (of 70) |
|---|---:|---:|
| Skills Boost / Coursera learning path | **25%** | ~17.5 h |
| Reading official Google Cloud docs directly | **25%** | ~17.5 h |
| Tagged practice exams (volume + retros) | **50%** | ~35 h |

The 50% on practice questions is the surprise. Other passers disagree on
proportions — Pozdniakova says docs are heaviest, ExamCert says console
hands-on beats docs 3:1, Paraschiv says concepts first then questions — but
everyone agrees on the **sequence**: build conceptual scaffold (Weeks 1-4) →
hands-on labs/console (Weeks 4-8) → high-volume tagged practice (Weeks 8-12).

The questions aren't a final test, they're the **primary learning loop** in the
back half. Each wrong answer becomes:
1. A note in your wrong-answer log (we track this in `data/progress.json`)
2. A doc page you read directly (Google syphons questions from official docs —
   Pozdniakova, Paraschiv)
3. An entry in your personal Anki/NotebookLM deck (Paraschiv built his own;
   no usable PMLE Anki deck exists publicly — see Resources page)
"""
    )

    # ---------------------------------------------------------------------
    st.header("3 · The exam is MLOps in a Vertex AI costume")
    st.markdown(
        """
Two seemingly contradictory passer claims:

- *"Vertex AI is 60-70% of the exam."* — Nyambura, ExamCert, Anil Kumar
- *"MLOps is 60% of the exam."* — DSumit, ExamCert (yes, the same ExamCert blog says both)

Both are right. **Vertex AI is the vehicle; MLOps is the content.** Pipelines,
Model Registry, Feature Store, Endpoints, Monitoring are simultaneously "Vertex AI"
and "MLOps" topics. There is no real conflict.

The official v3.1 weights (memorize):

| § | Domain | Weight |
|---|---|---:|
| 1 | Architecting low-code AI (BQML, AutoML, ML APIs, Agent Builder) | 13% |
| 2 | Collaborating across teams (data + models) | ~14% |
| 3 | Scaling prototypes into ML models (custom training, hyperparams, hardware) | ~18% |
| 4 | Serving and scaling models (online/batch, Feature Store, endpoints) | ~20% |
| **5** | **Pipelines + automation (highest weight)** | **~22%** |
| 6 | Monitoring AI solutions (drift, skew, Explainable AI) | ~13% |

**Section §5 is the highest-yield investment.** §3+§4 are the second-highest at
~38% combined. **§1 GenAI bullets** (Model Garden, Agent Builder, RAG) account
for an estimated **8-12% of questions**, which is meaningful but not dominant.
        """
    )

    # ---------------------------------------------------------------------
    st.header("4 · The five highest-yield distinguishing topics")
    st.markdown(
        """
These are the items that *separate* a passing answer from a wrong one in a
multi-choice scenario where two options look right. Memorize each.

#### 4.1 Skew vs drift (§6.2) — the one-liner

> **Skew is training vs production. Drift is production vs production-yesterday.**

That's it. Memorize verbatim. *Skew* compares a feature's distribution between
your training data and what's actually arriving at the endpoint. *Drift* compares
a recent window of incoming features to an earlier production window. Vertex AI
Model Monitoring v1's default drift threshold = **0.3** (don't over-memorize this
— v2 SDK examples use much smaller defaults, and v2 is still Pre-GA as of Apr
2026 but exam-fair).

Source: `research/concepts/skew-vs-drift.md`.

#### 4.2 Reduction Server (§3.3) — the highest-yield distinguishing topic, full stop

> Reduction Server is a Vertex-AI-only algorithm with documented **75% throughput uplift** on NCCL GPU training, **no code changes**.

Single biggest "right answer" surprise in distributed-training questions. If a
question asks how to speed up multi-GPU training without rewriting the code,
**Reduction Server** is almost always the answer. It implements an optimized
all-reduce on dedicated reducer VMs.

Source: `research/decision-trees/compute-selection.md`.

#### 4.3 §5 orchestrator cost lever — Pipelines vs Composer

| | Per-run cost | Idle cost |
|---|---|---|
| **Vertex AI Pipelines** | $0.03/run + compute | none |
| **Cloud Composer 3** | $0.06/DCU-hr | **~$400/month floor** on a small environment |

Single biggest input to *"which orchestrator?"* exam questions. If the question
mentions cost, ML-only workloads, or a small team, **Vertex AI Pipelines wins**.
If it mentions multi-step workflows touching many GCP services beyond ML,
**Composer wins**.

Source: `research/decision-trees/pipelines-comparison.md`.

#### 4.4 AutoML endpoint scale-to-zero trap (§4.1)

AutoML endpoints **cannot scale to zero**. An idle classification endpoint
costs **~$991/month**. Common §4 distractor: *"deploy AutoML to a Vertex
endpoint"* when **batch prediction** would do for a non-real-time use case.

If a question describes a low-traffic use case ("nightly", "weekly batch",
"few requests per hour") and offers AutoML-endpoint as an option,
**batch prediction is the right answer**.

Source: `research/decision-trees/tabular-modeling.md`.

#### 4.5 Gemini SFT is LoRA-based PEFT under the hood

Gemini supervised fine-tuning is implemented as LoRA (Low-Rank Adaptation),
which is a form of PEFT (Parameter-Efficient Fine-Tuning). Adapter sizes
**1 / 2 / 4 / 8 / 16**. Only **Gemini 2.5 Pro / Flash / Flash-Lite** are
tunable. Pro maxes at **adapter size 8**. **Preference tuning** (RLHF-style)
is **Flash and Flash-Lite only**.

Source: `research/genai/vertex-ai-overview.md`.
"""
    )

    # ---------------------------------------------------------------------
    st.header("5 · GenAI is real but bounded — don't over-weight it")
    st.markdown(
        """
There's an active disagreement in the passer corpus about how much GenAI is
on the v3.1 exam:

- **Paraschiv (Feb 2026):** *"Only about 3-4 GenAI-related questions"* (~6-8%)
- **DSumit (Nov 2025):** *"Didn't see much reference to Gen AI"*
- **Nyambura (Jan 2026):** GenAI was not notable on her exam
- **Anil Kumar (Oct 2025):** Treats GenAI as a *major* theme — outlier; he
  likely got a high-GenAI draw on a randomized exam pool
- **Omkar Rahane (Dec 2024, borderline):** ~10% of exam was GenAI

**Triangulated estimate: 8-12% of questions.** Plan a single dedicated
study week (Week 10) — don't spread GenAI across the whole 12 weeks. The
key topics actually tested:

- **Model Garden** model selection (which model for which use case)
- **Agent Builder / Gemini Enterprise Agent Platform** RAG patterns
- **Foundation-model fine-tuning** (LoRA / PEFT, see §4.5 above)
- **GenAI evaluation** — AutoSxS, side-by-side LLM eval, the new §2.3 bullet
- **Responsible AI** for generative — prompt injection, content safety
"""
    )

    st.warning(
        "**Apr 22, 2026 rebrand alert.** Vertex AI is now **Gemini Enterprise "
        "Agent Platform**. The PMLE v3.1 exam guide and Skills Boost courseware "
        "still use the 2025 names. **Translate function-first, then map to "
        "whichever name appears in the answer choice.**",
        icon="⚠️",
    )

    # ---------------------------------------------------------------------
    st.header("6 · Common exam-day surprises (so they aren't surprises)")
    st.markdown(
        """
Aggregated from the 10 passer writeups:

1. **Multiple "technically correct" answers per question.** Pick the
   Google-best-practice one — managed service > custom, cost-effective > raw
   power, AutoML/BQML > custom training when the use case fits.
2. **Few-to-zero multi-select questions on the actual exam.** Paraschiv
   reports **zero** multi-select on his exam despite practice apps including
   them. Don't burn time strategy-optimizing for multi-select; practice them
   for concept reinforcement only.
3. **GPU vs TPU infrastructure choice tested explicitly.** Often missed.
   General rule: TPU for transformer-heavy / large batch / TF-or-JAX training;
   GPU for everything else, especially mixed PyTorch ecosystems.
4. **Train/serve skew and Feature Store consistency.** Recurring traps. If
   the question describes a feature being computed differently online vs
   in batch training, the answer involves Feature Store (or its successor —
   Bigtable online serving is the safe answer post-2027 when Vertex Feature
   Store sunsets).
5. **Time pressure is real but not crushing.** Paraschiv's pacing: 50 questions
   in ~1 hour first pass + 45 min second pass + 15 min review. Nyambura got
   30 min of buffer. Don't sit on a hard question — flag and move on.
6. **The pattern-recognition "click" mid-exam.** Nyambura describes the first
   30 minutes feeling impossible until you internalize the Google decision
   pattern, after which questions accelerate. Mock exams (Weeks 11-12) are
   where you build this muscle.

Source: `research/anecdotes/recent-passers.md` §6.
"""
    )

    # ---------------------------------------------------------------------
    st.header("7 · The deprecation watch (things changing under your feet)")
    st.markdown(
        """
The PMLE exam is testing today's products, but two of them are deprecated
or sunsetting:

- **Vertex Explainable AI** — officially deprecated **March 16, 2026**.
  Shutdown **March 16, 2027**. v3.1 still tests Sampled Shapley / Integrated
  Gradients / XRAI — soak it up but expect retirement-era questions. The
  exam may or may not be updated before the shutdown.
- **Vertex AI Feature Store (Legacy + Optimized online serving)** —
  sunset **Feb 17, 2027**. No new features after May 17, 2026.
  **Bigtable online serving is the safe exam answer** for post-sunset
  scenarios. A possible "Agent Platform Feature Store" rename is propagating
  in docs as of Apr 2026.

And one major rebrand:

- **Vertex AI → Gemini Enterprise Agent Platform** (Apr 22, 2026, at Cloud
  Next 2026). Affects Agent Builder / Studio / Search only. Pipelines,
  Training, Model Registry, ML Metadata, Experiments names are intact.
  See the 🪧 Rebrand alerts tab on each Weekly Overview week for which
  weeks this affects.

Source: `CLAUDE.md` "Live state and rebrand alerts".
"""
    )

    # ---------------------------------------------------------------------
    st.header("8 · The three-bank stack (and why we don't use four)")
    st.markdown(
        """
Two beginners hitting 80% on a clean stack don't need NDA-violating dumps.
Our stack is **three banks** and stops there:

1. **Google official sample form** (free, ~15-25 Qs, v3.1 aligned). Take
   cold in Week 1 for baseline; again Week 11 for calibration.
2. **AndyTheFactory `gcp-pmle-quiz`** (free, 841 Qs, 537 GenAI-flagged).
   The workhorse — Weeks 3-8 daily drills. Already loaded into this app.
3. **One paid bank in Weeks 9-10.** First choice: Pluralsight / A Cloud Guru
   if either of us has the sub. Fallback: Whizlabs (Premium 7-day trial).
   Last resort: a vetted Udemy 2026-refresh course.

We **explicitly don't use** ExamTopics, Skillcertpro, or any of the dump
aggregators (PassQuestion, ITExams, Marks4sure, etc.). They reconstruct live
exam content, which Google's Certification Program Terms ban under sections
(c), (e), and (m). Penalties: exam invalidation and decertification.

We also **don't bother searching for** Tutorials Dojo / ExamPro / Anki decks
for PMLE — none of them exist as of Apr 2026 (TD has no PMLE-specific product;
ExamPro covers Cloud Digital Leader and Generative AI Leader only; no usable
PMLE Anki deck exists on AnkiWeb / AnkiHub).

See the **📚 Resources** page for the full audit.
"""
    )

    # ---------------------------------------------------------------------
    st.header("9 · The week-12 readiness rule")
    st.markdown(
        """
Two mock exams are scheduled into the plan (data already tagged in Phase 2 —
100 questions per pool, held out from regular Quiz Mode):

| When | What | Pass threshold |
|---|---|---:|
| **Sat Week 11** | Mock #1 — 50 Qs from `mock1-pool`, full 2-hour timed | **≥ 70%** |
| **Wed Week 12** | Mock #2 — 50 Qs from `mock2-pool`, full 2-hour timed | **≥ 80%** |
| **Sat Week 12** | **REAL EXAM** | Pass = ≥ 70% per Google |

Mock #2's threshold is **80%** (not 70%) deliberately — it gives us a buffer
above the real-exam threshold. If Mock #2 < 80%, push the real exam by a week
and use the buffer for wrong-answer drill on the weakest 3 sections.

The **⏱️ Mock Exam** page in this app surfaces those held-out 200 questions
in a timed UI. They're excluded from Quiz Mode by default so they retain
calibration value when you finally run them.
"""
    )

    # ---------------------------------------------------------------------
    st.header("10 · The session protocol")
    st.markdown(
        """
This is what we do every day, every week. Boring and structured beats
ambitious and undisciplined.

#### Daily (Mon-Fri) — 45-60 min
- **≤ 30 min** active learning (video / docs / blog)
- **≥ 15 min** active recall (quiz batch in this app)
- **5-min sync** with partner (text/Slack): *what did you cover, what stuck, what blocked*

#### Friday — paired quiz session, 30 min
- Topic-of-week, alternating reader/explainer
- 10-15 questions; both must give answer + reasoning before revealing
- Wrong = mark in app, drill again Sunday

#### Saturday — paired lab session, 90 min
- One partner reads lab steps aloud; the other types
- Switch every 30 min
- End-of-lab: each names one *"ohhh"* insight; push to shared notes

#### Sunday — retrospective, 60 min
1. Run weekly self-assessment quiz (≥ 20 Qs, this week's topic tags)
2. Review wrong answers together — explain WHY each correct answer wins
3. Each partner names: 1 thing learned, 1 stuck-on, 1 ahead-of-plan
4. Set Monday's first 30-min focus

Source: `study_plan.md`.
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("Closing — what to skip")
    st.markdown(
        """
The single hardest discipline in 12-week prep is **knowing what NOT to do**.
Per the research:

- **Do NOT** deep-dive TensorFlow/PyTorch authoring. The exam doesn't test
  coding skill. Python + SQL literacy is sufficient.
- **Do NOT** memorize derivations. Both of us are math-strong; we can skim.
- **Do NOT** over-weight GenAI. ~8-12% of the exam. One week is enough.
- **Do NOT** strategy-optimize for multi-select questions. Real exam has
  near-zero multi-select per recent passers.
- **Do NOT** read older study guides (pre-2024) as authoritative. The "AI
  Platform → Vertex AI" rename completed in 2022; pre-2024 content using
  AI Platform terminology is outdated.
- **Do NOT** use NDA-violating dump sites. Three-bank stack is enough.
- **Do NOT** lab everything. Strategic labs only — pick the ones whose
  console-clicking adds info you can't get from docs.

What's left is the actual content of the exam. Go drill.
"""
    )

    st.divider()

    st.markdown(
        "<p style='text-align:center;color:#888;font-size:0.9em;'>"
        "📂 Sources: <code>CLAUDE.md</code> · <code>study_plan.md</code> · "
        "<code>research/</code> (14 reports) · 10 passer writeups (April 2025+).<br>"
        "All claims with publication dates. Re-validate Q3 2026 if a v3.2 exam guide drops."
        "</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
