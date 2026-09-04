# E18.2 — Capacity-Governed V4D

## Verdetto

La candidate supera il gate development completo e recupera il controllo
economico V4D senza cambiare topologia. Chiude `56-0`, media `121.149,84` sul
pool attivo e batte V4D `14-0`: `93.401,71` contro `90.012,00`, delta
`+3.389,71` (`+3,77%`). Zero errori, fallback e perdite zootecniche.

Non è stata consumata evidenza holdout/final e non è stata effettuata una
submission Kaggle automatica.

## Evoluzione delle ablation

1. `7-7-4` con un pascolo Q2 recuperato: interrotta dopo i primi match,
   regressioni osservate fino a circa `-60k` contro V4D.
2. `RECOVERY` con deviazione di un worker `PASS`: interrotta, regressioni fra
   `-13,7k` e `-55,3k`. I `PASS` V4D non sono capacità libera generica: sono
   parte della sincronizzazione del routing.
3. `RECOVERY` solo sul tile corrente: ammessa. Il worker può servire un task
   già sotto i piedi, senza `MOVE` e senza cambiare gli altri comandi.

La falsificazione delle prime due varianti è parte del risultato: la
reattività utile è locale e non distrugge gli impegni impliciti del provider.

## Risultati

| Confronto | Record E18.2 | E18.2 medio | Avversario medio | Delta medio |
|---|---:|---:|---:|---:|
| V4D | 14-0 | 93.401,71 | 90.012,00 | +3.389,71 |
| E18.1 ablation | 14-0 | 92.933,43 | 71.907,43 | +21.026,00 |
| Claude E18.2 | 14-0 | 139.836,71 | 7.614,14 | +132.222,57 |
| Copilot E18.2 | 14-0 | 158.427,50 | 260,00 | +158.167,50 |
| **Pool** | **56-0** | **121.149,84** | — | — |

### Gate diretto V4D

| Gate | E18.2 | V4D | Esito |
|---|---:|---:|---|
| denaro | 93.401,71 | 90.012,00 | +3,77%, PASS |
| PASS | 688 | 724 | -4,97%, PASS |
| weed tile-days | 15 | 14 | +7,14%, PASS sotto cap +10% |
| animali finali | 19 | 19 | pari |
| perdite verificate | 0 | 0 | PASS |
| errori / fallback | 0 / 0 | 0 / 0 | PASS |

Il gate complessivo passa `9/9`. `DENSE_V4D` e `RECOVERY` producono entrambi
effetti reali sulle azioni; la candidate mostra divergenza condizionata degli
action stream in `14/14` gruppi. La topologia resta intenzionalmente stabile:
la reattività di questa iterazione è nel controllo di capacità/servizio, non
nel numero di pascoli.

Un fixture causale isola anche l'adattamento all'avversario: con lo stesso
stress proprio lieve, la pressione pubblica alta abilita il servizio locale e
quella bassa lascia invariato il `PASS`; lo stress proprio severo conserva
sempre la precedenza.

## Bundle

Standalone:
`submission/submission_codex_e18_2_capacity_governed_v4d.py`.

- SHA-256: `C5FB1FC4966B81F238CDD0DE4CA5E15B16EA6B8AE077A08ECC881F8729FD01F7`;
- parità completa verificata in entrambi i seat contro V4D;
- topologia reclaim disabilitata nel freeze;
- holdout/final non consumati.

Descrizione suggerita per Kaggle:

> Codex E18.2 — capacity-governed V4D: topology-preserving on-tile recovery,
> D28 terminal passthrough; 56-0 dev gate, +3.77% vs V4D.

## Artefatti

- `artifacts/derived/codex/E18_2_CAPACITY_GOVERNED_V4D_DEV_GATE_V1.json`;
- `artifacts/derived/codex/E18_2_CAPACITY_GOVERNED_V4D_DEV_GATE_V1.csv`;
- `tools/codex/run_e18_2_capacity_governed_v4d_gate.py`;
- `tests/test_e18_2_capacity_governed_v4d_gate.py`;
- `tools/codex/build_e18_2_capacity_governed_submission.py`;
- `tools/codex/verify_e18_2_capacity_governed_submission.py`.
