# E15 — M2 Independent Challenge — CODEX

## Ruolo
Agisci come owner/reviewer indipendente del MODEL_SPEC Codex dopo M2.

Non modificare codice, frozen artifact, ontology, submission o MODEL_SPEC frozen.
Non eseguire M3.

## Artefatti
Leggi:
- `experiments/archive/e15/artifacts/freeze/ONTOLOGY_E15_FROZEN.md`
- `experiments/archive/e15/artifacts/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md`
- `experiments/archive/e15/artifacts/M2_codex_vs_copilot/match_metadata.json`
- `summary.json`
- `telemetry.json`
- `raw_replay.json`
- `E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md`

## Esito
Codex: `$27,510`
Copilot: `$37,752`
Delta: `-$10,242`

## Obiettivo
Challenge-a la forensics senza confondere sconfitta con falsificazione.

Per ogni concetto usa solo:
`SUPPORTED`, `WEAKENED`, `NOT_DISCRIMINATED`, `CONFOUNDED`, `INCONCLUSIVE`.

## Punti obbligatori
- `crop_surface_maintained`: Codex max 37 vs Copilot 28.
- `watering_execution_rate`: Codex 475 vs Copilot 446.
- `productive_action_share`: Codex più alto ma perde.
- `movement_overhead`: praticamente identico.
- `worker_action_monetization_rate`: proxy $5.17 vs $7.13 per action.
- `livestock_headcount` / pasture: Codex 7 animals/9 pasture vs Copilot 4/5.
- `operating_cash_buffer`: Codex mantiene più cash early, ma Copilot recupera.
- `deployable_capital_window`: analizza il diverso payback temporale.
- `wheat_operating_flow`: Copilot usa più BUY/SELL Wheat.
- `feed_market_dependency`: verifica se M2 permette davvero un verdetto.
- `economic_lock_in_onset`: Copilot avanti permanentemente da circa Day 12.
- `inventory_to_cash_conversion` / `product_mix_revenue`: evitare di inventare transaction values.

## Output
1. Codex M2 self-audit.
2. Tabella concept_id discriminati.
3. 3–7 challenge forti.
4. Parti Codex non testate.
5. Delta post-tournament proposti, senza applicarli.
6. Verdict:
   - `ACCEPT_NEUTRAL_ANALYSIS`
   - `ACCEPT_WITH_CHALLENGES`
   - `REJECT_WITH_EVIDENCE`

Non autorizzare M3.
