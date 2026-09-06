# E18 — formato standard di confronto tra agenti V4

Adottato su richiesta del proprietario il 2026-09-06. Per i nuovi report
supera V3, mantenendo le definizioni V1–V3 salvo l'aggiunta seguente.

22 grafici D1–D30, sempre due serie: una versione candidata e un solo
riferimento Top770 identificato nel registro. Due colonne desktop, una mobile.
I primi 21 pannelli conservano ordine e significato; il pannello 22 è **CARE
riusciti per giorno**, distinto da FEED (21) e WATER (20). CARE non misura
direttamente il bonus prodotto e non sostituisce il controllo delle perdite.

WATER, FEED e CARE derivano dalle azioni eseguite verificate dal ledger, non
dalle richieste. Se la riconciliazione non è possibile, indicare N/D invece
di un falso zero. Cause PASS resta escluso dai grafici.

Riportare fonte/ID/hash, data, versione, numero di replay e criterio topologico.
Separare simulazioni interne e replay pubblici; curve di partite differenti
non diventano scontri diretti né confronti a parità di mercato. Mediana
puntuale e min–max osservato non sono una traiettoria reale o un intervallo
di confidenza. Restano obbligatorie tabelle, diagnosi e limiti del V1.

Un benchmark consultato entra nel registro come esposto: non riutilizzarlo
come prova indipendente per una release successiva. Sono preservati i report
storici, che non costituiscono nuovi test.

## Estensione V4.1 — capacità del terreno

Richiesta del proprietario del 2026-09-06: nel pannello 03 sovrapporre alle
tile coltivate le tile totali sbloccate, per confrontare l'acquisto di Q1 e Q2.
Rimangono 22 pannelli e due agenti. Nel solo pannello 03 ci sono quattro curve:
colore per agente, linea continua per coltivate e tratteggiata per totali.
Coltivate conserva la definizione PLANT, senza includere gli animali, già nel
pannello 04. Totali = 25 per quadrante sbloccato: Q0 25, +Q1 50, +Q2 75.
Non reinterpretare le tile coltivate come tutta la superficie occupata.

Il tooltip riporta entrambe le quantità per entrambi gli agenti. I gradini
seguono i checkpoint giornalieri già usati dal report; quando servono gli
orari precisi, verificarli nelle transizioni effettive dei replay, non nei
soli comandi BUY_LAND richiesti. La rigenerazione dello stesso corpus non
costituisce un nuovo ciclo di validazione del benchmark.
