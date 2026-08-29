# E12-X1.7 — Kaggle External Validation

## Obiettivo

E12-X1.7 ha raggiunto una configurazione locale stabile ma ancora sotto il champion E11-X1.7:

- E12-X1.7 Mean Final Money locale: **$22,386.80**
- E12-X1.6 Mean Final Money locale: **$22,008.80**
- E11-X1.7 Mean Final Money locale: **$28,083.80**

L'audit D3 ha inoltre chiarito che il limite principale di X1.7 non è l'assenza di capacità teorica, ma la **late activation** delle tile marginali e il mismatch tra orizzonte residuo e MELON.

Prima di proseguire con E12-X1.8, vogliamo eseguire una **validazione esterna Kaggle** della configurazione corrente E12-X1.7 per capire come si comporta contro il leaderboard reale.

Questa validazione NON cambia la strategia.

---

## 1. Obiettivo della submission

Verificare esternamente:

> **quanto vale E12-X1.7 sul leaderboard Kaggle rispetto al champion E11-X1.7 già noto e alle submission precedenti.**

Non ottimizzare il codice prima dell'upload.

---

## 2. Configurazione da validare

La submission deve contenere esattamente la configurazione:

**E12-X1.7 — Workforce Capacity Scaling**

con:

- `LIVESTOCK_PRIMARY` centered;
- livestock core 2×2;
- Cow scaling progressivo;
- 5 `CROP_PRIMARY`;
- 4 crop tile per crop worker;
- MELON-oriented crop portfolio;
- WHEAT feed buffer;
- emergency WATER;
- weed retention policy;
- locality;
- stessa configurazione usata nel benchmark canonico X1.7.

NON incorporare fix o idee D3/X1.8.

---

## 3. Provenance gate

Prima dell'upload:

1. identificare source/config della run canonica E12-X1.7;
2. verificare che `submission/submission.py` corrisponda esattamente alla variante X1.7;
3. registrare SHA-256 del file;
4. eseguire:
   - suite test completa;
   - `tests/test_submission.py`;
5. verificare che non siano presenti modifiche locali non documentate che cambino il comportamento.

Se la submission non corrisponde esattamente alla build canonica X1.7:

**STOP — non caricare su Kaggle.**

---

## 4. Build della submission

Eseguire:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
.venv\Scripts\pytest.exe tests/
.venv\Scripts\pytest.exe tests/test_submission.py
```

Documentare:

- esito build;
- test pass/fail;
- SHA-256 finale;
- dimensione di `submission/submission.py`;
- variant ID incorporato.

---

## 5. Upload Kaggle

Usare il normale workflow Kaggle già validato nel progetto.

Se l'accesso automatico/API Kaggle funziona:

- caricare `submission/submission.py`;
- usare una descrizione inequivocabile, ad esempio:

```text
E12-X1.7 Workforce Capacity Scaling
```

Se Kaggle/API non è accessibile dall'ambiente:

- NON aprire ripetutamente finestre browser;
- NON tentare loop di login;
- fermarsi e fornire il file pronto con le istruzioni minime per upload manuale.

---

## 6. Submission slot discipline

Prima dell'upload verificare il numero massimo di submission attive/visibili e la situazione corrente.

NON eliminare il champion E11-X1.7 se è ancora necessario come riferimento.

Se serve liberare uno slot:

- identificare la submission meno utile;
- proporre quale rimuovere;
- NON cancellare automaticamente il riferimento champion senza conferma.

---

## 7. Dati da registrare subito dopo l'upload

Registrare:

- timestamp;
- submission label;
- Kaggle score iniziale;
- ranking iniziale;
- stato (`running`, `scored`, errore);
- eventuale errore di validazione;
- screenshot/evidenza se disponibile.

---

## 8. Monitoraggio

La validazione Kaggle deve essere monitorata per almeno il periodo necessario a distinguere:

- score iniziale transitorio;
- score stabilizzato;
- ranking relativo.

Confrontare con:

- E11-X1.7 champion;
- altre submission E12 ancora visibili;
- top leaderboard osservabili.

Non trarre conclusioni dal primo aggiornamento se il leaderboard è ancora in assestamento.

---

## 9. Metriche di confronto esterno

Produrre una tabella:

| Variant | Local Mean | Kaggle Score | Relative Rank | Note |
|---|---:|---:|---:|---|
| E11-X1.7 | $28,083.80 | valore noto | rank | champion |
| E12-X1.7 | $22,386.80 | nuovo score | rank | external validation |

Aggiungere eventuali precedenti E12 se utili.

---

## 10. Interpretazione

### Caso A — Kaggle score nettamente peggiore di E11-X1.7

Conclusione:

```text
E12-X1.7 EXTERNAL UNDERPERFORMANCE
```

Procedere comunque con X1.8 soltanto come sviluppo della nuova architettura, non come candidate submission.

### Caso B — Kaggle score simile a E11-X1.7

Conclusione:

```text
E12 HYBRID ARCHITECTURE EXTERNALLY CREDIBLE
```

D3/X1.8 diventa prioritario perché siamo vicini al champion anche esternamente.

### Caso C — Kaggle score migliore di E11-X1.7

Conclusione:

```text
E12-X1.7 NEW EXTERNAL CHAMPION
```

Congelare la configurazione prima di ulteriori modifiche.

---

## 11. Nessun tuning durante la validazione

Durante questa fase NON modificare:

- crop timing;
- Worker #5;
- Q1/Q2;
- MELON horizon;
- worker count;
- tiles/worker;
- Cow scaling.

La submission deve rappresentare il risultato già validato localmente.

---

## 12. Documentazione

Creare/aggiornare:

```text
docs/versions/E12_X1_7_kaggle_external_validation.md
docs/PROJECT_STATE.md
docs/EXPERIMENT_LOG.md
```

Documentare:

- commit/source;
- hash submission;
- local metrics;
- Kaggle score;
- ranking;
- interpretazione.

---

## 13. Output richiesto

Restituire:

### A. Provenance check
### B. Build/test status
### C. Submission hash
### D. Upload status
### E. Kaggle score
### F. Ranking
### G. Comparison with E11-X1.7
### H. Recommendation

Una sola raccomandazione:

```text
PROCEED E12-X1.8 — EARLIER WORKFORCE / CAPACITY ACTIVATION
```

oppure:

```text
HOLD E12 — EXTERNAL PERFORMANCE TOO WEAK
```

oppure:

```text
E12-X1.7 NEW EXTERNAL CHAMPION — FREEZE & VALIDATE
```

---

## Approval

Questo prompt autorizza:

1. provenance check;
2. build;
3. test;
4. upload Kaggle;
5. monitoraggio score;
6. documentazione della validazione.

Non autorizza modifiche strategiche.

---

## Principio guida

> **Prima di correggere X1.7 con le evidenze D3, misuriamo quanto vale davvero l'architettura ibrida corrente sul leaderboard Kaggle.**
