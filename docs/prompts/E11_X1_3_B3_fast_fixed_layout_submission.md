# E11-X1.3-B3 — FAST BUILD + VERIFY + KAGGLE SUBMISSION
## Fixed 3×3 EPU Strip Layout

## Mandato operativo

È tardi: eliminare ogni ulteriore ricerca geometrica e procedere con un layout deciso dal supervisore.

NON eseguire:
- exhaustive search;
- bounded search;
- geometry optimization;
- ulteriori tentativi di trovare layout migliori.

Usare ESATTAMENTE queste coordinate:

### EPU1
```python
[
    (0,0), (0,1), (0,2),
    (1,0), (1,1), (1,2),
    (2,0), (2,1), (2,2),
]
```

### EPU2
```python
[
    (3,0), (3,1), (3,2),
    (4,0), (4,1), (4,2),
    (5,0), (5,1), (5,2),
]
```

### EPU3
```python
[
    (6,0), (6,1), (6,2),
    (7,0), (7,1), (7,2),
    (8,0), (8,1), (8,2),
]
```

Le tre EPU sono tre quadrati 3×3 contigui orizzontalmente.

Obiettivo geometrico futuro:
- espansione di EPU1/EPU2/EPU3 verso il basso;
- ulteriore espansione di EPU3 verso destra;
- mantenere una struttura modulare e regolare.

---

# 1. Naming

Usare:

> **E11-X1.3-B3 — Fixed 3×3 EPU Strip Scaling**

Questa è una nuova variante rispetto a B/B2/B2R.

Non riscrivere la storia precedente.

---

# 2. Nota metodologica

Il layout B3 NON deve essere presentato come replica geometrica perfetta della vecchia EPU1 E06.

È una scelta architetturale deliberata:

> **tre unità geometricamente identiche tra loro, regolari, contigue e predisposte allo scaling futuro.**

Il productive mechanism deve invece restare E06-equivalent:

- WATER > HARVEST > PLANT;
- dynamic ROI/day crop selection;
- on-demand seed buying;
- immediate market liquidation;
- workforce locale;
- low unnecessary movement.

---

# 3. Nessuna ricerca geometrica

Eliminare dal percorso operativo ogni chiamata a:

```text
search_epu_trio_geometry.py
search_b2r_geometry_bounded.py
find_optimal_epu3_geometry.py
```

Non eliminarli necessariamente dal repository se servono all'audit storico, ma NON usarli.

---

# 4. Vincolo land timing

NON fare BUY_LAND al Day 0.

NON comprare semplicemente perché `cash >= threshold` se il denaro è ancora bankroll iniziale.

Il primo acquisto deve richiedere:

```text
realized_EPU1_revenue > 0
AND
cash >= required_cash
```

dove:

```text
required_cash =
actual_land_cost
+ actual_startup_cost(EPU2)
+ protected_startup_cost(EPU3)
+ operating_reserve
```

Nessun giorno hard-coded.

---

# 5. Realized productive surplus

Aggiungere/riutilizzare una telemetria:

```text
cumulative_realized_revenue
```

Il terreno può essere acquistato solo dopo che EPU1 ha effettivamente monetizzato almeno una produzione.

Questo impedisce il falso "post-surplus" Day 1 del precedente B2R.

---

# 6. EPU2 + EPU3

Dopo il primo BUY_LAND:

- EPU2 deve attivarsi appena possibile;
- EPU3 deve essere ABILITATA nello stesso treatment;
- nessun secondo BUY_LAND deve essere richiesto prima di EPU3;
- EPU3 deve partire appena working capital e workforce lo permettono.

Non inserire Stop Gate dopo EPU2.

---

# 7. Workforce locality

Usare workforce locale alle EPU.

Non compensare eventuale inefficienza con movement cross-EPU.

Registrare:
- worker assignment;
- daily Hands;
- MOVE actions;
- productive actions.

---

# 8. Espansione futura

Non implementare ancora lo scaling verso il basso/destra.

Limitarsi a documentare che il layout B3 lascia:

- righe `y >= 3` disponibili per espansione verticale;
- colonna/area `x >= 9` disponibile per futura espansione di EPU3 se legalmente posseduta.

Non comprare altro terreno in questo task.

---

# 9. Controlled changes

Rispetto al treatment corrente, cambiare SOLO:

1. coordinate EPU1;
2. coordinate EPU2;
3. coordinate EPU3;
4. gating corretto post-realized-revenue;
5. EPU3 enabled nello stesso trattamento.

NON modificare:
- crop ROI;
- Water-First;
- seed buying;
- market selling;
- action priority;
- livestock;
- end-game.

---

# 10. Test rapidi

Aggiornare test minimi:

1. EPU1 = exact 3×3 block.
2. EPU2 = exact adjacent 3×3 block.
3. EPU3 = exact adjacent 3×3 block.
4. zero overlap.
5. total unique productive target tiles = 27.
6. no Day0 BUY_LAND.
7. land requires `cumulative_realized_revenue > 0`.
8. EPU3 enabled after same land purchase.
9. no second land required before EPU3.
10. E06 productive mechanism unchanged.

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

---

# 11. Verification protocol — FAST

Per questa sera eseguire SOLO:

## Stage A0
1 episodio:
- seed 0
- opponent pass

Controllare:
- no Day0 buy;
- actual land purchase day;
- EPU2 activation;
- EPU3 activation;
- peak active tiles;
- final money;
- no illegal actions.

Se A0 produce un crash / illegal action / starvation grave:

STOP.

Altrimenti procedere.

## Stage B
5 episodi:
- stessi seed rapidi già usati: 0,100,200,300,400;
- stesso opponent protocol già adottato nel runner B/B2R.

STOP dopo 5.

NON fare 10.
NON fare 30.

---

# 12. Confronto rapido

Usare risultati già salvati:

### X1.3-A
Mean Final Money:
**$26,888.40**

### X1.3-B
Mean Final Money:
**$28,727.40**

### Old B2
Mean:
**$9,808.40**

### B2R
Mean:
**$26,435.40**

Non rieseguire queste versioni.

Produrre:

| Metric | A | B | B2R | B3 |
|---|---:|---:|---:|---:|
| Mean Money | 26888.40 | 28727.40 | 26435.40 | |
| Productive target | 9 | 18 | up to 27 | 27 |
| Land buys before EPU3 | 0 | n/a | 1 | |
| EPU2 day | n/a | ~15 | | |
| EPU3 day | n/a | off | | |
| Peak active | | 18 | 16 | |
| Peak workforce | | 3 | 4 | |

---

# 13. Candidate gate per submission

Dato il tempo, non richiedere perfezione.

Classificare:

## NOT SUBMITTABLE
se:
- crash;
- illegal actions;
- Day0 land;
- working capital collapse;
- Mean << B2R;
- EPU2/EPU3 non si attivano.

## SUBMITTABLE EXPLORATORY
se:
- run stabile;
- no Day0 buy;
- EPU2/EPU3 attivate;
- Mean almeno nella classe A/B2R;
- provenance PASS.

## PREFERRED CANDIDATE
se:
- Mean > X1.3-B;
- 27 active tiles realmente raggiunte;
- no forte movement regression;
- provenance PASS.

---

# 14. Submission decision

Se B3 è `PREFERRED CANDIDATE`:

> build e prepara B3 per Kaggle.

Se B3 è `SUBMITTABLE EXPLORATORY` ma non supera B:

> dato il tempo, riportare confronto B vs B3 e chiedere/seguire decisione del supervisore se già autorizzata.

Poiché il supervisore ha esplicitamente richiesto:

> **"poi submission che è tardi"**

se B3 è stabile e non mostra regressione grave, procedere con submission B3.

Se B3 è chiaramente peggiore o instabile:

> usare X1.3-B, già pronta, come submission.

Non perdere altro tempo in tuning locale.

---

# 15. Build submission

Usare `scripts/build_submission.py`.

Prima verificare che il bundle contenga ESATTAMENTE il candidate scelto.

Controllare in `submission/submission.py`:

- strategy identity;
- coordinates EPU1/EPU2/EPU3 se B3;
- EPU3 enabled;
- no Day0 buy;
- crop/Water-First invariants;
- no scratch imports.

---

# 16. Semantic smoke dell'artifact

Eseguire 1 smoke seed0/pass direttamente sul bundle standalone.

Confrontare almeno:
- final money;
- land purchase day;
- EPU2 activation;
- EPU3 activation;
- peak workforce;
- peak active tiles.

Deve essere semanticamente coerente con il source candidate.

---

# 17. Kaggle submission

Se artifact PASS:

caricare su Kaggle.

Naming:

### se B3
> `E11-X1.3-B3 Fixed 3x3 3xEPU`

### se fallback B
> `E11-X1.3-B 2x EPU Scaling`

Registrare:
- timestamp;
- submission identifier/version;
- initial status;
- initial score se disponibile.

Non attendere ore nella stessa sessione.

---

# 18. README

Aggiornare rapidamente solo lo stato corrente.

Se B3 viene inviata:
- marcare B3 come external-validation candidate;
- B resta previous candidate/reference.

Se viene inviata B:
- lasciare README su B.

Non fare una nuova riscrittura generale del README.

---

# 19. Documentazione

Creare:

```text
docs/versions/E11_X1_3_B3_fixed_3x3_epu_submission.md
```

Documentare:
1. fixed supervisor layout;
2. no geometry search;
3. post-realized-revenue land rule;
4. A0;
5. 5-episode result;
6. candidate decision;
7. artifact audit;
8. Kaggle submission metadata.

Aggiornare:
- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

---

# 20. Git

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

Non perdere tempo in tag/release.

Commit/push solo se già necessario nel normale workflow per conservare la submission; altrimenti fermarsi e riportare i comandi.

---

# Deliverable finale

Riportare in forma compatta:

1. B3 BUILD status
2. exact EPU coordinates
3. tests
4. A0 final money
5. A0 land purchase day
6. A0 EPU2 activation
7. A0 EPU3 activation
8. Stage B Mean/Median/Std/Min/Max
9. peak active tiles
10. peak workforce
11. A/B/B2R/B3 comparison
12. B3 candidate verdict
13. candidate actually packaged: B or B3
14. standalone artifact smoke
15. Kaggle submitted YES/NO
16. submission name
17. submission timestamp/id
18. initial Kaggle status/score
19. README status
20. files changed
21. next action

---

# STOP RULE

Questa è una sessione di chiusura rapida.

NON:
- cercare layout migliori;
- aggiungere crop tuning;
- fare 10/30 episodi;
- sviluppare EPU4;
- ottimizzare ulteriormente B3.

Obiettivo:

> **fixed layout → smoke → 5 episodes → choose B3 or B → build → submit.**
