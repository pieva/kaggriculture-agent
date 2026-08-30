# NEW SESSION — MODEL_SPEC TOURNAMENT C2

- **Phase:** `MODEL_SPEC TOURNAMENT C2`
- **Status:** `READY TO RUN`
- **Foundation C2:** `UPSTREAM_READY_FOR_MODEL_SPEC` (Blockers Closed, NOT FROZEN)
- **Candidates:** `3/3 TOURNAMENT_READY`
- **Repository Validation:** `168 passed` | `git diff --check PASS`
- **Tournament Status:** `NOT RUN`
- **Kaggle Validation:** `NOT RUN`

---

## 1. Foundation C2 Status

```text
FOUNDATION C2:
- upstream-ready for MODEL_SPEC
- Feature Model blockers closed
- Foundation C2: NOT FROZEN (upstream-ready, non-blocking for tournament)
```

- **Ontology C2:** `docs/model/ontology/ONTOLOGY_C2.md`
- **State Machine C2:** `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`
- **Feature Model C2:** `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`

---

## 2. The Three C2 Candidates

| Candidato | MODEL_SPEC | Candidate Executable | Configuration | Build Verification |
|---|---|---|---|---|
| **Antigravity C2** | `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md` | `src/agricola/strategy/antigravity/agent_c2.py` | `src/agricola/strategy/antigravity/c2_config.py` | `results/model_spec_c2/antigravity/BUILD_VERIFICATION.md` |
| **Codex C2** | `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md` | `src/agricola/strategy/codex_c2.py` | `configs/model_spec_c2/CODEX_C2_CONFIG.json` | `results/model_spec_c2/codex/BUILD_VERIFICATION.md` |
| **Copilot C2** | `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md` | `src/agricola/strategy/copilot/agent_c2.py` | `src/agricola/strategy/copilot/c2_config.py` | `results/model_spec_c2/copilot/BUILD_VERIFICATION.md` |

Tutti e 3 i candidati sono dichiarati `TOURNAMENT_READY: YES`.

---

## 3. Obiettivo della Prossima Sessione

> **Obiettivo:**
> Verificare se il lavoro sulla Foundation C2 e sui tre MODEL_SPEC si traduce in migliore policy realization e performance.

Il torneo deve rispondere alla domanda fondamentale:
> *Quale dei tre MODEL_SPEC corregge meglio i meccanismi che hanno performato peggio, e quali modifiche decisionali producono un miglioramento verificabile?*

---

## 4. Protocollo Iniziale della Prossima Sessione

La nuova sessione deve partire direttamente dall'esecuzione del torneo seguendo questo ordine:

1. **Verificare l'integrità dei tre candidati** (verificare che nessun artefatto sia stato alterato o corrotto).
2. **Definire e congelare un solo protocollo comune di torneo** (stessi avversari, stessi seed, stesse regole di configurazione).
3. **Stessa telemetria ed instrumentation comune.**
4. **Stesso budget sperimentale.**
5. **Eseguire i tre candidati** in condizioni rigorosamente identiche.
6. **Confrontare outcome economici e meccanismi causali.**
7. **Produrre tre POST-TOURNAMENT REVIEW indipendenti** (una per ciascun agente).
8. **Confrontare le tre review.**
9. **Selezionare il candidato più promettente.**
10. **Eseguire la validazione esterna Kaggle.**

---

## 5. Metriche Computabili da Preservare

Nel confronto del torneo utilizzare esclusivamente metriche supportate dall'ambiente e dall'infrastruttura di telemetria:

- `final_money` (outcome economico principale)
- `completion` (completamento partita/step)
- `crop_target_attainment` (realizzazione del target di colture)
- `active_crop_surface` / `maintained_productive_surface`
- `watering_execution` & `watering_continuity`
- `premature_harvest_count`
- `failed_action_count` & `no_op_action_count`
- `WEED/lost_tile_count` & `lost_tile_persistence`
- `replant_latency`
- `movement_share` & `productive_action_share`
- `workforce_utilization`
- `inventory state` (shed storage vs overflow loss)
- `market activity`
- `livestock contribution` (se rilevante nel mix)

---

## 6. Review Post-Torneo Già Contrattualizzate

Dopo l'esecuzione del torneo, ciascun agente (Antigravity, Codex, Copilot) dovrà analizzare tutti e tre i concorrenti secondo la catena causale obbligatoria:

```text
RISULTATO
    ↓
MECCANISMO OSSERVATO
    ↓
DECISIONE MODEL_SPEC
    ↓
SPIEGAZIONE CAUSALE
    ↓
MODIFICA PROPOSTA
    ↓
PREVISIONE VERIFICABILE
```

> [!NOTE]
> La review post-torneo non fa parte della chiusura corrente e sarà eseguita nella prossima sessione.
