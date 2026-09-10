# Evoluzione E18 / E19 / E20.1

Questo banco separa diagnosi, esperimento causale locale e validazione. E18 e il riferimento principale; E19 ed E20.1 sono controlli congelati, non sorgenti da mescolare nello stesso stato.

- [Protocollo e seed riservati](PROTOCOL.md)
- [Analisi economica dei tre modelli](reports/diagnostic_20260910/REPORT.md)
- [Primo esperimento ripetibile H001](reports/diagnostic_20260910/H001_REPORT.md)
- [Registro dei campioni e degli esperimenti](REGISTRY.json)

## Riprodurre il lavoro

Dalla radice del repository, con il runtime `.venv/Scripts/python.exe`:

```powershell
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/analyze_three.py
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/branch_replay.py --model E18 --condition control
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/branch_replay.py --model E18 --condition omit_one_hire
```

Ripetere le due condizioni per `E19` ed `E20.1`, sempre in sequenza, poi:

```powershell
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/report_branches.py
```

Il primo strumento usa i replay esistenti del torneo e20_1_confirmation. Il secondo realizza l esperimento H001 definito nel protocollo: ricostruisce entrambi i controller dalla storia fino a D20 e riparte con l engine dallo stesso checkpoint. Ogni esecuzione scrive un replay completo, un record con gli hash e le verifiche; il report riconcilia i flussi con l auditor comune dei 22 KPI. I replay compressi sono artefatti locali: per riprodurre altrove occorre trasferire quelli indicati nel manifesto, non solo il codice.

I file derivati `.kpi.json` sono una cache: eliminarli esplicitamente prima di ricalcolare un esperimento modificato, oppure usare un nuovo identificativo. Non cambiare il trattamento mantenendo il nome H001. Questa prima versione del runner implementa il checkpoint e il trattamento specifici di H001; aggiungere nuove condizioni richiede un protocollo distinto.

## Criterio per il prossimo passo

Prima di un nuovo modello, selezionare un meccanismo dagli incidenti: meno vendite per minori volumi, prezzi inferiori o consegne tardive sono spiegazioni differenti. Registrare cosa dovrebbe cambiare e cosa smentirebbe l ipotesi. Provare alternative solo su stati compatibili con il controller originale e verificare prima la prosecuzione senza intervento.

Un effetto su una singola partita e un risultato locale. Una regola candidata richiede ripetizione su seed/ruoli diagnostici, controllo biologico e limite di runtime. Solo dopo il congelamento della regola si apre il campione di validazione riservato, una volta, riportando tutti gli esiti. Nessuna promozione e nessuna submission sono parte di H001.

## H002: vendita e prezzi

[Scomposizione dei ricavi](reports/sales_20260910/REPORT.md) e [esperimento H002](reports/H002/REPORT.md). Nei sei casi il rinvio di una richiesta SELL fragole cambia i ricavi senza cambiare gli stati fisici delle fattorie, i servizi eseguiti o le quantita totali vendute. Il segno e opposto tra E18 ed E19/E20.1; nessuna regola adottata. Protocollo in H002_PROTOCOL.md; seed di validazione ancora non eseguiti.

```powershell
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/analyze_sales.py
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/branch_h002.py --model E18 --seed 180910202 --condition control
.venv/Scripts/python.exe docs/model_specs/codex/evolution/tools/branch_h002.py --model E18 --seed 180910202 --condition defer_strawberry
```

Ripetere per i tre modelli e i due seed201/202 definiti nel protocollo. I controlli seed201 sono riusati da H001; generare solo il trattamento H002 per quel seed. Dopo tutti i rami, eseguire report_h002.py: verifica hash e parita dei controlli, produce audit, transazioni riuscite,22KPI e confronto degli stati fisici. isolate_h002.py puo rigenerare solo l ultima verifica dai risultati gia presenti.

## H003: ordine delle vendite nello stesso batch

[Report H003](reports/H003/REPORT.md):84decisioni da42transizioni verificate e quattro nuove prosecuzioni complete. Regola diagnostica: portare la vendita di fragole al primo posto, solo attraverso altre vendite, una volta in D20. Migliora tutti i confronti immediati contro E18 ma puo peggiorare contro E19/E20.1. Nessuna adozione. La diagnosi dell ordine avversario usa dati retrospettivi, non disponibili come input contemporaneo della policy.

Riproduzione: scan_h003.py, poi branch_h003.py con --model E19 oppure E20.1, --seed180910201 oppure180910202 e --condition strawberry_first (separare opzioni e valori con spazi). report_h003.py riusa i controlli H001/H002 verificandone gli hash, produce audit/22KPI, confronta stati fisici e genera la diagnosi retrospettiva. E18 gia vende fragole al primo posto nei casi selezionati e il ramo invariato riusa il controllo.

Il prossimo passo e verificare se la storia osservabile consente di stimare la priorita di vendita concorrente, prima di formulare una regola adattiva. Non usare nomi dei modelli o azioni contemporanee/future degli avversari.

## H004: inferenza da osservazioni proprie precedenti

[Report H004](reports/H004/REPORT.md). Modello inverso da cinque H1 precedenti al target:420testimonianze,64identificate senza errori retrospettivi;18forecast corretti su84, tutti in casi E18 senza riordini utili. E19/E20.1: astensione totale. Non adottato, utilita operativa zero.

run_h004.py produce e congela predizioni prima di leggere le etichette target e i payoff H003. check_h004.py riproduce tutto da storie troncate prima di D20, oscurando anche la fattoria pubblica avversaria e verificando input immutabili. Nessuna azione/privato concorrente entra nel classificatore. infer_market_order.py esclude acquisti propri, floor e casi incompatibili; non pretende di identificare tutte le strategie di mercato. Il prossimo ampliamento deve supportare ordini misti, non diminuire ex post le soglie di evidenza.

## H005: transazioni miste

[Protocollo](H005_PROTOCOL.md) e [report conclusivo](reports/H005/REPORT.md). Copertura 31/84, nessun riordino: non adottato. Stesse soglie e stesso campione diagnostico di H004.

Eseguire dalla radice, in sequenza con `.venv/Scripts/python.exe`: `docs/model_specs/codex/evolution/tools/test_h005_accounting.py`, `run_h005.py`, `check_h005.py`, `diagnose_h005.py`, `close_h005.py` (gli ultimi quattro nella stessa directory tools). Il runner congela le predizioni prima della valutazione; la chiusura aggiunge interpretazione e manifest.

## H006: ricavi certi al prezzo minimo

[Protocollo](H006_PROTOCOL.md) · [Report](reports/H006/REPORT.md). Dalla radice eseguire con `.venv/Scripts/python.exe`, in sequenza, gli script in `docs/model_specs/codex/evolution/tools/`: `test_h006_accounting.py`, `run_h006.py`, `check_h006.py`, `close_h006.py`. Nessuna promozione sul campione diagnostico.

## H006: prosecuzioni complete

[Protocollo](H006_CONTINUATION_PROTOCOL.md) · [Report e grafici dei 22 KPI](reports/H006_FULL/REPORT.md). Script nella directory tools, da eseguire con il Python del progetto in sequenza: `branch_h006_full.py`, `report_h006_full.py`, `plot_h006_full.py`, `close_h006_full.py`. Otto simulazioni seriali; campione diagnostico, nessuna adozione.
