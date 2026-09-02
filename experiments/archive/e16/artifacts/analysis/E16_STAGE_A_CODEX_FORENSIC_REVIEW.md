# E16 Stage A Codex Forensic Review

**Review role:** independent forensic review  
**Evidence role:** `TRAINING` under review; no new evidence generated  
**Dataset:** 28 original E16 Stage A episodes  
**Review date:** 2026-08-29  
**New runs executed:** 0

## 1. Scope and method

This review used all mandatory design, implementation, execution, manifest,
instrumentation, analysis, gate, and Antigravity diagnosis sources. It also
inspected the frozen treatment snapshot, live E16 modules, the four E16 test
files, all 28 result JSON files, and all 28 event ledgers.

Read-only reconstruction parsed ledger order by `(day, hour)`. The engine
invokes one unit-action block per player in player order and each block begins
with `unit:0`. Every one of the 20,160 episode-hours contained exactly two such
blocks, so this provides an exact reconstruction of player 0 versus player 1
for the recorded engine version. It is useful forensic recovery, not an
acceptable substitute for correct first-party attribution.

## 2. Integrity baseline

| Check | Verified result |
|---|---|
| Treatment artifact SHA-256 | `8a897209ca331f9be21e430107b2452bb5b26df9e8d5b88c015b052a5185355e` |
| Frozen configuration SHA-256 | `4c6ca43025d5a95acd6b2c8c5eb51a17a4bc4cadd672146055c317d54864ec92` |
| Frozen opponent SHA-256 | `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb` |
| Stage A result files | 28/28 present; all `completed=true` |
| Stage A event ledgers | 28/28 present |
| Result hashes | 28/28 match the run manifest |
| Frozen seeds | only `1678077158`, `1802163452` |
| Seat protocol | treatment seats 0 and 1 for every cell/seed |
| Cells | only A01-A07; 4 runs per cell |
| Post-freeze treatment substitution | none; all 28 embed the expected three hashes |

The baseline is intact. The defects below belong to the frozen implementation
and measurement path; they are not caused by artifact substitution.

## 3. F1 - watering semantics

### 3.1 Code-level finding

The formula is confirmed in both `experiments/archive/e16/source/agricola/e16/policy.py:267-270` and the
byte-for-byte treatment snapshot at
`experiments/archive/e16/artifacts/manifests/E16_TREATMENT_BUILD.py:267-270`:

```python
water_quota = math.ceil(watering_priority * len(self.watering_needs))
remaining_water = max(0, water_quota - len(self.watering_successes))
water_targets = water_targets[:remaining_water]
```

Operationally:

- `watering_needs` and `watering_successes` are cleared at each day boundary;
- needs accumulate as unique active crop positions observed during that day;
- LOW/MID/HIGH cap the requested daily service at `ceil(p * N)`;
- WATER is the first dispatch group only until that quota is met;
- `water_targets` is sliced in fixed crop-plan/CROP_POSITIONS order;
- there is no rotation, age rule, debt counter, lottery, or fairness mechanism.

The excluded `(1-p)` share is therefore not merely lower priority. It is
ineligible after the quota is reached, and the same fixed suffix is repeatedly
excluded while it remains active. All reconstructed WATER requests in the 28
runs executed successfully, so this exclusion occurred without WATER action
failure and does not require workforce overload.

The engine initializes a planted crop with `consecutive_unwatered = 1` and
replaces it with WEED when the daily refresh raises the counter to at least 2
(`kaggriculture.py:216-224,769-785`). A fixed-prefix fractional budget can thus
cause mortality solely through selection, even when every requested WATER
action succeeds.

### 3.2 Frozen-semantics assessment

The inference that the quota is automatically incoherent with the frozen
treatment is not fully established. The design uses the name
`watering_dispatch_priority`, which suggests precedence, but defines 0.20,
0.45, and 0.70 as **successful-service intent**. The implementation prompt says
that the parameter must express service intent and must not be a synonym for
the realized `watering_execution_rate`. A fractional request budget is
compatible with one reading of those clauses; an all-needs-eligible precedence
weight is compatible with another.

The current code does not make the parameter equal to the observed metric: it
sets a request cap and actual engine effects remain separately measurable.
What is clearly unsupported is the unrecorded choice of a permanently fixed
eligible prefix. That choice materially changes mortality, survivor selection,
and the steady-state denominator.

**F1 classification: `PARTIALLY_CONFIRMED`.** The quota formula, fixed subset,
absence of fairness, and mortality mechanism are confirmed. The stronger claim
that any quota necessarily violates the frozen semantics is unresolved because
the frozen text admits two materially different operationalizations.

## 4. F2 - event ledger attribution

### 4.1 Defect and extent

`EngineEventLedger._register_state` maps `id(farm)` values obtained from
`state[0].observation.farms` (`telemetry.py:271-276`). The farm object passed by
the engine to `_apply_unit_action` does not retain that mapped identity, so the
wrapper falls back to `player = -1` (`telemetry.py:121-132`).

Across all 28 ledgers:

| Event family | Player values | Count |
|---|---:|---:|
| Unit actions, treatment and opponent | `-1` | 295,691 |
| Market orders | `0` | 17,600 |
| Market orders | `1` | 17,570 |

Thus F2 affects every farmer and farm-hand action for both players, not WATER
alone. Market attribution is unaffected because `_process_market` registers
state immediately before market recording and records the explicit player
loop.

`derive_episode_telemetry` filters successful WATER and all actor events with
`event["player"] == treatment_seat` (`telemetry.py:689-698,733-738`). The filter
therefore produces an empty set/list in every episode. This forces the reported
watering metrics to 0.0 and also corrupts action failure, crop-loss attribution,
transit, product collection/storage, purchase-to-activation lag, and other
unit-action-derived telemetry. State-derived crop surface/final state and
correctly attributed market cash flows are not affected by F2.

The E0 gate was a false negative: it checked the constant `treatment_seat`
metadata but had no invariant requiring each attributable unit event to have a
valid `player`.

### 4.2 Ex-post recovery boundary

The deterministic block reconstruction had no ordering anomaly in any of the
28 episodes and exactly reproduces Antigravity's treatment WATER counts. It can
recover player, unit action, target, request, execution, and success for this
dataset. Combined with the persisted state-derived aggregate need denominator,
it recovers the frozen global execution-rate ratio exactly.

It cannot recover `watering_continuity` to forensic-grade certainty. The raw
artifacts persist aggregate steady-window needs and daily active counts, but not
the per-day position sets used as the continuity denominators. In three A04
episodes, the aggregate unique crop-day denominator is larger than the sum of
daily maximum active counts, proving that count-only reconstruction loses
within-day membership information. Assumptions about crop identity or policy
behavior would be required.

The instrumentation wrapper calls the original engine mutation once and only
observes before/after state. No evidence indicates a policy or engine behavior
change caused by F2.

**F2 classification: `CONFIRMED`.** Behavioral impact is none; observability and
analysis impact are high and systematic.

## 5. Independent treatment reconstruction

`realized_water_requests` and `realized_water_successes` are per-episode means
over the four seed/seat runs. `reconstructed_execution_rate` is the median of
the exact episode ratios:

```text
unique successful treatment crop-day WATER effects in the steady window
/
persisted unique treatment crop-day watering needs in the steady window
```

This is the global ratio defined in the frozen design. The current telemetry
code instead stores the median of daily ratios (`telemetry.py:873`), an
additional R3 implementation-fidelity defect. A01 has a zero steady productive
denominator, so its rate is undefined rather than zero.

| cell_id | crop_target | assigned_watering_priority | implemented_watering_rule | realized_water_requests | realized_water_successes | reconstructed_execution_rate | reported_execution_rate | crop_target_attainment | final_money median | evidence_class |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| A01 | 10 | LOW 0.20 | daily `ceil(0.20*N)` fixed-prefix budget | 4.00 | 4.00 | `UNOBSERVABLE` (`N=0`) | 0.000 | 0.000 | 19,145.50 | CONTAMINATED |
| A02 | 10 | HIGH 0.70 | daily `ceil(0.70*N)` fixed-prefix budget | 53.00 | 53.00 | 0.900 | 0.000 | 0.200 | 15,274.00 | PARTIALLY_SALVAGEABLE |
| A03 | 25 | LOW 0.20 | daily `ceil(0.20*N)` fixed-prefix budget | 21.00 | 21.00 | 0.875 | 0.000 | 0.040 | 300.00 | PARTIALLY_SALVAGEABLE |
| A04 | 25 | HIGH 0.70 | daily `ceil(0.70*N)` fixed-prefix budget | 94.50 | 94.50 | 0.782 | 0.000 | 0.120 | 8,407.00 | PARTIALLY_SALVAGEABLE |
| A05 | 17 | MID 0.45 | daily `ceil(0.45*N)` fixed-prefix budget | 32.00 | 32.00 | 0.762 | 0.000 | 0.059 | 23,646.00 | PARTIALLY_SALVAGEABLE |
| A06 | 25 | MID 0.45 | daily `ceil(0.45*N)` fixed-prefix budget | 34.75 | 34.75 | 0.563 | 0.000 | 0.040 | 300.00 | PARTIALLY_SALVAGEABLE |
| A07 | 17 | HIGH 0.70 | daily `ceil(0.70*N)` fixed-prefix budget | 83.75 | 83.75 | 0.846 | 0.000 | 0.088 | 19,511.50 | PARTIALLY_SALVAGEABLE |

These recovered rates describe the actually implemented fixed-prefix quota.
They do not resolve continuity and do not convert the runs into valid evidence
for the alternative precedence interpretation.

## 6. F3 - crop-target-25 cash floor

The endpoint observation is replicated: A03 and A06 finish at exactly $300 in
all four seed/seat runs and acquire zero cows. The proposed Day-0 chronology and
permanent-stall mechanism are not accurate.

For A03, A04, and A06 alike, attributed Day-0 spending is:

| Category | Day-0 realized spend |
|---|---:|
| Land | $1,000 |
| Seeds | $1,500 |
| Workforce | $143 |
| Total | $2,643 |
| Cash after Day-0 spending | $357 |

A03 first reaches $300 on Day 3 through a HIRE from $301 to $300. A04 and A06
first reach $300 on Day 2 through HIRE. Every run in all three cells later rises
above $300 on Day 10 through a strawberry sale. A03/A06 subsequently spend or
lose that limited recovery and end at $300; A04 generates enough later crop cash
flow to buy four cows and remain above the floor at termination.

Therefore:

- crop target 25 creates a real opening-liquidity burden jointly with the
  common land purchase and hire schedule;
- reaching $300 is not unique to A03/A06 and is not a Day-0 event;
- the A03/A06 endpoint is not a permanent no-market-order lock from Day 0;
- the divergence from A04 depends on subsequent crop service and cash flow,
  whose causal interpretation is subject to F1;
- F2 does not invalidate this cash reconstruction because market events are
  correctly attributed.

**F3 classification: `PARTIALLY_CONFIRMED`. Evidence class:
`PARTIALLY_SALVAGEABLE`.** The observed liquidity burden and endpoints are
reliable descriptions of the implemented policy. The claimed timing and simple
direct causal chain are refuted, and the signal is not safe for a MODEL_SPEC
threshold update.

## 7. Evidence salvage matrix

| Conclusion | Classification | Reason | Affected defect | Can be recomputed without rerun | Safe for model update |
|---|---|---|---|---|---|
| A02-A01 final_money contrast | PARTIALLY_SALVAGEABLE | Exact paired median is -$4,737, with mixed signs; it describes the quota implementation only | F1 | YES, descriptively | NO |
| A04-A03 final_money contrast | PARTIALLY_SALVAGEABLE | Exact paired median is +$8,107 in all four pairs; assigned-treatment meaning remains unresolved | F1 | YES, descriptively | NO |
| Primary LOW/HIGH x 10/25 interaction | CONTAMINATED | The final-money difference-in-differences is +$12,916.50, but it estimates fixed-prefix quota behavior, not an unambiguous frozen treatment | F1 | NO, as a causal estimand | NO |
| Crop target 17 working-region signal | CONTAMINATED | High final money is livestock-dominated while crop attainment is 0.059-0.088; no capacity region is established | F1; unit telemetry loss | NO | NO |
| Crop target 25 cash-floor signal | PARTIALLY_SALVAGEABLE | Opening burden/endpoints are valid; Day-0 permanent-stall interpretation is false and water semantics confound recovery | F1 | YES, descriptively | NO |
| `watering_execution_rate` gate | INVALID as reported | All official values are false zeros; global rate is recoverable except undefined A01, but this is not the whole capacity gate | F2; R3 formula | PARTIAL | NO |
| `watering_continuity` gate | INVALID | Official zeros are false; per-day need sets are not persisted sufficiently for exact recovery | F2 | NO | NO |
| `crop_target_attainment` gate | PARTIALLY_SALVAGEABLE | State-derived values are valid for realized fixed-prefix behavior; all capacity cells fail 0.80 | F1 only for causal meaning | YES | NO |
| `C_STAR = NONE` | CONTAMINATED for intended treatment | It is logically true for the realized quota runs from attainment alone, but not established for the semantically unresolved frozen treatment | F1 | NO, for intended treatment | NO |
| Stage B blocking decision | VALID | No capacity cell passes valid attainment; measurement uncertainty can only reinforce the conservative stop | F1/F2 do not justify advancing | YES | NO; procedural only |

The original run and market facts remain valid provenance. No contaminated
contrast, operating-region signal, or threshold is suitable for MODEL_SPEC
update.

## 8. Three-layer assessment

### MODEL_VALIDITY: UNRESOLVED

The observed quota levels change realized WATER actions and outcomes, but the
scientific parameter has two plausible frozen meanings and one of the primary
service metrics is unrecoverable. The theoretical service-by-surface relation
is therefore neither cleanly supported nor falsified. Antigravity's
`STRONGLY_SUPPORTED` assessment is too strong.

### POLICY_REALIZATION: UNRESOLVED

The code faithfully realizes a deterministic fixed-prefix fractional budget.
The frozen text does not establish whether that is the assigned treatment or
whether all needs were meant to remain eligible under dispatch precedence.
The permanent-prefix selection rule is nowhere frozen. A normative semantic
clarification is required before a correct implementation can be specified.

### IMPLEMENTATION_FIDELITY: FAIL

All unit actions lose player attribution, E0 did not detect it, official unit
metrics are corrupted, and the stored episode execution-rate aggregation does
not implement the frozen global ratio. State and market subpaths remain usable,
but runner/telemetry/analysis do not correctly measure the full realized
treatment.

## 9. Gate and replication decision

For the original fixed-prefix quota runs, all three capacity candidates fail
the independently valid attainment threshold: A02 = 0.200, A04 = 0.120, and
A07 = 0.088. It remains correct not to execute Stage B. This does not establish
that `C* = NONE` for whichever treatment semantics is ratified.

Replication cannot be authorized until the design owner selects and records
one operational definition of `watering_dispatch_priority`. Once clarified,
the current fixed-prefix behavior must change under either credible repair
(all-needs precedence or a fair rotating service budget), and causal outcomes
cannot be reconstructed ex post. The required next experimental action is then
a full corrected Stage A replication, `E16-A-R1`, with the same DOE, seeds,
seats, and opponent in `results/e16/stage_a_r1/`. This review does not authorize
or execute it.

## 10. Final status

```text
FORENSIC_REVIEW_STATUS: COMPLETE

F1_WATERING_SEMANTICS:
  STATUS: PARTIALLY_CONFIRMED
  IMPACT: Fractional fixed-prefix quota and mortality mechanism confirmed; frozen precedence-versus-service-budget meaning remains ambiguous.

F2_LEDGER_ATTRIBUTION:
  STATUS: CONFIRMED
  BEHAVIORAL_IMPACT: NONE DETECTED
  OBSERVABILITY_IMPACT: HIGH; all 295691 unit actions for treatment and opponent have player=-1.
  ANALYSIS_IMPACT: HIGH; official WATER, continuity, and other unit-action-derived metrics are invalid, with only bounded ex-post salvage.

F3_CASH_FLOOR:
  STATUS: PARTIALLY_CONFIRMED
  EVIDENCE_CLASS: PARTIALLY_SALVAGEABLE

MODEL_VALIDITY: UNRESOLVED
POLICY_REALIZATION: UNRESOLVED
IMPLEMENTATION_FIDELITY: FAIL

E16_A_EVIDENCE:
  VALID: Integrity/provenance, completion, state outcomes, attributed market cash flows, and the conservative Stage B stop.
  PARTIALLY_SALVAGEABLE: Actual fixed-prefix WATER counts/global rates, descriptive final money, crop attainment, and target-25 liquidity burden.
  CONTAMINATED: Intended-treatment causal contrasts, primary interaction, crop-17 working-region signal, and C* inference.
  INVALID: Reported WATER execution/continuity and all other treatment unit-action-derived metrics that depend on player attribution.

C_STAR_NONE_VALID: UNRESOLVED
STAGE_B_BLOCK_DECISION_VALID: YES

REPAIR_REQUIRED: YES
REPAIR_IDS: R1, R2, R3

NEW_TREATMENT_BUILD_SHA256_REQUIRED: YES
NEW_CONFIG_SHA256_REQUIRED: YES

REPLICATION_DECISION:
  BLOCKED_PENDING_SEMANTIC_CLARIFICATION

PROPOSED_REPLICATION_ID: E16-A-R1

NEW_RUNS_EXECUTED: 0
STAGE_B_EXECUTED: NO

FILES_CHANGED:
  experiments/archive/e16/artifacts/analysis/E16_STAGE_A_CODEX_FORENSIC_REVIEW.md
  experiments/archive/e16/design/E16_IMPLEMENTATION_REPAIR_SPEC.md
```
