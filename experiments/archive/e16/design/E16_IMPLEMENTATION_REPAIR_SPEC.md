# E16 Implementation Repair Specification

**Repair status:** implemented and E0-verified  
**Corrected replication:** `E16-A-R1`, ready but not executed  
**Semantic authority:** `E16_WATERING_SEMANTICS_CLARIFICATION.md`  
**Stage B:** blocked pending corrected Stage A gate

## 1. Frozen boundary and provenance

The repair preserves all Stage A factor/control values, cells A01-A07, seeds,
seat swap, opponent, engine version, and gate thresholds. The original 28 runs
and all 57 files under `results/e16/stage_a/` remain byte-for-byte unchanged.

```text
OLD_TREATMENT_BUILD_SHA256 =
8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e

NEW_TREATMENT_BUILD_SHA256 =
7f331511a235e409833a726a324a4cda9881f3c8836a1ee260a2d6f36b78e1a8

OLD_CONFIG_SHA256 =
4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92

NEW_CONFIG_SHA256 =
f37496d1653cfc78672632c7fb779fc07ee93897a22341cf54f2242290e9f199

OPPONENT_SHA256 =
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

The old treatment/config artifacts are retained at their original paths. The
new config records the predecessor hashes and these repair reasons exactly:

```text
semantic clarification
implementation repair
telemetry repair
```

## 2. R1 - watering dispatch semantics

```text
repair_id: R1
defect: watering_dispatch_priority was implemented as ceil(p * needs) fixed-prefix coverage instead of relative dispatch precedence.
files_affected:
  - experiments/archive/e16/design/E16_WATERING_SEMANTICS_CLARIFICATION.md
  - experiments/archive/e16/source/agricola/e16/policy.py
  - experiments/archive/e16/tests/test_e16_policy.py
  - experiments/archive/e16/artifacts/manifests/E16_TREATMENT_BUILD_R1.py
required_behavior: All current unwatered crop needs remain eligible. LOW/MID/HIGH insert the complete WATER candidate class at deterministic ranks 6/3/0 among the existing task classes; lower rank means higher precedence.
forbidden_behavior: No percentage target, quota, slicing, sampling, fixed-prefix exclusion, or direct assignment of observed watering metrics.
acceptance_test: Rank ordering, all-needs eligibility at every level, suffix eligibility, 100 percent service with sufficient capacity, and deterministic replay are covered by policy tests.
regression_test: A worker located on a former fixed-prefix suffix need must select WATER at LOW when no higher-priority competitor consumes the turn.
impact_on_frozen_semantics: Applies the authorized precedence clarification without changing numeric levels or any other DOE field/control.
requires_new_treatment_hash: YES
requires_new_config_hash: YES
status: PASS
```

Canonical rank mapping:

| Level | Rank | WATER precedence |
|---|---:|---|
| HIGH 0.70 | 0 | before all existing task classes |
| MID 0.45 | 3 | after fertilizer collection, animal harvest, CARE |
| LOW 0.20 | 6 | after all existing task classes |

The non-WATER task order is unchanged. Within WATER, deterministic nearest-task
routing and the existing coordinate tie break are preserved.

## 3. R2 - unit-action attribution

```text
repair_id: R2
defect: Cross-adapter farm object identity caused all original unit events to use player=-1.
files_affected:
  - experiments/archive/e16/source/agricola/e16/telemetry.py
  - experiments/archive/e16/source/agricola/e16/runner.py
  - experiments/archive/e16/tests/test_e16_telemetry.py
required_behavior: Attribute unit events from the engine's validated invocation cycle. Each transition has exactly one player block per registered player; a block starts at unit index 0 and player blocks follow engine player order. Record player, seat, actor_role, unit_index, cell, seed, transition context, requested payload, engine-applied payload, executed payload, and status.
forbidden_behavior: Object identity as the sole unit binding; player=-1 fallback; action-content inference; silent missing/duplicate player cycles.
acceptance_test: Integration probes for treatment P0/P1 and opponent P1/P0 verify every farmer event, role, seat, and attribution status.
regression_test: Invalid ordering or an incomplete/extra player cycle fails closed instead of emitting an unattributed event.
impact_on_frozen_semantics: NONE; the wrapper still calls the original engine mutation exactly once.
requires_new_treatment_hash: NO
requires_new_config_hash: YES
status: PASS
```

Telemetry schema `e16.telemetry.v2` adds:

```text
seat
actor_role
unit_index
engine_applied_payload
attribution_status
```

`requested_payload`, `engine_applied_payload`, and `executed_payload` remain
separate so engine validation rewrites and actual mutation can be audited.

## 4. R3 - derived watering metrics

```text
repair_id: R3
defect: Player attribution emptied the treatment WATER numerator, and episode execution rate incorrectly used median(daily rates) instead of the frozen global effects/needs ratio.
files_affected:
  - experiments/archive/e16/source/agricola/e16/telemetry.py
  - experiments/archive/e16/source/agricola/e16/analysis.py
  - experiments/archive/e16/source/agricola/e16/runner.py
  - experiments/archive/e16/tests/test_e16_telemetry.py
  - experiments/archive/e16/tests/test_e16_analysis.py
required_behavior: Persist unique per-day need/effect counts, compute the pooled episode execution ratio, compute continuity from daily ratios, expose formula/provenance/status, enforce [0,1], and make unobserved zero-denominator episodes gate-ineligible.
forbidden_behavior: Invalid-player effects, requested-but-not-executed WATER, duplicate crop-day effects, median daily rate substituted for pooled rate, or zero denominator treated as an observed pass.
acceptance_test: Synthetic unequal-denominator, known-continuity, duplicate-effect, bounds, and gate-ineligibility tests.
regression_test: Days 1/1 and 0/9 yield execution rate 0.10 and continuity 0.50, not median-daily execution 0.50.
impact_on_frozen_semantics: NONE; implements the frozen formulas.
requires_new_treatment_hash: NO
requires_new_config_hash: YES
status: PASS
```

For each steady productive day `d`:

```text
N_d = unique treatment crop positions with a watering need on d
S_d = unique positions in N_d with an executed treatment WATER effect on d
daily_watering_execution_rate_d = |S_d| / |N_d|
```

Episode formulas:

```text
watering_execution_rate = sum_d |S_d| / sum_d |N_d|
watering_continuity = count_d(daily rate >= 0.50) / count_d(productive days)
```

If there is no steady productive day, both bounded numeric fields are 0.0 for
serialization compatibility and `watering_metric_status` is
`NO_STEADY_PRODUCTIVE_DAYS`. The corrected gate requires status `OBSERVED` in
all four cell episodes, so an unobserved metric cannot qualify a cell.

## 5. Verification record

### Test suite

```text
pytest: 143 passed / 143 total
ruff check: PASS
ruff format --check: PASS after formatting
```

The suite includes regressions for:

1. HIGH > MID > LOW WATER precedence;
2. no fixed-prefix exclusion;
3. 100 percent eligibility/service with sufficient capacity;
4. deterministic dispatch;
5. treatment P0 and P1 attribution;
6. opponent P0 and P1 attribution;
7. no attributable unit event with `player=-1`;
8. seat/role/unit/cell/seed/action separation;
9. pooled execution rate with known unequal denominators;
10. continuity with known daily results;
11. duplicate effect suppression and `[0,1]` invariants;
12. unobserved metric gate exclusion;
13. legacy treatment/config hash preservation;
14. new treatment/config/semantic artifact consistency.

### E0 instrumentation gate

E0 ran only non-analytic smoke/probe episodes, with treatment in P0 and P1.
All checks passed, including attribution, role separation, WATER attribution,
metric bounds, and formula reconciliation.

```text
E0_STATUS: PASS
E0_EVENT_COUNT: 2722
E0_TREATMENT_SEATS: 0, 1
E16_A_R1_RUNS_EXECUTED: 0
```

## 6. Corrected replication boundary

The implementation and E0 gate are ready for a separately authorized full
corrected replication:

```text
replication_id: E16-A-R1
output_root: results/e16/stage_a_r1/
cells: A01, A02, A03, A04, A05, A06, A07
seeds: 1802163452, 1678077158
treatment_seats: 0, 1
episode_count: 28
opponent_sha256: 604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
overwrite_results/e16/stage_a/: PROHIBITED
stage_b: PROHIBITED_PENDING_CORRECTED_GATE
```

This specification does not authorize or execute the replication.

## 7. Final repair status

```text
REPAIR_SPEC_STATUS: READY
SEMANTIC_CLARIFICATION_APPLIED: YES
R1_WATERING_SEMANTICS: PASS
R2_LEDGER_ATTRIBUTION: PASS
R3_DERIVED_METRICS: PASS
TESTS: 143/143
E0_STATUS: PASS
ORIGINAL_STAGE_A_PRESERVED: YES
E16_A_R1_READY: YES
NEW_RUNS_EXECUTED: 0
STAGE_B_EXECUTED: NO
BLOCKERS: NONE
```
