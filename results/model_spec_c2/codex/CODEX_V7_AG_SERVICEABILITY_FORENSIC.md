# CODEX V7 vs AG — Serviceability Forensic

## 1. Executive Finding

Codex V7's livestock deficit is not caused by pasture geometry, pathfinding, insufficient wheat in the shed, or an intrinsically inadequate number of livestock-role hours after the herd is rebuilt. It is caused first by an unserviceable bootstrap and then by capability-unaware task dispatch and inefficient service sequencing.

All 24 observed escapes are the four day-0 bootstrap animals in each of the six canonical V7 episodes. Every one escapes at the same boundary, day 5 / step 120, after receiving no feed during the decisive day-4 service window even though the shed still contains 8 WHEAT. The controller has no COW or SHEEP specialist during that window: the intended livestock roles are worker indices W4 and W5, but the active roster is underfilled. Hard FEED tasks are consequently exposed to FLOAT and CROP workers that may travel to an animal without carrying wheat and cannot convert the trip into a legal feed action.

The immediate loss creates an eight-day empty-herd interval in most runs. A full 3-cow/3-sheep herd is not restored until day 14. That gap, rather than weak production from a continuously serviced herd, explains most of the observed Codex shortfall relative to the canonical AG evidence.

After reconstruction, local routes are almost always shortest paths, but macro-sequencing remains expensive. FLOAT_RESERVE is the largest single-role MOVE source, livestock workers perform about 98 pasture–shed–pasture loops per run, and approximately 344.5 moves per run belong to abandoned target commitments. PASS is similarly dominated by task visibility and role-local eligibility, not healthy slack.

The minimal correction is therefore a three-part serviceability change: bind bootstrap placement to a real feed owner, make feed dispatch inventory-aware before movement, and batch feed-first work within each livestock cluster. These changes can plausibly restore MILK to 80–93, WOOL to 62–74, and escapes to zero while retaining the crop routines responsible for V7's crop advantage.

## 2. Sources and Reproducibility

### Evidence read

- `results/model_spec_c2/codex/KAGGRICULTURE_C2_CODEX_V7_AG_SERVICEABILITY_FORENSIC_PROMPT.md`
- `results/model_spec_c2/antigravity/experiments/Q0_3X3/LUCCC_EXACT_Q0_3COW_3SHEEP_REPLICATION.md` and its canonical CSV
- `results/model_spec_c2/antigravity/experiments/ROUTINE_PLANNING/Q0_3X3_ROUTINE_WORKER_PLANNING_TEST.md` and its canonical CSV
- the AG cleanup report in the same evidence tree
- the current Codex V7 controller, its build report, and its canonical result artifacts
- the installed local Kaggriculture engine's animal end-of-day refresh logic

### Replay protocol

The current V7 agent was replayed locally and deterministically against the same inert pass policy for seeds 26090101, 26090102, and 26090103, from both player seats, with `episodeSteps=720`. This gives six episodes and reproduces the canonical V7 aggregate:

| Metric | Replayed V7 mean |
|---|---:|
| Final money | 39,265.67 |
| MILK | 28.17 |
| WOOL | 14.67 |
| Animal escapes | 4.00 |
| MOVE | 2,196.83 |
| Verified productive actions | 688.17 |
| PASS | 871.50 |
| MOVE / productive action | 3.1923 |

The replay wrapper observed controller inputs, emitted actions, next observations, role assignments, task claims, inventory, animal state, and day/hour boundaries. The engine has no persistent animal identifier, so animal identity was reconstructed deterministically as species + tile + placement day. This is sufficient here because the relevant bootstrap animals occupy stable, unique positions until escape.

### Reproducibility limitation on AG

The historical modules `antigravity_luccc_replication` and `antigravity_routine_planning` are no longer present after the documented cleanup. Therefore AG's step-level service delays, worker geometry, interrupt timing, and exact inventory movements cannot be independently replayed from the current repository. AG comparisons below are limited to the preserved reports and CSVs; no missing AG trace is reconstructed by assumption.

The preserved AG artifacts also contain a unit-accounting inconsistency. One exact-replication narrative reports 30 MILK and 18 WOOL, values consistent with its stated base revenues, while the canonical routine/forensic evidence track records approximately 93 MILK and 74 WOOL. This audit uses 93/74 as the requested canonical livestock benchmark and explicitly treats it as report-level evidence, not a newly reproduced trace.

## 3. AG vs Codex Production Contrast

| System/evidence track | Final money | Crops | MILK | WOOL | Escapes |
|---|---:|---:|---:|---:|---:|
| AG exact/control canonical | 37,997.67 | 24.70 | 93 | 74 | 0 |
| AG routine-planning canonical | 39,695.33 | 85.33 | 88 | 70 | 0 |
| Codex V7 replay | 39,265.67 | 135.17 | 28.17 | 14.67 | 4 |

Codex V7 is economically competitive only because its crop output is materially higher. Its livestock gap against the requested AG benchmark is approximately 64.83 MILK and 59.33 WOOL per episode. The contrast is structural:

- AG evidence reports zero escapes and continuous livestock service.
- V7 loses the entire bootstrap herd at day 5.
- V7 then has no animals for roughly eight days.
- V7 restores full livestock capacity only around day 14, leaving less than half of the episode for full-herd production.

The conclusion does not require assuming that every AG service mechanism is superior. Continuous animal availability alone explains a large portion of the production delta. V7's later herd does receive substantial feed service, but the early irreversible availability loss caps total product opportunities.

## 4. Animal Escape Timeline

The timeline is identical across the six deterministic replays unless otherwise noted.

| Time | Herd state | Serviceability observation |
|---|---|---|
| D0 | 2 cows + 2 sheep placed by bootstrap | Placement bypasses normal capacity admission and does not bind each cluster to a feed-capable owner. |
| D1–D3 | 2 cows + 2 sheep | Animals remain present. |
| D4 / S96 boundary | 2 cows + 2 sheep | Every bootstrap animal enters its first consecutive-unfed day. |
| D4 H0 | 2 cows + 2 sheep | Only W0/FLOAT_RESERVE is active at (4,4). W4/W5 livestock specialists do not exist. |
| D4 H18–H21 | 2 cows + 2 sheep | FLOAT/CROP workers claim or approach sheep FEED work without wheat; no legal FEED action results. |
| D4 H20 | 2 cows + 2 sheep | Shed contains 8 WHEAT. Per species, pending tasks include 2 FEED, 2 CARE, and 2 fertilizer collections; crop pending is 7 and current slack is -21. |
| D4 H23 | 2 cows + 2 sheep | W0 is at (2,4), W1/CROP_ZONE_0 at (4,2); no affected animal has received feed. |
| D5 / S120 boundary | 0 animals | All four bootstrap animals escape simultaneously in every episode. |
| D5–D12 | 0 animals in five runs | No livestock production is possible. |
| D12–D13 | partial rebuilding | One run buys 1 cow + 1 sheep on D12 and the remainder on D13; the other five start rebuilding on D13. |
| D14 | 3 cows + 3 sheep | Full herd is present in all runs. |

Across six episodes this yields exactly 24 escapes:

- 12 cows and 12 sheep;
- all placed on day 0;
- all lost at day 5 / step 120;
- zero FEED requests and zero FEED effects for those animals in the decisive D4 window;
- no evidence of feed stockout, because shed WHEAT is 8 at H20.

The local engine increments `consecutive_unfed` when an animal ends the day unfed and removes the animal once the value reaches 2. The observed D4 state and D5 boundary loss match this rule exactly.

## 5. Escape Root Causes

### Primary cause: FEED_NOT_STAGED

All 24 escapes are classified primarily as `FEED_NOT_STAGED`. Wheat existed centrally, but no worker carrying wheat completed service before the second unfed boundary. “Feed available in the shed” was incorrectly treated as equivalent to “feed serviceable at the animal.”

### Secondary cause: LEGALITY_STATE_ERROR

The controller can create and prioritize a hard FEED target globally, reserve it, and route a worker toward it without proving that the worker carries WHEAT. The legality condition is enforced only at the interaction point. A remote assignment can therefore be “hard and urgent” in planning state while still being impossible in execution state.

This is capability-unaware dispatch rather than a physical path failure:

- livestock roles without wheat can create a PICKUP WHEAT task;
- FLOAT and CROP roles can receive the global hard FEED target;
- those roles are not guaranteed to stage wheat first;
- the target may be claimed and approached, yet no FEED action can be emitted.

### Contributing cause: unserviceable bootstrap

Role identity is tied to worker index. COW and SHEEP specialists are W4 and W5, but the bootstrap animals exist before the roster and cash policy make those workers available. The placement path bypasses the capacity gate and does not assign a temporary feed owner. The system therefore admits four living obligations with no proven delivery chain.

### Causes rejected by the evidence

| Candidate cause | Verdict | Evidence |
|---|---|---|
| NO_FEED_AVAILABLE | Rejected | Shed has 8 WHEAT during the decisive D4 window. |
| PASTURE_TOO_FAR | Rejected | Completed livestock route segments have stretch 1.0 and short median distances. |
| ENGINE_ESCAPE_BUG | Rejected | Escape timing matches the documented two-day unfed rule. |
| RANDOM_VARIANCE | Rejected | Same four losses at the same boundary in all six deterministic runs. |
| DIRECT_CAPACITY_REJECTION | Rejected for these 24 | Bootstrap placement bypasses admission rather than being rejected by it. |

## 6. Livestock Service Cadence

The following values are V7 means unless a total is explicitly stated.

| Service measure | Value |
|---|---:|
| FEED requests/effects per run | 100.33 / 100.33 |
| Feed due animal-days | 734 total |
| Feed served on time | 602 / 734 = 82.02% |
| Feed due-to-effect delay | mean 7.67 h; median 7 h; max 13 h |
| CARE requests per run | 34.50 |
| CARE next-snapshot effects per run | 29.00 |
| CARE completed legal segments per run | 34.50 |
| Care served on time | 207 / 734 = 28.20% |
| Care due-to-action delay | mean 18.68 h; median 19 h; max 24 h |
| Product collection events per run | 21.17 |
| Collected MILK units per run | 28.17 |
| Collected WOOL units per run | 14.67 |
| Collection due-to-effect delay | mean 17.89 h; median 15 h; max 39 h |

The CARE difference between 34.50 legal completed segments and 29.00 next-snapshot effects is a boundary-observation artifact: approximately 5.5 actions per run cross the end-of-day transition and cannot be attributed by the simple next-snapshot detector. It is not evidence that the engine rejected those actions.

End-of-day pending load, averaged over a run's 30 days:

| Pending task | Count/run | Mean/day |
|---|---:|---:|
| FEED | 16.00 | 0.533 |
| CARE | 87.33 | 2.911 |
| FERTILIZER_COLLECTION | 25.50 | 0.850 |
| ANIMAL_COLLECTION | 5.50 | 0.183 |

V7's post-rebuild feed completion is materially better than its bootstrap outcome, but CARE and collection are late. This supports a priority/sequencing diagnosis: basic feed can often be completed once specialists exist, while lower-priority service and product extraction age in the queue.

## 7. Worker Geometry

### COW role

| Measure | Per run |
|---|---:|
| Shed returns | 57.50 |
| Shed-target commitments | 55.00 |
| Pasture→shed→pasture loops | 54.67 |
| Cross-cluster service | 0 |
| Empty MOVE while no target | 0 |
| Product collection events | 12.00 |

Completed COW service segments are short: FEED mean 1.04 moves, CARE 1.04, fertilizer collection 0.91, and animal-product collection 1.06. Medians are 1 and maxima are 2.

### SHEEP role

| Measure | Per run |
|---|---:|
| Shed returns | 32.83 |
| Shed-target commitments | 51.50 |
| Pasture→shed→pasture loops | 43.33 |
| Cross-cluster service | 0 |
| Empty MOVE while no target | 0 |
| Product collection events | 9.17 |

Completed SHEEP service segments are also bounded: FEED mean 2.12 moves, CARE 2.00, fertilizer collection 1.14, and animal-product collection 1.82. Maxima are 3–4 moves.

The geometry is therefore compact and stable. The inefficiency comes from repeated alternation between pasture and shed, not excessive distance within an individual route. Together, the two specialists execute approximately 98 pasture–shed–pasture loops per run.

Livestock roles also perform 44.83 fertilizer collections per run, 55.5% of the system total of 80.83, despite the dedicated FERTILIZER_LOGISTICS role. Inventory-task precedence forces product and fertilizer unloading and contributes to repeated shed returns. Feed-first batching and clearer fertilizer ownership can reduce loops without relocating pastures or changing the map.

## 8. MOVE Decomposition by Role

“Productive” below denotes emitted productive requests attributed by the action wrapper. The replay's engine-verified productive total differs by 2.5 per run because terminal/no-post-state and NO_OP attribution are treated differently.

| Role | MOVE/run | Productive/run | MOVE/productive | PASS/run | Target commitments/run | Mean target distance | MOVE/active role-day | Immediate backtracks | MOVE share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CROP_ZONE_0 | 357.17 | 124.67 | 2.865 | 109.00 | 144.33 | 2.63 | 13.74 | 3.83 | 16.26% |
| CROP_ZONE_1 | 305.17 | 94.83 | 3.218 | 164.50 | 116.33 | 2.67 | 12.21 | 3.33 | 13.89% |
| CROP_ZONE_2 | 327.50 | 106.33 | 3.080 | 102.67 | 123.17 | 2.62 | 13.74 | 2.00 | 14.91% |
| FERTILIZER_LOGISTICS | 291.67 | 64.33 | 4.534 | 104.50 | 131.33 | 2.63 | 13.89 | 7.50 | 13.28% |
| FLOAT_RESERVE | 444.67 | 94.67 | 4.697 | 154.67 | 204.00 | 2.81 | 14.82 | 9.50 | 20.24% |
| LIVESTOCK_COW | 214.67 | 113.00 | 1.900 | 127.33 | 178.67 | 1.21 | 9.68 | 0.00 | 9.77% |
| LIVESTOCK_SHEEP | 256.00 | 92.83 | 2.758 | 108.83 | 151.00 | 1.74 | 11.64 | 0.17 | 11.65% |

The three crop roles collectively account for 989.83 moves, or 45.06%, because they are three roles. FLOAT_RESERVE is the largest single-role source and has the worst MOVE/productive ratio. It is also the role most exposed to global hard targets and later target abandonment.

Route-optimality diagnostics separate path quality from sequencing quality:

| Role family | Completed-segment stretch | Daily macro stretch | Abandoned MOVE/run |
|---|---:|---:|---:|
| Crop | 1.029 | 1.601 | 64.50 |
| Livestock | 1.000 | 2.367 | 29.50 |
| Fertilizer | 1.004 | 1.771 | 101.33 |
| Float | 1.000 | 1.945 | 149.17 |

Completed routes are essentially shortest paths. Yet 344.50 moves per run, about 15.7% of all MOVE, belong to commitments that are later abandoned or superseded. The system is locally optimal and globally wasteful.

## 9. PASS Decomposition

| PASS classification | Count/run | Share |
|---|---:|---:|
| NO_LOCAL_TASK_BUT_GLOBAL_TASK_EXISTS | 518.50 | 59.50% |
| ROUTE_STATE_BUG | 250.17 | 28.71% |
| RESERVE_IDLE | 42.83 | 4.91% |
| WAITING_FOR_BIOLOGICAL_EVENT | 60.00 | 6.88% |
| Other classes | 0.00 | 0.00% |

Only RESERVE_IDLE plus WAITING_FOR_BIOLOGICAL_EVENT, 102.83 PASS/run or 11.8%, is clearly healthy slack. The remaining 768.67 PASS/run occurs while global or candidate work exists. Some role partitioning is intentional, but the magnitude shows that eligibility and state transitions prevent useful conversion.

Role decomposition:

| Role | PASS/run | No local/global exists | Route state | Biological wait | Reserve idle |
|---|---:|---:|---:|---:|---:|
| CROP_ZONE_0 | 109.00 | 91.00 | 4.00 | 14.00 | 0 |
| CROP_ZONE_1 | 164.50 | 117.67 | 32.83 | 14.00 | 0 |
| CROP_ZONE_2 | 102.67 | 46.50 | 42.17 | 14.00 | 0 |
| LIVESTOCK_COW | 127.33 | 119.33 | 0.00 | 8.00 | 0 |
| LIVESTOCK_SHEEP | 108.83 | 97.33 | 3.50 | 8.00 | 0 |
| FERTILIZER_LOGISTICS | 104.50 | 46.67 | 55.83 | 2.00 | 0 |
| FLOAT_RESERVE | 154.67 | 0.00 | 111.83 | 0.00 | 42.83 |

The primary PASS mechanism is role-local eligibility: useful work exists globally, but the current role has no admissible local action. The livestock specialists are the largest contributors inside that class, while CROP_ZONE_1 has the largest total PASS. FLOAT's dominant issue is route/reservation state, consistent with its high abandoned-move count.

## 10. Cross-Zone Assist Analysis

The controller telemetry value of 51.67 cross-zone assists per run counts dwell/continuation steps, not distinct assist assignments. Reconstructing unique commitments gives 18.33 crop cross-zone assists per run at mean target distance 3.29.

Across six runs, the 110 unique assists are:

| Origin → target zone | Task | Total | Per run |
|---|---|---:|---:|
| CROP_ZONE_1 → zone 2 | hard WATER | 30 | 5.00 |
| CROP_ZONE_2 → zone 0 | hard WATER | 6 | 1.00 |
| CROP_ZONE_0 → zone 1 | hard WATER | 12 | 2.00 |
| CROP_ZONE_0 → zone 2 | hard WATER | 45 | 7.50 |
| CROP_ZONE_1 → zone 0 | retirement clear | 6 | 1.00 |
| CROP_ZONE_0 → zone 1 | retirement clear | 6 | 1.00 |
| CROP_ZONE_1 → zone 2 | retirement clear | 5 | 0.83 |

At the decision point for every reconstructed assist, the origin zone's pending count is zero. No origin deadline is directly displaced. Cross-zone assistance is therefore not the root cause of the crop or livestock deficit, though repeated target continuation inflates telemetry and contributes some movement.

FLOAT hard assignments average 6.83 animal tasks, 30.67 crop-water tasks, 2 harvest tasks, and 0.33 blocking tasks per run. Crop assistance is often useful. Animal assistance is not reliably useful because the worker may lack staged wheat. The correction should preserve cross-zone crop rescue while requiring capability proof for livestock rescue.

## 11. Capacity Admission Accuracy

The existing admission artifacts contain 64 rejection records and 14 acceptance records:

- 18 rejections for cash/feed constraints;
- 46 rejections for negative predicted slack;
- 14 accepted decision records.

Those records do not map one-to-one to animal units. A per-species accepted decision can be reused across repeated turns, producing 36 late purchases across six episodes. Five runs buy 3 cows + 3 sheep during D13 H0–H2. One run buys 1 + 1 on D12 and 2 + 2 on D13.

Typical accepted D13 prediction:

| Field | Predicted/observed value |
|---|---:|
| Available next-day hours | 24 |
| Route estimate | 2 |
| Required hours | 22 |
| Minimum slack | 2 |
| Observed capacity proxy | 87–90 |

On the first full-herd day, actual values are:

| Measure | Five typical runs | Early-purchase run |
|---|---:|---:|
| Total MOVE | 109 | 108 |
| Productive actions | 32 | 33 |
| Livestock handling actions | 9 | 9 |
| FEED | 6 | 6 |
| CARE | 3 | 3 |
| Livestock-role MOVE | 26 | 26 |
| Pending livestock tasks at EOD | 3 | 3 |

The estimated route cost of 2 versus 26 observed livestock-role moves is a 13× miss. The “available next day” value of 24 is also structurally misleading around H0 because the temporary hands have expired and only the farmer is guaranteed, while the observed-capacity proxy comes from previous multiworker days. Finally, cow and sheep decisions are assessed separately on the same snapshot, and a decision framed as one candidate is reused to buy multiple units.

Classification:

| Admission group | Units | Primary assessment |
|---|---:|---|
| D0 bootstrap | 24 | BAD_CAPACITY_ESTIMATE: gate bypass with no serviceable feed owner; all escape. |
| D12–D13 rebuild | 36 | BAD_ROUTE_ESTIMATE with concurrent UNMODELED_FEED_LOGISTICS. |

The later herd does not escape, so admission is directionally adequate after specialists exist, but its numerical capacity model is not accurate. A binary “survived” outcome must not validate a route estimate that is wrong by an order of magnitude.

## 12. AG Mechanisms Worth Importing

Because AG's historical controllers are unavailable, these are mechanism-level imports supported by preserved outcomes, not claims about exact AG code or dispatch hour.

| Mechanism | Import value | V7 adaptation |
|---|---|---|
| Continuous feed dispatch | High | Treat feeding as a delivery chain, not only a target priority. |
| Explicit livestock service ownership | High | Bind every live cluster to a worker capable of staging and delivering wheat. |
| Wheat staging before remote dispatch | High | Convert FEED into PICKUP→DELIVER when inventory is absent. |
| Service priority above secondary collection | High | Close the due FEED set before CARE, fertilizer, or optional unload loops. |
| Crop-capacity reservation | High | Preserve V7's crop-zone ownership and hard-water rescue. |
| Inventory reserve policy | Medium | Reserve enough wheat for the live herd; exact AG reserve behavior is not reproducible. |
| Dedicated fertilizer ownership | Medium | Keep routine fertilizer collection away from livestock roles unless necessary. |
| Interrupt/retarget discipline | Medium | Retarget only when the new task is both harder and immediately serviceable. |
| Pasture ordering/location | Low | V7's existing completed paths are already short and optimal. |
| Atomic movement commitment alone | Low | V7 already has near-optimal local paths; the defect is commitment selection and legality. |

The key lesson is not to copy AG wholesale. V7 should import service continuity and inventory-aware ownership while retaining its stronger crop planner.

## 13. Crop Preservation Constraints

Any correction must preserve the mechanisms responsible for V7's 135.17 crop units:

1. Do not change crop footprints, planting mix, or retirement policy.
2. Do not remove zone ownership or hard WATER escalation.
3. Do not reserve a permanent crop worker for livestock; temporary reassignment is permitted only for an unresolved hard FEED obligation.
4. Do not let routine CARE, fertilizer collection, or product collection preempt an origin-zone crop deadline.
5. Preserve useful cross-zone crop rescue when the origin zone has no pending task.
6. Keep the animal fix within dispatch, staging, and sequencing. No economic retuning is required for the forensic hypothesis.

The bootstrap binding proposed below can use FLOAT and the first available worker only until the due FEED set is closed. The late-game cluster batching is performed by the existing livestock roles. These boundaries keep expected crop regression risk low.

## 14. Minimal Correction Set

### Fix 1 — SERVICEABLE_BOOTSTRAP_BINDING

Before placing a bootstrap animal, prove that its cluster has an active feed owner. While W4/W5 are absent, temporarily bind FLOAT and the first available worker to the cow/sheep clusters until the hard FEED set is closed. If no owner can stage and deliver wheat, defer placement.

Expected effect: eliminate the D5 bootstrap escape cohort and the resulting empty-herd interval.

### Fix 2 — INVENTORY_AWARE_FEED_DISPATCH

A worker may not reserve or move toward FEED unless it already carries WHEAT. When it does not, its commitment must be the composed SHED/PICKUP WHEAT → pasture/FEED route. Check capability before movement, not only at the animal tile.

Expected effect: remove impossible remote feed commitments, reduce route-state PASS, and ensure hard animal rescue is executable.

### Fix 3 — FEED_FIRST_CLUSTER_BATCHING

For each livestock cluster, stage enough wheat once and feed all due animals before CARE, product collection, fertilizer collection, or nonessential shed return. Prefer FERTILIZER_LOGISTICS for routine fertilizer handling and keep the livestock owner in-cluster until the due feed set is closed.

Expected effect: reduce approximately 98 pasture–shed–pasture loops per run, lower daily macro stretch, and improve care/collection cadence after feed safety is satisfied.

No fourth change is justified by the forensic evidence. Pasture relocation, new crop policy, broad role redesign, or economic retuning would expand scope without addressing the demonstrated failure chain.

## 15. Counterfactual Economic Range

This is a diagnostic range, not a tournament prediction. It assumes V7 crop output is preserved and adds only livestock recovery relative to the observed V7 baseline. Fertilizer uplift and speculative crop changes are excluded.

Observed V7 sale attribution:

| Product | Sold units/run | Revenue/run | Implied quote/unit |
|---|---:|---:|---:|
| MILK | 28.17 | 7,297.33 | 259.08 |
| WOOL | 14.67 | 3,367.50 | 229.60 |

Additional units to the 93/74 benchmark are approximately 64.83 MILK and 59.33 WOOL. Preserving the four bootstrap animals also avoids an estimated 1,800 of replacement cost: V7 later spends about 2,700 to buy six animals, whereas expansion from a surviving 2+2 bootstrap to 3+3 would require only two animals, approximately 900.

| Case | Incremental livestock revenue | Avoided replacement | Extra feed | Handling/opportunity reserve | Counterfactual final money |
|---|---:|---:|---:|---:|---:|
| Low | 20,640, recovery to 88/70 at conservative base values | +1,800 | -2,122 | -2,000 | 57,584 |
| Central | 26,075, recovery to 93/74 at 210/unit | +1,800 | -1,500 | -750 | 64,891 |
| High | 27,378, recovery to 93/74 at 90% of V7 implied quotes | +1,800 | -1,167 | -250 | 67,027 |

The incremental revenue is added to the current 39,265.67 baseline; existing V7 livestock revenue is not counted twice. The range is intentionally broad because the AG unit-accounting inconsistency and absence of an executable AG trace prevent precise quote-by-quote replication.

## 16. Final Verdict

AG's livestock advantage is explained at mechanism level. V7 creates an unserviceable bootstrap, dispatches hard FEED work without staging the required inventory, then rebuilds too late. Its later workers follow short local paths but sequence too many shed returns, secondary collections, and abandoned global commitments. The evidence supports a narrow serviceability correction, not a foundation rewrite.

The crop advantage is real and should be preserved. No implementation, tournament, Kaggle run, commit, or push is authorized by this forensic task.

```text
PRIMARY_ESCAPE_CAUSE: FEED_NOT_STAGED
SECONDARY_ESCAPE_CAUSE: LEGALITY_STATE_ERROR
PRIMARY_MOVE_SOURCE: FLOAT_RESERVE / GLOBAL_HARD_ROUTING_WITH_ABANDONED_COMMITMENTS
PRIMARY_PASS_SOURCE: NO_LOCAL_TASK_BUT_GLOBAL_TASK_EXISTS / ROLE_LOCAL_ELIGIBILITY
CAPACITY_ADMISSION_ACCURATE: NO
AG_LIVESTOCK_ADVANTAGE_EXPLAINED: YES
CODEX_CROP_ADVANTAGE_TO_PRESERVE: YES
MINIMAL_FIX_COUNT: 3
FIX_1: SERVICEABLE_BOOTSTRAP_BINDING
FIX_2: INVENTORY_AWARE_FEED_DISPATCH
FIX_3: FEED_FIRST_CLUSTER_BATCHING
EXPECTED_LIVESTOCK_RECOVERY: MILK 80-93; WOOL 62-74; ANIMAL_ESCAPES 0
CROP_REGRESSION_RISK: LOW
COUNTERFACTUAL_FINAL_MONEY_LOW: 57584
COUNTERFACTUAL_FINAL_MONEY_CENTRAL: 64891
COUNTERFACTUAL_FINAL_MONEY_HIGH: 67027
NEXT_STEP: MINIMAL_V7_CORRECTION_BUILD
IMPLEMENTATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```
