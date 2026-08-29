# E12-X1.1 — Feed-First Cow Pipeline

## Obiettivo

E12-X1.0 ha validato la meccanica di costruzione e posizionamento del livestock core, ma ha fallito economicamente:

- 4 pasture costruite;
- 4 cow attive;
- 0 MILK raccolto;
- Mean Final Money: `$6,227.60`;
- baseline/champion E11-X1.7: `$28,083.80`.

Questo risultato NON falsifica ancora l'ipotesi E12.

Falsifica invece l'implementazione X1.0, perché il capitale e il lavoro sono stati assorbiti dalla costruzione del livestock core prima che fosse disponibile un feed loop capace di generare ricavi.

Il prossimo esperimento deve quindi isolare e risolvere esclusivamente questo collo di bottiglia.

Nome esperimento:

**E12-X1.1 — Feed-First Cow Pipeline**

Non riaprire l'intera architettura E12 e non effettuare tuning opportunistico sulle altre componenti.

---

## 1. Ipotesi X1.1

### H12-X1.1

Una cow early può diventare economicamente sostenibile se:

1. il WHEAT necessario viene prodotto e reso effettivamente disponibile prima del bisogno di FEED;
2. viene attivata inizialmente una sola cow;
3. la cow completa rapidamente un ciclo produttivo verificato;
4. il MILK viene effettivamente raccolto e monetizzato;
5. una cow successiva viene attivata soltanto dopo che il sistema ha dimostrato di poter sostenere quella precedente.

La progressione target non è:

`4 pasture -> 4 cow -> wheat -> feed`

ma:

`WHEAT READY -> Cow #1 -> FEED -> MILK -> SELL -> Cow #2 -> ...`

---

## 2. Invariante principale

Implementare una regola forte:

> **Non attivare Cow N+1 finché il sistema non ha dimostrato di poter alimentare e monetizzare Cow N, oppure non dispone già del feed buffer verificato necessario a sostenere l'incremento.**

Per X1.1 il bootstrap deve quindi iniziare con:

- livestock core 2×2 ancora RISERVATO;
- una sola pasture inizialmente ATTIVA;
- una sola cow inizialmente ATTIVA;
- capacità restante del 2×2 non costruita finché non viene superato il gate produttivo.

Il limite iniziale di una cow è un **bootstrap gate sperimentale**, non il target finale della strategia E12.

---

## 3. Prima del BUILD: diagnosi obbligatoria della pipeline

Prima di modificare la policy, usa l'environment per ricostruire con certezza l'intera catena:

```text
BUY_SEED WHEAT
    ->
PICKUP WHEAT seed
    ->
PLANT WHEAT
    ->
WATER / growth requirements
    ->
HARVEST WHEAT
    ->
[dove finisce il WHEAT?]
    ->
[come diventa disponibile per FEED?]
    ->
FEED cow
    ->
[esatta trasformazione dello stato della pasture/cow]
    ->
[tempo/cooldown]
    ->
[azione che genera o raccoglie MILK]
    ->
[dove finisce MILK?]
    ->
SELL MILK
    ->
cash
```

Per ogni passaggio documenta:

- comando engine esatto;
- prerequisiti;
- posizione del farmer;
- costo;
- inventory prima/dopo;
- tile state prima/dopo;
- eventuale cooldown;
- numero di turn richiesti;
- prodotto risultante.

Non assumere che `FEED` produca immediatamente MILK.
Non assumere che `HARVEST` sia l'azione corretta senza verificarlo.
Non assumere dove WHEAT e MILK vengano depositati.

Crea, se utile, uno script diagnostico minimale separato che esegua una sola pipeline controllata.

---

## 4. Feed-first bootstrap

Una volta verificata la meccanica, modifica E12 in modo che la priorità iniziale sia creare un **feed buffer realmente utilizzabile**.

La state machine deve distinguere almeno:

```text
BOOTSTRAP_WHEAT
WAIT_WHEAT_READY
HARVEST_WHEAT
ACTIVATE_COW_1
FEED_COW
WAIT_PRODUCT
COLLECT_MILK
SELL_MILK
PRODUCTION_CONFIRMED
SCALE_LIVESTOCK
```

I nomi possono essere adattati all'architettura esistente, ma gli stati logici devono essere distinguibili in telemetria.

### Vincolo

Non costruire pasture successive mentre la pipeline Cow #1 è ancora bloccata in uno degli stati precedenti, salvo azioni gratuite/non interferenti dimostrate come tali.

---

## 5. Wheat capacity

Non usare `4 WHEAT tiles` come costante.

Per Cow #1 determina empiricamente il minimo necessario per:

- produrre il primo feed;
- evitare starvation immediata dopo il primo ciclo;
- mantenere contemporaneamente una componente crop capace di generare cash.

Definisci:

```text
feed_buffer_required(active_cows)
```

in base alle meccaniche verificate.

La policy deve scalare la superficie WHEAT soltanto quando il numero di cow o il consumo reale lo richiedono.

Registra separatamente:

- WHEAT planted;
- WHEAT ready;
- WHEAT harvested;
- WHEAT available for FEED;
- WHEAT consumed.

---

## 6. Progressive Cow Gate

Cow #2 può essere attivata soltanto quando Cow #1 ha superato un gate esplicito.

Preferenza per X1.1:

```text
Cow #1 placed
AND
Cow #1 successfully fed
AND
MILK successfully obtained
AND
MILK successfully sold
AND
feed capacity remains sufficient
AND
next productive cycle remains fundable
```

Solo allora:

```text
activate Cow #2
```

Applicare lo stesso principio a Cow #3 e Cow #4.

Se il benchmark mostra che questo gate è troppo conservativo, sarà materia di X1.2. NON anticipare quel tuning in X1.1.

---

## 7. Capital deployment

Mantieni il principio emerso dal replay:

> convertire rapidamente il capitale iniziale in capacità produttiva.

Ma distinguere:

**productive capital deployment** da **premature infrastructure deployment**.

Una pasture senza feed e una cow che non produce MILK sono capitale immobilizzato.

Quindi la priorità economica X1.1 deve essere:

1. feed capability;
2. prima cow produttiva;
3. monetizzazione;
4. reinvestimento;
5. livestock expansion.

Non mantenere grandi cash reserve arbitrarie, ma non spendere capitale in pasture/cow che non possono entrare rapidamente in produzione.

---

## 8. Crop strategy

Per X1.1 NON effettuare un nuovo tuning generale della crop strategy.

Mantieni il più possibile:

- geometria centered;
- logica E11-X1.7 dove compatibile;
- livestock core 2×2 riservato;
- superficie crop attorno al core.

L'unica modifica agricola autorizzata è quella necessaria a:

- produrre WHEAT;
- sostenere il feed loop;
- evitare che la produzione WHEAT distrugga completamente il cash flow crop.

Non usare i seed del benchmark per scegliere ex post crop mix o soglie.

---

## 9. Q1 e Q2

### Q1

Mantieni il comportamento già verificato salvo che interferisca direttamente con il feed-first bootstrap.

Se emerge un conflitto `Q1 vs feed/cow activation`, documentalo esplicitamente.

### Q2

Per X1.1 Q2 NON è una priorità sperimentale.

Non effettuare tuning del timing Q2.

Se viene raggiunto naturalmente e in modo sostenibile, registralo.
Se non viene raggiunto, non considerarlo un fallimento di X1.1.

La domanda sperimentale è prima di tutto:

> **riusciamo a chiudere presto e ripetutamente WHEAT -> FEED -> MILK -> CASH?**

---

## 10. Telemetria obbligatoria

### Turn 1–48

Per X1.1 estendere la telemetria turn-by-turn almeno fino al turn 48.

Registrare:

- turn;
- state machine state;
- cash;
- farmer position;
- farmer action;
- market actions;
- Q1/Q2;
- pasture reserved;
- pasture built;
- cow purchased;
- cow placed;
- active cow count;
- WHEAT seed inventory;
- WHEAT planted;
- WHEAT growth/ready state;
- WHEAT harvested;
- WHEAT feed-available;
- FEED attempts;
- successful FEED count;
- cow/pasture state dopo FEED;
- MILK generated;
- MILK collected;
- MILK inventory;
- MILK sold;
- cumulative MILK revenue;
- cumulative crop revenue;
- failed/impossible actions.

### Eventi milestone

Registrare esplicitamente:

- `FIRST_WHEAT_PLANTED`
- `FIRST_WHEAT_READY`
- `FIRST_WHEAT_HARVESTED`
- `FIRST_COW_BOUGHT`
- `FIRST_COW_PLACED`
- `FIRST_SUCCESSFUL_FEED`
- `FIRST_MILK_AVAILABLE`
- `FIRST_MILK_COLLECTED`
- `FIRST_MILK_SOLD`
- `COW_2_ACTIVATED`
- `COW_3_ACTIVATED`
- `COW_4_ACTIVATED`

Ogni milestone deve includere almeno `turn` e `cash`.

---

## 11. Test richiesti

Aggiorna `tests/test_e12_centered_hybrid.py` o crea test specifici X1.1.

Verificare almeno:

1. il 2×2 rimane riservato;
2. all'avvio viene costruita una sola pasture;
3. Cow #2 non viene attivata prima del production gate;
4. WHEAT ha priorità sufficiente per completare il primo feed;
5. FEED viene realmente eseguito;
6. MILK viene realmente prodotto/raccolto secondo la meccanica engine;
7. MILK viene venduto;
8. dopo la vendita la state machine può sbloccare Cow #2;
9. nessuna regressione nei test esistenti.

Eseguire:

`.venv\Scripts\pytest.exe tests/`

---

## 12. Stage A0 — criterio molto più severo

Prima del benchmark B eseguire:

`scripts/benchmark_e12_x1.py --stage A0`

oppure aggiornare il runner con variante X1.1.

### A0 PASS soltanto se:

- almeno una Cow è stata collocata;
- almeno un FEED ha avuto successo;
- almeno una unità/evento MILK è stata effettivamente ottenuta;
- almeno una vendita MILK è stata completata;
- il cash è aumentato per effetto della vendita;
- la provenance è valida.

Se:

`MILK == 0`

A0 è **FAIL**.

In tal caso NON eseguire Stage B.

Continuare esclusivamente la diagnosi della pipeline finché il ciclo minimo non è dimostrato.

---

## 13. Stage A1 consigliato

Dopo A0, prima dei cinque seed completi, esegui un secondo smoke test sul seed `100`.

Obiettivo:

verificare che il ciclo non funzioni soltanto sul seed 0.

A1 PASS con gli stessi criteri funzionali di A0.

Solo dopo A0 + A1 PASS procedere a Stage B.

---

## 14. Stage B

Usare gli stessi paired seed:

`0, 100, 200, 300, 400`

e gli stessi opponent già utilizzati.

Baseline primaria:

**E11-X1.7 — Corner-Pruned 26t**

- Mean Final Money: `$28,083.80`
- Median: `$30,081.00`
- Peak: `$33,371.00`.

Confrontare almeno:

- Mean Final Money;
- Median;
- Standard deviation `ddof=1`;
- min/max;
- delta assoluto;
- delta percentuale;
- paired win rate vs X1.7.

Aggiungere:

- first cow turn;
- first successful feed turn;
- first milk turn;
- first milk sale turn;
- total feeds;
- total milk;
- MILK revenue;
- cow count finale;
- pasture count finale;
- WHEAT production/consumption;
- crop revenue.

---

## 15. Criterio di interpretazione

Non richiediamo necessariamente che X1.1 batta immediatamente `$28,083.80`.

X1.1 deve prima dimostrare che la componente livestock è **produttiva e monetizzabile**.

### Caso A — Pipeline non funziona

`MILK == 0`

E12 rimane non valutabile economicamente.
Continuare diagnosi meccanica.

### Caso B — Pipeline funziona ma peggiora drasticamente il risultato

MILK > 0, ma final money rimane molto inferiore a X1.7.

Conclusione possibile:

- cow economics insufficienti;
- feed burden eccessivo;
- activation timing errato.

Analizzare prima di scalare.

### Caso C — Pipeline funziona e recupera gran parte del gap

Segnale forte che X1.0 era principalmente un errore di sequencing.

Passare a X1.2 per ottimizzare timing/numero cow.

### Caso D — Pipeline funziona e supera X1.7

H12 riceve una prima conferma forte.

Procedere con scaling controllato, senza tuning post-hoc sui seed.

---

## 16. Provenance

Mantenere il protocollo SHA-256 già utilizzato.

Ogni Stage A0/A1/B deve essere associato inequivocabilmente a:

- config;
- source hash;
- benchmark runner;
- seed;
- opponent;
- episode output.

Nessun confronto deve mescolare artefatti provenienti da build differenti.

---

## 17. Output richiesto

Al termine restituisci:

### A. Pipeline verification
Tabella completa delle azioni engine verificate per WHEAT -> FEED -> MILK -> SELL.

### B. Modifiche X1.1
File, funzioni e policy modificate.

### C. Test
Esito suite completa.

### D. Stage A0
Telemetria dettagliata del primo ciclo produttivo.

### E. Stage A1
Verifica sul secondo seed.

### F. Stage B
Solo se A0 e A1 hanno entrambi dimostrato MILK > 0 e vendita riuscita.

### G. Diagnosi
Confronto con E12-X1.0 ed E11-X1.7.

### H. Raccomandazione
Una sola delle seguenti:

- `CONTINUE PIPELINE DEBUG`
- `PROCEED E12-X1.2`
- `HOLD E12 / RETAIN E11-X1.7`

Non preparare una nuova submission Kaggle E12 finché la strategia non dimostra un vantaggio locale sufficientemente credibile.

---

## Approval

Questo prompt costituisce autorizzazione a:

1. diagnosticare la pipeline;
2. implementare E12-X1.1;
3. eseguire test;
4. eseguire A0;
5. eseguire A1;
6. eseguire Stage B esclusivamente se A0 e A1 superano i gate funzionali.

Non richiedere un'ulteriore approvazione tra questi passaggi.

Fermati invece se il ciclo WHEAT -> FEED -> MILK -> SELL non può essere dimostrato nell'environment.

---

## Principio guida X1.1

> **Prima dimostra che una cow può produrre reddito. Poi scala le cow.**

E12-X1.1 deve trasformare il livestock da infrastruttura immobilizzata a ciclo produttivo misurabile.
