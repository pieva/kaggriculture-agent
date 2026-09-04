# MODEL SPEC — ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1

- **Candidate ID**: `ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1`
- **Model Spec Version**: `ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1`
- **Experiment**: `E18`
- **Round Role**: `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Author**: Antigravity Pair Programmer
- **Date**: 2026-09-04
- **Runtime Module**: `src/agricola/strategy/antigravity/antigravity_e18_reactive_reboot_v1.py`
- **Configuration**: `docs/model_specs/antigravity/e18/configs/ANTIGRAVITY_E18_1_REACTIVE_REBOOT_V1.json`

---

## 1. Diagnosi Causale del Fallimento E17 (Engine Contract Audit)

Nel torneo a quattro E18 V2 (`experiments/e18/artifacts/derived/common/E18_FOUR_AGENT_REACTIVE_TOURNAMENT_V2.json`), la linea Antigravity E17 (`antigravity_e17_native_3q.py`) ha totalizzato un record di `0-42-0` con $0 di profitto finale, 0 crop raccolti, 0 animali, 0 hands assunti e oltre 700 `PASS` per partita.

L'audit analitico del codice e delle prime decisioni ha individuato la causa scatenante esatta:
1. **Drenaggio Immediato del Capitale**: In `ANTIGRAVITY_E17_0_NATIVE_3Q_BASELINE_CONFIG.json`, `q1_unlock_day = 0` e `q2_unlock_day = 0` con soglia cassa di $2000. Al turno 0 e 1, l'agente ha emesso due ordini consecutivi di `BUY_LAND`, spendendo $1000 per NE (Q1) e $2000 per SW (Q2), azzerando interamente il capitale iniziale di $3000 nei primi due turni.
2. **Priorità di Mercato Invertita**: Gli ordini `BUY_LAND` avevano priorità assoluta su `BUY_SEED`. Con $0 residui, non è stato possibile acquistare alcun seme.
3. **Assenza di Forza Lavoro**: L'agente non assumeva lavoratori (`hands: []` fisso).
4. **Stallo del Contadino**: Il contadino ha ripulito 2-4 erbacce iniziali sulle caselle obiettivo (`DIG`), dopodiché, non avendo semi per piantare né colture da curare/raccogliere né merce nello shed da vendere, ha restituito `PASS` per i restanti 710 turni.

---

## 2. Architettura E18.1 a Cinque Livelli

Per superare i limiti di E17, la nuova architettura `ANTIGRAVITY-E18.1-REACTIVE-REBOOT-V1` implementa cinque livelli modulari e deterministici:

```text
[Livello 1: PUBLIC_OPPONENT_SNAPSHOT (D4-D8)]
                     │
                     ▼
[Livello 2: REGIME_CLASSIFIER (Soglia di Pressione)]
                     │
                     ▼
[Livello 3: STICKY_POLICY_SELECTOR (Blocco Regime Epistemicamente Isolato)]
                     │
                     ▼
[Livello 4: LIFECYCLE_AND_WORKFORCE_GOVERNOR (Colture, DROP nello Shed, HIRE Fibonacci)]
                     │
                     ▼
[Livello 5: ACTION_ARBITER (Allocazione Manhattan senza conflitti per Farmer + Hands)]
```

### Livello 1: Snapshot Pubblico Avversario
Eseguito esattamente una volta nella finestra D4–D8 (default D4/D6 all'ora 0) leggendo esclusivamente lo stato pubblico `observation["farms"][1 - seat]`:
- Conteggio colture attive (`crop_tiles`), erbacce (`weed_tiles`), animali (`animal_tiles`), operai visibili (`hands`), quadranti sbloccati e cassa.
- Calcolo del punteggio di pressione causale:
  $$\text{pressure\_score} = 2 \cdot \text{crops} + 3 \cdot \text{weeds} + 3 \cdot \text{hands} + 2 \cdot \text{animals}$$

### Livello 2: Classificatore di Regime
Confronto tra `pressure_score` e soglia parametrizzata ($\text{threshold} = 20.0$):
- $\text{pressure\_score} \ge 20.0 \implies \text{EXPANSION\_TEMPO}$
- $\text{pressure\_score} < 20.0 \implies \text{BALANCED\_SERVICE}$

### Livello 3: Selettore Sticky
Il regime viene bloccato in modo permanente per il resto della partita (`mode_decisions = 1`, `regime_transitions = 1`), registrando giorno e pressione di decisione.

### Livello 4: Gestore Ciclo Vitale e Forza Lavoro
- **Protezione Capitale**: Riserva minima di liquidità ($150) sempre garantita prima di assumere o espandere.
- **Sblocco Quadranti Condizionato**: Sblocco di Q1 e Q2 subordinato a giorno minimo e riserva cassa post-acquisto.
- **Sizing Forza Lavoro (HIRE)**: All'ora 0 di ogni giorno (D1+), assunzione progressiva di hands secondo la serie di Fibonacci commisurata al backlog:
  $$\text{desired\_hands} = \min(\text{max\_hands}, \max(\text{target\_hands}, 1 + \lfloor \text{backlog} / 4 \rfloor))$$
- **Ciclo Vitale e DROP**:
  1. `WEED` $\to$ `DIG`
  2. `PLANT` in crescita ($\text{age} < \text{first\_yield\_day}$) $\to$ `WATER` prioritario giornaliero
  3. `PLANT` matura ($\text{age} \ge \text{first\_yield\_day}$ e $\text{yield\_units} > 0$) $\to$ `HARVEST`
  4. Inventario operaio $\ge 2$ unità o fine giornata $\to$ rotta verso casella shed `(4, 4)` e azione `DROP`
  5. Merce nello shed $\to$ vendita immediata via ordine di mercato `SELL`

### Livello 5: Arbitro Azioni (Worker Allocation)
Distribuzione ottimale dei task tra contadino e mani basata su priorità e distanza Manhattan, con mantenimento persistente dell'incarico ed eliminazione dei conflitti.

---

## 3. Risultati Sperimentali

### Gate A: Audit del Contratto Motore (PASS)
- **Matrice**: 3 seed development (`180903001`, `180903002`, `180903003`), entrambi i seat (6 partite da 720 turni).
- **Esito**: **PASS** completo.
- **Verifiche**:
  - Turni completati: 720/720 in 6/6 run.
  - Errori tecnici e fallbacks: 0.
  - Catena `DIG -> PLANT -> WATER -> HARVEST -> DROP -> SELL` osservata al 100%.
  - Guadagno finale: compreso tra $8.660 e $14.852 (soglia minima $2.840 ampiamente superata in 6/6 run).

### Gate B: Economia Indipendente (PASS)
- **Matrice**: 7 seed development x 2 seat x 2 avversari (Inert e Antigravity E17) = 28 partite da 720 turni.
- **Esito**: **PASS** completo.
- **Metriche aggregate**:
  - Denaro medio: **$10.712,71** (target $\ge \$10.000$).
  - Denaro minimo: **$5.971,00** (nessun run a zero).
  - Denaro massimo: **$18.347,00**.
  - Azioni produttive medie: **1.270,89**.
  - Residuo vendibile terminale: **0 unità** (liquidazione perfetta).

### Fase C: Torneo Reattivo a Quattro Agenti
- **Matrice**: 7 seed development x 2 seat x 3 peer (`CODEX_E18_1`, `CLAUDE_E18_1`, `COPILOT_E18_1`) = 42 partite.
- **Record Complessivo**: **24 Vittorie, 18 Sconfitte, 0 Pareggi** (da 0-42 di E17 a 24-18 positivo).
- **Head-to-Head**:
  - vs `CLAUDE_E18_1`: **10-4-0** (Antigravity mean $7.080,29 vs Claude $4.612,07; delta +$2.468,21)
  - vs `COPILOT_E18_1`: **14-0-0** (Antigravity mean $9.573,64 vs Copilot $2.840,00; delta +$6.733,64)
  - vs `CODEX_E18_1`: **0-14-0** (Antigravity mean $9.064,29 vs Codex $129.185,36)
- **Divergenza Comportamentale**: 35 action stream hash distinti su 42 partite.
- **Attivazione Regimi**: Entrambi i regimi (`BALANCED_SERVICE` e `EXPANSION_TEMPO`) attivati causalmente.
- **Sicurezza**: Zero errori tecnici, zero fallbacks mascherati da PASS, zero fughe o perdite.

---

## 4. Invarianti e Isolamento

- **Isolamento Namespace**: Tutte le creazioni risiedono sotto `docs/model_specs/antigravity/` e `src/agricola/strategy/antigravity/`.
- **Integrità Storica**: Nessuna modifica apportata all'obsoleto `antigravity_e17_native_3q.py` né ai file di Codex, Claude o Copilot.
- **Nessun Seed Riservato**: Holdout e Final Confirmation seeds non sono stati toccati né consumati.
- **Nessuna Submission Kaggle**: Nessun artefatto di submission generato prima dell'autorizzazione dell'owner.
