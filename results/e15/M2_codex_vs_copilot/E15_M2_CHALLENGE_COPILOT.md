# E15 — M2 Independent Challenge — COPILOT

## Ruolo
Agisci come owner/reviewer indipendente del MODEL_SPEC Copilot dopo M2.

La vittoria non valida automaticamente il MODEL_SPEC.
Non modificare codice, frozen artifact, ontology, submission o MODEL_SPEC frozen.
Non eseguire M3.

## Artefatti
Leggi:
- `results/e15/freeze/ONTOLOGY_E15_FROZEN.md`
- `results/e15/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md`
- `results/e15/M2_codex_vs_copilot/match_metadata.json`
- `summary.json`
- `telemetry.json`
- `raw_replay.json`
- `E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md`

## Esito
Copilot: `$37,752`
Codex: `$27,510`
Delta: `+$10,242`

## Obiettivo
Stabilire quali tesi Copilot erano realmente predittive ex ante e quali risultano solo compatibili ex post.

Per ogni concetto usa solo:
`SUPPORTED`, `WEAKENED`, `NOT_DISCRIMINATED`, `CONFOUNDED`, `INCONCLUSIVE`.

## Punti obbligatori
- `throughput_to_cash_conversion` / `worker_action_monetization_rate`: winner con meno azioni e working set più piccolo.
- `working_set_capacity_gate` / `state_capacity_alignment`.
- `crop_surface_maintained`: Copilot max 28 vs Codex 37 e vince.
- `watering_execution_rate`: entrambi forti; Codex irriga persino di più.
- `pasture_to_livestock_alignment`: 5 pasture/4 animals vs 9/7.
- `livestock_headcount`: distinguere "dynamic compact herd" da target universale 4.
- `wheat_feed_security`: Copilot compra più Wheat sul mercato; challenge alla formulazione strong feed-security.
- `operating_cash_buffer`: Copilot ha meno cash nei Days 4–9 ma poi recupera.
- `deployable_capital_window` / `asset_liquidity_lag`.
- `inventory_to_cash_conversion`: 298 SELL orders vs 212, ma requests non ledger.
- `product_mix_revenue`.
- `economic_lock_in_onset`: permanente dal Day 12 solo per M2.

## Divieti epistemici
- Victory ≠ Model Validity.
- Non chiamare "profitto" le requested quantities.
- Non generalizzare una seed.
- Non retrofittare ranking/confidence frozen.
- Non trasformare correlazione in causalità.

## Output
1. Copilot M2 self-audit.
2. Tabella concept_id discriminati.
3. 3–7 challenge forti.
4. Parti Copilot non testate.
5. Delta post-tournament proposti, senza applicarli.
6. Verdict:
   - `ACCEPT_NEUTRAL_ANALYSIS`
   - `ACCEPT_WITH_CHALLENGES`
   - `REJECT_WITH_EVIDENCE`

Non autorizzare M3.
