# MODEL SPEC — Codex E18.18 7-7-0 capacity and trajectory planner V1

## Stato

`GATE_0_ORACLE_PASSED__GATE_1_SMOKE_FAILED__ROLLING_REPLAN_REQUIRED`.

E18.18 non nasce come overlay di comandi su E18.16. Prima viene costruito e
validato un simulatore offline che deve produrre una traiettoria completa e
feasible; solo dopo il suo superamento il piano diventa una policy esecutiva.

## Invarianti

- topologia livestock: `7-7-0`;
- pascoli pieni: `14`;
- cap risorse COW/SHEEP: `14`;
- manodopera: `12` hands assunti al picco, più il farmer, quindi `13` unità
  capaci di azione. Questa è la semantica dell'attuale metrica
  `peak_hands=12`; un eventuale target di 12 unità totali richiederebbe una
  ablation esplicita separata;
- stagione: 30 giorni, 24 turni al giorno;
- nessun cambio a topologia, cap o workforce durante l'ottimizzazione del
  piano;
- E18.16 resta il controllo interno, non il generatore autoritativo delle
  traiettorie E18.18.

## Diagnosi architetturale

Le regressioni E18.7–E18.17 non dimostrano che la dinamica interna non sia
pianificabile. Dimostrano che un correttivo locale non può sostituire una
traiettoria senza ricalcolare il lavoro successivo. Intercettare un WATER,
ritardare un MOVE o bloccare un PLANT modifica posizione, inventario e finestre
future di uno schedule registrato altrove; l'effetto economico appare quindi
molti turni dopo l'override.

Il nuovo contratto è `PLAN → EXECUTE → ACK → DAILY_REPLAN`, non
`PROVIDER → LOCAL_OVERRIDE`.

## Modello esatto da simulare

Il simulatore usa le regole dell'environment Kaggriculture come source of
truth, incluse legalità e transizioni di fine giornata. Non usa durate o yield
stimati quando sono disponibili le regole esatte.

### Stato e decisioni

Per ogni giorno, turno e unità registra:

- posizione e azione;
- tile/entità assegnata e cluster proprietario;
- inventario trasportato;
- evento biologico servito e relativa finestra;
- transizione attesa e ack osservato;
- slack residuo prima della hard deadline.

Le variabili decisionali sono:

- coordinate crop utilizzabili dopo avere fissato pascoli, coop e corridoi;
- specie coltivata e giorno di PLANT per ogni tile/coorte;
- giorno/turno di WATER, HARVEST, DIG e replant;
- giorno/turno di FEED, CARE e raccolta prodotto per ogni animale;
- sequenza di tile percorsa da ciascuna unità ogni giorno;
- PICKUP/DROP e liquidazione terminale;
- ultimo giorno di PLANT per ciascuna specie.

### Vincoli duri

1. una sola azione per unità e turno; un MOVE attraversa una sola tile;
2. tutte le azioni devono essere legali sullo stato simulato;
3. un nuovo PLANT deve essere annaffiato nello stesso giorno;
4. nessuna pianta può raggiungere due end-of-day consecutivi senza WATER;
5. nessun animale può raggiungere due end-of-day consecutivi senza FEED;
6. WATER e FEED duplicati nello stesso giorno sono vietati;
7. maturazione, intervalli di produzione, decadimento e max-held rispettano
   esattamente l'engine;
8. semi, Wheat di FEED, inventari, shed capacity 100, cash e market-order cap
   devono restare feasible;
9. ogni raccolto terminale deve includere il percorso di ritorno, DROP e SELL
   prima della fine: il solo raggiungimento biologico entro D30 non basta;
10. nessuna rotta può usare uno slot già prenotato per struttura, logistica o
    safety.

### Obiettivo lessicografico

1. zero fughe animali, crop persi per starvation e hard-deadline miss;
2. zero comandi illegali/no-op pianificati;
3. massimizzare valore venduto netto di semi, animali, land e hires;
4. minimizzare MOVE, poi PASS;
5. mantenere almeno l'`1%` della capacità giornaliera non prenotata nel piano
   nominale. È una soglia di fattibilità Gate 0A, non un margine sufficiente per
   il live: il campione Top770 usa il `93%` circa degli slot complessivi e nei
   picchi la composizione esatta `7-7-0` lascia poco slack; weed, retry e
   deviazioni saranno quindi assorbiti dal rolling replan del Gate 1.

Il numero di crop tile non è quindi un target scelto a priori: è il massimo
insieme di coorti per cui tutte le future finestre di servizio, raccolta e
liquidazione possono essere prenotate rispettando la riserva.

## Deadline biologiche iniziali

Con D1–D30 come numerazione umana, gli ultimi giorni teorici di PLANT sono:

| Coltura | Ultimo PLANT per maturazione/ciclo completo entro D30 | Ultimo PLANT per almeno un HARVEST entro D30 |
|---|---:|---:|
| Wheat | D26 | D28 |
| Carrot | D27 | D28 |
| Tomato | D19 per quattro produzioni | D22 |
| Strawberry | D14 per quattro produzioni | D20 |
| Melon | D18 | D20 |

Sono upper bound biologici, non cutoff operativi. Il planner deve anticiparli
quando il percorso HARVEST → shed → DROP → SELL e la riserva di capacità non
entrano nell'orizzonte residuo.

## Decomposizione del solver

Per evitare un MILP monolitico ingestibile su 13 unità × 720 turni:

1. **layout freeze** — fissa strutture, corridoi e cluster della `7-7-0`;
2. **cohort/capacity allocation** — sceglie mix, tile e date di PLANT con
   prenotazione delle finestre future per giorno e cluster;
3. **daily route solver** — costruisce route multi-unità dal deposito centrale,
   preservando carrier affinity per Wheat e prodotti;
4. **exact engine replay** — esegue il piano nell'environment reale e confronta
   transizioni attese/osservate;
5. **daily rolling replan** — a D+1 ricostruisce soltanto il futuro non ancora
   eseguito, mantenendo fermi gli impegni entro la safety window.

Il mercato entra come insieme di scenari economici; non può rendere infeasible
la cura biologica già prenotata. Weed casuali e variazioni di prezzo consumano
la riserva, non riscrivono continuamente tutte le route.

## Output obbligatori prima della policy

- mappa con ruolo di ogni tile;
- numero di crop tile per specie e coorte;
- ultimo giorno operativo di PLANT per specie;
- calendario giornaliero di servizi richiesti, capacità, MOVE e slack;
- traiettoria di ciascuna delle 13 unità per ogni turno;
- ledger di task planned/executed/acknowledged/missed;
- curva di produzione, shed occupancy, vendite e money;
- spiegazione di ogni infeasibilità e del vincolo che limita una tile
  addizionale.

## Gate preregistrati

### Gate 0 — oracle deterministico

- weed spawn disabilitato e mercato nominale;
- 100% azioni legali ed eventi hard-deadline completati;
- zero starvation/escape e zero overflow;
- almeno 1% di slack giornaliero pianificato nel caso oracle nominale;
- liquidazione terminale completa;
- due esecuzioni identiche producono lo stesso hash di piano e outcome.

### Gate 1 — robustezza development

- sette seed development, entrambi i seat, regole standard;
- zero perdite animali e zero crop starvation causati dal piano;
- nessun giorno supera la capacità disponibile;
- almeno 95% degli eventi entro la finestra target e 100% entro la hard
  deadline;
- nessun uso di holdout/final-confirmation.

### Gate 2 — campioni interni

Solo dopo Gate 0 e Gate 1, confronto matched con E18.16, E18.2 ed E17 V4D.
La promozione richiede contemporaneamente integrità, money non inferiore a
E18.16, MOVE non superiore e maggiore output monetizzato. Una matrice non può
essere usata per modificare retroattivamente i vincoli del planner.

## Ordine di implementazione

1. estrarre layout, calendario e traiettorie E18.16 come baseline osservata;
2. implementare simulatore biologico e testarlo per parità con l'engine;
3. aggiungere prenotazione di capacità e calcolo automatico dei cutoff;
4. aggiungere solver delle route giornaliere;
5. eseguire Gate 0 e produrre la prima proposta di mix/tile/cutoff;
6. soltanto dopo, costruire l'executor E18.18 e procedere ai Gate 1–2.

Nessun codice agente E18.18 e nessuna submission sono autorizzati prima del
superamento del Gate 0.

### Avanzamento Gate 0 — 2026-09-05

Il sottogate `0A` è superato con un planner deterministico nativo, senza
riutilizzare E18.16 come provider e senza copiare lo stream di azioni esterno.
Il piano usa le evidenze Top770 come vincoli di consistenza:

- mix finale `9 COW + 5 SHEEP`;
- checkpoint crop D1/D5/D10/D15/D20/D25 e chiusura D30;
- peak 62 entro D13, plateau 61 e stop ai replant annuali a D25;
- fertilizzazione allocata sotto vincolo di riserva, con output shadow 892
  contro il riferimento 885;
- route multi-unità tutte feasible sul capacity envelope osservato, con rientro
  quotidiano a uno degli accessi shed e `DROP` esplicito per ogni carrier;
- route ricalcolate sul timing reale: farmer e primi 10 HIRE da T2, ultimi 2 da
  T3;
- riserva minima `>=1%`, zero starvation/escape/azioni illegali shadow;
- annuali Q2 collocati sulle sette tile più vicine allo shed; raccolte
  permanenti distribuite per fase e WATER Q2 differibili di un solo giorno nei
  picchi D20/D23/D25;
- raccolta fertilizzante arrestata dopo D16, eliminando stock e rientri senza
  impiego pianificato;
- due costruzioni producono lo stesso hash.

Il solo risultato `0A` non equivaleva al Gate 0 completo: restavano da
dimostrare nell'interprete reale unlock, hire, cash, semi, feed, inventari,
shed e vendite terminali. Quella verifica è ora registrata nel sottogate `0B`
seguente; `executor_authorized=false` resta comunque un vincolo duro fino alle
guardie `0C`.

Artefatti:

- `tools/e18_18_capacity_trajectory_planner.py`;
- `tools/run_e18_18_770_capacity_trajectory_gate_0a.py`;
- `artifacts/derived/E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_V1.json`;
- `reports/E18_18_770_CAPACITY_TRAJECTORY_GATE_0A_REPORT_IT.md`.

### Avanzamento Gate 0B — 2026-09-05

Il replay nell'interprete esatto ha chiuso il sottogate `0B`, con una seconda
esecuzione identica sul seed oracle `180918001`:

- hash piano `844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1`;
- tutti i checkpoint crop e animali D1/D5/D10/D15/D20/D25/D30 esatti;
- `7-7-0`, `9 COW + 5 SHEEP`, 61 crop a D15/D20/D25 e zero crop starvation;
- 169/169 PLANT e 40/40 DIG riconosciuti;
- 100% dei WATER effettivamente emessi riconosciuti; 8 richieste nominali su
  coorti esaurite vengono filtrate state-aware prima dell'emissione;
- money terminale `117.077`, crop terminali `0` e shed terminale vuoto;
- hash dello stream esatto e outcome identici nel replay di conferma.

Il vincolo economico D7 è parte del piano, non un override: i due ovini
scaricano separatamente 6 WOOL ai turni 10–11, NE viene acquistato nello stesso
batch e i cinque PLANT iniziano soltanto dopo l'ack dell'unlock. Gli spawn degli
hands 11–12 sono ricalcolati sulle posizioni effettive a T2, perché l'engine li
crea dopo che le prime unità hanno già agito.

`policy_build_authorized=true`, ma `executor_authorized=false`. Le guardie
state-aware sono incluse nel controller oracle e impediscono l'emissione dei
comandi divenuti inapplicabili. L'estrazione in una policy autonoma resta
subordinata al rolling replan richiesto dal Gate 1.

Artefatti aggiuntivi:

- `tools/run_e18_18_770_capacity_trajectory_gate_0b.py`;
- `artifacts/derived/E18_18_770_CAPACITY_TRAJECTORY_GATE_0B_V1.json`;
- `reports/E18_18_770_CAPACITY_TRAJECTORY_GATE_0B_REPORT_IT.md`.

### Gate 1 smoke — 2026-09-05

Il primo seed development `180903001`, eseguito in entrambi i seat contro
E18.16 con weed e mercato standard, fallisce in modo identico nei due lati:

- E18.18 `55.934` contro E18.16 `85.578`, margine `-29.644` (`-34,64%`);
- topologia finale corretta `7-7-0`, ma solo `7 COW + 4 SHEEP`;
- 8 PLANT nominali, 7 DIG e 69 FEED vengono intercettati dalle guardie dopo
  una deviazione di stato;
- nessun errore tecnico, nessun uso di holdout o final-confirmation.

La causa non è la composizione `7-7-0`: una weed su un target impedisce il
task pianificato, la guardia evita il comando illegale ma il calendario statico
non reinserisce `DIG → task originario → servizio successivo`. Il ritardo si
propaga a posizione, feed e placement fino a perdere tre animali e circa il
35% del valore contro il controllo.

Il Gate 1 completo a 14 match non viene avviato dopo questo fail informativo.
La prossima implementazione deve aggiungere, in quest'ordine:

1. backlog per-worker con reinserimento del task originario dopo un DIG weed;
2. correzione di posizione verso la prossima tile pianificata;
3. priorità non differibile a FEED/PLACE e compressione dei task opzionali;
4. rolling replan giornaliero di rotte e procurement sullo stato osservato;
5. ripetizione dello smoke prima del Gate 1 preregistrato.

Artefatti smoke:

- `tools/run_e18_18_770_capacity_trajectory_gate_1_smoke.py`;
- `artifacts/derived/E18_18_770_CAPACITY_TRAJECTORY_GATE_1_SMOKE_V1.json`;
- `reports/E18_18_770_CAPACITY_TRAJECTORY_GATE_1_SMOKE_REPORT_IT.md`.

### Esito del successore E18.19 — 2026-09-05

Il backlog state-aware è stato implementato in E18.19. A parità di piano e
seed, il delta diretto supera E18.18 in entrambi i seat (`+69,95%` sulla
mediana) e ripristina `9 COW + 5 SHEEP`. Lo smoke separato contro E18.16 resta
però `FAIL` economico (`-34,50%`), pur conservando topologia e composizione.
E18.18 resta quindi un piano oracle valido ma non un executor live; lo stato
del successore e la prossima ablation sono in
`MODEL_SPEC_CODEX_E18_19_770_RETRYING_TRAJECTORY_V1.md`.

## Baseline trajectory extraction

Prima estrazione completata sul seed development `180903001`, player 0,
contro mirror E18.16. La matrice contiene le 75 tile di Q0/Q1/Q2 e tutti i
720 step; le azioni sono associate alla tile sorgente prima dell'esecuzione.
Sono proiettati `7.296` eventi unitari. Altri `222` eventi hanno origine in Q3
(soprattutto transito/spawn su tile locked) e sono conservati nel riepilogo,
ma non aggiunti come 76a riga per rispettare la matrice richiesta.

L'identità cromatica `M01..M12` rappresenta lo slot hand del giorno, non una
persona persistente fra giorni, perché gli hands scadono e vengono riassunti
ogni fine giornata. Il farmer usa un'identità separata. La baseline registra
le azioni richieste; l'ack planned/executed sarà il livello successivo del
simulatore.

Artefatti riproducibili:

- `tools/build_e18_16_base_trajectory_matrix.py`;
- `artifacts/derived/E18_16_BASE_TRAJECTORY_MATRIX_S180903001_P0.json`.
