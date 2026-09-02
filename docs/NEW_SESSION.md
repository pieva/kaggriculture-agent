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
KAGGLE_SCORE_PRIOR_SNAPSHOT: 1159.9
KAGGLE_POSITION_PRIOR_SNAPSHOT: 2542
KAGGLE_E17_INTERIM_RATING: 996
KAGGLE_E17_ENTRY_RATING: 600
KAGGLE_E17_INTERIM_DELTA: +396
KAGGLE_E17_SCORE_STATUS: STABILIZING_NOT_FINAL
VISIBLE_TOP3_2026_09_02: Crop_Dusta=2917.8, tetsuya=2890.3, 3정훈=2878.5

NEXT_EXPERIMENT: E17
E17_PHASE: E17.0 COMPLETE / STOP BEFORE E17.1
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: NOT_STARTED
E17_CROSS_AGENT_REVIEW: CLOSED
E17_STRATEGY_FREEZE: experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_1_AUTHORIZED: NO
E17_EXTERNAL_SUBMISSION: LIVE_SCORE_STABILIZING
E17_EXTERNAL_RELEASE: CODEX-E17.0-EXTERNAL-CONTROL-V1
E17_KAGGLE_SUBMISSION_ID: 559588638
ACTIVE_DEVELOPMENT_AGENT: CODEX_ONLY
ANTIGRAVITY_STATUS: PAUSED_CREDIT_EXHAUSTION
COPILOT_E17_NATIVE: PRESERVED_LOCAL_ONLY_NO_KAGGLE_SUBMISSION
LOCAL_TOURNAMENTS: SKIPPED_WHILE_ANTIGRAVITY_UNAVAILABLE
```

## Stato raggiunto

La Foundation C2.1 e il riordino del repository sono chiusi con gate A7
`PASS`. La strategia E17 è stata riconciliata e congelata dopo tre review
indipendenti. E17.0 è completo per Codex, Antigravity e Copilot; il lavoro è
fermato prima di E17.1 come richiesto. Codex V9 resta la baseline e la
submission Kaggle correnti. Il benchmark discovery E17 è stato
completato su nove replay unici dei tre player che occupavano il Top 3 nello
snapshot di raccolta (`tetsuya`, `OceanMix`, `Crop Dusta`), con 18 player-seat
e 720 step per episodio.

La review cross-agent è formalmente chiusa:

- Copilot: `ACCEPT_WITH_CHANGES`;
- Antigravity: `ACCEPT`;
- audit fughe Crop Dusta: 31/31 eventi compatibili con fuga secondo criterio
  EOD stretto, classificati `DERIVED`;
- nessuna policy è stata modificata durante benchmark e review.

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
132.019,3 sulla stessa matrice development. Queste differenze non autorizzano
una promozione o un torneo: definiscono la readiness da riconciliare.

## Prossima azione operativa

1. attendere che il rating della submission E17 si stabilizzi, senza usare la
   rilevazione intermedia `996` come risultato finale;
2. registrare rating stabile, numero di episodi ed eventuale dispersione degli
   outcome rispetto al precedente riferimento V9 `1159,9`;
3. scegliere una sola famiglia causale E17 sulla base del confronto esterno e
   del ledger già raccolto;
4. autorizzare E17.1 o una diversa ablation soltanto dopo questa decisione.

Non implementare ancora guardie di mercato, nuovi layout, timing D10 o mix
produttivi. Copilot ha prodotto la propria versione nativa ma non verrà
sottomessa; Antigravity è in pausa. Finché il confronto esterno non è stabile,
non si eseguono tornei locali incompleti né si promuovono nuove policy.

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
- `docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`.
