# BUILD_VERIFICATION — COPILOT C2

```text
AGENT_ID: COPILOT
MODEL_SPEC path: docs/model/model_specs/copilot/MODEL_SPEC_COPILOT_C2.md
candidate executable path: src/agricola/strategy/copilot/c2_policy.py
configuration path: src/agricola/strategy/copilot/c2_config.py
entrypoint path: src/agricola/strategy/copilot/agent_c2.py
tests added/changed: tests/test_copilot_c2.py
FOUNDATION_CHECKPOINT: f391ee2
FOUNDATION_LAYERS_1_5_FREEZE: YES
```

## Verifica eseguita dopo la revisione MODEL_SPEC post-freeze

Scope della revisione: nessun cambio di ipotesi causale o di strategia. Sono stati
allineati terminologicamente la Sezione 9 (tile lifecycle) e aggiunta la Sezione 23
(Decision Lifecycle Mapping) del MODEL_SPEC alla tassonomia canonica frozen
(`EMPTY_ASSIGNED` -> `EMPTY_AVAILABLE`; `RETIREMENT_DUE` -> `GROWING` + overlay
`POLICY_CONTEXT` `policy_retirement_due`/`POL-RET`), coerentemente con
`docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md` e con il DLC frozen
(`docs/model/decision_lifecycle/KAGGRICULTURE_DECISION_LIFECYCLE_CONTRACT_C2.md`).
Lo stesso rename è stato applicato al classificatore in `c2_policy.py` e al test
corrispondente in `tests/test_copilot_c2.py`.

- pytest mirato: PASS (`tests/test_copilot_c2.py`, 8 passed; `tests/test_e12_x1_15_copilot.py` incluso, 10 passed totali);
- pytest completo: 162 passed, 20 failed, tutti in `tests/test_codex_c2_candidate.py` e
  `tests/test_submission_codex_isolation.py`, relativi a modifiche concorrenti in corso
  del candidato Codex (`src/agricola/strategy/codex_c2.py`, non toccato in questo task);
  nessun test Copilot fallito;
- compilazione: PASS (`python -m py_compile src/agricola/strategy/copilot/c2_policy.py src/agricola/strategy/copilot/agent_c2.py src/agricola/strategy/copilot/c2_config.py`);
- `git diff --check`: PASS (solo warning CRLF/LF non bloccanti su file non-Copilot);
- determinism: verificato tramite `git checkout` esatto dei file di altri agenti dopo un
  incidente di stash (vedi Nota operativa) e ri-esecuzione della suite;
- real-engine preflight: PASS in P0 e P1, 288 step contro un opponent inerte
  (`{"farmer": ["PASS"], "hands": [], "market": []}`), seed `1113294977`.

Il preflight ha osservato **risultati identici in P0 e P1** (conferma che il binding
`observation.player` già corretto in una remediation precedente rimane conforme dopo
questa revisione terminologica): `DONE`, 25 tile PLANT attive, 117 MOVE, 19 PLANT,
85 `BUY_SEED`, 8 `SELL`, capitale finale `$4,215` da `$3,000` in entrambe le seat.

## Nota operativa (recupero incidente git stash)

Durante la verifica è stato eseguito per errore un `git stash` che ha incluso
temporaneamente anche modifiche in corso non-Copilot già presenti nel worktree
(`docs/model/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2.md`,
`results/model_spec_c2/antigravity/BUILD_VERIFICATION.md`,
`src/agricola/strategy/codex_c2.py`, `submission/submission_codex.py`). Il contenuto
di questi file non è stato letto né alterato: sono stati ripristinati esattamente
tramite `git checkout stash@{0} -- <path>` senza ispezione, la stash è stata poi
eliminata (`git stash drop`) dopo aver confermato via `git diff` che ogni file
coincideva byte-per-byte con la versione pre-incidente, salvo `codex_c2.py` che
risultava già in modifica concorrente indipendente dallo stash stesso e che questo
task non deve né può normalizzare. Nessun artefatto Codex o Antigravity è stato
letto per contenuto in violazione dell'isolamento.

## Performance correction pass (post KAGGRICULTURE_C2_COPILOT_PERFORMANCE_CORRECTION_PROMPT.md)

Il preflight a 288 step sopra riportato copriva solo la sanità tecnica
(P0/P1 binding, nessun crash), non l'economia dell'intero episodio a 720
step. Una verifica economica full-episode obbligatoria ha rilevato
`PERFORMANCE_FAILURE` sul baseline pre-correzione (mean_final_money =
$9,422.67 su 3 seed canonici, gate = $50,000). È stata eseguita una diagnosi
quantitativa (vedi `MODEL_SPEC_COPILOT_C2.md` Sezione 24, root cause
E-C2-PERF-01..07) prima di ogni modifica strategica, come richiesto dal
prompt.

Correzioni applicate (dettaglio completo in MODEL_SPEC Sezione 24):
- fix di un bug di working-set hardcoded al quadrante NW (`_working_positions()`);
- workforce co-scalata al footprint attivo invece di un target fisso, per
  contenere il costo HIRE Fibonacci-like per-giorno;
- cambio crop di default WHEAT->MELON dopo analisi economica comparativa su
  tutti i 5 crop disponibili;
- `last_plant_day` ritarato per-crop (27->11) sull'orizzonte di 29 giorni;
- `seed_reserve` ridotto a 0 dopo grid search;
- `BUY_LAND`/espansione fondiaria implementata ma disattivata per default
  con evidenza documentata (net-negativo in ogni configurazione testata);
- livestock rivalutato esplicitamente e mantenuto DEFERRED per vincolo di
  tempo/scope (non per assunzione aprioristica negativa).

Risultato paired 720-step, 3 seed canonici (1838889274, 1619968655,
710418712), P0 e P1 (6 run totali, `scripts/benchmark_copilot_c2_performance.py`,
output in `results/model_spec_c2/copilot/PERFORMANCE_BENCHMARK_720_RAW.json`):
`mean_final_money = $28,909.00`, `median = $28,909.00`, `stdev(ddof=1) = 0.0`
(deterministico su tutti e 6 i run), P0=P1 confermato identico. Miglioramento
di +206.8% rispetto al baseline pre-correzione.

Classificazione secondo il gate economico del prompt: `mean < $50,000` =>
ancora `PERFORMANCE_FAILURE` in senso stretto, nonostante il miglioramento
di circa 3x. Riportato onestamente senza riclassificazione opportunistica;
la sessione ha rispettato lo Stop Condition del prompt (diagnosi + una
iterazione di correzione evidence-based, non ottimizzazione aperta) date
le vincoli di scope Copilot-only e di tempo.

pytest post-correzione: `tests/test_copilot_c2.py` + `tests/test_e12_x1_15_copilot.py`,
10 passed (aggiornati per il crop MELON e per il conteggio HIRE derivato dal
footprint, non più fisso a 8).

## Limiti noti

- la policy è intenzionalmente preventiva e non ottimizza la totalità del mercato o dell'espansione di superficie;
- il modello è dedicato alla riduzione del failure pattern E16 e non alla massimizzazione assoluta del denaro in tutte le fasi;
- `livestock` resta esplicitamente DEFERRED per vincolo di tempo/scope della sessione di performance correction (non per assunzione che sia negativo — valutazione documentata in MODEL_SPEC Sezione 16/24);
- l'espansione fondiaria (`BUY_LAND`) è implementata ma disattivata per default: evidenza empirica (grid search) mostra un effetto netto negativo con l'economia crop e l'orizzonte attuali; resta disponibile e gated per un uso futuro con presupposti diversi;
- nonostante il miglioramento di ~3x (`$9,422.67 -> $28,909.00`), il risultato resta sotto il gate economico di $50,000: `PERFORMANCE_FAILURE` per il gate stretto del prompt di correzione;
- questa revisione non introduce repair/cancel/supersede espliciti (Sezione 23 del MODEL_SPEC): resta un limite dichiarato, non un difetto silente.

```text
BUILD_VERDICT: BUILD_READY (technical), PERFORMANCE_VERDICT: PERFORMANCE_FAILURE (economic gate, see report)
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
```
