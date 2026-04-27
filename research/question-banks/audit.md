# PMLE v3.1 Practice Question Bank Audit

Audit date: 2026-04-25. Target: select 2-4 question banks for two beginners studying together for ~10-12 weeks for the Google Cloud Professional Machine Learning Engineer (PMLE) exam, version 3.1 (current since April 2025; emphasizes generative AI on Model Garden / Vertex AI Agent Builder, RAG, and foundation-model fine-tuning).[^cloud-cert] [^exam-guide]

## 1. Summary table

| Bank | Q count | Price USD | Last updated | Quality (1-5) | v3.1 GenAI | Ethical | Recommended |
|---|---|---|---|---|---|---|---|
| Google official sample (Form) | ~15-25 Qs | Free | v3.1 aligned[^cloud-cert] | 5 | Yes | Y | Yes |
| Tutorials Dojo PMLE | No product[^td-portal] | n/a | n/a | n/a | n/a | Y | No (n/a) |
| Whizlabs PMLE | Not public | $49/mo or $199/yr; +$79/$299[^whiz-pricing] | Blog dated 2021[^whiz-blog] | 3 | Partial | Y | Maybe |
| ExamTopics PMLE | 300+[^et-page] | Free / $149[^et-page] | Q299+ active[^et-q299] | 2 | Partial | **N** dump | No |
| Skillcertpro PMLE | 887 / 15 tests[^scp-product] | $19.99 (RRP $39.99)[^scp-product] | 2026-04-21[^scp-product] | 3 | Partial-Yes | **N** "from real exams"[^scp-product] | No |
| Top Udemy PMLE | 200-400 typ. | $10-20 sale | 2025-26[^udemy-refresh] | 2-3 | Partial | Mixed | Maybe (1, vetted) |
| Pluralsight / A Cloud Guru | Bundled[^ps-help] | $29/mo or $299/yr | Jan 2026 review[^ps-help] | 3-4 | Partial | Y | Maybe |
| ExamPro (Andrew Brown) | No product[^exampro-search] | n/a | n/a | n/a | n/a | Y | No (n/a) |
| AndyTheFactory gcp-pmle-quiz | 841 (verified)[^andy-local] | Free | Data file 2025-03-20[^andy-local] | 3-4 | Yes (537/841 hits)[^andy-local] | Mixed (transparent)[^andy-medium] | Yes |
| Anki decks (PMLE-specific) | None found[^ankiweb] | n/a | n/a | n/a | n/a | Y | No (build your own) |
| PassQuestion / ITExams / etc. | 100s leaked[^itexams] | $20-80 | Continuous | 1-2 | Yes | **N** NDA[^gcp-terms] | No |

## 2. Detailed notes

### Google official sample exam
The Google Form linked from the certification landing page shows "Page 1 of 17" with branching/explanation pages (well under ~25 scenario items) and is intentionally not scored.[^cloud-cert] [^official-form] It is the only resource Google publishes openly, aligned to exam guide v3.1 including Model Garden and Agent Builder.[^cloud-cert] [^exam-guide] Treat it as calibration, not a bank: do it once early to learn the question style and once near the end.

### Tutorials Dojo (Jon Bonso)
TD is the gold standard for AWS practice exams (Bonso: 272k students, ~48k reviews)[^td-quality] but **as of 2026-04-25 no PMLE-specific TD product exists on the TD portal or GCP study-guide hub**.[^td-portal] [^td-gcp] If TD ships one mid-prep, revisit.

### Whizlabs PMLE
Whizlabs bundles PMLE inside Premium ($199/yr) or Premium+ ($299/yr); the standalone product page does not publish a question count, and the free-questions blog post carries 2021 metadata.[^whiz-pricing] [^whiz-blog] G2/Trustpilot reviews are mixed: praised for "structured, longer-than-real-exam difficulty" but criticized for pricing and slow content refresh.[^whiz-g2] Publicly visible content shows limited explicit Model Garden / Agent Builder / RAG coverage, so v3.1 GenAI updates appear incomplete.[^whiz-blog]

### ExamTopics — Professional Machine Learning Engineer
ExamTopics hosts a free Q&A topic past Q299 with active discussion threads; questions are **reconstructed from real exam content by test-takers**.[^et-page] [^et-q299] [^et-discuss] That is exactly what Google's certification Terms ban under sections (c) ("reconstruction through memorization") and (e) ("brain-dump material").[^gcp-terms] **Do not use.**

### Skillcertpro PMLE
Skillcertpro sells a 15-test, 887-question PMLE bundle for $19.99 (retail $39.99), updated 2026-04-21.[^scp-product] **Critical ethical flag**: the product page itself states questions are "Taken exclusively from the previous real exams."[^scp-product] That language is a textbook braindump. Reviews are bimodal: some report "70%+ identical phrasing to the real exam" (which is itself the problem), while a Medium reviewer flags inconsistent and incorrect answers and a Trustpilot snippet says "about 30% of answers are plain wrong."[^scp-medium] [^scp-trustpilot-snippet] Avoid.

### Top Udemy PMLE practice tests
There is no clear #1 Udemy PMLE author equivalent to Stephane Maarek/Bonso on the AWS side; the topic page returns a long tail of "MA Rahman" / "ExamsDigest" / "IBM Solution Architect" / 2026 Refresh courses, none with dominant volume.[^udemy-topic] [^udemy-prep25] [^udemy-refresh] Most are 4-6 timed tests, ~250-360 Qs, $10-20 on sale, with claimed Vertex AI / GenAI coverage. Quality is uneven and several visibly recycle ExamTopics content, so spot-check 2-3 free preview questions against ExamTopics before buying.

### A Cloud Guru / Pluralsight
Pluralsight (owner of A Cloud Guru) confirms PMLE practice exams are bundled in the standard subscription, refreshed against the latest exam guide (a January 2026 review date appears in the search snippet).[^ps-help] [^ps-acg] No public question count; reviews suggest 1-2 full-length exams with good explanations but slower v3.1 GenAI updates. Worth using if you already have a subscription; not worth subscribing solely for PMLE.

### ExamPro (Andrew Brown)
ExamPro publishes free GCP video content but, as of 2026-04-25, **no dedicated PMLE practice-test product appears on exampro.co or in Brown's Udemy catalog**.[^exampro-search] [^exampro-yt] Brown's GCP coverage skews to Cloud Digital Leader and Generative AI Leader. Watch the GenAI Leader videos for free GenAI grounding; do not count on it for PMLE-style scenario questions.

### AndyTheFactory/gcp-pmle-quiz (GitHub)
The repo contains exactly **841 quiz items** in `data/quizzes.jsonl` (verified locally), each with question, options, integer answer index, and explanation.[^andy-local] [^andy-readme] 537/841 items hit at least one keyword in vertex/gemini/model garden/agent builder/RAG/fine-tun/generative/foundation model/LLM - unusually strong v3.1 GenAI coverage for a community bank.[^andy-local] The author Andrei Paraschiv documents on Medium that he initially used SkillCertPro and ExamTopics, found errors, and built his own curated bank with explanations - so some provenance is community-recall, but it is free, open source, and inspectable.[^andy-medium] Streamlit UI tracks wrong answers and supports re-drilling. Risk: no formal QA, small commit history, and item overlap with ExamTopics. Recommended **as the workhorse bank**, paired with a vetted secondary source.

### Anki decks (r/googlecloud, AnkiHub, AnkiWeb)
Searches across AnkiWeb, AnkiHub, and GoogleCloudPlatform/google-cloud-flashcards returned **no usable PMLE-specific deck**; available GCP decks cover ACE, Cloud Architect, and Data Engineer only.[^ankiweb] [^gcp-flash-gh] Plan to build ~150-300 cards yourselves from the v3.1 exam guide and your wrong-answer log.

### PassQuestion / ITExams / similar dump aggregators
Dump aggregators (ITExams, Certification-Questions, CloudPass, Marks4sure, Pass4itsure, DumpsPedia, PrepAway, ExamCollection, etc.) publish reconstructed real exam content for $20-80, "updated" weekly to track exam revisions.[^itexams] [^certq] [^cloudpass] They violate Google Cloud Certification Program Terms sections (c) and (e) and risk decertification.[^gcp-terms] **Do not use any of them.**

## 3. Recommended consumption order

**Pick 3 banks for the 10-12 week plan, in this order:**

**Weeks 1-2 (calibrate):** Take the Google official sample form once cold to feel the question style, then put it aside.[^cloud-cert] [^official-form] Skim the v3.1 exam guide twice and tag the six domains in your notes.[^exam-guide]

**Weeks 3-8 (build & drill):** Drive your daily review with the **AndyTheFactory/gcp-pmle-quiz** Streamlit app on the laptop you already cloned it to. Do ~30-60 questions/day in topic-shuffle mode, save wrong answers, and use those wrong-answer exports as Notebook LM seeds (the README documents this workflow).[^andy-readme] In parallel, build a personal Anki deck of ~250 cards from your wrong-answer log and the GenAI sub-domain (Model Garden, Agent Builder, RAG patterns, fine-tuning vs prompt-tuning vs distillation tradeoffs, evaluation metrics for LLMs).

**Weeks 9-10 (rigor pass):** Add **one** vetted secondary bank for fresh question style. Best options, in order of preference: (a) **Pluralsight/A Cloud Guru PMLE practice exams** if you or your study partner already have a subscription (legitimate, exam-guide-aligned, Jan 2026 refresh)[^ps-help]; (b) **Whizlabs PMLE** standalone or via 7-day Premium trial if Pluralsight is not available, despite the dated blog metadata[^whiz-pricing] [^whiz-blog]; (c) one carefully chosen **Udemy** PMLE practice course, only after reading 5+ recent reviews that confirm v3.1 GenAI coverage and answer accuracy.[^udemy-prep25]

**Weeks 11-12 (final calibration):** Re-take the Google official form, then 2-3 timed full-length practice exams from your secondary bank under proctor-style conditions, targeting >=80%. Use the last 3 days for wrong-answer review only - not new content.

Rationale 1: the goal of a beginner pair is **breadth across 841+ scenarios** and **reps in the GenAI sub-domain v3.1 emphasizes**, not identical-to-real-exam phrasing. Andy's bank is large enough for multiple full passes, free, locally hosted (private wrong-answer log), and unusually GenAI-heavy. Pairing it with one professional bank in the back half catches stale or wrong items without NDA exposure.

Rationale 2: we exclude SkillCertPro and ExamTopics not because they would not "work" - they would - but because they reconstruct live-exam content in violation of Google's Terms.[^gcp-terms] [^scp-product] [^et-page] Two beginners can hit 80%+ on a clean stack (Andy's bank + Pluralsight or Whizlabs + your own Anki deck + the v3.1 guide + Vertex AI labs); there is no need for the ethical risk.

## 4. Ethical / dump-site warnings

Sources we judge to be **verbatim or near-verbatim leaked exam content (do not use)**:

- **ExamTopics** PMLE - openly described as "actual Q&As" reconstructed by test-takers, hundreds of items, discussion threads.[^et-page] [^et-q299] [^et-discuss]
- **Skillcertpro** PMLE - product page says "Taken exclusively from the previous real exams" - textbook braindump per Google's terms.[^scp-product]
- **PassQuestion, ITExams, Marks4sure, Pass4itsure, Certification-Questions, DumpsPedia, ExamCollection, PrepAway, DumpsArena, DumpsGate, Cloud Pass, certshero, Validexamdumps, Pass4success** - all market as "exam dumps" with frequent updates tracking real exam revisions; fail Google's Terms (c), (e), (m).[^itexams] [^certq] [^cloudpass] [^gcp-terms]
- Some Udemy PMLE courses visibly copy from ExamTopics; spot-check 5-10 Qs against ExamTopics before purchase.[^udemy-topic]

Google's Certification Program Terms (effective 2021-08-31, current as of 2026-04-25) ban (c) "reconstruction through memorization or any other method," (e) "Using unauthorized materials (including brain-dump material...)," and (m) accessing "materials in forums, chat rooms, discussion groups, blogs or other sharing sites with intent to circumvent Exam procedures."[^gcp-terms] Penalties: exam invalidation and decertification.[^gcp-terms]

Grey zone: AndyTheFactory's bank includes items whose phrasing overlaps community resources. Acceptable because it is free, inspectable, and the author is transparent. If a question reads like a memorized exam scenario, study the underlying concept - do not memorize the question.

## 5. References

All access dates 2026-04-25.

[^cloud-cert]: Google Cloud, "Professional ML Engineer Certification" landing page. https://cloud.google.com/learn/certification/machine-learning-engineer (page version not dated; v3.1 exam guide linked).
[^exam-guide]: Google, "Professional Machine Learning Engineer Exam Guide v3.1." https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf (PDF marked v3.1 final; current per cert landing page).
[^official-form]: Google official PMLE sample exam (Google Form). https://docs.google.com/forms/d/e/1FAIpQLSeYmkCANE81qSBqLW0g2X7RoskBX9yGYQu-m1TtsjMvHabGqg/viewform (form indicates "Page 1 of 17"; access requires Google sign-in; not scored).
[^whiz-pricing]: Whizlabs Pricing. https://www.whizlabs.com/pricing/ (Premium $49/mo or $199/yr; Premium+ $79/mo or $299/yr; verified via search snippet 2026-04-25).
[^whiz-blog]: Whizlabs, "25 Free Questions - Google Cloud Certified Professional Machine Learning Engineer." https://www.whizlabs.com/blog/gcp-professional-machine-learning-engineer-questions/ (page metadata still shows 2021-11-30; topic list does not publicly include Model Garden / Agent Builder / RAG).
[^whiz-g2]: G2, "Whizlabs Reviews 2026." https://www.g2.com/products/whizlabs/reviews (mixed reviews; pricing complaint pattern; 2026 dated index).
[^et-page]: ExamTopics, "Google Professional Machine Learning Engineer." https://www.examtopics.com/exams/google/professional-machine-learning-engineer/ (positions content as "actual Q&As").
[^et-q299]: ExamTopics discussion thread for Topic 1 Q299. https://www.examtopics.com/discussions/google/view/157543-exam-professional-machine-learning-engineer-topic-1-question/ (confirms 299+ active questions in catalog).
[^et-discuss]: ExamTopics discussion thread for Topic 1 Q171. https://www.examtopics.com/discussions/google/view/130588-exam-professional-machine-learning-engineer-topic-1-question/ (community-corrected answers, characteristic of brain-dump model).
[^scp-product]: SkillCertPro, "Google Machine Learning Engineer Exam Questions 2026." https://skillcertpro.com/product/google-machine-learning-engineer-exam-questions/ (price $19.99 down from $39.99; 887 questions across 15 mock exams; "last updated April 21, 2026"; product copy: "Taken exclusively from the previous real exams").
[^scp-medium]: Andrei Paraschiv, "How I passed the Google Cloud Professional Machine Learning Engineer (PMLE) Exam in 30 Days, and so can you." Medium, published 2026-02-15. https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4 (cites SkillCertPro/ExamTopics for "exposure" but flags inconsistent and incorrect answers).
[^scp-trustpilot-snippet]: Trustpilot reviews of skillcertpro.com (search-engine snippet retrieved 2026-04-25; full Trustpilot page returned 403 to direct fetch). https://www.trustpilot.com/review/skillcertpro.com (snippet: "many of the questions have serious wording errors, and about 30% of their answers are plain wrong").
[^udemy-topic]: Udemy topic page for Google Cloud Professional Machine Learning Engineer (April 2026 index). https://www.udemy.com/topic/google-cloud-professional-machine-learning-engineer/.
[^udemy-prep25]: Udemy, "Google Professional Machine Learning Engineer Exam Prep 2025." https://www.udemy.com/course/google-professional-machine-learning-engineer-exam-prep-2025/.
[^udemy-refresh]: Udemy, "Google Professional Machine Learning Engineer [2026 Refresh]." https://www.udemy.com/course/2026-google-professional-machine-learning-engineer-exams/.
[^ps-help]: Pluralsight Help Center, "Google Cloud certification practice exams." https://help.pluralsight.com/hc/en-us/articles/24392127517972-Google-Cloud-certification-practice-exams (PMLE practice exam included; "reviewed January 2026" per search snippet 2026-04-25; full page returned 403 to direct fetch).
[^ps-acg]: Pluralsight / A Cloud Guru, "AI and machine learning courses (GCP)." https://www.pluralsight.com/cloud-guru/paths/gcp-data-machine-learning.
[^exampro-search]: ExamPro / exampro.co (no PMLE practice-test product visible as of 2026-04-25; confirmed via web search 2026-04-25).
[^exampro-yt]: ExamPro YouTube channel. https://www.youtube.com/channel/UC2EsmbKnDNE7y1N3nZYCuGw.
[^andy-local]: Local clone at /Users/patricktaylor/Documents/Google-PMLE/gcp-pmle-quiz; `wc -l data/quizzes.jsonl` returns 841; keyword grep for vertex/gemini/model garden/agent builder/RAG/fine-tun/generative/foundation model/LLM returns 537 hits (2026-04-25).
[^andy-readme]: AndyTheFactory/gcp-pmle-quiz README. https://github.com/AndyTheFactory/gcp-pmle-quiz (Streamlit app; ~850 questions; Notebook LM export workflow).
[^andy-medium]: Andrei Paraschiv, "How I passed the Google Cloud Professional Machine Learning Engineer (PMLE) Exam in 30 Days." Medium 2026-02-15. https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4 (author of Andy quiz repo; documents provenance).
[^ankiweb]: AnkiWeb shared decks search (queried 2026-04-25); only ACE / Data Engineer / Cloud Architect decks returned; no PMLE-specific deck of usable size. Examples: https://ankiweb.net/shared/info/1707301842, https://ankiweb.net/shared/info/1346064888, https://ankiweb.net/shared/info/1476025060.
[^gcp-flash-gh]: GoogleCloudPlatform/google-cloud-flashcards. https://github.com/GoogleCloudPlatform/google-cloud-flashcards (general GCP flashcards; not PMLE-specific).
[^itexams]: ITExams, "Google Professional Machine Learning Engineer." https://www.itexams.com/exam/Professional-Machine-Learning-Engineer.
[^certq]: Certification-Questions.com, "Google Professional-Machine-Learning-Engineer Dumps." https://www.certification-questions.com/google-exam/professional-machine-learning-engineer-dumps.html (markets itself as "Updated 2026-03-09").
[^cloudpass]: CloudPass.pro, "Google PMLE Exam Dumps and Practice Questions 2025." https://www.cloudpass.pro/en/exams/gcp/google-pmle.
[^gcp-terms]: Google Cloud Certification Program Terms (effective 2021-08-31, current as of 2026-04-25). https://cloud.google.com/certification/terms/index-20210831 (extracted misconduct sections (c), (e), (m); confidential information clause).
[^td-portal]: Tutorials Dojo Portal. https://portal.tutorialsdojo.com (no GCP PMLE practice exam product listed as of 2026-04-25).
[^td-gcp]: Tutorials Dojo, "Google Cloud Exam Study Guides." https://tutorialsdojo.com/google-cloud-gcp-exam-study-guides/ (GCP study-guide hub; no PMLE practice exam product link).
[^td-quality]: Stephane Maarek / Jon Bonso reputation references aggregated via Quora and Medium (2024-2026). https://www.quora.com/What-are-your-thoughts-on-the-Tutorials-Dojo-Jon-Bonso-practice-exam-in-Udemy-Has-anyone-recently-passed-this and https://www.udemy.com/user/jonjonbonso/.
[^serverside]: TheServerSide, "Google Professional Machine Learning Engineer Certification Practice Exams." https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Google-Professional-Machine-Learning-Engineer-Certification-Practice-Exams (recommends honest study; warns against dumps).

---

**Confidence:** Medium-High on the ethical recommendations and on AndyTheFactory's metrics (verified locally). Medium on Whizlabs / Pluralsight question counts and Udemy author rankings (vendor sites returned 403 to direct fetch; relied on search snippets and aggregator data).

**Decay risk (what will go stale fastest):**
1. **Skillcertpro / Whizlabs / Udemy pricing and update dates** - these change monthly; reverify before purchase.
2. **Tutorials Dojo PMLE existence** - TD has been expanding into GCP; a PMLE product may launch mid-prep and would likely become a top-2 recommendation if it does.
3. **Pluralsight / A Cloud Guru subscription pricing and PMLE practice-exam refresh date** - Pluralsight refactored their pricing tiers in 2025-2026; reverify at purchase time.
4. **Google's Certification Program Terms version** - 2021-08-31 is current today, but Google has announced certification program revamps; check cloud.google.com/certification/terms for a newer dated version before exam day.
5. **AndyTheFactory repo activity** - if upstream stops accepting fixes, drift from v3.1 will start to bite around the GenAI sub-domain by late 2026.
