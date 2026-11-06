---
name: verify-ownership
description: Test whether the engineer can independently explain and debug a feature they just shipped, using implementation-grounded questions with hidden answer keys. Use for T2 changes or on request — never for trivial diffs.
metadata:
  layer: knowledge
  stage: ownership
---


# Skill: verify-ownership

The point is not to quiz. The point is to find the specific places where the engineer's mental
model diverges from the code, while the change is still fresh and cheap to correct.

## When to use

| Use | Skip |
|-----|------|
| T2 implementation just finished | T0/T1 change with no new failure surface |
| Engineer says "I don't fully get this part" | Engineer is mid-debug and wants speed |
| Taking ownership of inherited code | Pure refactor with identical behaviour |
| Pre-interview / pre-review confidence check | Framework boilerplate |

Ask once. If declined, drop it and do not re-offer this session.

## Procedure

### 1. Build the question set (5–7 questions)

Read the diff and the knowledge report first. Every question must be answerable **only** from
this implementation — no general-knowledge questions.

Cover the five levels, in this order:

| Level | Question shape | What a wrong answer reveals |
|-------|----------------|-----------------------------|
| **Locate** | "Which file/function owns X?" | the map in their head is wrong |
| **Trace** | "A request hits <endpoint>. What happens between the controller and the row landing in <table>?" | they know pieces, not the chain |
| **Decide** | "Why is <mechanism> here instead of <obvious alternative>?" | the trade-off was never internalised |
| **Fail** | "The <dependency> times out after the write. What state is the system in?" | no failure model |
| **Operate** | "<Symptom> is reported in production. Where do you look first, and what do you check?" | cannot debug without AI |

Rules for the set:
- At least one Trace and one Fail question. These two carry the most signal.
- No question whose answer is a name, a constant, or a syntax detail.
- No question about code the engineer wrote by hand in this session — they already know it.
- Anchored to real identifiers from the diff. If you cannot cite `file:line` as evidence, the
  question is invalid.

### 2. Prepare the key privately

Before asking anything, write to `.ai/knowledge/ownership/<slug>.md`:

```
| # | Level | Question | Expected answer points | Evidence | Pass if |
```

`Pass if` is a criterion, not the answer: e.g. "names the tx boundary AND says the event is lost",
not "says 'transaction'".

Do not reveal this file, the answers, or hints at the end of each question. Reveal only what was
missing, after the engineer's answer.

### 3. Ask one at a time

- One question per message. Wait.
- Never bundle. Never answer your own question while waiting.
- If the answer is partially right: score it, name precisely what was missing, then move on.
- If the answer is "I don't know": score 0, give the shortest correct answer with a `file:line`
  pointer, and continue. Do not lecture.

Scoring per question: `2` = complete and correct · `1` = right shape, missing a load-bearing
detail · `0` = wrong or absent.

### 4. Verdict

```
score = sum / (2 × n)

≥ 80%   self-sufficient — you can maintain and debug this without me
50–79%  guided — one re-read path, then re-ask the failed questions next session
< 50%   paired — do not hand this feature over; walk the Tier A path together first
```

### 5. Produce the gap list

For each `0` or `1`, one line:

```
- <missing mechanism> → read <file:line–line> (≈N min) → be able to answer: <the question, rephrased as a statement you could explain>
```

Then 1–3 exercises, tied to the real code, each ≤20 minutes:

| Type | Example |
|------|---------|
| Predict | "Before running it: what will `select count(*) from outbox` return after you kill the app mid-checkout?" |
| Break | "Comment out the idempotency check, replay one webhook twice, explain the resulting rows." |
| Extend | "Add a `cancelled` state. List every path that must now handle it." |
| Trace-by-hand | "Follow order id 123 through the code, write the row states at each hop." |

### 6. File the result

Append to `.ai/knowledge/ownership/<slug>.md`:

```
Date · score · verdict · gaps (n) · next review: <date or trigger>
```

One line to `.ai/knowledge/index.md`.

## Anti-patterns

- **Trivia.** "What does the DTO validate?" is a lookup, not understanding.
- **Fake difficulty.** Asking about a line the AI wrote 4 minutes ago tests working memory.
- **Soft grading.** A `1` for an answer that missed the transaction boundary teaches the engineer
  to be vague. Be exact about what was missing.
- **Lecture after a wrong answer.** One sentence, one pointer, next question.
- **Re-asking the same set.** Re-ask only the failed questions, in a new phrasing, next session.

## Non-goals

- Performance reviews or capability judgements. This measures one feature, not a person.
- Interview practice (use the interview drills for that).
- Covering the whole codebase. Scope is one change or one module.
