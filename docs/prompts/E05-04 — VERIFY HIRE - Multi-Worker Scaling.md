# E05-04 — VERIFY HIRE / Multi-Worker Scaling

Stiamo proseguendo **E05 — HIRE / Multi-Worker Scaling** del progetto Kaggriculture Agent.

Segui rigorosamente il metodo di progetto:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Sono state completate e approvate:

- **DEFINE:** `docs/experiments/E05-01_HIRE_Capability_Analysis.md`
- **PLAN:** `docs/plans/E05_HIRE_MultiWorker_Scaling.md`
- **BUILD:** `docs/versions/E05_build_antigravity.md`

La BUILD è stata completata con esito positivo:

- `25/25` test passati;
- standalone submission generata e verificata;
- smoke test completato con `100%` Completion Rate;
- `0%` Disqualification Rate;
- 30 `HIRE` osservati in 30 giorni;
- artifact storici E01–E04 preservati;
- output E05 isolato in un file risultati dedicato.

Questo prompt riguarda **esclusivamente la fase VERIFY**.

Non effettuare ancora REVIEW.

Non effettuare SHIP.

Non creare commit finale, push o tag Git.

---

## 1. Obiettivo della VERIFY

Verificare sperimentalmente se:

> **L'aggiunta giornaliera di una farm hand tramite `HIRE` rende economicamente sostenibile il footprint NW da 9 tile che in E04 aveva mostrato una regressione economica rispetto a E03.**

La VERIFY deve produrre evidenze quantitative riproducibili.

Non modificare la strategia in base ai risultati osservati.

Non effettuare tuning durante il benchmark.

---

## 2. Configurazione sperimentale da verificare

### Agente E05

`HIRENWClusterROIAgent`

### Footprint

9 tile NW:

`{(x,y) | x ∈ [2,4], y ∈ [2,4]}`

### Worker

- 1 farmer principale;
- 1 farm hand assunta giornalmente tramite `HIRE`.

### Partitioning fisso

#### Farmer principale — 4 tile

`{(4,4), (4,3), (3,4), (3,3)}`

#### Farm Hand 1 — 5 tile

`{(4,2), (3,2), (2,4), (2,3), (2,2)}`

### Policy

`HARVEST > PLANT > WATER`

### Altri vincoli

Mantieni invariati:

- crop ROI logic E03/E04;
- `yield = 2.0`, dove previsto;
- no `DIG`;
- no `BUY_LAND`;
- no Water-First;
- no horizon logic;
- no dynamic worker balancing;
- no multiple HIRE treatment;
- no modifica del footprint.

---

## 3. Benchmark protocol

Utilizza lo stesso protocollo consolidato di E03/E04.

Esegui:

- **30 episodi totali**;
- stesso set di opponent:
  - `pass`
  - `random`
  - `starter`
- stessa distribuzione degli episodi per opponent utilizzata nei benchmark precedenti;
- stessa configurazione ambiente;
- stessi criteri di seeding/riproducibilità;
- stesso timeout.

Prima di eseguire, verifica nel repository il comando effettivamente utilizzato in E03/E04.

Non modificare il protocollo senza documentarlo.

---

## 4. Output dedicato E05

Non utilizzare file risultati E01–E04.

Salva il benchmark completo in:

`results/e05_hire_multiworker.json`

Se lo smoke test ha già scritto in questo file, il benchmark completo può sovrascrivere **esclusivamente questo artifact E05**.

Verifica prima dell'esecuzione che:

- `results/e01_baseline.json` sia invariato;
- nessun artifact E02–E04 venga modificato.

---

## 5. Esecuzione preliminare dei test

Prima del benchmark completo, esegui:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Condizione richiesta:

- tutti i test devono passare.

Se la regression suite fallisce:

**FERMATI.**

Non eseguire il benchmark completo.

---

## 6. Standalone build

Rigenera:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
```

Verifica che:

- `submission/submission.py` venga generato;
- i test standalone passino;
- non esistano dipendenze locali mancanti.

Se la standalone build fallisce:

**FERMATI.**

---

## 7. Benchmark E05 completo

Esegui il benchmark completo da 30 episodi utilizzando l'output dedicato E05.

Utilizza il comando coerente con l'infrastruttura corrente.

L'esecuzione deve includere i tre opponent:

`pass, random, starter`

e produrre 30 episodi complessivi con la stessa distribuzione di E03/E04.

Non interrompere il benchmark in base ai primi risultati.

Non modificare l'agente durante l'esecuzione.

---

## 8. Metriche principali obbligatorie

Calcola e registra:

- Total Episodes;
- Completed Episodes;
- Completion Rate;
- Disqualification Count;
- Disqualification Rate;
- Wins;
- Losses;
- Draws;
- Overall Win Rate;
- Mean Final Money;
- sample standard deviation con `ddof=1`;
- Median Final Money.

Verifica esplicitamente il numero effettivo di episodi utilizzato nei calcoli.

---

## 9. Breakdown per opponent

Per ciascuno di:

- `pass`;
- `random`;
- `starter`;

riporta almeno:

- episodi;
- wins;
- losses;
- draws;
- Win Rate;
- Mean Final Money;
- standard deviation, se statisticamente applicabile;
- Median Final Money.

Mantieni la stessa interpretazione utilizzata nei benchmark precedenti.

---

## 10. Confronto economico E05 vs E04

Usa come riferimento E04:

`Mean Final Money E04 = $11232.47 ± $661.26`

Calcola:

### Delta assoluto

`Mean E05 - 11232.47`

### Delta percentuale

`((Mean E05 - 11232.47) / 11232.47) × 100`

### Interpretazione primaria

Il criterio minimo di successo economico è:

`Mean Final Money E05 > $11232.47`

Se vero, l'introduzione della capacità lavorativa aggiuntiva migliora economicamente la configurazione E04.

Se falso:

`Mean Final Money E05 <= $11232.47`

l'ipotesi economica primaria è falsificata, salvo problemi di integrità o implementazione.

---

## 11. Confronto economico E05 vs E03

Usa come riferimento E03:

`Mean Final Money E03 = $14682.47 ± $1164.33`

Calcola:

### Delta assoluto

`Mean E05 - 14682.47`

### Delta percentuale

`((Mean E05 - 14682.47) / 14682.47) × 100`

### Strong Success

Il criterio di successo economico forte è:

`Mean Final Money E05 >= $14682.47`

Se soddisfatto, il footprint multi-worker da 9 tile raggiunge o supera il benchmark economico E03 da 4 tile.

---

## 12. Weed Conversions

Registra:

`Total Weed Conversions E05`

Confronta con E04:

`E04 = 238`

Calcola:

- variazione assoluta;
- variazione percentuale.

Interpretazione:

- una riduzione significativa supporta l'ipotesi che la capacità lavorativa fosse collegata alla starvation;
- `0` weed conversions costituisce **strong operational success**;
- valori residui non implicano automaticamente fallimento economico.

Non utilizzare soglie arbitrarie.

---

## 13. Mean Unwatered End-of-Day Ratio

Registra:

`Mean Unwatered End-of-Day Ratio E05`

Confronta con E04:

`3.33%`

Calcola:

- differenza assoluta in punti percentuali;
- differenza percentuale relativa, se significativa.

Verifica se l'aggiunta della farm hand riduce il fenomeno osservato in E04.

---

## 14. Diagnostica HIRE

Registra, dove l'instrumentation è disponibile e affidabile:

- Total HIRE actions;
- Mean HIRE actions per episode;
- successful hires;
- expected/observed HIRE cost;
- worker-active turns;
- farmer action count;
- farm hand action count;
- breakdown azioni farmer:
  - `HARVEST`;
  - `PLANT`;
  - `WATER`;
  - movement;
  - `PASS`;
- breakdown azioni hand con le stesse categorie.

Verifica che il lifecycle osservato sia coerente con:

- 1 `HIRE` al giorno;
- 30 giorni per episodio;
- circa 30 HIRE per episodio.

Segnala ogni deviazione.

---

## 15. Diagnostica di utilizzo worker

Valuta se la farm hand viene realmente utilizzata.

Se le metriche lo consentono, riporta:

- percentuale di turni in cui la hand è attiva;
- numero medio di azioni non-`PASS`;
- rapporto farmer/hand sulle azioni agricole;
- eventuale sottoutilizzo evidente.

Questo serve a distinguere:

- capacità aggiuntiva efficace;
- capacità disponibile ma non sfruttata;
- problemi di coordinamento.

Non introdurre nuove metriche se non misurabili affidabilmente.

---

## 16. Performance e timeout safety

Registra:

- Agent Mean Turn Latency;
- Maximum Turn Latency, se disponibile;
- eventuali timeout;
- eventuali disqualification.

Confronta qualitativamente con E04:

`Agent Mean Turn Latency E04 = 0.0570 ms/turno`

Non è necessario che E05 sia più veloce.

È necessario che resti ampiamente entro:

`actTimeout = 1.0 s`

---

## 17. Integrità sperimentale

Prima di interpretare i risultati, verifica:

1. 30 episodi effettivamente completati o correttamente contabilizzati;
2. stesso protocollo opponent di E03/E04;
3. nessuna modifica dell'agente durante il benchmark;
4. nessun artifact storico E01–E04 sovrascritto;
5. output salvato nel file dedicato E05;
6. nessuna disqualification;
7. nessun timeout;
8. HIRE lifecycle coerente;
9. nessuna deviazione dal partitioning 4:5;
10. nessuna introduzione di modifiche strategiche non previste.

Se uno di questi punti è violato in modo sostanziale, non dichiarare valido il risultato economico.

---

## 18. Classificazione preliminare dell'esito

La VERIFY deve classificare il risultato senza ancora svolgere la REVIEW completa.

Utilizza una delle seguenti classificazioni preliminari.

### A. Strong Success Candidate

Se:

`Mean Final Money E05 >= Mean Final Money E03`

con benchmark integro.

### B. Minimum Success Candidate

Se:

`Mean Final Money E04 < Mean Final Money E05 < Mean Final Money E03`

con benchmark integro.

### C. Failure Candidate

Se:

`Mean Final Money E05 <= Mean Final Money E04`

con benchmark integro.

### D. Inconclusive

Se problemi tecnici, disqualification, artifact contamination o deviazioni metodologiche impediscono il confronto.

Questa classificazione non sostituisce la successiva REVIEW.

---

## 19. Distinzione tra risultati economici e operativi

Nel documento VERIFY separa chiaramente:

### Risultato economico

- Mean Final Money;
- delta vs E04;
- delta vs E03.

### Risultato operativo

- Weed Conversions;
- Unwatered Ratio;
- utilization farm hand;
- action distribution.

Non dedurre automaticamente una relazione causale definitiva.

Ad esempio:

- meno weeds + più denaro è evidenza coerente con l'ipotesi capacity bottleneck;
- meno weeds senza miglioramento economico richiede REVIEW;
- miglioramento economico con weeds residue non invalida il trattamento.

---

## 20. Documento VERIFY richiesto

Crea:

`docs/versions/E05_verify_antigravity.md`

Il documento deve contenere almeno:

1. **Obiettivo VERIFY**
2. **Configurazione sperimentale**
3. **Protocollo benchmark**
4. **Integrità sperimentale**
5. **Risultati complessivi**
6. **Breakdown per opponent**
7. **Confronto E05 vs E04**
8. **Confronto E05 vs E03**
9. **Weed Conversions**
10. **Unwatered End-of-Day Ratio**
11. **Diagnostica HIRE**
12. **Worker utilization**
13. **Performance e latenza**
14. **Anomalie**
15. **Deviazioni dal PLAN/BUILD**
16. **Classificazione preliminare**
17. **Readiness per REVIEW**

---

## 21. Tabelle richieste

Inserisci almeno una tabella comparativa:

| Experiment | Workers | Tiles | Mean Final Money | Std Dev | Median | Weed Conversions | Unwatered Ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| E03 | 1 | 4 | ... | ... | ... | ... | ... |
| E04 | 1 | 9 | ... | ... | ... | ... | ... |
| E05 | 2 | 9 | ... | ... | ... | ... | ... |

Non inventare valori E03/E04 non disponibili.

Se una metrica storica non è disponibile, indica:

`N/A`

anziché stimarla.

---

## 22. Verifica artifact

Al termine del benchmark verifica:

```powershell
git diff --stat
git status --short
```

Conferma esplicitamente che:

- `results/e01_baseline.json` non è stato modificato;
- nessun artifact E02–E04 è stato sovrascritto;
- `results/e05_hire_multiworker.json` contiene il benchmark E05 completo.

---

## 23. Decisione finale VERIFY

Concludi il documento con esattamente una delle seguenti decisioni:

- `READY FOR REVIEW`
- `VERIFY FAILED`
- `VERIFY INCONCLUSIVE`

Motiva la decisione esclusivamente con le evidenze raccolte.

Non dichiarare ancora:

- hypothesis validated;
- hypothesis falsified;
- SHIP passed;
- experiment final.

Queste decisioni appartengono alla fase REVIEW.

---

## 24. Condizione finale di arresto

Al termine:

1. mostra il risultato completo del benchmark;
2. mostra Mean Final Money, std dev e mediana;
3. mostra delta assoluto e percentuale vs E04;
4. mostra delta assoluto e percentuale vs E03;
5. mostra Weed Conversions e confronto vs E04;
6. mostra Mean Unwatered End-of-Day Ratio;
7. mostra breakdown per opponent;
8. mostra diagnostica HIRE;
9. mostra latenza;
10. mostra classificazione preliminare;
11. indica il percorso di:
   `docs/versions/E05_verify_antigravity.md`;
12. mostra:
   `git diff --stat`;
13. mostra:
   `git status --short`.

Poi **FERMATI**.

Non effettuare REVIEW.

Non effettuare SHIP.

Non eseguire commit finale, push o tag.

Attendi approvazione esplicita prima di passare da **VERIFY** a **REVIEW**.