# H003: priorita delle fragole fra le vendite correnti

Condizione osservabile: esiste una vendita di fragole preceduta soltanto da altre vendite. Si porta al primo posto una sola volta in D20, senza cambiare quantita, ora o comandi dei lavoratori. La regola non usa gli ordini contemporanei o futuri dell avversario.

## Effetto immediato sul campione diagnostico

42 transizioni originali riprodotte esattamente, 84 decisioni dei due giocatori. Azione avversaria originale fissata solo nella transizione simultanea; nessun uso dell azione avversaria per scegliere la modifica. Media sui soli casi applicabili. Tutti i sette seed sono gia esposti.

| Modello | Applicabili | Delta cassa medio | Positivi / nulli / negativi |
|---|---:|---:|---|
| E18 | 0/28 | +0.0 | 0 / 0 / 0 |
| E19 | 28/28 | +29.1 | 19 / 0 / 9 |
| E20.1 | 28/28 | +33.4 | 20 / 0 / 8 |

## Effetto immediato per avversario

| Modello | Avversario | Casi | Delta cassa medio | Positivi | Negativi |
|---|---|---:|---:|---:|---:|
| E19 | E18 | 14 | +87.0 | 14 | 0 |
| E19 | E20.1 | 14 | -28.7 | 5 | 9 |
| E20.1 | E18 | 14 | +87.1 | 14 | 0 |
| E20.1 | E19 | 14 | -20.3 | 6 | 8 |

Contro E18 tutti i casi applicabili migliorano la transazione corrente; i negativi emergono negli scontri E19/E20.1. E una segmentazione diagnostica successiva agli esiti, non una condizione da inserire nella policy. Identita del modello avversario e sua azione contemporanea non sono input della regola. Prima di una regola adattiva occorre verificare se il suo comportamento di vendita sia inferibile dalla storia osservabile del mercato.

## Prosecuzioni complete: due seed, ruolo0

E18 e gia al primo posto nei due casi: il controllo viene riusato come esito non applicabile, non contato come nuova simulazione. Quattro trattamenti nuovi, sei controlli verificati e riusati con confronto degli hash. Gli avversari reagiscono in tutte le prosecuzioni complete.

| Modello | Seed | Delta cassa | Delta margine | Stress controllo/intervento | Fughe controllo/intervento | Stati fisici / servizi identici | Decisione |
|---|---:|---:|---:|---:|---:|---|---|
| E18 | 180910201 | +0 | +0 | 22/22 | 0/0 | True / True | NOT_APPLICABLE |
| E18 | 180910202 | +0 | +0 | 21/21 | 0/0 | True / True | NOT_APPLICABLE |
| E19 | 180910201 | +202 | +377 | 6/6 | 0/0 | True / True | DIAGNOSTIC_ONLY |
| E19 | 180910202 | +179 | +340 | 5/5 | 0/0 | True / True | DIAGNOSTIC_ONLY |
| E20.1 | 180910201 | +157 | +292 | 3/3 | 0/0 | True / True | DIAGNOSTIC_ONLY |
| E20.1 | 180910202 | +195 | +368 | 6/6 | 0/0 | True / True | DIAGNOSTIC_ONLY |

## Fragole e altre componenti, D20-D30

| Modello | Seed | Delta vendite fragole | Delta altre vendite | Delta acquisti | Delta salari | Delta unita fragole |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 180910201 | +0 | +0 | +0 | +0 | +0 |
| E18 | 180910202 | +0 | +0 | +0 | +0 | +0 |
| E19 | 180910201 | +202 | +0 | +0 | +0 | +0 |
| E19 | 180910202 | +179 | +0 | +0 | +0 | +0 |
| E20.1 | 180910201 | +157 | +0 | +0 | +0 | +0 |
| E20.1 | 180910202 | +195 | +0 | +0 | +0 | +0 |

Nessuna promozione: lo scan misura una sola transizione; le quattro traiettorie nuove coprono soltanto due seed. Tutti i rami nuovi hanno719chiamate per agente e DONE/DONE, nessun errore nei core strumentati; parita fino al trigger e controlli fino al terminale. Il beneficio sulla singola richiesta non dimostra una buona regola per tutti i giorni/prodotti. [Protocollo](../../H003_PROTOCOL.md) - [Dati](RESULT.json) - [Scan completo](ONE_STEP.json) - [22KPI](daily_22_kpi.csv).

## Diagnosi retrospettiva della posizione concorrente

| Posizione delle fragole nella lista avversaria, base0 | Positivi | Negativi |
|---|---:|---:|
| 0 | 28 | 0 |
| 1 | 11 | 8 |
| 2 | 0 | 9 |

Questa informazione spiega dove cercare il meccanismo, ma e ricostruita dopo la partita: non si puo passare l ordine concorrente contemporaneo alla policy. Il prossimo esperimento deve prima verificare un inferenza dalla sola storia osservata. Nessuna regola basata sul nome del modello o sui dati futuri viene adottata.
