# E17.2 — piano causale `BATCHED_CLUSTER_ROUTING_V4_D28`

- **Data:** 2026-09-02
- **Stato:** `EXECUTED / V4D ALL DEVELOPMENT GATES PASS`
- **Controllo:** `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28`
- **Candidata A:** `CODEX-E17.2-BATCHED-ROUTING-V4A-D28`
- **Candidata B:** `CODEX-E17.2-CLUSTERED-ROUTING-V4B-D28`
- **Evidenza ammessa:** soli seed development già consumati
- **Holdout/final confirmation:** vietati

## 1. Diagnosi engine

L'inventario di ciascun worker non ha una capacità massima configurata.
Imporre una soglia numerica di riempimento introdurrebbe quindi un vincolo
estraneo all'engine. Lo shed ha invece capacità finita e, a fine giornata,
l'engine deposita automaticamente gli inventari dei worker prima di rimuovere
gli assistenti e riportare il farmer allo spawn.

Il rapporto V3 `MOVE/service = 3,000` è coerente con due inefficienze:

1. in D28 ogni inventario positivo genera subito un rientro, benché il
   deposito EOD sia automatico;
2. in D29 DROP ha precedenza su un ulteriore HARVEST ancora compatibile con il
   tempo necessario per tornare allo shed e depositare.

## 2. Ablation A — batching inventory/deadline

La V4A modifica esclusivamente il gate di rientro:

- D28: nessun DROP esplicito; gli inventari restano ai worker fino al deposito
  automatico EOD;
- D29: se un worker porta output vendibile, HARVEST resta prioritario finché
  esiste un task fattibile con percorso completo
  `posizione→target→shed→DROP` entro gli step residui;
- quando nessun ulteriore HARVEST è fattibile, il DROP torna prioritario;
- il market coordinato V3 resta invariato e continua a includere i DROP dello
  stesso batch.

Non vengono introdotte soglie di quantità: il trigger inventory è
semplicemente `sellable_units > 0`, conforme al contratto reale dell'engine.

## 3. Ablation B — affinità di cluster

La V4B applica tutto il trattamento V4A e aggiunge soltanto una penalità
deterministica al cambio di quadrante per lo stesso worker. Priorità biologica,
fattibilità terminale e valore economico prevalgono sempre sulla penalità.

I cluster sono i quattro quadranti geometrici 5×5 della board. L'affinità è
memoria operativa agent-local e viene aggiornata dall'ultimo task assegnato;
non modifica la Foundation né introduce una deliberazione condivisa.

## 4. Invarianti

Restano invariati rispetto alla V3:

- handoff D28 e liquidazione D29;
- provider di bootstrap, HIRE, acquisti, unlock e topologia;
- composizione Q0/Q1/Q2 come outcome;
- task FEED, WATER e HARVEST generati dallo snapshot;
- preservazione integrale degli ordini non-SELL;
- limite di dieci ordini market e liquidazione same-batch;
- ledger requested/executed fuori dal decision path.

## 5. Matrice

```text
3 seed development × 2 seat × (V4A, V4B, V3) = 18 episodi
```

Avversario: `INERT_PASS_POLICY`. Nessun seed può essere escluso dopo
l'esecuzione.

## 6. Gate

Gate comuni V4A/V4B:

```text
TECHNICAL_ERRORS == 0
INVALID_ACTION_SHAPES == 0
ANIMAL_ESCAPES == 0
UNIT_LEDGER_CLASSIFICATION_COVERAGE == 1.0
MARKET_LEDGER_CLASSIFICATION_COVERAGE == 1.0
NON_SELL_PROVIDER_ORDERS_PRESERVED == true
ACTIVATION_DAY == 28
TERMINAL_SELLABLE_RESIDUAL == 0
HOLDOUT_USED == false
FINAL_CONFIRMATION_USED == false
```

Gate causali V4A:

```text
BATCHED_HARVEST_ASSIGNMENTS > 0
D28_EXPLICIT_DROP_COUNT == 0
MOVE_PER_SERVICE < V3_MOVE_PER_SERVICE
MEAN_REWARD_DELTA_VS_V3 >= 0
```

Gate incrementali V4B:

```text
CLUSTER_STICKY_ASSIGNMENTS > 0
CLUSTER_SWITCH_RATE <= V4A_CLUSTER_SWITCH_RATE
MOVE_PER_SERVICE <= V4A_MOVE_PER_SERVICE
MEAN_REWARD_DELTA_VS_V4A >= -0.5%
```

Se V4A fallisce, il batching non viene promosso. Se V4A passa ma V4B fallisce,
si promuove soltanto V4A. Un PASS resta development-only e non autorizza
holdout, submission Kaggle o modifica del MODEL_SPEC.

## 7. Esito V4A/V4B e preregistrazione V4C

La matrice è stata eseguita integralmente. V4A riduce `MOVE/service` da 3,000
a 2,676 ma perde il `2,529%` di reward rispetto alla V3; V4B modifica il
reward di appena `+0,001%` rispetto a V4A e porta `MOVE/service` a 2,682.
Entrambe falliscono i gate e non sono promosse.

Il replay diagnostico sul seed development già consumato `26090101` isola la
causa: prima dell'EOD D28 V4A porta 98 unità nei worker con 41 unità nello
shed. Il deposito automatico può conservarne soltanto 59 e scarta l'overflow.
La V3 arriva invece a 51+43=94 unità e non satura lo shed.

Prima di un nuovo benchmark viene quindi preregistrata V4C, che aggiunge alla
sola V4A un flush guidato dalla pressione di capacità:

```text
PRESSURE = shed_units + droppable_worker_units
TRIGGER = PRESSURE >= 85% della capacità shed
TARGET_AFTER_SELL = 50% della capacità shed
```

Quando il trigger scatta in D28, il rientro viene mantenuto con isteresi fino
al deposito. Durante l'avvicinamento la vendita coordinata crea spazio nello
shed prima del DROP, perché l'engine applica le unit action prima del market
nel medesimo batch. Gli output dei carrier Wheat restano esclusi dal flush per
non compromettere FEED.

La V4C è confrontata direttamente con V3 sulla matrice 3 seed × 2 seat × 2
policy. Oltre ai gate comuni deve soddisfare:

```text
CAPACITY_FLUSH_TRIGGER_EVENTS > 0
D28_EXPLICIT_DROP_COUNT > 0
MOVE_PER_SERVICE < V3_MOVE_PER_SERVICE
MEAN_REWARD_DELTA_VS_V3 >= 0
TERMINAL_SELLABLE_RESIDUAL == 0
```

Le soglie 85/50 sono congelate prima della matrice V4C. Il seed diagnostico
non costituisce validazione indipendente e resta dichiarato come tuning.

## 8. Esito V4C e preregistrazione V4D

V4C riproduce esattamente V4A: il trigger scatta sei volte, ma non si attiva
alcun batch di flush e non viene eseguito alcun DROP D28. Tutti i worker con
output portano anche Wheat; l'esclusione assoluta dei carrier impedisce quindi
al meccanismo di operare. V4C fallisce i gate e non è promossa.

V4D corregge esclusivamente l'ambito temporale della protezione Wheat:

- finché esiste almeno un animale `fed_today == false`, i carrier Wheat
  restano esclusi come in V4C;
- dopo che tutti gli animali risultano alimentati nello snapshot D28, il Wheat
  non ha più un impiego biologico nel giorno e i carrier possono partecipare
  al flush di capacità;
- trigger 85%, target 50%, batching terminale e ogni altra regola restano
  invariati.

V4D usa la stessa matrice matched 3 seed × 2 seat contro V3 e gli stessi gate
di V4C, con l'ulteriore requisito:

```text
POST_FEED_WHEAT_CARRIER_RELEASES > 0
```

La modifica è preregistrata prima della matrice V4D. Anche questo confronto è
development-only.

## 9. Esito V4D

La matrice V4D è stata completata senza esclusioni:

- media V4D `135.096,83`, V3 `134.351,33`;
- delta medio `+745,50` (`+0,555%`), minimo matched `+497`;
- `MOVE/service` da 3,000 a 2,872;
- 72 DROP espliciti D28, 161 HARVEST eseguiti con inventario già positivo;
- 12 eventi di trigger, 36 batch di flush e 251 decisioni worker-callback di
  rilascio post-feed dei carrier Wheat;
- ledger unità `3198/3198`, ledger market `71/71`;
- zero errori, fallback, forme invalide, fughe, residui terminali e violazioni
  degli ordini non-SELL.

Tutti i gate V4D passano. V4D sostituisce V3 come candidata interna
development. Non è una submission e non è stata esposta a holdout o final
confirmation. Prima di anticipare l'handoff a D27 deve essere sottoposta a
stress development con regimi di mercato controllati.
