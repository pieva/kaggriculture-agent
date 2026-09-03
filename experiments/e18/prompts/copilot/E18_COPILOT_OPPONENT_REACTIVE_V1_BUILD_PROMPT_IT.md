# E18 — prompt Copilot per una candidate opponent-reactive V1

## Mandato

Costruisci e verifica una nuova candidate Copilot E18 realmente
opponent-reactive. Non fermarti alla proposta: implementa controller,
configurazione, telemetria, test, runner development e report. Mantieni
l'indipendenza e la robustezza tecnica della linea Native, ma supera il suo
controller crop-only quasi statico.

Il target finale è 100.000 di denaro. Questa iterazione deve produrre un delta
misurabile sia nei KPI sia nell'architettura; non basta rinominare soglie o
aggiungere una guardia che non cambia l'action stream.

## Evidenza di partenza

Nel torneo E18 V1, Copilot Native ha prodotto:

- 28 run, record `1-27-0`;
- media `9.812,46`, mediana `8.847`, range `8.261–15.183`, pari al `9,81%`
  del target;
- media `10.967,93` contro Codex E18 e `8.657,00` contro Claude V3;
- zero errori, fallback e perdite zootecniche;
- 9 action stream/profili su 28 run;
- divergenza condizionata all'avversario `6/14` sugli action stream e `0/14`
  sulla topologia;
- una sola topologia finale, nessun selector opponent-aware e mean peak weed
  `34,29`.

Il punto di forza da conservare è un controller indipendente, deterministico
e sicuro. Le lacune sono scala economica, poca diversità causale, workforce
rigida e un lifecycle che lascia troppa superficie trasformarsi in weed.

Leggi come evidenza numerica:

- `experiments/e18/reports/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md`;
- `experiments/e18/artifacts/derived/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1.json`;
- `experiments/e18/reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md`;
- `experiments/e18/reports/common/E18_CLAUDE_COPILOT_CANDIDATE_INTAKE_IT.md`.

Usa `src/agricola/strategy/copilot/e17_native_3q.py` come controllo congelato.
Costruisci la nuova strategia nel namespace Copilot usando soltanto codice
Copilot o infrastruttura condivisa non strategica. Non importare, copiare o
avvolgere controller, planner, routine o action table Codex/Claude. Gli altri
agenti sono avversari black-box.

## Scelta progettuale obbligatoria

Prima di implementare, dichiara e congela una delle due famiglie:

1. `ADAPTIVE_CROP`: crop-only, ma con almeno due footprint/topologie di
   coltivazione e due piani di workforce materialmente diversi;
2. `ADAPTIVE_MIXED`: crop/livestock, con almeno due distribuzioni
   topologiche intenzionali e controllo completo di capacità/feed.

Non cambiare famiglia dopo aver visto i risultati del torneo. In entrambi i
casi la reattività deve derivare da stato pubblico corrente dell'avversario,
non da nome, rating, seed, replay ID, inventari privati o memoria
cross-episode.

## Architettura richiesta

Implementa componenti separati e testabili:

1. `PUBLIC_OPPONENT_SNAPSHOT`, acquisito in una finestra D4–D8, con feature
   dichiarate quali quadranti, workers visibili, crop, animali, pascoli e weed;
2. `REGIME_CLASSIFIER`, che restituisce regime, feature contribution e
   confidence;
3. `HYSTERETIC_SELECTOR`, sticky oppure con transizioni limitate e motivate;
4. `FOOTPRINT_PLANNER`, che converte il regime in celle target e budget;
5. `WORKFORCE_CAPACITY_CONTROLLER`, basato su backlog servibile, distanze,
   scadenze e capacità giornaliera, non su un conteggio fisso;
6. `CROP_LIFECYCLE_CONTROLLER` con stati
   `KEEP / HARVEST / DIG / REPLANT`;
7. `ACTION_ARBITER` con priorità esplicite e nessun fallback silenzioso.

I regimi devono modificare almeno footprint e workforce; cambiare soltanto il
tipo di seme non vale come architettura dinamica. Per esempio, senza imporre
la soluzione, una fixture a bassa pressione può privilegiare consolidamento
e resa, mentre una ad alta pressione può anticipare espansione e personale.

## Correzione del lifecycle

Usa età, `max_lifespan_step`, acqua, weed, yield e giorni residui. Aggiungi
fixture deterministiche per:

- Strawberry prossima alla scadenza → `DIG` → Wheat → `WATER` → `HARVEST`;
- Wheat mantenuta viva fino a una resa conveniente;
- recupero di backlog prima di espandere il footprint;
- aumento di workforce quando capacità prevista < domanda di servizio;
- riduzione controllata del footprint quando il backlog non è recuperabile.

Misura separatamente `starved_to_weed`, `expired_to_weed`, weed exit, mean
peak weed, raccolti, resa per harvest, tile-days vivi, backlog e idle worker.

## Gate architetturali

Sono hard gate indipendenti dal denaro:

- almeno 2 regimi nominati e attivati nelle fixture;
- selector con decisione o transizioni registrate e causalmente spiegate;
- fixture avversarie diverse a stesso seed/seat producono action stream,
  footprint e piano workforce differenti nel `100%` dei casi previsti;
- nel torneo development, divergenza condizionata action stream almeno
  `12/14` e topologia/work allocation almeno `10/14` gruppi seed-seat;
- almeno 2 profili finali intenzionali di footprint o workforce;
- zero errori, fallback silenziosi e contract breach;
- per `ADAPTIVE_MIXED`, zero perdite verificate su tile+shed+inventari;
- per `ADAPTIVE_CROP`, `starved_to_weed=0` nelle fixture e mean peak weed
  ridotta almeno del `50%` rispetto a `34,29`;
- snapshot, classificazione, regime, transizioni, footprint, backlog,
  capacità e motivazione delle azioni presenti nella telemetria.

## Gate KPI e milestone verso 100k

Usa soltanto i seed development E18 `180903001–180903007`, entrambi i seat,
senza sostituire run fallite. Confronta la nuova candidate con Copilot Native,
Codex E18 e Claude V3 congelati, riportando ogni matchup separatamente.

La candidate supera il gate economico di questa iterazione soltanto se:

- migliora di almeno `+50%` la media paired rispetto a Copilot Native sulla
  stessa matrice;
- non peggiora il minimo Native di `8.261` di oltre il `10%`;
- migliora il matchup contro Codex E18 di almeno `+25%` rispetto alla media
  Native di `10.967,93`;
- dimezza mean peak weed e migliora resa media per harvest;
- raggiunge almeno `15.000` di media complessiva come milestone M1;
- mantiene zero errori, fallback e perdite verificate.

Documenta la distanza dalle milestone M2 `25.000`, M3 `50.000` e dal target
`100.000`. Il target non è raggiunto perché un matchup debole porta la media
sopra 100k: serve robustezza per classe di avversario.

## Artefatti obbligatori

Crea file nuovi senza sovrascrivere Native o le ablation 6-6-2 V3/V4:

- controller sotto `src/agricola/strategy/copilot/`;
- config sotto `experiments/e18/configs/copilot/`;
- test unitari e fixture sotto `experiments/e18/tests/`;
- runner sotto `experiments/e18/tools/copilot/`;
- JSON e CSV derivati sotto `experiments/e18/artifacts/derived/copilot/`;
- report italiano sotto `experiments/e18/reports/copilot/`;
- SHA-256 di sorgente, config, runner e artefatti.

Il report deve terminare con verdetti distinti:

```text
TECHNICAL_GATE: PASS|FAIL
DYNAMIC_ARCHITECTURE_GATE: PASS|FAIL
ECONOMIC_GATE: PASS|FAIL
PROMOTION_RECOMMENDATION: PROMOTE|REJECT|ITERATE
```

Una policy economicamente migliore ma architetturalmente inerte non viene
promossa. Una policy dinamica che non migliora weed, resa e denaro resta una
prova tecnica. Non usare holdout o final confirmation e non preparare una
submission Kaggle senza nuova autorizzazione del proprietario.
