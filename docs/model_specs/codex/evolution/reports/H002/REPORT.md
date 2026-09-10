# H002: rinvio di una richiesta di vendita delle fragole

Sei situazioni: tre modelli, due seed diagnostici, ruolo0. Stesso stato iniziale in ogni confronto con se stesso, avversario reattivo. Nessuna promozione. Il trattamento elimina una richiesta corrente e lascia al controller le decisioni successive, non impone un ritardo di durata fissa.

| Modello | Seed | Delta cassa finale | Delta margine | Stress controllo/intervento | Fughe controllo/intervento | Decisione |
|---|---:|---:|---:|---:|---:|---|
| E18 | 180910201 | -391 | -1100 | 22/22 | 0/0 | DIAGNOSTIC_ONLY |
| E18 | 180910202 | -162 | -421 | 21/21 | 0/0 | DIAGNOSTIC_ONLY |
| E19 | 180910201 | +93 | +93 | 6/6 | 0/0 | DIAGNOSTIC_ONLY |
| E19 | 180910202 | +81 | +81 | 5/5 | 0/0 | DIAGNOSTIC_ONLY |
| E20.1 | 180910201 | +126 | +126 | 3/3 | 0/0 | DIAGNOSTIC_ONLY |
| E20.1 | 180910202 | +46 | +46 | 6/6 | 0/0 | DIAGNOSTIC_ONLY |

## D20: intervento meno controllo

| Modello | Seed | Delta cassa | Delta vendite fragole | Delta unita fragole | Prezzo medio controllo/intervento | Delta stock fragole |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 180910201 | -791 | -791 | -10 | 71.55/65.25 | +10 |
| E18 | 180910202 | -162 | -162 | +0 | 143.43/131.86 | +0 |
| E19 | 180910201 | +93 | +93 | +0 | 59.50/65.31 | +0 |
| E19 | 180910202 | +81 | +81 | +0 | 117.56/126.56 | +0 |
| E20.1 | 180910201 | +126 | +126 | +0 | 128.36/137.36 | +0 |
| E20.1 | 180910202 | +46 | +46 | +0 | 42.25/46.08 | +0 |

## D20-D22: intervento meno controllo

| Modello | Seed | Delta cassa | Delta vendite fragole | Delta unita fragole | Prezzo medio controllo/intervento | Delta stock fragole |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 180910201 | -391 | -391 | +0 | 38.73/32.10 | +0 |
| E18 | 180910202 | -162 | -162 | +0 | 101.73/98.43 | +0 |
| E19 | 180910201 | +93 | +93 | +0 | 29.85/32.17 | +0 |
| E19 | 180910202 | +81 | +81 | +0 | 84.68/86.82 | +0 |
| E20.1 | 180910201 | +126 | +126 | +0 | 103.47/106.27 | +0 |
| E20.1 | 180910202 | +46 | +46 | +0 | 10.30/11.11 | +0 |

## D20-D30: intervento meno controllo

| Modello | Seed | Delta cassa | Delta vendite fragole | Delta unita fragole | Prezzo medio controllo/intervento | Delta stock fragole |
|---|---:|---:|---:|---:|---:|---:|
| E18 | 180910201 | -391 | -391 | +0 | 22.58/20.49 | +0 |
| E18 | 180910202 | -162 | -162 | +0 | 39.16/38.23 | +0 |
| E19 | 180910201 | +93 | +93 | +0 | 13.69/14.16 | +0 |
| E19 | 180910202 | +81 | +81 | +0 | 21.15/21.53 | +0 |
| E20.1 | 180910201 | +126 | +126 | +0 | 34.43/35.06 | +0 |
| E20.1 | 180910202 | +46 | +46 | +0 | 4.89/5.12 | +0 |

## Tempi effettivi

Primo SELL fragole riuscito al trigger o dopo, verificato eseguendo il mercato sui due giocatori e riconciliando la cassa.

| Modello | Seed | Trigger | Vendita controllo | Vendita intervento |
|---|---:|---|---|---|
| E18 | 180910201 | D20 H1 | D20 H1 | D20 H2 |
| E18 | 180910202 | D20 H1 | D20 H1 | D20 H3 |
| E19 | 180910201 | D20 H1 | D20 H1 | D20 H2 |
| E19 | 180910202 | D20 H1 | D20 H1 | D20 H2 |
| E20.1 | 180910201 | D20 H1 | D20 H1 | D20 H2 |
| E20.1 | 180910202 | D20 H1 | D20 H1 | D20 H2 |

I sei controlli sono verificati fino al terminale; tre del seed201 vengono riusati da H001 dopo confronto degli hash di sorgente, bundle ed engine. Tutti i rami hanno719chiamate per agente, zero errori nei core che espongono il contatore e DONE/DONE. Audit dei flussi e transazioni riuscite; prezzi medi ponderati per unita vendute. Lo stock conta deposito e inventari, non frutti ancora sulle caselle.

Un prezzo medio diverso puo includere quantita e tempi differenti, oltre a reazioni dell avversario. Il trattamento identifica un effetto locale della richiesta omessa, non la causa universale del divario tra i modelli. Due seed non autorizzano una regola generale. [Protocollo](../../H002_PROTOCOL.md) - [Dati](RESULT.json) - [Scomposizione vendite](../sales_20260910/REPORT.md).

## Verifica del meccanismo

| Modello | Seed | Batch di lavoro diversi, agente/avversario | Delta altre vendite | Delta acquisti | Delta salari |
|---|---:|---:|---:|---:|---:|
| E18 | 180910201 | 0/0 | +0 | +0 | +0 |
| E18 | 180910202 | 0/0 | +0 | +0 | +0 |
| E19 | 180910201 | 0/0 | +0 | +0 | +0 |
| E19 | 180910202 | 0/0 | +0 | +0 | +0 |
| E20.1 | 180910201 | 0/0 | +0 | +0 | +0 |
| E20.1 | 180910202 | 0/0 | +0 | +0 | +0 |

In tutti e sei i casi il lavoro di entrambi gli agenti resta identico per l intero seguito, le quantita totali di fragole vendute e lo stock finale coincidono, e il delta di cassa e interamente riconciliato con gli incassi delle fragole. Questa prova circoscrive l effetto locale al calendario di vendita e al prezzo realizzato, senza un cambiamento del lavoro fisico. E18 peggiora in entrambi i seed; E19 ed E20.1 migliorano modestamente. Non emerge una regola universale di rinvio.

Prossimo punto da verificare: prezzo ottenibile e concorrenza nelle finestre di vendita, non un ritardo fisso applicato a tutte le topologie. Il deficit medio E20.1 rispetto a E19 non e spiegato integralmente da questa singola richiesta.
