# PROJECT_STATE — Kaggriculture

## Stato corrente

```text
PROJECT: Kaggriculture
STATUS_DATE: 2026-09-02
PHASE: FOUNDATION C2.1 CLOSED / E17.0 EXTERNAL VALIDATION LIVE / STOP BEFORE E17.1

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
REPOSITORY_REORGANIZATION: COMPLETE / A0-A7 PASS
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
COMMON_EXECUTION_PROMPT: experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md

NEXT_EXPERIMENT: E17
E17_PHASE: E17.0 COMPLETE / STOP BEFORE E17.1
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: NOT_STARTED
E17_DISCOVERY_BENCHMARK: COMPLETE
E17_CROSS_AGENT_REVIEW: CLOSED
E17_STRATEGY_DRAFT: experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md
E17_STRATEGY_FROZEN: experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_1_AUTHORIZED: NO
E17_EXTERNAL_SUBMISSION: LIVE_SCORE_STABILIZING
E17_EXTERNAL_RELEASE: CODEX-E17.0-EXTERNAL-CONTROL-V1
E17_KAGGLE_SUBMISSION_ID: 559588638
ACTIVE_DEVELOPMENT_AGENT: CODEX_ONLY
ANTIGRAVITY_STATUS: PAUSED_CREDIT_EXHAUSTION
COPILOT_E17_NATIVE: PRESERVED_LOCAL_ONLY_NO_KAGGLE_SUBMISSION
```

## Evidenza Kaggle esterna corrente

Snapshot Codex del 2026-09-01 e leaderboard aggiornata fornita dall'utente il
2026-09-02:

| Indicatore | Valore |
|---|---:|
| Codex V9 3Q | `1159,9` — snapshot precedente, non visibile nella schermata aggiornata |
| Codex E17 external control | `996` — rilevazione intermedia, ingresso a `600`, non stabilizzata |
| Delta E17 intermedio dall'ingresso | `+396` |
| Codex V7.3 dual-Q | `598,3` |
| Delta V9 vs V7.3 | `+561,6` (`+93,9%`) |
| Posizione Codex V9 | `2542` — snapshot precedente |
| Leader corrente visibile | `2917,8` (`Crop Dusta`) |
| Secondo corrente visibile | `2890,3` (`tetsuya`) |
| Terzo corrente visibile | `2878,5` (`3정훈`) |

Il passaggio alla versione 3Q costituisce quindi un miglioramento esterno
materiale, ma non una convergenza verso il vertice. Lo score Kaggle non va
confuso con `final_money` dei benchmark locali: E17 deve definire come usare
le metriche locali per selezionare candidate con maggiore probabilità di
miglioramento esterno.

Il nuovo snapshot non mostra Codex, quindi gap e quota contemporanei non
possono essere ricalcolati senza riusare un valore di un'altra finestra. La
variazione dell'ordine — Crop Dusta da terzo a primo e tetsuya da primo a
secondo — conferma che rating e piccolo campione replay misurano orizzonti
diversi.

La submission E17 è stata successivamente caricata su Kaggle con ID
`559588638`. Gli screenshot forniti dal proprietario mostrano una progressione
da `600` a `996`, con vittorie recenti e un episodio ancora in corso. Il valore
`996` è quindi un'osservazione intermedia: non sostituisce ancora il precedente
riferimento V9 `1159,9` e non autorizza inferenze sull'effetto della policy,
che è rimasta comportamentalmente identica.

Il benchmark discovery E17 ha verificato nove replay unici dei tre player che
erano Top 3 al momento della raccolta: in tutti i player-seat target la
sequenza è `NW -> NE -> SW`, senza Q3. Il campione identifica tre archetipi
distinti (`tetsuya` distribuito, `OceanMix` compatto, `Crop Dusta`
ultra-precoce), ma non dimostra che 3Q o 12 hands siano ottimi globali. Nello
snapshot 2026-09-02 Crop Dusta è leader e OceanMix non è nei primi sette
visibili: i risultati vanno quindi trattati come benchmark di archetipi, non
come fotografia permanente della classifica. I risultati sono documentati in
`experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`.

## Foundation corrente

Il riferimento canonico e i relativi hash sono in
`docs/foundation/FOUNDATION_C2_1_MANIFEST.md`:

1. `docs/foundation/ontology/ONTOLOGY_C2_1.md`;
2. `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md`;
3. `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md`;
4. `src/agricola/core/observation_contract.py`.

La Foundation non prescrive un processo deliberativo condiviso. Routine,
planner, working set e priorità sono agent-local.

## Baseline 3Q congelate

### Codex V9

- MODEL_SPEC: `docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`;
- source: `src/agricola/strategy/codex/codex_3q_mixed_high_density.py`;
- routine: `src/agricola/strategy/codex/codex_v9_routine_data.py`;
- config: `docs/model_specs/codex/configs/CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json`;
- submission: `submission/submission_codex.py`;
- SHA-256 submission E17 esterna: `0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`;
- parent V9 frozen SHA-256: `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421`;
- parità standalone: `719/719 PASS`.

### Antigravity V4

Baseline 3Q derivativa con liquidazione terminale. Submission canonica e
freeze sono byte-identiche, SHA-256
`5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872`.

### Copilot V2

Baseline 3Q derivativa senza submission canonica. È mantenuta per diagnostica
e confronto, non come strategia indipendente promossa.

La successiva baseline nativa Copilot E17.0 è conservata con source, config,
freeze e report nei percorsi agent-local di `experiments/e17/`; per decisione
del proprietario non verrà sottoposta a Kaggle. La directory `submission/`
contiene quindi soltanto la candidate canonica Codex.

Il torneo di chiusura resta valido come replica e ablation, non come confronto
fra tre strategie indipendenti, perché le baseline storiche Antigravity V4 e
Copilot V2 riusano la routine Codex. Quel gate storico resta `FAIL`. Le nuove
baseline native costruite in E17.0 hanno invece superato l'audit locale e di
integrazione: `E17_0_STRATEGIC_INDEPENDENCE_GATE: PASS`.

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

Il riferimento operativo corrente è
`experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`. La review della strategia
è chiusa ed E17.0 è stato eseguito. Nessuna mutazione della policy oltre il
perimetro di costruzione delle baseline native è iniziata; E17.1 non è
autorizzato.

E17 non assume che uno dei tre archetipi sia universalmente vincente. Ogni
profilo combina livelli differenti di timing, topologia, densità,
diversificazione, reinvestimento e chiusura. Il benchmark deve stimare prima
gli effetti principali di queste dimensioni e poi le interazioni più
plausibili, senza assemblare post-hoc le caratteristiche dei vincitori.

## Chiusura E17.0

Il riepilogo normativo è
`experiments/e17/reports/common/E17_0_GATE_AND_BLOCKER_SUMMARY.md`.

| Agente | Ruolo | Parità/riproducibilità | Ledger | Errori | Fughe EOD | Mean development | Stato |
|---|---|---|---:|---:|---:|---:|---|
| Codex | V9 frozen + ledger | `4314/4314`, outcome `6/6` | 51.834 / 100% | 0 | 0 | 132.019,3 | PASS |
| Antigravity | baseline nativa 3Q | `6/6` | 4.326 / 100% | 0 | 0 | 0 | PASS con limitazione maggiore |
| Copilot | baseline nativa 3Q | `6/6` | 26.163 / 100% | 0 | 0 | 8.941,5 | PASS |

I gate tecnici E17.0 sono superati e holdout/final confirmation non sono stati
consumati. La competitività locale delle baseline native non è stabilita:
Antigravity è 3Q ma non produttiva (`max_hands=0`), mentre Copilot è produttiva
ma molto sotto la V9 Codex contro opponent inert. Antigravity è ora in pausa
per crediti e Copilot non verrà sottoposta; il prossimo intervento verrà scelto
solo dopo la stabilizzazione del rating esterno Codex. E17.1 resta non
autorizzato.

## Confronto esterno E17 autorizzato

Antigravity non è disponibile per esaurimento dei crediti; il torneo locale a
tre è pertanto omesso. È stata caricata la release
`CODEX-E17.0-EXTERNAL-CONTROL-V1`, basata sul file canonico
`submission/submission_codex.py`, SHA-256
`0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`.

La release cambia soltanto i metadati del wrapper e mantiene parità
comportamentale con la V9: non promette un incremento sistematico rispetto al
precedente score Kaggle `1159,9`, ma misura la ripetibilità esterna dopo il
riordino e la chiusura del gate E17.0. Manifest e report sono in:

- `experiments/e17/artifacts/freeze/codex/E17_EXTERNAL_SUBMISSION_MANIFEST.json`;
- `experiments/e17/reports/codex/E17_EXTERNAL_SUBMISSION_READINESS_REPORT_IT.md`.

La submission Kaggle `559588638` ha raggiunto la rilevazione intermedia `996`
da `600` (`+396`). Il rating è ancora in assestamento e non viene usato come
esito finale. E17.1 resta non iniziato; lo sviluppo proseguirà con Codex solo
dopo la stabilizzazione del confronto esterno.
