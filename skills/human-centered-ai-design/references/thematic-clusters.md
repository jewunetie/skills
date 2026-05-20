# Thematic Clusters: SOTA Recommendations by Topic

This file consolidates post-2024 SOTA recommendations across 10 thematic clusters. The file is large; do not read it whole. Read this TOC first, then use `view_range` to load only the cluster relevant to the user's question.

## Table of contents

| Cluster | Topic | Approximate line range |
|---|---|---|
| 1 | Determining when (and when not) to use AI | 22 to 63 |
| 2 | Setting expectations and mental models | 64 to 108 |
| 3 | Explainability and transparency | 109 to 144 |
| 4 | Trust calibration and appropriate reliance | 145 to 190 |
| 5 | Feedback and user control | 191 to 222 |
| 6 | Errors, failure, and hallucination handling | 223 to 268 |
| 7 | Generative-AI-specific patterns | 269 to 313 |
| 8 | Agentic-AI patterns | 314 to 355 |
| 9 | Data practices and responsible AI foundations | 356 to 385 |
| 10 | Post-launch evaluation and continuous improvement | 386 to end |

Line ranges are approximate. If a range looks wrong because the file has been edited, use `grep -n "^## Cluster N"` to find the exact start line.

## Cluster 1: Determining when (and when not) to use AI

The earliest and least negotiable design decision is whether AI should be used at all. Every authoritative source treats this as a precondition for everything else.

### Core consensus recommendation

Start from a real user need, not a technological capability. Map the intersection of (a) genuine user problems where (b) AI offers unique value over heuristics, rules, or manual control. Avoid AI when:

- Predictability matters more than personalization
- Costly errors outweigh benefit gains
- Full transparency or determinism is required (regulated logic, open-source software)
- A static information form will do
- Users explicitly do not want a task automated

Source: Google PAIR, *User Needs + Defining Success* chapter.

### Augmentation vs automation framing

PAIR distinguishes tasks that should be **automated** (difficult, unpleasant, scale-driven, with consensus on the correct way) from tasks that should be **augmented** (tasks people enjoy, that carry social capital, or where there is no agreed-upon correct approach). CMU 05-318 frames the same distinction through Shneiderman and Maes' direct-manipulation-vs-interface-agents debate (1997) and Lee and Seppelt's levels-of-automation taxonomy. Stanford HAI (Landay) emphasizes "augment, not automate" as a core principle.

### Quality bar by feature type

Apple HIG (Generative AI section, Machine Learning section): Critical features need accuracy and reliability; complementary features can tolerate imperfect quality. Proactive AI features face a higher quality bar than reactive ones because users did not request them. People may have less tolerance for low-quality information from proactive features.

### Responsible-by-design framing

IBM Weisz et al. (CHI 2024), "Design Responsibly": Use a human-centered approach (design thinking, participatory methods); identify and resolve value tensions across stakeholders; expose or limit emergent behaviors deliberately; test and monitor for user harms (bias, toxicity, misinformation).

### The shift from model-centric to human-centric metrics

Stanford HAI (Amershi keynote, "AI in the Loop"): Shift the evaluation question from "what can these models do?" to "what can people do with these models?". Adopt human-centered metrics (interpretability, fairness, team utility, complementarity, performance explainability) rather than raw model accuracy.

### Post-2024 additions

PAIR's generative-AI updates explicitly add a "before-you-build" question for GenAI: would a deterministic rule-based or retrieval system serve users better than a generative one?

Microsoft "Fostering Appropriate Reliance" (Vorvoreanu et al. March 2025) extends this with task-suitability analysis. Novices and experts over-rely differently. Tasks differ in stakes, complexity, and verifiability. This should drive whether (and how heavily) GenAI is used at all, not just whether AI in general is appropriate.

### Tension flag

For a deeper look at the productivity-maximalist vs human-centered camps on agentic autonomy, see `tensions.md` (Tension 3). The "should I automate or augment" question becomes acute for agentic systems.

## Cluster 2: Setting expectations and mental models

Helping users form an accurate mental model is universally recognized as the single biggest leverage point for safe, effective AI use.

### Initial expectation-setting

Microsoft HAX Guidelines 1 and 2 (Amershi et al., CHI 2019, still current SOTA):

- G1: Make clear what the system can do.
- G2: Make clear how well the system can do it (communicate accuracy, error rates, limitations).

Google PAIR Mental Models chapter:

- Set realistic expectations early.
- Describe user benefits, not technology.
- Build on familiar mental models from existing products.
- Onboard in stages.
- Avoid "AI magic" marketing that creates over-expectation.

Apple HIG (Generative AI): Communicate where the app uses AI so people can make informed choices; explicitly communicate machine-learning limitations.

IBM Weisz et al. "Design for Mental Models" principle: Orient users to **generative variability** (the same input can yield different outputs each time). Teach effective use through tooltips, in-context explanations, and curated example galleries (DALL-E's example-and-prompt pairs are the canonical reference). Understand the user's existing mental model. Teach the AI about the user (ChatGPT's Custom Instructions).

### Onboarding patterns

PAIR pattern "Onboard in stages": Introduce features at the moment they become relevant, not in a long initial tutorial. Suggest a low-risk reversible action immediately so users can tinker.

PAIR pattern "Plan for co-learning": Frame the relationship as one in which users teach the system over time and the system adapts. This turns the first failure into an opportunity rather than a betrayal.

Microsoft Copilot UX: Use prompt starters and conversation starters in zero or empty states; show capability previews via curated cards.

Shape of AI and Smashing Magazine (Wroblewski and Sharma, 2025) catalog: Help users construct their first prompt; solve the blank canvas problem with prompt clues; share sample generations with their prompts and parameters.

### Mental models specific to generative AI (post-2024)

PAIR "Generative AI is reshaping mental models" (Pushkarna and Jeong, 2024): GenAI shifts the user's mental model from tool to collaborator or partner. Designers must promote this shift through language and characteristics, not just functionality.

Microsoft "Fostering Appropriate Reliance" (2025): Across studies, novice users assume GenAI summarization "is like a search engine that does not make mistakes." Users mistake fluent style for accuracy. Users treat LLM plugins as super-apps that will not confabulate. Recommendation: explicitly educate users that GenAI generates rather than retrieves; that summaries can be wrong in subtle ways; and that fluency is not a quality signal.

Nielsen Norman Group: GenAI introduces a third UI paradigm, "intent-based outcome specification", fundamentally different from command-based interaction. Mental models around iterative refinement, not point-and-click control, become central.

### Tension flag

PAIR (and Apple HIG broadly) leans toward promoting AI as a collaborator (controlled anthropomorphism). Microsoft's 2025 lessons-learned report and several CHI 2025 papers (Bo et al.; Tankelevitch et al.) show that anthropomorphic and fluent presentation correlates with overreliance and metacognitive laziness. The current SOTA position is **calibrated anthropomorphism**: adopt collaborative framing where it improves task framing, but pair it with explicit, repeated transparency about limits, especially for novice users. See `tensions.md` Tension 1 for full treatment.

## Cluster 3: Explainability and transparency

### Communicating AI's presence and provenance

Apple HIG (Generative AI), confirmed by Apple Developer Forums 2024 to 2025: Communicate where the app uses AI; provide clear attribution when content is AI-generated; flag AI suggestions visually (Apple uses subtle indicators such as sparkle icons or descriptive labels). For Apple Intelligence integration, designers must indicate AI involvement and explain how the AI arrived at its suggestion.

Microsoft Copilot Custom Engine Agents UX: AI labels are automatically added to all agent messages; citations are returned by the model and rendered with the Teams SDK. This is treated as a non-negotiable transparency baseline.

C2PA / Content Credentials (adopted by Google, Adobe, Microsoft, OpenAI, 2024 to 2025): Content provenance metadata embedded cryptographically so AI-generated content can be traced. The C2PA 2.1 specification (2024) and its expected ISO standardization (2025) are now the dominant interoperable approach for signaling AI-generated media at scale.

EU AI Act compliance signals (2025): Visible markings for deep-fake content and machine-readable provenance markings are now legal requirements, not optional design choices, for many providers.

### Explanations of why the AI produced a specific output

PAIR "Explain for understanding, not completeness": Do not try to explain everything. Explain the aspects that affect user trust and decision-making. Use partial explanations, progressive disclosure, and example-based rationales. Save detailed system explanations for marketing pages or onboarding, not the active flow.

Microsoft HAX Guideline 11: Make clear why the system did what it did.

IBM Weisz et al. "Calibrate trust using explanations" plus "Provide rationales for outputs": Show source materials and capabilities-and-limits up front (ChatGPT's intro screen as the canonical example).

CHI 2025 (Suh et al., HCXAI workshop): Devil's-advocate explanations (using LLMs to generate counter-explanations) can mitigate overreliance better than supporting explanations alone.

### Confidence and uncertainty communication

PAIR "How to show model confidence": Confidence displays help when interpretable but can confuse users; test multiple representations early. Use ordered lists, partial confidence cues, or progressive disclosure rather than raw probabilities when stakes are not high.

Kim et al. (FAccT 2024, replicated in 2025): First-person uncertainty expressions ("I am not sure, but...") increase user accuracy on a task but can also reduce confidence in the system and increase task time. Numeric confidence ("85% confident") is hard for non-experts to interpret.

Microsoft "Fostering Appropriate Reliance" (2025): Uncertainty expressions are a double-edged sword. The mere presence of citations can backfire by increasing trust without increasing verification. Test mitigations empirically because they regularly produce counter-intuitive effects.

MDPI review (December 2025) of 84 HAIC studies: Simple visual highlights are more effective at trust calibration than complex visualizations or interactive features.

### Tension flag

PAIR and IBM endorse showing model confidence as a trust-calibration tool. Microsoft's empirical 2024 to 2025 findings show that confidence cues, citations, and explanations can each *increase* overreliance unless carefully designed. SOTA reconciliation: treat any verification aid as a hypothesis to be A/B-tested, not a reliable mitigation. Apple HIG implicitly takes the more conservative position: keep AI suggestions as starting points users edit, rather than relying on confidence labels to guide reliance. See `tensions.md` Tension 2 for full treatment.

## Cluster 4: Trust calibration and appropriate reliance

This cluster has expanded dramatically post-2024 and is now arguably the most active area of human-AI interaction research.

### Core construct

Google PAIR (Explainability + Trust): "Help users calibrate their trust." The user should not trust the system completely. Explanations should help users know when to trust and when to apply judgment.

IBM (Design for Appropriate Trust and Reliance): Use friction to avoid overreliance; signify the role of AI explicitly ("your AI pair programmer"); provide rationales; calibrate via explanations.

Microsoft framing (Vorvoreanu et al., 2025): Appropriate reliance equals users accept correct AI outputs *and* reject incorrect ones. Both over-reliance and under-reliance reduce decision quality, often below the AI alone or human alone.

### The three Microsoft UX goals for appropriate reliance (post-2024 framework, March 2025)

1. **Create useful mental models.** Make the AI's capabilities and limitations realistic, not just present.
2. **Signal when to verify.** Make it easy to spot mistakes; draw attention when verification matters.
3. **Facilitate verification.** Reduce cognitive load when users do verify (link directly to the relevant snippet, not the whole document).

### Specific patterns

**Cognitive forcing functions** (Buçinca et al. 2021, replicated CHI 2024 to 2025): Force users to think before consuming the AI's answer (make their own first guess; confirm dialog; deliberate pause). Effective at reducing over-reliance especially when user trust is high. Caveat: friction can backfire by causing users to abandon AI advice entirely (under-reliance).

**Trust-adaptive interventions** (Srinivasan et al., IUI 2025; updated 2026 arXiv): Show supporting explanations during low-trust moments and counter-explanations during high-trust moments. Achieves up to 38% reduction in inappropriate reliance and 20% accuracy improvement. Forced pauses adaptively inserted at high-trust moments reduce over-reliance.

**Reliance disclaimer** (Bo et al., CHI 2025): Static disclaimers added enough friction in some tasks to dissuade habitual over-reliance, but performance varies by task. Implicit-answer interventions (where AI gives a hint instead of the answer) reduce over-reliance but may cause disproportionate under-reliance because of cognitive cost.

**Verification-focused explanations** (vs background explanations): Show *how* to check correctness, not just rationale. GPT-4V drawing the maze path so the user can verify the answer is the canonical example.

**PAIR "Use friction to avoid overreliance"**: Show multiple drafts so users compare; require explicit acceptance of suggestions.

**Microsoft Copilot agentic UI** (2025): The explicit "Conversation pane plus side-by-side panel" pattern preserves human authority by making the chat the canonical source of intent and control, with structured workspace alongside.

### What has not worked or has backfired

**Citations alone increase overreliance**: Microsoft's studies found that the mere presence and formatting of citations made users trust outputs more, even when the cited sources were fabricated.

**Explanations alone increase reliance**: Multiple studies (Microsoft 2025 synthesis; "The Amplifying Effect of Explainability in AI-assisted Decision-making in Groups" CHI 2025) show explanations increase trust in AI suggestions even when explanations are wrong.

**Source links at the document level burden users so much they skip verification**: "The amount of manual work it takes to verify is not fair." Facilitating verification means linking to the *exact passage*, not the whole document.

### Tension flag

The PAIR-vs-Microsoft tension on whether explanations and confidence calibrate or amplify trust is the central methodological debate in this area. Every overreliance mitigation must be empirically validated in your specific context. Defaults that look benign (citations, friendly disclaimers, confidence percentages) often produce the opposite of the intended effect. PAIR v2 patterns (2024) acknowledge this with explicit "test different displays early" guidance. See `tensions.md` Tension 2.

There is also a tension around cognitive forcing functions specifically: they reduce over-reliance but can drive under-reliance. See `tensions.md` Tension 4.

## Cluster 5: Feedback and user control

### The control-vs-automation balance

PAIR (Feedback + Control): Three principles:

- Align feedback with model improvement.
- Communicate value and time-to-impact.
- Balance control and automation. Be more proactive with automation when failure tolerance is high; be more conservative (more user control) when stakes are high or systems are new.

PAIR pattern "Allow users to test or turn off": Respect users' decision not to use a feature even after onboarding.

Microsoft HAX Guidelines 7 to 9 (Amershi et al. CHI 2019, still current): Support efficient invocation; support efficient dismissal; support efficient correction.

PAIR "Manual failsafe": Always provide a non-AI path to complete the task, especially in early adoption. The manual fallback is the default error-recovery surface.

### Feedback mechanisms

PAIR distinction between implicit and explicit feedback: Tell users what implicit feedback is collected; let users opt out; never collect implicitly without disclosure.

Microsoft Copilot Custom Engine Agents: Feedback loops are surfaced as built-in, low-friction, tiered (thumbs up or down, then optional reason, then optional free-text, then "report a problem").

dev.to and production-chat patterns (2024 to 2025): Tiered feedback collection; inline placement; low friction; live regions for streaming so users know what is happening.

### User agency in generative AI specifically

IBM "Design for Co-Creation": Help users craft effective outcome specifications; provide both generic input parameters (number of outputs, seed) and use-case-specific controls (style, tone, persona); support co-editing of generated outputs.

Apple HIG (Generative AI): User agency remains paramount. AI should augment human decision-making, not replace it. Always make AI output editable, regenerable, and rejectable. AI output is a starting point, not a finished product.

PAIR (generative AI updates): Co-evolution. Products and policies must evolve along with their extended communities of users. Integrate product design and AI development end-to-end rather than treating UX as a wrapper around the model.

## Cluster 6: Errors, failure, and hallucination handling

### Foundational error taxonomy (PAIR Errors + Graceful Failure)

Three error types: **user input errors**, **system or data errors**, and **context errors** (the system technically works but is unhelpful in this user's situation).

Three core principles: identify errors clearly; communicate the way forward; learn from errors via user feedback.

### Microsoft HAX Guidelines 7 to 11 (the "When wrong" cluster)

7. Support efficient invocation.
8. Support efficient dismissal.
9. Support efficient correction.
10. Scope services when in doubt (partial answers, abstention, narrow claims).
11. Make clear why the system did what it did.

### The HAX Playbook (NLP-specific failures)

Microsoft's interactive tool for proactively enumerating likely failure modes (transcription errors, false positives, dialect failures, ambiguity errors) for NLP systems before building. Used to plan recovery flows in early prototyping.

### Hallucination-specific patterns (post-2024)

NN/g "AI Hallucinations: What Designers Need to Know" (2024): Communicate uncertainty in language ("I am not completely sure, but..."); flag potentially low-confidence outputs visually; require user confirmation for high-stakes decisions.

Microsoft "Fostering Appropriate Reliance" (2025): Uncertainty expressions, cognitive forcing functions, AI critiques, and AI questioning are the four leading directions, each with empirically demonstrated trade-offs.

**RAG as a UX pattern, not just a backend technique**: Inline numbered citations, click-through to specific source passages, expandable source previews, and quality indicators on cited sources are now standard for any LLM-based product handling factual content (Graphlit guides 2024; eugeneyan.com "LLM Patterns"; Microsoft Copilot Studio's grounding requirement to refuse ungrounded responses by default).

**Two-step generation pattern** (Lakshmanan, "Generative AI Design Patterns" 2024): Separate factual data assembly (low-risk) from formatting and styling (creative). Reduces hallucination in customer-facing content.

**"Allow ungrounded responses" toggle** (Microsoft Copilot Studio): Default-off; turn on only when creative or non-factual answers are acceptable. Ungrounded responses are explicitly bracketed with stronger disclaimers.

**Self-check and verification patterns**: Multiple recent papers (CHI 2025; "Think Twice Before Trusting" / T3) propose generating multiple candidate answers and reflecting on inconsistencies; useful at the model level but also as a UX surface (showing draft variations to the user).

### Graceful degradation

PAIR pattern "Provide paths forward": When AI fails, fall back to non-AI mode; do not dead-end the user.

Microsoft Copilot guidance (2024): When confidence is low or sources are absent, refuse with an actionable, transparent explanation rather than a generic "I do not know."

Apple HIG: AI systems should gracefully handle uncertainty and provide clear paths forward when confidence is low.

### Tension flag

PAIR's older guidance (fail gracefully to non-AI options) is a fallback model. Newer agentic-system guidance (Google Cloud agentic patterns, Microsoft Copilot agents, 2025) emphasizes **escalation and human handoff** with full audit trails as the primary failure mode rather than silent fallback. The shift reflects the increased stakes of agentic actions: silent fallback may hide serious issues; explicit escalation forces accountability. See Cluster 8 for agentic specifics.

## Cluster 7: Generative-AI-specific patterns

This cluster covers patterns specific to LLM-powered products that did not exist or were peripheral in pre-2024 frameworks. For concrete pattern descriptions with "what it is, when to use, when it backfires", see `patterns.md`.

### The new interaction paradigm

Nielsen (NN/g, 2023, reinforced through 2025): Intent-based outcome specification is the third UI paradigm in 60 years. Users specify what, not how. Implications: control reverses; iterative refinement becomes core; new patterns for rounds of refinement become essential.

IBM Weisz et al. (CHI 2024) "Design for Generative Variability": Same input, different outputs. Patterns: leverage multiple outputs (show several options); visualize the user's journey; enable curation, annotation, favoriting, collections; draw attention to differences across outputs.

### Prompt-construction patterns (the articulation barrier)

Synthesis from Shape of AI, Smashing Magazine (Wroblewski and Sharma, 2025), NN/g 2024 to 2025, Microsoft Copilot UX docs:

- **Prompt starters and conversation starters**: predefined prompts in zero or empty state.
- **Prompt suggestions and example galleries**: curated examples with input plus output.
- **Reverse prompting**: derive a prompt from a desired output (Midjourney's Describe).
- **Style galleries and parametrization**: let users pick styles, tones, lengths via UI controls rather than text.
- **Targeted prompt rewrite or aided prompt understanding**: system shades or annotates prompt elements that may produce poor results.
- **Related and follow-up prompts**: Perplexity-style next-question suggestions.
- **Prompt builders and structured templates**: fillable forms that compose into a full prompt.
- **Custom instructions and persistent user context**: let users teach the AI about themselves persistently.

### Output-presentation patterns

- **Streaming responses**: buffer partial tokens, prevent layout thrash, expose stop and retry controls (dev.to, thefrontkit, Graphlit guides 2024 to 2025).
- **Inline numbered citations with expandable source previews**: now standard (Microsoft Copilot, ChatGPT Search, Bing Chat, Perplexity).
- **AI labels**: automatic visual badge on AI-generated messages (Microsoft Teams SDK, Apple's recommended sparkle icons, C2PA-based content credentials).
- **Multiple-draft, regenerate, and variation patterns**: Google Gemini draft-A-B-C, DALL-E grid, ChatGPT regenerate, Adobe Firefly variations.
- **Granular edit controls**: make-shorter, make-longer, change-tone, regenerate-this-paragraph; users keep agency over output.

### Conversational-goal management

OnGoal (UIST 2025): Visualize conversational goals across turns to reduce drift in multi-turn LLM interactions.

Microsoft Copilot guidance: Surface intermediate workflow steps in long-running tasks; preserve context across turns; collapse expanded workspaces back into a chat chiclet to maintain continuity.

### Cognitive-load and metacognition

Tankelevitch et al. (Microsoft, CHI 2024): Generative AI imposes new metacognitive demands. Users must now monitor their own prompting, evaluate outputs, and decide reliance. Designers should reduce metacognitive load via prompt scaffolds, visible intermediate steps, and verification aids.

Lee et al. (Microsoft, CHI 2025): GenAI reduces cognitive effort on the *generation* side but shifts effort to *verification and integration*. Knowledge workers' reported confidence in the AI doing a task negatively correlates with their critical-thinking enaction. Design implication: explicit critical-thinking prompts ("does this answer make sense given X?") help.

"Streaming, Fast and Slow" (UIST 2025): Adapt streaming speed to the cognitive load on the user. Slower for content needing review, faster for content being scanned.

## Cluster 8: Agentic-AI patterns

A new layer of patterns has emerged specifically for LLM-based agents that take actions, not just produce text.

### The four foundational agentic patterns (Andrew Ng, 2024; reused widely)

- **Reflection**: agent critiques and revises its own output before presenting.
- **Tool Use**: agent calls external functions, APIs, or code execution.
- **Planning**: agent decomposes a goal into a sequence of subtasks (Plan-and-Solve).
- **Multi-Agent Collaboration**: specialized agents coordinate via shared protocols.

### Human-in-the-loop (HITL) at runtime

Sources: Google Cloud Architecture Center 2025, StackAI, AgentWiki, Codebridge "5 Agentic AI Design Patterns CTOs Must Evaluate" 2026.

- **Approval checkpoints**: agent pauses before high-impact actions (financial, deletions, irreversible tool use).
- **Propose vs commit separation**: agent stores a structured action payload; reviewer approves; only then is the tool call executed with idempotency keys and post-action verification.
- **Review loops**: secondary supervisor agents or human reviewers evaluate outputs.
- **Asynchronous notification on long-running tasks**: agent works in the background and notifies on completion; users can keep chatting (Microsoft Copilot custom engine agents).

### Proactive pausing for ambiguity (UIST 2025)

Morae (Peng et al., UIST 2025): UI agents automatically detect decision points and pause to surface choices to the user. Users rated this significantly better than fully-automatic competitors (TaxyAI, Operator) on satisfaction with choices, awareness of choices, ease of choice-making, and confidence.

### Trace and oversight UIs

Microsoft Research "Overseeing Agents Without Constant Oversight" (2026): Action traces should be informative but not overwhelming. Design challenge is to surface the right decision-relevant detail without flooding the user. Found that an intermediate level of detail in action traces enabled better error finding than either minimal or full verbose traces.

Microsoft Copilot Studio agents (2025): Mandatory observability hooks recording rationale, tools invoked, and data used; rollback or compensation defined for downstream failures.

### Guardrails and policy gating

Microsoft Copilot Studio: Toxicity classifiers, jailbreak and prompt-injection filters, "allow ungrounded responses" toggle (off by default), citation enforcement, RAG-grounded answer requirement.

Apple Foundation Models framework (2024 to 2025): Safety guardrails enforced at framework level; safety taxonomy (12 primary categories, 51 subcategories); adversarial red-teaming combining automated and human approaches.

Risk-tiered autonomy (VentureBeat 2025; Codebridge 2026): "Suggest-only" then "propose-and-approve" then "execute-with-rollback" autonomy modes; choose mode based on stakes and reversibility.

### Tension flag

There is a real disagreement between the productivity-maximalist agentic camp (full automation of long workflows, minimal HITL) and the human-centered agentic camp (proactive pausing, propose-and-commit separation). CHI and UIST 2025 evidence (Morae; Microsoft Research traces work) leans strongly toward more frequent, not less, human checkpoints. Enterprise and VC literature acknowledges this but emphasizes that human dependency limits scalability. Current SOTA reconciliation: tier checkpoints by reversibility. Fully automate reversible cheap actions; propose-and-approve costly or irreversible actions; never silently execute high-stakes actions. See `tensions.md` Tension 3.

## Cluster 9: Data practices and responsible AI foundations

### Data transparency

PAIR (Data Collection + Evaluation chapter): Match user needs to data needs; build transparency about training data into user-facing explanations.

**Data Cards** (Pushkarna, Zaldivar, Kjartansson, FAccT 2022; still endorsed in PAIR v2): Structured, modular dataset documentation accessible to multiple stakeholders.

**Model Cards** (Mitchell et al., 2019; reused in IBM, Apple, AWS Service Cards 2024): Capabilities, limitations, performance breakdowns by demographic or condition.

**C2PA Content Credentials** (2024 to 2025): Cryptographic provenance for generated media.

### Bias and fairness

PAIR pattern "Embrace noisy data": Train on data resembling what users will actually produce, including blurry photos, abbreviations, emojis, accents.

Microsoft HAX Guideline 6: Mitigate social biases.

Apple safety taxonomy: Explicit categories for hate speech, discrimination, marginalization; updated continuously.

PatternFly AI: Fairness as one of five core principles (alongside accountability, explainability, transparency, human-centeredness).

### Privacy

PAIR (Feedback + Control): Always allow opt-out of implicit feedback and behavior logging; show users where their data is and how to change settings.

Apple Responsible AI principle "Protect privacy": On-device processing, federated learning, differential privacy, Private Cloud Compute architecture.

Microsoft Copilot: Tenant-scoped LLM instances; user prompts not used for training outside the tenant; permission inheritance from existing Microsoft 365 access controls.

## Cluster 10: Post-launch evaluation and continuous improvement

This cluster was not an explicit focus of pre-2024 frameworks (which focused on design-time guidance) but emerges as critical from post-2024 empirical research where mitigations frequently backfire and need iterative validation.

### Human-centered metrics (not just accuracy)

Stanford HAI (Amershi keynote): Shift from "what can the model do?" to "what can people do well with this model?". Metrics include:

- **Interpretability** (do users understand the output?)
- **Team utility and complementarity** (does the human-AI team outperform either alone?)
- **Performance explainability** (can users predict when AI will succeed or fail?)
- **Appropriate reliance** (do users accept correct outputs and reject incorrect ones?)
- **Decision quality** (not just speed)

PAIR "Define success metrics that include reward function tuning": Success metrics for AI features should map to user value, not just model accuracy.

### Feedback-loop instrumentation

PAIR (Feedback + Control): Align feedback collection with model improvement. Tier feedback (thumbs up or down, then optional reason, then optional free-text). Live regions for streaming responses so users know progress.

Microsoft Copilot Custom Engine Agents: Built-in tiered feedback surface; report-a-problem path for severe issues; continuous instrumentation of user corrections and dismissals as implicit feedback signals.

### Red-teaming and adversarial evaluation

Apple Foundation Models framework: Adversarial red-teaming combining automated and human approaches. Safety taxonomy with 12 primary categories and 51 subcategories drives systematic testing.

Microsoft Responsible AI Standard: Required impact assessment, fit-for-purpose review, fairness-and-inclusiveness testing across demographic slices.

IBM (Design Responsibly): Test and monitor for user harms (bias, toxicity, misinformation) on an ongoing basis, not just at launch.

### Monitoring for overreliance and drift

Microsoft "Fostering Appropriate Reliance" (March 2025): Overreliance is detectable via behavioral signals (skipped verifications, accepted-without-edit rates, low feedback engagement). Underreliance is detectable via abandoned suggestions and low feature engagement. Both metrics should be monitored continuously.

Lee et al. (CHI 2025): Critical-thinking enaction inversely correlated with reported AI confidence. Implication: track whether users still exercise judgment over time, not just whether they accept outputs.

### A/B testing trust-calibration interventions

Microsoft Aether and FAccT 2024 to 2025 findings: Citations, confidence cues, disclaimers, and explanations frequently produce counter-intuitive effects. Every trust-calibration intervention must be A/B-tested in the actual deployment context, not assumed to work based on the literature. The literature itself is divided (see `tensions.md`).

### Evaluating with the right comparison baselines

Stanford HAI: Evaluate human-AI team performance against (a) human alone, (b) AI alone, (c) human plus alternative tool, not just against AI baseline. Otherwise improvements may be illusory.

PAIR "Plan for co-evolution": Products and policies must evolve along with their extended communities of users. Treat the launched product as a starting point for ongoing user research, not a finished design.

### What is genuinely new post-2024 in this cluster

- Recognition that mitigations backfire and need empirical validation in context.
- Behavioral monitoring of overreliance and underreliance as routine product metrics.
- Structured red-teaming taxonomies (Apple's 12-and-51 framework) as design-cycle artifacts.
- Critical-thinking and metacognitive engagement metrics (Tankelevitch, Lee) as new product KPIs.
- Risk-tiered evaluation cadence: high-stakes interventions get continuous monitoring; low-stakes get periodic spot-checks.
