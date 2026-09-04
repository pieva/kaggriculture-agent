# MODEL_SPEC — Claude E17.1 3Q Reactive Independent V5

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V5`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-03
- **Foundation:** C2.1 (RECONCILED)
- **Stato:** AS-BUILT — ablation pre-benchmark (Sezione 1.1) ha scartato la
  leva #2 (cap zootecnico) dal default per interazione negativa severa con
  la #1; V5 spedisce con la sola leva #1 (clustering). Matrice completa a
  7 seed eseguita: `+3,31%` di denaro medio vs V3, `28/28` match senza
  collassi né errori (Sezione 4)
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
  (`FROZEN_WITH_FAILED_GATES`; V4 — leva topologica SW/Q2 — è stata
  testata e respinta, esito `-8,9%`, non è il predecessore di V5)
- **Sorgente:** `src/agricola/strategy/claude/e17_reactive_3q_v5.py`
- **Config:** `docs/model_specs/claude/e17/configs/CLAUDE_E17_1_3Q_REACTIVE_V5.json`
- **Origine:** `experiments/e17/reports/common/E17_THREE_AGENT_DEVELOPMENT_TOURNAMENT_V2_REPORT_IT.md`
  (torneo a tre 2026-09-03, 42/42 match development, Codex 28-0-0,
  Claude V3 14-14-0, Copilot 0-28-0), Sezione "Decisione": *"Il prossimo
  round deve essere un'ablation development per ciascun agente, senza
  combinare leve: [...] routing e cap zootecnico per Claude"*.

---

## 1. Diagnosi del torneo (non assunta, misurata su 28 match V3 vs Codex/Copilot)

| KPI | Claude V3 | Codex 6-6-2 | Copilot native |
|---|---:|---:|---:|
| MOVE/produttive | **3,754** | 1,372 | 1,221 |
| Peak animali | 4,82 | 15,00 | 0,00 |
| Fughe EOD derivate | **57** | 0 | 0 (crop-only) |
| Peak crop | 30,64 | 59,93 | 51,50 |

Le raccomandazioni testuali del torneo per Claude (Sezione "Miglioramenti
prioritari"):

1. *"Il collo di bottiglia principale è logistico: 4.321 MOVE/run e 3,754
   MOVE/produttive. Introdurre cluster per quadrante, continuità di target
   e riassegnazione anti-collisione prima di aumentare la superficie."*
2. *"Ridurre bestiame alla capacità realmente servibile: 57 fughe, solo
   4,32 animali terminali medi e 3,68 strutture zootecniche vuote."*
5. *"Non riproporre da sola la leva V4 Q2-livestock: prima va risolta la
   capacità di movimento e servizio dimostrata insufficiente."*

Il punto 5 esclude esplicitamente di ripartire da V4 (coerente con
l'esito già registrato: spot-check 4 seed, `-8,9%`, non promossa). V5
riparte quindi da V3.

Nota aritmetica di verifica: `8` strutture costruite (`4` per quadrante ×
`2` quadranti ammessi, config V3) meno `4,36` animali terminali medi
(media 28 match, `E17_1_V3_DEV_BENCHMARK_VS_CODEX.json`) fa esattamente
`3,68` — conferma diretta che la capacità di costruzione eccede
sistematicamente quella di popolamento, non un artefatto di un solo seed.

---

## 2. Ipotesi V5

**H-CR5.1 (clustering, non solo tie-break):** il tie-break di prossimità
di quadrante già in V3 (`cross_quadrant_penalty`) agisce **solo a parità
di priorità**. Una singola tile `URGENT_WATER`/`FEED_NEEDED` ovunque sulla
mappa vince comunque contro qualunque opportunità non critica più vicina e
nello stesso quadrante del worker, perché la priorità numerica domina la
chiave di ordinamento prima del tie-break. Nella pratica ciò significa che
ogni worker rimane "disponibile" a essere richiamato dall'altra parte
della mappa per compiti non critici (BUILD, HARVEST, PLANT, CARE, PLACE
ANIMAL), producendo il MOVE/produttive osservato. Rendere il confinamento
di quadrante una restrizione **dura** per i soli generi non critici,
lasciando i due generi critici (`URGENT_WATER`, `FEED_NEEDED` — gli
stessi già usati da `CRITICAL_PRIORITY_CEILING` per la preemption di
stickiness, MODEL_SPEC V3 Sez. 6.2 punto 5) liberi di attraversare,
dovrebbe ridurre il MOVE senza reintrodurre le fughe che la preemption
critica già preveniva.

**H-CR5.2 (cap zootecnico):** costruire sistematicamente più strutture di
quante il gregge raggiunga mai (`8` contro `4,36`) spende turni worker in
BUILD_OPPORTUNITY che non producono mai animali. Abbassare il target di
costruzione al livello realmente dimostrato (`3` per quadrante anziché
`4`) libera turni worker per servizio/produzione senza modificare la
formula di capacità di alimentazione (`herd_per_worker_ratio`), che non è
la causa diagnosticata.

**Portata:** entrambe le ipotesi appartengono alla stessa famiglia
assegnata dal torneo ("routing e cap zootecnico per Claude") ed erano
inizialmente pianificate insieme, come due leve di config
indipendentemente disattivabili. Un'ablation isolata pre-benchmark
(Sezione 1.1) ha però trovato un'interazione negativa severa fra le due:
V5 spedisce quindi con la sola leva #1, rimandando la #2 a un round
separato (Sezione 6).

### 1.1 Ablation pre-benchmark: le due leve interagiscono male

Prima del benchmark contro Codex a più seed, le due leve sono state
isolate su singole run dirette (seed `26090101`, seat 0, stesso avversario
`CODEX_V9`):

| Configurazione | Denaro | Hands finali | Quadranti sbloccati |
|---|---:|---:|---|
| V3 (baseline) | 12.174 | 8 | NW, NE, SW |
| Solo clustering (leva #1) | **17.178** | 5 | NW, NE |
| Solo cap ridotto (leva #2) | 10.346 | 8 | NW, NE, SW |
| **Entrambe insieme** | **345** | 5 | NW, NE |

Nessuna delle due leve isolata riproduce il collasso; solo la
combinazione lo fa. Ripetendo "solo clustering" su altri tre seed di
sviluppo (`26090102`, `26090103`, `1838889274`, sempre seat 0) il quadro
è: `15.693` (contro V3 `10.267`), `12.560` (contro V3 `17.076`), `13.419`
(contro V3 `13.854`) — nessun collasso, segno misto ma prevalentemente
positivo. Questo isola con ragionevole confidenza la leva #2 (o la sua
interazione con la #1) come causa del collasso, non la #1 da sola.
**Decisione:** V5 spedisce con `cluster_by_home_quadrant=true` e
`structures_target_per_quadrant` lasciato al valore V3 (`4`); la leva #2
resta implementata e config-toggleable ma disattivata di default, per un
round di ablation separato (Sezione 6).

---

## 3. Modifica implementata

`src/agricola/strategy/claude/e17_reactive_3q_v5.py`:

### 3.1 Home-quadrant clustering (`_best_opportunity`, `_home_quadrant_for`)

- Ogni worker riceve un `home_quadrant` calcolato per round-robin
  sull'indice del worker nel roster del turno corrente
  (`worker_index % len(unlocked_quadrants)`), **ricalcolato a ogni
  chiamata**, non persistito fra step: coerente con il contratto motore
  già documentato ("Hands are physically replaced every EOD"), quindi non
  serve un nuovo stato cross-day.
- `_best_opportunity` con `home_quadrant` impostato: cerca prima solo fra
  le opportunità del quadrante home; se lì trova già un genere critico, si
  ferma. Altrimenti cerca fra *tutte* le opportunità critiche ovunque sulla
  mappa; se ce n'è una, la restituisce (attraversamento consentito). Se non
  c'è nulla di critico, restituisce il migliore risultato home (se esiste)
  o, solo in sua assenza, ricade sulla ricerca globale (per non far
  restare un worker inattivo con un quadrante home già completamente
  servito).
- Con `home_quadrant=None` (flag disattivato) il comportamento è
  bit-per-bit quello di V3 (stesso tie-break `cross_quadrant_penalty`,
  nessuna restrizione dura).
- Config: `dispatch.cluster_by_home_quadrant` (default `true` in V5,
  `false` riproduce V3).

### 3.2 Cap zootecnico (`ReactiveConfigV5`) — implementato, non attivo di default

- `livestock.structures_target_per_quadrant`: campo config esiste ed è
  consumato dal codice esattamente come in V4, ma il valore di default
  spedito in `CLAUDE_E17_1_3Q_REACTIVE_V5.json` resta `4` (V3), non `3`,
  per l'esito dell'ablation di Sezione 1.1.
- `herd_per_worker_ratio` (formula di capacità di servizio): **invariato**
  a `0,5` in ogni caso — l'ipotesi H-CR5.2 riguardava la sovra-costruzione,
  non la formula di capacità.
- `max_quadrants_for_livestock`: **invariato** a `2` (V4, che lo portava a
  `3`, non è il predecessore di questa versione ed è fuori scope).

### 3.3 Cosa NON è stato toccato

Guardia `_core_established`, soffitto workforce (`max_hands=15`), riserva
dedicata zootecnica, timing di espansione (`_expansion_guard`), catena di
vendita, `herd_per_worker_ratio`, cap zootecnico (Sezione 3.2). Tutte le
altre leve V1-V3 restano bit-per-bit identiche (verificato con `diff`
contro `e17_reactive_3q_v3.py`: solo rinomina di identificatori più il
clustering di Sezione 3.1).

---

## 4. Stato del benchmark

Eseguito secondo lo stesso protocollo già stabilito per V4
(`docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V4_STATIC_PLAN_IT.md`
Sezione 5): spot-check a 4 seed positivo (`+13,6%`), esteso alla matrice
completa a 7 seed × 2 seat (28 match): denaro medio `13.989,79` contro
`13.540,86` di V3 (`+3,31%`), `crop_tiles_final` quasi triplicato
(`3,14` contro `1,00`), zero errori tecnici, zero collassi. Un match
(seed `26090101`, seat `0`) resta anomalo — bloccato a `5 hands`/`2Q`
invece di `8`/`3Q`, non dannoso in quel caso specifico ma non ancora
compreso. Nessun seed holdout o final-confirmation consumato. Dettaglio:
`docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V5_DEVELOPMENT_REPORT_IT.md`.

---

## 5. Vincoli invariati

Identici a V3: nessun import da `agricola.strategy.codex`/`antigravity`/
`copilot`, nessuna tabella di azioni indicizzata per step, nessun consumo
di seed holdout o final-confirmation, benchmark contro Codex rigorosamente
black-box. La progettazione del clustering (Sezione 3.1) è stata derivata
esclusivamente dai KPI aggregati pubblicati nel report del torneo
(MOVE/produttive, fughe, strutture vuote) e dal comportamento già
documentato di `CRITICAL_PRIORITY_CEILING` nel proprio codice V3; nessun
sorgente, routine o dispatcher Codex/Copilot è stato letto per
progettarla.

---

## 6. Prossimo passo: cap zootecnico come ablation isolata

La leva #2 (Sezione 3.2) resta implementata, testata singolarmente con
esito neutro/lievemente negativo (`10.346` vs `12.174` su un seed, `-15%`)
e disattivata di default. Il prossimo round dovrebbe testarla **da sola,
sopra V5 con clustering già stabile** (non sopra V3), con lo stesso
protocollo a 2→4→7 seed, per capire se l'interazione negativa osservata in
Sezione 1.1 è specifica della combinazione con il clustering o si
ripresenta anche isolata su più seed. Non deve essere riattivata insieme
al clustering nello stesso esperimento senza una diagnosi più precisa
della causa dell'interazione.
