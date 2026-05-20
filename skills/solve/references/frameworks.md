# Framework Reference

Detailed descriptions of each problem-solving framework available to the structured problem solver. Load this file when you need deeper context on how to apply a specific framework.

## Table of Contents

1. [MECE Structuring](#mece-structuring)
2. [Issue Trees and Logic Trees](#issue-trees-and-logic-trees)
3. [Hypothesis-Driven Problem Solving](#hypothesis-driven-problem-solving)
4. [Pareto Analysis (80/20 Rule)](#pareto-analysis-8020-rule)
5. [5 Whys (Root Cause Analysis)](#5-whys-root-cause-analysis)
6. [Fishbone (Ishikawa) Diagrams](#fishbone-ishikawa-diagrams)
7. [Effort/Impact Matrix](#effortimpact-matrix)
8. [Eisenhower Matrix](#eisenhower-matrix)
9. [First-Principles Thinking](#first-principles-thinking)
10. [The Pyramid Principle (Minto)](#the-pyramid-principle-minto)
11. [Decision Matrix (Weighted Scoring)](#decision-matrix-weighted-scoring)
12. [Pre-Mortem Analysis](#pre-mortem-analysis)

---

## MECE Structuring

**Mutually Exclusive, Collectively Exhaustive.** A grouping principle where every item belongs to exactly one category (no overlaps) and all categories together cover 100% of the problem space (no gaps). Created by Barbara Minto at McKinsey. MECE is the foundational discipline underlying all structured decomposition.

### Five strategies for creating MECE breakdowns

1. **Mathematical formulas.** Profit = Revenue - Cost. Each side is inherently distinct and together they fully define profit.
2. **Binary splits.** Internal vs. External. Quantitative vs. Qualitative. Before vs. After. Automatically ME and CE.
3. **Process steps.** Sourcing -> Manufacturing -> Distribution -> Retail. Each step is distinct; all steps cover the whole chain.
4. **Defined segments.** Geographic regions, age brackets, product lines -- where categories are explicitly defined to prevent overlap.
5. **Catch-all buckets.** Add "Other" when categories might miss edge cases, guaranteeing collective exhaustiveness.

### When to use

At the start of nearly every structured analysis. Any time you decompose something into parts, those parts should be MECE. It underlies issue trees, market sizing, data segmentation, and recommendation logic.

### Common pitfalls

- Over-segmentation: creating 7-8 granular categories when 3-5 would be clearer
- Overlapping categories (e.g., "marketing," "sales," and "customer acquisition" bleed into each other)
- Treating MECE as the goal rather than a tool -- the structure organizes thinking but does not produce answers
- Rigidity: sticking with an initial structure when new data suggests it should change

---

## Issue Trees and Logic Trees

A visual, hierarchical diagram that breaks a complex problem into progressively smaller sub-issues. The trunk states the central question; branches represent increasingly specific sub-questions. Every branch at each level must be MECE.

### Three types

**Diagnostic trees ("Why trees"):** Decompose a "Why" question. "Why has profit declined?" branches into "Revenue declined?" vs. "Costs increased?" and continues drilling down.

**Solution trees ("How trees"):** Decompose a "How" question. "How can we increase profitability by $13M?" branches into possible actions. Use the same issue tree template from SKILL.md, but frame each branch as an action rather than a diagnostic question.

**Hypothesis trees:** A more focused variant. Start with a specific testable proposition and break it into sub-hypotheses that must be true for the main hypothesis to hold. More efficient than open-ended issue trees when enough information exists to form an initial hypothesis.

### How to build one

1. Define the problem as an outcome-focused, measurable question
2. Create Layer 1: 2-5 MECE branches using a decomposition lens (stakeholder, process, segment, or math-based)
3. Create Layer 2: For each branch, break further into sub-questions
4. Continue to Layer 3-4 as needed -- stop when each bucket is directly answerable
5. Prioritize branches using 80/20 thinking
6. Gather data, confirm or reject branches, prune and refine

### Critical rules

- Never skip levels. Confirm a branch before drilling deeper into it.
- Limit to 3-5 branches per level.
- Stop decomposing when you reach something directly answerable.
- Do not mix abstraction levels within a single tier.

### Common pitfalls

- Branch-hopping: jumping between sub-branches without confirming any
- Going too deep before gathering any data
- Confusing issue trees with brainstorming lists (which lack logical hierarchy)
- Treating the tree as fixed rather than evolving it with new information

---

## Hypothesis-Driven Problem Solving

Start with an educated guess about the answer and gather data to prove or disprove it. The opposite of the bottom-up approach of collecting all data first and then searching for patterns.

### The method

1. Define the problem precisely
2. Form an initial hypothesis (the "day one answer") based on available information
3. Structure the hypothesis using an issue/hypothesis tree
4. Plan analyses to test each sub-hypothesis, identifying quick wins first
5. Gather data and test
6. Synthesize findings continuously
7. Develop recommendations based on confirmed hypotheses

### The day one answer

Even on the first day, have a coherent summary of your best understanding and a proposed solution path. Structure it as: (1) current situation, (2) the complication or problem, (3) the proposed resolution.

### Characteristics of a good hypothesis

- **Specific and falsifiable** -- it can be wrong
- **Actionable** -- it points toward decisions
- **Not obvious** -- it says something beyond common knowledge
- **Debatable** -- not merely a statement of fact

### When NOT to use

- In truly novel domains where no pattern recognition exists and exploration is needed
- In safety-critical domains where near-100% certainty is required
- When premature commitment to a hypothesis could cause harm

### Common pitfalls

- **Confirmation bias** -- seeking confirming data and ignoring disconfirming evidence. Counter with explicit stress-testing.
- Treating hypotheses as facts without testing them
- Not revising when data contradicts the hypothesis

---

## Pareto Analysis (80/20 Rule)

Roughly 80% of effects come from 20% of causes. The core insight is that outputs are not evenly distributed across inputs. The exact ratio varies -- the principle is about disproportionate impact, not a precise split.

### How to apply (quantitative)

When you have data:

1. Define the problem specifically
2. Collect data on contributing factors and their frequency or impact
3. Rank factors in descending order of impact
4. Calculate cumulative percentages
5. Identify the "vital few" -- the small number of factors driving most of the impact
6. Focus resources on the vital few

### How to apply (qualitative)

When you do not have hard data (the more common case in this skill):

1. List all factors, branches, or items under consideration
2. For each, make a rough judgment: "If I could only address one thing, which would move the needle most?"
3. Force-rank by estimated impact using High/Medium/Low or relative ordering
4. Identify the top 2-3 items that likely account for the majority of the outcome
5. Focus analysis and recommendations on those items first
6. Acknowledge the ranking is judgment-based and invite the user to adjust

The qualitative version is less precise but still valuable. The point is to avoid treating all items as equally important, which is almost never true.

### Role in structured problem solving

- Prioritize which branches of an issue tree to investigate first
- Focus analysis time on the work yielding the most insight
- Seek "good enough" answers rather than perfect ones
- Identify the small number of drivers behind a large outcome

### Common pitfalls

- Treating 80/20 as an exact law rather than a heuristic
- Ignoring the "useful many" -- some may be low-effort wins
- Static analysis: the vital few today may shift tomorrow
- In safety-critical domains, rare events can have catastrophic consequences, so you cannot ignore the long tail

---

## 5 Whys (Root Cause Analysis)

An iterative technique that drills past symptoms to root causes by repeatedly asking "Why?" Each "why" targets the answer to the previous "why," creating a causal chain.

### How to apply

Start with the observed problem. Ask "Why did this happen?" Take the answer and ask "Why?" again. Continue until you reach a cause that is **actionable** -- something you can fix with a concrete countermeasure. Verify the chain by working backward with "therefore" statements.

### Classic example (Taiichi Ohno, Toyota)

Problem: A machine stopped.
- Why? The fuse blew from overload.
- Why the overload? Bearing was not sufficiently lubricated.
- Why? The lubrication pump was not working.
- Why? The pump shaft was worn out.
- Why? No strainer was installed, so metal scraps got in.

Root cause: missing strainer. Countermeasure: install a strainer. Without the 5 Whys, workers would just replace the fuse -- a band-aid fix that ensures recurrence.

### When to stop

When you reach a cause that is directly actionable. The number 5 is not magic -- sometimes 3 suffice, sometimes 8 are needed.

### Common pitfalls

- Stopping at symptoms rather than drilling to root causes
- Single-thread bias: isolating one root cause when multiple causal paths exist
- Too simplistic for complex, multi-causal problems -- pair with fishbone diagrams when causes interact

---

## Fishbone (Ishikawa) Diagrams

A visual map of all potential causes of a specific problem, organized by category. The "head" states the problem; "major bones" represent cause categories; "sub-bones" represent specific causes.

### Standard categories

**Manufacturing/Operations (6Ms):** Manpower, Machine, Method, Material, Measurement, Mother Nature (Environment).

**Service industries (4Ps):** Places, Procedures, People, Policies.

**General-purpose (adaptable):** People, Process, Technology, Environment, Information, Resources.

Choose the category set that fits the domain. The categories are prompts for brainstorming, not rigid constraints.

### How to build one

1. State the problem clearly (the fish head)
2. Choose 4-6 cause categories appropriate to the domain
3. For each category, brainstorm specific causes: "What in [category] could cause this problem?"
4. For each cause, drill deeper with "Why?" to 2-3 sub-levels
5. Prioritize the most likely or impactful causes for investigation

### Common pitfalls

- The fishbone generates hypotheses, not proof -- data verification is still required
- Teams waste time debating which category a cause belongs in (just pick one and move on)
- Stopping too shallow -- go 2-3 levels deep on sub-causes

---

## Effort/Impact Matrix

A 2x2 grid plotting potential actions on Impact (value, benefit) versus Effort (cost, time, resources).

### The four quadrants

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | **Quick Wins** -- do first | **Big Bets** -- plan carefully |
| **Low Impact** | **Fill-Ins** -- when time allows | **Money Pits** -- drop or deprioritize |

### How to apply

1. List all potential actions or tasks
2. Score each on Impact and Effort (use High/Medium/Low or a 1-5 scale)
3. Plot on the matrix
4. Sequence: Quick Wins first, then Big Bets with planning, Fill-Ins in slack time, drop Money Pits
5. Revisit periodically as priorities shift

### Common pitfalls

- Overestimating impact and underestimating effort (the planning fallacy)
- Sunk cost fallacy: continuing Money Pit tasks because of prior investment
- Static thinking: the matrix is a snapshot, not a permanent assignment

---

## Eisenhower Matrix

Categorizes tasks by Importance (contribution to long-term goals) versus Urgency (demands immediate attention).

### The four quadrants

| | Urgent | Not Urgent |
|---|---|---|
| **Important** | **Q1: DO** -- crises, hard deadlines | **Q2: SCHEDULE** -- strategic work, personal development |
| **Not Important** | **Q3: DELEGATE** -- interruptions, most emails | **Q4: DELETE** -- time-wasters, distractions |

**The key insight:** Highly effective people spend most of their time in Q2 (Important but Not Urgent). Q3 creates the "urgency trap" -- tasks that feel pressing but do not matter.

### How to apply

1. List all current tasks, commitments, and demands on time
2. For each, ask two questions: "Does this contribute meaningfully to my long-term goals?" (Importance) and "Does this have a deadline or consequence if not done soon?" (Urgency)
3. Place each task in the appropriate quadrant
4. Execute Q1 items immediately
5. Schedule specific time blocks for Q2 items -- these are the most valuable and the most likely to be neglected
6. Delegate Q3 items where possible; if you cannot delegate, batch them into a short daily window
7. Eliminate Q4 items. If something has been in Q4 for weeks and nothing bad happened, stop doing it.
8. Review weekly: the goal is to shrink Q1 (through better Q2 planning) and Q3 (through delegation or elimination)

### Common pitfalls

- The Mere-Urgency Effect: gravitating toward time-sensitive tasks regardless of importance
- Q2 work gets perpetually postponed because nothing forces it
- Difficulty distinguishing Important from Urgent in the moment -- ask "Will this matter in 6 months?"

---

## First-Principles Thinking

Break a problem down to its most fundamental, indisputable truths and reason upward to construct new solutions. The opposite of reasoning by analogy (copying what has been done before).

### The 3-step process

1. **Identify assumptions.** List everything you currently believe about the problem.
2. **Break down to fundamentals.** What do you know for certain? What are the physical, logical, or factual constraints that cannot be changed?
3. **Build up from scratch.** Construct new solutions from the fundamental truths, ignoring conventional approaches.

### Supporting techniques

- **Socratic questioning:** Why do I think this? How do I know it is true? What if the opposite were true?
- **5 Whys on assumptions:** Apply the 5 Whys not to symptoms but to your own beliefs about the problem.

### When to use

- When existing approaches are clearly suboptimal and incremental improvement has hit diminishing returns
- When entering a new domain where conventional wisdom may not apply
- When the user says "nothing we have tried works" or "everyone does it this way but it does not make sense"

### When NOT to use

- For routine decisions -- analogical reasoning is faster and usually sufficient
- When accumulated wisdom in a domain encodes centuries of hard-won knowledge that should be respected
- The Dunning-Kruger risk: thinking you have reached fundamental truths when your "first principles" are themselves unexamined assumptions

---

## The Pyramid Principle (Minto)

Information sorted into a pyramidal structure is easier to understand. Think bottom-up (data -> patterns -> themes -> main idea), then communicate top-down (main idea -> supporting arguments -> evidence).

### Structure

- **Top:** The governing thought -- your main recommendation or conclusion
- **Middle:** 3-4 key supporting arguments
- **Bottom:** Evidence, data, and detailed findings backing each argument

### Three rules

1. Ideas in each grouping must be the same kind of idea
2. Ideas at each level must summarize the ideas grouped below them
3. Ideas in each grouping must be logically ordered (chronologically, structurally, or comparatively)

### Inductive vs. deductive

Prefer **inductive logic** -- each supporting idea independently supports the main idea. If one is disproved, the others still stand. Deductive logic (where points build on each other) is riskier: if one link breaks, the whole chain collapses.

### SCR / SCQA for framing

**Situation:** Agreed-upon context. **Complication:** What changed. **Resolution:** Your recommendation.

The longer form adds a **Question** between Complication and Answer: "Given this complication, what should we do?"

Use **direct order** (Resolution first) for receptive audiences. Use **indirect order** (Situation -> Complication -> Resolution) when the audience needs to be brought along.

### Action titles

When helping a user structure a presentation or document, each slide title or section heading should be a complete sentence stating the key takeaway of that section -- not a topic label. "Q3 Revenue" is a topic label. "Q3 revenue grew 12% driven by enterprise expansion" is an action title. A reader should be able to read only the titles and understand the full argument.

---

## Decision Matrix (Weighted Scoring)

A structured table for evaluating multiple options against weighted criteria.

### How to build one

1. List options as rows
2. Define evaluation criteria as columns
3. Assign weights to each criterion (1-5 scale or percentages summing to 100%)
4. Score each option against each criterion (1-5 or 1-10)
5. Calculate weighted scores (Score x Weight for each cell)
6. Sum across criteria for each option
7. Highest total = recommended option
8. Sanity check: does the result match informed intuition? If not, revisit weights.

### When it beats intuition

- 3+ options competing on 4+ criteria
- Stakeholders need an auditable rationale
- The decision is too complex to hold in your head
- Past gut-feel decisions have led to regret

### Common pitfalls

- False precision: a 0.5-point difference is not meaningful
- Gaming weights by marking everything as "high importance"
- Ignoring qualitative factors the matrix cannot capture
- Not doing a gut-check on the result

---

## Pre-Mortem Analysis

Imagine a project has already failed and work backward to generate plausible reasons. Developed by psychologist Gary Klein. Daniel Kahneman called it one of the most effective debiasing techniques.

### Why it works

Grounded in **prospective hindsight** -- imagining a future event as already having occurred increases the ability to identify reasons for that outcome by approximately 30%. It reverses normal team dynamics: instead of pressure to be supportive, people demonstrate insight by identifying risks.

### How to conduct one

1. Brief on the plan
2. Set the frame: "It is [timeframe] from now. This plan was a complete failure."
3. Individual generation (2-3 minutes): each person (or the analyst) independently writes down every plausible failure reason
4. Share and discuss
5. Group and prioritize by likelihood and impact
6. Adjust the plan to address the top risks
7. Document and revisit throughout execution

### When to use

- Before launching any significant initiative, project, or decision
- When optimism bias is high (the team is excited and not thinking about what could go wrong)
- As a stress-test after selecting a recommendation

### Common pitfalls

- Running it as standard critique rather than assuming failure has already happened (the framing matters)
- Not acting on the results
- Allowing debate during generation (suppresses candor)
