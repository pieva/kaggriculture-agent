# E11-X1 — BUILD + VERIFY — Verified 3Q Capital Accumulation

## Contesto

La nuova e unica baseline quantitativa autorevole è **E11-VB1 — Verified Baseline 1** (`E11-VB1-20260827-084428`), con provenance verifier PASS, config snapshot, raw episode records, summary e SHA-256 verificati.

Baseline macchina:

- Mean Final Money: **$429.00**
- 3Q / 75 tile unlock: **0 / 30**
- 4Q / 100 tile unlock: **0 / 30**
- Peak land: **50 tile / 2Q**
- Mean / Peak active tiles: **16.93 / 17**
- Mean / Peak workforce: **2 / 2**
- Livestock: **OFF**

Il primo gap verificato è **Expansion Capital Protection Deadlock**: dopo il primo acquisto territoriale la cassa scende a circa `$899`, la produzione essenziale continua a consumare capitale e il cash non raggiunge più la soglia necessaria per il successivo `BUY_LAND`.

Il benchmark competitor indipendentemente validato mostra invece:

- 3Q / 75 tile: Mean Day **4.20**
- 4Q / 100 tile: Mean Day **8.53**
- workforce @75: **4–6**
- workforce @100: **8–10**
- active tiles @75: **35–45**
- active tiles @100: **75–85**
- livestock activation: **Day 9–12**

E11-X1 deve affrontare esclusivamente il primo salto:

> **2Q / 50 tile → 3Q / 75 tile**

## 1. Obiettivo

Procedere con **E11-X1 — Verified 3Q Capital Accumulation**.

Domanda sperimentale:

> **Quale politica minima di accumulo e spesa permette a E11-VB1 di finanziare e completare il passaggio da 50 a 75 tile senza interrompere la produzione essenziale necessaria a generare il capitale?**

E11-X1 NON deve ancora cercare di raggiungere 100 tile, scalare workforce a 8–10, attivare livestock, ottimizzare il crop portfolio o raggiungere $50k/$75k.

## 2. Principio sperimentale

E11-X1 deve essere un trattamento controllato rispetto a E11-VB1.

Modificare una sola area:

> **essential spending vs next-land capital accumulation**

Mantenere invariati land readiness, workforce, locality, livestock, crop catalog, action hierarchy, end-game, environment, benchmark seeds e opponent set.

Non riaprire le policy sintetiche o non verificate della vecchia catena E11-03…E11-06.

## 3. Controlled Change

Intervenire esclusivamente sulla gestione della spesa durante **ACCUMULATE_3Q**.

Distinguere almeno:

- **Essential production spending**: indispensabile per mantenere una capacità produttiva minima.
- **Deferrable spending**: rinviabile senza bloccare la farm e potenzialmente impeditiva del raggiungimento della soglia land.

Non introdurre soglie arbitrarie (`$800`, `$850`, `$950`) solo perché comparse negli audit precedenti. Se serve un parametro, deve derivare da land cost, operating reserve, seed cost, inventory, active tiles e harvest horizon ed essere documentato come ipotesi X1.

## 4. Capital Gap

Calcolare e registrare esplicitamente:

`capital_gap_to_3q`

come differenza tra capitale necessario per `BUY_LAND` + buffer operativo e cash effettivamente disponibile.

## 5. Land Purchase

Quando capital readiness, minimum operational readiness e remaining horizon sono soddisfatti, `BUY_LAND` 3Q deve essere eseguito senza ritardi strategici non necessari.

La metrica primaria è:

> **3Q Unlock Rate**

Baseline E11-VB1: **0%**.

E11-X1 deve produrre **3Q Unlock Rate > 0%** come requisito minimo.

Il timing competitor Day 4.20 è riferimento competitivo, non soglia rigida X1.

## 6. Productive Stability

L'espansione non deve essere ottenuta distruggendo completamente la farm.

Registrare active tiles prima/dopo 3Q, cash post-acquisto, workforce e final money.

## 7. Protocollo di benchmark ridotto

Da E11-X1 in avanti NON rieseguire sistematicamente tutte le versioni precedenti.

Confronto ordinario:

- **E11-VB1**
- **E11-X1**

Non eseguire E05/E06/E08/E09/E10 o vecchie E11 salvo specifica necessità diagnostica.

### Stage A — Smoke Test
**1 episodio**

Scopo: legality, telemetry, provenance, possibilità di 3Q.

### Stage B — Mini Verification
**5 episodi appaiati**

Scopo: verificare se il trattamento modifica realmente il comportamento e se 3Q viene raggiunto.

### Stage C — Standard Iteration Benchmark
**10 episodi appaiati**

Questo diventa il benchmark standard per le normali iterazioni E11-Xn.

**NON eseguire automaticamente 30 episodi.**

## 8. Benchmark da 30 episodi

Il benchmark da 30 episodi diventa un gate di validazione/milestone, non il default.

In questo task:

> **1 → 5 → 10 e STOP**

Eseguire 30 episodi solo in un task successivo, se X1 supera il gate architetturale nei 10 episodi e il supervisore approva.

## 9. Seed protocol ridotto

Definire e congelare un subset stabile di 10 episodi, mantenendo rappresentati gli opponent (ad esempio 4 pass, 3 random, 3 starter o struttura equivalente).

Salvare esplicitamente seed/opponent nel config snapshot e riutilizzare lo stesso subset per i benchmark rapidi successivi.

## 10. E10 control

E10 resta controllo storico verificato.

NON rieseguirlo a ogni treatment.

Rieseguirlo solo se cambia l'ambiente o l'infrastruttura benchmark, emerge un sospetto di regressione tecnica o si prepara una milestone importante.

## 11. Provenance protocol obbligatorio

E11-X1 deve usare esattamente il protocollo R3:

`CONFIG SNAPSHOT → RUN ID → RAW EPISODES → SUMMARY → SHA-256 → PROVENANCE VERIFIER`

Nessun benchmark è valido senza **Provenance PASS**.

Creare:

`results/e11/<RUN_ID>/config.json`
`results/e11/<RUN_ID>/episodes.json`
`results/e11/<RUN_ID>/summary.json`

Non sovrascrivere E11-VB1 o altri treatment.

Run ID:

`E11-X1-<timestamp>`

## 12. Config Delta

Il delta E11-VB1 → E11-X1 deve essere esplicitamente ricostruibile.

Produrre nel report una tabella:

| Parameter | VB1 | X1 |
|---|---|---|

Non devono esistere differenze non documentate.

## 13. Telemetria X1

Per ogni episodio registrare almeno:

- run_id
- variant_id
- seed
- opponent
- final money
- completion
- disqualification
- 3Q unlock
- 3Q timing
- peak land
- peak active tiles
- workforce
- cash trajectory
- capital gap to 3Q
- seed inventory
- seed spending
- harvestable tiles
- next-land readiness
- blocked spending events
- BUY_LAND event
- checkpoint telemetry

## 14. Test

Estendere la suite e testare almeno:

1. E11-VB1 factory invariata.
2. E11-X1 config distinta.
3. X1 modifica solo la spending policy autorizzata.
4. Essential spending consentita.
5. Deferrable spending bloccata quando necessario.
6. Operating reserve rispettata.
7. Land readiness invariata.
8. Workforce invariata.
9. Livestock invariato.
10. `BUY_LAND` 3Q eseguibile.
11. Config non mutata runtime.
12. Provenance schema valido.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

## 15. Stop Gate progressivo

### Stage A
Se crash, illegal action, telemetry incompleta o provenance failure: correggere il problema tecnico.

### Stage B
Se X1 = **0/5 a 3Q** e la trace mostra lo stesso deadlock: **STOP**. Non eseguire Stage C.

### Stage C
Solo se Stage B mostra cambiamento reale, eseguire **10 episodi appaiati**.

Confrontare:

| Metric | E11-VB1 | E11-X1 |
|---|---:|---:|
| 3Q unlock | | |
| 3Q mean day | | |
| Final Money | | |
| Peak active | | |
| Peak workforce | | |
| Completion | | |
| DQ | | |

## 16. Criteri X1

- **X1 NOT VALIDATED**: 3Q = 0/10 o comportamento sostanzialmente identico a VB1.
- **X1 PARTIAL**: alcuni episodi raggiungono 3Q, comportamento instabile.
- **X1 VALIDATED**: 3Q raggiunto ripetutamente, farm operativa, provenance valida.

Non richiedere ancora 4Q.

## 17. Target strategici

I target E11 restano:

- Minimum Success: **$50k**
- Competitive Target: **$75k**

Ma NON usarli come gate di X1.

X1 è un esperimento architetturale sul primo land unlock.

## 18. Deliverable

Creare:

`docs/versions/E11_X1_verified_3q_capital_accumulation.md`

Struttura minima:

1. Executive Summary
2. E11-VB1 Baseline
3. Verified Gap
4. H11-X1
5. Controlled Change
6. Config Delta
7. 3Q Accumulation Logic
8. Essential vs Deferrable Spending
9. Telemetry
10. Provenance Protocol
11. Tests
12. Stage A
13. Stage B
14. Stage C
15. 3Q Unlock Results
16. Timing
17. Productive Stability
18. Economic Diagnostics
19. Provenance Verification
20. X1 Verdict
21. 30-Episode Validation Recommendation
22. Next Step

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato finale:

> **E11-X1 BUILD + REDUCED LOCAL VERIFY COMPLETED — awaiting supervisor review**

Non dichiarare X1 nuova baseline finché non viene eventualmente validata su 30 episodi.

## 19. Git

Alla fine:

`git status`
`git diff --stat`
`git diff --check`

NON effettuare commit, tag, push o Kaggle submission.

## 20. Deliverable finale obbligatorio

Riportare:

1. E11-X1 BUILD status
2. run_id
3. controlled change
4. config delta VB1 → X1
5. test suite result
6. Stage A result
7. Stage B episode count
8. Stage B 3Q unlock
9. Stage C executed YES/NO
10. Stage C episode count
11. VB1 3Q unlock
12. X1 3Q unlock
13. X1 3Q mean timing
14. competitor 3Q timing reference
15. peak land
16. peak active tiles
17. peak workforce
18. Mean Final Money
19. Median / Std / Min / Max
20. productive stability verdict
21. capital-gap telemetry
22. provenance verifier result
23. config SHA-256
24. episodes SHA-256
25. X1 validation verdict
26. 30-episode validation recommended YES/NO
27. file creati/modificati
28. next-step recommendation

# Regola operativa futura

Da questo momento il protocollo standard E11 è:

> **1 episodio smoke → 5 episodi mini → 10 episodi standard → 30 episodi solo per milestone/validazione**

e il confronto ordinario è:

> **baseline verificata corrente vs treatment corrente**

Non rieseguire tutte le versioni storiche a ogni iterazione.

Ogni run deve comunque conservare:

> **raw records + config snapshot + hash + provenance PASS.**
