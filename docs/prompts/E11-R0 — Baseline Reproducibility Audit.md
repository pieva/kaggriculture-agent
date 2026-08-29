# E11-R0 — Baseline Reproducibility Audit

## Contesto

La serie sperimentale **E11 — 3× Productive Mass Expansion** ha prodotto risultati progressivi su più iterazioni:

- E11-01 — Productive Mass Baseline
- E11-02 — Expansion Capital Protection
- E11-03 — Expansion Gate Unlock
- E11-04 — Seed–Expansion Synchronization
- E11-05 — Staged Expansion Capital Release
- E11-06 — Workforce–Land Co-Scaling

Durante il benchmark E11-06 è emersa una discrepanza grave:

> **le baseline storiche E11 non risultano più riprodurre i risultati precedentemente documentati.**

Questo rende il risultato E11-06 **non interpretabile causalmente** finché non viene verificata la riproducibilità delle configurazioni precedenti.

---

# 1. Discrepanza osservata

Alcune configurazioni storiche avevano prodotto risultati nettamente differenti.

Indicativamente:

| Variante | Risultato storico | Benchmark E11-06 |
|---|---:|---:|
| E11-01 | ~$23–24k | ~$7.1k |
| E11-02 | ~$15.7k | ~$7.2k |
| E11-03 | ~$7.5k + forte land expansion | ~$7.2k |
| E11-04 | comportamento distinto | ~$7.2k |
| E11-05 | forte regressione economica | ~$7.1k |

Nel benchmark E11-06 quasi tutte le varianti E11 risultano improvvisamente concentrate nella fascia:

> **~$7.0k–$7.2k**

nonostante le rispettive policy avessero in precedenza prodotto comportamenti architetturali molto differenti.

Questo è un segnale di possibile:

- contaminazione della configurazione;
- regressione nel codice condiviso;
- instanziazione errata nel benchmark;
- mutazione/config sharing;
- perdita di isolamento tra le versioni E11.

---

# 2. Stato E11-06

Registrare formalmente E11-06 come:

> **E11-06 RESULT INVALID FOR CAUSAL INTERPRETATION — baseline reproducibility failure suspected**

NON classificare ancora E11-06 come:

- conferma;
- falsificazione;
- FAIL causale della workforce policy.

Il Mean Final Money osservato può essere registrato come dato tecnico del run, ma NON utilizzato per trarre conclusioni sperimentali sulla H11-06.

---

# 3. Obiettivo E11-R0

Eseguire:

> **E11-R0 — Baseline Reproducibility Audit**

La domanda principale è:

> **Le configurazioni E11-01, E11-02, E11-03, E11-04 ed E11-05 sono ancora realmente riproducibili e indipendenti dopo le modifiche introdotte nelle iterazioni successive?**

Il task deve identificare la causa della divergenza prima di qualsiasi nuova modifica strategica.

---

# 4. Vincolo assoluto

Questo task è esclusivamente un audit tecnico.

NON:

- progettare E11-07;
- modificare la strategia economica;
- introdurre nuovi trigger;
- cambiare crop policy;
- cambiare capital protection;
- cambiare workforce policy;
- cambiare livestock;
- effettuare tuning;
- effettuare submission Kaggle.

È consentito modificare codice esclusivamente se necessario per:

> **ripristinare la corretta separazione e riproducibilità delle configurazioni storiche**

e solo dopo aver identificato esattamente il problema.

---

# 5. Fonti di verità storiche

Prima di modificare qualsiasi file, leggere i documenti:

- `docs/versions/E11_build_productive_mass_expansion.md`
- `docs/versions/E11_02_expansion_capital_protection.md`
- `docs/versions/E11_03_expansion_gate_unlock.md`
- `docs/versions/E11_04_seed_expansion_synchronization.md`
- `docs/versions/E11_05_staged_expansion_capital_release.md`
- `docs/versions/E11_06_workforce_land_co_scaling.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Ricostruire per ogni versione:

- configurazione prevista;
- comportamento previsto;
- risultato benchmark storico;
- metriche architetturali;
- principali flag/config.

---

# 6. Matrice di riproducibilità attesa

Creare una tabella iniziale:

| Variante | Config attesa | Mean storico | Land storico | Workforce storica | Livestock |
|---|---|---:|---|---|---|
| E11-01 | | | | | |
| E11-02 | | | | | |
| E11-03 | | | | | |
| E11-04 | | | | | |
| E11-05 | | | | | |
| E11-06 | | | | | |

Usare esclusivamente valori presenti nella documentazione.

Non ricostruire “a memoria”.

---

# 7. Audit della classe ProductiveMassROIAgent

Ispezionare:

`src/agricola/strategy/productive_mass_roi.py`

Verificare se modifiche successive hanno alterato:

- default config;
- comportamento base della classe;
- branching per `expansion_gate_mode`;
- branching per `expansion_crop_policy`;
- branching per `capital_release_mode`;
- branching per workforce scaling;
- hiring logic;
- livestock activation;
- crop policy;
- state initialization.

La domanda è:

> **una configurazione storica riesce realmente a riattivare il comportamento originale oppure il codice comune è ormai cambiato semanticamente?**

---

# 8. Audit di ProductiveMassConfig

Verificare:

- valori default;
- mutabilità;
- eventuali `list`, `dict`, `set` condivisi;
- dataclass defaults;
- nested mutable objects;
- modifiche runtime della config;
- shallow copy vs deep copy;
- eventuali parametri aggiunti successivamente con default incompatibili.

Controllare in particolare se configurazioni nominalmente diverse condividono lo stesso oggetto.

---

# 9. Identity Test delle configurazioni

Per ogni variante E11:

- istanziare la config;
- stampare/serializzare tutti i parametri;
- confrontare gli object ID quando rilevante;
- verificare che una modifica a una config non alteri un’altra.

Creare un piccolo test diagnostico, se necessario.

Esempio concettuale:

```python
assert e11_01_config is not e11_03_config
assert e11_03_config != e11_06_config
```

Non limitarsi all’identity: confrontare anche i valori.

---

# 10. Snapshot completo delle config

Produrre per ciascuna variante:

```text
E11-01
  parameter_a = ...
  parameter_b = ...
  ...

E11-02
  ...

E11-06
  ...
```

Evidenziare:

- parametri differenti;
- parametri identici;
- eventuali valori inattesi.

Questo snapshot deve diventare parte del report E11-R0.

---

# 11. Audit benchmark_e11_performance.py

Ispezionare attentamente:

`scripts/benchmark_e11_performance.py`

Verificare per ogni variante:

- factory utilizzata;
- classe istanziata;
- config passata;
- eventuali lambda;
- closure;
- late binding;
- config mutation;
- factory reuse;
- global state;
- agent instance reuse;
- accidental aliasing.

Controllare soprattutto pattern come:

```python
lambda: ProductiveMassROIAgent(config)
```

dentro loop, dove una closure può catturare l’ultima variabile.

Se presente, verificare late binding.

---

# 12. Factory Identity Audit

Per ciascuna entry benchmark E11:

- creare l’agente;
- stampare nome variante;
- config effettiva;
- class name;
- strategy mode;
- eventuali state flags.

Verificare che:

> E11-01 benchmark factory crei davvero E11-01

e così via.

---

# 13. Controllo shared mutable state

Verificare se `ProductiveMassROIAgent` o moduli correlati utilizzano:

- class attributes mutabili;
- module globals;
- cache condivise;
- telemetry globals;
- static state;
- singleton config;
- mutable default args.

Ogni episodio deve iniziare da stato pulito.

---

# 14. Episode Reset Audit

Verificare che tra episodi venga resettato:

- economic state machine;
- expansion target;
- worker locality state;
- telemetry;
- cumulative spending;
- livestock state interno;
- cached target;
- crop allocation;
- current phase.

Eseguire, se necessario:

> stesso agente factory → due episodi consecutivi

e verificare che il secondo episodio inizi con stato identico al primo.

---

# 15. Randomness / Seed Audit

Verificare:

- seed passati al benchmark;
- seed ambiente;
- seed agent;
- eventuali random globali;
- numpy/random state;
- ordine degli agenti nel benchmark.

La divergenza è troppo ampia per essere spiegata solo dalla casualità, ma il controllo deve essere documentato.

---

# 16. E10 Control

Utilizzare E10-01 come controllo esterno.

E10 nei benchmark recenti rimane nell’ordine di:

> `$22–23k`

Questo suggerisce che:

- environment;
- benchmark runner;
- opponent setup;

sono probabilmente ancora funzionanti.

Verificare comunque E10 su un piccolo subset riproducibile.

---

# 17. Reproduction Test — E11-01 isolata

Prima di benchmark multipli:

> eseguire E11-01 DA SOLA

sugli stessi seed storici.

Registrare:

- Mean Final Money;
- Median;
- land;
- active tiles;
- workers;
- livestock.

Confrontare con il report storico.

Classificare:

- `REPRODUCED`
- `PARTIALLY REPRODUCED`
- `NOT REPRODUCED`

---

# 18. Reproduction Test — E11-02 isolata

Ripetere la stessa procedura.

Verificare che torni il comportamento storico:

- capital protection;
- land lock;
- crop restriction;
- relativo money range.

---

# 19. Reproduction Test — E11-03 isolata

Questa è la verifica più importante.

E11-03 deve riprodurre indicativamente:

- 3Q unlock rate ~`83%`;
- 4Q unlock rate ~`60%`;
- 100 tile raggiungibili;
- peak active tiles ~`54`;
- peak workforce ~`6`;
- money nell’ordine storico.

Non richiedere identità perfetta se il precedente benchmark aveva una lieve differenza di seed/protocollo.

Ma il comportamento architetturale deve essere chiaramente riconoscibile.

Se E11-03 rimane a 2Q / 50 tile:

> **la baseline è definitivamente non riprodotta.**

---

# 20. Reproduction Test — E11-04 isolata

Verificare che riemerga la specifica regressione prevista da E11-04.

E11-04 non deve comportarsi identicamente a E11-03 se le config sono realmente separate.

---

# 21. Reproduction Test — E11-05 isolata

Verificare che la state machine staged venga realmente attivata.

Registrare le transizioni:

- ACCUMULATE_Q2;
- PRODUCTIVE_WINDOW;
- ACCUMULATE_Q3;
- MASS_ACTIVATION.

Verificare che non stia invece usando il comportamento di E11-03/E11-06.

---

# 22. Single Seed Trace

Utilizzare almeno un seed rappresentativo per produrre una trace comparativa molto leggibile.

Per esempio:

```text
Seed 0

Day | E11-01 | E11-02 | E11-03 | E11-04 | E11-05
---------------------------------------------------
...
```

Tracciare almeno:

- money;
- quadrants;
- active tiles;
- workers;
- current mode/state.

Se tutte le varianti producono la stessa trace:

> configurazione/branching è chiaramente rotto.

---

# 23. Behavioral Fingerprints

Definire per ciascuna variante un fingerprint semplice.

Esempio:

### E11-03 expected fingerprint

- capital protection ON
- MIN_OPERATIONAL gate
- 3Q/4Q expansion
- no permissive seed release
- no staged release
- default workforce policy

### E11-05 expected fingerprint

- STAGED capital release
- Productive Window state visible

Verificare automaticamente questi fingerprint prima di benchmark.

---

# 24. Aggiungere Reproducibility Tests

Aggiungere o estendere test per garantire che le configurazioni storiche restino distinte.

Testare almeno:

1. config E11-01 ≠ E11-03;
2. E11-03 usa `MIN_OPERATIONAL`;
3. E11-04 usa la propria crop policy;
4. E11-05 usa `STAGED`;
5. E11-06 usa workforce co-scaling;
6. factory benchmark restituisce config corretta;
7. una config non muta l’altra;
8. agent state non persiste fra episodi.

Questi test devono impedire future contaminazioni.

---

# 25. Eventuale correzione tecnica

Solo dopo aver identificato la causa, correggere il minimo necessario.

Possibili categorie:

## Factory bug

Correggere `benchmark_e11_performance.py`.

## Shared config bug

Creare copie indipendenti.

## Default semantic regression

Ripristinare branching esplicito per le versioni storiche.

## State leak

Implementare reset corretto.

## Closure / late binding

Correggere factory.

NON approfittare della correzione per modificare la strategia.

---

# 26. Version Preservation

Dopo la correzione, ogni variante E11 deve avere una factory/config esplicita.

Preferire una struttura del tipo:

```python
def make_e11_01():
    return ProductiveMassROIAgent(config=...)

def make_e11_02():
    return ProductiveMassROIAgent(config=...)

def make_e11_03():
    return ProductiveMassROIAgent(config=...)
```

oppure equivalente.

Evitare costruzioni implicite difficili da auditare.

---

# 27. Config Freeze / Snapshot

Valutare se introdurre una struttura esplicita di configurazioni versionate:

```text
E11_01_CONFIG
E11_02_CONFIG
E11_03_CONFIG
...
```

Queste configurazioni devono essere:

- indipendenti;
- documentate;
- non mutate runtime.

Non è obbligatorio introdurre immutable dataclass se complica inutilmente il codice.

Ma il comportamento storico deve essere congelabile.

---

# 28. Benchmark post-fix

Solo dopo aver ottenuto riproducibilità isolata:

eseguire benchmark paired completo.

Confrontare:

- E10-01
- E11-01
- E11-02
- E11-03
- E11-04
- E11-05

NON includere E11-06 nel confronto causale finché le baseline non sono validate.

---

# 29. Acceptance Criteria — Baseline Reproducibility

Considerare l’audit risolto solo se:

### E11-01

torna alla propria classe di comportamento storico.

### E11-02

mostra il proprio comportamento di capital protection.

### E11-03

torna a mostrare:

- elevato 3Q unlock;
- significativo 4Q unlock;
- 100 tile raggiungibili.

### E11-04

mostra regressione distinta.

### E11-05

mostra staged state machine distinta.

Non è richiesta identità numerica al centesimo.

È richiesta:

> **riproducibilità comportamentale + compatibilità statistica ragionevole.**

---

# 30. Classificazione finale

Per ogni variante riportare:

- `REPRODUCED`
- `PARTIALLY REPRODUCED`
- `NOT REPRODUCED`

e spiegazione.

---

# 31. Verifica E11-06

Solo DOPO aver validato E11-01…05:

rieseguire E11-06 isolatamente e poi nel benchmark paired.

A quel punto verificare se il risultato precedente:

> ~$7.1k / 2Q / 1 worker

era causato dal bug di riproducibilità oppure dalla workforce policy.

Classificare:

- `E11-06 RESULT VALIDATED`
- oppure
- `E11-06 PREVIOUS RESULT INVALIDATED`

---

# 32. Nessun E11-07

Non progettare E11-07 in questo task.

In particolare NON implementare:

> Dynamic Adaptive Capital Release

La logica proposta:

```text
cash < 800 → seeds allowed
cash > 850 → land protection
```

è concettualmente simile al ramo già testato e falsificato in E11-04.

Non riaprirlo senza nuove evidenze.

---

# 33. Deliverable documentale

Creare:

`docs/versions/E11_R0_baseline_reproducibility_audit.md`

Struttura minima:

1. Executive Summary
2. Problem Statement
3. Historical Baselines
4. Expected Reproducibility Matrix
5. ProductiveMassROIAgent Audit
6. ProductiveMassConfig Audit
7. Benchmark Factory Audit
8. Shared State Audit
9. Episode Reset Audit
10. Seed Audit
11. E10 Control
12. E11-01 Isolated Reproduction
13. E11-02 Isolated Reproduction
14. E11-03 Isolated Reproduction
15. E11-04 Isolated Reproduction
16. E11-05 Isolated Reproduction
17. Single Seed Trace
18. Root Cause
19. Technical Fix
20. Reproducibility Tests
21. Post-Fix Benchmark
22. Final Reproducibility Matrix
23. E11-06 Re-evaluation
24. Final Verdict
25. Next Step Recommendation

---

# 34. Aggiornamento stato progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Durante l’audit registrare:

> **E11-R0 Baseline Reproducibility Audit IN PROGRESS**

Al termine:

> **E11-R0 COMPLETED — baseline reproducibility [RESTORED / NOT RESTORED]**

E11-06 deve rimanere:

> **RESULT INVALID FOR CAUSAL INTERPRETATION**

finché non viene rieseguito dopo il fix.

---

# 35. Git

Alla fine eseguire:

```powershell
git status
git diff --stat
git diff --check
```

NON effettuare:

- commit finale;
- tag;
- push;
- Kaggle submission.

---

# Deliverable finale

Al termine fermarsi e riportare:

1. **root cause identificata**
2. **tipo di contaminazione**
3. **file responsabile**
4. **correzione tecnica applicata**
5. **test suite result**
6. **E10 control result**
7. **E11-01 reproduction verdict**
8. **E11-02 reproduction verdict**
9. **E11-03 reproduction verdict**
10. **E11-03 3Q unlock rate**
11. **E11-03 4Q unlock rate**
12. **E11-03 peak land**
13. **E11-03 peak active tiles**
14. **E11-03 peak workforce**
15. **E11-04 reproduction verdict**
16. **E11-05 reproduction verdict**
17. **config isolation test**
18. **episode state isolation test**
19. **post-fix benchmark summary**
20. **E11-06 re-run result**
21. **E11-06 causal validity verdict**
22. **baseline reproducibility overall verdict**
23. **file creati/modificati**
24. **raccomandazione successiva**

## Regola finale

Se E11-03 NON torna al proprio fingerprint storico:

> **non procedere con E11-06 né E11-07.**

Se E11-03 viene riprodotta correttamente:

> **rieseguire E11-06 dalla baseline E11-03 ripristinata.**

Se il precedente risultato E11-06 cambia:

> **invalidare formalmente il precedente benchmark E11-06.**

Se il precedente risultato E11-06 viene confermato:

> **solo allora interpretare causalmente Workforce–Land Co-Scaling.**

**Nessuna nuova strategia finché la catena sperimentale E11 non è nuovamente riproducibile.**