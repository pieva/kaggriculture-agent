# CODEX — Feedback indipendente sul round C2

```text
AGENT_ID: CODEX
REVIEW_TYPE: INDEPENDENT C2 ROUND FEEDBACK
SCOPE: ANALISI DEGLI ARTEFATTI ESISTENTI
REMEDIATION: NON AUTORIZZATA / NON ESEGUITA
```

## 1. Risposta sintetica

Il risultato C2 non è spiegato da una singola failure tecnica. È il prodotto di una perdita di corrispondenza fra tre oggetti diversi:

```text
correzione causale di un failure E16
policy agricola completa dal reale stato iniziale
candidato economicamente competitivo
```

Il processo ha trattato questi oggetti come se fossero intercambiabili.

La Foundation C2 ha migliorato materialmente la conoscenza dei meccanismi dell'engine, soprattutto su maturity, WATER, WEED, DIG ed EOD. Il mandato comune ha però concentrato i tre MODEL_SPEC sulla stessa diagnosi forense E16 e ha premiato il principio di intervento causale minimo. BUILD e VERIFY hanno poi certificato soprattutto classifier, action dispatch, invocabilità e assenza di regressioni locali. Nessun gate obbligatorio richiedeva che il candidato, partendo da `$3,000`, zero seed e farmer allo spawn, realizzasse la catena completa:

```text
acquisizione
-> accesso spaziale
-> produzione
-> mantenimento
-> raccolta
-> inventario
-> vendita
-> reinvestimento
```

Questo ha permesso due esiti estremi:

- Antigravity aveva una policy nominalmente ampia, ma non raggiungeva neppure il primo turno utile per un errore di contratto runtime occultato dal fail-closed;
- Copilot aveva implementato un frammento locale coerente, ma non una policy inizializzabile: nessun seed bootstrap, nessun movimento, nessuna vendita e binding P1 errato.

Codex ha invece ereditato un loop E16 completo e quindi ha funzionato end-to-end. Tuttavia ha portato nel torneo una policy di trattamento sperimentale deliberatamente stretta, con target 17, routing nearest-task, workforce e mercato lasciati invariati. Ha corretto il lifecycle ma non ha risolto la capacità di mantenere e monetizzare scala. Il risultato è stato un candidato robustamente positivo ma non competitivo rispetto alle evidenze storiche: `$16,846.50` medi, `9.17` crop attive medie e nessun episodio capace di raggiungere il target 17.

Il difetto comune principale è quindi:

> `TOURNAMENT_READY` attestava che un delta locale era implementato e invocabile, non che esistesse una policy agricola completa, realizzata e competitiva.

---

## 2. Cause dei failure tecnici

### 2.1 Antigravity

La catena osservata è deterministica:

```text
observation["private"] reale = dict/Struct del solo agente
-> BUILD lo tratta come lista multi-player
-> private[player_index]
-> KeyError: 0
-> fail-closed silenzioso
-> PASS per 720 step
-> $3,000 e superficie 0
```

I controlli che avrebbero dovuto intercettarla erano economici:

1. una observation reale prelevata da `kaggle_environments.make("kaggriculture")`;
2. una smoke P0/P1 con fallback counter obbligatoriamente a zero;
3. un'asserzione su almeno una transizione della propria farm;
4. un controllo di conformità delle costanti biologiche all'engine.

Non erano obbligatori. I test Antigravity costruivano `"private": [{...}]`, riproducendo la stessa assunzione del BUILD. Il report dichiarava `TOURNAMENT_READY: YES` dopo cinque test locali e la suite repository-wide, senza real-engine smoke documentato.

Classificazione:

| Livello | Valutazione |
|---|---|
| Foundation | `FOUNDATION AMBIGUITY`: la State Machine usa la notazione `private[player_id]` nella sezione sulla visibilità, mentre il callable riceve il proprio `private` già filtrato. Non è la causa sufficiente, ma è un boundary contract formulato in modo fuorviante. |
| MODEL_SPEC | `MODEL_SPEC DEFECT`: manca lo schema top-level dell'observation e manca un acceptance contract end-to-end. |
| BUILD | `BUILD ERROR`: accesso `private` errato; inoltre la failure review ha trovato `player_index`, costanti crop e livestock incompleti. |
| VERIFY | `VERIFY ERROR`: mock non conforme e nessun effetto runtime verificato. |
| Processo | `PROCESS DEFECT`: readiness senza real-engine transition gate e fallback non osservabile. |

L'assunzione non verificata decisiva è stata che `farms` e `private` avessero la stessa cardinalità e lo stesso schema multi-player nel payload dell'agente.

### 2.2 Copilot

Copilot contiene tre blocker indipendenti:

```text
player_index=0 in P1
+ market=[] con seed iniziali pari a zero
+ nessun percorso NORTH/SOUTH/EAST/WEST
```

Il binding errato fa leggere `farms[0]` mentre le azioni vengono applicate a `farms[1]`. Anche correggendo questo difetto, `PLANT` resta irraggiungibile: la policy pianta solo se possiede già seed, ma non può emettere `BUY_SEED`. Anche aggiungendo i seed, il farmer non possiede target spaziali né routing e resta allo spawn. Anche aggiungendo movimento e produzione, non esiste una chiusura inventory-to-cash.

I test verificavano che una funzione sintetica restituisse `DIG`, `WATER` o `HARVEST`, non che tali azioni modificassero la farm del candidato. Il callable test accettava qualunque lista `market`, inclusa una lista permanentemente vuota. Il documento di BUILD dichiarava lo stesso limite come scelta intenzionale e, contemporaneamente, `TOURNAMENT_READY: YES`.

Classificazione:

| Livello | Valutazione |
|---|---|
| Foundation | `NO EVIDENCE OF DEFECT` come causa immediata: movement, market phase, seed precondition e ownership sono descritti. Manca però un initialization contract canonico completo. |
| MODEL_SPEC | `MODEL_SPEC DEFECT`: specifica un controllore locale di tile già raggiunta, non una policy agricola dallo stato iniziale. |
| BUILD | `BUILD ERROR`: binding P0 hardcoded e assenza materiale di bootstrap, movement e market closure. |
| VERIFY | `VERIFY ERROR`: action label equiparata a effetto e nessun test P1/own-state. |
| Processo | `PROCESS DEFECT`: un frammento prevention-only poteva soddisfare le condizioni comuni di readiness. |

L'assunzione non verificata decisiva è stata l'esistenza implicita di seed, posizione utile e working set già attivo. Nessuno di questi presupposti è vero allo step iniziale del torneo.

### 2.3 Perché 168 test verdi non erano evidenza sufficiente

La quantità di test ha mascherato una carenza di copertura semantica. Antigravity e Copilot avevano fixture quasi speculari e testavano gli stessi meccanismi locali. Codex aveva test più accurati sul lifecycle e una smoke reale di 48 step, ma il report chiariva che la smoke verificava soltanto caricamento, schema azioni e compatibilità engine.

Il repository non richiedeva:

- osservazioni reali in entrambi i seat;
- fallback activation pari a zero;
- azioni accettate e non soltanto richieste;
- delta di seed, tile, inventory e cash;
- chiusura di almeno un ciclo produttivo;
- crescita della superficie o della capacità monetizzata.

Il runner del torneo aggravava il masking: il wrapper comune intercettava eccezioni generiche e restituiva `PASS`; il pre-flight chiamato “integrity” controllava percorsi e hash, non l'esecuzione dei candidati.

---

## 3. Cause delle prestazioni economiche di Codex

### 3.1 Scala nominale troppo bassa e scala realizzata ancora più bassa

Codex ha fissato:

```text
2 quadranti = 50 tile possedute
crop target = 17
pasture target = 5
herd target = 4
```

Il crop target usa nominalmente solo il 34% della superficie posseduta. Anche sommando cinque pasture, l'allocazione produttiva nominale arriva a 22/50 tile. Nel torneo la superficie crop media è stata 9.17/50, circa il 18.3% della land posseduta.

I sei raw summary mostrano inoltre:

| Metrica Codex | Evidenza raw C2 |
|---|---:|
| `mean_active_surface` | 9.17 |
| `max_active_surface` | 16 in tutti i sei episodi |
| `final_active_surface` | 6–8 |
| target 17 raggiunto | mai |
| `PLANT` richieste medie | 69.3 |
| `DIG` richieste medie | 39.2 |

La policy raggiunge rapidamente 15–16 crop, poi perde superficie e oscilla per il resto dell'episodio. La correzione lifecycle ha reso possibile il recupero, ma non una continuità prossima al target.

### 3.2 Routing e scheduling dominano l'action budget

Il MODEL_SPEC ha lasciato invariato il nearest-task routing, benché la diagnosi E16 lo classificasse come amplificatore secondario e misurasse già movement share elevate (`0.6060–0.6765`).

Nei raw summary C2 Codex emette in media:

```text
3,861.2 MOVE
su 4,988.3 unit actions classificate
= 77.4% movement share
```

Le azioni direttamente produttive e di servizio considerate insieme sono circa il 12.1%. La reservation è ricalcolata a ogni step, non mantiene un assignment persistente e assegna una sola unità per target anche durante il transito. Il reset EOD dei worker allo shed riapre ogni giorno il costo spaziale. Dieci hands nominali non equivalgono quindi a dieci slot produttivi efficaci.

Il `TOURNAMENT_SUMMARY.md` riporta `MOVE = 1,514.8` per episodio, valore incompatibile con i `total_move_actions` dei sei summary individuali (`3,840–3,890`). Per questa review prevalgono gli artefatti raw. La discrepanza è essa stessa evidenza che la telemetria aggregata non è stata riconciliata prima dell'interpretazione economica.

### 3.3 Workforce fissa, costosa e non workload-derived

Il candidato richiede fino a dieci hands e i raw summary registrano 191 ordini `HIRE` emessi in ogni episodio. I contratti scadono a EOD; la policy tenta quindi di ricostruire giornalmente la capacità, mentre la cassa e il numero di ordini limitano la workforce effettiva.

Non esiste una regola che colleghi il numero di hands a:

- backlog di WATER/HARVEST/DIG/PLANT;
- distanza residua dei task;
- valore marginale atteso dell'azione;
- cassa disponibile dopo obblighi;
- superficie realmente mantenuta.

Questo ripete esattamente la distinzione Foundation `workforce_headcount != worker capacity != monetized actions`, ma il MODEL_SPEC la riconosce senza tradurla in policy.

### 3.4 Capitale bloccato e reinvestimento tardivo

La policy acquista immediatamente land, seed, workforce e animali, mantenendo un floor fisso di `$300`. In tutti e sei gli episodi:

- il minimo cash è `$300`;
- la cassa è a o sotto il floor per 248 step campionati;
- al Day 10 è ancora `$300`;
- il primo incremento di cassa avviene allo step 321, circa Day 13 Hour 9.

Il mix 7 WHEAT / 7 STRAWBERRY / 3 MELON contiene dieci posizioni con `first_yield_day = 10`; il WHEAT è inoltre trattenuto come riserva feed (`herd_target * 3 + 2`). Il risultato è un lungo liquidity lag nel quale l'agente ha già comprato capacità ma non può comporre ricavi e reinvestimenti.

I 390.5 ordini market medi per episodio dimostrano attività richiesta, non qualità economica. La policy non misura marginal payback, executed transaction value, sell-through lag o valore per action. Il mercato è stato “lasciato invariato” proprio dopo che E15 aveva mostrato che, sopra la soglia operativa, monetizzazione e state-capacity alignment discriminavano più della superficie grezza.

### 3.5 Crop horizon ed endgame incoerenti

Lo shutdown blocca nuove semine soltanto negli ultimi 48 step. Questa finestra è sufficiente per WHEAT ma non per STRAWBERRY o MELON, che richiedono dieci giorni, circa 240 step, prima della prima resa. La policy può quindi comprare e piantare crop lunghe quando non esiste più un orizzonte sufficiente per monetizzarle.

La scelta è un gate uniforme di sicurezza, non un vero `crop_horizon_alignment`. Riduce il valore economico degli ultimi cicli e conferma che il lifecycle è stato modellato soprattutto per evitare failure, non per massimizzare cash terminale.

### 3.6 Livestock e byproduct non sono integrati in una strategia di scala

Quattro COW e cinque pasture sono ereditati come bundle conservativo. Il codice dà priorità a pickup/feed/drop e raccoglie fertilizer, ma non stima il costo opportunità sulla crop surface, il carico logistico o il rendimento marginale dell'animale. Il target è fisso e non dipende da feed flow, cash, workforce o capacità di mantenere crop.

Non c'è evidenza che livestock sia la causa primaria dei `$16.8k`; c'è però evidenza che il sottosistema assorba task, acquisti e WHEAT mentre la superficie crop resta molto sotto target. Va quindi classificato come contributo strategico non identificato, non come meccanismo ottimizzato.

---

## 4. Adeguatezza della Foundation C2

La Foundation C2 era sufficiente per evitare molti errori meccanici, ma non sufficiente da sola per costruire una policy competitiva. Questa seconda insufficienza è in larga parte intenzionale: Ontology e State Machine dichiarano esplicitamente di non prescrivere target, routing o strategia.

### Informazione adeguata

La Foundation descrive correttamente e con buon dettaglio:

- ordine delle fasi engine;
- maturity e `first_yield_day`;
- disidratazione EOD e WEED;
- DIG preventive/recovery;
- reset giornaliero dei hands;
- movimento e assenza di collisioni;
- market phase e atomicità di PLANT;
- separazione fra ownership, activation e maintenance;
- separazione fra headcount, capacity e monetized actions;
- distinzione fra eligibility e serviceability.

Queste informazioni erano sufficienti per non costruire una policy senza movimento, senza seed acquisition o con crop constants errate, se BUILD avesse validato il contratto reale.

### `FOUNDATION MISSING INFORMATION`

Manca un initialization contract canonico e testabile che fissi almeno:

```text
starting money
starting seeds/inventory
unlocked quadrants
farmer spawn
own-private observation shape
player ownership binding
```

Il protocollo del torneo registra successivamente `$3,000`, zero seed impliciti nella realtà osservata, NW sbloccato e spawn `(4,4)`, ma questi elementi non sono composti in un contratto Foundation consumabile dai MODEL_SPEC.

### `FOUNDATION AMBIGUITY`

La notazione `private[player_id]` nella State Machine è coerente con lo stato interno globale dell'engine, ma ambigua nel contesto del payload passato al singolo callable, dove `observation.private` è già il dict/Struct del player. La Foundation avrebbe dovuto distinguere esplicitamente:

```text
engine-internal privates[player_id]
agent observation.private
agent observation.farms[observation.player]
```

Inoltre `serviceable_before_deadline`, workforce capacity e varie metriche economiche restano `PARTIALLY_KNOWN` o non freeze-ready. Questo non causa i due blocchi tecnici, ma lascia ai MODEL_SPEC la parte più difficile della trasformazione da meccanica a strategia.

### Valutazione finale Foundation

```text
FOUNDATION-LEVEL ROOT CAUSE OF ANTIGRAVITY/COPILOT FAILURE:
NO

FOUNDATION RUNTIME-BOUNDARY AMBIGUITY:
YES

FOUNDATION SUFFICIENT FOR ENGINE-CORRECT LOCAL MECHANISMS:
LARGELY YES

FOUNDATION SUFFICIENT AS COMPETITIVE POLICY BLUEPRINT:
NO, BY DESIGN
```

Attribuire alla Foundation la sotto-performance economica sarebbe improprio. La responsabilità di trasformare concetti neutrali in un piano di bootstrap, scala e monetizzazione apparteneva ai MODEL_SPEC e al processo di accettazione.

---

## 5. Adeguatezza dei MODEL_SPEC

Il mandato comune dichiarava correttamente che il MODEL_SPEC era una “ipotesi causale implementabile”, ma non richiedeva esplicitamente che fosse anche una policy completa. Consentiva `UNCHANGED`, `DEFERRED` e `NOT_CAUSALLY_PRIORITIZED`, invitava a non modificare tutto e prescriveva previsioni concentrate su HARVEST, WEED, WATER e attainment.

Questa impostazione era adatta a un esperimento di ablation. Era insufficiente per costruire tre concorrenti autonomi.

### Divergenza fra i tre MODEL_SPEC

| Candidato | Come è stato trattato il MODEL_SPEC |
|---|---|
| Antigravity | Specifica apparentemente completa: working set, routing, market, workforce, inventory, livestock e shutdown. La completezza documentale non è stata verificata contro il BUILD. |
| Codex | Delta causale stretto applicato a una policy E16 ereditata. Il documento dichiara esplicitamente invariati routing, workforce, market, land, crop mix e livestock. È completo soltanto perché presume valido l'intero stack E16. |
| Copilot | Insieme di meccanismi locali prevention-first su una tile già raggiunta. Market, routing, bootstrap, vendita e reinvestimento non fanno parte della policy operativa. |

La risposta alla domanda obbligatoria è quindi:

> C2 non ha imposto una nozione comune di “policy agricola completa”. Antigravity l'ha descritta, Codex l'ha ereditata e Copilot non l'ha specificata. Il processo ha valutato i tre documenti come equivalenti perché condividevano struttura, classifier e action semantics.

Il common template ha favorito `local correctness`, `failure prevention` e `constraint satisfaction` a scapito di `end-to-end policy realization`, `productive scaling` ed `economic growth`. Anche la previsione Codex su `final_money` era deliberatamente non direzionale: il candidato poteva correggere il meccanismo ma peggiorare competitivamente senza falsificare la propria ipotesi principale.

---

## 6. Adeguatezza di BUILD e VERIFY

BUILD e VERIFY hanno ottimizzato implicitamente per:

```text
funzione importabile
output formalmente valido
classifier corretto
action branch raggiungibile nel mock
test verdi
nessuna regressione locale
```

Non hanno verificato:

```text
own-state binding
bootstrap dallo stato iniziale
effectful action transition
crescita e mantenimento della superficie
chiusura inventory-to-cash
scaling e reinvestimento
competitività minima contro una baseline
```

I gate mancanti non sono semplicemente “più unit test”. Sono tre controlli semantici distinti:

1. schema runtime reale e seat correctness;
2. state-transition/economic-loop realization;
3. adeguatezza strategica rispetto alle baseline storiche.

La smoke Codex di 48 step ha verificato compatibilità ma non poteva osservare il ciclo delle dieci crop lunghe né il primo cash inflow, che nei replay arriva allo step 321. Antigravity e Copilot non avevano neppure questa smoke reale documentata. Il pre-flight del tournament verificava soltanto hash e presenza file.

Il fail-safe era presente nel candidate wrapper e anche nel runner. Senza contatori, eccezioni e fallback erano osservazionalmente equivalenti a una scelta intenzionale di `PASS`.

Infine, la telemetria ha contato opcode richiesti. Pur raccogliendo traiettorie di money e surface, non ha prodotto il ledger necessario a distinguere in modo sistematico `DISPATCHED`, `ACCEPTED`, `NO-OP`, `FAILED` e `STATE TRANSITION`. La discrepanza MOVE fra summary e raw conferma che anche gli aggregati disponibili richiedevano reconciliation.

---

## 7. Perdita dell'obiettivo strategico

Il punto di svolta è identificabile nel passaggio dalla diagnosi E16 al mandato di build C2.

E16 aveva stabilito:

```text
Stage B bloccato
C* = NONE
target 17 = regione diagnostica, non optimum
routing/workforce = amplificatori non identificati
```

Il mandato successivo ha tuttavia chiesto candidati da torneo preservando il principio di intervento minimo. In Codex questo si è tradotto letteralmente nel riuso dell'infrastruttura E16 e nella modifica dei soli task eligibility/arbitration. Un trattamento sperimentale controllato è così diventato un concorrente senza una fase di sintesi competitiva.

Segnali concreti della perdita di obiettivo:

- tutti i MODEL_SPEC convergono sul failure E16 più recente, riducendo la diversità strategica;
- `final_money` deve essere misurato ma non ha una previsione competitiva o una soglia minima;
- target 17 viene riutilizzato pur non essendo `C*`;
- routing, market, workforce e crop mix possono restare invariati anche se la storia li identifica come discriminanti;
- `TOURNAMENT_READY` non include maintained surface, first revenue o economic closure;
- il torneo parte senza un benchmark attivo e finisce per confrontare Codex con due economie ferme.

La correttezza locale non è stata perseguita “troppo”; è stata usata come sostituto della readiness strategica.

---

## 8. Uso delle evidenze storiche

Le evidenze recenti E16 sono state usate molto bene per maturity, WEED e DIG. Le evidenze più ampie sono state usate in modo selettivo e non operativo.

### Evidenze realmente incorporate

- evitare HARVEST prematuri;
- proteggere WATER continuity;
- recuperare WEED;
- limitare land a due quadranti;
- tenere herd/pasture compatti;
- preservare un cash floor.

### Evidenze riconosciute ma non trasformate in decisioni

- E15: Copilot realizza 25–28 crop con forte sell-through e batte Codex; Codex raggiunge 28–37 crop ma monetizza peggio;
- E15: sopra la soglia operativa, `state_capacity_alignment`, monetization e sell-through discriminano più del volume grezzo;
- E16: A07 raggiunge `$27,076` ma soltanto `0.4706` attainment; quindi profitto e mantenimento sono separati e il target 17 non è validato;
- E16: movement share già superiore al 62% e workforce intermittente sono amplificatori materiali;
- benchmark storici: policy avversarie sopra `$86k–$90k` raggiungono 46–50 tile produttive, con workforce 10–12 e mix di ricavi diversificato;
- benchmark compatto: anche la policy a un solo quadrante da `$50,420` monetizza densamente 15 tile produttive, mostrando che il problema non è “grande sempre”, ma capacità mantenuta e valore per tile/action.

Codex C2 ha scelto 17 crop e ne ha mantenute 9.17 in media; ciò è lontano sia dalla massa produttiva delle baseline grandi sia dalla densità monetaria della baseline compatta. Ha quindi conservato la prudenza di E16 senza acquisire né scala né densità.

### Lesson learned storiche non chiuse

| Lesson | Stato in Codex C2 |
|---|---|
| massa produttiva | target ridotto e mai raggiunto |
| utilizzo del terreno acquistato | basso: 9.17 crop medie su 50 tile possedute |
| working-set dimensioning | 17 scelto come operating region, non come anchor validato |
| workforce | target fisso, non workload-derived |
| routing | nearest-task invariato nonostante movement già elevato |
| livestock | bundle fisso, non ROI/capacity-gated |
| market | regole E16 invariate, nessuna stima di transaction value o reinvestment |
| reinvestimento | primo inflow allo step 321, capitale bloccato a lungo |
| continuità superficie | peak 16, media 9.17, finale 6–8 |

La perdita di continuità con la storia è anche documentale: il mandato comune rende obbligatorie Foundation ed evidenza E16, ma non richiede un confronto esplicito con il Benchmark Registry o con i migliori fingerprint E15 prima di congelare la scala del candidato.

---

## 9. SELF-CRITIQUE

La responsabilità specifica di Codex non è limitata al fatto che “gli altri due non funzionavano”. Il mio candidato ha preso decisioni che spiegano direttamente il proprio ceiling.

### 9.1 Ho confuso isolamento causale e design competitivo

Nel MODEL_SPEC ho scritto che l'intervento era “deliberatamente stretto” e nel codice ho riusato `E16TrainingAgent`, cambiando soprattutto eligibility e arbitration. Ho preservato target, crop mix, routing, workforce, land, market e livestock per non introdurre un secondo trattamento.

Questa è una buona scelta per attribuire causalmente l'effetto della correzione lifecycle. È una scelta insufficiente per presentare il risultato come miglior candidato competitivo disponibile. Avrei dovuto distinguere esplicitamente:

```text
mechanism-validation build
competitive synthesis build
```

e non dichiarare il primo direttamente `TOURNAMENT_READY`.

### 9.2 Ho scelto target 17 senza un capacity anchor

Sapevo che:

- `C*=NONE`;
- A07 non era un optimum;
- A07 aveva attainment `0.4706`;
- E15 osservava policy operative a 25–37 crop.

Ho comunque fissato 17 come candidate operating region. Il fatto di averlo dichiarato “non optimum” ha reso la decisione epistemicamente corretta, ma non strategicamente adeguata. Il torneo ha mostrato che nemmeno 17 era mantenibile: peak 16, media 9.17, finale 6–8.

### 9.3 Ho lasciato invariato un routing già sospetto

La diagnosi E16 riportava movement share 0.6211 per A07 e classificava routing/workforce come amplificatori. Ho scelto nearest-task per isolare il lifecycle. Nei replay C2 il movement share raw sale al 77.4%.

Questa decisione ha trasformato gran parte della workforce in capacità di transito. Non posso attribuire il risultato soltanto a weed o seed: il mio MODEL_SPEC aveva già identificato il rischio e ha deliberatamente deciso di non trattarlo.

### 9.4 Ho mantenuto una strategia di capitale e crop mix incompatibile con compounding rapido

Land, seed, hands, COW e feed assorbono rapidamente la cassa fino al floor. Dieci delle diciassette crop hanno maturity a dieci giorni, mentre il WHEAT è trattenuto per feed. Il primo aumento cash arriva soltanto allo step 321.

Ho protetto la solvibilità, ma non il tempo di ritorno del capitale. Il floor fisso previene bankruptcy; non costituisce una strategia di reinvestimento.

### 9.5 Ho usato un endgame gate non crop-aware

Il cutoff uniforme di 48 step consente semine STRAWBERRY/MELON molto oltre il punto in cui possono produrre prima del terminale. La policy conosce `first_yield_day`, ma non lo usa per decidere se un nuovo investimento è monetizzabile entro l'orizzonte.

### 9.6 Ho verificato il delta, non l'intero sistema

I test Codex disabilitano workforce, pasture e livestock nella maggior parte delle fixture e si concentrano sui branch lifecycle. La smoke reale di 48 step ha certificato `DONE`, non superficie, transizioni o cash. Non ho richiesto un full-loop effect test, una prova P1 esplicita o una baseline economica minima prima di `TOURNAMENT_READY: YES`.

In sintesi:

> Ho costruito correttamente la correzione che avevo specificato, ma ho specificato una correzione troppo stretta per l'obiettivo competitivo e ho certificato come ready un sistema le cui limitazioni note coincidevano con i principali driver economici ancora aperti.

---

## 10. Critica del processo comune

| Finding | Classificazione | Evidenza |
|---|---|---|
| Observation/private boundary non canonico | `PROCESS DEFECT` con `FOUNDATION AMBIGUITY` | Notazione Foundation e mock concorrenti non allineati al payload callable reale. |
| Antigravity non operativo | `CANDIDATE DEFECT` + `PROCESS DEFECT` | KeyError, fail-closed, nessuna real-engine smoke/effect gate. |
| Copilot non inizializzabile | `CANDIDATE DEFECT` + `PROCESS DEFECT` | Spec e build non contengono bootstrap/movement/market; readiness lo consente. |
| Codex sottoscala | `STRATEGIC ERROR` + `MODEL_SPEC INTERPRETATION` | Reimpiego del trattamento E16, target 17, routing/market invariati. |
| Unit test verdi | `NO EVIDENCE OF END-TO-END CORRECTNESS` | Fixture sintetiche e asserzioni su opcode, non su state transition. |
| Runner fail-closed | `EXPERIMENTAL DESIGN DEFECT` | Eccezioni generiche convertite in PASS senza telemetry di fallback. |
| Tournament comparability | `EXPERIMENTAL DESIGN DEFECT` | Due candidati non realizzano policy; il round non discrimina tre MODEL_SPEC competitivi. |
| Mancato mirror automatico | `NO EVIDENCE OF DEFECT` per la domanda principale | Le failure sono di own-state correctness, non prova di bias ambientale sistematico. |
| Assenza di baseline attiva | `EXPERIMENTAL DESIGN DEFECT` | Codex è confrontato soltanto con economie ferme; manca un anchor competitivo comune. |
| Foundation mechanics | `NO EVIDENCE OF ROOT DEFECT` | I meccanismi necessari erano in larga parte presenti e corretti. |

Tre decisioni comuni hanno aumentato maggiormente la probabilità del risultato:

1. promuovere direttamente dal forensic E16 a un tournament build prima di chiudere un capacity anchor;
2. definire `TOURNAMENT_READY` tramite proprietà locali e repository health;
3. impedire una verifica competitiva comune dei candidati prima del freeze, lasciando al runner soltanto hash validation.

Il torneo stesso è stato eseguito correttamente rispetto al protocollo congelato. Il difetto sperimentale è a monte: il protocollo ha ricevuto candidati non comparabili e non possedeva un validity gate per respingerli.

---

## 11. Tre modifiche prioritarie al processo futuro

### Priorità 1

```text
MODIFICA:
Sostituire l'attuale readiness smoke con un unico REAL-ENGINE EFFECT PREFLIGHT
obbligatorio, eseguito sul reale stato iniziale sia come P0 sia come P1. Il preflight
deve rendere osservabili eccezioni e fallback e deve seguire almeno un percorso
candidate-owned da acquisizione risorsa a state transition produttiva e cash delta.

PROBLEMA RISOLTO:
Intercetta observation contract errati, hardcoded player index, bootstrap impossibile,
assenza di movimento, action no-op e fail-closed loop prima del torneo.

EVIDENZA:
Antigravity sarebbe fallito al primo accesso a private; Copilot avrebbe mostrato
BUY_SEED=0, MOVE=0 e active surface=0; la smoke Codex di 48 step non verificava effetti.

RISULTATO ATTESO:
Nessun candidato entra nel torneo senza realizzare sulla propria farm almeno le
transizioni essenziali dichiarate dal MODEL_SPEC. Due prefix run P0/P1 hanno costo
molto inferiore ai nove episodi spesi in un confronto non conclusivo.

COME FALSIFICARLA:
La modifica è falsificata se un candidato supera il preflight con fallback=0 e con
delta coerenti di risorsa/tile/inventory/cash, ma nel torneo replica deterministicamente
una failure di schema, ownership o bootstrap già presente nel preflight.
```

### Priorità 2

```text
MODIFICA:
Rendere obbligatoria nel MODEL_SPEC una INITIAL-STATE REACHABILITY & ECONOMIC-CLOSURE
TABLE. La tabella deve separare il delta causale sotto test dalla policy competitiva
ereditata e mostrare, per ogni arco, precondizione reale, branch implementato, effetto
atteso e fallback: capital -> acquisition -> movement -> plant/produce -> maintain ->
harvest -> inventory -> sell -> reinvest. Un sottosistema UNCHANGED deve indicare il
codice realmente ereditato, non soltanto il nome.

PROBLEMA RISOLTO:
Impedisce di confondere una collezione di meccanismi locali o un trattamento di
ablation con una policy autonoma completa.

EVIDENZA:
Copilot soddisfaceva la struttura documentale pur non avendo acquisition, routing o
sale. Codex era completo solo per ereditarietà E16; Antigravity descriveva componenti
che il BUILD non realizzava fedelmente.

RISULTATO ATTESO:
I buchi di raggiungibilità emergono prima del codice e il reviewer può verificare
MODEL_SPEC -> branch -> state effect senza introdurre una nuova tassonomia generale.

COME FALSIFICARLA:
La modifica è falsificata se la tabella risulta completa e fedele al codice congelato,
ma una semplice analisi di raggiungibilità dallo stato iniziale dimostra ancora che
nessun percorso verso output monetizzato è possibile.
```

### Priorità 3

```text
MODIFICA:
Separare MECHANISM VALIDATION da COMPETITIVE SYNTHESIS. Dopo il preflight funzionale,
eseguire per ogni candidato un solo economic sentinel preregistrato contro una baseline
frozen competente e su seed non usati nel torneo. Il sentinel non seleziona il vincitore:
verifica soltanto maintained surface, utilizzo land, movement share, first-revenue time,
cash-lock duration e chiusura reinvestimento rispetto a bound storici dichiarati.

PROBLEMA RISOLTO:
Evita che una cella di training controllata, valida per isolare un meccanismo ma priva
di scala o monetizzazione, venga promossa direttamente a candidato competitivo.

EVIDENZA:
C*=NONE e A07 non-optimum erano noti; Codex ha comunque portato target 17 e routing
invariato. Un singolo sentinel avrebbe mostrato peak 16, media circa 9, 77.4% MOVE,
248 step al cash floor e first inflow allo step 321, contro fingerprint storici da
25-50 tile produttive o alta densità monetaria.

RISULTATO ATTESO:
Il torneo confronta policy funzionali che hanno almeno superato un bound strategico
minimo, mentre il tuning resta confinato alla fase TRAINING e i seed del torneo
rimangono puliti.

COME FALSIFICARLA:
La modifica è falsificata se i sentinel preregistrati non predicono né failure di scala
né ordine di grandezza economico su più round, oppure se il costo aggiuntivo non riduce
materialmente il numero di tornei non informativi.
```

Queste sono esattamente tre modifiche. Non propongo una proliferazione di gate indipendenti: ciascuna sostituisce un punto debole esistente con un controllo ad alto information gain.

---

## 12. Decisione singola che cambierei

Se potessi cambiare una sola decisione presa prima del tournament C2, cambierei questa:

> Non avrei dichiarato `TOURNAMENT_READY: YES` per Codex dopo la smoke di compatibilità da 48 step; avrei richiesto un episodio real-engine preregistrato che dimostrasse mantenimento della superficie e chiusura del primo ciclo inventory-to-cash prima del freeze.

È una decisione concreta perché avrebbe modificato il gate Codex già esistente, non la Foundation né il torneo. Avrebbe mostrato prima del confronto che il candidato non raggiungeva 17, spendeva la maggioranza delle azioni in movimento e generava il primo inflow soltanto allo step 321. Lo stesso criterio, applicato simmetricamente, avrebbe respinto Antigravity e Copilot senza spendere nove episodi in un confronto prestazionale non conclusivo.

```text
C2_ROUND_FEEDBACK_COMPLETE
NO_REMEDIATION_PERFORMED
```
