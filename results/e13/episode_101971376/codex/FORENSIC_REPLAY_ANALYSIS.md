# E13 Forensic Replay Analysis: Episode 101971376

## Replay Identity

- Episode: `101971376`
- Seed: `1630102796`
- SHA-256: `7afdf3b8672c1828bf7520e8f5973f69ad11e8378155a77aa7c4b5eaf4480db4`
- Steps: `720`
- Statuses: `['DONE', 'DONE']`
- Player 0: `Pietro Valocchi`, reward `$7,123`
- Player 1: `Harith Al-Ani`, reward `$133,049`

## Material Divergence

Material divergence is defined as the first end-of-day point where Harith's cash gap exceeds `$1,000`, at least one capacity dimension also diverges materially (`productive gap >= 8`, `land gap >= 1`, or livestock gap `>= 3`), and the cash lead remains positive afterwards.

Detected first material divergence:

- Day: `12`
- Cash gap: `$2,419`
- Productive tile gap: `41`
- Land/quadrant gap: `1`
- Livestock count gap: `7`

The divergence is not a single superficial variable. It becomes persistent because capacity differences turn into more worker actions, more output, more sells, and more reinvestment room.

## Final State

| Player | Money | Quadrants | Productive | Crop | Pasture | Empty owned | Weeds | Hands | Livestock |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| Pietro Valocchi | `$7,123` | `NE,NW,SW` | 18 | 0 | 18 | 54 | 3 | 12 | `{'COW': 13, 'SHEEP': 4}` |
| Harith Al-Ani | `$133,049` | `NE,NW,SW` | 22 | 5 | 17 | 47 | 6 | 7 | `{'COW': 8, 'SHEEP': 7}` |

## Action Throughput

| Player | Worker actions | Productive/logistics actions | Productive share | Movement | Idle | Crop care | Livestock care | Logistics | Harvest/collect |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Pietro Valocchi | 7080 | 1939 | 27.39% | 4936 | 205 | 259 | 636 | 646 | 398 |
| Harith Al-Ani | 7135 | 3037 | 42.56% | 3464 | 634 | 1333 | 704 | 686 | 314 |

## Market Ledger Summary

Values are reconstructed from observed market prices when available, falling back to base prices only when needed. HIRE cost is not valued because the replay action does not encode a direct price per HIRE order.

| Player | Estimated sell value | Estimated buy value excluding HIRE | Top sells | Top buys |
|---|---:|---:|---|---|
| Pietro Valocchi | `$83,418` | `$77,082` | `{'WHEAT': 712, 'MILK': 242, 'WOOL': 84, 'FERTILIZER': 16}` | `{'WHEAT': 916, 'STRAWBERRY': 63, 'MELON': 20, 'COW': 14, 'CARROT': 6, 'SHEEP': 4, 'BUY_LAND': 2}` |
| Harith Al-Ani | `$171,870` | `$45,694` | `{'WHEAT': 253, 'STRAWBERRY': 239, 'FERTILIZER': 228, 'MILK': 208, 'WOOL': 162, 'MELON': 84}` | `{'WHEAT': 404, 'STRAWBERRY': 42, 'MELON': 17, 'SHEEP': 12, 'COW': 8, 'BUY_LAND': 2}` |

## Gap Decomposition

### Cause 1 — Persistent capacity compounding

**Status:** OBSERVED

**Evidence:** Harith establishes the first material divergence on Day `12` and ends with a much larger cash position. The daily timeline shows land/productive/livestock dimensions diverging before the late game.

**Economic mechanism:** capacity -> actions -> output/inventory -> SELL -> cash -> reinvestment.

**Confidence:** HIGH

**Alternative explanation:** Some of the lead may be seed/path-specific tactical routing rather than strategic architecture.

### Cause 2 — More monetized market output

**Status:** OBSERVED

**Evidence:** Harith estimated sell value `$171,870` versus Pietro `$83,418`. Harith's top sells are `{'WHEAT': 253, 'STRAWBERRY': 239, 'FERTILIZER': 228, 'MILK': 208, 'WOOL': 162, 'MELON': 84}`.

**Economic mechanism:** larger and broader product conversion creates cash that can be reinvested instead of remaining as uncollected potential.

**Confidence:** HIGH

**Alternative explanation:** Exact dynamic prices may differ; the ledger is still action-derived, not a native transaction journal.

### Cause 3 — Land/surface used as throughput, not just ownership

**Status:** OBSERVED / INFERRED

**Evidence:** Harith reaches more quadrants and productive capacity, while the action ledger shows the surface is paired with more productive/logistics activity.

**Economic mechanism:** owned land matters only after it is activated, maintained, harvested and sold.

**Confidence:** MEDIUM

**Alternative explanation:** Stronger market timing or livestock may dominate the apparent land effect.

### Cause 4 — Livestock/product engine scale

**Status:** OBSERVED

**Evidence:** Harith's sell ledger includes animal products/Fertilizer at much higher monetized volume than Pietro.

**Economic mechanism:** feed/care/harvest/collection cycles compound into Milk/Wool/Egg/Fertilizer cash.

**Confidence:** MEDIUM

**Alternative explanation:** Crop revenue and land expansion are entangled with livestock support.

### Cause 5 — Early gap is amplified rather than created late

**Status:** OBSERVED

**Evidence:** The material divergence detector identifies Day `12`, not the final phase, as the first persistent break.

**Economic mechanism:** late game is the cash-out of a pre-existing production system.

**Confidence:** HIGH

**Alternative explanation:** Late liquidation timing can still amplify the final dollar gap.

## Simple Hypotheses

See `EVIDENCE_MATRIX.csv` for the full matrix. The clearest falsification is that the gap is mainly late game: the persistent material divergence starts earlier and compounds.

## Local vs Kaggle Fidelity Pointers

Useful future fidelity metrics from this replay:

- day of persistent cash/capacity divergence;
- market sell value by engine;
- productive action share;
- Q1/Q2 activation state before/after purchase;
- livestock product collection/sell lag;
- Wheat buy/sell ledger with actual prices.

## Not Observable

- Internal decision intent.
- Exact HIRE cost from action records.
- True per-transaction P/L if dynamic prices differ from observed/base price at action time.
- Opportunity cost of alternative actions not taken.
- Causal allocation of exact dollar gap across causes.
