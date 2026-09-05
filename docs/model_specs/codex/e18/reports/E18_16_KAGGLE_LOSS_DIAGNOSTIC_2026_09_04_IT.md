# E18.16 — diagnosi delle sconfitte Kaggle della submission 56012496

Data di acquisizione: 2026-09-04. Ruolo epistemico:
`EXTERNAL_DIAGNOSTIC_NOT_HOLDOUT`.

## Perimetro e integrità

La lista Kaggle della submission `56012496` mostrava rating `952` e 37 replay
completati: 20 vittorie e 17 sconfitte. Sono state acquisite e analizzate tutte
le 17 sconfitte visibili, con 17 seed e 17 avversari distinti; Codex occupa P0
in 11 episodi e P1 in 6. Ogni replay contiene 720 step e stato terminale
`DONE/DONE`. Il parser è lo stesso usato dal benchmark lifecycle E18.

Gli action record sono comandi richiesti; PLANT/WATER/HARVEST/DIG
`acknowledged` sono invece verificati sulle transizioni di stato. I flussi di
cassa sono delta osservati del denaro, quindi eseguiti ma non attribuibili con
certezza a un singolo ordine quando acquisti e vendite condividono lo stesso
turno. Gli avversari sono eterogenei: il confronto paired descrive il gap
osservato nelle sconfitte, non identifica da solo un controfattuale causale.

Artefatti riproducibili:

- `docs/model_specs/codex/e18/artifacts/derived/E18_16_KAGGLE_LOSS_DIAGNOSTIC_2026_09_04.json`;
- `docs/model_specs/codex/e18/artifacts/derived/E18_16_KAGGLE_LOSS_EPISODES_2026_09_04.csv`;
- `docs/model_specs/codex/e18/tools/analyze_e18_16_kaggle_losses.py`.

## Sintesi economica

E18.16 perde mediamente `6.268` (`76.018` contro `82.286`, `-7,6%`), con
mediana `-3.803`. Le tre sconfitte più pesanti — monnosuke, AMANI DD e Pascal
— valgono `58.351`, pari al `54,8%` della somma di tutti i margini negativi.

Il dato decisivo è temporale. Codex è avanti mediamente di `1.388` a D10 e di
`6.172` a D20; tra D20 e D30 produce però soltanto `36.697` netti contro
`49.138`, cedendo `12.440`. La perdita non deriva da spesa eccessiva nel
late-game: Codex incassa `18.395` in meno e spende `5.954` in meno. Il numero
di incrementi positivi del denaro è più alto, ma l'incremento medio D21-D30 è
`556` contro `1.075`: ricavo molto più frammentato e `-48,3%` per evento.

## KPI paired nelle 17 sconfitte

| KPI medio | E18.16 | Vincitori | Delta E18.16 | Lettura |
|---|---:|---:|---:|---|
| Reward finale | 76.018 | 82.286 | -6.268 | gap osservato `-7,6%` |
| Denaro D10 | 2.312 | 923 | +1.388 | apertura non debole |
| Denaro D20 | 39.320 | 33.148 | +6.172 | vantaggio prima del late-game |
| Guadagno netto D20-D30 | 36.697 | 49.138 | -12.440 | inversione economica principale |
| Incassi lordi D21-D30 | 45.951 | 64.346 | -18.395 | deficit di monetizzazione |
| Spesa lorda D21-D30 | 9.254 | 15.208 | -5.954 | non è overspending |
| Incasso per evento positivo D21-D30 | 556 | 1.075 | -519 | transazioni/produzione frammentate |
| Crop tile-days D21-D30 | 506,6 | 392,6 | +113,9 | più superficie, non più output |
| Unwatered tile-days D21-D30 | 231,4 | 153,0 | +78,4 | backlog idrico `+51,2%` |
| Water-stressed tile-days D21-D30 | 218,6 | 155,5 | +63,1 | stress `+40,5%` |
| Uscite a weed | 45,0 | 34,6 | +10,4 | degrado del lifecycle |
| Starved-to-weed | 12,1 | 3,9 | +8,2 | oltre tre volte il riferimento |
| Unità raccolte | 579,2 | 621,9 | -42,6 | output `-6,9%` con più tile |
| Crop service acknowledged | 1.353,1 | 1.227,4 | +125,8 | più lavoro, resa inferiore |
| Azioni produttive | 3.064,7 | 2.777,2 | +287,5 | volume non convertito in denaro |
| MOVE | 3.606,9 | 3.758,6 | -151,8 | movimento non è il primo problema |
| MOVE/produttive | 1,177 | 1,362 | -0,185 | efficienza geometrica già migliore |
| PASS | 847,4 | 552,8 | +294,6 | capacità inutilizzata `+53,3%` |
| PASS share | 11,27% | 7,85% | +3,42 pp | backlog non assegnato |
| Live crop rotations | 1,0 | 3,47 | -2,47 | reazione tardiva alla fine ciclo |
| Animali finali | 14,0 | 13,18 | +0,82 | cap 14 raggiunto; non è il gap primario |

E18.16 mantiene `7-7-0` esatto in `17/17`. Le topologie finali dei vincitori
sono `8-5-1` in 9 episodi, `6-6-2` in 2 e altre sei configurazioni singole.
Questo campione contiene soltanto sconfitte e non consente di attribuire il
gap alla topologia; in base alla decisione corrente, `7-7-0` resta congelata.

## Efficienza del crop service

| Opcode | E18.16 richiesti | E18.16 ack | Ack rate | Vincitori richiesti | Vincitori ack | Ack rate |
|---|---:|---:|---:|---:|---:|---:|
| PLANT | 192,0 | 189,6 | 98,8% | 151,1 | 148,6 | 98,4% |
| WATER | 901,9 | 876,9 | 97,2% | 853,3 | 827,6 | 97,0% |
| HARVEST | 385,9 | 242,5 | 62,8% | 329,8 | 223,1 | 67,7% |
| DIG | 46,2 | 44,1 | 95,4% | 30,2 | 27,9 | 92,4% |

La quasi totalità del differenziale di comandi non riconosciuti è HARVEST:
E18.16 emette circa `143,5` HARVEST non confermati per episodio, contro
`106,6` dei vincitori (`+36,9`). PLANT e WATER sono quasi sempre eseguiti; il
problema non è inviare WATER, ma dimensionare superficie e timing affinché il
ciclo produca raccolti ad alta resa prima della scadenza.

Nel late-game E18.16 emette inoltre più PLANT (`+21,9`), HARVEST (`+13,1`) e
DIG (`+14,0`) dei vincitori, con WATER sostanzialmente pari (`+1,4`). La
combinazione “più tile + più comandi + meno unità” identifica un deficit di
coordinamento e service capacity, non una carenza assoluta di azioni.

## Episodi acquisiti

| Episode | Avversario | Seat | E18.16 | Avversario | Margine | Topologia avversaria |
|---:|---|---:|---:|---:|---:|---|
| 105496417 | Rf28 | P1 | 61.550 | 67.545 | -5.995 | 8-5-1 |
| 105493733 | AMANI DD | P1 | 72.911 | 94.333 | -21.422 | 5-5-3 |
| 105492836 | Csaba József | P0 | 85.596 | 89.494 | -3.898 | 8-5-1 |
| 105491963 | 好7吊黑上唔去 | P1 | 90.966 | 94.659 | -3.693 | 8-4-0 |
| 105491066 | Pablo Montenegro | P0 | 109.290 | 113.093 | -3.803 | 14-0-0 |
| 105490149 | CyberRacoon | P0 | 74.248 | 80.791 | -6.543 | 8-5-1 |
| 105488377 | Nikita Biryukov | P0 | 59.726 | 63.012 | -3.286 | 10-0-0 |
| 105486567 | Mutte1904 | P0 | 63.564 | 68.006 | -4.442 | 8-5-1 |
| 105485677 | Sujith Kumar Sashikanth | P0 | 72.246 | 75.039 | -2.793 | 8-5-1 |
| 105483909 | monnosuke | P0 | 63.633 | 87.446 | -23.813 | 11-2-1 |
| 105480327 | Jiarui (Jerry) Cao | P1 | 82.111 | 88.802 | -6.691 | 8-5-1 |
| 105477657 | Tekin24 | P1 | 90.102 | 90.349 | -247 | 6-6-2 |
| 105476781 | Monster | P0 | 75.140 | 75.280 | -140 | 8-5-1 |
| 105475877 | Avvy Lavoienne | P0 | 57.230 | 58.989 | -1.759 | 8-5-1 |
| 105474957 | ziheng | P1 | 92.382 | 94.421 | -2.039 | 6-6-2 |
| 105473174 | Pascal | P0 | 94.114 | 107.230 | -13.116 | 10-6-0 |
| 105470464 | kaggle_bbgg | P0 | 47.490 | 50.367 | -2.877 | 8-5-1 |

## Criticità ordinate per potenziale impatto economico

### 1. Conversione economica D21-D30 — impatto molto alto

Segnale: il vantaggio `+6,2k` a D20 diventa `-6,3k`; il differenziale netto
del solo D20-D30 è `-12,4k`, trainato da `-18,4k` di incassi lordi. Codex ha
più eventi positivi ma ciascuno vale circa la metà.

Cause probabili: ciclo crop non sincronizzato con maturazione, inventario e
vendita; output in lotti piccoli; slot produttivi mantenuti attivi senza una
garanzia di raccolta e monetizzazione entro l'orizzonte residuo.

Rimedio: introdurre in E18.17 un controller late-game state-driven che ammetta
nuovi PLANT soltanto con service slack sufficiente e assegni priorità a
HARVEST_READY e WATER con deadline. Conservare `7-7-0`, cap 14 e FEED.

### 2. Sovraccarico del lifecycle crop — impatto alto

Segnale: `+29%` crop tile-days late, ma `-6,9%` unità; unwatered `+51%`,
water-stressed `+41%`, starved-to-weed più che triplo. La superficie supera la
capacità effettiva di servizio.

Cause probabili: PLANT calendarizzato senza admission control, priorità WATER
non sensibile alla scadenza e DIG reattivo dopo la degenerazione a weed.

Rimedio: budget giornaliero di service capacity per cluster; bloccare PLANT
quando `water_due + harvest_ready + route_slack` supera la capacità residua;
ordinare WATER per rischio di starvation e fare rotazione locale prima della
weed quando il payback residuo è positivo.

### 3. HARVEST richiesti ma non completati — impatto medio-alto

Segnale: ack HARVEST `62,8%` contro `67,7%`; circa `36,9` fallimenti
aggiuntivi per episodio. PLANT/WATER hanno invece ack vicino al 98%.

Cause probabili: missioni cancellate o rese stale da spostamenti intermedi,
target non più pronto all'arrivo, assenza di reservation e feedback ack nel
dispatcher. È coerente con i precedenti fallimenti degli overlay MOVE.

Rimedio: missioni persistenti `route → service → ack`, reservation del tile,
invalidazione soltanto su mutazione osservata e riassegnazione dalla posizione
corrente. Non trasformare indiscriminatamente PASS in MOVE e non sovrascrivere
la logistica dello shed.

### 4. Liquidazione frammentata — impatto medio, evidenza non ancora causale

Segnale: `+13,4` eventi di cassa positivi late ma ricavo per evento `-48%`.
Il dato è netto-eseguito e può includere acquisti nello stesso turno, quindi
va confermato con un ledger market requested/executed locale.

Cause probabili: carrier che rientrano con inventario ridotto, SELL frequenti
prima del batch economico, mancato coordinamento fra harvest, DROP e SELL.

Rimedio: strumentare subito il ledger; mantenere la policy invariata in
E18.17. Se il segnale sopravvive al gate lifecycle, isolare in E18.18 un batch
inventory/slack-aware per DROP/SELL, senza cambiare topologia o crop mix.

### 5. Capacità inutilizzata e rigidità open-loop — impatto medio

Segnale: PASS `+53%`, pur con MOVE/produttive migliore. Nelle 17 sconfitte la
policy è strutturalmente quasi invariata: `7-7-0` in 17/17, una sola live crop
rotation in ogni episodio, 66 PLANT late in ogni episodio e unità raccolte in
un intervallo strettissimo, mentre il reward varia da `47.490` a `109.290`.

Cause probabili: schedule fisso che non adatta volume e composizione al
backlog, ai prezzi e allo stato eseguito; mission queue esaurita senza refill
causale. Il solo riempimento dei PASS è già stato falsificato da E18.8.

Rimedio: refill del dispatcher soltanto a mission completion, scegliendo un
task locale dal backlog osservato; rendere le soglie di PLANT/WATER/HARVEST
dipendenti da service pressure e giorni residui. La reattività deve essere
verificata con activation ledger e divergenza spiegabile, mantenendo target
topologico `7-7-0`.

## Raccomandazione per la prossima release

E18.17 dovrebbe isolare una sola famiglia causale:
`SYNCHRONIZED_LATE_CROP_MISSION_CONTROLLER`. Scope minimo:

1. admission control dei PLANT D21-D30 basato su service slack;
2. priorità `HARVEST_READY → WATER_AT_RISK → DIG/ROTATE → PLANT`;
3. missioni persistenti con reservation e ack prima del refill;
4. nessuna nuova topologia, nessun hand aggiuntivo, nessuna modifica a cap 14,
   FEED, coop/oca o market batching;
5. nuova telemetria per backlog, deadline, mission cancellation, ack e
   cashflow requested/executed.

Target diagnostici da verificare contro E18.16 sugli stessi campioni interni:
ridurre almeno della metà il gap starved-to-weed, portare l'ack HARVEST almeno
al riferimento `67,7%`, aumentare le unità raccolte senza aumentare MOVE e
ridurre unwatered late senza regressione del denaro minimo matched. Il
cashflow batching resta una ablation successiva, per non confondere le cause.
