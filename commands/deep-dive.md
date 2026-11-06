---
description: Generate a comprehensive deep-dive doc explaining how a hook/module works, from concepts to algorithms to API flow
---

# Deep Dive

> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;
> T2 stops once, after the plan. Investigation notes, plan, and step list all live in
> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.

Produce a comprehensive deep-dive document for one or more source files. Follow this structure strictly.

---

## 1 · EXPLORATION — Research only, no output

1. Read all target files in full
2. Read all imported modules (types, executors, constants, utilities)
3. Read all consumer files where the target is invoked
4. Read the API layer that persists downstream changes
5. Trace one complete operation: user action → target → library → consumer → API → response
6. Write findings into `.ai/knowledge/plans/<slug>.md`:
   - Entry points and signatures
   - File relationships
   - Event/channel names
   - Key variables and their roles

---

## 2 · PLAN — Structure only, no content

1. Define document outline:
   - Sections to include
   - Diagrams to produce
   - Variables needing declarative definitions
   - Type definitions to extract
2. Write into `.ai/knowledge/plans/<slug>.md`:
   - TOC with section headings
   - Diagram types per section
   - Ordering rationale

---

## 3 · WRITE DOCUMENT

Produce the final `.md` file following these rules:

### Document Structure (in this order)

1. **OVERVIEW TABLE** — name | path | one-sentence role

2. **DECLARATIVE KNOWLEDGE** — explain concepts before algorithms
   - *The Problem*: ASCII diagram of the core issue (coordinate systems, broken values)
   - *Core Variables table*: variable name | type | plain-English meaning in one sentence, no jargon
   - *Key Concepts table*: term | definition

3. **DATA STRUCTURES** — actual `type X = { ... }` blocks with field comments

4. **ALGORITHM DIAGRAMS** (per hook/module, ASCII art)
   - Architecture: boxes with arrow flow
   - Key formulas: `input → computation → output`, with concrete numeric examples
   - Mode comparison: side-by-side if multiple modes exist

5. **EVENT LIFECYCLE** — trace one full operation from user action → target → library → consumer → API → response. Use concrete values at each step.

6. **FULL-STACK FLOW** — horizontal swimlane diagram: User → Library → Hooks → Feature Page → Backend

7. **DESIGN DECISIONS** — "Why X instead of Y" for each non-obvious choice. State what breaks without it.

8. **EDGE CASES TABLE** — scenario | how handled, with source line numbers

9. **INTEGRATION POINT** — copy-paste the actual call site with inline comments on each argument

10. **FILE MAP** — tree of all related files with one-line role per file

### Hard Rules

- No paragraph longer than 4 lines
- Every variable MUST appear in Declarative Knowledge or Data Structures before it's used in algorithms — no forward references
- Every algorithm block shows: `input → formula → output`
- All examples use concrete numbers, never foo/bar/baz
- Include source line numbers for all guard logic
- Write for someone who has never read the source code

**Output**: One `.md` file in `docs/`
