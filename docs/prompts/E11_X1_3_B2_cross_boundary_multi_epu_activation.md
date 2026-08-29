# E11-X1.3-B2 — BUILD + VERIFY — Cross-Boundary Multi-EPU Activation

## Contesto

E11-X1.3-A ha replicato con successo il meccanismo E06 come 1× Elementary Productive Unit (EPU):

- 9 tile compatte
- 2 worker
- Water-First
- fast ROI crop rotation
- low movement
- no land expansion
- seed0/pass: **$25,847 exact match**
- 5-episode Mean Final Money: **$26,888.40**
- provenance: **PASS**

E11-X1.3-B ha verificato il primo scaling a 2× EPU:

- 18/18 active tiles
- 3 workers
- EPU2 attivata dopo BUY_LAND
- Mean Final Money: **$28,727.40**
- scaling ratio vs A: **1.07×**
- scaling efficiency: **53.4%**
- EPU2 activation: circa Day 15
- Gate B precedentemente STOP

La diagnosi principale è che B valuta una seconda EPU attivata troppo tardi e attribuisce tutto il costo del primo land purchase a una sola unità aggiuntiva.

Il nuovo insight architetturale è:

> **lo stesso land purchase può essere usato per predisporre spazio sufficiente ad attivare EPU2 ed EPU3 quasi consecutivamente.**

Pertanto il precedente vincolo:

> **STOP dopo EPU2 / non attivare EPU3 nello stesso treatment**

viene rimosso.

---

# 1. Obiettivo

Procedere con:

> **E11-X1.3-B2 — Cross-Boundary Multi-EPU Activation**

Domanda sperimentale:

> **Un singolo land purchase, combinato con un layout cross-boundary ad alta densità, può abilitare EPU2 ed EPU3 quasi contemporaneamente e trasformare il modesto scaling 2× di B in un vero compounding 3× senza richiedere un secondo acquisto territoriale immediato?**

La sequenza da testare è:

```text
EPU1
  ↓
productive surplus
  ↓
single BUY_LAND
  ↓
EPU2 activation
  ↓
EPU3 activation as soon as startup capital + workforce permit
  ↓
27 active productive tiles
```

---

# 2. Cambiamento rispetto a X1.3-B

B2 NON deve essere una semplice ottimizzazione crop.

La modifica architetturale primaria è:

> **layout + activation policy**

In particolare:

1. EPU2 non deve occupare inutilmente un intero quadrante operativo.
2. EPU2 deve essere collocata a cavallo del confine tra terreno già disponibile e terreno appena acquistato, se compatibile con la geometria reale.
3. Il layout deve lasciare spazio sufficiente nel nuovo terreno per EPU3.
4. EPU3 può essere attivata nello stesso treatment B2.
5. Non è richiesto un secondo land purchase prima di EPU3 se 27 productive tiles possono essere ospitate nel terreno già posseduto.

---

# 3. Eliminazione del vecchio Stop Gate B

Rimuovere il vincolo:

> `Scaling Efficiency B < 60% => do not evaluate EPU3`

Questo gate era valido quando EPU3 rappresentava un ulteriore investimento territoriale indipendente.

Con B2, invece:

> **EPU3 può essere proprio il meccanismo che ammortizza economicamente il primo BUY_LAND.**

Quindi il nuovo trattamento deve valutare l'economia complessiva:

```text
1× EPU
→ land purchase
→ 2× EPU
→ 3× EPU
```

prima di giudicare definitivamente l'efficienza del land investment.

---

# 4. Vincolo territoriale da verificare prima del BUILD

Prima di implementare il layout:

ricostruire esattamente la geometria dei quadranti e delle coordinate possedute.

Produrre una mappa/tabella:

| EPU | Coordinates | Quadrant ownership required | Tile count |
|---|---|---|---:|
| EPU1 | | | 9 |
| EPU2 B2 | | | 9 |
| EPU3 B2 | | | 9 |

Verificare:

- 9 tile per EPU;
- nessuna sovrapposizione;
- coordinate legalmente possedute al momento dell'attivazione;
- contiguità o quasi-contiguità;
- movement burden;
- spazio residuo dopo EPU3.

NON assumere a priori che una coordinata appartenga a Q1/Q2 solo dal nome usato nei report precedenti.

Usare la geometria effettiva dell'environment.

---

# 5. Standard di nomenclatura

Per evitare ambiguità, usare sempre:

- owned tiles;
- numero quadranti;
- coordinate.

Esempio:

> `2Q / 50 owned tiles`

Non usare soltanto Q1/Q2/Q3 quando può generare confusione.

---

# 6. Layout objective

Il layout B2 deve massimizzare:

> **productive density per land purchase**

e minimizzare:

> **distance / movement**

Preferire cluster che consentano assegnazione stabile ai worker.

---

# 7. EPU1 invariata

EPU1 resta la replica verificata E06:

- 9 tile NW;
- stesso spatial partitioning;
- stessa crop logic;
- stesso Water-First;
- stessa seed discipline;
- workforce E06-equivalent.

Non modificarla.

---

# 8. EPU2 cross-boundary

Progettare EPU2 come cluster da 9 tile che sfrutti il confine territoriale in modo da:

- usare il minor nuovo terreno possibile;
- rimanere compatta;
- evitare travel dilution;
- lasciare spazio utile ad EPU3.

Registrare:

- distanza media dal worker assegnato;
- distanza massima;
- tile già possedute prima del BUY_LAND;
- tile rese disponibili dal BUY_LAND.

---

# 9. EPU3 sullo stesso land purchase

EPU3 deve poter essere attivata:

> **senza un secondo BUY_LAND**

se la geometria lo consente.

Questo è un acceptance criterion architetturale importante.

Registrare:

```text
land_purchase_count_before_EPU3
```

Target:

> **1**

---

# 10. Attivazione EPU3

Rimuovere qualsiasi flag o gate che impedisca EPU3 nello stesso treatment.

EPU3 può essere attivata non appena:

- EPU2 è operativa;
- startup capital EPU3 è disponibile;
- workforce richiesta è sostenibile;
- working capital delle EPU esistenti resta protetto.

NON imporre un ritardo minimo artificiale.

---

# 11. Quasi-contemporaneità

Registrare:

```text
EPU2_activation_day
EPU3_activation_day
delta_EPU2_EPU3_days
```

Obiettivo:

> minimizzare `delta_EPU2_EPU3_days`

senza compromettere stabilità produttiva.

Non imporre `delta = 0` come requisito rigido.

---

# 12. Working capital

L'attivazione EPU3 non deve prosciugare EPU1/EPU2.

Definire:

```text
required_cash_for_EPU3 =
EPU3_startup_capital
+ operating_reserve_existing_EPUs
```

Non includere nuovo land cost se nessun secondo acquisto è necessario.

---

# 13. Land trigger

Il primo land purchase deve restare derivato da:

```text
land_cost
+ startup_capital_required_for_next_productive_mass
+ operating_reserve_existing_EPU
```

Con B2, valutare se il "next productive mass" può includere:

> **EPU2 + partial/full EPU3 startup**

se il surplus lo consente.

Non introdurre magic threshold non derivati.

---

# 14. Workforce

La workforce deve essere workload-driven.

Esiste:

> **1 Farmer permanente + N Hands giornalieri**

NON esistono più Farmer multipli.

Per ogni giorno registrare:

- requested Hands;
- accepted Hands;
- total workers;
- worker-to-EPU assignment.

---

# 15. Worker assignment

Preferire assegnazioni per EPU/cluster per ridurre interferenze.

Per esempio, concettualmente:

- Worker set A → EPU1
- Worker set B → EPU2
- Worker set C → EPU3

ma non imporre due worker fissi per EPU se il workload dimostra che una distribuzione diversa è più efficiente.

---

# 16. Crop policy

Per B2 NON introdurre ancora una nuova crop optimization.

Usare il productive mechanism E06 replicato come base.

La domanda B2 è:

> **layout + activation density**

non:

> quale crop nuovo scegliere.

Se il crop horizon diventa bottleneck dopo l'attivazione EPU3, registrarlo per il prossimo treatment.

---

# 17. Water-First invariato

Mantenere Water-First E06-equivalent.

Non modificare priority ordering per compensare altri problemi.

---

# 18. Market / seed logic invariati

Mantenere:

- on-demand seed buying;
- fast ROI selection;
- immediate/full relevant market liquidation;

come già replicati.

---

# 19. Benchmark locale rapido

Prima della submission Kaggle:

utilizzare il protocollo:

> **1 → 5**

Stage 10 NON è obbligatorio per B2 prima della prima decisione.

## Smoke

1 episodio seed0/pass.

## Mini

5 episodi paired.

Se B2 mostra un miglioramento netto rispetto a B:

> può diventare candidata submission.

Se B2 è instabile:

> STOP.

---

# 20. Confronti

NON rieseguire A/B se i dataset verificati sono già disponibili.

Usare:

- X1.3-A dataset append-only esistente;
- X1.3-B dataset append-only esistente;
- B2 nuovo dataset.

Confrontare:

| Metric | A | B | B2 |
|---|---:|---:|---:|
| Productive tiles | 9 | 18 | up to 27 |
| Land purchases | 0 | 1 | target 1 |
| EPU2 day | n/a | ~15 | |
| EPU3 day | n/a | not active | |
| Final Money | 26.9k | 28.7k | |
| Scaling ratio vs A | 1× | 1.07× | |
| Scaling efficiency | 100% | 53.4% @2× | |

---

# 21. Scaling metrics B2

Calcolare:

```text
ratio_B2_vs_A =
Money_B2 / Money_A
```

e:

```text
effective_EPU_level =
active_productive_tiles / 9
```

Per 27 active tiles:

```text
scaling_efficiency_3x =
ratio_B2_vs_A / 3
```

NON usare più la sola efficienza 2× come stop.

---

# 22. Land amortization efficiency

Calcolare:

```text
incremental_money_per_land_purchase =
(Money_B2 - Money_A) / land_purchase_count
```

e confrontarlo con B.

Questo misura se il medesimo investimento land produce più valore grazie a EPU3.

---

# 23. Activation density

Calcolare:

```text
productive_tiles_per_land_purchase
```

Per B:

> +9 productive tiles per land purchase

Per B2, target ideale:

> +18 productive tiles per land purchase

se EPU2+EPU3 vengono entrambe abilitate.

---

# 24. Utilization

Registrare:

```text
active_tiles / owned_tiles
```

ai momenti:

- pre-land;
- EPU2 activation;
- EPU3 activation;
- peak.

---

# 25. Movement burden

Confrontare B vs B2:

- MOVE actions;
- movement per productive action;
- distance proxy;
- cross-boundary travel.

Il layout cross-boundary è valido solo se non genera una penalità operativa maggiore del beneficio territoriale.

---

# 26. Stage Smoke acceptance

Nel seed0/pass verificare:

1. EPU1 replica invariata.
2. primo BUY_LAND avviene.
3. EPU2 si attiva.
4. EPU3 può attivarsi senza secondo BUY_LAND.
5. nessuna illegal action.
6. provenance completa.

Se EPU3 richiede comunque secondo terreno:

> STOP e correggere layout, non strategia economica.

---

# 27. Stage Mini acceptance

Su 5 episodi classificare:

## B2 NOT VALIDATED

se:

- EPU3 non si attiva;
- richiede secondo land purchase;
- money <= B;
- movement degrada fortemente.

## B2 PARTIAL

se:

- EPU3 si attiva in alcuni episodi;
- delta EPU2→EPU3 elevato;
- miglioramento economico limitato.

## B2 VALIDATED

se:

- EPU2 + EPU3 vengono attivate con un solo land purchase nella maggioranza dei run;
- 27 active tile raggiungibili;
- money > B;
- provenance PASS.

---

# 28. Submission candidate gate

B2 diventa candidata Kaggle se:

- B2 VALIDATED o forte PARTIAL;
- local Mean Final Money > X1.3-B;
- nessuna regressione grave;
- artifact semantic match verificabile.

NON è necessario eseguire 10 episodi prima di una submission esplorativa se 5 episodi mostrano un segnale netto e stabile.

---

# 29. Kaggle submission

La submission X1.3-B precedente resta sospesa.

Se B2 supera il gate locale:

> preparare B2 come nuova candidata submission.

Non caricare automaticamente su Kaggle nello stesso task a meno che il supervisore lo abbia esplicitamente richiesto.

Questo task deve fermarsi con:

> `B2 READY / NOT READY FOR KAGGLE`

---

# 30. Provenance

Run ID:

> `E11-X1.3-B2-<timestamp>`

Directory append-only:

```text
results/e11/<RUN_ID>/
    config.json
    episodes.json
    summary.json
```

SHA-256 e verifier PASS obbligatori.

---

# 31. Config delta

Produrre:

| Parameter / Behavior | X1.3-B | X1.3-B2 |
|---|---|---|

Le differenze ammesse devono riguardare:

- layout EPU2;
- layout EPU3;
- EPU3 activation enabled;
- land-density/activation logic necessaria.

Non modificare crop mechanism, Water-First o market logic.

---

# 32. Test

Aggiungere test per:

1. EPU1 unchanged.
2. EPU2 has exactly 9 unique tiles.
3. EPU3 has exactly 9 unique tiles.
4. no EPU overlap.
5. EPU2 cross-boundary geometry legal.
6. EPU3 fits after same land purchase.
7. one land purchase sufficient before EPU3.
8. EPU3 activation gate enabled.
9. no artificial B stop gate.
10. workload-driven Hands.
11. working capital protection.
12. Water-First unchanged.
13. crop policy unchanged.
14. provenance.
15. config immutable.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 33. Deliverable documentale

Creare:

`docs/versions/E11_X1_3_B2_cross_boundary_multi_epu_activation.md`

Struttura minima:

1. Executive Summary
2. Why B2
3. X1.3-A Reference
4. X1.3-B Limitation
5. New Architectural Hypothesis
6. Environment Geometry Audit
7. EPU Coordinate Map
8. EPU2 Cross-Boundary Layout
9. EPU3 Same-Land Layout
10. Config Delta
11. Working Capital
12. Workforce
13. Tests
14. Provenance
15. Smoke
16. Mini Benchmark
17. EPU2 Activation
18. EPU3 Activation
19. Delta Activation Days
20. Land Purchase Count
21. Productive Tiles per Land Purchase
22. Utilization
23. Movement
24. Scaling Ratio
25. 3× Scaling Efficiency
26. Land Amortization Efficiency
27. A vs B vs B2
28. B2 Verdict
29. Kaggle Candidate Verdict
30. Next Step

---

# 34. Aggiornamento documentazione

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Se README è già stato riconciliato nel task precedente:

aggiornarlo SOLO se necessario per indicare che B2 è ora current local treatment.

Non riscrivere nuovamente sezioni non coinvolte.

---

# 35. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

NON:

- tag;
- push;
- final release.

---

# Deliverable finale obbligatorio

Riportare:

1. B2 BUILD status
2. run_id
3. environment geometry verified YES/NO
4. EPU1 coordinates
5. EPU2 coordinates
6. EPU3 coordinates
7. EPU2/EPU3 overlap YES/NO
8. land purchases required before EPU2
9. land purchases required before EPU3
10. EPU2 activation day
11. EPU3 activation day
12. delta EPU2→EPU3
13. active tiles peak
14. owned tiles peak
15. utilization peak
16. daily workforce
17. peak workforce
18. movement burden
19. Mean Final Money
20. Median / Std / Min / Max
21. A Mean reference
22. B Mean reference
23. B2/A ratio
24. B2/A 3× scaling efficiency
25. productive tiles per land purchase
26. incremental money per land purchase
27. working capital trajectory
28. land trigger
29. provenance verdict
30. config SHA-256
31. episodes SHA-256
32. tests result
33. B2 validation verdict
34. B2 ready for Kaggle YES/NO
35. README update required YES/NO
36. files created/modified
37. recommended next action

---

# Regola finale

Il precedente schema:

> **A → B → STOP → C separata**

è superato.

B2 deve verificare:

> **A → single land purchase → EPU2 + EPU3**

quando working capital e workforce lo consentono.

Il criterio economico corretto non è più:

> "quanto rende EPU2 da sola?"

ma:

> **"quanto valore produttivo complessivo riesce ad abilitare il primo land purchase?"**

Se lo stesso terreno abilita 18 nuove productive tiles invece di 9, il primo investimento territoriale può avere una logica economica completamente diversa.
