# NEW SESSION — Kaggriculture Agent

## Stato del progetto

Il progetto ha completato e consolidato tre iterazioni sperimentali supervisionate.

Metodo adottato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Branch corrente:

`main`

Stato Git atteso:

- `main` allineato con `origin/main`;
- working tree pulito.

Ultimo commit consolidato:

`Finalize E03 multi-tile scaling experiment`

Tag disponibili:

- `v0.1-e01-baseline`
- `v0.2-e02-roicrop`
- `v0.3-e03-multitile`

---

## Progressione Sperimentale

`E01 operational baseline → E02 economic crop selection → E03 production scaling`

---

## E01 — Baseline

Strategia: `CarrotLoopAgent`

- coltura fissa `CARROT`;
- singola tile `(4, 4)`;
- nessun movimento;
- ciclo operativo: `BUY_SEED → PLANT → WATER → HARVEST → SELL`

Risultati benchmark locale:
- Mean Final Money: `$3567.63 ± $205.38`;
- Median Final Money: `$3528.00`;
- Overall Win Rate: `66.67%`;
- Win Rate vs `starter`: `0.00%` (100% pareggi).

Tag: `v0.1-e01-baseline`

---

## E02 — Dynamic Crop Selection & ROI Scaling

Strategia: `ROICropAgent`

Variabile sperimentale: **selezione dinamica della coltura basata sul ROI/giorno e sulla liquidità disponibile**.

Formula: `NetProfitPerDay = ((SellPrice * 2.0) - SeedPrice) / Days`

Risultati benchmark locale:
- Mean Final Money: `$5857.17 ± $132.37` (`+64.18%` vs E01);
- Median Final Money: `$5837.00`;
- Overall Win Rate: `100.00%`;
- Win Rate vs `starter`: `100.00%`.

Tag: `v0.2-e02-roicrop`

Submission Kaggle E02: Status `Complete`, rating iniziale osservato `600.0` (successivamente `285.1`).

---

## E03 — Multi-Tile Scaling

Strategia: `MultiTileROIAgent`

Variabile sperimentale: **espansione della coltivazione da 1 tile a un cluster compatto 2×2 di 4 tile adiacenti `{(4,4), (4,3), (3,4), (3,3)}` con spatial task prioritization (`HARVEST > PLANT > WATER`) e navigazione Manhattan**.

Modifiche abilitanti:
- Bug fix del formato delle azioni di movimento (`["NORTH"]`, `["SOUTH"]`, `["EAST"]`, `["WEST"]`).
- Coda di priorità delle tile e tie-breaking deterministico `(y, x)`.
- Acquisto semi matched al numero di tile vuote gestite.

### Risultati benchmark locale E03
- Total Episodes: `30`;
- Completion Rate: `100.00%`;
- Disqualification Rate: `0.00%`;
- Overall Win Rate: `100.00%` (30W / 0L / 0D);
- Win Rate vs `pass`: `100.00%` ($15,257.00);
- Win Rate vs `random`: `100.00%` ($14,284.10);
- Win Rate vs `starter`: `100.00%` ($14,506.30);
- Mean Final Money: **`$14682.47`**;
- Sample Std Dev (`ddof=1`): **`± $1164.33`**;
- Median Final Money: **`$14146.00`**;
- Agent Mean Turn Latency: **`0.0698 ms/turno`**.

Confronto E02 → E03:
- Mean Final Money: `$5857.17 → $14682.47`;
- Incremento assoluto: `+$8825.30`;
- Incremento percentuale: **`+150.68%`**;
- Ipotesi Economica E03: **SUPPORTATA**.

### VERIFY Osservabile
- Episodio completo 720 step vs `starter`: Finale **$14,226.00** vs $3,421.00;
- Utilizzo reale di tutte e 4 le tile;
- Movimento direzionale verificato;
- Nessuna irrigation starvation (4 watering + 3 step = 7h/giorno, 17h buffer);
- Zero deadlock, zero oscillazioni, zero disqualification.

### REVIEW & SHIP
- Experimental Integrity: `PASSED`
- Operational Readiness: `READY FOR SHIP`
- Economic Hypothesis: `SUPPORTED`
- SHIP: **`PASSED`**
- Evidenza visuale Kaggle: [`docs/screenshots/E03-001_kaggle_submission_successful.png`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/screenshots/E03-001_kaggle_submission_successful.png)
- Descrizione sottomissione: `E03 supervised iteration: Multi-Tile ROI Agent 2x2 cluster`
- Status Kaggle: **`Complete`**
- Skill Rating iniziale E03 osservato: **`600.0`** (Rating E02 nello stesso screenshot: `285.1`).

Tag: `v0.3-e03-multitile`

---

## Punto di partenza della prossima sessione

Non iniziare automaticamente E04.

La prossima attività consiste nell'analizzare le evidenze ed individuare la successiva **singola variabile sperimentale**.

Prima di scegliere E04:
1. Osservare l'evoluzione del Kaggle Skill Rating per E03 sul leaderboard globale;
2. Confrontarla con i dati di E01 ed E02;
3. Riesaminare le evidenze locali di benchmark;
4. Identificare il principale limite residuo dell'agente.

Le principali candidate per le prossime iterazioni rimangono:
- End-of-Season Horizon (evitare acquisto/semina di colture che non maturano entro il turno 720);
- Market Timing (gestione dinamica del momento di vendita);
- Modello economico con `max_yield` specifico per coltura;
- Scaling geografico oltre le 4 tile (sblocco nuovi quadranti via `BUY_LAND`).

La successiva iterazione deve continuare a mantenere la logica:

**una modifica strategica principale per esperimento**

<!-- END OF DOCUMENT -->