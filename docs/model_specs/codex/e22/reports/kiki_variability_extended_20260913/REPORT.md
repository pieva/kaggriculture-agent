# Kiki yi2 — variabilità estesa

Submission 56137379: 39 replay su 468 pubblici disponibili. Selezione cronologica distribuita: 32 indici equidistanti, uniti agli 8 replay precedenti; una sovrapposizione. Nessun filtro su risultato o configurazione. Periodo campionato: 2026-09-10T04:51:59.730044100Z — 2026-09-13T12:30:46.807471Z. Non è un censimento né un campione casuale.

A D20: 4 mix animali, 1 impronte spaziali e 2 disposizioni dei tipi di struttura. Sostituzioni di specie su caselle precedentemente occupate: 0; rimozioni animali: 1. Queste ultime possono essere fughe e non scelte strategiche.

## Mix animali a D20

- **COW:8, SHEEP:8**: 3 replay.
- **COW:8, GOOSE:3, SHEEP:6**: 26 replay.
- **COW:6, SHEEP:10**: 9 replay.
- **COW:6, GOOSE:3, SHEEP:8**: 1 replay.

Regola precedente, senza riadattare soglie: a D8 H2 ordine SHEEP se YARN_STORE è presente. Copertura 39/39, corrispondenze 38/39. Associazione osservata: non identifica il programma né dimostra il beneficio economico.

## Colture

- STRAWBERRY:33, WHEAT:25: 37 replay a D20.
- STRAWBERRY:32, WHEAT:25: 1 replay a D20.
- STRAWBERRY:33, WHEAT:24: 1 replay a D20.

Replay con almeno una semina di pomodoro: 0/39. I grafici giornalieri permettono di distinguere mix a D20 e successioni finali.

## Limiti

Le assenze di animali o colture non sono automaticamente decisioni di portafoglio: possono essere investimenti incompleti o perdite. Prezzi riportati a fine giornata, non prezzi realizzati delle vendite. In questa estensione si verificano hash, episodi completi e transizioni; non si ripete l'audit economico dei due giocatori eseguito sugli otto replay precedenti. Le frequenze descrivono solo il campione; nessuna modifica di policy.

[Grafici D1–D30](REPORT.html) · [Dati sintetici ed episodi per gruppo](SUMMARY.json) · [Dati completi](ANALYSIS.json).


## Cosa cambia rispetto al primo campione

Le quattro configurazioni corrispondono a due finestre di acquisto: D8 COW oppure SHEEP, D11–D12 GOOSE oppure SHEEP. Le combinazioni osservate sono COW/GOOSE in 26 casi, SHEEP/SHEEP in 9, COW/SHEEP in 3 e SHEEP/GOOSE in 1. Non sono quattro riscritture del piano intero: sono compatibili con due decisioni locali, senza provare che il codice le calcoli indipendentemente.

Il controesempio 107961405 sceglie SHEEP a D8 H2 senza negozio lana, con latte 210 e lana 189; poi sceglie GOOSE. Quindi YARN_STORE non è una spiegazione completa. Anche il secondo ramo richiede analisi: 107358349 acquista pecore dopo l'arrivo di YARN_STORE, ma 107663612 e 107775518 fanno lo stesso senza quel negozio. Non introdurre una regola assoluta ricavata dagli otto replay iniziali.

Le successioni tardive mostrano lo stesso insieme di coppie giorno/specie in tutti i 39 replay: semine di grano a D20–D25 e in alcuni passaggi D27–D28, carote a D25–D28; nessun pomodoro. Questa misura non implica identità dei comandi, delle coordinate o delle quantità. Il nucleo colturale resta molto stabile.

Una rimozione nell'episodio 108444786 è verificata come fuga: pecora (7,4), passaggio D16→D17, non alimentata e consecutive_unfed=1 prima del refresh. Non viene ricomprata; non è una rotazione. Tutti gli ultimi collocamenti animali del campione avvengono entro D12.

Per la nostra evoluzione conviene quindi studiare separatamente la scelta COW/SHEEP su pascoli liberi e la scelta delle tre strutture finali, conservando il calendario, prima di affiancare la conversione colturale a pomodoro. Nessuna prova qui dimostra ancora quanto ciascuna scelta riduca la saturazione rispetto alla sua alternativa nello stesso mercato.
