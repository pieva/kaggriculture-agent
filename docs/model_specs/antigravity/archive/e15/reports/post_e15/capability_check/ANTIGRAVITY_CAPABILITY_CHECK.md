# POST-E15 — MODEL CAPABILITY CHECK — ANTIGRAVITY

**Modeler:** Antigravity (Claude Opus 4.6 Thinking)  
**Date:** 2026-08-29  
**E15 Status:** `EPISTEMICALLY CLOSED`  
**E15 Closure Commit:** `922015f`  
**Target:** `FINAL_MONEY`  
**Constraint:** E15 = `TRAINING EVIDENCE`. No file modification. No code. No submission.

---

## Provenance Legend

Throughout this report, each claim is tagged with its provenance:

| Tag | Meaning |
|---|---|
| **[FRAME]** | METHODOLOGICAL FRAME — definitions from README.md / ontology |
| **[E15-PRI]** | PRIMARY E15 EVIDENCE — directly observed in frozen telemetry, summary.json, or forensic analyses |
| **[E15-SYNTH]** | POST-E15 INTERPRETATION — interpretations already formulated in E15_FINAL_TOURNAMENT_SYNTHESIS.md or consensus docs |
| **[MY-INF]** | YOUR INFERENCE — inference produced autonomously in this capability check |

---

## A. Evidence Reconstruction

### A.1 Experiment Structure

**[E15-PRI]** E15 was a pairwise round-robin tournament of 3 frozen agents:

| Match | Pairing | Seed | P0 | P1 | Steps |
|---|---|---|---|---|---:|
| M1 | Antigravity vs Codex | 1113294977 | Antigravity | Codex | 720 |
| M2 | Codex vs Copilot | 3033283457 | Codex | Copilot | 720 |
| M3 | Copilot vs Antigravity | 3122977751 | Copilot | Antigravity | 720 |

Source: [match_metadata.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M1_antigravity_vs_codex/match_metadata.json) and equivalent files for M2, M3.

All frozen submissions, MODEL_SPECs and ontology verified by SHA256 against [FREEZE_MANIFEST.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md). Environment position bias audited: `NO_MATERIAL_POSITION_BIAS_FOUND` ([P0_P1_ENVIRONMENT_AUDIT.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/P0_P1_ENVIRONMENT_AUDIT.md)).

### A.2 Observed Results

**[E15-PRI]** Source: [summary.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M1_antigravity_vs_codex/summary.json) per match.

| Match | Agent A | $A | Agent B | $B | Winner |
|---|---|---:|---|---:|---|
| M1 | Antigravity | $8,672 | Codex | $20,461 | Codex |
| M2 | Codex | $27,510 | Copilot | $37,752 | Copilot |
| M3 | Copilot | $26,629 | Antigravity | $9,371 | Copilot |

Final standing: **Copilot 2–0**, **Codex 1–1**, **Antigravity 0–2**.

### A.3 Key Observed Action Profiles (Primary Telemetry)

**[E15-PRI]** Source: `telemetry.json` per match.

#### Antigravity Fingerprint (M1 vs M3 Replication)

| Metric | M1 | M3 | Δ |
|---|---:|---:|---|
| WATER | 34 | 30 | ~stable |
| HARVEST | 414 | 374 | ~stable |
| FEED | 309 | 315 | ~stable |
| MOVE | 5,019 | 5,047 | ~stable |
| max hands | 12 | 12 | identical |
| max pasture | 18 | 18 | identical |
| max animals | 18 | 18 | identical |
| final herd | 17 | 17 | identical |
| quadrants | 3 | 3 | identical |
| FINAL_MONEY | $8,672 | $9,371 | +$699 |

**[MY-INF]** The Antigravity submission produces a highly deterministic behavioral fingerprint across two different seeds and two different opponents. This is the strongest replication signal in E15.

#### Copilot Fingerprint (M2 vs M3 Replication)

| Metric | M2 | M3 | Δ |
|---|---:|---:|---|
| WATER | 446 | 439 | ~stable |
| PLANT | 116 | 115 | ~stable |
| HARVEST | 110 | 113 | ~stable |
| CARE | 84 | 84 | identical |
| FEED | 84 | 84 | identical |
| max pasture | 5 | 5 | identical |
| max animals | 4 | 4 | identical |
| max hands | 9 (M2:10) | 9 | ~stable |
| SELL orders | 298 | 302 | ~stable |

#### Codex Profile (M1 and M2)

| Metric | M1 (as P1) | M2 (as P0) |
|---|---:|---:|
| WATER | 439 | 475 |
| PLANT | 111 | 126 |
| HARVEST | 105 | 91 |
| max crops | 28 | 37 |
| max pasture | 9 | 9 |
| max animals | 7 | 7 |
| FINAL_MONEY | $20,461 | $27,510 |

**[MY-INF]** Codex shows more seed-dependent variability in crop footprint (28 → 37) and in FINAL_MONEY ($20k → $27.5k) than Copilot or Antigravity. With only two observations this is insufficient to characterize the sensitivity fully.

### A.4 Requested vs Executed: Critical Observability Limit

**[E15-PRI]** The telemetry records **market_orders** as *requested* quantities, not as *executed transaction ledger*. This is explicitly noted in:
- [M1 Forensic §5](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M1_antigravity_vs_codex/E15_M1_NEUTRAL_FORENSIC_ANALYSIS.md): "Le quantità sono richieste di market order; non vanno automaticamente trattate come quantità tutte eseguite"
- [M2 Forensic §6](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M2_codex_vs_copilot/E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md): "Le quantità sono **requested quantities**, non executed transaction ledger"
- [M3 Forensic §6](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M3_copilot_vs_antigravity/E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md): "Quantità richieste, **non automaticamente quantità eseguite o revenue**"

**[MY-INF]** Any inference about revenue per unit, margin per product, or market profitability that uses requested order quantities as if they were executed is methodologically unsafe. The E15 evidence **does not contain** an executed transaction ledger, executed transaction value, or price realization data.

### A.5 Limits of the Available Evidence

**[E15-PRI / MY-INF]** E15 does not provide:

1. Executed transaction ledger (only requests)
2. Revenue by product type
3. Price realization data
4. Marginal revenue per action
5. Per-day active crop surface counts
6. Per-day watered crop fraction
7. Worker utilization rates
8. Action success/failure breakdown (e.g., how many HARVEST were successful vs. retry)
9. Purchase→productive-use latency
10. Causal counterfactuals
11. Multi-seed systematic validation (3 seeds, 1 per match)
12. Local-vs-Kaggle fidelity comparison

---

## B. Layer Diagnosis

### B.1 MODEL_VALIDITY

**[E15-PRI + MY-INF]**

**Copilot:** E15 provides the strongest support. The frozen MODEL_SPEC's core theses — throughput-to-cash conversion (#1), working set capacity gating (#2), crop activation and monetization (#3), conservative livestock alignment — are all directionally consistent with the observed policy fingerprint and the outcomes in both M2 and M3. The two-match replication with stable behavior reinforces this.

However, M2 shows that some claimed mechanisms are confounded:
- `wheat_feed_security`: Copilot avoids feed dependency through lightweight herd, not through feed buffering (avoidance ≠ security).
- `operating_cash_buffer`: Copilot operates with *lower* early-game cash than Codex in M2 (Days 4–9) and still wins. Buffer-as-monotonic-good is weakened.

**Verdict:** `SUBSTANTIALLY_SUPPORTED` with specific confounded elements.

**Codex:** M1 strongly supports the Codex model direction: land activation payback, monetized throughput over raw asset counts, irrigated crop surface, cash/deployable capital discipline. M2, however, weakens the model's prediction that more maintained crop surface and higher watering are monotonically better — Codex had 37 max crops vs. 28 for Copilot, 475 WATER vs. 446, yet lost.

**Verdict:** `PARTIALLY_TO_SUBSTANTIALLY_SUPPORTED`. The model's direction is sound but it does not yet distinguish "above-threshold maintenance" from "quality of conversion."

**Antigravity:** The MODEL_SPEC contains principles that E15 *supports at the concept level*: irrigation priority, maintained crop surface, activation payback, feed awareness. The problem is that the frozen submission systematically failed to realize these principles (34/30 WATER vs. MODEL_SPEC ranking it #1). E15 cannot determine whether the MODEL_SPEC itself is invalid or merely whether the policy translation was defective.

**Verdict:** `PARTIALLY_SUPPORTED` at concept level; the MODEL cannot be fully evaluated because POLICY_REALIZATION failure dominates the observations.

### B.2 POLICY_REALIZATION

**[E15-PRI]**

**Copilot:** The observed policy fingerprint is strongly consistent with the MODEL_SPEC's declared priorities. Compact working set, high watering, high SELL volume, low livestock. The match between spec and behavior is the strongest in the tournament.

**Verdict:** `SUPPORTED`.

**Codex:** M1 shows good alignment between model concepts and realized behavior (high watering, activated crops, monetization). M2 shows weaker alignment: the model prioritizes crop surface and productive action share, but these proved insufficient as discriminants against Copilot.

**Verdict:** `PARTIALLY_SUPPORTED`.

**Antigravity:** This is the most clear-cut layer diagnosis. The MODEL_SPEC declares watering as `Critical / Rank #1`, yet the submission realizes 34 (M1) and 30 (M3) total WATER actions across 720 steps. The spec declares cash-crop rotation; the submission registers zero Strawberry/Melon SELL orders. The spec declares feed autarky; the submission issues massive BUY_PRODUCT Wheat orders. This is replicated across two matches.

**Verdict:** `STRONGLY_WEAKENED`.

### B.3 IMPLEMENTATION_FIDELITY

**[E15-PRI + MY-INF]**

**Copilot:** No visible implementation anomalies. The high stability M2→M3 of the fingerprint suggests the code faithfully implements a stable decision procedure.

**Verdict:** `SUPPORTED` (no countervailing evidence).

**Codex:** No clear implementation anomalies detected. The HARVEST/PLANT ratio is approximately 1:1 in both matches (0.95 in M1, 0.72 in M2), consistent with effective dispatch. Seed-variability in crop footprint may be policy-level adaptation rather than implementation error.

**Verdict:** `UNRESOLVED` — insufficient evidence to distinguish policy adaptation from implementation variance.

**Antigravity:** The HARVEST/PLANT ratio (4.45 in M1, 3.74 in M3) is a strong *signature* of either dispatch failure (workers repeatedly attempt HARVEST on non-ready crops) or routing inefficiency (workers traverse long distances without completing production cycles). Combined with 5,000+ MOVE actions, 30–34 WATER, and max 8–9 active crops despite 12 hands and 3 quadrants, the implementation appears to fail at converting the MODEL_SPEC's declared priorities into actual worker behavior.

**Verdict:** `STRONGLY_WEAKENED`.

> [!IMPORTANT]
> For Antigravity, MODEL_VALIDITY cannot be cleanly assessed because the POLICY_REALIZATION and IMPLEMENTATION_FIDELITY failures are so dominant. The MODEL_SPEC may be valid but untested by its own submission.

---

## C. Feature Analysis

### C.1 `watering_execution_rate`

```text
concept_id: watering_execution_rate
feature_status: FEATURE
relationship: thresholded — below ~30–34 WATER/game, strongly associated with failure; above ~440 WATER, both winners and losers observed
e15_evidence: [E15-PRI] Antigravity 34/30 WATER → $8.6k/$9.4k (lost both). Codex 439/475 WATER → $20.5k/$27.5k (won M1, lost M2). Copilot 446/439 WATER → $37.8k/$26.6k (won both).
failure_region: WATER < ~100 (based on Antigravity observations at 30–34)
success_region: WATER ≥ ~440 (necessary but not sufficient — Codex at 475 still lost M2)
candidate_threshold_or_interval: lower bound for adequate watering appears to be somewhere between 34 and 439. This interval is extremely wide. E15 provides NO observations in the ~35–438 range.
confidence: HIGH that very low watering is a failure mode. LOW on the precise threshold.
confounders: WATER co-varies with dispatch efficiency, workforce allocation, crop surface, and routing. Cannot isolate WATER causally.
next_test_values: 100, 200, 300, 400 — to narrow the minimum viable watering level
falsification_condition: If an agent with WATER ~100–200 achieves FINAL_MONEY ≥ $20k, the "high watering required" thesis weakens. If an agent with WATER > 450 consistently loses, monotonic-positive is falsified (partial M2 evidence already weakens monotonicity above threshold).
```

### C.2 `livestock_headcount`

```text
concept_id: livestock_headcount
feature_status: FEATURE
relationship: non_monotonic — both extremes observed. 17–18 animals associated with loss; 4 animals associated with win; 7 animals associated with intermediate position.
e15_evidence: [E15-PRI] Antigravity max 18 animals → lost both ($8.6k, $9.4k). Codex max 7 → won M1 ($20.5k), lost M2 ($27.5k). Copilot max 4 → won both ($37.8k, $26.6k).
failure_region: max animals ≥ 17 (associated with Antigravity failure in both matches)
success_region: max animals ≤ 7 (associated with winning or competitive results)
candidate_threshold_or_interval: [4, 7] as E15-observed competitive range. 17–18 appears to be in failure territory. Interval between 8 and 16 is entirely unobserved.
confidence: MEDIUM — 3 agents × 2 matches provides only a coarse signal. Livestock co-varies with pasture, cash, workforce.
confounders: Herd size is confounded with pasture allocation, cash pressure, feed expenditure, and watering capacity. Antigravity's large herd may fail because of cash/dispatch problems, not because of herd size per se.
next_test_values: 4, 7, 10, 13 — covering observed and unobserved parts of the range
falsification_condition: If an agent with max animals = 13 and adequate watering/dispatch achieves FINAL_MONEY ≥ $25k, then "small herd is necessary" is weakened. If an agent with max animals = 4 and poor watering fails, livestock_headcount alone is not the cause.
```

### C.3 `state_capacity_alignment`

```text
concept_id: state_capacity_alignment
feature_status: FEATURE
relationship: positive — better alignment between owned capacity (land, workers, livestock) and activated/monetized capacity is associated with higher FINAL_MONEY across all three matches.
e15_evidence: [E15-PRI] M1: Antigravity owns 3Q/12hands/18pasture but activates only 8 crops vs Codex 2Q/10hands/28crops. M2: Codex 37crops/9pasture/7animals vs Copilot 28crops/5pasture/4animals — Copilot wins with smaller but better-aligned working set. M3: Replicates M1 pattern.
failure_region: Large nominal capacity with low activation ratio (Antigravity: 18 pasture + 18 animals + 12 hands → 8-9 active crops)
success_region: Compact, well-aligned working set (Copilot: 5 pasture + 4 animals + 9 hands → 25-28 active crops)
candidate_threshold_or_interval: No numeric threshold; the concept is a ratio/alignment measure. E15 suggests that active_crops / (pasture + hands + animals) is a better predictor than any individual component.
confidence: HIGH across all three matches. This is the most consistently discriminating concept in E15.
confounders: State-capacity alignment is a composite concept that subsumes watering, dispatch, and monetization. Its discriminative power may be because it captures the joint effect of several features, not because it is a primitive cause.
next_test_values: Test agents with deliberately mis-aligned configurations (high capacity, low activation) against well-aligned configurations at matched scale.
falsification_condition: If an agent with poor alignment (large nominal, low activation) achieves high FINAL_MONEY by compensating through a different mechanism (e.g., pure market trading), then alignment is not necessary.
```

### C.4 `crop_surface_maintained`

```text
concept_id: crop_surface_maintained
feature_status: FEATURE
relationship: thresholded — below some minimum, associated with failure; above threshold, NOT monotonically positive.
e15_evidence: [E15-PRI] M1: Antigravity 8 max active crops → loss; Codex 28 → win. M2: Codex 37 max active crops → loss; Copilot 28 → win. M3: Copilot 25 → win; Antigravity 9 → loss.
failure_region: max active crops ≤ 9 (both Antigravity observations)
success_region: max active crops in [25, 37] — but 37 lost to 28 in M2
candidate_threshold_or_interval: minimum viable ≥ ~20 (inferred, wide uncertainty). Range [8–9] confirmed failure. Optimum NOT determinable — 37 lost to 28.
confidence: MEDIUM — clear failure below ~10, but relationship becomes non-monotonic above ~25.
confounders: Crop surface co-varies with watering, workforce allocation, revenue mix. Codex's 37 crops may have been over-extended relative to monetization capacity.
next_test_values: 15, 20, 25, 30, 35 — to map the response curve
falsification_condition: If an agent with ~15 active crops and strong monetization matches or beats an agent with ~30 crops, then maintained crop surface is not a primary driver above a minimum threshold.
```

### C.5 `worker_action_monetization_rate`

```text
concept_id: worker_action_monetization_rate
feature_status: FEATURE
relationship: positive — higher FINAL_MONEY per action is associated with winning.
e15_evidence: [E15-PRI] M2 forensic: Copilot ~$7.13/action vs Codex ~$5.17/action. M1: Codex earns 2.36× Antigravity with similar total action counts. M3: Copilot 2.84× Antigravity.
failure_region: Low monetization rate (Antigravity: high action volume, low FINAL_MONEY)
success_region: High monetization rate (Copilot consistently highest)
candidate_threshold_or_interval: UNRESOLVED — proxy metric only, no ledger data for true revenue-per-action.
confidence: MEDIUM — directionally strong but the proxy ($FINAL_MONEY / total_actions) is crude. Does not decompose into which actions produce revenue.
confounders: This is a composite outcome metric, not a primitive feature. High monetization may result from better crop mix, better sell timing, or fewer wasted actions.
next_test_values: Requires executed transaction ledger to decompose.
falsification_condition: If an agent with low $/action wins through terminal liquidation or asset appreciation rather than flow income, then flow monetization rate is not sufficient.
```

### C.6 `pasture_arable_surface_tradeoff`

```text
concept_id: pasture_arable_surface_tradeoff
feature_status: FEATURE
relationship: conditional — excessive pasture allocation crowds out arable crop surface, but some minimum pasture is necessary for livestock revenue.
e15_evidence: [E15-PRI] M1: Antigravity 18 pasture / 8 crops vs Codex 9 pasture / 28 crops. M2: Codex 9 pasture / 37 crops vs Copilot 5 pasture / 28 crops. M3: Antigravity 18 pasture / 9 crops vs Copilot 5 pasture / 25 crops.
failure_region: pasture ≥ 18 with crop surface ≤ 9
success_region: pasture ≤ 9 with crop surface ≥ 25
candidate_threshold_or_interval: competitive pasture range [5, 9]; 18 is over-allocated. Range [10, 17] unobserved.
confidence: MEDIUM — consistent across matches but confounded with livestock headcount, cash allocation, and watering.
confounders: Pasture allocation is not independent of livestock decisions and cash flow. Reducing pasture without reducing livestock creates a different failure mode.
next_test_values: Test pasture = 5, 9, 12 with livestock at 4, 7, 10 respectively (factorial design).
falsification_condition: If pasture = 12 with strong watering and moderate livestock achieves competitive FINAL_MONEY, then 5 is not necessary.
```

### C.7 `movement_overhead`

```text
concept_id: movement_overhead
feature_status: UNRESOLVED
relationship: conditional — high MOVE count is associated with Antigravity failure, but MOVE-share (as % of total actions) is similar across agents in M2.
e15_evidence: [E15-PRI] M1: Antigravity 5,019 MOVE (71% of actions); Codex 3,761 MOVE (71%). M2: Codex 3,763 (70.7%); Copilot 3,768 (71.1%). M3: Copilot 3,765 (~71%); Antigravity 5,047 (~72%).
failure_region: absolute MOVE > 5,000 (Antigravity)
success_region: UNRESOLVED — winners and losers both show ~71% MOVE-share
candidate_threshold_or_interval: UNRESOLVED — MOVE-share is not discriminating; absolute MOVE is confounded with total action count.
confidence: LOW — movement is a consequence of spatial layout and worker dispatching, not clearly an independent feature.
confounders: High absolute MOVE may be a symptom of 3-quadrant expansion and dispatch inefficiency, not a cause.
next_test_values: Compare agents with identical quadrant count but different routing strategies.
falsification_condition: If an agent in 3Q achieves < 4,000 MOVE and competitive FINAL_MONEY, then movement overhead is reducible by routing, not just by quadrant count.
```

### C.8 `action_dispatch_failure`

```text
concept_id: action_dispatch_failure
feature_status: FEATURE
relationship: negative — high HARVEST/PLANT ratio is a strong signature of dispatch inefficiency, associated with failure.
e15_evidence: [E15-PRI] Antigravity HARVEST/PLANT: 4.45 (M1), 3.74 (M3). Codex: 0.95 (M1), 0.72 (M2). Copilot: 0.95 (M2), 0.98 (M3).
failure_region: HARVEST/PLANT ratio > 3 (Antigravity in both matches)
success_region: HARVEST/PLANT ratio ≈ 0.7–1.0 (Codex and Copilot in all appearances)
candidate_threshold_or_interval: ratios ≤ ~1.0 appear normal; > 3.0 indicates systematic dispatch/retry pathology.
confidence: HIGH for the signature being a reliable failure indicator. Cannot confirm whether high HARVEST counts represent literal failed harvests or other mechanisms (e.g., multi-step harvest on different tiles).
confounders: Low WATER can cause crops to die → retry → inflated HARVEST/PLANT. Cannot separate dispatch failure from crop death due to dehydration.
next_test_values: Require action success/failure logging to decompose HARVEST attempts.
falsification_condition: If HARVEST/PLANT > 3 but with per-action success confirmation, the "dispatch failure" interpretation would be falsified.
```

### C.9 `operating_cash_buffer`

```text
concept_id: operating_cash_buffer
feature_status: FEATURE
relationship: non_monotonic — too little cash leads to operational stalls, but higher early-game cash is NOT monotonically better.
e15_evidence: [E15-PRI] M1: Antigravity drops to $49 early, hits $81 at Day 19 during expansion. Codex maintains more cash. M2: Copilot operates with LOWER cash than Codex in Days 4–9 but wins. M3: Antigravity hits $73 at Day 18; Copilot maintains moderate levels.
failure_region: cash approaching $0 during mid-game expansion (Antigravity Day 18–19)
success_region: UNRESOLVED — Copilot won M2 with lower early cash than Codex
candidate_threshold_or_interval: minimum viable mid-game cash ≥ ~$100 (very rough, based on Antigravity distress). NOT a maximum-is-better relationship.
confidence: LOW-MEDIUM — cash trajectory is confounded with investment timing, asset acquisition, and revenue cycle.
confounders: Cash depletion during expansion is expected; the question is whether the investments produce return. Antigravity's cash depletion coincides with non-productive expansion.
next_test_values: Test conservative (maintain $500+ buffer) vs. aggressive (invest to $100) with matched other parameters.
falsification_condition: If aggressive early investment to near-zero cash with strong watering/dispatch produces high FINAL_MONEY, then buffer-as-feature is weakened.
```

### C.10 `deployable_capital_window`

```text
concept_id: deployable_capital_window
feature_status: FEATURE
relationship: positive — timing of capital deployment relative to operational readiness is associated with outcome.
e15_evidence: [E15-PRI] M3 forensic: Copilot advantage becomes permanent at step 252 (Day 10 Hour 12), before Antigravity's Q2 expansion. M1 forensic: Antigravity temporarily leads at Days 8–9 and 18, then collapses after Q2 expansion.
failure_region: capital deployed before operational readiness (Antigravity Q2 + workforce + herd expansion at Day 18–19)
success_region: capital deployed in alignment with demonstrated monetization capacity
candidate_threshold_or_interval: UNRESOLVED — qualitative concept, not directly quantifiable from E15 data.
confidence: MEDIUM — consistent narrative across matches but causal isolation is weak.
confounders: Capital deployment co-occurs with multiple decisions (hiring, land, animals); cannot separate.
next_test_values: Test agents with identical models but delayed vs. early expansion triggers.
falsification_condition: If early aggressive expansion with strong dispatch succeeds, then timing is less important than execution quality.
```

### C.11 `inventory_to_cash_conversion`

```text
concept_id: inventory_to_cash_conversion
feature_status: FEATURE
relationship: positive — more SELL orders associated with higher FINAL_MONEY.
e15_evidence: [E15-PRI] Copilot SELL orders: 298 (M2), 302 (M3). Codex: 245 (M1), 212 (M2). Antigravity: 198 (M1), 198 (M3).
failure_region: SELL orders ~198 (Antigravity, both matches)
success_region: SELL orders ~300 (Copilot, both matches)
candidate_threshold_or_interval: [198, 302] observed range. Higher SELL correlates with better outcome but these are REQUESTED orders.
confidence: MEDIUM — direction consistent but quantities are requests, not confirmed executions.
confounders: More SELL orders may reflect more production (cause) or more market churn (mechanism unknown). Copilot also has much higher BUY_PRODUCT orders (wheat trading flow).
next_test_values: Require executed transaction ledger. Test SELL order decomposition by product type.
falsification_condition: If an agent with ~200 SELL orders but high-value products achieves competitive FINAL_MONEY, then volume is less important than value.
```

### C.12 `wheat_operating_flow`

```text
concept_id: wheat_operating_flow
feature_status: UNRESOLVED
relationship: unresolved — both winners show intense wheat buy/sell flow, but profitability of this flow is not observable.
e15_evidence: [E15-PRI] Copilot BUY_PRODUCT Wheat: 1,828 (M2), 1,889 (M3). SELL Wheat: 1,767 (M2), 1,831 (M3). Codex BUY_PRODUCT Wheat: 1,334 (M2). Antigravity: 904–1,007 range.
failure_region: UNRESOLVED — low wheat flow may simply reflect low production, not a causal failure
success_region: UNRESOLVED — high wheat flow is present in both Copilot (winner) and Codex (mixed)
candidate_threshold_or_interval: UNRESOLVED
confidence: LOW — without executed transaction ledger, cannot determine if this flow is profitable, neutral, or a cost center.
confounders: Wheat may serve as feed, as commodity for resale, or as a cash-flow management tool. The same volume could have very different economic meanings.
next_test_values: Require executed transaction ledger with price data.
falsification_condition: If an agent with minimal wheat trading achieves competitive FINAL_MONEY with adequate internal feed, then wheat_operating_flow is not a necessary feature.
```

### C.13 `crop_revenue_mix`

```text
concept_id: crop_revenue_mix
feature_status: FEATURE
relationship: positive — presence of cash-crop sales (Strawberry/Melon) is associated with winning.
e15_evidence: [E15-PRI] M1 forensic: Codex sells Strawberry (52 units) and Melon (47 units); Antigravity sells zero cash crops. M2: Copilot sells Strawberry 52, Melon 49; Codex sells Strawberry 30, Melon 56. M3: Copilot sells Strawberry 54, Melon 58; Antigravity sells zero cash crops.
failure_region: zero cash-crop SELL orders (Antigravity, both matches)
success_region: ≥ 30 units of cash-crop SELL orders
candidate_threshold_or_interval: [0, ~55] observed. Some cash-crop sales appear necessary; quantity unclear.
confidence: MEDIUM — direction clear but these are requested orders, not revenue. Market prices for cash crops are unknown.
confounders: Cash crops require longer growth cycles and more watering. The ability to sell them presupposes adequate watering and crop management. Cash-crop sales may be a symptom of good operations, not an independent driver.
next_test_values: Test agents that vary cash-crop allocation (0%, 30%, 60% of crop surface) with watering held constant.
falsification_condition: If a wheat-only agent with strong monetization achieves competitive FINAL_MONEY, then cash crop presence is not necessary.
```

### C.14 `land_surface_total`

```text
concept_id: land_surface_total
feature_status: NOT_FEATURE (as primary driver)
relationship: weakened — more quadrants are not better. 3Q lost to 2Q in both Antigravity matches.
e15_evidence: [E15-PRI] Antigravity 3Q → lost both. Codex 2Q, Copilot 2Q → won or competitive.
failure_region: 3Q with low activation
success_region: 2Q with high activation
candidate_threshold_or_interval: 2Q appears sufficient. 3Q is not necessary and was associated with failure (confounded with other Antigravity problems).
confidence: MEDIUM — E15 only observed 3Q in one agent (Antigravity) with confounded implementation failures. 3Q might work with adequate dispatch.
confounders: Antigravity's Q3 failure is inseparable from its watering/dispatch/livestock problems. Q3 may be viable with different execution.
next_test_values: Test 2Q-only vs 3Q agents with matched watering and dispatch quality.
falsification_condition: If a 3Q agent with strong watering and dispatch achieves competitive FINAL_MONEY, then Q-count is not a feature and the Antigravity failure was implementation-driven.
```

---

## D. Confounder Analysis

### D.1 The Watering ↔ Dispatch ↔ Livestock ↔ Cash Confounder Cluster

**Features entangled:** `watering_execution_rate`, `action_dispatch_failure`, `livestock_headcount`, `operating_cash_buffer`, `crop_surface_maintained`.

**Falsely suggested interpretation:** "Low watering *causes* low FINAL_MONEY."

**What is missing:** Low watering may be a *symptom* of dispatch failure (workers dispatched to non-productive tasks), which may itself result from large livestock requiring FEED/CARE, which consumes worker-turns that could be used for WATER. Alternatively, the causality may run: large herd → high FEED demand → cash spent on BUY_PRODUCT Wheat → cash depletion → cannot invest in crop infrastructure → low crop surface → low revenue.

**Experiment to separate:** Test two agents with identical livestock (e.g., 4 animals) and identical land (2Q) but different watering priorities (high vs. low). This isolates watering from livestock and expansion confounders.

### D.2 The Copilot "Compact Working Set" Confounder

**Features entangled:** `state_capacity_alignment`, `pasture_arable_surface_tradeoff`, `livestock_headcount`, `inventory_to_cash_conversion`.

**Falsely suggested interpretation:** "Small working set *causes* high profit."

**What is missing:** Copilot's working set is small *and* well-maintained *and* well-monetized. We cannot determine whether the *size* matters (i.e., a large well-maintained working set would do equally well or better) or whether smallness enables better maintenance given fixed workforce.

**Experiment to separate:** Test an agent with Copilot's watering/dispatch quality but a deliberately larger working set (e.g., 35+ crops, 9 pasture, 7 animals) to see if larger-but-well-maintained outperforms.

### D.3 The Market Trading Volume Confounder

**Features entangled:** `wheat_operating_flow`, `inventory_to_cash_conversion`, `crop_revenue_mix`.

**Falsely suggested interpretation:** "More SELL orders cause more profit."

**What is missing:** The executed transaction ledger. Copilot's ~300 SELL requests and ~1,800+ BUY_PRODUCT Wheat requests create a massive wheat trading volume. Without knowing execution rates and prices, we cannot determine if this is profitable arbitrage, a neutral cash-flow tool, or a costly churn.

**Experiment to separate:** Add executed transaction and price logging. Compare agents with different trading frequencies at matched production levels.

### D.4 Seed-Specificity Confounder

**Features entangled:** all features.

**Falsely suggested interpretation:** "Copilot's strategy is universally optimal."

**What is missing:** Each match used a different seed (1113294977, 3033283457, 3122977751). Market dynamics, shop unlocks, weed patterns, and price trajectories are seed-dependent. Copilot won on 2 seeds; Codex won on 1. This is NOT multi-seed systematic validation.

**Experiment to separate:** Run the same frozen submissions on 10+ seeds to characterize seed-variance. This is the most basic validation gap in E15.

---

## E. Candidate Design for the Next Common Training Round

### E.1 Primary Experiment: Watering Threshold Discovery

```text
training_or_validation: TRAINING
hypothesis: There exists a minimum watering threshold below which FINAL_MONEY degrades sharply, and above which marginal watering has diminishing returns.
feature_under_test: watering_execution_rate
controlled_variables: livestock_headcount = 4, quadrants = 2, workforce = 9, crop_revenue_mix = include cash crops
test_values: Total WATER targets: 50, 150, 250, 350, 450
expected_discrimination: If the response curve shows a sharp elbow (e.g., between 150 and 250), we can narrow the minimum threshold from the current [34, 439] interval to a ~100-unit window.
falsification_condition: If the response curve is linear or flat, then watering is not a thresholded feature.
evidence_that_must_be_recorded: FINAL_MONEY, total WATER actions, active crop surface per day, watered crop fraction, HARVEST/PLANT ratio, executed transaction ledger.
```

### E.2 Secondary Experiment: Livestock Scale Sensitivity

```text
training_or_validation: TRAINING
hypothesis: Livestock headcount has a non-monotonic relationship with FINAL_MONEY — optimal range is in [4, 10], not at extremes.
feature_under_test: livestock_headcount
controlled_variables: watering = high (target ~440), quadrants = 2, workforce = 9
test_values: max_animals = 0, 4, 7, 10, 14
expected_discrimination: If FINAL_MONEY peaks at 4–7 and declines at 10–14, we confirm E15's initial signal. If FINAL_MONEY is flat from 4–10, livestock_headcount is less important than currently estimated.
falsification_condition: If max_animals = 14 with high watering achieves competitive FINAL_MONEY, then E15's Antigravity failure was not livestock-driven.
evidence_that_must_be_recorded: FINAL_MONEY, herd counts per day, feed expenditure, pasture allocation, livestock product revenue (requires executed ledger).
```

### E.3 Tertiary Experiment: Working Set Scale (Compact vs. Extended)

```text
training_or_validation: TRAINING
hypothesis: With adequate watering and dispatch, a larger crop surface produces more FINAL_MONEY than a compact one.
feature_under_test: crop_surface_maintained (as interaction with state_capacity_alignment)
controlled_variables: watering = high (~440), livestock = 4, quadrants = 2
test_values: target max_active_crops = 15, 20, 25, 30, 35
expected_discrimination: If FINAL_MONEY increases from 15 to 25 then plateaus, crop surface is thresholded. If it continues rising to 35, Codex's M2 loss was due to monetization quality, not crop surface excess.
falsification_condition: If max_active_crops = 35 consistently beats 25 with matched parameters, then Copilot's compact working set is suboptimal and E15's M2 result was misleading.
evidence_that_must_be_recorded: FINAL_MONEY, active crop surface per day, watered fraction, SELL orders by product, executed revenue by product type.
```

### E.4 Design Rationale: Minimum Sufficient Design

**[MY-INF]** These three experiments target the three highest-information-gain gaps identified in E15:

1. **Watering threshold** — E15's largest observational gap (no data between 34 and 439).
2. **Livestock scale** — E15's most confounded variable (co-varies with pasture, cash, dispatch).
3. **Working set size** — E15's most paradoxical signal (37 crops lost to 28 in M2, but 8–9 crops clearly failed).

All three should be run on **multiple seeds** (minimum 3–5 per configuration) to begin addressing the seed-specificity confounder.

All three require the **executed transaction ledger** — the single most critical new observability for E16+.

> [!IMPORTANT]
> E15 evidence is `TRAINING EVIDENCE`. The three experiments above produce `TRAINING EVIDENCE` for bounding. Only after these bounds are established should a `VALIDATION` round test the resulting constrained model on held-out seeds.

---

## F. Epistemic Audit

### SUPPORTED

Conclusions directly supported by E15 primary evidence:

1. **Very low watering (30–34) is a replicated failure mode.** Source: Antigravity telemetry M1+M3.
2. **High livestock + low crop activation is a replicated failure mode.** Source: Antigravity fingerprint M1+M3.
3. **State-capacity alignment is the most consistently discriminating concept across all three matches.** Source: M1+M2+M3 forensic analyses.
4. **Antigravity's submission systematically fails to realize its MODEL_SPEC's declared priorities.** Source: WATER rank #1 in MODEL_SPEC, 34/30 in execution.
5. **Copilot produces the most stable policy fingerprint across matches.** Source: M2+M3 telemetry comparison.
6. **Scale (quadrants, hands, pasture, animals) is NOT a sufficient driver of FINAL_MONEY.** Source: Antigravity 3Q/12h/18p/18a lost to 2Q/9h/5p/4a.
7. **SELL order volume is positively associated with FINAL_MONEY.** Source: 198/198 (Antigravity) vs. 298/302 (Copilot), with caveat that these are requested, not executed.
8. **Cash-crop SELL presence is associated with winning; zero cash-crop sales with losing.** Source: M1+M3 Antigravity sells no Strawberry/Melon.
9. **No position bias (P0/P1) affects the results.** Source: Environment audit.

### PROVISIONAL

Reasonable inferences still requiring tuning/falsification:

1. **There exists a watering threshold below which operations collapse.** The threshold is somewhere in [34, 439] — interval too wide for operational use.
2. **Optimal livestock headcount lies in [4, 10].** E15 provides only 3 data points (4, 7, 17–18).
3. **Copilot's compact working set reflects a genuine strategic advantage.** Could alternatively reflect lower ambition that happened to be rewarded by these particular opponents.
4. **HARVEST/PLANT ratio > 3 is a reliable dispatch-failure signature.** Plausible but requires action-level success/failure data for confirmation.
5. **The two-regime model (below vs. above operational threshold) describes E15's structure.** Supported by the match data but is an interpretive framework, not a directly observed feature.
6. **Crop surface has diminishing or non-monotonic returns above ~25.** Based on M2 alone (37 lost to 28); single observation.

### UNRESOLVED

Questions E15 does not allow to determine:

1. **The precise minimum viable watering threshold.** No data between 34 and 439.
2. **Whether wheat trading flow is profitable, neutral, or costly.** No executed transaction ledger.
3. **Whether Antigravity's MODEL_SPEC is fundamentally flawed or merely poorly implemented.** POLICY_REALIZATION failure prevents MODEL evaluation.
4. **Whether Copilot's values (4 animals, 5 pasture, 9 hands, ~440 WATER) are near-optimal or simply above-threshold.** No parametric variation tested.
5. **Whether Q3 is inherently disadvantageous or only disadvantageous with Antigravity's implementation.** Confounded.
6. **Seed-specific vs. general superiority of any strategy.** 3 seeds total, 1 per match.
7. **Species margin differential (Cow vs. Sheep).** No clean comparison.
8. **Endgame liquidation's causal contribution to final score.** Not isolable from accumulated wealth.
9. **Price realization and revenue decomposition by product.** Not recorded.
10. **Feed market expenditure as cost center.** Only requests observed, not expenditures.

### DO_NOT_INFER

Conclusions that appear plausible but MUST NOT be drawn from E15:

1. **"439–446 WATER is the optimal watering level."** These are the only high-watering values observed. They may be above threshold, not at optimum.
2. **"4 animals is the optimal herd size."** Only one agent used 4 animals. This is a single observation, not a validated optimum.
3. **"2 quadrants is always better than 3."** The only 3Q agent had massive implementation failures. 3Q has never been tested with competent execution.
4. **"Copilot's MODEL_SPEC is the correct model."** Copilot won competitively; this does not establish MODEL_VALIDITY as universal.
5. **"Codex's model is structurally inferior to Copilot's."** Codex lost M2 but by a narrower margin (1.37×) compared to Antigravity's losses (2.36×, 2.84×). The models differ on emphasis, not on fundamental direction.
6. **"Antigravity's MODEL_SPEC is falsified."** The spec contains principles E15 supports. The implementation failure prevents model evaluation.
7. **"Wheat churn is profitable."** No executed transaction data.
8. **"Market dependency is positive or negative."** Copilot uses more market wheat and wins; this does not establish market dependency as a positive feature.
9. **"The M2/M3 Copilot outcomes represent validation evidence."** All E15 evidence is TRAINING EVIDENCE. It cannot be re-used as validation.
10. **"The competitive ranking (Copilot > Codex > Antigravity) equals model quality ranking."** Victory ≠ Model Validity. Defeat ≠ Model Falsification.

---

## Source Artifacts Referenced

| Artifact | Path |
|---|---|
| README.md | [README.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/README.md) |
| E15 Synthesis | [E15_FINAL_TOURNAMENT_SYNTHESIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/E15_FINAL_TOURNAMENT_SYNTHESIS.md) |
| Freeze Manifest | [FREEZE_MANIFEST.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md) |
| M1 Summary | [summary.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M1_antigravity_vs_codex/summary.json) |
| M1 Telemetry | [telemetry.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M1_antigravity_vs_codex/telemetry.json) |
| M1 Forensic | [E15_M1_NEUTRAL_FORENSIC_ANALYSIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M1_antigravity_vs_codex/E15_M1_NEUTRAL_FORENSIC_ANALYSIS.md) |
| M2 Summary | [summary.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M2_codex_vs_copilot/summary.json) |
| M2 Telemetry | [telemetry.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M2_codex_vs_copilot/telemetry.json) |
| M2 Forensic | [E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M2_codex_vs_copilot/E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md) |
| M2 Copilot Audit | [M2_COPILOT_INDEPENDENT_AUDIT.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M2_COPILOT_INDEPENDENT_AUDIT.md) |
| M3 Summary | [summary.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M3_copilot_vs_antigravity/summary.json) |
| M3 Telemetry | [telemetry.json](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M3_copilot_vs_antigravity/telemetry.json) |
| M3 Forensic | [E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/M3_copilot_vs_antigravity/E15_M3_NEUTRAL_FORENSIC_ANALYSIS.md) |
| Environment Audit | [P0_P1_ENVIRONMENT_AUDIT.md](file:///c:/Users/pietr/Projects/kaggriculture-agent/experiments/archive/e15/artifacts/P0_P1_ENVIRONMENT_AUDIT.md) |
