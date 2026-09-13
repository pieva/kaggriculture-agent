# Kiki yi2 — scelta del mix e rischio di saturazione

Submission **56137379**, otto replay già acquisiti: cinque del pilota e tre della precedente verifica. Questo approfondimento non aggiunge un campione indipendente. Hash dei replay verificati, registri economici di entrambi i giocatori riconciliati.

## Risultato

**Zero sostituzioni e zero rimozioni di animali negli otto replay.** La variabilità è nella costruzione del portafoglio durante la crescita, non in una rotazione di animali già collocati dopo la caduta dei prezzi. Nel motore locale `DIG` non rimuove animali e `PLACE` richiede una struttura libera; le colture hanno quindi una flessibilità diversa.

Le 17 coordinate dedicate all'allevamento a D20 coincidono in tutti gli otto replay. I tipi di struttura cambiano: 14 pascoli + 3 pollai nel ramo misto, 17 pascoli nel ramo lana. È un'impronta stabile con una scelta di struttura su tre caselle, non una topologia integralmente identica.

## Decisione osservata a D8 H2

- Nei cinque casi senza negozio di lana, l'ordine compra una mucca. A D20: 8 mucche, 6 pecore, 3 oche.
- Nei tre casi con uno o due negozi di lana, l'ordine compra una pecora. A D20: 6 mucche, 10 pecore, nessuna oca; un pascolo è privo di animale.
- La corrispondenza negozio/scelta è 8/8 in questo campione già studiato. È un'associazione osservata, non l'identificazione del codice o una prova di rendimento causale.

Un contrasto utile: episodio 108483384, latte 210 e lana 200, con negozio lana, sceglie pecora; episodio 108487585, latte 194 e lana 195, senza negozio lana, sceglie mucca. Il solo prezzo istantaneo più alto non spiega entrambi.

## Quanto protegge dalla saturazione?

Nei tre casi del ramo lana vengono vendute 244 unità di lana, con prezzo medio realizzato circa 238–245. Nei cinque casi del ramo misto vengono vendute 161 unità, ma il prezzo realizzato è circa 42–58. È coerente con la presenza di domanda persistente nel primo ramo. Non misura il guadagno della scelta: mercati e avversari sono diversi e non abbiamo simulato la scelta alternativa nello stesso scenario.

Kiki continua a produrre e vendere anche nel ramo con lana poco remunerativa. Non emerge dagli animali una correzione tardiva del mix in risposta a saturazione già avvenuta. I grafici confrontano vendite proprie e avversarie; non attribuiscono automaticamente tutta la discesa del prezzo alle nostre vendite. Prezzo a fine giornata e prezzo medio effettivamente incassato sono distinti.

## Collegamento con i pomodori

Base di riferimento: **E20.9fix**, file `submission/submission_codex_e20_9_placefix_internal.py`, derivata da E20v44 late tomato con la successiva correzione dei depositi PLACE. Le due conversioni fragola→pomodoro a D20–D21 sono programmate, con controllo della cassa; non sono già un trigger di saturazione. Rimangono limiti di liquidazione finale.

L'evoluzione comune da sperimentare è scegliere l'investimento sulla domanda attesa alla produzione: per animali nelle caselle ancora libere, per colture alla successione utile. Il costo comprende acquisto/semi, lavoro, fertilizzante, grano e valore della vendita rinunciata per autoconsumo. Una coltura alternativa deve maturare, essere raccolta, consegnata e venduta entro D30.

## Primo esperimento proposto, non implementato

Conservare le coordinate e il calendario di riferimento. Prima isolare la scelta COW/SHEEP su pascoli ancora liberi a D8, usando la presenza del negozio di lana come regola osservabile da verificare. Questo è un trasferimento parziale del comportamento kiki: non replica il ramo che cambia tre pollai in pascoli. Tenere invariati gli altri animali e le colture per misurarne l'effetto.

Poi valutare separatamente la conversione a pomodoro, con produzione propria e avversaria attesa e domanda dei negozi, anziché reagire soltanto al prezzo odierno. Infine combinare le due modifiche. Servono confronti accoppiati della policy di base, della modifica animale, della modifica colturale e della combinazione: cassa, margine, quantità vendute, prezzi realizzati, costo del lavoro, mangime e residui. L'obiettivo è migliorare il margine finale evitando eccessi di offerta; smettere di vendere a prezzo basso può da solo peggiorare il risultato.

Nessuna policy modificata o pubblicata in questo approfondimento. [Grafici D1–D30](REPORT.html), [dati sintetici](SUMMARY.json), [transizioni e registri economici](ANALYSIS.json).
