# D20-D30: trasferimento mirato del lavoro residuo

6 casi appaiati contro E18. Delta cassa medio: +0.0 (+0.00%). Nessuna promozione su questo campione di sviluppo.

| Modello | Cassa finale | MOVE D20-D30 | PASS D20-D30 | WATER D20-D30 | Costo manovali D20-D30 | Coltivate: somma checkpoint D20-D30 |
|---|---:|---:|---:|---:|---:|---:|
| E20.1 | 61,571.7 | 1654.3 | 251.3 | 298.0 | 3765.0 | 419.7 |
| E20v30 | 61,571.7 | 1654.3 | 251.3 | 298.0 | 3765.0 | 419.7 |

| Seed | Ruolo | E20.1 | E20v30 | Delta |
|---|---:|---:|---:|---:|
| 180910101 | 1 | 62498.0 | 62498.0 | +0.0 |
| 180910102 | 1 | 47507.0 | 47507.0 | +0.0 |
| 180910103 | 1 | 74710.0 | 74710.0 | +0.0 |
| 180910101 | 0 | 62498.0 | 62498.0 | +0.0 |
| 180910102 | 0 | 47507.0 | 47507.0 | +0.0 |
| 180910103 | 0 | 74710.0 | 74710.0 | +0.0 |

Tutte le azioni prima di D20 identiche al controllo. Entrambi gli agenti ricevono 719 chiamate; nessun errore del core E20v30. Missioni attive conservate, costi residui sottratti ai budget. D30 conserva il gestore terminale originale. PASS e MOVE sono comandi richiesti; WATER/FEED/CARE sono esecuzioni verificate.

[Protocollo](PROTOCOL.md) Ãƒâ€šÃ‚Â· [Dati completi](RESULT.json)

## Esito e diagnosi

E20v30 non adottata. Tutti i comandi coincidono con E20v28 in tutti e sei i confronti (tre seed distinti). Due trasferimenti provvisori di coda, uno per ciascun ruolo del seed 180910101, non cambiano le azioni finali: nessun beneficio economico o operativo dimostrato.

Nel replay di controllo seed 180910101, ruolo 0, la strumentazione riproduce 719 azioni esatte. Dei 209 PASS D20-D30, 161 si concentrano nelle ore 22-24 (77,0%). Sono opportunita per lavoratore, non ore di calendario.

- 194 PASS: tutti i tentativi osservati di preparazione delle attivita vengono rifiutati; 164 di questi con coda vuota, 30 con coda residua.
- 7 PASS: missione attiva in attesa, tre PICKUP di grano e quattro PLANT di grano.
- 3 PASS: almeno una preparazione disponibile ma nessuna assegnazione finale.
- 5 PASS: nessun tentativo di preparazione osservato.

Le categorie descrivono le decisioni effettive. Non provano che ciascun PASS fosse evitabile, ne distinguono ancora tutti i rifiuti per tempo, materiali e riserve. Il campione diagnostico e un solo replay.

Prossima ipotesi: pianificazione della chiusura giornaliera, anticipando i percorsi lunghi e riservando servizi brevi per il tempo residuo, con budget che includa l'eventuale rientro al deposito. Prima di implementarla distinguere i rifiuti di preparazione per causa e identificare le attivita che una diversa sequenza avrebbe reso completabili. Nessuna nuova submission o modifica a E20.1 pubblicata.

[Diagnostico completo](ADMISSION_DIAGNOSTIC.json) · [Fonti e hash](manifest.json).
