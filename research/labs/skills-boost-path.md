# Google Skills (formerly Cloud Skills Boost) - Professional ML Engineer Learning Path Inventory

**Audience:** Two beginners with no prior GCP/ML experience, math-strong, 10-12 week timeline, preparing for PMLE v3.1 (April 2025+, includes generative AI content).
**Compiled:** 2026-04-24

---

## 1. Path Overview

The official preparation track for the Google Cloud **Professional Machine Learning Engineer** certification lives at path `/paths/17`. The original URL `https://www.cloudskillsboost.google/paths/17` now permanently 308-redirects to `https://www.skills.google/paths/17` — Google rebranded the platform from "Google Cloud Skills Boost" to "Google Skills" in **October 2025** and migrated the domain from `cloudskillsboost.google` to `skills.google` (the old domain still redirects, so old URLs continue to resolve). [1][2][3] The path is "Managed by Google Cloud", contains **20 activities** (a mix of on-demand video courses, hands-on labs, and skill badges), and was last refreshed approximately 1 month before the access date (so ~late March 2026). [1] A site-wide banner reads: *"Vertex AI is now Gemini Enterprise Agent Platform! We are currently updating our content to reflect this change."* — meaning some module names and screenshots still say "Vertex AI" while Google renames product surfaces. [1] Summing the per-course durations from the live course pages gives a **total nominal duration of roughly 50-55 hours** (the GitHub mirror's older figures totalled ~127 h, but live pages now show shorter "estimated time to complete" numbers for the post-2025 refreshes — the path has been compressed and de-duplicated). [4] **Pricing as of April 2026:** Starter $0/mo (35 free monthly credits, limited labs), Pro **$29/mo**, Career Certificates **$49/mo or $349/yr**; a **7-day free trial** is offered to new subscribers; no path-specific promotion was advertised at access time. [5][6]

---

## 2. Full Inventory

URLs use the canonical `skills.google` domain (the legacy `cloudskillsboost.google` ones still redirect 1:1). All durations are taken from the live course pages where reachable; fallback values from a public mirror of the path are flagged with `(M)`. [4] Skill points are not displayed publicly on the new Google Skills UI for any of the items in this path (the platform now surfaces "credits" and "badges" rather than skill points) — flagged "n/p" (not published). [1][7] Type column: C = Course (video + reading), SB = Skill Badge (course + hands-on challenge lab assessment), L = standalone Lab. Many items in the path are *both* a course and a skill-badge gateway — in those cases I list the more useful framing for a beginner.

| # | Name | Type | Direct URL | Duration | Skill Points | Exam §s most addressed | Rating | Justification |
|---|------|------|------------|----------|--------------|------------------------|--------|---------------|
| 1 | Introduction to AI and Machine Learning on Google Cloud | C | https://www.skills.google/course_templates/593 | 4 h [8] | n/p | §1 (13%), §2 (14%), survey of all | **Must** | Single best on-ramp to GCP's AI portfolio for true beginners — covers Vertex AI, BigQuery ML, Model Garden, AutoML, Gemini in one sitting. |
| 2 | Prepare Data for ML APIs on Google Cloud | SB | https://www.skills.google/course_templates/631 | 0.75 h [9] | n/p | §1 (13%), §2 (14%) | **Must** | Skill-badge challenge lab that forces hands-on Dataprep/Dataflow/ML APIs — the cheapest way to internalise §1.2 ML APIs sub-domain. |
| 3 | Working with Notebooks in Vertex AI | C | https://www.skills.google/course_templates/923 | 4.5 h [10] | n/p | §2 (14%) | **Must** | §2.2 "Model prototyping using Jupyter notebooks" is an exam-guide bullet — Workbench/Colab Enterprise mechanics matter. |
| 4 | Create ML Models with BigQuery ML | SB | https://www.skills.google/course_templates/626 | 0.5 h [11] | n/p | §1 (13%) | **Must** | §1.1 is *entirely* BQML; the challenge lab is the fastest way to get the SQL pattern (`CREATE MODEL` / `ML.PREDICT`) into muscle memory. |
| 5 | Engineer Data for Predictive Modeling with BigQuery ML | SB | https://www.skills.google/course_templates/627 | 0.5 h [12] | n/p | §1 (13%), §2 (14%) | **Should** | Reinforces §1.1 + §2.1 (Dataflow/BQ ETL); skip if comfortable after #4. |
| 6 | Feature Engineering | C | https://www.skills.google/course_templates/11 | 7.25 h [13] | n/p | §2 (14%), §3 (18%) | **Must** | Vertex AI Feature Store appears explicitly in §2.1 and §2.2 — this is the only deep treatment in the path. |
| 7 | Build, Train and Deploy ML Models with Keras on Google Cloud | C | https://www.skills.google/course_templates/12 | 10.75 h [14] | n/p | §3 (18%), §4 (20%) | **Must** | TensorFlow/Keras custom training + Vertex AI deployment hits §3.1, §3.2, §4.1 all at once. Longest course in the path; carries the most weight. |
| 8 | Production Machine Learning Systems | C | https://www.skills.google/course_templates/17 | 11 h [15] | n/p | §3 (18%), §4 (20%), §5 (22%) | **Must** | Static vs dynamic training/inference, batch vs online — these distinctions appear verbatim in exam questions. Last updated ~Feb 2026. |
| 9 | Machine Learning Operations (MLOps): Getting Started | C | https://www.skills.google/course_templates/158 | 0.75 h [16] | n/p | §5 (22%), §6 (13%) | **Must** | Sets vocabulary (CT/CI/CD, drift, serving signature) used across §5 and §6. Very short, very high ROI. |
| 10 | MLOps with Vertex AI: Manage Features | C | https://www.skills.google/course_templates/584 | 1.75 h [17] | n/p | §2 (14%), §5 (22%) | **Should** | Streaming ingestion to Feature Store is niche but explicitly enumerated in the exam guide §2.1. |
| 11 | Introduction to Generative AI | C | https://www.skills.google/course_templates/536 | 0.5 h [18] | n/p | §1.2, §2.3, §3.2 (gen-AI bullets across the guide) | **Must** | The v3.1 update explicitly added "tasks related to generative AI" — this is the cheapest unit to satisfy that. |
| 12 | Introduction to Large Language Models | C | https://www.skills.google/course_templates/539 | 0.25 h [19] | n/p | §1.2, §3.2 | **Should** | 10-minute survey; useful only if the learner has zero LLM exposure. |
| 13 | Machine Learning Operations (MLOps) for Generative AI | C | https://www.skills.google/course_templates/927 | 0.5 h [20] | n/p | §5 (22%), §6 (13%) | **Must** | Gen-AI MLOps (prompt versioning, eval harness, RAG monitoring) is a v3.1 net-new topic that older study guides miss. |
| 14 | MLOps with Vertex AI: Model Evaluation | C | https://www.skills.google/course_templates/1080 | 1 h [21] | n/p | §2.3, §5 (22%), §6 (13%) | **Must** | "Evaluating generative AI solutions" is called out in the v3.1 cover paragraph and §2.3 — this course is the only resource that targets it specifically. |
| 15 | ML Pipelines on Google Cloud | C | https://www.skills.google/course_templates/191 | 2.25 h (M) [4] | n/p | §5 (22%) | **Must** | Vertex AI Pipelines / Kubeflow / TFX = ~half of §5 weight; cannot be skipped. |
| 16 | Build and Deploy Machine Learning Solutions on Vertex AI | SB | https://www.skills.google/course_templates/684 | 8.25 h (M) [4] | n/p | §3 (18%), §4 (20%) | **Must** | Capstone-style skill badge — AutoML + custom training + endpoint deployment in one challenge lab. Highest §3+§4 yield per hour. |
| 17 | Create Generative AI Apps on Google Cloud | SB | https://www.skills.google/course_templates/1120 | 4.75 h [22] | n/p | §1.2, §3.2, §4.1 | **Must** | RAG with Vertex AI Agent Builder is named in §1.2 of the v3.1 guide — this badge is the only hands-on path resource that builds it. |
| 18 | Responsible AI for Developers: Fairness and Bias | C | https://www.skills.google/course_templates/985 | 2.25 h [23] | n/p | §6 (13%), cross-cutting | **Should** | Responsible-AI questions are 1-2 on the exam; do this *if time allows*. |
| 19 | Responsible AI for Developers: Interpretability and Transparency | C | https://www.skills.google/course_templates/989 | 2 h [24] | n/p | §3.1, §6 (13%) | **Should** | §3.1 lists "modeling techniques given interpretability requirements" — Vertex Explainable AI is the answer key. |
| 20 | Responsible AI for Developers: Privacy and Safety | C | https://www.skills.google/course_templates/1036 | 3.75 h [25] | n/p | §2.1, §6 (13%) | **Skip** (for 12-week beginner plan) | Long, mostly conceptual, low question-yield; revisit only if the duo has slack in week 12. |

**Totals (Must items only):** 14 items, ~58 hours of nominal Skills-Boost time. **All 20 items**, taking only the live numbers above, sums to ~67 hours; budget 1.5x for the lab queue waits and re-tries -> **~100 hours wall-clock** is a realistic estimate for two beginners.

---

## 3. Recommended 12-Week Sequencing

Designed to interleave concept courses with hands-on skill badges so the lab credits keep getting consumed (and so a stalled lab never blocks an entire week). Numbers in `[]` = item index from the table above.

| Week | Items | Hours | Theme |
|------|-------|-------|-------|
| 1 | [1] Intro to AI & ML on GCP; **read the v3.1 exam guide PDF** | ~5 | Orientation. Sign up *before* week 1, burn the 7-day trial here. |
| 2 | [4] BQML skill badge; [5] BQML data engineering badge | ~1 + reading | §1 Architecting low-code AI (13%) — 2 quick wins to bank momentum. |
| 3 | [2] Prepare Data for ML APIs SB; [3] Working with Notebooks in Vertex AI | ~5.25 | §1.2 + §2.2 (notebook backends). |
| 4 | [6] Feature Engineering | ~7.25 | §2 + §3 backbone — split across 5 sessions. |
| 5 | [7] Build, Train, Deploy ML Models with Keras on GCP — first half | ~5.5 | TensorFlow primer; pair-program the labs. |
| 6 | [7] Keras course — finish; [10] MLOps Manage Features | ~7 | §3 + §4 entry. |
| 7 | [8] Production ML Systems | ~11 | §3/§4/§5 powerhouse. Pace 2 hours/day. |
| 8 | [15] ML Pipelines on Google Cloud; [9] MLOps Getting Started | ~3 | §5 (22%) — biggest single section, intro layer. |
| 9 | [16] Build and Deploy ML Solutions on Vertex AI (skill badge) | ~8.25 | Capstone hands-on — practice the *exam scenarios* in real consoles. |
| 10 | [11] Intro to Gen AI; [12] Intro to LLMs; [13] MLOps for Gen AI; [14] Model Evaluation | ~2.25 | v3.1 generative-AI sweep — short courses, dense net-new content. |
| 11 | [17] Create Generative AI Apps on GCP (skill badge) | ~4.75 | RAG + Agent Builder hands-on. |
| 12 | [18] Fairness & Bias; [19] Interpretability; **two full-length practice exams**; targeted re-watch on weak §s | ~4 + practice | Final consolidation; **[20] Privacy & Safety only if time permits**. |

A 10-week version drops items 5, 12, 18, 19 and combines weeks 10+11.

---

## 4. Free / Trial-Friendly Content (Do FIRST While the Subscription Clock Isn't Running)

Every Google account starts at the **Starter (free) tier** which grants **35 free credits per month** and access to selected free labs/skill badges. [5] Burn these *before* you subscribe:

1. **Read the v3.1 exam guide PDF** — free, official, definitive. (Already on disk: `professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf`.)
2. **Item [11] Introduction to Generative AI** — free 30-min course, no subscription needed for the video portion. [18]
3. **Item [12] Introduction to Large Language Models** — free 10-min course. [19]
4. **Item [9] MLOps: Getting Started** — short course, often inside the free tier window. [16]
5. **Sign up via the Google Cloud Innovators community** — confers an extra **35 unrestricted learning credits per month** in addition to the Starter allotment, which fully covers the early skill-badge labs (#2, #4, #5). [7]
6. **Sample exam form** (Google Forms, free, ungraded) — https://docs.google.com/forms/d/e/1FAIpQLSeYmkCANE81qSBqLW0g2X7RoskBX9yGYQu-m1TtsjMvHabGqg/viewform — take it cold *before* the first paid week. [3]
7. **Time the 7-day Pro trial** so it starts on the morning of Week 1 of the heavy-lab phase (Week 4 in my plan above), not Week 1 — that way the trial covers Feature Engineering and the Keras course where lab consumption peaks. [5]
8. **Always-free public talks**: Cloud OnAir certification webinars are public; [3] the recorded sessions explain exam intent without using a credit.

**Gotchas:** the 7-day trial auto-converts to paid; cancel from `skills.google/payments` *before* day 7 if you want to pause. Free credits do **not** roll over month to month. Some "free" courses still gate their labs behind a subscription — only the *video* portions are free.

---

## 5. Estimated Total Time and Cost (Must-Do Items Only)

**Must items:** #1, 2, 3, 4, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17 (14 items).
**Sum of nominal durations:** ~58 study hours.
**Realistic wall-clock for two beginners (1.5x multiplier for lab queue waits, retries, and re-watches):** **~85-90 hours.**

**Cost paths (per learner, USD):**

- **Cheapest viable** — 1 month Pro at **$29** [5] + use free Starter credits + Innovators credits for the rest. Risk: rushed timeline.
- **Recommended for 12 weeks** — 3 months Pro at **$29 x 3 = $87** [5] (start subscription Week 4, end after Week 12). This is the option to budget for.
- **All-in/safest** — Annual Career Certificates at **$349/yr** [5] = unlimited labs + advanced content for 12 months. Worth it only if both learners share one account *or* if either one plans to chase another GCP cert in the same year.
- **Free / promotional path** — Stack Innovators (35 credits/mo) + GEAR program (35 credits/mo) [7] = 70 credits/mo per learner; *most* labs cost 1-7 credits, so this can cover ~50-70% of the path with patience. Plan an extra 2-3 weeks if going this route.

**Exam fee:** $200 (separate from Skills Boost; voucher sometimes offered with annual sub). [3] **Total project budget for two learners on the recommended plan:** $87 x 2 + $200 x 2 = **$574** plus optional retake buffer.

---

## 6. Dated / Outdated Content (Pre-v3.1 Risk)

The v3.1 exam guide (April 2025) [26] adds explicit generative-AI bullets (§1.2 ML APIs *and Model Garden*, §2.3 *evaluating generative AI solutions*, §3.2 *fine-tuning foundational models*). Items in the path that **predate that update** and are therefore at risk of being misaligned:

- **#6 Feature Engineering — last updated ~9 months ago** (per the live course page) [13] — content references TF 2.x patterns that still pass exam questions, but the Vertex AI Feature Store UI has been renamed in the Gemini Enterprise Agent Platform rebrand. **Flag, don't skip** — the *concepts* are still correct, just expect UI mismatch in the labs.
- **#10 MLOps with Vertex AI: Manage Features — last updated ~9 months ago** [17] — same UI-rebrand risk.
- **#19 Responsible AI: Interpretability — last updated ~8 months ago** [24] and **#20 Privacy & Safety — last updated ~8 months ago** [25] — pre-Gemini-Enterprise content; conceptual material is fine but the demo screenshots are dated.
- **#15 ML Pipelines on Google Cloud** — content still teaches TFX heavily; the v3.1 guide *also* references Kubeflow Pipelines and Vertex AI Pipelines (the modern Google-recommended option). Use the course for orchestration concepts but supplement with current Vertex AI Pipelines docs.
- The site-wide banner *"Vertex AI is now Gemini Enterprise Agent Platform! We are currently updating our content to reflect this change"* applies across the path. [1] On the exam, both names may appear; the underlying APIs are unchanged as of v3.1.

Items that are **explicitly post-v3.1** (low decay risk): #1 (refreshed within 3 months), #8 (refreshed ~Feb 2026), #11, #13, #14, #17. These are the safest to trust verbatim.

**Not in the path but worth knowing:** the v3.1 exam guide cover page also points readers to **Generative AI for Developers Learning Path** (`/journeys/183`), **Explore and Evaluate Models using Model Garden** (`/focuses/71938`), and **Integrate Search in Applications using Vertex AI Agent Builder** (`/focuses/71943`) [26] — none of these are inside path 17, but at least one Model Garden lab is essentially mandatory for §1.2 mastery.

---

## 7. References

All accessed 2026-04-24 unless otherwise noted.

1. Google Skills, *Professional Machine Learning Engineer Certification* — https://www.skills.google/paths/17 (path 17, "20 activities", "Last updated about 1 month ago", banner about Gemini Enterprise Agent Platform).
2. Google blog, *Start learning all things AI on the new Google Skills* — https://blog.google/products-and-platforms/products/education/google-skills/ (rebrand announcement, October 2025).
3. Google Cloud, *Professional ML Engineer Certification* — https://cloud.google.com/learn/certification/machine-learning-engineer (cert overview, links to v3.1 exam guide PDF, sample questions form, Cloud OnAir webinars).
4. GitHub mirror, *gperdrizet/GCSB_MLE* — https://github.com/gperdrizet/GCSB_MLE (community-maintained snapshot of the path's 20 items with course_template IDs and durations; used as fallback where live page rendered only the homepage).
5. Google Skills, *Purchase A Subscription* — https://www.skills.google/payments/new (Starter free with 35 monthly credits; Pro $29/mo; Career Certificates $49/mo or $349/yr; 7-day trial for new subscribers).
6. Google Cloud blog, *Discover the Google Cloud Skills Boost annual subscription benefits* — https://cloud.google.com/blog/topics/training-certifications/discover-the-google-cloud-skills-boost-annual-subscription-benefits.
7. Google Cloud, *Innovators / GEAR program credits* — referenced via https://cloud.google.com/innovators and https://www.skills.google/ ("35 monthly credits for hands-on learning"). Cross-confirmed by Google Developer forums announcement at https://discuss.google.dev/t/just-announced-google-skills-your-new-destination-for-ai-learning-and-more/272259.
8. Google Skills, *Introduction to AI and Machine Learning on Google Cloud* — https://www.skills.google/course_templates/593 (4 hours, introductory, updated within ~3 months).
9. Google Skills, *Prepare Data for ML APIs on Google Cloud* — https://www.skills.google/course_templates/631 (45 minutes, skill badge).
10. Google Skills, *Working with Notebooks in Vertex AI* — https://www.skills.google/course_templates/923 (4.5 hours, introductory).
11. Google Skills, *Create ML Models with BigQuery ML* — https://www.skills.google/course_templates/626 (30 minutes, skill badge, last updated ~4 months ago).
12. Google Skills, *Engineer Data for Predictive Modeling with BigQuery ML* — https://www.skills.google/course_templates/627 (30 minutes, skill badge).
13. Google Skills, *Feature Engineering* — https://www.skills.google/course_templates/11 (7 h 15 min, last updated ~9 months ago).
14. Google Skills, *Build, Train and Deploy ML Models with Keras on Google Cloud* — https://www.skills.google/course_templates/12 (10 h 45 min).
15. Google Skills, *Production Machine Learning Systems* — https://www.skills.google/course_templates/17 (11 hours, updated ~2 months ago).
16. Google Skills, *MLOps: Getting Started* — https://www.skills.google/course_templates/158 (45 minutes, updated ~30 days ago).
17. Google Skills, *MLOps with Vertex AI: Manage Features* — https://www.skills.google/course_templates/584 (1 h 45 min, ~9 months ago).
18. Google Skills, *Introduction to Generative AI* — https://www.skills.google/course_templates/536 (30 min, ~2 months ago).
19. Google Skills, *Introduction to Large Language Models* — https://www.skills.google/course_templates/539 (10 min).
20. Google Skills, *MLOps for Generative AI* — https://www.skills.google/course_templates/927 (~30 min, intermediate).
21. Google Skills, *MLOps with Vertex AI: Model Evaluation* — https://www.skills.google/course_templates/1080 (1 hour, intermediate).
22. Google Skills, *Create Generative AI Apps on Google Cloud* — https://www.skills.google/course_templates/1120 (4 h 45 min).
23. Google Skills, *Responsible AI: Fairness and Bias* — https://www.skills.google/course_templates/985 (2 h 15 min).
24. Google Skills, *Responsible AI: Interpretability and Transparency* — https://www.skills.google/course_templates/989 (2 hours, ~8 months ago).
25. Google Skills, *Responsible AI: Privacy and Safety* — https://www.skills.google/course_templates/1036 (3 h 45 min, ~8 months ago).
26. Google Cloud, *Professional Machine Learning Engineer Exam Guide v3.1 (English, final)* — https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf (also available locally; six sections: §1 Architecting low-code AI 13%, §2 Collaborating data+models ~14%, §3 Scaling prototypes ~18%, §4 Serving and scaling ~20%, §5 Pipelines + automation ~22%, §6 Monitoring ~13%).
27. Google Skills Help, *Purchase and manage a subscription* — https://support.google.com/qwiklabs/answer/9139481 (subscription mechanics, cancellation; note help domain still uses `qwiklabs` path — Qwiklabs has been merged into Skills Boost / Google Skills since 2019, with the merger fully completed at the rebrand in October 2025).

---

### Confidence

- **High confidence (cross-confirmed by ≥2 sources):** The list of 20 items and their template IDs [1][4]; current pricing tiers and the 7-day trial [5][6]; rebrand to Google Skills in October 2025 [2]; v3.1 exam-section weights [26].
- **Medium confidence (single live-page source, may drift):** Exact per-course durations — Google rounds these and they have changed before. Most are within ±15 minutes of what's on the live page right now. The "last updated" relative timestamps on each course page are approximate.
- **Lower confidence:** Skill points per course — the new Google Skills UI does not surface them publicly; the figures were visible on the legacy `cloudskillsboost.google` UI but are now hidden. I marked these "n/p". My **Must / Should / Skip** ratings are judgment calls; another reviewer optimising for §6 monitoring weight might promote #18-19 to Must.

### Decay risk

- **High decay (re-check before kickoff):** The path's contents — Google rotated/renumbered ~3 items between 2023 and 2025 [4]. Re-fetch `https://www.skills.google/paths/17` on Day 1 and diff against this table.
- **High decay:** Pricing and free-trial length — both have changed twice since 2023. Re-confirm at https://www.skills.google/payments/new before subscribing.
- **High decay:** Vertex AI -> Gemini Enterprise Agent Platform rename is rolling through course UIs; expect more screenshot mismatches over the 12-week window.
- **Medium decay:** Exam guide v3.1 has been stable since April 2025; a v3.2 has not been announced as of access date but Google typically refreshes the PMLE every 18-24 months — monitor for an announcement around mid-2026.
- **Low decay:** Section weights, course template IDs (Google does not recycle these even when content is rewritten — IDs persist across rewrites, so a URL that works today will still work).
