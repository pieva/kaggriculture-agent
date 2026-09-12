## 2026-09-12 — E20.8 / E20v40 pubblicata per verifica esterna

Su richiesta utente, ricondotta alla E20 la variante calendario comune con 8C/6S/2G (14 pascoli + 2 pollai, topologia pascoli761). Sorgenti/piani canonici in e20/tools/operational_calendar_{base,goose2}.py e e20/configs/e20v40; bundle `submission/submission_codex_e20_8_e20v40_calendar_2g.py`, SHA256 `3305aef93ac53aa805db01541feb7e79022df1f5e04a2f167d0e6c00b69c63a5`. Parità2876azioni e partita caricatore reale ruolo1 passate. Invio Kaggle confermato dalla UI, ora Complete con punteggio iniziale600.0 (non un rating stabilizzato); stato aggiornato in e20/reports/e20_8_release/PUBLICATION.json. [Scheda release](model_specs/codex/e20/E20_8_RELEASE.md), [report 22 KPI con prezzi](model_specs/codex/e20/reports/e20_8_three_calendars/REPORT.html). E21 conserva esperimenti e provenienza storici. Nessuna modifica strategica rispetto alla Goose2 V2 testata. Commit/push e riordino autorizzati dall’utente.

## Passaggio attivo alla nuova chat: E21 774

Richiesta utente del 12 settembre 2026: salvare lo stato; aprira personalmente una nuova chat per E21. Prima ristudiare la vecchia 774 e confrontarla con la nuova impostazione di pianificazione biologica, missioni complete e analisi economica. Non avviare nuove versioni in questa chat.

**Leggere per primo [il brief E21](model_specs/codex/e21/NEW_SESSION_BRIEF.md)**: contiene base/hash E18, provenienza della 775 dalla routine V9, riferimenti reali alla vecchia 774, confronti proposti, diagnosi recenti e verifiche mancanti. E21 e un ramo diagnostico 774; E18 resta riferimento competitivo. E20 ferma a .7, massimo .10 se riaperta; nessuna prosecuzione automatica del vecchio obiettivo di battere E18. Nessuna nuova simulazione, submission, commit o push per questo passaggio. Le sezioni sottostanti sono storiche e subordinate a questa decisione.

---

## 2026-09-12 — Analisi prima di nuove versioni: routine animale E18/E20

Completata analisi descrittiva dei 14 diretti E18–E20.2 e revisione degli esperimenti storici. Report: `docs/model_specs/codex/e20/reports/livestock_routine_20260912/REPORT.md`, dati ANALYSIS.json. E18 mostra assegnazioni animali più persistenti e minori MOVE/PASS tardivi, ma FEED per animale quasi pari, CARE da distinguere dal bonus monetizzato; più perdite crop per sete. Molti tentativi E18 storici appartenevano alla 770, non alla 775 vincente. Raccomandazione: round mirato sulla E18 775 preservando rotte e topologia, prima audit PLANT→WATER D12–19 e separatamente CARE→bonus→vendita. Questi due audit marginali restano da svolgere: non confonderli con la presente normalizzazione descrittiva. Nessuna nuova versione, simulazione o submission in questa analisi. Attendere il seguito sulla scelta di sviluppo; limite E20.10 conservato per eventuale riapertura del ramo E20.

---

## 2026-09-12 — Selezione candidati per verifica esterna

E20.7 conclusa: 14 partite, margine medio −9662 contro E18, 0/7 seed positivi; NON ADOTTATA. Scelta complessiva E18; scelta esplorativa della serie E20: E20.2, nessuna revisione successiva supera i gate. Nessun upload eseguito. Bilancio: `docs/model_specs/codex/e20/reports/candidate_selection_20260912/REPORT.md`; dati SELECTION.json. Selezione allo stato E20.7; E20.8–E20.10 non generate. Resta il limite massimo E20.10, non proseguire indefinitamente né avviare E20.11. Le sezioni precedenti che richiedono continuazione senza limite o descrivono E20.7 in corso sono storiche e superate. Seed indipendenti 180912401–407 inutilizzati.

---

## 2026-09-12 — Conferma E20.2 conclusa; E20.3 in sviluppo

Torneo a tre completo: 42 partite valide, sette seed 180911301–307 ora esposti. E20.2 contro E18: margine medio -3539, 2/7 seed positivi; contro E19 +1138,7, 5/7 positivi. Decisione DO_NOT_SUBMIT_E20_2. Audit saldi completo, report 22 KPI in `model_specs/codex/e20/reports/e20_2_confirmation/REPORT.html`; dettagli contabili in CASH_GAP.md/JSON e decisione in SUBMISSION_DECISION.md.

E18 meno E20.2: maggiori ricavi +18290,7, maggiori acquisti -14422,4, maggiori assunzioni -329,4, differenza netta +3539. Circa 2679,7 nasce D12–19, solo 859,3 D20–30. Raccolto grano quasi uguale (316,7 vs 313,9), quindi i maggiori ricavi del grano non indicano maggiore produzione: E18 compra e vende più grano. Lana: raccolto 238 vs 137,9, ricavi +6407,1; latte ricavi quasi uguali. E20.2 acquista 10 mucche/6 pecore, E18 8/11 oltre a un'oca. Non attribuire la perdita ai PASS.

Avviata E20.3/E20v33, unica variazione sul portafoglio: 8 mucche/8 pecore, due pecore in Q2, stessa topologia 772 e resto di E20.2 invariato. Protocollo E20_3_PROTOCOL.json congelato, bundle v33 congelato. Screen sei partite seriali: seed 180911301 (prima perdita) e 180911303 (prima vittoria), due ruoli per candidata e un controllo esatto intero per seed. Runner `tools/develop_e20_3.py`, stage `e20_3_mix_development`; non lanciare simulazioni concorrenti. Richiesti delta cassa positivi in entrambi i seed e nessun peggioramento biologico per caso. Poi ampliare ai sette seed esposti, non chiamarli holdout. Nuovi seed 180912401–407 riservati e NON eseguiti. Non modificare policy/bundle/protocollo durante lo screen. Obiettivo utente: proseguire upgrade fondati su diagnosi economica fino a superare E18 in validazione indipendente; nessuna submission automatica.

---

## 2026-09-12 — Torneo indipendente E20.2 / E18 / E19 in corso

Avviato stage `e20_2_confirmation`: 42 partite seriali, sette seed 180911301–307, tutte le coppie e scambio dei ruoli. Questi seed sono ora destinati alla conferma e vanno considerati esposti appena eseguiti; non riutilizzarli per selezionare varianti. Bundle congelati; criteri e hash in [E20_2_CONFIRMATION_PROTOCOL.json](model_specs/codex/e20/E20_2_CONFIRMATION_PROTOCOL.json).

Gate prima dei risultati: E20.2 deve avere margine diretto medio positivo contro ciascun riferimento, positivo in almeno 5/7 seed (ruoli mediati), senza peggiorare stress colture e fughe medi; esecuzioni complete e prive di errori core strumentati. Nessuna submission automatica. Runner riprendibile `tools/confirm_e20_2.py`; log `reports/e20_2_confirmation/RUN.log`, decisione finale attesa in `DECISION.json`. La voce storica sottostante sui seed inutilizzati si riferisce al precedente lavoro diagnostico.

---

## 2026-09-12 — E20.2 generata e verificata localmente

Congelata E20v32, base E20.1/E20v28, topologia 7-7-2. Da D20 esclude nuove offerte CARE quando il prezzo pubblico del prodotto animale è 1; non cambia FEED né sostituisce comandi con PASS. Ipotesi economica sul prezzo corrente, non garanzia di resa futura.

Otto rami completi (quattro controlli esatti e quattro candidate), seed diagnostici 180910201/203, entrambi i ruoli contro E18. 719 chiamate per agente, zero errori core E20, prefisso identico di 456 azioni; controlli identici nelle 263 transizioni successive. Topologia verificata, bundle eseguito senza __file__.

Delta cassa +2775/+4629 sul seed 201 e -907/-907 sul 203; media +1397,5. Margine medio +865. Stress colture e fughe non peggiorano; PASS cresce nel primo seed e cala nel secondo. Decisione DEVELOPMENT_SIGNAL_ONLY: nessuna promozione o submission. Due seed già esposti, non quattro repliche indipendenti; riservati 180911301–307 inutilizzati.

[Specifica E20.2](model_specs/codex/e20/E20_2_SPEC.md) e [report leggibile dei 22 KPI](model_specs/codex/e20/reports/e20_2/REPORT.html). Bundle submission_codex_e20_772_e20v32_candidate.py, SHA256 2e23faa7e581b0ab3a391da0e4707e49d04b6eebeaff4bdb495cacd9e91b317c. Verifica visiva HTML bloccata dalla policy del browser; dati e struttura verificati.

Ripresa: analizzare perché il seed 203 perde cassa e margine nonostante meno PASS, confrontando produzione, vendite e impiego del lavoro liberato. Completare le verifiche CARE/grano/FEED elencate sotto prima di formulare un nuovo intervento. La diagnosi preliminare ha contato 708 richieste CARE D20–30 in sette replay E20.1 (131 a prezzo minimo, nessuna prima del FEED o su animale già curato), ma non misura bonus persi o valore marginale. Non considerare chiuso l'audit del contratto. E18 resta il riferimento esterno; verificare la submission E18 del 10 settembre prima di eventuali nuovi invii.

---

## 2026-09-10 - Chiusura sessione e nuova submission E18

Budget residuo ridotto: fermati gli esperimenti. Reinviato il bundle E18.2 V4D invariato (SHA256 c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7), migliore candidato esterno documentato. Kaggle mostra Pending al salvataggio; punteggio nuovo non ancora disponibile. Punteggi storici osservati: E18 1162,9 (reinvio precedente 1083,5), E19 V48 932,6, E20.1 922,8. Questi punteggi non sono il risultato del nuovo invio.

H001-H006 conclusi come diagnostici, nessuna variante promossa. H006 completo: +18,5 cassa e +34,5 margine medi su due seed/entrambi i ruoli; altri 21 KPI identici. E20v29-v31 restano esperimenti non adottati. Salvati codice, protocolli, risultati e replay compressi. Cache Python escluse da Git e mantenute: cancellazione bloccata dalla revisione automatica. Nessun dato sperimentale eliminato.

Ripresa: verificare prima lo stato della nuova E18 su Kaggle e aggiornare la ricevuta `model_specs/codex/evolution/E18_RESUBMISSION_20260910.json`; non reinviare alla cieca. Leggere il report H006_FULL prima di nuove modifiche. I seed 180911301-307 restano riservati e inutilizzati. Non confondere i piccoli guadagni commerciali H006 con un miglioramento della manodopera.

---

## 2026-09-10 — H006: quattro prosecuzioni complete verificate

Completate quattro prosecuzioni modificate e quattro controlli esatti fino a D30, E19 contro E18, seed 180910204 e 180910206, entrambi i ruoli. Tutti gli otto rami hanno 719 chiamate per agente, DONE/DONE e zero errori nei core strumentati; ogni controllo riproduce 263 transizioni complete dopo 456 azioni ricostruite per agente. Il forecast H006 e ricostruito dalla storia propria e coincide con le predizioni congelate.

Delta cassa terminale medio +18.5, intervallo [+17, +20]; delta margine medio +34.5, intervallo [+32, +37]. Due seed, non quattro repliche indipendenti. Beneficio iniziale esattamente conservato fino a D30: True. Lavoro, servizi e fattorie fisiche invariati in entrambi gli agenti: True. Differenza di cassa isolata negli incassi delle fragole, con uguali volumi/stock finali, altre vendite, acquisti e salari: True.

Sono disponibili le traiettorie dei 22 KPI di entrambi gli agenti, le differenze giornaliere e due grafici completi. Nessuna modifica o promozione dei modelli. Il campione e diagnostico gia esposto; i seed riservati restano inutilizzati. Questa verifica misura la persistenza di un singolo riordino D20 H1: non dimostra una regola utile ogni giorno, un miglioramento della manodopera o un vantaggio su altri avversari.

[Report e 22 KPI](model_specs/codex/evolution/reports/H006_FULL/REPORT.md).

---

## 2026-09-10 — H006: ricavi certi al prezzo minimo

H006 recupera le vendite proprie di prodotti non acquistabili gia al prezzo minimo come ricavi certi, senza stimare il volume concorrente. Soglie e campione invariati rispetto a H005.

Ricostruzioni identificate: 83 -> 116/420; previsioni: 31 -> 40/84. Errori storici 0, errori forecast 0, riordini selezionati 4, riordini negativi 0, delta cassa one-step totale 74.0. Decisione: **DIAGNOSTIC_ONLY_REQUIRES_FULL_CONTINUATIONS**, non adottato.

Passati 120 casi sintetici sul motore, inclusi casi di astensione per fragole e grano al minimo. Riprodotte 420 testimonianze e 84 previsioni senza D20/seguito e senza azioni o stato privato avversari; input e predizioni invariati. Le predizioni H005 restano identiche. Nessuna nuova partita completa, nessuna modifica ai tre modelli, nessun accesso ai seed riservati.

Gli errori sono misurati solo nei casi coperti del campione diagnostico gia esposto (sette seed, ruoli accoppiati). Le astensioni non sono successi. I prodotti che raggiungono il minimo durante il batch restano un limite del modello inverso; il presente esperimento non ne ricostruisce la saturazione.

[Report H006](model_specs/codex/evolution/reports/H006/REPORT.md).

---

## 2026-09-10 — H005: transazioni miste, copertura maggiore ma zero riordini

Completato il seguito preregistrato di H004, con SELL/BUY_PRODUCT/BUY_SEED/HIRE e soglia invariata. Sui medesimi 42 replay diagnostici: 83/420 ricostruzioni identificate (H004: 64), 31/84 previsioni (H004: 18), zero errori nei casi coperti. Tutte le previsioni sono not_first: E18 24, E19 7, E20.1 zero. Nessun riordino selezionato, nessun guadagno dimostrato: NON ADOTTATO.

Passati 24 test sintetici sul motore e riproduzione di 420 testimonianze/84 previsioni senza D20 o seguito, senza azioni/privato avversari, con input e hash predizioni invariati. Diagnosi: 116 residui incompatibili su latte/lana, 50 gia al prezzo minimo iniziale. Prossimo passo: nuovo protocollo per il ricavo certo dei prodotti non acquistabili gia al minimo e, separatamente, saturazione durante il batch. Nessuna modifica ai modelli o ai seed riservati; nessuna nuova partita o submission.

[Report H005](model_specs/codex/evolution/reports/H005/REPORT.md) · [Protocollo](model_specs/codex/evolution/H005_PROTOCOL.md).

---

## 2026-09-10 — H004: previsione da storia propria, utilita operativa zero

Test preregistrato su84situazioni del torneo diagnostico, cinque H1 precedenti D15-D19, nessun accesso ai seed riservati. Modello inverso da cassa/deposito propri, ordini propri e mercato pubblico, con consumo cittadino e costo HIRE ricostruiti. Enumera posizioni prima/uguale/dopo compatibili con ricavi; astensione per acquisti propri, floor, residuo negativo o ambiguita. Forecast con almeno2testimonianze univoche concordi, soglie congelate. Predizioni scritte/hashate prima di leggere le etichette D20 e payoff H003.

420testimonianze:64identificate,0errori storici;14ambigue,10floor,86residuo negativo,108ordini propri non supportati,138senza vendita fragole propria.18/84forecast coperti,0errori: tutti E18 e tutti not_first. E19/E20.1: astensione totale. Nessun riordino H003 selezionato, delta zero. **Non adottato: utilita operativa zero**, non considerare le astensioni successi o la precisione selettiva generalizzazione.

CHECKS: riprodotte420testimonianze e84forecast con D20/seguito rimossi e fattoria avversaria pubblica oscurata; azioni/privato avversari non passati al classificatore, input immutabili, hash predizioni invariato dopo valutazione. Non sono nuove partite complete. Prossimo passo tecnico: acquisti/vendite misti e gestione floor nel modello inverso, poi nuovo test temporale; nessun abbassamento post hoc delle soglie. Il residuo negativo puo derivare anche da floor, non solo acquisti avversari. [Report H004](model_specs/codex/evolution/reports/H004/REPORT.md) · [Protocollo](model_specs/codex/evolution/H004_PROTOCOL.md) · [Controlli](model_specs/codex/evolution/reports/H004/CHECKS.json).

---

## 2026-09-10 — H003: priorita nel batch e concorrenza

Proseguito il metodo a tre. Il mercato esegue gli ordini per posizione nella lista e quota le unita concorrenti in lockstep. H003 preregistrato: una tantum in D20 portare SELL STRAWBERRY davanti alle sole altre SELL precedenti, senza cambiare orario, quantita o lavoro. Condizione basata solo sugli ordini propri.

Scan diagnostico:42transizioni originali esattamente riprodotte,84decisioni,7seed/ruoli. E18 gia prima in28/28casi (non applicabile). E19 applicabile28:19positivi/9negativi, delta medio+29,1; E20.1:20positivi/8negativi,+33,4. Contro E18 14/14positivi per entrambi (+87,0/+87,1); contro altra versione media-28,7/-20,3. Nessuna generalizzazione dal solo avversario E18.

Quattro nuove prosecuzioni complete (due seed201/202 ruolo0), controlli H001/H002 riusati dopo hash: E19 cassa+202/+179, margine+377/+340; E20.1 cassa+157/+195, margine+292/+368. Stati fisici, servizi, stress e fughe identici; quantita fragole vendute identiche, delta cassa interamente incassi fragole, altre vendite/acquisti/salari invariati.719chiamate per agente, DONE/DONE, zero errori core strumentati, parita fino al trigger e controlli fino al terminale. E18 ramo non applicabile, controllo riusato.

Diagnosi retrospettiva: con fragole avversarie in posizione0 ci sono28positivi/0negativi; in posizione1,11/8; in posizione2,0/9. Non e un input osservabile contemporaneo: **H003 non adottata**. Prossimo passo: verificare se la storia osservata permette di stimare comportamento/ordine concorrente, senza usare nomi del modello o azioni avversarie future. Seed di validazione180911301-307 non toccati. [Report H003](model_specs/codex/evolution/reports/H003/REPORT.md) · [Protocollo](model_specs/codex/evolution/H003_PROTOCOL.md) · [22KPI](model_specs/codex/evolution/reports/H003/daily_22_kpi.csv).

---

## 2026-09-10 — H002: separati lavoro fisico e calendario delle vendite

Continuato il metodo a tre, riferimento E18. Scomposizione esatta dei ricavi sul torneo diagnostico42partite: E20.1 meno E19 contro E18 D20-D24, delta vendite-1229,4 = componente volumi+56,0 e componente prezzi realizzati-1285,4. Fragole-865,4 (+149,7 volumi; -1015,0 prezzi). Componente prezzi negativa in5/7seed. Analisi contabile, non attribuzione causale universale.

H002 preregistrato: omissione una tantum della prima richiesta SELL STRAWBERRY in D20; tre modelli, seed180910201/202, ruolo0, avversario reattivo. Sei situazioni, nove nuove prosecuzioni piu tre controlli H001 riusati dopo hash sorgente/bundle/engine. Parita controlli263stati/coppie azioni fino al terminale; trattamenti identici prima del trigger,719chiamate per agente, DONE/DONE, zero errori nei core dotati di contatore.

Delta cassa finale sui due seed: E18-391/-162 (margine-1100/-421); E19+93/+81; E20.1+126/+46. Stress e fughe invariati. In tutti i casi comandi di lavoro di entrambi gli agenti identici, stati fisici delle fattorie identici esclusa cassa, servizi effettivi identici; uguali quantita totali fragole vendute e stock terminale. Delta cassa interamente riconciliato con incassi fragole; altre vendite, acquisti e salari invariati. Primo SELL riuscito rinviato H1->H2, tranne E18seed202 H1->H3. **Nessuna promozione**: due seed, segno opposto fra modelli, nessuna regola universale di ritardo. Ora e verificato un effetto locale del calendario di vendita separato dal lavoro fisico.

Prossima ipotesi da formulare: prezzo ottenibile e concorrenza nelle finestre di vendita, con condizione osservabile, senza applicare un ritardo fisso a tutte le topologie. Il singolo rinvio non spiega tutto il divario medio fra versioni. Seed180911301-307 ancora riservati e non eseguiti. [Report H002](model_specs/codex/evolution/reports/H002/REPORT.md) · [Volumi e prezzi](model_specs/codex/evolution/reports/sales_20260910/REPORT.md) · [22KPI](model_specs/codex/evolution/reports/H002/daily_22_kpi.csv).

---

## 2026-09-10 — Metodo di evoluzione a tre: E18, E19, E20.1

E18 e il riferimento principale per lo sviluppo. Sospesa la successione di euristiche E20: costruito un banco diagnostico che separa traiettorie complete, interventi dallo stesso stato e validazione riservata. Riusate tutte le 42 partite e20_1_confirmation, sette seed ormai esposti, tutti gli accoppiamenti/ruoli; esportati i 22 KPI con identita dell avversario. Finestre senza doppio conteggio D15-D19, D20-D24, D25-D30, flussi di cassa riconciliati esattamente. E19 supera leggermente E18 nella media interna; questo non modifica il riferimento esterno, ma impedisce di assumere una superiorita universale. Contro E18, E20.1 perde 3397 di cassa media rispetto a E19 (migliora in 1/7 seed); D15-D24 il costo del lavoro e identico, il divario contabile e soprattutto nelle vendite.

H001 completato sui tre modelli, seed180910201 ruolo0: ricostruzione di 456 azioni per agente fino a D20; controlli riproducono esattamente le successive 263 coppie di azioni e 263 stati fino al terminale (escluso solo remainingOverageTime). Sei rami completi, 719 chiamate per agente, nessun errore nei core che espongono il contatore. Capsule con stato/configurazione/info seed, riferimenti alla storia e hash engine/bundle. Nessuno scambio di controller fra fattorie.

Intervento una tantum: omessa una richiesta HIRE nel primo batch D20, poi reazione libera di entrambi gli agenti. Delta cassa E18 +7930, E19 +4096, E20.1 +413. **Nessuna promozione**: E18 peggiora stress22->34 e fughe0->1; E19/E20.1 sono risultati locali su un solo seed. E18 resta a11 manovali in D20, E19 ed E20.1 recuperano12 entro H3: il trattamento non equivale alla stessa riduzione di capacita. Lettura competitiva supplementare post hoc: delta margine E18+4167, E19-5469, E20.1+5501; includere il margine esplicitamente nei futuri protocolli.

Seed180911301-307 riservati e non eseguiti. Prima di aprirli congelare candidato, hash, avversari e soglie. Prossimo passo: separare numero/orario/assegnazione della manodopera e spiegare il divario vendite con volumi, prezzi e tempi di consegna; nuovi interventi predefiniti e replicati sul campione diagnostico. [Banco e istruzioni](model_specs/codex/evolution/README.md) · [Analisi a tre](model_specs/codex/evolution/reports/diagnostic_20260910/REPORT.md) · [H001](model_specs/codex/evolution/reports/diagnostic_20260910/H001_REPORT.md).

---

## 2026-09-10 — E20v31: chiusura giornaliera D20-D29, non adottata

Sei confronti completi contro E18 su tre seed esposti, entrambi i ruoli. Servizi su colture/animali esistenti svincolati dalle code nelle ultime sei ore di D20-D29, con controlli di materiali e rientro conservati. Cassa media 61.571,7 -> 60.603,7 (-968; -1,57%); PASS D20-D30 251,3 -> 222,0 (-11,67%); MOVE 1654,3 -> 1693,7 (+2,38%). Coltivate: somma checkpoint 419,7 -> 427,7; stress intera partita 2,33 -> 2,00; zero fughe animali. Solo un seed migliora la cassa; ruoli invertiti identici. **E20v31 non adottata; E20.1 pubblicata invariata.**

Diagnosi baseline seed 180910101 ruolo0, 719 azioni identiche: 209 PASS; tentativi con viaggio/lavoro oltre il tempo in 167 opportunita, blocco coda in 132, materiali mancanti in 15, prenotati in 2, riserva rientro in 10, margine approvvigionamento in 3 (categorie sovrapposte). Solo tre opportunita di lavoratore libero H19-H24 hanno servizi preparabili ignorando le code. Non sono conteggi di PASS evitabili. La variante modifica anche assegnazioni gia eseguibili. Priorita successiva da verificare: costo dei percorsi/rifornimenti prima del finale, senza assumere che piu manovali o meno margine risolvano il problema.

Verifiche: 719 chiamate per entrambi in tutte le partite, DONE/DONE, zero errori core E20v31, topologia772, azioni D1-D19 identiche. [Report](model_specs/codex/e20/reports/labor_closing/REPORT.md) · [Diagnosi](model_specs/codex/e20/reports/labor_closing/DIAGNOSIS_SUMMARY.json).

---

## 2026-09-10 — E20v30: trasferimento mirato del lavoro residuo

Sei partite complete su tre seed gia esposti, entrambi i ruoli contro E18. E20v30 conserva tutte le azioni di E20v28: delta economico e operativo zero. Due trasferimenti provvisori di coda non cambiano il comportamento. **Non adottata**, E20.1 pubblicata invariata.

Diagnosi sul seed 180910101 ruolo0, 719 azioni riprodotte: 209 PASS D20-D30, 161 nelle ore22-24; 194 con preparazioni tutte rifiutate, 7 missioni in attesa di input, 3 con preparazione ma senza assegnazione, 5 senza tentativi. Non equivale a 209 PASS evitabili. Prossimo punto da verificare: rifiuti per tempo/materiali e pianificazione della chiusura giornaliera.

[Report](model_specs/codex/e20/reports/labor_transfer/REPORT.md) · [Traccia](model_specs/codex/e20/reports/labor_transfer/ADMISSION_DIAGNOSTIC.json).

---

Checkpoint precedenti:

## 2026-09-10 — Manodopera D20-D30: primo test concluso

E20v29: code ripianificate ogni ora D20-D29; D1-D19 e gestore terminale D30 invariati. Sei confronti appaiati contro E18 su tre seed gia esposti, ruoli invertiti identici. Cassa +680,7 (+1,11%), positiva in un solo seed; PASS D20-D30 251,3 -> 239,7, MOVE 1654,3 -> 1655,3, costo manovali 3765 -> 3767. Zero perdite animali ma stress 2,33 -> 3,00. **Non adottata**. E20.1 pubblicata invariata.

[Report](model_specs/codex/e20/reports/labor_d20_d30/REPORT.md) · [Dati e protocollo](model_specs/codex/e20/reports/labor_d20_d30/RESULT.json). Prossima ipotesi: trasferimento mirato del lavoro residuo a lavoratori liberi con minor costo di viaggio; non ancora implementato.

---

Checkpoint precedenti:

## 2026-09-10 — Prima coorte E20.1 esterna

Submission **56142698 Complete**, rating osservato alla prima acquisizione **944**. Congelati 22 replay: 21 competitivi e un self-play separato; escluso l'incontro Jessica Jennifer ancora in corso al cutoff. 12/21 vittorie, cassa media 84.022,24 contro 79.886,71, zero perdite animali E20.1 e topologia finale 772 in 21/21. Tutti 720 stati DONE/DONE, ledger riconciliati. Il report mostra i 22 KPI D1-D30 con mediana e banda min-max, CSV e catalogo hash.

[Report esterno](model_specs/codex/e20/reports/external_first_20260910/REPORT.html). Benchmark Top772: identita da chiarire con il proprietario; non presente nel registro o tra gli avversari della coorte. Non sostituire silenziosamente Top772 con Top770-002, gia consumato. Nessuna modifica alla policy o nuova submission in questa acquisizione.

---

Checkpoint precedenti:

# Stato del progetto — E20.1, correzione caricamento Kaggle

Aggiornamento 2026-09-10. Il primo invio E20v28 ha fallito la validazione (episodio 107444826): `NameError: name '__file__' is not defined`, alla prima chiamata. Il loader Kaggle usa un namespace exec senza quel campo; i precedenti test con runpy non riproducevano questa condizione.

Corretto soltanto il nome diagnostico passato a due compile dei moduli incorporati. Il bundle originale resta congelato. Nuovo file: `submission/submission_codex_e20_772_e20v28_loaderfix.py`, SHA256 `9d84c838de39c2c8df620a21db258ea4a4065a5a2b4f75288bde53218d71c9bb`.

Verifica: 2 test di regressione passati senza __file__ e senza letture di file; 719 azioni identiche per ciascuno dei due ruoli (1.438 totali) sui replay E20v28 seed 180910101, usando la funzione agent del bundle caricata con exec. Nessuna modifica alla strategia. Nuovo invio Kaggle: **Pending**; rating non disponibile.

Il risultato interno rimane: +6,16% nello sviluppo, -5,82% nella conferma indipendente contro E18; non promossa economicamente. La pubblicazione serve alla verifica esterna richiesta dal proprietario.

- [Ricevuta del fallimento](model_specs/codex/e20/artifacts/E20_1_EXTERNAL_PUBLICATION_RECEIPT.json)
- [Ricevuta del nuovo invio](model_specs/codex/e20/artifacts/E20_1_LOADERFIX_PUBLICATION_RECEIPT.json)
- [Verifica di parita](model_specs/codex/e20/reports/e20_1/LOADER_FIX_VALIDATION.json)
- [Report economico e 22 KPI](model_specs/codex/e20/reports/e20_1/REPORT.html)

---

Checkpoint precedenti (stati di pubblicazione storici):

## 2026-09-10 — E20.1 inviata per verifica esterna

Su richiesta esplicita del proprietario, caricato su Kaggle il bundle E20v28 congelato (target 772), SHA256 `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. Stato osservato: **Pending**, nessun rating ancora disponibile. Il mancato superamento del gate economico interno rimane registrato; questa pubblicazione e una verifica esterna sperimentale.

[Ricevuta](model_specs/codex/e20/artifacts/E20_1_EXTERNAL_PUBLICATION_RECEIPT.json) · [Submission Kaggle](https://www.kaggle.com/competitions/kaggriculture/submissions).

---

Checkpoint interno precedente (le indicazioni di mancata pubblicazione qui sotto sono storiche):

# Stato del progetto — E20.1, revisione del pianificatore

Lavoro del 2026-09-10 concluso. **Non promossa: il gate indipendente non è superato.** Nessuna nuova pubblicazione Kaggle. La candidata è E20v28, target 7–7–2: percorsi con tile lontani inseriti per primi a parità di urgenza e filtro dei CARE senza incremento produttivo possibile.

Sviluppo: 10 seed già noti, entrambi i ruoli; +6,16% rispetto a E19, 8/10 seed positivi, stress 2,30 per partita, zero perdite animali.

Conferma indipendente: 7 nuovi seed, 42 partite tra E18/E19/E20.1. Contro E18, delta E20.1−E19 -5,82%, 1/7 seed positivi, stress 3,79, perdite animali 0. Il risultato di sviluppo non sostituisce questa verifica.

| Modello | Vittorie / partite | Cassa media torneo |
|---|---:|---:|
| E18 | 20/28 | 60.978,89 |
| E19 | 13/28 | 61.443,11 |
| E20.1 | 9/28 | 59.671,43 |

## Artefatti e ripresa

- [Report finale E20.1](model_specs/codex/e20/reports/e20_1/REPORT.html).
- [Torneo e 22 KPI](model_specs/codex/e20/reports/e20_1_confirmation/REPORT.html).
- [Specifica](model_specs/codex/e20/E20_1_SPEC.md) e [protocollo](model_specs/codex/e20/E20_1_PROTOCOL.json).
- [Decisione verificata](model_specs/codex/e20/reports/e20_1/DECISION.json) e [verifica delle 42 partite](model_specs/codex/e20/artifacts/E20_1_CONFIRMATION_VERIFICATION.json).
- [Bundle E20.1](../submission/submission_codex_e20_772_e20v28_candidate.py).
- [Controllo 770 con lo stesso pianificatore](model_specs/codex/e20/reports/e20_1/topology_control/REPORT.html): controllo di ricerca, non nuova versione ufficiale E19.

SHA256 E20.1: `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. E18 V4D, E19 V48 e la precedente E20v18 restano congelati. Riferimento pubblicato invariato: submission Kaggle 56101593, V48 770.

Tutti i 17 seed usati in questa revisione sono ora esposti: non riutilizzarli come holdout dopo modifiche. Il gate è definito prima dei risultati e distingue cassa media, distribuzione per seed e fragilità biologica. Non promuovere una variante soltanto per il migliore seed o per il numero di WATER/PASS.

Su questo portatile usare un solo processo per i confronti ufficiali. Il solo stato finale DONE non basta: entrambi gli agenti devono ricevere 719 chiamate. Cinque tentativi incompleti del torneo e due del controllo 770 sono archiviati in `invalid_under_load`; sono stati ripetuti senza modificare modelli, seed o limiti di gioco. Non includerli nelle medie.

Il lettore dei replay deve ricostruire il campo condiviso `step` anche per il ruolo 1. Le traiettorie standard e i saldi derivano da ledger verificati. I replay compressi restano disponibili localmente e ignorati da Git.

[Checkpoint precedente E20v18](history/e20_1_before_20260910/PROJECT_STATE.md).
