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
E17_PHASE: E17.1 DEVELOPMENT EXHIBITION COMPLETE / OFFICIAL HOLDOUT BLOCKED
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: CODEX_REACTIVE_FROZEN / CLAUDE_V2_FAILED_GATES
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
ACTIVE_DEVELOPMENT_AGENTS: CODEX, CLAUDE
CODEX_REACTIVE_STATUS: FROZEN_FOR_REACTIVE_TOURNAMENT
CODEX_REACTIVE_DEVELOPMENT_MEAN: 139420.2857
CODEX_REACTIVE_DELTA_VS_V9: 0
CLAUDE_REACTIVE_STATUS: V1_REJECTED / V2_FROZEN_WITH_FAILED_GATES
CLAUDE_ACTIVATION_AUDIT: PASS_WITH_LOCAL_CLEANUP
CLAUDE_ROOT_BOOTSTRAP: REMOVED
CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK: AUTHORIZED_DEVELOPMENT_ONLY
CLAUDE_V3_IMPLEMENTATION: NOT_STARTED
E17_RAW_V1_V2_RUNS: LOCAL_ONLY_GITIGNORED
ANTIGRAVITY_STATUS: FROZEN_EXCLUDED_FROM_REACTIVE_TOURNAMENT
COPILOT_STATUS: FROZEN_EXCLUDED_FROM_REACTIVE_TOURNAMENT
NEW_KAGGLE_SUBMISSION: REACTIVE_PROBE_UPLOADED_BY_OWNER
NEXT_ACTION: BENCHMARK_KAGGLE_REACTIVE_RESULTS
```

## Stato raggiunto

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
ledger grezzi V1/V2 e Codex development restano disponibili localmente per
l'analisi forense, ma sono esclusi da Git per non appesantire il repository.

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

1. mantenere congelati Codex V9 e Codex E17.1 reattivo;
2. analizzare i replay Kaggle del reattivo per collegare il delta esterno
   `1353,6 - 1089,7` ai trigger Wheat/feed effettivamente osservati;
3. non consumare l'holdout: Claude V2 resta esclusa per media 14.445,29, tre
   fughe passive e 3Q in 13/14 run;
4. sviluppare, in una sessione successiva, una Claude V3 indipendente che
   riduca movimento/retry, aumenti densità produttiva e workforce e superi
   tutti i gate development; Claude può usare le candidate Codex congelate
   come soli avversari black-box, senza leggere o importare i loro sorgenti;
5. ripetere audit e freeze Claude prima di autorizzare il torneo holdout;
6. conservare l'esibizione development 42/42 come diagnosi, non come selezione
   ufficiale.

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
