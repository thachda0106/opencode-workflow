---
description: Design a production-grade shared core platform package with DDD, Clean Architecture, and distributed systems patterns — 10 output phases across architecture review, API design, TypeScript interfaces, implementations, ADRs, and roadmap
agent: platform-architect
subtask: false
---

# Design Platform Core

Design a reusable shared core platform package for a large-scale distributed microservices platform. The package provides cross-cutting concerns, DDD primitives, distributed systems primitives, infrastructure abstractions, and enterprise-grade patterns — framework and infrastructure agnostic.

> [!CAUTION]
> This workflow requires human approval between every phase.
> Do NOT skip phases. Do NOT combine phases into a single response.
> DO NOT start coding immediately — challenge architecture first.

---

## PHASE 1 — SCRATCHPAD (Architecture Review)

**No design output in this phase. Review and challenge only.**

1. Load and read the following architecture documents (these are the output of a prior deep architecture review — use them as your foundation, do not re-derive from scratch):
   - `../context/ARCHITECTURE_REVIEW.md` — scope analysis, module assessment (Keep/Move/Remove), risk register (10 risks), anti-patterns (7 identified), trade-off analysis
   - `../context/RECOMMENDED_STRUCTURE.md` — the target 5-package split (@platform/foundation, core, messaging, persistence, distributed) with full file trees, dependency graph, extension points, and evolution strategy
   - `../context/ADR_CANDIDATES.md` — 15 mandatory Architecture Decision Records that must be written before implementation
2. Read the full platform-architect agent directive (module specifications, design rules, non-functional requirements)
3. Challenge the architecture using the review documents as context:
   - Verify the review findings against your own analysis — do not blindly accept, but do not re-derive
   - Identify any risks or gaps NOT covered by the existing review
   - Identify coupling risks (where do modules leak into each other?)
   - Identify scalability risks (where does the design break under load?)
   - Identify DDD violations (where do domain concepts leak into infrastructure?)
   - Identify distributed systems risks (split-brain, partial failure, ordering, consistency)
   - Identify anti-patterns in the proposed module structure
4. Suggest improvements with trade-off analysis (add to, but do not replace, the existing review findings)
5. Write findings into `SCRATCHPAD.md`:
   - Module-by-module gap analysis
   - Risk register (coupling, scalability, DDD, distributed)
   - Improvement proposals with rationale
   - Trade-off decisions to be made

**Output**: `SCRATCHPAD.md`

### 🛑 HARD STOP — APPROVAL GATE 1

```
Say: "Phase 1 (Architecture Review) complete. Please review SCRATCHPAD.md.
Reply APPROVE to continue to the planning phase, or provide feedback."
WAIT for explicit approval.
```

---

## PHASE 2 — PLAN (Package Structure & Dependency Rules)

**Scratchpad must be APPROVED. No implementation in this phase.**

1. Define the improved package structure based on approved scratchpad:
   - Final directory layout with rationale per module
   - What goes in core vs. what lives in adapter packages
2. Define dependency rules:
   - Module dependency graph (what depends on what)
   - Allowed dependencies (e.g., errors can be used by all modules)
   - Disallowed dependencies (e.g., messaging must not depend on persistence)
   - Layer rules (e.g., contracts → abstractions → implementations)
3. Define extension points per module:
   - Where adapters plug in (interfaces that external packages implement)
   - What cannot be extended (sealed abstractions)
4. Write into `PLAN.md`:
   - Refined package structure diagram
   - Dependency graph (Mermaid or ASCII)
   - Per-module dependency rules table
   - Extension point catalog

**Output**: `PLAN.md`

### 🛑 HARD STOP — APPROVAL GATE 2

```
Say: "Phase 2 (Plan) complete. Please review PLAN.md.
Reply APPROVE to continue to the task breakdown phase, or provide feedback."
WAIT for explicit approval.
```

---

## PHASE 3 — TASKS (Breakdown)

**Plan must be APPROVED. No code in this phase.**

1. Break the plan into ordered deliverables across the remaining 8 output phases:

   | Task | Phase | Deliverable |
   |------|-------|-------------|
   | Task 1 | Public API Design | All interfaces and contracts per module |
   | Task 2 | TypeScript Interfaces | Full TypeScript type definitions |
   | Task 3 | Abstract/Base Implementations | Reusable base classes |
   | Task 4 | Example Usages | Concrete usage patterns for each module |
   | Task 5 | Testing Strategy | Unit, integration, contract testing approach |
   | Task 6 | Architecture Decision Records | ADRs for key decisions |
   | Task 7 | Implementation Roadmap | Prioritized, phased implementation plan |

2. For each task, specify:
   - Modules covered
   - Files/artifacts to produce
   - Dependencies between tasks
   - Acceptance criteria

3. Write into `TASKS.md`

**Output**: `TASKS.md`

### 🛑 HARD STOP — APPROVAL GATE 3

```
Say: "Phase 3 (Task Breakdown) complete. Please review TASKS.md.
Reply APPROVE to begin implementation, or provide feedback."
WAIT for explicit approval.
```

---

## PHASE 4 — IMPLEMENTATION (API Design → Interfaces → Implementations → Examples → Testing Strategy)

**Tasks must be APPROVED before writing any code.**

Execute Tasks 1-5 in order:

### Task 1 — Public API Design

For EVERY module (config, execution-context, contracts, validation, observability, resilience, persistence, messaging, distributed, cache, security, idempotency, consistency, tenancy, workflow, scheduler, feature-flags, serialization, errors, web), define:
- Purpose and responsibilities
- Public interfaces (TypeScript `interface`)
- Abstract classes where applicable
- Extension points (where adapters plug in)
- Dependency rules (what it can/cannot import)

### Task 2 — TypeScript Interfaces

Produce full TypeScript type definitions for all public APIs:
- All `interface` declarations with JSDoc
- All `type` aliases
- All generic constraints
- All error types with discriminated unions
- Module re-exports (`index.ts` barrel files)

### Task 3 — Abstract/Base Implementations

For modules that benefit from shared behavior:
- Abstract base classes with template methods
- Default implementations (e.g., `InMemoryCacheStore`, `NoOpMetrics`)
- Guard clauses and invariant checks
- Fail-fast validation in constructors

### Task 4 — Example Usages

For every module, provide:
- Minimal working example (copy-paste runnable)
- Integration example (how modules compose together)
- Adapter implementation example (how to plug in infrastructure)
- Anti-pattern example (what NOT to do)

### Task 5 — Testing Strategy

Define:
- Test pyramid: unit → integration → contract → E2E
- Per-module testing approach
- Test doubles strategy (mocks vs fakes vs stubs)
- Contract testing for adapter interfaces
- Property-based testing opportunities
- Coverage targets per layer

---

## PHASE 5 — TESTING & VALIDATION (ADRs → Roadmap → Final Review)

After implementation:

### Task 6 — Architecture Decision Records

Write ADRs for critical decisions:
- Format: Title → Status → Context → Decision → Consequences → Alternatives Considered
- Minimum ADRs: core package boundary, async local storage choice, error model design, messaging envelope design, fencing token strategy, tenancy strategy
- Cross-reference ADRs to module documentation

### Task 7 — Implementation Roadmap

Produce a prioritized, phased implementation plan:
- Phase-by-phase breakdown with dependencies
- Effort estimates per phase
- Risk mitigation per phase
- Rollout strategy (how services adopt the core package)
- Backward compatibility guarantees
- Deprecation and migration policy

### Final Review

- Verify all 10 output phases are complete
- Verify no infrastructure-specific code leaked into core
- Verify all interfaces are framework-agnostic
- Verify dependency rules are enforced
- Verify all modules have purpose/responsibilities/APIs/extensions/examples
- Run type checking on all TypeScript deliverables
