# KPI del parametrico 770 V2 rispetto al campione E18.2 V4D

Confronto locale riprodotto il 2026-09-07. Due lati delle stesse 14 partite: sette seed development, entrambi i ruoli. Nessuna modifica alle strategie e nessun nuovo campione esterno consumato.

Il parametrico termina con cassa media **59.612**, contro **109.677** della V4D. Le 14 partite sono tutte sconfitte. Il riferimento è il campione effettivo, non un altro core parametrico.

## Lettura dei risultati e ipotesi Q0

**L’ipotesi di un avvio Q0 inadeguato è sostenuta dai dati, ma non ancora dimostrata come unica causa del divario.** Il deficit finale medio è -45,6% nel confronto diretto con la V4D.

Il bootstrap attuale è già pilotato: ammette solo WHEAT/CARROT e mantiene il tetto 2 COW/2 SHEEP fino a `first_confirmed_crop_harvest`. Questa guida impedisce proprio il portafoglio iniziale usato dal campione. Non basta quindi aggiungere più vincoli: occorre cambiare quelli economici e verificare l’effetto separatamente.

| Evidenza | Parametrico | V4D nella stessa partita |
|---|---:|---:|
| Meloni Q0 D1, media | 0,0 | 12,0 |
| Grano Q0 D1, media | 18,0 | 7,0 |
| COW D5, media | 2,0 | 4,0 |
| Primo raccolto meloni, giorno mediano (min–max) | 16,0 (16–16) | 11,0 (11–11) |
| Fragole D10, caselle medie | 0,3 | 20,0 |
| Vendite cumulate D15, media | 24.702 | 49.398 |
| Costo manovali D1–D10, media | 1.047 | 540 |

La maggiore liquidità iniziale del parametrico non è un vantaggio sufficiente: il campione investe prima nei meloni e prepara prima le fragole. Il ritardo dei raccolti osservato rende plausibile una propagazione del ritardo verso incassi e reinvestimenti. Anche la composizione successiva diverge: la sola correzione di D1 potrebbe non recuperare tutta la stagione.

**Controevidenza da conservare:** la vecchia variante E18 V19 (profilo V7, pesi grano:meloni 1:2) era già stata respinta: quattro casi, cassa 60.828 contro E18.16 e 57.245 contro E18.2, in entrambi i ruoli. Nel primo caso piantava già 10 meloni D1 e arrivava a 12 D2, ma D10 aveva 23 meloni, 11 grani e soltanto 1 fragola. È un core precedente, quindi non un’ablation causale di questa V2; dimostra però che ripetere soltanto il cambio dei pesi iniziali non è una soluzione già validata. Fonte: [gate V19](../../../e18/artifacts/derived/E18_CLOSEOUT_GATE_V19_INITIAL_PORTFOLIO_20260907.json) e [worklog E18](../../../e18/reports/E18_PARAMETRIC_RELEASE_WORKLOG_20260907_IT.md).

### Scomposizione contabile del divario finale

Differenze medie di contributo alla cassa: parametrico meno V4D. Un numero positivo aiuta il parametrico. Vendite e acquisti sono lordi: per esempio comprare e rivendere grano non va contato come ricavo netto.

| Componente | Contributo al divario |
|---|---:|
| Vendite | -64.052,0 |
| Acquisti | 14.834,3 |
| Manovali | -846,9 |
| Terreni | -0,0 |
| Operazioni sulle caselle | 0,0 |
| **Totale cassa finale** | **-50.064,6** |

### Guida iniziale da sottoporre a prova

1. Usare il portafoglio Q0 della V4D come ipotesi di partenza: 12 meloni, 7 grani e 2 COW/2 SHEEP iniziali, subordinati a budget e certificazione delle cure. Sono quantità osservate nel campione, non nuovi obiettivi già validati per ogni geometria.
2. Riservare esplicitamente capitale e capacità di lavoro per quel portafoglio; impedire che grano opportunistico riempia tutta Q0. Portare l’obiettivo di lavoro dai compiti effettivi, confrontando il costo con la V4D.
3. Verificare una transizione osservabile verso il portafoglio successivo, incluse mucche e fragole. Il primo raccolto di una coltura veloce, da solo, non certifica che l’impostazione economica sia quella desiderata.
4. Isolare gli effetti: A = core congelato; B = solo mix iniziale corretto; C = solo crescita bestiame/lavoro corretta; D = combinazione dopo aver misurato B e C. Stessi avversari, entrambi i ruoli, più campione non usato nel tuning prima di una promozione.
5. Mantenere V4D come gate competitivo. Richiedere sicurezza, flussi di cassa riconciliati e risultati diretti competitivi; non promuovere una variante perché batte soltanto la 770 o la 662 deboli.

**In questo lavoro non sono state modificate né pubblicate strategie.** Le proposte sono esperimenti da progettare dopo questi report.

![Trend KPI 770](770_trend.png)

## Metodo e perimetro

- Modello: `submission/submission_codex_e19_control_770_v2.py`. Profilo iniziale e core congelati V2; per 770 si usa il controllo sullo stesso core della E19 V2, non la vecchia E18 V24.
- Campione: `submission/submission_codex_e18_2_capacity_governed_v4d.py`, invariato.
- Seed 180903001–180903007, seat 0 e 1. Ogni partita riproduce hash di tutte le azioni e ricavi finali del gate precedente.
- Cassa di entrambi i giocatori ricostruita dal motore per 719 batch per partita; nessuna discrepanza ammessa.
- Stock e Q0 ai checkpoint indice D×24−1: ultima osservazione prima del refresh, con D30 terminale. I flussi giornalieri coprono tutti i batch del giorno: possono includere un batch successivo al checkpoint dello stock.
- Curve = medie; bande = minimo/massimo, non intervalli di confidenza. Q0 = quadrante NW, coordinate x,y da 0 a 4. Mappe = un caso dichiarato, non una configurazione media.
- Le due serie V4D dei due report sono i rispettivi avversari effettivi: non vanno unite fingendo identiche condizioni di mercato. Il test descrive differenze; non identifica da solo una causa.

## Avvio D1–D10

![Avvio 770](770_startup.png)

| Giorno | Cassa param./V4D | COW param./V4D | SHEEP param./V4D | Colture param./V4D | Manovali param./V4D | Incassi cumulati param./V4D |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 819,0 / 20,0 | 2,0 / 2,0 | 2,0 / 2,0 | 21,0 / 19,0 | 7,0 / 5,0 | 0,0 / 224,0 |
| 2 | 1.102,0 / 235,0 | 2,0 / 2,0 | 2,0 / 2,0 | 21,0 / 19,0 | 1,0 / 4,0 | 398,0 / 709,0 |
| 3 | 962,0 / 200,0 | 2,0 / 3,0 | 2,0 / 2,0 | 21,0 / 17,0 | 6,0 / 4,0 | 398,0 / 1.131,0 |
| 4 | 662,4 / 244,0 | 2,0 / 3,0 | 3,0 / 2,0 | 20,0 / 19,0 | 9,0 / 5,0 | 996,4 / 1.607,0 |
| 5 | 772,4 / 649,9 | 2,0 / 4,0 | 3,0 / 2,0 | 6,0 / 19,0 | 6,0 / 4,0 | 2.280,0 / 2.237,0 |
| 6 | 495,0 / 840,3 | 2,0 / 4,0 | 5,0 / 2,0 | 9,6 / 19,0 | 9,0 / 5,0 | 3.508,3 / 2.839,4 |
| 7 | 1.402,9 / 510,6 | 4,0 / 6,0 | 5,0 / 2,0 | 20,7 / 31,0 | 9,4 / 8,0 | 6.222,0 / 5.671,4 |
| 8 | 779,3 / 609,4 | 5,0 / 8,0 | 5,0 / 2,0 | 25,6 / 36,9 | 9,4 / 8,0 | 6.807,7 / 7.153,3 |
| 9 | 3.039,0 / 978,1 | 5,3 / 8,0 | 5,0 / 4,0 | 27,1 / 36,9 | 9,7 / 10,0 | 9.774,0 / 9.787,3 |
| 10 | 1.733,4 / 2.480,9 | 7,6 / 8,0 | 5,0 / 4,0 | 27,1 / 36,9 | 12,0 / 11,0 | 12.456,9 / 12.375,1 |

## Q0: composizione e geometria

![Composizione Q0 770](770_q0.png)

![Mappa Q0 770](770_q0_map.png)

| Giorno / modello | Grano Q0 | Carote Q0 | Meloni Q0 | Pomodori Q0 | Fragole Q0 | Animali Q0 |
|---|---:|---:|---:|---:|---:|---:|
| D1 770 | 18,0 | 3,0 | 0,0 | 0,0 | 0,0 | 4,0 |
| D1 V4D | 7,0 | 0,0 | 12,0 | 0,0 | 0,0 | 4,0 |
| D3 770 | 18,0 | 3,0 | 0,0 | 0,0 | 0,0 | 4,0 |
| D3 V4D | 5,0 | 0,0 | 12,0 | 0,0 | 0,0 | 5,0 |
| D5 770 | 4,0 | 0,0 | 2,0 | 0,0 | 0,0 | 5,0 |
| D5 V4D | 7,0 | 0,0 | 12,0 | 0,0 | 0,0 | 6,0 |
| D7 770 | 2,9 | 0,3 | 7,7 | 0,9 | 0,0 | 6,7 |
| D7 V4D | 2,0 | 0,0 | 12,0 | 0,0 | 4,0 | 6,0 |
| D10 770 | 1,6 | 0,0 | 12,6 | 0,9 | 0,0 | 7,0 |
| D10 V4D | 1,9 | 0,0 | 12,0 | 0,0 | 5,0 | 6,0 |

## Impiego del capitale e vendite

Valori cumulati medi, su giornate complete. La voce operazioni sulle caselle include costruzioni e altri effetti monetari delle azioni.

| Termine / modello | Vendite | Acquisti totali | Animali | Semi | Grano comprato | Manovali | Terreni | Operazioni caselle (saldo) | Cassa riconciliata |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| D1 770 | 0 | 2.148 | 1.800 | 240 | 108 | 33 | 0 | 0 | 819 |
| D1 V4D | 224 | 3.192 | 1.800 | 1.030 | 362 | 12 | 0 | 0 | 20 |
| D5 770 | 2.280 | 3.346 | 2.300 | 400 | 646 | 162 | 1.000 | 0 | 772 |
| D5 V4D | 2.237 | 4.542 | 2.600 | 1.130 | 812 | 45 | 0 | 0 | 650 |
| D10 770 | 12.457 | 9.615 | 5.529 | 2.217 | 1.869 | 1.047 | 2.857 | 0 | 1.938 |
| D10 V4D | 12.375 | 11.354 | 5.200 | 3.270 | 2.528 | 540 | 1.000 | 0 | 2.481 |
| D20 770 | 48.415 | 17.053 | 6.100 | 4.575 | 6.378 | 4.807 | 3.000 | 0 | 26.554 |
| D20 V4D | 82.817 | 28.577 | 9.000 | 6.320 | 11.767 | 4.156 | 3.000 | 0 | 50.083 |
| D30 770 | 91.235 | 23.092 | 6.100 | 4.669 | 12.324 | 8.530 | 3.000 | 0 | 59.612 |
| D30 V4D | 155.287 | 37.927 | 9.000 | 6.980 | 19.940 | 7.683 | 3.000 | 0 | 109.677 |

### Origine degli incassi nella stagione

Vendite lorde medie per prodotto. Il grano comprende compravendite, non solo produzione propria; confrontarlo insieme alla spesa per grano della tabella precedente.

| Prodotto | Parametrico | V4D | Differenza |
|---|---:|---:|---:|
| WHEAT | 2.707 | 17.047 | -14.339 |
| CARROT | 757 | 0 | 757 |
| MELON | 13.845 | 17.524 | -3.679 |
| TOMATO | 3.586 | 0 | 3.586 |
| STRAWBERRY | 24.594 | 44.892 | -20.297 |
| MILK | 19.489 | 32.872 | -13.383 |
| WOOL | 16.059 | 24.998 | -8.939 |
| FERTILIZER | 10.197 | 16.732 | -6.535 |

### Composizione produttiva dopo l’avvio

| Giorno / modello | Grano | Carote | Meloni | Pomodori | Fragole | COW | SHEEP |
|---|---:|---:|---:|---:|---:|---:|---:|
| D10 770 | 4,0 | 0,0 | 21,1 | 1,7 | 0,3 | 7,6 | 5,0 |
| D10 V4D | 4,9 | 0,0 | 12,0 | 0,0 | 20,0 | 8,0 | 4,0 |
| D15 770 | 0,7 | 0,0 | 21,9 | 3,3 | 20,1 | 9,0 | 5,0 |
| D15 V4D | 14,0 | 0,0 | 8,0 | 0,0 | 30,0 | 8,0 | 10,0 |
| D20 770 | 0,0 | 0,0 | 6,5 | 5,3 | 20,1 | 9,0 | 5,0 |
| D20 V4D | 9,0 | 0,0 | 8,0 | 0,0 | 37,9 | 8,0 | 10,0 |
| D25 770 | 1,6 | 0,0 | 0,0 | 4,0 | 20,1 | 9,0 | 5,0 |
| D25 V4D | 31,0 | 0,0 | 0,0 | 0,0 | 20,9 | 8,0 | 10,0 |
| D30 770 | 0,0 | 0,6 | 0,0 | 1,6 | 4,7 | 9,0 | 5,0 |
| D30 V4D | 0,9 | 0,0 | 0,0 | 0,0 | 13,9 | 8,0 | 10,0 |

### Stato finale e controlli

| Modello | Pascoli Q0/Q1/Q2/Q3 medi | Perdite colture totali | Fughe animali totali |
|---|---|---:|---:|
| 770 | 7,0/7,0/0,0/0,0 | 0 | 0 |
| V4D | 7,0/7,0/5,0/0,0 | 308 | 0 |

## Trend completo D1–D30

| Giorno | Cassa param./V4D | FEED param./V4D | CARE param./V4D | WATER param./V4D | HARVEST param./V4D | MOVE param./V4D | PASS % param./V4D |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 819,0 / 20,0 | 4,0 / 2,0 | 4,0 / 4,0 | 21,0 / 19,0 | 0,0 / 0,0 | 58,0 / 41,0 | 31,5 / 26,1 |
| 2 | 1.102,0 / 235,0 | 4,0 / 4,0 | 4,0 / 4,0 | 0,0 / 4,0 | 0,0 / 0,0 | 9,0 / 24,0 | 19,4 / 59,5 |
| 3 | 962,0 / 200,0 | 4,0 / 4,0 | 1,0 / 4,0 | 21,0 / 22,0 | 0,0 / 6,0 | 72,0 / 40,0 | 15,4 / 24,1 |
| 4 | 662,4 / 244,0 | 5,0 / 3,0 | 5,0 / 5,0 | 23,0 / 20,0 | 3,0 / 1,0 | 85,0 / 61,0 | 15,6 / 20,1 |
| 5 | 772,4 / 649,9 | 5,0 / 5,0 | 5,0 / 6,0 | 18,0 / 10,0 | 14,0 / 3,0 | 60,0 / 42,0 | 21,2 / 31,9 |
| 6 | 495,0 / 840,3 | 7,0 / 6,0 | 6,3 / 6,0 | 9,6 / 23,0 | 0,0 / 4,0 | 69,0 / 48,0 | 28,0 / 26,3 |
| 7 | 1.402,9 / 510,6 | 9,0 / 8,0 | 8,0 / 8,0 | 11,1 / 28,0 | 2,0 / 5,0 | 46,6 / 102,0 | 42,3 / 7,7 |
| 8 | 779,3 / 609,4 | 10,0 / 7,0 | 7,6 / 10,0 | 14,7 / 28,9 | 0,3 / 0,0 | 110,7 / 88,0 | 21,3 / 18,4 |
| 9 | 3.039,0 / 978,1 | 9,3 / 11,0 | 7,0 / 12,0 | 16,1 / 39,9 | 2,1 / 7,0 | 98,6 / 113,0 | 27,1 / 13,8 |
| 10 | 1.733,4 / 2.480,9 | 11,4 / 12,0 | 10,5 / 12,0 | 20,7 / 40,9 | 6,6 / 5,9 | 120,9 / 105,0 | 21,7 / 24,1 |
| 11 | 1.936,4 / 18.924,4 | 13,6 / 12,0 | 12,1 / 12,0 | 23,5 / 21,0 | 4,3 / 15,0 | 141,2 / 120,0 | 17,4 / 20,0 |
| 12 | 3.220,2 / 16.523,1 | 13,6 / 17,9 | 11,2 / 19,0 | 23,9 / 45,9 | 3,3 / 1,0 | 148,5 / 130,0 | 16,5 / 5,7 |
| 13 | 4.853,6 / 18.855,0 | 12,3 / 19,0 | 9,5 / 19,0 | 25,0 / 15,9 | 5,0 / 10,9 | 163,5 / 108,0 | 14,5 / 29,0 |
| 14 | 4.793,4 / 19.919,1 | 11,1 / 18,0 | 9,6 / 18,0 | 33,6 / 49,0 | 0,6 / 3,0 | 174,7 / 155,0 | 11,4 / 4,4 |
| 15 | 7.180,1 / 24.052,0 | 12,6 / 19,0 | 11,5 / 19,0 | 30,3 / 30,0 | 8,6 / 13,0 | 165,0 / 144,0 | 9,8 / 5,1 |
| 16 | 10.456,9 / 27.635,4 | 10,0 / 17,0 | 8,4 / 19,0 | 31,4 / 41,0 | 6,9 / 18,0 | 191,1 / 144,0 | 6,3 / 1,4 |
| 17 | 12.239,6 / 31.847,8 | 11,9 / 19,0 | 11,1 / 19,0 | 30,3 / 26,9 | 6,7 / 12,0 | 173,4 / 138,0 | 8,3 / 8,8 |
| 18 | 16.632,3 / 37.966,0 | 10,9 / 17,0 | 8,9 / 19,0 | 31,9 / 29,0 | 9,1 / 21,0 | 182,6 / 168,0 | 6,7 / 0,0 |
| 19 | 24.081,7 / 46.495,1 | 10,5 / 17,0 | 8,1 / 17,0 | 28,9 / 31,9 | 13,9 / 22,0 | 178,6 / 151,0 | 6,4 / 2,0 |
| 20 | 26.249,0 / 49.636,4 | 10,9 / 19,0 | 8,2 / 19,0 | 23,9 / 35,0 | 9,4 / 15,0 | 181,9 / 144,0 | 7,8 / 3,7 |
| 21 | 28.875,3 / 56.980,8 | 11,1 / 19,0 | 9,1 / 18,0 | 22,2 / 28,9 | 12,9 / 25,0 | 178,9 / 148,0 | 7,3 / 1,7 |
| 22 | 32.725,3 / 63.527,8 | 10,8 / 19,0 | 7,4 / 19,0 | 17,9 / 35,0 | 17,4 / 17,0 | 176,2 / 153,0 | 7,7 / 0,3 |
| 23 | 35.542,4 / 70.632,4 | 11,4 / 19,0 | 8,6 / 19,0 | 16,8 / 17,9 | 14,8 / 21,0 | 181,5 / 162,0 | 7,4 / 1,4 |
| 24 | 39.515,4 / 75.055,2 | 12,6 / 16,0 | 8,0 / 18,0 | 15,4 / 35,0 | 16,4 / 19,0 | 179,1 / 133,0 | 7,4 / 0,0 |
| 25 | 44.071,9 / 78.774,9 | 11,9 / 18,0 | 8,6 / 18,0 | 15,3 / 25,9 | 18,9 / 17,0 | 176,5 / 146,0 | 7,3 / 1,7 |
| 26 | 47.220,4 / 83.195,4 | 10,9 / 17,0 | 7,1 / 18,0 | 15,9 / 41,9 | 15,8 / 15,0 | 184,8 / 142,0 | 7,4 / 1,0 |
| 27 | 51.385,1 / 89.588,1 | 11,9 / 18,0 | 8,9 / 19,0 | 14,8 / 30,0 | 18,2 / 22,9 | 174,9 / 144,0 | 7,8 / 1,0 |
| 28 | 55.316,0 / 92.526,5 | 12,9 / 16,0 | 4,4 / 17,0 | 12,1 / 44,9 | 19,8 / 21,0 | 165,1 / 133,0 | 13,0 / 1,4 |
| 29 | 57.718,0 / 96.809,9 | 12,8 / 19,0 | 0,0 / 0,0 | 6,0 / 12,0 | 12,5 / 27,9 | 132,8 / 219,1 | 29,8 / 0,0 |
| 30 | 59.612,3 / 109.676,9 | 11,1 / 0,0 | 0,0 / 0,0 | 6,8 / 0,0 | 11,4 / 38,1 | 83,5 / 149,3 | 21,2 / 17,0 |

## Dati e riproducibilità

Aggregati: [770_aggregates.json](770_aggregates.json). Dati per partita: `../../artifacts/derived/paired_kpi_v4d_20260907/770_SEED_SEAT.json`.
Bundle parametrico SHA256: `73d27802df67901afdf71c7f27230b1527b9a145557340274238285db6a033ef`.
Campione SHA256: `c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7`.
Runner `tools/run_paired_kpi_v4d.py`; generatore `tools/build_paired_kpi_reports.py`. Le osservazioni interpretative sono nel riepilogo iniziale aggiunto dopo l’esame dei risultati.
