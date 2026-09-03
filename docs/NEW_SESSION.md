# NEW_SESSION — Kaggriculture

## Ripresa operativa

```text
START_HERE: docs/PROJECT_STATE.md
FOUNDATION: C2.1 RECONCILED
FOUNDATION_MANIFEST: docs/foundation/FOUNDATION_C2_1_MANIFEST.md
REPOSITORY_CLEANUP: COMPLETE
REPOSITORY_REORGANIZATION: COMPLETE / A0-A7 PASS
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
COMMON_EXECUTION_PROMPT: experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md

CURRENT_CODEX_MODEL: CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY
CURRENT_CODEX_SUBMISSION: submission/submission_codex.py
CURRENT_CODEX_SUBMISSION_SHA256: 0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6
CURRENT_CODEX_REACTIVE_SUBMISSION: submission/submission_codex_e17_reactive.py
CURRENT_CODEX_REACTIVE_SUBMISSION_SHA256: 0874EB10F287DC7E6A268CDB64517BAE98E246EB1A124EF9C643A3B7DCE0082C
KAGGLE_SCORE_PRIOR_SNAPSHOT: 1159.9
KAGGLE_POSITION_PRIOR_SNAPSHOT: 2542
KAGGLE_E17_INTERIM_RATING: 996
KAGGLE_E17_ENTRY_RATING: 600
KAGGLE_E17_INTERIM_DELTA: +396
KAGGLE_E17_SCORE_STATUS: STABILIZING_NOT_FINAL
KAGGLE_E17_CONTROL_RATING_SNAPSHOT: 1089.7
KAGGLE_E17_REACTIVE_RATING_SNAPSHOT: 1353.6
KAGGLE_E17_REACTIVE_DELTA: +263.9 (+24.2%)
VISIBLE_TOP3_2026_09_02: Crop_Dusta=2917.8, tetsuya=2890.3, 3정훈=2878.5

NEXT_EXPERIMENT: E17
E17_PHASE: E17.3 6-6-2 TOURNAMENT COMPLETE / HOLDOUT NOT USED
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: CODEX_SERVICE_ROUTING_V3_CONTROL / CODEX_POST_FEED_CAPACITY_BATCHING_V4D_INTERNAL
E17_CROSS_AGENT_REVIEW: CLOSED
E17_STRATEGY_FREEZE: experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_1_AUTHORIZED: YES_BY_POST_FREEZE_OWNER_DECISION
E17_REACTIVE_DESIGN: experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md
E17_REACTIVE_AUTHORIZATION: experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md
E17_REACTIVE_TOURNAMENT: HOLDOUT_BLOCKED_CLAUDE_V2_FAILED_GATES
E17_REACTIVE_PARTICIPANTS: CODEX_V9_FROZEN, CODEX_REACTIVE, CLAUDE_REACTIVE
E17_DEVELOPMENT_EXHIBITION: COMPLETE_42_OF_42_NON_QUALIFYING
E17_EXTERNAL_SUBMISSION: REACTIVE_LIVE_SCORE_STABILIZING
E17_EXTERNAL_RELEASE: CODEX-E17.0-EXTERNAL-CONTROL-V1
E17_KAGGLE_SUBMISSION_ID: 559588638
E17_REACTIVE_KAGGLE_SUBMISSION_ID: 559631298
E17_REACTIVE_EXTERNAL_BENCHMARK: COMPLETE_10_EPISODES_5W_5L
E17_REACTIVE_EXTERNAL_MEAN_MONEY: 78808.7
E17_REACTIVE_ACTION_STREAMS: 1_UNIQUE_OF_10
E17_REACTIVE_STRUCTURAL_TRAJECTORIES: 4_UNIQUE_OF_10
E17_REACTIVE_Q2_VS_Q0_ANIMAL_TILE_DAYS: 63.29%
E17_TRUE_REACTIVITY_PLAN: experiments/e17/design/E17_CODEX_TRUE_REACTIVITY_ACTIVATION_PLAN_V1.md
E17_TRUE_REACTIVITY_V2: DEVELOPMENT_GATES_PASS_NOT_KAGGLE_READY
E17_TRUE_REACTIVITY_RUNS: 48
E17_TRUE_REACTIVITY_INERT_DELTA: +1.55%
E17_TRUE_REACTIVITY_OVERALL_DELTA_VS_V1: -0.26%
E17_TRUE_REACTIVITY_Q2_OUTCOME: FINAL_ANIMALS_8_6_5_UNCHANGED
E17_TRUE_REACTIVITY_REPORT: experiments/e17/reports/codex/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md
E17_SERVICE_ROUTING_PLAN: experiments/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V2.md
E17_SERVICE_ROUTING_V2: SUPERSEDED_INTERNAL_BY_V3_D28
E17_SERVICE_ROUTING_V3: ALL_DEVELOPMENT_GATES_PASS_NOT_KAGGLE_RELEASED
E17_SERVICE_ROUTING_ACTIVATION_DAY: 28
E17_SERVICE_ROUTING_LIQUIDATION_DAY: 29
E17_SERVICE_ROUTING_RUNS: 12
E17_SERVICE_ROUTING_MEAN: 134351.33
E17_SERVICE_ROUTING_CONTROL_MEAN: 134060.17
E17_SERVICE_ROUTING_DELTA: +0.217%
E17_SERVICE_ROUTING_DELTA_VS_V2_D29: +1.82%
E17_SERVICE_ROUTING_UNIT_LEDGER: 3198/3198_CLASSIFIED
E17_SERVICE_ROUTING_MARKET_LEDGER: 78/78_CLASSIFIED
E17_SERVICE_ROUTING_COMMANDS: ROUTING_2256 / SERVICE_752
E17_SERVICE_ROUTING_SAFETY: NON_SELL_VIOLATIONS_0 / ANIMAL_ESCAPES_0
E17_SERVICE_ROUTING_TERMINAL_SELLABLE_RESIDUAL: 0
E17_SERVICE_ROUTING_REPORT: experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md
E17_BATCHED_ROUTING_PLAN: experiments/e17/design/E17_CODEX_BATCHED_CLUSTER_ROUTING_PLAN_V1.md
E17_BATCHED_ROUTING_V4A: REJECTED_REWARD_MINUS_2.529%
E17_CLUSTERED_ROUTING_V4B: REJECTED_NO_LOGISTIC_GAIN
E17_CAPACITY_ROUTING_V4C: REJECTED_TRIGGER_BLOCKED_BY_WHEAT_GUARD
E17_POST_FEED_CAPACITY_V4D: ALL_DEVELOPMENT_GATES_PASS_NOT_KAGGLE_RELEASED
E17_V4D_RUNS: 12
E17_V4D_MEAN: 135096.83
E17_V4D_CONTROL_MEAN: 134351.33
E17_V4D_DELTA: +0.555%
E17_V4D_MIN_MATCHED_DELTA: +497
E17_V4D_MOVE_PER_SERVICE: 2.872
E17_V4D_LEDGER: UNIT_3198/3198 / MARKET_71/71
E17_V4D_SAFETY: ERRORS_0 / ESCAPES_0 / TERMINAL_RESIDUAL_0
E17_V4D_REPORT: experiments/e17/reports/codex/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md
E17_V4D_MARKET_STRESS: PASS_48_OF_48 / D27_ADMITTED
E17_V4D_MARKET_STRESS_MATCHED: 24_OF_24_NONNEGATIVE
E17_V4D_MARKET_STRESS_MEAN: 124090.17
E17_V4D_MARKET_STRESS_CONTROL_MEAN: 123199.54
E17_V4D_MARKET_STRESS_DELTA: +0.723%
E17_V4D_MARKET_STRESS_WORST_REGIME: INERT_+0.555%
E17_V4D_MARKET_STRESS_MOVE_PER_SERVICE: 2.922_VS_2.967
E17_V4D_MARKET_STRESS_REPORT: experiments/e17/reports/codex/E17_CODEX_V4D_CONTROLLED_MARKET_STRESS_REPORT_IT.md
E17_D27_HANDOFF_ABLATION: FAIL_REWARD / V4D_D28_RETAINED
E17_D27_RUNS: 12
E17_D27_MEAN: 133290.33
E17_D27_CONTROL_MEAN: 135096.83
E17_D27_DELTA: -1.337%
E17_D27_MATCHED_NONNEGATIVE: 0/6
E17_D27_MOVE_PER_SERVICE: 2.605_VS_2.872
E17_D27_CAUSAL_DIAGNOSIS: ONE_FEWER_Q0_CROP_IN_6/6
E17_D27_REPORT: experiments/e17/reports/codex/E17_CODEX_D27_HANDOFF_ABLATION_REPORT_IT.md
E17_V4D_KAGGLE_RELEASE: READY_FOR_OWNER_UPLOAD
E17_V4D_SUBMISSION: submission/submission_codex_e17_v4d.py
E17_V4D_SUBMISSION_SHA256: 2792244CA71115E6CAAFDFC942B6D9AAAF09B95FC717A5B182D07A31D9717CD7
E17_V4D_SUBMISSION_PARITY: 4314/4314
E17_V4D_KAGGLE_UPLOAD: NOT_YET_RECORDED
E17_V4D_RELEASE_REPORT: experiments/e17/reports/codex/E17_CODEX_V4D_KAGGLE_SUBMISSION_READINESS_REPORT_IT.md
E17_662_MODEL: CODEX-E17.3-TOPOLOGY-FILL-662-V2
E17_662_SUBMISSION: submission/submission_codex_e17_topology_662.py
E17_662_SUBMISSION_SHA256: 3DF5C15D078552AF0A3849653057303698C9D750B4C7BB087B8A29092FADBAE8
E17_662_TOPOLOGY: Q0_6 / Q1_6 / Q2_2 / FILLED_14_OF_14
E17_662_KAGGLE_UPLOAD: OWNER_ACTION_REPORTED / SUBMISSION_ID_NOT_RECORDED
E17_THREE_AGENT_TOURNAMENT: COMPLETE_42_OF_42_DEVELOPMENT_NON_QUALIFYING
E17_THREE_AGENT_STANDINGS: CODEX_28_0_0 / CLAUDE_14_14_0 / COPILOT_0_28_0
E17_THREE_AGENT_MEAN_MONEY: CODEX_123620.29 / CLAUDE_15511.21 / COPILOT_10537.18
E17_THREE_AGENT_REPORT: experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md
ACTIVE_DEVELOPMENT_AGENTS: CODEX, CLAUDE, COPILOT
CODEX_REACTIVE_STATUS: FROZEN_FOR_REACTIVE_TOURNAMENT
CODEX_REACTIVE_DEVELOPMENT_MEAN: 139420.2857
CODEX_REACTIVE_DELTA_VS_V9: 0
CLAUDE_REACTIVE_STATUS: V1_REJECTED / V2_FROZEN_WITH_FAILED_GATES
CLAUDE_ACTIVATION_AUDIT: PASS_WITH_LOCAL_CLEANUP
CLAUDE_ROOT_BOOTSTRAP: REMOVED
CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK: AUTHORIZED_DEVELOPMENT_ONLY
CLAUDE_V3_IMPLEMENTATION: COMPLETE_FROZEN_WITH_FAILED_GATES
CLAUDE_V3_10X_PROMPT: experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_V3_10X_ACTIVATION_PROMPT_IT.md
REPLAY_JSON_ROOT: data/replays/json
REPLAY_JSON_CATALOG: data/replays/json/json.md
E17_RAW_CODEX_DEV_AND_CLAUDE_V1: REMOVED_REPRODUCIBLE
CLAUDE_V2_RAW: LOCAL_ONLY_GITIGNORED_RETAINED
ANTIGRAVITY_STATUS: OWNER_UNAVAILABLE_UNTIL_2026_09_04 / EXCLUDED_FROM_E17_3_TOURNAMENT
COPILOT_STATUS: E17_0_NATIVE_INCLUDED_IN_DEVELOPMENT_TOURNAMENT / NO_POLICY_MUTATION
NEW_KAGGLE_SUBMISSION: E17_662_OWNER_ACTION_REPORTED / ID_AND_SCORE_PENDING
NEXT_ACTION: RECORD_E17_662_KAGGLE_ID_AND_SCORE / RUN_ONE_FACTOR_DEVELOPMENT_ABLATIONS
```

## Stato raggiunto

E17.3 introduce la candidata Codex 6-6-2: 14 pascoli target costruiti e
riempiti, cinque celle recuperate a crop, zero breach Q2, zero fughe ed esatto
cap strutturale `6-6-2`. La submission standalone è pronta; il proprietario ha
segnalato l'azione Kaggle, ma ID e score non sono ancora registrati.

Il torneo development Codex/Claude/Copilot è completo: 42 match, sette seed
development e due seat, senza holdout/final. Classifica: Codex `28-0-0`, Claude
`14-14-0`, Copilot `0-28-0`. Antigravity è escluso fino al 2026-09-04. La
prossima sessione deve registrare l'esito Kaggle 6-6-2 e trasformare i punti di
miglioramento del report in ablation a una sola variabile.

La Foundation C2.1 e il riordino del repository sono chiusi con gate A7
`PASS`. La strategia E17 è stata riconciliata e congelata dopo tre review
indipendenti. E17.0 è completo per Codex, Antigravity e Copilot. Una decisione
successiva del proprietario autorizza ora E17.1, con Codex V9 congelata come
controllo, Codex reattivo come evoluzione derivativa e Claude reattivo come
policy indipendente. Antigravity e Copilot restano congelati. Codex V9 resta la
baseline e la submission Kaggle correnti. Il benchmark discovery E17 è stato
completato su nove replay unici dei tre player che occupavano il Top 3 nello
snapshot di raccolta (`tetsuya`, `OceanMix`, `Crop Dusta`), con 18 player-seat
e 720 step per episodio.

La review cross-agent è formalmente chiusa:

- Copilot: `ACCEPT_WITH_CHANGES`;
- Antigravity: `ACCEPT`;
- audit fughe Crop Dusta: 31/31 eventi compatibili con fuga secondo criterio
  EOD stretto, classificati `DERIVED`;
- nessuna policy è stata modificata durante benchmark e review.

L'audit successivo dell'attivazione Claude è
`PASS_WITH_LOCAL_CLEANUP`: tutte le scritture sono rimaste nei namespace
assegnati, non risultano letture dei sorgenti strategici altrui, import
proibiti, uso dei seed riservati o mutazioni Git. Il bootstrap locale
`CLAUDE.md` è stato rimosso; i prompt puntano ora ai documenti canonici. I
replay grezzi sono consolidati nella cartella unica `data/replays/json/` e
catalogati in `json.md`. I ledger Codex development e Claude V1, riproducibili
e già sintetizzati, sono stati rimossi; i ledger Claude V2 restano disponibili
localmente per la remediation V3 e sono esclusi da Git.

Il benchmark esterno della probe reattiva è completo su dieci replay della
submission Kaggle `559631298`: 5W-5L, denaro medio `78.808,7`, zero fughe e
3Q in 10/10. La policy ha emesso una sola sequenza completa di comandi nei
dieci episodi, mentre lo stato strutturale eseguito presenta quattro hash:
nel campione le guardie reattive non hanno quindi prodotto una divergenza
osservabile dell'action stream. La quota Q2 è il `63,29%` degli
animal-tile-days Q0 tra sblocco Q2 e D28, intermedia fra tetsuya (`75,38%`),
Crop Dusta (`38,17%`) e OceanMix (`0%`). La quota Q2 è diventata un outcome,
non il trattamento. Il controller `MARKET_REGIME_ADAPTATION` V2 è stato
verificato su 48 episodi development: +1,55% sul controllo inerte,
action-stream discriminanti, 100% di override tracciati, zero errori e zero
fughe. La composizione animale Q0/Q1/Q2 resta 8/6/5: il solo timing
commerciale non rende ancora reattiva la struttura. I replay esterni restano
diagnostici e holdout/final confirmation non sono stati usati. Report:
`experiments/e17/reports/codex/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md`.

Il passo successivo è stato eseguito con
`REACTIVE_SERVICE_AND_ROUTING_CORE_V2`. Il core ricostruisce dallo stato
osservato task di servizio e percorsi, senza cambiare il blocco market. Un
override locale della routine è stato respinto perché i suoi `PASS` sono
anche punti impliciti di sincronizzazione; la soluzione promossa usa un
handoff progressivo al giorno 29. Su 12 episodi development matched ottiene
`131.947,17` contro `134.060,17` (`−1,576%`), genera 750 comandi di routing e
252 servizi, classifica tutti i 1.434 record del ledger e mantiene a zero
errori, mutazioni market e fughe. È una prova architetturale, non una
submission. Il prossimo test è anticipare l'handoff a D28 coordinando
raccolta, deposito e liquidazione terminale. Report:
`experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_DEVELOPMENT_REPORT_IT.md`.

La V3 ha completato il passaggio a D28: FEED e WATER preparano l'ultimo ciclo,
gli output vengono depositati senza serializzare artificialmente gli accessi
shed e D29 coordina DROP e SELL nello stesso batch. Nei 12 episodi matched la
media è `134.351,33` contro `134.060,17` (`+0,217%`), ossia circa `+1,82%`
rispetto alla V2 D29. Il residuo vendibile terminale è zero, con zero fughe,
errori e violazioni market. Holdout e final confirmation restano intatti e la
V3 non è una submission. La prossima sessione deve mantenere D28, introdurre
routing per cluster e rientri basati su inventario/slack, e tentare D27 solo
dopo avere preservato score, sicurezza e liquidazione completa. Report:
`experiments/e17/reports/codex/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md`.

Il trattamento logistico è stato poi scomposto causalmente. V4A riduce i MOVE
ma perde `2,529%` per overflow EOD dello shed; V4B mostra che l'affinità di
quadrante non aggiunge efficienza; V4C rileva la pressione di capacità ma la
guardia Wheat impedisce il flush. V4D rilascia i carrier soltanto dopo il feed
completo e supera tutti i gate: `135.096,83` contro `134.351,33` (`+0,555%`),
delta positivo in 6/6 confronti, `MOVE/service = 2,872`, zero fughe, errori e
residui terminali. È la candidata interna corrente, non una submission. La
prossima sessione deve stressare V4D nei regimi market development già
controllati prima di valutare D27. Report:
`experiments/e17/reports/codex/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md`.

## Evidenza E17 consolidata

I nove replay mostrano tre archetipi diversi, tutti 3Q NW→NE→SW e senza Q3:

| Profilo | Q1 | Q2 | Topologia | MOVE/produttive | Rischio terminale |
|---|---|---|---|---:|---|
| `tetsuya` | D7 | D10 | bestiame distribuito, Q1 crop-dense | 1,2553 | 0 fughe, inventario 0 |
| `OceanMix` | D6 | D11 | livestock Q0/Q1, Q2 crop-only | 1,0468 | 0 fughe |
| `Crop Dusta` | D5–D6 | D8–D9 | tre quadranti misti e dispersi | 1,4267 | 31 fughe derivate |

Questi dati supportano il 3Q e il picco di 12 hands come baseline di lavoro,
non come ottimi globali. Non identificano causalmente il vantaggio di D10,
della topologia compatta o della diversificazione. Rating Kaggle, denaro finale
dei replay e score dei runner locali restano metriche diverse.

Lo snapshot leaderboard del 2026-09-02 cambia l'ordine: `Crop Dusta` è primo
con 2.917,8, `tetsuya` secondo con 2.890,3 e `3정훈` terzo con 2.878,5;
`OceanMix` non compare nei primi sette visibili. Il benchmark resta valido
come confronto di tre archetipi, ma non va più chiamato fotografia del Top 3
corrente. La leadership di Crop Dusta rende obbligatorio mantenere in E17 una
frontiera di espansione precoce/diversificata; non annulla però le 31 fughe
derivate né autorizza a saltare ledger e vincoli di serviceability.

## Strategia E17 congelata

Il draft iniziale resta disponibile come provenance; il riferimento normativo
corrente è:

`experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`

Principio cardine: **E17 non deve convergere a priori verso un singolo
archetipo**. `tetsuya`, `OceanMix` e `Crop Dusta` sono tre combinazioni
osservate di fattori. Timing, topologia, densità, capitale, specie e chiusura
devono essere separati e testati causalmente. Solo dopo la misura degli effetti
principali sono ammessi test di interazione e una candidata composita.

La sequenza condivisa è:

1. `E17.0` — ledger requested/executed a parità comportamentale;
2. `E17.1` — singola guardia fill-aware sul mercato WHEAT;
3. `E17.2` — contrasto topologico distribuito vs livestock compatto Q0/Q1;
4. `E17.3` — anticipo isolato di Q2 da D11 a D10;
5. `E17.4` — liquidazione terminale reattiva;
6. `E17.5` — diversificazione di una sola specie per esperimento;
7. `E17.6` — checkpoint obbligatorio della frontiera Q2 D8, soltanto con zero
   fughe e serviceability provata.

Le linee minime da confrontare includono:

- timing Q2 `D11 / D10 / D8`;
- livestock `distribuito / compatto Q0-Q1 / misto nei tre quadranti`;
- diversificazione crop `3 / 4 / 5 specie`;
- diversificazione animale `2 / 3 specie`;
- reinvestimento aggressivo vs riserva di liquidità;
- liquidazione e servicing terminale reattivi vs schedule fisso.

E17.0 ha aggiunto il ledger comune `E17_LEDGER_V1` fuori dal decision path.
Codex ha dimostrato parità `4314/4314`, outcome e stato terminale `6/6`, senza
modificare la V9. Antigravity e Copilot hanno eliminato la dipendenza dalle
routine Codex e costruito baseline native con audit locale d'indipendenza
`PASS`. Tutti i ledger hanno record coverage del 100%, zero errori tecnici e
zero fughe EOD derivate.

Il PASS è tecnico, non competitivo. Antigravity attiva tre quadranti ma
consuma tutto il capitale iniziale (`max_hands=0`, reward 0 in 6/6); Copilot è
produttiva ma ottiene mean 8.941,5 contro opponent inert. Codex V9 ottiene mean
132.019,3 sulla stessa matrice development. Al termine di E17.0 queste
differenze non autorizzavano una promozione; il nuovo torneo è autorizzato da
un decision record successivo e non modifica retroattivamente quel verdetto.

## Prossima azione operativa

1. mantenere congelati V9 e Codex reattivo V1 come controlli e submission
   correnti;
2. conservare market-reactive V2 e service-routing core V2 come prove
   development, senza submission;
3. anticipare il solo handoff del core da D29 a D28, rendendo efficiente e
   verificabile la catena raccolta→shed→liquidazione;
4. misurare separatamente `MOVE/service`, output raccolto e output realmente
   monetizzato prima di anticipare ulteriormente l'handoff;
5. mantenere acquisition/placement e quota allevamento Q2 fuori dalla prossima
   mutazione: resteranno outcome finché il routing non ripianificherà in modo
   economicamente equivalente le dipendenze strutturali;
6. non consumare holdout o final confirmation e mantenere Claude V3 congelata
   con gate falliti; Antigravity e Copilot restano congelati;
7. usare metriche separate per seed, seat e regime, senza selezionare una
   candidata dalla sola media complessiva.

Antigravity e Copilot non vengono modificati e non partecipano al torneo.
La submission reattiva è stata autorizzata e caricata dal proprietario come
probe esterna separata; ulteriori submission richiedono una nuova decisione.

## Esibizione reattiva development a tre

La matrice seat-balanced sui sette seed development è completa: 42/42 match,
zero errori. Codex V9 e Codex reattivo sono primi ex aequo con `15-12-1`,
media 112.149,21, zero fughe e delta diretto medio zero. Claude V2 chiude
`0-0-28`, media 11.777,64, due fughe e MOVE/produttive 2,9719. In ogni match
competitivo Claude ha comunque raggiunto 3Q. Nessun override Codex è scattato,
quindi il vantaggio Kaggle non è riprodotto dalla matrice locale corrente.

Report:
`experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`.

## Confronto esterno E17

Antigravity non è disponibile per esaurimento dei crediti. Il proprietario ha
quindi escluso il torneo locale incompleto e autorizzato una submission E17
per confronto esterno. La candidate mantiene le azioni V9 con soli metadati
di release aggiornati ed è identificata come controllo
`CODEX-E17.0-EXTERNAL-CONTROL-V1`. La submission Kaggle `559588638` è attiva:
la rilevazione più recente fornita dal proprietario è `996`, dopo un ingresso
a `600` (`+396`), con un episodio ancora in corso nello snapshot. È evidenza
osservata ma non ancora un rating stabile né uno score conclusivo. Il report è
in
`experiments/e17/reports/codex/E17_EXTERNAL_SUBMISSION_READINESS_REPORT_IT.md`.

## Gate E17 finali proposti

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR >= 90000
ANIMAL_ESCAPES == 0
MOVE_PER_PRODUCTIVE <= 1.20
EXECUTED_MARKET_LEDGER_COVERAGE == 100%
STRATEGIC_INDEPENDENCE_GATE == PASS  # per il prossimo torneo a tre
```

## Vincoli inderogabili

- nessun agente può importare o copiare routine, action table, planner,
  dispatcher o schedule di un altro;
- Foundation, replay discovery, schema del ledger e protocollo di benchmark
  possono essere condivisi;
- ogni variazione strategica deve modificare una sola famiglia causale;
- i nove replay Top 3 sono dati offline di discovery, mai input online;
- distinguere sempre `requested`, `executed`, `DERIVED` e `UNKNOWN`;
- nessuna submission Kaggle prima del superamento dei gate preregistrati,
  salvo autorizzazione esplicita del proprietario per un controllo esterno
  dichiarato e senza mutazione di policy.

## Documenti da leggere

- `docs/PROJECT_STATE.md`;
- `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md`;
- `docs/repository/REPOSITORY_ARCHITECTURE.md`;
- `docs/repository/migration/POST_E17_EXTERNAL_RELEASE_CLEANUP.md`;
- `experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`;
- `experiments/e17/reviews/common/E17_STRATEGY_RECONCILIATION.md`;
- `experiments/e17/reports/common/E17_0_GATE_AND_BLOCKER_SUMMARY.md`;
- `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`;
- `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`;
- `experiments/e17/reports/codex/E17_TOP3_REPLAY_ANALYSIS.md`;
- `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`;
- `docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`;
- `docs/model_specs/codex/CODEX_V9_E17_RUNTIME_AND_FOUNDATION_MAPPING_IT.md`;
- `experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`;
- `experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`;
- `experiments/e17/prompts/claude/E17_CLAUDE_REACTIVE_3Q_INDEPENDENT_BUILD_PROMPT.md`;
- `experiments/e17/reviews/common/E17_CLAUDE_ACTIVATION_COMPLIANCE_AND_CLEANUP_AUDIT.md`;
- `experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`;
- `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md`.
