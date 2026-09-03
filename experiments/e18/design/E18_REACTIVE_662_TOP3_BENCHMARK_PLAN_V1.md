# E18 — piano benchmark Top 3 per una 6-6-2 realmente reattiva

## Obiettivo

E18 parte dalla candidata Kaggle E17 `CODEX-E17.3-TOPOLOGY-FILL-662-V2` e
mantiene invarianti la topologia `6-6-2`, il riempimento `14/14`, zero fughe e
la liquidazione terminale. La nuova linea pianificata è
`CODEX-E18.1-REACTIVE-662-V1`.

L'obiettivo non è modificare nuovamente il layout: è rendere osservabile e
causale la scelta di regime per mercato, servizio e capacità, misurandola
contro il profilo temporale e produttivo degli archetipi Top 3 selezionati.

## Confine dell'evidenza

I profili `tetsuya`, `OceanMix` e `Crop Dusta` provengono dai replay discovery
E17 già consumati. Sono training evidence e archetipi storici, non policy
callable e non una fotografia garantita della leaderboard corrente. Non
possono essere usati come holdout E18.

Il baseline E18 riusa inoltre il torneo development E17 da 84 match. Nessun
seed holdout o final-confirmation è consumato dall'apertura di E18.

## Benchmark di ingresso

| Dimensione | Top 3 osservati | 6-6-2 E17 | Gate E18 |
|---|---:|---:|---|
| Score/denaro | 82,5k–96,6k medi | 132,2k vs Claude; 79,3k self-play | ≥100k anche in contesa simmetrica |
| Q1 | D5–D7 | D6 medio | mantenere D5–D7 |
| Q2 | D8–D11 | D11 medio | mantenere D8–D11 senza layout statico cieco |
| Peak crop | 58–61 | 59,93 | ≥58 |
| Peak animali | 14,25–16,8 circa | 15 | 14–16, zero fughe |
| Movimento | OceanMix 48,99% active | 1,37 MOVE/produttive | non peggiorare e misurare entrambe le unità |
| Reattività | traiettorie diverse per archetipi | V3/V2 identici 28/28 | divergenza causale tracciata |

Le scale `mean_move_share_active_pct` dei replay e `MOVE/produttive` del runner
locale non sono intercambiabili. E18 deve calcolare entrambe nello stesso
ledger prima di dichiarare parità logistica con i Top 3.

## Singola famiglia causale autorizzata

`OBSERVABLE_MARKET_AND_SERVICE_REGIME_SELECTION_WITH_662_INVARIANTS`

La prima candidata può cambiare esclusivamente:

1. classificazione online del regime (`growth`, `service_pressure`,
   `market_contention`, `liquidation`);
2. quantità/timing degli ordini animali e semi in risposta al regime;
3. priorità dei worker liberati verso weed, harvest e drop;
4. handoff anticipato state-driven soltanto se capacità e backlog lo
   giustificano.

Non può cambiare nello stesso round: coordinate dei 14 pascoli, cap Q2,
target animali, crop mix strutturale o protocollo dei seed.

## Telemetria obbligatoria prima del benchmark economico

- `regime_transitions` con giorno/step e feature causali;
- `guard_activations`;
- `animal_orders_seen` e `orders_throttled`;
- `animal_units_suppressed`;
- backlog weed/service al momento dell'override;
- hash dell'action stream per scenario;
- invarianti 14/14, Q2 ≤2, zero fughe, residuo terminale zero.

Una candidata che non diverge dal controllo in almeno uno scenario forzato
non è ammessa al torneo economico, anche se i test tecnici passano.

## Sequenza sperimentale

1. **Activation fixtures:** stati controllati per ciascun regime, senza match.
2. **2-seed smoke:** nuovo seed set E18, seat speculari, controllo V2.
3. **4-seed expansion:** solo se action stream e contatori provano
   l'attivazione prevista.
4. **7-seed development:** gate economico, self-play e archetipi controllati.
5. **Holdout:** richiede decisione esplicita del proprietario; non autorizzato
   da questo piano.

## Gate di promozione development

- delta medio matched >0 e nessun seed con regressione >5%;
- media self-play/forte contesa ≥100.000;
- minimo development ≥80.000;
- 14/14 e Q2 ≤2 in tutte le run;
- zero fughe, errori, fallback e residui terminali;
- almeno una divergenza causale prevista per ogni regime testato;
- nessuna dipendenza da replay o metriche post-action nel decision path.

Se la leva non supera prima l'activation gate, E18 conserva la V2 senza
creare una nuova submission nominalmente diversa ma comportamentalmente
identica.
