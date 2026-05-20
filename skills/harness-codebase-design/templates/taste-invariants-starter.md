# Taste invariants starter

> A starter list of invariants worth encoding as custom lint rules or structural tests. Each one earns its place because it is mechanically checkable, applies broadly, and prevents a class of agent drift. Adopt selectively. Do not enable all of them on day one.
>
> When implementing each rule, write the lint error message to teach the fix. The agent reads the error, self-corrects, and tries again. A bad lint says "rule violated"; a good lint says "Cannot import from `ui/components` in service layer. Move this logic to the service layer and pass results down as parameters. See docs/architecture/dependency-rules.md."

---

## Architecture rules

### Forward-only layer dependencies

Code can only depend "forward" through the layer set: `Types -> Config -> Repo -> Service -> Runtime -> UI` (or whatever your project uses). Layers cannot reach backward.

Implementation: a custom import-check rule. Tools: `eslint-plugin-import` for JS/TS, `import-linter` for Python, `arch-go` for Go, `ArchUnit` for Java.

Error message template:

```text
Layer violation in [file]:[line]
[file] is in the [X] layer; it cannot import from [Y] which is in a forward layer.
Move this logic to the [appropriate] layer and pass results down as parameters.
See docs/architecture/dependency-rules.md.
```

### Cross-cutting concerns through Providers only

Auth, logging, telemetry, feature flags enter business logic through a single `Providers/` interface. Direct imports of the underlying packages (`auth-lib`, `logger-lib`, `feature-flags-lib`) are blocked outside `Providers/`.

Error message template:

```text
Direct import of [auth-lib] is not allowed in [file]:[line]
Cross-cutting concerns enter through Providers/. Use Providers.auth instead.
See docs/architecture/providers.md.
```

## Data shape rules

### Boundary validation required

Functions exposed at architectural or external boundaries (HTTP handlers, database row mappers, message handlers) must validate their input. Untyped or partially-typed parameters fail lint.

Implementation: depends on the language. For TypeScript with Zod or io-ts, check that boundary functions either accept already-validated types or call a parser. For Python with Pydantic, check that handler signatures use a Pydantic model.

Error message template:

```text
Boundary function [name] in [file]:[line] accepts an unvalidated input.
External data must be parsed at the boundary. Add a schema parser or use a typed model.
See docs/architecture/boundary-validation.md.
```

### No `any` or `unknown` access without narrowing

In TypeScript, accessing properties on `any` or `unknown` without a type guard fails lint.

Implementation: TypeScript strict mode plus eslint rules `@typescript-eslint/no-explicit-any` and `@typescript-eslint/no-unsafe-member-access`.

## Logging and observability rules

### Structured logging only

All log statements use the project logger with a structured shape (event name, structured fields). No `console.log`, `console.error`, `print`, `fmt.Println`, etc. in non-test code.

Implementation: forbid the bare logging functions in lint config. Allowlist test files.

Error message template:

```text
Bare console.log in [file]:[line]
Use the project logger: logger.info({ event: "...", ...fields })
See docs/conventions/logging.md.
```

### No silent error swallowing

Catch blocks must either log or re-throw. Empty catch blocks fail lint. Catch blocks that only return without logging fail lint.

### No credential strings in code

Detect literal strings that match credential patterns (`AKIA...`, `ghp_...`, `sk_...`). Block them in pre-commit and in lint.

Implementation: `git-secrets`, `gitleaks`, or a custom regex rule.

## Naming rules

### Canonical names for domain entities

If the project has a domain glossary, enforce it. A `User` is `User` everywhere; `Customer` and `Person` are forbidden as aliases.

Implementation: a custom rule that scans for forbidden names. Allowlist for legitimate uses (a third-party library's `Customer` type, for example).

### Naming conventions for architectural roles

A repo for `User` is named `UserRepo`, not `UserRepository` or `UserStore`. A service for `User` is `UserService`. Pick one convention per role and enforce.

Implementation: a custom regex rule that checks file names and exported types.

## Size rules

### File size limit

Files over a threshold (commonly 600 to 1000 lines) fail lint. This forces decomposition.

### Function size limit

Functions over a threshold (commonly 50 to 150 lines) trigger a warning or error.

### Function parameter limit

Functions with more than [N] parameters (commonly 5) trigger a warning. Use a named parameter object instead.

## Test rules

### Test edits require explicit authorization

A pre-commit hook greps the diff for changes to test files. If any test file is edited, the commit message must include `[test-edit-authorized]` or the commit fails. This implements the strongly-worded constraint "It is unacceptable to remove or edit tests."

### No skipped tests without an issue link

Detect `.skip(`, `xit(`, `test.skip(`, `pytest.mark.skip` and require an issue link in the comment above.

Implementation: regex check. Error message references the relevant doc.

### No test of internal implementation details

Soft rule. Hard to enforce mechanically, but a partial check: forbid imports from internal-marked modules (`__internals__` or similar) inside test files except via the public interface.

## Concurrency and timing rules

### No `Date.now()` outside the clock abstraction

Force time to come from the project clock. Block direct `Date.now()`, `time.time()`, `System.currentTimeMillis()`. Allowlist the clock implementation file itself.

### No bare `setTimeout` outside the time abstraction

Same pattern, applied to scheduled work.

### No raw `fetch` or `requests`

HTTP goes through the project HTTP client. Block direct usage.

## Configuration rules

### No hard-coded URLs in business logic

URLs come from config. Detect literal `http://` or `https://` strings outside the config layer.

Implementation: regex with allowlist for tests, fixtures, and config files.

### No magic numbers

Numeric literals other than 0, 1, -1 in business logic must be named constants. Soft rule; partial enforcement possible.

## Lint config protection

### Lint config edits require approval

A pre-commit hook checks whether the diff touches `.eslintrc`, `eslint.config.js`, `pyproject.toml`, `.golangci.yml`, etc. If yes, require an approval comment from a human in the PR. This prevents the failure mode of "agent disables a rule to make CI pass."

---

## How to introduce these gradually

For an existing codebase that already violates many of these:

1. Pick one rule.
2. Implement the lint with `error` severity.
3. Generate an allowlist of existing violations (most lint tools support this directly: `# eslint-disable-next-line`, `# noqa`, `# nolint`).
4. New code is held to the rule. Existing violations are tracked.
5. A scheduled cleanup agent drains the allowlist over weeks. Each cleanup PR removes a few violations.
6. Add the next rule once the first allowlist is mostly drained.

Trying to enable everything at once produces an unworkable build and a team that disables the rules to ship.

## How to write custom lints with the agent

A standard prompt for generating a custom lint:

> Write a custom [eslint / ruff / golangci / arch-go] rule that flags [specific violation]. Return the rule plus a remediation message that teaches an LLM how to fix the violation. The remediation message should reference the relevant doc and suggest a concrete next action.

Most modern lint frameworks support custom rules. Once the agent has produced one, you have the pattern; subsequent rules are easier.
