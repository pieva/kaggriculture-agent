# C2 REMEDIATION — COPILOT

## Scope

Remediation autorizzata del solo candidato Copilot C2, basata sulla failure review
post-tournament. Non sono stati modificati Foundation C2, altri candidati, configurazioni
di torneo o runner comune; non è stato avviato Kaggle né il tournament comune.

## Failure e limiti C2 presi in carico

| Classe | Problema C2 | Evidenza |
|---|---|---|
| BUG / RUNTIME DEFECT | L'entrypoint forzava `player_index=0`, anche in P1. | Nei sei replay C2, Copilot P1 leggeva `farms[0]` mentre l'engine applicava le azioni a `farms[1]`. |
| BUG / RUNTIME DEFECT | L'entrypoint non accettava l'argomento `configuration` dell'engine diretto. | Il primo preflight reale ha sollevato `TypeError` prima di eseguire l'episodio. |
| POLICY-REALIZATION DEFECT | Nessun bootstrap seed, nessun ordine market e nessuna vendita. | Stato iniziale reale: zero seed; `market: []` permanente; `PLANT` irraggiungibile. |
| POLICY-REALIZATION DEFECT | Nessun target spaziale né `MOVE`. | Farmer fermo a `(4,4)`, active surface zero e MOVE zero nei replay. |
| MODEL_SPEC-TO-BUILD MISMATCH | Il MODEL_SPEC descriveva lifecycle locale ma non contrattualizzava il loop iniziale. | Acquisizione, routing e ricavo erano assenti o esplicitamente non prioritari. |

## Modifiche ed evidenza → meccanismo

| Problema C2 | Modifica | Meccanismo atteso | Previsione verificabile nel prossimo tournament |
|---|---|---|---|
| Binding P1 errato | `CopilotC2Agent` usa `observation.player`; `private` dict è trattato come stato della seat chiamante. | Azioni calcolate sulla propria farm in P0 e P1. | Nessuna divergenza P1 tra tile lette e tile mutate; completion senza fallback. |
| Firma non conforme | `__call__` accetta `configuration`. | Invocazione diretta compatibile con `kaggle_environments`. | Nessun `TypeError` in entrambe le seat. |
| Zero seed e nessun ricavo | Ordini `BUY_SEED WHEAT` per il deficit del core e `SELL` dello shed crop. | Capitale → seed → PLANT → HARVEST → shed → ricavo → replant. | `BUY_SEED`, `SELL` e denaro oltre capitale iniziale osservabili. |
| Farmer stationary | Core NW 3x3 centrato sulla spawn, target nearest-first e routing cardinale. | Le azioni lifecycle raggiungono tile lavorabili senza routing globale. | MOVE > 0, posizioni distinte e active surface > 0. |
| Contratto insufficiente | MODEL_SPEC aggiornato con ownership, bootstrap, routing e vendita limitata. | BUILD e policy hanno un loop minimo esplicito e verificabile. | Le transizioni previste sono osservabili nel preflight e nel tournament. |

## Risultati test e controlli

| Comando | Risultato |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest tests\test_copilot_c2.py -q` | PASS — 7 passed |
| `.\.venv\Scripts\python.exe -m pytest` | 164 passed, 8 failed: tutti i failure sono in `tests/test_codex_c2_candidate.py`, contro modifiche concorrenti Codex già presenti nel worktree; nessun failure Copilot |
| `.\.venv\Scripts\python.exe -m py_compile src\agricola\strategy\copilot\c2_policy.py src\agricola\strategy\copilot\agent_c2.py` | PASS |
| `git diff --check` | PASS |

## Real-engine preflight P0/P1

Comando eseguito: script inline Python con `kaggle_environments.make("kaggriculture",
configuration={"seed": 1113294977, "episodeSteps": 144}, debug=True)`, Copilot C2
contro `starter`, una volta in P0 e una in P1.

| Metrica | P0 | P1 |
|---|---:|---:|
| step registrati / stato finale | 144 / DONE | 144 / DONE |
| errori / fallback patologici | 0 / 0 | 0 / 0 |
| posizioni farmer uniche | 4 | 4 |
| MOVE / PLANT / WATER / HARVEST | 24 / 12 / 24 / 8 | 24 / 12 / 24 / 8 |
| `BUY_SEED` / `SELL` | 9 / 2 | 9 / 2 |
| massimo seed / active surface / shed crop | 4 / 4 / 4 | 4 / 4 / 4 |
| capitale iniziale → finale | $3,000 → $3,083 | $3,000 → $3,083 |

Le assertion del preflight richiedevano `DONE`, movimento reale, acquisizione seed,
superficie PLANT, HARVEST con unità nello shed e `SELL` con denaro massimo superiore
al capitale iniziale. Sono tutte passate in P0 e P1.

## Failure residui

- Il core è deliberatamente limitato a 3x3 e il preflight ha raggiunto al massimo quattro
  tile attive: il candidate è operativo ma non rivendica ottimalità di scala.
- Nessun test di 144 step dimostra la performance relativa su tutte le seed; questa è
  precisamente la domanda riservata al prossimo tournament comune.
- Livestock, espansione fondiaria e market timing restano fuori dallo scope C2.

Questi limiti non impediscono la comparabilità: il productive loop minimo è realizzato
e le transizioni critiche sono state osservate nel real engine in entrambe le seat.

## Freeze

Hash SHA-256 rilevati dopo il preflight:

- `src/agricola/strategy/copilot/agent_c2.py`: `1C24AF2FA5A9D068E45DAB457A05BC2AB73551D1FE4F6F0B34CB186DC6B4256D`
- `src/agricola/strategy/copilot/c2_policy.py`: `0E2A5BC008457BEA49D934B5CA8A9356F85B176B2E19C332C5363C1C803AE5FE`
- `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`: `BF22E3A570156606100FF5543D67B343572FAE99E3A8DD1FFEE8D0E539564FFC`

## File modificati

- `docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md`
- `src/agricola/strategy/copilot/agent_c2.py`
- `src/agricola/strategy/copilot/c2_policy.py`
- `tests/test_copilot_c2.py`
- `results/model_spec_c2/copilot/BUILD_VERIFICATION.md`
- `results/model_spec_c2/remediation/COPILOT_C2_REMEDIATION.md`

```text
C2_REMEDIATION_COMPLETE
TOURNAMENT_READY: YES
```
