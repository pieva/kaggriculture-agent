# E03 — Multi-Tile Scaling — VERIFY

La fase BUILD di E03 è completata.

Risultato BUILD:

- `MultiTileROIAgent` implementato;
- cluster gestito: `{(4,4), (4,3), (3,4), (3,3)}`;
- priorità: `HARVEST > PLANT > WATER`;
- navigazione Manhattan;
- tie-breaking deterministico `(y, x)`;
- movement bug fix applicato;
- suite completa: `14 passed`, `0 failed`.

Metodo sperimentale:

`DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP`

Procedi ora esclusivamente con la fase:

# VERIFY

Non modificare la strategia E03 durante questa fase.

Non ottimizzare il codice sulla base dei risultati osservati.

Se emergono problemi, documentali prima di proporre qualsiasi correzione.

---

## 0. Chiarimento preliminare sullo stato della submission

Lo stato Git al termine della BUILD riportava:

```text
M submission/submission.py
```

anche se la fase SHIP non è stata autorizzata.

Prima della VERIFY determina esclusivamente:

- perché `submission/submission.py` risulta modificato;
- quale comando o test lo ha rigenerato/modificato;
- se la modifica è semplicemente il risultato automatico del processo di BUILD/test oppure se è stata eseguita un'attività non prevista.

Documenta la spiegazione.

NON caricare la submission su Kaggle.

NON eseguire SHIP.

NON modificare il file per il solo scopo di ripristinarlo prima di averne spiegato l'origine.

---

# VERIFY A — Episodio osservabile

Esegui un singolo episodio E03 da:

`720 step`

utilizzando un avversario coerente con le verifiche precedenti.

Lo scopo non è ottenere una performance statisticamente significativa, ma verificare empiricamente il comportamento del nuovo agente.

## Evidenze richieste

Traccia almeno:

- turno;
- posizione del farmer;
- tile target;
- classe di priorità attiva:
  - `HARVEST`;
  - `PLANT`;
  - `WATER`;
  - `PASS`;
- movimento eseguito;
- ordini di mercato;
- coltura selezionata;
- numero di semi;
- stato delle quattro tile;
- azioni `PLANT`;
- azioni `WATER`;
- azioni `HARVEST`;
- vendite;
- money;
- eventuali anomalie.

Non è necessario stampare tutti i 720 turni se questo rende il log inutilizzabile.

Produci invece una trace leggibile contenente gli eventi significativi e sufficienti a dimostrare il comportamento.

## La VERIFY osservabile deve dimostrare concretamente

### Multi-tile

L'agente deve utilizzare realmente più di una tile del cluster:

`{(4,4), (4,3), (3,4), (3,3)}`

Idealmente devono essere osservabili tutte e quattro.

### Movimento

Deve essere osservato almeno un movimento reale mediante:

- `["NORTH"]`
- `["SOUTH"]`
- `["EAST"]`
- `["WEST"]`

e deve essere dimostrato che il farmer cambia effettivamente posizione nell'ambiente.

Questo deve confermare empiricamente il bug fix di `ActionBuilder.move()`.

### Target selection

Mostra almeno alcuni casi che permettano di verificare:

`HARVEST > PLANT > WATER`

e la scelta della tile più vicina all'interno della classe di priorità più alta disponibile.

### Stato indipendente delle tile

Dimostra che tile differenti possono trovarsi contemporaneamente in stati differenti e che l'agente le gestisce correttamente.

### Ciclo produttivo

Osserva almeno un ciclo effettivamente completato:

`BUY_SEED → PLANT → WATER → HARVEST → SELL`

su più tile.

### Irrigazione

Verifica esplicitamente che la priorità `HARVEST > PLANT > WATER` non provochi starvation dell'irrigazione.

Segnala:

- eventuali tile non irrigate quando avrebbero dovuto esserlo;
- eventuali ritardi sistematici;
- effetti osservabili sulla resa.

### Stabilità

Verifica:

- assenza di loop di movimento;
- assenza di oscillazioni tra tile;
- assenza di deadlock;
- assenza di azioni invalide;
- completamento dell'episodio;
- assenza di disqualification.

---

## Evidenza documentale

Salva la VERIFY osservabile in:

`docs/versions/E03_verify_antigravity.md`

Includi una sequenza di eventi sufficientemente dettagliata da poter ricostruire il comportamento dell'agente.

Non interpretare ancora il risultato competitivo.

---

# VERIFY B — Benchmark quantitativo

Solo dopo che la VERIFY osservabile ha dimostrato il corretto funzionamento operativo, esegui il benchmark completo E03.

Mantieni la configurazione identica a E01/E02:

- `30` episodi totali;
- `10` vs `pass`;
- `10` vs `random`;
- `10` vs `starter`;
- `720` step per episodio.

Utilizza l'infrastruttura esistente senza modificare metriche o avversari.

Salva i risultati in:

`results/e03_multi_tile.json`

---

## Metriche obbligatorie

Riporta:

- Total Episodes;
- Completion Rate;
- Disqualification Rate;
- Overall Win Rate;
- Win Rate vs `pass`;
- Win Rate vs `random`;
- Win Rate vs `starter`;
- Mean Final Money;
- Sample Std Dev (`ddof=1`);
- Median Final Money;
- Agent Mean Turn Latency.

---

# Confronto E02 → E03

Baseline E02:

- Mean Final Money: `$5857.17`;
- Sample Std Dev: `$132.37`;
- Median Final Money: `$5837.00`;
- Overall Win Rate: `100.00%`;
- Win Rate vs `starter`: `100.00%`;
- Agent Mean Turn Latency: `0.0267 ms/turno`.

Calcola per Mean Final Money:

- differenza assoluta;
- differenza percentuale.

Non confondere queste metriche con il Kaggle Skill Rating.

---

# Criterio sperimentale primario

L'ipotesi economica E03 è supportata, nelle condizioni sperimentali testate, se:

`Mean Final Money E03 > $5857.17`

Il valore:

`$10,000`

rimane esclusivamente un target esplorativo e NON costituisce criterio obbligatorio.

---

# Criteri operativi

Verifica anche:

- Completion Rate = `100%`;
- Disqualification Rate = `0%`;
- nessun errore operativo grave;
- Agent Mean Turn Latency `< 0.1 ms/turno`.

Overall Win Rate e Win Rate vs `starter` devono essere riportati e confrontati con E02, ma non alterare né adattare l'agente durante VERIFY per mantenere artificialmente il `100%`.

---

# Interpretazione

Al termine classifica separatamente:

## Validità operativa

Uno tra:

- `PASSED`
- `PASSED WITH OBSERVATIONS`
- `FAILED`

## Ipotesi economica E03

Uno tra:

- `SUPPORTED`
- `NOT SUPPORTED`
- `INCONCLUSIVE`

utilizzando esclusivamente le evidenze prodotte dalla VERIFY.

Un eventuale risultato peggiore di E02 è un risultato sperimentale valido e NON deve essere corretto durante questa fase.

---

# Git

Al termine mostra:

```powershell
git status --short
```

Non eseguire commit.

---

# STOP

NON modificare `MultiTileROIAgent`.

NON cambiare il numero di tile.

NON modificare le priorità.

NON introdurre end-of-season optimization.

NON introdurre market timing.

NON modificare la formula ROI.

NON acquistare terra.

NON effettuare tuning dopo aver visto i risultati.

NON caricare alcuna submission su Kaggle.

NON eseguire SHIP.

Al termine mostra:

1. origine della modifica già presente in `submission/submission.py`;
2. risultato della VERIFY osservabile;
3. principali evidenze multi-tile;
4. risultato del benchmark;
5. confronto numerico E02 → E03;
6. validità operativa;
7. valutazione dell'ipotesi E03;
8. eventuali anomalie;
9. file prodotti;
10. stato Git.

Attendi la REVIEW prima di qualsiasi altra modifica.