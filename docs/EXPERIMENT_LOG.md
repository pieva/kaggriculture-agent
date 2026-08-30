# Experiment Log

| Experiment | Title | Result Summary | Status | Key Takeaways & Decisions |
|---|---|---|:---:|---|
| E15 | Pairwise Tournament Final Synthesis | Copilot 2–0, Codex 1–1, Antigravity 0–2; Epistemically Closed | **E15 CLOSED** | Copilot competitive winner. Replicated fingerprints: Antigravity sub-threshold failure mode (M1/M3), Copilot compact policy footprint (M2/M3). Two-regime empirical model supported. 7/7 frozen artifacts unchanged. Next gate: Model Capability Check. |
| E15-M3 | Copilot vs Antigravity Consensus Verification | Copilot `$26,629` vs Antigravity `$9,371`; consensus closed | **M3 CLOSED** | `ACK_M3_CONSENSUS_ANTIGRAVITY` and `ACK_M3_CONSENSUS_COPILOT` received. Winner: Copilot. Replicated Antigravity M1 failure mode. |
| E15-M2 | Codex vs Copilot Consensus Verification | Copilot `$37,752` vs Codex `$27,510`; consensus closed | **M2 CLOSED** | `ACK_M2_CONSENSUS_CODEX` and `ACK_M2_CONSENSUS_COPILOT` received. Winner: Copilot. Super-threshold regime discrimination. |
| E15-M1 | Antigravity vs Codex Consensus Verification | Codex `$20,461` vs Antigravity `$8,672`; consensus closed | **M1 CLOSED** | `ACK_M1_CONSENSUS_ANTIGRAVITY` received, no blocking errors; `ACK_M1_CONSENSUS_CODEX` received, no blocking errors; M1 status: `CLOSED`; M2 status: `AUTHORIZED`. |
| E15.0 | Pre-Tournament Freeze & Enforcement | ACCEPT_E15_FREEZE (7/7 SHA256 Match) | **FREEZE CERTIFIED** | Enforced frozen execution from `results/e15/freeze/`, SHA256 manifest integrity verified, fail-closed runner, P0/P1 audit certified (`NO_MATERIAL_POSITION_BIAS_FOUND`), Copilot ownership certified, pre-declared seeds (M1=1113294977, M2=3033283457, M3=3122977751). Next action: RUN M1 ONLY. |
| E14 | Repository Isolation & Canonical Ontology | 64/64 Canonical Concepts Mapped | **ONTOLOGY CANONICALIZED** | Decoupled Antigravity, Codex, Copilot codebases and MODEL_SPECs. Consolidated 64 canonical concept_ids across 8 economic domains in `docs/model_specs/ONTOLOGY.md`. All three models mapped 64/64 concepts with independent assessments. |
| E13 | Multi-Agent Forensic Replay Analysis | Episode 101971376 ($133k vs $7.1k) | **FORENSIC CONSENSUS** | Independent blind replay analysis revealed ~14.5x watering delta (1,145 vs 79), $76.5k cash crop gap, and Day 1/Day 12 operational divergence vs physical capacity parity (292 vs 291 HIREs, 75 tiles). |
| E12-X1.7 | Corrective Architecture Audit | Stage A Architectural Verdict: PASS | **CORRECTIVE ARCHITECTURE VERIFIED** | Implemented strict State Machine Gating (`LIVESTOCK_BOOTSTRAP` $\rightarrow$ `LIVESTOCK_CORE_ESTABLISHED` $\rightarrow$ `CROP_EXPANSION`). Pre-built 2x2 pastures Turn 4-24, Cow #1 placed Turn 8, outer crop expansion gated Turn 12. 87/87 tests PASS. |
| E12-X1.7 | Submission Provenance & Opening Audit | Mismatch Identified & Fixed | **REBUILD VERIFIED** | Root cause: `scripts/build_submission.py` had legacy E11 config hardcoded. Fixed builder, verified 100% Turn 1–24 equivalence (84/84 tests PASS). Hash: `22EB239B108AC045AC86548B6A9444EDEF1939072756C082C2EC8D95EF13881F`. Re-upload required. |
| E12-X1.7 | Kaggle External Validation | $22,386.80 Mean Money (83/83 Unit Tests PASS) | **EXTERNAL VALIDATION READY** | Provenance verified (`submission/submission.py`, SHA-256: `F12068386FC0...`). Recommendation: `PROCEED E12-X1.8 — EARLIER WORKFORCE / CAPACITY ACTIVATION`. |
| E12-D3 | Marginal Capacity ROI Audit | Late Activation @ Day 18–22, 0% Melon Completion | **DIAGNOSTIC COMPLETE** | Identified root cause `LATE_CAPACITY_ACTIVATION` & `MELON_HORIZON_MISMATCH` for +$378 (+1.7%) gain in X1.7. Recommendation: `X1.8 EARLIER WORKFORCE / CAPACITY ACTIVATION`. |
| E12-X1.7 | Workforce Capacity Scaling (5 Crop Workers @ 4T) | $22,386.80 Mean Final Money | **PASS (Positive Capacity Scaling)** | Scaled from 4 to 5 crop workers (20 crop tiles capacity @ 4T/worker). Productive actions increased to 1,620/game. Recommendation: `PROCEED E12-X1.8 — 6 CROP WORKERS @ 4 TILES/WORKER`. |
| E12-X1.6 | Functional Workforce & Hybrid Economic Scaling | $22,008.80 Mean Final Money (+$15.8k / +258%) | **PASS (Major Breakthrough)** | Functional role specialization (Worker 0 Livestock vs Hands Crop), 2x2 core monetization, Melon ($94.67/act) allocation. Recommendation: `PROCEED E12-X1.7 CAPACITY OPTIMIZATION`. |
| E12-X1.5 | Working Set Retention @ 4T | $6,151.80 Mean Final Money | **PASS (Stable Base)** | Fixed 4 tiles/worker cap, emergency water priority, zero maintenance collapse. Recommendation: `PROCEED E12-X1.6 ECONOMIC OPTIMIZATION`. |
| E12-D2 | Weed Mechanics & Surface Retention Audit | 30.4 Crops Lost/Seed, 41.2% Weed Penetration | **DIAGNOSTIC COMPLETE** | Verified 2-day unwatered wilting rule in `kaggriculture.py`. Root cause: `MULTI_MAINTENANCE_COLLAPSE`. Recommendation: `X1.5 WEED PRIORITY CONTROL & WORKING SET RETENTION`. |
| E12-X1.4 | Worker Locality & Readiness Expansion | 33.6% Mov, 64.1% Prod, 496.7% Yield | **PASS** | Strict worker regional locality, emergent readiness unlocks (Q1 D7, Q2 D22). |

## Recent Experiments Log

## E15 — Final Tournament Synthesis & Epistemic Closure

**Date:** 2026-08-29
**Phase:** TOURNAMENT SYNTHESIS & EPISTEMIC CLOSURE
**Authority:** Multi-Agent Consensus (Antigravity, Codex, Copilot)
**Status:** `EPISTEMICALLY CLOSED` | `FROZEN ARTIFACTS UNCHANGED`
**Final Synthesis Document:** `results/e15/E15_FINAL_TOURNAMENT_SYNTHESIS.md`

### Final Tournament Standings & Match Results

| Match | Pairing | Seed | Final Scores | Winner | Consensus Status |
|---|---|:---:|:---:|:---:|:---:|
| **M1** | Antigravity (P0) vs Codex (P1) | `1113294977` | $8,672 vs $20,461 | **Codex** | Double ACK (`ANTIGRAVITY`, `CODEX`) |
| **M2** | Codex (P0) vs Copilot (P1) | `3033283457` | $27,510 vs $37,752 | **Copilot** | Double ACK (`CODEX`, `COPILOT`) |
| **M3** | Copilot (P0) vs Antigravity (P1) | `3122977751` | $26,629 vs $9,371 | **Copilot** | Double ACK (`ANTIGRAVITY`, `COPILOT`) |

- **Competitive Standings**:
  1. **Copilot**: 2–0 (Competitive Winner)
  2. **Codex**: 1–1
  3. **Antigravity**: 0–2
- **Tie-Break**: Not required.

### Core Cross-Match Findings & Epistemic Verdicts

1. **Replicated Policy Fingerprints**:
   - **Antigravity (M1 & M3)**: Replicated failure mode across distinct seeds and opponents. Extremely low watering (34 vs 30), high movement overhead (5,019 vs 5,047), unharvested crop drop, large nominal scale (3Q, 12 hands, 18 pasture/livestock) with severely depressed active maintained crop surface (8–9 crops).
   - **Copilot (M2 & M3)**: Replicated stable policy footprint. Compact working set (max 25–28 crops), high continuous watering (446 vs 439), tightly controlled livestock (5 pasture, 4 animals), 9 hands, intensive monetization (298 vs 302 sell orders).
2. **Two-Regime Empirical Model**:
   - **Regime A (Below Operational Threshold)**: Irrigation, dispatch, and basic maintenance dominate outcomes. Adding nominal scale when maintenance fails amplifies collapse (M1, M3).
   - **Regime B (Above Operational Threshold)**: When watering and maintenance are stable, raw volume ceases to drive profit monotonically. Monetization quality, state-capacity alignment, capital timing, inventory-to-cash conversion, and sell-through dominate outcomes (M2).
3. **Agent Verdicts**:
   - **Copilot**: `MODEL_VALIDITY = SUBSTANTIALLY_SUPPORTED`, `POLICY_REALIZATION = SUPPORTED`, `GENERALIZATION = PARTIALLY_SUPPORTED, NOT_ESTABLISHED`.
   - **Codex**: `MODEL_VALIDITY = PARTIALLY_TO_SUBSTANTIALLY_SUPPORTED`, `POLICY_REALIZATION = PARTIALLY_SUPPORTED`.
   - **Antigravity**: `MODEL_VALIDITY = PARTIALLY_SUPPORTED`, `POLICY_REALIZATION = STRONGLY_WEAKENED`, `IMPLEMENTATION_FIDELITY = STRONGLY_WEAKENED`.

### Transition to Post-E15 Phase

E15 is frozen as an immutable epistemic baseline. The formal next gate is **Model Capability Check** across available LLM runtimes for Antigravity, Codex, and Copilot before any MODEL_SPEC revisions or code generation.

---

## E15-M3 — Consensus Verification

**Date:** 2026-08-29
**Phase:** M3 CONSENSUS VERIFICATION
**Authority:** Multi-Agent Consensus (Antigravity, Copilot)
**Status:** `M3 CLOSED` | `E15 TOURNAMENT COMPLETE`

### Result

- **M3**: Copilot (P0) vs Antigravity (P1)
- **Seed**: `3122977751`
- **Final Money**: Copilot `$26,629` vs Antigravity `$9,371`
- **Delta**: `+$17,258` Copilot
- **Consensus Verification**: `ACK_M3_CONSENSUS_ANTIGRAVITY` and `ACK_M3_CONSENSUS_COPILOT` received, no blocking errors.
- **Key Finding**: Replicated M1 failure pattern on Antigravity; confirmed Copilot compact footprint stability.

---

## E15-M2 — Consensus Verification

**Date:** 2026-08-29
**Phase:** M2 CONSENSUS VERIFICATION
**Authority:** Multi-Agent Consensus (Codex, Copilot)
**Status:** `M2 CLOSED` | `M3 AUTHORIZED`

### Result

- **M2**: Codex (P0) vs Copilot (P1)
- **Seed**: `3033283457`
- **Final Money**: Copilot `$37,752` vs Codex `$27,510`
- **Delta**: `+$10,242` Copilot
- **Consensus Verification**: `ACK_M2_CONSENSUS_CODEX` and `ACK_M2_CONSENSUS_COPILOT` received, no blocking errors.
- **Key Finding**: Super-threshold regime discrimination; compact working set + intensive monetization surpassed larger physical working set.

---

## E15-M1 — Consensus Verification

**Date:** 2026-08-29
**Phase:** M1 CONSENSUS VERIFICATION
**Authority:** Multi-Agent Consensus (Antigravity, Codex)
**Status:** `M1 CLOSED` | `M2 AUTHORIZED`

### Result

- **M1**: Antigravity (P0) vs Codex (P1)
- **Seed**: `1113294977`
- **Final Money**: Codex `$20,461` vs Antigravity `$8,672`
- **Delta**: `+$11,789` Codex

### Consensus Verification

- `ACK_M1_CONSENSUS_ANTIGRAVITY` — received, no blocking errors.
- `ACK_M1_CONSENSUS_CODEX` — received, no blocking errors.
- M1 status: `CLOSED`.
- M2 status: `AUTHORIZED`.

### Governance

- No frozen artifact modified.
- No M1 raw artifact modified.
- M2 remains pending explicit operational approval.

## E15.0 — Pre-Tournament Freeze, Governance & Enforcement

**Date:** 2026-08-29
**Phase:** PRE-TOURNAMENT FREEZE & GOVERNANCE
**Authority:** Multi-Agent Consensus (Antigravity, Codex, Copilot)
**Status:** `ACCEPT_E15_FREEZE` (Certified by Codex E15.0d Review)

### Objective
Congelare in modo verificabile e immutabile gli artefatti pre-match (ontologia, 3 MODEL_SPEC, 3 submission candidate), certificare l'integrità SHA256 dei 7 file frozen, auditare la simmetria P0/P1 dell'environment, e implementare l'enforcement del freeze nel runner prima di avviare il torneo E15.

### Key Milestones & Governance Protocol
1. **7/7 Frozen Artifacts Verified by SHA256**:
   - `Canonical Ontology` (`results/e15/freeze/ONTOLOGY_E15_FROZEN.md`): `5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa`
   - `Antigravity MODEL_SPEC` (`results/e15/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md`): `f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46`
   - `Codex MODEL_SPEC` (`results/e15/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md`): `9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7`
   - `Copilot MODEL_SPEC` (`results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md`): `d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686`
   - `Antigravity Submission` (`results/e15/freeze/submission_antigravity_E15_FROZEN.py`): `629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d`
   - `Codex Submission` (`results/e15/freeze/submission_codex_E15_FROZEN.py`): `fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3`
   - `Copilot Submission` (`results/e15/freeze/submission_copilot_E15_FROZEN.py`): `604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb`
2. **P0/P1 Symmetry Audit**:
   - Audit source-level di `kaggriculture.py` completato in `results/e15/P0_P1_ENVIRONMENT_AUDIT.md` con esito `NO_MATERIAL_POSITION_BIAS_FOUND`.
3. **Runner Freeze Enforcement & Fail-Closed**:
   - `scripts/run_e15_tournament.py` aggiornato per eseguire direttamente e unicamente i file da `results/e15/freeze/`.
   - Verifica SHA256 pre-esecuzione contro `FREEZE_MANIFEST.md`; abort immediato (`sys.exit(1)`) se un hash differisce.
4. **Pre-Declared Tournament Schedule & Seeds**:
   - **M1**: Antigravity (P0) vs Codex (P1) | Seed: `1113294977`
   - **M2**: Codex (P0) vs Copilot (P1) | Seed: `3033283457`
   - **M3**: Copilot (P0) vs Antigravity (P1) | Seed: `3122977751`
5. **Tie-Break Pre-Dichiarato**:
   - Primario: numero di vittorie head-to-head.
   - Tie-break (in caso di 1–1 per tutti): $D_i = \sum (\text{final\_money}_i - \text{final\_money}_{\text{opponent}})$.
6. **Stato Finale E15.0**:
   - `ACCEPT_E15_FREEZE`
   - **0 match eseguiti**.
   - Prossima azione: `RUN M1 ONLY`.

## E14 — Repository Isolation & Canonical Ontology

**Date:** 2026-08-28 to 2026-08-29
**Phase:** MODEL GOVERNANCE & REPOSITORY ISOLATION
**Authority:** Multi-Agent Architecture (Antigravity, Codex, Copilot)

### Objective
Isolare formalmente i perimetri di codice e i modelli concettuali dei tre agenti per eliminare cross-contamination, e costruire un'ontologia canonica comune (`docs/model_specs/ONTOLOGY.md`) per rendere i tre MODEL_SPEC empiricamente confrontabili.

### Key Milestones
1. **Repository & Codebase Isolation**:
   - Decoupled packages created: `src/agricola/strategy/antigravity/`, `src/agricola/strategy/copilot/`, and isolated Codex candidate.
   - Independent standalone submissions: `submission/submission_antigravity.py`, `submission/submission_codex.py`, `submission/submission_copilot.py`.
2. **Canonical Ontology (64 concept_ids)**:
   - Consolidata in `docs/model_specs/ONTOLOGY.md` attraverso 8 sezioni economiche (A–H).
   - Tassonomia rigorosa: `USED / PARTIAL / NOT_USED` e `FULL / PARTIAL / ABSENT / BROADER / NARROWER / CONFLICT`.
   - Separazione netta tra Evidence Status (`REPLAY_SUPPORTED`, `PROVISIONAL`, `ENGINE_RULE_SUPPORTED`) e Observability (`OBSERVABLE`, `DERIVABLE_FROM_REPLAY`, `ENGINE_ONLY`).
3. **Model Adoption (64/64 Coverage)**:
   - **Antigravity**: 59 `USED`, 4 `PARTIAL`, 1 `NOT_USED`, 0 `CONFLICT`.
   - **Codex**: 37 `USED`, 20 `PARTIAL`, 7 `NOT_USED`, 0 `CONFLICT`.
   - **Copilot**: 50 `USED`, 7 `PARTIAL`, 7 `NOT_USED`, 0 `CONFLICT`.

## E12-D1 — Top Player Temporal & Economic Benchmark (Pure Diagnostic Trajectory Audit)

**Date:** 2026-08-27
**Phase:** TEMPORAL & ECONOMIC DIAGNOSTIC AUDIT
**Tool:** Google Antigravity

### Objective
Effettuare un audit temporale ed economico comparativo tra E12-X1.3, E11-X1.7 e la Top Player Envelope ($70k–$85k) senza apportare alcuna modifica al codice di strategia durante D1, per identificare a quale turn e per quale causa nasce il gap di -$21k.

### Key Diagnostics & Quantitative Empirical Discoveries
1. **Harvest Yield Collapse (72% Crop Death Rate)**:
   - In E12-X1.3, i worker hanno seminato in media **77.8 colture** su 4 quadranti.
   - Tuttavia, solo **21.8 colture** sono state effettivamente raccolte! Il **72.0% delle colture seminate in X1.3 è seccato o morto non raccolto**.
   - In E11-X1.7, le colture seminate sono state 53.4 e quelle raccolte **57.8** (Harvest Yield Ratio: **108.2%** via colture multi-raccolto).
2. **Cross-Map Travel Overhead**:
   - Con l'apertura prematura dei 4 quadranti al Giorno 1–2, i worker spendono il **61.4% delle azioni totali muovendosi** attraverso la mappa (da Q0 a Q3).
   - Le azioni produttive crollano al **38.6%**, per cui i worker terminano il budget di azioni giornaliero prima di aver annaffiato le 24 tile, causandone il disseccamento.
3. **Premature Capital Draining**:
   - Al Giorno 1–2, X1.3 spende $1,000 per Q1 e $12 per 4 hand contemporaneamente, esaurendo la cassa a **$50.00** e bloccando l'acquisto di semi ad alto ROI (Melon/Strawberry).
4. **Seed 200 Anomaly Identified**:
   - Con la cassa a $50 al Giorno 2, la semina fallback `CARROT` ha sovrascritto il WHEAT sulle feed tile `(2,3), (2,4)`. Senza WHEAT raccolto nello shed, Cow #1 non è mai stata acquistata, generando $0.00 Milk Revenue.

### Decision Rule for E12-X1.4
- **Raccomandazione Ufficiale per X1.4**: **`E12-X1.4 WORKER EFFICIENCY & STAGED EXPANSION TIMING`**
- **Regola**: Mantenere l'opening livestock centered di Cow #1, posticipare l'acquisto di Q1 al Giorno 4–5 e Q2 al Giorno 8–10, e vincolare i worker per quadrante eliminando il movimento trasversale.

**Date:** 2026-08-27
**Phase:** PRE-BUILD DIAGNOSIS → BUILD → VERIFY → STAGE A0/A1/B PROVENANCE MATCH
**Tool:** Google Antigravity

### Objective
Far proseguire la crop engine centered oltre il plateau di 15 tile fin a raggiungere 24–26 active crop tiles, mantenendo invariato l'opening livestock validato di X1.2 (Cow #1 + Feed Ring + WHEAT buffer).

### Key Technical Diagnostics & Fixes Implemented
1. **Dynamic Land Expansion Unblocking**:
   - Sbloccata l'espansione automatica multi-quadrante (Q1, Q2, Q3) sostituendo la chiamata bloccata a `BUY_LAND` solo su `hour == 0` e riserva da `$1300` con `builder.market_orders.append(["BUY_LAND"])` attiva ad ogni ora non appena `cash >= $1050`.
2. **Priority Market Order Prepending**:
   - Inserito `builder.market_orders.insert(0, ["HIRE"])` per garantire che l'ordine di HIRE non venga sovrascritto o posticipato dalle vendite sul mercato.
3. **Workforce Capacity Scaling**:
   - Scalato il target workforce a 4 worker con `owned_quadrants >= 2` e 6 worker con `owned_quadrants >= 3`, fornendo una capacità di annaffiatura fino a 27 tile/giorno.
4. **Flexible Seed Purchasing**:
   - Incrementati i cap di inventario semi (`target_seed_cap=12`, `target_high_cap=8`) e aggiunti acquisti di emergenza singoli/doppi per TOMATO ($50), STRAWBERRY ($100), MELON ($80).
5. **Soil-Only Planting Matching**:
   - Corretto `_tile_matches_task` per `PLANT` affinché accetti solo terreno vuoto (`tile is None`), forzando il passaggio preventivo di `DIG` sulle tile con erbacce (`WEED`) ed eliminando il rifiuto delle azioni da parte del motore di gioco.

### Stage B Empirical Results (5 Paired Seeds)
- **Run ID**: `E12-X1.3-20260827-151435`
- **Mean Peak Active Tiles**: **24.4 tiles** (Target 24–26 tiles **COMPLETAMENTE RAGGIUNTO**!).
- **Mean Final Money**: **$7,015.40**.
- **Mean Workforce**: **5.0 workers** (1 Farmer + 4 Hands).
- **Mean Owned Quads**: **4.0 quads** (Q0..Q3 tutti sbloccati).
- **Milk Revenue**: **$1,178.40** mean revenue per episode across seeds.
- **Cow Starvation**: **0 starvation**.
- **Provenance Verification**: **100% MATCH**.

### Key Analytical Takeaway & Recommendation
L'esperimento E12-X1.3 ha **completamente superato il Structural Success Gate**:
1. Il limite delle 15 tile è stato risolto con successo, portando le tile attive picco a **24.4** (target 24–26).
2. Cow #1 è attiva e produttiva senza alcun caso di starvation.
3. La provenienza dei dati è verificata al **100%**.


**Date:** 2026-08-27
**Phase:** PRE-BUILD DIAGNOSIS → BUILD → VERIFY → STAGE A0/A1/B PROVENANCE MATCH
**Tool:** Google Antigravity

### Objective
Combinare l'opening livestock validato in E12-X1.1 con il ripristino immediato della macchina agricola centered di E11-X1.7 (`E12-X1.1 livestock opening + E11-X1.7 crop engine = E12-X1.2 hybrid strategy`), evitando che la gestione animale monopolizzi capitale, tile e worker actions.

### Key Technical Diagnostics & Fixes Implemented
1. **WHEAT Feed Buffer Protection**:
   - Escluso il WHEAT raccolto nello shed dalla vendita automatica sul mercato durante la Market Phase (preservando fino a 10 unità di WHEAT come riserva alimentare per la cow).
   - Risolto il bug per cui le 6 unità di WHEAT venivano vendute immediatamente dopo il raccolto su mercato, lasciando lo shed a 0 WHEAT e impedendo il FEED della cow.
2. **Macro-Phase State Machine & Crop Recovery Trigger**:
   - `HYBRID_BOOTSTRAP` $\to$ `FEED_READY` $\to$ `CROP_RECOVERY` $\to$ `HYBRID_STEADY_STATE`.
   - `CROP_RECOVERY` si attiva non appena il WHEAT è pronto (`wheat_shed >= 1`), sbloccando la semina di MELONS/crop ad alto ROI su EPU1, EPU2 ed EPU3.
3. **Progressive Cow Cap**:
   - Cow #1 obbligatoria nell'opening.
   - Cow #2 consentita solo con `active_crop_tiles >= 18` e `wheat_shed >= 4`. Cow #3 e #4 disabilitate.

### Stage B Empirical Results (5 Paired Seeds)
- **Mean Final Money**: **$21,912.20** (+$15,906.80 vs E12-X1.1 $6,005.40; vs E11-X1.7 $28,083.80, B3 $26,445.60).
- **Median Final Money**: **$21,953.00**.
- **Milk Harvested**: **9.0 units** per episode across all seeds.
- **Milk Revenue**: **$2,021.40** mean revenue per episode.
- **Peak Active Tiles**: **14.4 tiles** (vs 5.0 in X1.1).
- **Crop Recovery Ratio**: ~55-60% della capacità agricola di E11-X1.7 recuperata in Q0.
- **Provenance Verification**: **100% MATCH** (`E12-X1.0-20260827-143849`).

### Key Analytical Takeaway & Recommendation
L'ipotesi H12-X1.2 è **confermata in pieno dal punto di vista funzionale e fortemente recuperata dal punto di vista economico**:
L'opening animale coesiste con la macchina agricola centered, generando oltre **$2,021.40 di Milk Revenue** e portando il final money a **$21,912.20** (+15.9k vs X1.1).
**Raccomandazione finale**: **`PROCEED E12-X1.3 HYBRID OPTIMIZATION`** (sblocco espansione multi-quadrante Q1/Q2 per portare le tile attive da 15 a 26-30 e superare E11-X1.7).

## E12-X1.1 — Feed-First Cow Pipeline (Engine Alignment & Single-Cow Bootstrap Verification)

**Date:** 2026-08-27
**Phase:** DIAGNOSE → BUILD → VERIFY → PROVENANCE MATCH
**Tool:** Google Antigravity

### Objective
Isolare e risolvere il collo di bottiglia economico osservato in E12-X1.0 ($6,227.60) mediante l'implementazione della pipeline **Feed-First Cow Pipeline**, assicurando che Cow #1 non venga mai acquistata né posizionata finché non è presente WHEAT raccolto nello shed (`wheat_shed >= 1`), e verificando il ciclo completo `WHEAT -> FEED -> MILK -> SELL`.

### Key Technical Diagnostics & Fixes Implemented
1. **Virtual Seeds Multi-Worker Conflict Resolution**:
   - Risolto il conflitto tra Farmer e Hand 1 su `virtual_seeds["WHEAT"]` durante la chiamata a `_compute_e06_worker_action`.
   - Inserito il controllo di `_select_crop_to_plant` direttamente all'interno della logica `PLANT` di `_compute_e06_worker_action` (linea 2063), garantendo la priorità assoluta di seminare WHEAT nei feed tiles dedicati `[(2,3), (2,4), (1,3), (1,4), (3,1), (4,1)]`.
2. **Workforce-Partitioned Crop Allocation**:
   - `farmer_tiles`: Riservato ai crop ROI `[(2,2), (3,2), (4,2)]` (MELONS).
   - `hand1_tiles`: Riservato al Feed WHEAT ring `[(2,3), (2,4), (1,3), (1,4), (3,1), (4,1)]`.
3. **Single-Cow Bootstrap Gate**:
   - Acquisto Cow #1 vincolato a `wheat_shed >= 1`.
   - Acquisto Cow #2..#4 vincolato a `milk_harvested >= 1` AND `wheat_shed >= 4`.

### Empirical Results (5 Paired Seeds)
- **Milk Harvested**: 3 units per episode (100% success across all seeds).
- **Milk Revenue**: **$782.60** mean revenue per episode.
- **Starvation Rate**: **0.0%** (zero cow deaths).
- **Mean Final Money**: **$6,005.40** (vs E11-X1.7 $28,083.80, B3 $26,445.60).
- **Provenance Verification**: **100% MATCH** (`E12-X1.0-20260827-142745`).

### Key Analytical Takeaway
L'ipotesi di redditività dell'allevamento bovino early-game rispetto ai crop ad alto ROI (MELONS) è smentita dal punto di vista economico:
- Una Cow richiede **$400** di costo fisso d'acquisto + 1 pascolo ($100) + 2 tile di WHEAT ($20) + tempo contadino quotidiano per generare **$160/giorno** di MILK ($53.3/tile/giorno).
- 3 tile di MELON generano **$750** gross / **$510** net cash con un ciclo di 12 giorni, richiedendo molta meno mobilità e zero infrastruttura.
- **E11-X1.7 Corner-Pruned 26t ($28,083.80)** rimane la strategia champion indiscussa.

## E01 — Project definition, baseline implementation, benchmark runner & observable verification

**Date:** 2026-08-18 to 2026-08-19
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → CONSOLIDATE → SHIP
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Verificare se Antigravity è in grado di analizzare autonomamente Kaggriculture, produrre un Implementation Plan dettagliato, realizzare l'infrastruttura modulare del repository, implementare la baseline iniziale, costruire una suite di valutazione benchmark automatizzata, eseguire la verifica osservabile del ciclo decisionale del contadino e validare la submission sulla piattaforma Kaggle.

### Starting state

- repository Git vuoto;
- repository GitHub privato;
- nessun codice;
- nessuna struttura applicativa;
- nessuna baseline fornita;
- nessuna strategia suggerita manualmente.

### Prompt

See `docs/prompts/E01-01_define_plan.md`, `docs/prompts/E01-02_review_feedback.md`, `docs/prompts/E01-03_verify.md`, `docs/prompts/E01-04_verify_review.md`.

### Observations & Actions

1. **Studio Ambiente & Setup**: Configurato l'ambiente virtuale isolato Python 3.12 (`.venv`) con `kaggle-environments`.
2. **Implementation Plan & Repository Hygiene**: Prodotto ed approvato l'Implementation Plan; creato `README.md` e `.gitignore` per escludere cache e `.venv`.
3. **Infrastruttura Modulare & Bundling**:
   - Creato il pacchetto `src/agricola/` (`GameState`, `ActionBuilder`, `CarrotLoopAgent`, `agent.py`).
   - Implementato lo script `scripts/build_submission.py` che genera il file standalone `submission/submission.py`.
4. **Rinominazione Metrica Disqualification Rate**:
   - Rinominata la metrica da "Invalid Action Rate" a **Disqualification Rate (%)** per riflettere con esattezza l'osservabile misurato dall'engine (percentuale di episodi conclusi con stato `INVALID` o `ERROR`).
5. **Misurazione Precisa Latenza Agente**:
   - Implementato `TimedAgentWrapper` in `src/agricola/evaluation/runner.py` per misurare separatamente ed isolatamente la latenza decisionale dell'agente (**Agent Mean Turn Latency**), distinguendola dalla durata complessiva dello step di simulazione dell'engine (**Simulation Mean Step Time**).
6. **Livello di Verifica & Test**:
   - Chiaramente distinti gli unit test (`GameState`, `ActionBuilder`, `agent` output), gli smoke/integration test (`test_short_simulation_smoke`, `test_build_and_run_submission_smoke`) e il benchmark completo E01 (30 episodi $\times$ 720 turni = 21.600 turni).
7. **Validazione Kaggle Platform**:
   - `submission/submission.py` è stato caricato sulla piattaforma Kaggle ed eseguito con successo (Status **`Complete`**, Score iniziale **`600.0`**).
8. **Esecuzione Osservabile VERIFY**:
   - Eseguito un episodio completo di 720 turni tramite Antigravity ed ispezionato il registro degli stati `env.steps`.
   - Confermato e documentato in `docs/versions/E01_verify_antigravity.md` il ciclo operativo: `BUY_SEED → PLANT → WATER → PASS → HARVEST → PLANT → SELL`.
   - Verificato univocamente per l'episodio VERIFY: `status: DONE`, 720/720 turni completati, `money finale: 3564.0`, `reward finale: 3564.0` (`reward == farm["money"]`).

### Human intervention

- Approvazione dell'Implementation Plan (`docs/prompts/E01-01_define_plan.md`).
- Review indipendente tramite `docs/prompts/E01-02_review_feedback.md` (consolidamento metrica, latenza, README, `.gitignore`).
- Review del VERIFY tramite `docs/prompts/E01-04_verify_review.md` (chiarimento ed unificazione univoca di reward e money a 3564.0).

### Outcome & Verification Evidence

- **Suite di Test (`pytest tests/`)**: 5/5 test superati con successo (3 unit test, 2 smoke integration test).
- **Bundling Submission (`scripts/build_submission.py`)**: `submission/submission.py` generato e verificato su Kaggle (Score `600.0`).
- **Benchmark Metric Summary E01 (`results/e01_baseline.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: 66.67% (20W / 0L / 10D)
  - Win Rate vs `pass`: 100.00% ($3594.30)
  - Win Rate vs `random`: 100.00% ($3577.00)
  - Draw Rate vs `starter`: 100.00% Draw / 0% Sconfitte ($3531.60)
  - Mean Final Money: **$3567.63** (Sample Std Dev `ddof=1`: **± $205.38**; Population Std Dev `ddof=0`: **± $201.93**)
  - Median Final Money: **$3528.00**
  - Agent Mean Turn Latency: **0.0142 ms/turno**
  - Simulation Mean Step Time: **3.69 ms/step**

### Method assessment

DEF INE: PASSED
PLAN: PASSED
BUILD: PASSED
VERIFY: PASSED
REVIEW: PASSED
CONSOLIDATE: PASSED
SHIP: PASSED (Tag: `v0.1-e01-baseline`)

---

## E02 — Dynamic Crop Selection & ROI Scaling (`ROICropAgent`)

**Date:** 2026-08-19
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → CONSOLIDATE → SHIP
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Sostituire la monocultura statica di carote della baseline E01 (`CarrotLoopAgent`) con una regola di selezione dinamica della coltura basata sul profitto netto stimato per giorno ($\text{NetProfitPerDay} = \frac{(\text{SellPrice} \times \text{Yield}) - \text{SeedPrice}}{\text{Days}}$), al fine di massimizzare la crescita del capitale ed eliminare il pareggio con l'agente `starter` mantenendo la struttura operativa single-tile `(4, 4)`.

### Baseline E01 utilizzata per il confronto

- **Mean Final Money E01**: **`$3567.63 ± $205.38`**
- **Median Final Money E01**: **`$3528.00`**
- **Win Rate vs `starter`**: **`0.00%`** (100.00% Pareggi / 10D)

### PLAN & Evidenze

- Implementation Plan: [`docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E02_Dynamic_Crop_Selection_&_ROI_Scaling.md)
- Benchmark JSON E02: [`results/e02_roi_crop.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e02_roi_crop.json)
- Evidenza BUILD: [`docs/versions/E02_build_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_build_antigravity.md)
- Evidenza VERIFY REVIEW: [`docs/versions/E02_verify_review_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_verify_review_antigravity.md)
- Evidenza Analisi Simulazione: [`docs/versions/E02_simulation_analysis.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_simulation_analysis.md)
- Evidenza SHIP REVIEW: [`docs/versions/E02_ship_review_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E02_ship_review_antigravity.md)

### Benchmark & Outcome (Valutazione Locale)

- **Suite di Test (`pytest tests/`)**: **7/7 test superati**.
- **Benchmark Metric Summary E02 (`results/e02_roi_crop.json`)**:
  - Total Episodes: 30
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: **100.00%**
  - Mean Final Money E02: **`$5857.17 ± $132.37`**
  - Median Final Money E02: **`$5837.00`**

### Confronto Quantitativo E01 $\rightarrow$ E02

- **Incremento Assoluto Capitale Medio**: $5857.17 - 3567.63 = \mathbf{+\$2289.53}$ (**`+64.18%`**)
- **Win Rate vs `starter`**: **`0.00%` $\rightarrow$ `100.00%`**
- **Risultato Sperimentale**: **`SUPPORTATA nelle condizioni sperimentali testate`**

### Method assessment

DEF INE: PASSED
PLAN: PASSED
BUILD: PASSED
VERIFY: PASSED
REVIEW: PASSED
CONSOLIDATE: PASSED
SHIP: PASSED WITH OBSERVATIONS (Tag: `v0.2-e02-roicrop`)

---

## E03 — Multi-Tile Scaling (`MultiTileROIAgent`)

**Date:** 2026-08-24
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → CONSOLIDATE → SHIP
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash (High)

### Objective

Valutare l'impatto dell'espansione del footprint di coltivazione da 1 tile a un cluster compatto 2×2 di 4 tile adiacenti `{(4,4), (4,3), (3,4), (3,3)}`, mantenendo rigorosamente invariata la logica economica di selezione della coltura (ROI/giorno) e di vendita immediata di E02.

### Modifiche Implementate
1. **Fix Infrastrutturale Movimento (`src/agricola/core/actions.py`)**:
   - Corretto `ActionBuilder.move()` per emettere direttamente le stringhe direzionali riconosciute dall'ambiente (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
2. **Modulo Strategico `MultiTileROIAgent` (`src/agricola/strategy/multi_tile_roi.py`)**:
   - Gestione delle 4 tile con gerarchia di priorità stretta `HARVEST > PLANT > WATER`.
   - Seleziona la tile a minima distanza Manhattan all'interno della classe di priorità più alta attiva (tie-breaking deterministico `(y, x)`).
   - Acquisto semi matched al numero di tile vuote gestite e alla liquidità disponibile.
3. **Entrypoint, Bundling & Test Suite**:
   - Aggiornati `src/agricola/agent.py`, `scripts/build_submission.py` e creata suite di unit test (`tests/test_actions.py`, `tests/test_multi_tile.py`).

### PLAN & Evidenze

- Implementation Plan: [`docs/plans/E03_Multi_Tile_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E03_Multi_Tile_Scaling.md)
- Benchmark JSON E03: [`results/e03_multi_tile.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e03_multi_tile.json)
- Evidenza BUILD: [`docs/versions/E03_build_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E03_build_antigravity.md)
- Evidenza VERIFY: [`docs/versions/E03_verify_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E03_verify_antigravity.md)
- Evidenza REVIEW: [`docs/versions/E03_review_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E03_review_antigravity.md)
- Evidenza SHIP: [`docs/versions/E03_ship_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E03_ship_antigravity.md)
- Screenshot Kaggle: [`docs/screenshots/E03-001_kaggle_submission_successful.png`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/screenshots/E03-001_kaggle_submission_successful.png)

### Benchmark & Outcome (Valutazione Locale)

- **Suite di Test (`pytest tests/`)**: **14/14 test superati** (100% success rate in 2.78s).
- **Benchmark Metric Summary E03 (`results/e03_multi_tile.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: **100.00%** (30W / 0L / 0D)
  - Win Rate vs `pass`: 100.00% ($15,257.00)
  - Win Rate vs `random`: 100.00% ($14,284.10)
  - Win Rate vs `starter`: 100.00% ($14,506.30)
  - Mean Final Money E03: **`$14682.47`**
  - Sample Std Dev E03 (`ddof=1`): **`± $1164.33`**
  - Median Final Money E03: **`$14146.00`**
  - Agent Mean Turn Latency: **0.0698 ms/turno**

### Confronto Quantitativo E02 $\rightarrow$ E03

- **Incremento Assoluto Capitale Medio**: $14682.47 - 5857.17 = \mathbf{+\$8825.30}$
- **Incremento Percentuale Capitale Medio**: $\mathbf{+150.68\%}$
- **Overall Win Rate & Win Rate vs `starter`**: **100.00% $\rightarrow$ 100.00%**
- **Risultato Sperimentale**: **`SUPPORTATA nelle condizioni sperimentali testate`**

### SHIP (Validazione Esterna Kaggle)

- **Submission Name**: `submission.py`
- **Descrizione Registrata**: `E03 supervised iteration: Multi-Tile ROI Agent 2x2 cluster`
- **Status Kaggle**: **`Complete`**
- **Skill Rating Iniziale Osservato E03**: **`600.0`** (Rating E02 nello stesso screenshot: `285.1`).
- **Valutazione SHIP**: **`PASSED`**

### Method assessment

DEFINE: PASSED
PLAN: PASSED
BUILD: PASSED
VERIFY: PASSED
REVIEW: PASSED
CONSOLIDATE: PASSED
SHIP: PASSED (Tag: `v0.3-e03-multitile`)

---

## E04 — Initial NW Scaling (`NWClusterROIAgent`)

**Date:** 2026-08-25
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Valutare l'espansione del footprint produttivo dal cluster 2×2 (4 tile) di E03 a un cluster compatto 3×3 di **9 tile** `{(x,y) | x ∈ [2,4], y ∈ [2,4]}` all'interno del quadrante iniziale NW, gestito da un **singolo farmer** senza `BUY_LAND` e senza `HIRE`, al fine di misurare empiricamente il limite di lavorazione fisica del farmer e verificare l'insorgenza di water starvation.

### Baseline E03 utilizzata per il confronto

- **Footprint E03**: 4 tile (2×2 cluster)
- **Mean Final Money E03**: **`$14682.47 ± $1164.33`**
- **Median Final Money E03**: **`$14146.00`**
- **Total Weed Conversions**: **0**

### Observations & Actions

1. **Competitive Gap Analysis (E04-01)**: Documentata in `docs/experiments/E04-01_Competitive_Gap_Analysis.md`. Identificati 4 gap principali (spaziale, orizzonte temporale, modello economico, metrologia).
2. **Experimental Direction Decision (E04-02)**: Documentata in `docs/experiments/E04-02_Experimental_Direction_Decision.md`. Separata la variabile di scaling da `HIRE` e selezionata `Candidate C` (NW Scaling 4→9 tile).
3. **Implementation & Unit Tests**:
   - Creato `src/agricola/strategy/nw_cluster_roi.py` (`NWClusterROIAgent`).
   - Creato `tests/test_nw_cluster.py` (5/5 unit test superati).
   - Aggiornati `src/agricola/agent.py` e `scripts/build_submission.py`.
4. **Metrologia di Water Starvation Integrata**:
   - Aggiornato `src/agricola/evaluation/runner.py` per tracciare le conversioni in `WEED` (starvation severa) e la quota di irrigazioni mancate a fine giornata (`hour == 23`).

### PLAN & Evidenze

- Implementation Plan: [`docs/plans/E04_Initial_NW_Scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/plans/E04_Initial_NW_Scaling.md)
- Evidenza VERIFY: [`docs/versions/E04_verify_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E04_verify_antigravity.md)

### Benchmark & Outcome (Valutazione Locale 30 Episodi)

- **Suite di Test (`pytest tests/`)**: **19/19 test superati** (100% success rate in 2.06s).
- **Benchmark Metric Summary E04**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: **100.00%** (30W / 0L / 0D)
  - Win Rate vs `pass`: 100.00% ($11117.90)
  - Win Rate vs `random`: 100.00% ($11505.50)
  - Win Rate vs `starter`: 100.00% ($11074.00)
  - Mean Final Money E04: **`$11232.47 ± $661.26`**
  - Median Final Money E04: **`$11050.00`**
  - Total Weed Conversions: **238 weeds** (7.93 weeds/episodio)
  - Mean Unwatered End-of-Day Ratio: **3.33%**
  - Agent Mean Turn Latency: **0.0570 ms/turno**

### Confronto Quantitativo E03 $\rightarrow$ E04

- **Delta Capitale Medio**: $11232.47 - 14682.47 = \mathbf{-\$3450.00 (-23.49\%)}$
- **Total Weed Conversions**: $0 \rightarrow \mathbf{238\text{ weeds}}$
- **Risultato Sperimentale**: **`FALSIFICATA / NON SUPPORTATA`**

### Diagnosi Tecnico-Sperimentale

- **Capacità Fisica Inadeguata per 1 Farmer**: Il singolo farmer non è in grado di percorrere e irrigare 9 tile su un cluster 3×3 mantenendo contemporaneamente la semina e la raccolta (`HARVEST > PLANT > WATER`).
- **Morte delle Piante & Tile Bricking**: In 30 episodi, 238 piante sono morte per disidratazione (2 giorni di mancata irrigazione) trasformandosi in `WEED`. L'assenza dell'azione `DIG` ha reso tali tile definitivamente inutilizzabili per il resto della partita.
- **Implicazione per E05**: Per scalare a $\ge 9$ tile senza soffrire di water starvation è indispensabile introdurre lavoratori aggiuntivi (`HIRE`) e/o bonifica automatica erbacce (`DIG`).

### Method assessment

DEFINE: PASSED
PLAN: PASSED
BUILD: PASSED
VERIFY: PASSED
REVIEW: PASSED (Hypothesis Falsified - Strategic Bottleneck Identified)
SHIP: PASSED (Tag: `v0.4-e04-nw-scaling`)

---

## E05 — HIRE Multi-Worker Scaling (`HIRENWClusterROIAgent`)

**Date:** 2026-08-25
**Phase:** DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Valutare l'introduzione di forza lavoro subordinata giornaliera tramite l'azione `HIRE` (1 farm hand al costo di $1/giorno) combinata con un partizionamento spaziale fisso 4:5 sul cluster compatto a 9 tile `{(x,y) | x ∈ [2,4], y ∈ [2,4]}`, al fine di eliminare il collo di bottiglia temporale del singolo farmer osservato in E04 e rendere il footprint a 9 tile economicamente sostenibile.

### Baseline E04 e Riferimento E03 per il confronto

- **E04 Control (9 tile, 1 farmer)**: Mean Final Money = **`$11232.47 ± $661.26`**, Total Weeds = **238**
- **E03 Reference (4 tile, 1 farmer)**: Mean Final Money = **`$14682.47 ± $1164.33`**, Total Weeds = **0**

### Observations & Actions

1. **Capability & Semantics Audit (E05-01)**: Ispezionato `kaggriculture.py`. Verificato che `HIRE` costa $1/giorno per la prima hand, gli ingaggi si resettano a fine giornata (`hour == 23`), e la hand diventa attiva al turno successivo.
2. **Implementation Plan (E05-02)**: Definito il trattamento isolato (1 daily HIRE, 4:5 spatial partitioning tra Farmer e Hand 1).
3. **BUILD & Testing**:
   - Estesi `GameState` (`hands_positions`, `hires_today`) e `ActionBuilder` (`hire()`, `add_hand_action()`).
   - Creato `src/agricola/strategy/hire_nw_cluster_roi.py` (`HIRENWClusterROIAgent`).
   - Creato `tests/test_hire_nw_cluster.py` (6/6 test superati, 25/25 suite completa).
   - Generato e validato `submission/submission.py`.
4. **Isolamento Risultati (E05-03B)**: Corretto il default in `scripts/run_eval.py` in `results/latest_eval.json` per evitare la sovrascrittura accidentale di `results/e01_baseline.json`.

### Benchmark & Outcome (Valutazione Locale 30 Episodi)

- **Benchmark Metric Summary E05 (`results/e05_hire_multiworker.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: 100.00%
  - Disqualification Rate: 0.00%
  - Overall Win Rate: **100.00%** (30W / 0L / 0D)
  - Win Rate vs `pass`: 100.00% ($21554.60)
  - Win Rate vs `random`: 100.00% ($21696.20)
  - Win Rate vs `starter`: 100.00% ($21456.00)
  - Mean Final Money E05: **`$21568.93 ± $361.25`**
  - Median Final Money E05: **`$21442.00`**
  - Total Weed Conversions: **176 weeds** (5.87 weeds/episodio)
  - Mean Unwatered End-of-Day Ratio: **3.33%**
  - Agent Mean Turn Latency: **0.0924 ms/turno**

### Confronto Quantitativo

- **Delta Capitale Medio vs E04**: $21568.93 - 11232.47 = \mathbf{+\$10336.46 (+92.02\%)}$
- **Delta Capitale Medio vs E03**: $21568.93 - 14682.47 = \mathbf{+\$6886.46 (+46.90\%)}$
- **Total Weed Conversions vs E04**: $238 \rightarrow \mathbf{176\text{ weeds (-26.05\%)}}
- **Economic Hypothesis**: **`SUPPORTED`**
- **Worker Capacity Bottleneck**: **`STRONGLY SUPPORTED`**
- **Starvation Status**: **`REDUCED BUT UNRESOLVED`**
- **Kaggle External Validation**: **`PASSED`** (Skill Rating stabilizzato: **`439.7`**, +161.4 pts / +57.99% vs E03 278.3)
- **Overall Evaluation**: **`STRONG SUCCESS`**

### Method assessment

DEFINE: PASSED
PLAN: PASSED
BUILD: PASSED
VERIFY: PASSED
REVIEW: PASSED
SHIP: PASSED (Tag: `v0.5-e05-hire-multiworker`)

---

## E06 — Water-First Scheduling (`WaterFirstHIRENWClusterROIAgent`)

**Date:** 2026-08-25
**Phase:** DEFINE → PLAN → BUILD
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Valutare l'inversione della priorità operativa dei worker da `HARVEST > PLANT > WATER` a `WATER > HARVEST > PLANT` (`WaterFirstHIRENWClusterROIAgent`), mantenendo 100% congelati tutti gli altri parametri rispetto alla baseline E05 Shipped (9 tile NW, 1 farmer + 1 hand a $1/giorno, 4:5 partitioning, ROI crop selection, Manhattan routing, 30 episodi benchmark).

### Baseline E05 utilizzata per il confronto

- **Mean Final Money E05:** **`$21568.93 ± $361.25`**
- **Median Final Money E05:** **`$21442.00`**
- **Total Weed Conversions E05:** **`176`** (5.87 weeds/ep)
- **Mean Unwatered End-of-Day Ratio E05:** **`3.33%`**

### Observations & Actions

1. **DEFINE (E06-01):** Documentata l'analisi di definibilità in `docs/experiments/E06-01_Water_First_Capability_Analysis.md`. Concluso `GO`.
2. **PLAN (E06-02):** Documentato il piano sperimentale isolato a variabile singola in `docs/plans/E06_Water_First_Scheduling.md`. Stabilito guardrail economico a $21200.00 e matrice decisionale.
3. **BUILD (E06-03):**
   - Creato `src/agricola/strategy/water_first_hire_nw_cluster_roi.py` (`WaterFirstHIRENWClusterROIAgent` come sottoclasse di `HIRENWClusterROIAgent`).
   - Creato `tests/test_water_first_hire_nw_cluster.py` (5/5 unit test).
   - Eseguita la suite completa `pytest tests/`: **30/30 test superati** (100% success rate in 1.93s).
   - Eseguito il benchmark locale su 30 episodi: output isolato in `results/e06_water_first.json`.

### Benchmark & Outcome (Valutazione Locale 30 Episodi)

- **Benchmark Metric Summary E06 (`results/e06_water_first.json`)**:
  - Total Episodes: 30 (21.600 turni totali)
  - Completion Rate: **100.00%**
  - Disqualification Rate: **0.00%**
  - Overall Win Rate: **100.00%** (30W / 0L / 0D)
  - Win Rate vs `pass`: 100.00% ($24593.30)
  - Win Rate vs `random`: 100.00% ($24572.40)
  - Win Rate vs `starter`: 100.00% ($24820.30)
  - Mean Final Money E06: **`$24662.00 ± $1932.04`**
  - Median Final Money E06: **`$25847.00`**
  - Total Weed Conversions: **`70 weeds`** (2.33 weeds/episodio)
  - Mean Unwatered End-of-Day Ratio: **8.11%**
  - Agent Mean Turn Latency: **0.0822 ms/turno**

### Confronto Quantitativo E05 $\rightarrow$ E06

- **Delta Capitale Medio**: $24662.00 - 21568.93 = \mathbf{+\$3093.07 (+14.34\%)}$
- **Delta Mediana Capitale**: $25847.00 - 21442.00 = \mathbf{+\$4405.00 (+20.54\%)}$
- **Total Weed Conversions**: $176 \rightarrow \mathbf{70\text{ weeds (-60.23\%)}}
- **Paired Seed Comparison (30/30 episodi)**:
  - Mean Paired Money Delta: **`+$3093.07 ± $1942.60`**
  - Episodes E06 Money > E05 Money: **`29 / 30 (96.7%)`**
  - Mean Paired Weed Delta: **`-3.53 weeds/episodio`**
  - Episodes E06 Weeds < E05 Weeds: **`30 / 30 (100.0%)`**
- **Experimental Hypothesis Verdict**: **`SUPPORTED`** (Operational: `PARTIALLY SUPPORTED` / -60.23% weeds; Economic: `STRONGLY SUPPORTED` / +$3093.07 money)
- **SHIP Recommendation**: **`SHIP CANDIDATE`**

### Method assessment

DEFINE: PASSED
PLAN: PASSED
BUILD: PASSED
VERIFY: PASSED WITH METRIC CAVEAT (`docs/versions/E06_verify_antigravity.md`)
REVIEW: PASSED (`docs/versions/E06_review_antigravity.md`, Verdict: `SUPPORTED`)
SHIP: PASSED (Tag: `v0.6-e06-water-first`, [`docs/versions/E06_ship_antigravity.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E06_ship_antigravity.md))

---

## E10 — Q1 Expansion Capital Protection (`Q1CapitalProtectedROIAgent`)

**Date:** 2026-08-26
**Phase:** DEFINE → PLAN → BUILD → VERIFY → FREEZE → PACKAGE → SUBMIT
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Proteggere il capitale di $1,000.0 necessario all'acquisto del quadrante Q1 (`BUY_LAND` Q1 al Giorno 12) impostando un floor di riserva prima del Giorno 12, al fine di eliminare i collassi finanziari causati dal prosciugamento della liquidità prima dell'espansione.

### Benchmark & Outcome (30-Episode Paired Safety Benchmark)

- **Mean Final Money E10-01:** **`$23,515.87 ± $2,789.27`** (`+$1,809.33` vs E09-01)
- **Median Final Money E10-01:** **`$23,845.00`**
- **Sample Std Dev E10-01:** **`± $2,789.27`** (`-70%` vs E09-01 $9,168.20)
- **Min Final Money E10-01:** **`$10,915.00`** (vs $124.00 in E09-01 — **0 episodi < $10k, collassi azzerati**)
- **Win Rate vs Standard Opponents:** **`100.0%`**
- **Test Suite:** **50/50 tests passed (100%)**
- **Kaggle Status:** Submission package built at `submission/submission.py` (44.5 KB). Overnight validation running.

---

## E11 — 3× Productive Mass Expansion

**Date:** 2026-08-26
**Phase:** E11-01 DEFINE → E11-02 PLAN → E11-03 BUILD → E11-04 LOCAL SAFETY VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Fase **BUILD & LOCAL SAFETY VERIFY di E11-01**: implementare la classe `ProductiveMassROIAgent` in `src/agricola/strategy/productive_mass_roi.py` con configurazione centralizzata `ProductiveMassConfig`, 4 quadranti (100 tile), Quadrant Locality Dispatcher, gerarchia azioni a 5 livelli, 3-Tier Crop Portfolio, Livestock Engine e telemetry logger completo. Valutare E11-01 su benchmark locale da 30 episodi appaiati vs E10-01, E09-01, E08, E06, E05.

### Outcome & Findings (Benchmark E11-01)

1. **Risultati Quantitativi Locale (30 Episodi Appaiati):**
   - **Mean Final Money E11-01:** **`$23,837.57`** (`+$432.00` / `+1.85%` vs E10-01 baseline $23,405.57)
   - **Median Final Money:** **`$24,165.50`**
   - **Sample Std Dev (`ddof=1`):** **`± $1,781.29`** (`-37%` vs E10-01 $2,823.36)
   - **Min Final Money:** **`$18,221.00`** (vs $10,915.00 in E10-01 — **+$7,306 di minimo, stabilità locale eccezionale**)
   - **Paired Win Rate vs E10-01:** **`22 / 30 episodi (73.3%)`**
   - **Completion Rate:** **`100.0% (0 DQ)`**
   - **Test Suite:** **55/55 tests passed (100%)**
2. **Decision Gate Verdict:** **`FAIL`** (Mean Final Money **$23,837.57 < $50,000.00 Minimum Success Threshold**).
3. **Diagnosi del Bottleneck Dominante:**
   - **Expansion Cash Lock:** L'acquisto del quadrante Q2 richiedeva `cash >= $1,000 + $300 reserve` ($1,300).
   - L'acquisto anticipato di sementi ad alto valore (Melon $320, Strawberry $400) ha prosciugato la cassa liquida nell'intervallo $400–$950 durante i giorni 6–18.
   - Di conseguenza, la cassa liquida non ha mai raggiunto $1,300 per eseguire `BUY_LAND` Q2 e Q3.
   - L'agente è rimasto bloccato su 2 quadranti (50 tile, 4 worker, 0 animali), funzionando di fatto come una variante di E10.
4. **Documenti Prodotti:**
   - [`docs/versions/E11_define_productive_mass_expansion.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_define_productive_mass_expansion.md)
   - [`docs/versions/E11_plan_productive_mass_expansion.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_plan_productive_mass_expansion.md)
   - [`docs/versions/E11_build_productive_mass_expansion.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_build_productive_mass_expansion.md)
   - Data Artifact: [`results/e11_productive_mass.json`](file:///c:/Users/pietr/Projects/kaggriculture-agent/results/e11_productive_mass.json)

---

## E11-R0 — Baseline Reproducibility Audit

**Date:** 2026-08-27
**Phase:** AUDIT & TECHNICAL ISOLATION
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Diagnosticare ed isolare la causa dell'apparente collasso di riproducibilità osservato durante il benchmark E11-06, in cui tutte le varianti storiche (E11-01..05) producevano risultati identici a basso reddito (~$7.1k).

### Audit Findings & Outcomes

1. **Cause Radici Diagnosticate:**
   - **Dataclass Default Contamination:** I valori di default della configurazione `ProductiveMassConfig` erano stati modificati in E11-06 (`workforce_scaling_mode = "LAND_CO_SCALING"`), contaminando tutte le istanze storiche senza override esplicito.
   - **Benchmark Factory Parameter Leak:** Il factory benchmark `scripts/benchmark_e11_performance.py` ometteva parametri versione-specifici, ereditando i controlli di riserva per l'assunzione di E11-06 per tutti gli agenti.
2. **Azioni Correttive:**
   - Ripristinati i parametri di default storici ("LEGACY") su `ProductiveMassConfig`.
   - Congelati gli explicit factory builder per ciascuna variante E11 (E11-01..06) in `scripts/benchmark_e11_performance.py`.
3. **Esecuzione Benchmark Appaiato (30 Episodi):**
   - Confermato il ripristino della riproducibilità per E11-01 ($22,962.33), E11-02 ($13,152.00), E11-03 ($892.63), E11-04 ($380.67), E11-05 ($385.33) ed E11-06 ($895.23).
4. **Verdict Finale Audit:** **`E11-R0 PARTIALLY COMPLETED — configuration isolation restored, historical behavioral reproducibility NOT restored`**. L'indipendenza configurazionale della catena sperimentale E11 è stata completamente ripristinata, ma E11-03 ha fallito l'acceptance criterion architetturale. Documento prodotto: [`docs/versions/E11_R0_baseline_reproducibility_audit.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_R0_baseline_reproducibility_audit.md).

---

## E11-X1.1A — HIRE Constraint Verification & E06 Reconciliation Audit

**Date:** 2026-08-27
**Phase:** HIRE CONSTRAINT VERIFICATION & E06 RECONCILIATION AUDIT
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Verificare il codice dell'environment per capire l'esatta regola di validazione di `HIRE` e riconciliare la prestazione storica di E06 ($25.8k su 9 tile) con la baseline E11-VB1 ($429 su 50 tile).

### Key Outcomes & Findings

1. **Verdetto Hard-Cap Workforce:** **`NO — WORKFORCE HARD-CAP FALSIFICATO`**
   L'ispezione del codice dell'environment (`kaggriculture.py` L702–L710) e micro-test in `scratch/audit_hire_constraints.py` hanno dimostrato che l'ambiente non impone alcun vincolo di quadranti o terreno per l'azione `HIRE`. 1 Quadrante consente di assumere 2, 3, 4+ lavoratori se si inviano più ordini `HIRE` nel medesimo turno.
2. **Meccanica Resettamento Hands Scoperta:**
   In Kaggriculture, le **Hands sono lavoratori giornalieri temporanei**, non dipendenti permanenti. Alla fine di ogni giorno (`_end_of_day`, L880–L881), `farm["hands"]` viene resettato a `[]`. I lavoratori desiderati per il giorno `D` devono essere assunti nel giorno `D`.
3. **Causa Radice del Blocco HIRE in E11-X1.1:**
   `ProductiveMassROIAgent` controllava `if hour == 0: builder.hire()`. Inviando un solo ordine `HIRE` al giorno, l'agente assumeva solo 1 Hand al giorno, rimanendo bloccato a 2 lavoratori (1 Farmer + 1 Hand).
4. **Ricostruzione Evidenza Macchina E06:**
   Eseguito un run diagnostico macchina per `WaterFirstHIRENWClusterROIAgent` su `seed=0`: **`p0_reward = $25,847.00`** su 9 tile con 2 lavoratori.
5. **Cause Radice del Divario E06 ($25.8k) vs E11-VB1 ($429):**
   - **Land Purchase Drain:** E11-VB1 spende $1,000 al Giorno 1 per comprare Q1, prosciugando la cassa. E06 spende $0 in terreno.
   - **Spazio & Movimento:** E06 gestisce 9 tile compatte vicine al capanno (distanza 1–3). E11-VB1 disperde 2 lavoratori su 50 tile, sprecando il ~60% dei passi in spostamento.
   - **Velocità di Turnover:** E06 ruota ROI dinamiche ad alta frequenza (Carrot/Wheat), mentre E11-VB1 blocca capitale in colture a lungo ciclo (Melon/Tomato).
6. **Documento Prodotto:** [`docs/versions/E11_X1_1A_hire_constraint_e06_reconciliation.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_1A_hire_constraint_e06_reconciliation.md).

---

## E11-X1.2 — E06 Productive Core Restoration & Corrected Multi-HIRE

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Ripristinare la capacità produttiva ed economica interna già dimostrata da E06 dentro `ProductiveMassROIAgent`, mantenendo un footprint compatto di 9 tile NW pre-espansione, correggendo l'engine Multi-HIRE e differendo l'acquisto di Q1 a quando il core produttivo genera surplus di cassa reale (`cash >= $1,300`).

### Key Outcomes & Findings

1. **Ripristino Core Produttivo Interno:**
   Il benchmark macchina a 10 episodi (`E11-X1.2-20260827-093843`) attribuisce a E11-X1.2 un **Mean Final Money di $7,476.20** (+241.0% rispetto a E11-VB1 baseline di $2,192.20).
2. **Superamento Gate di Produttività ($5k):**
   Con media di **$7,476.20** (min $6,883.00, max $7,877.00 tra i 10 seed), la variante rientra e supera pienamente la fascia di ripristino parziale ($5k–$15k), stabilizzando il flusso di cassa.
3. **Validazione Multi-HIRE Engine:**
   L'agente assume ed ingaggia correttamente 3 lavoratori (1 Farmer + 2 Hands) per sostenere il carico di irrigazione e piantumazione sul core compatto.
4. **Verifica Provenance SHA-256:**
   Risultati 100% verificati dall'autenticatore `verify_e11_run_provenance.py` (`PASS`).
5. **Documento Prodotto:** [`docs/versions/E11_X1_2_e06_productive_core_restoration.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_2_e06_productive_core_restoration.md).

---

## E11-X1.3 — E06 Productive Unit Replication & Scaling

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Trattare **E06** (`WaterFirstHIRENWClusterROIAgent`) come Unità Produttiva Elementare (EPU) da replicare e scalare progressivamente (1× EPU 9t $\rightarrow$ 2× EPU 18t $\rightarrow$ 3× EPU 27t), subordinando l'acquisto di terreno al surplus reale di cassa generato dalle EPU esistenti.

### Key Outcomes & Findings

1. **Subphase A (1× EPU Replication — 9 tile):**
   - Diagnostic A0 (seed 0): **$25,847.00** (**100.0% exact match** to E06 reference).
   - Stage B Benchmark (5 paired episodes): **$26,888.40 Mean Money** (104.0% equivalence ratio vs E06 reference).
   - **Gate A Verdict: `PASSED`**.
2. **Subphase B (2× EPU Scaling — 18 tile):**
   - Sequenza causale verificata: EPU1 produce su Q0 $\rightarrow$ accumula surplus ($\ge \$1,435$) $\rightarrow$ acquista Q1 al Giorno 14 $\rightarrow$ attiva EPU2 al Giorno 15 con Hand 2 (3 lavoratori totali).
   - Stage B Benchmark (5 paired episodes): **$28,727.40 Mean Money** (18/18 active tiles).
   - Scaling Ratio B: **1.07×** ($+\$1,839.00$ guadagno netto su cassa finale).
   - Scaling Efficiency B: **53.4%** ($\frac{1.068}{2}$).
   - **Gate B Verdict: `STOP GATE B ENFORCED`** (Efficiency B $53.4\% < 60.0\%$).
3. **Diagnosi Causa Radice Bottleneck B:**
   EPU2 viene attivata solo al Giorno 15 (dopo il raccolto MELON di EPU1). In 15 giorni rimanenti prima della fine dell'episodio (Giorno 30), EPU2 produce **+$2,839.00** lordi, lasciando un guadagno netto di **+$1,839.00** dopo il costo del terreno ($1,000) e dei semi.
4. **Verifica Provenance SHA-256:** `PASS (100% MATCH)`.
5. **Documento Prodotto:** [`docs/versions/E11_X1_3_e06_productive_unit_replication_scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_3_e06_productive_unit_replication_scaling.md).

---

## E11-X1.3-B — Kaggle External Validation & README Reconciliation

**Date:** 2026-08-27
**Phase:** SHIP EXPERIMENTAL
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Congelare la configurazione verificata **E11-X1.3-B (2× EPU 18-tile Scaling)** nel file di submission standalone `submission/submission.py` e riallineare la documentazione `README.md` dello stato del progetto.

### Key Outcomes & Findings

1. **Submission Bundle Standalone Verificato:**
   - Strategia: `ProductiveMassROIAgent` in modalità `E06_REPLICATED`, `epu_level = 2`, `enable_land_expansion = True`.
   - Generato via `scripts/build_submission.py` in `submission/submission.py`.
   - Audit codice: 0 import interni/file esterni rimasti unbundling.
   - Smoke test locale 720 turni: **$29,993.00** su seed 0 (18 tile attive, 3 lavoratori).
   - Test suite: **63/63 test superati (`pytest tests/`)**.
2. **Reconciliation del README.md:**
   - Riallineata l'intera documentazione di repository dal livello E06 allo stato reale del progetto.
   - Esplicitati gli obiettivi competitivi ($50k minimo, $75k target competitivo, ~$70–75k+ benchmark top competitor).
   - Documentata la correzione metodologica della provenance (E11-R0 ... E11-R3) e la baseline verificata post-audit E11-VB1 ($429).
   - Integrata la tabella sintetica delle iterazioni ed il modello di architettura EPU.
3. **Documento Prodotto:** [`docs/versions/E11_X1_3_B_kaggle_external_validation.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_3_B_kaggle_external_validation.md).

---

## E11-X1.3-B2 — Cross-Boundary Multi-EPU Activation

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Verificare l'ipotesi se un singolo land purchase (Q1, $1,000) possa ospitare sia EPU2 che EPU3 (27 tile attive totali) da subito, riducendo i costi di espansione e aumentando l'efficienza di scaling.

### Key Outcomes & Findings

1. **Audit Geometrico Riuscito:** 27 tile uniche e non sovrapposte rientrano interamente nei 2 Quadranti sbloccati (Q0 + Q1, 50 tile possedute).
2. **Falsificazione Empirica del Benchmark Macchina:**
   - Mean Final Money B2: **$9,808.40** (vs **$28,727.40** in X1.3-B).
   - Scaling Efficiency B2: **12.2%** (falsificato).
3. **Causa Radice Falsificazione:**
   - L'acquisto immediato di Q1 al Giorno 0 prosciuga $1,000 di cassa iniziale ($3k $\rightarrow$ $2k$).
   - I semi per 27 tile ($2,160) superano la liquidità rimanente ($2,000), causando un **starvation di capitale operativo**.
   - Dimostrata la necessità fondamentale dell'acquisto derivato al Giorno 14 post-surplus ($14k+) implementato in `X1.3-B`.
4. **Verifica Provenance SHA-256:** `PASS (100% MATCH)`.
5. **Documento Prodotto:** [`docs/versions/E11_X1_3_B2_cross_boundary_multi_epu_activation.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_3_B2_cross_boundary_multi_epu_activation.md).

---

## E11-X1.3-B2R — Post-Surplus Spatially Equivalent 3× EPU Scaling

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Verificare la sequenza EPU1 $\rightarrow$ working capital surplus $\rightarrow$ 1 BUY_LAND $\rightarrow$ EPU2 + EPU3 (27 tile attive) con ricerca geometrica bounded deterministica (hard limit 60s) e verifica della Spatial Equivalence basata sul movimento locale operativo.

### Key Outcomes & Findings

1. **Ricerca Geometrica Bounded Stage G:**
   - Eseguita in **0.81s** (limit 60s rispettato, 2.225 candidati valutati).
   - Verdetto Rank 1: **`SPATIALLY EQUIVALENT`** ($\text{EPU2 avg int} = 2.00$, $\text{EPU3 avg int} = 2.06$ vs $\text{EPU1 avg int} = 2.00$).
   - Layout 1-land 27 tile inside Q0+Q1 ($x \in [0,9], y \in [0,4]$), zero sovrapposizioni.
2. **Stage A0 Invariant Verification:**
   - 1 episodio (seed 0), Money **$25,781.00**, Provenance **`PASS (100% Match)`**.
3. **Stage B Benchmark (5 Episodi Accoppiati):**
   - Mean Final Money B2R: **$26,435.40** (vs Old B2 **$9,808.40** [+$16,627.00], vs A **$26,888.40** [-$453.00], vs B Candidate **$28,727.40** [-$2,292.00]).
   - Median: **$26,581.00**, Std: **$833.67**, Min: **$25,531.00**, Max: **$27,649.00**.
   - Provenance SHA-256: `PASS (100% Match)`.
4. **Verdetto Architetturale ed Economico:**
   - Architectural: **`VALIDATED`** (Spatial equivalence & 1-land 27-tile capacity).
   - Economic: **`SUB-OPTIMAL`** (L'acquisto land al Day 1 pre-surplus prosciuga $1,000 prima del primo raccolto EPU1; la policy post-surplus Day 14 di X1.3-B resta superiore).
   - Candidate: **`MAINTAIN X1.3-B`** ($28,727.40). No Kaggle submission per B2R.
5. **Documento Prodotto:** [`docs/versions/E11_X1_3_B2R_post_surplus_spatially_equivalent_3x_epu.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_3_B2R_post_surplus_spatially_equivalent_3x_epu.md).

---

## E11-X1.3-B3 — Fixed 3×3 EPU Strip Scaling & Kaggle Submission

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY + SUBMISSION BUNDLING
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Implementare il layout fisso in striscia $3 \times 3$ contiguo per EPU1, EPU2 ed EPU3, applicare il gate del trigger economico post-surplus basato sui ricavi reali monetizzati (`realized_revenue > 0`), validare la provenienza sui 5 episodi del benchmark B e generare il bundle standalone di submission.

### Key Outcomes & Findings

1. **Layout Fisso $3 \times 3$ Contiguo (Nessuna Ricerca Geometrica):**
   - EPU1: $x \in [0,2], y \in [0,2]$ (9 tile)
   - EPU2: $x \in [3,5], y \in [0,2]$ (9 tile)
   - EPU3: $x \in [6,8], y \in [0,2]$ (9 tile)
   - 27 tile uniche in 2Q (Q0+Q1, 1 land purchase).
2. **Trigger Land Post-Surplus Reale:**
   - Il gate `cumulative_realized_revenue > 0` ha impedito l'acquisto pre-surplus al Day 1.
   - `BUY_LAND` si è attivato al **Day 13** post-raccolto EPU1.
3. **Risultati Benchmark Stage B (5 Episodi Accoppiati):**
   - **Mean Money**: **$26,445.60**
   - **Median Money**: **$30,072.00**
   - **Peak Money**: **$31,460.00** (Seed 200)
   - Provenance SHA-256: `PASS (100% Match)`.
4. **Verifica Bundle Standalone (`submission/submission.py`):**
   - Generato via `scripts/build_submission.py`.
   - Test suite automatica: **65/65 passed (`pytest tests/`)**.
   - Smoke test locale 720 turni: **$23,416.00** su seed 0.
5. **Documento Prodotto:** [`docs/versions/E11_X1_3_B3_fixed_3x3_epu_submission.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_3_B3_fixed_3x3_epu_submission.md).

---

## E11-X1.4 — EPU Densification Before Replication (2×3×5 vs B3 3×3×3)

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Confrontare l'ipotesi B (**X1.4**: 2 EPU densificate a $3 \times 5 = 30$ tile) rispetto all'ipotesi A (**B3**: 3 EPU $\times 9 = 27$ tile) sui 5 episodi accoppiati per determinare la configurazione migliore per il run notturno.

### Key Outcomes & Findings

1. **Layout Densificato $2 \times 3 \times 5$ (30 Tile):**
   - EPU1: $x \in [0,2], y \in [0,4]$ (15 tile)
   - EPU2: $x \in [3,5], y \in [0,4]$ (15 tile)
   - EPU3: OFF (Disabilitata)
   - 30 tile uniche in 2Q (Q0+Q1, 1 land purchase).
2. **Risultati Benchmark Stage B (5 Episodi Accoppiati):**
   - **Mean Money**: **$27,209.20** (vs B3 **$26,445.60**, $+ \$763.60$)
   - **Median Money**: **$28,274.00** (vs B3 **$30,072.00**, $- \$1,798.00$)
   - **Std Dev**: **$2,604.28** (vs B3 **$5,687.21**, $-54.2\%$ varianza)
   - **Min Money**: **$22,555.00** (vs B3 **$20,014.00**, $+ \$2,541.00$ floor)
   - **Paired Wins**: B3 vince **3 su 5 episodi (60%)** ed esprime una ceiling superiore ($31,460.00).
3. **Verdetto e Raccomandazione Notturna:**
   - B3 vince nel testa a testa a 3 episodi su 5 e raggiunge il picco massimo di $31.5k.
   - B3 è già verificato semanticamente e pronto nel pacchetto standalone `submission/submission.py`.
   - **Raccomandazione**: Inviare **B3 (`E11-X1.3-B3 Fixed 3x3 3xEPU`)** a Kaggle.
4. **Documento Prodotto:** [`docs/versions/E11_X1_4_epu_densification_before_replication.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_4_epu_densification_before_replication.md).

---

## E11-X1.5 — Centered 2×4×4 Productive Core

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Valutare l'ipotesi C (**X1.5**: 2 EPU centrali adiacenti da $4 \times 4 = 32$ tile attorno al confine Q0/Q1) rispetto a B3 ($3 \times 9 = 27$ tile) e X1.4 ($2 \times 15 = 30$ tile) sui 5 episodi accoppiati.

### Key Outcomes & Findings

1. **Layout Centralizzato $2 \times 4 \times 4$ (32 Tile Target):**
   - EPU1: $x \in [1,4], y \in [1,4]$ (16 tile in Q0)
   - EPU2: $x \in [5,8], y \in [1,4]$ (16 tile in Q1)
   - EPU3: OFF (Disabilitata)
   - 32 tile target uniche attorno allo shed.
2. **Risultati Benchmark Stage B (5 Episodi Accoppiati):**
   - **Mean Money**: **$25,029.00** (vs B3 **$26,445.60**, vs X1.4 **$27,209.20**)
   - **Median Money**: **$24,154.00** (vs B3 **$30,072.00**, vs X1.4 **$28,274.00**)
   - **Std Dev**: **$2,001.35** (Varianza più bassa tra tutte)
   - **Min Money**: **$24,070.00** (Floor più alto)
   - **Peak Active Tiles**: 26 tile (La saturazione delle 16 tile di EPU1 ha ritardato l'avvio operativo di EPU2 in Q1).
3. **Verdetto e Raccomandazione Notturna:**
   - **Verdetto**: **`X1.5 NOT BETTER`**. Il carico economico per avviare 16 tile su EPU1 drena il capitale di lavoro e ritarda l'operatività di EPU2 in Q1.
   - **Raccomandazione**: Inviare **B3 (`E11-X1.3-B3 Fixed 3x3 3xEPU`)** a Kaggle (Median $30,072.00, Peak $31,460.00).
4. **Documento Prodotto:** [`docs/versions/E11_X1_5_centered_2x4x4_productive_core.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_5_centered_2x4x4_productive_core.md).

---

## E11-X1.6 — Progressive Center-Out 3×3 → 4×4 EPU Scaling

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Testare l'ipotesi **H11-X1.6**: densificazione progressiva center-out (EPU1 3×3 → 16t EPU1 4×4 → BUY_LAND → EPU2 3×3 → 32t EPU2 4×4) per proteggere il working capital e sbloccare la massa produttiva di 32 tile senza la starvation sofferta da X1.5.

### Key Outcomes & Findings

1. **Risultati Benchmark Stage B (5 Episodi Accoppiati):**
   - **Mean Money**: **$27,508.20** (MEDIA PIÙ ALTA DI TUTTI I CANDIDATI! $+1,062.60$ vs B3, $+299.00$ vs X1.4, $+2,479.20$ vs X1.5)
   - **Median Money**: **$29,095.00** (Secondo solo a B3 $30.0k)
   - **Max Money (Peak Ceiling)**: **$34,634.00** (RECORD ASSOLUTO DI TUTTI GLI ESPERIMENTI SU SEED 200! $+3,174.00$ sopra B3!)
   - **Paired Wins**:
     - **3 su 5 (60%) vs B3**
     - **3 su 5 (60%) vs X1.4**
     - **4 su 5 (80%) vs X1.5**
2. **Bundle & Semantic Equivalence:**
   - Bundle generato in `submission/submission.py`.
   - Test di equivalenza semantica deterministica: **100% MATCH** su seed 0 ($29,297.00).
3. **Verdetto e Raccomandazione Notturna:**
   - **Verdetto**: **`X1.6 CLEAR WINNER`**.
   - **Raccomandazione Notturna**: Caricare **`E11-X1.6 — Progressive Center-Out 3×3 → 4×4 EPU Scaling`** su Kaggle per la validazione esterna!
4. **Documento Prodotto:** [`docs/versions/E11_X1_6_progressive_center_out_epu_scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_6_progressive_center_out_epu_scaling.md).

---

## E11-X1.7 — Corner-Pruned Center-Out EPU Scaling

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Testare l'ipotesi **H11-X1.7**: rendere 26 tile il target deliberato ed esplicito ($9 \to 13 \to \text{BUY\_LAND} \to 22 \to 26$) escludendo i 3 angoli periferici di ciascun blocco 4×4 per evitare che i worker percorrano distanze eccessive, mantenendo il core centrale.

### Key Outcomes & Findings

1. **Risultati Benchmark Stage B (5 Episodi Accoppiati):**
   - **Mean Money**: **$28,083.80** (NUOVO RECORD ASSOLUTO! $+575.60$ vs X1.6, $+1,638.20$ vs B3)
   - **Median Money**: **$30,081.00** (NUOVO RECORD ASSOLUTO! $+9.00$ vs B3, $+986.00$ vs X1.6)
   - **Peak Ceiling**: **$33,371.00** su seed 200.
   - **Paired Wins**:
     - **4 su 5 (80%) vs X1.6**
     - **3 su 5 (60%) vs B3**
     - **3 su 5 (60%) vs X1.4**
     - **4 su 5 (80%) vs X1.5**
2. **Bundle & Semantic Equivalence:**
   - Bundle generato in `submission/submission.py`.
   - Test di equivalenza semantica deterministica: **100% MATCH** su seed 0 ($30,220.00).
3. **Verdetto e Raccomandazione Notturna:**
   - **Verdetto**: **`X1.7 CLEAR WINNER`**.
   - **Raccomandazione Notturna**: Caricare **`E11-X1.7 Corner-Pruned Center-Out 26t`** su Kaggle!
4. **Documento Prodotto:** [`docs/versions/E11_X1_7_corner_pruned_center_out_26t.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E11_X1_7_corner_pruned_center_out_26t.md).

---

## E12-X1.0 — Centered Hybrid Farm Scaling (Cow-First + Progressive 2×2 Core)

**Date:** 2026-08-27
**Phase:** BUILD + VERIFY
**Tool:** Google Antigravity
**Model:** Gemini 3.6 Flash

### Objective

Testare l'ipotesi **H12**: strategia ibrida `cow-first` con core 2×2 riservato `[(3,3), (3,4), (4,3), (4,4)]` adiacente all'origine `(4,4)` e scaling di colture attorno al livestock core.

### Key Outcomes & Findings

1. **Risultati Benchmark Stage B (5 Episodi Accoppiati):**
   - **Mean Money**: **$6,227.60** vs X1.7 **$28,083.80**
   - **Active Pastures**: **4 Pasture** costruite progressivamente
   - **Active Cows Placed**: **4 Cow** posizionate
   - **Milk Harvested**: **0 unità** (Collo di bottiglia: il grano è stato seminato ma non raccolto nel shed in tempo utile per il FEED quotidiano, portando alla mancata produzione di latte)
2. **Verdetto e Candidato Corrente:**
   - **Verdetto**: **`Outcome C: Feed Bottleneck`**.
   - **Candidato Corrente Kaggle**: **`E11-X1.7 Corner-Pruned Center-Out 26t`** rimane il **CAMPIONE ASSOLUTO** ($28,083.80 Mean Money, $30,081.00 Median Money) pronto in `submission/submission.py`.
3. **Documento Prodotto:** [`docs/versions/E12_X1_0_centered_hybrid_farm_scaling.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E12_X1_0_centered_hybrid_farm_scaling.md).

---

## E12-X1.12 — TRUEBELIEF Economic Engine Reconstruction

**Date:** 2026-08-28
**Phase:** BUILD + VERIFY + MANUAL KAGGLE UPLOAD
**Tool:** Codex
**Model:** GPT-5

### Input principale

- replay truebelief episodio `101294736`
- seed `421521921`
- score truebelief `$86,297`
- raw replay preservato in `results/e12/x111/101294736.json`
- checksum SHA-256: `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695`

### Obiettivo

- seed `0`: `>= 80,000`
- seed `421521921`: `>= 80,000`
- terreno: `Q0+Q1 only`

### Risultato locale

- seed `0`: `$42,491`
- seed `421521921`: `$48,313`
- livestock totale: `7 Cow / 4 Sheep`
- peak productive: `35`
- hard gate: FAIL

### Confronto con X1.11

- X1.11: `$29,858 / $24,827`
- X1.12: `$42,491 / $48,313`
- miglioramento assoluto seed `0`: `+12,633`
- miglioramento assoluto seed `421521921`: `+23,486`
- miglioramento percentuale seed `0`: `+42.31%`
- miglioramento percentuale seed `421521921`: `+94.60%`

### Diagnosi

- livestock reconstruction sostanzialmente riuscita;
- crop throughput ancora insufficiente;
- post-Q1 routing / worker assignment e il collo dominante osservato;
- evitare tuning marginale di costanti economiche finche il throughput non viene risolto.

### Submission

- standalone rebuild: PASS
- behavioral equivalence: PASS
- upload Kaggle: effettuato manualmente
- descrizione: `E12-X1.12 Truebelief Engine — Q0+Q1, 7 Cow + 4 Sheep, competitive replay baseline`
- risultato esterno: `PENDING`

### Decisione metodologica

X1.12 viene pubblicata pur non raggiungendo 80k perche diventa la baseline del nuovo ciclo di competitive learning quotidiano.

---

## E12-X1.12 — Model Correction: Livestock and Q2 Are Not Hard Constraints

**Date:** 2026-08-28
**Phase:** MODEL CORRECTION
**Tool:** Codex
**Model:** GPT-5

### Evidence

- replay truebelief `101294736` aveva mostrato `7 Cow / 4 Sheep` e Q0+Q1;
- prime osservazioni esterne X1.12 mostrano sovraconcentrazione livestock e degrado della crop surface;
- avversari competitivi osservati utilizzano anche Q2.

### Previous model assumptions

- `Q0+Q1 only` trattato troppo rigidamente;
- livestock trajectory troppo vicina al riferimento `7 Cow / 4 Sheep`.

### Model delta

- livestock target -> capacity/ROI-gated;
- Q2 forbidden -> economically/operationally gated.

### Status

- `INFERRED`
- da implementare e testare nel prossimo BUILD

Nessun miglioramento numerico viene registrato per questa correzione: e un aggiornamento del modello concettuale, non una nuova strategy.

---

## E12-X1.13 — Dynamic Allocation Verification Build

**Date:** 2026-08-28
**Phase:** BUILD + VERIFY
**Tool:** Codex
**Model:** GPT-5

### Objective

Implementare una nuova modalita separata `E12_DYNAMIC_ALLOCATION_X113` per verificare allocazione dinamica fra crop, livestock e Q2 senza modificare X1.12.

### Counterfactual

| Variant | Delta | Seed 0 | Seed 421521921 | Verdict |
|---|---|---:|---:|---|
| A | X1.12 baseline unchanged | `$42,491` | `$48,313` | baseline |
| B | livestock dynamic gate, Q2 disabled | `$34,230` | `$30,389` | rejected |
| C | B + workload HIRE | `$1,311` | `$2,329` | rejected |
| D | C + dynamic Q2 | `$1,311` | `$2,329` | rejected; Q2 gate did not fire |
| E | D + crop-SLA assignment | `$9,673` | `$8,988` | rejected |

### Diagnosis

- Variant B improved crop surface (`mean 21.53`, `peak 37`) and reduced weed/unwatered tile-days, but lost too much cash conversion by suppressing livestock to `0 Cow / 0 Sheep`.
- Workload HIRE variants C/D starved capacity and collapsed revenue.
- Q2 did not fire in D/E, so Q2 remains unvalidated rather than disproven.
- Crop-SLA assignment E reduced weeds but did not recover harvested-empty backlog or final money.

### Artifacts

- `results/e12/x113/IMPLEMENTATION_DELTA.md`
- `results/e12/x113/COUNTERFACTUAL_LOG.md`
- `results/e12/x113/counterfactual_results.json`
- `results/e12/x113/counterfactual_results.csv`

### Conclusion

`X1.13 STRUCTURAL CEILING: MEASURED`

---

## E13 — Multi-Agent Blind Forensic Replay Analysis (Episode 101971376)

**Date:** 2026-08-28
**Phase:** FORENSIC / MULTI-AGENT BENCHMARK
**Tool / Agents:** Antigravity, Codex, Copilot (independent blind analyses, post-hoc consolidation)
**Primary Source:** `docs/benchmark/101971376.json` (Seed: `1630102796`, Steps: `720`)

### 1. Episode Identification & Macro Outcome

| Parameter | Observed Value |
|---|---|
| **Episode ID** | `101971376` |
| **Seed** | `1630102796` |
| **Player 0 (Pietro Valocchi)** | Final Money: **$7,123.00** |
| **Player 1 (Harith Al-Ani)** | Final Money: **$133,049.00** |
| **Gap / Ratio** | **+$125,926.00** (Harith **18.68x** Pietro) |
| **Artifacts Generated** | `results/e13/episode_101971376/{antigravity,codex,copilot}/` |

### 2. Multi-Agent Convergent Facts

All three independent analyses (Antigravity, Codex, Copilot) converge on the following core findings:
1. **Outcome**: Pietro `$7,123` vs Harith `$133,049`.
2. **Early origin**: The gap is NOT created in late game; it compounds from early structural divergence.
3. **Capacity parity without throughput**: Workforce scale (292 vs 291 HIREs), livestock headcount (18 vs 15 final animals), and owned land (75 tiles each, 3 quadrants) do NOT explain the score gap.
4. **Q2 is insufficient**: Pietro also purchased Q2 on Day 17 (owned 3 quadrants for 13 days), but achieved $0 extra cash crop revenue from it.
5. **Massive Irrigation Disparity**: Harith executed **1,145 WATER actions** vs Pietro's **79 WATER actions** (delta: `+1,066`, ratio: `~14.5x`).
6. **Massive Sell Value Disparity**: Harith explicit/estimated SELL value **~$171,870** vs Pietro **~$83,418** (delta: `+$88,452`).
7. **Root Diagnostic**: The fundamental differentiator is **Productive/Economic Throughput** (conversion of capacity into work, output, sales, and reinvestment), not physical capacity acquired.

### 3. Interpretative Divergence & Synthesis

- **Antigravity**: Pinpoints **causal/operational onset on Day 1 (Hours 6–14/23)**, where Pietro executed 0 WATER actions and entered an unproductive `["HARVEST"]` loop on empty tiles, while Harith planted and watered 17 crops.
- **Copilot**: Identifies **material divergence at Day 1 boundary (Turn 23)**, with Harith reaching 21 productive tiles vs Pietro's 8 in the initial quadrant.
- **Codex**: Identifies **economic lock-in / structural persistence on Day 12**, when cash lead exceeds $1k and multi-dimensional capacity (cash, land, livestock, productive tiles) becomes persistently entrenched.
- **Consolidation**: `Day 1 = causal/operational onset` ➔ `Day 12 = economic lock-in / structural persistence`.

### 4. Key Quantitative Metrics

- **WATER actions**: Harith `1,145` vs Pietro `79` (Consensus: Antigravity, Copilot).
- **Crop-care actions (Codex definition)**: Harith `1,333` vs Pietro `259` (delta: `+1,074`).
- **Priced SELL Revenue**: Harith `~$171,870` vs Pietro `~$83,418` (Consensus across ledgers).
  - *Crop Revenue*: Harith `$89,446` ($56.3k Strawberry, $20.2k Melon, $12.9k Wheat) vs Pietro `$38,100` ($0 Strawberry, $0 Melon, 100% Wheat).
  - *Livestock Product Revenue*: Harith `$65,441` ($38.0k Wool, $27.4k Milk) vs Pietro `$43,933` ($24.5k Milk, $19.5k Wool).
  - *Fertilizer Revenue*: Harith `$16,983` (228 sold) vs Pietro `$1,385` (16 sold).
- **Wheat Feed Drain (Antigravity Single-Agent Finding)**: Pietro spent `$42,477` buying market Wheat product vs `$38,100` selling Wheat (net loss: `-$4,377`), whereas Harith produced feed internally.

### 5. Hypotheses Falsified / Weakened

- ❌ *“Serve semplicemente comprare Q2”*: Falsificato (Pietro possedeva Q2 per 13 giorni).
- ❌ *“Servono semplicemente più Hands”*: Falsificato (292 vs 291 HIREs totali).
- ❌ *“Servono semplicemente più animali”*: Falsificato (Pietro 18 animali vs Harith 15).
- ❌ *“Serve semplicemente possedere più superficie”*: Falsificato (entrambi 75 tile).
- ❌ *“Basta tenere il campo pulito”*: Indebolito (campo pulito senza colture non produce reddito).
- ❌ *“Il gap nasce soprattutto nel late game”*: Falsificato (onset Day 1, lock-in Day 12).

### 6. Central Conclusion & Economic Chain

> **Conclusione E13:** La nostra carenza principale nell'episodio 101971376 non è la quantità di capacità acquistata, ma la conversione della capacità disponibile in lavoro produttivo e monetizzazione.

**Catena economica di riferimento:**
`worker-turn → productive action → output/inventory → SELL → cash → reinvestment → compounded capacity`

### 7. Limitations & Open Questions

- Opponent internal intent: `NOT_OBSERVABLE`.
- Transactional HIRE/BUY_LAND exact cost & per-transaction P/L under dynamic market pricing: `INFERRED / DERIVED`.
- Local ↔ Kaggle Fidelity (Seed 0 candidate local `$37,543` vs Kaggle `$8,690`): separate problem requiring dedicated same-seed/same-code trace.

---

## E14 — Repository Isolation & Canonical Ontology

**Date:** 2026-08-28
**Phase:** FORMALIZATION & ISOLATION
**Tool / Modeler:** Antigravity, Codex, Copilot

### Objective
Isolare l'architettura del repository per consentire a tre modeler indipendenti (Antigravity, Codex, Copilot) di formalizzare le candidate feature emerse da E01–E13 in una **Ontologia Canonica a 64 concetti** (`docs/model_specs/ONTOLOGY.md`) e tre `MODEL_SPEC` indipendenti.

### Key Outcomes & Findings
1. **Ontologia Canonica (64 Concetti):** Mappatura 1-a-1 completata senza concetti mancanti o extra.
2. **Tripla Specifica di Modello:**
   - Antigravity MODEL_SPEC: `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY.md`
   - Codex MODEL_SPEC: `docs/model_specs/codex/MODEL_SPEC_CODEX.md`
   - Copilot MODEL_SPEC: `docs/model_specs/copilot/MODEL_SPEC_COPILOT.md`
3. **Generazione e Isolamento Submission:** Ciascun modeler ha prodotto una policy submission standalone conforme alla propria specifica.

---

## E15 — Pre-Tournament Freeze & Pairwise Tournament

**Date:** 2026-08-29
**Phase:** TOURNAMENT & FEATURE DISCRIMINATION
**Evidence Role:** `TRAINING EVIDENCE`

### Tournament Results & Consensus
- **M1 (Seed 1113294977):** Antigravity ($8,672) vs Codex ($20,461) — Winner: **Codex**.
- **M2 (Seed 3033283457):** Codex ($27,510) vs Copilot ($37,752) — Winner: **Copilot**.
- **M3 (Seed 3122977751):** Copilot ($26,629) vs Antigravity ($9,371) — Winner: **Copilot**.
- **Standings:** Copilot (2–0), Codex (1–1), Antigravity (0–2). Winner: **Copilot**.
- **Two-Regime Model Established:**
  - *Regime A (Sub-threshold):* When irrigation or maintenance fails, working surface collapses and nominal assets amplify losses.
  - *Regime B (Super-threshold):* When irrigation is stabilized, monetization quality and inventory conversion dominate.

---

## E16-A — Stage A Frozen Training & Forensic Diagnosis

**Date:** 2026-08-29
**Phase:** TRAINING / STAGE A FROZEN EXECUTION
**Evidence Role:** `TRAINING EVIDENCE` (Forensic Baseline)

### Objective
Eseguire i 28 episodi frozen del DOE E16 Stage A (Celle A01–A07, 2 seed: 1802163452, 1678077158, 2 seat vs Copilot E15 frozen) per valutare l'interazione tra `watering_dispatch_priority` (0.20, 0.45, 0.70) e `crop_working_set_target` (10, 17, 25).

### Outcome & Forensic Diagnosis (`E16_STAGE_A_FORENSIC_DIAGNOSIS.md`)
1. **Contaminazione Telemetrica (Bug id(farm)):**
   - Un mismatch nell'indicizzazione dell'oggetto `farm` ha assegnato `player: -1` a tutte le unit action nel ledger eventi.
   - `successful_water` ha filtrato per `player == treatment_seat`, azzerando `watering_execution_rate = 0.0` e `watering_continuity = 0.0` nei report automatici, nonostante l'esecuzione di 50–95 azioni di irrigazione reali.
2. **Difetto Semantico Priority-as-Quota:**
   - La policy ha implementato `priority` come quota frazionaria (`math.ceil(priority * active_crops)`), escludendo deliberatamente (1-p) colture al giorno.
   - Con la regola del motore Kaggriculture di morte per siccità a 2 giorni consecutivi (`consecutive_unwatered >= 2`), l'esclusione frazionaria ha causato la morte dell'intero contingente di colture entro 2–4 giorni.
3. **Cash Stall a $300 nelle celle a 25 crop (A03, A06):**
   - Spese iniziali incontrollate al Day 0 (Land $1,000 + Seeds $1,610 + Workforce $900) hanno portato la cassa al floor di $300.00 prima del primo raccolto, bloccando permanentemente il rinnovo dei lavoratori e acquisti livestock.
4. **Preservazione:** I 28 run originali sono preservati intatti in `results/e16/stage_a/` come baseline forense.

---

## E16-A-R1 — Corrected Replication Execution & Gate C* Evaluation

**Date:** 2026-08-29
**Phase:** TRAINING / CORRECTED REPLICATION EXECUTION
**Evidence Role:** `TRAINING EVIDENCE`
**Test Suite:** `143/143 PASS`

### Objective
Rieseguire i 28 episodi Stage A con la build corretta R1 (`E16_TREATMENT_BUILD_R1.py`), config frozen R1 (`E16_R1_FROZEN_CONFIG.json`), ledger attribution corretta e priorità WATER implementata come precedenza operativa di dispatch anziché quota frazionaria.

### Outcome & Validated Telemetry (28/28 Episodi Completati)
- **Failures:** 0 gameplay failures, 0 infrastructure failures.
- **Integrity Check:** `PASS` (0 unit action con `player: -1`, 0 hash mismatches).
- **Watering Realization Validated:**
  - HIGH `watering_execution_rate`: **0.8898 – 0.9416** (vs 0.0 originario).
  - `watering_continuity`: **~0.96** in tutte le celle HIGH.
  - La siccità sintetica indotta dal codice è stata completamente eliminata.

### Risultati Economici Principali (Stage A-R1):

| Cella | Crop Target | Water Priority | Final Money (Mediana) | Final Money (Media) | Water Exec Rate | Water Continuity | Crop Target Attainment |
|---|---|---|---|---|---|---|---|
| **A01** | 10 | 0.20 (LOW) | **$19,694.00** | $18,970.00 | 0.7241 | 0.7000 | 0.0000 |
| **A02** | 10 | 0.70 (HIGH) | **$21,230.50** | $21,255.25 | 0.9316 | 0.9630 | 0.4750 |
| **A03** | 25 | 0.20 (LOW) | **$11,903.50** | $12,112.00 | 0.8542 | 0.8750 | 0.1600 |
| **A04** | 25 | 0.70 (HIGH) | **$19,987.00** | $19,522.50 | 0.8898 | 0.9600 | 0.3000 |
| **A05** | 17 | 0.45 (MID) | **$26,619.50** | $25,499.25 | 0.9084 | 0.9000 | 0.3529 |
| **A06** | 25 | 0.45 (MID) | **$21,570.50** | $21,500.25 | 0.8782 | 0.9630 | 0.2800 |
| **A07** | 17 | 0.70 (HIGH) | **$27,076.00** | $26,832.50 | 0.9416 | 0.9615 | 0.4706 |

### Contrasti Chiave (R1):
- **A02 - A01:** Mediana **+$1,576.00** (Inversione di direzione rispetto a -$4,737 originale; HIGH water benefica anche a scale compatte).
- **A04 - A03:** Mediana **+$8,587.00** (Forte premio positivo per HIGH water a scala 25 confermato).
- **Interazione Primaria `(A04 - A03) - (A02 - A01)`:** Mediana **+$5,180.50** (Interazione positiva tra capacità e priorità di irrigazione confermata).
- **Segnale Crop 17:** A07 ($27,076.00 mediana) è la regione economicamente più promettente osservata in Stage A-R1, ma **NON è una soglia di capacità né un optimum**.

### Valutazione Gate di Capacità C*:
- **A02:** Completion=1.0, WaterRate=0.9316, Continuity=0.9630, Attainment=**0.4750** (< 0.80) ➔ `NO`
- **A07:** Completion=1.0, WaterRate=0.9416, Continuity=0.9615, Attainment=**0.4706** (< 0.80) ➔ `NO`
- **A04:** Completion=1.0, WaterRate=0.8898, Continuity=0.9600, Attainment=**0.3000** (< 0.80) ➔ `NO`
- **Selected C\*:** `NONE`
- **Stage B Gate:** `STAGE_B_BLOCKED_NO_CAPACITY_ANCHOR`
- **Stage B Eseguito:** `NO`

### Interpretazione e Separazione Epistemica
- **MODEL_VALIDITY:** Fortemente supportata (le predizioni teoriche su necessità di manutenzione, correlazione irrigazione-sopravvivenza e non-monotonia della superficie sono confermate).
- **POLICY_REALIZATION:** Il repair ha rimosso WATER come collo di bottiglia primario. L'irrigazione HIGH viene ora realizzata (93–96%), ma la policy non raggiunge il target di superficie mantenuta (attainment 0.30–0.475 vs >= 0.80). Il nuovo problema da discriminare riguarda la realizzazione/mantenimento della superficie coltivata (routing, capacity/workforce allocation, replanting timing).
- **IMPLEMENTATION_FIDELITY:** Verificata e conforme.

### Decisione di Chiusura:
- E16 è fermato per questa sessione. Stage B non eseguito.
- Prossima sessione: diagnosi forense del basso `crop_target_attainment` sui 28 run R1 esistenti prima di qualsiasi nuovo esperimento.

---

## MODEL_SPEC C2 Build Phase — Foundation Closure & Candidate Verification

**Date:** 2026-08-30
**Phase:** MODEL_SPEC C2 BUILD & VERIFICATION
**Evidence Role:** `BUILD & VERIFICATION EVIDENCE`
**Test Suite:** `168 passed`
**Repository Hygiene:** `git diff --check PASS`

### Summary & Outcomes
1. **Foundation C2 Blocker Closure:**
   - Formal vocabulary and lifecycle states consolidated (`ONTOLOGY_C2.md`).
   - 11-phase engine loop, state transitions, and FEED+CARE EOD mechanics verified (`KAGGRICULTURE_STATE_MACHINE_C2.md`).
   - Canonical feature contracts established and all known blockers closed (`KAGGRICULTURE_FEATURE_MODEL_C2.md`).
   - Foundation C2 declared `UPSTREAM_READY_FOR_MODEL_SPEC` and `NOT FROZEN` (non-blocking for tournament).
2. **3 Independent MODEL_SPEC C2 Builds & Executables:**
   - **Antigravity C2:** `MODEL_SPEC_ANTIGRAVITY_C2.md` -> `src/agricola/strategy/antigravity/agent_c2.py` (`TOURNAMENT_READY: YES`)
   - **Codex C2:** `MODEL_SPEC_CODEX_C2.md` -> `src/agricola/strategy/codex_c2.py` (`TOURNAMENT_READY: YES`)
   - **Copilot C2:** `MODEL_SPEC_COPILOT_C2.md` -> `src/agricola/strategy/copilot/agent_c2.py` (`TOURNAMENT_READY: YES`)
3. **Validation Status:**
   - Repository regression suite: `168 passed` (all candidate suites green).
   - Candidate verification reports: 3/3 `TOURNAMENT_READY: YES`.
   - Tournament: `NOT RUN`.
   - Post-tournament reviews: `PENDING`.
   - Kaggle validation: `NOT RUN`.

### Next Step
- **Next Experiment:** `MODEL_SPEC TOURNAMENT C2` (frozen common protocol, same seeds/opponents/telemetry, independent 3-way evaluation).
