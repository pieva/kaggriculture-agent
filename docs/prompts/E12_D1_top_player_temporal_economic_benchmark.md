# E12-D1 — Top Player Temporal & Economic Benchmark

## Obiettivo

E12-X1.3 ha raggiunto una struttura finalmente comparabile, almeno a livello macro, con quella osservata nei player top:

- livestock early;
- geometria centered;
- espansione multi-quadrante;
- 5 worker;
- circa 24–25 crop tile;
- Cow #1 produttiva.

Nonostante questo, il risultato economico rimane molto inferiore:

- E12-X1.3 Mean Final Money: `$7,015.40`;
- E11-X1.7 Mean Final Money: `$28,083.80`.

Prima di procedere con ulteriori modifiche strategiche, dobbiamo capire **in quale fase temporale ed economica nasce il gap rispetto ai top player osservati nei replay**.

Questo esperimento è esclusivamente diagnostico.

Nome:

**E12-D1 — Top Player Temporal & Economic Benchmark**

NON modificare la strategia E12-X1.3 durante D1.

---

## 1. Domanda sperimentale

La domanda non è più:

> "La nostra architettura assomiglia a quella dei top?"

Ora la domanda è:

> **"A parità approssimativa di architettura, dove e quando iniziamo a perdere rispetto ai top in termini di capitale, massa produttiva e velocità di scaling?"**

Dobbiamo ricostruire una traiettoria:

```text
turn
  ->
cash
  ->
productive mass
  ->
land/workforce
  ->
livestock/crop composition
```

e confrontarla con quella dei top.

---

## 2. Principio metodologico

Non usare un singolo replay come verità assoluta.

Costruire una **Top Player Envelope** usando almeno 2–3 player top osservabili.

Obiettivo:

- trovare pattern comuni;
- identificare range/min-max;
- evitare di copiare una singola strategia;
- distinguere scelte strutturali ricorrenti da scelte individuali.

Le informazioni estratte dai replay devono essere classificate come:

- `DIRECTLY_OBSERVED`
- `INFERRED_FROM_VISUAL`
- `NOT_OBSERVABLE`

Non inventare dati non visibili.

---

## 3. Nessuna modifica al codice strategico

Durante E12-D1:

- NON cambiare crop planner;
- NON cambiare livestock;
- NON cambiare Q1/Q2 timing;
- NON cambiare worker count;
- NON cambiare geometria;
- NON fare tuning.

È consentito soltanto:

- aggiungere telemetry;
- aggiungere script di analisi;
- aggiungere parser/tooling per dati replay se tecnicamente possibile;
- creare report e grafici;
- eseguire X1.3 sugli stessi seed per produrre milestone confrontabili.

---

## 4. Milestone temporali comuni

Per X1.3 e per i top estrarre, quando possibile:

`turn 1, 2, 3, 6, 12, 24, 48, 72, 96, 120, 144, 168, 192, 240`

Se il replay non permette letture esatte a tutti i turn, utilizzare i turn osservabili più vicini e registrare chiaramente l'offset.

Per ogni milestone estrarre almeno:

- cash;
- worker count;
- active crop tiles;
- active pasture tiles;
- active cows;
- owned/unlocked quadrants;
- approximate productive radius;
- crop types visibili;
- wheat/feed tiles visibili;
- eventuale Q1/Q2 state se deducibile;
- farmer position se utile;
- note qualitative.

---

## 5. Benchmark economico-temporale

Costruire almeno queste curve comparative:

### A. Money over time

```text
turn -> cash
```

per:

- E12-X1.3;
- Top Player A;
- Top Player B;
- Top Player C, se disponibile.

### B. Productive mass over time

```text
turn -> active productive tiles
```

dove:

```text
productive tiles =
crop tiles + active livestock tiles
```

Tenere anche crop e livestock separati.

### C. Workforce over time

```text
turn -> active workers
```

### D. Land expansion over time

```text
turn -> owned quadrants / unlocked productive area
```

---

## 6. Milestone benchmark principali

Calcolare per X1.3 e top, quando osservabile:

### Livestock
- turn Cow #1;
- turn pasture #1;
- turn Cow #2/#3/#4;
- money at Cow #1;
- money at Cow #2/#3/#4.

### Crop mass
- turn first 9 crop tiles;
- turn first 15 crop tiles;
- turn first 18 crop tiles;
- turn first 24 crop tiles;
- turn first 26 crop tiles.

### Money at crop milestones
- cash at 9 tiles;
- cash at 15 tiles;
- cash at 24 tiles;
- cash at 26 tiles.

### Workforce
- turn worker #2;
- turn worker #3;
- turn worker #4;
- turn worker #5;
- turn worker #6, se presente.

### Land
- first visible Q1 expansion;
- first visible Q2 expansion;
- full multi-quadrant expansion;
- cash around each expansion.

---

## 7. Opening benchmark

L'opening è particolarmente importante.

Per turn `1–24`, confrontare:

- starting money;
- minimum cash;
- turn of minimum cash;
- capital deployed entro turn 2;
- capital deployed entro turn 3;
- capital deployed entro turn 6;
- capital deployed entro turn 12;
- capital deployed entro turn 24.

Calcolare:

```text
Capital Deployment Ratio(turn T) =
(starting_cash - cash_at_T)
/
starting_cash
```

Questo deve aiutarci a capire se:

- il top investe più aggressivamente;
- il top investe meno ma in asset più produttivi;
- X1.3 spende molto ma recupera lentamente;
- il gap nasce già nell'opening.

---

## 8. Money Recovery

Per ogni player identificare:

- minimum cash;
- primo turn in cui recupera il 50% del capitale iniziale;
- primo turn in cui torna a starting cash;
- primo turn sopra `$4,000`;
- primo turn sopra `$5,000`;
- ulteriori soglie utili se i replay le rendono osservabili.

Definire:

```text
Capital Recovery Time =
turn_when_cash_recovers_starting_cash
-
turn_of_minimum_cash
```

Questa metrica è centrale per confrontare qualità del reinvestimento.

---

## 9. Productivity-normalized metrics

Dove i dati lo consentono, calcolare:

```text
Cash per Productive Tile =
cash / productive_tiles
```

```text
Cash per Crop Tile =
cash / active_crop_tiles
```

```text
Productive Tiles per Worker =
productive_tiles / workers
```

```text
Cash per Worker =
cash / workers
```

Queste metriche non sono ROI contabile perfetto, ma servono come indicatori comparativi temporali.

---

## 10. X1.3 telemetry enrichment

Per X1.3 produrre dati più ricchi di quelli ricavabili visivamente dai replay top.

A ogni milestone registrare:

- cash;
- crop revenue cumulativo;
- milk revenue cumulativo;
- active crop tiles;
- active livestock tiles;
- worker count;
- Q1/Q2;
- seed spend cumulativo;
- land spend cumulativo;
- hire spend cumulativo;
- livestock spend cumulativo;
- movement actions;
- crop productive actions;
- livestock actions;
- idle/pass actions.

Questi dati serviranno per spiegare la divergenza rispetto alla envelope top.

---

## 11. Top Player Envelope

Per ogni milestone, se abbiamo almeno due top, costruire:

```text
TOP_MIN
TOP_MEDIAN
TOP_MAX
```

per:

- cash;
- crop tiles;
- productive tiles;
- workers;
- cows;
- owned quadrants.

Poi confrontare X1.3 con il range.

Esempio concettuale:

```text
Turn 72
Top cash envelope:     1800–2400
X1.3 cash:             950

Top productive tiles:  18–22
X1.3 productive tiles: 16
```

Non inventare numeri: usare solo osservazioni reali.

---

## 12. Divergence Detection

Per ogni metrica identificare il primo milestone in cui X1.3 esce materialmente dalla top envelope.

Classificare la divergenza come:

- `CAPITAL_DIVERGENCE`
- `PRODUCTIVE_MASS_DIVERGENCE`
- `WORKFORCE_DIVERGENCE`
- `LAND_EXPANSION_DIVERGENCE`
- `LIVESTOCK_TIMING_DIVERGENCE`
- `CROP_MIX_DIVERGENCE`
- `RECOVERY_SPEED_DIVERGENCE`
- `MULTI_FACTOR_DIVERGENCE`

Obiettivo:

trovare il **primo punto causale plausibile**, non soltanto il gap finale.

---

## 13. Scenario Interpretation

### Caso A — Cash diverge prima della massa produttiva

Se X1.3 e top hanno massa simile ma il top possiede più cash:

probabile problema di:

- crop yield;
- crop cycle;
- crop mix;
- harvesting;
- worker efficiency;
- selling timing.

### Caso B — Massa produttiva diverge prima del cash

Se il top scala tile/workers più rapidamente:

probabile problema di:

- reinvestment speed;
- land timing;
- hiring timing;
- planner scheduling.

### Caso C — X1.3 investe più capitale ma produce meno

Probabile:

- overinvestment;
- premature land/hiring;
- low utilization;
- excessive movement;
- idle capacity.

### Caso D — X1.3 investe meno dei top

Probabile:

- cash reserve troppo conservativa;
- upgrade gating;
- delayed scaling.

### Caso E — Architettura simile ma recovery molto diversa

Probabile:

- produttività per tile;
- azioni per ciclo;
- crop composition;
- harvest efficiency.

---

## 14. Benchmark replay: procedura operativa

Se i replay possono essere interrogati automaticamente:

1. individuare formato/API disponibile;
2. estrarre stati per turn;
3. salvare dati raw;
4. creare parser riproducibile;
5. documentare provenienza del replay/player.

Se NON è possibile estrarre automaticamente:

1. predisporre una tabella/template manuale;
2. usare screenshot/replay osservati;
3. registrare soltanto valori leggibili;
4. marcare valori approssimati;
5. NON ricostruire artificialmente valori mancanti.

---

## 15. Template dati top

Creare un file strutturato, ad esempio:

`results/e12/top_player_benchmark.csv`

con colonne almeno:

```text
player_id
turn
cash
workers
crop_tiles
pasture_tiles
cows
quadrants
crop_types
wheat_tiles
observation_type
source_note
```

`observation_type`:

- `EXACT`
- `APPROX`
- `NOT_VISIBLE`

---

## 16. X1.3 benchmark data

Creare dati equivalenti per X1.3:

`results/e12/x13_temporal_benchmark.csv`

con gli stessi campi, più metriche interne disponibili.

Questo consentirà merge diretto:

```text
turn + metric
```

---

## 17. Output grafici

Generare almeno:

1. `money_over_time`
2. `crop_tiles_over_time`
3. `productive_tiles_over_time`
4. `workers_over_time`

e, se i dati sono sufficienti:

5. `cash_vs_productive_tiles`
6. `capital_recovery_curve`

I grafici devono mostrare:

- X1.3;
- singoli top;
- eventualmente top envelope.

Non usare interpolazioni che diano l'impressione di dati osservati dove non lo sono.

---

## 18. Rapporto finale richiesto

Produrre:

### A. Top replay sources
- quali player;
- quali replay;
- quali turn osservati;
- qualità dei dati.

### B. Opening comparison
Tabella turn 1–24.

### C. Temporal benchmark
Cash, productive mass, workers, land.

### D. Milestone comparison
Cow, crop tiles, workers, quadrants.

### E. Top envelope
Range dei top per milestone.

### F. Divergence analysis
Primo punto di divergenza per ogni metrica.

### G. Root-cause hypothesis
Massimo 3 cause, ordinate per evidenza.

### H. Implicazioni per X1.4
Indicare esattamente cosa deve essere modificato e cosa NON deve essere toccato.

---

## 19. Regola decisionale per X1.4

Non proporre un generico "economic optimization".

La raccomandazione deve essere una sola tra:

- `X1.4 CROP PRODUCTIVITY RECOVERY`
- `X1.4 CAPITAL DEPLOYMENT TIMING`
- `X1.4 WORKER EFFICIENCY`
- `X1.4 LAND/WORKFORCE TIMING`
- `X1.4 CROP MIX ALIGNMENT`
- `X1.4 MULTI-FACTOR RECOVERY`

La scelta deve derivare dal primo gap osservato rispetto alla top envelope.

---

## 20. Nessuna modifica strategica durante D1

E12-D1 è concluso soltanto quando abbiamo risposto quantitativamente a:

1. A quale turn X1.3 comincia a divergere dai top?
2. Diverge prima in cash o in massa produttiva?
3. A parità di tile, chi ha più soldi?
4. A parità di soldi, chi ha più capacità produttiva?
5. Quanto velocemente il top recupera il capitale investito?
6. Qual è il primo collo di bottiglia plausibile da correggere?

Solo dopo queste risposte si passa a X1.4.

---

## Approval

Questo prompt autorizza:

- raccolta dati replay;
- sviluppo tooling diagnostico;
- telemetry aggiuntiva;
- esecuzione X1.3 per confronto temporale;
- creazione dataset/grafici;
- report D1.

NON autorizza modifiche alla strategia E12-X1.3.

---

## Principio guida

> **Ora che le architetture sono comparabili, il benchmark deve spostarsi dal risultato finale alla traiettoria: quando investono i top, quanto spendono, quanto rapidamente trasformano capitale in massa produttiva e quanto velocemente il denaro ritorna.**
