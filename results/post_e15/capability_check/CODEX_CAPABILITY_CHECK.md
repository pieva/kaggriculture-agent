# POST-E15 Model Capability Check

## 1. Provenance

- **METHODOLOGICAL FRAME:** [README.md](C:/Users/pietr/Projects/kaggriculture-agent/README.md), [ontologia frozen](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/freeze/ONTOLOGY_E15_FROZEN.md).
- **FROZEN DECLARATIONS:** [freeze manifest](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/freeze/FREEZE_MANIFEST.md) e MODEL_SPEC/submission frozen. I sette SHA256 corrispondono integralmente al manifest.
- **PRIMARY E15 EVIDENCE:** `summary.json`, `telemetry.json` e `raw_replay.json` di [M1](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/M1_antigravity_vs_codex/raw_replay.json), [M2](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/M2_codex_vs_copilot/raw_replay.json), [M3](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/M3_copilot_vs_antigravity/raw_replay.json).
- **POST-E15 INTERPRETATION:** analisi neutrali, consensus e [sintesi finale](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/E15_FINAL_TOURNAMENT_SYNTHESIS.md).
- **YOUR INFERENCE:** classificazioni e candidate bounds riportati sotto.

## 2. Evidence Reconstruction

E15 è un round-robin pairwise frozen di tre match, 720 step ciascuno, con seed distinti e ogni agente una volta P0 e una volta P1.

| Match | Seed | Final money | WATER richieste | Max crop osservate | Pasture / animali max | Hands max |
|---|---:|---:|---:|---:|---:|---:|
| M1 | 1113294977 | Antigravity 8,672; Codex 20,461 | 34; 439 | 8; 28 | 18/18; 9/7 | 12; 10 |
| M2 | 3033283457 | Codex 27,510; Copilot 37,752 | 475; 446 | 37; 28 | 9/7; 5/4 | 10; 10 |
| M3 | 3122977751 | Copilot 26,629; Antigravity 9,371 | 439; 30 | 25; 9 | 5/4; 18/18 | 9; 12 |

La ricostruzione indipendente dai replay produce inoltre questo proxy: media, nei giorni 0-27 con colture attive, della frazione di crop che a fine giornata risultano `watered_today`.

| Policy-match | Frazione media |
|---|---:|
| Antigravity M1 | 0.082 |
| Antigravity M3 | 0.144 |
| Codex M1 | 0.711 |
| Codex M2 | 0.733 |
| Copilot M2 | 0.752 |
| Copilot M3 | 0.739 |

Questa è una **YOUR INFERENCE derivata dal replay**, non una metrica E15 predefinita.

Antigravity replica su due seed una firma molto stabile: 3 quadranti, 12 hands, 18 pasture, 18 animali max, solo 8-9 crop max, 30-34 WATER richieste e rapporto HARVEST/PLANT 3.74-4.45. Codex e Copilot mostrano invece 25-37 crop max, 439-475 WATER e HARVEST/PLANT 0.72-0.98.

M2 impedisce però una lettura monotona: Codex ha più crop, più WATER e una quota produttiva grezza maggiore di Copilot, ma final money inferiore.

### Requested versus executed

`telemetry.market_orders` e le quantità nelle azioni del replay sono **richieste**, non un ledger di transazioni eseguite. Non sono disponibili quantità eseguite, valore transato, motivo di rifiuto o P/L per commodity. Anche i conteggi worker rappresentano azioni emesse: senza action-effect ledger non è dimostrato che ogni `HARVEST`, `WATER` o `SELL` abbia prodotto l’effetto previsto.

C’è inoltre una discrepanza documentale: la sintesi finale riporta 9 hands Copilot in M2 e M3, mentre il replay primario M2 e l’[analisi neutrale M2](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/M2_codex_vs_copilot/E15_M2_NEUTRAL_FORENSIC_ANALYSIS.md) mostrano 10 in M2. Prevale il replay.

## 3. Layer Diagnosis

| Agente | MODEL_VALIDITY | POLICY_REALIZATION | IMPLEMENTATION_FIDELITY |
|---|---|---|---|
| Antigravity | `PARTIALLY_SUPPORTED` | `STRONGLY_WEAKENED` | `STRONGLY_WEAKENED` |
| Codex | `PARTIALLY_SUPPORTED` | `PARTIALLY_SUPPORTED` | `PARTIALLY_SUPPORTED` |
| Copilot | `PARTIALLY_SUPPORTED` | `SUBSTANTIALLY_SUPPORTED`, non completo | `PARTIALLY_SUPPORTED` |

**MODEL_VALIDITY.** E15 supporta come candidate feature watering, crop maintenance, dispatch effectiveness e capacità allineata. Indebolisce target monotoni o rigidi di land, workforce, herd e productive-action share. Non isola causalmente nessuna singola componente.

**POLICY_REALIZATION.** Copilot realizza stabilmente un working set compatto; Codex realizza watering e crop activation ma in M2 converte peggio un working set più grande. Antigravity realizza una policy opposta alle priorità dichiarate: scala livestock e territorio mentre la crop engine resta piccola.

**IMPLEMENTATION_FIDELITY.** Tutte le submission completano 720 step senza timeout e producono fingerprint ripetibili. Tuttavia, nel [codice Antigravity frozen](C:/Users/pietr/Projects/kaggriculture-agent/results/e15/freeze/submission_antigravity_E15_FROZEN.py:599), il WATER “emergency” viene dopo harvest, feed e care livestock; il WATER generale viene persino dopo DIG. Questo contraddice il rank #1 dichiarato. Nel codice Copilot, il gate dinamico modifica soprattutto i target animali e delega alla policy X112; land e workforce restano in larga parte calendar-based. Inoltre `max_hands=6` del wrapper non limita `_x112_desired_hands`, e M2 raggiunge 10.

## 4. Feature Analysis

```text
concept_id: watering_execution_rate
feature_status: FEATURE
relationship: positive, thresholded, conditional
e15_evidence: 30-34 richieste e proxy EOD 0.082-0.144 nei due Antigravity; 439-475 e 0.711-0.752 nelle altre quattro osservazioni.
failure_region: 30-34 richieste; mean EOD watered fraction 0.082-0.144.
success_region: 439-475 richieste; mean EOD watered fraction 0.711-0.752.
candidate_threshold_or_interval: transizione non osservata fra 0.144 e 0.711; non è un optimum.
confidence: medium; replica forte ma confusa con dispatch, crop surface e livestock.
confounders: crop count, distanza, workforce, priorità FEED/CARE/HARVEST, azioni WATER fallite.
next_test_values: mean daily serviced fraction 0.15, 0.30, 0.45, 0.60, 0.72.
falsification_condition: a working set controllato, valori bassi producono maintained surface e final money equivalenti ai valori alti su più seed.
```

```text
concept_id: watering_continuity
feature_status: FEATURE
relationship: positive, thresholded
e15_evidence: Antigravity raggiunge una frazione EOD >=0.5 in 2/24 giorni produttivi; Codex/Copilot in 23-24/28.
failure_region: continuità >=0.5 limitata a 2 giorni produttivi.
success_region: continuità >=0.5 in 23-24 giorni produttivi.
candidate_threshold_or_interval: intervallo tra 2/24 e 23/28 non discriminato.
confidence: medium.
confounders: endgame shutdown, sostituzione delle crop, raccolta precedente allo snapshot EOD.
next_test_values: 25%, 50%, 75%, 90% dei giorni produttivi con serviced fraction >=0.5.
falsification_condition: interrompere la continuità non riduce persistenza delle crop o final money a parità di volume WATER.
```

```text
concept_id: crop_surface_maintained
feature_status: FEATURE
relationship: thresholded, non_monotonic, conditional
e15_evidence: failure Antigravity con 8-9 crop max; altre policy 25-37. In M2, 28 crop battono 37.
failure_region: max active-crop proxy 8-9.
success_region: max active-crop proxy 25-37, senza ordinamento monotono interno.
candidate_threshold_or_interval: regione 10-24 non osservata; active crop non equivale ancora a maintained surface formalmente definita.
confidence: medium.
confounders: watering, crop mix, horizon, routing, pasture footprint e sell-through.
next_test_values: cap 9, 13, 17, 21, 25 con watering e herd controllati.
falsification_condition: 9 crop ben mantenute e monetizzate eguagliano stabilmente 25, oppure 25 non migliorano la pipeline rispetto a 9.
```

```text
concept_id: land_surface_total
feature_status: UNRESOLVED
relationship: conditional, unresolved
e15_evidence: le due osservazioni a 3Q perdono; tutte le policy a 2Q ottengono final money maggiore.
failure_region: 3Q insieme a 8-9 crop, 18 pasture e forte stress di cassa.
success_region: 2Q insieme a 25-37 crop e herd 4-7.
candidate_threshold_or_interval: nessuna soglia land isolabile; E15 falsifica soltanto “più land è sempre meglio”.
confidence: low.
confounders: timing, activation, pasture, workforce, cash e differente implementazione.
next_test_values: 2Q e 3Q con identici crop cap, herd, workforce e land-activation schedule.
falsification_condition: 3Q attivato in modo controllato produce un vantaggio ripetibile, oppure 2Q resta superiore anche con activation e cash equivalenti.
```

```text
concept_id: pasture_arable_surface_tradeoff
feature_status: FEATURE
relationship: negative above capacity, conditional
e15_evidence: 18 pasture coesistono con 8-9 crop e basso final money; 5-9 pasture con 25-37 crop e final money maggiore.
failure_region: 18 pasture nel bundle Antigravity.
success_region: 5-9 pasture nei bundle Codex/Copilot.
candidate_threshold_or_interval: intervallo 9-18 non osservato; non prova che 5 sia ottimale.
confidence: medium-low.
confounders: livestock count, land totale, workload FEED/CARE e crop mix.
next_test_values: pasture 5, 9, 13, 18 a herd e land costanti.
falsification_condition: pasture aggiuntive senza animali riducono poco il target, oppure maggiore pasture produce output monetizzato sufficiente a compensare la superficie sottratta.
```

```text
concept_id: livestock_headcount
feature_status: FEATURE
relationship: non_monotonic, thresholded, conditional
e15_evidence: max 18/finale 17 nelle due failure; max 4-7 nelle policy con final money maggiore.
failure_region: 17-18 animali osservati insieme a 18 pasture.
success_region: 4-7 animali osservati.
candidate_threshold_or_interval: transizione 7-17 non osservata; 4 non è un optimum.
confidence: medium-low.
confounders: pasture footprint, feed, specie, workforce, cash e crop opportunity cost.
next_test_values: 4, 7, 10, 13, 17.
falsification_condition: herd 13-17, con feed/pasture/crop capacity controllate, eguaglia o supera stabilmente herd 4-7.
```

```text
concept_id: workforce_headcount
feature_status: UNRESOLVED
relationship: conditional, non_monotonic
e15_evidence: 12 hands nelle due failure; 9-10 nelle altre policy; M2 ha 10 per entrambi ma outcome differente.
failure_region: 12 nel bundle Antigravity.
success_region: 9-10, ma headcount non discrimina M2.
candidate_threshold_or_interval: possibile transizione 10-12, non causalmente attribuibile.
confidence: low.
confounders: workload, routing, wages, contract timing e action-order effectiveness.
next_test_values: 9, 10, 11, 12 a working set fisso.
falsification_condition: il marginale 10->12 aumenta final money con la stessa efficacia per action e senza alterare altri fattori.
```

```text
concept_id: action_dispatch_failure
feature_status: FEATURE
relationship: negative, thresholded
e15_evidence: proxy HARVEST/PLANT 3.74-4.45 nelle failure; 0.72-0.98 nelle altre quattro osservazioni.
failure_region: HARVEST/PLANT >=3.74 con solo 8-9 crop max.
success_region: HARVEST/PLANT <=0.98.
candidate_threshold_or_interval: intervallo 0.98-3.74 non osservato; il ratio non dimostra che ogni HARVEST fallisca.
confidence: medium.
confounders: raccolti ripetibili, yield disponibile, distanza e inventario pieno.
next_test_values: retry/effectiveness policy che produca ratio circa 1.0, 1.7, 2.5, 3.7.
falsification_condition: l’action-effect ledger mostra che i HARVEST elevati sono quasi tutti efficaci o che ridurli non libera crop-care capacity.
```

```text
concept_id: productive_action_share
feature_status: NOT_FEATURE
relationship: unresolved
e15_evidence: in M2 Codex ha share grezza 18.35% contro 17.24% Copilot ma perde.
failure_region: non separabile dalla success region con la formula grezza corrente.
success_region: non separabile.
candidate_threshold_or_interval: nessuna soglia sostenuta.
confidence: medium per il rigetto della formulazione grezza, non del concetto di effectiveness.
confounders: composizione delle azioni, valore dei prodotti e azioni richieste ma fallite.
next_test_values: due policy con share 0.17 e 0.19 ma identica composizione/effectiveness.
falsification_condition: la share grezza predice final money su più seed dopo aver controllato composizione e valore.
```

```text
concept_id: operating_cash_buffer
feature_status: FEATURE
relationship: thresholded, conditional, non_monotonic
e15_evidence: min cash 19-25 nelle failure; 87-331 nelle altre policy. Copilot opera però con meno cash di Codex nei giorni 4-9 e vince M2.
failure_region: minimo episodico 19-25 e centinaia di step sotto 250.
success_region: minimo 87-331; non esiste evidenza che buffer più alto sia sempre migliore.
candidate_threshold_or_interval: transizione osservativamente aperta fra 25 e 87.
confidence: medium-low.
confounders: investimento intenzionale, obblighi futuri, timing dei ricavi e prezzi condivisi.
next_test_values: floor di policy 25, 50, 87, 150.
falsification_condition: floor molto basso non aumenta stall/failure oppure floor alto non sacrifica opportunità redditizie.
```

```text
concept_id: state_capacity_alignment
feature_status: UNRESOLVED
relationship: conditional
e15_evidence: il bundle 2Q/25-37 crop/4-7 animali/9-10 hands supera 3Q/8-9 crop/18 animali/12 hands.
failure_region: bundle Antigravity replicato.
success_region: bundle Codex/Copilot.
candidate_threshold_or_interval: nessuna soglia scalare; l’ontologia richiede formula, sotto-metriche e pesi che E15 non definisce.
confidence: medium sulla presenza dell’interazione, low sulla sua misurazione.
confounders: tutti i componenti del bundle e target leakage se la formula incorpora final money.
next_test_values: fattoriale watering fraction 0.15/0.72 x livestock bundle compatto/grande, più punto centrale.
falsification_condition: le singole componenti spiegano interamente l’outcome e una metrica composita non aggiunge capacità discriminante.
```

```text
concept_id: inventory_to_cash_conversion
feature_status: UNRESOLVED
relationship: positive, unresolved
e15_evidence: SELL-order requests 198 nelle due failure, contro 212-302 nelle altre policy; final cash segue la stessa direzione grossolana.
failure_region: 198 richieste, ma esecuzione e valore ignoti.
success_region: 212-302 richieste, non equivalenti a revenue.
candidate_threshold_or_interval: nessuno senza executed transaction-value ledger.
confidence: low.
confounders: quantità per ordine, prezzo, rifiuti, Wheat churn, prodotto e inventory iniziale.
next_test_values: sell cadence 1, 4 e 8 ordini per turno con identica quantità disponibile.
falsification_condition: il ledger eseguito mostra conversione/value equivalenti nonostante le differenti richieste.
```

```text
concept_id: feed_market_dependency
feature_status: UNRESOLVED
relationship: unresolved, possibly non_monotonic
e15_evidence: i winner richiedono spesso più BUY_PRODUCT Wheat: 1483 vs 1007 in M1, 1828 vs 1334 in M2, 1889 vs 904 in M3.
failure_region: non identificabile da richieste.
success_region: alta dipendenza richiesta coesiste con vittorie, ma non prova esecuzione o profitto.
candidate_threshold_or_interval: nessuno.
confidence: low.
confounders: Wheat rivenduto, feed consumato, prezzi dinamici, quantità eseguite e shared market.
next_test_values: dependency ratio 0.25, 0.50, 0.75 a herd e Wheat flow controllati.
falsification_condition: executed ledger mostra costo netto monotonicamente negativo e replicato della maggiore dipendenza.
```

## 5. Confounder Analysis

| Confounder | Feature collegate | Falsa interpretazione possibile | Osservabilità mancante | Separazione sperimentale |
|---|---|---|---|---|
| Irrigation-working set | WATER, crop surface, dispatch | “Più WATER causa direttamente più money” | action success e daily need denominator | Variare serviced fraction a crop cap fisso |
| Livestock bundle | animali, pasture, feed, crop, workforce | “17 animali sono dannosi” | ROI e workload marginale per animale | Herd variabile con pasture fisse, poi pasture variabili con herd fisso |
| Expansion bundle | land, cash, workforce, herd | “Q2 causa il fallimento” | purchase-to-activation e payback lag | 2Q/3Q con stesso working set e stesso capitale residuo |
| Action counts | movement, harvest, productive share | “MOVE/HARVEST sono spreco” | effetto per azione e transito necessario | Action-effect ledger e ablation dei retry |
| Market requests | conversion, feed dependency, churn | “Più SELL significa più revenue” | quantità e valore eseguiti, rejection reason | Executed transaction ledger per ordine |
| Seed/opponent market | tutte le feature economiche | “Fingerprint = effetto universale” | repliche sugli stessi seed e opponent | Celle paired sugli stessi training seed contro benchmark frozen |
| Derived metrics | alignment, monetization rate | “Il proxy dimostra causalità” | formula predefinita e input non target-derived | Pre-registrare formula prima dei replay |

## 6. Candidate Design for the Next Common Training Round

```text
training_or_validation: TRAINING
hypothesis: esiste un’interazione fra crop watering sufficiente e scala livestock/pasture; sotto la soglia di irrigazione la scala amplifica il failure, mentre sopra soglia il rendimento della scala può essere stimato separatamente.
feature_under_test: mean daily watered-crop fraction x livestock_headcount/pasture footprint.
controlled_variables: una sola implementazione comune; 2Q; active-crop target 25; workforce 10; crop mix, routing, land timing, cash gate, endgame e benchmark opponent frozen; stessi tre seed pre-dichiarati.
test_values: sei celle: (0.15,4 animali,5 pasture), (0.15,17,18), (0.72,4,5), (0.72,17,18), centro (0.44,10,12), sentinel pasture-only (0.72,4,18).
expected_discrimination: i quattro corner stimano effetti principali e interazione; il centro rileva threshold/curvatura; il sentinel separa costo pasture da costo animale a watering alto.
falsification_condition: watering alto non migliora maintained surface/final money in entrambi i regimi di scala, oppure il bundle grande non cambia outcome una volta controllato watering e pasture.
evidence_that_must_be_recorded: requested ed executed actions; success/failure reason; daily active/watered crop denominator; executed transaction quantity/value/price/rejection; cash-flow category; herd/pasture/feed state; worker inventory; movement necessario; purchase-to-activation lag; terminal inventory; final_money.
```

Sono sei configurazioni per tre seed comuni, quindi 18 episodi di training. Non costituiscono validation: ogni risultato usato per restringere gli intervalli resta training evidence.

## 7. Epistemic Audit

### SUPPORTED

- Gli outcome finali e l’integrità frozen sono osservati.
- Antigravity replica una specifica failure signature su due seed e due avversari.
- Watering estremamente basso e working crop surface piccola co-occorrono con i due outcome più bassi.
- Oltre quel regime, più WATER, più crop o maggiore productive-action share non implicano monotonicamente più final money.
- Requested market orders non equivalgono a executed transactions.

### PROVISIONAL

- Esistenza di un regime sotto soglia irrigation/maintenance e di un regime sopra soglia.
- Candidate gaps: watered fraction 0.144-0.711, max crop 9-25, herd 7-17, min cash 25-87.
- Interazione fra crop capacity, herd/pasture, workforce e capitale.
- HARVEST/PLANT elevato come proxy di dispatch failure.

### UNRESOLVED

- Soglie e parametri ottimali.
- Effetto causale indipendente di land, workforce, herd, pasture o watering.
- Redditività di Wheat flow, feed dependency, churn e SELL cadence.
- Formula valida di `state_capacity_alignment`.
- Generalizzazione multi-seed, Kaggle fidelity e validation indipendente.
- Exact action/transaction execution fidelity per tutti gli ordini.

### DO_NOT_INFER

- Copilot possiede il modello universalmente corretto.
- 4 animali, 5 pasture, 9-10 hands o 2Q sono ottimali.
- Q2 è intrinsecamente negativo.
- Sheep sono inferiori alle Cow.
- Più richieste SELL o BUY_PRODUCT implicano più revenue o più spesa.
- Final money/action è una prova causale di efficienza.
- E15 può essere riutilizzato come validation o test evidence.
