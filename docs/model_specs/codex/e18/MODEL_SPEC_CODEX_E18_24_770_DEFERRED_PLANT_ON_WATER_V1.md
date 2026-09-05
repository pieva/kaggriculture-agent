# MODEL SPEC — Codex E18.24 7-7-0 deferred PLANT on WATER V1

## Stato

`REJECTED_PRE_GATE__STALE_DUPLICATE_DIAGNOSIS__NO_UPLOAD`

E18.24 è un'ablation diagnostica derivata direttamente da E18.22. Non è una
candidata promossa e non autorizza Gate 1, holdout, final confirmation o
upload Kaggle.

## Ipotesi preregistrata

Contro E18.16 le 11 azioni `PLANT` di D11 dirette alla SW vengono respinte
perché la land non è ancora sbloccata. Tutte le stesse coordinate ricevono
una visita `WATER` a D12–D13. L'ipotesi era recuperare la semina usando quello
slot già pianificato, senza aggiungere MOVE né cambiare worker o route.

## Trattamento isolato

Per le sole 11 coordinate `PLANT` respinte a D11, E18.24 intercetta il primo
`WATER` successivo sulla medesima tile:

- se la tile è vuota e il seed è disponibile, emette `PLANT`;
- se è infestata, emette `DIG` e mantiene il retry;
- se è già occupata, marca il target come risolto senza alterare l'azione.

Il piano E18.18 e il suo hash, il mercato E18.22, le route, `7-7-0`, 14
animali e 12 hands restano invariati.

## Evidenza

### Delta causale contro E18.22

| Seat E18.24 | E18.24 | E18.22 | Margine | PLANT reali recuperati |
|---:|---:|---:|---:|---:|
| 0 | 74.682 | 74.378 | +304 | 1 |
| 1 | 74.510 | 74.550 | -40 | 1 |

La mediana è `74.596` contro `74.464`, ma un seat regredisce. Il singolo
recupero nel matchup simmetrico aumenta inoltre gli `HARVEST` respinti a
43–44: il delta non è robusto e fallisce il gate causale.

### Confronto con E18.16

| Seat E18.24 | E18.24 | E18.16 | Margine | PLANT recuperati | Target già occupati |
|---:|---:|---:|---:|---:|---:|
| 0 | 52.379 | 79.284 | -26.905 | 0 | 11 |
| 1 | 51.704 | 77.693 | -25.989 | 0 | 11 |

L'outcome è esattamente uguale a E18.22. Al primo `WATER` utile tutte le 11
tile risultano già occupate: i rifiuti D11 sono duplicati obsoleti nella
traiettoria, non 11 colture mancanti. Anche 65 degli 80 `HARVEST` rifiutati
nei due seat cadono su tile vuote e 15 su weed, indicando task superati dallo
stato più che perdite economiche dimostrate.

## Verdetto e implicazione

L'ipotesi è falsificata. Non bisogna valorizzare il numero grezzo di comandi
respinti come perdita economica né riempire automaticamente i `PASS`: il gap
residuo è nel minor turnover produttivo del piano e nella fase D21–D30. Una
nuova versione deve intervenire sul planner delle colture, con target espliciti
di cicli completati e monetizzati, non con un altro overlay di recupero.

## Artefatti

- config: `configs/CODEX_E18_24_770_DEFERRED_PLANT_ON_WATER_V1.json`;
- controller: `tools/e18_24_deferred_plant_on_water_controller.py`;
- test: `tests/test_codex_e18_24_deferred_plant_on_water_controller.py`;
- runner: `tools/run_e18_24_770_deferred_plant_on_water_gate.py`;
- risultati: `artifacts/derived/E18_24_770_DEFERRED_PLANT_ON_WATER_PRE_GATE_V1.json`;
- report: `reports/E18_24_770_DEFERRED_PLANT_ON_WATER_PRE_GATE_REPORT_IT.md`;
- diagnosi sorgente: `reports/E18_22_CROP_REJECTION_DIAGNOSTIC_REPORT_IT.md`.
