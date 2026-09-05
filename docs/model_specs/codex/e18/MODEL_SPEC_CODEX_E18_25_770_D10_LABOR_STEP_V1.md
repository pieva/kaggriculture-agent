# MODEL SPEC — Codex E18.25 7-7-0 D10 labor step V1

## Stato

`GENERATED__MATCHED_PARENT_DELTA_PASS__INCUMBENT_GATE_FAIL__NO_UPLOAD`.

E18.25 recupera il primo gap temporale misurato contro Top770: a fine D10
porta la forza lavoro da 7 a 12 unità attive, cioè farmer più 11 hands. La
versione è un miglioramento riproducibile di E18.22, ma non supera E18.16 e
non è autorizzata a Gate 1, holdout, final confirmation o upload Kaggle.

## Diagnosi causale

Il limite non era un errore di `HIRE`, né insufficienza di capitale. Il planner
E18.18 sceglieva deliberatamente il minimo numero di hands che copriva il
workload nominale con riserva dell'1%. A D10 selezionava 6 hands più farmer:
161 slot disponibili per 156 azioni pianificate.

Top770 osservato nei replay exact `7-7-0` arriva invece a 12 unità a D10. Il
costo di 11 assunzioni nello stesso giorno è 232 contro 20 per 6 assunzioni:
il trattamento richiede quindi 212 di capitale aggiuntivo, disponibile nel
nostro stato D10.

## Trattamento isolato

Il planner accetta ora un vincolo opzionale `minimum_hands_by_day`. Soltanto
per E18.25 è impostato a `{"10": 11}`. Restano invariati:

- topologia `7-7-0` e 14 pascoli;
- cap 14 e mix finale `9 COW + 5 SHEEP`;
- checkpoint D10 `12 MELON + 20 STRAWBERRY + 5 WHEAT` e
  `9 COW + 4 SHEEP`;
- calendario, azioni biologiche, mercato E18.22 e retry executor;
- tutti gli altri target giornalieri di manodopera.

Il nuovo hash del piano è
`ffa39984acd4d506db39856d5269e3e8e1af909ddf2a4324a9d16955d834a786`.
Il piano E18.18 congelato conserva il proprio hash
`844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1`.

## Effetto sul piano D10

| KPI | E18.22 | E18.25 | Delta |
|---|---:|---:|---:|
| unità attive | 7 | 12 | +5 |
| slot disponibili | 161 | 275 | +114 |
| slot pianificati | 156 | 150 | -6 |
| MOVE pianificati | 65 | 59 | -6 |
| azioni produttive | 91 | 91 | 0 |

Le cinque unità aggiuntive accorciano l'instradamento di sei MOVE, ma non
ricevono nuovo lavoro produttivo. I 120 `PASS` annuali aggiuntivi sono
esattamente le cinque unità per i 24 turni di D10. Questo spiega perché il
salto di workforce è economicamente positivo ma molto inferiore al gap Top770.

## Evidenza pre-gate

Il confronto causale usa lo stesso seed `180903001`, gli stessi seat e lo
stesso avversario E18.16 del risultato congelato E18.22.

| Seat | E18.22 | E18.25 | Delta |
|---:|---:|---:|---:|
| 0 | 52.379 | 52.563 | +184 |
| 1 | 51.704 | 51.888 | +184 |
| mediana | 52.041,5 | 52.225,5 | +184 |

Il delta matched passa in entrambi i seat; struttura e composizione finali
sono esatte e gli errori controller sono zero. A D10 contro E18.16 E18.25 ha
12 unità reali e 1.337 di denaro, mentre E18.16 ha 12 unità e 2.105.

Nel testa-a-testa E18.25–E18.22 la mediana è 82.349 contro 67.524. Questo è
registrato come stress competitivo, non come stima causale: il diverso
comportamento simultaneo modifica prezzi e interazioni dell'episodio.

## Verdetto e prossima leva

Il gap di manodopera a D10 è recuperato, ma l'ipotesi “più hands da sole” è
insufficiente. Contro E18.16 la mediana resta 52.225,5 contro 78.959,5 e il
gate incumbent fallisce. Il successore deve mantenere le 12 unità D10 e
riempire la capacità liberata con cicli produttivi economicamente completi.

La prossima famiglia causale ammessa è quindi un replan D7–D10 con gate su:

1. HARVEST e unità crop monetizzate cumulative entro D10;
2. costo totale HIRE e denaro a fine D10;
3. nessuna regressione di FEED/CARE e composizione;
4. delta matched positivo in entrambi i seat.

Non sono ammessi ulteriori aumenti della manodopera senza task addizionali,
né modifiche simultanee a topologia, animali o procurement Wheat.

## Artefatti

- config: `configs/CODEX_E18_25_770_D10_LABOR_STEP_V1.json`;
- planner: `tools/e18_18_capacity_trajectory_planner.py`;
- controller: `tools/e18_25_d10_labor_step_controller.py`;
- test: `tests/test_codex_e18_25_d10_labor_step_controller.py`;
- runner: `tools/run_e18_25_770_d10_labor_step_gate.py`;
- piano: `artifacts/derived/E18_25_770_D10_LABOR_STEP_PLAN_V1.json`;
- risultato: `artifacts/derived/E18_25_770_D10_LABOR_STEP_PRE_GATE_V1.json`;
- report: `reports/E18_25_770_D10_LABOR_STEP_PRE_GATE_REPORT_IT.md`.
