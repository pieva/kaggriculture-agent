# MODEL_SPEC Copilot C2 3Q — Post Foundation Review

```text
AGENT_OWNER: COPILOT
VERSION: COPILOT-C2-V2.0-3Q-HIGH-DENSITY
STATUS: IMPLEMENTED DERIVATIVE BASELINE; NOT STRATEGICALLY INDEPENDENT; NOT PROMOTED
FOUNDATION_BASELINE: C2.1 reconciled
ENGINE: kaggle-environments 1.32.7 / kaggriculture 0.1.0
ENGINE_AGGREGATE_SHA256: 4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d
```

## 1. Artefatti, source, config e freeze

| Artefatto | Percorso | SHA-256 |
|---|---|---|
| Controller V2 | `src/agricola/strategy/copilot/three_quadrant.py` | `960B146452BD6A0BE136938F22C229C0B3F3444AC519B08D6E12AF7D942F3B76` |
| Config V2 | `configs/model_spec_c2/COPILOT_C2_V2_0_3Q_HIGH_DENSITY_CONFIG.json` | `73F5292936BF53C6B33669105D0FC3381EE41E629F8E6B5D7AF8774134DA8F74` |
| Routine usata | importata da Codex | `C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4` |
| Diagnostica passiva V2 | `results/model_spec_c2/copilot/COPILOT_3Q_PASSIVE_DIAGNOSTIC.json` | `3BF3261C1F93A6CCF780A7D91026DC777400AAFC99C2D8CEE3A39A28D7E6F44F` |
| Smoke triangolare V2 | `results/model_spec_c2/copilot/COPILOT_3Q_TRIANGULAR_SMOKE_RESULTS.json` | `24D7D5E78CEB25CB31F4500402A2ECF21F2659E1BD4CD31682FB8EE15B4E81B7` |

Non esiste una freeze standalone Copilot V2 né una submission Kaggle canonica Copilot V2 autorizzata. Questa spec non ne crea una. L'hash engine è quello verificato dalla Foundation C2.1 riconciliata; gli hash sopra sono calcolati sui byte presenti nel worktree alla review.

## 2. Architettura realmente implementata

`CopilotThreeQAgent` delega a `CopilotThreeQPolicy`. La policy:

1. legge solo `observation["step"]`;
2. restituisce una deep copy di `ROUTINE_ACTIONS[step]`, importata da `agricola.strategy.codex_v9_routine_data`;
3. restituisce `PASS` fuori dai 719 step;
4. allo step 195 porta il primo ordine `BUY_PRODUCT WHEAT` a almeno 4 e rimuove gli ordini `BUY_ANIMAL COW`.

È pertanto una routine deterministica open-loop con patch locale, non un planner reattivo. `error_count` e `fallback_count` sono inizializzati ma non incrementati dal percorso attuale; non sono un ledger executed.

## 3. Q0/Q1/Q2, workforce, working set e cadenza

La config contratta dichiara `quadrants_owned=3`, `workforce_total=13`, 719 action entries e la correzione feed allo step 195. Il source V2 non possiede una mappa di tile, una definizione di working set, un planner di path o un'ownership per-Q verificabile: Q0/Q1/Q2, cadenze locali e assegnazione Farmer/Hands sono contenuti nella tabella Codex importata e non sono attribuibili a Copilot.

La dichiarazione onesta è quindi:

```text
Q0_OWNERSHIP_COPILOT_LOCAL: NOT_DEFINED
Q1_OWNERSHIP_COPILOT_LOCAL: NOT_DEFINED
Q2_OWNERSHIP_COPILOT_LOCAL: NOT_DEFINED
WORKING_SET_COPILOT_LOCAL: NOT_DEFINED
CADENCE_COPILOT_LOCAL: EXTERNAL ROUTINE ACTION INDEX
PEAK_WORKFORCE: CONFIGURED 13; NOT INDEPENDENTLY RE-ATTESTED BY A V2 EXECUTED LEDGER
```

## 4. Contratti causali Foundation consumati

Il wrapper consuma direttamente solo lo step. La routine importata presume il contratto C2.1: clock parametrico, HIRE Fibonacci al commit soltanto, nessun salario EOD, Hands da `t+1` e scadenza EOD, mercato lockstep/order/seat-sensitive, quote pre-stato distinte da fill/prezzo/delta post-stato, e vincoli FEED/EOD.

Il wrapper non verifica questi predicati su osservazione e non consuma online `POST-44..57`. Ogni risultato post-stato deve restare review-only; non è lecito promuovere il valore quotato a fill garantito.

## 5. Contratto osservativo e deliberazione agent-local

```text
SHARED_OBSERVATION_CONTRACT: src/agricola/core/observation_contract.py
SHARED_DELIBERATION_RUNTIME: NONE
```

Clock, snapshot, adapter e hashing sono disponibili nel contratto osservativo
neutrale. V2 non usa una deliberazione condivisa: routine, priorità e patch
restano agent-local e nessun elemento della policy Copilot entra nella
Foundation.

## 6. Risultati disponibili e loro limite

| Classe | Evidenza | Risultato | Stato |
|---|---|---:|---|
| Passiva | 8 seat-run, seed 26090101/2/3/562040596 | mean `$66,285.50`, min `$48,959`, max `$76,616`, 0 escapes | diagnostica disponibile, non freeze canonica |
| Holdout | nessun manifesto V2 dedicato | — | non disponibile |
| Mirror | nessun run V2 dedicato | — | non disponibile |
| Torneo | smoke triangolare, un solo seed, 6 match | Copilot 3–1, mean `$29,734.25` | non canonico e non attribuibile come indipendente |

Il test mirato corrente passa `3 passed`, inclusi il prefisso reale a 72 step e la patch step 195. Non dimostra equilibrio competitivo, fill executed, risultati 720-step o indipendenza.

## 7. Punti di forza, failure modes e target

**Punti di forza:** interfaccia Kaggle-compatible, deep copy che evita mutazione della tabella importata, fallback `PASS` oltre orizzonte, e correzione feed esplicita.

**Failure modes:** dipendenza completa dalla routine Codex, temporalità rigida, nessuna reattività dichiarata a weeds/fill/desync, assenza di ledger requested/executed, e cannibalizzazione di mercato possibile. Il singolo smoke non è un benchmark.

I target di una futura candidata **indipendente** (non E17 avviato qui) sono: `ANIMAL_ESCAPES=0`, ledger executed di mercato 100%, canonical+holdout seat-balanced preregistrati, mirror dedicato, e nessuna importazione/copia/hash della routine altrui.

## 8. Provenance e gate di indipendenza

```text
ROUTINE_ORIGIN: CODEX V9 routine data
PARENT_ROUTINE_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
BEHAVIORAL_DELTA: step 195 WHEAT minimum 4; remove COW purchase
INDEPENDENCE_STATUS: DERIVATIVE_IMPLEMENTATION
NO_IMPORT_OTHER_AGENT_ROUTINE: FAIL
NO_COPY_OTHER_AGENT_ACTION_TABLE: FAIL
NO_IDENTICAL_ROUTINE_SHA: FAIL
NO_THIN_WRAPPER_AS_MODEL: FAIL
PROVENANCE_DISCLOSURE: PASS
STRATEGIC_INDEPENDENCE_GATE: FAIL
```

Directly importing `ROUTINE_ACTIONS` and `ROUTINE_SHA256` is dispositive. V2 may serve as a transparently labelled derivative baseline/replica only; it cannot be counted as Copilot's independent strategy or comparative merit.

## 9. Chiusura Foundation e pulizia

La riconciliazione finale del 2026-09-01 ha accettato questa disclosure come baseline derivativa e ha reso C2.1 il riferimento attivo:

```text
ONTOLOGY_C2_1: RECONCILED
STATE_MACHINE_C2_1: RECONCILED
FEATURE_MODEL_C2_1: RECONCILED
POST_3Q_FOUNDATION_PHASE: COMPLETE
```

Le versioni Copilot C2 precedenti, il candidato V1 central-cluster e i relativi manifest/report di build e torneo sono stati rimossi. Restano solo questa spec, il controller/config V2 e le due evidenze V2 necessarie a riprodurre la baseline derivativa. La Foundation C2, le candidate di review C2.1 e gli artefatti degli altri owner restano invariati per audit.

## 10. Canonical Kaggle production authority

No existing Copilot builder or test is authorized to generate or overwrite a canonical Kaggle file for V2. `submission/submission_codex.py` and its builder are not Copilot-owned and must not be used as a Copilot output path. Any future authorized Copilot builder must write an explicit Copilot-only noncanonical output first, verify source/config/output SHA-256 and isolation, then receive separate promotion authority.
