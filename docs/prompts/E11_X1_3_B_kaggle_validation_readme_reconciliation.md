# E11-X1.3-B — SHIP EXPERIMENTAL — Kaggle External Validation + README Project Reconciliation

## Contesto

La serie E11 è stata bonificata metodologicamente attraverso:

- E11-R0 — Configuration Isolation Audit
- E11-R1 — Historical Behavioral Reconstruction
- E11-R2 — Historical Benchmark Provenance Audit
- E11-R3 — Verified Baseline Re-establishment

La baseline quantitativa autorevole è:

> **E11-VB1 — Verified Baseline 1**

La linea sperimentale verificata successiva è:

- **E11-X1.2** — E06 Productive Core Restoration + Corrected Multi-HIRE
- **E11-X1.3-A** — 1× EPU replication
- **E11-X1.3-B** — 2× EPU scaling

E11-X1.3-A ha replicato esattamente E06 sul diagnostico seed-0/pass:

> **$25,847**

e ha prodotto su 5 episodi:

> **$26,888.40 Mean Final Money**

E11-X1.3-B ha introdotto il primo scaling reale:

> **1× EPU (9 tile) → 2× EPU (18 tile)**

con sequenza verificata:

```text
EPU1 productive
    ↓
cash surplus
    ↓
BUY_LAND Q1
    ↓
EPU2 activation
    ↓
18/18 active tiles
```

Risultato locale B:

- Mean Final Money: **$28,727.40**
- Median: **$29,244.00**
- scaling ratio vs A: **1.07×**
- scaling efficiency: **53.4%**
- Gate B: **STOP**
- provenance: **PASS**

X1.3-C non è stato eseguito.

---

# 1. Obiettivo del task

Procedere con un unico passaggio operativo:

> **E11-X1.3-B — Kaggle External Validation + README Project Reconciliation**

Il task ha due deliverable principali:

1. preparare e verificare la submission Kaggle di **X1.3-B**;
2. aggiornare il `README.md` del repository per riallinearlo allo stato reale del progetto.

NON modificare la strategia.

NON implementare X1.4.

NON eseguire X1.3-C.

---

# 2. Perché X1.3-B e non X1.3-A

X1.3-A è un controllo positivo:

> replica E06.

La sua funzione sperimentale è già stata soddisfatta.

X1.3-B è invece:

> **il primo trattamento realmente nuovo di scaling della productive unit E06**

e deve essere validato esternamente.

La submission deve quindi usare esattamente:

> **2× EPU / 18 productive tiles**

nella configurazione verificata localmente.

---

# 3. Freeze strategico

Prima della build della submission:

NON modificare:

- crop logic;
- EPU layouts;
- workforce;
- multi-HIRE;
- land trigger;
- Water-First;
- seed buying;
- market selling;
- movement;
- working capital;
- config thresholds.

Qualsiasi differenza rispetto al run verificato X1.3-B invalida la submission.

---

# 4. Identificare la configurazione X1.3-B esatta

Recuperare dal run verificato:

`results/e11/E11-X1.3-B-20260827-100010/config.json`

e dal codice benchmark:

`scripts/benchmark_e11_x1_3.py`

Identificare tutti i parametri effettivi della configurazione B.

Creare una tabella nel deliverable:

| Parameter | X1.3-B verified value |
|---|---|
| productive_core_mode | |
| epu_level | |
| enable_land_expansion | |
| workforce mode | |
| land trigger mode | |
| crop policy | |
| Water-First | |
| seed buying | |
| market selling | |
| other relevant fields | |

Non usare default impliciti senza verificarli.

---

# 5. Config snapshot comparison

Confrontare:

> config del run locale verificato

con:

> config che verrà incorporata nella submission.

Acceptance:

> **100% semantic match**

Se esiste qualsiasi differenza:

STOP.

Correggere la build artifact, NON la strategia.

---

# 6. Build della submission

Usare lo script esistente:

`scripts/build_submission.py`

ma prima verificarne la logica.

L'artefatto finale deve usare:

> **ProductiveMassROIAgent configured as X1.3-B**

NON:

- X1.3-A;
- E06 directly;
- E11-VB1;
- config default;
- config legacy;
- X1.2.

---

# 7. Verifica di `submission/agent.py`

Dopo build:

aprire integralmente:

`submission/agent.py`

Verificare:

1. strategy class corretta;
2. config B corretta;
3. `epu_level = 2`;
4. E06-replicated productive core;
5. land expansion abilitata secondo B;
6. Multi-HIRE corretto;
7. 18-tile target/layout;
8. nessun import locale non disponibile su Kaggle;
9. nessun riferimento a file esterni;
10. nessun codice scratch/debug.

---

# 8. Submission fingerprint

Aggiungere un fingerprint leggibile nell'artefatto, se già compatibile con lo stile del progetto, oppure documentarlo esternamente.

Per esempio:

```text
strategy_id = E11-X1.3-B
productive_core = E06_REPLICATED
epu_level = 2
target_productive_tiles = 18
```

Non introdurre side effects.

---

# 9. Test submission

Eseguire:

```powershell
.venv\Scripts\pytest.exe tests/
```

e gli eventuali test submission esistenti.

Se esiste:

`tests/test_submission.py`

eseguirlo esplicitamente.

Eseguire anche:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
```

seguendo l'ordine appropriato.

---

# 10. Smoke locale dell'artefatto submission

Se il progetto dispone di una modalità per eseguire `submission/agent.py` localmente:

eseguire un solo episodio smoke.

Confrontare comportamento minimo con X1.3-B:

- EPU1 startup;
- land expansion event;
- EPU2 activation;
- workforce;
- action legality.

Non eseguire un nuovo benchmark da 5/10/30.

---

# 11. Kaggle submission

Preparare la submission X1.3-B per Kaggle.

Se l'ambiente Antigravity dispone di accesso Kaggle funzionante:

procedere con la submission secondo la procedura già usata dal progetto.

Se l'accesso Kaggle non funziona:

NON aprire loop di browser o tentativi ripetuti.

Fermarsi dopo avere prodotto l'artefatto pronto e riportare il comando/manual step necessario.

---

# 12. Nome submission

Usare un identificatore chiaramente riconoscibile.

Preferenza:

> `E11-X1.3-B 2x EPU Scaling`

o naming equivalente compatibile con Kaggle.

Non chiamarla genericamente E11.

---

# 13. Cosa registrare della submission

Registrare:

- submission/version ID;
- timestamp;
- strategy ID;
- config fingerprint;
- eventuale Kaggle score iniziale;
- stato pending/running/completed;
- eventuali errori.

Non interpretare uno score ancora in assestamento come risultato finale.

---

# 14. External validation question

La submission serve a rispondere:

> **Il primo scaling reale del modello E06 da 9 a 18 tile produce un vantaggio competitivo esterno rispetto alla vecchia capacità E06, nonostante una scaling efficiency locale di solo 53.4%?**

Non serve ancora a verificare $75k.

---

# 15. Decision matrix post-submission

Documentare:

## Se X1.3-B migliora E06 esternamente

Conclusione preliminare:

> **EPU scaling direction externally supported**

X1.4 dovrà concentrarsi sull'efficienza della seconda EPU.

## Se X1.3-B ≈ E06

Conclusione:

> nuova capacità non genera ancora vantaggio competitivo.

Diagnosi prioritaria:

- expansion timing;
- EPU2 activation timing;
- land amortization.

## Se X1.3-B < E06

Conclusione:

> scaling introduces external regression.

Non procedere a 3× EPU.

---

# 16. README — problema attuale

Il `README.md` è fermo circa allo stato E06.

Questo non rappresenta più correttamente il progetto.

Aggiornarlo nello stesso task.

---

# 17. Obiettivo README

Il README deve diventare:

> **una sintesi aggiornata e affidabile dello stato del progetto**

NON un dump dell'intero EXPERIMENT_LOG.

Deve permettere a un lettore GitHub di capire:

- obiettivo;
- architettura;
- percorso sperimentale;
- stato corrente;
- benchmark interni;
- benchmark competitivi;
- metodologia di verifica;
- trattamento corrente.

---

# 18. Struttura README consigliata

Rivedere il README mantenendo, se utili, le sezioni già esistenti.

Includere almeno:

## Project Goal

Kaggriculture agent optimization.

## Current Competitive Goal

- Minimum Success: **$50k**
- Competitive Target: **$75k**
- top-player reference: **~$70–75k+**

## Verified Methodology

- append-only run directories;
- config snapshot;
- raw episodes;
- summary;
- SHA-256;
- provenance verifier;
- 1 → 5 → 10 reduced benchmark;
- 30 episodes only for milestones.

## Internal Sanity Benchmark

E06.

## EPU Scaling Architecture

E06 → X1.3-A → X1.3-B.

## Current Status

X1.3-B external validation.

---

# 19. README — cronologia sintetica

Inserire una tabella compatta.

Esempio:

| Version | Main idea | Local result | Status |
|---|---|---:|---|
| E01 | baseline | | historical |
| E02–E05 | early ROI iterations | | historical |
| E06 | compact Water-First + HIRE | ~25k class | internal sanity reference |
| E07–E10 | scaling / livestock / capital experiments | | historical |
| E11-R0…R3 | reproducibility & provenance recovery | | methodology restored |
| E11-VB1 | verified baseline | $429 verified baseline | authoritative baseline |
| E11-X1.2 | E06 core restoration | $7.48k | verified treatment |
| E11-X1.3-A | 1× EPU replication | $26.89k | verified positive control |
| E11-X1.3-B | 2× EPU scaling | $28.73k | current treatment / Kaggle validation |
| E11-X1.3-C | 3× EPU | not executed | blocked |

Popolare con valori supportati dalla documentazione.

Non inventare numeri per versioni storiche non necessarie.

---

# 20. README — provenance correction

Inserire una nota metodologica concisa:

> alcuni risultati storici E11 intermedi sono stati ritirati come baseline quantitativa dopo un audit di provenance; da E11-R3 in avanti vengono considerati autorevoli solo run ricostruibili dai raw episode records.

Non serve descrivere tutto l'incidente.

Serve essere trasparenti.

---

# 21. README — E06 status

Distinguere:

- E06 historical benchmark;
- E06 seed-0 verified diagnostic;
- X1.3-A verified replication.

Non affermare che una media E06 è machine-verifiable se non lo è.

---

# 22. README — X1.3 numbers

Usare:

## X1.3-A

- A0 seed0/pass: **$25,847 exact E06 match**
- 5-episode Mean: **$26,888.40**
- 1× EPU / 9 tile

## X1.3-B

- 5-episode Mean: **$28,727.40**
- 2× EPU / 18 active tile
- scaling ratio: **1.07×**
- scaling efficiency: **53.4%**
- EPU2 activation around Day 15
- current external validation candidate

---

# 23. README — competitive benchmark

Riportare il benchmark top validato:

- 3Q mean Day **4.20**
- 4Q mean Day **8.53**
- 4–6 worker @3Q
- 8–10 worker @4Q
- 35–45 active tiles @3Q
- 75–85 @4Q
- ~$70–75k+ final benchmark

Specificare:

> competitor benchmark / not our result.

---

# 24. README — current hypothesis

Descrivere:

> **E06 Productive Unit scaling**

Una EPU è:

- 9 compact productive tiles;
- E06-equivalent Water-First;
- fast ROI crop rotation;
- workforce adeguata;
- low movement;
- preserved working capital.

Current question:

> can 2×/3× EPU scale efficiently enough to reach competitive mass?

---

# 25. README — non promuovere X1.3-B a successo definitivo

X1.3-B è:

> **current treatment**

NON:

- validated competitive architecture;
- new baseline;
- success at $50k;
- success at $75k.

Il Gate B locale è fallito sulla scaling efficiency.

La submission serve proprio a ottenere evidenza esterna.

---

# 26. Documentazione di versione

Creare:

`docs/versions/E11_X1_3_B_kaggle_external_validation.md`

Struttura:

1. Executive Summary
2. Why X1.3-B
3. Verified Local Configuration
4. Config Fingerprint
5. Submission Build
6. Submission Artifact Audit
7. Tests
8. Local Smoke
9. Kaggle Submission
10. Submission Metadata
11. Initial External Result
12. Comparison with E06
13. Interpretation Rules
14. README Reconciliation
15. Files Changed
16. Stop Gate
17. Next Step

---

# 27. Aggiornare stato progetto

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/EXPERIMENT_LOG.md`
- `docs/NEW_SESSION.md`

Stato:

> **E11-X1.3-B KAGGLE EXTERNAL VALIDATION SUBMITTED / READY — awaiting external result**

Usare `SUBMITTED` solo se la submission è realmente avvenuta.

---

# 28. Git status

Alla fine:

```powershell
git status
git diff --stat
git diff --check
```

---

# 29. Commit policy

NON effettuare automaticamente:

- tag;
- release tag;
- final SHIP tag.

Per il commit:

se il workflow corrente del progetto richiede che l'artefatto submission e README siano versionati prima della submission, è consentito preparare il commit ma NON eseguirlo senza indicazione esplicita del supervisore.

Se non necessario:

fermarsi prima del commit.

---

# 30. Nessun X1.4

NON:

- implementare X1.4;
- cambiare crop policy EPU2;
- anticipare land timing;
- eseguire X1.3-C.

Prima:

> ottenere la validazione esterna X1.3-B.

---

# Deliverable finale obbligatorio

Riportare:

1. Task status
2. X1.3-B verified run source
3. Exact config fingerprint
4. Submission build status
5. `submission/agent.py` strategy identity
6. `epu_level`
7. target productive footprint
8. land expansion mode
9. workforce mode
10. crop policy
11. tests result
12. submission smoke result
13. Kaggle submission executed YES/NO
14. Kaggle submission ID/version
15. submission timestamp
16. Kaggle initial status
17. Kaggle initial score if available
18. previous E06 Kaggle reference if documented
19. README update summary
20. methodology section updated YES/NO
21. EPU architecture documented YES/NO
22. competitor benchmark documented YES/NO
23. provenance correction documented YES/NO
24. current treatment clearly identified YES/NO
25. docs version report path
26. project state update
27. experiment log update
28. new session update
29. git status
30. files created/modified
31. stop gate confirmation
32. recommended next action after external result

---

# Stop Gate

Dopo:

- submission artifact verified;
- README reconciled;
- Kaggle submission effettuata o pronta;

> **STOP.**

Non modificare X1.3-B.

Non progettare X1.4 sulla sola base del benchmark locale.

Attendere il risultato Kaggle e confrontarlo con:

> E06 internal/external reference + X1.3-B local telemetry + competitor expansion benchmark.
