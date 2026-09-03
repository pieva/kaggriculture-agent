# E17.2 — Codex service-routing V3 con handoff D28

- **Data:** 2026-09-02
- **Ruolo dell'evidenza:** `DEVELOPMENT_ONLY`
- **Candidata:** `CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28`
- **Controllo:** `CODEX-E17.1-TRUE-REACTIVE-V2`
- **Avversario:** `INERT_PASS_POLICY`
- **Holdout/final confirmation:** non usati
- **Verdetto:** `ALL_DEVELOPMENT_GATES_PASS / INTERNAL_CANDIDATE / NOT_KAGGLE_RELEASED`

## 1. Risultato

La V3 anticipa dal giorno 29 al giorno 28 l'handoff completo delle unità al
dispatcher state-driven. A differenza della V2, prepara l'ultimo ciclo
produttivo con FEED e WATER normali, deposita gli output anche in D28 e al
giorno 29 coordina DROP e SELL nello stesso batch. Acquisti, HIRE, unlock,
topologia e quantità zootecniche restano sotto il provider congelato.

La matrice finale comprende tre seed development, entrambi i seat e controllo
matched: 12 episodi totali.

| Indicatore | V3 D28 | Controllo | Delta |
|---|---:|---:|---:|
| Reward medio | **134.351,33** | 134.060,17 | **+291,17** |
| Delta percentuale | — | — | **+0,217%** |
| Peggior delta matched | — | — | −122 |
| Animali finali medi | 19,00 | 19,00 | 0 |
| Crop finali medi | 24,50 | 13,83 | +10,67 |
| Perdite crop EOD derivate | 77 | 83 | −6 |
| Fughe EOD strette | 0 | 0 | 0 |
| Output vendibile terminale residuo | **0** | 54 | −54 |

Risultati matched:

| Seed | Seat | V3 | Controllo | Delta |
|---:|---:|---:|---:|---:|
| 26090101 | 0 | 183.784 | 183.102 | +682 |
| 26090101 | 1 | 183.784 | 183.102 | +682 |
| 26090102 | 0 | 122.757 | 122.879 | −122 |
| 26090102 | 1 | 122.757 | 122.879 | −122 |
| 26090103 | 0 | 78.436 | 78.333 | +103 |
| 26090103 | 1 | 114.590 | 114.066 | +524 |

Rispetto al core V2 D29, la media sale da `131.947,17` a `134.351,33`:
`+2.404,17`, pari a circa `+1,82%`, pur anticipando l'handoff di un giorno.

## 2. Causa verificata

L'engine applica prima le azioni delle unità e poi gli ordini market del
medesimo turno. Questo rende possibile una transazione causale completa:

```text
worker su accesso shed → DROP → prodotto nello shed → SELL nello stesso batch
```

La V2 manteneva byte-equivalente il market provider. Il provider osservava lo
stato precedente al DROP e non poteva richiedere la vendita del nuovo output.
Inoltre il dispatcher riservava ciascun accesso shed a una sola unità, mentre
l'engine consente più worker sulla stessa tile. Le due correzioni decisive
sono quindi:

- ordini SELL costruiti dallo shed osservato più i DROP fattibili del batch;
- rientri paralleli, senza esclusione artificiale dell'accesso allo shed.

Al giorno 28 il core deposita inoltre gli output non-Wheat in tempo per le
vendite già pianificate dal provider. Il Wheat trasportato resta protetto fino
al completamento del feed; non vengono introdotte nuove decisioni di acquisto.

## 3. Servizio biologico e routing

Nei sei episodi candidati sono stati emessi:

| Operazione | Numero |
|---|---:|
| MOVE | 2.256 |
| PICKUP Wheat | 24 |
| FEED | 114 |
| WATER | 78 |
| HARVEST | 331 |
| DROP | 205 |
| PASS | 190 |
| Servizi complessivi non-MOVE/non-PASS | 752 |

Tutti i 19 animali vengono alimentati in D28 in ciascun episodio. D29 non
genera FEED o WATER senza ritorno economico entro l'orizzonte. Un HARVEST
terminale parte soltanto se la distanza consente anche il rientro e il DROP;
fra task fattibili la priorità usa il valore osservato e il percorso residuo.

Il rapporto `MOVE/service` è `3,000`. È il principale limite rimasto: il core
è economicamente equivalente sul perimetro D28-D29, ma percorre ancora molti
tragitti singoli raccolta→shed.

## 4. Liquidazione e ledger market

La V3 ha prodotto 78 batch market coordinati, 94 ordini SELL incrementali e
238 unità incrementali richieste. Il risultato terminale è zero unità
vendibili nello shed o negli inventari delle unità in tutti i sei episodi.

| Outcome batch market | Numero |
|---|---:|
| `EXECUTED` | 72 |
| `NOT_EXECUTED` | 0 |
| `UNKNOWN` | 6 |

I sei `UNKNOWN` sono gli ultimi batch di ciascun episodio: l'engine termina
senza una successiva callback osservabile. Non sono imputati come eseguiti,
anche se lo stato terminale aggregato mostra residuo zero. Tutti gli ordini
non-SELL del provider sono preservati; le violazioni rilevate sono zero.

## 5. Ledger unità

| Outcome | Numero | Quota |
|---|---:|---:|
| `EXECUTED` | 2.917 | 91,21% |
| `NOT_EXECUTED` | 0 | 0% |
| `UNKNOWN` | 281 | 8,79% |

La copertura è `3198/3198`. Gli `UNKNOWN` comprendono PASS, ultimo batch e le
MOVE all'ultimo turno di D28: il reset EOD riporta i worker allo shed prima
dell'osservazione successiva, quindi l'esecuzione della MOVE non è
identificabile dalla posizione post-reset.

## 6. Collegamento alla Foundation

La policy usa il contratto osservativo C2.1 per clock, tile, posizioni,
inventari, shed, stato biologico e prezzi. Le regole strategiche rimangono
locali Codex:

- task queue ricostruita a ogni callback;
- priorità FEED/WATER/HARVEST/DROP;
- matching distanza-valore;
- deadline terminale e previsione del deposito nello stesso batch.

La state machine Foundation descrive i vincoli biologici e temporali, ma non
impone il planner. Non viene reintrodotto `decision_lifecycle`. I due ledger
restano fuori dal decision path e distinguono comando richiesto ed esito
osservabile.

## 7. Gate e decisione

Tutti i gate preregistrati passano:

- zero errori, fallback e forme invalide;
- zero fughe;
- copertura ledger unità e market 100%;
- ordini non-SELL preservati al 100%;
- FEED, WATER, DROP e SELL coordinati presenti naturalmente;
- handoff effettivo D28;
- delta medio `+0,217%`, superiore alla soglia `−5%`;
- determinismo coperto da test mirato;
- holdout e final-confirmation intatti.

La V3 è congelata come nuova candidata interna development. Non viene
preparata o caricata alcuna submission. Il prossimo trattamento deve restare
su D28 e ridurre `MOVE/service` tramite raccolte raggruppate e una soglia di
rientro basata su inventario e slack terminale. Solo dopo aver mantenuto
score, residuo zero e sicurezza si potrà provare l'handoff D27.

## 8. Artefatti

- piano: `experiments/e17/design/E17_CODEX_REACTIVE_SERVICE_AND_ROUTING_PLAN_V2.md`;
- policy: `src/agricola/strategy/codex/codex_e17_reactive_service_routing_v3.py`;
- config: `experiments/e17/configs/codex/CODEX_E17_2_REACTIVE_SERVICE_ROUTING_CORE_V3_D28.json`;
- test: `experiments/e17/tests/test_codex_e17_reactive_service_routing_v3.py`;
- runner: `experiments/e17/tools/codex/run_codex_e17_service_routing_v3_development.py`;
- metriche: `experiments/e17/artifacts/derived/codex/E17_2_REACTIVE_SERVICE_ROUTING_V3_D28_DEVELOPMENT_METRICS.json`.
