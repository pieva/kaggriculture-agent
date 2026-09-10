# D20-D30: ripianificazione oraria della manodopera

6 casi appaiati contro E18. Delta cassa medio: +680.7 (+1.11%). Nessuna promozione su questo campione di sviluppo.

| Modello | Cassa finale | MOVE D20-D30 | PASS D20-D30 | WATER D20-D30 | Costo manovali D20-D30 | Coltivate: somma checkpoint D20-D30 |
|---|---:|---:|---:|---:|---:|---:|
| E20.1 | 61,571.7 | 1654.3 | 251.3 | 298.0 | 3765.0 | 419.7 |
| E20v29 | 62,252.3 | 1655.3 | 239.7 | 301.3 | 3767.0 | 421.7 |

| Seed | Ruolo | E20.1 | E20v29 | Delta |
|---|---:|---:|---:|---:|
| 180910101 | 1 | 62498.0 | 62020.0 | -478.0 |
| 180910102 | 1 | 47507.0 | 50100.0 | +2593.0 |
| 180910103 | 1 | 74710.0 | 74637.0 | -73.0 |
| 180910101 | 0 | 62498.0 | 62020.0 | -478.0 |
| 180910102 | 0 | 47507.0 | 50100.0 | +2593.0 |
| 180910103 | 0 | 74710.0 | 74637.0 | -73.0 |

Tutte le azioni prima di D20 identiche al controllo. Entrambi gli agenti ricevono 719 chiamate; nessun errore del core E20v29. Missioni attive conservate, costi residui sottratti ai budget. D30 conserva il gestore terminale originale. PASS e MOVE sono comandi richiesti; WATER/FEED/CARE sono esecuzioni verificate.

[Protocollo](PROTOCOL.md) Ã‚Â· [Dati completi](RESULT.json)

## Decisione

Non adottare E20v29 come nuova versione ufficiale. I ruoli invertiti restituiscono risultati identici: il campione contiene tre seed distinti, non sei repliche indipendenti. Il guadagno medio di 680,7 (+1,11%) dipende da un solo seed; lo stress medio sale da 2,33 a 3,00 e gli spostamenti non diminuiscono.

La diagnosi esterna D20-D30 mostra MOVE al 49-65% delle opportunita di comando fra D20 e D28, contro PASS generalmente al 4-10%. A D29-D30 i PASS salgono al 16-17%. Queste percentuali non misurano da sole inattivita evitabile: comprendono anche vincoli di posizione, materiali e scadenze.

Prossimo esperimento proposto: mantenere le assegnazioni valide e trasferire soltanto lavoro residuo a un lavoratore libero quando puo completarlo con minor costo di viaggio, verificando materiali, budget e conflitti. Il trasferimento non e implementato in questa variante. E20.1 pubblicata resta invariata; nessuna nuova submission.
