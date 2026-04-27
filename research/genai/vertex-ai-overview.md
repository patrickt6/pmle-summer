# Vertex AI Generative AI — PMLE v3.1 Study Overview

**Audience:** Two PMLE candidates (math-strong, GCP/ML-production beginners) on a 10–12 week plan, preparing for the v3.1 exam (effective April 2025; first version with explicit GenAI content).
**Decay warning:** This is the highest-decay area on the exam. Google rebranded the entire Vertex AI surface to **Gemini Enterprise Agent Platform** at Google Cloud Next 2026 (April 22, 2026). The exam guide and most blog posts/courseware still say "Vertex AI." Both names are correct for the exam — but the docs you click into will increasingly say "Agent Platform."

---

## 1. Overview — what GenAI scope means on the v3.1 exam

The v3.1 exam guide (effective April 2025) is the first PMLE version to explicitly test generative AI. The official guide ([services.google.com PDF](https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf)) introduces five GenAI touchpoints: §1.2 (build RAG with Agent Builder; consume ML APIs from Model Garden; use industry APIs like Document AI/Retail), §2.2 (foundation + open-source models in Model Garden), §2.3 (evaluating GenAI solutions), §3.2 (fine-tuning foundation models), and §6 (monitoring GenAI for drift, hallucination, safety). The questions are scenario-based — they test *which Vertex AI product to pick* and *which technique fits a given constraint*, not API trivia. You should be able to defend choices like "managed RAG via Agent Builder + Vertex AI Search" vs "custom RAG via Vector Search + Gemini" or "supervised fine-tune with LoRA" vs "RLHF/preference tuning" vs "RAG only." The biggest study trap: 2022–2023 PMLE guides predate this entire surface area, so legacy material is useless for these sections (FlashGenius 2026 guide, [link](https://flashgenius.net/blog-article/google-professional-machine-learning-engineer-certification-2026-guide)).

---

## 2. Concept-to-product map

| Exam concept | Product (legacy / current name) | Console / docs entry point |
|---|---|---|
| Foundation model catalog (Gemini, Imagen, Veo, Lyria, Claude, Llama, Mistral, Gemma, DeepSeek, Qwen) | **Vertex AI Model Garden** (now "Model Garden on Gemini Enterprise Agent Platform"; ~200 models) | `cloud.google.com/model-garden` |
| Prompt design, prompt gallery, prompt optimizer, side-by-side prompt comparison | **Vertex AI Studio** (formerly *Generative AI Studio*; now *Agent Platform Studio*) | `console.cloud.google.com/vertex-ai/studio` |
| Build RAG / search / chat agents (managed) | **Vertex AI Agent Builder** (formerly *Gen App Builder* → *Vertex AI Search and Conversation* → *AI Applications* → now *Gemini Enterprise Agent Platform*) | `cloud.google.com/products/agent-builder` |
| Enterprise document/website search backbone | **Vertex AI Search** (formerly *Enterprise Search* / *Generative AI App Builder Search*; renaming to *Agent Search*) | `docs.cloud.google.com/generative-ai-app-builder/docs` |
| Conversational chatbot designer | **Conversational Agents** (formerly *Dialogflow CX*, late-2024 rename) | `docs.cloud.google.com/dialogflow/cx/docs` |
| Managed RAG pipeline service | **Vertex AI RAG Engine** (now *Agent Platform RAG Engine*; GA Dec 2024) | `docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview` |
| ANN vector store for DIY RAG | **Vertex AI Vector Search** (formerly *Vertex AI Matching Engine*, renamed Aug 29 2023) | `docs.cloud.google.com/vertex-ai/docs/vector-search/overview` |
| Tether output to verifiable data | **Grounding** (Google Search, Vertex AI Search, Maps, Elasticsearch, custom) | `docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview` |
| Fine-tune Gemini | **Supervised fine-tuning** + **Preference tuning** (RLHF-style) on Gemini 2.5 Pro / Flash / Flash-Lite (LoRA-based PEFT) | `docs.cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models` |
| Agent runtime + framework | **Vertex AI Agent Engine** (formerly *Reasoning Engine* / *LangChain on Vertex AI*) + **Agent Development Kit (ADK)** (preview Apr 2025) | `docs.cloud.google.com/agent-builder/agent-engine/overview` |
| Evaluate GenAI quality | **Gen AI Evaluation Service** (pointwise + pairwise) and **AutoSxS** (pairwise pipeline) | `docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview` |
| Monitor GenAI in prod | **Model Observability Dashboard** + **Cloud Monitoring** + **Eval service on production logs** | `docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-observability` |
| Industry/document parsing APIs | **Document AI**, **Retail API** (cited in §1.2) | `cloud.google.com/document-ai` |

---

## 3. Vertex AI Model Garden

**What it is:** A curated catalog of ~200 models that you discover, test, customize, and deploy from one console, with consistent integration into Vertex AI tuning/eval/serving (Model Garden overview, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models), retrieved Apr 2026).

**Three model categories the exam expects you to know:**
1. **First-party Google foundation models** — Gemini (3.1 Pro/Flash, 2.5 Pro/Flash/Flash-Lite, embedding variants), Imagen 3/4 (image gen + Virtual Try-On), Veo 2/3/3.1 (video), Lyria (music), Chirp (speech). Native tuning + eval support.
2. **Partner / third-party models (Model-as-a-Service)** — Anthropic Claude (Opus, Sonnet, Haiku), xAI Grok, Mistral, Meta Llama, plus open-source MaaS like DeepSeek, Qwen, MiniMax. Pay-per-token, no infrastructure to manage.
3. **Open-source self-deployed** — Gemma (Google's open family), Llama, others. You pick a deployment (e.g., GKE, custom container) and pay compute. (Categories per [Google Cloud Model Garden product page](https://cloud.google.com/model-garden), Apr 2026.)

**How to invoke** (exam-relevant): Console UI → "Deploy" or "Open notebook"; Python SDK (`google-cloud-aiplatform` / `vertexai`); CLI; REST. ML-API style (no infra) for first-party + MaaS partner models; endpoint-style for self-deployed open models.

**Exam traps:** (a) Model Garden ≠ Studio. Model Garden is the *catalog*; Studio is the *prompt-design tool* that calls catalog models. (b) For "industry APIs" in §1.2, prefer **Document AI** (forms/invoices) or **Retail API** (recommendations/search) over generic Gemini calls — they are pre-trained and require no prompt engineering.

---

## 4. Vertex AI Agent Builder (now Gemini Enterprise Agent Platform)

**Critical naming note:** This product has been renamed five+ times. For the exam (which still uses v3.1 wording from April 2025), say **"Vertex AI Agent Builder"**. In current Google docs (April 2026 forward) you will see **"Gemini Enterprise Agent Platform"** ([Google Cloud Blog, Apr 22 2026](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform)). They are the same thing.

**Current scope (post-April 2025 rebrand to "AI Applications", then April 2026 rebrand to "Gemini Enterprise Agent Platform"):**
- **Vertex AI Search** — turnkey enterprise search over your docs, websites, structured data; provides retrieval + grounding APIs.
- **Conversational Agents** (formerly Dialogflow CX, renamed late-2024 → early-2025 per [Zenn rename log](https://zenn.dev/soundtricker/articles/2ae25658eb41b2)) — visual chatbot/voicebot designer; integrates Vertex AI Search as a "data store" tool.
- **Agent Engine** — managed runtime for deployed agents; handles sessions, memory, scaling, tracing. Supports any framework (ADK, LangGraph, CrewAI, custom).
- **Agent Development Kit (ADK)** — open-source Python framework for authoring multi-agent workflows (preview April 2025; [adk.dev](https://google.github.io/adk-docs)).
- **Agent Garden** — gallery of pre-built agent templates (April 2025).
- **Agent Studio** — low/no-code visual agent builder added at Next 2026.

**How RAG works in Agent Builder (managed pattern, exam favorite):**
1. Create a Vertex AI Search **data store** pointing at GCS, BigQuery, websites, or Drive.
2. Vertex AI Search auto-handles parsing, chunking, embedding, indexing.
3. At query time, the agent calls the search data store, gets ranked snippets, passes them as context to Gemini with grounding metadata.
4. Response includes citations / grounding attribution (per [Grounding with Vertex AI Search docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-vertex-ai-search), updated 2026-04-10).

This is the §1.2 "RAG with Vertex AI Agent Builder" pattern the exam guide names.

---

## 5. Vertex AI Studio

**What it is:** The browser IDE for prompt engineering against Model Garden models. Originally launched June 2023 as **Generative AI Studio**, renamed to **Vertex AI Studio**, and now branded **Agent Platform Studio** ([InfoWorld 2026](https://www.infoworld.com/article/2336686/google-vertex-ai-studio-puts-the-promise-in-generative-ai.html); [Google Skills 2026](https://www.skills.google/focuses/86502)).

**Capabilities the exam expects you to recognize** (per [Studio capabilities docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/vertex-ai-studio-capabilities), retrieved Apr 2026):
- **Freeform prompt design** — text, code, image, video, audio inputs.
- **Prompt gallery** — sample prompts for extraction, summarization, customer-service, healthcare, code (per [prompt-gallery docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery)).
- **Prompt template management** — save, version, share.
- **Help-me-write** (`/prompt`) — Gemini drafts/refines your prompt.
- **Side-by-side comparison** (`/compare`) — run the same prompt against two models or two prompt variants.
- **Vertex AI Prompt Optimizer** — automatic prompt optimization (APO) based on Google Research's NeurIPS 2024 paper; iterative LLM-based search using an "optimizer" + "evaluator" model ([Google Cloud Blog announcement](https://cloud.google.com/blog/products/ai-machine-learning/announcing-vertex-ai-prompt-optimizer)).
- **Code export** — download the prompt as Python/REST.

Studio is the *workbench*; once a prompt is good, you save it, then call from your app via SDK or wire it to Agent Builder.

---

## 6. Gemini fine-tuning

The exam guide §3.2 says "fine-tune foundational models with Vertex AI / Model Garden." On Vertex AI today (April 2026) the supported tuning paths for **first-party Gemini** are ([tune-models overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models)):

| Method | What it does | Use when | Vertex AI implementation |
|---|---|---|---|
| **Supervised fine-tuning (SFT)** | Teach a new task/skill from labeled (input, output) pairs | You have ≥100–1,000 high-quality examples and a defined output format | LoRA-based PEFT under the hood; JSONL dataset, max 1 GB, configurable adapter size 1/2/4/8/16; supported on Gemini 2.5 Pro / Flash / Flash-Lite (per [Gemini SFT docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning)) |
| **Preference tuning** (RLHF-style) | Align model with subjective preference signals from human (or LLM) raters | Quality is subjective — tone, safety, style — and SFT alone misses nuance | Available on Gemini 2.5 Flash / Flash-Lite; uses preference-pair datasets |
| **Distillation** | Train a smaller model to mimic a larger one | You need lower latency/cost while preserving quality of a tuned big model | Available via Vertex AI tuning pipelines for select model families |
| **Adapter / parameter-efficient (PEFT)** | Update a small subset of weights | You want lower training cost, faster iteration, multiple task-specific adapters | Built into Gemini SFT (LoRA); standard for OSS models in Model Garden |

**Decision heuristic the exam loves:** Try **prompting** first. If quality plateaus and you have labeled data, do **SFT**. If you need *behavioral* alignment (helpfulness, tone, safety) and only have preference data, use **preference tuning / RLHF**. If you cannot share data with a foundation model API, RAG ≠ tuning — they solve different problems (RAG injects facts at inference; tuning bakes in skill/style). Cited in [Google Cloud Blog "RAG vs. Fine-tuning"](https://cloud.google.com/blog/products/ai-machine-learning/to-tune-or-not-to-tune-a-guide-to-leveraging-your-data-with-llms).

---

## 7. Evaluating GenAI solutions

§2.3 wants you to know that GenAI eval is **not** a single accuracy number. Vertex AI offers two complementary tools:

**A. Gen AI Evaluation Service** ([eval overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)) — a Python SDK + API that runs metrics against your model's outputs. Two evaluation **modes**:
- **Pointwise** — judge one model's output against criteria; output is a 0–5 (or 0/1 pass/fail) score. Used for absolute quality gates, regression tests.
- **Pairwise** — judge model A vs model B on the same prompts; output is a win-rate / preference. Used for migrations and A/B comparisons.

Three **metric families**:
- **Computation-based** — deterministic: ROUGE, BLEU, exact match, edit distance. Need ground truth.
- **Model-based (LLM-as-judge)** — a "judge" Gemini scores fluency, factuality, groundedness, safety. Implemented as **adaptive rubrics** (auto-generated per-prompt unit-test-style criteria; recommended) or **static rubrics** (fixed scale).
- **Custom** — user-defined Python function metrics.

**B. AutoSxS** (Automatic Side-by-Side, [docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/side-by-side-eval)) — a managed *pairwise* pipeline that runs an autorater LLM to compare two model versions on summarization or QA tasks (4,096-token limit). Outputs win-rate + per-example preference and rationale. Best for offline regression testing of a tuned model vs the base. (The service is still active in April 2026; the docs note that newer pairwise features live in the broader Eval Service — [eval-overview note](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview).)

**Exam mapping:** automated metrics → cheap, fast, regression-friendly, but blind to factuality nuance. Human eval → expensive, gold standard. Model-based metrics + AutoSxS → the practical middle ground, what production teams use.

---

## 8. RAG implementation patterns — managed vs DIY

The §1.2 RAG question almost always reduces to *which pattern fits the scenario*. Two canonical patterns ([Google Cloud Blog "RAG and grounding on Vertex AI"](https://cloud.google.com/blog/products/ai-machine-learning/rag-and-grounding-on-vertex-ai)):

### Managed RAG (default answer for "fastest time-to-prod" / "no ML team")
**Stack:** Vertex AI Agent Builder + Vertex AI Search data store + Gemini with grounding.
- Point Vertex AI Search at GCS, BigQuery, websites, Drive, Cloud SQL, Spanner.
- Search handles parsing, chunking, embedding, indexing, ranking, citations.
- Agent / Gemini API calls grounding endpoint; response includes source attribution.
- Or use **Vertex AI RAG Engine** ([RAG Engine overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview), GA Dec 2024) for a pipeline you can configure but not build from scratch — it orchestrates ingestion → transform → embed → index → retrieve → generate, with pluggable vector stores (RagManagedDb default, Weaviate, Pinecone, Vertex AI Vector Search).

### DIY RAG (when you need control, custom embeddings, hybrid search, niche stores)
**Stack:** Vertex AI Vector Search + your own pipeline + Gemini.
- Generate embeddings with `text-embedding-004` / `text-multilingual-embedding-002`.
- Index in Vertex AI Vector Search (ScaNN-based ANN, formerly Matching Engine).
- Retrieve top-k, rerank with a cross-encoder, build prompt with citations.
- Optionally orchestrate with LangChain / LlamaIndex / Firebase GenKit.
- Use for billion-scale corpora, hybrid (sparse + dense) search, or when you need control over chunking strategy.

**Exam-style decision rule:** "Out-of-the-box, low-code, fast" → managed (Agent Builder + Search). "Billions of vectors, custom pipeline, or specialized domain ranking" → Vector Search + custom. Mid-ground "I want a pipeline I configure but not maintain" → RAG Engine.

---

## 9. Monitoring GenAI (§6)

GenAI monitoring is genuinely young. The exam expects you to combine **operational** monitoring (latency, error rate, throughput, cost) with **quality** monitoring (drift, hallucination, safety):

- **Model Observability Dashboard** — built-in, in the Vertex AI section of console. Surfaces QPS, token throughput, first-token latency, prediction error counts. Pulls only from API calls, not Studio interactions ([model-observability docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-observability), retrieved Apr 2026).
- **Cloud Monitoring + Cloud Logging + Cloud Trace** — for custom alerts on `prediction/online/error_count`, latency percentiles, and request traces.
- **Vertex AI Model Monitoring v2** — primary use is feature/data drift on tabular endpoints, but the same drift framework is used to track **prompt distribution drift** and **embedding drift** for GenAI ([model-monitoring overview](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview)).
- **Gen AI Evaluation Service on production logs** — sample real prompts/responses, run model-based metrics (factuality, groundedness, safety) over them as a continuous "eval-as-monitoring" loop.
- **Safety filters** — Gemini's built-in harm-category filters (HARM_CATEGORY_HARASSMENT, HATE_SPEECH, SEXUALLY_EXPLICIT, DANGEROUS_CONTENT) emit blocked-response counts you alert on.

**Hallucination is monitored, not eliminated:** the practical pattern is grounding (RAG) + groundedness metric on a sampled stream + human triage for low-score outputs.

---

## 10. Rename / restructure history (2023–2026)

| Date | Old name | New name | Source |
|---|---|---|---|
| Jun 2023 | (launch) | **Generative AI Studio** | [Wikipedia: Vertex AI](https://en.wikipedia.org/wiki/Vertex_AI) |
| Aug 29, 2023 | Vertex AI **Matching Engine** | Vertex AI **Vector Search** | [google-cloud-4-words issue](https://github.com/priyankavergadia/google-cloud-4-words/issues/102) |
| 2023 (rolling) | Generative AI Studio | **Vertex AI Studio** | [InfoWorld](https://www.infoworld.com/article/2336686/google-vertex-ai-studio-puts-the-promise-in-generative-ai.html) |
| 2023–2024 | **Gen App Builder** / **Discovery Engine** / **Vertex AI Search and Conversation** | **Vertex AI Agent Builder** | [TechCrunch Apr 9 2024](https://techcrunch.com/2024/04/09/with-vertex-ai-agent-builder-google-cloud-aims-to-simplify-agent-creation/) |
| Late 2024 → early 2025 | **Dialogflow CX** | **Conversational Agents** | [Dialogflow release notes](https://docs.cloud.google.com/dialogflow/docs/release-notes); [Zenn rename log](https://zenn.dev/soundtricker/articles/2ae25658eb41b2) |
| Late 2024 → early 2025 | Dialogflow CX **Messenger** / **Phone Gateway** | **Conversational Messenger** / **Conversational Phone Gateway** | (same) |
| Dec 2024 | Vertex AI **RAG Engine** | (GA — not a rename, milestone) | [Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes) |
| Mar 2025 | (launch) | **Vertex AI Agent Engine** (formerly *Reasoning Engine* / *LangChain on Vertex AI*) | [Zenn rename log](https://zenn.dev/soundtricker/articles/2ae25658eb41b2) |
| Apr 9, 2025 | **Vertex AI Agent Builder** product | renamed **AI Applications** (became a solution-group name); endpoints unchanged | [Vertex AI Search release notes](https://docs.cloud.google.com/generative-ai-app-builder/docs/release-notes) |
| Apr 2025 | (preview launch) | **Agent Development Kit (ADK)** + **Agent Garden** | [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/build-and-manage-multi-system-agents-with-vertex-ai) |
| Apr 22, 2026 | **Vertex AI** (umbrella) | **Gemini Enterprise Agent Platform** (Vertex AI is now "part of" it) | [Google Cloud Blog Apr 22 2026](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform); [HPCwire AIwire](https://www.hpcwire.com/aiwire/2026/04/23/google-unveils-gemini-enterprise-agent-platform/) |
| Apr 2026 | **Vertex AI Search** | renaming to **Agent Search** | [Vertex AI Search release notes](https://docs.cloud.google.com/generative-ai-app-builder/docs/release-notes) |
| Apr 2026 | **Vertex AI Studio** | rebranded **Agent Platform Studio** | [Google Skills 2026](https://www.skills.google/focuses/86502) |
| Apr 2026 | docs hostname | `cloud.google.com/...` → `docs.cloud.google.com/...` (301 redirects) | observed during research, Apr 2026 |

**Bottom line for exam day:** the exam guide and Cloud Skills Boost still use 2025-era names. If a question says "Vertex AI Agent Builder", it means the same thing as "Gemini Enterprise Agent Platform"; if it says "Vertex AI Studio", it means "Agent Platform Studio". Don't get thrown off by mid-document terminology drift.

---

## 11. Sample exam-style questions

```jsonl
{"id": 1, "mode": "single_choice", "question": "Your team needs to build a customer-support chatbot that answers questions strictly from 5,000 internal PDF policy documents stored in Cloud Storage. The team has no MLOps engineers and wants to ship in two weeks. Which approach minimizes infrastructure work while preserving citation/grounding?", "options": ["A. Fine-tune Gemini 2.5 Flash on the PDFs using supervised fine-tuning, then deploy to a custom endpoint.", "B. Use Vertex AI Agent Builder with a Vertex AI Search data store pointed at the GCS bucket, then call Gemini with grounding to Vertex AI Search.", "C. Build a custom RAG pipeline: chunk PDFs, embed with text-embedding-004, store in Vertex AI Vector Search, retrieve top-k, and prompt Gemini.", "D. Upload all 5,000 PDFs into a single Gemini prompt context window for each user query."], "answer": 1, "explanation": "The managed RAG pattern (Agent Builder + Vertex AI Search + Gemini grounding) handles parsing, chunking, embedding, indexing, ranking, and citations out of the box — the lowest-ops choice. SFT (A) bakes facts into weights and is wrong for facts that change; it does not provide citations. Vector Search (C) gives more control but requires a pipeline the team cannot maintain. Stuffing 5,000 PDFs in context (D) busts the window and is non-grounded.", "ml_topics": ["RAG", "grounding", "managed services"], "gcp_products": ["Vertex AI Agent Builder", "Vertex AI Search", "Gemini", "Cloud Storage"], "gcp_topics": ["GenAI §1.2", "managed RAG"]}
{"id": 2, "mode": "single_choice", "question": "You have 1,200 labeled (prompt, ideal-response) pairs in a domain where Gemini 2.5 Flash gives generally fluent but factually wrong outputs about your product taxonomy. Prompt engineering plateaued. Cost matters. Which Vertex AI tuning method should you try first?", "options": ["A. RLHF / preference tuning, because the outputs are subjectively wrong.", "B. Supervised fine-tuning of Gemini 2.5 Flash with LoRA-based PEFT.", "C. Distillation from Gemini 2.5 Pro to a smaller custom model.", "D. Full fine-tuning of all Gemini parameters."], "answer": 1, "explanation": "Supervised fine-tuning fits when you have hundreds-to-thousands of labeled (input, ideal-output) pairs and a well-defined task — exactly this scenario. On Vertex AI, Gemini SFT is implemented as LoRA-based PEFT under the hood, which is the cheap, default path. RLHF/preference tuning needs preference *pairs*, not labeled targets, and is for subjective/style alignment. Distillation is for size/latency reduction. Full FT of Gemini parameters is not exposed on Vertex AI.", "ml_topics": ["supervised fine-tuning", "PEFT", "LoRA", "RLHF"], "gcp_products": ["Vertex AI", "Gemini 2.5 Flash"], "gcp_topics": ["GenAI §3.2", "fine-tuning"]}
{"id": 3, "mode": "single_choice", "question": "You are migrating from Gemini 2.5 Flash to Gemini 2.5 Pro and need to certify the new model is at least as good on your 500-prompt regression suite before flipping traffic. Which Vertex AI feature is the best fit?", "options": ["A. Use BLEU and ROUGE alone — they are deterministic and do not need a judge.", "B. Use the Gen AI Evaluation Service in pairwise mode (or AutoSxS) with a judge model to compute a win-rate of Pro over Flash.", "C. Deploy both models to production with a 50/50 traffic split and watch latency dashboards.", "D. Run pointwise eval only against Gemini 2.5 Pro to confirm it scores above a threshold."], "answer": 1, "explanation": "Pairwise evaluation (Gen AI Evaluation Service pairwise metrics, or the AutoSxS pipeline) is purpose-built for head-to-head model comparisons during migration; it produces a win-rate per criterion. Computation-only metrics (A) miss factuality/groundedness. A traffic split (C) measures business impact, not output quality, and exposes users to a possibly-worse model. Pointwise on Pro alone (D) does not actually compare to Flash.", "ml_topics": ["evaluation", "pairwise vs pointwise", "model migration"], "gcp_products": ["Vertex AI Gen AI Evaluation Service", "AutoSxS"], "gcp_topics": ["GenAI §2.3"]}
{"id": 4, "mode": "single_choice", "question": "A retail team needs grounded answers about product specs (stable text) AND breaking news about today's promotional offers (changes hourly). Which grounding combination should you configure on Gemini in Vertex AI?", "options": ["A. Grounding with Vertex AI Search only, pointed at a GCS bucket of product specs.", "B. Grounding with Google Search only.", "C. Grounding with Vertex AI Search for product specs, combined with Grounding with Google Search for breaking offers.", "D. Disable grounding and increase the temperature to encourage creativity."], "answer": 2, "explanation": "Vertex AI supports combining Grounding with Vertex AI Search (your private docs) and Grounding with Google Search in the same request, which is the canonical pattern for 'private stable + public dynamic' data. (A) misses the dynamic data; (B) misses private specs; (D) is the opposite of what you want for factual answers.", "ml_topics": ["grounding", "RAG", "hybrid retrieval"], "gcp_products": ["Vertex AI Search", "Gemini", "Grounding"], "gcp_topics": ["GenAI §1.2"]}
{"id": 5, "mode": "single_choice", "question": "A Gemini-powered support agent has been live for 30 days. Customers report occasional 'made-up' policy details. Which monitoring approach catches this hallucination drift in production?", "options": ["A. Set a Cloud Monitoring alert on prediction latency p99.", "B. Sample production prompt/response pairs into the Gen AI Evaluation Service with model-based groundedness and factuality metrics, alert when scores drop.", "C. Rely on Gemini's built-in safety filters; hallucination is a safety category.", "D. Re-run AutoSxS weekly comparing the live model to itself."], "answer": 1, "explanation": "Hallucination is a *quality* problem, not an operational one. The production pattern is to sample real traffic, run the Gen AI Evaluation Service with model-based groundedness/factuality metrics on the samples, and alert when the rolling score drops — eval-as-monitoring. Latency alerts (A) miss content quality. Safety filters (C) catch harm categories (harassment, hate, etc.), not factual hallucination. AutoSxS against itself (D) returns ~50/50 by construction.", "ml_topics": ["monitoring", "hallucination", "drift", "eval-as-monitoring"], "gcp_products": ["Vertex AI Gen AI Evaluation Service", "Cloud Monitoring", "Gemini"], "gcp_topics": ["GenAI §6"]}
```

---

## 12. References

- Google Cloud, *Generative AI on Vertex AI overview*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/overview)
- Google Cloud, *Model Garden overview*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models)
- Google Cloud, *Model Garden product page*, [link](https://cloud.google.com/model-garden)
- Google Cloud, *Vertex AI Agent Builder / Gemini Enterprise Agent Platform product page*, [link](https://cloud.google.com/products/agent-builder)
- Google Cloud Blog, *Introducing Gemini Enterprise Agent Platform*, 2026-04-22, [link](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform)
- Google Cloud, *Agent Platform release notes (Generative AI on Vertex AI)*, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes)
- Google Cloud, *Vertex AI Search release notes (rename to Agent Search)*, [link](https://docs.cloud.google.com/generative-ai-app-builder/docs/release-notes)
- Google Cloud, *Vertex AI Studio capabilities*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/vertex-ai-studio-capabilities)
- Google Cloud, *Tune Gemini models — overview*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models)
- Google Cloud, *Tune Gemini models with supervised fine-tuning*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning)
- Google Cloud Blog, *Supervised Fine Tuning for Gemini LLM*, [link](https://cloud.google.com/blog/products/ai-machine-learning/supervised-fine-tuning-for-gemini-llm)
- Google Cloud Blog, *RAG vs. Fine-tuning and more*, [link](https://cloud.google.com/blog/products/ai-machine-learning/to-tune-or-not-to-tune-a-guide-to-leveraging-your-data-with-llms)
- Google Cloud, *Gen AI Evaluation Service overview*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview)
- Google Cloud, *AutoSxS pairwise evaluation pipeline*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/side-by-side-eval)
- Google Cloud Blog, *Evaluate AI models with Vertex AI & LLM Comparator*, [link](https://cloud.google.com/blog/products/ai-machine-learning/evaluate-ai-models-with-vertex-ai--llm-comparator)
- Google Cloud, *Grounding overview*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview)
- Google Cloud, *Grounding with Vertex AI Search*, last updated 2026-04-10, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-vertex-ai-search)
- Google Cloud, *Agent Platform RAG Engine overview*, last updated 2026-04-22, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview)
- Google Cloud Blog, *RAG and grounding on Vertex AI*, [link](https://cloud.google.com/blog/products/ai-machine-learning/rag-and-grounding-on-vertex-ai)
- Google Cloud, *Vector Search overview (formerly Matching Engine)*, [link](https://docs.cloud.google.com/vertex-ai/docs/vector-search/overview)
- Google Cloud, *Model Observability dashboard for GenAI*, retrieved 2026-04-24, [link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-observability)
- Google Cloud, *Vertex AI Model Monitoring v2 overview*, [link](https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview)
- Google Cloud, *Vertex AI Prompt Optimizer announcement*, [link](https://cloud.google.com/blog/products/ai-machine-learning/announcing-vertex-ai-prompt-optimizer)
- Google Cloud, *Agent Engine overview*, [link](https://docs.cloud.google.com/agent-builder/agent-engine/overview)
- Google ADK docs, [link](https://google.github.io/adk-docs)
- Google Cloud, *PMLE certification page*, [link](https://cloud.google.com/learn/certification/machine-learning-engineer)
- Google, *Professional Machine Learning Engineer Exam Guide (v3.1)* (PDF), [link](https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf)
- TechCrunch, *With Vertex AI Agent Builder, Google Cloud aims to simplify agent creation*, 2024-04-09, [link](https://techcrunch.com/2024/04/09/with-vertex-ai-agent-builder-google-cloud-aims-to-simplify-agent-creation/)
- HPCwire AIwire, *Google Unveils Gemini Enterprise Agent Platform*, 2026-04-23, [link](https://www.hpcwire.com/aiwire/2026/04/23/google-unveils-gemini-enterprise-agent-platform/)
- TheNextWeb, *Google Cloud Next 2026: AI agents, A2A protocol, Workspace Studio*, [link](https://thenextweb.com/news/google-cloud-next-ai-agents-agentic-era)
- Zenn (Soundtricker), *Vertex AI AI-Agent service rename history (chronological log)*, [link](https://zenn.dev/soundtricker/articles/2ae25658eb41b2)
- FlashGenius, *Google PMLE Certification: 2026 Guide*, [link](https://flashgenius.net/blog-article/google-professional-machine-learning-engineer-certification-2026-guide)
- InfoWorld, *Google Vertex AI Studio puts the promise in generative AI*, [link](https://www.infoworld.com/article/2336686/google-vertex-ai-studio-puts-the-promise-in-generative-ai.html)
- google-cloud-4-words GitHub issue #102, *Vertex AI Matching Engine renamed to Vector Search* (2023-08-29), [link](https://github.com/priyankavergadia/google-cloud-4-words/issues/102)

---

## 13. Confidence + decay risk

**Confidence (high):** Core mental model — Model Garden = catalog, Studio = prompt IDE, Agent Builder = managed-RAG/agent stack, Eval Service = pointwise+pairwise, AutoSxS = pairwise pipeline, Vector Search = ANN store, RAG Engine = managed RAG pipeline, Vertex AI Search = enterprise search. SFT-via-LoRA on Gemini 2.5 (Pro/Flash/Flash-Lite) with JSONL datasets. Managed-RAG vs DIY-RAG decision rule. Grounding combinations (Search + Vertex AI Search). Distinction between operational monitoring and quality monitoring (eval-as-monitoring).

**Confidence (medium):** Exact April 2025 launch date for the v3.1 exam variant — community sources and the Google certification page both reference October 2024 GenAI additions and an updated v3.1 guide live in 2025; treat the "April 2025" effective date in the prompt as authoritative. Distillation availability surface — confirmed for some model families, not uniformly across all Gemini variants.

**Confidence (low — high decay):** Anything tied to *current product names*. As of April 2026, Google has just rebranded the umbrella to **Gemini Enterprise Agent Platform**, *Vertex AI Studio* → *Agent Platform Studio*, *Vertex AI Search* → *Agent Search*. Expect more renames over the next 6 months. Specific Gemini model versions (3.1 Pro, 3 Flash, 2.5 family) will roll. Eval Service "adaptive rubrics" feature naming is recent (2025–2026) and still maturing.

**6-month decay flags:**
1. The "Vertex AI" brand will fade from console UI; exam-guide wording will lag by 6–12 months. Memorize *both* names for every product.
2. ADK + Agent Engine + Agent Garden will likely converge under Agent Platform Studio with new sub-product names.
3. Vertex AI RAG Engine vs Vertex AI Search will continue to overlap; expect consolidation.
4. AutoSxS may be folded entirely into the Gen AI Evaluation Service pairwise mode; the standalone pipeline page already nudges readers to "Define your metrics."
5. The doc hostname migration (`cloud.google.com` → `docs.cloud.google.com`) is rolling — old links will keep 301-ing for now; bookmark the new host.

**Study tactic:** When you read any GenAI question on the v3.1 exam, translate product names to their *function* first ("RAG store", "prompt IDE", "managed agent runtime"), choose the function, then map back to the name in the answer choices. Names will keep shifting; functions will not.
