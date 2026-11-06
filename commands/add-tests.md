---
description: Generate comprehensive tests following project testing standards
agent: test-engineer
subtask: false
---

# Add Tests

> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;
> T2 stops once, after the plan. Investigation notes, plan, and step list all live in
> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.

Generate comprehensive tests for the selected code following project testing standards.

---

## 1 · INVESTIGATE — Exploration

**No code or plans in this phase. Analysis only.**

1. Ask user which test type to generate:
   - **Unit Test** — Isolated module testing with mocked dependencies (default)
   - **Integration Test** — Full flow with real dependencies
   - **E2E Test** — End-to-end API/UI testing
2. Read the code to be tested
3. Understand business logic and edge cases
4. Identify dependencies to mock
5. Find existing test patterns for consistency
6. Write analysis into `.ai/knowledge/plans/<slug>.md`

---

## 2 · PLAN — Test Strategy

1. Define the test strategy from the plan file:
   - Coverage areas (service logic, error handling, data access, API, validation, edge cases)
   - Mocking strategy for dependencies
   - Test file naming and location per project conventions
   - Setup/teardown approach
2. Risk analysis — what's hard to test? What could be flaky?
3. Write into `.ai/knowledge/plans/<slug>.md`

---

## 3 · STEPS — Test Cases

1. List specific test cases to implement, organized by file:
   - [ ] Test file 1: `module.service.spec.ts` (or equivalent)
     - Case 1: Description
     - Case 2: Description
   - [ ] Test file 2: `module.controller.spec.ts` (or equivalent)
     - Case 1: Description
     - Case 2: Description
2. For each test case, specify:
   - What is being tested
   - Input / setup
   - Expected outcome
   - Dependencies to mock
3. Write into `.ai/knowledge/plans/<slug>.md`

---

## 4 · IMPLEMENT — Write Tests

Follow project conventions:
- Arrange-Act-Assert pattern
- Descriptive test names explaining the scenario
- Proper mock setup and cleanup
- One behavior per test case

---

## 5 · VALIDATION

After tests are written:
- Run the generated tests and confirm they pass
- Verify coverage of success and failure paths
- Check for proper mock cleanup between tests

## Best Practices

- Mock external dependencies (database, HTTP clients, file system)
- Use descriptive test names that explain the scenario
- Test one behavior per test case
- Keep tests independent and isolated
- Use factories for creating test data
- Clean up state between tests
- Test both success and failure paths
