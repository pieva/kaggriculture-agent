# E18 — Claude opponent-reactive V1: report di sviluppo

- **Data:** 2026-09-03
- **Candidata:** `CLAUDE-E18.1-OPPONENT-REACTIVE-V1`
- **Ruolo epistemico:** `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Predecessore/controllo:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
  (media E18 `12.850,18`, `12,85%` del target)
- **MODEL_SPEC:** `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E18_1_OPPONENT_REACTIVE_V1.md`
- **Sorgente:** `src/agricola/strategy/claude/e18_opponent_reactive_v1.py`
- **Config:** `docs/model_specs/claude/e18/configs/CLAUDE_E18_1_OPPONENT_REACTIVE_V1.json`
- **Runner:** `docs/model_specs/claude/e18/tools/run_claude_e18_opponent_reactive_dev_matrix.py`
- **Artifact:** `docs/model_specs/claude/e18/artifacts/derived/E18_CLAUDE_OPPONENT_REACTIVE_V1_DEV_MATRIX.json`
- **Test:** `docs/model_specs/claude/e18/tests/test_claude_e18_opponent_reactive_v1.py` (29/29 PASS)
- **Holdout/final-confirmation:** non consumati. Nessuna submission Kaggle.

---

## 1. Cosa è stato costruito

Un controller a cinque livelli espliciti (dettaglio completo in
MODEL_SPEC), nuovo namespace, nessun import da Codex/Copilot:

1. `PUBLIC_OPPONENT_SNAPSHOT` — fotografia della farm pubblica
   dell'avversario in finestra D4-D8;
2. `REGIME_CLASSIFIER` — punteggio di pressione serializzabile contro
   soglia preregistrata (`26,0`);
3. `STICKY_POLICY_SELECTOR` — una sola decisione per run, bloccata per
   il resto dell'episodio;
4. `CAPACITY_AND_LIFECYCLE_CONTROLLER` — stato esplicito
   KEEP/HARVEST/DIG per ogni tile coltivata, verificato contro il motore
   ufficiale (non contro un'ipotesi), più un ledger zootecnico a rischio
   zero per i nuovi acquisti;
5. `ACTION_ARBITER` — dispatch persistente per priorità, ereditato dalla
   disciplina V1-V3 di questo agente.

I due regimi (`LOW_PRESSURE_BALANCED`, `HIGH_PRESSURE_WHEAT_TEMPO`)
divergono su tre dimensioni: soffitto/floor di workforce (12/3 contro
15/4), pesi del mix colturale (Wheat 40% contro 70%) e strutture
zootecniche per quadrante (3 contro 2).

## 2. Bug trovato e corretto durante lo sviluppo

La prima versione del lifecycle leggeva `max_lifespan_step` senza
distinguere il sentinella `-1` (colture perenni ancora produttive, mai
scadute) da una vera scadenza, e applicava lo stesso margine di sicurezza
a step fisso (48 step) sia alle perenni sia a Wheat. Verificato contro il
motore ufficiale (`kaggle_environments/envs/kaggriculture/kaggriculture.py`,
regole pubbliche, non un'altra strategia): per Wheat la finestra di
crescita dura solo 2 giorni (età 2-4), quindi quel margine forzava una
raccolta anticipata quasi ad ogni ciclo. Sintomo osservato: partite senza
collassi di cassa ma con denaro persistentemente basso nonostante alta
densità di coltura (fino a 38 tile piantate). Dopo la correzione (Sezione
2.4 del MODEL_SPEC) lo stesso seed passa da `2.904` a `7.482` nello stesso
confronto contro Copilot. Il fix è verificato dai test di fixture
(Sezione 3 del MODEL_SPEC), non dal solo seed di diagnosi.

## 3. Matrice di sviluppo (42 match: 7 seed × 2 seat × 3 avversari)

| Avversario | Record | Denaro medio candidata | Denaro medio avversario | Delta medio | Min–max | Run <5.000 | Perdite verificate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude V3 (controllo) | 1-13-0 | 5.139,93 | 15.969,29 | -10.829,36 | 136–13.968 | 9/14 | 16 |
| Codex E18 (black-box) | 0-14-0 | 3.763,64 | 139.404,57 | -135.640,93 | 67–7.168 | 9/14 | 15 |
| Copilot Native | 0-14-0 | 2.391,14 | 8.554,93 | -6.163,79 | 48–7.482 | 11/14 | 24 |
| **Complessivo** | 1-41-0 | **3.764,90** | — | — | 48–13.968 | 29/42 | **55** |

Zero errori tecnici e zero fallback su tutti i 42 match. Divergenza di
action stream condizionata all'avversario: `14/14` gruppi seed-seat
(gate architetturale passato). Regime attivato correttamente in funzione
della pressione avversaria osservata (`LOW_PRESSURE_BALANCED` contro
Claude V3, `HIGH_PRESSURE_WHEAT_TEMPO` contro Codex e Copilot — entrambi
misurano pressione ≥ soglia a D4-D8), una sola decisione per run in
`42/42`.

**La candidata perde anche contro Copilot Native**, il controllo più
debole del pool (Claude V3 lo batte 14-0 nel torneo E17 di riferimento).
Questo non è spiegabile solo con il bug di Sezione 2 (già corretto prima
di questa matrice): resta una sotto-monetizzazione strutturale non
ancora diagnosticata a fondo, oltre a un problema di sicurezza
zootecnica autonomo (sotto).

### 3.1 Perdite zootecniche verificate: gate fallito

Il ledger a rischio zero (MODEL_SPEC Sezione 2.4) blocca nuovi acquisti
quando un animale è già a rischio, ma **non garantisce che ogni animale
già posseduto venga nutrito ogni giorno**: `verified_livestock_losses`
totalizza `55` sui 42 match (fino a `5` in un singolo match), non zero.
Ipotesi non ancora verificata per la prossima iterazione: pressione di
servizio quando la workforce è distribuita su più quadranti con un
gregge già esistente, la stessa dinamica mai risolta in V3 (`19` perdite
nel torneo E18 V1) e qui ereditata, non introdotta. Il ledger riduce la
crescita del rischio ma non il rischio residuo sull'esistente.

## 4. Gate

```text
TECHNICAL_GATE: PASS
DYNAMIC_ARCHITECTURE_GATE: FAIL
ECONOMIC_GATE: FAIL
PROMOTION_RECOMMENDATION: ITERATE
```

**TECHNICAL_GATE — PASS.** Zero errori tecnici e zero fallback su 42/42
match; schema azione sempre valido; nessuna violazione dell'observation
contract; 29/29 test unitari passano, incluse tutte le fixture di
sicurezza e lifecycle richieste.

**DYNAMIC_ARCHITECTURE_GATE — FAIL.** I cinque livelli sono implementati
e osservabili in telemetria (`telemetry_snapshot()`), la divergenza di
action stream condizionata all'avversario è `14/14` e la decisione di
regime è esattamente una per run in `42/42`. Ma il gate esplicito **zero
perdite zootecniche verificate** fallisce (`55` totali), quindi il gate
architetturale complessivo non passa: la sicurezza zootecnica è parte
integrante del gate richiesto, non un requisito separato.

**ECONOMIC_GATE — FAIL.** Nessuna soglia raggiunta:

- delta vs Claude V3: **-60,0%** (richiesto: +25%);
- delta vs Codex E18: **-63,4%** (richiesto: +20% sul riferimento
  `10.292,86` di V3);
- `9` run sotto `5.000` solo contro V3 (richiesto: zero, su ogni
  matchup);
- milestone M1 (`16.000`): non raggiunta (media complessiva `3.764,90`);
  gap da M2 `25.000`: `21.235,10`; gap da M3 `50.000`: `46.235,10`; gap
  dal target `100.000`: `96.235,10`.

**PROMOTION_RECOMMENDATION — ITERATE.** L'architettura richiesta esiste,
è testata e in parte funziona (regime corretto, divergenza condizionata,
fix del bug di lifecycle già misurabile), ma non è pronta: la sicurezza
zootecnica non è a posto e il livello economico è **peggiore** del
controllo V3 su ogni matchup, non solo lontano dal target. Non
`REJECT` perché non c'è evidenza di un difetto architetturale
irrecuperabile (a differenza di V4/V6 in E17, qui non ci sono collassi
di cassa near-zero sistemici né un meccanismo di regressione scoperto e
non risolto); non `PROMOTE` per ragioni evidenti.

## 5. Prossimi passi consigliati, in ordine

1. Diagnosticare la causa delle `55` perdite verificate (telemetria
   dedicata: quale quadrante, quale distanza dal worker più vicino,
   quanti animali contemporaneamente a rischio) prima di qualunque altra
   modifica — è un gate di sicurezza, non un'ottimizzazione;
2. Capire perché la candidata perde anche contro Copilot Native
   (l'avversario più debole del pool): tracciare denaro giorno per
   giorno su 2-3 seed rappresentativi, come già fatto per il bug di
   Sezione 2, prima di ipotizzare nuove cause;
3. Solo dopo aver risolto 1-2, ripetere la matrice di sviluppo completa
   e ricontrollare tutti i gate, non solo quello economico;
4. Non introdurre altre leve (clustering, cap zootecnico aggiuntivo,
   nuovi regimi) finché sicurezza e monetizzazione di base non sono
   risolte — coerente con la lezione già registrata in
   `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V6_REJECTION_REPORT_IT.md`
   sul combinare leve non ancora isolate.

## 6. SHA-256 di sorgente, config, runner e artefatti

| File | SHA-256 |
|---|---|
| `src/agricola/strategy/claude/e18_opponent_reactive_v1.py` | `F7846B834A58241BAFBB44369F1ADBB8213BEE4D77B611C86E842A9CCA2A76EE` |
| `docs/model_specs/claude/e18/configs/CLAUDE_E18_1_OPPONENT_REACTIVE_V1.json` | `92611D60F150C5FC1C9E025D8147FC28AF509EEE7C05681EA8966DDA5C869236` |
| `docs/model_specs/claude/e18/tools/run_claude_e18_opponent_reactive_dev_matrix.py` | `843DD44AD8E8A9CD35E71FED4CB0C34A3D22964411D77E2F2FEE688D7D618272` |
| `docs/model_specs/claude/e18/artifacts/derived/E18_CLAUDE_OPPONENT_REACTIVE_V1_DEV_MATRIX.json` | `CB197DA6898D08CA2E97473A7EB659E49A410E527DDC5311E697890345ADAA70` |
| `docs/model_specs/claude/e18/tests/test_claude_e18_opponent_reactive_v1.py` | `9FF5CDF5DDCF5A9E8B7411D899D9C4180DC7F5B626CD17350D7776BB8B1DFEF1` |

## 7. Cosa NON è stato fatto

- Nessun seed holdout o final-confirmation consumato (solo i 7 seed di
  sviluppo E18 `180903001`-`180903007`).
- Nessuna submission Kaggle.
- Nessuna lettura di sorgente, config o MODEL_SPEC Codex/Copilot; Codex
  E18 affrontato solo come avversario black-box tramite la sua factory
  pubblica.
- Nessuna modifica ai file di altri agenti o alla submission canonica.
