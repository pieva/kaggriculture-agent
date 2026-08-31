# Codex V7.1 Serviceability — Report finale

## 1. Esito

Lo sviluppo ha raggiunto e superato l'obiettivo economico concordato.

La versione `CODEX-C2-COMPACT-Q0-ROUTINE-V7.1-SERVICEABILITY` ottiene una media di **61.118,83** sui sei replay canonici, contro il requisito minimo di 50.000. Anche il risultato peggiore, **57.859**, supera la soglia. Le fughe animali scendono da 24 complessive a **zero**.

Il risultato è ottenuto senza regressione della componente agricola: la produzione media MELON + STRAWBERRY passa da 135,17 a 139,83 unità e il ricavo colturale medio cresce da 29.786,67 a 30.561,17.

## 2. Perimetro dello sviluppo

L'intervento è stato limitato alla serviceability del bestiame. Non sono stati modificati:

- footprint Q0 e posizioni produttive;
- piano colturale 9 MELON / 8 STRAWBERRY / 1 WHEAT;
- coorti di semina;
- proprietà delle tre zone colturali;
- gestione delle urgenze WATER e dell'assistenza cross-zone;
- contratto Foundation o motore Kaggriculture.

Non sono stati eseguiti torneo, upload/esecuzione Kaggle o push. La submission
standalone viene salvata nel commit locale richiesto successivamente
dall'utente.

## 3. Correzioni implementate

### 3.1 SERVICEABLE_BOOTSTRAP_BINDING

I ruoli W4/W5 rimangono i proprietari ordinari dei cluster COW e SHEEP. Quando i temporary hands sono scaduti e questi indici non esistono, viene creato un binding di emergenza:

- il farmer/FLOAT assume il cluster COW;
- il primo hand disponibile assume il cluster SHEEP;
- se il farmer è solo, assume entrambi i cluster.

Il binding riguarda esclusivamente il servizio animale e non modifica in modo permanente la mappa dei ruoli.

### 3.2 INVENTORY_AWARE_FEED_DISPATCH

FEED non è più trattato come un semplice target remoto. Il worker assegnato può:

1. alimentare l'animale se trasporta già WHEAT; oppure
2. eseguire prima un commitment `SHED → PICKUP WHEAT`, dimensionato sull'intero insieme di animali dovuti, e successivamente consegnare il mangime.

I ruoli non proprietari non ricevono più target FEED globali non eseguibili. La verifica della capacità avviene quindi prima del movimento, non soltanto quando il worker raggiunge l'animale.

### 3.3 FEED_FIRST_CLUSTER_BATCHING

Il servizio FEED viene valutato prima dello scarico di prodotti e fertilizzante. Il worker preleva in una sola operazione il WHEAT necessario al proprio cluster e chiude il relativo insieme di feed prima di tornare alle attività secondarie.

Quando il roster completo è disponibile, la raccolta ordinaria del fertilizzante viene lasciata al ruolo FERTILIZER_LOGISTICS, evitando che i due specialisti livestock abbandonino il cluster per quel compito.

## 4. Protocollo di verifica

Sono stati utilizzati gli stessi parametri della baseline V7:

- seed: 26090101, 26090102 e 26090103;
- entrambi i seat per ciascun seed;
- avversario: `INERT_PASS_POLICY`;
- 720 step, 24 turni al giorno;
- sei episodi deterministici complessivi;
- nessun adattamento tra un episodio e l'altro.

Prima del benchmark economico è stata eseguita la verifica tecnica con build della submission standalone. Dopo il benchmark è stata eseguita l'intera suite del repository.

Esito verifiche:

| Verifica | Esito |
|---|---:|
| Technical smoke | PASS |
| Errori/fallback dell'agente | 0 |
| Test mirati serviceability | PASS |
| Suite completa | 185 PASS |
| Lint sui file modificati | PASS |

È comparso soltanto un warning non funzionale: pytest non ha potuto aggiornare la propria cache locale per permessi. Nessun test è stato saltato o fallito per questo motivo.

## 5. Risultati per episodio

| Seed | Seat | Final money | MILK | WOOL | MELON | STRAWBERRY | Fughe |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 26090101 | 0 | 64.752 | 90 | 60 | 108 | 36 | 0 |
| 26090101 | 1 | 59.222 | 90 | 60 | 102 | 37 | 0 |
| 26090102 | 0 | 63.377 | 90 | 60 | 102 | 37 | 0 |
| 26090102 | 1 | 63.377 | 90 | 60 | 102 | 37 | 0 |
| 26090103 | 0 | 57.859 | 90 | 60 | 102 | 37 | 0 |
| 26090103 | 1 | 58.126 | 90 | 60 | 102 | 37 | 0 |

Statistiche economiche:

| Metrica | Valore |
|---|---:|
| Media | **61.118,83** |
| Mediana | 61.299,50 |
| Minimo | **57.859,00** |
| Massimo | 64.752,00 |
| Deviazione standard | 2.786,28 |
| Episodi sopra 50.000 | **6/6** |

## 6. Confronto con V7

| Metrica media | V7 | V7.1 | Delta |
|---|---:|---:|---:|
| Final money | 39.265,67 | **61.118,83** | **+21.853,17 / +55,65%** |
| MILK | 28,17 | **90,00** | +61,83 |
| WOOL | 14,67 | **60,00** | +45,33 |
| MELON | 95,00 | **103,00** | +8,00 |
| STRAWBERRY | 40,17 | 36,83 | -3,33 |
| Colture totali | 135,17 | **139,83** | +4,67 |
| Ricavo colturale | 29.786,67 | **30.561,17** | +774,50 |
| Ricavo livestock | 10.664,83 | **35.288,00** | +24.623,17 |
| Fughe complessive | 24 | **0** | -24 |
| Hard deadline miss complessivi | 50 | **29** | -21 |
| Azioni produttive | 688,17 | **858,00** | +169,83 |
| MOVE | 2.196,83 | 2.601,33 | +404,50 |
| MOVE / azione produttiva | 3,1923 | **3,0321** | -5,02% |

I MOVE assoluti aumentano perché gli animali restano vivi per l'intero episodio e generano molte più operazioni di feed, care e raccolta. L'aumento non rappresenta una regressione equivalente: le azioni produttive crescono più rapidamente e il rapporto MOVE/produttiva migliora del 5,02%.

La riduzione della raccolta fertilizzante da 80,83 a 59,83 unità è compensata da un'applicazione più efficace: FERTILIZE cresce da 20,17 a 31,83 azioni medie. Il ricavo colturale conferma che il cambio di ownership non ha danneggiato l'economia agricola.

## 7. Verifica dei gate

| Gate | Soglia | Risultato | Stato |
|---|---:|---:|---:|
| Final money medio | ≥50.000 | 61.118,83 | PASS |
| Final money minimo per episodio | ≥50.000 desiderabile | 57.859,00 | PASS |
| Fughe | 0 | 0 | PASS |
| MILK | ≥80 | 90 | PASS |
| WOOL | ≥62 come target ideale precedente | 60 | NON RAGGIUNTO |
| Colture totali | ≥128,4 | 139,83 | PASS |
| Technical pass | obbligatorio | true | PASS |

Il gate economico concordato è raggiunto con margine e in tutti gli episodi. Il solo obiettivo ideale non raggiunto è WOOL 62; lo scarto è di 2 unità e non impedisce il superamento del requisito economico. Non è stato introdotto un ulteriore ciclo di tuning perché avrebbe ampliato lo sviluppo dopo il raggiungimento dell'obiettivo autorizzato.

## 8. Artefatti prodotti

- `src/agricola/strategy/codex_compact_q0.py`: controller V7.1;
- `configs/model_spec_c2/CODEX_C2_CONFIG.json`: binding alla nuova versione;
- `submission/submission_codex.py`: standalone rigenerata;
- `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_TECHNICAL_SMOKE.json`;
- `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_RESULTS.csv`;
- `results/model_spec_c2/codex/CODEX_V7_1_SERVICEABILITY_RESULTS.json`.

Gli harness di verifica e benchmark sono stati aggiornati per scrivere artefatti V7.1 separati, preservando i risultati canonici V7 utilizzati come baseline.

## 9. Limiti dell'evidenza

Il risultato dimostra il raggiungimento della soglia nel protocollo locale preregistrato contro `INERT_PASS_POLICY`. Non costituisce una previsione garantita di rendimento in un torneo competitivo o su Kaggle.

Il confronto economico è causale rispetto alla baseline locale perché seed, seat, durata e avversario sono invariati. Non misura la robustezza contro interferenza avversaria, prezzi o configurazioni differenti.

## 10. Conclusione

La diagnosi forense è confermata: il principale limite V7 era la mancata serviceability del feed, non la strategia colturale. Le tre correzioni minime eliminano tutte le fughe, mantengono il bestiame produttivo e portano il risultato medio oltre 61.000 senza sacrificare il comparto crop.

```text
OBJECTIVE_MIN_FINAL_MONEY: 50000
FINAL_MONEY_MEAN: 61118.83
FINAL_MONEY_MIN: 57859.00
ALL_EPISODES_ABOVE_50000: YES
ANIMAL_ESCAPES_TOTAL: 0
MILK_MEAN: 90
WOOL_MEAN: 60
CROP_OUTPUT_PRESERVED: YES
TECHNICAL_PASS: YES
FULL_TEST_SUITE: 185 PASS
OBJECTIVE_REACHED: YES
KAGGLE_SUBMISSION_FILE: submission/submission_codex.py
NEXT_RECOMMENDED_STEP: FREEZE_V7_1_CANDIDATE_AND_REQUEST_SEPARATE_TOURNAMENT_AUTHORIZATION
TOURNAMENT_EXECUTED: NO
KAGGLE_EXECUTED: NO
COMMIT_EXECUTED: YES
PUSH_EXECUTED: NO
```
