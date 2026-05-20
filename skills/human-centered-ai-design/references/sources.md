# Source Attribution Map

Quick lookup for "what does framework X say about topic Y?". Use this when the user asks about a specific framework or wants to cite a particular source. For full content, see `thematic-clusters.md`.

## Tier 1: Foundational frameworks (universally endorsed)

### Google PAIR (People + AI Research) Guidebook

**URL.** pair.withgoogle.com/guidebook

**Original chapters (still current).**

1. User Needs + Defining Success
2. Data Collection + Evaluation
3. Mental Models
4. Explainability + Trust
5. Feedback + Control
6. Errors + Graceful Failure

**Post-2024 additions.**

- Guidebook v2 reorganization (2024) into eight task-oriented question clusters.
- Generative AI updates following 2024 Google I/O launch.
- Pushkarna and Jeong 2024 "Generative AI is reshaping our mental models."

**Strengths.** Best general-purpose starting framework; product-team friendly; pattern catalog is concrete.

**Coverage gaps relative to other sources.** Light on agentic AI; treats explanations and confidence cues optimistically (see Tension 2 in `tensions.md`).

### Microsoft HAX Toolkit and Guidelines for Human-AI Interaction

**Foundational paper.** Amershi et al., "Guidelines for Human-AI Interaction", CHI 2019. The 18 guidelines remain SOTA in 2026.

**The 18 guidelines, organized by phase.**

- Initially: G1 (make clear what the system can do), G2 (make clear how well).
- During interaction: G3 (time services based on context), G4 (show contextually relevant information), G5 (match relevant social norms), G6 (mitigate social biases).
- When wrong: G7 (support efficient invocation), G8 (support efficient dismissal), G9 (support efficient correction), G10 (scope services when in doubt), G11 (make clear why the system did what it did).
- Over time: G12 (remember recent interactions), G13 (learn from user behavior), G14 (update and adapt cautiously), G15 (encourage granular feedback), G16 (convey consequences of user actions), G17 (provide global controls), G18 (notify users about changes).

**Toolkit components.**

- HAX Workbook (planning).
- HAX Design Library (concrete patterns).
- HAX Design Patterns.
- HAX Playbook (NLP-failure-mode enumeration).

**Post-2024 extensions.**

- "Fostering Appropriate Reliance on GenAI: Lessons learned from early research" (Vorvoreanu, Passi, Dhanorkar, Heger, Walker, March 2025).
- "Appropriate Reliance on Generative AI: Research Synthesis" (2024).
- "Overreliance Risk Identification and Mitigation Framework" (aka.ms/overreliance-framework, 2025).
- "Addressing Overreliance on AI" (Springer Handbook of Human-Centered AI, 2025).

**Strengths.** Strongest empirical grounding; most rigorous on overreliance; HAX Playbook is the best proactive failure-enumeration tool.

**Coverage gaps.** The 18 guidelines are pre-generative-AI; post-2024 extensions are layered on top rather than integrated.

### Apple Human Interface Guidelines (HIG)

**URLs.** developer.apple.com/design/human-interface-guidelines (Generative AI section, Machine Learning section).

**Generative AI section (introduced 2024 with Apple Intelligence, refined WWDC 2025).**

- Communicate where the app uses AI.
- Provide clear attribution when content is AI-generated.
- Flag AI suggestions visually (sparkle icons, descriptive labels).
- Make AI output editable, regenerable, rejectable.
- Higher quality bar for proactive features.

**Four Responsible AI principles.**

1. Empower users with intelligent tools.
2. Represent our users.
3. Design with care.
4. Protect privacy.

**Strengths.** Concrete UI guidance; tight integration with platform conventions; strong privacy framing.

**Coverage gaps.** Apple-platform-specific in many recommendations; less rigorous on overreliance research.

### IBM Design Principles for Generative AI Applications

**Foundational paper.** Weisz et al., "Design Principles for Generative AI Applications", CHI 2024 (best-paper-track).

**The six principles.**

1. Design Responsibly.
2. Design for Mental Models.
3. Design for Appropriate Trust and Reliance.
4. Design for Generative Variability.
5. Design for Co-Creation.
6. Design for Imperfection.

**Follow-on work.** Cognitive forcing functions in CHIWORK 2025; overreliance studies.

**Strengths.** Most generative-AI-native of the foundational frameworks; good on variability and co-creation; concrete patterns.

**Coverage gaps.** Less developed on agentic AI specifically; treats trust-calibration aids more optimistically than Microsoft empirical work.

## Tier 2: Academic curricula

### Stanford CS 247A: Design for Artificial Intelligence

**Instructor.** Julie Stanford.

**Format.** Project-based studio; cross-listed as SYMSYS 195A; builds on CS 147 (Intro to HCI Design).

**Focus.** Design for human-centered AI experiences. Constraints, opportunities, and specialized processes for making AI systems work for the humans involved.

**Use as a source.** Course-level synthesis of HCI methods applied to AI; canonical example of design-thinking for AI products.

### Stanford CS 147: Intro to HCI Design

**Instructor.** James Landay.

**Coverage.** User-centered design, rapid prototyping, comparative evaluation, heuristic evaluation. Foundational design-thinking prerequisite for 247A.

### CMU 05-318 / 05-618: Human-AI Interaction

**Recent instructors.** Haiyi Zhu, Motahhare Eslami (Spring 2026); previously Hong Shen, Ken Holstein, Jeffrey Bigham, Steven Wu, Chinmay Kulkarni.

**Spring 2026 syllabus topics.** Agency and initiative; AI ethics; bias and transparency; confidence and errors; human augmentation and amplification; trust and explainability; mixed-initiative systems; programming by example.

**Key readings on syllabus.**

- Shneiderman and Maes (1997): direct manipulation vs interface agents debate.
- Vagia et al. (2016): levels of automation.
- Lee and Seppelt (2009): trust in automation.
- Yang et al. (2019): "Unremarkable AI."
- Kawakami et al. (2022): on AI in expert workflows.

### Stanford HAI (Human-Centered AI Institute)

**Position.** Three things jointly necessary: a design process accounting for community and society; responsible technical development; policy alignment. Human-centered AI is sociotechnical, not just UX.

**Key voices.** James Landay, Fei-Fei Li, John Etchemendy. Saleema Amershi (Microsoft Research) has presented at Stanford HAI's "AI in the Loop" conference; her keynote is widely cited in this space.

**Notable framing.** Amershi keynote: shift from "what can these models do?" to "what can people do well with these models?". Adopt human-centered metrics (interpretability, fairness, team utility, complementarity, performance explainability) rather than raw model accuracy.

## Tier 3: Recent academic and industry research (post-2024)

### Microsoft Research / Aether

**Key publications.**

- Vorvoreanu, Passi, Dhanorkar, Heger, Walker, "Fostering appropriate reliance on GenAI: Lessons learned from early research" (March 2025). The three UX goals for appropriate reliance: useful mental models, signal when to verify, facilitate verification.
- "Appropriate Reliance on Generative AI: Research Synthesis" (2024).
- Tankelevitch et al. "The Metacognitive Demands and Opportunities of Generative AI" (CHI 2024).
- Lee et al. "The Impact of Generative AI on Critical Thinking" (CHI 2025).
- "Overseeing Agents Without Constant Oversight" (Microsoft Research 2026).

### CHI 2024, CHI 2025, CHI 2026

**Notable papers.**

- Bo et al. "To Rely or Not to Rely? Evaluating Interventions for Appropriate Reliance on LLMs" (CHI 2025).
- Kim et al. "I'm Not Sure, But..." on uncertainty expression (FAccT 2024, replicated 2025).
- Suh et al. on devil's-advocate explanations (CHI 2025 HCXAI workshop).
- "The Amplifying Effect of Explainability in AI-assisted Decision-making in Groups" (CHI 2025).
- Sharma et al. on echo-chamber effects of LLM search.

### UIST 2024 to 2025

**Notable papers.**

- Peng et al. "Morae: Proactively Pausing UI Agents for User Choices" (UIST 2025).
- "Streaming, Fast and Slow: Cognitive Load-Aware Streaming for Efficient LLM Serving" (UIST 2025).
- OnGoal: visualizing conversational goals across turns.
- Numan et al. "SpaceBlender", Rajaram et al. "BlendScape", Antar et al. "VIME".

### Srinivasan et al. (IUI 2025; updated 2026 arXiv)

"Adjust for Trust: Mitigating Trust-Induced Inappropriate Reliance on AI Assistance." Trust-adaptive interventions: supporting explanations during low-trust moments, counter-explanations during high-trust moments, forced pauses adaptively inserted at high-trust moments. Up to 38% reduction in inappropriate reliance, 20% accuracy improvement.

## Tier 4: Industry pattern catalogs

### Shape of AI

**URL.** shapeof.ai

**What it is.** A catalog of UX patterns for AI design. Pattern format: name, description, examples, considerations.

### Smashing Magazine "Design Patterns for AI Interfaces"

**Authors.** Wroblewski, Sharma 2025.

**What it is.** Industry-targeted essay covering chat patterns, prompt patterns, citation patterns.

### Nielsen Norman Group (Jakob Nielsen)

**Notable pieces.**

- "AI: First New UI Paradigm in 60 Years" (intent-based outcome specification).
- "AI Hallucinations: What Designers Need to Know" (2024).
- "Aided Prompt Understanding."
- "Prompt Augmentation: UX Design Patterns for Better AI Prompting."
- "Intent by Discovery: Designing the AI User Experience."

### Andrew Ng's four agentic patterns (2024)

Reflection, Tool Use, Planning, Multi-Agent Collaboration. Widely cited as the foundational decomposition of agentic patterns.

### Lakshmanan, "Generative AI Design Patterns" (2024 book)

GitHub catalog at github.com/lakshmanok/generative-ai-design-patterns. Concrete patterns including the two-step generation pattern.

### Red Hat PatternFly AI

**Five core principles.** Accountability, explainability, transparency, fairness, human-centeredness.

## Tier 5: Standards and infrastructure

### C2PA (Coalition for Content Provenance and Authenticity)

**Key milestone.** C2PA 2.1 specification (2024). ISO standardization expected 2025.

**Adopters.** Google, Adobe, Microsoft, OpenAI joint adoption 2024 to 2025.

**What it provides.** Cryptographically signed provenance metadata for generated content.

### EU AI Act (2025 enforcement)

**Relevant provisions for design.** Visible markings for deep-fake content; machine-readable provenance markings for AI-generated media. Now legal requirements for many providers, not optional design choices.

### Model Cards and Data Cards

**Model Cards.** Mitchell et al. (2019). Capabilities, limitations, performance breakdowns by demographic or condition. Reused in IBM, Apple, AWS Service Cards 2024.

**Data Cards.** Pushkarna, Zaldivar, Kjartansson (FAccT 2022). Structured, modular dataset documentation accessible to multiple stakeholders. Endorsed in PAIR v2.

## How to attribute claims in your responses

When the user asks something that has source backing in this skill, attribute the claim inline:

- Specific guidelines: "Microsoft HAX Guideline 11" or "PAIR Mental Models chapter."
- Authored research: "Vorvoreanu et al. 2025" or "Weisz et al. CHI 2024."
- Apple HIG: "Apple HIG (Generative AI)."
- Newer industry frameworks: "Shape of AI catalog" or "Smashing Magazine 2025."

Do not invent citations. If you cannot trace a claim to a specific source in this file or in `thematic-clusters.md`, either find the source via search or omit the citation.
