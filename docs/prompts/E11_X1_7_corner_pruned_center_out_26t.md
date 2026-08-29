# E11-X1.7 --- Corner-Pruned Center-Out EPU Scaling

## Mandato

Implementare e verificare **E11-X1.7 --- Corner-Pruned Center-Out EPU
Scaling** come evoluzione controllata di **E11-X1.6**.

L'obiettivo è verificare se il vantaggio di X1.6 deriva dal mantenimento
di un **core produttivo compatto e vicino all'origine**, evitando di
obbligare i worker a completare le tile marginali dei 4×4 che aumentano
il carico senza produrre sufficiente rendimento.

**Non reinterpretare la geometria. Le coordinate sotto sono
prescrittive.**

Il confronto principale è contro:

-   **E11-X1.6** --- Progressive Center-Out 3×3 → 4×4;
-   **B3** --- Fixed 3×3 3×EPU, score Kaggle **541.3**;
-   X1.4 e X1.5 solo come riferimenti locali secondari.

------------------------------------------------------------------------

# 1. Ipotesi

X1.6 ha ottenuto:

-   Mean Final Money: **\$27,508.20**
-   Median: **\$29,095**
-   Peak: **\$34,634**
-   Peak Active Productive Tiles: **26**
-   3 worker
-   BUY_LAND post-surplus
-   miglior media locale finora.

Pur avendo una geometria massima teorica di 32 tile, X1.6 ha raggiunto
un picco effettivo di **26 tile produttive**.

X1.7 deve verificare esplicitamente l'ipotesi:

> **26 tile non sono un 32-tile incompleto: possono essere il footprint
> produttivo ottimale.**

La nuova strategia deve quindi rendere **26 tile il target deliberato**,
usando due EPU center-out da **13 tile ciascuna**:

**9 → 13 → BUY_LAND → 22 → 26**

Gli angoli periferici del 4×4 vengono esclusi intenzionalmente.

------------------------------------------------------------------------

# 2. Sistema di coordinate

Coordinate **0-indexed**.

-   Q0: `x = 0..4`, `y = 0..4`
-   Q1: `x = 5..9`, `y = 0..4`
-   origine / shed: **(4,4)**

Non ruotare, traslare o rispecchiare il layout.

------------------------------------------------------------------------

# 3. Geometria prescrittiva

## EPU1 --- core 3×3 completo

``` python
EPU1_CORE_3X3 = [
    (2,2), (2,3), (2,4),
    (3,2), (3,3), (3,4),
    (4,2), (4,3), (4,4),
]
```

Tutte le 9 tile devono essere mantenute. In particolare **(2,2) NON deve
essere eliminata**.

## EPU1 --- estensione corner-pruned

Aggiungere soltanto:

``` python
EPU1_EXTENSION = [
    (1,3), (1,4),
    (3,1), (4,1),
]
```

Quindi:

``` python
EPU1_TARGET = EPU1_CORE_3X3 + EPU1_EXTENSION
```

Target EPU1 = **13 tile**.

Le tile periferiche del 4×4 non comprese nel target devono restare
inattive.

------------------------------------------------------------------------

## EPU2 --- core 3×3 completo

``` python
EPU2_CORE_3X3 = [
    (5,2), (5,3), (5,4),
    (6,2), (6,3), (6,4),
    (7,2), (7,3), (7,4),
]
```

Target iniziale EPU2 = **9 tile**.

## EPU2 --- estensione corner-pruned

Aggiungere soltanto:

``` python
EPU2_EXTENSION = [
    (5,1), (6,1),
    (8,3), (8,4),
]
```

Quindi:

``` python
EPU2_TARGET = EPU2_CORE_3X3 + EPU2_EXTENSION
```

Target EPU2 = **13 tile**.

------------------------------------------------------------------------

# 4. Invarianti geometrici obbligatori

Verificare automaticamente:

1.  `len(EPU1_CORE_3X3) == 9`
2.  `len(EPU1_TARGET) == 13`
3.  `len(EPU2_CORE_3X3) == 9`
4.  `len(EPU2_TARGET) == 13`
5.  `EPU1_CORE_3X3 ⊂ EPU1_TARGET`
6.  `EPU2_CORE_3X3 ⊂ EPU2_TARGET`
7.  `EPU1_TARGET ∩ EPU2_TARGET == ∅`
8.  EPU1 interamente in Q0.
9.  EPU2 interamente in Q1.
10. Target complessivo = **26 tile**.
11. **EPU3 DISABLED.**
12. Nessuna tile diversa dalle 26 prescritte deve entrare nel productive
    target.

Se uno degli invarianti fallisce: **STOP**.

------------------------------------------------------------------------

# 5. Progressione produttiva

La progressione deve essere:

### Fase P1

Attivare **EPU1 core 3×3 = 9 tile**.

Preservare il meccanismo produttivo E06/X1.6:

-   `WATER > HARVEST > PLANT`
-   crop selection dinamica ROI/day;
-   seed buying on-demand;
-   immediate shed liquidation;
-   workforce workload-driven;
-   nessuna espansione fondiaria prematura.

### Fase P2

Quando capitale e workload lo consentono, espandere EPU1:

**9 → 13 tile**

usando esclusivamente `EPU1_EXTENSION`.

Non completare il 4×4.

### Fase P3

Acquistare Q1 **solo post-surplus**, con la stessa disciplina economica
validata da X1.6.

Vincoli:

-   **NO Day-0 BUY_LAND**
-   nessun giorno hardcoded;
-   trigger economico runtime;
-   preservare operating reserve;
-   evitare working-capital starvation.

### Fase P4

Dopo l'acquisto di Q1 attivare:

**EPU2 core 3×3 = 9 tile**

Portando il target complessivo:

**13 + 9 = 22 tile**

### Fase P5

Se workload e capitale lo consentono, attivare:

`EPU2_EXTENSION`

Portando il target massimo a:

**13 + 13 = 26 tile**

### Divieto

**NON attivare EPU3. NON espandere oltre 26 tile.**

Questo esperimento deve isolare l'effetto del corner pruning.

------------------------------------------------------------------------

# 6. Workforce

Non imporre un numero di worker solo per raggiungere il footprint.

Il workforce deve restare **workload-driven**, ma deve essere misurato
esplicitamente.

Registrare almeno:

-   workforce per giorno;
-   peak simultaneous workers;
-   active productive tiles;
-   active tiles / worker;
-   productive actions / worker;
-   MOVE actions;
-   WATER / HARVEST / PLANT;
-   MOVE / productive-action ratio.

Obiettivo: verificare se 26 tile compatte consentono ai 3 worker di X1.6
di produrre più efficacemente eliminando le 6 tile marginali del 32-tile
theoretical footprint.

------------------------------------------------------------------------

# 7. Implementazione

## Core strategy

Modificare:

`src/agricola/strategy/productive_mass_roi.py`

Aggiungere una modalità/configurazione chiaramente identificabile, per
esempio:

``` python
productive_core_mode = "EPU_CORNER_PRUNED_CENTER_OUT"
epu_level = 2
max_productive_tiles = 26
enable_epu3 = False
```

Non alterare il comportamento delle configurazioni storiche B3, X1.4,
X1.5 e X1.6.

------------------------------------------------------------------------

# 8. Test

Aggiornare:

`tests/test_e11_productive_mass.py`

Aggiungere test per:

-   coordinate esatte;
-   cardinalità 9/13/9/13;
-   disjointness;
-   Q0/Q1 containment;
-   total target = 26;
-   EPU3 disabled;
-   nessuna tile esterna al target;
-   progressione 9 → 13 → 22 → 26;
-   no Day-0 land purchase;
-   preservazione invarianti E06;
-   configurazioni precedenti non modificate.

Eseguire:

``` powershell
.venv\Scripts\pytest.exe tests/
```

Tutti i test devono passare prima del benchmark.

------------------------------------------------------------------------

# 9. Benchmark X1.7

Creare:

`scripts/benchmark_e11_x1_7.py`

## Stage A0

Seed 0 vs `pass`, 720 step.

Verificare:

-   geometria;
-   ordine di attivazione;
-   land purchase;
-   workforce;
-   peak active tiles;
-   final money;
-   nessuna tile non prescritta.

Se errore strutturale: STOP.

## Stage B

Usare **gli stessi identici 5 paired episodes** già usati per X1.6:

    Seed Opponent
  ------ ----------
       0 pass
     100 pass
     200 random
     300 random
     400 starter

Nessuna sostituzione di seed o opponent.

------------------------------------------------------------------------

# 10. Confronto obbligatorio

Produrre tabella paired:

  Seed     B3   X1.4   X1.5   X1.6   X1.7 Winner
  ------ ---- ------ ------ ------ ------ --------

Per X1.7 calcolare:

-   Mean Final Money
-   Median
-   Std (`ddof=1`)
-   Min
-   Max
-   paired wins vs X1.6
-   paired wins vs B3
-   delta assoluto e percentuale vs X1.6
-   delta assoluto e percentuale vs B3.

Riferimenti X1.6:

-   Mean: **\$27,508.20**
-   Median: **\$29,095**
-   Peak: **\$34,634**
-   Peak active productive tiles: **26**

Riferimento Kaggle B3:

-   **Score: 541.3**

Non confondere score Kaggle e final money locale.

------------------------------------------------------------------------

# 11. Diagnostica specifica

Il report deve rispondere esplicitamente:

1.  X1.7 raggiunge realmente 26 tile?
2.  Quanto tempo passa a 9, 13, 22 e 26 tile?
3.  Quali tile erano responsabili del mancato completamento del 32t in
    X1.6?
4.  Eliminare gli angoli aumenta le productive actions per worker?
5.  Diminuisce `MOVE/productive-action`?
6.  Migliora il cash disponibile durante l'espansione?
7.  EPU2 viene attivata prima, uguale o dopo X1.6?
8.  Il pruning aumenta il floor sui seed 300/400?
9.  Mantiene o supera il ceiling di X1.6?
10. Il 26-tile footprint appare economicamente saturo oppure esiste
    ancora capacità per una successiva espansione?

------------------------------------------------------------------------

# 12. Decision rule

Dopo Stage B classificare X1.7:

### `CLEAR WINNER`

se:

-   mean \> X1.6,
-   e paired wins vs X1.6 ≥ 3/5,
-   senza grave regressione del floor.

### `PROMISING`

se:

-   mean circa equivalente a X1.6,
-   ma minore varianza / floor migliore / maggiore efficienza operativa.

### `NOT BETTER`

se:

-   mean inferiore,
-   senza compensazione significativa in stabilità o produttività.

------------------------------------------------------------------------

# 13. Submission Kaggle

Se Stage A0 e Stage B sono strutturalmente validi, **preparare comunque
X1.7 come submission Kaggle**, perché vogliamo una validazione esterna
rapida della nuova geometria.

Aggiornare `scripts/build_submission.py` in modo che il bundle
standalone usi esattamente X1.7.

Generare:

`submission/submission.py`

Eseguire:

1.  test standalone;
2.  smoke test 720 step;
3.  semantic-equivalence check source ↔ standalone almeno su seed 0;
4.  verificare:
    -   Final Money identico;
    -   BUY_LAND day/step identico;
    -   activation milestones identici;
    -   peak workforce identico;
    -   peak active tiles identico.

**Non dichiarare READY se l'equivalenza non è 100%.**

Nome submission:

`E11-X1.7 Corner-Pruned Center-Out 26t`

------------------------------------------------------------------------

# 14. Documentazione

Creare:

`docs/versions/E11_X1_7_corner_pruned_center_out_26t.md`

Aggiornare:

-   `docs/PROJECT_STATE.md`
-   `docs/EXPERIMENT_LOG.md`
-   `docs/NEW_SESSION.md`
-   `README.md` solo se necessario per riflettere il nuovo candidato
    corrente.

Registrare provenance e SHA-256 dei risultati.

------------------------------------------------------------------------

# 15. Output finale obbligatorio

Al termine restituire:

1.  test result;
2.  coordinate finali effettivamente usate;
3.  Stage A0;
4.  Stage B 5-seed table;
5.  confronto B3 / X1.4 / X1.5 / X1.6 / X1.7;
6.  milestone 9 → 13 → 22 → 26 per episodio;
7.  workforce telemetry;
8.  movement/productivity telemetry;
9.  capital/land-purchase telemetry;
10. verdict `CLEAR WINNER / PROMISING / NOT BETTER`;
11. semantic-equivalence verdict;
12. percorso di `submission/submission.py`;
13. nome esatto della submission Kaggle.

## STOP

Dopo avere generato e verificato il bundle standalone, **non avviare
ulteriori esperimenti**. Fermarsi e attendere la validazione Kaggle del
supervisore.
