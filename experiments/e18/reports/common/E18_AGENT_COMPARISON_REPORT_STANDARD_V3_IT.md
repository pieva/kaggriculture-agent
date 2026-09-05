# E18 — formato standard di confronto tra agenti V3

ADOTTATO su richiesta del proprietario del 2026-09-05. Supera V2 per i nuovi
report; mantiene definizioni, normalizzazioni e controlli di
[V1](E18_AGENT_COMPARISON_REPORT_STANDARD_V1_IT.md) e
[V2](E18_AGENT_COMPARISON_REPORT_STANDARD_V2_IT.md), salvo queste modifiche.

## Due serie, sempre

Ogni diagramma di confronto presenta **Top770 e una sola versione sotto
esame**. Non aggiungere il parent o altri agenti come terza linea, nemmeno
nascosta di default dietro un selettore. Per altre versioni usare report
separati; i risultati matched con il parent possono restare nelle tabelle.
Conservare il criterio topologico e il limite descrittivo del riferimento
pubblico: non sono partite a parità di mercato, seed e avversario.

## Ventuno pannelli standard

I pannelli 1–19 di V2 mantengono ordine e significato. Aggiungere:

| N. | Chiave | Definizione |
|---:|---|---|
| 20 | `WATER` | Azioni WATER riuscite nella giornata esecutiva, somma di tutte le unità |
| 21 | `FEED` | Azioni FEED riuscite nella giornata esecutiva, somma di tutte le unità |

Sono flussi giornalieri, non cumulate, non richieste e non tile/animali
presenti al checkpoint. Usare il ledger delle azioni eseguite e verificare
la somma contro i totali operativi. Un dato non auditabile è N/D; un conteggio
di richieste non va etichettato come eseguito. WATER non sostituisce il
pannello delle tile non irrigate, né FEED quello delle perdite animali.

Rimuovere il diagramma **Cause PASS**. I contatori grezzi possono restare
nei derivati per diagnosi puntuali, senza obbligo di mostrarli nel report.
Eventuali altri KPI pertinenti seguono i 21 standard, sempre a due serie
al massimo e con N/D espliciti.

## Interpretazione del miglioramento

Ridurre i PASS rispetto al parent non equivale a risolvere il gap con Top770.
Indicare finestra, totali medi per partita e quota sui comandi disponibili;
per l'indagine corrente evidenziare D15–D30. Non spostare date di acquisto
animali basandosi sulla cassa finale: verificare cassa impegnata, mangime,
pickup, collocazione e FEED entro le scadenze dell'apertura.

Questa decisione modifica il reporting, non autorizza nuovi test, upload,
promozioni, cambiamenti di policy o allineamento Git.
