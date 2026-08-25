# E05-07 — Kaggle Submission & External Validation

L'esperimento **E05 — HIRE / Multi-Worker Scaling** è già stato completato e shipped localmente.

Stato consolidato:

- Strategia: `HIRENWClusterROIAgent`
- Tag: `v0.5-e05-hire-multiworker`
- Test Suite: `PASSED`
- Standalone Build: `PASSED`
- Experimental Integrity: `PASSED`
- Economic Hypothesis: `SUPPORTED`
- Experiment Evaluation: `STRONG SUCCESS`
- Working tree atteso: pulito

Questo prompt riguarda esclusivamente la **submission Kaggle e la validazione esterna sulla leaderboard**.

La submission Kaggle non modifica retroattivamente la validità del benchmark locale E05.

Non modificare la strategia in funzione del punteggio Kaggle.

Non effettuare tuning.

---

## 1. Obiettivo

Sottomettere su Kaggle la standalone submission E05 già validata:

`submission/submission.py`

e registrare il risultato come evidenza di **external validation**.

La finalità è verificare il comportamento dell'agente nell'infrastruttura ufficiale della competizione, mantenendo separati:

- benchmark locale;
- risultato Kaggle.

---

## 2. Controllo preliminare del repository

Prima della submission verifica:

```powershell
git status
git log -1 --oneline
git tag --list
```

Conferma:

- branch `main`;
- `main` allineato con `origin/main`;
- working tree pulito;
- tag `v0.5-e05-hire-multiworker` presente.

Non modificare il codice se questi requisiti sono soddisfatti.

---

## 3. Verifica standalone E05

Controlla che:

`submission/submission.py`

contenga effettivamente:

`HIRENWClusterROIAgent`

come strategia corrente.

Verifica inoltre che il file sia self-contained e coerente con l'ultima BUILD E05.

Se necessario, rigenera esclusivamente tramite:

```powershell
.venv\Scripts\python.exe scripts/build_submission.py
```

Non modificare manualmente `submission/submission.py`.

---

## 4. Test finale pre-submission

Esegui:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Condizione richiesta:

`25 passed`

o il numero corrente equivalente, se nel frattempo la suite è aumentata legittimamente.

Se esistono failure:

**FERMATI.**

Non procedere con la submission Kaggle.

---

## 5. Submission Kaggle

Individua il workflow già utilizzato nel progetto per E01.

Se la submission richiede interazione manuale tramite interfaccia web Kaggle, non simulare l'upload.

Prepara invece:

- il file corretto da caricare;
- il nome/descrizione consigliata della submission;
- eventuali istruzioni operative minime.

Nome consigliato:

`E05 HIRE Multi-Worker Scaling`

Descrizione consigliata:

`E05 - HIRENWClusterROIAgent - 9 tiles, 1 farmer + 1 daily hand`

Se il repository dispone già di un comando/script funzionante per la submission Kaggle e le credenziali sono configurate, puoi utilizzarlo.

Non introdurre nuove credenziali nel repository.

Non salvare token o API key.

---

## 6. Evidenza della submission

Dopo l'invio, registra almeno:

- data della submission;
- nome della submission;
- versione/tag associato:
  `v0.5-e05-hire-multiworker`;
- file inviato:
  `submission/submission.py`;
- stato iniziale della submission;
- eventuale Submission ID disponibile.

Se l'invio viene effettuato manualmente dall'utente, predisponi la documentazione e attendi il risultato riportato dall'utente.

---

## 7. Risultato Kaggle

Quando il risultato è disponibile, registra:

- Kaggle Score;
- eventuale posizione leaderboard;
- eventuale stato `successful`, `error`, `failed` o equivalente;
- timestamp o data del risultato;
- eventuali messaggi diagnostici mostrati da Kaggle.

Non confrontare il punteggio Kaggle direttamente con `Mean Final Money` locale come se fossero la stessa metrica.

Sono due evidenze diverse.

---

## 8. Confronto con submission precedenti

Se il repository contiene evidenze Kaggle precedenti, confronta E05 con esse.

In particolare, per E01 è disponibile una submission Kaggle con score storico.

Riporta il confronto solo se i valori sono realmente documentati.

Non ricostruire o stimare score mancanti.

Struttura consigliata:

| Iterazione | Strategia | Local Mean Final Money | Kaggle Score | Note |
|---|---|---:|---:|---|
| E01 | `CarrotLoopAgent` | valore storico | valore storico | baseline |
| E05 | `HIRENWClusterROIAgent` | `$21568.93 ± $361.25` | valore osservato | external validation |

Se altre submission E02–E04 non sono state effettuate o non sono documentate, indicare `N/A`.

---

## 9. Interpretazione

Mantieni rigorosamente separate:

### Local Validation

E05 benchmark locale:

- 30 episodi;
- Mean Final Money:
  `$21568.93 ± $361.25`;
- Completion:
  `100%`;
- Disqualification:
  `0%`.

### Kaggle External Validation

Score e ranking ufficiali della submission.

Il risultato Kaggle può:

- rafforzare la fiducia nell'agente;
- mostrare differenze fra benchmark locale e ambiente competitivo reale;
- evidenziare eventuali problemi di generalizzazione.

Non deve essere usato retroattivamente per cambiare il risultato sperimentale locale già shipped.

---

## 10. Caso di score peggiore del previsto

Se il Kaggle Score è inferiore alle aspettative:

- non modificare E05;
- non effettuare tuning;
- non rieseguire automaticamente una submission modificata;
- registra semplicemente la discrepanza;
- trattala come nuova evidenza per una possibile iterazione futura.

E05 rimane shipped sulla base del protocollo locale già validato.

---

## 11. Caso di submission failure

Se Kaggle rifiuta la submission o restituisce errore tecnico:

1. raccogli il messaggio di errore;
2. determina se si tratta di:
   - packaging;
   - import;
   - schema action;
   - timeout;
   - runtime;
   - altro problema tecnico;
3. non modificare la strategia economica;
4. limita eventuali correzioni alla compatibilità della standalone submission;
5. documenta ogni correzione.

Se la correzione cambia il comportamento dell'agente, **FERMATI** prima di una nuova submission.

---

## 12. Screenshot / evidenze manuali

Se la submission viene effettuata dall'interfaccia Kaggle, salva screenshot coerenti con le convenzioni del progetto.

Preferibilmente almeno:

1. submission pronta/inviata;
2. submission completata con score;
3. leaderboard o pagina che mostri il risultato E05, se utile.

Utilizza nomi coerenti con gli screenshot esistenti, ad esempio:

`docs/screenshots/E05-001_kaggle_submission_ready.png`

`docs/screenshots/E05-002_kaggle_submission_successful.png`

`docs/screenshots/E05-003_kaggle_leaderboard.png`

Adatta i nomi alle convenzioni effettive già presenti nel repository.

Non creare screenshot artificiali.

---

## 13. Documento di external validation

Crea:

`docs/versions/E05_kaggle_validation.md`

Il documento deve contenere almeno:

1. **Obiettivo**
2. **Versione E05 sottoposta**
3. **Standalone artifact**
4. **Test pre-submission**
5. **Procedura di submission**
6. **Submission metadata**
7. **Kaggle Score**
8. **Leaderboard position**, se disponibile
9. **Confronto con submission precedenti**
10. **Confronto Local vs Kaggle**
11. **Eventuali anomalie**
12. **Screenshot / evidenze**
13. **Interpretazione**
14. **External Validation Decision**

Decisione finale ammessa:

- `EXTERNAL VALIDATION PASSED`
- `EXTERNAL VALIDATION PARTIAL`
- `EXTERNAL VALIDATION FAILED`
- `PENDING KAGGLE RESULT`

---

## 14. Aggiornamento documentazione

Solo dopo avere un risultato Kaggle effettivo, valuta aggiornamenti minimi a:

- `README.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`
- `docs/EXPERIMENT_LOG.md`

Aggiungi il Kaggle Score come **external validation**, mantenendolo separato dal benchmark locale.

Non riscrivere i risultati E05 già consolidati.

---

## 15. Commit della validazione Kaggle

Dopo aver registrato il risultato e le eventuali evidenze:

```powershell
git status
git diff --stat
```

Verifica che le modifiche riguardino esclusivamente:

- documentazione Kaggle;
- screenshot;
- eventuali artifact di validazione;
- eventuali minime correzioni di packaging, solo se necessarie e documentate.

Se tutto è corretto:

```powershell
git add .
git commit -m "Add E05 Kaggle external validation"
git push origin main
```

Non creare un nuovo tag sperimentale.

Il tag E05 resta:

`v0.5-e05-hire-multiworker`

perché identifica la strategia shipped prima della validazione esterna.

---

## 16. Condizione finale

Se la submission può essere effettuata automaticamente e il risultato è già disponibile:

1. mostra test pre-submission;
2. mostra file inviato;
3. mostra metadata submission;
4. mostra Kaggle Score;
5. mostra posizione leaderboard, se disponibile;
6. mostra confronto con E01 e altre submission documentate;
7. mostra External Validation Decision;
8. indica il percorso:
   `docs/versions/E05_kaggle_validation.md`;
9. mostra `git status`;
10. mostra eventuale commit/push effettuato.

Se invece serve un passaggio manuale dell'utente sull'interfaccia Kaggle:

1. verifica il file da caricare;
2. indica esattamente quale file selezionare;
3. indica nome e descrizione della submission;
4. **FERMATI prima di inventare un risultato**;
5. attendi che l'utente fornisca screenshot o score.

Non iniziare E06.