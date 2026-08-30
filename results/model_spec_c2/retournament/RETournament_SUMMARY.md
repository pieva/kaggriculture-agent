# C2 — Retournament summary

```text
PROTOCOL: MODEL_SPEC_C2_RETOURNAMENT_FROZEN_V2
EPISODES_COMPLETE: 9/9
ENGINE_FRAMES: 6480
INTEGRATED_C2_READINESS: PASS
C2_RETournament_COMPLETE: YES
NO_KAGGLE_RUN_PERFORMED
```

## 1. Verifica integrata

- `git diff --check`: PASS.
- repository-wide `pytest`: 175 passed in 101,96 s; un solo warning non
  funzionale sulla cache pytest non scrivibile.
- Ruff repository: non configurato; nessun autofix eseguito.
- 9/9 episodi conclusi a 720 step con status `DONE` per entrambi i player.
- audit offline: 12.942/12.942 action riprodotte esattamente dai replay;
  errori 0, fallback 0, mismatch 0.

## 2. Ranking economico

La deviazione standard è campionaria (`ddof=1`) su sei score per candidato.

| Rank | Candidate | W-L-T | Mean | Median | Std | Min | Max | Completion | Error/Fallback |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Antigravity C2 | 5-1-0 | $16.671,00 | $16.969,50 | $1.616,36 | $13.783,00 | $18.347,00 | 6/6 | 0/0 |
| 2 | Codex C2 | 4-2-0 | $15.156,00 | $14.619,00 | $1.300,92 | $14.267,00 | $17.691,00 | 6/6 | 0/0 |
| 3 | Copilot C2 | 0-6-0 | $4.154,00 | $4.225,50 | $201,38 | $3.793,00 | $4.332,00 | 6/6 | 0/0 |

Antigravity batte Codex 2-1 nello scontro diretto, con differenziale cumulato
+$4.371. Il vantaggio medio Antigravity su Codex è $1.515, ma le distribuzioni
si sovrappongono: il ranking è utile, non una dimostrazione di dominanza fuori
dalle tre seed preregistrate.

## 3. Risultati dei nove episodi

| Round / seed | P0 | P0 money | P1 | P1 money | Winner |
|---|---|---:|---|---:|---|
| R1 / 1113294977 | Antigravity | $16.264 | Codex | $14.512 | Antigravity |
| R1 / 3033283457 | Antigravity | $13.783 | Codex | $14.267 | Codex |
| R1 / 1678077158 | Antigravity | $17.482 | Codex | $14.379 | Antigravity |
| R2 / 1113294977 | Antigravity | $16.457 | Copilot | $3.793 | Antigravity |
| R2 / 3033283457 | Antigravity | $17.693 | Copilot | $4.266 | Antigravity |
| R2 / 1678077158 | Antigravity | $18.347 | Copilot | $4.332 | Antigravity |
| R3 / 1113294977 | Codex | $14.726 | Copilot | $4.059 | Codex |
| R3 / 3033283457 | Codex | $15.361 | Copilot | $4.289 | Codex |
| R3 / 1678077158 | Codex | $17.691 | Copilot | $4.185 | Codex |

## 4. Stato produttivo ed economico

| Candidate | Active mean / max / final mean | First revenue step | Min cash | Max quadrants | Workforce max / effective mean |
|---|---:|---:|---:|---:|---:|
| Antigravity | 14,04 / 17 / 11,0 | 65 | $423 | 2 | 10 / 9,61 |
| Codex | 13,46 / 24 / 3,5 | 53 | $302 | 2 | 9 / 8,62 |
| Copilot | 3,30 / 4 / 4,0 | 73 | $2.920 | 1 | 1 / 1,00 |

Codex realizza la superficie massima più ampia, ma il final mean 3,5 mostra il
ritiro crop-aware di fine orizzonte. Antigravity mantiene 11 tile finali.
Copilot chiude stabilmente quattro tile senza land o workforce aggiuntiva.

## 5. Action dispatch e state transition

Valori medi per episodio, espressi come `dispatch / effect`. L'effect richiede
una transizione osservabile coerente nel frame engine, quindi non tutti gli
opcode emessi diventano necessariamente una transizione nello stesso step.

| Candidate | PLANT | WATER | HARVEST | DIG | MOVE |
|---|---:|---:|---:|---:|---:|
| Antigravity | 112,0 / 80,0 | 492,0 / 258,0 | 107,0 / 89,0 | 30,0 / 29,0 | 4.377,0 / 710,0 |
| Codex | 183,5 / 122,8 | 415,5 / 264,5 | 142,8 / 117,8 | 67,0 / 57,7 | 4.931,2 / 704,3 |
| Copilot | 60,0 / 60,0 | 120,0 / 120,0 | 56,0 / 56,0 | 0,0 / 0,0 | 132,0 / 132,0 |

La differenza dispatch/effect per MOVE riflette soprattutto molte unità in
movimento nello stesso step contro un singolo cambio congiunto di posizioni;
non va interpretata come 3.000+ failure di movimento.

## 6. Market dispatch ed effetti

| Candidate | Market total | BUY_SEED dispatch/effect | SELL dispatch/effect | BUY_LAND dispatch/effect | HIRE dispatch/effect |
|---|---:|---:|---:|---:|---:|
| Antigravity | 443,0 | 84,0 / 62,0 | 88,0 / 80,0 | 1,0 / 1,0 | 270,0 / 41,0 |
| Codex | 529,2 | 126,5 / 112,2 | 121,2 / 114,0 | 1,0 / 1,0 | 240,0 / 32,0 |
| Copilot | 71,0 | 57,0 / 43,0 | 14,0 / 14,0 | 0,0 / 0,0 | 0,0 / 0,0 |

HIRE effect conta gli step in cui la workforce cresce, non il numero di hands
assunte. BUY_SEED e SELL effect richiedono rispettivamente incremento seed e
riduzione del prodotto/crescita di cassa osservabili.

## 7. Efficacia delle remediation

### Antigravity

- il collasso a $3.000 è eliminato: mean $16.671, minimo $13.783;
- ciclo produttivo reale: active max 17, PLANT/WATER/HARVEST/SELL con effetti
  osservati e first revenue step 65;
- 6/6 completion, 0 errori, 0 fallback.

### Copilot

- il collasso runtime/economico a $3.000 è eliminato: mean $4.154;
- ciclo produttivo reale ma minimale: quattro crop, un worker, un quadrante,
  first revenue step 73;
- 6/6 completion, 0 errori, 0 fallback;
- la remediation chiude il ciclo, non colma il gap di capacità competitiva.

### Codex

- active mean sale dal precedente 9,17 a 13,46 e il massimo da 16 a 24;
- first revenue passa dal precedente step 321 allo step 53;
- la cassa minima resta sopra il floor ($302) e il ciclo economico è osservato;
- mean final money scende da $16.846,50 a $15.156 (-$1.690,50; -10,03%).

L'ultimo delta è descrittivamente corretto ma non identifica causalmente il
solo cambiamento Codex: nel retournament anche gli avversari sono remediati e
competono sullo stesso mercato, mentre nel C2 originale erano bloccati a
$3.000. La remediation Codex migliora chiaramente realization e cash timing,
ma non migliora il final money in questo confronto congiunto.

## 8. Confronto con il C2 originale

| Candidate | Original mean | Remediated mean | Delta | Delta % | Validità |
|---|---:|---:|---:|---:|---|
| Antigravity | $3.000,00 | $16.671,00 | +$13.671,00 | +455,70% | forte evidenza di rimozione del collasso |
| Codex | $16.846,50 | $15.156,00 | -$1.690,50 | -10,03% | descrittivo; non isolabile dagli avversari remediati |
| Copilot | $3.000,00 | $4.154,00 | +$1.154,00 | +38,47% | evidenza di closure, capacità ancora ridotta |

## 9. Riferimento storico Kaggriculture

Il miglior candidato, Antigravity con mean $16.671 e max $18.347, resta sotto i
riferimenti locali ~21–23k:

- gap dalla soglia $21k: $4.329 (-20,61%);
- gap dalla soglia $23k: $6.329 (-27,52%).

Il retournament risolve la confrontabilità e produce un ranking, ma non
raggiunge ancora la capacità economica storica. Il superamento del vecchio
failure da $3.000 non costituisce da solo successo strategico.

## 10. Interpretazione

```text
RUNTIME REALIZATION
PASS — 18/18 player-episode DONE, 0 errori, 0 fallback,
       12.942 action riprodotte senza mismatch.

ECONOMIC CLOSURE
PASS FORTE — Antigravity e Codex chiudono cicli multi-crop a $15–17k mean.
PASS MINIMA — Copilot monetizza realmente, ma resta a $4,15k mean.

COMPETITIVE CAPACITY
RANKING VALIDO — Antigravity > Codex >> Copilot sulle seed congelate.
CAPACITÀ INSUFFICIENTE — anche il leader resta sotto ~21–23k.
```

Esito: torneo valido con ranking utile; dispersione e sole tre shared seed
impongono cautela sulla distanza Antigravity/Codex. Non sono state aggiunte seed.

## 11. Artifact

- `results/model_spec_c2/retournament/INTEGRATED_READINESS.md`
- `results/model_spec_c2/retournament/RETournament_PROTOCOL.md`
- `results/model_spec_c2/retournament/RETournament_SUMMARY.md`
- `results/model_spec_c2/retournament/aggregated_results.json`
- `results/model_spec_c2/retournament/aggregated_results.csv`
- `results/model_spec_c2/retournament/raw/` — 9 summary arricchiti e 9 replay
- `scripts/analyze_c2_retournament.py` — analisi neutrale e audit action replay

```text
INTEGRATED_C2_READINESS: PASS
C2_RETournament_COMPLETE: YES
KAGGLE_RUN: NO
```
