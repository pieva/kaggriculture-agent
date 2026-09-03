# E17.2 — piano causale `SERVICE_ROUTING_CORE_V3_D28`

- **Data:** 2026-09-02
- **Stato:** `EXECUTED / ALL DEVELOPMENT GATES PASS / NOT KAGGLE RELEASED`
- **Candidata:** `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28`
- **Controllo primario:** `CODEX-E17.1-TRUE-REACTIVE-V2`
- **Controllo architetturale:** Core V2 con handoff D29
- **Evidenza ammessa:** soli seed development già consumati
- **Holdout/final confirmation:** vietati

## 1. Ipotesi

La regressione del core con handoff D28 dipende da due omissioni osservabili:

1. al giorno 28 il planner serviva soltanto animali già critici, quindi non
   preparava tutta la produzione zootecnica disponibile al giorno 29;
2. al giorno 29 il market provider non può conoscere gli output che verranno
   depositati dalle unità nello stesso batch, benché l'engine applichi prima
   le azioni unità e poi gli ordini market.

Un dispatcher che alimenta e irriga per l'ultimo ciclo produttivo e che
liquida nello stesso turno gli inventari depositati dovrebbe permettere
l'handoff D28 senza mutare bootstrap, unlock, topologia o quota Q2.

## 2. Trattamento ammesso

Dal giorno 28 la candidata prende in carico l'intera coda unità e può:

- raccogliere output maturi;
- prelevare Wheat dallo shed e alimentare tutti gli animali ancora non serviti
  in D28;
- irrigare le colture non servite in D28;
- raccogliere fertilizzante disponibile soltanto dopo feed/harvest prioritari;
- portare allo shed gli inventari vendibili;
- dal giorno 29 consolidare o aggiungere ordini `SELL` per prodotti già nello
  shed o depositati nello stesso batch.

Restano vietati nel decision path del core:

- nuove scelte HIRE, BUY_LAND, BUY_ANIMAL, BUY_SEED o BUY_PRODUCT;
- BUILD, PLACE, DIG e PLANT dopo l'handoff D28;
- soglie o target diretti per Q0/Q1/Q2;
- rimozione o modifica degli ordini non-SELL proposti dal provider.

Il liquidatore può modificare soltanto quantità/ordini `SELL` di `WHEAT`,
`CARROT`, `TOMATO`, `STRAWBERRY`, `MELON`, `EGG`, `MILK`, `WOOL` e
`FERTILIZER`, nel limite engine di dieci ordini per turno.

## 3. Ordine di servizio

```text
CRITICAL_FEED / PICKUP_WHEAT / DROP_INVENTORY
FEED / CRITICAL_WATER
HARVEST
WATER
COLLECT_FERTILIZER
PASS
```

Il giorno 29 è terminale: FEED, WATER e COLLECT_FERTILIZER non vengono più
generati; restano HARVEST, DROP e vendita coordinata.

## 4. Confronto

Matrice finale prevista:

```text
3 seed development × 2 seat × candidata/controllo = 12 episodi
```

L'avversario è `INERT_PASS_POLICY`, identico al benchmark V2. Nessun seed può
essere escluso dopo l'esecuzione. Le esplorazioni di implementazione sul seed
`26090101` restano tuning e saranno indicate separatamente.

## 5. Metriche

- reward e delta matched rispetto al controllo;
- reward rispetto al core D29 e alla precedente frontiera D28;
- MOVE, FEED, WATER, HARVEST, DROP, COLLECT_FERTILIZER;
- `MOVE/service` e task completati;
- quantità richiesta e quantità eseguita/stimata delle vendite coordinate;
- output nei worker, output depositato e output residuo terminale;
- ledger unità e ledger market `EXECUTED / NOT_EXECUTED / UNKNOWN`;
- fughe, perdite crop, animali/crop finali, workforce e unlock come outcome.

## 6. Gate preregistrati

```text
TECHNICAL_ERRORS == 0
INVALID_ACTION_SHAPES == 0
ANIMAL_ESCAPES == 0
UNIT_LEDGER_CLASSIFICATION_COVERAGE == 1.0
MARKET_LEDGER_CLASSIFICATION_COVERAGE == 1.0
NON_SELL_PROVIDER_ORDERS_PRESERVED == true
ACTIVATION_DAY == 28
NATURAL_FEED_COUNT > 0
NATURAL_WATER_COUNT > 0
NATURAL_DROP_COUNT > 0
COORDINATED_SELL_COUNT > 0
INERT_MEAN_DELTA_VS_TRUE_REACTIVE_V2 >= -5%
SAME_INITIAL_STATE_DETERMINISM == PASS
HOLDOUT_USED == false
FINAL_CONFIRMATION_USED == false
```

Il PASS qualifica soltanto la V3 come candidata development. Non autorizza
submission Kaggle, holdout o promozione del MODEL_SPEC.

## 7. Amendement di implementazione tracciato

Gli smoke test sul seed development `26090101` hanno introdotto due correzioni
interne al trattamento preregistrato:

1. i task `DROP_INVENTORY` non riservano in esclusiva un accesso allo shed:
   l'engine permette la co-occupazione e la serializzazione lasciava unità con
   output invenduti;
2. al giorno 29 un HARVEST viene assegnato soltanto se restano azioni
   sufficienti per raggiungere il target, raccogliere, tornare allo shed e
   depositare. Fra i task fattibili viene privilegiato il valore corrente per
   unità di percorso.

Il ledger è stato inoltre corretto senza cambiare il decision path: una MOVE
emessa all'ultimo turno di D28 è `UNKNOWN`, non `NOT_EXECUTED`, perché il reset
EOD della posizione avviene prima dell'osservazione successiva.

Frontiera diagnostica sul seed di tuning:

| Variante | Reward |
|---|---:|
| precedente core con handoff D28 | 164.906 |
| V3 + feed/water + liquidazione | 176.020 |
| filtro deadline terminale | 176.594 |
| rientri paralleli | 177.672 |
| DROP D28 per rendere eseguibili le vendite programmate | 181.261 |
| priorità di valore terminale | 181.889 |
| rientri D28 paralleli per worker | **183.784** |
| controllo matched | 183.102 |

Questa sequenza è tuning, non validazione indipendente.

## 8. Esito della matrice development

La matrice finale preregistrata di 12 episodi produce:

- candidata `134.351,33`, controllo `134.060,17`;
- delta medio `+291,17` (`+0,217%`), minimo matched `−122`;
- 2.256 MOVE e 752 servizi, `MOVE/service = 3,000`;
- 114 FEED, 78 WATER, 331 HARVEST, 205 DROP e 24 PICKUP;
- 78 batch market coordinati, 94 ordini incrementali e 238 unità richieste;
- ledger unità `3198/3198` classificato: 2.917 `EXECUTED`, 281 `UNKNOWN`;
- ledger market `78/78`: 72 `EXECUTED`, 6 `UNKNOWN` terminali;
- zero errori, fallback, forme invalide, fughe e violazioni degli ordini
  non-SELL;
- zero unità vendibili terminali residue, contro 54 del controllo.

Tutti i gate passano. La V3 diventa candidata interna congelata per il
prossimo incremento, ma non è una submission. Prima di anticipare a D27 si
deve ridurre il costo logistico con raccolte raggruppate e soglie di rientro
inventory/deadline.
