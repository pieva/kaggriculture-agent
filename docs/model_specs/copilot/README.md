# Indice MODEL_SPEC Copilot

> **Linea abbandonata dal 2026-09-09 — `ABANDONED_PERFORMANCE_GAP`.** Decisione
> del proprietario dopo il torneo a tre vie V6 vs V5 vs Codex V48 (14 partite
> per candidata, stessi sette seed di sviluppo): V6 chiude a -28,1% di cassa
> media rispetto a V5, ed entrambe restano molto al di sotto di Codex
> ([report](../../../experiments/e18/reports/common/E18_COPILOT_E18_10_VS_E18_8_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html)).
> Nessuna nuova iterazione, tuning o submission su questa linea. Gli asset
> restano come evidenza storica e avversari black-box nei runner comuni.

| Stato | File | Uso |
|---|---|---|
| ABANDONED / NOT PROMOTED | [`MODEL_SPEC_COPILOT_E18_ECONOMIC_RECOVERY_V6.md`](MODEL_SPEC_COPILOT_E18_ECONOMIC_RECOVERY_V6.md) | bozza più recente V6, orientata a cash buffer, irrigazione e gate di livestock. Torneo a tre vie vs V5 e Codex V48: -28,1% di cassa media rispetto a V5; linea chiusa dal proprietario, non promossa. |
| ABANDONED / HISTORICAL | [`MODEL_SPEC_COPILOT_E18_ECONOMIC_RECOVERY_V5.md`](MODEL_SPEC_COPILOT_E18_ECONOMIC_RECOVERY_V5.md) | baseline Copilot E18 precedente, coerente con il contratto reale del motore e verificata localmente. Superata da V6 solo per confronto; entrambe chiuse. |
| FROZEN / HISTORICAL | [`MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md`](MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md) | baseline Copilot C2 post-Foundation, conservata come riferimento storico |

Gli asset specifici di round sono in [`e17/`](e17/) ed [`e18/`](e18/), inclusi
candidate harness, config, prompt, report, review, tool, test e artifact. I
confronti multi-agente restano sotto `experiments/`.

## Linea E18 — ultimo stato prima della chiusura

- Implementazione runtime (V5, precedente): [`../../src/agricola/strategy/copilot/e18_economic_recovery_v5.py`](../../src/agricola/strategy/copilot/e18_economic_recovery_v5.py)
- Implementazione runtime (V6, più recente, non promossa): [`../../src/agricola/strategy/copilot/e18_economic_recovery_v6.py`](../../src/agricola/strategy/copilot/e18_economic_recovery_v6.py)
- Configurazione V5: [`e18/configs/COPILOT_E18_8_ECONOMIC_RECOVERY_V5.json`](e18/configs/COPILOT_E18_8_ECONOMIC_RECOVERY_V5.json)
- Configurazione V6: [`e18/configs/COPILOT_E18_10_ECONOMIC_RECOVERY_V6.json`](e18/configs/COPILOT_E18_10_ECONOMIC_RECOVERY_V6.json)
- Runner del benchmark V5: [`e18/tools/run_copilot_e18_economic_recovery_v5_tournament.py`](e18/tools/run_copilot_e18_economic_recovery_v5_tournament.py)
- Evidenza del torneo V5: [`e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json`](e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json)
- Torneo finale a tre vie (V6 vs V5 vs Codex V48): [`../../experiments/e18/reports/common/E18_COPILOT_E18_10_VS_E18_8_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html`](../../experiments/e18/reports/common/E18_COPILOT_E18_10_VS_E18_8_VS_CODEX_V48_D01_D30_COMPLETE_KPI.html)

Entrambe restano solo per audit e provenienza; la linea non è più in sviluppo.
La versione `C2` precedente resta anch'essa solo per audit e provenienza.
