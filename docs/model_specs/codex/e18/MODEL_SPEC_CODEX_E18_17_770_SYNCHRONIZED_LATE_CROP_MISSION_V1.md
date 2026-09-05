# MODEL SPEC — Codex E18.17 7-7-0 synchronized late crop mission V1

## Obiettivo

Correggere l'inversione economica D21-D30 osservata nelle 17 sconfitte Kaggle
di E18.16, senza modificare topologia `7-7-0`, cap 14, FEED, market, numero di
worker o composizione zootecnica.

## Ipotesi causale

E18.16 mantiene più superficie crop dei vincitori ma accumula più stress,
weed e HARVEST non riconosciuti. La causa candidata è la mancata
sincronizzazione fra ammissione dei nuovi PLANT, priorità di servizio e
completamento delle route. Una policy che riduca il work-in-progress quando il
backlog è alto e completi una missione HARVEST prima del refill deve aumentare
output e monetizzazione senza richiedere nuova capacità.

## Trattamento isolato

Tra D21 e D28:

1. priorità locale `HARVEST_READY → WATER_AT_RISK → DIG_WEED → PLANT`;
2. admission control strumentato ma con soglie conservative in V1, dopo che il
   pre-gate ha falsificato sia il blocco aggressivo (59 PLANT soppressi e
   output `-28%`) sia il cutoff D27-D28 (16 PLANT soppressi e output `-3,6%`);
3. una sola missione HARVEST persistente e riservata, assegnata esclusivamente
   a un'unità già sul target in PASS e fuori dagli accessi shed;
4. completion soltanto dopo ack osservato come riduzione/rimozione dello yield;
   un mancato ack rilascia subito worker e reservation, evitando retry che
   blocchino la traiettoria del provider;
5. telemetria di backlog, admission, route, retry, cancellation e ack.

Le missioni HARVEST già emesse dal provider vengono adottate nel ledger di
reservation/ack senza modificarne il comando. Un PASS locale viene convertito
solo se nessun'altra unità sta già servendo lo stesso tile.

Gli override locali e la missione toccano soltanto PASS. Non esiste rerouting:
MOVE, FEED, PICKUP, DROP e ogni altra logistica restano autoritativi. Il
pre-gate ha mostrato che anche sei soli MOVE ritardati peggioravano raccolto e
starvation, quindi V1 mantiene route distance zero. Il primo gate completo ha
inoltre falsificato due WATER locali sugli accessi shed: causavano due perdite
animali per match e sono ora vietati in modo esplicito.

## Freeze

- base: `CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-V1`;
- pastures: `Q0=7`, `Q1=7`, `Q2=0`, fill 14;
- livestock resource cap: 14;
- market e worker count invariati;
- nessun batching SELL in questa release;
- sole feature pubbliche; nessun uso dell'inventario privato per il routing;
- nessuna memoria cross-episode.

## Gate development

Confronto causalmente matched contro E18.16 sui sette seed development e
entrambi i seat. Requisiti minimi:

- topologia/fill/cap 14 e zero livestock loss in tutti i match;
- zero errori e fallback;
- mission ack osservato e zero override di comandi non autorizzati;
- effetto del trattamento sulle azioni osservato in ogni match: la sola
  telemetria passiva non vale come attivazione causale;
- money medio non inferiore al controllo e worst matched almeno `-2%`;
- HARVEST ack rate e unità raccolte non inferiori al controllo;
- late unwatered e starved-to-weed non peggiori;
- MOVE non oltre `+1%`.

Solo dopo il gate causale la candidata viene confrontata, senza tuning, con i
campioni interni congelati E18.2 e E17 V4D. Holdout e final-confirmation non
sono autorizzati né consumati.

## Esito development

Verdetto: `FAIL — SAFE_BUT_BEHAVIORALLY_INERT`.

Il gate completo su sette seed development e due seat (`14` match) conferma
topologia/fill `7-7-0/14` in `14/14`, cap 14, zero perdite livestock, zero
errori e zero fallback. Il ledger passivo adotta e riconosce in media `79`
HARVEST del provider per match, ma il trattamento non modifica alcun comando:
PLANT bloccati, override locali e route/service mission aggiuntivi sono tutti
zero.

Di conseguenza E18.17 V1 replica E18.16 su tutti i KPI aggregati: money
`65.632,29`, MOVE `3.608,14`, PASS `846,14`, HARVEST ack `62,91%`, unità
raccolte `579,79`, late-unwatered `232` e starved-to-weed `12`. Il record
grezzo `1-1` sul seed `180903004` è interamente un effetto seat: a parità di
seat candidata e controllo ottengono lo stesso money.

La matrice più ampia contro E18.2 ed E17 V4D non viene eseguita: il gate
preregistrato la ammette soltanto dopo un effetto causale osservabile. E18.16
resta la base interna; E18.17 V1 non è promuovibile né candidabile alla
submission quotidiana. La decisione successiva E18.18 sostituisce l'idea di
un altro override con un capacity/trajectory planner offline: solo una
traiettoria feasible e validata diventerà un dispatcher nativo. Strutture,
accessi shed e logistica restano vincoli duri, perché il pre-gate ha già
falsificato cutoff PLANT, anticipo MOVE e WATER locale sullo shed.

Report riproducibile:
`reports/E18_17_770_SYNCHRONIZED_LATE_CROP_MISSION_DEV_GATE_REPORT_IT.md`.
