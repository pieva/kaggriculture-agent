# COPILOT C2 — Performance Iteration

## 1. Stato iniziale

Il retournament C2 era tecnicamente valido: 6/6 episodi Copilot `DONE`, zero
errori, zero fallback e audit action replay senza mismatch. Il candidato era
operativo ma non competitivo: mean final money `$4,154`, median `$4,225.50`,
sample std `$201.38`, min/max `$3,793/$4,332`, record `0-6-0`.

## 2. Diagnosi quantitativa

| Dimensione | Evidenza retournament Copilot |
|---|---:|
| owned / max active / final active surface | 25 / 4 / 4 |
| active mean | 3.30 |
| workforce max / effective mean | 1 / 1.00 |
| quadranti massimi | 1 |
| first revenue step | 73 |
| minimum cash | $2,920 |
| PLANT / WATER / HARVEST effect medi | 60 / 120 / 56 |
| SELL effect medi | 14 |

Le transizioni erano valide: nessun opcode Copilot mostrava un gap dispatch/effect
nel retournament. Il valore si perdeva quindi prima del throughput, per capacità
deliberatamente non attivata: 21 delle 25 tile NW possedute restavano inutilizzate,
non erano presenti hand e quasi tutto il capitale iniziale restava inattivo.

## 3. Collo di bottiglia dominante

Classificazione sostenuta: `CAPACITY_LIMIT`, `WORKFORCE_LIMIT`,
`LAND_UTILIZATION_LIMIT`. Non sono supportati `BIOLOGICAL_LIMIT` o
`SERVICE_LIMIT` nel micro-core: WATER, HARVEST e SELL avevano effetto osservabile.
Non si compra ulteriore terra, perché la superficie già posseduta era inutilizzata:
`OWNED_SURFACE != ACTIVE_SURFACE != SERVICEABLE_SURFACE != PRODUCTIVE_SURFACE`.

## 4. Ipotesi causale congelata

```text
HYPOTHESIS_ID: COPILOT_C2_PI_H1_SERVICEABLE_NW_THROUGHPUT
OBSERVED_PROBLEM: $4,154 mean, max active 4, workforce 1, cash minimum $2,920.
EVIDENCE: transizioni locali valide; 21 tile NW e capitale disponibili ma inattivi.
CAUSAL_MECHANISM: la policy preveniva failure locali ma il micro-cluster non aveva
  massa né service capacity per generare throughput competitivo.
MODEL_CHANGE: 25 tile NW, workforce totale 9, task distinti nearest-first, WHEAT
  rapido, reinvestimento in seed e workforce, vendita continua.
EXPECTED_INTERMEDIATE_EFFECT: P0/P1 con >=20 active, >=9 workforce e WATER,
  HARVEST, SELL con state transition.
EXPECTED_ECONOMIC_EFFECT: final_money UP; target comune mean >$23,000.
FALSIFICATION_CONDITION: assenza degli effetti intermedi in P0/P1 falsifica H1;
  mean tournament <=$23,000 falsifica il target economico.
```

## 5. Revisione del MODEL_SPEC

Il MODEL_SPEC ora contrattualizza il quadrante NW intero come working set
serviceable, le distinzioni owned/active/serviceable/productive/monetized, la
workforce totale nove, l'allocazione a target distinti e il cutoff di semina day
27. Non introduce expansion, livestock o market timing.

## 6. Modifiche implementate

- [c2_config.py](C:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/copilot/c2_config.py):
  raggio configurato fino alle 25 tile NW, workforce target 9, riserva semi e
  cutoff di semina.
- [c2_policy.py](C:/Users/pietr/Projects/kaggriculture-agent/src/agricola/strategy/copilot/c2_policy.py):
  assegnazione greedy di task distinti, semina dalla frontiera vicina allo shed,
  riassunzione giornaliera, vendita e seed reinvestment entro il limite market.
- [test_copilot_c2.py](C:/Users/pietr/Projects/kaggriculture-agent/tests/test_copilot_c2.py):
  verifica di task PLANT distinti per unità disponibili.

## 7. Previsioni preregistrate

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: >23000

METRIC_A: active surface / workforce
CURRENT_VALUE: max 4 / 1
EXPECTED_VALUE_OR_DIRECTION: >=20 / >=9 nel preflight
WHY_CAUSAL: misura directly il capacity activation di H1.

METRIC_B: WATER / HARVEST / SELL effects
CURRENT_VALUE: effetti presenti su solo quattro tile
EXPECTED_VALUE_OR_DIRECTION: effetti presenti con active surface >=20 in P0/P1
WHY_CAUSAL: esclude superficie non serviceable come spiegazione apparente.
```

## 8. Preflight P0/P1

Unico preflight meccanicistico: `kaggriculture`, seed non ufficiale `26083002`,
360 step, Copilot contro `starter`, esecuzioni separate in P0 e P1. Non è un
tournament né usa seed comuni.

| Metrica | P0 | P1 |
|---|---:|---:|
| status / step | DONE / 360 | DONE / 360 |
| error / fallback | 0 / 0 | 0 / 0 |
| max / final active surface | 25 / 25 | 25 / 25 |
| max / mean workforce | 9 / 8.67 | 9 / 8.67 |
| WATER effect steps | 203 | 203 |
| HARVEST yield-reduction steps | 42 | 42 |
| SELL cash-gain steps | 11 | 11 |
| initial / minimum / final cash | $3,000 / $2,078 / $4,432 | $3,000 / $2,078 / $4,432 |

Tutte le assertion preregistrate del preflight sono passate in entrambe le seat.

## 9. Test

| Comando | Risultato |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest tests\test_copilot_c2.py -q` | PASS — 8 passed |
| `.\.venv\Scripts\pytest.exe -q` | PASS — 176 passed |
| `.\.venv\Scripts\python.exe -m py_compile src\agricola\strategy\copilot\c2_policy.py src\agricola\strategy\copilot\c2_config.py` | PASS |
| `git diff --check` | PASS |
| `.\.venv\Scripts\ruff.exe check` sui file Copilot | Non configurato nel progetto; il default corrente segnala esclusivamente regole di modernizzazione/stile `UP*` del typing preesistente. Nessun autofix eseguito. |

## 10. Limiti residui

- Il preflight conferma il meccanismo, non il target mean: nessuna performance
  claim è fatta prima del prossimo tournament comune.
- Il modello usa solo WHEAT e una sola terra; crop mix, livestock e land expansion
  restano ipotesi non testate e fuori da H1.
- La workforce viene riassunta ogni giorno per semantica engine; la routing
  efficiency a 720 step sarà valutata esclusivamente nel round comune.

## 11. Freeze degli artifact

- `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`
- `src/agricola/strategy/copilot/c2_config.py`
- `src/agricola/strategy/copilot/c2_policy.py`
- `tests/test_copilot_c2.py`
- `results/model_spec_c2/performance_iteration/COPILOT_C2_PERFORMANCE_ITERATION.md`

Hash SHA-256 dopo le verifiche:

- `MODEL_SPEC_COPILOT_C2.md`: `7B5DA675D784BF3B607B1CFC148C7EBBB7B3995EF76D1E289E46F9FA496C560B`
- `c2_config.py`: `F2F6481E6F21A5BF71D43469020EF506EA6BE52D10CFDF31F006ABF89CA01A2D`
- `c2_policy.py`: `F9064A6C7F5249A01D8BFA3441A4555516FEA82D3868CFEA403789355C10D3B2`
- `test_copilot_c2.py`: `BB53974ADF61DE08809437A046AEC757BFB65FC9FBDDADAD908FB2DFCD4782A2`

## 12. Stato finale

```text
C2_PERFORMANCE_ITERATION_COMPLETE: YES
TOURNAMENT_READY: YES
TARGET_MEAN_FINAL_MONEY: >23000
```
