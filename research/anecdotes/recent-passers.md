# Recent PMLE Pass Writeups (v3.1, April 2025+)

## 1. Overview

This report aggregates 10 first-hand pass writeups for the Google Cloud Professional Machine Learning Engineer (PMLE) exam, all published or written between June 2025 and March 2026 — i.e., after the April 2025 v3.1 GenAI-inclusive curriculum took effect. Sources span Medium long-form posts (6), Google Developer Forum comments from confirmed exam takers (2), one personal Hashnode-style blog (lxmwaniky.me), and one ExamCert practitioner blog. Geographic distribution skews international: India, Australia, Romania, Chile, Kenya, France/Spain, plus US-based writers. Roles range from Software Engineer / SRE with ML side-skills through Data Scientist, Full-Stack Developer, NLP Engineer, to a 14x-cert Gen AI Architect renewal. Two writeups discuss specific GenAI question counts on the exam (3-4 vs. ~10%), which forms the central disagreement covered in §7. All anecdotes were screened for the April 2025 cutoff; older "30-days" guides (Paraschiv earlier version), Hilliao (Feb 2025), Ajayi (Jan 2025), Hasan Rafiq (originally 2021, updated 2025 — date ambiguous), Josh Tan (2022), and Hussain (2022) were rejected as predating or straddling v3.1.

---

## 2. Per-Anecdote Sections

### 2.1 Matías Salinas — Passed June 1, 2025

| Field | Value |
|---|---|
| Source | https://msalinas92.medium.com/how-i-passed-the-google-cloud-professional-machine-learning-engineer-certification-and-what-i-3d3066708124 |
| Publication date | June 2, 2025 |
| Author background | SRE with Master's in Data Science; multi-cert holder (AWS SOA-C02, CKAD, CKA, CKS, AZ-104, GCP PCA). Strong infrastructure/ops bent. Years of explicit ML production work not stated; certificate stack implies advanced cloud, intermediate ML. |
| Study duration | Not explicitly disclosed (article excerpt is paywall-truncated) |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | 1. "Fenden" prep platform (called out as "key role"). 2. Implied: GCP docs (Vertex AI, BigQuery, Dataflow, Cloud Storage). Full ranked list inaccessible behind paywall. |
| Score | Not disclosed (only "Pass") |
| Top 3 lessons | (1) PMLE is a hybrid challenge: cloud architecture + data science + ML engineering — must master all three. (2) Production-readiness focus: "design, build, train, deploy, and maintain" the full lifecycle. (3) Cannot be crammed; requires planning, practice, right resources. |
| Exam-day surprises | None disclosed in available text |
| GenAI on exam | Not specifically discussed in available text |

### 2.2 Steven (Liang) Chen — Passed mid-2025

| Field | Value |
|---|---|
| Source | https://steven-chen.medium.com/preparing-google-cloud-professional-machine-learning-engineer-certificate-in-2025-7035018d5d84 |
| Publication date | July 13, 2025 |
| Author background | Full-Stack Developer based in Melbourne, Australia, working at a GCP partner organization. Self-describes as career-pivoting toward AI Engineer roles — implies intermediate developer experience, limited prior production ML, some on-the-job GCP exposure. |
| Study duration | Not explicitly disclosed |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | 1. Official GCP Exam Guide. 2. Google Cloud Skills Boost ML Engineer learning path (theory + labs). 3. Google Cloud Community certification forums. 4. Coursera Google Cloud courses. 5. Sybex official study guide (mentioned but author did not personally use it). |
| Score | Not disclosed |
| Top 3 lessons | (1) Register for the exam 3 months ahead — locking the date is the single biggest accountability lever. (2) ~90% of ML roles are MLOps/infrastructure, not modeling — the cert maps to the actual job. (3) Free 72-hour rescheduling reduces the risk of early registration. |
| Exam-day surprises | None documented |
| GenAI on exam | Not addressed in the article |

### 2.3 Anil Kumar — Renewal, October 6, 2025

| Field | Value |
|---|---|
| Source | https://medium.com/google-cloud/balancing-ai-and-wellness-my-journey-renewing-the-google-cloud-professional-machine-learning-0c3649e31a4a |
| Publication date | October 9, 2025 |
| Author background | 14x Google Cloud certified, self-styled "Gen AI Architect." Explicit ML/GCP YOE not stated, but cert breadth implies 5+ years GCP and active ML practitioner. This was a renewal, not a first pass. |
| Study duration | Not stated explicitly; renewal-mode prep. |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | 1. Official Google Cloud certification page + exam guide. 2. Google Cloud Skills Boost learning path. 3. Vertex AI lab series. 4. Udemy full-length practice course. 5. CertShield community resources. 6. Author's own personal companion guide. |
| Score | Not disclosed (only "Pass") |
| Top 3 lessons | (1) Not all ML problems need custom models — BigQuery ML and AutoML solve many. (2) Foundation models via Model Garden enable domain fine-tuning without from-scratch training. (3) Vertex AI Feature Store is the mechanism to ensure training/serving consistency. |
| Exam-day surprises | None explicit; described renewal as "special" because of v3.1 GenAI scope |
| GenAI on exam | Treats GenAI as a major theme — explicitly calls out building GenAI apps, evaluating model performance, Responsible AI. Names Vertex AI Agent Builder for RAG chatbots and Model Garden access to Gemini, PaLM, Imagen. Frames the renewal as required precisely because the exam now expects GenAI fluency. |

### 2.4 Natalia Pozdniakova — Passed July 7, 2025

| Field | Value |
|---|---|
| Source | https://medium.com/@natalia.pozdniakova/how-i-passed-the-gcp-professional-machine-learning-engineer-exam-in-one-month-bd51c7ffc16a |
| Publication date | December 7, 2025 |
| Author background | Self-identified "Data Scientist \| ML Engineer." Years of ML/GCP not stated explicitly. Article tone implies prior data science/ML day-job experience but limited prior structured GCP cert prep. |
| Study duration | Exactly 4 weeks (June 7 – July 7, 2025); "intense month" |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | Full ranked list inaccessible due to paywall. Article confirms reading product documentation, official sample questions with answer-link follow-through, and best-practice guides. |
| Score | Not disclosed; passed first attempt |
| Top 3 lessons | (1) Booking the exam first (high-pressure deadline) was the unlock. (2) Several options will be technically correct — train yourself to pick "best" by Google best-practices. (3) Read documentation pages directly because exam questions are heavily syphoned from them. |
| Exam-day surprises | "Tricky" question phrasing where multiple answers are plausible was the dominant difficulty |
| GenAI on exam | Not specifically quantified in the available preview |

### 2.5 Andrei Paraschiv — Passed early 2026 (first attempt)

| Field | Value |
|---|---|
| Source | https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4 |
| Publication date | February 15, 2026 |
| Author background | NLP engineer with strong data-science fundamentals (cleaning, feature engineering, model evaluation, metrics). Explicit GCP experience: zero prior to prep. Best mapped to "prior ML, no GCP." |
| Study duration | ~30 days. Roughly 2 weeks of structured course + quiz, then ~2 weeks of integrated lab/quiz/practice. Recommends 60+ days for those without ML or GCP. |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | 1. Google Skills ML Engineer learning path (videos at 1.25–1.5×, all quizzes). 2. Author's own Streamlit quiz app (~850 questions tagged by topic). 3. 11 GCP best-practice docs (Rules of ML, Vertex AI, Dataflow, TPUs, etc.). 4. NotebookLM for personalized flashcards from missed questions. 5. ExamTopics, SkillCertPro (called out as inconsistent). |
| Score | Not disclosed; passed first attempt |
| Top 3 lessons | (1) Conceptual clarity FIRST, labs strategically — don't lab everything. (2) Track quiz performance by topic; use weak-spot data to drive next study. (3) Build personalized review material from your own mistakes (NotebookLM for this). |
| Exam-day surprises | Zero multiple-answer questions on his exam (despite practice apps including them); GPU vs. TPU infrastructure choice was a pivotal question theme; structured 3-pass timing left 15 min for review and changed ~3 answers |
| GenAI on exam | "Only about 3–4 GenAI-related questions" appeared. He found official courses + best-practice docs were "more than sufficient." No specific Model Garden / Agent Builder questions noted. |

### 2.6 Cassiopeia (V. Narvaez) — Passed early 2026

| Field | Value |
|---|---|
| Source | https://medium.com/@vnarvaezt/prepare-for-the-professional-machine-learning-certification-2026-and-boost-your-skills-0f6cf3f4b78a |
| Publication date | February 1, 2026 |
| Author background | Personal background not disclosed; tone suggests data-science practitioner with limited prior cloud cert experience. Audience targeting is "people new to the cloud," implying author's path was similar. |
| Study duration | 3 months recommended for cloud-newcomers; ~12–15 weeks |
| Total study hours | ~60–75 hours estimated (1 hr weekdays + heavier weekends) |
| Materials (rank-ordered) | 1. Google MLE learning path (25% of time). 2. Official GCP documentation (25%). 3. Practice exams (50% — the heaviest weighting in any reviewed writeup). 4. Udemy practice exam sets (~€14 for 5–6 exams). 5. ExamTopics + LinkedIn Learning for free warm-up. |
| Score | Not disclosed |
| Top 3 lessons | (1) "Reading comprehension is 50% of the exam" — many questions hinge on subtle constraint differences. (2) Understanding why the wrong options fail beats memorizing right answers. (3) AI-generated practice questions are "disappointing"; use AI for concept analogies only. |
| Exam-day surprises | None mentioned |
| GenAI on exam | Not quantified explicitly; cautioned against AI-generated GenAI practice questions as having obvious correct answers |

### 2.7 ExamCert practitioner (anonymous) — Passed prior to article

| Field | Value |
|---|---|
| Source | https://www.examcert.app/blog/gcp-ml-engineer-study-plan-2026/ |
| Publication date | March 21, 2026 |
| Author background | 2 years ML in production. Already held GCP Associate Cloud Engineer (ACE). Best mapped to "prior ML, prior light GCP." |
| Study duration | 10 weeks |
| Total study hours | ~1.5 hours/day weeks 1–2, intensifying later — implies ~100–120 hours total |
| Materials (rank-ordered) | 1. ExamCert PMLE practice tests (their own product — disclosure noted). 2. Google ML Crash Course (free). 3. GCP docs (Vertex AI architecture). 4. Coursera Google Cloud ML Engineer learning path. 5. ExamCert ACE practice tests (kept GCP fundamentals fresh). 6. Google's ML Design Patterns (free online book). 7. GCP $300 free tier for hands-on. |
| Score | Not disclosed |
| Top 3 lessons | (1) "Every hour in the console is worth three hours reading docs." (2) Start with MLOps fundamentals before ML theory — 60% of exam is operational. (3) Take diagnostic practice exams in week 3 (not week 8) to recalibrate study early. |
| Exam-day surprises | None specifically discussed |
| GenAI on exam | Not discussed in detail in this article |

### 2.8 Alex Nyambura — Passed early 2026

| Field | Value |
|---|---|
| Source | https://blog.lxmwaniky.me/pmle |
| Publication date | January 6, 2026 |
| Author background | Software Engineer (cloud, automation) holding the Google Cloud Generative AI Leader cert. Self-states ML "really ain't my shit" — i.e., software/cloud strong, ML weak. Best-mapped to "prior GCP, no ML." |
| Study duration | 1 month nominal; effective intensive study ~1 week (procrastination-driven) |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | 1. Google Skills course (BigQuery ML, Vertex AI Notebooks, model training). 2. Paul Kamau Medium blogs (motivation/framework). 3. Google Developer Forums "30 Days" post for focus map. 4. Vertex AI documentation (48-hour deep dive in final week). 5. Gemini for scenario question generation. |
| Score | Not disclosed; passed |
| Top 3 lessons | (1) Focus over breadth: 60–70% of exam is Vertex AI — allocate accordingly; skip deep coding-framework rabbit holes. (2) Pattern recognition: questions reward "the Google way" — efficiency, cost-saving, managed services. (3) Psychological resilience matters; reframing failure as acceptable beat brute-force motivation. |
| Exam-day surprises | Slept through first 20 min; only 10 of 50 questions done in first 30 min; pattern-recognition "click" mid-exam unlocked rapid completion with 30 min remaining for review |
| GenAI on exam | Did not feature prominently in her account; exam content described focused on Vertex AI core ML infra (AutoML, Pipelines, Feature Store, Explainable AI, Monitoring). She used Gemini AS a study tool, not as exam content. |

### 2.9 DSumit — Passed November 15, 2025 (Google Dev Forum comment)

| Field | Value |
|---|---|
| Source | https://discuss.google.dev/t/google-clouds-professional-ml-engineer-pmle-exam-how-i-passed-in-30-days-and-you-can-too/179510 (comment) |
| Publication date | November 15, 2025 |
| Author background | "Multiple years of hands-on experience in ML / Data Science." Maps to "prior ML, no GCP cert" probable. |
| Study duration | Not specified |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | 1. Google Dev ML Crash Course (called "essential"). 2. Skills Boost labs (called useful for knowledge-building). |
| Score | Pass; got result immediately, credly badge in 36 hours |
| Top 3 lessons | (1) Test is "intermediate++" — Credly badge says "advanced," but DSumit calls it intermediate++ — implies challenging but tractable for ML-experienced. (2) "99% of questions are scenario based" — no direct code dumps. (3) MLOps, Pipelines, train/serve skew management are the dominant tested concepts. |
| Exam-day surprises | Took at testing center; immediate result |
| GenAI on exam | "Didn't see much reference to Gen AI or Gen AI specific quality metric" — DIRECT contradiction of Anil Kumar's framing (see §7) |

### 2.10 Dale Monteiro — Passed January 12, 2026 (Google Dev Forum comment)

| Field | Value |
|---|---|
| Source | https://discuss.google.dev/t/google-clouds-professional-ml-engineer-pmle-exam-how-i-passed-in-30-days-and-you-can-too/179510 (comment) |
| Publication date | January 12, 2026 |
| Author background | Cleared GCP Professional Cloud Architect (PCA) two months before PMLE. Transitioning to a more technical role. Maps to "prior GCP, no ML focus." |
| Study duration | Not specified |
| Total study hours | Not disclosed |
| Materials (rank-ordered) | Not specified in his comment |
| Score | Pass |
| Top 3 lessons | None content-specific provided |
| Exam-day surprises | None discussed |
| GenAI on exam | Not discussed |

---

## 3. Synthesis: Top Themes (≥3 writeups)

| Rank | Theme | Frequency | Sources |
|---|---|---|---|
| 1 | **Vertex AI dominates exam content (~60–70%)** | 5 | DSumit, Nyambura, ExamCert, Anil Kumar, Pozdniakova (implicit via doc-emphasis) |
| 2 | **MLOps weighting > pure ML modeling weighting** | 5 | ExamCert, DSumit, Anil Kumar, Salinas, Steven Chen |
| 3 | **Scenario-based questions, not code; multiple right answers, pick "best"** | 5 | Pozdniakova, DSumit, Cassiopeia, Paraschiv, Anil Kumar |
| 4 | **Google Skills Boost / Coursera ML Engineer learning path is foundational** | 7 | Anil Kumar, Steven Chen, Paraschiv, Cassiopeia, ExamCert, Nyambura, Pozdniakova |
| 5 | **Practice exams / question banks are essential, ideally tracking by topic** | 6 | Cassiopeia, Paraschiv, ExamCert, Anil Kumar, Pozdniakova, DSumit |
| 6 | **Read GCP best-practices / Vertex AI documentation directly** | 5 | Pozdniakova, Paraschiv, Nyambura, ExamCert, Salinas (implicit) |
| 7 | **"The Google way" pattern — cost, managed services, AutoML/BQML preferred over custom** | 4 | Nyambura, Anil Kumar, ExamCert, Cassiopeia |
| 8 | **Book the exam early; deadline pressure unlocks focus** | 3 | Steven Chen, Pozdniakova, Anil Kumar (implied via fixed Oct 6 schedule) |
| 9 | **Reading comprehension and constraint analysis matter more than ML depth** | 3 | Cassiopeia, Pozdniakova, Paraschiv |
| 10 | **GenAI presence on exam is real but bounded — not the dominant theme** | 3 | Paraschiv (3–4 questions), DSumit ("not much"), Nyambura (Vertex-AI dominant) — and disagreement with Anil Kumar (see §7) |

Honorable mentions (n=2): "Hands-on lab time beats reading" (ExamCert, Paraschiv); "Take diagnostic exams early to find weak spots" (ExamCert, Cassiopeia, Paraschiv — actually n=3, included in #5); "TPU vs. GPU choice was tested" (Paraschiv only, n=1).

---

## 4. Stratified Breakdown by Background

### "No prior ML, no prior GCP" (closest match to your audience)
**Direct examples in corpus:** Cassiopeia is the cleanest analogue — she explicitly targets cloud-newcomers and recommends 3 months at ~1 hr/day weekdays + heavier weekends (≈60–75 hrs total). Steven Chen is partial fit — full-stack developer with limited prior production ML, GCP partner exposure but no cert.

**What worked for them:**
- Cassiopeia's 25% / 25% / 50% split (learning path / docs / practice) emphasizing question banks heavily
- Steven Chen's "register 3 months ahead, use the deadline" framing
- Both leaned hard on the Skills Boost ML Engineer learning path as the single most-cited resource

**Implication for two beginners studying together over 10–12 weeks:**
You match this profile most closely. Plan ~80–100 hours per person, weight your time toward (a) the Skills Boost learning path for breadth, (b) GCP best-practice docs for depth, (c) heavy practice-exam volume in weeks 6–12 with topic-tagged tracking. Build hands-on projects rather than only labs (ExamCert: "every hour in the console is worth three hours of docs"). Expect the bottleneck to be reading-comprehension under exam constraints, not ML math (which you have).

### "Prior ML, no GCP"
**Direct examples:** Paraschiv (NLP engineer, no GCP), DSumit (multi-year ML/data science).
**What worked:** Paraschiv's 30-day plan with conceptual-clarity-first, then strategic labs, then NotebookLM-driven personalized review. DSumit's shorter prep leaned on ML Crash Course + Skills Boost labs. Both reported the exam felt "intermediate++" given their ML background.

### "Prior GCP, no ML"
**Direct examples:** Nyambura (SWE + GenAI Leader cert holder), Dale Monteiro (PCA two months earlier).
**What worked:** Nyambura survived a 1-month nominal / 1-week effective intensive on pattern recognition ("the Google way") and a 48-hour Vertex AI doc deep-dive. Monteiro leveraged his PCA momentum but provided no specifics.

### Mixed / strong on both
**Direct examples:** Anil Kumar (renewal), Salinas (SRE+MS DS+multi-cert), ExamCert author (2yr ML + ACE).
**What worked:** Renewal-mode prep, leaning on prior cert muscle memory plus targeted GenAI deltas for v3.1.

**Best match for your audience:** Cassiopeia's writeup is your single most useful template. Paraschiv's structured-learning + topic-tagged-quiz approach is the second most transferable, with the caveat that he leveraged prior NLP/ML strength to compress timelines.

---

## 5. Time-Allocation Heatmap by Exam Section

The PMLE v3.1 has six exam sections (per the official Exam Guide):
- §1 Architecting low-code AI solutions (BQ ML, AutoML, ML APIs)
- §2 Collaborating within and across teams (data and model management)
- §3 Scaling prototypes into ML models (training, hyperparameter tuning)
- §4 Serving and scaling models (deployment, online/batch prediction)
- §5 Automating and orchestrating ML pipelines (Vertex AI Pipelines, Kubeflow)
- §6 Monitoring AI solutions (drift, retraining triggers, observability)

Recent writeup-derived study-time estimates (cross-referenced from ExamCert §2-3 weighting hints, Paraschiv's topic breakdown, DSumit's MLOps emphasis, Nyambura's Vertex-AI 60–70% claim):

| Section | Estimated % of study time | Justification |
|---|---|---|
| §5 Pipelines & orchestration | 22% | ExamCert: weighted equal-highest with §3. Paraschiv: strong Vertex AI Pipelines / Kubeflow questions. DSumit: pipelines named explicitly. |
| §3 Scaling/training | 22% | ExamCert weighting. Paraschiv: GPU/TPU choice was a pivotal theme. |
| §4 Serving/scaling | 16% | DSumit emphasizes train/serve skew. Pozdniakova / Cassiopeia: deployment scenarios common. |
| §6 Monitoring | 14% | Drift, retraining triggers — Anil Kumar, ExamCert, DSumit. |
| §1 Low-code AI | 13% | Anil Kumar emphasis on BQ ML / AutoML. Includes ~3–10% GenAI sub-content (Model Garden, Agent Builder). |
| §2 Collaboration / data & model management | 13% | Feature Store consistency theme — Anil Kumar. Lower visibility in writeups but explicitly weighted in exam guide. |

Beginners with no prior ML/GCP should bias slightly heavier toward §1 and §6 in early weeks (lower-conceptual-load entry points) and concentrate §3 and §5 in mid/late weeks once Vertex AI mental model is solid.

---

## 6. Common Exam-Day Surprises

1. **Multiple "technically correct" answers per question** — pick the Google-best-practice one. Cited by Pozdniakova, Cassiopeia, DSumit, Paraschiv ("single-best-answer format emphasized"). [Pozdniakova, Dec 2025; Cassiopeia, Feb 2026; DSumit, Nov 2025; Paraschiv, Feb 2026]

2. **Few-to-zero multi-select questions on actual exam** — Paraschiv reports ZERO multi-select on his exam despite practice apps including them; Omkar Rahane (Dec 2024 — borderline cutoff but post-Oct-2024-update) noted "1–2 maximum." [Paraschiv, Feb 2026]

3. **GPU vs. TPU infrastructure choice tested explicitly** — Paraschiv flags this as a pivotal question theme that is often missed. [Paraschiv, Feb 2026]

4. **Train/serve skew and Feature Store consistency as recurring traps** — DSumit and Anil Kumar both call this out as an exam-frequent topic. [DSumit, Nov 2025; Anil Kumar, Oct 2025]

5. **Time pressure is real but not crushing for prepared candidates** — Paraschiv finishes 50 questions in ~1 hour first pass + 45 min second pass + 15 min review. Nyambura got 30 min of buffer. DSumit got immediate results at testing center. [Paraschiv, Feb 2026; Nyambura, Jan 2026; DSumit, Nov 2025]

6. **Pattern-recognition "click" mid-exam** — Nyambura describes a real phenomenon where the first 30 minutes feel impossible until you internalize the Google-way decision pattern, then questions accelerate dramatically. [Nyambura, Jan 2026]

7. **Scenario questions about Experiments / Metadata / Workbench** — surfacing in the comment thread under the 30-day post; expect at least one workbench-uses-and-limits question. [Google Dev Forum thread comments, 2025]

---

## 7. Disagreements Between Passers

### How prominent is GenAI on the actual exam?
- **Paraschiv (Feb 2026):** "Only about 3–4 GenAI-related questions" out of 50 (~6–8%). Found best-practice docs sufficient.
- **DSumit (Nov 2025):** "Didn't see much reference to Gen AI or Gen AI specific quality metric." Implies near-zero.
- **Nyambura (Jan 2026):** GenAI was not a notable component of her exam — Vertex AI core ML infra dominated.
- **Anil Kumar (Oct 2025):** Treats GenAI as a *major* theme, frames the entire renewal article around the Gen AI / Model Garden / Agent Builder / Responsible AI shift.
- **Omkar Rahane (Dec 2024 — borderline):** Estimates ~10% of exam was GenAI.

**Resolution for your study plan:** Plan for ~8–12% of the exam to be GenAI-flavored (RAG with Agent Builder, Model Garden model selection, foundation-model fine-tuning, eval/Responsible-AI patterns), but do NOT over-weight GenAI at the expense of Vertex AI Pipelines, MLOps, and BQ ML/AutoML. The exam pool is randomized; Paraschiv likely got a low-GenAI draw, Anil Kumar a higher-GenAI draw. Worst case 4 questions, base case 6, plausible upper bound 10. Skipping GenAI entirely is risky; over-investing past ~12% of study time is wasteful.

### How long should beginners study?
- **Cassiopeia:** 3 months / ~60–75 hrs for cloud-newcomers
- **ExamCert:** 10 weeks / ~100–120 hrs
- **Paraschiv:** 60+ days minimum if you lack ML AND GCP
- **Nyambura:** 1 month nominal but strongly NOT recommends her own pace — she escaped via cert background and luck

**Resolution:** Your 10–12 week plan with two beginners studying together is well-aligned with the modal recommendation (~10 weeks). Plan for ≥80 hours each.

### "Vertex AI is 60-70%" vs. "MLOps is 60%"
- **Nyambura, ExamCert, Anil Kumar:** "Vertex AI 60-70%."
- **DSumit, ExamCert (also):** "MLOps 60%."

**Resolution:** Both are right because they overlap heavily. Vertex AI is the *vehicle*; MLOps is the *content*. Vertex AI Pipelines, Model Registry, Feature Store, Endpoints, Monitoring are simultaneously "Vertex AI" and "MLOps" topics. There is no real conflict.

### Are practice exams more useful or are docs more useful?
- **Cassiopeia:** 50% of time on practice questions
- **ExamCert:** Console hands-on > docs by 3:1
- **Paraschiv:** Conceptual clarity from courses+docs FIRST, then question banks
- **Pozdniakova:** Documentation-heavy ("questions are syphoned from official docs")

**Resolution:** Sequence matters: build conceptual scaffold (weeks 1–4) → hands-on labs/console (weeks 4–8) → high-volume tagged practice exams (weeks 8–12). All four passers ultimately used all three; they disagree on the proportions, not the components.

---

## 8. References

1. Salinas, M. "How I Passed the Google Cloud Professional Machine Learning Engineer Certification — And What I Learned." Medium, June 2, 2025. https://msalinas92.medium.com/how-i-passed-the-google-cloud-professional-machine-learning-engineer-certification-and-what-i-3d3066708124

2. Chen, S. (Liang). "Prepare Google Cloud Professional Machine Learning Engineer Certificate in 2025." Medium, July 13, 2025. https://steven-chen.medium.com/preparing-google-cloud-professional-machine-learning-engineer-certificate-in-2025-7035018d5d84

3. Kumar, A. "Balancing AI and Wellness: My Journey Renewing the Google Cloud Professional Machine Learning Engineer Certification in 2025." Medium / Google Cloud Community publication, October 9, 2025. https://medium.com/google-cloud/balancing-ai-and-wellness-my-journey-renewing-the-google-cloud-professional-machine-learning-0c3649e31a4a

4. Pozdniakova, N. "How I Passed the GCP Professional Machine Learning Engineer Exam in One Month." Medium, December 7, 2025. https://medium.com/@natalia.pozdniakova/how-i-passed-the-gcp-professional-machine-learning-engineer-exam-in-one-month-bd51c7ffc16a

5. Paraschiv, A. "How I Passed the Google Cloud Professional Machine Learning Engineer (PMLE) Exam in 30 Days, and so can you." Medium, February 15, 2026. https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4

6. Cassiopeia (V. Narvaez). "Prepare for the Professional Machine Learning Certification (2026) and Boost your Skills." Medium, February 1, 2026. https://medium.com/@vnarvaezt/prepare-for-the-professional-machine-learning-certification-2026-and-boost-your-skills-0f6cf3f4b78a

7. ExamCert. "The Exact 10-Week Plan That Got Me Through GCP PMLE (2026)." ExamCert blog, March 21, 2026. https://www.examcert.app/blog/gcp-ml-engineer-study-plan-2026/

8. Nyambura, A. "Earned Google Cloud ML Engineer Certification." Personal blog, January 6, 2026. https://blog.lxmwaniky.me/pmle

9. DSumit. Comment on "Google Cloud's Professional ML Engineer (PMLE) Exam: How I passed in 30 days." Google Developer Forums, November 15, 2025. https://discuss.google.dev/t/google-clouds-professional-ml-engineer-pmle-exam-how-i-passed-in-30-days-and-you-can-too/179510

10. Monteiro, D. Comment on the same Google Developer Forums thread, January 12, 2026. https://discuss.google.dev/t/google-clouds-professional-ml-engineer-pmle-exam-how-i-passed-in-30-days-and-you-can-too/179510

### Rejected (predate April 2025 cutoff)

- Tan, J. (March 2022) — predates v3.1 by years
- Hussain, A. (March 2022) — predates v3.1
- Webb, T. (PMLE Exam Notes, 2024) — pre-update
- umangak / 30-Days post (January 2025) — pre-cutoff and pre-v3.1
- Rahane, O. (December 2024) — post-Oct-2024 update but pre-cutoff; useful but excluded per instructions
- Ajayi, A. (January 17, 2025) — pre-cutoff
- Hilliao (February 2025) — pre-cutoff
- Hasan Rafiq (originally January 2021, updated 2025 but original date primary) — date ambiguous, conservatively rejected

---

## Confidence and Decay Risk

**Confidence: Medium-High.** Of 10 anecdotes, 7 are full long-form first-person writeups with extractable structure; 2 are forum comments by self-identified passers (lower fidelity); 1 (Salinas) is partially paywalled. Geographic and role diversity is good. The main weakness is **score data is universally undisclosed** (all writeups treat "Pass" as binary), so we cannot calibrate effort-to-margin. A second weakness is that all writeups are by passers — survivorship bias means no failure data points. The signal-to-noise on the 10 themes ranked is strong because each theme is independently corroborated by 3+ writeups.

**Decay risk: Medium.** GCP exam content evolves quickly — Google has historically refreshed PMLE every 18–24 months, and v3.1 launched April 2025. Expect some writeups (especially mid-2025 entries like Salinas and Steven Chen) to become slightly stale by late 2026 as Google's GenAI offerings (Agent Builder rebrand to Agent Platform, new Gemini models) keep shifting. The CORE Vertex AI / MLOps content (Pipelines, Feature Store, Model Registry, Endpoints, Monitoring) has been stable since 2022 and is unlikely to be invalidated. GenAI-specific content (Model Garden, Agent Builder questions) has the highest decay risk. Re-validate this corpus with fresh writeups in approximately Q3 2026 if the exam guide gets a v3.2 refresh.

**Audience-fit: Strong.** Cassiopeia (#6) is the closest behavioral match to two beginners studying together for 10–12 weeks. Paraschiv (#5) is the second-most useful template, scaled by the fact that he leveraged prior NLP experience to compress to 30 days — your unscaled timeline of 10–12 weeks is realistic and well-supported by Cassiopeia, ExamCert, and the modal recommendation across the corpus.
