# Codex C2 — Compact Q0 Routine Build Report

## 1. Executive Verdict

Il candidate `CODEX-C2-COMPACT-Q0-ROUTINE-V7` è stato costruito come nuovo
planner agent-specific, verificato tecnicamente e misurato una sola volta sul
batch preregistrato. La build tecnica è `PASS`: sei episodi economici su sei
sono terminati `DONE`, senza errori o fallback.

Il risultato economico medio è `39.265,67`. È un miglioramento sostanziale
rispetto a Codex V6 e supera di `1.268,00` il riferimento AG Q0 3+3, ma
resta sotto 50.000 e a `-17.506,33` da LuCcc. Inoltre si registrano 24
fughe animali. Il gate è quindi `FAILURE` e il verdetto è
`BUILD_NOT_READY`.

Non è stato eseguito tuning dopo il batch, né tournament, Kaggle, commit o push.

## 2. Foundation / Repository Verification

| Check | Esito |
|---|---|
| branch / HEAD | `main` / `f391ee2` |
| Foundation richiesta | `f391ee2` — invariata |
| Foundation / DLC condivisi modificati | NO |
| Antigravity / Copilot modificati da questo build | NO |
| Q1 o `BUY_LAND` usati | NO |
| worktree condiviso | dirty per attività concorrenti preesistenti; preservate |

La revisione è limitata a MODEL_SPEC, controller, configurazione, tooling,
test, standalone ed evidenze Codex. Le modifiche concorrenti di altri agenti
non sono state ripristinate né incluse nell'identità della build.

## 3. MODEL_SPEC Changes

`docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md` è stata riscritta
direttamente per il candidate V7. Contiene obiettivo, footprint Q0, sette ruoli,
zone e route, orizzonti, commitment atomico, hard interrupt, capacity admission,
coorti, attivazione livestock, fertilizer loop, market policy, verifica,
strumentazione e criteri di review.

Il lifecycle runtime è ridotto a identity, PLAN locale, commitment, verifica
post-state, invalidazione, reason code ed evidence logging. Non è stato creato
un nuovo layer documentale e il DLC comune non è stato modificato.

## 4. V6 Components Removed

Sono stati rimossi dalla policy produttiva:

- calendario hard a 17 giorni;
- riserve fisse route 20% ed exception 15%;
- daily commitment immutabile;
- limite generico di due nuove entità al giorno;
- default a due quadranti;
- planner produttivo V6.

Sono stati riutilizzati soltanto adapter engine, legality guard, identità
stabile, verifica request/effect, telemetry e compatibilità standalone.
`src/agricola/strategy/codex_c2.py` è ora uno shim di compatibilità verso il
nuovo controller.

## 5. Production Architecture

Il footprint congelato è interamente in Q0:

```text
18 crop = 9 MELON + 8 STRAWBERRY + 1 WHEAT
6 pasture
livestock target = 3 COW + 3 SHEEP
workforce target = farmer + 6 hands
GOOSE = 0
```

La shed centrale resta accessibile; non esiste una diciannovesima crop tile e
non viene mai richiesto acquisto di terra.

## 6. Worker Roles and Zones

| Worker | Ruolo persistente | Ambito |
|---:|---|---|
| 0 | `FLOAT_RESERVE` | interrupt hard e overload |
| 1–3 | `CROP_ZONE_0..2` | tre zone locali da sei crop |
| 4 | `LIVESTOCK_COW` | route COW |
| 5 | `LIVESTOCK_SHEEP` | route SHEEP |
| 6 | `FERTILIZER_LOGISTICS` | shed, feed, fertilizer, unblock |

I ruoli non hanno oscillato durante i run (media `ROLE_CHANGES = 0`).
Le reservation hanno impedito duplicate assignment (totale zero). Il float
non vaga: ogni azione non-PASS è collegata a un target. Le assistenze
cross-zone sono state 51,67 per episodio in media.

## 7. Planning and Replanning

Il controller usa route locali rolling e commitment atomici. Il target cambia
solo per completion, invalidation, worker unavailability o hard interrupt.
Il global replan è limitato a EOD, cambi workforce/asset e invalidazioni
strutturali; l'hard schedule copre il giorno corrente e la successiva boundary
biologica.

Gli interrupt osservati nel batch sono:

| Reason code | Totale |
|---|---:|
| `ANIMAL_ESCAPE_PREVENTION` | 7 |
| `CROP_WATER_LOSS` | 34 |
| `HARVEST_TERMINAL_RISK` | 19 |

La bassa frequenza di retarget (0,04769 per worker-day) e il dwell medio 3,118
step confermano che la policy non è tornata al rescan opportunistico per turno.

## 8. Capacity Admission

La rule registra `AVAILABLE`, servizi hard, MOVE, handling,
`REQUIRED`, slack corrente/successivo e capacità osservata sugli ultimi
tre giorni completi. Prima della finestra osservabile consente soltanto il
bootstrap preregistrato.

Nel batch sono state registrate 64 rejection: 18 per
`CASH_OR_FEED_BUFFER_INSUFFICIENT` e 46 per
`NEGATIVE_ACTION_SLACK`. Le ammissioni risultano 14: 12 al day 13 e 2 al
day 12. Le due ammissioni in eccesso rispetto alle 12 espansioni nominali sono
coerenti con sostituzioni successive a perdita di animali, non con crescita
oltre il target finale 3+3.

La rule ha quindi evitato l'espansione forzata ai day 7/8, ma non ha prevenuto
la successiva perdita di animali dopo l'ammissione.

## 9. Crop Cohorts

MELON è congelato in tre coorti spaziali di tre con offset `0/1/2`;
STRAWBERRY in due coorti di quattro con offset `0/2`; WHEAT occupa una
sola tile e alimenta il feed buffer.

La produzione media high-value è 135,17 unità (95 MELON + 40,17
STRAWBERRY). L'indicatore
`HIGH_VALUE_CROP_UNITS_VS_COHORT_PLAN` è 1,1264 rispetto al riferimento
strumentale di 120 unità. MELON supera il range preregistrato 48–60, mentre
STRAWBERRY resta sotto il minimo 45.

## 10. Livestock Activation

Il bootstrap 2 COW + 2 SHEEP è stato eseguito tra day 0 e 1. L'espansione
prevista circa day 7/8 è stata respinta da feed/cash e slack; il 3+3 è stato
raggiunto prevalentemente al day 13, con sei animali finali in tutti i run.

Questo risultato finale non equivale a serviceability: ogni episodio registra
quattro fughe (24 totali) e le sostituzioni mantengono il conteggio finale a
3 COW + 3 SHEEP. La media output è soltanto 28,17 MILK e 14,67 WOOL, molto
sotto i range preregistrati 90–100 e 85–95.

## 11. Fertilizer / Logistics

Il closed loop pasture → collection → high-value crop → WATER è implementato.
Le medie sono 80,83 fertilizer raccolti e 20,17 applicati, pari a circa il
24,95% del raccolto convertito in applicazione diretta. WHEAT consumato è
100,33 ed è stato venduto per 16,67 unità in media.

La contribution trading resta zero per definizione: il mercato è usato per
input e monetizzazione della produzione, non per arbitraggio.

## 12. Technical Verification

| Verifica | Esito |
|---|---|
| import controller / compile | PASS |
| build standalone / isolated import | PASS |
| source–standalone parity | PASS, esatta per 120 step sui seed 26090101/02 |
| prefix engine P0/P1 | PASS, 120 step, zero error/fallback |
| terminal P0/P1 | PASS, `DONE` / `TERMINAL_CLOSED` |
| manual `DROP` / `BUY_LAND` | zero |
| request/effect verification | PASS |
| test agent-specific + isolation | 20 passed |
| suite repository applicabile | 183 passed |
| Ruff percorsi Codex | PASS |

L'unico warning test è l'impossibilità del runner di creare
`.pytest_cache` (WinError 5); non incide sugli esiti. I messaggi
OpenSpiel relativi a giochi opzionali mancanti sono rumore d'import e non
errori Kaggriculture.

## 13. Seed-Level Performance

Protocollo: tre seed preregistrati, entrambi i seat, 720 step, avversario
controllato `INERT_PASS_POLICY`.

| Seed | Seat | FINAL_MONEY | MILK | WOOL | MELON | STRAWBERRY | On-time | Miss | Escape |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 26090101 | 0 | 40.677 | 28 | 15 | 95 | 40 | 79,37% | 9 | 4 |
| 26090101 | 1 | 39.531 | 28 | 15 | 95 | 40 | 79,37% | 9 | 4 |
| 26090102 | 0 | 38.355 | 28 | 15 | 95 | 40 | 79,37% | 9 | 4 |
| 26090102 | 1 | 38.355 | 28 | 15 | 95 | 40 | 79,37% | 9 | 4 |
| 26090103 | 0 | 41.156 | 30 | 14 | 95 | 42 | 79,16% | 8 | 4 |
| 26090103 | 1 | 37.520 | 27 | 14 | 95 | 39 | 80,34% | 6 | 4 |

Media `39.265,67`, mediana `38.943`, deviazione standard
popolazione `1.312,86`; range 37.520–41.156. Tutti i run sono
tecnicamente validi.

## 14. Production Decomposition

| Metrica media | Risultato |
|---|---:|
| crop revenue | 29.786,67 |
| livestock revenue | 10.664,83 |
| market/trading contribution | 0 |
| MELON | 95,00 |
| STRAWBERRY | 40,17 |
| MILK | 28,17 |
| WOOL | 14,67 |
| WHEAT consumed / sold | 100,33 / 16,67 |
| fertilizer collected / applied | 80,83 / 20,17 |

Il ramo crop produce il 73,64% della revenue produttiva registrata; il
livestock il 26,36%. I costi di hire, input, animali e sostituzioni spiegano
perché la somma delle revenue non coincide con FINAL_MONEY.

## 15. Worker Efficiency Metrics

| Indicatore medio | Valore |
|---|---:|
| productive actions | 688,17 |
| MOVE actions | 2.196,83 |
| PASS actions | 871,50 |
| `MOVE_PER_PRODUCTIVE_ACTION` | 3,1923 |
| `PRODUCTIVE_UTILIZATION` | 67,43% |
| productive utilization finale | 42,36% |
| `ON_TIME_CROP_SERVICE_RATIO` | 79,49% |
| `HARD_DEADLINE_MISSES` | 50 totali / 8,33 per episodio |
| `RETARGET_PER_WORKER_DAY` | 0,04769 |
| target dwell | 3,118 step |
| duplicate assignments | 0 |

Commitment e deduplica funzionano, ma l'elevato costo di movimento e le 871,5
PASS medie tengono l'utilizzazione sotto il target 80–96%.

## 16. Comparison vs AG Q0 3+3

Il riferimento AG Q0 3+3 è 37.997,67. V7 raggiunge 39.265,67:

```text
DELTA: +1.267,997
RELATIVE: +3,34%
```

È un superamento misurabile del riferimento, ma non sufficiente a cambiare il
gate del progetto. La comparazione usa solo il valore aggregato fornito; non
attribuisce causalità a differenze non misurate di protocollo.

## 17. Comparison vs LuCcc

Rispetto a LuCcc 56.772:

```text
DELTA: -17.506,333
RELATIVE: -30,84%
MINIMUM_ACCEPTABLE 56.773: mancato di 17.507,333
```

La predizione preregistrata 60–68k non è confermata. Anche il limite inferiore
di strong success, 60.000, dista 20.734,33.

## 18. Failure/Success Diagnosis

`PRIMARY_BOTTLENECK: LIVESTOCK_SERVICEABILITY`.

Evidenze convergenti:

- 24 fughe contro il requisito zero;
- MILK a 28,17 contro 90–100 e WOOL a 14,67 contro 85–95;
- espansione normalmente rinviata al day 13;
- 14 ammissioni anziché 12 nominali, coerenti con replacement;
- 100,33 WHEAT consumato senza conversione proporzionata in output animale.

`ROUTING` e `CROP_SERVICEABILITY` sono fattori secondari:
3,192 MOVE per produttiva, utilizzo 67,43%, on-time 79,49% e 50 miss mostrano
capacità dispersa. Non sono scelti come primary perché il gate esplicito più
netto e la perdita produttiva maggiore sono nel sottosistema livestock.
Non viene applicata alcuna correzione sui seed osservati.

## 19. Final Gate

La build soddisfa il gate tecnico ma non quello economico, non elimina le
fughe e non preserva materialmente l'output livestock. Resta chiusa a
tournament e Kaggle.

```text
AGENT_ID:
codex

ARCHITECTURE:
Q0_18CROP_6PASTURE_3COW_3SHEEP_7WORKERS

MODEL_SPEC_REVISION:
COMPLETE

TECHNICAL_BUILD:
PASS

FINAL_MONEY_MEAN:
39265.6667

FINAL_MONEY_MEDIAN:
38943.0000

FINAL_MONEY_STD:
1312.8597

MILK_MEAN:
28.1667

WOOL_MEAN:
14.6667

MELON_MEAN:
95.0000

STRAWBERRY_MEAN:
40.1667

PRODUCTIVE_UTILIZATION:
0.674326

MOVE_PER_PRODUCTIVE_ACTION:
3.192311

RETARGET_PER_WORKER_DAY:
0.047685

ON_TIME_CROP_SERVICE_RATIO:
0.794950

HARD_DEADLINE_MISSES:
50

ANIMAL_ESCAPES:
24

DELTA_VS_CODEX_V6_9851:
29414.6667

DELTA_VS_AG_Q0_3X3_37997_67:
1267.9967

DELTA_VS_LUCCC_56772:
-17506.3333

ECONOMIC_GATE:
FAILURE

PRIMARY_BOTTLENECK:
LIVESTOCK_SERVICEABILITY

BUILD_VERDICT:
BUILD_NOT_READY

TOURNAMENT_AUTHORIZED:
NO

KAGGLE_AUTHORIZED:
NO

COMMIT_AUTHORIZED:
NO

PUSH_AUTHORIZED:
NO
```
