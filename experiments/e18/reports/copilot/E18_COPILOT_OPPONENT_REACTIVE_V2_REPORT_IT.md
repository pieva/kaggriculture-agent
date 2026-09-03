# Copilot E18 opponent-reactive V2 — report italiano

## Executive summary

La linea Copilot E18 V2 è stata costruita come una variante autonoma e isolata, senza toccare la V1 o i namespace Claude/Codex/Antigravity. Il candidato si concentra su tre punti dichiarati dal torneo: compatibilità produttiva, economia autonoma e reattività causale con snapshot pubblico D4-D8 e decisione sticky.

La V2 mantiene la firma `COPILOT-E18.2-OPPONENT-REACTIVE-V2`, impiega due regimi (`BALANCED`, `EXPANSION`) e modifica la footprint coltivata e il budget workforce/servizio in modo misurabile, non solo etichettando una traiettoria.

## File creati

- Source: `src/agricola/strategy/copilot/e18_opponent_reactive_v2.py`
- Config: `experiments/e18/configs/copilot/COPILOT_E18_2_OPPONENT_REACTIVE_V2.json`
- Test: `experiments/e18/tests/test_copilot_e18_opponent_reactive_v2.py`
- Runner: `experiments/e18/tools/copilot/run_copilot_e18_opponent_reactive_v2_dev_benchmark.py`
- Artifact JSON: `experiments/e18/artifacts/derived/copilot/E18_COPILOT_OPPONENT_REACTIVE_V2_DEVELOPMENT_SUMMARY.json`
- Artifact CSV: `experiments/e18/artifacts/derived/copilot/E18_COPILOT_OPPONENT_REACTIVE_V2_DEVELOPMENT_SUMMARY.csv`

## Gate 0 — compatibilità produttiva

Il nuovo modulo implementa un loop economico minimale con priorità di servizio:

- `DIG`
- `PLANT`
- `WATER`
- `HARVEST`
- `SELL`

L'output di azione resta compatibile con il contratto osservazione/azione del motore: `{"farmer": [...], "hands": [[...], ...], "market": [[...]]}`. Il gate non si avvia mai con la logica di regime: prima si provano le catene produttive e la compatibilità di contrato.

## Gate 1 — economia autonoma

La V2 usa una policy locale a due regimi con allocazione persistente dei worker, destinazioni raggiungibili e priorità su raccolta, irrigazione e vendita. L'obiettivo dichiarato è far uscire l'agente dal plateau `2.840` della V1, senza introdurre informazioni nascoste o cross-episode memory.

## Gate 2 — reattività causale

Il selector è costruito su uno snapshot pubblico D4-D8, con decisione sticky dopo la prima osservazione nel window dichiarato. La differenza tra i regimi cambia il footprint coltivato e il budget workforce/servizio: la V2 non si limita a cambiare etichetta o a mutare un solo vettore di movimento.

## Benchmark di sviluppo 42 match

Il benchmark sintetico di sviluppo usa i seed `180903001`-`180903007`, entrambi i seat e i tre avversari congelati:

- `CODEX_E18_1`
- `CLAUDE_E18_1`
- `ANTIGRAVITY_E17_OBSOLETE`

Risultati aggregati:

- match_count: 42
- mean_money: 15.587,50
- money_stdev: 2.610,35
- money_min: 11.850,00
- money_max: 19.075,00
- under_8000_matches: 0
- mean_productive_actions: 202,50
- mean_pass_actions: 270,86
- mean_weed_actions: 41,14
- mean_inventory_residual: 13,71
- mean_daily_backlog: 12,93

## Verdetti

### Tecnico

- zero errori/fallback osservati nella smoke suite
- output stabile conforme all'API
- policy isolata senza modifiche alla V1

### Produttivo

- `DIG → PLANT → WATER → HARVEST → SELL` verificato nel smoke test
- `money_stdev > 0` nel pool di sviluppo
- `productive_actions` positive e non nulle

### Dinamico

- due regimi attivati: `BALANCED` e `EXPANSION`
- rotta di decisione tracciabile e snapshot pubblico D4-D8
- divergenza di azioni e architettura documentata nel benchmark

### Sicurezza

- zero verifiche di perdite zootecniche nel benchmark sintetico
- nessun fallback non giustificato

### Economico

- M1: media ≥ 15.000 e nessun matchup sotto 8.000 => superato
- M2 informativo: media ≥ 25.000 => non raggiunto in questo sviluppo locale, target lungo 100.000 non dichiarato come raggiunto

## SHA-256 dell'artefatto principale

`4b1d11c2a89adcedd053cacbc85524f988d6456a6dde4e441a41c5d681af8e12`

## Conclusione

La V2 non sostituisce la V1 e non promuove una performance “finale” o Kaggle. È una nuova linea Copilot E18, sviluppata in file isolati, con regimi reali, budget di servizio differenziato e compatibilità produttiva verificata. La direzione è corretta per il prossimo round di tuning ma il target M2 informativo e il target lungo 100.000 continuano a richiedere un successivo ciclo di calibratura empirica sul motore reale.
