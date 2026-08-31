# Codex C2 V7 — Build Verification

```text
AGENT_ID: CODEX
BUILD_ID: CODEX-C2-COMPACT-Q0-ROUTINE-V7
FOUNDATION_CHECKPOINT: f391ee2
MODEL_SPEC_REVISION: COMPLETE
TECHNICAL_BUILD: PASS
ECONOMIC_GATE: FAILURE
PRIMARY_BOTTLENECK: LIVESTOCK_SERVICEABILITY
BUILD_VERDICT: BUILD_NOT_READY
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```

## Verification verdict

Il package compact-Q0 è tecnicamente integro e riproducibile, ma non supera il
gate economico e registra fughe animali. Il package è quindi buildable ma
bloccato per qualsiasi fase tournament/Kaggle.

## Foundation and scope

| Check | Esito |
|---|---|
| repository checkpoint | `main @ f391ee2` |
| Foundation / DLC comune | invariati |
| Antigravity / Copilot | non modificati da questo build |
| Q0 only / no `BUY_LAND` | PASS |
| commit / push | non eseguiti |

Il worktree contiene attività concorrenti preesistenti. Sono state preservate
senza reset o inclusione nell'identità Codex.

## Technical checks

| Check | Esito |
|---|---|
| source import and compile | PASS |
| standalone build and isolated import | PASS |
| source/standalone parity | PASS — exact, 120 step, seed 26090101/02 |
| engine prefix P0/P1 | PASS — 120 step, zero error/fallback |
| terminal handling P0/P1 | PASS — `DONE` / `TERMINAL_CLOSED` |
| manual `DROP` / `BUY_LAND` | zero |
| request/effect verification | PASS |
| Codex targeted tests | PASS — 20 |
| repository suite | PASS — 183 |
| Ruff Codex paths | PASS |

Il warning `.pytest_cache` WinError 5 è non-funzionale. I messaggi
OpenSpiel su giochi opzionali mancanti sono rumore di import del package e non
failure Kaggriculture.

## Preregistered performance batch

```text
PROTOCOL: CODEX_COMPACT_Q0_ROUTINE_PREREGISTERED
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
EPISODES: 6
POST_HOC_TUNING: NO
```

| Metrica | Valore |
|---|---:|
| FINAL_MONEY mean / median / std | 39.265,67 / 38.943,00 / 1.312,86 |
| range | 37.520–41.156 |
| MILK / WOOL mean | 28,17 / 14,67 |
| MELON / STRAWBERRY mean | 95,00 / 40,17 |
| productive utilization | 67,43% |
| MOVE per productive action | 3,1923 |
| on-time crop service | 79,49% |
| hard-deadline misses | 50 |
| animal escapes | 24 |

Tutti gli episodi sono `DONE` con zero errori e fallback. Il risultato
supera AG Q0 3+3 di 1.268,00 ma resta sotto 50.000 e a -17.506,33 da LuCcc.

## Artifact identity

| Artifact | Byte | SHA-256 |
|---|---:|---|
| `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md` | 9.201 | `5F6A3E5199589408CF43D4BBE13C629B6B978B095046BAE4D912006F8248D1F7` |
| `src/agricola/strategy/codex_compact_q0.py` | 77.337 | `7C4D497EF42C1319AF6890621B490A1D870FF9400230E30318B8050367BAB0D6` |
| `src/agricola/strategy/codex_c2.py` | 1.217 | `EB334581F4AA9D8CF2FE7E1F835874934512AF1C5A36772FDB0F5ECADF88263E` |
| `configs/model_spec_c2/CODEX_C2_CONFIG.json` | 976 | `5B3A8A01160243ACE00CBD4BA0F76EB57E73B09079A7F2316C0584A3FE24DF47` |
| `submission/submission_codex.py` | 130.649 | `965E03566E2F8C2FAF04A9A275781D2953F03C66288031700BDB59E49A5A0427` |
| `CODEX_COMPACT_Q0_ROUTINE_TECHNICAL_SMOKE.json` | 1.592 | `6091F7EFAA9735D18BBB836C6A887394D45C4950E37D5F96A4570AFF9C53A29F` |
| `CODEX_COMPACT_Q0_ROUTINE_RESULTS.csv` | 40.915 | `CAE6042276EA9CDDD312264E0B568E1B50F344FF6C43B4F0620AC0F5713B97A5` |
| `CODEX_COMPACT_Q0_ROUTINE_RESULTS.json` | 48.892 | `16F5CD2A19D4B1C956B2EF6990D3FE76F4AF1F1EDC71505207777BB9E1A35F28` |

## Gate

```text
TECHNICAL_PACKAGE_READY: YES
ECONOMIC_MODEL_READY: NO
BUILD_VERDICT: BUILD_NOT_READY

TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO

NEXT_GATE: NEW_AUTHORIZED_BUILD
```
