# E05-06 — SHIP HIRE / Multi-Worker Scaling

Stiamo concludendo **E05 — HIRE / Multi-Worker Scaling** del progetto Kaggriculture Agent.

Segui rigorosamente il metodo di progetto:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Sono state completate:

- **DEFINE:** `docs/experiments/E05-01_HIRE_Capability_Analysis.md`
- **PLAN:** `docs/plans/E05_HIRE_MultiWorker_Scaling.md`
- **BUILD:** `docs/versions/E05_build_antigravity.md`
- **VERIFY:** `docs/versions/E05_verify_antigravity.md`
- **REVIEW:** `docs/versions/E05_review_antigravity.md`

La REVIEW ha concluso:

- `ECONOMIC HYPOTHESIS SUPPORTED`
- `STARVATION REDUCED BUT UNRESOLVED`
- Worker Capacity Bottleneck: `STRONGLY SUPPORTED`
- Esperimento: `STRONG SUCCESS`
- Internal Validity: `HIGH`
- External Validity: `MEDIUM`
- SHIP Readiness: `READY FOR SHIP`

Questo prompt riguarda **esclusivamente la fase SHIP**.

Non modificare la strategia E05.

Non effettuare ulteriori tuning.

Non eseguire nuovi benchmark salvo controllo finale strettamente necessario.

---

## 1. Obiettivo SHIP

Consolidare E05 come iterazione sperimentale completata e riproducibile.

SHIP deve:

1. verificare lo stato finale del codice;
2. verificare test e standalone submission;
3. consolidare la documentazione E05;
4. aggiornare lo stato complessivo del progetto;
5. preservare i risultati storici E01–E04;
6. creare il commit finale E05;
7. effettuare push su `main`;
8. creare e pubblicare il tag E05.

SHIP consolida **il risultato sperimentale osservato**, non una strategia perfetta.

La presenza di 176 Weed Conversions residue non impedisce SHIP perché il failure mode è stato correttamente identificato e documentato.

---

## 2. Risultato E05 da consolidare

### Strategia

`HIRENWClusterROIAgent`

### Configurazione

- footprint NW da 9 tile;
- 1 farmer principale;
- 1 farm hand giornaliera tramite `HIRE`;
- costo `$1/giorno`;
- 30 HIRE per episodio;
- partizionamento fisso 4:5;
- policy invariata:
  `HARVEST > PLANT > WATER`;
- no `DIG`;
- no `BUY_LAND`;
- no Water-First;
- nessun dynamic worker balancing.

### Benchmark verificato

- Total Episodes: `30`
- Completion Rate: `100.00%`
- Disqualification Rate: `0.00%`
- Overall Win Rate: `100.00%`
- Mean Final Money: **`$21568.93 ± $361.25`**
- Median Final Money: **`$21442.00`**
- Min / Max: `$21282.00 / $22867.00`
- Agent Mean Turn Latency: `0.0924 ms/turn`

### Confronto E04

E04:

`$11232.47 ± $661.26`

E05:

- delta assoluto: **`+$10336.46`**
- delta percentuale: **`+92.02%`**

### Confronto E03

E03:

`$14682.47 ± $1164.33`

E05:

- delta assoluto: **`+$6886.46`**
- delta percentuale: **`+46.90%`**

### Operational diagnostics

- E04 Weed Conversions: `238`
- E05 Weed Conversions: `176`
- variazione: `-62`
- riduzione: `-26.05%`
- Mean Unwatered End-of-Day Ratio:
  - E04: `3.33%`
  - E05: `3.33%`

---

## 3. Interpretazione finale da preservare

E05 è un:

`STRONG SUCCESS`

sulla domanda sperimentale economica.

La conclusione deve distinguere chiaramente:

### Supportato

> L'introduzione di una farm hand giornaliera tramite `HIRE`, coordinata tramite partizionamento fisso 4:5, rende il footprint NW da 9 tile economicamente sostenibile e nettamente superiore sia a E04 sia a E03.

### Fortemente supportato

> I risultati supportano fortemente l'interpretazione secondo cui la capacità operativa del singolo farmer costituiva un importante fattore limitante nella configurazione E04.

Non formulare questa conclusione come dimostrazione assoluta che **tutto** il delta E04→E05 sia causato esclusivamente dalla capacità del worker, perché il trattamento richiede anche il partitioning 4:5 come meccanismo di coordinamento.

### Non risolto

> E05 non elimina il failure mode di water starvation.

Le Weed Conversions diminuiscono:

`238 → 176`

ma persistono.

Il Mean Unwatered End-of-Day Ratio resta:

`3.33% → 3.33%`

La classificazione operativa finale deve quindi restare:

`STARVATION REDUCED BUT UNRESOLVED`

---

## 4. Correzioni editoriali obbligatorie prima di SHIP

Rivedi `docs/versions/E05_review_antigravity.md` e correggi, se presenti, formulazioni eccessivamente causali.

### Evitare

> La capacità del singolo farmer era con certezza la causa primaria di E04.

### Preferire

> I risultati supportano fortemente l'interpretazione secondo cui la capacità del singolo farmer costituiva un fattore limitante primario nella configurazione E04.

Inoltre, se il costo HIRE `$30/episodio` viene descritto come percentuale dei **ricavi lordi**, correggi la formulazione salvo che il repository disponga effettivamente di una metrica formalmente definita di gross revenue.

Puoi riportare invece:

> `$30/episodio`, pari a circa lo `0.14%` del Mean Final Money E05.

Non modificare i risultati numerici.

---

## 5. Verifica finale degli artifact E05

Conferma l'esistenza e coerenza di:

### DEFINE

`docs/experiments/E05-01_HIRE_Capability_Analysis.md`

### PLAN

`docs/plans/E05_HIRE_MultiWorker_Scaling.md`

### Prompt

Verifica che siano presenti almeno:

- `docs/prompts/E05-01 ...`
- `docs/prompts/E05-02 ...`
- `docs/prompts/E05-03 ...`
- `docs/prompts/E05-03B ...`
- `docs/prompts/E05-04 ...`
- prompt REVIEW E05, se salvato nel workflow corrente;
- prompt SHIP E05, se previsto dalle convenzioni del repository.

Non rinominare arbitrariamente file già tracciati.

### BUILD

`docs/versions/E05_build_antigravity.md`

### VERIFY

`docs/versions/E05_verify_antigravity.md`

### REVIEW

`docs/versions/E05_review_antigravity.md`

### Risultati

`results/e05_hire_multiworker.json`

### Strategia

`src/agricola/strategy/hire_nw_cluster_roi.py`

### Test

`tests/test_hire_nw_cluster.py`

### Standalone

`submission/submission.py`

---

## 6. Verifica isolamento degli artifact storici

Conferma che gli artifact E01–E04 non siano stati modificati accidentalmente.

In particolare verifica:

`results/e01_baseline.json`

e gli eventuali file risultati E02–E04.

La modifica infrastrutturale a:

`scripts/run_eval.py`

che cambia il default di output in:

`results/latest_eval.json`

è parte legittima di E05 perché impedisce future sovrascritture accidentali dei risultati storici.

Documentala nello SHIP report.

---

## 7. Test suite finale

Esegui:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Il risultato atteso dalla BUILD è:

`25 passed`

Se la suite non passa integralmente:

**FERMATI.**

Non effettuare commit/tag finché la regressione non è risolta.

---

## 8. Standalone build finale

Esegui:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
```

Verifica che:

- `submission/submission.py` venga generato;
- il standalone test passi;
- `HIRENWClusterROIAgent` sia effettivamente l'agente entrypoint;
- non esistano dipendenze locali non incluse.

Non rieseguire il benchmark da 30 episodi se il risultato E05 già verificato è integro.

---

## 9. Documento SHIP

Crea:

`docs/versions/E05_ship_antigravity.md`

Il documento deve contenere almeno:

1. **Obiettivo SHIP**
2. **Strategia consolidata**
3. **Configurazione E05**
4. **Risultato benchmark**
5. **Confronto vs E04**
6. **Confronto vs E03**
7. **Risultato economico**
8. **Risultato operativo**
9. **Worker Capacity interpretation**
10. **Starvation residuale**
11. **Test finali**
12. **Standalone build**
13. **Artifact isolation**
14. **File E05 consolidati**
15. **Modifica infrastrutturale `run_eval.py`**
16. **Limiti dell'esperimento**
17. **Candidate directions successive**
18. **Direzione raccomandata dalla REVIEW**
19. **Stato Git**
20. **SHIP Decision**

La decisione finale prevista, se tutti i controlli passano, è:

`SHIP PASSED`

---

## 10. Aggiornamento EXPERIMENT_LOG

Individua il file di log sperimentale corrente del progetto, presumibilmente:

`docs/EXPERIMENT_LOG.md`

oppure il percorso effettivamente utilizzato nel repository.

Aggiungi E05 mantenendo lo stile delle iterazioni precedenti.

Registra almeno:

- `E05 — HIRE / Multi-Worker Scaling`
- `HIRENWClusterROIAgent`
- 9 tile;
- 1 farmer + 1 farm hand giornaliera;
- Mean Final Money `$21568.93 ± $361.25`;
- Median `$21442.00`;
- `+92.02%` vs E04;
- `+46.90%` vs E03;
- Weed Conversions `176`;
- `-26.05%` vs E04;
- Completion `100%`;
- Disqualification `0%`;
- Win Rate `100%`;
- Economic Hypothesis: `SUPPORTED`;
- Starvation: `REDUCED BUT UNRESOLVED`;
- Experiment: `STRONG SUCCESS`.

Non modificare retroattivamente i risultati E01–E04.

---

## 11. Aggiornamento PROJECT_STATE

Aggiorna il file di stato corrente del progetto, se presente:

`PROJECT_STATE.md`

oppure il percorso effettivo.

Deve risultare chiaramente che:

- E05 è concluso;
- E05 è shipped;
- E05 è il miglior risultato economico locale corrente;
- il Mean Final Money corrente migliore è:
  **`$21568.93 ± $361.25`**;
- il problema di starvation non è risolto;
- rimangono 176 Weed Conversions nel benchmark;
- la scelta di E06 **non è ancora stata effettuata**.

---

## 12. Aggiornamento NEW_SESSION

Aggiorna:

`NEW_SESSION.md`

mantenendolo come documento operativo per la prossima sessione.

Deve includere una progressione sintetica:

`E01 → E02 → E03 → E04 → E05`

con almeno:

### E04

- 9 tile;
- 1 farmer;
- `$11232.47 ± $661.26`;
- `FALSIFIED`.

### E05

- 9 tile;
- 1 farmer + 1 daily HIRE;
- `$21568.93 ± $361.25`;
- `+92.02% vs E04`;
- `+46.90% vs E03`;
- 176 Weed Conversions;
- `STARVATION REDUCED BUT UNRESOLVED`;
- `STRONG SUCCESS`.

Il punto di partenza della sessione successiva deve essere:

> **E05 è concluso e shipped. Non iniziare automaticamente E06. Valutare prima le direzioni candidate emerse dalla REVIEW.**

Elenca le candidate senza sceglierne automaticamente una:

1. Water-First Scheduling con HIRE;
2. DIG / Weed Recovery con HIRE;
3. Worker Allocation / Partitioning;
4. Additional HIRE;
5. Further Spatial Scaling.

Indica che la REVIEW considera **Water-First con HIRE** la direzione attualmente più informativa, ma che la scelta E06 deve essere effettuata esplicitamente nella prossima sessione.

---

## 13. Aggiornamento README

Valuta se il `README.md` contiene lo stato o i risultati correnti degli esperimenti.

Se sì, aggiorna solo le parti necessarie per includere E05.

Non effettuare una riscrittura generale del README.

Il README deve essere coerente con:

- E05 shipped;
- best local Mean Final Money:
  `$21568.93 ± $361.25`;
- strategia:
  `HIRENWClusterROIAgent`.

---

## 14. Controllo delle candidate E06

Nel documento SHIP conserva le candidate emerse dalla REVIEW:

### A — Water-First Scheduling con HIRE

Variabile:

priorità di irrigazione.

Obiettivo:

ridurre/eliminare le 176 Weed Conversions residue mantenendo il vantaggio economico E05.

### B — DIG / Weed Recovery con HIRE

Variabile:

recovery delle tile convertite in WEED.

### C — Worker Allocation / Partitioning

Variabile:

allocazione delle 9 tile fra farmer e hand.

### D — Additional HIRE

Variabile:

seconda farm hand.

### E — Further Spatial Scaling

Variabile:

footprint > 9 tile.

Non creare documenti PLAN E06.

Non implementare E06.

---

## 15. Git pre-commit verification

Prima del commit esegui:

```powershell
git status
git diff --stat
```

Verifica che:

- tutti gli artifact E05 attesi siano presenti;
- non esistano file temporanei indesiderati;
- gli artifact E01–E04 siano preservati;
- nessun file esterno all'esperimento sia stato modificato senza motivazione.

Se emergono anomalie, risolvile prima del commit.

---

## 16. Commit E05

Se tutti i controlli precedenti passano:

```powershell
git add .
git commit -m "Finalize E05 HIRE multi-worker scaling experiment"
```

Se il repository richiede una diversa convenzione di commit coerente con E01–E04, utilizza quella convenzione mantenendo chiaramente `E05` e `HIRE`.

---

## 17. Push

Esegui:

```powershell
git push origin main
```

Verifica che il push completi con successo.

---

## 18. Tag E05

Crea un tag annotato coerente con la progressione esistente.

Tag previsto:

`v0.5-e05-hire-multiworker`

Messaggio:

`E05 HIRE Multi-Worker Scaling validated and shipped`

Esegui:

```powershell
git tag -a v0.5-e05-hire-multiworker -m "E05 HIRE Multi-Worker Scaling validated and shipped"
git push origin v0.5-e05-hire-multiworker
```

Prima della creazione verifica che il tag non esista già.

---

## 19. Verifica post-SHIP

Dopo push e tag esegui:

```powershell
git status
git log -1 --oneline
git tag --list
```

Lo stato finale richiesto è:

- branch `main`;
- `main` allineato con `origin/main`;
- working tree clean;
- commit E05 presente;
- tag `v0.5-e05-hire-multiworker` presente.

---

## 20. Decisione finale SHIP

Se tutti i controlli sono superati, registra:

- Test Suite: `PASSED`
- Standalone Build: `PASSED`
- Experimental Integrity: `PASSED`
- Economic Hypothesis: `SUPPORTED`
- Starvation: `REDUCED BUT UNRESOLVED`
- Experiment: `STRONG SUCCESS`
- SHIP Status: `PASSED`

Non dichiarare:

`STARVATION RESOLVED`

Non dichiarare che 4:5 è ottimale.

Non dichiarare che una hand è il numero ottimale.

---

## 21. Condizione finale

Al termine mostra:

1. risultato dei test;
2. risultato standalone build;
3. sintesi finale E05;
4. Mean Final Money;
5. delta vs E04;
6. delta vs E03;
7. Weed Conversions;
8. stato starvation;
9. file SHIP creato;
10. file di stato/documentazione aggiornati;
11. commit hash e messaggio;
12. esito push;
13. tag creato e pubblicato;
14. `git status`;
15. `git log -1 --oneline`;
16. lista dei tag.

Concludi esplicitamente con:

`E05 SHIPPED`

e poi **FERMATI**.

Non iniziare E06.

Non creare il PLAN E06.

La scelta della prossima direzione sperimentale avverrà nella sessione successiva.