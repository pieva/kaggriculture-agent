# X1.13 Dynamic Allocation Counterfactual Log

Primary seeds: `0`, `421521921`.

Conclusion: no X1.13 variant produced a structural improvement over X1.12. Variant B improved crop surface and reduced weed/unwatered tile-days, but final money fell sharply because the livestock gate suppressed Milk/Wool/Fertilizer revenue. Variants C/D/E worsened cash conversion and did not pass the Q2 gate.

| Variant | Seed | Final | Mean Crop | Peak Crop | Weeds TD | Empty TD | Unwatered TD | Prod/Move | Livestock | Q2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| A | 0 | $42,491 | 17.47 | 26 | 137 | 309 | 137 | 0.393 | 7C/4S | no |
| A | 421521921 | $48,313 | 17.47 | 26 | 129 | 317 | 137 | 0.393 | 7C/4S | no |
| B | 0 | $34,230 | 21.53 | 37 | 56 | 288 | 111 | 0.239 | 0C/0S | no |
| B | 421521921 | $30,389 | 21.53 | 37 | 56 | 288 | 111 | 0.239 | 0C/0S | no |
| C | 0 | $1,311 | 11.77 | 21 | 41 | 661 | 79 | 0.485 | 0C/0S | no |
| C | 421521921 | $2,329 | 12 | 21 | 50 | 645 | 85 | 0.486 | 0C/0S | no |
| D | 0 | $1,311 | 11.77 | 21 | 41 | 661 | 79 | 0.485 | 0C/0S | no |
| D | 421521921 | $2,329 | 12 | 21 | 50 | 645 | 85 | 0.486 | 0C/0S | no |
| E | 0 | $9,673 | 12.5 | 20 | 30 | 605 | 81 | 0.366 | 0C/0S | no |
| E | 421521921 | $8,988 | 11.73 | 20 | 33 | 623 | 66 | 0.343 | 0C/0S | no |

## Variant Definitions

- A: X1.12 baseline unchanged.
- B: livestock dynamic gate, Q2 disabled.
- C: livestock dynamic gate plus workload-based HIRE, Q2 disabled.
- D: livestock dynamic gate plus workload-based HIRE plus dynamic Q2 gate.
- E: D plus crop-SLA-first assignment under crop degradation pressure.

## Measured Diagnosis

- Livestock de-hardcoding is directionally valid, but the first gate is too conservative: all X1.13 variants B-E ended with `0 Cow / 0 Sheep`.
- Crop surface alone is not sufficient: B raised mean/peak crop tiles to `21.53/37` but dropped to `$34,230 / $30,389`.
- Workload-based HIRE implementation C/D reduced HIRE spend but starved operational capacity and cash conversion.
- Q2 gate did not fire in D/E, so Q2 remains unvalidated rather than rejected as a concept.
- Assignment fix E reduced weeds but increased harvested-empty backlog and did not recover revenue.

## Machine-Readable Artifacts

- JSON: `experiments/archive/e12/artifacts/x113/counterfactual_results.json`
- CSV: `experiments/archive/e12/artifacts/x113/counterfactual_results.csv`
