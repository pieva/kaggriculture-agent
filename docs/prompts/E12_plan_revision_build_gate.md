# E12 — PLAN REVISION / BUILD APPROVAL GATE

## Centered Hybrid Farm Scaling — Opening progressivo e capital deployment

Il PLAN E12 è sostanzialmente approvato nella direzione strategica, ma deve essere corretto sulla base dell'osservazione dettagliata dei primi turni del replay del top player prima di procedere al BUILD.

Non implementare ancora finché non hai applicato e documentato le correzioni seguenti.

---

## 1. Nuove evidenze dal replay

È stata osservata direttamente la sequenza **Day 1, Turn 1–6** del top player.

### Evidenza A — Shed

Lo **Shed è graficamente a cavallo dei quattro tile centrali** e non occupa un tile produttivo proprio.

Pertanto NON eliminare `(4,4)` dal possibile livestock core soltanto perché coincide graficamente con lo Shed.

La proposta:

`[(3,3), (3,4), (4,3), (4,4)]`

rimane una geometria candidata valida, purché sia compatibile con le coordinate effettive dell'environment.

Verificala nel game state/API e documenta il risultato.

### Evidenza B — Il 2×2 non viene attivato tutto insieme

Il replay mostra un'attivazione **progressiva** della zona verde/livestock nei primi turni.

Quindi:

**2×2 livestock core target/reserved != 4 pasture costruite immediatamente**

Il 2×2 deve rappresentare una **capacity reservation** vicino all'origine.

Le pasture e le cow devono essere attivate progressivamente all'interno di questo spazio.

### Evidenza C — Opening estremamente aggressivo sul capitale

Cash osservato:

- Turn 1: `$3,000`
- Turn 2: `$713`
- Turn 3: `$205`
- Turn 4: `$178`
- Turn 5: `$178`
- Turn 6: `$178`

Il top player converte quindi quasi tutto il capitale iniziale in capacità produttiva nei primissimi turni.

Questo è un segnale strategico importante.

E12 NON deve adottare automaticamente una politica conservativa di cash reserve elevata.

L'ipotesi da testare diventa:

> il capitale iniziale deve essere convertito rapidamente in capacità produttiva centered, purché rimanga possibile completare il ciclo operativo successivo.

---

## 2. Correzione del paradigma E12

La strategia non deve essere modellata semplicemente come:

`cow-first`

ma come:

`capital deployment first -> progressive livestock core -> feed/crops -> reinvestment -> centered scaling`

Opening concettuale:

```text
$3,000 initial capital
        |
        v
aggressive productive investment
        |
        v
reserve centered 2×2 livestock core
        |
        v
activate Cow #1 / required pasture
        |
        v
progressively activate additional livestock capacity
        |
        v
feed + diversified crop production
        |
        v
reinvest first revenues
        |
        v
centered productive scaling
        |
        v
sustainable Q2
```

---

## 3. Livestock core: regola corretta

Mantieni come candidata la geometria:

`[(3,3), (3,4), (4,3), (4,4)]`

ma separa rigorosamente tre concetti:

1. `LIVESTOCK_CORE_RESERVED_TILES`
2. `ACTIVE_PASTURE_TILES`
3. `ACTIVE_COW_COUNT`

All'inizio:

- il 2×2 può essere riservato al livestock;
- NON devono necessariamente essere costruite quattro pasture;
- NON devono necessariamente essere acquistate quattro cow.

L'attivazione deve essere progressiva.

### Cow progression

Non imporre artificialmente:

- `MAX_COWS = 1`, oppure
- `BUILD_ALL_4_PASTURES_IMMEDIATELY`.

La policy deve consentire:

`Cow #1 -> Cow #2 -> Cow #3 -> Cow #4`

quando le condizioni economiche e operative lo permettono.

Per ogni incremento del numero di cow verificare:

- costo della pasture aggiuntiva;
- costo della cow;
- wheat/feed disponibile;
- capacità di eseguire FEED e raccolta/prodotto;
- cash necessario per non interrompere il ciclo produttivo;
- costo di movimento/lavoro;
- beneficio marginale atteso.

Il limite geometrico iniziale è la saturazione del 2×2, non un numero di cow hardcoded inferiore.

---

## 4. Feed/Wheat: eliminare il vincolo arbitrario dei 4 tile

Nel PLAN precedente era proposta una riserva fissa di almeno 4 WHEAT tile.

Non implementarla come costante senza una giustificazione quantitativa.

Ricostruisci dal motore:

- consumo WHEAT per FEED;
- frequenza FEED;
- tempo di crescita WHEAT;
- resa per tile;
- inventory behavior;
- numero massimo di cow sostenibili da un wheat tile nel tempo.

Definisci quindi una funzione/policy del tipo:

`required_wheat_capacity = f(active_cows, feed_rate, wheat_yield, cycle_time, inventory)`

La superficie WHEAT deve aumentare quando aumenta la domanda effettiva di feed.

L'obiettivo è mantenere un **feed safety loop positivo**, non replicare visivamente quattro tile osservati nel replay.

---

## 5. Pipeline Cow/Milk da verificare prima del BUILD

Il PLAN contiene formulazioni potenzialmente ambigue tra `FEED`, produzione di `MILK`, `HARVEST` e vendita.

Prima di scrivere la state machine, verifica nel codice/environment la pipeline esatta.

Documenta esplicitamente:

```text
BUY_ANIMAL
    ->
PICKUP COW
    ->
BUILD_PASTURE (ordine effettivo se diverso)
    ->
PLACE COW
    ->
FEED
    ->
[esatta trasformazione di stato]
    ->
[azione necessaria per ottenere MILK]
    ->
[inventory destination]
    ->
SELL MILK
```

Per ogni passaggio indica:

- action;
- prerequisiti;
- posizione richiesta;
- costo;
- consumo inventory;
- prodotto generato;
- destinazione del prodotto;
- eventuale cooldown/ciclo temporale.

Non implementare la pipeline basandoti soltanto sull'interpretazione del replay.

---

## 6. Q1 — verificare il vero ruolo nell'opening

Il PLAN assume Q1 precoce.

Mantieni l'ipotesi, ma verifica esattamente:

- area inizialmente accessibile;
- posizione del 2×2 livestock core;
- se Cow #1 può essere attivata prima di Q1;
- se Q1 è prerequisito tecnico oppure soltanto un investimento di scaling;
- costo opportunità di Q1 rispetto a Cow #1 e feed loop.

Confronta almeno logicamente:

```text
A: Q1 -> Cow #1
B: Cow #1 -> Q1
```

Se entrambe le sequenze sono tecnicamente possibili, scegli quella che converte più rapidamente il capitale in capacità produttiva sostenibile.

---

## 7. Q2 — rimuovere la soglia fissa `$2,500`

NON usare:

`if cash > 2500: buy Q2`

come regola primaria.

Il replay mostra che un player molto forte opera intenzionalmente con liquidità estremamente bassa nell'opening.

Q2 deve essere acquistato quando il sistema può finanziarlo senza interrompere la produzione.

Definisci invece una condizione di **sustainable reinvestment**, ad esempio concettualmente:

```text
available_cash
    >= Q2_COST
     + NEXT_REQUIRED_FEED_COST
     + NEXT_REQUIRED_SEED_COST
     + MANDATORY_OPERATION_COSTS
     + SMALL_SAFETY_MARGIN
```

La formula definitiva deve derivare dalle meccaniche reali dell'environment.

Il safety margin deve essere piccolo e giustificato, non una grande riserva arbitraria.

---

## 8. Crop diversification e geometria

Mantieni il principio E12:

- livestock nel core centrale;
- feed crops sufficientemente vicine;
- crop ROI attorno al core;
- espansione centered;
- evitare periferia a basso ROI/hour.

Ma NON copiare rigidamente la fotografia del replay.

Le coordinate delle crop devono derivare da:

1. distanza dal core/origine;
2. disponibilità del tile;
3. funzione produttiva;
4. costo operativo;
5. ROI;
6. necessità di feed;
7. compatibilità con l'espansione futura.

La strategia deve replicare il **principio economico**, non il layout grafico.

---

## 9. Opening telemetry obbligatoria

Per E12 serve una telemetria molto più fine nei primi 24 turni.

Registra **ogni turn da 1 a 24** almeno:

- cash;
- farmer position;
- current action/state;
- Q1 owned;
- Q2 owned;
- reserved livestock tiles;
- active pasture count;
- active cow count;
- WHEAT tiles;
- altri crop tiles per tipo;
- WHEAT inventory;
- MILK inventory;
- feed count cumulativo;
- milk produced/collected cumulativo;
- money earned from MILK;
- money earned from crops;
- productive tile count;
- eventuali failed/impossible actions.

Mantieni inoltre milestone sintetiche successive:

`48, 72, 120, 240, 480, 720`.

---

## 10. Metriche sperimentali E12-X1.0

Baseline primaria confermata:

**E11-X1.7 — Corner-Pruned 26t**

- Mean Final Money: `$28,083.80`
- Median: `$30,081.00`
- Peak: `$33,371.00`
- Paired Win Rate vs B3: `60% (3/5)`

E12-X1.0 deve essere confrontato direttamente con X1.7 sugli stessi seed.

### Metriche economiche

- Mean Final Money
- Median
- Standard deviation (`ddof=1`)
- Peak
- delta assoluto vs X1.7
- delta percentuale vs X1.7
- paired win rate vs X1.7

### Metriche strutturali

- turn prima Cow;
- turn Q1;
- turn Cow #2/#3/#4 se raggiunte;
- turn Q2;
- minimum opening cash;
- cash deployment entro turn 2/3/6/12/24;
- pasture count;
- active cows;
- WHEAT/feed balance;
- MILK revenue;
- crop revenue;
- productive tile count;
- max productive radius;
- movement/travel burden se misurabile.

---

## 11. Criterio di successo

Il criterio primario rimane:

**Mean Final Money E12-X1.0 > $28,083.80**

ma E12 deve essere considerato interessante anche quando il risultato finale non supera immediatamente X1.7 se mostra un miglioramento strutturale netto e diagnosticabile, ad esempio:

- forte MILK revenue;
- migliore produttività per tile;
- minore travel burden;
- crescita economica più rapida dopo l'opening;
- Q2 sostenibile;
- chiara evidenza che il numero/timing delle cow è la leva da ottimizzare nella successiva iterazione.

Non dichiarare successo sulla base di un singolo seed.

---

## 12. Revisione richiesta prima del BUILD

Ora:

1. verifica le coordinate del 2×2 rispetto allo Shed;
2. conferma che lo Shed non consumi un tile produttivo;
3. verifica la pipeline completa Cow -> Milk;
4. calcola il fabbisogno WHEAT per cow;
5. determina se Q1 deve precedere Cow #1;
6. sostituisci la soglia Q2 `$2,500` con sustainable reinvestment;
7. definisci la progressione Cow #1 -> #4;
8. definisci la state machine aggiornata;
9. aggiorna il piano E12;
10. mostra le modifiche rispetto al PLAN precedente.

### Approval gate

Dopo questa revisione:

- se non emergono incompatibilità meccaniche sostanziali;
- se la pipeline cow/feed/milk è verificata;
- se la geometria è valida;
- se la state machine non contiene soglie arbitrarie non motivate;

**puoi procedere direttamente al BUILD di E12-X1.0 senza richiedere un'ulteriore approvazione.**

Durante il BUILD:

- implementa la versione più semplice e misurabile della policy;
- aggiungi i test;
- esegui lo smoke test A0;
- se A0 è tecnicamente valido, esegui il benchmark paired B;
- NON effettuare tuning post-hoc sui seed del benchmark;
- restituisci risultati completi e telemetria opening prima di proporre E12-X1.1.

---

## Principio guida

Non replicare la fotografia del top player.

Replica e testa il principio che emerge dal replay:

> **convertire aggressivamente il capitale iniziale in capacità produttiva centered, attivare progressivamente il livestock core e reinvestire i ricavi senza mantenere riserve di liquidità inutilmente elevate.**
