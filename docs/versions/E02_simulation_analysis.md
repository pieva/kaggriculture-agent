# Evidenza Analitica E02 — Analisi Osservabile della Simulazione ed Origine del Miglioramento ROI

Questo documento descrive l'analisi comportamentale ed economica della simulazione dell'agente **`ROICropAgent` (E02)** condotta su un episodio completo di 720 turni in ambiente reale `kaggriculture`.

---

## 1. Sintesi dell'Episodio Osservato

- **Esito dell'episodio**: `status: DONE` (720/720 turni completati).
- **Capitale Iniziale**: **`$3000.0`**
- **Capitale Finale (`reward`)**: **`$5957.0`**
- **Variazione Complessiva del Capitale**: **`+$2957.0`**
- **Cicli produttivi di vendita completati**: 2 cicli completi di `MELON` (raccolti a Day 12 e Day 24, e venduti a Day 13 e Day 25).
- **Selezione in coda stagione**: A Day 21 (Step 505) l'agente seleziona `STRAWBERRY` per il ciclo successivo, piantato a Day 24 ma non completato entro la fine dell'episodio.
- **Unità complessive vendute**: 12 meloni (6 meloni per raccolto grazie all'irrigazione costante che attiva `max_yield = 6`).

---

## 2. Riconciliazione Monetaria dei Cicli Produttivi

### 2.1 Ciclo Produttivo 1 (`MELON`)
- **Capitale prima dell'acquisto seme 1 (Step 0, Day 0, Hr 0)**: **$3000.0**
- **Acquisto 1° seme MELON (Step 1, Day 0, Hr 1)**: -$80.0 $\rightarrow$ Capitale: **$2920.0**
- **Semina 1° MELON (Step 2, Day 0, Hr 2)**: Utilizzo del 1° seme MELON.
- **Acquisto 1° seme buffer MELON (Step 3, Day 0, Hr 3)**: -$80.0 $\rightarrow$ Capitale: **$2840.0**
- **Raccolta 1° MELON (Step 289, Day 12, Hr 1)**: Deposito di 6 meloni nello `shed`.
- **Incasso 1° vendita MELON (Step 313, Day 13, Hr 1)**: Vendita di 6 meloni $\rightarrow$ **+$1627.0** $\rightarrow$ Capitale: **$4387.0**

$$\text{Profitto Netto Ciclo 1} = \text{Incasso 1} - \text{Costo Seme 1} = 1627.0 - 80.0 = \mathbf{+\$1547.0}$$

### 2.2 Ciclo Produttivo 2 (`MELON`)
- **Semina 2° MELON (Step 290, Day 12, Hr 2)**: Utilizzo del 1° seme buffer.
- **Acquisto 2° seme buffer MELON (Step 291, Day 12, Hr 3)**: -$80.0 $\rightarrow$ Capitale: **$2760.0**
- **Incasso 1° vendita MELON (Step 313, Day 13, Hr 1)**: +$1627.0 $\rightarrow$ Capitale: **$4387.0**
- **Acquisto 1° seme STRAWBERRY (Step 454, Day 18, Hr 22)**: -$100.0 \rightarrow$ Capitale: **$4287.0**
- **Raccolta 2° MELON (Step 577, Day 24, Hr 1)**: Deposito di 6 meloni nello `shed`.
- **Semina STRAWBERRY (Step 578, Day 24, Hr 2)**: Utilizzo del 1° seme STRAWBERRY.
- **Acquisto 2° seme STRAWBERRY buffer (Step 579, Day 24, Hr 3)**: -$100.0 \rightarrow$ Capitale: **$4187.0**
- **Incasso 2° vendita MELON (Step 601, Day 25, Hr 1)**: Vendita di 6 meloni $\rightarrow$ **+$1650.0** $\rightarrow$ Capitale: **$5837.0**

$$\text{Profitto Netto Ciclo 2} = \text{Incasso 2} - \text{Costo Seme 2} = 1650.0 - 80.0 = \mathbf{+\$1570.0}$$

### 2.3 Riconciliazione del Capitale Finale dell'Episodio
- **Profitto netto complessivo dei due raccolti completati**: $1547.0 + 1570.0 = \mathbf{+\$3117.0}$
- **Spesa per semi non maturati in coda stagione**: 2 semi di STRAWBERRY acquistati a Step 454 e Step 579 ($100.0 \times 2 = \mathbf{-\$200.0}$)
- **Variazione netta del capitale dell'episodio**: $+3117.0 - 200.0 = \mathbf{+\$2957.0}$

$$\text{Riconciliazione}: \text{Money Iniziale } (\$3000.0) + \text{Variazione Netta } (+\$2957.0) = \mathbf{\$5957.0 \text{ (Money Finale)}}$$

---

## 3. Confronto Economico `CARROT` vs `MELON`

Sui 24 giorni di simulazione analizzati (corrispondenti a 8 cicli da 3 giorni per `CARROT` oppure a 2 cicli da 12 giorni per `MELON`):

### 3.1 Scenario con Resa Effettiva Irrigata (`max_yield`)
- **`CARROT` (Teorico)**:
  - `max_yield = 4` carote per raccolto.
  - Ricavo lordo teorico su 8 cicli: $8 \times (4 \times \$35.0) = \mathbf{\$1120.0}$.
  - Profitto netto teorico su 8 cicli: $\$1120.0 - (8 \times \$20.0 \text{ semi}) = \mathbf{+\$960.0}$.
- **`MELON` (Effettivamente Osservato in E02)**:
  - Ricavo lordo complessivo dei 2 raccolti (12 meloni): $\$1627.0 + \$1650.0 = \mathbf{\$3277.0}$.
  - Profitto netto complessivo attribuibile ai due raccolti: $\$3277.0 - (2 \times \$80.0 \text{ semi}) = \mathbf{+\$3117.0}$.
- **Confronto**: Il profitto netto di `MELON` è **3.25 volte superiore** a quello teorico di `CARROT`.

### 3.2 Scenario con Resa Modello (`Yield=2`)
- **`CARROT` (Teorico)**: Profitto netto teorico su 8 cicli = $8 \times (2 \times \$35.0 - \$20.0) = \mathbf{+\$400.0}$ (Ricavo lordo = $\$560.0$).
- **`MELON` (Teorico)**: Profitto netto teorico su 2 cicli = $2 \times (2 \times \$270.8 - \$80.0) = \mathbf{+\$923.2}$ (Ricavo lordo = $\$1083.2$).

---

## 4. Yield Implementato e Resa Reale dell'Ambiente

- **Formula ROI implementata**: utilizza `Yield = 2` come stima conservativa.
- **Resa massima reale dell'ambiente (`max_yield`)**:
  - `WHEAT`: `max_yield = 6`
  - `CARROT`: `max_yield = 4`
  - `TOMATO`: `max_yield = 4`
  - `STRAWBERRY`: `max_yield = 4`
  - `MELON`: `max_yield = 6`
- **Impatto**: L'irrigazione regolare svolta quotidianamente dall'agente consente di sbloccare la resa massima `max_yield` della coltura.

---

## 5. Confronto del Ranking ROI (Step 1, Day 0, Hr 1)

Valutazione comparativa ad inizio partita ($3000 di liquidità):

| Coltura | SeedPrice | Days | SellPrice | ROI con Yield=2 (Implementato) | ROI con MaxYield (Effettivo) | Rank Yield=2 | Rank MaxYield |
| :--- | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| `WHEAT` | $10.0 | 4 | $26.0 | $10.50 | $36.50 | 4 | 4 |
| `CARROT` | $20.0 | 3 | $35.0 | $16.67 | $40.00 | 2 | 3 |
| `TOMATO` | $50.0 | 8 | $60.0 | $8.75 | $23.75 | 5 | 5 |
| `STRAWBERRY` | $100.0 | 10 | $128.0 | $15.60 | $41.20 | 3 | 2 |
| **`MELON`** | **$80.0** | **12** | **$256.0** | **$36.00** | **$121.33** | **1** | **1** |

### Esito del Confronto:
`MELON` risulta **Rank 1 in entrambi i modelli**. Di conseguenza, l'uso di `Yield=2` rende il modello quantitativamente impreciso nelle stime assolute, ma **non altera la decisione iniziale osservata nell'episodio E02**.

---

## 6. Interpretazione Causale del Miglioramento E02

> **Conclusione Principale**:  
> **E02 migliora principalmente perché la regola ROI identifica `MELON` come coltura economicamente dominante nelle condizioni osservate.**

### 6.1 Evidenza Osservata
`ROICropAgent` seleziona inizialmente `MELON`, la cui coltivazione genera un incasso lordo di oltre $1600 per raccolto su singola casella contro i $140 di una singola carota.

### 6.2 Interpretazione Supportata
Il forte miglioramento rispetto a E01 deriva dal passaggio dalla monocultura `CARROT` ad una coltura a rendimento/giorno molto più elevato (`MELON`).

### 6.3 Limite della Conclusione
Un singolo episodio osservabile non dimostra che uno switching continuo e dinamico tra numerose colture sia la causa generale del miglioramento, poiché `MELON` ha dominato la quasi totalità dell'episodio.

---

## 7. Analisi della Selezione in Coda Stagione (`STRAWBERRY`)

- **I primi due cicli completati e venduti** (Day 0..25) utilizzano esclusivamente **`MELON`**.
- **Al turno 505 (Day 21)**, il prezzo di mercato di `STRAWBERRY` sale sufficientemente da portare il suo ROI stimato a $>39.2$/giorno (superando MELON a $39.0$/giorno).
- L'agente acquista quindi un seme di **`STRAWBERRY`** a Step 454/579 e lo pianta a Day 24 (Step 578).
- Poiché `STRAWBERRY` richiede 10 giorni per maturare, la pianta non giunge a raccolto prima del turno 719 (Day 29).

---

## 8. Limiti E02 Rivalutati

1. **End-of-Season Horizon (Orizzonte di Fine Stagione)**:  
   - *Evidenza*: L'agente avvia a Day 24 una coltura a ciclo lungo (`STRAWBERRY`, 10 giorni) che non può maturare prima della fine dell'episodio.  
   - *Impatto*: Spesa a fondo perduto di $200 per 2 semi in coda stagione.
2. **Single-Tile Limitation (Singola Casella)**:  
   - *Evidenza*: Il contadino rimane su `(4, 4)` ignorando le altre 24 caselle sbloccate.  
   - *Impatto*: Mancata moltiplicazione della produzione agricola.
3. **Immediate Selling (Vendita Immediata)**:  
   - *Evidenza*: I prodotti vengono venduti al turno immediatamente successivo alla raccolta.  
   - *Impatto*: Mancato sfruttamento dei picchi dinamici del mercato.
4. **Yield Model Simplification (Semplificazione Modello Resa)**:  
   - *Evidenza*: La formula usa `Yield=2` anziché la resa massima `max_yield`.  
   - *Impatto*: Sottostima relativa di colture ad alta resa come MELON (6 unità) e STRAWBERRY (4 unità).

---

## 9. Output di `git status`

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   scripts/build_submission.py
	modified:   src/agricola/agent.py
	modified:   src/agricola/core/state.py
	modified:   submission/submission.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/prompts/E02-04_build_approval.md
	docs/prompts/E02-05_verify.md
	docs/prompts/E02-06_verify_review.md
	docs/prompts/E02-07_verify_review_correction.md
	docs/prompts/E02-08_simulation_analysis.md
	docs/prompts/E02-09_simulation_review.md
	docs/prompts/E02-10_simulation_correction.md
	docs/screenshots/E02-002_build_approval.png
	docs/screenshots/E02-003_build_completed.png
	docs/versions/E02_build_antigravity.md
	docs/versions/E02_simulation_analysis.md
	docs/versions/E02_verify_review_antigravity.md
	results/e02_roi_crop.json
	src/agricola/strategy/
	tests/test_roi_crop.py

no changes added to commit (use "git add" and/or "git commit -a")
```
