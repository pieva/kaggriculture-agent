# E17.3 — Torneo development Codex / Claude / Copilot

- **Data:** 2026-09-03
- **Esito:** COMPLETE — 42/42 match
- **Ruolo epistemico:** DEVELOPMENT ONLY / NON QUALIFYING
- **Seed:** 7/7 development, entrambi i seat
- **Holdout/final confirmation:** non consumati
- **Antigravity:** escluso su richiesta del proprietario fino al 2026-09-04

## Partecipanti

| ID | Policy as-built | Stato di ingresso |
|---|---|---|
| `CODEX_662` | `CODEX-E17.3-TOPOLOGY-FILL-662-V2` | candidata Kaggle corrente |
| `CLAUDE_V3` | `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3` | freeze con gate economici/sicurezza falliti |
| `COPILOT_NATIVE` | `COPILOT-E17.0-NATIVE-3Q-CROP-BASELINE-V1` | freeze E17.0 PASS |

Claude V4 non è stata ammessa: lo spot-check development già registrato è
negativo (`-8,9%` vs V3). Per Copilot è stata usata la policy E17.0 nativa,
non la precedente V2 derivativa dalla routine Codex.

## Classifica

| Agente | W-L-T | Denaro medio | Mediana | Min–max | Seat 0–1 |
|---|---:|---:|---:|---:|---:|
| **Codex 6-6-2** | **28-0-0** | **123.620,29** | 123.308,00 | 87.792–156.129 | −2.412,71 |
| **Claude V3** | **14-14-0** | **15.511,21** | 14.700,50 | 7.861–27.616 | +682,57 |
| **Copilot native** | **0-28-0** | **10.537,18** | 9.566,50 | 8.158–14.574 | +153,64 |

Il ranking è identico in ogni seed e orientamento. I testa-a-testa sono:

| Pair | Risultato | Delta medio del vincitore |
|---|---:|---:|
| Codex vs Claude | 14-0 | +118.612,93 |
| Codex vs Copilot | 14-0 | +102.993,57 |
| Claude vs Copilot | 14-0 | +9.196,57 |

## Diagnostica comune

| KPI medio per run | Codex 6-6-2 | Claude V3 | Copilot native |
|---|---:|---:|---:|
| Q1 / Q2 activation day | 6,00 / 11,00 | 2,00 / 11,21 | 0,00 / 5,00 |
| Peak hands | 12,00 | 11,79 | 5,00 |
| Peak crop | **59,93** | 30,64 | 51,50 |
| Peak animali | **15,00** | 4,82 | 0,00 |
| MOVE | 3.591,71 | 4.321,32 | **2.287,89** |
| Azioni produttive | **2.617,89** | 1.155,82 | 1.875,11 |
| MOVE/produttive | 1,372 | 3,754 | **1,221** |
| Peak weed | 14,14 | 7,29 | 33,89 |
| Fughe EOD derivate | **0** | **57** | 0 (crop-only) |
| Errori / fallback | 0 / 0 | 0 / 0 | 0 / 0 |

## Codex 6-6-2

### Punti di forza osservati

- Vince 28/28 con il denaro, la densità crop e il throughput produttivo più
  alti.
- In tutte le 28 run costruisce e riempie `14/14` pascoli: `6-6-2`, nessun
  pascolo target vuoto, cinque celle recuperate a crop e zero breach Q2.
- Mantiene 15 animali di picco, zero fughe, zero errori e zero fallback.
- L'efficienza logistica (`1,372` MOVE/produttive) è molto migliore di Claude,
  pur usando il doppio della forza lavoro di Copilot.

### Miglioramenti prioritari

1. La macro-topologia resta fissa. Il controllo è reattivo su riempimento e
   servizio, ma non sceglie ancora fra `6-6-0`, `6-6-2` o un'altra struttura in
   base a mercato, contesa e capacità osservata.
2. Lo score ha dispersione elevata (`σ=22.070,83`, minimo `87.792`) e cala a
   `115.434,86` contro Copilot rispetto a `131.805,71` contro Claude: la
   pressione crop/market dell'avversario va trattata come regime osservabile.
3. Restano in media `877,43` PASS e un picco weed di `14,14`: prioritizzare
   recupero weed e riuso dei worker idle senza rompere la sincronizzazione V4D.
4. Ridurre la dipendenza dalla routine open-loop con un handoff state-driven
   graduale, mantenendo come invarianti 14/14, zero fughe e liquidazione.

## Claude V3

### Punti di forza osservati

- Batte Copilot in 14/14, raggiunge 3Q in 28/28 ed è tecnicamente stabile.
- Scala a quasi dodici hands e usa un dispatcher realmente state-driven con
  assegnazioni persistenti.
- Il vantaggio su Copilot è positivo in ogni seed/seat, non dipende da un solo
  outlier.

### Miglioramenti prioritari

1. Il collo di bottiglia principale è logistico: `4.321` MOVE/run e
   `3,754` MOVE/produttive. Introdurre cluster per quadrante, continuità di
   target e riassegnazione anti-collisione prima di aumentare la superficie.
2. Ridurre bestiame alla capacità realmente servibile: 57 fughe, solo 4,32
   animali terminali medi e 3,68 strutture zootecniche vuote.
3. Q1 a D2 è prematuro rispetto al throughput: legare BUY_LAND a densità,
   cassa post-acquisto e backlog di servizio, non al solo raggiungimento di una
   soglia locale.
4. Aggiungere una catena terminale HARVEST→DROP→SELL e dare precedenza a
   FEED/CARE prima dell'espansione. Il picco crop è circa metà di Codex.
5. Non riproporre da sola la leva V4 Q2-livestock: prima va risolta la capacità
   di movimento e servizio dimostrata insufficiente nello spot-check.

## Copilot native

### Punti di forza osservati

- È la policy più semplice e logisticamente efficiente: `1,221`
  MOVE/produttive, quasi nessun PASS e seat delta di soli `154`.
- Raggiunge 3Q in 28/28, arriva a 51,5 crop di picco ed è completamente
  state-driven, table-free e tecnicamente stabile.
- L'assenza di zootecnia elimina una famiglia di failure, ma lo zero fughe non
  è confrontabile con Codex e Claude.

### Miglioramenti prioritari

1. L'espansione è troppo precoce (`Q1 D0`, `Q2 D5`) per cinque hands: usare
   density/cash/backlog gates e reinvestire prima nel workforce.
2. Il picco weed di `33,89` mostra che copertura non equivale a servizio:
   aggiungere priorità weed, scadenze e riassegnazione dopo comandi non
   eseguiti.
3. Raccogliere quando il tile produce, non attendere solo la cadence fissa;
   introdurre acknowledgement/deduplica degli ordini market.
4. Dopo il risanamento crop-only, testare separatamente diversificazione crop
   e un piccolo modulo mixed-farming con cap di servizio, senza importare
   routine altrui.
5. Aggiungere MODEL_SPEC E17 nativa e correggere l'export del package, che oggi
   espone ancora la vecchia candidata V2 derivativa.

## Decisione

Codex 6-6-2 resta l'unica candidata Kaggle del round. Il torneo non autorizza
la promozione di Claude o Copilot e non consuma evidenza riservata. Le capacità
da trasferire come idee, non come codice, sono:

- da Claude: dispatch state-driven e assegnazioni persistenti;
- da Copilot: semplicità, bilanciamento crop e basso MOVE/produttive;
- da Codex: controllo di capacità, densità mista e invarianti di sicurezza.

Il prossimo round deve essere un'ablation development per ciascun agente,
senza combinare leve: market-regime/topology choice per Codex, routing e cap
zootecnico per Claude, workforce/weed/harvest cadence per Copilot.

## Provenance

- JSON completo: `experiments/e17/artifacts/derived/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.json`
- CSV: `experiments/e17/artifacts/derived/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.csv`
- Protocollo: `experiments/e17/design/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2.md`
- Runner: `experiments/e17/tools/common/run_e17_three_agent_development_tournament_v2.py`
