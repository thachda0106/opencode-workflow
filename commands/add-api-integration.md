---
description: Add integration with an external API or service
agent: feature-builder
subtask: false
---

# Add API Integration

> **Gates**: this command follows the tier model in `AGENTS.md`. T0/T1 run with no stops;
> T2 stops once, after the plan. Investigation notes, plan, and step list all live in
> `.ai/knowledge/plans/<slug>.md` — not in three root-level files.

Add integration with an external API or third-party service.

---

## 1 · INVESTIGATE — Exploration

**No code in this phase. Research only.**

1. Gather requirements from the user:
   - What API/service to integrate?
   - Which endpoints/operations are needed?
   - Authentication method (API key, OAuth, token)?
   - Rate limiting considerations?
2. Analyze existing integrations:
   - Check for existing HTTP client setup
   - Find similar integrations for pattern consistency
   - Review error handling patterns for external calls
3. Read project context if present (`context/PROJECT.md`, `context/CONVENTIONS.md`, `context/BOUNDARIES.md`); if those files are absent, infer conventions from existing code and say so
4. Write findings into `.ai/knowledge/plans/<slug>.md`

---

## 2 · PLAN — Integration Design

1. Define integration architecture:
   - Service/client structure
   - Error handling and retry strategy
   - Request/response DTOs
   - Authentication handling
   - Timeout configuration
2. Risk analysis (rate limits, downtime, breaking changes)
3. Write into `.ai/knowledge/plans/<slug>.md`

---

## 3 · STEPS — Breakdown

1. Break the integration into ordered steps:
   - [ ] Step 1: Create service/client for external API
   - [ ] Step 2: Implement authentication handling
   - [ ] Step 3: Add request/response DTOs
   - [ ] Step 4: Implement error handling and retries
   - [ ] Step 5: Add timeout configuration
   - [ ] Step 6: Write tests
2. Write into `.ai/knowledge/plans/<slug>.md`

---

## 4 · IMPLEMENT

- Implement tasks sequentially per `.ai/knowledge/plans/<slug>.md`
- Never hardcode API keys or secrets
- Use environment variables for configuration
- Implement circuit breaker pattern for critical APIs
- Add structured logging for API calls
- Handle rate limiting gracefully

---

## 5 · TESTING & VALIDATION

After implementation:
- Unit tests with mocked HTTP responses
- Test error scenarios (timeouts, 4xx, 5xx)
- Test retry logic if applicable
- Document the integration in project docs
