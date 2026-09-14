# E22 — replay e variante Q0

Storico congelato: 78 partite pubbliche concluse, 46 vittorie, 32 sconfitte, 0 pareggi. Rating dopo l’ultimo episodio 108602447: 2223.9; massimo osservato 2279.6. Il rating varia nel tempo e non coincide con la cassa di una partita.

Audit dettagliato di 20 replay: 16 posizioni equidistanti nello storico, tre episodi segnalati e i margini estremi, senza duplicati. Campione diagnostico selezionato, non stima imparziale della frequenza delle strategie. Cassa verificata a ogni transizione per entrambi i giocatori: zero discrepanze. I KPI monetari seguono il giorno dell’azione; le mappe e la cassa sono osservazioni H24, prima dell’ultima azione del giorno quando presente.

Nell’episodio 108561064, la submission 56165125 sostituisce effettivamente con pascoli le coordinate (4,1), (3,2), (2,3), e mantiene il pollaio vuoto (3,7) in Q2. Coordinate zero-based: Q0 = x<5,y<5; Q2 = x<5,y>=5. E22 termina con {'GOOSE': 3, 'COW': 8, 'SHEEP': 6}, l’avversario con {'SHEEP': 10, 'COW': 6}. Cassa 121.069 contro 130.059, differenza 8.990. Il confronto comprende anche altre differenze del mix e del calendario: non isola l’effetto dei soli tre pascoli.

## Scomposizione del margine avversario nel caso 108561064

- Ricavi WOOL: +16,393 monete.
- Ricavi EGG: -4,366 monete.
- Ricavi MILK: -1,303 monete.
- Ricavi FERTILIZER: -1,239 monete.
- Ricavi WHEAT: -895 monete.
- Ricavi STRAWBERRY: -358 monete.
- Ricavi CARROT: -17 monete.
- Ricavi MELON: +0 monete.
- Effetto purchases: +2,118 monete.
- Effetto labor: -1,343.0 monete.
- Effetto land: +0.0 monete.
- Effetto unit_cash: +0.0 monete.

La somma è esattamente +8.990, ma è una scomposizione contabile, non l’effetto causale dei soli pascoli.

[Grafici sui 30 giorni e selettore replay](REPORT.html). [Dati sintetici](SUMMARY.json).
