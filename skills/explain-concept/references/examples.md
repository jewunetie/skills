# Worked Examples

Three examples demonstrating the explain-concept skill at each tier. These show
the tone, pacing, structure, and decision-making the skill produces. Read these
before your first use of the skill in a session.

## Table of Contents

1. Quick Concept: "What is idempotency?"
2. Structured Explanation: "How does RLHF work?"
3. Deep Dive: "Teach me about the CAP theorem and its practical implications"

---

## 1. Quick Concept: "What is idempotency?"

**Tier detection reasoning:** Single mechanism, one core idea, no sub-systems.

**Anchor assessment:** User has a software engineering background. Structural analogy
available from everyday interactions.

**Research decision:** Stable, well-established concept. No research needed.

### Example output:

You know how clicking "Place Order" twice on a slow checkout page can accidentally
create two orders? Idempotency is the property that prevents that -- the system
recognizes the action already happened and returns the same result without creating
a duplicate.

More precisely, an operation is idempotent if performing it multiple times produces
the same result as performing it once. HTTP PUT is idempotent (updating a record to
the same values repeatedly changes nothing after the first call). HTTP POST
typically is not (each call might create a new record).

This matters most in distributed systems where network failures mean you cannot
always know if your request succeeded. If your operation is idempotent, you can
safely retry without fear of side effects. If it is not, you need additional
mechanisms (like idempotency keys) to prevent duplicates.

The compressed version: idempotency means "safe to retry." Design operations so
repeating them does not change the outcome, and your system becomes resilient to
the inevitable network hiccups.

---

**What to notice about this example:**

- Anchor is drawn from a universally relatable scenario (double-clicking checkout)
- No decomposition -- the concept does not have multiple interacting parts
- No checkpoint -- Quick Concept tier skips it
- Compressed version arrives fast
- Total length is a few paragraphs, conversational throughout

---

## 2. Structured Explanation: "How does RLHF work?"

**Tier detection reasoning:** 3-4 distinct components that interact (base model,
reward model, human feedback, PPO optimization). Understanding requires grasping
relationships between parts.

**Anchor assessment:** User has a product background. A/B testing and iterative
feedback loops are a strong structural analogy.

**Research decision:** Structured tier. Core concepts are stable, but check if
anything has shifted recently in the RLHF landscape. Light research warranted.

### Example output:

> The following is what the user would actually see. Notice that step labels are
> NOT present in the output -- the structure is felt through the flow of the
> writing, not announced with headers.

RLHF works like the feedback cycle you run when iterating on a product. You ship a
version, put it in front of users, collect their reactions (this flow feels clunky,
this feature is exactly right, something is off here but I cannot say what), and use
those reactions to guide the next iteration. The users are not redesigning the product
themselves -- they are shaping it through preferences.

RLHF does the same thing for language models. The model generates outputs, humans
rate which outputs they prefer, and the model is trained to produce more of what
humans liked. The humans are not editing the model's weights -- they are shaping its
behavior through preferences.

This analogy breaks down in one important way: user feedback on a product is usually
rich and contextual (a user explains *why* something does not work). In RLHF, the
feedback is typically thin -- just a preference ranking between two outputs, with
no explanation attached.

So why does RLHF exist? Language models trained on internet text learn to predict what
comes next in a sequence, but "what comes next" is not the same as "what is helpful,
honest, and harmless." A base model can write convincing text that is confidently
wrong, toxic, or unhelpful. RLHF is the bridge between "good at predicting text" and
"good at being useful."

The process has three major zones: supervised fine-tuning (getting the model into
roughly the right behavioral neighborhood), reward modeling (building a system that
scores outputs the way a human would), and policy optimization (training the model to
maximize that score). These happen in sequence, each building on the previous one.

Let me walk through each.

**Supervised fine-tuning (SFT):** Before RLHF begins, you need the model to be in
the right ballpark. Human annotators write high-quality example responses to prompts,
and the model is fine-tuned on these examples. This is expensive (you are paying
humans to write) but necessary -- RLHF refines behavior, it does not create it from
scratch. Without SFT, the model would not even know what "being helpful" looks like
well enough for preference comparisons to be meaningful.

**Reward modeling:** This is where the human preferences come in. The SFT model
generates multiple responses to the same prompt. Human raters rank them (response A
is better than response B). A separate neural network -- the reward model -- is
trained on these rankings to predict which responses humans would prefer. Once
trained, this reward model can score any output without needing a human in the loop.
This matters because you cannot have a human rate every single training example -- the
reward model is the scalable proxy for human judgment.

**Policy optimization (PPO):** Now you have a scoring function (the reward model) and
a language model you want to improve. Proximal Policy Optimization (PPO) is the
algorithm that adjusts the language model's behavior to maximize the reward model's
scores, while staying close enough to the original model that it does not degenerate
into reward hacking -- gaming the score in ways that technically score high but are
clearly bad outputs.

The connection between these pieces: SFT gets you a model that behaves roughly
correctly. The reward model encodes human preferences into a computable signal. PPO
uses that signal to systematically push the model toward better behavior. Remove any
one piece and the system fails -- no SFT means preferences are meaningless (the model
is too far from useful), no reward model means you cannot scale beyond a handful of
human-rated examples, no PPO means the reward model's knowledge never reaches the
actual language model.

The core tension in RLHF is that human judgment has to be compressed into a
numerical score that a training algorithm can optimize against. Where do you think
that compression is most likely to lose something important?

> *[Annotation: This is the restating checkpoint. Wait for user response. If they
> identify the reward model as the bottleneck -- the "thin feedback" problem from
> the anchor -- confirm and proceed. If they point elsewhere, explore their reasoning
> before correcting or validating.]*

> *[Annotation: After the user responds and understanding is confirmed, deliver the
> compressed version:]*

RLHF in one paragraph: Start with a model that roughly knows how to be helpful
(SFT). Have humans rank its outputs to build a scoring function (reward model). Then
train the model to maximize that score without degenerating (PPO). The whole system
is bottlenecked by the quality of human preferences and how well the reward model
captures them.

I can export a reference memo from this if you want to hold onto it.

---

**What to notice about this example:**

- No step labels in the output -- the flow from anchor to landscape to decomposition
  to checkpoint to compression is felt through the writing, not announced
- Anchor maps the RLHF mechanism to a general product feedback loop, not a persona-
  specific context
- Anchor names its limit (thin feedback vs rich contextual feedback)
- Landscape answers why, what zones, and how it relates -- without explaining
  mechanisms yet
- Decompose explains each piece's mechanism, why it matters, AND how it connects to
  the other pieces
- Checkpoint is tailored to the specific tension in the topic (preference compression)
- Compress is tight -- one paragraph, optimized for recall
- Memo offer is visible but not pushed

---

## 3. Deep Dive: "Teach me about the CAP theorem and its practical implications"

**Tier detection reasoning:** Multiple interacting concepts (consistency, availability,
partition tolerance), competing schools of thought (CP vs AP systems), requires
understanding distributed systems context to grasp why the theorem matters, and has
practical implications that vary by use case. Expert would need more than 5 minutes.

**Anchor assessment:** User is a software developer. A relatable multi-node data
scenario makes the trade-off immediately tangible.

**Research decision:** Deep Dive tier -- research first, non-negotiable. Check for
recent critiques or refinements of CAP (e.g., Kleppmann's critiques, PACELC).

### Example output:

> The following is what the user would actually see. Step labels are annotations
> only -- they do not appear in the actual output.

*[Research phase completed -- results inform the explanation below but the research
process is not narrated to the user.]*

Imagine your app's database is replicated across two data centers. A user updates
their account email in data center A. At that exact moment, the network link between
the two data centers goes down.

Now you have a choice. Option A: data center B refuses to serve any account data
until the network recovers and it can sync the update. The data is always correct,
but users on that side are locked out. Option B: data center B keeps serving requests
with its last-known data, and some users might briefly see the old email. The system
stays up, but the data is temporarily wrong.

That is the CAP theorem in one scenario. You cannot have both perfect consistency
and continuous availability when network partitions happen. You have to choose which
failure mode you prefer.

This analogy maps well to the core trade-off but breaks down in two places: real CAP
decisions involve subtler gradations than this binary choice, and "partition" in CAP
means something more specific than "network is down" -- it means the system is split
into groups that cannot communicate with each other.

The CAP theorem exists because distributed systems are fundamentally different from
single-machine systems. On one computer, reading data after writing it always gives
you the latest version. The moment you spread data across multiple machines connected
by a network, that guarantee becomes expensive or impossible to maintain under all
conditions.

The theorem, formalized by Eric Brewer in 2000 and proven by Gilbert and Lynch in
2002, says a distributed system can provide at most two of three guarantees
simultaneously:

1. **Consistency** -- every read returns the most recent write
2. **Availability** -- every request gets a response (no timeouts, no errors)
3. **Partition tolerance** -- the system keeps functioning when network communication
   between nodes is lost

The important context: since network partitions *will* happen in any real distributed
system, partition tolerance is not actually optional. The practical choice is between
consistency and availability *during a partition*. Outside of partitions, you can have
both. This reframing -- from "pick two of three" to "what do you sacrifice during
failures" -- is the key to understanding why CAP matters in practice.

Let me unpack each piece.

**Consistency (C):** Every node in the system returns the same data at the same time.
If a write succeeds on one node, all subsequent reads on any node reflect that write.
This matters when correctness is non-negotiable -- financial transactions, inventory
counts, anything where seeing stale data leads to bad decisions. The cost: to
guarantee consistency during a partition, nodes that cannot verify they have the
latest data must refuse to respond. The system becomes partially unavailable.

**Availability (A):** Every request receives a non-error response. No node ever says
"I cannot answer right now." This matters when uptime and responsiveness are more
important than perfect accuracy -- a product catalog, a content delivery network,
a system where brief staleness is tolerable. The cost: during a partition, some nodes
may serve stale data because they cannot check if they have the latest version.

**Partition Tolerance (P):** The system continues to operate despite network splits
between nodes. In any system that runs on more than one machine, partitions are not
hypothetical -- they are inevitable. Hardware fails, cables get cut, cloud regions
lose connectivity. A system that cannot tolerate partitions is effectively a
single-machine system. This is why "pick two" is misleading -- you always need P,
so the real choice is C or A during partitions.

**How the pieces connect:** Outside of a partition, a well-designed system provides
both consistency and availability. The trade-off only activates when nodes cannot
communicate. CP systems (like traditional relational databases with synchronous
replication) choose consistency -- they block or error when they cannot guarantee
correctness. AP systems (like Cassandra, DynamoDB in its default mode) choose
availability -- they keep serving requests and reconcile inconsistencies later. The
engineering challenge is not picking a side permanently, but designing systems where
the trade-off activates as rarely as possible and degrades gracefully when it does.

**Beyond CAP -- PACELC:** Researcher Daniel Abadi pointed out that CAP only describes
behavior during partitions, but systems also make trade-offs during normal operation.
PACELC extends the framework: during a Partition, choose Availability or Consistency;
Else (normal operation), choose Latency or Consistency. A system might be consistent
during partitions (CP) but still sacrifice some consistency for speed during normal
operation. This extension better captures the design space of real systems.

The part that trips most people up about CAP is the relationship between the theorem
(which sounds like you are choosing two properties) and the practical reality (which
is about failure-mode design). How would you describe the actual decision a system
designer is making when they "choose" between consistency and availability?

> *[Annotation: This is the restating checkpoint. Wait for user response. Key things
> to listen for: do they frame it as a design-time choice or a failure-mode choice?
> Do they recognize that the trade-off only activates during partitions? If they
> frame it as "you just pick two and lose one forever," correct toward the
> partition-conditional understanding.]*

> *[Annotation: After user responds and understanding is confirmed:]*

CAP theorem in brief: any distributed system must tolerate network partitions, so the
real question is what happens during a partition -- do you block requests to stay
correct (CP) or keep serving potentially stale data to stay responsive (AP)? Outside
partitions, you can have both. PACELC extends this: even during normal operation, you
trade between latency and consistency. The engineering work is minimizing how often
the trade-off activates and managing degradation when it does.

If you want, I can pull this into a reference memo you can come back to.

---

**What to notice about this example:**

- No step labels in the output -- transitions between anchor, landscape, decomposition,
  checkpoint, and compression happen through natural writing flow
- Research happened before the explanation began (not narrated)
- Anchor uses a generic two-data-center scenario relatable to any developer
- Anchor names two specific limits
- Landscape gives the history (Brewer, Gilbert and Lynch) and the critical reframing
  (not "pick two" but "what do you sacrifice during failures") before any mechanism
  is explained
- Decompose covers each component's mechanism, why it matters, what it costs, and how
  it connects to the others
- Decompose naturally includes a concrete advancement (PACELC) because it illuminates
  the core concept -- not forced, but relevant
- Checkpoint targets the specific misconception most common with CAP
- Compress is tight and actionable

---

## Export Memo Example

If the user asked "go deeper on how this applies to our architecture" and then
requested a memo, the output file would look like this:

```markdown
# The CAP Theorem and Distributed System Trade-offs

## Summary
Any distributed system must tolerate network partitions, so the real question is what
happens during a partition: block requests to stay correct (CP) or keep serving
potentially stale data to stay responsive (AP). Outside partitions, you can have both.

## Core Analogy
Two data centers replicating account data: if data center A updates an email and the
link to data center B goes down, the system must choose between locking B's users out
(consistency) or letting them work with stale data (availability). Breaks down when:
real CAP involves subtler gradations than this binary, and "partition" is more specific
than "network down."

## Key Components

### Consistency
Every node returns the same data at the same time. Critical when stale data leads to
bad decisions (financial transactions, inventory). Cost: unavailability during
partitions when nodes cannot verify they have the latest data.

### Availability
Every request gets a response, no timeouts. Important when uptime matters more than
perfect accuracy. Cost: stale data possible during partitions.

### Partition Tolerance
System operates despite network splits. Not optional in any real distributed system.
This is why "pick two of three" is misleading -- you always need partition tolerance.

### PACELC Extension
During Partition: choose Availability or Consistency. Else: choose Latency or
Consistency. Captures the full design space better than CAP alone.

## Examples
- Two-data-center account sync scenario (partition during email update)
- CP system behavior: data center B locks out until sync restores
- AP system behavior: data center B serves stale email, reconciles later

## Nuances and Corrections
- Initial framing of "pick two" was refined to "what do you sacrifice during
  partitions" -- the trade-off is conditional, not permanent
- Clarified that "partition" means nodes unable to communicate with each other,
  not simply "network is down" -- the distinction matters for diagnosing real failures

## Open Questions
- Which data in our system requires CP behavior vs can tolerate AP?
- How does our current replication strategy handle partition scenarios?
- How does PACELC apply to our latency requirements?
```

---

**What to notice about the memo:**

- Standalone -- someone could read it without the conversation and understand the
  concept
- Preserves reasoning, not just facts
- Nuances section captures what evolved during dialogue
- Open questions give the user a clear path for future exploration
- Context-neutral -- the open questions are placeholders the user fills in, not
  assumed specifics
