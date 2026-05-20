# Code Review Reference

Per-pass categories for reviewing code (any language).

## Pass 1: Surface

- Typos in identifiers, comments, error messages, log strings
- Formatting: indentation, line length, trailing whitespace, blank-line conventions
- Linter-style issues: unused imports, unused variables, dead code, unreachable branches
- Syntax: missing brackets, unmatched quotes, broken string interpolation
- Documentation: docstring/comment formatting, broken markdown in docstrings
- Inconsistent naming conventions across the file (camelCase mixed with snake_case)
- Magic numbers that should be named constants

## Pass 2: Logic and internal consistency

- Off-by-one errors in loops and indexing
- Edge cases: empty input, null/None, single element, very large input, unicode, negative numbers
- Error handling: are exceptions caught at the right level, are error messages useful, are silent failures hidden
- Boundary conditions on numeric ranges, string lengths, array sizes
- Concurrency: race conditions, shared mutable state, ordering of async operations
- Resource leaks: unclosed files, sockets, database connections
- Type correctness: do return types match what callers expect, are nullable values handled
- Control flow: are all branches reachable, is the happy path actually correct, are early returns consistent
- Are introduced functions/variables actually used? Are used functions/variables actually defined or imported?
- Does the code do what its surrounding documentation claims it does?

## Pass 3: Cross-reference

- Original request: does the implementation cover every requirement the user stated?
- Spec or design doc: does the code match the spec, especially around data shapes and API contracts?
- Existing codebase conventions: does new code follow the patterns already used (naming, error handling, layering)?
- Test files: are there tests for new behavior? Do existing tests still pass conceptually given the changes?
- Imports: are all imports actually used? Are all referenced names actually imported?
- External APIs and library calls: are the function signatures correct, are deprecated APIs avoided?
- Database/schema/migration files: do they line up with model definitions?
- User formatting preferences from the conversation (e.g., specific style choices the user has stated)

## Pass 4: Regression

- Did a fix introduce a new typo or syntax error?
- Did a `str_replace` partially update a string and leave stale text behind?
- Did renaming a function/variable update all call sites?
- Did the fix neighbor unrelated code that is now broken?
- Did indentation get corrupted by the edit?
- Did a fix in one file create an inconsistency with another file (mismatched function signatures, stale imports)?
- Did the fix conflict with the user's stated preferences (e.g., introduced an em-dash, added a contraction)?

## Severity guidance

When reporting, distinguish:

- **Bug**: code does the wrong thing or fails
- **Risk**: code is fragile and likely to fail under realistic conditions
- **Style**: code works but violates conventions or readability
- **Question**: Claude is unsure whether something is intentional

Fix bugs and risks. Surface style as a single batched report. Surface questions for the user.
