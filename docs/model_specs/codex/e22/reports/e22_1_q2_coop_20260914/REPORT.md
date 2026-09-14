# E22.1 — dal pollaio vuoto alla coltura finale

**Sì: conviene riutilizzare (3,7) con una coltura breve seminata a D28.** Il pollaio previsto a D29 H5 resta vuoto in tutti i 20 replay e non produce reddito. Con il motore effettivo, grano e carote aggiungono due unità raccolte e vendute entro D30, senza assunzioni aggiuntive e senza ridurre le altre raccolte verificate.

## Risultati economici

| Successione dopo le fragole | Incremento medio cassa | Minimo | Massimo | Replay positivi | Costo seme |
|---|---:|---:|---:|---:|---:|
| Grano | +68.15 | +32 | +83 | 20/20 | 10 |
| Carote | +72.30 | +25 | +119 | 20/20 | 20 |

Gli incrementi sono differenze della cassa finale dell'intera fattoria, dopo costo del seme, vendite effettive e cambiamenti di prezzo. Non sono stime ottenute moltiplicando il raccolto per un prezzo fisso. Nessun acquisto di fertilizzante; acqua senza costo monetario diretto. Il costo della manodopera resta invariato: si riassegnano comandi all'interno delle giornate già pagate. Carote migliori del grano in 11/20 casi; il vantaggio medio di 4,15 non prova una superiorità generale.

## Abbinamento con le caselle vicine

| Casella | Situazione a D28 | Coltura finale D29–D30 | Collegamento operativo |
|---|---|---|---|
| (3,7) | Ultima raccolta fragole D28 H6; DIG H7 | Nuovo grano o carote | Stesso lavoratore 10, semina H8 e acqua H9 |
| (3,6), nord | Fragole a fine ciclo | Grano, 20/20 replay | Stesso calendario di maturazione D30 |
| (4,7), est | Fragole a fine ciclo | Grano, 20/20 replay | Il lavoratore 10 lo raccoglie a D30, poi visita (3,7) |
| (2,7), ovest | Ultime fragole | Liberata a D29 | Attraversata dal giro del lavoratore 6 |
| (3,8), sud | Ultime fragole | Fine ciclo; nessuna nuova coltura | Il DIG subito dopo la raccolta si può omettere |
| (2,6), nord-ovest | Fragole a fine ciclo | Grano | Altra successione breve già presente |
| (2,8), sud-ovest | Carote | Carote | Conferma che anche la seconda alternativa è compatibile col settore |

**Scelta consigliata per un calendario semplice: grano in (3,7).** Si inserisce nel gruppo di grano a nord ed est, ha il seme meno caro e il minimo incremento osservato più alto. Le carote restano un'alternativa valida con rendimento medio leggermente maggiore; nei due esperimenti hanno esattamente lo stesso costo di manodopera. L'omogeneità delle colture, da sola, non fa risparmiare comandi nel motore: il risparmio concreto deriva dalle visite condivise e dalla consegna accorpata.

## Calendario verificato e manodopera

1. D28: si conservano raccolta fragole H6 e DIG H7. Il lavoratore 10 semina a H8 e irriga a H9. Il seme viene acquistato a H7, prima del turno di semina, evitando conflitti con le altre richieste PLANT.
2. Per recuperare i due comandi, si omettono il DIG finale in (3,8) e l'acqua non produttiva D28 delle carote giovani in (1,7). Il controllo dei 20 casi conferma la sopravvivenza e la raccolta invariata delle carote; il percorso torna al calendario originale prima di fine giornata.
3. D29 H5: il lavoratore 6, già in (3,7), irriga invece di costruire il pollaio. Non cambia percorso.
4. D30: il lavoratore 10, dopo il grano di (4,7), compie WEST → WATER → HARVEST → EAST. Irrigazione H9 e raccolta H10 in (3,7), per due unità. Si eliminano un PASS iniziale e la prima consegna intermedia, si usano due PASS finali e si accorpa il trasporto alla consegna H22. Le vendite H22 incassano i prodotti entro la chiusura.

Non basta cambiare BUILD_COOP in PLANT a D29: la maturazione minima di due giorni cadrebbe a D31. Nuove fragole, pomodori e meloni sono troppo lenti. Anche (4,5) viene liberata solo a D29 H3 nel calendario attuale: non offre la stessa finestra senza anticipare altre operazioni. Per questo il test conserva le fragole esistenti fino all'ultima raccolta e usa direttamente (3,7).

## Metodo e limiti

20 replay E22.1, submission 56206528, con hash originali verificati. Per ogni replay: ripartenza dallo stato reale all'inizio di D28 e tre esecuzioni del motore fino alla fine, baseline + grano + carote (60 esecuzioni). La baseline riproduce esattamente fattorie, inventari privati e mercato a ogni passo. Le altre due esecuzioni mantengono le azioni avversarie registrate e ricalcolano prezzi, consumi e cassa.

Verificati: due unità aggiuntive, nessuna diminuzione delle altre raccolte confrontate, identici inventari e semi finali alla baseline e nessun prodotto aggiuntivo invenduto. Il confronto automatico dei totali di raccolta esclude i ritorni notturni H24; i comandi H24 restano invariati. È un esperimento diagnostico su avversari congelati e su un intervento scelto guardando questi replay, non un test indipendente o un aumento dimostrato del rating. Le due colture sono state provate solo nel piano locale dell'esperimento: nessuna modifica ai bundle E22.1 o E22.2 fix pubblicata.

[Risultati sintetici](CROP_SUMMARY.json) · [Stati, comandi e cassa per replay](CROP_COUNTERFACTUALS.json) · [Audit del pollaio e delle due caselle](EVIDENCE.json).
