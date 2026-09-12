# E20.2 / E20v32 — candidata locale

Base E20.1 (E20v28), topologia 7-7-2. Da D20, il pianificatore non genera nuove offerte CARE se il prezzo pubblico corrente del prodotto animale è al minimo (1). FEED, raccolta e gestione delle missioni già assegnate restano disponibili. Prima di D20 il comportamento è invariato.

È un'ipotesi di allocazione del lavoro: il prezzo corrente non garantisce il prezzo alla produzione. Non è una correzione dell'engine né una soluzione completa alla gestione della manodopera.

## Verifica locale

Due seed diagnostici già esposti (180910201, 180910203), entrambi i ruoli contro E18; quattro candidate e quattro controlli. Tutti completano 719 chiamate per agente senza errori core E20. Ogni controllo riproduce esattamente 263 transizioni dopo 456 azioni ricostruite per agente; anche le candidate coincidono nel prefisso. Bundle caricato senza `__file__`, topologia verificata a ogni passo.

Delta cassa: +2775, +4629, -907, -907; media +1397,5. Delta margine medio +865. Nessun aumento degli eventi di stress delle colture o delle fughe. CARE diminuisce in tutti i casi, ma PASS aumenta sul seed 201 e diminuisce sul 203: il lavoro liberato non è sistematicamente produttivo.

Stato: **DEVELOPMENT_SIGNAL_ONLY**, non promossa, non inviata. Due seed non bastano a dimostrare robustezza. E18 resta il riferimento esterno. Restano da completare le diagnosi su bonus CARE persi, acquisti di grano e FEED mancati. I seed riservati 180911301–307 non sono stati usati.

- [Protocollo](E20_2_PROTOCOL.md)
- [Report dei 22 KPI](reports/e20_2/REPORT.html)
- [Risultati per scontro](reports/e20_2/RESULT.json)
- [Bundle congelato](../../../../submission/submission_codex_e20_772_e20v32_candidate.py)

SHA256 bundle: `2e23faa7e581b0ab3a391da0e4707e49d04b6eebeaff4bdb495cacd9e91b317c`.

Riproduzione: `branch_e20_2.py`, poi `diagnose_e20_2.py` e `report_e20_2.py` nella cartella `tools`, usando un solo processo di simulazione. Conservare i risultati congelati prima di una nuova esecuzione.

Il report HTML usa il template leggibile dei 22 KPI già presente nel progetto. Verifica visiva non eseguita: apertura del file locale bloccata dalla policy del browser.
