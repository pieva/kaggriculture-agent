# E16 Watering Semantics Clarification

**Semantic version:** `e16.watering_dispatch_precedence.v1`  
**Status:** normative clarification for corrected replication `E16-A-R1`  
**Predecessor design:** `E16_TRAINING_DESIGN_FROZEN.md`

## Canonical meaning

`watering_dispatch_priority` is a controlled policy variable that determines
the relative precedence of WATER requests against other concurrently eligible
action classes when irrigation demand exists.

It is not:

- a target percentage of crop-day watering needs;
- a quota or coverage fraction;
- a fixed count of crop tiles to select;
- an observed execution rate;
- a fixed-prefix eligibility rule.

The frozen values remain:

```text
LOW  = 0.20
MID  = 0.45
HIGH = 0.70
```

They map deterministically to the WATER class rank in the existing ordered task
groups:

| Level | WATER insertion rank | Relative behavior |
|---|---:|---|
| HIGH 0.70 | 0 | WATER precedes every other task class |
| MID 0.45 | 3 | WATER follows fertilizer collection, animal harvest, and CARE |
| LOW 0.20 | 6 | WATER follows all other existing task classes |

Rank 0 is the highest precedence. The non-WATER task order is unchanged.

## Eligibility and realization

Every active, unwatered crop need is included in the WATER candidate set at
every level. No level slices, samples, or permanently excludes a fraction of
that set. Within WATER, the existing deterministic nearest-target rule and
coordinate tie break apply. With sufficient actors, time, and route capacity,
100 percent of the eligible needs can be served at LOW, MID, or HIGH.

The three quantities remain distinct:

```text
watering_dispatch_priority  controlled policy parameter
watering_execution_rate     observed successful crop-day WATER effects / needs
watering_continuity         observed temporal consistency of that service
```

Changing dispatch precedence may change realized coverage through competition
for actor turns. It never assigns the realized metric directly.

## Frozen boundary

This clarification changes only the operational meaning and implementation of
`watering_dispatch_priority`. All numeric Stage A cells, controls, seeds, seat
swap, opponent, engine version, and gate thresholds remain unchanged.

The original 28 Stage A runs retain the original treatment and config hashes.
Only the future corrected replication `E16-A-R1` may use this clarification and
its new versioned artifacts.
