# Active Tensions in Human-Centered AI Design (Post-2024)

This file covers the four active disagreements in the post-2024 literature. Use it when the user's question touches one of these topics. Present both sides; do not pick one. Offer a decision heuristic at the end of each tension.

The general meta-heuristic across all four tensions: **tier by stakes, test empirically**. Mitigations that look benign in the literature frequently backfire in deployment. Validate in your specific context.

## Index

1. Anthropomorphic vs tool-like framing
2. Confidence cues, explanations, and citations as trust calibrators vs as overreliance amplifiers
3. Speed of agentic autonomy (productivity-maximalist vs human-centered camps)
4. Cognitive forcing functions as overreliance mitigators vs as friction that drives underreliance

## Tension 1: Anthropomorphic vs tool-like framing

Should AI systems be presented as collaborators, partners, or assistants (anthropomorphic framing) or as tools that users wield (tool-like framing)?

### Camp A: Anthropomorphic framing aids learning and engagement

**Position.** Promoting AI as a collaborator helps users form productive mental models. Users have rich existing models of human collaboration that they can transfer. Conversational framing reduces the articulation barrier (users know how to ask another person a question; they may not know how to write a prompt).

**Sources.**

- Google PAIR (Pushkarna and Jeong, 2024): "Generative AI is reshaping our mental models of how products work." Explicitly recommends shifting the user's mental model from tool to collaborator.
- IBM Weisz et al. (CHI 2024): "Signify the role of AI explicitly" with phrases like "your AI pair programmer." Anthropomorphic framing is seen as helpful for trust calibration.
- Apple HIG (Generative AI): Treats AI as a feature that augments user agency, with conversational and assistant-like framing supported throughout Apple Intelligence.

### Camp B: Anthropomorphic framing exacerbates overreliance and emotional dependence

**Position.** Fluent and conversational presentation correlates with overreliance. Users mistake fluency for accuracy. Anthropomorphic framing encourages users to treat the system as having judgment, intent, and reliability that it does not have. Critical-thinking enaction drops.

**Sources.**

- Microsoft "Fostering Appropriate Reliance on GenAI" (Vorvoreanu et al., March 2025): Across studies, novice users treat fluent LLM outputs as if they were authoritative search results. Recommends explicit, repeated transparency about limits.
- Tankelevitch et al. (CHI 2024): Generative AI imposes new metacognitive demands that anthropomorphic framing can mask.
- Lee et al. (CHI 2025): "The impact of generative AI on critical thinking." Reported confidence in the AI doing a task negatively correlates with users' critical-thinking enaction.
- Bo et al. (CHI 2025): Anthropomorphic and fluent presentation correlates with reduced verification.

### Decision heuristic

**Calibrated anthropomorphism.** Use collaborative framing where it improves task framing (lowering articulation barrier, supporting iterative refinement) but pair it with explicit, repeated transparency about limits, especially for novice users. Practical implementation:

- Use assistant or partner language in onboarding and conversational surfaces.
- Pair every assistant phrase with a structural reminder of limits ("AI-generated, verify before sending").
- Calibrate by user expertise: novices need more frequent transparency reminders; experts need less.
- Stress-test in user research: do users in your study cohort develop unrealistic confidence? If yes, dial down the anthropomorphism.

**Worked example.** A legal AI assistant uses "your AI co-counsel" framing during onboarding, but every output ends with "AI-generated; this is not legal advice; verify against primary sources." The chat surface uses neutral typography (no avatar, no first-person voice) for outputs, while the onboarding uses warmer collaborator language.

## Tension 2: Confidence cues, explanations, and citations as trust calibrators vs as overreliance amplifiers

Should designers add explanations, confidence indicators, and citations to AI outputs to help users calibrate trust?

### Camp A: Yes, these aids calibrate trust

**Position.** Users need information to decide when to trust AI. Explanations reveal reasoning. Confidence cues reveal uncertainty. Citations reveal sources. Without these, users have no basis for calibration.

**Sources.**

- Google PAIR (Explainability + Trust chapter): "Help users calibrate their trust." Explanations should help users know when to trust and when to apply judgment. PAIR provides specific guidance for showing model confidence and source attribution.
- IBM Weisz et al. (CHI 2024): "Calibrate trust using explanations" and "Provide rationales for outputs." ChatGPT's intro screen showing capabilities and limitations is the canonical example.
- Microsoft HAX Guideline 11: "Make clear why the system did what it did."

### Camp B: These aids increase overreliance, not calibration

**Position.** Empirical evidence post-2024 shows that explanations, confidence cues, and citations frequently increase user trust *regardless of accuracy*. The mere presence of an aid signals "I have done my homework" and reduces verification behavior. Worse than no aid because they create false confidence.

**Sources.**

- Microsoft "Fostering Appropriate Reliance" (March 2025): The mere presence and formatting of citations made users trust outputs more, even when the cited sources were fabricated. Uncertainty expressions are "a double-edged sword."
- "The Amplifying Effect of Explainability in AI-assisted Decision-making in Groups" (CHI 2025): Explanations increase trust in AI suggestions even when explanations are wrong.
- Kim et al. (FAccT 2024, replicated 2025): First-person uncertainty expressions increase user accuracy on a task but reduce confidence and increase task time. Numeric confidence is hard for non-experts to interpret.
- MDPI review (December 2025) of 84 HAIC studies: Simple visual highlights are more effective than complex visualizations or interactive features.

### Decision heuristic

**Treat verification aids as testable hypotheses, not defaults.** Specifically:

1. Do not deploy citations, confidence cues, or explanations without an empirical evaluation in your context.
2. Prefer **verification-focused** aids (showing how to check) over **persuasion-focused** aids (showing why to trust).
3. Link citations to the *exact passage*, not the document, so verification is feasible.
4. Use simple visual highlights rather than numeric percentages for confidence.
5. Monitor behavioral signals of overreliance (skipped verifications, accept-without-edit rates) post-launch.
6. Consider counter-explanations (Suh et al. CHI 2025) alongside supporting explanations.

**Worked example.** Instead of showing "85% confident" alongside an answer, highlight the specific span the model is uncertain about, and link the citation directly to the paragraph in the source document where the claim originates. A/B test against a no-aid baseline; measure not just task speed but verification rate (do users actually click the citation?) and accuracy of accepted answers.

## Tension 3: Speed of agentic autonomy

How autonomous should AI agents be allowed to act?

### Camp A: Productivity-maximalist (full automation, minimal HITL)

**Position.** Agents should automate full workflows end-to-end. Human-in-the-loop is a scalability bottleneck. Most actions can be reversed or compensated post-hoc. Friction degrades productivity gains. Industry analyst forecasts and enterprise deployment trends point to substantial growth in agentic AI adoption over the next several years.

**Sources.**

- VentureBeat 2025 ("Designing the agentic AI enterprise"): Emphasizes that human dependency limits scalability.
- Codebridge 2026 ("5 Agentic AI Design Patterns CTOs Must Evaluate"): Recommends "execute-with-rollback" as the default tier for many enterprise use cases.
- Industry deployment patterns from Microsoft Copilot agents (2025) and Google Cloud Agentic AI: support for fully autonomous workflows with audit trails.

### Camp B: Human-centered (frequent oversight, propose-and-commit)

**Position.** Agentic actions have higher stakes and lower reversibility than text generation. Silent automation hides errors. Users need to retain meaningful control over consequential actions. CHI and UIST 2025 evidence consistently shows users prefer more oversight than purely-automated competitors offer.

**Sources.**

- Peng et al. "Morae" (UIST 2025): UI agents that proactively pause for ambiguity are rated significantly higher by users on satisfaction with choices, awareness of choices, ease of choice-making, and confidence than fully-automatic competitors (TaxyAI, Operator).
- Microsoft Research "Overseeing Agents Without Constant Oversight" (2026): Action traces at intermediate detail levels enabled better error finding than minimal or verbose traces.
- Google Cloud Architecture Center 2025: Recommends propose-and-commit separation for high-impact actions.

### Decision heuristic

**Tier by reversibility, not by user preference.** Specifically:

1. **Fully automate** reversible cheap actions (formatting, drafting that the user reviews before sending, idempotent reads).
2. **Propose-and-approve** costly or moderately reversible actions (sending external messages, financial actions under threshold, modifying shared documents).
3. **Never silently execute** high-stakes actions (financial above threshold, deletions, irreversible external commitments).
4. The autonomy tier should be **visible and switchable** per task, not a global setting.
5. Use **proactive pausing** (Morae pattern) for ambiguous decision points within otherwise-autonomous workflows.

**Worked example.** An email assistant agent operates in three modes. For drafting replies, it auto-generates and shows the draft (full automation, but the send action is gated). For scheduling meetings with new external contacts, it proposes the meeting time and recipient list and waits for confirmation. For irreversible actions like archiving entire folders or replying-all to large distribution lists, it always requires explicit approval with an undo window. (One illustrative design choice in this example: the user can switch a task into a stricter tier but not into a looser one. This is not a finding from the literature; it is a sensible default to discuss with stakeholders.)

## Tension 4: Cognitive forcing functions as overreliance mitigators vs as friction that drives underreliance

Should designers add friction to make users think before consuming AI output?

### Camp A: Friction reduces overreliance

**Position.** When users have access to AI output, they often accept it without verification. Forcing the user to make their own first guess, or pause before consuming the answer, breaks this pattern. Empirically demonstrated to reduce over-reliance, especially when user trust is high.

**Sources.**

- Buçinca et al. (2021): Foundational work on cognitive forcing functions. Users who made their own guess first relied less on miscalibrated AI advice.
- Replications in CHI 2024 to 2025: Effect persists across multiple task types.
- IBM Weisz et al. (CHI 2024): Endorses friction as a design lever for appropriate reliance.

### Camp B: Friction drives underreliance and abandonment

**Position.** Users abandon AI features that require too much cognitive overhead. Friction can drive users to skip the AI advice entirely (the worst outcome: lower performance than either the AI or the human alone). Static, repeated friction also tends to lose effectiveness as users adapt to it.

**Sources.**

- Bo et al. "To Rely or Not to Rely" (CHI 2025): Implicit-answer interventions reduce over-reliance but cause disproportionate under-reliance because of cognitive cost. Static disclaimers added enough friction in some tasks but variable performance.
- Microsoft "Fostering Appropriate Reliance" (2025): Cognitive forcing functions are one of four leading directions but each has demonstrated trade-offs.

### Decision heuristic

**Use trust-adaptive friction, not blanket friction.** Specifically:

1. Reserve friction for **high-trust moments** (when users are most likely to over-rely). Trust-adaptive interventions (Srinivasan et al. IUI 2025) use forced pauses adaptively at high-trust moments and supporting explanations at low-trust moments.
2. Tier friction by **stakes**: low-stakes outputs get no friction; high-stakes get explicit forcing.
3. Make friction **task-relevant**: instead of generic "are you sure?" dialogs, ask domain-specific verification questions ("does this answer make sense given X?").
4. **Test for abandonment**: monitor whether friction increases or decreases overall feature engagement. If users abandon the feature entirely, the friction is too much.
5. **Counter-explanations** can substitute for friction: instead of forcing pauses, surface plausible counter-arguments alongside the answer.

**Worked example.** A medical decision-support tool detects high-risk diagnoses and inserts a domain-specific verification prompt: "Before accepting this differential, consider the following counter-evidence from the patient's history." Lower-risk diagnoses skip the prompt. The intervention is paired with logging of acceptance rates, edit rates, and override rates so the team can detect both over-reliance and under-reliance signals over time.

## How to use this file in conversation

When a user asks a question that hits one of these tensions:

1. State the tension explicitly: "This is one of the four active disagreements in the post-2024 literature."
2. Summarize Camp A and Camp B briefly (one or two sentences each).
3. Cite at least one specific source from each camp.
4. Offer the decision heuristic.
5. Where possible, offer a worked example calibrated to the user's apparent context.

Do not pretend the field has reached consensus where it has not. The tensions themselves are useful information for the user.
