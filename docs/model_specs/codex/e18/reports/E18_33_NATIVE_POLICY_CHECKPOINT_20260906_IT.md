# E18.33 — policy comune: implementazione e prove diagnostiche

Checkpoint 2026-09-06. **Sviluppo non concluso; nessuna candidata eleggibile.**
La nuova policy non importa i controller storici né le loro traiettorie, ma
non soddisfa ancora il contratto economico e di capacità. Il target del profilo
è 770; la topologia effettivamente raggiunta nelle prove non è 770.
Nessuna submission, nessun nuovo benchmark esterno consumato, E19 non avviata.

## Mandato e separazione E18/E19

E18 deve consolidare una sola policy di pascoli e colture su tutti i quadranti,
con target globale 14, capacità uniforme 7, tre terreni e massimo 12 manovali.
I giorni di acquisto, le coordinate produttive e le colture scelte devono essere
conseguenze dello stato, non righe di un programma. La somiglianza con i KPI
esterni serve a individuare anomalie, non è una funzione obiettivo da inseguire.

E19 verificherà 770, 772 e 662 con codice e criteri congelati, cambiando soltanto
i parametri globali. La [roadmap E19](../../e19/MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md)
non autorizza esperimenti topologici durante questo sviluppo. I casi sintetici
15/16 pascoli e capacità 6 provano il contratto, non sono partite E19.

## Componenti realizzate e limiti

- `tools/e18_33_common_policy.py`: profilo validato, quote per ordine di
  disponibilità, mix globale, generazione uniforme di opportunità, geometria,
  necessità biologiche e flussi di un ciclo produttivo.
- `tools/e18_33_common_controller.py`: adattatore nativo guidato dalle
  osservazioni, prenotazioni e conferme delle missioni, servizi e investimenti,
  acquisti e assunzioni. Non eredita i controller E18.18–E18.32 e non carica piani.
- `tools/run_e18_33_common_gate.py`: prove sul motore originale, ledger e audit
  indipendenti riutilizzati dal runner storico. Il piano letto dal vecchio
  harness non viene passato alla policy nativa. Prezzi e parametri del motore
  sono iniettati come regola pura, non come accesso allo stato nascosto.
- Profilo, kernel, adattatore, runner e motore identificati con SHA-256 negli
  output. Versioni intermedie dell'adattatore conservate in `artifacts/source/`.

**Non realizzati integralmente:** confronto cronologico del portafoglio con/senza
investimento nei due scenari normativi, certificato congiunto di rotte/risorse/
salari/cassa e crescita, riconciliazione completa al cambio giorno e chiusura
terminale, standalone. I valori di singolo ciclo e le stime di carico attuali
sono approssimazioni diagnostiche, non quel certificato. Le priorità rigide di
manutenzione possono ancora rinviare un investimento utile: non costituiscono
la soluzione comune definitiva richiesta dal proprietario.

## Verifiche eseguite

**67 test passati:** 34 sul profilo, 22 sul kernel comune, 11 sul contratto con
il motore e sulle regressioni di finanziamento/distribuzione del mangime.
Inclusi: quote parametriche, candidatura del quindicesimo pascolo sul terzo
terreno in stato sintetico, indipendenza delle funzioni di allocazione dai nomi
dei quadranti, riapertura delle opportunità colturali, tempi di produzione e
necessità biologiche. Questi test non provano ancora l'invarianza dell'intero
controller su ogni stato né l'ottimalità della pianificazione.

Il motore installato non applica una commissione generalizzata del 10% a
BUY_PRODUCT/SELL. I moltiplicatori storici non sono regole del mercato. Il nuovo
adattatore usa il prezzo di acquisto dopo la riduzione dell'inventario e quello
di vendita prima dell'incremento, rispettando il pavimento. Conservatività dei
prezzi ed effettive commissioni non vanno confuse. Il reward terminale è cassa:
non viene attribuita una liquidazione automatica agli asset residui.

## Tutte le prove, incluse quelle fallite

Undici partite original-engine da 720 step. Seed development `180903001`;
V1–V3: seat 0 contro E18.16. V4–V5: entrambi i seat contro E18.16 ed E18.2/V4D.
Non sono un holdout né il gate completo dei sette seed preregistrati.

| Prototipo | n | Cassa media | Controllo E18.31 matched | PASS medi | MOVE medi | Morti colture / fughe animali, totali | Missioni terminali incomplete, totali |
|---|---:|---:|---:|---:|---:|---:|---:|
| V1 nativo | 1 | 13.149 | 85.073 | 1.084 | 2.013 | 36 / 13 | 0 |
| V2 riserva manutenzione | 1 | 20.517 | 85.073 | 1.296 | 1.669 | 59 / 8 | 0 |
| V3 ledger acquisti | 1 | 24.324 | 85.073 | 1.116 | 3.803 | 0 / 0 | 0 |
| V4 offerta futura colture e fertilizzazione | 4 | 45.412,50 | 82.560 | 1.142 | 3.761 | 0 / 8 | 2 |
| V5 ripartizione mangime | 4 | 71.869,25 | 82.560 | 892,25 | 4.024 | 0 / 0 | 2 |

V4 include due interventi e non è un'ablation che ne isola i contributi.
I diversi numeri di casi impediscono di confrontare le medie V1–V3 con V4–V5
come una progressione controllata unica. PASS/MOVE sono conteggi, non efficienza
normalizzata: organico e consistenze produttive cambiano fra i prototipi.

### Dettaglio V5 rispetto al controllo pubblico

| Avversario | Seat | Cassa V5 | Cassa E18.31 matched | Delta | PASS V5 | MOVE V5 | Topologia finale | Missioni incomplete |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| E18.16 | 0 | 75.347 | 85.073 | -9.726 | 908 | 4.027 | 6-5-0 | 0 |
| E18.16 | 1 | 72.309 | 85.073 | -12.764 | 891 | 3.999 | 6-5-0 | 1 |
| E18.2/V4D | 0 | 62.481 | 80.047 | -17.566 | 906 | 4.022 | 6-5-0 | 0 |
| E18.2/V4D | 1 | 77.340 | 80.047 | -2.707 | 864 | 4.048 | 6-5-0 | 1 |

Delta medio **-10.690,75 (-12,95%)**. I PASS del controllo matched sono 846,50
medi, i MOVE 3.446,50: neppure i conteggi operativi complessivi migliorano.
V5 ha zero morti/fughe nei quattro casi, ma non supera il gate: solo undici
animali (sei mucche e cinque pecore), nessun caso exact770, due casi con una
missione incompleta. Non chiamare questi risultati «770 ottimizzata».

Nel primo caso V5 le mucche rimangono zero fino a D7 e salgono a sei in D8;
non viene recuperata una crescita progressiva. I manovali osservati a fine
giorno sono 5, 2, 7, 3, 5, 3, 12, 12, 12, 9 nei primi dieci giorni.
La cassa finale elevata rispetto ai primi prototipi non risolve queste anomalie.

## Diagnosi: fatti, limiti e prossimo intervento

1. **Finanziamento del servizio — difetti verificati.** La crescita iniziale
   senza fondi per la manutenzione ha prodotto perdite. V2 ha poi contato
   nuovamente il grano già acquistato prima di assumere chi doveva distribuirlo.
   V3 sottrae le scorte osservate e non blocca il personale sullo stesso costo
   una seconda volta. Regressioni coperte da test.
2. **Distribuzione del mangime — difetto verificato.** Prima che HIRE fosse
   osservato, il solo contadino prelevava una quota calcolata su un lavoratore,
   lasciando gli assunti senza accesso al grano. V5 divide le scorte anche per
   la capacità di servizio richiesta, senza inviare comandi a lavoratori non
   ancora osservati. Le fughe V4 scompaiono nei quattro casi V5; resta uno smoke.
3. **Crescita e colture — modello economico incompleto.** Il valore del singolo
   investimento non include ancora tutta la sequenza di cassa, salari e
   sostituzioni. Il costo di convertire una coltura considera l'intero ciclo
   originale, non soltanto il valore residuo. La valutazione marginale dei
   volumi colturali non è un rollout del portafoglio. Sono difetti di modello
   osservabili nel codice; non è ancora attribuito causalmente il peso di
   ciascuno sull'arresto a undici animali.
4. **Ammissione e assegnazione — certificato mancante.** Il carico uniforme
   stimato non dimostra la fattibilità delle rotte. Le priorità lessicografiche
   di manutenzione precedono la crescita senza valutare il rinvio economico.
   Occorre certificare insieme servizio esistente, apertura di lavoro utile,
   acquisti e assunzioni; non aspettare che la manutenzione lasci spazio.
5. **Cambio giorno e terminale — da correggere.** Le missioni attive al refresh
   vengono scartate e ricalcolate; due terminali V5 restano incompleti. La
   prenotazione deve comprendere tempi effettivi di approvvigionamento, ritorno,
   consegna e vendita. Nessun PASS ridotto tramite lavoro senza ricavo finale.

Ulteriore copertura di contratto necessaria: `pasture_candidates` può proporre
un pascolo già vuoto anche in un quadrante con quota zero. Questo stato non è
stato prodotto dagli smoke nativi, ma il trattamento degli asset ereditati fuori
quota deve essere esplicito e testato prima di dichiarare generalità del runtime.

Il prossimo incremento deve rendere espliciti alternative e motivi di rifiuto
(valore residuo, fondi, scorte, deadline, percorso, capacità futura), quindi
validare il certificato comune su stati sintetici e sui due campioni interni.
Niente nuovi calendari Q0/Q1, soglie tarate sui Top o obbligo di comprare in D8:
va corretta la decisione generale che produce il gradino, non la sua data.
Prima del gate completo vanno fissati implementazione e protocollo; gli smoke
falliti non autorizzano a scegliere soltanto un seed favorevole.

## Provenienza e ripartenza

Sintesi leggibile da codice:
`artifacts/derived/E18_33_NATIVE_PROBES_CHECKPOINT_20260906.json`, generata da
`tools/summarize_e18_33_native.py`. Elenca tutti gli output sorgente, i casi
matched, i ledger, i cap e i gate falliti; selezione `NONE_ELIGIBLE`.
`complete: true` negli output indica che le simulazioni sono finite, **non**
che il gate sia passato. Gli output originali comprendono serie giornaliere,
eventi di ammissione/completamento e metriche di conferma; non sono replay
pubblici Kaggle né dimostrano il profitto di una politica controfattuale sui Top.

SHA-256 del kernel: `a657eff734049640ef60daa0d5693bfd059dc6f5e9de4bc94108a04d60db06fe`.
SHA-256 dell'adattatore V5: `735aa37693b00826887e25d75aa723fbaaa5fd6a9ec1b52c896126f57c97b308`.

Immutabilità verificata: bundle E18.31
`59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63`,
bundle E18.32 V9
`4d2d32ac41b38af5f4f632ef9e8dd9af2ebd37f7e7bcb1795c2c31cda4e92789`,
piano E18.28 C
`643970c6a8b4b6636f8352d4479c5550c6c985861104b9cc1e126f4723cdf9b8`.
Nessuna pulizia dei raw o alterazione delle baseline, nessun commit/push.
