# NEW_SESSION storico — prima del checkpoint anti-PASS, 2026-09-05

Cronologia precedente, non istruzioni correnti. Ripartire da `docs/NEW_SESSION.md`.

## Standard dei confronti — KPI D1-D30 (2026-09-05)

Il formato corrente è V3: **sempre Top770 vs una sola versione sotto esame**,
mai tre agenti sovrapposti. Conservare i 19 pannelli V2 e aggiungere WATER
e FEED riusciti al giorno (21 pannelli standard); eliminare il diagramma
Cause PASS. Tutte le cinque colture e le tre specie animali, anche zero,
cassa, persone, totali e strutture vuote distinte restano. Affiancare i KPI storici
di economia, lavoro, resa, qualità e sicurezza; i grafici di consistenza
non sostituiscono le tabelle operative. Definizioni e normalizzazioni:
`experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V3_IT.md`.
Report corrente e audit:
`docs/model_specs/codex/e18/reports/E18_29_SIMULATION_REPORT_IT.md`.
Il report E18.27 V3 resta l'esempio storico del formato originario.

COOP vuoti Top770: uno D11-D12, rimosso D13; due costruiti D29 e presenti
a D30. Zero oche possedute nei 720 stati di ognuno dei cinque replay.
Non sono animali nello shed o fughe. BUILD_COOP non addebita denaro nel
motore locale e impedisce spawn spontaneo di weed sulla tile; uso anti-weed
plausibile ma intenzione non dimostrata. Non classificarli come spreco certo.
Questa decisione cambia il reporting, non la priorità di sviluppo sotto.

## Priorità corrente — Top770 e produzione D25-D30 (2026-09-05)

Decisione più recente del proprietario: usare **Top770** come alias nella
documentazione e passare all'analisi D25-D30, comprendendo la produzione di
carote e non soltanto la chiusura. Questa priorità prevale sulla sequenza
storica di ulteriore consolidamento D10-D15 riportata sotto.

Analisi completata su cinque replay final-770 e 14 profili E18.27 V3 contro
E18.16. Top770 esegue 42 semine D26-D29 negli stessi slot: 6 sempre Carrot,
36 a scelta Wheat/Carrot; stessi WATER/HARVEST e 87 unità spostate tra specie.
Tre replay producono 99 Carrot, due ne producono 12; non è una composizione
fissa da copiare. In D25-D30 gli annuali raccolti sono 260 contro 184 locali.
Due semine D29 non maturano: escluderle. Entrambe le specie maturano a età 2;
le carote non sono più precoci del grano. D28 è soltanto il limite agronomico,
da anticipare dove la missione di consegna/vendita non termina entro D30.

Prossima specifica E18.28: A = chiusura/logistica delle missioni esistenti;
B = annuali tardive solo Wheat; C = stesso piano B con selettore Carrot/Wheat.
Congelare D1-D24 anche nel lookahead di mercato. Tenere separate le ablation
di Strawberry, FEED/CARE e Fertilizer. Nessuna nuova policy implementata.

E18.27 V3 resta non promossa, con regressioni e difetti D10-D15 già registrati;
non sono stati corretti o occultati durante questa diagnosi. Nessun holdout,
submission, commit o push. Runtime, config e piani congelati conservano i
propri identificativi tecnici storici per compatibilità; testi e titoli usano
Top770, con episode ID e hash come provenienza. Non interpretare l'alias come
garanzia che ogni episodio storico citato sia 770: il filtro resta esplicito.

Diagnosi:
`docs/model_specs/codex/e18/reports/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS_IT.md`.
Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_28_770_LATE_ANNUAL_MISSIONS_V1.md`.
Dataset:
`docs/model_specs/codex/e18/artifacts/derived/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS.json`.

## Ultimo sviluppo — E18.27 V3 verificata, non promossa (2026-09-05)

Implementata la prima fase D10-D15: Melon raccolti D11, vendita nello stesso
batch dei DROP reali, semine Q2 concentrate D12 dopo l'incasso, almeno 11
hands D11-D12. D1-D9 identico a E18.26 anche negli ordini di mercato; V3
corregge la retroazione del lookahead rilevata in V2. Chiusura D30 invariata.

Verifica su 18 casi matched unici / 36 episodi: E18.26 ed E18.27 contro
E18.16 su sette seed × due seat, e contro E18.25 ed E18.2/V4D sul seed
180903001 × due seat. Esiti candidati: zero fughe, FEED completo D11-D15,
zero errori, 770 e cap 14/max 12 hands in tutti i casi. Il target 61 crop e
14 animali a D15 passa nello smoke iniziale, non in tutti i seed estesi.

Contro E18.16: media candidata 69.156 contro parent 60.964,64 (+13,44%),
10/14 delta positivi, ma worst -21.920 e sconfitte dirette 14/14 contro
E18.16 (media 86.316). Contro E18.25: +18,87% matched e vittorie 2/2.
Contro E18.2/V4D: +2,01% matched, ma un seat negativo e sconfitte dirette
2/2 (57.680 contro 85.694). V3 resta development, non candidata all'upload.

Problemi residui: tre casi con crop D15 incompleti; seed 180903007 già con
un animale mancante D10, non recuperato (finale 9 Cow + 4 Sheep); regressioni
economiche nei seed 3/4. Nel seed 4 seat 0 siamo avanti a D15/D20, poi
perdiamo già D20-D25: più Milk/Strawberry venduti ma meno ricavi e meno
Wheat venduto. Non è dimostrato che basti la sola correzione dell'ultimo D30.

Ripresa: consolidare acknowledgement crop e recupero dei posti vuoti in
D10-D15; trattare separatamente monetizzazione/chiusura D20-D30 con gate
matched e senza tuning sul seed. Non tornare a cambiare topologia o apertura.
La seconda fase D30 non è stata implementata, né sono stati consumati
holdout/final-confirmation. Nessuna submission, promozione, commit o push.

Specifica corrente:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_27_770_D10_D15_CASHFLOW_V3.md`.
Report temporale e confronto completo:
`docs/model_specs/codex/e18/reports/E18_27_D10_D15_CONSOLIDATED_V3_REPORT_IT.md`.
Dataset:
`docs/model_specs/codex/e18/artifacts/derived/E18_27_D10_D15_CONSOLIDATED_V3.json`.
Questa sezione prevale sulle indicazioni storiche di versione seguente.

## Priorità di ripresa — D10-D15, poi chiusura D30 (2026-09-05)

Decisione più recente del proprietario: salvare le diagnosi e concentrare
la prossima versione sulla finestra D10-D15; affrontare la chiusura entro
D30 soltanto in una seconda fase verificata separatamente. Questo handoff
prevale sui NEXT_ACTION e sulle proposte storiche riportate più avanti.
Restano 7-7-0, 14 pascoli, cap 14 animali e massimo 12 hands più farmer.

Il gradino Top770 D11 è principalmente vendita Melon: 72 unità raccolte in
D11, vendute 60 in D11 e 12 in D12; E18.26 raccoglie le stesse 72 in D13 e
vende 36 in D13 e 36 in D14. Il planner mantiene il default di raccolto D13,
ma i Melon sono raccoglibili da D11: nella riesecuzione locale, dopo le
azioni D11, 11 tile hanno resa 6 e una resa 5. L'incasso locale è 11.262
contro 14.267–16.717 Top770; il delta pubblico non è causale perché cambiano
seed, avversario e prezzi. Pareggiare PLANT/WATER non prova parità per tile.

I pascoli si svuotano al cambio D13-D14, non durante D13: zero FEED D12 e
8/13 FEED D13 causano cinque fughe (3 Cow + 2 Sheep), 13→8; la Sheep già
prevista porta poi a 9. Nell'ultimo batch D13 arrivano l'incasso di 36 Melon
e cinque Wheat comprati, troppo tardi per distribuirli prima del refresh.
Da D14 non viene comprato alcun animale, neppure quando la cassa recupera:
prevenzione delle fughe e risposta ai vuoti sono problemi distinti.

Prima fase: preservare D1-D9 e isolare D10-D15, preparare WATER/HARVEST e
consegne/vendite Melon D11-D12, riservare cassa/mangime/azioni per FEED e
personale prima dell'espansione, riattivare le tile liberate verso i target
D15. Verificare contro E18.26 e i campioni interni, con seed preregistrati,
entrambi i seat e KPI temporali fino a D30. Le regole D16-D30 restano
invariate in questa prima ablation; le conseguenze sullo stato si misurano.
Il solo harvest-first Wheat D13 è una protezione di riserva, non più la
prima ipotesi: interviene dopo l'inizio della crisi.

Seconda fase: sulla migliore versione D10-D15 verificata, prenotare a ritroso
gli ultimi raccolti/consegne/vendite entro D30 prima di ridurre gli hands;
cutoff basati sulla monetizzazione possibile, non sul solo giorno di semina.
Non combinare i due trattamenti prima dei rispettivi confronti interni.

Analisi completa, evidenze e gate:
`docs/model_specs/codex/e18/reports/E18_26_D10_D15_CASH_FEED_DIAGNOSIS_AND_NEXT_PRIORITIES_IT.md`.
Model spec aggiornato:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_26_770_TOP770_BOOST_D10_V1.md`.
E18.26 resta non promossa; in questo salvataggio nessun codice, config,
piano congelato, submission, commit o push è stato modificato/eseguito.

## Decisione operativa corrente — target 7-7-0 e ciclo quotidiano (2026-09-04)

La topologia target per tutti i prossimi sviluppi Codex è `7-7-0`. Il lock
resta in vigore fino a quando il gap dai top non sarà stato ridotto in modo
consistente e ripetibile; fino ad allora non si aprono nuove linee `6-6-2`,
`7-7-x`, `10-7-0` o altre ablation topologiche. Le topologie osservate nei
replay dei leader restano evidenza strategica e diagnostica, non un motivo
per cambiare il trattamento durante l'ottimizzazione della `7-7-0`.

Lo sviluppo delle nuove versioni avviene contro un roster versionato di
campioni interni. Il campione incumbent e gli avversari ammessi devono essere
congelati per ciascuna matrice, con seed development preregistrati, entrambi i
seat e telemetria completa. Il confronto interno è la fonte primaria per
diagnosi causale, ablation e selezione del candidato giornaliero, perché
consente di osservare stato, azioni, lifecycle, routing, economia e failure
mode senza dipendere dal campione parziale dei replay pubblici. Ogni nuova
versione modifica una sola famiglia causale; holdout e final-confirmation
restano separati dal development.

È istituito il seguente ciclo quotidiano:

1. sviluppare e confrontare le candidate `7-7-0` contro i campioni interni;
2. selezionare il migliore sviluppo della giornata sulla base di risultati
   seat-balanced, integrità, sicurezza e KPI economici/operativi;
3. eseguire una sola submission Kaggle quotidiana del candidato selezionato,
   dopo parity e gate tecnici minimi, come verifica esterna e non come
   promozione automatica;
4. registrare artefatto, hash, submission ID, score in stabilizzazione e
   replay osservati; i risultati esterni alimentano le ipotesi della giornata
   successiva e non il tuning iterativo della stessa giornata;
5. analizzare quotidianamente gli agenti in testa alla leaderboard. Il
   benchmark di default usa gli attuali primi quattro e gli ultimi cinque
   replay completati per ciascuno, deduplicando gli episodi condivisi e
   registrando topologia, timing di espansione/contrazione, composizione,
   lifecycle, routing, MOVE/PASS, servizio crop, economia e chiusura.

La submission quotidiana è quindi autorizzata in via permanente dal
proprietario per il solo miglior sviluppo `7-7-0` del giorno. Non consuma né
sostituisce holdout/final-confirmation, non autorizza upload multipli per
inseguire il rating e non rende Kaggle un set di training. Le note storiche
che indicano `NO_UPLOAD`, `NOT_AUTHORIZED` o upload bloccato continuano a
descrivere correttamente il verdetto delle singole versioni, ma non annullano
questa policy successiva.

## Stato operativo dopo gate E18.17 V1 (2026-09-04)

E18.17 V1, prima implementazione della priorità lifecycle/missione HARVEST,
è `REJECTED_SAFE_BUT_BEHAVIORALLY_INERT`. Sul gate development completo
contro E18.16 (sette seed, entrambi i seat, 14 match) conserva esattamente
`7-7-0`, fill 14 e cap 14, con zero perdite livestock, errori e fallback.
Tuttavia non modifica alcuna azione: PLANT bloccati, override locali e
route/service mission aggiuntivi sono tutti zero. Tutti i KPI aggregati sono
identici a E18.16; il grezzo `1-1` è soltanto effetto seat sul seed
`180903004`.

Il confronto successivo con E18.2/E17 V4D non è stato eseguito perché il gate
preregistrato richiede un effetto causale osservabile. E18.16 resta la base
interna e la migliore submission disponibile; nessuna nuova submission viene
prodotta da E18.17 V1. Holdout e final-confirmation non sono stati consumati.

I pre-gate hanno inoltre falsificato quattro interventi troppo larghi: blocco
PLANT aggressivo (`-28%` output), cutoff terminale (`-3,6%` output), anche soli
sei MOVE ritardati, e WATER locale sugli accessi shed (due perdite livestock
per match). Il prossimo sviluppo ammesso parte quindi dal capacity/trajectory
planner E18.18 e soltanto dopo costruisce il dispatcher nativo, preservando
azioni strutturali, logistica e shed; non riapre topologia, cap 14 o FEED.

Report:
`docs/model_specs/codex/e18/reports/E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_DEV_GATE_REPORT_IT.md`.

## Decisione E18.18 — planner prima dell'agente (2026-09-04)

La prossima versione non deve nascere da un altro override locale. Prima si
costruisce un simulatore offline esatto che, dati `7-7-0`, 14 pascoli e 12
hands più farmer, determina layout, mix e numero delle crop tile, coorti,
cutoff operativi e traiettorie per turno. Il modello prenota WATER/HARVEST,
FEED/CARE/collection, movimento e logistica fino alla liquidazione e ammette
una tile soltanto se resta almeno l'1% di capacità giornaliera nominale. Il
rolling replan deve assorbire separatamente la variabilità live: il benchmark
Top770 mostra picchi incompatibili con una riserva statica del 15%.

E18.18 segue `PLAN → EXECUTE → ACK → DAILY_REPLAN`. Nessun agent build è
ammesso prima della parità del simulatore con l'engine e del Gate 0 oracle;
solo dopo si usano i sette seed development e infine i campioni interni.
Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_18_770_CAPACITY_TRAJECTORY_PLANNER_V1.md`.

Prima baseline estratta: E18.16 mirror, seed `180903001`, player 0. La matrice
Q0/Q1/Q2 contiene 75 tile × 720 step e `7.296` eventi richiesti sulla tile
sorgente; `222` eventi originano in Q3 e restano nel riepilogo fuori matrice.
I colori M01–M12 identificano gli slot hand giornalieri; il farmer è separato.
Artefatto:
`docs/model_specs/codex/e18/artifacts/derived/E18_16_BASE_TRAJECTORY_MATRIX_S180903001_P0.json`.

### Stato E18.18 al 2026-09-05

Gate 0 oracle superato. Il planner deterministico riproduce nell'engine esatto
tutti i checkpoint Top770, `7-7-0`, `9 COW + 5 SHEEP`, 61 crop a
D15/D20/D25, zero starvation, liquidazione completa e money `117.077`.
PLANT, DIG e WATER effettivamente emessi hanno ack 100%; il replay di conferma
ha lo stesso hash e outcome. L'unlock NE di D7 è finanziato da due drop WOOL
separati prima dei PLANT e gli spawn degli hands assunti a T2 vengono
ricalcolati sulle posizioni osservate.

Il primo smoke development `180903001`, entrambi i seat contro E18.16, è
`FAIL`: E18.18 `55.934` contro `85.578`, topologia corretta ma soltanto
`7 COW + 4 SHEEP`. Le guardie state-aware evitano comandi illegali, ma non
reinseriscono ancora un task bloccato da weed; la deviazione si propaga a
PLANT, FEED e PLACE. Il Gate 1 completo e la submission restano bloccati.

Prossima azione: backlog per-worker `DIG → retry`, correzione di posizione,
priorità hard FEED/PLACE e rolling replan giornaliero; poi ripetere lo smoke
prima dei 14 match preregistrati. Stato dettagliato:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_18_770_CAPACITY_TRAJECTORY_PLANNER_V1.md`.

## Stato E18.19 — retry della traiettoria (2026-09-05)

E18.19 V1 implementa il backlog richiesto senza cambiare il piano E18.18:
coda giornaliera per worker, correzione di posizione, `DIG → retry`, recupero
di `BUILD/PLACE`, prelievi parziali con un retry residuo e uscita limitata dai
prerequisiti non finanziabili. Hash piano, `7-7-0`, 14 pascoli,
`9 COW + 5 SHEEP`, crop plan e mercato restano congelati.

Il delta causale diretto contro E18.18 è `PASS`: mediana `93.361` contro
`54.933,5` (`+69,95%`), vittoria in entrambi i seat, topologia e composizione
finale esatte, zero errori. Il primo smoke contro l'incumbent E18.16 è invece
`FAIL`: mediana `51.517` contro `78.653,5` (`-34,50%`). La regressione non è
più una rottura strutturale: E18.19 mantiene 14 animali, chiude crop e shed e
lascia soltanto quattro righe fuori giornata per esecuzione, ma sotto contesa
registra per seat 19 FEED e 11 PLANT saltati.

E18.19 è quindi una candidata development generata ma non promossa. Gate 1 a
14 match, holdout, final-confirmation e upload Kaggle restano bloccati. La
prossima ablation ammessa mantiene immutati piano e route e isola soltanto
procurement/liquidazione sotto contesa, dopo avere derivato quantità, prezzi e
opportunity loss dal replay matched contro E18.16. Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_19_770_RETRYING_TRAJECTORY_V1.md`.

## Stato E18.20 — Wheat market netting (2026-09-05)

E18.20 V1 corregge una sola inefficienza di E18.19: dal D11 compensa nello
stesso batch `SELL WHEAT` e `BUY_PRODUCT WHEAT`, senza cambiare piano, route,
crop, animali o workforce. La diagnosi iniziale misurava, contro E18.16,
`2.942` unità vendute e `2.776` ricomprate, incluse 566 unità di round trip
nello stesso batch.

Il delta diretto E18.20–E18.19 è `PASS`: E18.20 vince entrambi i seat
(`+456`, `+78`), mediana `+267`, elimina da D11 rispettivamente 566/608 unità
di overlap e conserva `7-7-0`, `9 COW + 5 SHEEP`, shed/crop terminali vuoti e
zero errori. La variante con riserva aggregata fino a D+2 è stata respinta:
riduceva fortemente il churn e i FEED saltati, ma peggiorava il money.

Il gate contro E18.16 resta `FAIL`: mediana E18.20 `51.522` contro `78.648,5`,
delta `-27.126,5` (`-34,49%`). Gate 1 completo, holdout, final-confirmation e
upload Kaggle non sono autorizzati. Il prossimo sviluppo deve sostituire la
riserva aggregata con un ledger Wheat per obbligazione e worker, così da
eliminare il churn cross-turn residuo (`SELL 2.377 / BUY 2.211`) senza
immobilizzare capitale. Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_20_770_WHEAT_MARKET_NETTING_V1.md`.

## Stato E18.21 — Wheat obligation ledger (2026-09-05)

E18.21 corregge il gap temporale tra azioni worker e mercato: un
`PICKUP WHEAT` emesso veniva rimosso dai fabbisogni prima dell'esecuzione del
batch e le stesse unità potevano essere incluse in `SELL WHEAT`. Dal D11 il
controller registra l'obbligazione per worker e protegge la vendita soltanto
nello step corrente; piano, route, `7-7-0`, 14 animali e 12 hands restano
immutati.

Il delta diretto contro E18.20 è `PASS` in entrambi i seat (`+371`, `+59`;
mediana `+215`). Il trattamento interviene in 15 turni, protegge 115 unità e
riduce, contro E18.16, le richieste da `SELL 2.377 / BUY 2.211` a
`SELL 1.798 / BUY 1.646`. Topologia/composizione esatte, zero errori e zero
overlap Wheat da D11.

Il gate E18.16 resta `FAIL`: mediana `51.534,5` contro `78.644,5`, gap
`-34,47%`; il miglioramento assoluto sullo smoke E18.20 è soltanto 12,5 punti.
Le varianti con contratti D+2 riducono i FEED saltati da 19 a 12 ma peggiorano
il money e sono respinte. Gate 1 completo e upload non sono autorizzati. La
prossima ablation mantiene il guard in-flight e limita il procurement Wheat a
D+1, evitando di acquistare e poi rivendere la quota attribuibile soltanto a
D+2. Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_21_770_WHEAT_OBLIGATION_LEDGER_V1.md`.

## Stato E18.22 — Wheat JIT D+1 (2026-09-05)

E18.22 mantiene E18.21 e rimuove soltanto gli acquisti Wheat attribuibili a
D+2: dal D11 il procurement copre pickup in-flight, fabbisogni residui odierni
e D+1. Non modifica piano, route, `7-7-0`, 14 animali o 12 hands.

Il delta diretto E18.22–E18.21 è `PASS` in entrambi i seat (`+2.293`,
`+1.947`), mediana `+2.120` (`+2,84%`). Contro E18.16 il candidato sale da
`51.534,5` a `52.041,5`; il gap mediano si riduce a `-26.447` (`-33,70%`) ma
il gate resta `FAIL`. Struttura esatta, zero errori e zero overlap Wheat da
D11.

Le richieste Wheat contro E18.16 scendono a `SELL 365 / BUY 220`, ormai
paragonabili alle `SELL 415–417 / BUY 469` dell'incumbent; i FEED saltati
scendono da 19 a 12. Il mercato Wheat non è più il gap dominante. Restano 11
PLANT, 40 HARVEST, 102 WATER e 80 FERTILIZE saltati per seat: la prossima fase
deve classificare le cause di rifiuto PLANT/HARVEST e intervenire sul lifecycle,
senza cambiare procurement o topologia. Gate 1 completo e upload non sono
autorizzati. Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_22_770_WHEAT_JIT_D1_V1.md`.

## Stato E18.23–E18.24 — ablation lifecycle respinte (2026-09-05)

La diagnostica successiva ha scomposto i rifiuti crop di E18.22. Le 11
`PLANT` per seat sono tutte richieste D11 verso la SW ancora bloccata. Il terzo
quadrante costa 2.000: a D10 H24 E18.22 dispone di 1.479 prima della vendita
di quattro Fertilizer, quindi non può sbloccarlo. E18.23 anticipa a D10 il cap
Wheat JIT D+1, ma le cinque unità acquistate servono già entro D+1: nessun
ordine viene eliminato, lo SW resta a D12 H1 contro E18.16 e l'outcome è
identico a E18.22. Nel diretto parent le mediane coincidono e i margini sono
`+174/-174`. E18.23 è respinta.

E18.24 tenta di recuperare le 11 semine nello slot della successiva visita
`WATER` sulla stessa tile, senza MOVE o route aggiuntivi. Contro E18.16 tutte
le 11 tile sono già occupate al primo passaggio: recuperi reali zero e outcome
ancora identico a E18.22. Nel diretto parent compare un solo recupero per seat,
ma i margini `+304/-40` non sono robusti e gli HARVEST respinti salgono a
43–44. E18.24 è respinta. La classificazione aggregata mostra inoltre 65
`HARVEST` su tile vuote e 15 su weed nei due seat: il conteggio grezzo degli
skip è principalmente storia obsoleta, non opportunity loss misurata.

E18.22 rimane il miglior sviluppo corrente, ma non supera E18.16: mediana
`52.041,5` contro `78.488,5`. La prossima famiglia causale deve essere un
nuovo planner crop `7-7-0` che aumenti cicli completati e monetizzati, con
focus D21–D30 e gate espliciti su `PLANT/WATER/HARVEST` eseguiti, unità crop
vendute e money. Non sono ammessi altri overlay generici sugli skip o sui
`PASS`; Gate 1, holdout, final confirmation e upload restano bloccati.

Specifiche:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_23_770_SW_UNLOCK_LIQUIDITY_V1.md`
e
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_24_770_DEFERRED_PLANT_ON_WATER_V1.md`.

## Stato E18.25 — D10 labor step (2026-09-05)

Il confronto temporale con Top770 ha isolato il primo gap a D10: E18.22 aveva
7 unità attive, mentre il benchmark exact `7-7-0` ne aveva 12. La causa era
nel planner E18.18, che selezionava il minimo di 6 hands più farmer perché 161
slot coprivano le 156 azioni nominali; non era un errore `HIRE` né un vincolo
di liquidità.

E18.25 introduce un solo vincolo: minimo 11 hands a D10. In engine raggiunge
12 unità reali in entrambi i seat, preserva checkpoint crop/animali, topologia
`7-7-0`, `9 COW + 5 SHEEP` finali e zero errori. Sul confronto matched contro
E18.16 passa da 52.379/51.704 di E18.22 a 52.563/51.888: delta esattamente
`+184/+184`, mediana 52.225,5.

Il salto riduce i MOVE D10 da 65 a 59, ma lascia invariate le 91 azioni
produttive e aggiunge 120 PASS, pari a cinque unità per 24 turni. Il gap di
workforce è quindi recuperato, ma non quello di throughput: contro E18.16 la
mediana resta sotto 78.959,5 e il gate incumbent fallisce. E18.25 diventa il
miglior sviluppo matched post-E18.22, senza autorizzazione a Gate 1 o upload.

La prossima famiglia causale deve mantenere le 12 unità a D10 e ripianificare
D7–D10 per assegnare agli slot liberi cicli completi `PLANT/WATER/HARVEST` con
vendita entro D10. I gate primari sono HARVEST e unità crop monetizzate
cumulative, costo HIRE, denaro D10 e delta positivo su entrambi i seat. Non
sono ammessi altri aumenti della manodopera privi di task né cambi simultanei
a topologia, animali o Wheat procurement. Specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_25_770_D10_LABOR_STEP_V1.md`.

## Stato E18.26 — Top770 BoostD10 (2026-09-05)

La verifica replay corregge l'ipotesi “Top770 non usa Melon”: i cinque replay
storici exact `7-7-0` mostrano invariabilmente 12 Melon a D1/D5/D10, e anche
l'episodio corrente `105717134` ne mostra 12 a D10. I Melon vengono ritirati
prima di D15; il Top770 corrente non è però più exact `7-7-0`, quindi il target
controllato resta la coorte storica omogenea.

E18.26 mantiene topologia, 14 pascoli, cap 14 e 12 hands, ma porta il piano
D1–D10 da `PLANT/WATER/HARVEST/MOVE = 51/186/18/457` a
`63/254/30/529`. PLANT e WATER coincidono con Top770 (`63/254`), HARVEST resta
a `-2`; la replica non è ancora totale perché Top770 ha `790 MOVE`, 670 azioni
produttive e 221 PASS contro `529/598/570` del candidato. In engine tutte le
quattro esecuzioni raggiungono 11 hands e il mix D10
`12 MELON + 20 STRAWBERRY + 5 WHEAT`.

Il segnale economico è positivo: diretto contro E18.25, E18.26 ottiene mediana
`63.096` contro `61.269,5`; nel confronto matched contro E18.16 migliora il
risultato congelato E18.25 di `+2.198/+2.080`, `+2.139` in mediana. Il gate
resta tuttavia `FAIL`: sotto contesa con E18.25 D5 ha temporaneamente 5 Wheat,
e la transizione SW/payroll lascia FEED scoperto in D12–D13, con composizione
finale non exact 9+5. Nessun Gate 1, holdout, final confirmation o upload.

La proposta iniziale harvest-first Wheat D13 è superata dalla diagnosi
Melon/cassa: il successore isola D10-D15, conservando D1-D9 e anticipando
incassi e copertura FEED a D11-D12. Il Wheat D13 resta una protezione di
riserva, non il primo intervento. Segue la chiusura D30 in una fase separata.
Specifiche e gate correnti sono nel nuovo handoff in testa e nella specifica:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_26_770_TOP770_BOOST_D10_V1.md`.

### Evidenza Top770 estesa a D20 (2026-09-05)

L'episodio corrente `105717134` è stato acquisito a fine D1/D5/D10/D15/D20
con mappa tile-per-tile. Conserva l'opening crop della coorte exact `7-7-0`,
inclusi i 12 Melon a D10, ma è una strategia diversa: a D15 usa 18 slot
zootecnici `11-7-0`, 17 animali e una coop vuota; a D20 reclama la coop in
Wheat e chiude la fase a `10-7-0`, 17 animali (`5 Cow + 8 Sheep + 4 Goose`) e
58 crop (`33 Strawberry + 25 Wheat`). Money D10/D15/D20:
`3.233/19.149/48.939`.

Questa osservazione non riapre il lock Codex `7-7-0`. Per il successore di
E18.26 restano normativi i cinque replay exact `7-7-0`: ritiro completo dei
Melon entro D15, 14 animali `9 Cow + 5 Sheep` e 61 crop
`38 Strawberry + 23 Wheat` a D15-D20. Il replay corrente aggiunge soltanto due
ipotesi trasferibili: reclaim state-driven di una struttura vuota e analisi
separata, futura, della monetizzazione Goose/topologia dopo la riduzione del
gap 770.

Report canonico:
`docs/model_specs/codex/e18/reports/TOP770_REPLAY_105717134_D01_D20_ANALYSIS_IT.md`.
Artefatto con provenienza e mappe:
`docs/model_specs/codex/e18/artifacts/derived/JESSE_BULLARD_REPLAY_105717134_D01_D20_2026_09_05.json`.

### Confronto quotidiano D1-D20 E18.26 / Top770 770 (2026-09-05)

Ricostruiti tutti i checkpoint H24 dei primi 20 giorni, usando i cinque
replay storici Top770 con topologia finale 7-7-0 e due esecuzioni E18.26 contro
E18.16 sul seed development 180903001. I reward e i checkpoint E18.26
coincidono con il gate congelato. Persone = hands assunti + farmer, anche
fuori griglia; specie = tile effettivamente occupate, posti vuoti separati.

D10 coincide, ma D11-D12 E18.26 ha 9 persone contro 12. Top770 ritira i Melon
a D11 e arriva a 38 Strawberry a D12; E18.26 ritira i Melon a D13 e rimane a
29 Strawberry. A D14 E18.26 passa da 13 a 9 animali (6 Cow + 3 Sheep), contro
14 Top770; conserva 5 pascoli vuoti fino a D20. Da D16 entrambe hanno 13
persone, ma a D20 persistono 52 crop contro 61. Carrot/Tomato/Goose sono zero
in tutti i checkpoint dei due campioni. Le consistenze sono identiche fra
i replay del rispettivo campione, senza variabilità osservata su queste metriche.

Precisazione: Top770 è selezionato sulla topologia finale; nei transitori
D11-D12 ha 15 strutture e a D14 ne ha 16, rientrando a 14 da D15. Questo
non modifica il cap 14 Codex né autorizza una nuova topologia.

Report e dataset riproducibili:
`docs/model_specs/codex/e18/reports/E18_26_TOP770_D01_D20_TRAJECTORIES_IT.md` e
`docs/model_specs/codex/e18/artifacts/derived/E18_26_JESSE_770_D01_D20_TRAJECTORIES.json`.

### Estensione a D30: cassa, chiusura e fughe verificate (2026-09-05)

Completati i 30 checkpoint dei medesimi cinque Top770 final-770 e due seat
E18.26. Ogni batch worker+market è ricostruito su una copia del suo stato:
719 batch per profilo, 10.066 saldi cassa dei due giocatori verificati senza
scarti. Vendite/acquisti nel dataset sono eseguiti, non soltanto richiesti.

Correzione rispetto all'inferenza D20: al cambio D14 scappano cinque animali
(3 Cow + 2 Sheep), passando da 13 a 8; la Sheep prevista viene piazzata
durante D14 e porta il totale a 9. Nessun acquisto di animale da D14 in poi:
i cinque pascoli vuoti persistono fino a D30. Top770 non ha fughe.

Top770 mantiene 61 crop fino a D27, avvia da D23 il ritiro Strawberry con
rotazione Wheat/Carrot e tiene 12 persone a D26-D30. E18.26 chiude le crop
a D29 e arriva a 3 persone a D30. Nell'ultima giornata i flussi delle azioni
sono 5.122–8.562 netti Top770 contro -81/+70 Codex; non coincidono esattamente
con la differenza dei checkpoint H24, per il confine di campionamento.
D21-D30: Top770 vende sempre 189 Strawberry e 135 Milk, Codex 84 e 54;
Fertilizer venduto 131–140 contro zero. La variabilità pubblica è soprattutto
economica: 135 Milk generano 731–30.308 secondo episodio e prezzo.

Cassa D30: mediana Codex 54.364,5, Top770 75.629 [59.508–120.267]. Le due
coop vuote Top770 D29-D30 sono separate dai pascoli nei grafici. Resta la
priorità D10-D15, aggiornata dalla diagnosi Melon/cassa in testa al documento,
seguita dalla chiusura D30 in una fase separata. Il refill richiede margine
e scadenza, il taglio hands missioni complete. Nessuna implementazione o submission.

Report e dataset:
`docs/model_specs/codex/e18/reports/E18_26_TOP770_D01_D30_CLOSURE_IT.md` e
`docs/model_specs/codex/e18/artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json`.

## Stato operativo dopo submission E18.16 (2026-09-04)

La submission autonoma `submission/submission_codex_e18_16_770.py` è stata
completata da Kaggle con score `729,0`, contro `1199,7` di E18.2: delta
`-470,7` (`-39,24%`). SHA-256:
`4CD8F18F317D4C654F9CAB7E019EEE3ABAB906C65B46FA842B6A009EF5EB0350`.
La verifica esterna conferma il fallimento del Gate B e impedisce la
promozione di E18.16; non consuma holdout o final-confirmation locali.

Sviluppo attivo: solo Codex exact `7-7-0`. Antigravity, Claude e Copilot sono
`FROZEN_PERFORMANCE_GAP`; usarli soltanto come evidenza storica o avversari
black-box. La prossima ipotesi Codex è E18.17 lifecycle/route completion
D11-D30, senza cambiare topologia, cap 14 o guard FEED.

Foundation C2.1 verificata: `NO_FOUNDATION_REVISION_REQUIRED`.

## Handoff ottimizzazione WATER 7-7-0 post Top-3 (2026-09-04)

Aggiornamento: E18.16 `cap 14 + critical FEED` passa Gate A su 14 match.
Massimo 14 risorse in tutti i match, clamp e FEED attivi una volta per match,
zero perdite contro 14, fill/topologia esatti, zero errori/fallback/breach.
Money `+1,18%`, matched `+0,67%`, worst `-0,95%`, record `8–6`; MOVE `+0,13%`
e unità `+0,19%`. Gate B Top-3 fallisce. E18.10 V2 resta il controllo
congelato, mentre E18.16 è la nuova base di ricerca; l'upload esterno è stato
successivamente autorizzato ed eseguito.
Report:
`docs/model_specs/codex/e18/reports/E18_16_770_EXACT_CAP_CRITICAL_FEED_DEV_GATE_REPORT_IT.md`.

La linea E18.11–E18.15 è chiusa senza promozione. E18.11 converte in WATER
comandi locali invalidi, ma su 14 match lascia money, late unwatered, harvest
e unità invariati. E18.12 conferma che il cap 15 non causa la perdita animale,
ma identifica e rimuove un vero spreco: il provider compra il 15° animale a
D12 H3 dopo avere già raggiunto 14 risorse a D12 H2. Il cap 14 è quindi
accettato come invariante delle prossime `7-7-0`; da solo resta economicamente
neutro perché dopo la morte D20 compra un rimpiazzo. E18.13 elimina tutte le
perdite (`0` contro `14`) e migliora le medie, ma fallisce il worst matched
(`-2,85%`) e viene respinta standalone.

I due pre-gate successivi chiudono l'ipotesi “più WATER” come leva autonoma.
E18.14 rimuove coop/oca: WATER `+2,05%` e MOVE `-0,39%`, ma money `-2,94%`.
E18.15 aggiunge un hand WATER Q2 tra D15 e D19: `+21` WATER, ma harvest, unità
e late unwatered restano identici; money `-1.165`, esattamente il costo dei
cinque hire. Nessuna matrice completa è stata eseguita per E18.14/E18.15.

E18.10 V2 resta il best research control exact `7-7-0`. Il prossimo passo non
è un altro overlay WATER: E18.17 deve sincronizzare lifecycle crop e route
completion tra D11 e D30, mantenendo topologia, 12 hands, coop/oca e cap
COW/SHEEP 14 con safety FEED D20. Il profilo dei top è un target diagnostico: dalla fase
D11–D20 e ancor più D21–D30 combinano più PLANT/WATER/HARVEST con meno
MOVE/PASS. Holdout e final-confirmation restano bloccati. Gli upload ad hoc
restano vietati; vale soltanto la submission quotidiana disciplinata dalla
decisione operativa corrente. Sintesi:
`docs/model_specs/codex/e18/reports/E18_770_WATER_OPTIMIZATION_POST_TOP3_EVIDENCE_REPORT_IT.md`.

## Handoff E18.10 V2 WATER-before-DIG (2026-09-04)

La linea WATER è stata implementata e testata mantenendo `7-7-0`. E18.10 V1
è invalidata: il WATER inserito nella task queue poteva sovrascrivere logistica
non-PASS sullo shed access `(4,5)`, lasciando fill `13/14` e causando tre
perdite per match. Non usare V1.

E18.10 V2 corregge il meccanismo: dopo E18.9 converte esclusivamente un PASS
finale in WATER quando il worker è già su una Strawberry viva e unwatered; non
muove worker ed esclude `(4,5)`. Contro E18.9 chiude `12–2`, fill esatto
`14/14` in `14/14`, perdite uguali, zero errori/fallback/breach/override
non-PASS. Money `+1,70%` (matched `+1,46%`, worst `-0,05%`), WATER `+1,77%`,
DIG `-11,44%`, late unwatered `-4,10%`, late crop tile-days `+5,21%`, harvest
`+1,77%`, move `-0,22%`, ratio `-0,42%`.

Gate A resta `FAIL` soltanto su tre soglie di volume: crop service `+0,51%`
contro target `+1%`, unità `+0,58%` contro `+1%`, PASS `+0,22%` contro target
`-1%`. Gate B Top-3 fallisce. E18.10 V2 è il best research control 770, non
una release e non autorizza holdout/final/upload. Prossimo passo: aumentare la
copertura WATER dentro le priorità del dispatcher senza aggiungere movimento
né intercettare shed/logistica. Report:
`docs/model_specs/codex/e18/reports/E18_10_V2_770_WATER_BEFORE_DIG_GUARD_DEV_GATE_REPORT_IT.md`.

## Handoff ottimizzazione 7-7-0 E18.7–E18.9 (2026-09-04)

Sono state eseguite tre ablation topology-matched contro E18.6, sempre con
topologia e fill esatti `7-7-0`, 14 match development, entrambi i seat e senza
consumare holdout/final o autorizzare upload.

- E18.7 PASS→servizio sul tile corrente: sicura ma inerte; soltanto due WATER
  aggiuntivi per episodio, nessun delta su harvest o money.
- E18.8 PASS→missione crop adiacente nello stesso quadrante: respinta `0–14`;
  PASS `-17,3%`, ma `1.132/1.372` missioni cancellate, harvest `-32,0%`, money
  matched `-15,59%`. Anche un passo overlay rompe le traiettorie del provider.
- E18.9 guard del crop vivo: sopprime il DIG calendarizzato sui cinque target
  reclaimed senza rerouting. È la migliore candidata di ricerca: `10–4`,
  money `+0,48%`, worst matched `-0,95%`, late crop tile-days `+4,93%`, harvest
  riusciti `+2,33%`, unità `+2,78%`. Gate A resta formalmente `FAIL` perché le
  soglie preregistrate 5–10% non sono raggiunte; nessuna promozione.

Conclusione: il gap non si chiude “riempiendo i PASS” con movimento. La leva
positiva è preservare il lifecycle senza perturbare le traiettorie. Prossima
ablation: sugli stessi target, trasformare DIG protetto in WATER in-place
quando il crop vivo è unwatered; nessun altro cambio. Report principale:
`docs/model_specs/codex/e18/reports/E18_9_770_LIVE_CROP_ROTATION_GUARD_DEV_GATE_REPORT_IT.md`.

## Handoff E18.6 7-7-0 concentrata (2026-09-04)

La prova richiesta contro E18.2 è completa e respinta. La nuova variante
costruisce e riempie correttamente `7-7-0` in 14/14, ma perde `0-14`: money
`58.957,00` contro `71.104,43`. La concentrazione non riduce le move
(`+0,32%`); productive `-5,70%`, move/productive `+6,38%`, PASS `+23,26%`,
harvest `-6,90%`. Il lavoro zootecnico eliminato non viene sostituito dal
lifecycle crop Q2. Inoltre il cap 15 su 14 slot causa una perdita verificata
per match. Holdout/final non consumati, nessun upload. Report:
`docs/model_specs/codex/e18/reports/E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_REPORT_IT.md`.

Conclusione: l'intuizione geometrica è realizzabile, ma questa V1 mostra che
una 7-7-0 non guadagna efficienza conservando le rotte 7-7-5. Prima di
riprovare la topologia serve un lifecycle scheduler nativo che trasformi il
Q2 crop-only in throughput e accorci realmente le tratte.

Il confronto topology-matched successivo usa soltanto `7-7-0`: 14 profili
Codex contro due Giulio e quattro Top770; Crop non ha equivalenti esatti ed è
escluso. Con la tassonomia action normalizzata, Codex emette `+2,9%` comandi
totali ma ha PASS `+60,5%`, move `+4,1%`, crop service `-18,1%`, harvest
riusciti `-31,7%` e raccolto `-36,7%`. Il vecchio gap productive Top-3 era
sovrastimato per definizioni diverse: quello confrontabile è `-7,5%`.
Priorità: PASS → task crop nello stesso cluster, lifecycle persistente, poi
route completion; cap animali 14 separato, tredicesimo worker solo dopo.
Report:
`docs/model_specs/codex/e18/reports/E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_IT.md`.

## Handoff Top 3 corrente (2026-09-04)

Lo snapshot corrente verificato è Crop Dusta `3035,3`, Giulio Ravasio
`2976,0`, Top770 `2963,4`. Sono stati analizzati 11 replay head-to-head recenti: Crop
6-2 nel campione, otto action shape e sette topologie; Giulio usa zero pasture
Q2 in 7/7, moda `7-5-0`, e ripete una action shape in 5/7; Top770 conferma lo
stesso archetipo compatto. Tutti eseguono `3.237–3.377` productive e raccolgono
`887–917` unità con rapporto move/productive `1,01–1,26`, contro `2.223`,
`513` e `2,0026` di E18.5.

La conclusione del benchmark era che il fail 6-6-2 fosse di throughput, non
di geometria, e raccomandava un lifecycle controller da E18.2/V4D prima della
Q2 crop-only. La prova E18.6 ha deliberatamente invertito l'ordine su richiesta
e ne ha rafforzato la diagnosi: la sola 7-7-0 non riduce le move. La prossima
specifica resta quindi un lifecycle/router nativo; nessun nuovo numero è
ancora assegnato.
Report:
`experiments/e18/reports/common/E18_CURRENT_TOP3_STRATEGY_RECONSTRUCTION_2026_09_04_IT.md`.

## Handoff E18.5 6-6-2 (2026-09-04)

L'ablation controllata della topologia `7-7-2 → 6-6-2` è completa e respinta
al gate di efficienza. Su 14 match development comparabili la candidata
ottiene `4.451,86` move (`-0,57%`), `2.223,07` productive (`+0,25%`) e rapporto
`2,0026` (`-0,82%`) rispetto alla E18.4 V2 7-7-2 congelata. Il segnale è
favorevole ma non raggiunge la soglia `-5%`. Integrità completa: 6-6-2 e fill
14/14 in 14/14, zero errori/fallback/perdite/PASS azionabili/thrashing.
Money `+4,09%`, harvest `+8,59%`, late weeds `-40,08%`, ma record `0-14`
contro E18.2. Nessun holdout/final/upload. Report:
`docs/model_specs/codex/e18/reports/E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_REPORT_IT.md`.

## Handoff E18.4 V2 (2026-09-04)

Non caricare `CODEX-E18.4-STATE-DRIVEN-772-V1` né V2: entrambe sono respinte.
V2 passa topologia/fill, safety, zero PASS azionabili e zero route thrashing,
ma fallisce Gate A su move, productive, move/productive, harvest e late weeds.
Risultato: `0-14`, money `47.247,57` contro `77.644,29`; Gate B non eseguito.
Prima di una V3 serve una nuova specifica causale sul throughput, non un tuning
degli stessi pesi. Artifact e diagnosi V2 sono in
`docs/model_specs/codex/e18/artifacts/derived/E18_4_STATE_DRIVEN_772_V2_DEV_GATE.json`
e `docs/model_specs/codex/e18/reports/E18_4_STATE_DRIVEN_772_V2_DEV_GATE_REPORT_IT.md`.

## Ripresa operativa

```text
START_HERE: docs/PROJECT_STATE.md
FOUNDATION: C2.1 RECONCILED
FOUNDATION_MANIFEST: docs/foundation/FOUNDATION_C2_1_MANIFEST.md
REPOSITORY_CLEANUP: COMPLETE
REPOSITORY_REORGANIZATION: COMPLETE / A0-A7 PASS
REPOSITORY_REORGANIZATION_STATUS: COMPLETE
COMMON_EXECUTION_PROMPT: experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md

CURRENT_CODEX_MODEL: CODEX-E17.3-TOPOLOGY-FILL-662-V2
CURRENT_CODEX_SUBMISSION: submission/submission_codex_e17_topology_662.py
CURRENT_CODEX_SUBMISSION_SHA256: 3DF5C15D078552AF0A3849653057303698C9D750B4C7BB087B8A29092FADBAE8
E18_2_CANDIDATE_MODEL: CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1
E18_2_CANDIDATE_SUBMISSION: submission/submission_codex_e18_2_capacity_governed_v4d.py
E18_2_CANDIDATE_SHA256: C5FB1FC4966B81F238CDD0DE4CA5E15B16EA6B8AE077A08ECC881F8729FD01F7
E18_3_CODEX_ABLATION: COMPLETE_70_OF_70 / FIVE_FIXED_TOPOLOGIES
E18_3_RESULT: NO_PROMOTION / SUBMISSION_NOT_AUTHORIZED
E18_3_MONEY_VS_CONTROL: 775_-0.82% / 772_-14.31% / 662_-42.98% / 770_-34.69% / 670_-40.31%
E18_3_NEXT_ARCHITECTURE: NATIVE_STATE_DRIVEN_MISSION_SCHEDULER / START_FROM_772
E18_4_V1_GATE: REJECTED_0_OF_14 / 55940_VS_83095.71 / DELTA_-32.68_PERCENT
E18_4_V1_ARCHITECTURE: EXACT_772_AND_FILLED_16_OF_16_IN_14_OF_14 / LOSSES_0
E18_4_V1_WORK: MOVE_+29.35_PERCENT / PRODUCTIVE_-20.95_PERCENT
E18_4_V1_UPLOAD: NOT_AUTHORIZED
E18_4_V2_GATE_A: FAILED / GATE_B_NOT_RUN / NO_UPLOAD
E18_4_V2_RECORD: 0_14 / 47247.57_VS_77644.29
E18_4_V2_INTEGRITY: EXACT_772_AND_FILLED_16_OF_16_IN_14_OF_14 / LOSSES_ERRORS_FALLBACKS_0 / PASS_ACTIONABLE_0 / THRASH_0
E18_4_V2_WORK: MOVE_4477.43 / PRODUCTIVE_2217.43 / MOVE_PRODUCTIVE_2.0192 / HARVEST_472.57 / WEED_TD_36.36
E18_5_662_GATE: FAILED / 14_DEV_MATCHES / NO_HOLDOUT_FINAL_UPLOAD
E18_5_662_WORK: MOVE_4451.86_-0.57_PERCENT / PRODUCTIVE_2223.07_+0.25_PERCENT / MOVE_PRODUCTIVE_2.0026_-0.82_PERCENT
E18_5_662_ECONOMY: MONEY_49179.43_+4.09_PERCENT / HARVEST_513.14_+8.59_PERCENT / WEED_TD_21.79_-40.08_PERCENT
E18_5_662_INTEGRITY: EXACT_AND_FILLED_14_OF_14_IN_14_OF_14 / LOSSES_ERRORS_FALLBACKS_PASS_THRASH_0
E18_CURRENT_TOP3: CROP_DUSTA_3032.3 / GIULIO_RAVASIO_2967.3 / TOP770_2960.4
E18_CURRENT_TOP3_CORPUS: 11_HEAD_TO_HEAD_REPLAYS / 22_PROFILES / BOTH_SEATS
E18_CURRENT_TOP3_WORK: PRODUCTIVE_3237_TO_3377 / MOVE_PRODUCTIVE_1.01_TO_1.26 / HARVEST_887_TO_917
E18_CURRENT_TOP3_CONCLUSION: THROUGHPUT_COMMON / TOPOLOGY_NOT_COMMON / CROP_7_TOPOLOGIES / GIULIO_Q2_ZERO_7_OF_7
E18_6_770_GATE: REJECTED_0_OF_14 / 58957.00_VS_71104.43 / NO_HOLDOUT_FINAL_UPLOAD
E18_6_770_INTEGRITY: EXACT_AND_FILLED_770_IN_14_OF_14 / Q2_PASTURES_0 / ERRORS_FALLBACKS_BREACHES_0
E18_6_770_WORK: MOVE_+0.32_PERCENT / PRODUCTIVE_-5.70_PERCENT / MOVE_PRODUCTIVE_+6.38_PERCENT / PASS_+23.26_PERCENT
E18_6_770_LIFECYCLE: HARVEST_-6.90_PERCENT / HARVEST_PER_1000_MOVE_-7.19_PERCENT / LATE_UNWATERED_-2.09_PERCENT
E18_6_770_SAFETY: LIVESTOCK_LOSS_1_PER_MATCH / CAP_15_FOR_14_SLOTS
E18_6_770_MATCHED_TOP3: GIULIO_2 / TOP770_4 / CROP_0_EXCLUDED / EXACT_770_ONLY
E18_6_770_NORMALIZED_GAPS: UNIT_ACTIONS_+2.9 / PRODUCTIVE_-7.5 / PASS_+60.5 / CROP_SERVICE_-18.1 / MOVE_+4.1 / HARVEST_-36.7_PERCENT
E18_6_NEXT: PASS_TO_LOCAL_CROP_SERVICE_SINGLE_VARIABLE / THEN_LIFECYCLE / THEN_ROUTE_COMPLETION
E18_7_770_IN_PLACE_GATE: FAILED_SAFE_BUT_INERT / PASS_MINUS_2 / WATER_PLUS_2 / MONEY_FLAT
E18_8_770_ADJACENT_QUEUE_GATE: REJECTED_0_OF_14 / MONEY_-15.59_PERCENT / HARVEST_-31.96_PERCENT
E18_8_770_CAUSAL_DIAGNOSIS: 1132_OF_1372_MISSIONS_CANCELLED / OVERLAY_MOVE_BREAKS_PROVIDER_TRAJECTORY
E18_9_770_ROTATION_GUARD_GATE: FAILED_THRESHOLDS / POSITIVE_RESEARCH_SIGNAL / NO_PROMOTION
E18_9_770_RECORD: 10_4 / MONEY_+0.48_PERCENT / WORST_MATCHED_-0.95_PERCENT
E18_9_770_LIFECYCLE: DIG_-5.47_PERCENT / LATE_CROP_+4.93_PERCENT / HARVEST_EVENTS_+2.33_PERCENT / UNITS_+2.78_PERCENT
E18_10_V1_STATUS: INVALID_REJECTED / TASK_QUEUE_WATER_OVERRODE_SHARED_LOGISTICS / FILL_13_OF_14 / LOSSES_3_PER_MATCH
E18_10_V2_STATUS: BEST_770_RESEARCH_CONTROL / GATE_A_FAILED_3_VOLUME_THRESHOLDS / NO_PROMOTION_UPLOAD
E18_10_V2_RECORD: 12_2 / MONEY_+1.70_PERCENT / MATCHED_+1.46_PERCENT / WORST_-0.05_PERCENT
E18_10_V2_INTEGRITY: EXACT_FILLED_770_14_OF_14 / LOSSES_EQUAL_CONTROL / ERRORS_FALLBACKS_BREACHES_NONPASS_OVERRIDES_0
E18_10_V2_WATER: WATER_+1.77_PERCENT / DIG_-11.44_PERCENT / LATE_UNWATERED_-4.10_PERCENT / LATE_CROP_+5.21_PERCENT
E18_10_V2_OUTPUT: HARVEST_+1.77_PERCENT / UNITS_+0.58_PERCENT / MOVE_-0.22_PERCENT / RATIO_-0.42_PERCENT
E18_11_770_GATE: FAILED_SAFE_BUT_INERT / WATER_+0.97_PERCENT / OUTPUT_AND_MONEY_FLAT
E18_12_770_SPOT: CAP14_ACCEPTED_AS_FUTURE_770_INVARIANT / BLOCKS_D12_H3_SURPLUS / STANDALONE_MONEY_FLAT_DUE_D21_REPLACEMENT
E18_13_770_GATE: REJECTED_6_8 / LOSSES_0_VS_14 / MONEY_MEAN_+0.33_PERCENT / WORST_-2.85_PERCENT
E18_14_770_SPOT: REJECTED / WATER_+2.05_PERCENT / MOVE_-0.39_PERCENT / MONEY_-2.94_PERCENT
E18_15_770_SPOT: REJECTED / WATER_+21 / HARVEST_UNITS_STRESS_FLAT / MONEY_-1165_FIVE_HIRES
E18_16_770_GATE: PASSED_GATE_A_8_6 / GATE_B_TOP3_FAILED / NO_HOLDOUT_FINAL_UPLOAD
E18_16_770_LIVESTOCK: CAP14_ALL_MATCHES / CLAMP_AND_FEED_14_OF_14 / LOSSES_0_VS_14
E18_16_770_ECONOMY: MONEY_+1.18_PERCENT / MATCHED_+0.67_PERCENT / WORST_-0.95_PERCENT
E18_17_V1_GATE: FAILED_SAFE_BUT_BEHAVIORALLY_INERT / 14_MATCHES / NO_HOLDOUT_FINAL_UPLOAD
E18_17_V1_INTEGRITY: EXACT_FILLED_770_14_OF_14 / CAP14 / LOSSES_ERRORS_FALLBACKS_0
E18_17_V1_EFFECT: ACTION_MUTATIONS_0 / ALL_AGGREGATE_KPI_EQUAL_E18_16 / RAW_1_1_IS_SEAT_EFFECT
E18_770_CURRENT_CONTROL: E18_10_V2
E18_770_RESEARCH_BASE: E18_16_EXACT_CAP_CRITICAL_FEED
E18_770_NEXT: E18_18_CAPACITY_TRAJECTORY_PLANNER_GATE0_BEFORE_AGENT_BUILD
E18_DIAGNOSTIC_MODEL: CODEX-E18.1-OPPONENT-REACTIVE-662-770-V1
E18_DIAGNOSTIC_SUBMISSION: submission/submission_codex_e18_opponent_reactive_662_770.py
E18_DIAGNOSTIC_SUBMISSION_SHA256: 06727C1673EC289A323CE403596FAB8B272539535D27C9CEE74B8C917B78791B
CURRENT_CODEX_REACTIVE_SUBMISSION: submission/submission_codex_e17_reactive.py
CURRENT_CODEX_REACTIVE_SUBMISSION_SHA256: 0874EB10F287DC7E6A268CDB64517BAE98E246EB1A124EF9C643A3B7DCE0082C
KAGGLE_SCORE_PRIOR_SNAPSHOT: 1159.9
KAGGLE_POSITION_PRIOR_SNAPSHOT: 2542
KAGGLE_E17_INTERIM_RATING: 996
KAGGLE_E17_ENTRY_RATING: 600
KAGGLE_E17_INTERIM_DELTA: +396
KAGGLE_E17_SCORE_STATUS: STABILIZING_NOT_FINAL
KAGGLE_E17_CONTROL_RATING_SNAPSHOT: 1089.7
KAGGLE_E17_REACTIVE_RATING_SNAPSHOT: 1353.6
KAGGLE_E17_REACTIVE_DELTA: +263.9 (+24.2%)
VISIBLE_TOP3_2026_09_03: Crop_Dusta=2958.7, 3정훈=2948.1, sbol_ball=2929.8

NEXT_EXPERIMENT: E18
E17_PHASE: CLOSED / DEVELOPMENT COMPLETE / HOLDOUT NOT USED
E17_CLOSEOUT: COMPLETE_2026_09_03
E17_OBJECTIVE: COMPARE_CAUSAL_LINES_WITHOUT_PRESELECTING_ONE_ARCHETYPE
E17_POLICY_MUTATION: CODEX_SERVICE_ROUTING_V3_CONTROL / CODEX_POST_FEED_CAPACITY_BATCHING_V4D_INTERNAL
E17_CROSS_AGENT_REVIEW: CLOSED
E17_STRATEGY_FREEZE: experiments/e17/design/E17_STRATEGY_FROZEN_V1.md
E17_0_TECHNICAL_GATE: PASS
E17_0_COMPETITIVE_READINESS: NOT_ESTABLISHED
E17_1_AUTHORIZED: YES_BY_POST_FREEZE_OWNER_DECISION
E17_REACTIVE_DESIGN: experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md
E17_REACTIVE_AUTHORIZATION: experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md
E17_REACTIVE_TOURNAMENT: HOLDOUT_BLOCKED_CLAUDE_V2_FAILED_GATES
E17_REACTIVE_PARTICIPANTS: CODEX_V9_FROZEN, CODEX_REACTIVE, CLAUDE_REACTIVE
E17_DEVELOPMENT_EXHIBITION: COMPLETE_42_OF_42_NON_QUALIFYING
E17_EXTERNAL_SUBMISSION: REACTIVE_LIVE_SCORE_STABILIZING
E17_EXTERNAL_RELEASE: CODEX-E17.0-EXTERNAL-CONTROL-V1
E17_KAGGLE_SUBMISSION_ID: 559588638
E17_REACTIVE_KAGGLE_SUBMISSION_ID: 559631298
E17_REACTIVE_EXTERNAL_BENCHMARK: COMPLETE_10_EPISODES_5W_5L
E17_REACTIVE_EXTERNAL_MEAN_MONEY: 78808.7
E17_REACTIVE_ACTION_STREAMS: 1_UNIQUE_OF_10
E17_REACTIVE_STRUCTURAL_TRAJECTORIES: 4_UNIQUE_OF_10
E17_REACTIVE_Q2_VS_Q0_ANIMAL_TILE_DAYS: 63.29%
E17_TRUE_REACTIVITY_PLAN: docs/model_specs/codex/e17/design/E17_CODEX_TRUE_REACTIVITY_ACTIVATION_PLAN_V1.md
E17_TRUE_REACTIVITY_V2: DEVELOPMENT_GATES_PASS_NOT_KAGGLE_READY
E17_TRUE_REACTIVITY_RUNS: 48
E17_TRUE_REACTIVITY_INERT_DELTA: +1.55%
E17_TRUE_REACTIVITY_OVERALL_DELTA_VS_V1: -0.26%
E17_TRUE_REACTIVITY_Q2_OUTCOME: FINAL_ANIMALS_8_6_5_UNCHANGED
E17_TRUE_REACTIVITY_REPORT: docs/model_specs/codex/e17/reports/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md
E17_SERVICE_ROUTING_PLAN: docs/model_specs/codex/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V2.md
E17_SERVICE_ROUTING_V2: SUPERSEDED_INTERNAL_BY_V3_D28
E17_SERVICE_ROUTING_V3: ALL_DEVELOPMENT_GATES_PASS_NOT_KAGGLE_RELEASED
E17_SERVICE_ROUTING_ACTIVATION_DAY: 28
E17_SERVICE_ROUTING_LIQUIDATION_DAY: 29
E17_SERVICE_ROUTING_RUNS: 12
E17_SERVICE_ROUTING_MEAN: 134351.33
E17_SERVICE_ROUTING_CONTROL_MEAN: 134060.17
E17_SERVICE_ROUTING_DELTA: +0.217%
E17_SERVICE_ROUTING_DELTA_VS_V2_D29: +1.82%
E17_SERVICE_ROUTING_UNIT_LEDGER: 3198/3198_CLASSIFIED
E17_SERVICE_ROUTING_MARKET_LEDGER: 78/78_CLASSIFIED
E17_SERVICE_ROUTING_COMMANDS: ROUTING_2256 / SERVICE_752
E17_SERVICE_ROUTING_SAFETY: NON_SELL_VIOLATIONS_0 / ANIMAL_ESCAPES_0
E17_SERVICE_ROUTING_TERMINAL_SELLABLE_RESIDUAL: 0
E17_SERVICE_ROUTING_REPORT: docs/model_specs/codex/e17/reports/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md
E17_BATCHED_ROUTING_PLAN: docs/model_specs/codex/e17/design/E17_CODEX_BATCHED_CLUSTER_ROUTING_PLAN_V1.md
E17_BATCHED_ROUTING_V4A: REJECTED_REWARD_MINUS_2.529%
E17_CLUSTERED_ROUTING_V4B: REJECTED_NO_LOGISTIC_GAIN
E17_CAPACITY_ROUTING_V4C: REJECTED_TRIGGER_BLOCKED_BY_WHEAT_GUARD
E17_POST_FEED_CAPACITY_V4D: ALL_DEVELOPMENT_GATES_PASS_NOT_KAGGLE_RELEASED
E17_V4D_RUNS: 12
E17_V4D_MEAN: 135096.83
E17_V4D_CONTROL_MEAN: 134351.33
E17_V4D_DELTA: +0.555%
E17_V4D_MIN_MATCHED_DELTA: +497
E17_V4D_MOVE_PER_SERVICE: 2.872
E17_V4D_LEDGER: UNIT_3198/3198 / MARKET_71/71
E17_V4D_SAFETY: ERRORS_0 / ESCAPES_0 / TERMINAL_RESIDUAL_0
E17_V4D_REPORT: docs/model_specs/codex/e17/reports/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md
E17_V4D_MARKET_STRESS: PASS_48_OF_48 / D27_ADMITTED
E17_V4D_MARKET_STRESS_MATCHED: 24_OF_24_NONNEGATIVE
E17_V4D_MARKET_STRESS_MEAN: 124090.17
E17_V4D_MARKET_STRESS_CONTROL_MEAN: 123199.54
E17_V4D_MARKET_STRESS_DELTA: +0.723%
E17_V4D_MARKET_STRESS_WORST_REGIME: INERT_+0.555%
E17_V4D_MARKET_STRESS_MOVE_PER_SERVICE: 2.922_VS_2.967
E17_V4D_MARKET_STRESS_REPORT: docs/model_specs/codex/e17/reports/E17_CODEX_V4D_CONTROLLED_MARKET_STRESS_REPORT_IT.md
E17_D27_HANDOFF_ABLATION: FAIL_REWARD / V4D_D28_RETAINED
E17_D27_RUNS: 12
E17_D27_MEAN: 133290.33
E17_D27_CONTROL_MEAN: 135096.83
E17_D27_DELTA: -1.337%
E17_D27_MATCHED_NONNEGATIVE: 0/6
E17_D27_MOVE_PER_SERVICE: 2.605_VS_2.872
E17_D27_CAUSAL_DIAGNOSIS: ONE_FEWER_Q0_CROP_IN_6/6
E17_D27_REPORT: docs/model_specs/codex/e17/reports/E17_CODEX_D27_HANDOFF_ABLATION_REPORT_IT.md
E17_V4D_KAGGLE_RELEASE: READY_FOR_OWNER_UPLOAD
E17_V4D_SUBMISSION: submission/submission_codex_e17_v4d.py
E17_V4D_SUBMISSION_SHA256: 2792244CA71115E6CAAFDFC942B6D9AAAF09B95FC717A5B182D07A31D9717CD7
E17_V4D_SUBMISSION_PARITY: 4314/4314
E17_V4D_KAGGLE_UPLOAD: NOT_YET_RECORDED
E17_V4D_RELEASE_REPORT: docs/model_specs/codex/e17/reports/E17_CODEX_V4D_KAGGLE_SUBMISSION_READINESS_REPORT_IT.md
E17_662_MODEL: CODEX-E17.3-TOPOLOGY-FILL-662-V2
E17_662_SUBMISSION: submission/submission_codex_e17_topology_662.py
E17_662_SUBMISSION_SHA256: 3DF5C15D078552AF0A3849653057303698C9D750B4C7BB087B8A29092FADBAE8
E17_662_TOPOLOGY: Q0_6 / Q1_6 / Q2_2 / FILLED_14_OF_14
E17_662_KAGGLE_SUBMISSION_ID: 559767808
E17_662_KAGGLE_SCORE_SNAPSHOT: 1009.8_STABILIZING_NOT_FINAL
E17_THREE_AGENT_TOURNAMENT: COMPLETE_42_OF_42_DEVELOPMENT_NON_QUALIFYING
E17_THREE_AGENT_STANDINGS: CODEX_28_0_0 / CLAUDE_14_14_0 / COPILOT_0_28_0
E17_THREE_AGENT_MEAN_MONEY: CODEX_123620.29 / CLAUDE_15511.21 / COPILOT_10537.18
E17_THREE_AGENT_REPORT: experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md
E17_DELTA_TOURNAMENT: COMPLETE_84_OF_84_DEVELOPMENT_NON_QUALIFYING
E17_DELTA_TOURNAMENT_REPORT: experiments/e17/reports/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3_REPORT_IT.md
E17_CLAUDE_V5_DELTA: SHARED_+8.53% / DIRECT_-9.57% / NOT_PROMOTED
E17_CLAUDE_V6_REGRESSION: 1W_13L / MEAN_1538.50 / 3Q_1_OF_14 / REJECTED
E17_CLAUDE_V6_BLACKBOX: 0W_16L / MEAN_622.88 / OPPONENT_MEAN_144654.75
E17_COPILOT_662_V3_DELTA: 0.00% / IDENTICAL_28_OF_28 / NOT_PROMOTED
E17_COPILOT_662_V4: LATE_TECHNICAL_PROTOTYPE / NOT_BENCHMARKED / NOT_ADMITTED
ACTIVE_DEVELOPMENT_AGENTS: NONE_E17_CLOSED
CODEX_REACTIVE_STATUS: 662_V2_RETAINED_AS_E18_BASELINE
CODEX_REACTIVE_DEVELOPMENT_MEAN: 139420.2857
CODEX_REACTIVE_DELTA_VS_V9: 0
CLAUDE_REACTIVE_STATUS: V1_REJECTED / V2_FROZEN_WITH_FAILED_GATES
CLAUDE_ACTIVATION_AUDIT: PASS_WITH_LOCAL_CLEANUP
CLAUDE_ROOT_BOOTSTRAP: REMOVED
CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK: AUTHORIZED_DEVELOPMENT_ONLY
CLAUDE_V3_IMPLEMENTATION: COMPLETE_FROZEN_WITH_FAILED_GATES
CLAUDE_V3_10X_PROMPT: docs/model_specs/claude/e17/prompts/E17_CLAUDE_REACTIVE_V3_10X_ACTIVATION_PROMPT_IT.md
REPLAY_JSON_ROOT: data/replays/json
REPLAY_JSON_CATALOG: data/replays/json/json.md
E17_RAW_CODEX_DEV_AND_CLAUDE_V1: REMOVED_REPRODUCIBLE
CLAUDE_V2_RAW: REMOVED_REPRODUCIBLE_CATALOG_RETAINED
ANTIGRAVITY_STATUS: FROZEN_PERFORMANCE_GAP
COPILOT_STATUS: FROZEN_PERFORMANCE_GAP
CLAUDE_STATUS: FROZEN_PERFORMANCE_GAP
NEW_KAGGLE_SUBMISSION: E17_662_ID_559767808 / SCORE_SNAPSHOT_1009.8_STABILIZING

E18_PHASE: OPEN_770_OPTIMIZATION / E18_17_V1_REJECTED_SAFE_BUT_INERT
E18_ECONOMIC_CONTROL: CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28
E18_CANDIDATE: NONE / E18_16_770_RESEARCH_BASE_RETAINED / E18_17_V1_GATE_A_FAIL
E18_OPENING_REPLAY: 105080066 / ANALYZED / TRAINING_EVIDENCE
E18_OPENING_DIAGNOSIS: CROP_LIFECYCLE_SERVICE_AND_HARVEST_CADENCE_GAP
E18_LIFECYCLE_OUTPUT: CODEX_586 / YUSUF_829 / DELTA_-243
E18_LIFECYCLE_WEED_EXITS: CODEX_49 / YUSUF_9
E18_LIVE_TOP3_CORPUS: 8_REPLAYS / BOTH_SEATS_PER_AGENT / ACQUIRED_AND_ANALYZED
E18_CODEX_EXTERNAL_REACTIVITY: 1_UNIQUE_LIFECYCLE_PROFILE_OF_3
E18_TOP3_EXTERNAL_REACTIVITY: 8_UNIQUE_LIFECYCLE_PROFILES_OF_8 / 5_TOPOLOGIES
E18_TOP3_Q2_PASTURES: ZERO_IN_7_OF_8 / RANGE_INCLUDES_10-7-0_AND_8-4-3
E18_LIVE_OUTPUT_DELTA: HARVEST_+48.9_PERCENT / WHEAT_+87.5_PERCENT / UNWATERED_-22.9_PERCENT
E18_OPPONENT_SIGNAL: PUBLIC_FARM_OBSERVABLE / RATING_AND_CROSS_EPISODE_HISTORY_UNAVAILABLE
E18_PIPELINE_GAP: BRIDGED_IN_CANDIDATE_WITH_PUBLIC_OPPONENT_FARM_OBSERVER
REPLAY_STORAGE: 0_RAW_JSON / 29_FILES_765.18_MIB_REMOVED_WITH_OWNER_AUTHORIZATION
REPLAY_RECOVERY: KAGGLE_EPISODE_ENDPOINT_PLUS_JSON_MD_SHA256
E18_CANDIDATE_INTAKE: CLAUDE_E18_1_AND_COPILOT_E18_1_ADMITTED / NOT_PROMOTED
E18_CANDIDATE_INTAKE_REPORT: experiments/e18/reports/common/E18_CLAUDE_COPILOT_CANDIDATE_INTAKE_IT.md
E18_TARGET_MONEY: 100000
E18_BASELINE_VS_CLAUDE: 132217.68
E18_BASELINE_SYMMETRIC_662: 79323.86
E18_GAP_TO_TARGET: 20676.14 / +26.1%_REQUIRED
E18_DYNAMIC_TOURNAMENT: COMPLETE_56_OF_56 / ARCHITECTURE_GATE_PASS_10_OF_10
E18_DYNAMIC_TOPOLOGY: 662_28_OF_42 / 770_14_OF_42
E18_DYNAMIC_MODE_BY_OPPONENT: CLAUDE_AND_CONTROL_662 / COPILOT_770
E18_DYNAMIC_DIVERGENCE: ACTION_14_OF_14 / TOPOLOGY_14_OF_14
E18_DYNAMIC_MONEY: OVERALL_111654.45 / VS_662_80456.43 / VS_CLAUDE_127072.71 / VS_COPILOT_127434.21
E18_DYNAMIC_DELTA_VS_662: -3472.29 / -4.14_PERCENT
E18_REACTIVITY_GATE: PASS_CONDITIONED_ACTION_AND_TOPOLOGY_DIVERGENCE
E18_SAFETY_GATE: PASS_14_OF_14 / VERIFIED_LOSSES_0 / ERRORS_0 / FALLBACKS_0 / BREACHES_0
E18_MANIFEST: experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json
E18_PLAN: experiments/e18/design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md
E18_REPORT: experiments/e18/reports/common/E18_662_TOP3_BASELINE_BENCHMARK_IT.md
E18_LIFECYCLE_REPORT: experiments/e18/reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md
E18_LIVE_BENCHMARK_REPORT: experiments/e18/reports/common/E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_IT.md
E18_DYNAMIC_REPORT: experiments/e18/reports/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md
E18_NEXT_CANDIDATE_PROMPT: experiments/e18/prompts/common/E18_DYNAMIC_ARCHITECTURE_NEXT_CANDIDATE_PROMPT_IT.md
E18_CLAUDE_BUILD_PROMPT: docs/model_specs/claude/e18/prompts/E18_CLAUDE_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md
E18_COPILOT_BUILD_PROMPT: docs/model_specs/copilot/e18/prompts/E18_COPILOT_OPPONENT_REACTIVE_V1_BUILD_PROMPT_IT.md
E18_FOUR_AGENT_TOURNAMENT: COMPLETE_84_OF_84 / 6_PAIRS / 7_DEV_SEEDS / BOTH_SEATS
E18_FOUR_AGENT_RECORDS: CODEX_42-0 / CLAUDE_26-16 / COPILOT_16-26 / ANTIGRAVITY_0-42
E18_FOUR_AGENT_MONEY: CODEX_125983.74 / CLAUDE_6467.48 / COPILOT_2840 / ANTIGRAVITY_0
E18_FOUR_AGENT_PROMOTION: NONE
E18_ANTIGRAVITY_ROUNDS: 42_TOTAL / 14_PER_OPPONENT / P0_21 / P1_21 / ENGINE_COMPATIBILITY_FAIL
E18_LATEST_VS_V4D_BENCHMARK: COMPLETE_56_NEW_MATCHES_PLUS_42_FROZEN_COMPARATORS
E18_LATEST_VS_V4D_DIRECT: LATEST_0-14 / 71831.00_VS_89760.57 / DELTA_-19.97_PERCENT
E18_LATEST_VS_V4D_COMMON_POOL: 125983.74_VS_143486.45 / DELTA_-12.20_PERCENT
E18_LATEST_VS_V4D_DIAGNOSIS: PRODUCTIVE_-6.11_PERCENT / PASS_+24.77_PERCENT / WEED_TILE_DAYS_+320_PERCENT
E18_ECONOMIC_CONTROL: E17_V4D_RESTORED / E18_1_DIAGNOSTIC_ONLY
E18_KAGGLE_LIVE_SNAPSHOT: E18_1_825.4 / E17_662_941.4 / V4D_1131.7 / REACTIVE_1077.5 / V9_1082.9
E18_PEER_V2_REAL_ENGINE_TOURNAMENT: COMPLETE_84_OF_84 / V4D_ONLY_GATE_PASS
E18_CLAUDE_V2_INTAKE: REAL_ENGINE_MEAN_9756.29 / LOSSES_44 / NOT_PROMOTED
E18_COPILOT_V2_INTAKE: REAL_ENGINE_MEAN_260 / NOT_PROMOTED
E18_ACTIVE_TEST_ROSTER: CODEX_V4D_CONTROL / CODEX_E18_1_ABLATION / CLAUDE_E18_2 / COPILOT_E18_2
E18_ANTIGRAVITY_ACTIVE_STATUS: EXCLUDED_UNTIL_NEW_RELEASE
E18_CODEX_V2_DEV_GATE: PASS_9_OF_9 / 56_0 / MONEY_121149.84
E18_CODEX_V2_DIRECT_V4D: 14_0 / +3.77_PERCENT
E18_CODEX_V2_TOPOLOGY: V4D_7_7_5_PRESERVED / ON_TILE_RECOVERY_ONLY
E18_CODEX_V2_SAFETY: LOSSES_0 / ERRORS_0 / FALLBACKS_0
E18_KAGGLE_STABILITY_RULE: 4_VALID_HOURLY_SNAPSHOTS_OVER_3H / SCORE_RANGE_LT_50
E18_KAGGLE_MONITOR_STATUS: PROTOCOL_READY_NOT_SCHEDULED / AUTOMATION_TOOL_UNAVAILABLE / BROWSER_READ_BLOCKED
E18_KAGGLE_MONITOR_PROTOCOL: docs/model_specs/codex/e18/prompts/E18_CODEX_KAGGLE_STABILITY_MONITOR_PROTOCOL_IT.md
E18_CLAUDE_V2_PROMPT: docs/model_specs/claude/e18/prompts/E18_CLAUDE_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md
E18_COPILOT_V2_PROMPT: docs/model_specs/copilot/e18/prompts/E18_COPILOT_OPPONENT_REACTIVE_V2_REMEDIATION_PROMPT_IT.md
E18_ANTIGRAVITY_REBOOT_PROMPT: docs/model_specs/antigravity/e18/prompts/E18_ANTIGRAVITY_REACTIVE_V1_REBOOT_PROMPT_IT.md
E18_FOUR_AGENT_REPORT: experiments/e18/reports/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2_REPORT_IT.md
E18_SUBMISSION: submission/submission_codex_e18_16_770.py
E18_SUBMISSION_SHA256: 4CD8F18F317D4C654F9CAB7E019EEE3ABAB906C65B46FA842B6A009EF5EB0350
E18_SUBMISSION_PARITY: ISOLATED_PASS / 2880_ACTIONS / BOTH_SEATS
E18_SUBMISSION_ROLE: EXTERNAL_VALIDATION_NOT_FINAL_PROMOTION
E18_KAGGLE_STATUS: STABILIZING_2026_09_04 / SCORE_SNAPSHOT_952 / 37_GAMES_20_WINS_17_LOSSES
E18_HOLDOUT: NOT_CONSUMED / NOT_AUTHORIZED
E18_TOPOLOGY_TARGET: EXACT_770_LOCKED_UNTIL_CONSISTENT_REPEATABLE_GAP_REDUCTION
E18_DEVELOPMENT_SELECTION: VERSIONED_INTERNAL_CHAMPIONS / PREREGISTERED_DEV_SEEDS / BOTH_SEATS / FULL_TELEMETRY
E18_EXTERNAL_SUBMISSION_CADENCE: ONE_DAILY_BEST_770_CANDIDATE / EXTERNAL_VALIDATION_NOT_AUTOMATIC_PROMOTION
E18_EXTERNAL_EVIDENCE_POLICY: ARCHIVE_HASH_ID_SCORE_REPLAYS / INFORM_NEXT_DAY_ONLY / NO_INTRADAY_KAGGLE_TUNING
E18_DAILY_TOP_BENCHMARK: CURRENT_TOP4 / LATEST_5_COMPLETED_REPLAYS_EACH / DEDUP_SHARED_EPISODES
E18_HISTORICAL_E18_22_RESULT: WHEAT_JIT_D1 / PARENT_DELTA_+2.84_PERCENT / INCUMBENT_GATE_FAIL
E18_CURRENT_DEVELOPMENT_CANDIDATE: E18_27_D10_D15_CASHFLOW_V3 / PARENT_MEAN_DELTA_+13.44_PERCENT_VS_E18_16 / ROBUSTNESS_AND_INCUMBENT_GATE_FAIL / NO_UPLOAD
E18_LATEST_ABLATIONS: E18_27_V1_HARVEST_ONLY / V2_Q2_AND_SAME_BATCH_SELL_OPENING_LEAK / V3_OPENING_LOOKAHEAD_FROZEN
E18_CROP_SKIP_DIAGNOSIS: D11_PLANT_STALE_DUPLICATES / HARVEST_65_EMPTY_15_WEED_ACROSS_TWO_SEATS
E18_CURRENT_DIAGNOSIS: D25_D30_ANNUAL_OUTPUT_184_VS_TOP770_260 / NO_REPLANT_AFTER_D25 / TOP770_36_SWITCHABLE_CARROT_WHEAT_SLOTS_87_UNITS / D10_D15_DEFECTS_PRESERVED
E18_NEXT_SPEC: E18_28_770_LATE_ANNUAL_MISSIONS_V1 / SPECIFIED_NOT_IMPLEMENTED
NEXT_ACTION: E18_28_A_EXISTING_MISSION_CLOSURE / THEN_B_LATE_WHEAT_CYCLES / THEN_C_CARROT_WHEAT_SELECTOR / FREEZE_D1_D24 / KEEP_770_CAP14_12_HANDS
```

## Stato raggiunto

E17 è chiuso. La candidata Codex 6-6-2 mantiene 14 pascoli target riempiti,
cinque celle recuperate a crop, zero breach Q2 e zero fughe. La submission
Kaggle `559767808` ha uno snapshot `1009,8`, ancora in stabilizzazione.

La diagnostica E18.1 aggiunge un selector D6 sulla sola farm pubblica
avversaria: `6-6-2` contro Claude/controllo e `7-7-0` contro Copilot. Nel
torneo development da 56 match supera tutti i gate dinamici e di sicurezza,
con 14/14 pascoli e zero perdite verificate. La media globale è 111.654,45,
ma nel diretto col controllo 662 perde il 4,14%; resta quindi una submission
diagnostica, non la nuova baseline. Claude e Copilot devono ora presentare
candidate valutate anche su regime activation, action/topology divergence e
lifecycle, non soltanto sullo score.

Il successivo benchmark controllato contro il bundle V4D corregge il
riferimento economico: E18.1 perde `14/14` diretti, con `71.831,00` contro
`89.760,57` (`-19,97%`), e resta sotto del `12,20%` sul pool comune. Il calo
di azioni produttive (`-6,11%`) si converte quasi interamente in `PASS`
(`+24,77%`), mentre i weed tile-days crescono del `320%`. V4D torna quindi
controllo economico obbligatorio; E18.1 conserva solo il ruolo diagnostico.

Lo snapshot Kaggle ora accessibile mostra `825,4` per E18.1, `941,4` per la
6-6-2 E17.3 e `1.131,7` per V4D. Le nuove peer V2 entrano in intake senza
Antigravity: Claude ha evidenza real-engine ma fallisce ancora i gate;
Copilot è callable, mentre il suo benchmark dichiarato è sintetico e deve
essere rifatto integralmente nel motore reale.

Il torneo delta finale è completo: 84 match development, senza holdout/final.
Claude V5 non è promossa (`+8,53%` shared ma `-9,57%` diretto); V6 è respinta
(`1-13`, 3Q `1/14`). La 6-6-2 V3 attribuita al lavoro Copilot è identica alla
V2 in `28/28` profili ed è anch'essa non promossa.

E18 è aperto con la V2 come baseline. Il benchmark Top 3 è osservazionale:
gli archetipi storici `tetsuya`, `OceanMix` e `Crop Dusta` provengono da replay
E17 già consumati. Il primo gate è dimostrare attivazione causale; solo dopo si
misura il gap self-play di `20.676,14` (`+26,1%`) verso 100k.

La Foundation C2.1 e il riordino del repository sono chiusi con gate A7
`PASS`. La strategia E17 è stata riconciliata e congelata dopo tre review
indipendenti. E17.0 è completo per Codex, Antigravity e Copilot. Una decisione
successiva del proprietario autorizza ora E17.1, con Codex V9 congelata come
controllo, Codex reattivo come evoluzione derivativa e Claude reattivo come
policy indipendente. Antigravity e Copilot restano congelati. Codex V9 resta la
baseline e la submission Kaggle correnti. Il benchmark discovery E17 è stato
completato su nove replay unici dei tre player che occupavano il Top 3 nello
snapshot di raccolta (`tetsuya`, `OceanMix`, `Crop Dusta`), con 18 player-seat
e 720 step per episodio.

La review cross-agent è formalmente chiusa:

- Copilot: `ACCEPT_WITH_CHANGES`;
- Antigravity: `ACCEPT`;
- audit fughe Crop Dusta: 31/31 eventi compatibili con fuga secondo criterio
  EOD stretto, classificati `DERIVED`;
- nessuna policy è stata modificata durante benchmark e review.

L'audit successivo dell'attivazione Claude è
`PASS_WITH_LOCAL_CLEANUP`: tutte le scritture sono rimaste nei namespace
assegnati, non risultano letture dei sorgenti strategici altrui, import
proibiti, uso dei seed riservati o mutazioni Git. Il bootstrap locale
`CLAUDE.md` è stato rimosso; i prompt puntano ora ai documenti canonici. I
replay grezzi sono consolidati nella cartella unica `data/replays/json/` e
catalogati in `json.md`. I ledger Codex development e Claude V1, riproducibili
e già sintetizzati, sono stati rimossi; i ledger Claude V2 restano disponibili
localmente per la remediation V3 e sono esclusi da Git.

Il benchmark esterno della probe reattiva è completo su dieci replay della
submission Kaggle `559631298`: 5W-5L, denaro medio `78.808,7`, zero fughe e
3Q in 10/10. La policy ha emesso una sola sequenza completa di comandi nei
dieci episodi, mentre lo stato strutturale eseguito presenta quattro hash:
nel campione le guardie reattive non hanno quindi prodotto una divergenza
osservabile dell'action stream. La quota Q2 è il `63,29%` degli
animal-tile-days Q0 tra sblocco Q2 e D28, intermedia fra tetsuya (`75,38%`),
Crop Dusta (`38,17%`) e OceanMix (`0%`). La quota Q2 è diventata un outcome,
non il trattamento. Il controller `MARKET_REGIME_ADAPTATION` V2 è stato
verificato su 48 episodi development: +1,55% sul controllo inerte,
action-stream discriminanti, 100% di override tracciati, zero errori e zero
fughe. La composizione animale Q0/Q1/Q2 resta 8/6/5: il solo timing
commerciale non rende ancora reattiva la struttura. I replay esterni restano
diagnostici e holdout/final confirmation non sono stati usati. Report:
`docs/model_specs/codex/e17/reports/E17_CODEX_TRUE_REACTIVITY_DEVELOPMENT_REPORT_IT.md`.

Il passo successivo è stato eseguito con
`REACTIVE_SERVICE_AND_ROUTING_CORE_V2`. Il core ricostruisce dallo stato
osservato task di servizio e percorsi, senza cambiare il blocco market. Un
override locale della routine è stato respinto perché i suoi `PASS` sono
anche punti impliciti di sincronizzazione; la soluzione promossa usa un
handoff progressivo al giorno 29. Su 12 episodi development matched ottiene
`131.947,17` contro `134.060,17` (`−1,576%`), genera 750 comandi di routing e
252 servizi, classifica tutti i 1.434 record del ledger e mantiene a zero
errori, mutazioni market e fughe. È una prova architetturale, non una
submission. Il prossimo test è anticipare l'handoff a D28 coordinando
raccolta, deposito e liquidazione terminale. Report:
`docs/model_specs/codex/e17/reports/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_DEVELOPMENT_REPORT_IT.md`.

La V3 ha completato il passaggio a D28: FEED e WATER preparano l'ultimo ciclo,
gli output vengono depositati senza serializzare artificialmente gli accessi
shed e D29 coordina DROP e SELL nello stesso batch. Nei 12 episodi matched la
media è `134.351,33` contro `134.060,17` (`+0,217%`), ossia circa `+1,82%`
rispetto alla V2 D29. Il residuo vendibile terminale è zero, con zero fughe,
errori e violazioni market. Holdout e final confirmation restano intatti e la
V3 non è una submission. La prossima sessione deve mantenere D28, introdurre
routing per cluster e rientri basati su inventario/slack, e tentare D27 solo
dopo avere preservato score, sicurezza e liquidazione completa. Report:
`docs/model_specs/codex/e17/reports/E17_CODEX_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_REPORT_IT.md`.

Il trattamento logistico è stato poi scomposto causalmente. V4A riduce i MOVE
ma perde `2,529%` per overflow EOD dello shed; V4B mostra che l'affinità di
quadrante non aggiunge efficienza; V4C rileva la pressione di capacità ma la
guardia Wheat impedisce il flush. V4D rilascia i carrier soltanto dopo il feed
completo e supera tutti i gate: `135.096,83` contro `134.351,33` (`+0,555%`),
delta positivo in 6/6 confronti, `MOVE/service = 2,872`, zero fughe, errori e
residui terminali. È la candidata interna corrente, non una submission. La
prossima sessione deve stressare V4D nei regimi market development già
controllati prima di valutare D27. Report:
`docs/model_specs/codex/e17/reports/E17_CODEX_BATCHED_CLUSTER_ROUTING_V4_DEVELOPMENT_REPORT_IT.md`.

## Evidenza E17 consolidata

I nove replay mostrano tre archetipi diversi, tutti 3Q NW→NE→SW e senza Q3:

| Profilo | Q1 | Q2 | Topologia | MOVE/produttive | Rischio terminale |
|---|---|---|---|---:|---|
| `tetsuya` | D7 | D10 | bestiame distribuito, Q1 crop-dense | 1,2553 | 0 fughe, inventario 0 |
| `OceanMix` | D6 | D11 | livestock Q0/Q1, Q2 crop-only | 1,0468 | 0 fughe |
| `Crop Dusta` | D5–D6 | D8–D9 | tre quadranti misti e dispersi | 1,4267 | 31 fughe derivate |

Questi dati supportano il 3Q e il picco di 12 hands come baseline di lavoro,
non come ottimi globali. Non identificano causalmente il vantaggio di D10,
della topologia compatta o della diversificazione. Rating Kaggle, denaro finale
dei replay e score dei runner locali restano metriche diverse.

Lo snapshot leaderboard del 2026-09-02 cambia l'ordine: `Crop Dusta` è primo
con 2.917,8, `tetsuya` secondo con 2.890,3 e `3정훈` terzo con 2.878,5;
`OceanMix` non compare nei primi sette visibili. Il benchmark resta valido
come confronto di tre archetipi, ma non va più chiamato fotografia del Top 3
corrente. La leadership di Crop Dusta rende obbligatorio mantenere in E17 una
frontiera di espansione precoce/diversificata; non annulla però le 31 fughe
derivate né autorizza a saltare ledger e vincoli di serviceability.

## Strategia E17 congelata

Il draft iniziale resta disponibile come provenance; il riferimento normativo
corrente è:

`experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`

Principio cardine: **E17 non deve convergere a priori verso un singolo
archetipo**. `tetsuya`, `OceanMix` e `Crop Dusta` sono tre combinazioni
osservate di fattori. Timing, topologia, densità, capitale, specie e chiusura
devono essere separati e testati causalmente. Solo dopo la misura degli effetti
principali sono ammessi test di interazione e una candidata composita.

La sequenza condivisa è:

1. `E17.0` — ledger requested/executed a parità comportamentale;
2. `E17.1` — singola guardia fill-aware sul mercato WHEAT;
3. `E17.2` — contrasto topologico distribuito vs livestock compatto Q0/Q1;
4. `E17.3` — anticipo isolato di Q2 da D11 a D10;
5. `E17.4` — liquidazione terminale reattiva;
6. `E17.5` — diversificazione di una sola specie per esperimento;
7. `E17.6` — checkpoint obbligatorio della frontiera Q2 D8, soltanto con zero
   fughe e serviceability provata.

Le linee minime da confrontare includono:

- timing Q2 `D11 / D10 / D8`;
- livestock `distribuito / compatto Q0-Q1 / misto nei tre quadranti`;
- diversificazione crop `3 / 4 / 5 specie`;
- diversificazione animale `2 / 3 specie`;
- reinvestimento aggressivo vs riserva di liquidità;
- liquidazione e servicing terminale reattivi vs schedule fisso.

E17.0 ha aggiunto il ledger comune `E17_LEDGER_V1` fuori dal decision path.
Codex ha dimostrato parità `4314/4314`, outcome e stato terminale `6/6`, senza
modificare la V9. Antigravity e Copilot hanno eliminato la dipendenza dalle
routine Codex e costruito baseline native con audit locale d'indipendenza
`PASS`. Tutti i ledger hanno record coverage del 100%, zero errori tecnici e
zero fughe EOD derivate.

Il PASS è tecnico, non competitivo. Antigravity attiva tre quadranti ma
consuma tutto il capitale iniziale (`max_hands=0`, reward 0 in 6/6); Copilot è
produttiva ma ottiene mean 8.941,5 contro opponent inert. Codex V9 ottiene mean
132.019,3 sulla stessa matrice development. Al termine di E17.0 queste
differenze non autorizzavano una promozione; il nuovo torneo è autorizzato da
un decision record successivo e non modifica retroattivamente quel verdetto.

## Prossima azione operativa storica E18 activation-first

La lista seguente è conservata come handoff storico. Per l'operatività
corrente prevale la decisione `7-7-0` e ciclo quotidiano posta all'inizio del
documento.

1. costruire fixture controllate per `growth`, `service_pressure`,
   `market_contention` e `liquidation`;
2. registrare transizioni, feature causali, guard activation, ordini visti,
   ordini throttled e unità soppresse;
3. richiedere divergenza spiegabile dalla V2 prima di qualsiasi torneo
   economico E18;
4. preservare `6-6-2`, `14/14`, Q2 ≤2, zero fughe e residuo terminale zero;
5. usare soltanto i nuovi seed development preregistrati nel manifest E18;
   holdout e final-confirmation restano non autorizzati.

## Esibizione reattiva development a tre

La matrice seat-balanced sui sette seed development è completa: 42/42 match,
zero errori. Codex V9 e Codex reattivo sono primi ex aequo con `15-12-1`,
media 112.149,21, zero fughe e delta diretto medio zero. Claude V2 chiude
`0-0-28`, media 11.777,64, due fughe e MOVE/produttive 2,9719. In ogni match
competitivo Claude ha comunque raggiunto 3Q. Nessun override Codex è scattato,
quindi il vantaggio Kaggle non è riprodotto dalla matrice locale corrente.

Report:
`experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`.

## Confronto esterno E17

Antigravity non è disponibile per esaurimento dei crediti. Il proprietario ha
quindi escluso il torneo locale incompleto e autorizzato una submission E17
per confronto esterno. La candidate mantiene le azioni V9 con soli metadati
di release aggiornati ed è identificata come controllo
`CODEX-E17.0-EXTERNAL-CONTROL-V1`. La submission Kaggle `559588638` è attiva:
la rilevazione più recente fornita dal proprietario è `996`, dopo un ingresso
a `600` (`+396`), con un episodio ancora in corso nello snapshot. È evidenza
osservata ma non ancora un rating stabile né uno score conclusivo. Il report è
in
`docs/model_specs/codex/e17/reports/E17_EXTERNAL_SUBMISSION_READINESS_REPORT_IT.md`.

## Gate E17 storici

Questi gate appartenevano alla proposta E17 e non sono i gate operativi E18;
E18 usa il manifest e il piano activation-first elencati sotto.

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR >= 90000
ANIMAL_ESCAPES == 0
MOVE_PER_PRODUCTIVE <= 1.20
EXECUTED_MARKET_LEDGER_COVERAGE == 100%
STRATEGIC_INDEPENDENCE_GATE == PASS  # per il prossimo torneo a tre
```

## Vincoli inderogabili

- nessun agente può importare o copiare routine, action table, planner,
  dispatcher o schedule di un altro;
- Foundation, replay discovery, schema del ledger e protocollo di benchmark
  possono essere condivisi;
- ogni variazione strategica deve modificare una sola famiglia causale;
- i nove replay Top 3 sono dati offline di discovery, mai input online;
- distinguere sempre `requested`, `executed`, `DERIVED` e `UNKNOWN`;
- nessun upload Kaggle ad hoc o iterativo: è autorizzata soltanto la
  submission quotidiana del miglior sviluppo `7-7-0`, dopo parity e gate
  tecnici minimi, come controllo esterno dichiarato; holdout e
  final-confirmation restano separati e l'esito non produce promozione
  automatica.

## Documenti da leggere

- `docs/PROJECT_STATE.md`;
- `experiments/e18/README.md`;
- `experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json`;
- `experiments/e18/design/E18_REACTIVE_662_TOP3_BENCHMARK_PLAN_V1.md`;
- `experiments/e18/reports/common/E18_662_TOP3_BASELINE_BENCHMARK_IT.md`;
- `experiments/e17/reports/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3_REPORT_IT.md`;
- `experiments/e17/prompts/common/E17_COMMON_REPOSITORY_REORGANIZATION_AND_LAUNCH_PROMPT.md`;
- `docs/repository/REPOSITORY_ARCHITECTURE.md`;
- `docs/repository/migration/POST_E17_EXTERNAL_RELEASE_CLEANUP.md`;
- `experiments/e17/design/E17_STRATEGY_FROZEN_V1.md`;
- `experiments/e17/reviews/common/E17_STRATEGY_RECONCILIATION.md`;
- `experiments/e17/reports/common/E17_0_GATE_AND_BLOCKER_SUMMARY.md`;
- `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`;
- `experiments/e17/reviews/common/E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`;
- `docs/model_specs/codex/e17/reports/E17_TOP3_REPLAY_ANALYSIS.md`;
- `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`;
- `docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`;
- `docs/model_specs/codex/e17/CODEX_V9_E17_RUNTIME_AND_FOUNDATION_MAPPING_IT.md`;
- `experiments/e17/reviews/common/E17_REACTIVE_DEVELOPMENT_AUTHORIZATION.md`;
- `experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md`;
- `docs/model_specs/claude/e17/prompts/E17_CLAUDE_REACTIVE_3Q_INDEPENDENT_BUILD_PROMPT.md`;
- `experiments/e17/reviews/common/E17_CLAUDE_ACTIVATION_COMPLIANCE_AND_CLEANUP_AUDIT.md`;
- `experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`;
- `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V3_IMPROVEMENT_PLAN.md`.
