# E17.2 — sviluppo Codex `REACTIVE_SERVICE_AND_ROUTING`

- **Data:** 2026-09-02
- **Ruolo dell'evidenza:** `DEVELOPMENT_ONLY`
- **Candidata:** `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V2`
- **Controllo:** `CODEX-E17.1-TRUE-REACTIVE-V2`
- **Avversario:** `INERT_PASS_POLICY`
- **Holdout/final confirmation:** non usati
- **Verdetto:** `DEVELOPMENT_GATES_PASS / PROGRESSIVE_HANDOFF_ONLY / NOT_KAGGLE_READY`

## 1. Risultato

È stato realizzato un dispatcher che ricostruisce i comandi delle unità dallo
snapshot Foundation invece di assumere coordinate derivate dallo step. Il
passaggio al core è stato reso progressivo: la V2 commerciale e la routine 3Q
operano fino al giorno 28; dal giorno 29 il core prende in carico le unità e
genera task terminali di raccolta e consegna allo shed. Il blocco `market`
resta esattamente quello proposto dalla V2.

Il benchmark finale comprende 12 episodi:

```text
3 seed development × 2 seat × 2 policy
```

| Indicatore | Core V2 | Controllo | Delta |
|---|---:|---:|---:|
| Reward medio | 131.947,17 | 134.060,17 | −2.113,00 |
| Delta percentuale | — | — | −1,576% |
| Peggior delta matched | — | — | −2.517 |
| Animali finali medi | 19,00 | 19,00 | 0 |
| Crop finali medi | 12,83 | 13,83 | −1,00 |
| Fughe EOD strette | 0 | 0 | 0 |
| Perdite crop EOD derivate | 83 | 83 | 0 |

La candidata supera il gate `INERT_REGRESSION >= -5%`. Non migliora ancora il
controllo e non viene proposta per Kaggle.

## 2. Perché non è un semplice override

Tre varianti iniziali cercavano di aggiungere routing alla sequenza V9:

- recupero aggressivo di `PASS` e comandi non fattibili: reward `8.497`;
- sole deadline biologiche senza rientro: `46.670`;
- detour con rientro durante finestre `PASS`: `123.858`.

Con il solo servizio critico il risultato sale a `176.990`; proiettando i
servizi già coperti dalla routine torna a `183.102`, ma senza deviazioni
naturali. L'evidenza mostra che le coordinate della routine formano un
contratto implicito: una deviazione di posizione rende fragili i comandi
successivi anche quando il worker rientra apparentemente in tempo.

La conseguenza è importante per l'architettura: un router vero deve possedere
l'intera coda delle unità nella finestra in cui è attivo. Non può essere una
collezione di correzioni locali applicate sopra uno schedule posizionale.

## 3. Frontiera di attivazione

È stato quindi creato un core state-driven capace di rappresentare:

- WATER normale e critico;
- FEED critico con staging Wheat dallo shed;
- HARVEST, CARE e consegna inventario;
- BUILD/PLACE/PICKUP/DIG/PLANT rispetto alla topologia target 3Q;
- assegnazione worker-task per priorità, distanza e continuità del task.

L'attivazione dal giorno 0 fallisce perché il provider commerciale spende
capitale assumendo la produttività del bootstrap V9, mentre il nuovo planner
non è ancora calibrato per generarla. Per separare bootstrap e servicing è
stata misurata questa frontiera sul seed development `26090101`:

| Handoff | Reward | Animali finali | Nota |
|---:|---:|---:|---|
| D20 | 90.924 | 19 | core funzionale, logistica costosa |
| D22 | 111.398 | 20 | — |
| D24 | 128.436 | 20 | — |
| D26 | 147.298 | 19 | — |
| D28 | 164.906 | 20 | −9,94% |
| D29 | 180.585 | 19 | −1,37% |

Questa ricerca usa un seed development già consumato: è selezione di soglia,
non prova indipendente. Il benchmark finale resta interamente development e
non autorizza generalizzazione.

## 4. Ledger requested/executed

Nella finestra reattiva sono stati registrati tutti i 1.434 comandi unità,
inclusi i `PASS`:

| Outcome | Numero | Quota |
|---|---:|---:|
| `EXECUTED` | 990 | 69,04% |
| `NOT_EXECUTED` | 0 | 0% |
| `UNKNOWN` | 444 | 30,96% |

Gli `UNKNOWN` sono 432 `PASS`, privi per definizione di una mutazione
osservabile, e 12 comandi dell'ultimo batch, per cui l'engine non richiama la
policy sullo stato terminale successivo. Non sono stati imputati come
eseguiti. La copertura di classificazione è 100%.

Il core ha emesso complessivamente:

- 750 mosse cardinali;
- 180 `HARVEST`;
- 72 `DROP`;
- 432 `PASS`;
- 252 servizi non-move, con `MOVE/service = 2,976`.

Ogni episodio produce 125 mosse e 42 servizi nella finestra D29. Non risultano
forme d'azione invalide, fallback o errori tecnici.

## 5. Collegamento alla Foundation

Il core usa soltanto lo snapshot normalizzato da
`src/agricola/core/observation_contract.py`:

- clock `step/day/hour` per attivazione e terminalità;
- `farm.tiles`, posizioni e quadranti per task e distanza;
- `private.shed`, `private.inventories` e `private.seeds` per precondizioni;
- stato di crop/animali (`yield_units`, water/feed debt, flag giornalieri) per
  distinguere task fattibili e urgenti.

La state machine Foundation resta descrittiva: il dispatcher non introduce
un `decision_lifecycle` condiviso. Priorità, matching, sticky assignment e
topologia sono decisioni locali Codex. Il ledger resta fuori dal decision
path e separa sempre comando richiesto da esito osservato.

## 6. Lettura economica

Il delta medio `−2.113` coincide con un crop finale in meno per episodio,
mentre fughe e perdite crop EOD sono identiche al controllo. L'inferenza più
plausibile è un disallineamento terminale: il core raccoglie un output in più,
ma non possiede ancora una liquidazione market coordinata che ne garantisca la
vendita entro l'ultimo step. Questa è un'ipotesi causale da testare, non un
esito verificato ordine per ordine.

## 7. Gate e decisione

| Gate | Esito |
|---|---|
| errori tecnici/fallback | PASS — 0/0 |
| forme d'azione invalide | PASS — 0 |
| mutazioni market | PASS — 0 |
| ledger classificato | PASS — 100% |
| fughe animali | PASS — 0 |
| regressione inerte almeno −5% | PASS — −1,576% |
| routing naturale | PASS — 750 |
| servizi naturali | PASS — 252 |
| determinismo stesso stato iniziale | PASS — test mirato |
| holdout/final confirmation intatti | PASS |

La V2 è conservata come **architettura di sviluppo**, non come submission. Il
prossimo incremento deve spostare l'handoff da D29 a D28 senza superare −5%,
riducendo `MOVE/service` e coordinando raccolta→shed→vendita. Solo dopo si
anticiperà un giorno per volta; WATER/FEED e infine acquisition/placement
diventeranno operativi quando la finestra corrispondente supera gli stessi
gate.

## 8. Artefatti

- piano: `docs/model_specs/codex/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V1.md`;
- overlay V1 diagnostico: `src/agricola/strategy/codex/codex_e17_reactive_service_routing.py`;
- core V2: `src/agricola/strategy/codex/codex_e17_reactive_service_routing_core.py`;
- config V2: `docs/model_specs/codex/e17/configs/CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V2.json`;
- runner: `docs/model_specs/codex/e17/tools/run_codex_e17_service_routing_development.py`;
- test: `docs/model_specs/codex/e17/tests/test_codex_e17_reactive_service_routing_core.py`;
- metriche: `docs/model_specs/codex/e17/artifacts/derived/E17_2_REACTIVE_SERVICE_ROUTING_DEVELOPMENT_METRICS.json`.
