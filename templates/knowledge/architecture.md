# <feature> — architecture

Mode: <Standard | Full Engineering> · Date: <YYYY-MM-DD>

## Component boundaries

| Component | Owns | Does not own | Boundary |
|-----------|------|--------------|----------|

## Dependencies

| From | To | Contract | Direction |
|------|----|----------|-----------|

## Architectural patterns

- <pattern followed> — copied from `<file:line>`; why it fits.
- <new pattern> — why the existing pattern was insufficient; cost.

## Data ownership

| Data | Owner | Readers | Written by | Consistency rule |
|------|-------|---------|------------|------------------|

## Integration points

| Integration | Protocol | Failure mode | Retry / timeout | Auth |
|-------------|----------|--------------|-----------------|------|

## Boundaries that must not be crossed

- <rule> — enforced by <test / import boundary / review convention>.

## Known limitations

- <limitation> — <consequence> — <revisit if>.
