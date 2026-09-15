# E24 — E22.1 e top: economia delle colture

Report: http://127.0.0.1:8772/crop_economics_20260915/REPORT.html

Campione congelato il 14 settembre: 20 replay E22.1 (56228842) e 8 ciascuno Catalyst (56218385), Thomas Tschinkel (56222223), Deodims (56223630). I top sono i tre riferimenti già selezionati, inclusi tutti i cinque replay iniziali e i tre di conferma, senza selezione per risultato. E22.1 ripubblicata il 15 settembre è lo stesso bundle; i suoi nuovi replay non sono inclusi.

## Metodo

40 pannelli standard (22 KPI più volumi/prezzi), 5 istogrammi interattivi per coltura, periodi D1–30 / D1–10 / D11–20 / D21–30. Istogrammi: medie per partita; traiettorie: mediana e min–max. Costi espliciti: semi e acquisti del prodotto, separati. Il saldo per prodotto include commercio e autoconsumo e non è un margine agricolo pieno. Manodopera, terreni, acquisti animali e fertilizzante non sono distribuiti arbitrariamente tra colture. Scorte non valorizzate; capitale iniziale riconciliato. Ogni ledger verifica 719 transizioni di cassa per entrambi i giocatori; i nuovi audit riproducono soltanto azioni registrate su copie dello stato, senza nuove partite o chiamate alle policy.

## Indicazioni E24

1. Grano: 518 raccolti in E22.1 contro 571–584 nei top, circa 163 semine. Indagare fertilizzazione, maturazione e raccolta prima di aumentare le superfici. Saldo prodotto E22.1 4.953, top 7.647–8.217; non è un effetto causale stimato.
2. Fragola: volumi quasi uguali, ricavi E22.1 da 7.962 a 56.247. Priorità a indicatori di domanda/prezzo osservabili al rinnovo, senza informazioni future.
3. Pomodoro: opzione minoritaria, non ricetta universale. Verificare casi e controesempi e costo di lavoro/terreno aggiuntivo.

La cassa media non ordina i competitor come il rating: E22.1 98.008, Catalyst 100.525, Thomas 92.612, Deodims 108.118. Differenze di mercati, avversari e numerosità impediscono inferenze causali. Non ci sono nuovi test economici né una nuova policy E24.

[Report completo](REPORT.html) · [Dati per replay/giorno/prodotto](CROP_DAILY.csv) · [Scomposizione ricavi](REVENUE_DECOMPOSITION.json) · [Manifesto](MANIFEST.json) · [Verifiche](VERIFICATION.json)
