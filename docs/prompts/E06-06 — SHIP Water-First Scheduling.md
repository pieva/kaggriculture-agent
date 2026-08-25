# E06-06 — SHIP Water-First Scheduling

Proseguiamo il progetto **Kaggriculture Agent** secondo il metodo sperimentale supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Le fasi E06 precedenti sono concluse:

- `E06-01 — DEFINE` → `GO`
- `E06-02 — PLAN` → `GO FOR BUILD`
- `E06-03 — BUILD` → `COMPLETED`
- `E06-04 — VERIFY` → `PASSED WITH METRIC CAVEAT`
- `E06-05 — REVIEW` → `SUPPORTED / SHIP CANDIDATE`

Procedi ora con:

# E06-06 — SHIP

---

# 1. Obiettivo

Consolidare e versionare l'esperimento:

`E06 — Water-First Scheduling`

Strategy:

`WaterFirstHIRENWClusterROIAgent`

come nuova baseline shipped del progetto.

La policy consolidata E06 è:

`WATER > HARVEST > PLANT`

rispetto alla baseline E05:

`HARVEST > PLANT > WATER`

---

# 2. Risultato sperimentale consolidato

## E05 baseline

- Mean Final Money: `$21568.93 ± $361.25`
- Median Final Money: `$21442.00`
- Total Weed Conversions: `176`
- Completion Rate: `100%`
- Disqualification Rate: `0%`
- Win Rate: `100%`

## E06

- Mean Final Money: `$24662.00 ± $1932.04`
- Median Final Money: `$25847.00`
- Min Final Money: `$22184.00`
- Max Final Money: `$27873.00`
- Total Weed Conversions: `70`
- Mean Weed Conversions: `2.33/episode`
- Mean Unwatered EOD Ratio: `8.11%`
- Completion Rate: `100%`
- Disqualification Rate: `0%`
- Win Rate: `100%`
- Agent Mean Turn Latency: `0.0822 ms/turn`

## Delta E06 vs E05

- Mean Final Money: `+$3093.07 / +14.34%`
- Median Final Money: `+$4405.00 / +20.54%`
- Weed Conversions: `-106 / -60.23%`

## Paired Evidence

- 30/30 valid pairs
- Mean Paired Money Delta: `+$3093.07 ± $1942.60`
- Median Paired Money Delta: `+$4405.00`
- Money Higher in E06: `29/30`
- Weeds Lower in E06: `30/30`

---

# 3. Verdict consolidato

Registrare:

- Experimental Integrity: `PASSED`
- Operational Result: `PARTIAL SUPPORT`
- Economic Result: `ECONOMIC IMPROVEMENT`
- Reliability: `PASSED`
- Hypothesis Verdict: `SUPPORTED`
- VERIFY: `PASSED WITH METRIC CAVEAT`
- SHIP Status: `PASSED`

Non modificare retroattivamente le soglie PLAN.

Non riclassificare le 70 weed come `STRONG SUCCESS`.

---

# 4. Metric Caveat

Conservare esplicitamente il caveat relativo a:

`Mean Unwatered End-of-Day Ratio = 8.11%`

La metrica:

- deve restare documentata;
- non deve essere cancellata;
- non deve essere considerata una misura affidabile della starvation reale per E06;
- non deve essere utilizzata come criterio primario per classificare E06.

Registrare che il campionamento a `hour == 23` può classificare come non irrigate tile appena seminate, introducendo un artefatto intra-day.

La redesign della metrica deve restare un'attività futura separata.

Non modificare ora il runner.

---

# 5. Correzione terminologica della causalità

Nei documenti finali E06 usare una formulazione metodologicamente corretta.

È accettabile affermare:

> Il confronto controllato E05/E06, basato su una singola modifica della scheduling policy, fornisce forte evidenza che Water-First sia responsabile del miglioramento complessivo osservato nel benchmark locale.

Evitare affermazioni del tipo:

> le 106 weed evitate hanno prodotto esattamente +$3093.07

oppure:

> ogni weed evitata equivale a X dollari.

Il nesso tra meno weed e maggiore capitale è coerente con il meccanismo economico dell'ambiente, ma non è stata effettuata una decomposizione causale quantitativa del delta monetario.

Se nei documenti E06 esistono formulazioni più forti, correggerle durante SHIP.

---

# 6. Standalone build finale

Aggiorna:

`submission/submission.py`

per includere la strategy shipped:

`WaterFirstHIRENWClusterROIAgent`

La standalone deve riprodurre la policy E06:

`WATER > HARVEST > PLANT`

senza dipendenze dal package locale.

Esegui quindi il processo di build standalone previsto dal repository.

---

# 7. Test finali pre-SHIP

Eseguire:

`.venv\Scripts\pytest tests/`

e registrare il risultato finale.

La suite deve essere completamente verde.

Verificare inoltre la standalone generata con i controlli già previsti dal repository.

Non procedere allo SHIP se:

- esistono test falliti;
- la standalone non è valida;
- E05 è stato accidentalmente modificato;
- il benchmark E06 non è preservato.

---

# 8. Preservazione artefatti

Verificare la presenza di:

- `docs/experiments/E06-01_Water_First_Capability_Analysis.md`
- `docs/plans/E06_Water_First_Scheduling.md`
- `docs/versions/E06_build_antigravity.md`
- `docs/versions/E06_verify_antigravity.md`
- `docs/versions/E06_review_antigravity.md`
- `results/e06_water_first.json`
- `src/agricola/strategy/water_first_hire_nw_cluster_roi.py`
- `tests/test_water_first_hire_nw_cluster.py`

Creare inoltre:

`docs/versions/E06_ship_antigravity.md`

---

# 9. Aggiornamenti documentali

Aggiorna:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`
- `docs/EXPERIMENT_LOG.md`
- `README.md`

Registrando E06 come:

`SHIPPED`

La progressione sperimentale deve diventare:

`E01 baseline → E02 ROI crop selection → E03 multi-tile scaling → E04 NW scaling → E05 HIRE multi-worker → E06 Water-First scheduling`

Registrare E06 come nuova baseline locale corrente.

---

# 10. Roadmap post-E06

Conservare nella documentazione le candidate future emerse dalla REVIEW, ordinate come segue:

1. `DIG / Weed Recovery`
2. `Dynamic Worker Partitioning`
3. `Dynamic Priority Scheduling`
4. `Multi-Hand Scaling`
5. `Metric Redesign`
6. eventuale `Further Spatial Scaling`

Non iniziare automaticamente E07.

La REVIEW E06 raccomanda come prima candidata:

`DIG / Weed Recovery`

ma deve essere rivalutata in una nuova fase DEFINE.

---

# 11. Git

Dopo aver completato documentazione, test e standalone:

eseguire:

`git status`

poi:

`git diff --stat`

quindi commit:

`git add .`

`git commit -m "Finalize E06 water-first scheduling experiment"`

eseguire:

`git push origin main`

Creare quindi il tag annotato:

`v0.6-e06-water-first`

con messaggio:

`E06 Water-First Scheduling validated and shipped`

e pubblicarlo:

`git push origin v0.6-e06-water-first`

---

# 12. Verifica finale Git

Al termine eseguire:

`git status`

e verificare:

- branch `main`;
- allineamento con `origin/main`;
- working tree clean.

Eseguire inoltre:

`git log -1 --oneline`

e:

`git tag --list`

---

# 13. Kaggle

**NON effettuare automaticamente una submission Kaggle durante SHIP.**

La standalone deve essere pronta, ma la submission ufficiale deve essere effettuata solo dopo nostra approvazione separata.

Non utilizzare eventuali risultati Kaggle per modificare retroattivamente il verdict locale E06.

---

# 14. Documento SHIP

Creare:

`docs/versions/E06_ship_antigravity.md`

con almeno:

1. Experiment Summary
2. Shipped Strategy
3. Experimental Progression
4. Final Local Benchmark
5. E05 vs E06
6. Paired Evidence
7. Operational Verdict
8. Economic Verdict
9. Reliability
10. Metric Caveat
11. Causal Interpretation
12. Final Hypothesis Verdict
13. SHIP Decision
14. Standalone Validation
15. Test Results
16. Final Artifacts
17. Git Commit
18. Git Tag
19. Future Candidates
20. Recommended Next Experiment

---

# 15. Output finale richiesto

Mostrami:

1. risultato finale E06;
2. verdict sperimentale;
3. risultati benchmark consolidati;
4. risultato test finale;
5. risultato standalone;
6. metric caveat;
7. file creati/modificati;
8. commit creato;
9. push;
10. tag `v0.6-e06-water-first`;
11. `git status`;
12. `git log -1 --oneline`;
13. `git tag --list`;
14. direzione raccomandata per E07.

**Fermati dopo SHIP. Non effettuare ancora submission Kaggle e non iniziare automaticamente E07.**