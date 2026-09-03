# MODEL_SPEC — Claude E17.1 3Q Reactive Independent V4

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V4`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-03
- **Foundation:** C2.1 (RECONCILED)
- **Stato:** AS-BUILT — benchmark a 4 seed completo, **esito negativo in
  aggregato** (`-8,9%` vs V3, incoerente per segno fra seed), matrice
  completa a 7 seed NON eseguita per protocollo (Sezione 4)
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
  (`FROZEN_WITH_FAILED_GATES`; nessuna regressione voluta, questo è un
  delta additivo su V3, non una remediation di un gate fallito)
- **Sorgente:** `src/agricola/strategy/claude/e17_reactive_3q_v4.py`
- **Config:** `experiments/e17/configs/claude/CLAUDE_E17_1_3Q_REACTIVE_V4.json`
- **Piano di origine:** `experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V4_STATIC_PLAN_IT.md`
  (Sezione 0, aggiornamento 2026-09-03)

---

## 1. Origine ed evidenza

Il piano statico V4 assumeva inizialmente l'archetipo offline OceanMix
(nove replay di discovery E17): bestiame confinato a Q0/Q1, SW
esclusivamente a coltura — assunzione mai verificata contro dati Kaggle
live, solo contro il corpus offline.

Il 2026-09-03 il proprietario ha fornito dieci screenshot Kaggle live
(evidenza transitoria, non i replay di discovery), da cui è stato ricontato
pixel-per-pixel il numero di tile a pascolo per quadrante. I file grezzi non
sono mantenuti nel repository; le osservazioni consolidate sono riportate
qui sotto:

| Farm osservato | NW | NE | SW | Esito / denaro finale |
|---|---:|---:|---:|---|
| Pietro Valocchi (submission Codex live, 6 partite indipendenti, layout identico) | 7 | 6 | 5 | vinto in 5/6, denaro `86.492`-`121.043` |
| `hisatarosu` | — | — | 0 | vinto, `1187 (+39)`, `118.775` |
| `iVl44d` | — | — | 0 | vinto, `1201 (+4)`, `102.159` |
| `shiggriculture` (1 partita) | 6 | 6 | **2** | vinto, `1283 (+5)`, `127.357` — il più alto osservato |

Nessuno dei due archetipi live con SW=0 e nessuno con SW pieno rappresenta
l'unica via; ma **entrambi gli archetipi che aprono SW lo fanno con una
quota molto più piccola di NW/NE**, mai a zero. Questo falsifica
l'assunzione "Q2 sempre crop-only" del piano OceanMix-based e motiva
questo delta. Dettaglio completo del conteggio: Sezione 0 del piano
statico citato sopra.

---

## 2. Ipotesi V4

**H-CR4.1 (SW non deve restare a zero animali):** dato che entrambi gli
archetipi live con SW aperta (Codex live, shiggriculture) superano il
target indicativo `100.000` — e che nessuno dei due tratta SW come
crop-only — vincolare Claude a SW=0 è una scelta architetturale non
supportata dai dati più recenti disponibili, non solo una scelta
subottimale.

**Portata esplicitamente limitata:** questa ipotesi riguarda solo *dove*
Claude è autorizzato a costruire strutture zootecniche (topologia), non
*quanto velocemente* le costruisce/acquista o *quanti lavoratori* impiega.
Non pretende di spiegare il gap `10,53×` verso Codex quantificato in
`E17_1_CLAUDE_REACTIVE_V4_100K_IMPROVEMENT_PLAN.md` (dominato da
movimento/workforce, non da topologia) — è un prerequisito strutturale
indipendente, testato in isolamento.

---

## 3. Modifica implementata (unica variabile)

`src/agricola/strategy/claude/e17_reactive_3q_v4.py`, `_extract_features`:

- V1-V3: `allowed_livestock_quadrants` limitava le nuove strutture COOP/
  PASTURE ai primi `max_quadrants_for_livestock` quadranti (default `2`,
  cioè NW+NE), con un'unica soglia di rango `livestock_structures_target_per_quadrant`
  (default `4`) applicata identicamente a ogni quadrante ammesso.
- V4: `max_quadrants_for_livestock` passa a `3` (include SW, terzo in
  ordine di sblocco canonico) e SW riceve una soglia di rango **propria e
  indipendente**, `livestock_structures_target_third_quadrant` (config:
  `2`), invece di ereditare quella di NW/NE. NW ed NE restano
  bit-per-bit identici a V3 (stessa soglia, stessa logica).
- Nessun'altra leva è toccata: guardia `_core_established`, soffitto
  workforce, `herd_per_worker_ratio`, riserva dedicata, tie-break di
  dispatch, timing di espansione (`_expansion_guard`) sono tutti
  invariati da V3. Il gate `_core_min_fill_ratio` (Sezione 6.4 di
  MODEL_SPEC V3) continua a misurare solo NW (`CORE_QUADRANT`) e non è
  influenzato dalla nuova soglia SW.

Config: unico campo nuovo `livestock.structures_target_third_quadrant`
(default di fallback nel codice: uguale a `structures_target_per_quadrant`
se assente, per compatibilità retroattiva con config V3 non aggiornate).

---

## 4. Stato del benchmark

Eseguito secondo il protocollo del piano statico (Sezione 5): 2 seed di
sviluppo contro Codex reattivo black-box, poi esteso a 4 seed (`26090101`,
`26090102`, `26090103`, `1838889274`; 16 match per versione). Risultato:
denaro medio V4 `12.054,00` contro `13.237,88` di V3 (`-8,9%`), segno del
delta incoerente fra seed (2 negativi, 2 positivi). Non stabile/positivo
per il criterio del protocollo — **la matrice completa a 7 seed non è
stata eseguita**. Nessun seed holdout o final-confirmation consumato.
Dettaglio e interpretazione:
`experiments/e17/reports/claude/E17_1_CLAUDE_REACTIVE_V4_DEVELOPMENT_REPORT_IT.md`.

---

## 5. Vincoli invariati

Identici a V3 (MODEL_SPEC V3 Sezione 2 e piano statico Sezione 6): nessun
import da `agricola.strategy.codex`/`antigravity`/`copilot`, nessuna
tabella di azioni indicizzata per step, nessun consumo di seed holdout o
final-confirmation, benchmark contro Codex rigorosamente black-box (solo
stato di gioco pubblico osservabile, mai sorgenti/routine).
