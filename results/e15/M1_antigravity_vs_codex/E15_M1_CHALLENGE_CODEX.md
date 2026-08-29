# E15 — M1 Independent Challenge — CODEX

## Ruolo

Agisci esclusivamente come **owner/reviewer indipendente del MODEL_SPEC Codex** dopo M1.

Non modificare codice, submission, MODEL_SPEC frozen, ontologia o risultati.
Non eseguire M2/M3.
Il fatto che Codex abbia vinto non costituisce validazione automatica del MODEL_SPEC.

## Artefatti da leggere

Obbligatori:
- `results/e15/freeze/ONTOLOGY_E15_FROZEN.md`
- `results/e15/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md`
- `results/e15/M1_antigravity_vs_codex/match_metadata.json`
- `results/e15/M1_antigravity_vs_codex/summary.json`
- `results/e15/M1_antigravity_vs_codex/telemetry.json`
- `results/e15/M1_antigravity_vs_codex/raw_replay.json`

Se disponibile, leggi anche il report neutrale ChatGPT `E15_M1_NEUTRAL_FORENSIC_ANALYSIS.md`, ma challenge-a le sue attribuzioni causali.

## Esito osservato

Codex: `$20,461`
Antigravity: `$8,672`
Delta: `+$11,789`

## Obiettivo

Stabilire quali parti del MODEL_SPEC Codex erano realmente predittive/discriminanti e quali vengono solo rese plausibili ex post dalla vittoria.

Per ogni punto:
1. cita `concept_id`;
2. richiama la posizione pre-match frozen;
3. mostra evidenza M1;
4. assegna soltanto:
   - `SUPPORTED`
   - `WEAKENED`
   - `NOT_DISCRIMINATED`
   - `CONFOUNDED`
   - `INCONCLUSIVE`
5. separa causalità, correlazione e semplice compatibilità.

## Challenge obbligatorie

Verifica in particolare:

- `land_surface_total` / `land_activation_payback`: Codex vince con 2Q contro 3Q.
- `worker_action_monetization_rate`: dimostra quanto è realmente misurabile senza inventare revenue ledger.
- `productive_action_share`: verifica se M1 lo discrimina davvero.
- `movement_overhead`: Antigravity ha più MOVE assoluti, ma controlla la quota rispetto alle azioni totali.
- `watering_execution_rate`: Codex lo tratta solo come parte della maintained surface; M1 mostra 439 vs 34. Valuta se il MODEL_SPEC lo sottopesava.
- `crop_revenue_mix` e `product_mix_revenue`: Codex monetizza Strawberry/Melon, Antigravity no.
- `wheat_operating_flow` / `market_churn_cost`: Codex presenta elevato BUY_PRODUCT/SELL Wheat; evita di chiamarlo profittevole senza transaction-value ledger.
- `livestock_headcount`: vittoria con herd compatto.
- `species_margin_differential`: Codex termina senza Sheep; valuta se M1 discrimina davvero il concetto.
- `fertilizer_byproduct_flow`: Codex vince con zero COLLECT_FERTILIZER.
- `operating_cash_buffer` / `deployable_capital_window`: verifica opening e cash trajectory.
- `economic_lock_in_onset`: il lead cambia più volte e diventa permanente solo dal Day 19.

## Divieti epistemici

- Victory ≠ Model Validity.
- Non promuovere automaticamente tutti i fattori Codex a SUPPORTED.
- Non inferire metriche non osservate.
- Le quantità di market order sono requests, non necessariamente executed quantities.
- Non retrofittare ranking o confidence.
- Non trasformare una singola seed victory in una regola generale.

## Output richiesto

Produci:

1. **Codex M1 self-audit**
2. tabella dei `concept_id` discriminati;
3. elenco delle 3–7 challenge più forti al report neutrale;
4. elenco delle parti del MODEL_SPEC Codex che M1 **non** ha testato;
5. proposta di aggiornamenti **post-tournament only**, senza applicarli;
6. verdict finale:
   - `ACCEPT_NEUTRAL_ANALYSIS`
   - `ACCEPT_WITH_CHALLENGES`
   - `REJECT_WITH_EVIDENCE`

Non autorizzare M2.
