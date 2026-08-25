# E05-01 — HIRE Capability & Experimental Design Analysis

We are starting **E05** of the Kaggriculture Agent project.

Follow the project methodology strictly:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

This prompt covers **DEFINE only**.

Do **not** implement E05 yet.  
Do **not** modify the production agent.  
Do **not** create the E05 implementation plan yet.  
Do **not** change the submission artifact.

## 1. Experimental context

The project has completed four supervised experiments:

- **E01 — Baseline**
- **E02 — Dynamic Crop Selection & ROI Scaling**
- **E03 — Multi-Tile Scaling**
- **E04 — Initial NW Scaling**

E03 established a strong 4-tile production strategy:

- Agent: `MultiTileROIAgent`
- Mean Final Money: `$14682.47 ± $1164.33`
- Win Rate vs starter: `100%`

E04 tested spatial scaling from **4 to 9 tiles** while deliberately retaining:

- a single farmer;
- the E03 operational policy;
- no `BUY_LAND`;
- no `HIRE`.

E04 used the NW footprint:

`{(x,y) | x ∈ [2,4], y ∈ [2,4]}`

E04 results:

- Completion Rate: `100%`
- Disqualification Rate: `0%`
- Overall Win Rate: `100%`
- Mean Final Money: `$11232.47 ± $661.26`
- Difference vs E03: `-$3450.00`
- Relative difference vs E03: `-23.49%`
- Total Weed Conversions: `238`
- Mean Unwatered End-of-Day Ratio: `3.33%`

The E04 economic hypothesis was therefore **FALSIFIED**.

The evidence suggests that simply increasing the production footprint while retaining a single worker does not scale economically.

## 2. Candidate direction for E05

The selected direction is:

**HIRE / Multi-Worker Scaling**

The working hypothesis is that the E04 regression may be caused primarily by a **worker-capacity / scheduling bottleneck**.

E05 should investigate whether introducing additional workers through `HIRE` can make the existing 9-tile E04 footprint economically sustainable.

At this stage this is only a hypothesis.

Do not assume that `HIRE` is beneficial.

## 3. First task — inspect HIRE semantics

Inspect the actual Kaggriculture environment, installed package/source code, available documentation, schemas, action definitions, examples and existing project code as appropriate.

Determine precisely how `HIRE` works.

At minimum establish:

1. whether `HIRE` is actually available to the agent;
2. the exact action syntax/schema;
3. the monetary or other cost of hiring;
4. when the cost is charged;
5. what entity is created by `HIRE`;
6. whether multiple workers can exist simultaneously;
7. whether there is a maximum worker count;
8. whether workers persist for the whole episode or have another lifetime;
9. how hired workers receive or select actions;
10. whether the main farmer explicitly controls workers;
11. whether workers have independent positions;
12. whether movement is required;
13. whether workers share inventory, money, land ownership or other state;
14. whether workers can perform the same actions as the original farmer;
15. whether there are restrictions on planting, watering, harvesting or other relevant actions;
16. how hired workers interact with the environment's turn/action model;
17. whether using multiple workers changes action timing, latency or timeout risk;
18. any other semantic constraint that materially affects an E05 experimental design.

Do not infer undocumented behavior if it can be established from the environment implementation.

For every important conclusion, identify the code, schema, documentation or runtime evidence that supports it.

## 4. Inspect compatibility with the current architecture

Review the current E03/E04 agent architecture and determine what would have to change conceptually to support `HIRE`.

Focus on:

- state representation;
- worker identification;
- action generation;
- tile assignment;
- scheduling;
- movement;
- collision or contention risk;
- shared economic decisions;
- crop selection;
- watering;
- harvesting;
- planting;
- end-of-day behavior;
- serialization / standalone submission compatibility.

Do not implement these changes.

Identify which existing E04 components could remain unchanged and which would necessarily need modification.

## 5. Experimental isolation

Evaluate whether a clean E05 experiment can be constructed with:

**Control: E04**
- 9-tile NW footprint;
- single farmer;
- existing E03-derived operational policy.

**Treatment: E05**
- same 9-tile NW footprint;
- same crop-selection logic where technically possible;
- additional worker capacity introduced through `HIRE`.

The purpose is to isolate the effect of additional worker capacity.

Do not introduce unrelated optimizations unless `HIRE` semantics make a minimal supporting change unavoidable.

In particular, do not combine E05 with:

- `DIG` / weed recovery;
- Water-First scheduling experiments;
- `BUY_LAND`;
- footprint resizing;
- new crop-economic heuristics;
- unrelated optimization of the E03/E04 policy.

If a supporting architectural change is unavoidable, distinguish it explicitly from the experimental variable.

## 6. Determine viable HIRE treatments

Based on the actual environment semantics, identify the smallest useful set of candidate E05 treatments.

For example, if supported by the environment, possibilities might include:

- one additional worker;
- more than one additional worker;
- fixed hiring at episode start;
- economically conditional hiring;
- spatial partitioning of the 9-tile footprint.

These are examples only.

Do not adopt them unless justified by the environment.

Prefer the **simplest treatment capable of testing the capacity hypothesis**.

Avoid turning E05 into a broad multi-variable optimization experiment.

## 7. Economic break-even analysis

If the environment exposes a deterministic hiring cost, calculate the economic implications.

Determine:

- direct cost of `HIRE`;
- minimum additional production required to recover that cost;
- whether repeated hiring would require separate break-even thresholds;
- whether the 720-step episode length materially constrains payback;
- whether hiring immediately versus later has an obvious economic implication.

Clearly distinguish:

- facts established from the environment;
- calculations based on those facts;
- experimental hypotheses that still require measurement.

Do not fabricate missing economic parameters.

## 8. Success criteria proposal

Propose measurable criteria for E05.

The primary comparison must be:

**E05 vs E04**

E04 reference:

`Mean Final Money = $11232.47 ± $661.26`

Also retain E03 as the higher economic reference:

`Mean Final Money = $14682.47 ± $1164.33`

At minimum consider:

- Completion Rate;
- Disqualification Rate;
- Mean Final Money;
- standard deviation (`ddof=1`);
- Median Final Money;
- absolute difference vs E04;
- percentage difference vs E04;
- comparison with E03;
- Win Rate overall and by opponent;
- worker utilization metrics, if measurable;
- watering / crop-loss indicators already available from E04;
- action latency and timeout safety.

Distinguish between:

1. **minimum success** — HIRE materially improves E04;
2. **strong success** — 9-tile multi-worker scaling reaches or exceeds the E03 economic reference;
3. **failure** — additional worker capacity does not economically compensate for its cost/complexity.

Do not choose arbitrary numerical thresholds unless there is a defensible reason for them.

## 9. Threats to validity

Identify threats that could prevent E05 from answering the intended question cleanly.

Consider at least:

- hiring cost masking productivity gains;
- worker under-utilization;
- action conflicts;
- inefficient spatial allocation;
- movement overhead;
- crop starvation;
- watering starvation;
- weed conversion;
- shared-resource contention;
- increased action-generation complexity;
- latency;
- opponent-specific effects;
- stochastic variance.

Separate problems caused by **HIRE economics** from problems caused by a potentially poor first implementation of worker scheduling.

This distinction will be important during REVIEW.

## 10. Required deliverable

Create:

`docs/experiments/E05-01_HIRE_Capability_Analysis.md`

The document should contain:

1. **Objective**
2. **E04 evidence motivating E05**
3. **Verified HIRE semantics**
4. **Evidence / source references**
5. **Compatibility with current E04 architecture**
6. **Candidate minimal treatments**
7. **Economic / break-even considerations**
8. **Recommended experimental variable**
9. **Variables to hold constant**
10. **Proposed success/failure criteria**
11. **Threats to validity**
12. **Open questions**
13. **Recommendation for E05 PLAN**

Finish with one explicit recommendation:

- `PROCEED TO PLAN`
- `REVISE EXPERIMENTAL DIRECTION`
- `HIRE NOT VIABLE`

with justification.

## 11. Stop condition

After creating the analysis document:

1. summarize the verified `HIRE` semantics;
2. summarize the recommended E05 treatment;
3. show the proposed success criteria;
4. list any unresolved questions;
5. report the path of the created document;
6. show `git status --short`.

Then **STOP**.

Do not implement the agent.

Do not create the E05 implementation plan.

Wait for explicit approval before moving from **DEFINE** to **PLAN**.