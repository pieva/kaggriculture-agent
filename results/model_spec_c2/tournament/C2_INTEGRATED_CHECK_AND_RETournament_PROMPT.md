# C2 — Verifica integrata finale e retournament immediato

## Mandato

Esegui ora la **verifica integrata finale del repository** e, se tutti i controlli risultano verdi, avvia immediatamente il **retournament C2** tra i tre candidati remediati:

- Antigravity C2
- Codex C2
- Copilot C2

Questa fase serve a verificare direttamente se le remediation indipendenti hanno prodotto tre policy realmente confrontabili e se la qualità economica del round C2 migliora rispetto al tournament precedente.

Non aprire C3. Non introdurre nuovi tuning, modifiche strategiche, modifiche Foundation o nuove remediation durante questa fase.

---

## 1. Stato di ingresso

### Antigravity C2
Stato dichiarato:

```text
C2_REMEDIATION_COMPLETE
TOURNAMENT_READY: YES
```

Evidenza disponibile:
- real-engine P0/P1 completo;
- 0 errori / 0 fallback;
- lifecycle produttivo realizzato;
- regression suite dichiarata verde nel worktree finale osservato dall'agente.

### Codex C2
Stato dichiarato:

```text
REMEDIATION_COMPLETE: YES
TOURNAMENT_READY: YES
```

Evidenza disponibile:
- real-engine P0/P1;
- 0 errori / 0 fallback;
- max active surface 23;
- primo ciclo economico step 53;
- cash 3000 iniziale / 379 minimo / 7895 finale;
- test candidato 18 passed;
- suite completa 175 passed;
- Ruff PASS;
- `git diff --check` PASS.

### Copilot C2
Stato dichiarato:

```text
C2_REMEDIATION_COMPLETE
TOURNAMENT_READY: YES
```

Evidenza disponibile:
- real-engine P0/P1;
- bootstrap, movement, seed acquisition, PLANT/WATER/HARVEST/SELL realizzati;
- cash 3000 → 3083 nel preflight;
- test candidato 7 passed.

Il precedente failure della suite completa osservato durante la remediation Copilot era attribuito a modifiche Codex concorrenti nel worktree. Deve quindi essere risolto definitivamente dalla verifica integrata seguente.

---

# 2. Regole di fase

Durante questa fase:

```text
NO FOUNDATION CHANGE
NO MODEL_SPEC CHANGE
NO POLICY CHANGE
NO CONFIG CHANGE
NO TEST CHANGE
NO REMEDIATION
NO TUNING
NO KAGGLE SUBMISSION
```

È consentito modificare esclusivamente:
- runner del retournament, se necessario per eseguire correttamente il protocollo già definito;
- artifact/report/result del retournament;
- eventuale telemetry/reporting neutrale che non modifichi il comportamento dei candidati.

Se un controllo integrato fallisce per un candidato, **NON correggere il candidato** in questa fase. Arresta il retournament e documenta il blocker.

---

# 3. Verifica integrata finale

Esegui sul worktree risultante dalle tre remediation:

```powershell
git status --short
git diff --check
.\.venv\Scripts\pytest.exe -q
```

Se Ruff è configurato nel repository e applicabile ai file Python modificati nel round, esegui anche il check Ruff senza autofix.

## Criterio di passaggio

Per poter avviare il retournament devono risultare contemporaneamente:

```text
git diff --check: PASS
pytest repository-wide: PASS
0 failure di import/runtime nei tre candidati
```

Non richiedere un nuovo preflight esteso se le evidenze P0/P1 già prodotte sono integre. È ammesso un **sanity check minimo** dei tre entrypoint solo se necessario a escludere un problema di integrazione del worktree finale.

Se tutto passa, registra:

```text
INTEGRATED_C2_READINESS: PASS
RETournament_AUTHORIZED: YES
```

E procedi immediatamente al torneo.

---

# 4. Protocollo del retournament

Mantieni il confronto il più possibile compatibile con il Tournament C2 precedente per consentire il confronto causale pre/post remediation.

Usa:
- gli stessi tre candidati remediati congelati;
- gli stessi pairwise matchup;
- gli stessi shared seed del tournament C2 precedente, salvo blocker tecnico documentato;
- 720 step per episodio;
- nessun mirroring aggiuntivo, dato che il precedente Stage A-R1 aveva classificato l'effetto di posizione come trascurabile per la performance;
- stessa metrica economica primaria: `final_money`;
- stessa raccolta di telemetry comparabile dove disponibile.

Shared seed precedenti:

```text
1113294977
3033283457
1678077158
```

Pairwise:

```text
Antigravity vs Codex
Antigravity vs Copilot
Codex vs Copilot
```

Totale previsto:

```text
3 matchup × 3 seed = 9 episodi completi
```

Non introdurre nuove seed per “migliorare” o stabilizzare il risultato prima di aver prodotto il risultato preregistrato su queste 9 partite.

---

# 5. Metriche obbligatorie

Per ogni candidato aggrega almeno:

- W / L / T
- mean final money
- median final money
- sample std (`ddof=1`)
- min / max final money
- error count
- fallback count
- completion rate
- active surface mean / max / final, se disponibile
- PLANT / WATER / HARVEST / DIG
- MOVE, se disponibile e semanticamente confrontabile
- market orders / BUY_SEED / SELL / BUY_LAND / HIRE, se disponibile
- first revenue step, se disponibile
- minimum cash, se disponibile
- land/quadrants utilizzati, se disponibile
- workforce effettiva, se disponibile

Distingui sempre:

```text
ACTION DISPATCH
STATE TRANSITION
ECONOMIC EFFECT
```

Non interpretare un opcode emesso come prova di policy realization se non corrisponde a un effetto osservabile.

---

# 6. Confronti obbligatori

Il report deve rispondere a quattro domande distinte.

## A. Remediation effectiveness

Per Antigravity e Copilot:
- il collasso a $3.000 è eliminato?
- la policy realizza realmente il ciclo produttivo?
- errori/fallback sono zero?

Per Codex:
- la remediation supera il precedente C2 economico?
- active surface, cash cycle e monetizzazione migliorano rispetto alla V1?

## B. Competitive ranking C2 remediated

Classifica i tre candidati per `mean final_money` e indica dispersione e stabilità.

## C. Confronto con il Tournament C2 originale

Riferimento precedente:

```text
Codex C2 original mean final money ≈ 16,846.50
Antigravity C2 original = 3,000
Copilot C2 original = 3,000
```

Calcola per ogni candidato:

```text
Δ assoluto
Δ percentuale
```

quando il confronto è semanticamente valido.

## D. Confronto con la traiettoria storica Kaggriculture

Il report deve dichiarare esplicitamente se il miglior candidato remediated:
- resta sotto i precedenti riferimenti locali ~21–23k;
- li raggiunge;
- li supera.

Non dichiarare successo strategico solo perché Antigravity/Copilot non sono più bloccati.

L'obiettivo strategico resta molto superiore al semplice superamento del C2 precedente.

---

# 7. Interpretazione

Separare esplicitamente:

```text
RUNTIME REALIZATION
ECONOMIC CLOSURE
COMPETITIVE CAPACITY
```

Possibili esiti:

### Caso 1 — tutti operativi, uno nettamente superiore
Il tournament è valido e produce un ranking utile.

### Caso 2 — tutti operativi ma tutti ancora economicamente deboli
Il problema di readiness è risolto ma resta un problema strategico di capacità/monetizzazione.

### Caso 3 — uno o più candidati ricadono in failure runtime/economic closure
Il problema di readiness non è ancora chiuso; non mascherarlo con la classifica economica.

### Caso 4 — risultati molto vicini o instabili
Dichiarare l'incertezza; non aggiungere automaticamente altre seed in questa fase.

---

# 8. Artifact richiesti

Salva almeno:

```text
results/model_spec_c2/retournament/INTEGRATED_READINESS.md
results/model_spec_c2/retournament/RETournament_PROTOCOL.md
results/model_spec_c2/retournament/RETournament_SUMMARY.md
results/model_spec_c2/retournament/aggregated_results.json
results/model_spec_c2/retournament/aggregated_results.csv
results/model_spec_c2/retournament/raw/
```

Se il runner precedente può essere riutilizzato senza modifiche comportamentali, preferisci riutilizzarlo.

Se deve essere modificato solo per telemetry/reporting, documenta la modifica e dimostra che non cambia il comportamento dei candidati.

---

# 9. Stop condition

Al termine del retournament:

```text
C2_RETournament_COMPLETE
NO_KAGGLE_RUN_PERFORMED
```

Non avviare automaticamente:
- Kaggle;
- C3;
- ulteriori remediation;
- tuning;
- nuova selezione di hyperparameter;
- modifiche Foundation/MODEL_SPEC.

Il risultato del retournament deve essere prima analizzato e deciso dal supervisore.

---

# 10. Output finale richiesto

Restituisci una sintesi molto compatta con:

1. esito verifica integrata;
2. suite test finale;
3. ranking economico dei tre candidati;
4. mean / median / std / min / max per candidato;
5. error/fallback/completion;
6. confronto con il C2 originale;
7. interpretazione in termini di runtime realization / economic closure / competitive capacity;
8. percorsi degli artifact prodotti;
9. stato finale:

```text
INTEGRATED_C2_READINESS: PASS|FAIL
C2_RETournament_COMPLETE: YES|NO
KAGGLE_RUN: NO
```
