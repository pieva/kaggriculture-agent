# E18.28 C — verifica full-season 770

2026-09-05. Candidata diagnostica quotidiana, non promossa a incumbent. Matrice development: 7 seed × 2 seat, stesso avversario E18.16; nessun holdout. Confronto Top770 pubblico/locale descrittivo, non causale (mercati e avversari diversi).

## Risultati economici matched

| Variante | Cassa finale media | Min–max | Vittorie su E18.16 |
|---|---:|---:|---:|
| PARENT | 69,156.00 | 41,141–92,680 | 0/14 |
| B | 72,343.57 | 42,601–97,519 | 0/14 |
| C | 74,491.57 | 51,338–96,030 | 1/14 |

| Seed | Seat | Parent E18.27 V3 | B Wheat | C Carrot | C−parent | C−B |
|---|---:|---:|---:|---:|---:|---:|
| 180903001 | 0 | 74,287 | 77,434 | 77,898 | +3,611 | +464 |
| 180903001 | 1 | 74,287 | 77,434 | 77,898 | +3,611 | +464 |
| 180903002 | 0 | 66,154 | 69,729 | 69,773 | +3,619 | +44 |
| 180903002 | 1 | 66,154 | 69,729 | 69,773 | +3,619 | +44 |
| 180903003 | 0 | 52,684 | 54,865 | 61,940 | +9,256 | +7,075 |
| 180903003 | 1 | 52,684 | 54,865 | 61,940 | +9,256 | +7,075 |
| 180903004 | 0 | 48,427 | 50,386 | 59,438 | +11,011 | +9,052 |
| 180903004 | 1 | 41,141 | 42,601 | 51,338 | +10,197 | +8,737 |
| 180903005 | 0 | 90,769 | 95,066 | 93,875 | +3,106 | -1,191 |
| 180903005 | 1 | 90,146 | 94,441 | 93,250 | +3,104 | -1,191 |
| 180903006 | 0 | 92,680 | 97,519 | 96,030 | +3,350 | -1,489 |
| 180903006 | 1 | 92,680 | 97,519 | 96,030 | +3,350 | -1,489 |
| 180903007 | 0 | 67,924 | 70,617 | 71,963 | +4,039 | +1,346 |
| 180903007 | 1 | 58,167 | 60,605 | 61,736 | +3,569 | +1,131 |

C guadagna 5,335.57 (7.72%) sul parent, minimo +3,104. C−B medio +2.148; due seed hanno delta negativo: nessuna regola condizionata al seed è stata introdotta.

## Carote: attribuzione economica B/C

Stesso calendario nominale, route e servizio; cambia la specie delle nuove semine D26-D28. Tabella seguente: flussi medi dell'intera partita (i delta B/C derivano dal trattamento tardivo). I prezzi reagiscono anche alle nostre vendite: ricavi per specie non equivalgono a prezzi esogeni.

| Voce | B Wheat | C Carrot | Delta C−B |
|---|---:|---:|---:|
| harvested:CARROT | 0.00 | 83.00 | +83.00 |
| harvested:WHEAT | 590.43 | 507.43 | -83.00 |
| hire_cash | 6,858.00 | 6,858.00 | +0.00 |
| planted:CARROT | 0.00 | 32.00 | +32.00 |
| planted:WHEAT | 162.71 | 130.71 | -32.00 |
| purchase_cash:BUY_SEED:CARROT | 0.00 | 640.00 | +640.00 |
| purchase_cash:BUY_SEED:WHEAT | 1,627.14 | 1,307.14 | -320.00 |
| sales_cash:CARROT | 0.00 | 6,315.14 | +6,315.14 |
| sales_cash:WHEAT | 21,855.07 | 18,007.93 | -3,847.14 |
| sold_units:CARROT | 0.00 | 83.00 | +83.00 |
| sold_units:WHEAT | 474.29 | 391.29 | -83.00 |

Tutti i delta di cassa sono riconciliati con vendite/acquisti/personale/terra/azioni. A D30: zero prodotti su tile, nello shed o trasportati, zero semi residui in tutti i 14 casi C. Non è un aumento puramente contabile delle consistenze.

## Traiettoria e sicurezza

12 hands + farmer mantenuti D25-D30 in tutti i casi C. Nuovi annuali D26-D28, raccolti a età 3 o 2 al terminale, prenotazione rotte entro H23 D30, nessun DIG finale senza resa. D1-D24 congelato rispetto a E18.27 V3, compreso il lookahead di mercato. Nel seed smoke le crop H24 D25-D30 sono 61,60,58,61,23,0 (parent 61,51,39,29,0,0). Anche Top770 liquida D29-D30: mantenere produzione fino a D30 non significa lasciare crop invendute al terminale.

Zero errori, fughe, violazioni cap 14/max 12 hands e strutture nel quadrante agricolo in tutti i 14 casi. Resta il posto Sheep vuoto ereditato sul seed 180903007. La candidata perde 13/14 contro E18.16; smoke E18.2/V4D 60.612 contro 85.329 in entrambi i seat. Vantaggio sul parent, non dimostrazione di competitività da top.

## Apertura progressiva: tentativi respinti

D anticipa Q0 a D3/D5 e Q1 a D8/D9/D10. E posticipa la terza Cow a D4 e attiva JIT/inflight da D1. Entrambi perdono una Sheep nello smoke: rispettivamente cassa 74.300 e 69.912 contro C 77.898. L'anticipo altera cash disponibile, pickup e servizio FEED; il piano nominale non basta. La release C conserva l'apertura a step. Il requisito della crescita progressiva resta aperto, non viene dichiarato implementato.

## Report standard a 19 pannelli

Cassa, persone, totale crop/animali, tutte le 5 colture e 3 specie, pascoli/COOP vuoti, MOVE e PASS per giornata, non irrigate H24, perdite animali verificate, WEED H24. Mancata irrigazione nel grafico è uno stato di servizio: H24 D1-D29 precede l'ultimo batch e non prova un danno o una scadenza mancata. WEED non significa automaticamente sete (esaurimento e spawn casuale sono distinti). Linea mediana, fascia min-max osservata; C n=14, Top770 n=5, campione pubblico final-770 congelato.

Grafici: `E18_28_TOP770_D01_D30_KPI_19.html`. Dati: `../artifacts/derived/E18_28_C_TOP770_D01_D30_KPI_19.json`. Standard comune: `experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V2_IT.md`.

## Rilascio e conservazione

Standalone stdlib-only, source hash e piano nel manifest; parity 719 azioni per seat e loader file Kaggle, 27 test unitari/regressione superati. Il dossier dei 22 download riscaricabili conserva URL, ID, seed, reward, SHA-256 e dimensione; i derivati restano. NEW_SESSION/PROJECT_STATE, pulizia conclusiva e Git sono differiti ai primi cicli esterni. Nessuna promozione automatica o tuning sullo score iniziale.
