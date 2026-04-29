"""Resources — every mock-question bank and resource from the research, in one place.

All entries link to public sources: AndyTheFactory's repo, the Google Skills
ML Engineer path, Andrei Paraschiv's pass writeup, and the canonical Vertex
AI / Gemini Enterprise Agent Platform docs.
"""

from pathlib import Path

import streamlit as st

from utils import set_css_style


def main():
    st.set_page_config(page_title="Resources", page_icon="📚", layout="wide")
    set_css_style(Path("style.css"))

    st.title("📚 Question Banks & Resources to Add")
    st.caption(
        "Master list, ranked and audited as of 2026-04-26. "
        "Source: [AndyTheFactory gcp-pmle-quiz repo](https://github.com/AndyTheFactory/gcp-pmle-quiz) + [Google Skills ML Engineer learning path](https://www.skills.google/paths/17)."
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("✅ Use these — practice question banks")
    st.markdown(
        """
- **Google official sample form** — ~15-25 scenario items, free, ungraded, exam-guide v3.1 aligned. Take *cold* before Week 1 (baseline) and again in Week 11 (calibration).
  - https://docs.google.com/forms/d/e/1FAIpQLSeYmkCANE81qSBqLW0g2X7RoskBX9yGYQu-m1TtsjMvHabGqg/viewform
- **AndyTheFactory `gcp-pmle-quiz` (already on disk)** — 841 verified questions, **537/841 hit v3.1 GenAI keywords** — unusually strong for a free community bank. Author transparent about provenance. Workhorse bank for Weeks 3-8.
  - Repo: https://github.com/AndyTheFactory/gcp-pmle-quiz
  - Author writeup (provenance): https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4
- **Pluralsight / A Cloud Guru PMLE practice exams** — bundled in standard subscription ($29/mo or $299/yr). Refreshed Jan 2026 against v3.1. **Add in Weeks 9-10** if either learner has a sub.
  - https://help.pluralsight.com/hc/en-us/articles/24392127517972-Google-Cloud-certification-practice-exams
"""
    )

    st.subheader("⚠️ Maybe — vet before paying")
    st.markdown(
        """
- **Whizlabs PMLE** — Premium $49/mo or $199/yr; standalone product page hides Q-count. v3.1 GenAI coverage looks incomplete (free-question blog still dated 2021). Use the 7-day Premium trial only if Pluralsight isn't available.
  - Pricing: https://www.whizlabs.com/pricing/
  - Free 25 sample Qs (older content): https://www.whizlabs.com/blog/gcp-professional-machine-learning-engineer-questions/
- **Top Udemy PMLE refresh courses** — $10-20 on sale, ~250-360 Qs across 4-6 timed tests. **Spot-check 5-10 free preview questions against ExamTopics before buying** — several Udemy courses recycle dump content. Examples (no #1 author equivalent to Bonso for PMLE):
  - https://www.udemy.com/course/google-professional-machine-learning-engineer-exam-prep-2025/
  - https://www.udemy.com/course/2026-google-professional-machine-learning-engineer-exams/
- **ExamCert PMLE practice tests** — referenced by one passer (March 2026 writeup); the writeup is itself a vendor blog so weight accordingly.
  - https://www.examcert.app/blog/gcp-ml-engineer-study-plan-2026/
"""
    )

    st.subheader("🚫 Do NOT use — Google Terms violations")
    st.markdown(
        """
These reconstruct live exam content (a textbook braindump). Google's Certification Program Terms ban this under sections (c), (e), (m); penalties include exam invalidation and decertification.
- **ExamTopics PMLE** — 300+ "actual Q&As reconstructed by test-takers". Free + $149.
- **Skillcertpro PMLE** — 887 Qs / 15 tests, $19.99. Product page literally says *"Taken exclusively from the previous real exams"*. Trustpilot snippet: "about 30% of answers are plain wrong."
- **PassQuestion / ITExams / Marks4sure / Pass4itsure / Certification-Questions / DumpsPedia / ExamCollection / PrepAway / DumpsArena / DumpsGate / CloudPass / certshero / Validexamdumps / Pass4success** — all market as "exam dumps", $20-80, weekly "updates" tracking real exam revisions.
- Google Certification Terms (Aug 31 2021, current): https://cloud.google.com/certification/terms/index-20210831
"""
    )

    st.subheader("❌ Doesn't exist for PMLE (don't waste time searching)")
    st.markdown(
        """
- **Tutorials Dojo / Jon Bonso** — TD has no PMLE-specific product as of Apr 2026 (gold standard for AWS, but they haven't shipped GCP PMLE). Re-check mid-prep — if it ships, promote to top 2.
- **ExamPro / Andrew Brown** — no PMLE practice-test product on exampro.co or in his Udemy catalog. His GCP coverage is Cloud Digital Leader and Generative AI Leader. His free GenAI Leader videos are still useful for grounding.
- **Anki decks** — no usable PMLE-specific deck on AnkiWeb / AnkiHub / GoogleCloudPlatform/google-cloud-flashcards. **Build your own** from wrong-answer NotebookLM exports, or skip Anki entirely.
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("🎓 Learning paths and courses")
    st.markdown(
        """
- **Google Skills (formerly Cloud Skills Boost) — ML Engineer Learning Path 17** — 20 activities, ~50-55 hrs nominal, ~85-90h wall-clock for two beginners. **The single most-cited resource** across all 10 recent passer writeups.
  - https://www.skills.google/paths/17
  - Pricing: Starter free (35 monthly credits), Pro $29/mo, Career Certificates $349/yr. 7-day trial.
  - **Time the Pro trial** to start Week 4 (Feature Engineering — peak lab consumption).
- **Google Cloud Innovators / GEAR program** — extra 35 credits/month free. Stack with Starter for ~70 credits/month covering early skill badges (#2, #4, #5).
  - https://cloud.google.com/innovators
- **Google Developer ML Crash Course** (free) — DSumit calls it "essential" for the ML fundamentals layer.
  - https://developers.google.com/machine-learning/crash-course
- **Coursera Google Cloud ML Engineer learning path** — same content as Skills Boost, sometimes preferred by people who like Coursera's UX.
- **Google's *ML Design Patterns* book** (free online) — recommended by one passer for the patterns vocabulary.
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("📖 Official Google docs (read these directly — questions are syphoned from them)")
    st.markdown(
        """
- **PMLE v3.1 exam guide PDF** — read cover-to-cover Week 1, then again Week 11.
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf
- **PMLE certification page** — links the sample form and the OnAir webinars.
  - https://cloud.google.com/learn/certification/machine-learning-engineer
- **Google's *Rules of Machine Learning*** — referenced by Paraschiv as one of the 11 best-practice docs.
  - https://developers.google.com/machine-learning/guides/rules-of-ml
- **Vertex AI documentation** (note: now `docs.cloud.google.com/...` after the 2025 hostname migration; old URLs 301-redirect)
  - Pipelines: https://cloud.google.com/vertex-ai/docs/pipelines/introduction
  - Feature Store: https://cloud.google.com/vertex-ai/docs/featurestore
  - Model Monitoring: https://cloud.google.com/vertex-ai/docs/model-monitoring/overview
  - Predictions: https://cloud.google.com/vertex-ai/docs/predictions/overview
  - Custom Training: https://cloud.google.com/vertex-ai/docs/training/overview
  - Vizier (hyperparameter tuning): https://docs.cloud.google.com/vertex-ai/docs/vizier/overview
  - Generative AI overview: https://cloud.google.com/vertex-ai/generative-ai/docs/overview
- **BigQuery ML docs** — §1.1 is *entirely* BQML.
  - https://cloud.google.com/bigquery-ml/docs
- **Cloud OnAir certification webinars** — recorded sessions explain exam intent without burning Skills credits.
  - https://cloudonair.withgoogle.com
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("✍️ First-hand passer writeups (post-v3.1, April 2025+)")
    st.markdown(
        """
Read these for the *strategy* (not the content). Cassiopeia is the closest behavioral match to two beginners studying together — make her writeup the default template.

- **V. Narvaez (Cassiopeia)** — Feb 2026, *recommended baseline.* 25/25/50 split (path / docs / practice), ~60-75h, 12-15 weeks.
  - https://medium.com/@vnarvaezt/prepare-for-the-professional-machine-learning-certification-2026-and-boost-your-skills-0f6cf3f4b78a
- **Andrei Paraschiv** — Feb 2026. 30 days, NLP background, ZERO multi-select on his exam, 3-4 GenAI questions. Author of the AndyTheFactory bank.
  - https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4
- **Anil Kumar (renewal)** — Oct 2025. The "GenAI is a major theme" voice — outlier vs. the others; he likely got a high-GenAI draw.
  - https://medium.com/google-cloud/balancing-ai-and-wellness-my-journey-renewing-the-google-cloud-professional-machine-learning-0c3649e31a4a
- **Natalia Pozdniakova** — Dec 2025. "Reading comprehension is 50% of the exam."
  - https://medium.com/@natalia.pozdniakova/how-i-passed-the-gcp-professional-machine-learning-engineer-exam-in-one-month-bd51c7ffc16a
- **Alex Nyambura** — Jan 2026. SWE+GenAI Leader; 1-week effective intensive. "60-70% Vertex AI" + pattern-recognition story.
  - https://blog.lxmwaniky.me/pmle
- **Steven Chen** — Jul 2025. *"Register for the exam 3 months ahead — locking the date is the single biggest accountability lever."*
  - https://steven-chen.medium.com/preparing-google-cloud-professional-machine-learning-engineer-certificate-in-2025-7035018d5d84
- **Matías Salinas** — Jun 2025 (paywalled).
  - https://msalinas92.medium.com/how-i-passed-the-google-cloud-professional-machine-learning-engineer-certification-and-what-i-3d3066708124
- **ExamCert practitioner** (vendor disclosure) — Mar 2026. *"Every hour in the console is worth three hours reading docs."*
  - https://www.examcert.app/blog/gcp-ml-engineer-study-plan-2026/
- **Google Developer Forum thread** (DSumit Nov 2025, Dale Monteiro Jan 2026 comments)
  - https://discuss.google.dev/t/google-clouds-professional-ml-engineer-pmle-exam-how-i-passed-in-30-days-and-you-can-too/179510
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("🛠️ Free / trial-friendly content (burn these BEFORE you subscribe)")
    st.markdown(
        """
- v3.1 exam guide PDF (free, official, definitive)
- Skills Boost item **#11 Introduction to Generative AI** (free 30-min video)
- Skills Boost item **#12 Introduction to LLMs** (free 10-min video)
- Skills Boost item **#9 MLOps Getting Started** (often inside free-tier window)
- Google Innovators sign-up — extra 35 unrestricted learning credits/month
- The Google free sample form (above)
- Cloud OnAir certification webinars (free, recorded)
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("📺 Video / channel inventory (PMLE-relevant)")
    st.markdown(
        """
For embedded playable videos see the **📺 Useful Videos** page. Sources to consider adding there:

- **ExamPro / Andrew Brown YouTube** — free GCP video content, especially Generative AI Leader walkthroughs.
  - https://www.youtube.com/channel/UC2EsmbKnDNE7y1N3nZYCuGw
- **Paul Kamau (Medium → YouTube)** — referenced by Nyambura as motivational/framework content.
- **Google Cloud Tech YouTube** — official tutorials on Vertex AI, Pipelines, Feature Store.
  - https://www.youtube.com/@googlecloudtech
- **Jash Radia — ML Engineer Cert Review** (already added)
  - https://www.youtube.com/watch?v=M4-iqESGPns
- **iCanStudy 3-hour study session** (already on home page)
  - https://www.youtube.com/watch?v=74cOUSKXMz0
"""
    )

    st.divider()

    # ---------------------------------------------------------------------
    st.header("📦 Canonical references this site cites")
    st.markdown(
        """
The Plan, Study Guide, and Knowledge Library all link back to these public sources. Open via the **📅 Weekly Overview** page or jump straight to the docs:

- [AndyTheFactory gcp-pmle-quiz repo](https://github.com/AndyTheFactory/gcp-pmle-quiz) — the full audit this page summarizes
- [Google Skills ML Engineer learning path](https://www.skills.google/paths/17) — every Skills Boost item with rating + sequencing
- [Andrei Paraschiv's PMLE pass writeup (Feb 2026)](https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4) — 10 post-v3.1 passer writeups
- [BigQuery ML introduction](https://docs.cloud.google.com/bigquery/docs/bqml-introduction) — §1.1 BQML vs AutoML vs custom
- [Vertex AI training compute config](https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute) — §3.3 GPU/TPU/Reduction Server
- [Vertex AI Pipelines introduction](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction) — §5 orchestrator picks
- [Vertex AI Feature Store overview](https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview) — §2 / §4.2 Feature Store (sunset Feb 2027)
- [Vertex AI predictions overview](https://docs.cloud.google.com/vertex-ai/docs/predictions/overview) — §4 online vs batch vs Dataflow vs BQML
- [Vertex AI Model Monitoring overview](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview) — §6 the one-liner to memorize
- [Google AI Principles](https://ai.google/principles/) — §6.1 (Explainable AI deprecated Mar 2026)
- [IAM overview](https://docs.cloud.google.com/iam/docs/overview) — cross-cutting IAM / VPC-SC / private endpoints
- [Vertex AI hyperparameter tuning overview](https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview) — §3.2 Vizier
- [Vertex AI Experiments intro](https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments) — §5.3 Experiments + ML Metadata
- [Gemini Enterprise Agent Platform](https://cloud.google.com/products/agent-builder) — full v3.1 GenAI map + rebrand history (12+ renames)
"""
    )


if __name__ == "__main__":
    main()
