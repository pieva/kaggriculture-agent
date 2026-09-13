# E20.9 / E20v44 — specifica del campione corrente

Stato al 13 settembre 2026. E20.9 è il campione corrente scelto per proseguire lo sviluppo, sulla base del salto esterno: il pannello Rating trajectory di Kaggle della submission56202079 mostra un massimo di1585, verificato direttamente nella pagina. L’analisi consolidata dei nuovi replay è rinviata: il picco non è un rating stabilizzato né una stima dell’effetto dei singoli interventi.

## Identità e fonti autorevoli

- Bundle pubblicato: [submission_codex_e20_9_e20v44_late_tomato.py](../../../../../submission/submission_codex_e20_9_e20v44_late_tomato.py).
- SHA256: `56956735924f78d3d5502754425b207c67849ff217980e3c383add726b47debe`.
- Identificativo runtime: `CODEX-E20.9-E20V44-LATE-TOMATO`.
- [Ricevuta di pubblicazione](../reports/e20_9_release/PUBLICATION.json): invio 13 settembre, 07:32:35 UTC. Stato Complete verificato; submission56202079. [Fonte Kaggle del massimo1585](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56202079&episodeId=108486736#). Il massimo appartiene alla traiettoria, non è attribuito specificamente all’episodio selezionato108486736.
- [Policy E20.9](../tools/operational_calendar_v44.py), [conversione delle oche](../tools/operational_calendar_goose2.py), [esecutore del calendario](../tools/operational_calendar_base.py).
- Piani canonici: [PLAN_772](../configs/e20v40/PLAN_772.json), [PLAN_NATIVE](../configs/e20v40/PLAN_NATIVE.json), [PROGRAM](../configs/e20v40/PROGRAM.json). Il nome e20v40 identifica la base ereditata, non una sostituzione del bundle E20.9.
- [Contratto engine](../../../../foundation/ENGINE_CONTRACT.md) e [codice ufficiale Kaggle](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture).

## Strategia

Partire da un calendario produttivo comune già efficace, organizzare visite e servizi in coerenza con i tempi biologici, correggere le fragilità di esecuzione e introdurre diversificazione quando concentrare l’offerta riduce la redditività. L’unità di pianificazione è il ciclo completo fino alla vendita, non il numero di PASS o di azioni di servizio.

E20.9 combina tre interventi: elimina un giro di scambi iniziale che poteva prosciugare la cassa, conserva la capacità di lavoro necessaria agli animali e converte due siti di fragole in pomodori per la produzione finale. Il buon risultato esterno sostiene questa direzione come pacchetto strategico; non dimostra ancora che ciascun componente contribuisca positivamente da solo.

La diversificazione attuale è una scelta predefinita suggerita dall’analisi dei prezzi. **Non esiste una selezione dinamica delle colture basata sulla pendenza dei prezzi**, né una previsione della domanda futura. Questa distinzione evita di attribuire al codice un adattamento che non implementa.

## Geometria e portafoglio

“772” è il nome del ramo di provenienza. La geometria effettiva di E20.9 è **14 pascoli 7-6-1, più due pollai**, con **8 mucche, 6 pecore e 2 oche**. Le oche occupano (6,3) e (4,5); il secondo sito animale meridionale è la pecora in (4,6). Coordinate del codice, a base zero.

I pomodori sostituiscono le fragole nelle caselle (3,7) e (4,8). Il resto della struttura produttiva conserva meloni iniziali, successioni di grano/carote, fragole e prodotti animali. Non è la geometria della E21 Common774.

## Calendario operativo

Giorni e ore descritti qui sono a base uno; l’osservazione engine usa day/hour a base zero.

| Fase | Piano e comportamento |
|---|---|
| D1–D6 | Azioni del programma comune originario; unica eccezione E20.9: mercato D1 H1. Le azioni dei lavoratori restano quelle registrate. |
| D7–D11 | Apertura Q1 e sviluppo del calendario; le visite spostate usano code ricompilate e recupero delle posizioni reali. Il mercato tiene conto delle scorte osservate. |
| Da D12 | Un aiutante aggiuntivo rispetto all’organico del programma serve i due siti meridionali: costruzione/collocamento se mancanti, FEED, CARE, raccolta e fertilizzante. Conclusa la coda può recuperare servizi osservati non coperti. |
| D19 H1 | Impegno alla conversione solo se la cassa osservata è almeno 1000. Nel corso di D19 viene integrata la dotazione fino a due semi di pomodoro. |
| D20–D21 | Missioni di conversione sulle due caselle; raccolta della fragola matura se disponibile, rimozione, semina e prima acqua. Nessuna nuova conversione dopo D21. |
| D22–D28 | Servizi agricoli già previsti riutilizzati per i pomodori; nessuna missione supplementare quotidiana di pomodoro sullo specialista animale. |
| D29–D30 | Missioni aggiuntive per servizio/raccolta dei pomodori; ammissione della raccolta finale comprensiva di viaggio, consegna e possibilità di vendita. |

Traguardi osservati nei test locali: 12 meloni D1–D10 con raccolta D11; 4 fragole a D6, 20 a D9, 33 a D12 prima della successiva conversione; un pomodoro seminato D20 e l’altro D21. Sono verifiche sui replay, non garanzie universali contro qualsiasi avversario.

## Esecuzione e adattamento allo stato

Le code mantengono l’ordine delle visite. I lavoratori non coinvolti dagli spostamenti seguono il programma originario, con recupero della posizione quando un comando di servizio sarebbe eseguito nel posto sbagliato. L’adattamento considera solo osservazioni disponibili, senza ordini contemporanei avversari o negozi futuri.

Prima di viaggiare, l’esecutore scarta servizi già soddisfatti o non applicabili: animale assente, FEED/CARE già eseguiti, acqua già fornita, raccolto assente, struttura già costruita. Per i servizi che richiedono risorse, cerca il deposito e preleva secondo le scorte effettive; le disponibilità di turno sono condivise fra i lavoratori per limitare richieste concorrenti.

La semina gestisce le dipendenze della casella: infestanti da rimuovere, raccolto precedente da raccogliere, coltura precedente da terminare, seme da acquistare. Le code incompiute sono registrate. Solo costruzioni e collocamenti animali sono riportati al giorno successivo: un servizio colturale mancato non viene dichiarato retroattivamente puntuale.

Lo specialista, una volta conclusa la propria coda, dà precedenza al recupero FEED su animali non nutriti; può anche recuperare WATER su colture con almeno un giorno di sete. Questa regola non è un pianificatore globale che certifica tutta la copertura futura: rimangono servizi mancati nei test.

## Apertura finanziaria e mercato

A D1 H1, la sequenza BUY WHEAT 13 / SELL WHEAT 13 / BUY WHEAT 13 diventa il solo BUY WHEAT 13. Conserva il fabbisogno netto iniziale di grano, ma cambia prezzi e regolamento degli scambi. Non è una neutralizzazione economicamente equivalente.

Nei 20 controlli diagnostici delle aperture pubbliche, i tre casi critici passano da cassa zero a 26 a fine D1: diventano possibili le tre assunzioni di D2 e restano quattro animali, invece di due. Le mosse avversarie erano registrate e il seed pubblico mancante era sostituito con un seed esposto: non è una prova universale contro fallimenti di liquidità. Non è implementato un sistema generale di riserva monetaria o recupero di ogni HIRE fallito.

Da D7, l’ordine storico di scambi/semi/assunzioni/terreni è mantenuto dove previsto, integrando lo stato:

- Acquisti animali calcolati sui collocamenti adattati mancanti, al netto di deposito e inventari.
- Vendite supplementari dei prodotti effettivamente presenti; il grano resta protetto dalla logica dei servizi, salvo le vendite previste dal programma.
- Riserva di fertilizzante collegata alle visite FERTILIZE ancora in coda; servizi opzionali scartati se il prodotto non è disponibile.
- Acquisti integrativi di grano quando i FEED mancanti superano la dotazione osservata.
- Assunzioni integrative per raggiungere l’organico del calendario più lo specialista da D12.
- Al massimo dieci ordini di mercato emessi per turno.

Non è implementato un modello di impatto marginale delle vendite o un algoritmo che attenda automaticamente il prezzo migliore.

## Pomodori: ammissione, biologia e tutela del lavoro

I due semi costano 100 complessivi. La soglia di cassa 1000 a D19 è una condizione di ammissione, non una somma vincolata in un conto separato. La semina richiede tempo per arrivare, liberare la casella, piantare e dare la prima acqua; se manca tempo, la missione viene saltata. La prima maturità del pomodoro è dopo otto giorni: seminare soltanto a fine mese non sarebbe utile.

Il lavoratore aggiuntivo riceve missioni dedicate solo D20, D21, D29 e D30. Negli altri giorni restano attivi i passaggi agricoli del calendario. I comandi PLANT/DIG degli altri lavoratori vengono bloccati sui due siti quando vi è effettivamente un pomodoro, evitando che la successione originaria lo distrugga; WATER/HARVEST/FERTILIZE possono continuare.

La sentinella interna TOMATO_MISSION è interpretata dalla policy e non viene inviata all’engine. Una conversione non avviene su una casella animale. A maturità, la missione raccoglie la resa presente; prima del termine considera anche il costo di consegna.

## Chiusura e realizzazione della cassa

A D30, un lavoratore con prodotti rientra verso il deposito quando le ore residue scendono alla distanza più tre. Una raccolta di pomodoro viene ammessa soltanto se viaggio, raccolta, rientro e consegna lasciano tempo per vendere. Il mercato di fine partita vende dalle scorte osservate del deposito, eliminando nuovi acquisti di prodotti/semi/animali da H21.

Queste protezioni limitano il raccolto che rimane trasportato; non garantiscono la liquidazione di ogni prodotto. Nei due scenari locali: quattro pomodori venduti per partita, nessun pomodoro raccolto rimasto in inventario, due unità di resa sulle piante non raccolte. Rimangono anche un grano e tre lana in deposito, semi grano/carota e due perdite colturali preesistenti. Non sommare stock o resa sulle piante alla cassa.

## Evidenza e limiti di interpretazione

Reportistica standard della versione: [ultimo report dei 22 KPI, volumi venduti e prezzi](../../e21/reports/four_common_calendars/REPORT.html). Include E20.9 con fix e pomodori, piano comune nativo, 774 comune ed E18.2 V4D. Per ogni produzione, i volumi venduti e i prezzi unitari sono collocati immediatamente sotto il grafico delle caselle o degli animali associati, con lo stesso asse temporale. Mantenere questo formato nei successivi aggiornamenti e aggiornare questo collegamento all’ultimo report disponibile, distinguendo sempre prove locali e replay esterni: il report attualmente collegato riguarda prove locali.

- Verifica tecnica: quattro partite complete su due seed esposti e ruoli scambiati; 2876 azioni identiche fra sorgente e bundle, reset e caricatore reale verificati, nessuna dipendenza da filesystem a runtime. [Controlli](../reports/e20_9_release/CHECKS.json).
- Diagnosi interna: margini su E18.2 −1885 e −456, media −1170,5. I ruoli producono gli stessi esiti e non sono repliche indipendenti. [Report](../reports/e20_9_release/REPORT.md).
- Evidenza esterna successiva: massimo1585 verificato nel pannello Rating trajectory della submission56202079 su Kaggle. Questo motiva la scelta di E20.9 come campione corrente; il confronto esterno consolidato e l’attribuzione causale sono ancora da svolgere. Il massimo storico non coincide con lo score corrente (1320,8 nella lista al momento della verifica).
- Le modifiche alla produzione influenzano il mercato condiviso; inoltre il motore accoppia casualità delle infestanti e apertura dei negozi. La stessa cassa avversaria non può essere riutilizzata come baseline fissa fra partite diverse.

## Prossimo sviluppo

Aspettare che maturino i risultati prima dell’analisi. Riprendere dai replay di questo bundle e dai migliori avversari per individuare un nuovo salto strategico verso score2000: organizzazione produttiva, copertura biologica, capacità di lavoro, composizione dell’offerta e impatto sul mercato. I22 KPI sono strumenti diagnostici e di verifica delle ipotesi, non obiettivi da ottimizzare isolatamente.

Proteggere il campione congelato. Ogni nuova ipotesi deve prevedere un ciclo operativo realizzabile, una misura economica e un confronto che distingua effetto proprio e risposta del mercato. Il passaggio da diversificazione programmata a scelta osservata del portafoglio è una possibile linea di ricerca, non una funzionalità già presente né una decisione di implementazione presa.
