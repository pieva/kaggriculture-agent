# E22 — replica osservata e correzione consegne

E22 replica il piano costante osservato della submission s56165462 56165462: 719 azioni indicizzate da giorno e ora. Non ricostruisce il codice interno né usa osservazioni future. Parità esatta su 14.380 azioni in 20 replay. E20.9 congelata resta intatta; E209Fix cambia soltanto la condizione che saltava PLACE di prodotti sulle caselle già occupate da animali.

Due seed esposti (180911301 e 180911303), entrambi i ruoli, quattro partite per variante contro E20.9 congelata. Otto simulazioni seriali. Mercato condiviso e politiche eseguite nel motore; non replay avversari forzati. Verifica della cassa a ogni transizione per entrambi i giocatori. Non è una stima del rating, né una conferma su seed riservati.

| Variante | Vittorie | Margine medio | Min | Max |
|---|---:|---:|---:|---:|
| E22Replica | 4/4 | 14981.0 | 14350.0 | 15612.0 |
| E209Fix | 4/4 | 6135.5 | 5503.0 | 6768.0 |

## Causa e intervento

`PLACE` ha due significati: collocare animali e depositare prodotti. Il controllo di lavoro già soddisfatto verificava soltanto la presenza di un animale sulla casella: saltava anche PLACE MELON. Ora applica quel controllo soltanto se il prodotto richiesto è un animale. Test di regressione sullo stato reale D11: PLACE MELON 6 non viene saltato. L’esistenza di un ordine SELL non dimostra la consegna né il suo successo.

## Come è sfuggito

Le verifiche precedenti controllavano correttamente quantità raccolte, cassa e corrispondenza bundle/sorgente, ma non imponevano la consegna del raccolto entro la finestra di vendita. La parità con la sorgente preservava anche questo difetto. La correzione resta separata dalla replica, per attribuire gli effetti.

## Limiti e prossima decisione

La replica è un riferimento interno: non adattando il piano, può fallire azioni quando cassa o stato divergono. Il confronto a seed accoppiati non rende identiche le condizioni di mercato dopo l’intervento: entrambi i giocatori influenzano il mercato, come previsto dal gioco. Non promuovere automaticamente alcun candidato dai soli seed esposti. Nessuna pubblicazione o commit.

[Grafici 30 giorni e dettaglio partite](REPORT.html) · [Protocollo](PROTOCOL.json) · [Dati](RESULTS.json)
