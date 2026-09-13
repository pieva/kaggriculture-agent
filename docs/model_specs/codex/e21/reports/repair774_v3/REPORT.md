# 774 — primo round di ottimizzazione, Repair3

Ripreso il ramo774 su richiesta utente. Base Repair2 congelata, topologia7-7-4 con8mucche,9pecore,1oca e un pascolo vuoto. La vecchia774 storica esatta non è stata recuperata: Repair2 è la ricostruzione moderna già verificata. E20.8 e E20.9 preservate; nessuna submission, commit o push.

## Ipotesi e prova

Prima modifica isolata: D12–D28, su coltura presente non irrigata, sostituire PASS e servizi animali impropri con WATER. Sostituire FERTILIZE solo con un giorno di sete già osservato. Nessuna nuova tratta; apertura e finale invariati. Protocollo e hash scritti prima delle simulazioni. Quattro partite seriali contro E18 congelata, seed esposti301/303, entrambi ruoli. Non consumati seed riservati.

| Seed | Cassa R2 | Cassa R3 | Delta | Margine R2 su E18 | Margine R3 su E18 |
|---|---:|---:|---:|---:|---:|
|180911301|65391|65563|+172|−5164|−9108|
|180911303|63410|60082|−3328|−4622|−8857|

I due ruoli restituiscono gli stessi risultati: due scenari, non quattro repliche indipendenti. Media cassa−1578 e margine−4089,5 rispetto aR2. **Repair3 scartata come upgrade economico.** Il primo caso mostra perché non basta misurare la nostra cassa: +172 accompagnato da un aumento molto maggiore della cassa avversaria. I prezzi e il consumo dei negozi possono cambiare; non attribuire tutto alla sola resa delle caselle irrigate.

Nel primo scenario le perdite per sete rimangono25, WATER riusciti808→810. Il controllo dettagliato trova11caselle perdute senza visite nella giornata segnalata dall’audit; altre sono attraversate con comandi di movimento. File COVERAGE.json: posizioni e comandi completi per25eventi. Quindi la disponibilità di azioni sul posto non copre il fabbisogno delle colture. La correzione non ha risolto la fragilità ipotizzata.

## Direzione successiva

Conservare Repair2 come controllo774. Per la nuova implementazione costruire un calendario di missioni completo: prima di PLANT, assegnare almeno la prima irrigazione e la copertura delle giornate successive, poi raccolta/consegna; per colture esistenti prenotare il passaggio prima del secondo giorno senza acqua. Controllare la compatibilità con FEED, rientri e prossima tappa di ciascun lavoratore. Iniziare dai11buchi di visita documentati e dalla semina aH24 in(2,9), senza trasformare i movimenti in WATER senza prevedere il recupero del ritardo.

Misurare il ciclo fino a vendite/cassa: non assumere che ridurre le morti colturali basti a vincere. Nessuna estensione automatica dei pomodori dalla772; decisione varietale dopo aver coperto il lavoro. Un solo intervento coerente per volta, confronto conR2 e775 sugli stessi scenari, controllo del calendario negozi; holdout solo dopo congelamento.

Report HTML:22KPI e, subito sotto ogni produzione, volumi venduti, prezzi realizzati ponderati e prezzi mercato. Le due curve sono774R2 e774R3 in partite separate contro lo stesso E18; tabella dei margini inclusa. Verifica tecnica completa in VERIFICATION.json; nessuna nuova verifica visiva browser per precedente diniego URLpolicy, rispettato.
