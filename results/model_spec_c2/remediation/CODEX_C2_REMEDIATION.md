# Codex C2 — Remediation e freeze immediata

```text
AGENT_ID: CODEX
BUILD_ID: CODEX-C2-REMEDIATED-V2
SOURCE_FEEDBACK: results/model_spec_c2/feedback/CODEX_C2_ROUND_FEEDBACK.md
COMPARATIVE_RETournament: NOT EXECUTED
KAGGLE_SUBMISSION: NOT EXECUTED
```

## Esito

La remediation è completa. MODEL_SPEC, configurazione, policy e test sono
allineati alla V2. La preflight sul motore reale è passata in P0 e P1 senza
eccezioni o fallback e con transizioni di stato/economia osservabili. Non è
stato eseguito il torneo comune.

## Diagnosi consolidata

| Classe | Esito della diagnosi |
|---|---|
| `BUG_RUNTIME` | Nessun crash nel primo torneo; era assente l'osservabilità esplicita del fallback. Aggiunti contatori e ultimo errore. |
| `POLICY_REALIZATION` | Il lifecycle era corretto localmente, ma routing, layout e sequenza economica non trasformavano capacità nominale in superficie e ricavo. |
| `SPEC_BUILD_MISMATCH` | La V1 dichiarava routing, market e workforce invariati, benché fossero determinanti nel failure osservato. La V2 li rende parte esplicita della policy. |
| `STRATEGIC_LIMITATION` | Target 17, mix 40/40/20, land immediata e riserva feed nominale producevano scala bassa, cash lock e monetizzazione tardiva. |

## Modifiche significative

### 1. Scala produttiva e layout

- **PROBLEMA:** working set nominale non realizzato e superficie troppo piccola.
- **EVIDENZA:** mean active surface 9,17, massimo 16, finale 6–8 contro target 17.
- **MODIFICA:** bootstrap compatto di 10 tile NW; target full 25; layout ordinato per distanza dallo shed, con pasture e shed esclusi.
- **MECCANISMO ATTESO:** dimostrare prima l'esecuzione locale, poi usare la seconda land per ampliare una base già produttiva.
- **PREVISIONE VERIFICABILE:** superare il precedente massimo 16 e osservare lo sblocco della seconda land solo dopo almeno 8 PLANT attive.

### 2. Mix crop e orizzonte

- **PROBLEMA:** quota elevata di crop a maturità day 10 e cutoff finale non crop-aware.
- **EVIDENZA:** mix V1 40/40/20; cash fermo a 300 e prima crescita allo step 321; STRAWBERRY/MELON richiedono 240 step alla prima maturity.
- **MODIFICA:** pattern 60/20/20 WHEAT/STRAWBERRY/MELON; sostituzione tardiva con WHEAT quando ancora maturabile; nessun replant quando nessuna crop è serviceable.
- **MECCANISMO ATTESO:** più cicli rapidi e nessun capitale immobilizzato in crop incapaci di maturare entro il termine.
- **PREVISIONE VERIFICABILE:** primo ciclo economico prima dello step 321; PLANT tardive bloccate mentre crop esistenti continuano a ricevere WATER/HARVEST/DIG.

### 3. Market e gate economici

- **PROBLEMA:** BUY_LAND immediato, seed deficit acquistato in blocco e floor quasi assorbito prima del ritorno economico.
- **EVIDENZA:** 248 campioni al/sotto del floor 300 e land acquisita prima di prova di utilizzo produttivo.
- **MODIFICA:** seed acquistati solo nella quantità sostenibile; BUY_LAND richiede 8 crop attive e cash 1.600; floor 300 preservato.
- **MECCANISMO ATTESO:** il bootstrap mantiene liquidità e l'espansione segue lo stato realizzato invece dell'intento nominale.
- **PREVISIONE VERIFICABILE:** nessun BUY_LAND iniziale; BUY_LAND singolo dopo il gate; cash minimo non inferiore al floor in esecuzione valida.

### 4. Workforce e routing

- **PROBLEMA:** movimento dominante e nearest-task ricalcolato a ogni step.
- **EVIDENZA:** MOVE raw medio 3.861,2 su 4.988,3 unit action, circa 77,4%; 191 richieste HIRE per episodio senza raggiungere il target produttivo.
- **MODIFICA:** 5 hands nel bootstrap, 8 dopo espansione; target sticky per worker entro il giorno; arbitration prima per priorità globale e poi per distanza.
- **MECCANISMO ATTESO:** meno retargeting, più continuità verso task crop urgenti e costo iniziale più controllato.
- **PREVISIONE VERIFICABILE:** transizioni reali di posizione e task effect in entrambi i seat; movement share direzionalmente inferiore alla V1, da verificare nel retournament.

### 5. Livestock e riserva WHEAT

- **PROBLEMA:** la riserva feed era calcolata sul target COW 4 anche prima della mandria.
- **EVIDENZA:** WHEAT era trattenuto mentre il ciclo economico crop restava tardivo.
- **MODIFICA:** livestock attivo solo con almeno 80% del target crop e cash 1.500; acquisto COW limitato alle pasture costruite; riserva feed sulle sole COW presenti.
- **MECCANISMO ATTESO:** priorità al motore crop e vendita del WHEAT non necessario.
- **PREVISIONE VERIFICABILE:** SELL WHEAT consentito con herd assente; nessun BUY_ANIMAL prima del gate.

### 6. Failure containment

- **PROBLEMA:** il SAFE_PASS mascherava la frequenza dei fallback.
- **EVIDENZA:** la V1 non esponeva contatori interrogabili dal runner.
- **MODIFICA:** `error_count`, `fallback_count` e `last_exception` sull'istanza isolata; eccezione top-level → SAFE_PASS puro.
- **MECCANISMO ATTESO:** ogni episodio non comparabile diventa immediatamente rilevabile.
- **PREVISIONE VERIFICABILE:** contatori 0/0 nelle preflight valide e incremento deterministico nel test di input invalido.

## Preflight real-engine

Protocollo: seed fisso `26083001`, 360 step, agente inerte come controparte,
esecuzione separata da P0 e P1. Il controllo richiede effetti di stato e non si
limita al conteggio degli opcode.

| Evidenza | P0 | P1 |
|---|---:|---:|
| status / step | DONE / 360 | DONE / 360 |
| player values | `[0]` | `[1]` |
| error / fallback | 0 / 0 | 0 / 0 |
| first movement effect | step 2 | step 2 |
| first PLANT surface effect | step 3 | step 3 |
| first WATER state effect | step 4 | step 4 |
| active-surface changes | 109 | 109 |
| max / final active surface | 23 / 5 | 23 / 5 |
| max quadrants / pasture / cows | 2 / 5 / 0 | 2 / 5 / 0 |
| HARVEST / SELL | 69 / 62 | 69 / 62 |
| initial / min / final cash | 3.000 / 379 / 7.895 | 3.000 / 379 / 7.895 |
| first SELL with cash gain | step 53 | step 53 |
| economic cycle observed | YES | YES |
| failures | none | none |

La differenza di MOVE/PASS fra P0 e P1 non produce differenze nello stato
produttivo o economico: entrambi verificano il binding alla propria farm. Il
livestock non si attiva (`max_cows=0`), coerentemente con il gate crop-first ma
ancora da valutare nel retournament.

## Verifiche tecniche

| Comando/check | Esito |
|---|---|
| `pytest tests/test_codex_c2_candidate.py -q` | PASS: 18 passed |
| repository `pytest -q` | PASS: 175 passed |
| Ruff sui file Python Codex | PASS |
| `git diff --check` | PASS |
| `scripts/preflight_codex_c2.py` | PASS: P0 e P1 |

## Artefatti modificati

- `docs/model/model_specs/codex/MODEL_SPEC_CODEX_C2.md`
- `configs/model_spec_c2/CODEX_C2_CONFIG.json`
- `src/agricola/strategy/codex_c2.py`
- `tests/test_codex_c2_candidate.py`
- `scripts/preflight_codex_c2.py`
- `results/model_spec_c2/remediation/CODEX_C2_PREFLIGHT.json`
- `results/model_spec_c2/codex/BUILD_VERIFICATION.md`
- `results/model_spec_c2/remediation/CODEX_C2_REMEDIATION.md`

## Freeze SHA-256

| Artefatto | SHA-256 |
|---|---|
| policy | `9D67AA44B6DAE89A2A05619A77B280E3A6D8B6ABCB8A6C67A3F3714921D2BC3A` |
| config | `7288281403E8CEBE5E0F941AD6F4A6E8A28ACDF0E5843F1F5CD27454DD4F4357` |
| MODEL_SPEC | `E664788936E3AED9A33D02D76C78AC9B35735FE0F216D4A6431D07854977DF8F` |
| candidate tests | `A5103E3C15E604A8CD5692032447D474F0FFB3DAB143C83281ED8D373B0D7EB0` |
| preflight runner | `2C3E76FF6AB46DB9D39CC778BB2A4599F96BA19DCDF2BA9DD6471B4AC098BE4C` |
| preflight evidence | `22F9F554FF76D4D00D37E989417E4CC24CE3410658B224CF6EF2368FFA81BE20` |

## Limiti residui

- La preflight a 360 step contro agente inerte non misura la competitività del
  torneo a 720 step.
- Il massimo 23 resta sotto il target nominale 25.
- MOVE rimane la classe di azione più frequente.
- I gate livestock e land sono scelte strategiche non ottimizzate.
- Nessun feedback indipendente degli altri agenti è stato letto o modificato.

```text
REMEDIATION_COMPLETE: YES
TOURNAMENT_READY: YES
```
