# E18 — opponent-reactive 6-6-2 / 7-7-0 toward Top-3 behavior

## E18.4 Codex — state-driven 7-7-2 V1

La prima implementazione con handoff completo D11 è congelata come
`REJECTED_AT_DEVELOPMENT_ECONOMIC_GATE`. In 14 match contro E18.2 ottiene
topologia esatta e fill 16/16 in 14/14, senza fughe o errori, ma chiude a
55.940 money medio contro 83.095,7 (-32,68%). La superficie colturale tardiva
è preservata (95,23% del controllo), mentre il dispatcher produce +29,35% di
movimenti e -20,95% di azioni produttive. Nessun upload Kaggle.

- report: `reports/codex/E18_4_STATE_DRIVEN_772_DEV_GATE_REPORT_IT.md`
- artifact: `artifacts/derived/codex/E18_4_STATE_DRIVEN_772_DEV_GATE_V1.json`
- model spec: `../../docs/model_specs/codex/MODEL_SPEC_CODEX_E18_4_STATE_DRIVEN_772_V1.md`
- prossimo gate: località per cluster e task aging, senza modificare market o
  topologia.

## Status

```text
PHASE: OPEN / E18.4_V1_STATE_DRIVEN_772_REJECTED / V2_LOCALITY_GATE_PENDING
ECONOMIC_CONTROL: CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28
CANDIDATE: CODEX-E18.4-STATE-DRIVEN-772-V1 / REJECTED_NO_UPLOAD
OBJECTIVE: LOCALITY_AWARE_STATE_DRIVEN_772_WITH_PRODUCTIVE_ACTION_PARITY
OPENING_REPLAY: 105080066 / ANALYZED / E18_TRAINING_EVIDENCE
OPENING_DIAGNOSIS: CROP_LIFECYCLE_SERVICE_AND_HARVEST_CADENCE_GAP
TOP3_LIVE_2026_09_03: CROP_DUSTA / 3정훈 / SBOL_BALL
TOP3_LIVE_CORPUS: 8_REPLAYS / BOTH_SEATS_PER_AGENT / ACQUIRED_AND_ANALYZED
CODEX_EXTERNAL_REACTIVITY: FAIL_1_OF_3_UNIQUE_LIFECYCLE_PROFILES
TOP3_EXTERNAL_REACTIVITY: 8_OF_8_UNIQUE_LIFECYCLE_PROFILES / 5_TOPOLOGIES
TOP3_Q2_PASTURES: ZERO_IN_7_OF_8 / RANGE_7-0-0_TO_10-7-0_AND_8-4-3
OPPONENT_SIGNAL: PUBLIC_FARM_OBSERVABLE / RATING_AND_CROSS_EPISODE_HISTORY_UNAVAILABLE
HARVEST_OUTPUT: CODEX_586 / TOP3_MEAN_872.5 / DELTA_+48.9_PERCENT
TARGET_MONEY: 100000
BASELINE_MONEY_VS_CLAUDE: 132217.68
BASELINE_MONEY_SYMMETRIC_662: 79323.86
BASELINE_SELFPLAY_GAP: 20676.14
BASELINE_REACTIVITY: FAIL_28_OF_28_ACTION_COUNT_PROFILES_IDENTICAL_V3_V2
BASELINE_SAFETY: 14_OF_14 / Q2_2 / ESCAPES_0 / BREACHES_0
HOLDOUT: NOT_CONSUMED / NOT_AUTHORIZED
FINAL_CONFIRMATION: NOT_CONSUMED / NOT_AUTHORIZED
LOCAL_TOURNAMENT: PASS_56_OF_56 / ARCHITECTURE_GATE_PASS_10_OF_10
DYNAMIC_TOPOLOGY: CLAUDE_AND_CONTROL_662 / COPILOT_770
CONDITIONED_DIVERGENCE: ACTION_14_OF_14 / TOPOLOGY_14_OF_14
LOCAL_MONEY: OVERALL_111654.45 / VS_662_80456.43 / VS_CLAUDE_127072.71 / VS_COPILOT_127434.21
SAFETY: 14_OF_14 / VERIFIED_LOSSES_0 / ERRORS_0 / FALLBACKS_0 / BREACHES_0
SUBMISSION: submission/submission_codex_e18_opponent_reactive_662_770.py
SUBMISSION_ROLE: EXTERNAL_DIAGNOSTIC_NOT_BASELINE_REPLACEMENT
KAGGLE_STATUS: COMPLETE_2026_09_03 / E18.1_825.4 / V4D_1131.7 / DELTA_-27.07_PERCENT
REPLAY_CACHE: RAW_JSON_0 / CATALOG_AND_DERIVED_EVIDENCE_RETAINED
FOUR_AGENT_TOURNAMENT: COMPLETE_84_OF_84 / SIX_PAIRS / BOTH_SEATS
FOUR_AGENT_RESULT: CODEX_42-0 / CLAUDE_26-16 / COPILOT_16-26 / ANTIGRAVITY_0-42
FOUR_AGENT_MONEY: CODEX_125983.74 / CLAUDE_6467.48 / COPILOT_2840 / ANTIGRAVITY_0
FOUR_AGENT_PROMOTION: NONE / ALL_FAIL_AT_LEAST_ONE_GATE
ANTIGRAVITY_ROUNDS: 42 / 14_PER_OPPONENT / P0_21 / P1_21
KAGGLE_MONITOR_RULE: HOURLY / 4_VALID_SNAPSHOTS_OVER_3H / SCORE_RANGE_LT_50
KAGGLE_MONITOR_STATUS: PROTOCOL_READY_NOT_SCHEDULED / BROWSER_SNAPSHOT_BLOCKED
LATEST_VS_V4D_DIRECT: 0-14 / 71831.00_VS_89760.57 / DELTA_-19.97_PERCENT
LATEST_VS_V4D_COMMON_POOL: 125983.74_VS_143486.45 / DELTA_-12.20_PERCENT
LATEST_VS_V4D_DIAGNOSIS: PRODUCTIVE_-6.11_PERCENT / PASS_+24.77_PERCENT / WEED_TILE_DAYS_+320_PERCENT
ECONOMIC_CONTROL: E17_V4D_RESTORED / E18.1_ARCHITECTURAL_DIAGNOSTIC_ONLY
ACTIVE_PEERS: CLAUDE_E18.2_REAL_ENGINE_FAIL_SAFETY_ECONOMY / COPILOT_E18.2_REAL_ENGINE_FAIL_PRODUCTIVE_CHAIN
ANTIGRAVITY: EXCLUDED_FROM_ACTIVE_TESTS_UNTIL_NEW_RELEASE
PEER_V2_REAL_ENGINE_INTAKE: COMPLETE_84_OF_84 / V4D_ONLY_GATE_PASS
CODEX_E18_2_DEV_GATE: PASS_9_OF_9 / 56_0 / MONEY_121149.84
CODEX_E18_2_DIRECT_V4D: 14_0 / 93401.71_VS_90012.00 / DELTA_+3.77_PERCENT
CODEX_E18_2_WORK: PASS_688_VS_724 / WEED_TILE_DAYS_15_VS_14
CODEX_E18_2_SAFETY: LOSSES_0 / ERRORS_0 / FALLBACKS_0
CODEX_E18_2_MODES: DENSE_V4D_AND_RECOVERY / TOPOLOGY_7_7_5_PRESERVED
CODEX_E18_2_SUBMISSION: submission/submission_codex_e18_2_capacity_governed_v4d.py
CODEX_E18_2_SUBMISSION_SHA256: C5FB1FC4966B81F238CDD0DE4CA5E15B16EA6B8AE077A08ECC881F8729FD01F7
NEXT_ACTION_E18_2: RETAIN_AS_EXTERNAL_CONTROL / NO_NEW_UPLOAD_IN_THIS_CYCLE
CODEX_E18_3_ABLATION: COMPLETE_70_OF_70 / FIVE_FIXED_TOPOLOGIES / CODEX_ONLY
CODEX_E18_3_RESULT: NO_CANDIDATE / SUBMISSION_NOT_AUTHORIZED
CODEX_E18_3_MONEY_VS_CONTROL: 775_-0.82_PERCENT / 772_-14.31_PERCENT / 662_-42.98_PERCENT / 770_-34.69_PERCENT / 670_-40.31_PERCENT
CODEX_E18_3_CAUSAL_RESULT: EXACT_TOPOLOGY_70_OF_70_BUT_REDUCED_GEOMETRIES_FAIL_CROP_LIFECYCLE
CODEX_E18_4_GATE: REJECTED_0_14 / 55940_VS_83095.71 / DELTA_-32.68_PERCENT
CODEX_E18_4_ARCHITECTURE: EXACT_772_14_OF_14 / FILL_16_OF_16_14_OF_14 / LOSSES_0
CODEX_E18_4_WORK: MOVE_+29.35_PERCENT / PRODUCTIVE_-20.95_PERCENT / HARVEST_80.83_PERCENT_CONTROL
NEXT_ACTION: BUILD_V2_LOCALITY_TASK_AGING_ABLATION_WITHOUT_KAGGLE_UPLOAD
```

## Entry point

E18 conserva il layout 6-6-2 e apre una sola linea causale: rendere mercato e
servizio realmente dipendenti dallo stato. Il benchmark Top 3 è osservazionale
e usa replay già consumati come training evidence; non è un confronto
head-to-head con policy eseguibili.

Materiali iniziali:

- `design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md`;
- `artifacts/baseline/E18_662_TOP3_BASELINE_BENCHMARK_V1.json`;
- `reports/common/E18_662_TOP3_BASELINE_BENCHMARK_IT.md`;
- `tools/common/build_e18_662_top3_baseline.py`;
- `tests/test_e18_662_top3_baseline.py`.

Nuovi materiali di apertura:

- `reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md`;
- `reports/common/E18_CLAUDE_COPILOT_CANDIDATE_INTAKE_IT.md`;
- `artifacts/discovery/E18_EPISODE_105080066_LIFECYCLE_ANALYSIS_V1.json`;
- `artifacts/discovery/E18_EPISODE_105080066_DAILY_TIMELINE_V1.csv`;
- `artifacts/discovery/E18_EPISODE_105080066_ACTIONS_BY_DAY_V1.csv`;
- `tools/common/analyze_episode_105080066.py`;
- `reports/common/E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_IT.md`;
- `artifacts/discovery/E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_V1.json`;
- `artifacts/discovery/E18_LIVE_TOP3_AND_CODEX_REPLAY_PROFILES_V1.csv`;
- `tools/common/build_e18_live_replay_benchmark.py`.

Il replay di apertura falsifica l'ipotesi troppo generica di una superficie
abbandonata prima: Codex conserva 496 crop-tile-days fra D21 e D30 contro 467,
ma raccoglie 586 unità contro 829. Il lotto live rafforza e precisa la
diagnosi: i tre replay Codex hanno un solo fingerprint agricolo, mentre i tre
leader ne hanno otto su otto e raccolgono in media 872,5 unità (`+48,9%`). La rotazione
aggressiva osservata in Yusuf è un meccanismo specifico; il segnale condiviso
dagli agenti leader è maggiore capacità di servizio e raccolta, con 173,7 late
unwatered tile-days contro 224.

## Intake Claude e Copilot

Le nuove linee dichiarate da Claude e Copilot entrano nell'audit E18, non nel
torneo economico in modo automatico. Nel repository non è ancora presente un
freeze E18 autonomo per nessuno dei due; gli asset callable da usare come
riferimento sono:

- Claude V3, ultimo riferimento tecnico state-driven stabile, ma con gate
  economici e di sicurezza falliti; V5 non è stata promossa e V6 è respinta;
- Copilot Native V1, indipendente e tecnicamente congelata ma ancora crop-only
  e valutata soltanto contro inert; le varianti 6-6-2 V3/V4 restano
  rispettivamente equivalente al controllo e prototipo non ammesso.

L'apertura E18 richiede per ogni nuova candidata: entry point callable,
config, hash/freeze, activation fixtures sul ciclo colturale e benchmark sui
soli seed development. Holdout e final restano bloccati.

I capitolati della prossima iterazione sono ora separati per linea:

- `prompts/claude/E18_CLAUDE_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md`:
  selector causale, lifecycle e azzeramento delle perdite zootecniche;
- `prompts/copilot/E18_COPILOT_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md`:
  footprint/workforce dinamici, lifecycle e dimezzamento delle weed.

Entrambi richiedono verdetti distinti per gate tecnico, architetturale ed
economico; nessuna media aggregata può compensare l'inerzia della policy.

## Torneo reattivo a quattro V2

Le nuove candidate Claude e Copilot sono state ammesse, insieme alla sonda
Codex E18.1 e all'Antigravity E17 obsoleto, a un round robin completo da 84
match. Antigravity ha disputato 42 round: 14 contro ciascun avversario, 21 per
seat, coprendo tutti i seed development. Il suo 0-42 a denaro zero e quasi
soli `PASS` identifica un problema di compatibilità operativa, non soltanto
una strategia debole.

Codex chiude 42-0 e supera 100k, ma attiva soltanto `6-6-2` e fallisce il gate
reattivo. Claude diverge causalmente in 14/14 gruppi, ma perde 31 animali e
vale 6.467,48. Copilot espone due regimi ma resta costante a 2.840, senza una
catena produttiva eseguita. Nessun agente viene promosso.

Materiali:

- `reports/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md`;
- `artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json`;
- `tools/common/run_e18_four_agent_reactive_tournament_v2.py`;
- `prompts/claude/E18_CLAUDE_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md`;
- `prompts/copilot/E18_COPILOT_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md`;
- `prompts/antigravity/E18_ANTIGRAVITY_REACTIVE_V1_REBOOT_PROMPT_IT.md`.

Per Codex non viene aperta una V2 locale sulla sola evidenza del torneo: la
calibrazione attende la stabilizzazione della submission Kaggle e l'analisi
completa dei replay esterni.

## Benchmark E18.1 contro E17 V4D

Il confronto controllato conferma la regressione osservata dall'utente su
Kaggle. Nei 14 scontri diretti E18.1 perde sempre e vale `71.831,00` contro
`89.760,57` di V4D (`-19,97%`). Sul pool comune Claude/Copilot/Antigravity il
delta resta `-12,20%` (`125.983,74` contro `143.486,45`).

Lo snapshot Kaggle successivamente leggibile rafforza la conclusione: E18.1
vale `825,4`, V4D `1.131,7` e la 6-6-2 E17.3 `941,4`. Il delta esterno
E18.1/V4D è `-27,07%`.

Le cinque celle sottratte ai pascoli non producono una conversione positiva:
E18.1 esegue il `6,11%` di azioni produttive in meno, il `24,77%` di `PASS` in
piu e il `320%` di weed tile-days in piu. Il selector resta inoltre in
`6-6-2` in tutti i match del pool. V4D torna quindi a essere il controllo
economico; E18.1 resta soltanto una diagnostica architetturale.

Materiali:

- `reports/codex/E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_REPORT_IT.md`;
- `artifacts/derived/codex/E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1.json`;
- `artifacts/derived/codex/E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1.csv`;
- `tools/codex/run_e18_latest_vs_e17_v4d_benchmark.py`.

## Roster attivo dopo le peer V2

I prossimi test escludono Antigravity fino a una nuova release callable e
compatibile con il motore. Il torneo di intake usa V4D come controllo
economico, E18.1 come ablation architetturale e le nuove Claude/Copilot V2.

Il nuovo intake real-engine chiude la lacuna. V4D vale `125.490,40` e vince
`42/42`; E18.1 vale `104.516,71`; Claude E18.2 `9.756,29` con `44` perdite
verificate; Copilot E18.2 resta a `260`. L'artifact sintetico Copilot non è
usato come evidenza. Report:
`reports/common/E18_PEER_V2_REAL_ENGINE_INTAKE_REPORT_IT.md`.

## Codex E18.2 — capacity governor topology-preserving

La nuova candidate riparte dal controllo V4D. Due smoke preliminari
falsificano sia il reclaim di un singolo pascolo Q2 sia la deviazione di un
worker `PASS`: entrambi rompono capacità o sincronizzazione e producono forti
regressioni. La variante ammessa conserva `7-7-5` e consente a un solo worker
altrimenti in `PASS` di servire `HARVEST`, `DIG` o `WATER` soltanto sul tile
corrente. D28-D29 restano passthrough V4D.

Nel gate real-engine da 56 match chiude `56-0`, media `121.149,84`; nel
diretto batte V4D `14-0`, `93.401,71` contro `90.012,00` (`+3,77%`). Riduce i
`PASS` da `724` a `688`, mantiene 19 animali e zero perdite; i weed tile-days
salgono da `14` a `15`, ancora entro il cap `+10%`. Tutti i nove gate passano
e i modi action-effect `DENSE_V4D` e `RECOVERY` sono entrambi attivi.

Lo standalone è isolato e action-parity verificato in entrambi i seat. È
pronto per una decisione esplicita di upload, ma non è stato inviato
automaticamente e non ha consumato holdout/final. Report:
`reports/codex/E18_2_CAPACITY_GOVERNED_V4D_DEV_REPORT_IT.md`.

## Top 3 corrente e acquisizione

Lo snapshot pubblico del 2026-09-03 è `Crop Dusta` 2958,7, `3정훈` 2948,1 e
`sbol ball` 2929,8. Otto replay sono acquisiti e analizzati, con entrambi i
seat coperti per ogni leader. Sette profili su otto usano zero pascoli in Q2,
ma Crop Dusta cambia da `7-0-0` a `8-4-3`; 3정훈 e sbol ball arrivano anche a
`10-7-0`. La topologia è quindi una decisione di regime, non un target
universale. La candidate E18.1 legge la farm pubblica avversaria al D6 e
congela `6-6-2` o `7-7-0`; catalogo e SHA-256 dei replay rimossi sono in
`data/replays/json/json.md`.

## Torneo dinamico e submission diagnostica

Il torneo development V1 usa 56 match, sette seed E18 e entrambi i seat. La
candidate attiva `6-6-2` in 28/42 run contro Claude V3 e controllo Codex,
`7-7-0` in 14/42 contro Copilot Native, e produce divergenza di action stream
e topologia in 14/14 gruppi seed/seat. Termina sempre con 14/14 pascoli,
zero perdite verificate, errori, fallback e breach.

Il final money medio è 111.654,45, ma la media dipende dal matchup. Contro il
controllo 6-6-2 vale 80.456,43 e perde 3.472,29 (`−4,14%`); contro Claude e
Copilot vale rispettivamente 127.072,71 e 127.434,21. Per questo lo standalone
`submission/submission_codex_e18_opponent_reactive_662_770.py` è pronto come
diagnostica Kaggle, non è ancora promosso a nuova baseline. Import isolato e
parità `719/719` passano in entrambi i regimi. Report:
`reports/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md`.

## Evidence boundary

- E17 development e Top-3 replay: training evidence riusata;
- E18 development: nuovo set preregistrato nel manifest E18;
- holdout/final: non consumati e non autorizzati;
- Kaggle: external validation successiva, non parte dell'entry benchmark.

## Ablation interna Codex E18.3

Il confronto Codex-only usa 70 match real-engine e separa cinque geometrie
fisse dal controllo E18.2. Tutti i bracci costruiscono la topologia prevista
in 14/14 match; soltanto il passthrough `7-7-5` resta vicino al controllo
(`-0,82%`). `7-7-2`, `6-6-2`, `7-7-0` e `6-7-0` perdono rispettivamente
`14,31%`, `42,98%`, `34,69%` e `40,31%`.

Il fallimento non è quindi geometrico: i bracci ridotti perdono crop-days
tardivi, accumulano weed-days, abbandonano più colture e raccolgono meno
unità. Nessuna submission è autorizzata. Report:
`reports/codex/E18_3_CODEX_INTERNAL_TOPOLOGY_ABLATION_REPORT_IT.md`.
