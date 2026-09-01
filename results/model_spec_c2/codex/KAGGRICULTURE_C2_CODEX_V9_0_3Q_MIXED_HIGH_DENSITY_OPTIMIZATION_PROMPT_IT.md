# KAGGRICULTURE C2 — CODEX V9.0 3Q MIXED HIGH-DENSITY

## Prompt di esecuzione della prossima fase di ottimizzazione

### Mandato

Sviluppare, verificare e documentare una candidata Codex V9.0 che superi i limiti della V7.3 e il fallimento della V8.0. La nuova versione deve combinare:

- tre quadranti realmente produttivi, senza replicare nominalmente Q0;
- cluster zootecnici locali ad alta densità e vicini ai capanni;
- portafoglio colturale dinamico, sensibile a prezzo e orizzonte;
- routing locale e ruoli serviceable con non più di 12 hands;
- liquidazione terminale completa, senza shutdown negli ultimi due giorni.

La V7.3 resta la baseline canonica e la submission congelata. La V8.0 è evidenza negativa. Il replay ufficiale `docs/benchmark/104498819.json` è una sorgente di evidenza competitiva, non un episodio sul quale effettuare fitting cieco. La specifica `docs/model_specs/ANTIGRAVITY_150K_CENTRAL_LIVESTOCK_PROMPT_SPEC.md` deve essere trattata come raccolta di ipotesi: usare solo le parti confermate dal replay o dall'engine.

Obiettivi economici della fase:

```text
MILESTONE_MINIMO: FINAL_MONEY_MEAN >= 100000
TARGET_CENTRALE: FINAL_MONEY_MEAN >= 130000
TARGET_STRETCH: FINAL_MONEY_MAX >= 150000
ANIMAL_ESCAPES_TOTAL: 0
```

Non dichiarare raggiunto il target 130K o 150K sulla base di un singolo replay. Se viene raggiunto solo il milestone 100K, documentare il risultato come checkpoint V9.x e non come strategia 150K validata.

---

## 1. Autorizzazioni e limiti

```text
TASK_TYPE: IMPLEMENTATION_LOCAL_CAUSAL_OPTIMIZATION_AND_VALIDATION
IMPLEMENTATION_AUTHORIZED: YES
LOCAL_REPLAY_AUTHORIZED: YES
BOUNDED_CAUSAL_ITERATION_AUTHORIZED: YES
DOCUMENTATION_AUTHORIZED: YES
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
ENGINE_MODIFICATION_AUTHORIZED: NO
ANTIGRAVITY_SOURCE_MODIFICATION_AUTHORIZED: NO
CANONICAL_SUBMISSION_REPLACEMENT_AUTHORIZED_AFTER_PROMOTION_GATES: YES
TOURNAMENT_AUTHORIZED: NO
KAGGLE_EXECUTION_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

Preservare tutte le modifiche preesistenti nel worktree. Non eliminare file, non ripulire artefatti altrui e non modificare la submission canonica prima del superamento dei gate di promozione.

---

## 2. Baseline e prove obbligatorie

### 2.1 Baseline canonica Codex V7.3

Usare come baseline comportamentale congelata:

- `src/agricola/strategy/codex_dual_q1_cadence.py`;
- `configs/model_spec_c2/CODEX_C2_DUAL_Q1_CADENCE_CONFIG.json`;
- `results/model_spec_c2/codex/CODEX_V7_3_Q1_CADENCE_RESULTS.json`;
- `results/model_spec_c2/codex/CODEX_V7_3_Q1_CADENCE_FINAL_REPORT_IT.md`;
- `submission/submission_codex.py` come artefatto canonico da non sostituire durante lo sviluppo.

Metriche V7.3:

```text
FINAL_MONEY_MEAN: 78036.17
FINAL_MONEY_MEDIAN: 77481.00
FINAL_MONEY_MIN: 71771.00
FINAL_MONEY_MAX: 88397.00
Q0_CROP_UNITS_MEAN: 137.17
Q1_CROP_UNITS_MEAN: 85.83
TOTAL_CROP_UNITS_MEAN: 223.00
MILK_MEAN: 146.17
WOOL_MEAN: 109.17
ANIMAL_ESCAPES_TOTAL: 0
MOVE_PER_PRODUCTIVE_ACTION: 3.0163
```

### 2.2 V8.0 come controllo negativo

La V8.0 non è una base da estendere. Ha prodotto:

```text
FINAL_MONEY_MEAN: 65218.83
DELTA_VS_V7_3: -12817.33
Q0_CROP_REGRESSION: 11.18%
Q1_CROP_REGRESSION: 13.59%
ANIMAL_ESCAPES_TOTAL: 23
```

Non riutilizzare i suoi meccanismi falliti:

- Q2 con 12 MELON o un altro crop statico dominante;
- Q2 6 COW + 6 SHEEP appoggiato agli owner Q0/Q1;
- soglia Q2 di 5.500 priva di sufficiente capitale operativo;
- alimentazione alternata che libera capacità ma provoca fughe;
- copia nominale di Q0/Q1 senza ledger di azioni, salari e payback.

### 2.3 Replay competitivo 104498819

Riprodurre prima di ogni modifica il replay `docs/benchmark/104498819.json`:

```text
EPISODE: 104498819
SEED: 562040596
LEADER_KEIZ_FINAL_MONEY: 158575
CODEX_V7_3_EXACT_REPLAY: 51875
```

La riproduzione V7.3 contro la sequenza di azioni registrata di `keiz` deve essere esatta a 51.875. In caso contrario fermarsi e correggere il harness prima di ottimizzare.

---

## 3. Correzioni fattuali obbligatorie alla specifica Antigravity

Non implementare affermazioni smentite dall'engine o dal replay.

1. `keiz` termina con 8 COW, 11 SHEEP e 1 GOOSE, ma una COW fugge al giorno 9: il replay non dimostra zero escapes.
2. Le 38 STRAWBERRY, 9 WHEAT e 8 MELON sono una fotografia circa al giorno 20, non una configurazione statica. Circa al giorno 25 il mix diventa 17 STRAWBERRY, 37 WHEAT e 0 MELON.
3. STRAWBERRY non è perpetua: primo output dopo 10 giorni, intervallo 2, massimo 4 eventi produttivi. La resa base massima è 4 unità per pianta, fino a 8 se fertilizzata; non 40+.
4. WHEAT non è foraggio gratuito. Richiede seed, semina, acqua, raccolta e routing. Nel replay `keiz` compra anche 467 unità di WHEAT.
5. Il cluster è centrale ma non tutto a distanza 0–1 dal capanno. Distribuzione osservata sugli animali: distanza 0 = 3, distanza 1 = 6, distanza 2 = 8, distanza 3 = 3.
6. Il replay arriva a un massimo di 12 hands. Con farmer più 12 hands gli worker id validi sono W0–W12; un ruolo W13 sarebbe una quattordicesima persona e viola il limite.
7. La vendita di 351 FERTILIZER è confermata; il relativo ricavo deve però essere calcolato dai prezzi realizzati, non da un prezzo fisso ipotetico.
8. Un solo episodio con 158.575 non dimostra una media di 130K o 140K.

Prima dell'implementazione verificare nuovamente questi contratti direttamente nel codice engine e citare file e righe nel report.

---

## 4. Evidenze causali già disponibili

Sul replay fisso contro le azioni registrate di `keiz` sono già stati misurati questi interventi in memoria:

| Variante | Denaro finale | Delta vs V7.3 |
|---|---:|---:|
| V7.3 esatta | 51.875 | 0 |
| shutdown terminale da 2 giorni a 0 | 56.346 | +4.471 |
| rotazione Q1 senza MELON + Q0 MELON→WHEAT dopo il primo raccolto | 57.034 | +5.159 |
| rotazione + shutdown 0 | 61.841 | +9.966 |
| combinazione precedente + gate Q1 a 1.800 | 63.579 | +11.704 |
| stessa logica con gate Q1 a 1.000 | 42.391 | -9.484 |

Questi risultati sono effetti condizionati a uno specifico avversario e non autorizzano l'integrazione simultanea non misurata. Devono essere riprodotti e poi trasferiti uno alla volta alla candidata, con confronto appaiato anche sul protocollo canonico.

---

## 5. Ipotesi architetturale V9.0

Nome descrittivo:

```text
3Q MIXED HIGH-DENSITY
+ CENTRAL LIVESTOCK
+ DYNAMIC CROP ROTATION
+ LOCAL SERVICE ROUTING
+ HORIZON-AWARE LIQUIDATION
```

Non usare il nome “mega-stalla con fragole perpetue”: entrambe le proposizioni inducono una rappresentazione errata dell'engine.

### 5.1 Fasi economiche

#### D0–D6 — Q0 compatto e cash generation

- attivare un Q0 compatto con MELON iniziale limitato e non permanente;
- costruire il primo nucleo livestock solo quando FEED, CARE e COLLECTION sono serviceable;
- arrivare progressivamente a 5–8 hands, non assumere il roster finale al giorno 0;
- proteggere un buffer operativo esplicito dopo ogni acquisto;
- usare il primo raccolto MELON come evento di transizione, non come portafoglio per tutto l'episodio.

#### D6–D10 — Q1 selettivo

- valutare il gate Q1 intorno a 1.800, senza trasformarlo in una costante cieca;
- richiedere Q0 maturo, nessuna urgenza arretrata e cash-flow proiettato positivo;
- orientare Q1 a STRAWBERRY quando l'orizzonte permette tutti gli eventi produttivi e a WHEAT quando il fabbisogno feed o il prezzo marginale lo giustificano;
- arrivare a 8–11 hands solo per coprire ruoli dimostrati serviceable.

#### D11–D20 — Q2 misto e capitalizzato

- non acquistare Q2 con una soglia nominale bassa;
- usare come ipotesi iniziale un gate di cassa/liquidità vendibile tra 15.000 e 18.000, coerente con i 17.912 osservati nel replay leader al giorno 11;
- configurare Q2 come modulo misto, non come copia di Q0: ipotesi iniziale circa 19 crop + 5 SHEEP;
- vietare Q2 se il suo ledger sottrae hard tasks a Q0/Q1 o richiede oltre 12 hands;
- misurare separatamente contributo Q2, cannibalizzazione di prezzo, salario marginale, costo feed e regressione del nucleo.

#### D20–D29 — rotazione e liquidazione terminale

- cessare il replant MELON quando non restano cicli economicamente completi;
- selezionare STRAWBERRY solo se il numero di output residui copre seed e azioni;
- ruotare verso WHEAT quando domanda feed, prezzo e tempo residuo lo rendono dominante;
- mantenere capacità operativa fino al giorno 29 se il ricavo marginale supera il salario;
- vendere inventario maturo e raccogliere output terminale; nessuno shutdown fisso di due giorni;
- lasciare invenduto o non raccolto soltanto ciò che è dimostrabilmente non recuperabile entro l'orizzonte.

### 5.2 Geometria zootecnica da testare

Usare come ipotesi iniziale le coordinate finali osservate, correggendo gli errori della specifica Antigravity:

```text
Q0 COW:   (4,2), (4,3), (2,4), (4,4)
Q0 SHEEP: (3,2), (3,3), (3,4)
Q0 GOOSE: (4,1)

Q1 COW:   (5,2), (6,3), (5,4), (6,4)
Q1 SHEEP: (6,2), (5,3), (7,4)

Q2 SHEEP: (3,5), (4,5), (3,6), (4,6), (4,7)
```

La coordinata `(5,5)` appartiene al quadrante SE non acquistato e non deve essere usata come pascolo Q2 SW. Le coordinate osservate sono un punto di partenza: accettarle solo se pathfinding, adiacenza, legalità di PLACE e accesso ai capanni sono verificati dall'engine.

### 5.3 Portafoglio colturale dinamico

Il controller deve scegliere il crop attraverso valore marginale atteso, non quote statiche. Per ogni tile candidata stimare almeno:

```text
EXPECTED_UNITS_BEFORE_HORIZON
EXPECTED_REALIZED_PRICE_AFTER_OWN_SUPPLY
SEED_COST
WATER_PLANT_HARVEST_ACTION_COST
EXPECTED_ROUTING_COST
FERTILIZER_OPPORTUNITY_COST
FEED_SUBSTITUTION_VALUE_FOR_WHEAT
EXPECTED_NET_VALUE
```

Vincoli:

- limitare MELON dopo il primo ciclo e impedirne la saturazione osservata;
- non assumere STRAWBERRY perpetua;
- non assumere WHEAT autosufficiente o gratuito;
- includere elasticità del prezzo alla propria offerta;
- preferire diversificazione e rotazione solo quando migliorano il valore netto realizzato;
- registrare il mix per giorno e quadrante, non soltanto lo snapshot finale.

### 5.4 Roster e routing

- massimo 12 hands, quindi W0 farmer e W1–W12 hands;
- nessun ramo per W13 se il roster resta a 12 hands;
- ruoli locali per capanno e sottocluster; assistenza cross-quadrant solo dopo le urgenze locali;
- pickup batch, depositi locali e task composti serviceable;
- ownership unica per FEED, CARE, COLLECTION e hard crop nella finestra corrente;
- prevenire target duplicati e movimenti verso interazioni non ancora legali;
- la priorità FEED deve derivare dal contratto engine osservabile, senza introdurre cadenze rischiose;
- il farmer è relief/logistics centrale, non sostituto ordinario degli owner mancanti.

Target di efficienza, usando una definizione uniforme nel confronto:

```text
MOVE_PER_PRODUCTIVE_ACTION <= 1.50
PASS_SHARE <= 15%
PRODUCTIVE_ACTION_SHARE >= 35%
```

Se le metriche del benchmark canonico usano una tassonomia diversa dal replay, produrre entrambe e non confrontare rapporti costruiti con denominatori differenti.

### 5.5 Ledger livestock e fertilizer

Per ogni modulo registrare:

- animali acquistati, attivi, venduti e fuggiti per specie;
- FEED dovuti e completati;
- CARE e COLLECTION dovuti, completati e mancati;
- MILK, WOOL, EGG e FERTILIZER prodotti, raccolti, venduti e residui;
- WHEAT comprato, prodotto, consumato e residuo;
- costo animali, pasture, feed, wheat, salari e routing;
- ricavo realizzato per prodotto e contributo netto per quadrante.

Il target di 20 animali è ammesso solo se tutti sono serviceable con zero fughe. In caso contrario ridurre il footprint; non mascherare l'errore aumentando la tolleranza alle fughe.

---

## 6. Protocollo causale

Sono ammessi al massimo cinque cicli principali dopo la riproduzione delle baseline. Ogni ciclo deve dichiarare una sola famiglia causale e mantenere invariati gli altri meccanismi.

### Ciclo 0 — harness e osservabilità

- riprodurre V7.3 sui 6 episodi canonici;
- riprodurre esattamente 51.875 sul replay competitivo;
- aggiungere telemetria per quadrante, ruolo, prodotto, prezzi, task mancati, salari e inventario terminale;
- nessuna modifica strategica.

### Ciclo 1 — quick wins già dimostrati

- integrare e verificare separatamente shutdown 0;
- integrare e verificare separatamente rotazione iniziale MELON→WHEAT / Q1 senza MELON;
- verificare il gate Q1 intorno a 1.800 con sweep ristretto e pre-dichiarato;
- non integrare automaticamente una modifica se regredisce la media canonica oltre l'1%.

### Ciclo 2 — portafoglio crop sensibile a prezzo e orizzonte

- introdurre il valore marginale atteso;
- misurare prezzi realizzati, volumi, costo azioni e cannibalizzazione;
- confrontare politica dinamica con quote statiche controllate.

### Ciclo 3 — cluster livestock centrale e routing locale

- partire da Q0/Q1 e dimostrare serviceability con massimo 12 hands;
- introdurre specie e pasture una alla volta o per sottocluster dichiarato;
- misurare guadagno netto per animale, azioni aggiuntive e distanza effettiva.

### Ciclo 4 — Q2 misto

- attivare Q2 soltanto dopo il superamento dei gate Q0/Q1;
- provare il footprint 19 crop + 5 SHEEP come ipotesi, non come obbligo;
- confrontare Q2 OFF e Q2 ON sugli stessi episodi;
- respingere Q2 se il contributo osservato è non positivo o se la regressione Q0/Q1 supera il 3%.

### Ciclo 5 — integrazione e holdout

- congelare parametri prima dell'holdout;
- eseguire la suite completa senza selezione post-hoc;
- non correggere la candidata sui risultati holdout; eventuali nuove modifiche aprono una nuova versione e un nuovo holdout.

---

## 7. Suite di valutazione

### 7.1 Protocollo canonico appaiato

```text
SEEDS: 26090101, 26090102, 26090103
SEATS: 0, 1
OPPONENT: INERT_PASS_POLICY
EPISODE_STEPS: 720
TURNS_PER_DAY: 24
EPISODES: 6
```

Confrontare V9.0 con V7.3 sullo stesso seed e seat. Conservare tutti i run.

### 7.2 Replay competitivo fisso

Usare `docs/benchmark/104498819.json` contro le azioni avversarie registrate. È un test causale riproducibile, non un sostituto degli holdout.

### 7.3 Holdout obbligatorio

Prima dell'esecuzione dichiarare in un manifest immutabile 12 episodi holdout, includendo seed, seat, opponent e hash della configurazione. Gli episodi non possono essere selezionati o esclusi dopo aver visto i risultati. Se il repository contiene già Phase B / Phase C ufficialmente congelate, usare quelle; altrimenti creare deterministicamente il manifest prima di eseguire la candidata e usare la stessa suite anche per V7.3.

Riportare separatamente:

- protocollo canonico;
- replay competitivo;
- holdout;
- aggregato complessivo, solo come informazione secondaria.

---

## 8. Gate progressivi

### Gate A — correttezza

```text
ERRORS: 0
FALLBACKS: 0
ILLEGAL_ACTIONS: 0
ANIMAL_ESCAPES_TOTAL: 0
BASELINE_V7_3_REPRODUCED: YES
COMPETITIVE_REPLAY_51875_REPRODUCED: YES
```

### Gate B — trasferimento dei quick wins

```text
COMPETITIVE_REPLAY_FINAL_MONEY >= 63500
CANONICAL_MEAN >= 78036.17
CANONICAL_MIN >= 71000
TERMINAL_COLLECTIBLE_VALUE_REGRESSION <= 0
ANIMAL_ESCAPES_TOTAL = 0
```

La soglia 63.500 convalida il trasferimento dell'evidenza già misurata; non è il target economico finale.

### Gate C — milestone promuovibile V9.x

```text
CANONICAL_FINAL_MONEY_MEAN >= 100000
CANONICAL_FINAL_MONEY_MIN >= 85000
HOLDOUT_FINAL_MONEY_MEAN >= 100000
HOLDOUT_FINAL_MONEY_MIN >= 80000
COMPETITIVE_REPLAY_FINAL_MONEY >= 90000
Q0_Q1_CORE_REGRESSION <= 3%
Q2_OBSERVED_NET_CONTRIBUTION > 0
MOVE_PER_PRODUCTIVE_ACTION <= 1.50
ANIMAL_ESCAPES_TOTAL = 0
TECHNICAL_PASS: YES
```

Solo il superamento del Gate C autorizza una proposta di sostituzione della submission canonica.

### Gate D — target centrale 130K

```text
CANONICAL_FINAL_MONEY_MEAN >= 130000
HOLDOUT_FINAL_MONEY_MEAN >= 130000
HOLDOUT_FINAL_MONEY_MEDIAN >= 125000
HOLDOUT_FINAL_MONEY_MIN >= 100000
FINAL_MONEY_MAX >= 150000
MILK_SOLD_MEAN >= 200
WOOL_SOLD_MEAN >= 200
FERTILIZER_SOLD_MEAN >= 250
ANIMAL_ESCAPES_TOTAL = 0
TECHNICAL_PASS: YES
```

Le soglie di prodotto sono diagnostiche subordinate al denaro finale: non acquistare o produrre unità in perdita per soddisfarle.

---

## 9. Controlli specifici sul codice Antigravity

Non copiare `src/agricola/strategy/antigravity/antigravity_150k_mega_cluster.py`. Prima di riusare una sua idea, verificare esplicitamente e documentare:

- il piano corrente di circa 30 MELON, 16 STRAWBERRY e 6 WHEAT, incompatibile con la rotazione osservata;
- il target 8 COW + 12 SHEEP senza GOOSE, diverso dal replay;
- il gate Q2 a 2.300, molto inferiore ai circa 17.912 osservati;
- l'eventuale ramo `worker_id == 13`, non raggiungibile con 12 hands;
- il conteggio seed: usare l'inventario seed corretto, non l'inventario prodotti;
- qualunque assunzione di resa STRAWBERRY perpetua.

Ogni meccanismo mutuato da Antigravity deve avere un test mirato e un ablation test.

---

## 10. Artefatti richiesti

Creare la candidata senza modificare la V7.3:

- `src/agricola/strategy/codex_3q_mixed_high_density.py`;
- `configs/model_spec_c2/CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json`;
- `tests/test_codex_3q_mixed_high_density.py`;
- `scripts/benchmark_codex_3q_mixed_high_density.py`;
- `results/model_spec_c2/codex/CODEX_V9_0_CAUSAL_ITERATIONS.json`;
- `results/model_spec_c2/codex/CODEX_V9_0_RESULTS.csv`;
- `results/model_spec_c2/codex/CODEX_V9_0_RESULTS.json`;
- `results/model_spec_c2/codex/CODEX_V9_0_FINAL_REPORT_IT.md`;
- manifest holdout con hash di config e controller;
- builder, verifier e test di isolamento solo dopo il Gate C.

Il report finale deve essere in italiano e distinguere chiaramente osservazioni, inferenze e ipotesi respinte.

---

## 11. Regole per la submission

1. Non modificare `submission/submission_codex.py` durante la ricerca.
2. Se il Gate C non è superato, conservare la V7.3 canonica.
3. Se il Gate C è superato, costruire una candidata standalone temporanea e verificarne l'import senza package `src`.
4. Richiedere parità esatta di tutte le decisioni rispetto al controller V9.0 sui replay canonici e holdout.
5. Sostituire `submission/submission_codex.py` soltanto dopo parità, test completi e report conclusivo.
6. Non eliminare o modificare submission non Codex.
7. Non eseguire upload Kaggle, commit o push.

---

## 12. Blocco finale obbligatorio

```text
CANDIDATE_VERSION: <value>
BASELINE_V7_3_REPRODUCED: YES | NO
COMPETITIVE_REPLAY_BASELINE_REPRODUCED: YES | NO
QUICK_WINS_TRANSFERRED: YES | PARTIAL | NO
Q0_ACTIVATION_DAY_MEAN: <value>
Q1_ACTIVATION_DAY_MEAN: <value>
Q2_ACTIVATION_DAY_MEAN: <value or NA>
HANDS_PEAK: <value>
ANIMALS_ACTIVE_PEAK: <value>
CANONICAL_FINAL_MONEY_MEAN: <value>
CANONICAL_FINAL_MONEY_MEDIAN: <value>
CANONICAL_FINAL_MONEY_MIN: <value>
CANONICAL_FINAL_MONEY_MAX: <value>
DELTA_VS_V7_3_CANONICAL: <value>
COMPETITIVE_REPLAY_FINAL_MONEY: <value>
DELTA_VS_51875_REPLAY: <value>
HOLDOUT_FINAL_MONEY_MEAN: <value>
HOLDOUT_FINAL_MONEY_MEDIAN: <value>
HOLDOUT_FINAL_MONEY_MIN: <value>
HOLDOUT_FINAL_MONEY_MAX: <value>
Q2_OBSERVED_NET_CONTRIBUTION: <value or NA>
MILK_SOLD_MEAN: <value>
WOOL_SOLD_MEAN: <value>
FERTILIZER_SOLD_MEAN: <value>
WHEAT_BOUGHT_MEAN: <value>
ANIMAL_ESCAPES_TOTAL: <value>
MOVE_PER_PRODUCTIVE_ACTION: <value>
PASS_SHARE: <value>
PRODUCTIVE_ACTION_SHARE: <value>
GATE_A_CORRECTNESS: PASS | FAIL
GATE_B_QUICK_WINS: PASS | FAIL
GATE_C_100K_MILESTONE: PASS | FAIL
GATE_D_130K_TARGET: PASS | FAIL
PEAK_150K_REACHED: YES | NO
TECHNICAL_PASS: YES | NO
SUBMISSION_REPLACED: YES | NO
PRIMARY_REMAINING_BOTTLENECK: <value or NONE>
NEXT_STEP: FREEZE_V9 | OPEN_V9_POINT_ITERATION | REJECT_AND_RETAIN_V7_3
TOURNAMENT_AUTHORIZED: NO
KAGGLE_EXECUTION_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

## STOP

Dopo implementazione, test, benchmark, report ed eventuale verifica locale della submission, fermarsi. Non eseguire torneo, upload Kaggle, commit o push. Se nessuna candidata supera il Gate C, non sostituire la V7.3 e dichiarare esplicitamente quali ipotesi sono state respinte.
