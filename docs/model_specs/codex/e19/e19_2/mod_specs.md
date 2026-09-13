# E19.2 — 770 reattiva

## Obiettivo e origine

Richiesta del 13 settembre 2026: pubblicare E22 come confronto esterno e ripartire da E19 770 V51C per sviluppare la candidata reattiva verso rating 2000. Il rating è un obiettivo da verificare su Kaggle, non una conseguenza dimostrata della topologia o della cassa interna.

Genitore congelato: `submission/submission_codex_e19_770_v51_candidate.py`, submission 56124996, SHA256 `43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda`. Geometria 770, portafoglio di riferimento 9 mucche e 5 pecore, intenzioni colturali 38 fragole e 23 grano. Le quantità sono obiettivi del pianificatore: occorre misurare quelle effettivamente realizzate.

## Correzione dell'ipotesi iniziale

Nel confronto precedente E22–V51C il divario medio di cassa è 36.642, di cui 3.597 di costo del lavoro. Quindi il lavoro spiega circa il 9,8% della differenza contabile; il resto richiede ricavi e altre spese. V51C contiene già una stima dinamica delle assunzioni, ma genera un carico di servizi elevato e nei replay il costo risulta quasi costante. Non è sufficiente abbassare il massimo dei lavoratori.

## Ablazioni implementate

- V52A: estensione del compilatore di servizi D29 a D12–D29. Respinta: penalizza crescita e fertilizzazione, nonostante il risparmio.
- V52B: servizi estesi anche al fertilizzante e tutela degli ordini di crescita. Respinta: 14 fughe animali in uno scenario.
- V52C: cap ordinario di assunzione 11 invece di 12 a D12–D29; ripristino 12 con stress osservato. Respinta: quattro sconfitte, pur senza fughe. Nel primo scenario vende 215 invece di 242 fragole e 196 invece di 240 grano.
- V52D: conserva il massimo originale e anticipa a D12 la valutazione biologica di CARE. Omette la cura senza produzione futura utile o con bonus saturo, tenendo conto del bonus che verrà consumato nel prossimo aggiornamento. Feed, geometria, percorsi e scelte colturali restano quelli del genitore. Respinta sul primo seed in entrambi i ruoli: margine −1.699 e una fuga animale per partita; il secondo seed è stato annullato. Anche una modifica del carico può cambiare gli esiti dei percorsi; la causa precisa della fuga richiede analisi, non è attribuita direttamente alla mancata cura.

## Protocollo

Partite dirette seriali contro V51C, seed esposti 180911301 e 180911303. A e B sono screening nel ruolo 0; C ha entrambi i ruoli. D è stato interrotto dopo il primo seed, di cui entrambi i ruoli erano completati al momento della cancellazione, perché fallisce il criterio di sopravvivenza. Namespace dei bundle isolati, episodi completi di 720 azioni, verifica dei registri economici, errori del core e fughe. I quattro replay di C rappresentano due scenari con inversione dei ruoli, non quattro seed indipendenti. Il mercato condiviso rende i risultati dipendenti dall'avversario: non confrontare la cassa assoluta con quella ottenuta contro E22 come se fosse un test accoppiato.

## Evoluzioni successive, non ancora implementate

1. Assunzioni dal carico di lavoro eseguibile: alimentazione, acqua necessaria, raccolta, consegna e fertilizzazione valorizzata, inclusi viaggio, deposito e conflitti tra lavoratori. Conservare capacità per crescita e monetizzazione. Lo stress osservato da solo arriva troppo tardi.
2. Rotazioni: confrontare margine del ciclo completo entro D30, input, acqua, fertilizzazione, trasporto, lavoro e vendita. Considerare grano autoconsumato al suo costo opportunità e rischio di saturazione. V51C ha già successioni tardive grano/carota; i pomodori di E20.9 sono programmati, non una vera scelta dinamica dai prezzi.
3. Portafoglio animale: valutare specie e quantità sul margine residuo, domanda dei negozi e alimentazione, senza imporre 9C/5S come soluzione finale. Separare questo esperimento da quello sulle assunzioni.

La selezione deve preservare produzione venduta, assenza di fughe e cassa finale. Solo una variante favorevole nello screening passa a confronti più ampi e seed di conferma; non pubblicare una variante solo perché risparmia salari.
