# E16 A-R1 Crop-Attainment Forensic Diagnosis

Evidence role: post-run forensic diagnosis of completed TRAINING artifacts only. No new gameplay, treatment, optimization, capacity-anchor selection, or Stage B execution was performed.

## 1. Executive diagnosis

`MODEL_VALIDITY` remains **STRONGLY SUPPORTED**. The observed failure is a `POLICY_REALIZATION` failure, not a model falsification. Gameplay `IMPLEMENTATION_FIDELITY` remains verified by the R1 hashes, completed run manifest, corrected applied-action ledger, and test suite. One seat-dependent state-row timestamp defect is documented as an `OBSERVABILITY` limitation and reconstructed from `day/hour`; it does not change the capacity-gate outcome.

The dominant mechanism is the **PLANTING / REPLANTING LOOP**. It has two directly supported components:

1. The frozen dispatcher treats `yield_units > 0` as sufficient harvest readiness, whereas the engine also requires crop age to reach `first_yield_day`. Across R1, 5,804 of 5,804 failed crop-HARVEST attempts occurred before that engine maturity threshold.
2. Every episode directly exposes at least one nominal working-set tile as `WEED`, but the frozen dispatcher has no `DIG` branch and R1 contains zero executed `DIG` events. A lost tile can therefore become a permanent sink that seed purchases and available workers cannot restore.

This is an interdependent chain: intermittent workforce availability and high transit load consume capacity and can increase missed or late crop service; premature HARVEST dispatch wastes further actions; crop losses create `WEED`; absence of weed recovery makes those losses irreversible. The irreversible sink is the dominant explanation for failure to **maintain** the working set. Routing and workforce are `SECONDARY`, not sufficient single causes.

Confidence: **HIGH** for the loop defect and irreversible sink; **MODERATE** for the relative upstream contributions of routing, workforce renewal, and capital pacing.

## 2. Data provenance & integrity

Repository preflight:

| Item | Observation |
|---|---|
| Branch | `main` |
| Commit | `4ff5c8541a10b7e6188d1625cbe2f104936a25be` (`Close E16 Stage A corrected replication`) |
| Initial `git status --short` | only `docs/prompts/E16_A_R1_CODEX_FORENSIC_DIAGNOSIS_PROMPT.md` was untracked |
| R1 manifest | `results/e16/stage_a_r1/E16_STAGE_A_R1_RUN_MANIFEST.json`, `COMPLETED`, 28 runs |
| Episode summaries | 28 `E16-A-R1-*.json` files |
| Event ledgers | 28 `E16-A-R1-*.events.jsonl` files |
| Config/cell metadata | R1 frozen config and per-run `cell_config` / manifest entries |
| Existing derived metrics | R1 episode telemetry, `E16_STAGE_A_R1_ANALYSIS.md`, `E16_STAGE_A_R1_COMPARISON.md` |
| Existing gate result | `E16_STAGE_B_GATE_R1.json` |
| Diagnostic integrity report | `E16_A_R1_DIAGNOSTIC_INTEGRITY.json` |

All 28 summary hashes match the run manifest. The frozen references also match their declared SHA256 values:

| Artifact | SHA256 status |
|---|---|
| Frozen design | `786d6aaf...ddc0c` MATCH |
| Watering semantic clarification | `fce78407...627d3` MATCH |
| Predecessor config | `4c6ca430...4ec92` MATCH |
| R1 config | `f37496d1...f199` MATCH across every episode |
| Predecessor treatment build | `8a897209...355e` MATCH |
| R1 treatment build | `7f331511...e1a8` MATCH |
| Frozen opponent | `604bd620...b8abb` MATCH |

The full repository suite passed `143/143`; pytest emitted only a cache-write permission warning.

**Observability qualification.** In all 14 treatment-seat-1 summaries, `state_rows.step` is constant `0`; the same rows have valid monotonic `day/hour`, and their ledgers have valid monotonic `step`. Diagnostic time is therefore reconstructed deterministically as `day * 24 + hour`. The frozen reported attainment values are retained as gate facts; corrected diagnostic-window values are reported separately. Corrected medians remain A02 `0.5000`, A07 `0.4706`, and A04 `0.3600`, all far below `0.80`. `STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR` and `C*=NONE` are unchanged.

## 3. Working-set reconstruction

The reconstruction uses one state row per hour/turn and the frozen steady window, Day 3 through Step 671 inclusive. `target_gap(t) = crop_target - active_crop_surface(t)`. Endgame shutdown Steps 672-719 is excluded from all steady-window metrics.

| Cell | Target | Reported attainment | Reconstructed attainment | Peak active / target | First 50% | First 80% | First 100% | Steady final active | Median / max gap | Cumulative gap tile-steps |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A01 | 10 | 0.0000 | 0.0000 | 10/10 | 8 | 13 | 15 | 0.0 | 10 / 10 | 5,304.0 |
| A02 | 10 | 0.4750 | 0.5000 | 10/10 | 9 | 11 | 20 | 1.0 | 5 / 9 | 3,534.0 |
| A03 | 25 | 0.1600 | 0.1600 | 17/25 | 10 | NR | NR | 0.0 | 21 / 25 | 13,556.0 |
| A04 | 25 | 0.3000 | 0.3600 | 16/25 | 15 | NR | NR | 2.0 | 16 / 23 | 10,447.5 |
| A05 | 17 | 0.3529 | 0.3529 | 15/17 | 9 | 15 | NR | 0.0 | 11 / 17 | 7,416.0 |
| A06 | 25 | 0.3200 | 0.3600 | 16/25 | 15 | NR | NR | 1.0 | 16 / 24 | 10,729.5 |
| A07 | 17 | 0.4706 | 0.4706 | 15/17 | 9 | 15 | NR | 1.5 | 9 / 16 | 6,294.0 |

Times are median steps after reconstructed T0; `NR` means the threshold was never reached in the pre-shutdown window. Cumulative gaps are medians across the four cell episodes and are not normalized across targets.

The summary telemetry does not retain a full-board tile-state history. `active`, `surviving`, and `harvest-ready` counts are direct state telemetry. Harvested-to-replanted tile pairs are derived from exact executed events at the same position. WEED counts are conservative lower bounds from actor-position snapshots, not complete board censuses.

## 4. Temporal anatomy of crop-target deficit

The HIGH cells show two distinct regimes:

| Cell | Initial attainment | Maintenance evidence | Fraction steady time >=80% | First drop below 50% after reaching 80% | Peak-to-steady-end decay |
|---|---|---|---:|---:|---:|
| A02 | reaches 10/10 | falls to median 1 active | 0.0383 | 261 steps after T0 | 9 tiles |
| A07 | reaches 15/17 | falls to median 1.5 active | 0.0100 | 69 steps after T0 | 13.5 tiles |
| A04 | reaches only 16/25 | never reaches 80%; falls to median 2 active | 0.0000 | not applicable | 14 tiles |

A02 is direct evidence of **failure to maintain** after complete initial attainment. A07 demonstrates both incomplete initial attainment and strong maintenance decay. A04 demonstrates an initial capacity ceiling plus later decay. The collapse is already present before the frozen endgame shutdown, so it is not an endgame artifact.

Direct working-set WEED observations begin during the productive phase and persist late: cell medians are 5 unique nominal tiles in A02, 10.5 in A07, and 18.5 in A04. The last WEED observations occur near Steps 710, 716.5, and 708 respectively. These counts are lower bounds because the ledger snapshots only the tile occupied by an acting unit.

## 5. Routing analysis

Applied movement actions consume a large share of observed treatment actor events in the HIGH cells:

| Cell | Target | Movement share | Movement per executed crop action | Steady productive share |
|---|---:|---:|---:|---:|
| A02 | 10 | 0.6060 | 18.76 | 0.1518 |
| A07 | 17 | 0.6211 | 13.07 | 0.1694 |
| A04 | 25 | 0.6765 | 10.64 | 0.1624 |

The movement share rises by about 7.1 percentage points from HIGH/10 to HIGH/25 and is consistent with growing spatial service cost. It does not, however, establish routing as the single cause: movement per executed crop action decreases rather than increases across the same cells, and large gaps persist when the full workforce is present while 17-26% of observed gap-period actor events are pass/no-op.

Classification: **SECONDARY**. The ledgers support a high transit load and a target-scaling association, but no existing R1 cell manipulates routing independently. The precise causal contribution is therefore not identifiable.

## 6. Workforce/action-capacity analysis

All cells reach a peak capacity of 11 actors (farmer plus 10 hands), but nominal workforce is not continuously available:

| Cell | Mean steady capacity | Fraction at full 11 | Fraction at farmer-only 1 | Median target gap at full 11 | Pass/no-op share during full-capacity gaps |
|---|---:|---:|---:|---:|---:|
| A02 | 7.53 | 0.6467 | 0.3117 | 7.0 | 0.2572 |
| A07 | 9.22 | 0.6725 | 0.0433 | 14.5 | 0.2442 |
| A04 | 6.38 | 0.5250 | 0.4267 | 21.0 | 0.1745 |

Intermittent renewal materially lowers the action supply, especially at target 25. It plausibly increases service latency and crop loss. Yet availability alone is not sufficient: even state rows with all 11 actors have large median gaps, and pass/no-op events remain observable while those gaps exist.

Effective capacity is further reduced by premature crop-HARVEST attempts. Cell-median failure rates are A02 `0.9222`, A07 `0.8926`, and A04 `0.8915`; every failed attempt is before the engine crop-specific `first_yield_day`. This is a dispatch-demand defect, not an exogenous shortage of workers.

Classification: **SECONDARY** in the causal chain. A pure workforce-saturation explanation is contradicted; intermittent capacity remains an upstream amplifier.

## 7. Seed replenishment analysis

| Cell | Deficit steps with any seed | Deficit steps with all three seed types | Executed seed-buy failures | Final seed inventory | Seed quantity bought after last PLANT |
|---|---:|---:|---:|---:|---:|
| A02 | 1.0000 | 0.2467 | 0 | 9.0 | 1.0 |
| A07 | 1.0000 | 0.9008 | 0 | 15.5 | 1.0 |
| A04 | 1.0000 | 1.0000 | 0 | 23.0 | 2.5 |

Across all 28 episodes, 544 seed-buy orders execute and zero fail. Twenty-six episodes have positive seed inventory at every sampled steady-window target-gap step. The two exceptions are the paired A03/S1802163452 episodes, where any-seed availability is `0.6617`; both nevertheless finish with 25 seeds and attainment `0.16`.

The acquisition-to-activation chain fails downstream of purchase: seed remains available while target gaps and WEED observations persist. Crop-specific short shortages may contribute to some A02 replant delays, but total or sustained seed stockout is not supported as the current primary bottleneck.

Classification: **NOT_SUPPORTED** as primary; a localized secondary role in A03/A02 remains possible.

## 8. Plant/replant loop analysis

This is the strongest causal family.

**Direct static evidence:**

- The frozen policy creates `PLANT` tasks only when a nominal tile is exactly `None`.
- It has no `WEED` task group and emits no `DIG` action.
- The engine requires `DIG` to clear a WEED tile before PLANT can succeed.
- The policy dispatches HARVEST on `yield_units > 0`; the engine also requires `day - planted_day >= first_yield_day`.

**Direct and derived R1 evidence:**

- All 28 episodes directly observe WEED on at least one nominal crop position; 329 distinct episode-position observations are recorded in aggregate.
- Zero `DIG` attempts and zero executed `DIG` events occur in all 28 ledgers.
- There are 5,804 failed crop-HARVEST attempts versus 655 executed; all 5,804 failures occur before the engine maturity threshold.
- Telemetry records 583 crop-loss transitions. Because this metric relies on event reconciliation, it is corroborative; the direct WEED and zero-DIG findings carry the causal conclusion.

| Cell | Executed / failed crop harvest | Median matched harvest->replant | P90 matched latency | Unmatched pre-shutdown harvests | Unique WEED tiles observed |
|---|---:|---:|---:|---:|---:|
| A02 | 13.0 / 154.0 | 61.5 steps | 190.0 | 5.0 | 5.0 |
| A07 | 46.5 / 388.0 | 22.25 steps | 34.25 | 22.5 | 10.5 |
| A04 | 23.5 / 192.5 | 87.75 steps | 277.6 | 14.5 | 18.5 |

Matched latencies apply only to executed harvests later followed by an executed PLANT at the same tile. Loss-to-WEED gaps are effectively right-censored for the full episode because no clearing event occurs. This is why seed purchases and later workforce availability cannot recover the nominal working set.

Classification: **PRIMARY**.

## 9. Market/capital pacing analysis

| Cell | Median steady cash | Minimum cash | Deficit steps above $300 floor | Mean workforce capacity | Final money |
|---|---:|---:|---:|---:|---:|
| A02 | $2,217.50 | $300 | 0.6800 | 7.53 | $21,230.50 |
| A07 | $4,247.75 | $300 | 0.9425 | 9.22 | $27,076.00 |
| A04 | $1,183.00 | $300 | 0.5600 | 6.38 | $19,987.00 |

The frozen floor is active during parts of A02 and A04 and may delay renewal or some acquisition. This supports a secondary market-to-workforce pathway. It does not explain persistent late crop gaps: cash is above the floor for most A07 deficit steps, all R1 seed-buy requests execute, and final seed inventories remain substantial.

Classification: **SECONDARY** through workforce/renewal pacing; **NOT_SUPPORTED** as the direct primary crop-attainment cause.

## 10. Cross-cell comparison

Water effects at constant target remain material but incomplete:

- A02 HIGH/10 versus A01 LOW/10 raises reported attainment from `0.0000` to `0.4750` and paired final money by `$1,576`, yet A02 maintains >=80% target for only `3.83%` of the reconstructed steady window.
- A04 HIGH/25 versus A03 LOW/25 raises reported attainment from `0.1600` to `0.3000` and paired final money by `$8,587`, yet A04 never reaches 80% target and ends the steady window at median 2/25 active.
- The frozen paired interaction remains `+$5,180.50`; it is economic evidence, not proof of capacity attainment.

HIGH target scaling isolates the operational gradient:

| Cell | Target | Reconstructed attainment | Peak fraction | Movement share | Mean capacity | Full-capacity median gap | Final money |
|---|---:|---:|---:|---:|---:|---:|---:|
| A02 | 10 | 0.5000 | 1.0000 | 0.6060 | 7.53 | 7.0 | $21,230.50 |
| A07 | 17 | 0.4706 | 0.8824 | 0.6211 | 9.22 | 14.5 | $27,076.00 |
| A04 | 25 | 0.3600 | 0.6400 | 0.6765 | 6.38 | 21.0 | $19,987.00 |

Target scaling worsens initial reach, transit share, and absolute gap. The same irreversible WEED mechanism is present at every target, so R1 cannot assign a clean marginal causal share to target-induced routing versus workforce versus loop recovery.

## 11. A07 forensic case

A07 is economically promising but is neither an optimum nor `C*`. Its cell medians combine `$27,076` final money, `$16,505.50` crop-product revenue, and `$19,163.50` livestock-product revenue with only `0.4706` crop-target attainment.

The selected representative episode is `E16-A-R1-A07-S1678077158-P1`, chosen by minimum normalized distance to the cell medians of final money and attainment. Its event-level trace shows:

- active crops reach 15/17 by Step 18 (17 steps after T0), then fall below 50% by Step 70;
- 45 crop HARVEST events execute and 357 fail before maturity;
- 22 harvests are followed by matched replants, median latency 22.5 steps;
- 11 nominal positions are directly observed as WEED, with no DIG action;
- steady-window final active count is 1, while final seed inventory is 16;
- 90% of sampled deficit steps have cash above the floor;
- final money is `$26,473`, supported by `$15,811` crop and `$19,361` livestock realized revenue.

Thus high economic return coexists with low nominal capacity because early/partial crop production and livestock revenue remain profitable even after the crop working set collapses. Profit does not satisfy the capacity gate.

Exact milestones and day-level event aggregations are in `E16_A_R1_SELECTED_EVENT_TRACE.csv` and `E16_A_R1_SELECTED_EVENT_TRACES.md`.

## 12. Falsification tests

| Hypothesis | Expected if primary | R1 confirming evidence | R1 falsifier / counterexample | Classification |
|---|---|---|---|---|
| Routing / transit overhead | Movement share rises with target; gaps track transit load | HIGH movement share rises `0.6060 -> 0.6211 -> 0.6765` | Movement per executed crop action falls; full-capacity gap periods still contain pass/no-op; no routing intervention exists | SECONDARY |
| Workforce / action capacity | Target gaps occur mainly when available capacity is low and actor slots are saturated | Mean capacity is below 11 and farmer-only periods are frequent in A02/A04 | At full capacity, median gaps are 7/14.5/21 and pass/no-op shares are 17-26% | SECONDARY |
| Seed replenishment | Gap periods coincide with zero required seed and close after acquisition | A03 has partial stockout; some A02 crop-specific shortage remains possible | Any seed is present in every sampled HIGH deficit step; zero seed-buy failures; large terminal inventories | NOT_SUPPORTED as primary |
| Planting / replanting loop | Initial reach is followed by loss; harvest/replant is delayed; blocked tiles persist | A02 reaches 100%, then decays; 28/28 expose WEED; 5,804 immature HARVEST failures; long replant latency | Potential falsifier would be successful DIG/recovery or sustained high attainment despite weeds; neither occurs | PRIMARY |
| Market pacing / capital | Deficits coincide with floor binding, failed purchases, or unavailable hires | Floor binds part-time and workforce availability is intermittent | A07 has cash above floor on 94.25% of deficit steps; all seed buys execute; gaps persist with seeds/cash | SECONDARY |
| WATER remains primary | HIGH cells should show low execution/continuity aligned with collapse | A small residual missed-water fraction remains | HIGH execution is `0.8898-0.9416`, continuity about `0.96`, but all HIGH cells fail attainment | NOT_SUPPORTED as primary |

## 13. Bottleneck classification

| Candidate | Classification | Evidence class and rationale |
|---|---|---|
| Planting / replanting loop | **PRIMARY** | DIRECT no-DIG policy/ledger and WEED observations; DERIVED immature-HARVEST failures, latency, and decay |
| Routing / transit overhead | **SECONDARY** | DERIVED high movement share and scaling; causal share UNRESOLVED without routing intervention |
| Workforce / action capacity | **SECONDARY** | DIRECT state capacity; DERIVED intermittent availability; contradicted as sole cause by full-capacity gaps and idle/no-op |
| Seed replenishment | **NOT_SUPPORTED** as primary | DIRECT executed acquisitions and positive inventories; crop-specific transient role remains UNRESOLVED |
| Market pacing / capital | **SECONDARY** | DIRECT cash/floor and market events; contradicted as sole cause by high-cash persistent gaps |
| WATER dispatch | **NOT_SUPPORTED** as primary | DERIVED corrected HIGH execution/continuity from direct applied-action events, plus persistent low attainment |

The causal chain best supported by R1 is:

`routing + intermittent workforce + premature harvest dispatch -> service/action waste and crop loss -> WEED -> no DIG -> no PLANT -> irreversible target gap`.

## 14. Evidence limitations

1. Treatment-seat-1 `state_rows.step` is not seat invariant. Day/hour reconstruction is deterministic and leaves the gate blocked, but the frozen reported medians must not be silently replaced.
2. Ledger tile snapshots cover unit positions, not the entire board. Unique WEED counts are lower bounds. Full weed-duration tile-time is not reconstructible.
3. `crop_losses` is a derived transition metric whose removal reconciliation uses ledger payloads; it is treated as corroboration, not the sole proof of loss.
4. No R1 cell independently manipulates routing, workforce renewal, maturity-aware harvest dispatch, weed recovery, or capital pacing. Relative causal shares among upstream mechanisms remain unidentified.
5. Only two seeds and one frozen opponent are represented. Findings are strong for the deterministic policy mechanism but performance magnitudes remain seed- and opponent-conditional.

## 15. Implications for next TRAINING decision

The next TRAINING decision should test whether restoring a complete crop lifecycle changes capacity realization while preserving the now-verified watering semantics. The question must isolate the downstream lifecycle mechanism from workforce, routing, target, crop mix, market floor, and opponent. R1 does not justify changing gate thresholds, selecting Crop 17 as an optimum, selecting `C*`, or executing Stage B.

# SUPERVISOR DECISION INPUT

### Dominant diagnosis

PRIMARY BOTTLENECK: PLANTING / REPLANTING LOOP (irreversible WEED sink plus harvest-readiness mismatch)

### Supporting evidence

- All 28 R1 episodes directly expose nominal crop positions as WEED, while all 28 ledgers contain zero executed DIG events (`E16_A_R1_EVIDENCE_TABLE.csv`, `GLOBAL-001`).
- A02 reaches 10/10 but decays to median 1 active; A07 peaks at 15/17 and decays to 1.5; A04 peaks at 16/25 and decays to 2 before shutdown (`E16_A_R1_CELL_DIAGNOSTIC_SUMMARY.csv`).
- 5,804/5,804 failed crop-HARVEST attempts occur before the engine first-yield-day precondition; HIGH-cell failure-rate medians are `0.8915-0.9222` (`E16_A_R1_EVIDENCE_TABLE.csv`, `GLOBAL-002`).
- Every sampled HIGH-cell deficit step has positive seed inventory; all 544 R1 seed-buy orders execute and zero fail, yet HIGH terminal seed medians are 9-23 (`E16_A_R1_EPISODE_DIAGNOSTIC_SUMMARY.csv`).
- At full 11-actor capacity, HIGH-cell median target gaps remain 7, 14.5, and 21, with 17-26% pass/no-op among observed actor events (`E16_A_R1_CELL_DIAGNOSTIC_SUMMARY.csv`).

### Competing explanation

WORKFORCE / ACTION CAPACITY plus ROUTING / TRANSIT OVERHEAD is the best alternative and likely an upstream amplifier: HIGH movement shares are `0.6060-0.6765`, and mean workforce capacity is only `6.38-9.22`. It is weakened as a complete explanation because large target gaps and pass/no-op events persist at full capacity, while WEED tiles remain non-actionable.

### Identifiability gap

The 28 runs cannot identify how much attainment would be recovered by maturity-aware HARVEST dispatch alone versus WEED recovery alone, nor the remaining marginal effects of routing and workforce once the crop lifecycle is complete.

### Recommended next experimental question

Does restoring maturity-valid HARVEST dispatch and loss-to-WEED recovery, while holding WATER priority, crop target, workforce schedule, routing, crop mix, market floor, seeds, opponent, and gate fixed, increase steady crop-target attainment without degrading watering continuity?

### Stage B status

STAGE B: BLOCKED
C*: NONE
