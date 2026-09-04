# E18 — prompt Claude per una candidate opponent-reactive V1

## Mandato

Costruisci e verifica una nuova candidate Claude E18 autonoma. Non limitarti
all'analisi: implementa controller, configurazione, telemetria, test, runner
development e report. La candidate deve migliorare insieme il risultato
economico e la qualità dell'architettura dinamica.

Il target finale resta 100.000 di denaro. Questa iterazione è un passo
misurabile verso il target, non deve dichiarare il successo sulla base di una
media aggregata favorevole o della sola variabilità terminale.

## Evidenza di partenza

Nel torneo E18 V1, Claude V3 ha prodotto:

- 28 run, record `13-15-0`;
- media `12.850,18`, mediana `14.733`, range `43–19.926`, pari al `12,85%`
  del target;
- media `10.292,86` contro Codex E18 e `15.407,50` contro Copilot Native;
- 28 action stream distinti e 8 profili topologici finali;
- divergenza condizionata all'avversario `14/14` sugli action stream e
  `10/14` sulla topologia;
- 19 perdite zootecniche verificate su `tile + shed + inventories`, 51 cali
  giornalieri sui tile e weed media terminale `9,18`;
- nessun selector esplicito, snapshot causale, decisione sticky o registro
  delle transizioni di regime.

Il punto di forza da preservare è la task selection state-driven, già capace
di produrre comportamenti differenti. I difetti da correggere sono perdite
di bestiame, collassi economici, servizio discontinuo e assenza di una
decisione architetturale interpretabile.

Leggi come evidenza numerica:

- `experiments/e18/reports/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1_REPORT_IT.md`;
- `experiments/e18/artifacts/derived/common/E18_DYNAMIC_ARCHITECTURE_TOURNAMENT_V1.json`;
- `experiments/e18/reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md`;
- `experiments/e18/reports/common/E18_CLAUDE_COPILOT_CANDIDATE_INTAKE_IT.md`.

Puoi usare Claude V3 come controllo e riutilizzare esclusivamente componenti
Claude o infrastruttura condivisa non strategica. Non leggere, copiare,
importare o avvolgere controller, planner, routine, action table o config
strategiche Codex e Copilot. Codex E18 può essere affrontato soltanto come
avversario black-box e confrontato tramite il report comune.

## Architettura richiesta

Implementa una pipeline esplicita in cinque livelli:

1. `PUBLIC_OPPONENT_SNAPSHOT`: in una finestra dichiarata tra D4 e D8,
   fotografa soltanto feature pubbliche correnti, per esempio quadranti
   attivi, workers visibili, crop, animali, pascoli e weed;
2. `REGIME_CLASSIFIER`: produce un regime nominato e una motivazione
   serializzabile; vietato usare nome, rating, seed, replay ID, inventario
   privato o memoria cross-episode;
3. `STICKY_POLICY_SELECTOR`: sceglie almeno due regimi operativi realmente
   distinti e limita l'oscillazione con decisione sticky o isteresi esplicita;
4. `CAPACITY_AND_LIFECYCLE_CONTROLLER`: coordina workforce, servizio delle
   colture e capacità zootecnica;
5. `ACTION_ARBITER`: risolve conflitti con priorità e motivazione osservabile,
   senza fallback silenzioso.

I due regimi devono differire materialmente in almeno due dimensioni fra:

- distribuzione topologica dei pascoli o delle colture;
- numero, collocazione o calendario dei workers;
- budget e timing di espansione;
- rapporto crop/livestock;
- priorità di servizio e raccolta.

Non chiamare “reattiva” una policy che produce profili diversi soltanto per
effetti emergenti dello stato condiviso. La telemetria deve collegare feature,
regime scelto e cambiamento dell'action stream.

## Sicurezza e lifecycle obbligatori

Mantieni un ledger unico degli animali che comprenda tile, shed e inventari.
Prima di comprare, spostare o ritardare il servizio verifica capacità futura,
feed, worker e scadenze. Il gate usa `verified_livestock_losses`, non il solo
conteggio dei cali sui tile.

Per ogni coltura implementa lo stato esplicito
`KEEP / HARVEST / DIG / REPLANT`, usando età, `max_lifespan_step`, acqua,
weed, resa corrente e giorni residui. Devono esistere fixture che dimostrino:

- Strawberry prossima alla scadenza → `DIG` → Wheat → `WATER` → `HARVEST`;
- Wheat viva non raccolta prematuramente quando attendere aumenta la resa;
- nessuna coltura servibile abbandonata a weed per starvation di workforce;
- emergenza zootecnica prevalente su un'espansione non urgente.

## Gate architetturali

Sono hard gate, separati dal denaro:

- almeno 2 regimi nominati e attivati nelle fixture;
- esattamente una decisione primaria per run, oppure transizioni enumerate
  con isteresi e causalità registrata;
- a seed e seat identici, fixture avversarie causalmente diverse producono
  action stream diversi in `100%` dei casi previsti;
- nel torneo development, divergenza condizionata action stream almeno
  `12/14` e topologia/work allocation almeno `10/14` gruppi seed-seat;
- almeno 2 profili topologici o di workforce intenzionali, non accidentali;
- zero errori, fallback silenziosi e violazioni dell'observation contract;
- zero perdite zootecniche verificate;
- se mixed-farming: tutti i pascoli target costruiti e riempiti oppure una
  riduzione intenzionale dichiarata dal regime, mai un vuoto accidentale;
- telemetria per snapshot, score del classifier, regime, transizioni,
  motivazione delle azioni, backlog e capacità.

## Gate KPI e milestone verso 100k

Usa gli stessi seed development E18 `180903001–180903007`, entrambi i seat,
senza sostituire run fallite. Confronta la candidate con Claude V3 congelata,
Codex E18 black-box e Copilot Native congelato.

Riporta separatamente i matchup. La candidate supera il gate economico di
questa iterazione soltanto se:

- migliora di almeno `+25%` la media paired rispetto a Claude V3 sulla stessa
  matrice;
- non registra run sotto `5.000`;
- migliora il matchup contro Codex E18 di almeno `+20%` rispetto alla media
  Claude V3 di `10.292,86`;
- riduce `verified_livestock_losses` da 19 a 0;
- non peggiora weed exit e aumenta la resa media per harvest;
- raggiunge almeno `16.000` di media complessiva come milestone M1.

Documenta anche la distanza dalle milestone M2 `25.000`, M3 `50.000` e dal
target `100.000`. Non sommare matchup disomogenei per sostenere il
raggiungimento del target.

## Artefatti obbligatori

Crea file nuovi senza sovrascrivere V3/V5/V6:

- controller sotto `src/agricola/strategy/claude/`;
- config sotto `docs/model_specs/claude/e18/configs/`;
- test unitari e fixture sotto `experiments/e18/tests/`;
- runner sotto `docs/model_specs/claude/e18/tools/`;
- JSON e CSV derivati sotto `docs/model_specs/claude/e18/artifacts/derived/`;
- report italiano sotto `docs/model_specs/claude/e18/reports/`;
- SHA-256 di sorgente, config, runner e artefatti.

Il report deve terminare con tre verdetti indipendenti:

```text
TECHNICAL_GATE: PASS|FAIL
DYNAMIC_ARCHITECTURE_GATE: PASS|FAIL
ECONOMIC_GATE: PASS|FAIL
PROMOTION_RECOMMENDATION: PROMOTE|REJECT|ITERATE
```

Una media migliore non compensa un gate architetturale fallito. Reattività
dimostrata senza sicurezza o progresso economico non autorizza la promozione.
Non usare holdout o final confirmation e non preparare una submission Kaggle
senza nuova autorizzazione del proprietario.
