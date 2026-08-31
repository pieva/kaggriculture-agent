# TOURNAMENT MANIFEST — ANTIGRAVITY MODEL_SPEC C2

- **AGENT_ID:** `antigravity`
- **Agent Name:** Antigravity C2 High-Attainment Horticultural Controller
- **MODEL_SPEC Path:** `docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md`
- **MODEL_SPEC Version:** `2.1.0`
- **Foundation Version:** `C2`
- **Date:** 2026-08-31
- **Status:** `TOURNAMENT_READY: YES`

---

## 1. Controller Entrypoint Specification

- **Python Module:** `agricola.strategy.antigravity.agent_c2`
- **Callable Class:** `AntigravityC2Agent`
- **Package Init Export:** `from agricola.strategy.antigravity import AntigravityC2Agent`
- **Standard Signature:** `__call__(observation: Dict[str, Any], configuration: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`
- **Action Schema Output:**
  ```python
  {
      "farmer": List[str],    # e.g. ["MOVE", "NORTH"] or ["WATER"] or ["HARVEST"] or ["PASS"]
      "hands": List[List[str]], # List of action commands for each active hand
      "market": List[List[Any]], # List of market orders e.g. [["SELL", "WHEAT", 5], ["HIRE"]]
  }
  ```

---

## 2. Configuration Parameters

```python
AntigravityC2Config(
    quadrants_owned=2,
    crop_working_set_target=40,
    pasture_allocation_target=0,
    livestock_headcount_target=0,
    workforce_headcount=10,
    operating_cash_floor=50.0,
    endgame_shutdown_steps=48,
    enable_strict_harvest_gate=True,
    enable_recovery_dig=True,
    enable_preventive_dig=True,
    enable_day0_water_priority=True,
    crop_mix_weights={"WHEAT": 0.20, "STRAWBERRY": 0.45, "MELON": 0.35},
)
```

---

## 3. Local Qualification Performance

| Metrica di Qualifica | Valore Misurato (3 Seeds: 1838889274, 1619968655, 710418712) |
|---|---|
| **Completion Rate** | 100.0% (3/3 completati senza errori o timeout) |
| **Disqualification Rate** | 0.0% (Zero violazioni di regole engine) |
| **Mean Final Money** | **$43,837.33** |
| **Median Final Money** | **$44,698.00** |
| **Min Final Money** | **$41,548.00** |
| **Max Final Money** | **$45,266.00** |
| **Standard Deviation** | $2,002.32 |
| **Baseline v2.0.0 Mean** | $29,112.33 |
| **Absolute Delta** | +$14,725.00 |
| **Percentage Delta** | +50.58% |
| **Premature Harvest No-Ops** | **0** (Azzerati al 100%) |
| **Lost Weed Persistence** | $< 3$ steps (Bonifica immediata via `DIG`) |
| **Daily Watering Compliance** | 100.0% (0 piante disidratate a EOD) |

---

## 4. Telemetry Schema & Decomposition Hook

Antigravity C2 supporta la registrazione dei ledger di performance:
- `crop_species_ledger`: Tracciamento di semi acquistati, azioni idriche erogate, rese raccolte, ricavi di mercato e margine lordo per WHEAT, STRAWBERRY, MELON, CARROT, TOMATO;
- `workforce_ledger`: Tracciamento del budget salariale giornaliero e della produttività media per unità di lavoro;
- `tile_lifecycle_ledger`: Frequenze di transizione tra `EMPTY_ASSIGNED`, `GROWING`, `HARVEST_READY`, `RETIREMENT_DUE`, `LOST_WEED`, `OUT_OF_SCOPE`.

---

## 5. Known Strategic Constraints

1. **Focus 2 Quadranti (40 tile su 48 arabili):** Antigravity concentra l'infrastruttura sui quadranti Q0 (NW) e Q1 (NE), differendo l'acquisto di Q2/Q3 per evitare l'inflazione di transito e il disallineamento della spesa salariale;
2. **Ablazione Zootecnica Totale:** Zero animali allevati per azzerare il lock-up di capitale e i costi di mangime, concentrando il 100% dell'energia operativa sulle colture ad altissima resa (Strawberry e Melon).

---

## 6. Tournament Readiness Declaration

```text
TOURNAMENT_MANIFEST: READY
TOURNAMENT_READY: YES
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
