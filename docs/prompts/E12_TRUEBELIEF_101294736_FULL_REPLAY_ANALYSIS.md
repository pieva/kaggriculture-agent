# E12 --- `truebelief` Episode 101294736: ricostruzione completa Day 1--30

## 0. Scopo e stato dell'evidenza

Questo documento ricostruisce in modo sistematico il comportamento
dell'agente Kaggle `truebelief` nell'episode **101294736**, per fornire
agli agenti successivi una base quantitativa e machine-usable per
DEFINE, audit e benchmark. La fonte primaria è il replay JSON raw
scaricato dal browser Kaggle autenticato. Non vengono usati screenshot o
stime visive quando il replay consente una misura diretta.

**Regola epistemica:** le sezioni marcate **OSSERVATO** derivano
direttamente da stato/azioni del replay; le sezioni marcate
**INFERENZA** interpretano economicamente quei dati. Le inferenze non
devono essere trattate come regole dell'engine né come prova causale.

### Provenance

-   Episode ID: `101294736`
-   Seed registrato dal replay: `421521921`
-   Agent 0: `Pietro Valocchi`
-   Agent 1: `truebelief` (`truebelief`)
-   Reward finale: `6.825` vs **`86.297`**
-   Engine/module version: `1.32.7`
-   Step: `720` = 30 giorni × `24` turni
-   Starting money: `3000`

## 1. Executive findings per gli agenti

### OSSERVATO

1.  `truebelief` chiude a **86.297** usando soltanto **Q0+Q1**. Q1 viene
    acquistato soltanto al **Day 11**, dopo dieci giorni completi su Q0.
2.  L'opening Day 1 satura Q0 con **21 crop + 4 pasture**, usando già un
    mix **6 Wheat + 8 Melon + 7 Strawberry** e **5 Hands**. Non esiste
    una fase iniziale Wheat-only.
3.  Il livestock viene acquistato prima dell'espansione: prima Cow
    acquistata Day 5, seconda Day 9; la prima Cow risulta piazzata
    Day 10. Tra Day 11--14 l'agente scala rapidamente fino a **7 Cow + 4
    Sheep attive su 11 pasture**.
4.  Il primo `SELL MILK` e il primo `SELL WOOL` compaiono al **Day 19**.
    Da quel punto la liquidità accelera: **10.810 Day 18 → 17.467 Day 19
    → 24.778 Day 20 → 53.135 Day 24 → 85.048 Day 29**.
5.  Dopo Day 20 il numero di crop tile diminuisce mentre il denaro
    continua ad accelerare: **39 crop Day 20 → 23 Day 29 → 16 Day 30**.
    Quindi superficie coltivata istantanea e final money non sono
    monotonicamente legati.
6.  L'agente non usa Carrot o Tomato in questo replay. Le vendite
    osservate sono Wheat, Melon, Strawberry, Milk, Wool e Fertilizer.
7.  Il Wheat è gestito come commodity operativa: **86 Wheat seed
    acquistati, 171 Wheat comprati come prodotto e 268 Wheat venduti**.
    Una policy `BUY_PRODUCT Wheat = sempre errore` è falsificata da
    questo benchmark competitivo.
8.  Workforce totale: **231 HIRE**. Nella fase matura vengono
    normalmente comprati circa 9--12 Hands/giorno. Il costo del lavoro
    viene accettato per aumentare throughput e velocità di conversione.
9.  Acquisti animali totali: **9 Cow + 5 Sheep**; animali attivi finali:
    **7 Cow + 4 Sheep**. A fine episodio rimangono **2 Cow + 1 Sheep nel
    shed**, quindi l'acquisto di animali supera deliberatamente/di fatto
    il numero piazzato.
10. A fine episodio restano anche inventari non monetizzati sui worker:
    **Milk 4, Wheat 4, Wool 2**, oltre a seed residui. 86.297 non è
    quindi il risultato di una liquidazione perfetta di ogni asset.

### INFERENZA

-   Il vantaggio di `truebelief` è meglio descritto come **sequencing +
    portfolio + cash-conversion throughput** che come semplice
    saturazione fisica.
-   Q1 sembra essere un investimento di seconda fase: prima viene
    costruito un motore Q0, poi l'espansione avviene quando
    Melon/Strawberry e livestock stanno iniziando a liberare cassa.
-   La fase Day 19--29 è il vero compounding osservabile: il capitale
    cresce di circa 67,6k mentre la superficie crop si contrae.
    L'architettura deve quindi ottimizzare **valore realizzato per
    giorno**, non mantenere un target CPS rigido.
-   Livestock è un secondo motore ricorrente, ma non isolabile
    causalmente dal replay senza counterfactual. Milk/Wool/Fertilizer
    entrano contemporaneamente al forte aumento del cash.

## 2. Timeline completa Day 1--30

  --------------------------------------------------------------------------------------------------------------
     Day    Money   Δ cash      Q   Hands   Crop Mix crop   Pasture Livestock     Weed Market actions/quantities
  ------ -------- -------- ------ ------- ------ -------- --------- ----------- ------ -------------------------
       1      928   -2.072      1       5     21 Whe 6.           4 ---              0 HIRE=5;
                                                 Mel 8.                                BUY_SEED:WHEAT=18;
                                                 Str 7                                 BUY_SEED:MELON=11;
                                                                                       BUY_SEED:STRAWBERRY=10

       2      916      -12      1       5     21 Whe 6.           4 ---              0 HIRE=5
                                                 Mel 8.                                
                                                 Str 7                                 

       3      904      -12      1       5     21 Whe 6.           4 ---              0 HIRE=5
                                                 Mel 8.                                
                                                 Str 7                                 

       4      892      -12      1       5     21 Whe 6.           4 ---              0 HIRE=5
                                                 Mel 8.                                
                                                 Str 7                                 

       5      876      -16      1       5     21 Whe 6.           4 ---              0 HIRE=5; BUY_ANIMAL:COW=1;
                                                 Mel 8.                                SELL:WHEAT=18
                                                 Str 7                                 

       6      864      -12      1       5     21 Whe 6.           4 ---              0 HIRE=5
                                                 Mel 8.                                
                                                 Str 7                                 

       7      852      -12      1       5     21 Whe 6.           4 ---              0 HIRE=5
                                                 Mel 8.                                
                                                 Str 7                                 

       8      840      -12      1       5     21 Whe 6.           4 ---              0 HIRE=5
                                                 Mel 8.                                
                                                 Str 7                                 

       9      718     -122      1       5     21 Whe 6.           4 ---              0 HIRE=5; BUY_ANIMAL:COW=1;
                                                 Mel 8.                                BUY_SEED:WHEAT=4;
                                                 Str 7                                 SELL:WHEAT=15

      10      684      -34      1       5     21 Whe 6.           4 Cow 1            0 HIRE=5;
                                                 Mel 8.                                BUY_PRODUCT:WHEAT=4;
                                                 Str 7                                 SELL:WHEAT=3

      11    1.794   +1.110      2       5     17 Whe 6.           4 Cow 3            0 HIRE=5; BUY_LAND=1;
                                                 Mel 3.                                BUY_ANIMAL:COW=5;
                                                 Str 8                                 BUY_SEED:WHEAT=22;
                                                                                       BUY_SEED:MELON=8;
                                                                                       BUY_SEED:STRAWBERRY=11;
                                                                                       BUY_PRODUCT:WHEAT=4;
                                                                                       SELL:MELON=24

      12    5.223   +3.429      2       6     22 Whe 6.           9 Cow 6.           0 HIRE=6; BUY_ANIMAL:COW=2;
                                                 Mel 5.             Sheep 2            BUY_ANIMAL:SHEEP=5;
                                                 Str 11                                BUY_PRODUCT:WHEAT=26;
                                                                                       SELL:MELON=24;
                                                                                       SELL:STRAWBERRY=7;
                                                                                       SELL:FERTILIZER=1

      13    4.969     -254      2       9     25 Whe 1.          11 Cow 7.           0 HIRE=9; BUY_SEED:MELON=2;
                                                 Mel 9.             Sheep 3            BUY_SEED:STRAWBERRY=1;
                                                 Str 15                                BUY_PRODUCT:WHEAT=7;
                                                                                       SELL:FERTILIZER=3

      14    6.515   +1.546      2      10     37 Whe 8.          11 Cow 7.           0 HIRE=10;
                                                 Mel 10.            Sheep 4            BUY_PRODUCT:WHEAT=14;
                                                 Str 19                                SELL:WHEAT=10;
                                                                                       SELL:STRAWBERRY=7;
                                                                                       SELL:FERTILIZER=3

      15    6.595      +80      2      10     39 Whe 10.         11 Cow 7.           0 HIRE=10;
                                                 Mel 10.            Sheep 4            BUY_PRODUCT:WHEAT=11;
                                                 Str 19                                SELL:FERTILIZER=6

      16    8.326   +1.731      2       9     39 Whe 10.         11 Cow 7.           0 HIRE=9;
                                                 Mel 10.            Sheep 4            BUY_PRODUCT:WHEAT=11;
                                                 Str 19                                SELL:STRAWBERRY=7;
                                                                                       SELL:FERTILIZER=6

      17    8.844     +518      2      10     39 Whe 10.         11 Cow 7.           0 HIRE=10;
                                                 Mel 10.            Sheep 4            BUY_PRODUCT:WHEAT=11;
                                                 Str 19                                SELL:WHEAT=3;
                                                                                       SELL:FERTILIZER=10

      18   10.810   +1.966      2      10     39 Whe 17.         11 Cow 7.           0 HIRE=10;
                                                 Mel 10.            Sheep 4            BUY_SEED:WHEAT=4;
                                                 Str 12                                BUY_PRODUCT:WHEAT=11;
                                                                                       SELL:WHEAT=7;
                                                                                       SELL:STRAWBERRY=7;
                                                                                       SELL:FERTILIZER=6

      19   17.467   +6.657      2      11     39 Whe 17.         11 Cow 7.           0 HIRE=11;
                                                 Mel 10.            Sheep 4            BUY_SEED:WHEAT=2;
                                                 Str 12                                SELL:WHEAT=23;
                                                                                       SELL:MILK=12;
                                                                                       SELL:WOOL=11;
                                                                                       SELL:FERTILIZER=13

      20   24.778   +7.311      2      12     39 Whe 17.         11 Cow 7.           0 HIRE=12;
                                                 Mel 10.            Sheep 4            BUY_PRODUCT:WHEAT=11;
                                                 Str 12                                SELL:MILK=21;
                                                                                       SELL:WOOL=11;
                                                                                       SELL:FERTILIZER=8

      21   27.587   +2.809      2      10     37 Whe 18.         11 Cow 7.           0 HIRE=10;
                                                 Mel 7.             Sheep 4            BUY_SEED:WHEAT=2;
                                                 Str 12                                BUY_PRODUCT:WHEAT=11;
                                                                                       SELL:WHEAT=3;
                                                                                       SELL:MILK=12;
                                                                                       SELL:FERTILIZER=5

      22   35.307   +7.720      2      12     34 Whe 17.         11 Cow 7.           0 HIRE=12;
                                                 Mel 5.             Sheep 4            BUY_SEED:WHEAT=14;
                                                 Str 12                                BUY_PRODUCT:WHEAT=11;
                                                                                       SELL:WHEAT=11;
                                                                                       SELL:MELON=18;
                                                                                       SELL:STRAWBERRY=1;
                                                                                       SELL:MILK=9; SELL:WOOL=8;
                                                                                       SELL:FERTILIZER=11

      23   44.125   +8.818      2      11     31 Whe 18.         11 Cow 7.           0 HIRE=11;
                                                 Mel 1.             Sheep 4            BUY_SEED:WHEAT=2;
                                                 Str 12                                SELL:WHEAT=45;
                                                                                       SELL:MELON=18;
                                                                                       SELL:STRAWBERRY=5;
                                                                                       SELL:MILK=11;
                                                                                       SELL:WOOL=4;
                                                                                       SELL:FERTILIZER=10

      24   53.135   +9.010      2      12     30 Whe 18.         11 Cow 7.           0 HIRE=12;
                                                 Str 12             Sheep 4            BUY_PRODUCT:WHEAT=6;
                                                                                       SELL:WHEAT=12;
                                                                                       SELL:MELON=24;
                                                                                       SELL:STRAWBERRY=5;
                                                                                       SELL:MILK=9;
                                                                                       SELL:WOOL=12;
                                                                                       SELL:FERTILIZER=11

      25   57.172   +4.037      2      11     30 Whe 18.         11 Cow 7.           0 HIRE=11;
                                                 Str 12             Sheep 4            BUY_SEED:WHEAT=2;
                                                                                       BUY_PRODUCT:WHEAT=11;
                                                                                       SELL:WHEAT=6;
                                                                                       SELL:STRAWBERRY=5;
                                                                                       SELL:MILK=9;
                                                                                       SELL:FERTILIZER=10

      26   62.344   +5.172      2      11     30 Whe 18.         11 Cow 7.           0 HIRE=11;
                                                 Str 12             Sheep 4            BUY_SEED:WHEAT=14;
                                                                                       BUY_PRODUCT:WHEAT=11;
                                                                                       SELL:WHEAT=6;
                                                                                       SELL:STRAWBERRY=5;
                                                                                       SELL:MILK=12;
                                                                                       SELL:WOOL=4;
                                                                                       SELL:FERTILIZER=7

      27   70.890   +8.546      2      11     30 Whe 18.         11 Cow 7.           0 HIRE=11;
                                                 Str 12             Sheep 4            BUY_SEED:WHEAT=2;
                                                                                       SELL:WHEAT=57;
                                                                                       SELL:STRAWBERRY=8;
                                                                                       SELL:MILK=12;
                                                                                       SELL:WOOL=8;
                                                                                       SELL:FERTILIZER=10

      28   77.325   +6.435      2      11     29 Whe 18.         11 Cow 7.           0 HIRE=11;
                                                 Str 11             Sheep 4            BUY_PRODUCT:WHEAT=11;
                                                                                       SELL:WHEAT=7;
                                                                                       SELL:STRAWBERRY=6;
                                                                                       SELL:MILK=12;
                                                                                       SELL:WOOL=8;
                                                                                       SELL:FERTILIZER=10

      29   85.048   +7.723      2       0     23 Whe 15.         11 Cow 7.           3 SELL:WHEAT=33;
                                                 Str 8              Sheep 4            SELL:STRAWBERRY=5;
                                                                                       SELL:MILK=15;
                                                                                       SELL:FERTILIZER=8

      30   86.297   +1.249      2       0     16 Whe 12.         11 Cow 7.           7 SELL:WHEAT=9;
                                                 Str 4              Sheep 4            SELL:STRAWBERRY=1;
                                                                                       SELL:WOOL=4
  --------------------------------------------------------------------------------------------------------------

**Nota:** `Δ cash` è la variazione tra gli snapshot di fine giornata.
Non equivale a revenue: incorpora contemporaneamente vendite, acquisti,
HIRE, land, seed, prodotti e animali.

## 3. Fasi economiche

### Fase A --- Day 1--4: bootstrap Q0 ad alta densità

**OSSERVATO.** Day 1: 5 HIRE, acquisto 11 Melon seed, 10 Strawberry seed
e due ordini Wheat da 9 ciascuno. A fine giornata Q0 contiene 21 crop (8
Melon, 7 Strawberry, 6 Wheat) e 4 pasture. Cash 928. Nei Day 2--4 la
struttura resta sostanzialmente invariata e vengono riassunti 5
Hands/giorno.

**INFERENZA.** `truebelief` sacrifica liquidità immediata per costruire
contemporaneamente tre asset: crop ad alto valore, Wheat operativo e
infrastruttura pasture. Non aspetta Q1 per diversificare.

### Fase B --- Day 5--10: accumulo controllato e pre-livestock

**OSSERVATO.** Prima Cow acquistata Day 5 dopo vendite Wheat; seconda
Day 9. Q0 resta l'unico quadrante. La prima Cow compare piazzata nel
farm state al Day 10. Il cash resta compresso tra 876 e 684.

**INFERENZA.** L'agente tollera \~10 giorni di liquidità bassa senza
comprare terra. Il capitale viene indirizzato prima a capacità
produttiva e livestock con payoff differito.

### Fase C --- Day 11--14: espansione e costruzione del portfolio

**OSSERVATO.** Day 11 vende 24 Melon, compra Q1, acquista 5 Cow e nuovi
seed. Day 12 vende altri 24 Melon e 7 Strawberry, compra 2 Cow + 5 Sheep
e 26 Wheat prodotto. Entro Day 14 risultano attivi 7 Cow + 4 Sheep, 11
pasture e 37 crop. Cash 6.515.

**INFERENZA.** Q1 viene comprato quando l'opening ha già generato una
prima monetizzazione importante. L'espansione non precede il motore
economico: lo segue.

### Fase D --- Day 15--18: stabilizzazione del motore Q0+Q1

**OSSERVATO.** 39 crop, 11 pasture, 7 Cow + 4 Sheep. Il mix si
stabilizza intorno a 19 Strawberry, 10 Wheat, 10 Melon, poi al Day 18
passa a 17 Wheat, 12 Strawberry, 10 Melon. Cash sale da 6.595 a 10.810.

**INFERENZA.** Questa è la fase di maturazione degli asset acquistati
nei giorni precedenti. La farm ha raggiunto la massima superficie crop
osservata, ma non ancora la massima velocità di cash generation.

### Fase E --- Day 19--24: accensione del compounding

**OSSERVATO.** Day 19 compaiono per la prima volta vendite Wool e Milk.
Da Day 19 a Day 24 il cash passa 17.467 → 53.135. Si vendono
contemporaneamente Milk, Wool, Fertilizer, Wheat e crop. Il numero di
crop scende da 39 a 30.

**INFERENZA.** Il benchmark entra in regime multi-engine: raccolti
maturi + livestock + fertilizer + Wheat trading/feeding. La riduzione
dei crop tile non impedisce l'accelerazione perché la variabile
dominante diventa il flusso di asset maturi monetizzati.

### Fase F --- Day 25--30: harvest/liquidation endgame

**OSSERVATO.** Il crop mix si semplifica progressivamente verso Wheat +
Strawberry; Melon scompare entro Day 24. Cash 57.172 → 86.297. Day 29 e
Day 30 non risultano Hands a fine giornata. Restano 7 Cow + 4 Sheep
attive, 2 Cow + 1 Sheep nello shed e piccoli inventari non liquidati.

**INFERENZA.** L'endgame riduce investimenti e superficie da mantenere,
privilegiando conversione e vendita. È coerente con una policy
time-to-cash/horizon-aware.

## 4. Ledger aggregato delle azioni di mercato

### Acquisti

  Categoria     Prodotto       Quantità osservata
  ------------- ------------ --------------------
  BUY_SEED      MELON                          21
  BUY_SEED      STRAWBERRY                     22
  BUY_SEED      WHEAT                          86
  BUY_PRODUCT   WHEAT                         171
  BUY_ANIMAL    COW                             9
  BUY_ANIMAL    SHEEP                           5
  HIRE          Hands                         231
  BUY_LAND      Q1                              1

### Vendite

  Prodotto       Quantità venduta osservata
  ------------ ----------------------------
  WHEAT                                 268
  FERTILIZER                            138
  MILK                                  134
  MELON                                 108
  WOOL                                   70
  STRAWBERRY                             69

### Lettura

Il replay mostra un'economia a **sei flussi di vendita**: Wheat 268,
Fertilizer 138, Milk 134, Melon 108, Wool 70, Strawberry 69. Non
compaiono vendite Carrot, Tomato o Egg. Questa composizione deve essere
considerata un'evidenza specifica del seed/episode, non una policy
universale.

## 5. Workforce e throughput

### Azioni aggregate

  Operazione             Farmer   Hands   Totale
  -------------------- -------- ------- --------
  WEST                      114     858      972
  NORTH                     107     844      951
  PASS                       87     750      837
  WATER                      95     717      812
  EAST                       79     692      771
  SOUTH                      57     455      512
  HARVEST                    44     172      216
  CARE                       10     174      184
  FEED                       47     137      184
  PICKUP                     29     123      152
  COLLECT_FERTILIZER         12     126      138
  PLACE                      17     105      122
  PLANT                      16     103      119
  BUILD_PASTURE               3       8       11
  DIG                         3       6        9

### OSSERVATO

-   231 HIRE complessivi.
-   Hands: 172 HARVEST, 137 FEED, 174 CARE, 126 COLLECT_FERTILIZER, 103
    PLANT, 717 WATER.
-   Farmer: 44 HARVEST, 47 FEED, 10 CARE, 12 COLLECT_FERTILIZER.
-   La maggioranza delle azioni di movimento è eseguita dalle Hands; il
    sistema compra quindi parallelismo e accetta un elevato volume di
    routing.

### INFERENZA

Il benchmark non supporta una strategia che minimizzi HIRE come
obiettivo primario. Supporta invece un criterio marginale: comprare
capacità quando il valore degli asset da servire/raccogliere supera il
costo del parallelismo.

## 6. Livestock: pipeline osservata

### Cronologia

-   Day 5: prima `BUY_ANIMAL COW`.
-   Day 9: seconda Cow acquistata.
-   Day 10: prima Cow osservata su pasture.
-   Day 11: +5 Cow acquistate; 3 Cow risultano attive a fine giornata.
-   Day 12: +2 Cow e +5 Sheep acquistate; 6 Cow + 2 Sheep attive.
-   Day 13: 7 Cow + 3 Sheep.
-   Day 14: configurazione stabile 7 Cow + 4 Sheep su 11 pasture.
-   Day 19: prima vendita osservata di Wool e Milk.
-   Day 19--29: Milk viene venduto quasi quotidianamente; Wool a
    intervalli.
-   Fine episodio: 7 Cow + 4 Sheep attive; 2 Cow + 1 Sheep ancora nello
    shed.

### Quantità aggregate

-   Cow acquistate: **9**; attive finali: **7**; shed finale: **2**.
-   Sheep acquistate: **5**; attive finali: **4**; shed finale: **1**.
-   Milk venduto: **134**.
-   Wool venduto: **70**.
-   Fertilizer venduto: **138**.
-   Wheat prodotto acquistato dal mercato: **171**, coerente con un
    fabbisogno feed/commodity non coperto soltanto dalla coltivazione
    interna.

### Implicazione per X1.12

La pipeline livestock non va modellata come `cows → milk` soltanto. Il
comportamento competitivo osservato è almeno
`Cow + Sheep → feed/care → Milk + Wool + Fertilizer → logistics → sell`,
integrato con Wheat interno e retail. Qualunque nuova architettura che
ometta Sheep/Wool/Fertilizer non sta replicando il portfolio del
benchmark.

## 7. Crop portfolio e transizione per fase

### OSSERVATO

-   Day 1--10: mix fisso 8 Melon + 7 Strawberry + 6 Wheat.
-   Day 11--17: espansione del mix su Q1 fino a 39 crop; picco 19
    Strawberry + 10 Wheat + 10 Melon.
-   Day 18--20: 17 Wheat + 12 Strawberry + 10 Melon.
-   Day 21--24: Melon viene progressivamente liquidato e non
    rimpiazzato: 7 → 5 → 1 → 0.
-   Day 24--27: 18 Wheat + 12 Strawberry.
-   Day 28--30: progressiva contrazione endgame fino a 12 Wheat + 4
    Strawberry.
-   Carrot e Tomato: **0 tile osservati nel mix di fine giornata** e
    nessun acquisto seed registrato.

### INFERENZA

Il portfolio è fortemente horizon-aware. Melon è centrale
nell'opening/growth e viene eliminato nell'endgame; Wheat acquista peso
relativo; Strawberry resta fino agli ultimi giorni. Questo è
incompatibile con un crop selector statico basato solo sul prezzo
corrente.

## 8. Wheat come commodity operativa

### OSSERVATO

-   BUY_SEED Wheat: **86**.
-   BUY_PRODUCT Wheat: **171**.
-   SELL Wheat: **268**.
-   Wheat è presente nei crop tile durante l'intero episodio.
-   Numerosi giorni mostrano contemporaneamente acquisto retail Wheat e
    vendite/gestione Wheat in altre fasi.

### INFERENZA

Il Wheat non è semplicemente `feed da autoprodurre`. È una risorsa di
bilanciamento tra produzione, feed, inventory e mercato. Per gli agenti
successivi: non imporre un cap arbitrario al retail Wheat; stimare
invece il valore marginale del Wheat acquistato rispetto a livestock
preservato, time-to-cash e prezzo di mercato.

## 9. Q1: timing e utilizzo

### OSSERVATO

-   Day 1--10: solo NW/Q0.
-   `BUY_LAND` avviene Day 11 dopo una vendita importante di Melon.
-   A fine Day 11 i crop scendono temporaneamente a 17 mentre vengono
    riallocati asset e animali.
-   Day 12: 22 crop + 9 pasture; Day 14: 37 crop + 11 pasture; Day 15:
    39 crop + 11 pasture.
-   Nessun Q2 acquistato nell'intero episodio.

### INFERENZA

Il benchmark dimostra che Q0+Q1 hanno capacità economica sufficiente per
almeno 86.297 sul seed osservato. La domanda per X1.12 non è
`come comprare più terra`, ma
`come replicare la sequenza che rende Q1 un moltiplicatore invece di un costo anticipato`.

## 10. Cash trajectory e punto di svolta

  Milestone      Money   Variazione dalla milestone precedente
  ----------- -------- ---------------------------------------
  Day 1            928                                  -2.072
  Day 5            876                                     -52
  Day 10           684                                    -192
  Day 11         1.794                                  +1.110
  Day 14         6.515                                  +4.721
  Day 18        10.810                                  +4.295
  Day 19        17.467                                  +6.657
  Day 20        24.778                                  +7.311
  Day 24        53.135                                 +28.357
  Day 29        85.048                                 +31.913
  Day 30        86.297                                  +1.249

### Lettura

Il vantaggio diventa **strutturalmente visibile al Day 19**, quando
entrano Milk/Wool e il cash giornaliero passa a un regime molto più
elevato. Il motore, però, viene costruito molto prima: opening Day 1,
prime Cow Day 5/9, Q1 Day 11, portfolio livestock completo Day 14. Il
lag tra investimento e accelerazione è quindi parte essenziale
dell'architettura.

## 11. Endgame e capitale residuo

### OSSERVATO al Day 30

-   Money: **86.297**
-   Crop: 16 = 12 Wheat + 4 Strawberry.
-   Pasture: 11; livestock attivo 7 Cow + 4 Sheep.
-   Shed: 2 Cow + 1 Sheep.
-   Worker inventories aggregate: Milk 4 + Wheat 4 + Wool 2.
-   Seed residui: Melon 3 + Strawberry 3 + Wheat 4.
-   Weed: 7.

### INFERENZA

Il benchmark non è perfettamente liquidato né fisicamente pulito. Quindi
copiare la forma finale della mappa sarebbe un errore. Il valore è nella
traiettoria e nel sequencing, non nello snapshot Day 30.

## 12. Confronto operativo con X1.11

Il benchmark locale X1.11 sullo stesso seed è **24.827**, contro
**86.297** di `truebelief`: gap **61.470**, X1.11 vale circa **28,8%**
del benchmark e `truebelief` circa **3,48×** X1.11.

### Root causes da usare come ipotesi per il prossimo DEFINE

  -----------------------------------------------------------------------
  Priorità                Differenza              Evidenza dal replay
  ----------------------- ----------------------- -----------------------
  PRIMARY                 Sequencing/capital      `truebelief` resta 10
                          deployment              giorni su Q0, compra Q1
                                                  solo Day 11 dopo
                                                  monetizzazione; X1.11
                                                  deve evitare
                                                  espansione/costi prima
                                                  del payoff del motore
                                                  precedente.

  PRIMARY                 Portfolio multi-engine  Crop diversificato Day
                                                  1 + 7 Cow + 4 Sheep +
                                                  Milk/Wool/Fertilizer;
                                                  X1.11 non monetizza
                                                  livestock.

  PRIMARY                 Cash-conversion         Day 19--29: +67k circa
                          throughput              mentre crop tile
                                                  scendono; valore
                                                  realizzato/giorno
                                                  domina CPS.

  MATERIAL                Workforce elasticity    231 HIRE, 9--12
                                                  Hands/giorno in regime:
                                                  parallelismo acquistato
                                                  quando serve.

  MATERIAL                Wheat market            171 BUY_PRODUCT Wheat e
                          integration             268 SELL Wheat:
                                                  feed/inventory/market
                                                  sono un unico
                                                  sottosistema.

  MATERIAL                Horizon-aware crop mix  Melon opening/growth,
                                                  poi phase-out;
                                                  Strawberry/Wheat
                                                  persistono.

  SECONDARY               Perfect liquidation     Rimangono animali e
                                                  inventory inutilizzati;
                                                  non è necessario per
                                                  raggiungere 86k.
  -----------------------------------------------------------------------

## 13. Vincoli per gli agenti che useranno questo documento

1.  **Non trasformare correlazione in causalità.** Il replay mostra cosa
    ha fatto `truebelief`, non il counterfactual di cosa sarebbe
    successo senza una singola leva.
2.  **Non copiare numeri come costanti.** `5 Hands Day 1`, `7 Cow`,
    `4 Sheep`, `11 pasture` e i crop count sono osservazioni di un seed,
    non parametri universalmente ottimali.
3.  **Non reintrodurre Q2** per spiegare il gap: il benchmark raggiunge
    86.297 con due quadranti.
4.  **Non usare CPS come goal.** La fase più redditizia coincide con
    contrazione della superficie crop.
5.  **Non vietare retail Wheat per principio.** Il benchmark lo usa
    pesantemente; serve una regola EV-based.
6.  **Non ridurre livestock a Cow/Milk.** Sheep/Wool/Fertilizer sono
    parte del motore osservato.
7.  **Non ottimizzare micro-routing prima del sequencing economico.** Il
    gap X1.11 è di oltre 61k.
8.  **Preservare la provenance.** Ogni nuovo claim su `truebelief` deve
    essere riconducibile al replay raw o marcato come inferenza.

## 14. Domande aperte da verificare sperimentalmente

-   Quale quota del +67k Day 19--29 è attribuibile a crop, Milk, Wool,
    Fertilizer e Wheat trading, ai prezzi effettivi di ogni transazione?
-   Le 2 Cow + 1 Sheep non piazzate sono buffer intenzionale, overbuy
    opportunistico o inefficienza?
-   Qual è il ROI marginale della settima Cow e della quarta Sheep
    rispetto a un tile crop?
-   Quanto del vantaggio deriva dalla market-price curve e quanto dalla
    pura produzione?
-   Qual è il valore del `CARE` sugli animali nel ciclo economico
    complessivo?
-   Quanti harvest avvengono entro 0/1/2 turni dalla maturità e come si
    confronta con X1.11?
-   Qual è il vero payback di Q1 se si ricostruiscono prezzi e costi
    transazione-per-transazione?
-   La stessa policy mantiene l'ordine di grandezza su altri seed o
    questo episodio è particolarmente favorevole?

## 15. Dataset giornaliero dettagliato per uso agentico

La tabella seguente aggiunge inventory e contatori operativi, utile per
parser/agent review.

  -------------------------------------------------------------------------------------------------
        Day     Money   Productive   Movement      PASS Shed       Worker          Seeds nonzero
                               ops                      nonzero    inventory       
                                                                   nonzero         
  --------- --------- ------------ ---------- --------- ---------- --------------- ----------------
          1       928           46         44        44 ---        ---             MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:12

          2       916           21         43        75 ---        ---             MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:12

          3       904           21         43        75 ---        ---             MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:12

          4       892           21         43        75 ---        ---             MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:12

          5       876           40         84        15 ---        COW:1           MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:6

          6       864           22         44        73 ---        COW:1           MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:6

          7       852           22         44        73 ---        COW:1           MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:6

          8       840           22         44        73 ---        COW:1           MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:6

          9       718           40         83        16 ---        COW:2. WHEAT:3  MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:4

         10       684           29         49        61 WHEAT:3    COW:1           MELON:3.
                                                                                   STRAWBERRY:3.
                                                                                   WHEAT:4

         11     1.794           55         78         6 COW:4.     FERTILIZER:1.   MELON:8.
                                                        WHEAT:4    WHEAT:1.        STRAWBERRY:13.
                                                                   MELON:24.       WHEAT:26
                                                                   STRAWBERRY:7    

         12     5.223           68         91         1 SHEEP:1.   COW:3.          MELON:6.
                                                        WHEAT:13   FERTILIZER:2.   STRAWBERRY:10.
                                                                   WHEAT:11.       WHEAT:26
                                                                   SHEEP:2         

         13     4.969           84        114        29 COW:1      STRAWBERRY:7.   MELON:4.
                                                                   WHEAT:40.       STRAWBERRY:7.
                                                                   COW:1.          WHEAT:25
                                                                   FERTILIZER:3.   
                                                                   SHEEP:2         

         14     6.515           85        144        22 COW:2.     WHEAT:28.       MELON:3.
                                                        SHEEP:1.   FERTILIZER:4    STRAWBERRY:3.
                                                        WHEAT:5                    WHEAT:18

         15     6.595           89        149        14 COW:2.     FERTILIZER:5.   MELON:3.
                                                        SHEEP:1.   STRAWBERRY:7.   STRAWBERRY:3.
                                                        WHEAT:7    WHEAT:26        WHEAT:15

         16     8.326           77        139        15 COW:2.     WHEAT:26.       MELON:3.
                                                        SHEEP:1.   FERTILIZER:5    STRAWBERRY:3.
                                                        WHEAT:7                    WHEAT:15

         17     8.844           84        154        13 COW:2.     STRAWBERRY:6.   MELON:3.
                                                        SHEEP:1.   WHEAT:29.       STRAWBERRY:3.
                                                        WHEAT:4    FERTILIZER:2    WHEAT:14

         18    10.810          110        131        11 COW:2.     MILK:6.         MELON:3.
                                                        SHEEP:1    WHEAT:47.       STRAWBERRY:3.
                                                                   WOOL:11.        WHEAT:4
                                                                   FERTILIZER:5    

         19    17.467           93        159        21 COW:2.     WHEAT:25.       MELON:3.
                                                        SHEEP:1.   FERTILIZER:3.   STRAWBERRY:3.
                                                        WHEAT:8    MILK:6. WOOL:5  WHEAT:4

         20    24.778           96        178        21 COW:2.     FERTILIZER:5.   MELON:3.
                                                        SHEEP:1.   MILK:6. WHEAT:6 STRAWBERRY:3.
                                                        WHEAT:27                   WHEAT:4

         21    27.587           92        143        19 COW:2.     FERTILIZER:7.   MELON:3.
                                                        SHEEP:1.   MELON:18.       STRAWBERRY:3.
                                                        WHEAT:3    WHEAT:30.       WHEAT:4
                                                                   WOOL:8. MILK:6. 
                                                                   STRAWBERRY:1    

         22    35.307          115        168        11 COW:2.     STRAWBERRY:3.   MELON:3.
                                                        SHEEP:1    WHEAT:64.       STRAWBERRY:3.
                                                                   MELON:12.       WHEAT:5
                                                                   WOOL:4.         
                                                                   FERTILIZER:5.   
                                                                   MILK:9          

         23    44.125          104        158        13 COW:2.     FERTILIZER:7.   MELON:3.
                                                        SHEEP:1    MELON:18.       STRAWBERRY:3.
                                                                   WHEAT:45.       WHEAT:4
                                                                   STRAWBERRY:3.   
                                                                   WOOL:4. MILK:6  

         24    53.135          100        180        15 COW:2.     WHEAT:20.       MELON:3.
                                                        SHEEP:1.   FERTILIZER:7.   STRAWBERRY:3.
                                                        WHEAT:13   STRAWBERRY:5.   WHEAT:4
                                                                   MILK:9          

         25    57.172           90        169        16 COW:2.     FERTILIZER:5.   MELON:3.
                                                        SHEEP:1.   STRAWBERRY:5.   STRAWBERRY:3.
                                                        WHEAT:2    WHEAT:31.       WHEAT:4
                                                                   MILK:9. WOOL:4  

         26    62.344          108        155        11 COW:2.     STRAWBERRY:7.   MELON:3.
                                                        SHEEP:1    WHEAT:66.       STRAWBERRY:3.
                                                                   FERTILIZER:5.   WHEAT:5
                                                                   WOOL:4. MILK:9  

         27    70.890           98        175         1 COW:2.     FERTILIZER:6.   MELON:3.
                                                        SHEEP:1    STRAWBERRY:4.   STRAWBERRY:3.
                                                                   WHEAT:40.       WHEAT:4
                                                                   WOOL:4. MILK:6  

         28    77.325           93        165        16 COW:2.     STRAWBERRY:5.   MELON:3.
                                                        SHEEP:1.   WHEAT:27.       STRAWBERRY:3.
                                                        WHEAT:6    FERTILIZER:8.   WHEAT:4
                                                                   MILK:6          

         29    85.048           13         20         2 COW:2.     STRAWBERRY:1.   MELON:3.
                                                        SHEEP:1    WHEAT:7. WOOL:4 STRAWBERRY:3.
                                                                                   WHEAT:4

         30    86.297            9         15         0 COW:2.     MILK:4.         MELON:3.
                                                        SHEEP:1    WHEAT:4. WOOL:2 STRAWBERRY:3.
                                                                                   WHEAT:4
  -------------------------------------------------------------------------------------------------

## 16. Fonte primaria

Replay raw: `101294736.json`. Conservare il file senza modificarlo. Per
analisi riproducibili, derivare sempre i dati strutturati dal raw invece
di ricopiare manualmente le tabelle di questo documento.

------------------------------------------------------------------------

### Sintesi operativa per X1.12

> `truebelief` dimostra sul seed 421521921 che Q0+Q1 supportano almeno
> 86.297 final money. Il comportamento osservato costruisce Q0 ad alta
> densità fin dal Day 1, introduce livestock prima di Q1, espande al Day
> 11 dopo la prima monetizzazione significativa, porta il portfolio a 7
> Cow + 4 Sheep e 39 crop, quindi dal Day 19 converte rapidamente crop +
> Milk + Wool + Fertilizer + Wheat in cash. La superficie crop
> successivamente diminuisce mentre il cash accelera. Il prossimo
> esperimento deve quindi essere progettato attorno a sequencing,
> portfolio multi-engine e cash-conversion throughput, non a
> massimizzazione della superficie fisica.
