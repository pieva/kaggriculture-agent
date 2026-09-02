# E16 E0 Instrumentation Report

Evidence role: E0_NON_ANALYTIC_SMOKE

E0_STATUS: PASS

This smoke output is excluded from TRAINING, bounds, and model-spec updates.

## Checks

- PASS: `event_ledger_present`
- PASS: `event_ledger_schema`
- PASS: `requested_executed_distinction`
- PASS: `accepted_status`
- PASS: `partial_status`
- PASS: `executed_status`
- PASS: `failed_status`
- PASS: `no_op_status`
- PASS: `realized_price_reconciliation`
- PASS: `realized_value_reconciliation`
- PASS: `cash_before_after_reconciliation`
- PASS: `inventory_flow_reconciliation`
- PASS: `failure_reason_coverage`
- PASS: `treatment_build_hash`
- PASS: `opponent_hash`
- PASS: `configuration_hash`
- PASS: `unit_player_attribution`
- PASS: `unit_seat_consistency`
- PASS: `treatment_opponent_separation`
- PASS: `both_treatment_seats`
- PASS: `watering_attribution`
- PASS: `watering_metric_bounds`
- PASS: `watering_metric_reconciliation`
- PASS: `quadrants_owned_numeric_semantics`
- PASS: `quadrants_hard_cap`
- PASS: `t0_detection`
- PASS: `seat_detection`
- PASS: `seed_detection`
- PASS: `cell_config_allowlist`

## Watering smoke metrics

- P0: status=NO_STEADY_PRODUCTIVE_DAYS, effects=0, needs=0, execution_rate=0.000000, continuity=0.000000
- P1: status=OBSERVED, effects=24, needs=27, execution_rate=0.888889, continuity=1.000000

## Provenance

- Event count: 2722
- Smoke episodes: `E16-E0-A04-S161803398-P0`, `E16-E0-A04-S161803398-P1`
- T0 steps: 1, 0
- Generated: 2026-08-29T20:27:11+00:00

E16-A-R1 was not run. The original Stage A evidence remains preserved.
