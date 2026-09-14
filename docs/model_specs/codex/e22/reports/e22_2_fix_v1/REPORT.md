# E22.2 fix v1 — correzioni e verifica locale

Nuovo bundle autonomo `submission_codex_e22_2_fix_v1.py`; E22.2 pubblicata (56212495) resta immutata. Pubblicata il 14 settembre 2026: [submission 56228129](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56228129), stato Complete; rating iniziale non stabilizzato.

Correzioni: vendita condizionale prima delle assunzioni non finanziate; recupero del pasto D2 della mucca centrale e riallineamento della rotta; rimozione infestanti e semina nel successivo slot WATER; rispetto delle sementi disponibili per evitare il blocco atomico; uso di slot inattivi/ridondanti per cibo, cura e acqua; spazio per il rientro notturno; consegna e vendita delle scorte finali. Restano il mix 8C9S e i tre pascoli Q0.

| Controllo nei 20 scenari | Pubblicata | Fix v1 |
|---|---:|---:|
| Fughe | 0 | 0 |
| Batch con lavoratori mancanti | 46 | 0 |
| Semine senza effetto | 6 | 0 |
| Giorni-animale senza pasto | 576 | 480 |
| Colture trasformate in infestanti dopo stress | 40 | 0 |
| Fertilizzante finale non venduto | 40 | 0 |
| Scarti al rientro notturno | {'WHEAT': 18, 'FERTILIZER': 2, 'WOOL': 24} | {} |

**8C9S in tutti i 20 scenari corretti**, senza animali bloccati, fughe o prodotti animali raccolti e poi persi. Risolte anche la risemina del grano D16 senza irrigazione e la perdita della fragola dopo il passaggio D21. Rimangono giornate senza pasto: questa è una correzione delle anomalie riproducibili, non una riscrittura completa del calendario. I comandi innocui ridondanti non sono tutti eliminati.

Confronto diretto con E22.1, 7 semi già esposti × 2 lati: fix **4/14 vittorie**, margine medio **-180.3**, mediano **-2738.0**. E22.2 pubblicata sugli stessi casi: 4/14, medio +353.1, mediano -2092.0. Tutte le 14 partite del fix chiudono 8C9S senza fughe.

Metodo: i 20 avversari esterni sono riprodotti mediante le loro azioni registrate, senza disporre del loro codice. Il motore ricalcola esiti e prezzi; sono prove diagnostiche, non stime di rating. Il controllo riutilizza i replay originali già auditati (campo `source`); ogni scenario del candidato finale viene eseguito nel loader Kaggle. Il test diretto usa invece i due bundle reali. Nessun seme riservato è stato usato.

22 KPI standard + 9 pannelli volumi + 9 prezzi realizzati. Parità contabile, 719 azioni per lato e riconciliazione dei prodotti controllate; gli scarti notturni sono verificati nel motore su 29 refresh per partita.

[Report interattivo](REPORT.html) · [Riepilogo](SUMMARY.json) · [Scarti](OVERFLOW.json) · [CSV KPI e prezzi](DAILY_22_KPI_PRICES.csv) · [Confronti diretti](direct/RESULTS.json).
