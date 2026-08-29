# E11-X1.3 — BUILD + VERIFY — E06 Productive Unit Replication & Scaling

## Executive Summary

The experiment **E11-X1.3** shifts the project perspective to treat **E06** (`WaterFirstHIRENWClusterROIAgent`) as an **Elementary Productive Unit (EPU)** to replicate and scale:

$$\text{1× EPU (9 tiles, 1Q)} \longrightarrow \text{2× EPU (18 tiles, 2Q)} \longrightarrow \text{3× EPU (27 tiles, 3Q)}$$

Subphase A (**1× EPU Replication**) achieved **100.0% exact replication** of the E06 baseline figure ($25,847.00 on seed 0) and a mean money of **$26,888.40** (+1,209.6% over the E11-VB1 baseline of $2,059.00).

Subphase B (**2× EPU Scaling**) activated EPU2 on 18 tiles (2Q) following a derived land purchase trigger on Day 14 ($1,435 working capital threshold), reaching **$28,727.40** mean money (+6.8% money gain over 1× EPU) with 100% active EPU2 tile utilization (18/18 active tiles).

Because Subphase B achieved a Scaling Efficiency of **53.4%** ($< 60.0\%$), **STOP GATE B IS ENFORCED**. In accordance with protocol guidelines, execution was halted before Subphase C to diagnose the exact 2× scaling bottleneck.

---

## 1. Verified Evidence Base & Comparative Matrix

### Verified Machine Benchmark Records:
- **X1.3-A (1× EPU):** `E11-X1.3-A-20260827-095542` (5 paired episodes)
- **X1.3-B (2× EPU):** `E11-X1.3-B-20260827-100010` (5 paired episodes)

| Benchmark / Subphase | Managed Footprint | Owned Land | Workforce | Mean Money ($) | Median Money ($) | Equivalence vs E06 Ref | Scaling Efficiency | SHA-256 Provenance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E11-VB1 Control** | 16.9 tiles | 2Q (50t) | 2.0 workers | $2,059.00 | $1,518.00 | 8.0% | - | `PASS` |
| **E06 Reference (Seed 0)** | 9 tiles | 1Q (25t) | 2.0 workers | $25,847.00 | $25,847.00 | **100.0%** | - | `PASS` |
| **X1.3-A (1× EPU)** | 9 tiles | 1Q (25t) | 2.0 workers | **$26,888.40** | $25,847.00 | **104.0%** | **100.0%** | `PASS` |
| **X1.3-B (2× EPU)** | 18 tiles | 2Q (50t) | 3.0 workers | **$28,727.40** | **$29,244.00** | **111.1%** | **53.4%** | `PASS` |
| **X1.3-C (3× EPU)** | 27 tiles | 3Q (75t) | - | *Not Executed* | *Not Executed* | - | - | **STOP B ENFORCED** |
| **Top Competitors** | 35–45 tiles | 3Q (75t) | 4–6 workers | ~$70,000+ | ~$75,000+ | ~290% | - | External Ceiling |

---

## 2. Subphase Breakdown & Stop Gate Evaluation

### Subphase A: 1× EPU Replication (9 Tiles) — `PASSED`
- **Goal:** Replicate exact E06 mechanism (`WaterFirstHIRENWClusterROIAgent`) inside `ProductiveMassROIAgent` without land expansion.
- **Diagnostic A0 (Seed 0):** **$25,847.00** (100.0% exact match to E06 reference).
- **Stage B Benchmark (5 Paired Episodes):** **$26,888.40** Mean Money.
- **Gate A Verdict:** **`PASSED`** (104.0% equivalence ratio vs E06 reference $\ge 50\%$).

### Subphase B: 2× EPU Scaling (18 Tiles) — `STOP GATE B ENFORCED`
- **Goal:** Scale to 18 active productive tiles across 2 quadrants (Q0 9 NW tiles + Q1 9 NE tiles) with 3 workers (1 Farmer + 2 Hands).
- **Causal Sequence Verified:** EPU1 operates on Q0 $\rightarrow$ Generates cash surplus ($\ge \$1,435.00$) $\rightarrow$ Buys Q1 on Day 14 $\rightarrow$ Activates EPU2 on Day 15 with Hand 2.
- **Stage B Benchmark (5 Paired Episodes):** **$28,727.40** Mean Money.
- **Scaling Ratio B:** $\frac{\$28,727.40}{\$26,888.40} = 1.0684\times (+6.8\text{ gain})$
- **Scaling Efficiency B:** $\frac{1.0684}{2} = \mathbf{53.4\%}$
- **Gate B Verdict:** **`STOP GATE B ENFORCED`** ($\text{Efficiency } B = 53.4\% < 60.0\%$).

---

## 3. Diagnostic Root Cause Analysis of Scaling Bottleneck B

The quantitative gap in 2× EPU scaling efficiency (53.4% vs 100.0% ideal) is caused by two fundamental mechanics:

1. **EPU2 Activation Horizon (Day 15–29):**
   EPU1 operates for the full 30 days of the episode. EPU2 is unlocked only after EPU1 generates sufficient cash to buy Q1 ($1,435 threshold reached on Day 14 post-harvest). Consequently, EPU2 operates for only **15 days** (half the episode).
2. **Land Purchase Capital Deduction ($1,000):**
   Buying Q1 deducts $1,000 from final liquid cash. EPU2 generates **+$2,839.00** in gross crop sales during its 15 active days, leaving a net incremental money gain of **+$1,839.00** after land and seed costs.
3. **Episode Hard Cap (30 Days):**
   In a fixed 30-day game, land acquired after Day 10 has insufficient remaining turns to double cumulative revenue.

---

## 4. SHA-256 Fingerprints & Auditability

```json
{
  "subphase_a_run_id": "E11-X1.3-A-20260827-095542",
  "subphase_a_config_sha256": "f55ad2ed71563634eefd208fe606e987acb7654a888c3fcdffefb0efacda5643",
  "subphase_a_episodes_sha256": "50b23f87f6ea1f79a95786ed8d3cf26e6c79a97eecfc6d6eeeb3d3e6488d5e1b",
  "subphase_b_run_id": "E11-X1.3-B-20260827-100010",
  "subphase_b_config_sha256": "8cfdab7e1c019fc63b028ffbfcecfbcac2d854ef244eb5b1db320f785cfa874f",
  "subphase_b_episodes_sha256": "ba9fadea3de5096dad49bcfbcff292e448bdfb1bfefaf81f9a1fbbd0a7a0b38d",
  "provenance_verifier": "PASS"
}
```

---

## 5. Conclusions & Next Experimental Step

1. **E06 Mechanism Fully Replicated:** `ProductiveMassROIAgent` in `E06_REPLICATED` mode matches E06 to the exact cent (**$25,847.00** on seed 0) and averages **$26,888.40** across 5 seeds.
2. **Causal EPU Scaling Validated:** Subphase B demonstrated the complete sequence: EPU1 surplus $\rightarrow$ derived land purchase ($1,435) $\rightarrow$ EPU2 18-tile deployment with 3 workers $\rightarrow$ **$28,727.40** mean final money.
3. **Next Step (E11-X1.4 — Fast ROI Crop Rotation for EPU2):**
   To resolve the 53.4% scaling bottleneck caused by EPU2's late start (Day 15), EPU2 must utilize fast 3-day ROI crop rotations (Carrot/Wheat) post-expansion to squeeze 4–5 harvest cycles out of the remaining 15 days, maximizing EPU2 net yield before Day 30.
