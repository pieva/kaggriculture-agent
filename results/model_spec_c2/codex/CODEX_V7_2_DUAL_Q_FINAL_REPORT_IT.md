# KAGGRICULTURE C2 — Report finale Codex V7.2 Dual-Q

## Esito

La candidata isolata `CODEX-C2-V7.2-DUAL-Q0-Q1` raggiunge il target economico richiesto: **77.418,50** di `FINAL_MONEY` medio sui sei replay canonici, contro 61.118,83 della V7.1. Il delta integrato è **+16.299,67 (+26,67%)**; il minimo è 70.799 e nessun episodio registra fughe, errori o fallback.

Il gate minimo è superato integralmente. Il target centrale economico di 75.000 è superato, così come i target di produzione crop, conservazione Q0, contributo Q1 e serviceability. Il gate centrale esteso non è però integralmente chiuso: latte e lana medi sono rispettivamente 134,83/145 e 90,83/100. La versione è quindi una baseline Dual-Q economicamente valida, non ancora un freeze biologico definitivo.

## Architettura realizzata

- Q0 conserva la geometria V7.1: 18 crop, 3 bovini, 3 ovini, 6 pascoli e 6 worker operativi.
- Q1 è un'immagine speculare orizzontale di Q0: 18 crop, 3 bovini, 3 ovini, 6 pascoli e 6 worker operativi dedicati.
- Il farmer resta condiviso per relief/logistics; la forza lavoro a regime è di 13 unità complessive.
- I proprietari di zone crop, cluster bovini, cluster ovini e fertilizer/logistics sono separati per quadrante.
- I fallback incompleti sono locali al modulo; l'assistenza crop ordinaria non attraversa il confine Q0/Q1.
- Q1 usa coorti relative al giorno reale di attivazione, non un calendario assoluto anticipato.
- La candidata, la configurazione, il benchmark e i risultati sono separati dagli artefatti V7.1.

Per rendere l'estensione possibile senza duplicare il controller, la V7.1 è stata rifattorizzata in modo behavior-preserving: geometria, piano colturale, route index, target workforce e riconoscimento dei ruoli fertilizer sono ora proprietà/extension point dell'istanza. I replay e i test V7.1 confermano che il comportamento Q0 resta invariato entro i gate.

## Attivazione e ledger economico

La configurazione finale usa una soglia di ammissione Q1 pari a 2.800, con finestra D6–D10 e buffer operativo. Il planner vende prima gli output disponibili, inserisce `BUY_LAND` prima degli hire e rispetta il limite di dieci ordini market per turno.

Costi strutturali dell'espansione:

| Voce | Costo/volume |
|---|---:|
| Terra Q1 | 1.000 una tantum |
| 3 bovini Q1 | 1.200 |
| 3 ovini Q1 | 1.500 |
| Prima dotazione seed Q1 (9 MELON, 8 STRAWBERRY, 1 WHEAT) | 1.530 |
| 12 hire giornalieri a regime | 376/giorno |
| 6 hire Q0 | 20/giorno |
| Costo marginale dei 6 hire Q1 | 356/giorno |
| WHEAT consumato, media V7.2 | 272 |
| WHEAT consumato, media V7.1 | 164 |
| Incremento WHEAT osservato | +108 |

Il costo seed riportato è quello della prima occupazione del footprint; reimpianti e feed seguono i prezzi e le quantità reali del replay. Il delta di `FINAL_MONEY` è già al netto di terra, animali, seed, WHEAT e hire effettivamente eseguiti dall'engine. Per questo **+16.299,67** è usato come contributo netto integrato di Q1. Non è una stima controfattuale pura del solo quadrante: include anche interazioni di prezzo, capacità condivisa e piccole variazioni di output Q0.

## Iterazione causale

Sono stati usati due cicli, sotto il limite massimo di tre.

### Ciclo 1 — soglia 4.200

Risultati per episodio: 81.331, 62.225, 74.730, 73.849, 69.774, 68.462.

- media: 71.728,50;
- minimo: 62.225;
- attivazione Q1: D9 in tutti i run;
- modulo Q1 completo: D12,33 medio;
- fughe: 0;
- diagnosi: la soglia di capitale ritardava di un giorno terra, workforce e prima coorte, comprimendo il payback nel caso peggiore.

### Ciclo 2 — soglia 2.800

È stata modificata una sola leva causale: `q1_activation_cash`, da 4.200 a 2.800. Il caso peggiore precedente è salito da 62.225 a 70.799; il replay canonico completo ha poi prodotto la distribuzione finale riportata sotto.

- attivazione Q1: D8 in tutti i run;
- modulo fisico completo (18 crop + 6 animali): D11 in tutti i run;
- primo output Q1 monetizzabile: D13, WHEAT, in tutti i run;
- media: 77.418,50;
- minimo: 70.799;
- fughe: 0.

Non è stato eseguito un terzo ciclo perché il target economico centrale era già superato e una nuova modifica avrebbe mescolato l'evidenza di attivazione con l'ottimizzazione biologica residua.

## Protocollo canonico

```text
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
EPISODES: 6
POST_HOC_SELECTION: NO
```

| Seed | Seat | Final money | Attivazione Q1 | Q1 completo | Primo output Q1 | Fughe |
|---:|---:|---:|---:|---:|---:|---:|
| 26090101 | 0 | 86.251 | D8 | D11 | D13 WHEAT | 0 |
| 26090101 | 1 | 70.799 | D8 | D11 | D13 WHEAT | 0 |
| 26090102 | 0 | 78.318 | D8 | D11 | D13 WHEAT | 0 |
| 26090102 | 1 | 78.318 | D8 | D11 | D13 WHEAT | 0 |
| 26090103 | 0 | 75.083 | D8 | D11 | D13 WHEAT | 0 |
| 26090103 | 1 | 75.742 | D8 | D11 | D13 WHEAT | 0 |

Distribuzione finale: media 77.418,50; mediana 77.030; minimo 70.799; massimo 86.251; deviazione standard 4.685,34.

## Confronto con V7.1

| Metrica media | V7.1 Q0 | V7.2 Q0+Q1 | Delta |
|---|---:|---:|---:|
| Final money | 61.118,83 | 77.418,50 | +16.299,67 (+26,67%) |
| Crop revenue | 30.561,17 | 45.586,33 | +15.025,17 |
| Livestock revenue | 35.288,00 | 48.681,67 | +13.393,67 |
| Crop units totali | 139,83 | 230,50 | +90,67 |
| Q0 crop units | 139,83 | 137,33 | -2,50 (-1,79%) |
| Q1 crop units | — | 93,17 | +93,17 |
| MILK | 90,00 | 134,83 | +44,83 |
| WOOL | 60,00 | 90,83 | +30,83 |
| Azioni produttive | 858,00 | 1.378,17 | +520,17 |
| MOVE | 2.601,33 | 4.259,17 | +1.657,83 |
| MOVE/produttiva | 3,0321 | 3,0905 | +0,0583 |
| Hard deadline misses, totale 6 run | 29 | 52 | +23 |
| Fughe, totale 6 run | 0 | 0 | 0 |

Q0 è preservato: la regressione crop è dell'1,79%, sotto il massimo del 5%, mentre la produzione animale Q0 resta esattamente 90 MILK e 60 WOOL in ogni episodio. Q1 aggiunge in media 93,17 crop units, 44,83 MILK e 30,83 WOOL.

L'aumento di offerta riduce il ricavo medio grezzo per unità: circa -9,5% sul crop e -8,3% sui prodotti animali rispetto a V7.1. Nonostante questa pressione e il costo marginale della capacità, il contributo economico integrato resta positivo.

## Serviceability e capacità

- 0 errori tecnici;
- 0 fallback tecnici;
- 0 fughe;
- 6 bovini e 6 ovini presenti a fine episodio in ogni run;
- 12 pascoli e 36 slot crop governati da owner locali;
- `MOVE_PER_PRODUCTIVE_ACTION` medio 3,0905, sotto il limite 3,50;
- nessuna sottrazione strutturale di worker da Q0: W1–W6 restano Q0, W7–W12 sono Q1.

Il principale residuo operativo è la densità dei deadline miss: 52 sui sei run contro 29 della V7.1. L'aumento è inferiore al raddoppio del footprint, ma segnala che il relief condiviso e i percorsi locali non chiudono ancora tutte le urgenze. È inoltre coerente con il mancato raggiungimento dei target biologici 145 MILK e 100 WOOL.

## Gate

| Gate | Soglia | Risultato | Esito |
|---|---:|---:|---|
| Technical pass | YES | YES | PASS |
| Errori / fallback | 0 / 0 | 0 / 0 | PASS |
| Final money medio minimo | 68.000 | 77.418,50 | PASS |
| Final money minimo | 55.000 | 70.799 | PASS |
| Fughe | 0 | 0 | PASS |
| Regressione crop Q0 | ≤5% | 1,79% | PASS |
| Contributo netto Q1 | >0 | +16.299,67 integrato | PASS |
| Target economico centrale | ≥75.000 | 77.418,50 | PASS |
| Minimo centrale | ≥65.000 | 70.799 | PASS |
| MILK | ≥145 | 134,83 | MISS |
| WOOL | ≥100 | 90,83 | MISS |
| Crop units totali | ≥220 | 230,50 | PASS |
| Crop units Q0 | ≥130 | 137,33 | PASS |
| Crop units Q1 | ≥85 | 93,17 | PASS |
| MOVE/produttiva | ≤3,50 | 3,0905 | PASS |

Il minimo soddisfa anche lo stretch `FINAL_MONEY_MIN ≥ 70.000`; la media non raggiunge ancora la fascia stretch 82.000–85.000.

## Verifica tecnica

- Ruff sui file V7.1/V7.2, benchmark e test: PASS.
- Test mirati Dual-Q + regressione Q0: 23 PASS.
- Suite pertinente del repository, escluso il test che rigenera deliberatamente la submission canonica V7.1: 186 PASS.
- Rerun canonico dopo l'aggiunta della telemetria del primo output: risultati economici bit-for-bit invariati.
- Unico warning: pytest non ha potuto scrivere `.pytest_cache`; nessun impatto sui test.

La submission canonica V7.1 non fa parte della nuova candidata e non deve essere sostituita in questa fase. Non sono stati eseguiti torneo, Kaggle, commit o push.

## Artefatti

- prompt di attivazione: `results/model_spec_c2/codex/KAGGRICULTURE_C2_CODEX_V7_2_DUAL_Q0_Q1_ACTIVATION_PROMPT_IT.md`;
- controller: `src/agricola/strategy/codex_dual_q0_q1.py`;
- configurazione: `configs/model_spec_c2/CODEX_C2_DUAL_Q0_Q1_CONFIG.json`;
- test: `tests/test_codex_dual_q0_q1.py`;
- benchmark: `scripts/benchmark_codex_dual_q0_q1.py`;
- risultati: `results/model_spec_c2/codex/CODEX_V7_2_DUAL_Q_RESULTS.csv` e `.json`.

## Conclusione

L'ipotesi dell'utente è confermata: Q1 non deve sottrarre capacità a Q0. Aumentando in modo esplicito workforce, footprint e ownership, Q1 diventa un secondo modulo produttivo con il solo svantaggio strutturale di partire più tardi. Il risultato medio di 77,4k rende realistico il target di 75k e lo supera con margine; resta da ottimizzare la cadenza livestock/deadline, non da ridimensionare Q1.

La raccomandazione è una sola ulteriore iterazione causale, focalizzata su service cadence Q1 e relief locale, mantenendo congelati attivazione D8, geometria, workforce e Q0. Obiettivo: chiudere MILK/WOOL senza perdere il floor economico di 75k.

```text
CANDIDATE_VERSION: CODEX-C2-V7.2-DUAL-Q0-Q1
Q0_MODULE_PRESERVED: YES
Q1_ACTIVATION_DAY_MEAN: 8.00
Q1_FULL_MODULE_DAY_MEAN: 11.00
Q1_FIRST_OUTPUT_DAY_MEAN: 13.00
FINAL_MONEY_MEAN: 77418.50
FINAL_MONEY_MEDIAN: 77030.00
FINAL_MONEY_MIN: 70799.00
FINAL_MONEY_MAX: 86251.00
DELTA_VS_V7_1: +16299.67
Q1_NET_CONTRIBUTION: +16299.67 (INTEGRATED_DELTA_VS_V7_1)
MILK_MEAN: 134.83
WOOL_MEAN: 90.83
Q0_CROP_UNITS_MEAN: 137.33
Q1_CROP_UNITS_MEAN: 93.17
TOTAL_CROP_UNITS_MEAN: 230.50
ANIMAL_ESCAPES_TOTAL: 0
MOVE_PER_PRODUCTIVE_ACTION: 3.0905
OBJECTIVE_68000_REACHED: YES
OBJECTIVE_75000_REACHED: YES
TECHNICAL_PASS: YES
PRIMARY_REMAINING_BOTTLENECK: HARD_DEADLINE_MISS_DENSITY_AND_Q1_LIVESTOCK_CADENCE
NEXT_STEP: ONE_MORE_CAUSAL_ITERATION
TOURNAMENT_AUTHORIZED: NO
KAGGLE_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```
