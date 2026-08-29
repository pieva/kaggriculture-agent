# MODEL_SPEC Critical Review

## Executive Verdict

MODEL_SPEC.md is a well-structured document that correctly maintains the distinction between OBSERVED, INFERRED, and TESTED claims. However, this critical review identifies **significant evidentiary gaps**, **several causal claims unsupported by available data**, and **multiple instances where interpretations have been elevated beyond what the replay evidence supports**. The document also contains claims that are **contradicted by the X1.14 counterfactual** and by inconsistencies across replay seeds.

The core finding: **the 3-episode benchmark batch is too small to support many of the generalizations that MODEL_SPEC currently treats as established patterns.** Several "cross-competitor invariants" are actually observed in only 2 of 3 replays, and some are observed in only 1. The batch also varies across seeds (`421521921`, `1056561958`, `1273000467`), making cross-episode comparison less clean than it appears.

---

## Evidence Base

### Primary Evidence: Raw Replay JSON

| Episode | Seed | Our Agent | Our Score | Competitor | Comp Score | JSON Size |
|---|---:|---|---:|---|---:|---:|
| `101294736` | `421521921` | Pietro Valocchi (pid 0) | `$6,825` | truebelief (pid 1) | `$86,297` | 16.1 MB |
| `101705751` | `1056561958` | Pietro Valocchi (pid 0) | `$38,815` | Dr. Mikholae Hutchinson (pid 1) | `$90,137` | 17.3 MB |
| `101717011` | `1273000467` | Alexander Sokolov (pid 0) | `$50,420` | Pietro Valocchi (pid 1) | `$24,314` | 13.8 MB |

### Secondary Evidence: Counterfactual Results

| Version | Seeds Tested | Variants | Best Required-Seed Result | Adoption |
|---|---:|---:|---|---|
| X1.13 | 2 | 5 (A-E) | A baseline `$42,491 / $48,313` | REJECTED |
| X1.14 | 4 | 6 (A-F) | A baseline `$42,491 / $48,313` | REJECTED |

### Methodological Limitations

> [!WARNING]
> **Sample Size**: 3 replays across 3 different seeds is insufficient for robust generalization. Any "invariant" supported by 3/3 is an observation from n=3, not a statistical regularity.

> [!WARNING]
> **Seed Confounding**: Each episode uses a different seed, so differences between competitors may be partly seed-dependent rather than strategy-dependent. We cannot separate seed effects from strategy effects.

> [!WARNING]
> **Price Information**: The replay JSON contains market prices (`prices` field in `market` observation) but these appear to be static base prices (e.g., WHEAT=25, MILK=160, FERTILIZER=100, WOOL=200, MELON=250, STRAWBERRY=120, CARROT=35, TOMATO=60, EGG=50). There is no direct evidence of dynamic pricing or buy/sell spread in the observed price data. The actual economic impact of BUY_PRODUCT/SELL operations cannot be computed from a ledger because no per-transaction revenue/cost fields are present in the replay actions.

> [!WARNING]
> **Our Agent is Different Across Episodes**: In `101294736` our agent (pid 0) is a different strategy version than in `101705751` and `101717011` (where pid 0 / pid 1 differ). The "our" side in episode `101294736` bought Q2 on Day 8 with $295, which is NOT X1.12 behavior. The "our" side in episodes `101705751` and `101717011` appears to be X1.12. This asymmetry means comparing "our side" across episodes is comparing different strategies.

---

## Hypothesis-by-Hypothesis Audit

### 1. Workforce

#### CLAIM: "Workforce is state-dependent: peak hands are 12, 10 and 8, so the invariant is throughput fit, not a copied count"

**Evidence from replays:**

| Episode | Competitor | Peak Hands | Reward | Competitor HIRE Count |
|---|---|---:|---:|---:|
| `101294736` | truebelief | 12 | $86,297 | 231 |
| `101705751` | Dr. Hutchinson | 10 | $90,137 | 270 |
| `101717011` | Sokolov | 8 | $50,420 | 222 |

Hands timeline from daily data:
- **truebelief**: 5→5→5→5→5→5→5→5→5→5→5→6→9→10→10→9→10→10→11→12→10→12→11→11→11→11→11→11→0→0 (peaks at 12 on days 20, 22)
- **Hutchinson**: 5→5→5→7→7→7→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→10→8→8→8 (stable at 10 from day 7)
- **Sokolov**: 8→8→8→6→0→8→8→8→6→2→8→8→8→8→8→8→8→8→8→8→8→8→8→8→8→8→8→8→8→8 (mostly 8, with dips to 0 and 2)

**Critical findings:**

1. **"More Hands -> more money" is NOT supported.** Hutchinson ($90,137) with peak 10 beats truebelief ($86,297) with peak 12. Sokolov ($50,420) with peak 8 beats our agent in the same episode.
2. **Hire timing matters more than count.** Truebelief stays at 5 hands through Day 10, then ramps aggressively after Q1. Hutchinson reaches 10 hands by Day 7 (before Q1 on Day 14). Sokolov starts at 8 hands on Day 1 and maintains that level.
3. **Sokolov's extreme PASS count (2071 PASS actions)** shows that having more hands does NOT guarantee productive utilization. He has 8 hands but most of them pass most of the time.
4. **The claim is PARTIALLY_SUPPORTED**: peak hands do vary (8, 10, 12), but the claim that this implies "throughput fit" is an INFERRED interpretation. The actual replay evidence shows hand count is correlated with quadrant count, not with a workload model.

**Classification: PARTIALLY_SUPPORTED / INFERRED**

The variation exists, but the causal mechanism is not observable. We observe different hand counts, but we cannot observe why these counts were chosen or whether they are optimal.

---

#### CLAIM: "Workforce Capacity First" (X1.14 hypothesis)

**X1.14 counterfactual evidence:**

| Variant | Seed 0 | Seed 421521921 | Seed 1273000467 |
|---|---:|---:|---:|
| A (X1.12 baseline) | $42,491 | $48,313 | $43,021 |
| B (workforce aggressive) | $39,301 | $36,238 | $54,228 |

**Critical finding:** Workforce Capacity First is **seed-dependent**, not universally beneficial. It improves on seed `1273000467` (+$11,207) but regresses on both required seeds (-$3,190 and -$12,075). MODEL_SPEC correctly notes this (line 305) but the implication for the broader model is understated: **any policy that changes workforce aggressiveness will likely have mixed seed results, making it impossible to validate on 2 seeds.**

**Classification: MIXED / seed-dependent**

---

### 2. Land Discipline

#### CLAIM: "Q0-only can be economically competitive"

**Direct evidence:**
- Sokolov: NW only, $50,420, beats our $24,314 with 2 quadrants
- X1.14 variant B (Q1 disabled by effect): $39,301 on seed 0 vs $42,491 X1.12 with Q1

**Classification: SUPPORTED**

Q0-only is competitive against our current policy. However, this does NOT prove Q0-only is competitive against the top tier: truebelief ($86,297) and Hutchinson ($90,137) both use Q1. The gap between Q0-only peak ($50,420) and Q1 peak ($90,137) is large.

---

#### CLAIM: "Q1 is payback-gated, not calendar-gated"

**Evidence:**
- truebelief: Q1 on Day 10, money at buy = $4,380, result = $86,297
- Hutchinson: Q1 on Day 13, money at buy = $2,355, result = $90,137
- Sokolov: no Q1, result = $50,420
- Our agent (ep 101294736): Q1 on Day 1 with $741, then Q2 on Day 8 with $295, result = $6,825

**Critical findings:**
1. Early Q1 with insufficient capital (Day 1, $741) is disastrous.
2. Q1 timing varies: Day 10 vs Day 13. The money-at-buy values are very different ($4,380 vs $2,355).
3. The claim that Q1 should be "payback-gated" is INFERRED. What we observe is different timing, not evidence of a payback calculation. Correlation between Q1 timing and success could be confounded by overall strategy quality.

**Classification: PARTIALLY_SUPPORTED**

The evidence rejects calendar-only triggers (Day 11 is not universal) but does not positively support payback-gated expansion, which remains INFERRED.

---

#### CLAIM: "Q2 not priority" / "Q2 conditional only"

**Evidence:** 0/3 competitors buy Q2. Our side in ep `101294736` buys Q2 and gets $6,825 (but this was not X1.12).

**Critical note: Absence of Q2 in 3 replays does NOT prove Q2 is negative.** MODEL_SPEC correctly notes this. However, the strength of language ("CONSISTENT REJECTION") is arguably too strong for n=3. We don't know if the best players in the competition use Q2 in other seeds/matchups.

**Classification: NOT SUPPORTED (as prohibition), OBSERVED (as absence in this batch)**

---

#### CLAIM: "land count is endogenous to economic capacity"

This phrase does not appear verbatim in MODEL_SPEC but the concept is expressed as "Deployable Capital" (Section 13). The claim is that land purchase should be gated by capital and capacity.

**Evidence:** The replay data shows land is purchased at different capital levels:
- truebelief: $4,380 at Q1 buy
- Hutchinson: $2,355 at Q1 buy
- Our agent: $741 at Q1 buy (ep 101294736)

The correlation between buy-capital and outcome exists but confounds multiple factors.

**Classification: INFERRED — not directly demonstrated from replays**

---

### 3. Productive Surface

#### CLAIM: "Productive capacity must be maintainable and monetizable"

**Evidence matrix:**

| Player | Peak Productive | Mean Productive D10-25 | Weed TDs | Unwatered TDs | Reward |
|---|---:|---:|---:|---:|---:|
| truebelief | 50 | 42.4 | 4 | 818 | $86,297 |
| Hutchinson | 44 | 36.1 | 28 | 573 | $90,137 |
| Sokolov | 18 | 16.9 | 148 | 301 | $50,420 |
| Our (101705751) | 28 | 23.8 | 195 | 442 | $38,815 |
| Our (101717011) | 30 | 24.1 | 185 | 435 | $24,314 |

**Critical findings:**

1. **Productive surface correlates with reward for Q1 players, but Sokolov breaks the pattern.** Sokolov has peak productive 18, yet earns $50,420 — more than our 28-30 peak productive runs. This means productive surface alone is not the driver.
2. **Weed tile-days have mixed relationship.** Truebelief (4 weed TDs) and Hutchinson (28 weed TDs) are both elite; Sokolov has 148 weed TDs but still earns well. Our agents have 185-195 weed TDs and earn less than Sokolov.
3. **Unwatered tile-days are HIGHER for truebelief (818) than for us (442, 435).** This is a surprising counterexample: the best performer has the most unwatered tile-days. This may mean unwatered tiles are planted tiles that haven't been watered yet on that day (at hour 0 measurement), not neglected tiles. This metric needs careful interpretation.
4. **X1.14 counterevidence**: Variants C/D reduce weed TDs from 137→6 but money drops from $42,491 to $31,585-$35,537. Weed elimination does NOT automatically improve money.

**Classification: PARTIALLY_SUPPORTED**

The relationship between productive surface and reward is real but non-monotonic and confounded by monetization quality, livestock revenue, and efficiency.

---

### 4. Livestock

#### CLAIM: "All competitors combine crop engine and livestock engine"

**Evidence:**

| Competitor | Final Livestock | Animal Buys | Total Animal Products Sold |
|---|---|---:|---|
| truebelief | 9 COW, 5 SHEEP | 9 COW, 5 SHEEP | MILK:134, WOOL:70, FERTILIZER:138 |
| Hutchinson | 7 COW, 4 SHEEP, 2 GOOSE | 8 COW, 4 SHEEP, 4 GOOSE | MILK:161, EGG:71, FERTILIZER:208, WOOL:36 |
| Sokolov | 4 COW, 2 SHEEP | 6 COW, 2 SHEEP | MILK:129, WOOL:52, FERTILIZER:69 |

**Classification: SUPPORTED (3/3 replays)**

All three competitors have livestock. This is the strongest pattern in the batch.

---

#### CLAIM: "7 Cow / 4 Sheep is OBSERVED_REFERENCE, not target"

**Evidence:** Competitor livestock varies:
- truebelief: 9C/5S (MORE than 7/4)
- Hutchinson: 7C/4S/2G (matches 7/4 for cows/sheep but adds goose)
- Sokolov: 4C/2S (LESS than 7/4)

**Critical note:** truebelief **bought** 9 COW and 5 SHEEP. Hutchinson bought 8 COW, 4 SHEEP, 4 GOOSE (note: ended with 7 COW, meaning 1 cow died or was not maintained). Sokolov bought 6 COW but ended with 4 (2 died/were lost).

Animal attrition is an observable phenomenon that MODEL_SPEC does not discuss. The gap between "animals bought" and "animals at end" suggests maintenance failures.

**Classification: SUPPORTED** — correctly maintained as reference, not target.

---

#### CLAIM: "Livestock as economic engine"

**Analysis of livestock contribution (estimated from base prices):**

| Competitor | Est. Livestock Revenue | Est. Crop Revenue | Livestock Share |
|---|---:|---:|---:|
| truebelief | MILK:$21,440 + WOOL:$14,000 + FERT:$13,800 = ~$49,240 | WHEAT:$6,700 + MELON:$27,000 + STRAW:$8,280 = ~$41,980 | ~54% |
| Hutchinson | MILK:$25,760 + EGG:$3,550 + FERT:$20,800 + WOOL:$7,200 = ~$57,310 | CARROT:$1,435 + WHEAT:$2,725 + STRAW:$15,840 + MELON:$3,000 = ~$23,000 | ~71% |
| Sokolov | MILK:$20,640 + WOOL:$10,400 + FERT:$6,900 = ~$37,940 | WHEAT:$18,900 + CARROT:$2,065 + TOMATO:$2,160 + STRAW:$1,680 + MELON:$3,000 = ~$27,805 | ~58% |

> [!IMPORTANT]
> **These revenue estimates use base prices only.** The actual prices may vary due to market dynamics (supply/demand). However, even with substantial price variation, livestock products constitute a MAJORITY of estimated revenue for all three competitors. This strongly supports livestock as an economic engine.

**Classification: SUPPORTED**

---

### 5. Multi-Engine Monetization

#### CLAIM: "Revenue is diversified across crop products, animal products and Fertilizer"

**Evidence:**

| Competitor | Distinct Products Sold | Top Revenue Sources |
|---|---:|---|
| truebelief | 6 | WHEAT(268), FERT(138), MILK(134), MELON(108), WOOL(70), STRAW(69) |
| Hutchinson | 8 | FERT(208), MILK(161), STRAW(132), WHEAT(109), EGG(71), CARROT(41), WOOL(36), MELON(12) |
| Sokolov | 8 | WHEAT(756), MILK(129), FERT(69), CARROT(59), WOOL(52), TOMATO(36), STRAW(14), MELON(12) |
| Our (101705751) | 5 | **WHEAT(1863)**, MILK(135), MELON(45), STRAW(40), WOOL(9) |

**Critical finding: Our agent sells overwhelmingly WHEAT, while competitors sell diversified products.** Our WHEAT:1863 vs Hutchinson's WHEAT:109. But we also BUY_PRODUCT WHEAT:2071 in the same episode. This is the wheat market loop problem.

**Classification: SUPPORTED** — competitors diversify; our agent does not.

---

### 6. Capital Deployment / Deployable Capital

#### CLAIM: "Deployable Capital is the correct framework for investment decisions"

**Evidence from money timelines:**

| Competitor | Day 10 Cash | Day 15 Cash | Day 20 Cash | Day 25 Cash | Final |
|---|---:|---:|---:|---:|---:|
| truebelief | $684 | $6,595 | $24,778 | $57,172 | $86,297 |
| Hutchinson | $74 | $2,509 | $19,978 | $50,762 | $90,137 |
| Sokolov | $1,762 | $5,572 | $14,874 | $29,843 | $50,420 |
| Our (101705751) | $226 | $5,541 | $11,833 | $25,467 | $38,815 |

**Critical finding:**
1. **Low cash early is NOT automatically good.** Hutchinson has $74 on Day 10 but ends with $90,137. Sokolov has $1,762 on Day 10 but ends with $50,420. Low cash could mean efficient deployment OR liquidity crisis.
2. **"Deployable capital" is NOT directly measurable from replays.** We can observe cash, but we cannot observe "working capital reserve" or "committed feed cost" because these are internal to the agent's decision model.
3. **The concept is analytically useful but remains an interpretive framework**, not an observable quantity.

**Classification: NOT OBSERVABLE (as a metric) / INFERRED (as a concept)**

---

### 7. Wheat Market Loop

#### CLAIM: "Our agent has excessive BUY_PRODUCT Wheat / SELL Wheat, potentially wasteful"

**Direct evidence from replays:**

| Player | Wheat Bought (BUY_PRODUCT) | Wheat Sold (SELL) | Net | Context |
|---|---:|---:|---:|---|
| Our (101705751) | 2,071 | 1,863 | -208 | Buys more than sells |
| Our (101717011) | 2,037 | 1,834 | -203 | Buys more than sells |
| truebelief | 171 | 268 | +97 | Sells more than buys; net producer |
| Hutchinson | 274 | 109 | -165 | Buys more than sells; feed use |
| Sokolov | 765 | 756 | -9 | Near-neutral |
| Our (101294736) | 100 | 74 | -26 | Different strategy, less active |

**Critical findings:**

1. **Our agent (X1.12) buys ~2,000 Wheat and sells ~1,800 per game.** This is 10-12x more than competitors. The sheer volume of market transactions is anomalous.
2. **The net is negative (-200), meaning we buy more than we sell.** At base price $25/unit, this is a net loss of ~$5,000 on wheat trading alone.
3. **However, we cannot confirm this is "waste" without a transaction-by-transaction ledger with actual prices.** The base price shown in the replay is $25 for wheat, but we don't know the actual buy/sell prices if they vary with supply/demand.
4. **Hutchinson also has negative net wheat (-165) but earns $90,137.** So negative net wheat is not automatically fatal — but Hutchinson's volume is much smaller (274 bought vs our 2,071).
5. **The volume discrepancy is the real red flag.** Our agent processes 4,000+ wheat market transactions (2,071 buy + 1,863 sell) while Hutchinson processes only ~383. This suggests a systemic loop, not intentional trading.

**Classification: PARTIALLY_SUPPORTED — the volume anomaly is OBSERVED; the economic damage is INFERRED but NOT PROVEN without price data**

> [!IMPORTANT]
> MODEL_SPEC is correct to not call this "waste" without a ledger. But the magnitude of the loop (10x competitor volume) is a strong red flag that warrants investigation even without exact price data.

---

### 8. Endgame / Horizon-Aware Shutdown

**Evidence from daily timelines:**

| Competitor | Last Hire Day | Hands Day 29 | Hands Day 30 | Last Sell Day | Selling on Day 30? |
|---|---:|---:|---:|---:|---|
| truebelief | 27 | 0 | 0 | 29 | No |
| Hutchinson | 29 | 8 | 8 | 30 | Yes (WHEAT:2) |
| Sokolov | 29 | 8 | 8 | 30 | Yes (WHEAT:2) |
| Our (101705751) | 27 | 0 | 0 | 30 | Yes (WHEAT:14) |

**Critical findings:**

1. **truebelief drops hands to 0 on Day 29.** This is the clearest endgame signal. MODEL_SPEC X1.12 also drops desired hands to 0 from Day 29, which mirrors this.
2. **Hutchinson and Sokolov maintain hands through Day 30.** They do NOT show a dramatic shutdown. This contradicts a universal "horizon-aware shutdown" principle.
3. **All competitors sell on the last days.** Liquidation behavior is common.
4. **truebelief's crop tiles drop from 29 (Day 28) → 23 (Day 29) → 16 (Day 30).** This suggests natural crop expiration, not active liquidation of crops.
5. **Sokolov continues buying seeds through Day 29** (last seed day analysis from extracted data).

**Classification: MIXED** — truebelief shows clear endgame; Hutchinson and Sokolov do not show dramatic shutdown but do sell in endgame.

---

## Cross-Competitor Evidence Matrix

| Hypothesis | truebelief (101294736) | Hutchinson (101705751) | Sokolov (101717011) | X1.14 Counter | Overall |
|---|---|---|---|---|---|
| Workforce Capacity First | MIXED — peaks at 12 late, stays 5 early | PARTIALLY — peaks at 10 early | MIXED — stays at 8, high PASS | CONTRADICTED on 2/3 seeds | **MIXED** |
| Dense Engine Before Expansion | SUPPORTED — Q1 at Day 10 with $4,380 | SUPPORTED — Q1 at Day 13 with $2,355 | SUPPORTED — no expansion | N/A | **SUPPORTED** |
| Land Discipline (Q0+Q1 sufficient) | SUPPORTED — NW+NE | SUPPORTED — NW+NE | SUPPORTED — NW only | N/A | **SUPPORTED** |
| Productive Surface First | SUPPORTED — peak 50, low weeds | SUPPORTED — peak 44, low weeds | NOT SUPPORTED — peak 18, high weeds, still wins | CONTRADICTED — less weeds didn't help | **PARTIALLY_SUPPORTED** |
| Multi-engine Monetization | SUPPORTED — 6 products | SUPPORTED — 8 products | SUPPORTED — 8 products | N/A | **SUPPORTED** |
| Livestock as economic engine | SUPPORTED — 9C/5S, major revenue | SUPPORTED — 7C/4S/2G, major revenue | SUPPORTED — 4C/2S, major revenue | CONTRADICTED — removing sheep killed revenue | **SUPPORTED** |
| Deployable Capital | NOT OBSERVABLE | NOT OBSERVABLE | NOT OBSERVABLE | NOT OBSERVABLE | **NOT OBSERVABLE** |
| Horizon-aware shutdown | SUPPORTED — hands→0 Day 29 | NOT SUPPORTED — maintains hands | NOT SUPPORTED — maintains hands | N/A | **MIXED** |
| Backlog avoidance | SUPPORTED — 4 weed TDs | SUPPORTED — 28 weed TDs | CONTRADICTED — 148 weed TDs, still earns well | CONTRADICTED — reducing weeds reduced money | **MIXED** |
| Q2 conditional only | SUPPORTED — no Q2 | SUPPORTED — no Q2 | SUPPORTED — no Q2 | N/A | **SUPPORTED** |
| HIRE based on marginal throughput | NOT OBSERVABLE | NOT OBSERVABLE | NOT OBSERVABLE | NOT OBSERVABLE | **NOT OBSERVABLE** |
| Crop SLA Before Expansion | INFERRED | INFERRED | NOT SUPPORTED — high weeds | CONTRADICTED — crop priority worsened money | **NOT_SUPPORTED** |
| Balanced Product Monetization | SUPPORTED | SUPPORTED | SUPPORTED | N/A | **SUPPORTED** |

---

## Claims Currently Too Strong

1. **"Backlog control is decisive for elite scores"** (MODEL_SPEC §13, line 213). Evidence: Sokolov has 148 weed tile-days but earns $50,420 and beats our 2-quadrant agent. X1.14 shows weed reduction from 137→6 with money DECREASE. Backlog control is important but calling it "decisive" overstates the evidence. **Recommendation: DOWNGRADE to "associated with elite scores in Q1+ configurations".**

2. **"Workforce should be workload-derived rather than copied"** (line 215). This is a reasonable design principle but is NOT OBSERVED in the replays — it is INFERRED. We see different hand counts but cannot see the decision model behind them. **Recommendation: REFRAME as INFERRED design principle, not observed pattern.**

3. **"Crop SLA Before Expansion"** (§13 line 237). This is CONTRADICTED by X1.14 where crop maintenance priority degraded results. And by Sokolov where 148 weed tile-days coexisted with good performance. **Recommendation: DOWNGRADE to conditional hypothesis.**

4. **"Deployable Capital"** (§13 line 235). This concept is analytically useful but entirely INFERRED. No replay contains data about capital allocation decisions, reserve calculations, or payback estimates. **Recommendation: Maintain as INFERRED, do not treat as observable.**

5. **"CONSISTENT REJECTION" for Q2** (line 249). Three replays is not "consistent rejection." It is "absence in a small sample." None of the replays are from the top of the leaderboard — we don't know what the actual top competitors do. **Recommendation: REFRAME to "Q2 not observed in current 3-replay batch."**

---

## Claims Supported by Multiple Replays

1. **All competitors have livestock** — 3/3 replays. Strongest pattern.
2. **All competitors sell diversified products** — 3/3 replays. Consistent.
3. **No competitor uses Q2** — 3/3 replays. Consistent within batch.
4. **Q1 timing varies** — Day 10, Day 13, never. Clear variation.
5. **Livestock mix varies** — 9C/5S, 7C/4S/2G, 4C/2S. Clear variation.

---

## Claims Contradicted by Counterexamples

1. **"More productive surface → more money"**: Sokolov earns $50,420 with peak 18 productive tiles vs our $24,314-$38,815 with peak 28-30.
2. **"Less weeds → more money"**: X1.14 shows weed tile-days dropping from 137→6 with money decreasing from $42,491→$31,585.
3. **"Workforce Capacity First"**: X1.14 variant B regresses on 2/3 required seeds.
4. **"Crop SLA Before Expansion"**: X1.14 variants C/D with crop priority produce worse results.
5. **"Horizon-aware shutdown" as universal**: Hutchinson and Sokolov maintain hands through Day 30.

---

## Claims Not Observable from Current Data

1. **Deployable Capital** — cannot compute from replay fields
2. **HIRE based on marginal monetizable throughput** — decision logic not visible
3. **Per-transaction profit/loss for wheat trading** — no per-transaction price data in actions
4. **Opportunity cost of Q2** — no Q2 observed to compare
5. **Workload model of competitors** — internal decision state not visible
6. **Whether crop is intentionally unwatered** — high unwatered TDs for truebelief (818) suggests possible deliberate strategy or measurement artifact

---

## Causal Claims Requiring Counterfactual/Experiment

| Claim | Current Status | Required Test |
|---|---|---|
| Livestock revenue drives elite scores | INFERRED | Remove livestock from a winning strategy and measure impact |
| Weed control improves monetization | CONTRADICTED by X1.14 | Needs careful experiment: weed control + maintained livestock |
| Q1 is positive EV when capital exceeds threshold | INFERRED | Q1 vs Q0 continuation on same seed with same strategy |
| Diversified monetization beats single-engine | INFERRED | Single-engine variant vs diversified with same workforce |
| Wheat market loop is wasteful | INFERRED | Measure exact P&L per wheat transaction |

---

## Confronto con X1.14

### X1.14 Key Results

| Variant | Seed 0 | Seed 421521921 | Seed 1273000467 | Weeds | Livestock |
|---|---:|---:|---:|---:|---|
| A (X1.12 baseline) | $42,491 | $48,313 | $43,021 | 137/129/138 | 7C/4S |
| B (workforce aggressive) | $39,301 | $36,238 | $54,228 | 21/21/88 | 7C/0S or 7C/4S |
| C (+ crop priority) | $31,585 | $35,537 | $35,102 | 6/6/6 | 7C/0S |
| D (+ livestock brake) | $31,744 | $35,654 | $35,190 | 6/6/6 | 7C/0S |
| F (+ all brakes) | $439 | $496 | $449 | 8/8/8 | 0C/0S |

### Critical Interpretation

1. **Weed reduction is not inherently valuable.** C/D have 6 weed tile-days (vs truebelief's 4) but earn $31-35K (vs truebelief's $86K). The difference is NOT weed control — it's the elimination of livestock revenue.
2. **The confound is clear: variants that reduce weeds also reduce livestock (0 SHEEP).** The weed improvement and livestock suppression are coupled in X1.14's implementation. This makes it impossible to attribute the revenue change to either factor alone.
3. **Variant B on seed 1273000467 ($54,228 vs $43,021) is the ONLY improvement.** But on required seeds it regresses. This strongly suggests that workforce aggressiveness interacts with seed-specific factors.
4. **Variant F ($439-$519) shows that removing livestock entirely is catastrophic.** This is the strongest evidence FOR livestock as an essential engine.

### MODEL_SPEC's Current Interpretation

MODEL_SPEC line 307: "Workforce Capacity First is not adopted as tested; the next model should combine workload-based capacity with explicit monetization density and Q1 payback rather than hiring/crop-priority alone."

**Assessment:** This interpretation is reasonable but somewhat stronger than warranted. The X1.14 evidence actually shows that **crop priority without maintained livestock revenue is destructive**, not that workforce capacity needs to be "combined with monetization density." The correct lesson may be simpler: **don't suppress livestock revenue to improve crop metrics.**

---

## Recommended MODEL_SPEC Patch Plan

| Claim / Section | Current Status | Proposed Action | Rationale |
|---|---|---|---|
| "Backlog control is decisive" (§13) | OBSERVED_REFERENCE | **DOWNGRADE** to "associated with elite Q1+ configurations" | Sokolov counterexample; X1.14 weed reduction didn't help |
| "Workforce should be workload-derived" (§13) | INFERRED | **REFRAME** to "INFERRED design principle; not directly observed in replays" | Decision logic is not visible in replay data |
| "Crop SLA Before Expansion" (§13) | INFERRED | **DOWNGRADE** to "NEEDS_MORE_EVIDENCE" | Contradicted by X1.14; Sokolov counterexample |
| "Deployable Capital" concept (§13) | INFERRED | **KEEP** as INFERRED, add explicit "NOT OBSERVABLE from replay data" | Useful concept but not measurable |
| "CONSISTENT REJECTION" for Q2 (§13) | Stated as conclusion | **REFRAME** to "not observed in 3-replay batch; insufficient sample for rejection" | n=3 is not "consistent rejection" |
| "7 Cow / 4 Sheep" as OBSERVED_REFERENCE (§14) | OBSERVED_REFERENCE | **KEEP** | Correctly classified |
| "Cross-Competitor Invariants" section title (§13) | Implies invariance | **REFRAME** to "Cross-Competitor Patterns" | 3 replays cannot establish invariants |
| "Horizon-aware shutdown" | INFERRED | **DOWNGRADE** to "observed in 1/3 competitors; not universal" | Only truebelief shows clear shutdown |
| Livestock as essential engine | INFERRED | **KEEP**, add note about attrition evidence | X1.14 variant F confirms; 3/3 competitors confirm |
| Wheat market loop diagnosis | INFERRED | **KEEP**, add "volume anomaly is OBSERVED; economic damage is INFERRED" | Volume difference is 10x; damage unproven without ledger |
| §7 unwatered tile-days interpretation | Not explicitly discussed | **ADD** warning about truebelief having highest unwatered TDs (818) | May be measurement artifact or deliberate strategy |
| Animal attrition | Not discussed | **ADD** observation that bought != final livestock count | truebelief: bought 9C/5S, ended 9C/5S (no loss); Hutchinson: bought 8C, ended 7C (1 lost); Sokolov: bought 6C, ended 4C (2 lost) |

---

## What Should NOT Be Changed Yet

1. **Section 4 (trigger/target table)**: Implementation details are correct for X1.12 and should not change without a new BUILD.
2. **Section 6 (benchmark targets)**: The $80,000 target and seed list are research goals, not MODEL_SPEC claims.
3. **Section 9-10 (protocol and discipline)**: Process documentation, not empirical claims.
4. **Section 11 (change log)**: Historical record, should only be appended.
5. **Section 12 (X1.13 results)**: Verified experimental results, correctly documented.
6. **Section 14 (X1.14 results)**: Verified experimental results, correctly documented.
7. **Livestock as economic engine**: Well-supported by evidence; do not weaken.
8. **Multi-engine monetization**: Well-supported; do not weaken.

---

## Open Questions for Next Benchmark Batch

1. **Do top-tier competitors (rank 1-5) use Q2?** Current batch may not include the actual best strategies.
2. **Is the unwatered tile-day metric measuring what we think?** truebelief's 818 unwatered TDs suggests either a measurement issue or a deliberate strategy.
3. **What are actual market prices?** Base prices are visible but dynamic pricing is not confirmed or denied.
4. **Are there competitors with Q0+Q1+Q2 who outperform Q0+Q1?** We cannot reject Q2 from 3 replays.
5. **Is Sokolov's strategy reproducible?** His high-PASS, one-quadrant, moderate-livestock strategy is very different from the elite Q1 strategies. Is this a fundamentally different viable archetype or just a weaker strategy that happened to beat our weak agent?
6. **What is the effect of animal attrition?** Buying 6 cows but ending with 4 (Sokolov) suggests maintenance failures that cost revenue. Is this a significant factor?
7. **Coop tiles**: Hutchinson has `coop_tiles=4` (Goose housing). This tile type is not discussed in MODEL_SPEC. What are its economics?

---

## Verification Summary

- **Replays analyzed**: 3 (`101294736`, `101705751`, `101717011`)
- **MODEL_SPEC claims analyzed**: 13 major hypotheses
- **Classification counts**:
  - SUPPORTED: 5 (Livestock engine, Multi-engine monetization, Q2 absence, Dense engine before expansion, Land discipline)
  - PARTIALLY_SUPPORTED: 3 (Workforce state-dependent, Productive surface, Wheat loop)
  - MIXED: 3 (Workforce capacity first, Backlog avoidance, Horizon-aware shutdown)
  - NOT_SUPPORTED: 1 (Crop SLA Before Expansion)
  - CONTRADICTED: 0 (as standalone claims, though several have counterexamples)
  - NOT OBSERVABLE: 2 (Deployable Capital, HIRE based on marginal throughput)

### Five Most Solid Claims

1. **All competitors have livestock** — 3/3, no exceptions
2. **Multi-engine monetization** — 3/3, confirmed by revenue analysis
3. **Q2 absent in batch** — 3/3, clear observation
4. **Livestock mix varies** — 3/3, clear variation
5. **Dense engine before expansion** — 3/3 (or 2/3 who expand)

### Five Most Weakly Supported Claims

1. **"Backlog control is decisive"** — contradicted by Sokolov and X1.14
2. **"Crop SLA Before Expansion"** — contradicted by X1.14
3. **"Horizon-aware shutdown"** — only truebelief shows it
4. **"Deployable Capital"** — entirely inferred, not measurable
5. **"HIRE based on marginal monetizable throughput"** — not observable, not tested successfully

### Contradictions with X1.14

1. Weed reduction does not improve money when coupled with livestock suppression
2. Crop maintenance priority worsens results
3. Workforce aggressiveness is seed-dependent
4. Livestock brake suppresses revenue even when crop metrics improve

---

## Files Created

- `results/benchmark/MODEL_SPEC_CRITICAL_REVIEW.md` (this file)
- `results/benchmark/MODEL_SPEC_EVIDENCE_MATRIX.csv`

## Files Modified

- None

---

MODEL_SPEC CRITICAL REVIEW: COMPLETE

STRATEGY CODE: NOT MODIFIED

MODEL_SPEC: NOT MODIFIED — PATCH PLAN ONLY
