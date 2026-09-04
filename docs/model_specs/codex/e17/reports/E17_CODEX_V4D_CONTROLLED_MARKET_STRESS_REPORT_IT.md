# E17.2 — Stress V4D sui regimi di mercato controllati

Data: 2026-09-02

Ruolo evidenza: `DEVELOPMENT_ONLY`

Verdetto: `PASS — D27_ADMITTED_FOR_ISOLATED_CAUSAL_TEST`

## Sintesi

La candidata congelata
`CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28` supera il controllo
`CODEX-E17.2-REACTIVE-SERVICE-ROUTING-CORE-V3-D28` in tutti i 24 confronti
matched e nei quattro regimi di mercato controllati. Il guadagno medio
complessivo è `+890,63` (`+0,723%`), con zero fughe, errori, fallback, residui
vendibili terminali o violazioni degli ordini non-SELL.

Tutti gli otto gate preregistrati passano. V4D è ammessa come baseline per un
test isolato dell'anticipo del routing da D28 a D27. Questo non costituisce
promozione a holdout o Kaggle.

## Disegno

- tre seed development: `26090101`, `26090102`, `26090103`;
- entrambi i seat;
- V4D candidata e V3 controllo;
- quattro regimi: `INERT`, `WHEAT_SCARCITY`, `OUTPUT_PRESSURE`,
  `LIQUIDITY_STRESS`;
- `48/48` episodi completati, nessuna sostituzione;
- seed holdout e final confirmation non consumati;
- sorgenti e config delle due policy verificati prima e dopo l'esecuzione.

Le pressioni sono prodotte dall'avversario V9 congelato mediante la definizione
storica `MarketRegimeOpponent` di E17.1. Non sono state applicate mutazioni
dirette allo stato privato della candidata.

## Risultati per regime

| Regime | V4D | V3 | Delta | Delta % | MOVE/service V4D | MOVE/service V3 |
|---|---:|---:|---:|---:|---:|---:|
| INERT | 135.096,83 | 134.351,33 | +745,50 | +0,555% | 2,872 | 3,000 |
| WHEAT_SCARCITY | 132.673,00 | 131.610,83 | +1.062,17 | +0,807% | 2,888 | 2,982 |
| OUTPUT_PRESSURE | 95.982,83 | 95.312,67 | +670,17 | +0,703% | 2,991 | 2,891 |
| LIQUIDITY_STRESS | 132.608,00 | 131.523,33 | +1.084,67 | +0,825% | 2,940 | 2,993 |
| **Totale** | **124.090,17** | **123.199,54** | **+890,63** | **+0,723%** | **2,922** | **2,967** |

Il peggior delta percentuale è quello inerte ed è comunque positivo
(`+0,555%`). Il minimo matched è `+497`; la quota di confronti non negativi è
`24/24 = 100%`.

## Effetto operativo

Sui 24 run V4D:

- MOVE: `8.690` contro `8.906` (`−216`);
- servizi: `2.974` contro `3.002`;
- `MOVE/service`: `2,922` contro `2,967`;
- HARVEST: `1.582` contro `1.321`;
- DROP: `552` contro `817`;
- trigger di capacità: `48`;
- batch di flush attivi: `144`;
- decisioni di rilascio post-feed: `1.004`;
- ledger unità: `12.792/12.792` classificato;
- ledger mercato: `274/274` classificato.

Il meccanismo di capacità è osservato in ciascun regime. Le decisioni di
rilascio sono callback di assegnazione del worker, non equivalgono da sole a
DROP fisici.

## Sicurezza e integrità

| Controllo | Esito V4D |
|---|---:|
| errori tecnici | 0 |
| fallback | 0 |
| action shape invalide | 0 |
| fughe animali EOD | 0 |
| perdite crop EOD | 311, identiche al controllo |
| residui vendibili terminali | 0 |
| violazioni non-SELL | 0 |
| copertura ledger unità | 100% |
| copertura ledger mercato | 100% |

## Gate preregistrati

| Gate | Esito |
|---|---|
| sicurezza comune in ogni regime | PASS |
| media complessiva non inferiore a V3 | PASS |
| media INERT non inferiore a V3 | PASS |
| almeno 3/4 regimi non negativi | PASS — 4/4 |
| peggior regime almeno −1% | PASS — +0,555% |
| almeno 75% matched non negativi | PASS — 100% |
| MOVE/service complessivo inferiore | PASS |
| meccanismo capacità presente in ogni regime | PASS |

## Interpretazione e limite

Il vantaggio di V4D non dipende dal solo scenario inerte: la gestione
post-feed della capacità continua a monetizzare più output anche quando il
mercato subisce scarsità Wheat, pressione sugli output o stress combinato.
Questo sostiene causalmente il meccanismo, non dimostra ancora robustezza su
avversari competitivi arbitrari né predice direttamente il rating Kaggle.

`OUTPUT_PRESSURE` è il regime da sorvegliare: V4D mantiene il vantaggio
economico, ma localmente aumenta `MOVE/service` rispetto a V3. Il successivo
test D27 deve quindi mutare soltanto il giorno di attivazione, conservare la
telemetria per regime e non confondere un anticipo temporale con un nuovo
intervento sulla topologia o sulla quota livestock Q2.

## Artefatti

- preregistrazione:
  `docs/model_specs/codex/e17/design/E17_CODEX_V4D_CONTROLLED_MARKET_STRESS_PLAN_V1.md`;
- runner:
  `docs/model_specs/codex/e17/tools/run_codex_e17_v4d_market_stress_development.py`;
- metriche:
  `docs/model_specs/codex/e17/artifacts/derived/E17_2_V4D_CONTROLLED_MARKET_STRESS_METRICS.json`.
