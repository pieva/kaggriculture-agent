# MODEL SPEC — Codex E18.23 7-7-0 SW unlock liquidity V1

## Stato

`REJECTED_PRE_GATE__NO_CAUSAL_DELTA__NO_UPLOAD`

E18.23 è un'ablation diagnostica di E18.22. Non è una candidata promossa e
non autorizza Gate 1, holdout, final confirmation o upload Kaggle.

## Ipotesi preregistrata

Nel matchup contro E18.16 la terza land costa 2.000. A D10 H24 E18.22 dispone
di 1.479 prima della vendita di quattro Fertilizer e la richiesta
`BUY_LAND` non viene eseguita; la SW compare soltanto a D12 H1. L'ipotesi era
che anticipare da D11 a D10 il procurement Wheat JIT D+1 liberasse almeno le
125 unità monetarie spese per cinque Wheat e anticipasse lo sblocco SW.

## Trattamento isolato

E18.23 cambia una sola variabile rispetto a E18.22: `activation_day` del cap
Wheat JIT da 11 a 10. Piano, route, crop, mercato non-Wheat, topologia
`7-7-0`, 14 animali e 12 hands restano invariati.

## Evidenza

### Delta causale contro E18.22

| Seat E18.23 | E18.23 | E18.22 | Margine |
|---:|---:|---:|---:|
| 0 | 76.661 | 76.487 | +174 |
| 1 | 76.487 | 76.661 | -174 |

Le mediane coincidono a `76.574`; il segno si inverte con il seat. Il delta
causale è nullo e fallisce il requisito di non regressione in entrambi i
seat. Le cinque unità Wheat di D10 appartengono già all'orizzonte D+1 e non
vengono rimosse dal trattamento.

### Confronto con E18.16

| Seat E18.23 | E18.23 | E18.16 | Margine | Primo SW osservato |
|---:|---:|---:|---:|---:|
| 0 | 52.379 | 79.284 | -26.905 | D12 H1 |
| 1 | 51.704 | 77.693 | -25.989 | D12 H1 |

L'outcome è identico a E18.22: mediana `52.041,5` contro `78.488,5`. Lo
sblocco SW non viene anticipato e restano 11 `PLANT` respinte per seat.

## Verdetto e implicazione

L'ipotesi è falsificata. La carenza osservata a D10 è almeno 461 dopo la
vendita prevista e non è risolvibile anticipando di un giorno il medesimo cap
JIT. E18.23 è respinta; E18.22 rimane il miglior sviluppo.

## Artefatti

- config: `configs/CODEX_E18_23_770_SW_UNLOCK_LIQUIDITY_V1.json`;
- controller: `tools/e18_23_sw_unlock_liquidity_controller.py`;
- test: `tests/test_codex_e18_23_sw_unlock_liquidity_controller.py`;
- runner: `tools/run_e18_23_770_sw_unlock_liquidity_gate.py`;
- risultati: `artifacts/derived/E18_23_770_SW_UNLOCK_LIQUIDITY_PRE_GATE_V1.json`;
- report: `reports/E18_23_770_SW_UNLOCK_LIQUIDITY_PRE_GATE_REPORT_IT.md`.
