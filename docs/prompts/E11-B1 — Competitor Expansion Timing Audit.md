# E11-B1 — Competitor Expansion Timing Audit

## Contesto

Prima di procedere con E11-06, è necessario misurare un elemento che finora è rimasto solo parzialmente osservato:

> **il timing effettivo con cui i competitor di vertice espandono la propria superficie produttiva.**

Finora E11 ha misurato soprattutto la massa finale dei top player:

- 4 quadranti / 100 tile;
- circa 75–90 tile produttive;
- workforce significativamente superiore alla nostra;
- livestock attivato;
- massa economica nell'ordine del benchmark competitivo `$70k–$75k+`.

Le iterazioni E11-01 → E11-05 hanno però mostrato che il **timing dell'espansione** è una variabile determinante.

In particolare E11-03, prima configurazione capace di sbloccare realmente l'espansione territoriale, ha ottenuto indicativamente:

- passaggio a 3 quadranti / 75 tile: circa **Day 5.4 medio**
- passaggio a 4 quadranti / 100 tile: circa **Day 11.2 medio**
- 3 quadranti raggiunti nell'83.3% degli episodi
- 4 quadranti raggiunti nel 60.0% degli episodi

Prima di progettare E11-06 dobbiamo quindi verificare se questi timing siano:

- competitivi;
- troppo lenti;
- troppo aggressivi;
- oppure corretti ma seguiti da una cattiva attivazione produttiva.

---

# 1. Obiettivo

Eseguire:

> **E11-B1 — Competitor Expansion Timing Audit**

senza modificare la strategia E11.

La domanda principale è:

> **In quali giorni/turni i top competitor passano mediamente da 50 → 75 → 100 tile, e come questi timing si confrontano con E11-03?**

L'audit deve permettere di distinguere tre scenari:

### Scenario A — Expansion Timing Gap

I competitor raggiungono 75/100 tile significativamente prima di E11-03.

### Scenario B — Activation Gap

E11-03 acquista terreno con timing comparabile ai top, ma utilizza male la nuova capacità.

### Scenario C — Mixed Gap

E11-03 è sia più lenta nell'espansione sia meno efficace nell'attivazione.

---

# 2. Correggere la nomenclatura

Nei report precedenti la nomenclatura Q0/Q1/Q2/Q3 è diventata ambigua.

Per questo audit evitare di utilizzare soltanto etichette come:

- Q1
- Q2
- Q3

senza specificarne il significato.

Utilizzare sempre, come riferimento principale:

> **50 tile / 2 quadranti**  
> **75 tile / 3 quadranti**  
> **100 tile / 4 quadranti**

Se vengono mantenute anche le etichette Q0/Q1/Q2/Q3, riportare sempre accanto il numero effettivo di tile/quadranti posseduti.

---

# 3. Baseline nostra da confrontare

Utilizzare come riferimento principale:

> **E11-03 — Expansion Gate Unlock**

perché è l'ultima configurazione che ha dimostrato realmente capacità di espansione territoriale senza introdurre nuovamente la regressione di E11-04/E11-05.

Baseline E11-03:

- **75 tile / 3 quadranti unlock rate:** `83.3%`
- **75 tile mean unlock timing:** circa `Day 5.4`
- **100 tile / 4 quadranti unlock rate:** `60.0%`
- **100 tile mean unlock timing:** circa `Day 11.2`
- **Peak active productive tiles:** `54`
- **Peak workforce:** `6`

Verificare questi valori dai risultati salvati prima di utilizzarli nel confronto.

Se i dataset storici restituiscono valori leggermente differenti a causa del benchmark specifico, riportare il valore effettivamente letto e spiegare la differenza.

---

# 4. Campione competitor

Riutilizzare, quando possibile, i replay/top competitor già utilizzati per:

> **E11-B0 — Top Player Benchmark**

Non sostituire il campione con player casuali.

L'obiettivo è misurare il comportamento della fascia competitiva superiore.

Per ogni replay identificare:

- competitor/player;
- replay/run;
- score/final money se disponibile;
- ranking/fascia competitiva se disponibile;
- completezza dei dati osservabili.

Se il numero di replay è limitato, dichiararlo esplicitamente.

---

# 5. Numero minimo di osservazioni

Cercare di ottenere almeno:

> **10 replay top-player**

se disponibili.

Preferibile:

> **15–30 osservazioni**

per avere una media più robusta.

Se non è possibile:

- usare tutti i replay disponibili;
- non inventare dati;
- indicare chiaramente `n`.

---

# 6. Evento Expansion 1 — 50 → 75 tile

Per ogni competitor rilevare il momento esatto o migliore stima possibile in cui passa da:

> **2 quadranti / 50 tile**

a:

> **3 quadranti / 75 tile**

Registrare:

- day;
- turn/hour, se disponibile;
- tile/quadranti prima;
- tile/quadranti dopo;
- cash pre-acquisto, se osservabile;
- cash post-acquisto, se osservabile;
- workforce;
- active productive tiles;
- crop mix;
- livestock state.

---

# 7. Evento Expansion 2 — 75 → 100 tile

Per ogni competitor rilevare il momento in cui passa da:

> **3 quadranti / 75 tile**

a:

> **4 quadranti / 100 tile**

Registrare le stesse metriche:

- day;
- turn/hour;
- cash pre/post;
- workforce;
- active tiles;
- crop mix;
- livestock.

---

# 8. Full Land Timing

Definire esplicitamente:

> **Full Land Timing = primo momento in cui il player possiede 100 tile / 4 quadranti.**

Registrare per ogni run.

Questo diventa uno degli indicatori principali del benchmark.

---

# 9. Metriche statistiche

Per ciascun evento calcolare almeno:

### 75 tile timing

- mean day;
- median day;
- sample standard deviation;
- min;
- max;
- n.

### 100 tile timing

- mean day;
- median day;
- sample standard deviation;
- min;
- max;
- n.

Se disponibile il timing intraday, mantenere maggiore precisione.

---

# 10. Distribuzione

Non limitarsi alla media.

Creare una distribuzione semplice, per esempio:

### 75 tile

- Day 1–3
- Day 4–5
- Day 6–7
- Day 8+

### 100 tile

- Day 1–6
- Day 7–9
- Day 10–12
- Day 13+

Adattare i bucket solo dopo aver osservato i dati.

Lo scopo è capire se il timing medio è rappresentativo o se esistono strategie molto differenti.

---

# 11. Workforce al momento dell'espansione

Per ogni evento misurare, se disponibile:

### al raggiungimento di 75 tile

- numero worker;
- worker/tile ratio;
- active tiles/worker.

### al raggiungimento di 100 tile

- numero worker;
- worker/tile ratio;
- active tiles/worker.

Questo dato è fondamentale per valutare la proposta futura di workforce scaling.

---

# 12. Productive Utilization al momento dell'espansione

Misurare:

```text
active_tiles / owned_tiles
```

al momento del passaggio:

- 50 → 75 tile;
- 75 → 100 tile.

Questo permette di capire se i top:

- saturano quasi completamente il terreno prima di espandere;
- oppure comprano nuova capacità con utilizzo ancora relativamente basso.

Quest'ultima informazione è particolarmente importante per verificare la validità del gate `MIN_OPERATIONAL`.

---

# 13. Crop state al momento dell'espansione

Per ogni evento osservare, quando possibile:

- numero crop differenti;
- presenza Melon;
- presenza Strawberry;
- presenza Tomato;
- presenza Wheat;
- presenza Carrot;
- percentuale indicativa di tile coltivate.

Non è necessario ricostruire ogni tile se il replay non lo permette.

Classificare il dato come:

- observed;
- estimated;
- unavailable.

---

# 14. Livestock timing

Registrare, quando osservabile:

> **primo giorno di attivazione livestock**

e confrontarlo con:

- 75 tile unlock;
- 100 tile unlock.

Determinare se i top player introducono livestock:

- prima di 75 tile;
- tra 75 e 100;
- dopo full land.

Questo dato sarà utile per capire se la nostra sequenza “land prima, livestock dopo” è corretta.

---

# 15. Revenue / Money trajectory

Se il replay rende disponibili valori economici nel tempo, registrare almeno:

- money al momento dei 75 tile;
- money al momento dei 100 tile;
- money a Day 15;
- money a Day 20;
- final money.

L'obiettivo è capire se i top:

> investono quasi tutta la cassa durante l'espansione

oppure:

> mantengono già una forte liquidità.

---

# 16. Tempo tra i due expansion event

Per ogni competitor calcolare:

```text
delta_expansion_days =
    full_land_day - three_quadrant_day
```

Calcolare:

- mean;
- median;
- std;
- min/max.

Questa metrica ci dice quanto rapidamente i top passano da 75 a 100 tile.

---

# 17. Confronto diretto con E11-03

Produrre una tabella:

| Metrica | Top competitor | E11-03 | Gap |
|---|---:|---:|---:|
| 75 tile mean day | | 5.4 | |
| 75 tile median day | | | |
| 100 tile mean day | | 11.2 | |
| 100 tile median day | | | |
| Delta 75→100 | | ~5.8 d | |
| Workforce @75 | | | |
| Workforce @100 | | | |
| Active tiles @75 | | | |
| Active tiles @100 | | | |
| Utilization @75 | | | |
| Utilization @100 | | | |

Usare i valori E11-03 effettivamente verificati.

---

# 18. Gap percentuale / temporale

Calcolare, quando sensato:

```text
timing_gap_days =
    E11_timing - competitor_timing
```

Esempio:

```text
competitor full land = Day 8
E11-03 full land = Day 11.2
gap = +3.2 days
```

Un gap di diversi giorni in un episodio di 30 giorni può essere economicamente molto rilevante.

---

# 19. Classificazione del timing

Definire:

## COMPETITIVE TIMING

Se E11-03 è sostanzialmente entro circa 1 giorno dal benchmark top.

## MODERATE TIMING GAP

Se il ritardo è circa 1–3 giorni.

## MAJOR TIMING GAP

Se il ritardo è superiore a circa 3 giorni.

Queste soglie sono interpretative, non target già validati.

Riportare comunque il valore numerico effettivo.

---

# 20. Analisi della sequenza strategica dei competitor

Verificare se emerge una sequenza prevalente del tipo:

```text
bootstrap
→ first expansion
→ workforce increase
→ second expansion
→ high-yield crop activation
→ livestock
```

oppure altra sequenza.

Non forzare il dato dentro questo schema.

Documentare la sequenza realmente osservata.

---

# 21. Cluster comportamentali

Se il campione lo consente, identificare eventuali pattern differenti.

Per esempio:

### Fast Land

Compra presto 100 tile e attiva successivamente.

### Balanced Expansion

Alterna terreno e capacità produttiva.

### Production First

Costruisce revenue prima di espandersi completamente.

Non creare cluster artificiali con pochi dati.

Usarli solo se emergono chiaramente dai replay.

---

# 22. Dati mancanti

Per ogni metrica distinguere:

- direttamente osservata;
- calcolata;
- proxy;
- stimata visivamente;
- non disponibile.

Non trasformare osservazioni qualitative in dati quantitativi certi.

---

# 23. Verifica della nomenclatura E11

Durante l'audit verificare anche i report precedenti per chiarire definitivamente la corrispondenza tra:

- Q0/Q1/Q2/Q3;
- numero di quadranti posseduti;
- numero di tile.

Se necessario aggiornare la documentazione per standardizzare da ora in avanti il linguaggio:

> `2Q / 50 tiles`  
> `3Q / 75 tiles`  
> `4Q / 100 tiles`

Questo deve diventare il formato preferito.

---

# 24. Decisione strategica richiesta

Al termine classificare il gap principale.

## TIMING GAP

I top raggiungono 75/100 tile significativamente prima di E11-03.

Implicazione:

> E11-06 deve intervenire ancora sull'espansione.

---

## ACTIVATION GAP

Il timing di E11-03 è competitivo, ma i top dispongono di:

- più worker;
- maggiore active footprint;
- crop migliori;
- più revenue;

immediatamente dopo l'espansione.

Implicazione:

> E11-06 deve concentrarsi su post-land activation.

---

## MIXED GAP

I top espandono prima e attivano meglio.

Implicazione:

> definire quale componente rappresenta il collo di bottiglia dominante prima del BUILD.

---

# 25. Non modificare il codice E11

Questo task è un audit.

NON:

- modificare `ProductiveMassROIAgent`;
- modificare soglie;
- creare E11-06;
- eseguire tuning;
- generare submission;
- effettuare run Kaggle della nostra policy.

È consentito creare script/tooling di analisi se necessario per estrarre dati dai replay.

---

# 26. Deliverable

Creare:

`docs/versions/E11_B1_competitor_expansion_timing_audit.md`

Struttura minima:

1. Executive Summary
2. Objective
3. Sample
4. Data Sources
5. Nomenclature Standardization
6. Method
7. 50→75 Tile Timing
8. 75→100 Tile Timing
9. Full Land Timing
10. Timing Distribution
11. Workforce at Expansion
12. Productive Utilization at Expansion
13. Crop State
14. Livestock Timing
15. Economic State at Expansion
16. 75→100 Expansion Delta
17. E11-03 Comparison
18. Timing Gap Classification
19. Strategic Sequence
20. Behavioral Patterns
21. Data Quality & Limitations
22. Final Diagnosis
23. Implication for E11-06

---

# 27. Aggiornamento documentazione

Aggiornare, se appropriato:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato:

> **E11-B1 Competitor Expansion Timing Audit COMPLETED — awaiting supervisor review**

Non modificare lo stato E11 come esperimento completato.

---

# 28. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

Non effettuare:

- commit finale;
- tag;
- push;
- submission.

---

# Deliverable finale

Al termine fermarsi e riportare:

1. **numero di competitor/replay analizzati**
2. **qualità/completa disponibilità dei dati**
3. **mean/median day 50→75 tile**
4. **std/min/max 50→75**
5. **mean/median day 75→100 tile**
6. **std/min/max 75→100**
7. **mean delta 75→100**
8. **full-land timing medio**
9. **workforce media @75 tile**
10. **workforce media @100 tile**
11. **active tiles medi @75**
12. **active tiles medi @100**
13. **utilization ratio @75**
14. **utilization ratio @100**
15. **livestock activation timing**
16. **crop pattern al momento dell'espansione**
17. **confronto E11-03**
18. **timing gap in giorni**
19. **TIMING / ACTIVATION / MIXED GAP verdict**
20. **principale evidenza causale**
21. **limiti dell'audit**
22. **file creati/modificati**
23. **raccomandazione precisa per E11-06**

## Regola finale

Non progettare E11-06 prima di aver risposto quantitativamente a questa domanda:

> **Il nostro problema è comprare i 100 tile troppo tardi, oppure comprare i 100 tile con timing corretto ma non riuscire ad attivarli?**

**Fermarsi dopo l'audit e attendere approvazione.**