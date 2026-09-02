# E17.0 — Riepilogo comune di gate e blocker

Data: 2026-09-02

Integration owner: Codex

Perimetro: measurement parity e costruzione delle baseline native 3Q

Verdetto comune: `E17_0_GATE_PASS_WITH_READINESS_LIMITATIONS`

## Decisione

Il Fronte A è chiuso e la barriera A→B è stata superata. Le tre review della
strategia sono state riconciliate, la strategia `E17_STRATEGY_FROZEN_V1` è
congelata e i tre agenti hanno consegnato report, metriche e freeze di E17.0.

I gate tecnici di E17.0 sono `PASS` per tutti gli agenti. Questo verdetto
attesta copertura del ledger, riproducibilità/parità ove applicabile,
provenance, assenza di errori e indipendenza locale delle nuove baseline. Non
attesta equivalenza economica o readiness per un torneo competitivo.

```text
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
POST_MIGRATION_REVIEWS: 3/3
E17_STRATEGY_REVIEWS: 3/3
E17_STRATEGY_FREEZE: PASS
E17_0_REPORTS: 3/3
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_1_STARTED: NO
HOLDOUT_CONSUMED: NO
FINAL_CONFIRMATION_CONSUMED: NO
```

## Matrice comparativa

| Agente | Ruolo E17.0 | Run | Parità/riproducibilità | Record ledger | Coverage record | Coverage market classificata | Errori | Fughe derivate | Denaro finale mean / min | Indipendenza locale | Esito |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| Codex | V9 congelata + ledger esterno | 6 coppie baseline/strumentata | `4314/4314`, outcome `6/6` | 51.834 | 100% | 18,9117% | 0 | 0 | 132.019,3 / 77.542 | PASS, baseline owner | PASS |
| Antigravity | baseline nativa 3Q | 6 coppie plain/strumentata | action e terminale `6/6` | 4.326 | 100% | 100% su 12 record market | 0 | 0 | 0 / 0 | PASS | PASS con limitazione maggiore |
| Copilot | baseline nativa 3Q | 6 run + replica deterministica | `6/6` | 26.163 | 100% | 10,1781% | 0 | 0 | 8.941,5 / 8.263 | PASS | PASS |

La coverage dei record e la coverage degli outcome classificabili sono misure
distinte. Tutti i comandi emessi hanno un record. Gli ordini multipli il cui
delta aggregato non consente attribuzione certa restano correttamente
`UNKNOWN`; non sono stati convertiti artificialmente in esiti eseguiti o non
eseguiti.

## Gate B5 riconciliati

| Gate | Codex | Antigravity | Copilot | Comune |
|---|---|---|---|---|
| Action parity | PASS `4314/4314` | PASS `6/6` plain/strumentata | N/A; riproducibilità PASS `6/6` | PASS |
| Ledger record coverage | 100% | 100% | 100% | PASS |
| Market outcome coverage dichiarata con `UNKNOWN` preservati | PASS | PASS | PASS | PASS |
| Technical errors | 0 | 0 | 0 | PASS |
| Fallback delta | 0 | 0 | 0 | PASS |
| Animal escape ledger | auditable; 0 | auditable; 0 | auditable; 0 | PASS |
| Source/config freeze | PASS | PASS | PASS | PASS |
| Strategic independence, audit locale e integrazione | PASS | PASS | PASS | PASS |

Il ledger condiviso congelato è `E17_LEDGER_V1`, SHA-256
`A22C97584D4AE81A341485744C8AF0FFBBF14A9C9A8491BD3210FC768AD672C9`.
L'opponent comune è `INERT_PASS_POLICY`, SHA-256
`C0CC94FC4F1297107272BA325075E645653131C1B7E585F34CD3B1E5A3388EF5`.

Verifica integrata finale: `62/62` test PASS, `50/50` JSON E17 validi,
`32/32` riferimenti hash dei freeze verificati, `0` link locali rotti sulla
superficie Markdown attiva e `git diff --check` senza errori.

## Audit di indipendenza

Le due baseline native non importano routine, planner, dispatcher, schedule o
action table di altri agenti. I fingerprint nativi sono distinti dalla routine
Codex:

- Antigravity: `7193885A584AC82E177BFB2E38E37F0B7884F465140C9FFE7FD6E9E7C9443C67`;
- Copilot: `315073D272A4EF38DA2E98AD1B559A2A3DC4A4C2C117CEC609DC377E324BCDAB`;
- routine Codex: `C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4`.

Il gate d'indipendenza E17.0 è quindi `PASS`. Prima di un futuro torneo di
Livello D resterà comunque necessaria la review indipendente prevista dal
protocollo congelato.

## Limiti e blocker per la fase successiva

### Blocker formali E17.0

Nessuno.

### Readiness da riconciliare prima di autorizzare E17.1

1. La baseline Antigravity possiede e registra tre quadranti in tutti i run,
   ma spende il capitale iniziale nell'espansione immediata: `max_hands=0` e
   reward `0` in 6/6. È valida per provenance e test del ledger, non è ancora
   una baseline produttiva comparabile.
2. La baseline Copilot è produttiva e realmente 3Q, ma contro opponent inert
   ottiene mean `8.941,5`, molto sotto la V9 Codex; il dato è diagnostico e non
   costituisce un gate di promozione.
3. La classification coverage market è conservativa e parziale per Codex e
   Copilot. Un eventuale obiettivo del 100% richiede correlazione engine-side,
   non inferenza post-hoc.
4. Le nuove baseline native non hanno consumato holdout, final confirmation o
   torneo indipendente. Nessuno di questi livelli è autorizzato da questo
   prompt.

Questi punti non riaprono E17.0, ma impediscono di interpretarne il PASS come
promozione automatica. La decisione fra una remediation E17.0b delle baseline
native e l'avvio di E17.1 richiede riconciliazione comune e autorizzazione del
proprietario.

## Evidenza primaria

- `experiments/e17/reports/codex/E17_0_IMPLEMENTATION_AND_PARITY_REPORT.md`;
- `experiments/e17/reports/antigravity/E17_0_IMPLEMENTATION_AND_PARITY_REPORT.md`;
- `experiments/e17/reports/copilot/E17_0_IMPLEMENTATION_AND_PARITY_REPORT.md`;
- `experiments/e17/artifacts/derived/{codex,antigravity,copilot}/E17_0_METRICS.json`;
- `experiments/e17/artifacts/freeze/{codex,antigravity,copilot}/E17_0_FREEZE_MANIFEST.json`.

## Stop

```text
POLICY_MUTATION_BEYOND_E17_0: NO
E17_1_IMPLEMENTED: NO
INDEPENDENT_TOURNAMENT: NO
KAGGLE_SUBMISSION: NO
COMMIT: NO
PUSH: NO
NEXT_ACTION: OWNER_REVIEW_AND_E17_0_RECONCILIATION
```
