## E12 — Competitive Architecture Reconstruction and Replay-Grounded Optimization

**Date:** 2026-08-27 to 2026-08-28  
**Phase:** iterative DEFINE → BUILD → VERIFY → differential diagnosis; X1.12 BUILD in progress  
**Tools:** Antigravity, Codex, GitHub Copilot Agent, ChatGPT, manual browser supervision  

### Objective

Move beyond marginal tuning and reconstruct a Kaggriculture architecture capable of reaching **final_money >= 80,000** on Q0+Q1, using primary competitive replay evidence rather than visual imitation or single-metric leaderboard comparison.

### X1.8 — Livestock-first architecture

- Built a centered livestock core and introduced Cow/feed handling.
- First crop expansion was too late and productive capacity remained insufficient.
- Established the need for a better Day-1 growth architecture.

### X1.9 — Growth-first architecture

- Day 1 successfully filled Q0 outside the pasture core.
- Q1 was purchased on Day 2 and Q2 later.
- Local final money around 8.7k; Kaggle observation against `truebelief`: 6,825 vs 86,297.
- Audit showed that purchased Q1/Q2 were largely unused after harvest/replant cycles.
- Dominant problem: working-set/maintenance exclusion, not lack of Hands.

### X1.10 — Continuous Productive Surface

Mode: `E12_CONTINUOUS_SURFACE_X110`

- Maintained very high physical utilization.
- Q1 Day 2; Q2 later after CPS stabilization.
- Local final money collapsed to approximately **825** on both principal diagnostic seeds.

Exact economic reconciliation showed no accounting bug. Main sinks were seed purchasing, retail Wheat, low/negative-value crop allocation and Q2 expansion. CPS itself worked physically but did not produce economic value.

Key lesson:

> **Physical utilization is not the objective. Continuous use of economically poor tiles can destroy capital.**

### Milk-pipeline verification

A dedicated subsystem trace corrected the earlier interpretation that livestock itself was economically destructive.

Findings:

- Milk collection uses `HARVEST`, not `COLLECT`.
- Cow warm-up = 8 days.
- X1.10 bought cows too late for adequate monetization.
- Hand livestock support contained a target-position dispatch bug.
- Milk harvested by a worker enters worker inventory and must reach shed inventory via logistics before `SELL` can monetize it.

Therefore X1.10's zero Milk revenue was primarily a functional/scheduling/logistics failure, not proof that cows have negative EV.

### X1.11 — Q0+Q1 80k engine attempt

Mode: `E12_Q0Q1_80K_ENGINE_X111`

Hard target:

- seed 0 >=80,000
- seed 421521921 >=80,000
- Q0+Q1 only
- source/submission behavioral equivalence

Verified results:

- seed 0: **29,858**
- seed 421521921: **24,827**

Both fail the 80k gate. The residual deficit was judged too large for marginal optimization.

### Acquisition of primary `truebelief` replay

Reference Kaggle episode:

- Episode ID: `101294736`
- Submission ID: `55829861`
- Seed: `421521921`
- Competitor: `truebelief`
- Our observed episode result: `6,825`
- truebelief result: **`86,297`**

The legacy episode-service API failed. Manual browser inspection of the authenticated Kaggle page discovered the current frontend replay endpoint:

`https://www.kaggle.com/competitions/episodes/101294736/replay.json`

The raw replay was downloaded and preserved in the repository as:

`results/e12/x111/101294736.json`

SHA-256:

`6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695`

This browser intervention became an important supervision/provenance lesson: when official/legacy APIs fail, inspect the real authenticated frontend traffic rather than inferring that replay data is unavailable.

### Reproducible truebelief benchmark

Codex rebuilt the comparison directly from the complete raw JSON rather than relying on a textual synthesis.

Artifacts:

- `scripts/benchmark_e12_x1_11_truebelief.py`
- `results/e12/x111/TRUEBELIEF_BENCHMARK.md`
- `results/e12/x111/truebelief_benchmark.json`
- `results/e12/x111/x111_truebelief_comparison_timeline.csv`
- `results/e12/x111/101294736.json`

Behavioral-equivalence test remained passing.

Main comparison:

- X1.11 same seed: **24,827**
- truebelief: **86,297**
- gap: **61,470**
- truebelief = **3.48×** X1.11
- X1.11 = **28.8%** of truebelief

### Replay-grounded architectural findings

Observed reference trajectory:

- Q0 fully productive from Day 1.
- Day-1 crop diversification: Wheat + Melon + Strawberry.
- Q1 not purchased until Day 11; Q2 never purchased.
- Livestock acquisition begins before Q1.
- Mature active livestock around 7 Cow + 4 Sheep.
- Monetization includes Milk, Wool and Fertilizer.
- Peak workforce 12 Hands; aggregate HIRE 231.
- Q0+Q1 reaches up to 50/50 productive tiles around the mature phase.
- Later crop surface declines while cash accelerates sharply.
- Days 29–30 show no Hands and clear horizon-aware wind-down.

Aggregate market quantities observed in the replay:

- HIRE 231
- BUY_PRODUCT Wheat 171
- BUY_SEED Wheat 86
- BUY_SEED Strawberry 22
- BUY_SEED Melon 21
- BUY_ANIMAL Cow 9
- BUY_ANIMAL Sheep 5
- BUY_LAND 1
- SELL Wheat 268
- SELL Fertilizer 138
- SELL Milk 134
- SELL Melon 108
- SELL Wool 70
- SELL Strawberry 69

These values are reference evidence, not policy constants.

### X1.12 — current BUILD

X1.12 is defined as a reconstruction of the **economic mechanisms** behind the reference trajectory, not a clone of one episode and not a marginal X1.11 tuning pass.

Primary mechanisms under reconstruction:

- diversified opening;
- Q0 compounding before Q1;
- economically gated land expansion;
- early Cow + Sheep architecture;
- full Milk/Wool/Fertilizer pipeline;
- dynamic feed economics;
- elastic workforce;
- harvest/logistics/selling throughput;
- Wheat as operational commodity when justified;
- realized net contribution/time-to-cash crop selection;
- horizon-aware liquidation.

Hard local success gate remains >=80,000 on both required seeds. The user will perform the final Kaggle upload manually.

### Methodological evolution — competitive learning loop

E12 established a new optimization protocol:

`OBSERVE → CAPTURE → COMPARE → DEFINE → BUILD → VERIFY → KAGGLE → REPLAY → COMPARE`

Target operating cadence after X1.12: **one strong competitor per day**.

The purpose is to reduce overfitting to a single opponent and evolve a parameterized policy. Each competitor replay is treated as a source of hypotheses rather than a blueprint.

Preferred multi-agent division of labor:

- Work/browser agent captures the strongest useful opponent episode as raw JSON with provenance/checksum;
- Codex reconstructs and benchmarks it against our current model, then implements and verifies adaptive changes;
- the human supervisor chooses the objective/competitor and manually publishes the candidate to Kaggle.

Critical handoff principle:

> **Pass primary artifacts between agents. A textual synthesis may accompany the replay, but must not replace the complete raw JSON.**

