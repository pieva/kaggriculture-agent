# PROJECT_STATE — Kaggriculture

## Stato corrente

```text
PROJECT: Kaggriculture
STATUS_DATE: 2026-09-01
PHASE: FOUNDATION C2.1 CLOSED / E17 BENCHMARK DEFINITION READY

ENGINE_CONTRACT: FROZEN
ONTOLOGY_C2_1: RECONCILED
STATE_MACHINE_C2_1: RECONCILED
FEATURE_MODEL_C2_1: RECONCILED
SHARED_DELIBERATION_LAYER: NONE
OBSERVATION_CONTRACT: src/agricola/core/observation_contract.py

CODEX_CLEANUP: COMPLETE
ANTIGRAVITY_CLEANUP: COMPLETE
COPILOT_CLEANUP: COMPLETE
TRANSITIONAL_C2_LINEAGES: REMOVED

NEXT_EXPERIMENT: E17
E17_PHASE: DEFINE
E17_OBJECTIVE: DEFINE_3Q_OPTIMIZATION_BENCHMARK_STRATEGY
E17_POLICY_MUTATION: NOT_STARTED
```

## Evidenza Kaggle esterna corrente

Snapshot fornito dall'utente il 2026-09-01:

| Indicatore | Valore |
|---|---:|
| Codex V9 3Q | `1159,9` |
| Codex V7.3 dual-Q | `598,3` |
| Delta V9 vs V7.3 | `+561,6` (`+93,9%`) |
| Posizione Codex V9 nello snapshot | `2542` |
| Leader visibile | `2943,6` |
| Gap dal leader visibile | `1783,7` |
| Quota del punteggio leader | `39,4%` |

Il passaggio alla versione 3Q costituisce quindi un miglioramento esterno
materiale, ma non una convergenza verso il vertice. Lo score Kaggle non va
confuso con `final_money` dei benchmark locali: E17 deve definire come usare
le metriche locali per selezionare candidate con maggiore probabilità di
miglioramento esterno.

Il replay pubblico `docs/benchmark/104498819.json` mostra una strategia ad alto
rendimento che termina con tre quadranti attivi (`NW`, `NE`, `SW`). Questo,
insieme al salto V7.3 -> V9, rende 3Q una forte ipotesi architetturale di
lavoro. La schermata leaderboard non espone però il codice dei concorrenti:
l'affermazione che tutti o la maggior parte dei top usino 3Q resta non
verificata e non deve essere trattata come fatto.

## Foundation corrente

Il riferimento canonico e i relativi hash sono in
`docs/model/FOUNDATION_C2_1_MANIFEST.md`:

1. `docs/model/ontology/ONTOLOGY_C2_1.md`;
2. `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md`;
3. `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md`;
4. `src/agricola/core/observation_contract.py`.

La Foundation non prescrive un processo deliberativo condiviso. Routine,
planner, working set e priorità sono agent-local.

## Baseline 3Q congelate

### Codex V9

- MODEL_SPEC: `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`;
- source: `src/agricola/strategy/codex_3q_mixed_high_density.py`;
- routine: `src/agricola/strategy/codex_v9_routine_data.py`;
- config: `configs/model_spec_c2/CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json`;
- submission: `submission/submission_codex.py`;
- SHA-256 submission: `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421`;
- parità standalone: `719/719 PASS`.

### Antigravity V4

Baseline 3Q derivativa con liquidazione terminale. Submission canonica e
freeze sono byte-identiche, SHA-256
`5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872`.

### Copilot V2

Baseline 3Q derivativa senza submission canonica. È mantenuta per diagnostica
e confronto, non come strategia indipendente promossa.

Il torneo di chiusura resta valido come replica e ablation, non come confronto
fra tre strategie indipendenti, perché Antigravity V4 e Copilot V2 riusano la
routine Codex. `STRATEGIC_INDEPENDENCE_GATE: FAIL`.

## Obiettivo E17 — definizione del benchmark di ottimizzazione 3Q

E17 non deve iniziare modificando la policy. Deve produrre e congelare una
strategia di benchmark che renda misurabile l'ottimizzazione del modello 3Q.

Output minimi richiesti:

1. baseline Codex V9 immutabile e identificata tramite hash;
2. matrice di benchmark con seed preregistrati, holdout separato, seat
   bilanciati e avversari congelati;
3. distinzione fra benchmark passivo economico, confronto competitivo e
   validazione esterna Kaggle;
4. metriche leading per Q0/Q1/Q2, workforce, azioni produttive, movimento,
   capacità, colture, livestock, mercato, liquidazione ed errori;
5. protocollo di ablation causale: una famiglia di leve per volta, senza
   variazioni aggregate non attribuibili;
6. criteri di promozione robusti su media, mediana, floor, varianza, seat e
   holdout, definiti prima di osservare il risultato;
7. ledger requested/executed e provenance completa di source, config,
   routine, benchmark e submission;
8. piano esplicito per verificare se i miglioramenti locali predicono la
   direzione dello score Kaggle.

Ogni agente potrà usare il benchmark comune, ma dovrà sviluppare una propria
strategia senza importare o copiare routine, planner, dispatcher o action
table di un altro agente.
