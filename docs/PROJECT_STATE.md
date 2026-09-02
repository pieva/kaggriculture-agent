# PROJECT_STATE — Kaggriculture

## Stato corrente

```text
PROJECT: Kaggriculture
STATUS_DATE: 2026-09-02
PHASE: FOUNDATION C2.1 CLOSED / E17.1 DEVELOPMENT EXHIBITION COMPLETE

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
E17_PHASE: E17.1 DEVELOPMENT EXHIBITION COMPLETE / OFFICIAL HOLDOUT BLOCKED
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: CODEX_REACTIVE_FROZEN / CLAUDE_V2_FAILED_GATES
E17_DISCOVERY_BENCHMARK: COMPLETE
E17_CROSS_AGENT_REVIEW: CLOSED
E17_STRATEGY_DRAFT: experiments/e17/design/E17_STRATEGY_DRAFT_V0_1.md
E17_STRATEGY_FROZEN: experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
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

## Evidenza Kaggle esterna corrente

Snapshot Codex del 2026-09-01 e leaderboard aggiornata fornita dall'utente il
2026-09-02:

| Indicatore | Valore |
|---|---:|
| Codex V9 3Q | `1159,9` — snapshot precedente, non visibile nella schermata aggiornata |
| Codex E17 external control | `996` — rilevazione intermedia, ingresso a `600`, non stabilizzata |
| Codex E17.0 / V9 — snapshot successivo | `1089,7` |
| Codex E17.1 reattivo — snapshot | `1353,6` |
| Delta reattivo vs controllo nello snapshot | `+263,9` (`+24,2%`) |
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
contiene la candidate canonica Codex E17.0 e la probe reattiva E17.1 separata;
le precedenti non sono state sovrascritte.

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
è chiusa ed E17.0 è stato eseguito. Il successivo decision record
`experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`
autorizza prospetticamente E17.1 e il protocollo
`experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`, lasciando
immutato il freeze storico.

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
ma molto sotto la V9 Codex contro opponent inert. Antigravity e Copilot sono
ora congelati e non verranno sottoposti nel nuovo torneo. Il decision record
successivo autorizza lo sviluppo Codex/Claude reattivo e il torneo a tre dopo
il freeze di entrambe le candidate; il rating esterno Codex continua a essere
registrato separatamente.

## Confronto esterno E17 autorizzato

Antigravity non è disponibile per esaurimento dei crediti; il precedente
torneo fra Codex, Antigravity e Copilot è stato pertanto omesso. È stata
caricata la release
`CODEX-E17.0-EXTERNAL-CONTROL-V1`, basata sul file canonico
`submission/submission_codex.py`, SHA-256
`0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`.

La release cambia soltanto i metadati del wrapper e mantiene parità
comportamentale con la V9: non promette un incremento sistematico rispetto al
precedente score Kaggle `1159,9`, ma misura la ripetibilità esterna dopo il
riordino e la chiusura del gate E17.0. Manifest e report sono in:

- `experiments/e17/artifacts/freeze/codex/E17_EXTERNAL_SUBMISSION_MANIFEST.json`;
- `experiments/e17/reports/codex/E17_EXTERNAL_SUBMISSION_READINESS_REPORT_IT.md`.

La submission Kaggle `559588638` ha raggiunto prima la rilevazione intermedia
`996` da `600` (`+396`) e successivamente `1089,7`. La probe E17.1 reattiva ha
raggiunto `1353,6`, pari a `+263,9` (`+24,2%`) rispetto al controllo nello
snapshot fornito. I rating restano in assestamento e non costituiscono un test
matched-pair. Una decisione successiva del proprietario ha avviato E17.1 con
un nuovo torneo fra V9, Codex reattivo e Claude reattivo. Codex reattivo ha
superato il development gate su 14 run con media 139.420,29, delta zero dalla
V9, zero errori, zero fughe e 3Q in ogni run. Claude V1 è stata respinta con
media 9.201,71 e otto fughe derivate; la V2 è indipendente e tecnicamente
valida, ma congelata con gate economico, fughe e copertura 3Q falliti. I seed
holdout e final confirmation restano non consumati.

## Esibizione E17.1 reattiva a tre

Claude V2 ha concluso con indipendenza, test, lint e provenance `PASS`, ma il
freeze è `FROZEN_WITH_FAILED_GATES`: media passiva 14.445,29, tre fughe EOD e
3Q in 13/14 run. Per questo il torneo ufficiale non è stato eseguito.

È stata invece completata un'esibizione non qualificante sui sette seed
development già consumati: 42 match seat-balanced. Codex V9 e Codex reattivo
chiudono entrambi `15-12-1`, media 112.149,21, zero fughe e delta diretto medio
zero; Claude V2 chiude `0-0-28`, media 11.777,64 e due fughe. Claude raggiunge
3Q in 28/28 match competitivi, ma il rapporto MOVE/produttive 2,9719 e la
bassa densità terminale spiegano il divario. Nessuna guardia Codex è scattata
nel campione locale.

Il report canonico è
`experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`.
I sei seed holdout e i quattro final-confirmation restano non consumati.

## Audit Claude e preparazione V3

L'audit post-attivazione Claude è `PASS_WITH_LOCAL_CLEANUP`: tutte le
scritture sono rimaste negli spazi agent-local e E17 autorizzati; non sono
state rilevate letture dei sorgenti strategici altrui, import proibiti,
scritture nella submission, comandi Git mutanti o uso dei seed holdout/final.
Il bootstrap locale `CLAUDE.md` è stato rimosso e `.claude/` è esclusa dalla
versione. I ledger grezzi riproducibili di E17.1 restano locali e gitignored;
metriche compatte, freeze, report, runner e test restano versionati.

Per la futura Claude V3 è autorizzato il confronto con Codex V9 e Codex
reattivo esclusivamente come avversari black-box sui seed development. Claude
può osservare esiti e metriche del contratto di gioco, ma non leggere,
analizzare, copiare o importare sorgenti, config, routine o MODEL_SPEC Codex.
L'autorizzazione non avvia la V3 e non sblocca holdout, final confirmation o
submission Kaggle. La prossima attività comune è il benchmark dei risultati
Kaggle della probe Codex reattiva.
