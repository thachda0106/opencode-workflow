---
description: Knowledge check — 5-7 implementation-grounded questions that test whether you can maintain this feature without AI
agent: build
---

# /ownership-check

Run the ownership verification for `$ARGUMENTS` (a feature slug, module path, or nothing = the
most recent change).

## 1. Load

- `.ai/knowledge/features/<slug>.md` if it exists — use it, do not start from scratch.
- The diff and the files it touched.

## 2. Refuse cheaply, when true

Print one line and stop, without ceremony:

```
Skipped: this change is T0/T1 with no new failure surface — nothing worth testing here.
```

Do not quiz on: renames, config, copy changes, style-only diffs, test-only changes.

## 3. Run

Load and follow `verify-ownership`.

- 5–7 questions, one per message, no hints in the message that contains the question.
- Write the answer key to `.ai/knowledge/ownership/<slug>.md` **before** asking the first question.
- Grade each answer immediately with what was missing (one sentence, with `file:line`).
- Finish with score, verdict band, gap list, and 1–3 exercises ≤20 min.

## 4. Close

```
Score: <n>/<max> (<%>) — <self-sufficient | guided | paired>
Gaps: <n> → see .ai/knowledge/ownership/<slug>.md
Next review: <trigger, e.g. before the next change to orders/**>
```

Then stop. Do not offer more exercises than the list, and do not re-ask failed questions in the
same session.
