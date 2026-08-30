# C2 COMMON PERFORMANCE TOURNAMENT — PROTOCOLLO SPERIMENTALE CONGELATO

- **Orchestratore Neutrale:** `ANTIGRAVITY` (Experimental Orchestrator & Auditor)
- **Data:** 2026-08-30
- **Stato Protocollo:** `FROZEN_BEFORE_EXECUTION: YES`
- **Fase:** MODEL_SPEC Tournament C2 Performance Iteration (Round 2)

---

## 1. Amendment Metodologico: Nuovi Seed Primari

In conformità al mandato di neutralità e indipendenza della valutazione, i 3 seed storici del ReTournament C2 (`1113294977`, `3033283457`, `1678077158`) sono esclusi dal set primario poiché sono stati utilizzati nelle verifiche private dei candidati.

Vengono generati e congelati prima di qualsiasi esecuzione 3 nuovi seed pseudo-casuali indipendenti a 32-bit:

```text
PRIMARY_SEED_1: 1838889274
PRIMARY_SEED_2: 1619968655
PRIMARY_SEED_3: 710418712
SEEDS_FROZEN_BEFORE_EXECUTION: YES
HISTORICAL_SEEDS_EXCLUDED_FROM_PRIMARY_SET: YES
```

I seed storici rimangono documentati unicamente come riferimento descrittivo e non vengono rieseguiti in questo round.

---

## 2. Freeze e Check di Integrità dei Candidati

I candidati partecipanti sono congelati nelle rispettive directory e verificati prima dell'avvio:

### 2.1 Antigravity C2 (Performance Iteration)
- **Spec:** `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md`
  - SHA256: `4e81e7042a470d63b5e475cd490c183c8b80fe8321189604fb119531dac733c2`
- **Executable:** `src/agricola/strategy/antigravity/agent_c2.py`
  - SHA256: `da37cdb20660c369905c9b833bc31cad438d2b866efcfd418bb8d628184219a1`
- **Policy:** `src/agricola/strategy/antigravity/c2_policy.py`
  - SHA256: `b2b4dbc44b0db5574f6c70927ab6a2fa582f1a19275a69b51d1b4c18c2e24830`
- **Config:** `src/agricola/strategy/antigravity/c2_config.py`
  - SHA256: `f9cdb9e452ffd70864abc4879910f9e9fda76fb575f0b33f66f54cc1c2686d88`

### 2.2 Codex C2 (V4 Performance Iteration)
- **Spec:** `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md`
  - SHA256: `a4215f6213eb445ac4402ebf07b36194a08f805231f9b17580619496ac2fbe93`
- **Executable:** `src/agricola/strategy/codex_c2.py`
  - SHA256: `333730c6d78246d7c9fb621ce80e81c34736d868688fd836d09926e31a6861d5`
- **Config:** `configs/model_spec_c2/CODEX_C2_CONFIG.json`
  - SHA256: `c5c3c1558ecbed55d0fbbb351930df43eed62e633f58cbaedf71c1135cb4375c`

### 2.3 Copilot C2 (Performance Iteration)
- **Spec:** `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`
  - SHA256: `7b5da675d784bf3b607b1cfc148c7ebbb7b3995ef76d1e289e46f9fa496c560b`
- **Executable:** `src/agricola/strategy/copilot/agent_c2.py`
  - SHA256: `1c24af2fa5a9d068e45dab457a05bc2ab73551d1fe4f6f0b34cb186dc6b4256d`
- **Policy:** `src/agricola/strategy/copilot/c2_policy.py`
  - SHA256: `f9064a6c7f5249a01d8bfa3441a4555516fea82d3868cfea403789355c10d3b2`
- **Config:** `src/agricola/strategy/copilot/c2_config.py`
  - SHA256: `f2f6481e6f21a5bf71d43469020ef506ea6be52d10cfdf31f006abf89ca01a2d`

---

## 3. Disegno Sperimentale e Struttura dei Match

Il torneo è strutturato in 3 round pairwise simmetrici sui 3 seed primari (9 match totali, 720 step ciascuno):

- **Round 1 (R1):** Antigravity C2 (Player 0) vs Codex C2 V4 (Player 1)
  - Match R1_S1 (Seed 1838889274)
  - Match R1_S2 (Seed 1619968655)
  - Match R1_S3 (Seed 710418712)
- **Round 2 (R2):** Antigravity C2 (Player 0) vs Copilot C2 (Player 1)
  - Match R2_S1 (Seed 1838889274)
  - Match R2_S2 (Seed 1619968655)
  - Match R2_S3 (Seed 710418712)
- **Round 3 (R3):** Codex C2 V4 (Player 0) vs Copilot C2 (Player 1)
  - Match R3_S1 (Seed 1838889274)
  - Match R3_S2 (Seed 1619968655)
  - Match R3_S3 (Seed 710418712)

Totale: **9 match ufficiali = 18 player-episodes (6 player-episodes per candidato)**.

---

## 4. Gate Economico C2

```text
IF max(candidate Mean Final Money sui 6 player-episodes) > 23000:
    C2_PERFORMANCE_SUCCESS = YES
ELSE:
    C2_PERFORMANCE_SUCCESS = NO
```

---

## 5. Condizioni di Arresto e Non-Intervento

Nessuna modifica, aggiustamento o re-run selettivo è ammesso dopo l'inizio del Round 1.
Tutti i dati e i replay raw verranno salvati in:
`results/model_spec_c2/performance_tournament/raw/`
