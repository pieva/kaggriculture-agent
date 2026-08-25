# E06-04 — VERIFY Water-First Scheduling

Proseguiamo il progetto **Kaggriculture Agent** secondo il metodo sperimentale supervisionato:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Repository:

`C:\Users\pietr\Projects\kaggriculture-agent`

Le fasi precedenti sono concluse:

- `E06-01 — DEFINE` → `GO`
- `E06-02 — PLAN` → `GO FOR BUILD`
- `E06-03 — BUILD` → `COMPLETED — AWAITING VERIFY`

Documenti di riferimento:

- `docs/experiments/E06-01_Water_First_Capability_Analysis.md`
- `docs/plans/E06_Water_First_Scheduling.md`
- `docs/versions/E06_build_antigravity.md`

Risultati BUILD osservati:

- Mean Final Money E05: `$21568.93 ± $361.25`
- Mean Final Money E06: `$24662.00 ± $1932.04`
- Delta: `+$3093.07 / +14.34%`
- Total Weed Conversions E05: `176`
- Total Weed Conversions E06: `70`
- Weed reduction: `-60.23%`
- Mean Unwatered EOD Ratio E05: `3.33%`
- Mean Unwatered EOD Ratio E06: `8.11%`
- Completion Rate E06: `100%`
- Disqualification Rate E06: `0%`
- Win Rate E06: `100%`
- Paired Money improvement: `29/30`
- Paired Weed improvement: `30/30`

Procedi ora esclusivamente con:

# VERIFY

Non effettuare ancora REVIEW o SHIP.

---

# 1. Obiettivo del VERIFY

Verificare indipendentemente:

1. integrità sperimentale E06;
2. correttezza dell'implementazione Water-First;
3. preservazione di E05;
4. riproducibilità del benchmark;
5. correttezza delle metriche calcolate;
6. correttezza del paired comparison;
7. significato effettivo della metrica `Mean Unwatered End-of-Day Ratio`;
8. eventuali anomalie o interpretazioni premature presenti nel BUILD.

---

# 2. Verifica implementazione single-variable

Confronta:

`HIRENWClusterROIAgent`

e:

`WaterFirstHIRENWClusterROIAgent`

Conferma mediante ispezione del codice che la sola differenza comportamentale sperimentale sia:

`HARVEST > PLANT > WATER`

→

`WATER > HARVEST > PLANT`

Verifica che non siano cambiate:

- logica HIRE;
- worker count;
- partitioning 4:5;
- footprint;
- crop selection;
- market logic;
- seed purchasing;
- movement;
- routing;
- Manhattan target selection;
- gestione dello shed;
- episode configuration.

Controlla inoltre la modifica effettuata a:

`src/agricola/agent.py`

Spiega esattamente perché è stata necessaria e verifica che non introduca una differenza comportamentale tra E05 ed E06 oltre alla selezione della strategy class.

Se introduce un confondente, fermati e segnalalo.

---

# 3. Verifica test

Riesegui:

`.venv\Scripts\pytest tests/`

Registra:

- collected;
- passed;
- failed;
- warning;
- tempo di esecuzione.

Verifica specificamente che i test E06 dimostrino:

- WATER prima di HARVEST;
- HARVEST prima di PLANT quando WATER non è disponibile;
- PLANT quando non esistono WATER/HARVEST;
- E05 mantiene `HARVEST > PLANT > WATER`;
- invarianti strutturali principali.

Non modificare i test per farli passare salvo presenza di un errore reale documentato.

---

# 4. Verifica standalone

Verifica la compatibilità della strategy E06 con il meccanismo standalone/build esistente.

Non modificare:

`submission/submission.py`

Non effettuare alcuna submission Kaggle.

Documenta il risultato come:

- `PASSED`;
- `FAILED`;
- oppure `NOT APPLICABLE` con motivazione.

---

# 5. Riproducibilità benchmark

Verifica che:

`results/e06_water_first.json`

sia stato prodotto con:

- 30 episodi;
- 10 `pass`;
- 10 `random`;
- 10 `starter`;
- stessi seed E05;
- 720 turni;
- stessa configurazione runner.

Controlla i dati episode-level e ricalcola indipendentemente almeno:

- Mean Final Money;
- sample standard deviation (`ddof=1`);
- median;
- min;
- max;
- Total Weed Conversions;
- Mean Weed Conversions per Episode;
- Completion Rate;
- Disqualification Rate;
- Win Rate;
- Mean Turn Latency.

Confronta i valori ricalcolati con quelli riportati nel BUILD.

---

# 6. Verifica paired E05/E06

Usa:

- `results/e05_hire_multiworker.json`
- `results/e06_water_first.json`

Verifica che ogni coppia rappresenti realmente:

- stesso opponent;
- stesso seed;
- stessa posizione/configurazione rilevante.

Ricalcola:

`delta_money_i`

e:

`delta_weeds_i`

per tutti i 30 episodi.

Conferma o correggi:

- Mean Paired Money Delta: `+$3093.07`
- Std Paired Money Delta: `$1942.60`
- Median Paired Money Delta: `+$4405.00`
- Min Delta: `-$668.00`
- Max Delta: `+$5305.00`
- E06 Money Higher: `29/30`
- Mean Paired Weed Delta: `-3.53`
- E06 Weeds Lower: `30/30`

Non interpretare ancora questi dati come decisione REVIEW.

---

# 7. Analisi critica della metrica Unwatered EOD

Questa è la verifica prioritaria.

Nel BUILD è stato osservato:

- E05 Mean Unwatered EOD Ratio: `3.33%`
- E06 Mean Unwatered EOD Ratio: `8.11%`

nonostante:

- weed conversions `176 → 70`;
- Mean Final Money `$21568.93 → $24662.00`.

È stata proposta la spiegazione secondo cui Water-First irriga all'inizio della giornata e il flag `watered_today` risulterebbe nuovamente `False` nelle ultime ore.

**Non assumere che questa spiegazione sia corretta. Verificala nel codice.**

Ispeziona:

- modello dello stato delle crop/tile;
- ciclo giorno/ora;
- reset di `watered_today`;
- momento esatto in cui avviene la morte/starvation;
- momento in cui viene calcolato `unwatered_end_of_day`;
- implementazione della metrica nel runner;
- eventuale differenza tra “non irrigata al momento del campionamento” e “non irrigata durante la giornata”.

Rispondi precisamente a queste domande:

1. Che cosa misura realmente `Mean Unwatered End-of-Day Ratio`?
2. Qual è il numeratore?
3. Qual è il denominatore?
4. In quale ora/tick viene rilevato?
5. `watered_today` quando viene impostato a `True`?
6. Quando viene resettato a `False`?
7. Può una crop essere irrigata correttamente e risultare comunque “unwatered” nella metrica?
8. Il valore `8.11%` rappresenta effettivamente maggiore starvation?
9. La metrica è appropriata per confrontare E05 ed E06?
10. Deve essere mantenuta, reinterpretata o sostituita in future iterazioni?

Se necessario, proponi una metrica diagnostica più corretta, ma:

**NON modificare il runner o l'esperimento E06 durante VERIFY.**

Eventuali modifiche metodologiche saranno decise successivamente.

---

# 8. Verifica delle Weed Conversions

Controlla anche la semantica di:

`weed_count`

e delle `Weed Conversions`.

Determina se il valore:

`176 → 70`

rappresenta realmente conversioni dovute a starvation/morte della crop o se include altri meccanismi ambientali.

Verifica:

- dove viene incrementato;
- quando una tile diventa `WEED`;
- se il conteggio è cumulativo;
- se una stessa tile può contribuire più volte;
- se DIG o altri meccanismi incidono sul conteggio.

Spiega precisamente cosa significa il delta `-106`.

Non affermare automaticamente che siano stati “salvati 106 giorni-tile di produzione” se questa equivalenza non è dimostrata dal modello dell'ambiente.

---

# 9. Verifica dell'interpretazione economica

Il BUILD afferma che la riduzione delle weeds avrebbe prodotto direttamente il miglioramento economico.

Verifica se questo nesso causale è dimostrabile con i dati disponibili.

Distinguere tra:

- **osservazione:** E06 ha meno weeds e più money;
- **associazione coerente con l'ipotesi:** i due effetti si muovono nella direzione prevista;
- **causalità dimostrata:** richiede evidenze specifiche.

Se i dati non permettono di attribuire quantitativamente `+$3093.07` alle `106` weed evitate, correggi la formulazione nel documento VERIFY.

---

# 10. Analisi della varianza economica

E05:

`$21568.93 ± $361.25`

E06:

`$24662.00 ± $1932.04`

La deviazione standard E06 è molto maggiore.

Analizza i risultati episode-level per capire l'origine di questa dispersione.

Verifica almeno:

- distribuzione per opponent;
- seed con money minimo;
- seed con money massimo;
- episodio paired con delta `-$668`;
- eventuali cluster di risultati;
- presenza di outlier evidenti;
- eventuale relazione con weed count;
- eventuale relazione con opponent.

Non eliminare outlier.

Documenta semplicemente il comportamento.

---

# 11. Classificazione preliminare

Dopo le verifiche, applica meccanicamente la matrice definita nel PLAN:

### Weed Classification

- `< 50` → `STRONG SUCCESS`
- `50–119` → `PARTIAL SUPPORT`
- `≥ 120` → `FALSIFIED`

### Economic Classification

- `> $21568.93` → `ECONOMIC IMPROVEMENT`
- `$21200 – $21568.93` → `SUBSTANTIAL NEUTRALITY`
- `$20500 – $21199.99` → `MODERATE REGRESSION`
- `< $20500` → `SEVERE REGRESSION`

Non trasformare ancora queste classificazioni nella decisione finale di REVIEW.

---

# 12. Documento VERIFY

Crea:

`docs/versions/E06_verify_antigravity.md`

Il documento deve contenere almeno:

1. **VERIFY Objective**
2. **Experimental Integrity**
3. **Single-Variable Verification**
4. **E05 Preservation**
5. **Test Suite Verification**
6. **Standalone Verification**
7. **Benchmark Recalculation**
8. **E05/E06 Comparison**
9. **Paired Comparison Verification**
10. **Unwatered EOD Metric Audit**
11. **Weed Conversion Metric Audit**
12. **Economic Variance Analysis**
13. **Causality vs Association**
14. **Outlier / Episode-Level Analysis**
15. **Preliminary Classification**
16. **Anomalies**
17. **VERIFY Verdict**
18. **Open Questions for REVIEW**

Il VERIFY verdict deve essere esclusivamente uno tra:

- `PASSED`
- `PASSED WITH METRIC CAVEAT`
- `FAILED`

Non dichiarare ancora SHIP.

---

# 13. Aggiornamento stato

Aggiorna, se necessario:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`
- `docs/EXPERIMENT_LOG.md`

Registrando solamente lo stato VERIFY.

Non dichiarare E06 shipped.

---

# 14. Vincoli

- NON modificare la strategy E06 salvo bug che renda invalido l'esperimento; in quel caso fermati prima.
- NON modificare E05.
- NON modificare il runner per correggere metriche.
- NON modificare `submission/submission.py`.
- NON eseguire Kaggle submission.
- NON effettuare REVIEW.
- NON effettuare SHIP.
- NON creare tag.
- NON effettuare commit.
- NON effettuare push.

---

# Output finale

Mostrami:

1. risultato verifica single-variable;
2. risultato test;
3. risultato standalone;
4. metriche benchmark ricalcolate;
5. paired comparison verificato;
6. spiegazione tecnica verificata del `Mean Unwatered EOD Ratio`;
7. significato verificato delle Weed Conversions;
8. analisi della maggiore varianza economica E06;
9. eventuali interpretazioni BUILD da correggere;
10. classificazione preliminare;
11. verdict `PASSED / PASSED WITH METRIC CAVEAT / FAILED`;
12. questioni aperte per REVIEW;
13. file creati/modificati;
14. `git diff --stat`;
15. `git status --short`.

**Fermati dopo VERIFY e attendi la mia approvazione prima di REVIEW.**