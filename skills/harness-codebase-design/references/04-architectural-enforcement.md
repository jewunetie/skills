# 04 Architectural enforcement

Documentation alone does not keep a codebase coherent when agents are doing the writing. Agents replicate whatever patterns already exist, including bad ones. They cross architectural boundaries unless boundaries are mechanically enforced. They invent variant names for the same concept unless naming is constrained.

The strategy: enforce invariants, do not micromanage implementations.

## The invariants-not-implementations principle

OpenAI's framing: require the agent to "parse data shapes at the boundary," but do not specify which library. The model can pick Zod, Pydantic, io-ts, or whatever fits. The constraint is the invariant ("data is validated at the boundary"), not the implementation ("use Zod").

Other examples of the same shape:

- "All log statements are structured" (invariant) versus "use the `winston.json()` formatter" (implementation).
- "Every public function has typed return values" (invariant) versus "use TypeScript strict mode with `noImplicitAny`" (implementation).
- "External calls have timeouts" (invariant) versus "use `axios` with the project default timeout" (implementation).

The reason this matters: agents are most effective in environments with strict boundaries and predictable structure. Strict on the boundary, loose on the implementation. The output may not match human stylistic preferences, and that is fine. The bar is correct, maintainable, and legible to future agent runs.

## Layered architecture as the load-bearing pattern

The single most consistently recommended pattern across the literature is forward-only layered architecture per business domain.

OpenAI's example layer order, for an "App Settings" domain:

```text
Types -> Config -> Repo -> Service -> Runtime -> UI
```

Code can only depend "forward" through the fixed layer set. Types know nothing about Config; Config knows about Types but not Repo; and so on up the chain. Cross-cutting concerns (auth, connectors, telemetry, feature flags) enter through a single explicit interface called Providers. Anything else is mechanically disallowed.

A simpler variant for smaller codebases (from MadPlay's example):

```text
domain -> application -> infrastructure
```

with the rule that infrastructure does not reference domain directly.

The exact layer order matters less than these properties:

- Layers are named and few (three to six is typical).
- Dependencies flow in one direction. No cycles.
- Cross-cutting concerns have one explicit entry point per domain.
- Violations are mechanically detected, not policed by humans in code review.

This is the kind of architecture you would normally postpone until you have hundreds of engineers. With agents, it is a day-one prerequisite. Constraints are what allow speed without architectural drift.

## Custom linters that teach the fix

Custom linters and structural tests do the enforcement. They can be agent-generated (have the agent write them).

The non-obvious lesson: lint error messages should inject remediation instructions back into the agent's context. A lint that says "rule violated" is less useful than one that teaches the fix.

A bad lint error:

```text
ERROR: Layer violation in services/payment.py:3
```

A good lint error (from Caprihan's Medium walkthrough):

```text
ERROR: Dependency violation in services/payment.py:3
  -> Cannot import from ui/components in service layer.
  -> Move this logic to the service layer and pass results down as parameters.
  -> See docs/architecture/dependency-rules.md
```

The good error is itself a prompt. The agent reads it, self-corrects, and tries again.

## Structural tests for non-lint-friendly invariants

Some invariants are easier to express as tests than as lints:

- "No service file is over 800 lines."
- "Every Repo class has a corresponding interface in Types."
- "No file imports both `auth` and `feature-flags` directly; both go through Providers."
- "Every public API endpoint has a test in `tests/api/`."

Tools like ArchUnit (Java), arch-go (Go), import-linter (Python), eslint-plugin-import (JavaScript) can encode these. Agent-generated structural tests work fine and are checked into the repo.

## Taste invariants worth encoding statically

Beyond architecture, there is a second category: small, opinionated rules about how code should look. These feel pedantic in a human-first workflow. With agents, they are multipliers because they apply everywhere at once.

A starter set, drawn from the literature:

- **Structured logging.** All log statements use the project logger with a consistent shape (event name, structured fields). No `console.log` or `print` in non-test code.
- **Naming conventions for schemas and types.** A Repo type for `User` is named `UserRepo`, not `UserRepository` or `UserStore`. Pick one and enforce.
- **File size limits.** Files over a threshold (often 600 to 1000 lines) fail lint. This forces decomposition.
- **Function length.** Functions over a threshold (50 to 150 lines) trigger a warning or error.
- **No data probing.** Do not access `.id` on an unknown shape. Validate the shape first or use a typed SDK. (Golden principle expression: "Do not probe data shapes blindly.")
- **No silent error swallowing.** `try ... catch` must log or re-throw, never return silently.
- **Reuse before creation.** If a utility-package function exists, use it. New helpers go in the utility package, not inline. (See garbage collection reference for how this is enforced over time.)
- **Boundary validation.** Data crossing a layer boundary (HTTP request to service, database row to domain object) is validated and typed.
- **Platform-specific reliability requirements.** If the project has SLAs around startup time, latency, or memory, encode them as test assertions.

The lints can themselves be agent-generated. Instructions: "Write a custom ESLint/ruff/golangci rule that flags X. Return the rule plus a remediation message that teaches an LLM how to fix the violation."

## Centralize boundaries, allow autonomy locally

The model: enforce at the boundary, allow freedom inside. Specifically:

- Care deeply about: layer boundaries, types crossing those boundaries, naming of architectural roles, cross-cutting interfaces, structured logging shape, test coverage at the boundary.
- Allow freedom in: choice of utility libraries, internal data structures, function decomposition style within a layer, comment style, formatting (handled by an autoformatter), variable naming inside a function.

Resulting code may not match human stylistic preferences. That is acceptable as long as the code is correct, the boundaries are intact, and future agent runs can navigate it.

## Where human taste enters the system

Human taste should never enter through ad-hoc review comments that do not make it back into the harness. The pattern:

1. Reviewer notices a stylistic or design issue.
2. Reviewer or someone else asks: "is this rule mechanically checkable?"
3. If yes, promote it into a lint or structural test. The rule now applies everywhere automatically.
4. If no, capture it as a documentation update (golden principle, design doc, or AGENTS.md line if universal).
5. Either way, the agent writes the change and commits it.

The discipline: human taste is captured once, then enforced continuously on every line of code.

## When you are retrofitting an existing codebase

Retrofitting is harder than greenfield because the existing code probably violates many of the rules you would want to add. Two failure modes:

- Add all the rules at once. The build is broken. The agent (and humans) drown in alerts. (Birgitta Boeckeler's analogy: running a static analysis tool on a codebase that has never had one and drowning in alerts.)
- Add rules with low severity. The rules get ignored.

A safer pattern:

1. Start with one or two architectural invariants that map cleanly to the existing layout. Add custom lints with `error` severity but a project-wide allowlist of existing violations. New code is held to the rule; existing violations are tracked.
2. Drain the allowlist over time using a scheduled cleanup agent. Each cleanup PR removes a few violations.
3. Add the next invariant once the first allowlist is mostly drained.
4. Repeat.

This is the same garbage-collection pattern described in `references/09-garbage-collection.md`, applied to legacy debt.

## Solo developer minimum

A solo developer probably does not need custom linters or structural tests on day one. The minimum:

- Choose a strongly-typed language or strict mode of a typed language. Type errors become free back-pressure.
- Encode three to five hard constraints in AGENTS.md ("never edit tests," "always use the project logger").
- Add custom lints only when the agent has violated the same architectural rule twice in two different sessions.
