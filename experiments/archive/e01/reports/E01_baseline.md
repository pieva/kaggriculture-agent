# E01 — Architettura e funzionamento della baseline

## 1. Obiettivo della prima versione

La versione E01 non nasce con l'obiettivo di essere già competitiva nella competizione Kaggriculture. Il suo compito è più elementare e, allo stesso tempo, più importante: costruire una prima catena completa e verificabile che permetta a un agente di:

1. ricevere lo stato della simulazione;
2. interpretarlo;
3. prendere una decisione;
4. restituire un'azione valida;
5. completare una stagione senza errori;
6. essere valutato automaticamente;
7. essere trasformato nel file standalone richiesto da Kaggle.

La strategia scelta, `CarrotLoopAgent`, è volutamente minimale. Il farmer rimane sulla singola casella iniziale e realizza continuamente un ciclo di produzione delle carote.

La semplicità della strategia permette di separare due problemi che nelle iterazioni successive diventeranno progressivamente più complessi:

- **far funzionare correttamente l'agente nell'ambiente Kaggriculture**;
- **rendere intelligente la strategia dell'agente**.

E01 affronta soprattutto il primo.

---

## 2. Struttura generale del software

Il nucleo applicativo è organizzato nel package `src/agricola/`:

```text
src/
└── agricola/
    ├── agent.py
    ├── core/
    │   ├── state.py
    │   └── actions.py
    ├── baseline/
    │   └── carrot_loop.py
    └── evaluation/
        └── runner.py
```

A questi componenti si aggiungono:

```text
scripts/
├── build_submission.py
└── run_eval.py

submission/
└── submission.py

tests/
├── test_baseline.py
└── test_submission.py

results/
└── e01_baseline.json
```

La struttura separa quindi quattro responsabilità:

```text
INTERPRETAZIONE DELLO STATO
        GameState
            ↓
DECISIONE
        CarrotLoopAgent
            ↓
COSTRUZIONE DELL'AZIONE
        ActionBuilder
            ↓
INTERFACCIA KAGGLE
        agent()
```

Accanto a questa catena principale esistono due infrastrutture indipendenti:

```text
VALUTAZIONE
runner → benchmark → metriche

DELIVERY
build_submission.py → submission.py → Kaggle
```

Questa separazione è importante perché le strategie future potranno cambiare senza dover ricostruire ogni volta il sistema di valutazione o l'interfaccia con Kaggle.

---

## 3. `GameState`: trasformare l'osservazione in uno stato utilizzabile

A ogni turno Kaggriculture consegna all'agente una struttura `observation` che contiene numerose informazioni relative alla simulazione.

`src/agricola/core/state.py` introduce la classe `GameState`, che costituisce un livello di astrazione sopra questa struttura.

Il costruttore estrae, tra le altre informazioni:

- step, giorno e ora;
- identificativo del giocatore;
- capitale disponibile;
- posizione del farmer;
- stato della griglia;
- magazzino;
- semi disponibili;
- prezzi e inventario del mercato;
- stato della fattoria avversaria.

Espone poi metodi come:

```python
state.current_tile()
state.get_seed_count("CARROT")
state.get_shed_count("CARROT")
state.get_price(...)
```

La strategia non deve quindi conoscere direttamente la struttura interna dell'oggetto `observation`.

Questa distinzione diventerà particolarmente utile nelle versioni successive. E01 utilizza soltanto una piccola parte delle informazioni già disponibili: la classe conosce l'intera griglia, la posizione del farmer, il mercato e perfino la fattoria avversaria, mentre la baseline usa quasi esclusivamente la casella corrente, il capitale, i semi e il magazzino.

L'architettura contiene quindi già più informazioni di quante la prima strategia sia in grado di sfruttare.

---

## 4. `ActionBuilder`: trasformare una decisione in un'azione valida

Se `GameState` traduce l'ambiente verso l'agente, `ActionBuilder` opera nella direzione opposta.

`src/agricola/core/actions.py` costruisce la struttura che deve essere restituita a Kaggriculture:

```python
{
    "farmer": ...,
    "hands": ...,
    "market": ...
}
```

Il builder dispone di operazioni quali:

```text
PASS
PLANT
WATER
HARVEST
MOVE
SELL
BUY_SEED
```

e garantisce che il risultato abbia sempre la forma prevista dall'ambiente.

Un aspetto importante dell'ambiente emerge già da questa struttura: l'azione del farmer e gli ordini di mercato sono **canali indipendenti**.

Lo stesso turno può quindi produrre, per esempio:

```python
{
    "farmer": ["WATER"],
    "hands": [],
    "market": [["SELL", "CARROT", 2]]
}
```

Il farmer può annaffiare mentre, nello stesso turno, vengono venduti prodotti sul mercato.

---

## 5. `CarrotLoopAgent`: la prima strategia

Il cuore decisionale della E01 si trova in:

```text
src/agricola/baseline/carrot_loop.py
```

La classe `CarrotLoopAgent` implementa una policy deterministica. Non cerca una strategia ottimale e non costruisce un piano globale della stagione.

A ogni turno osserva lo stato corrente e applica poche regole.

La logica del mercato è:

```text
SE ci sono carote nel magazzino
    → vendile tutte

SE non ci sono semi di carota
    → compra un seme
```

La logica del farmer è:

```text
SE la casella corrente è vuota
E possiedo un seme
    → PLANT CARROT

ALTRIMENTI SE contiene una carota

    SE la carota ha raggiunto il giorno di raccolta
        → HARVEST

    ALTRIMENTI SE non è stata annaffiata oggi
        → WATER

    ALTRIMENTI
        → PASS

ALTRIMENTI
    → PASS
```

Questa è sostanzialmente l'intera strategia E01.

Il farmer non esegue mai `MOVE`. Non esplora quindi la griglia e continua a utilizzare la stessa casella per tutta la stagione.

Non utilizza inoltre:

- altre colture;
- fertilizzanti;
- animali;
- farm hands;
- espansione del terreno;
- prezzi dinamici per decidere quando vendere;
- informazioni sull'avversario;
- pianificazione dei movimenti;
- ottimizzazione economica globale.

Questi limiti non rappresentano errori della E01: definiscono precisamente il punto di partenza rispetto al quale misurare le iterazioni successive.

---

## 6. `agent.py`: il punto di ingresso

Kaggle non conosce direttamente `CarrotLoopAgent`.

L'interfaccia verso l'esterno è la funzione:

```python
agent(observation, configuration)
```

definita in `src/agricola/agent.py`.

Il suo lavoro è deliberatamente ridotto:

```text
observation
    ↓
GameState(observation)
    ↓
CarrotLoopAgent.act(state)
    ↓
action
```

Esiste inoltre un fallback difensivo: se durante l'elaborazione viene sollevata un'eccezione non gestita, la funzione restituisce un'azione `PASS` invece di propagare l'errore.

La scelta privilegia la robustezza: per una baseline è preferibile perdere un turno piuttosto che rischiare la squalifica dell'intero episodio.

---

## 7. Eseguire e osservare direttamente la baseline

Dopo aver verificato che la submission fosse accettata da Kaggle, è stata eseguita localmente una partita breve contro l'agente `pass`, con l'obiettivo di osservare direttamente il comportamento di `CarrotLoopAgent`.

La verifica non serve soltanto a stabilire se il programma funziona. L'obiettivo è rendere osservabile il ciclo decisionale dell'agente, collegando lo stato della simulazione alle azioni prodotte dalla policy e verificando così il comportamento effettivo della baseline.

### 7.1 Preparazione dell'ambiente

Il repository utilizza un layout `src/`. Poiché il package `agricola` non risultava installato nella `.venv`, per la sessione di ispezione è stato impostato temporaneamente `PYTHONPATH`:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

È quindi possibile verificare che il package venga importato correttamente:

```powershell
.\.venv\Scripts\python.exe -c "from agricola.agent import agent; print('Import OK:', agent)"
```

Output osservato:

```text
Import OK: <function agent at 0x000002C63AAFDDA0>
```

L'indirizzo esadecimale varia a ogni esecuzione e non ha significato funzionale. La parte importante è che Python riesce a importare correttamente la funzione `agent()`.

Questa verifica preliminare permette di distinguere eventuali problemi dell'ambiente Python da quelli relativi al comportamento dell'agente.

### 7.2 Esecuzione di una partita breve contro `pass`

La seguente istruzione esegue una simulazione locale di 120 step e stampa soltanto i momenti in cui cambia l'azione dell'agente:

```powershell
@'
import kaggle_environments
from agricola.agent import agent

env = kaggle_environments.make(
    "kaggriculture",
    configuration={"episodeSteps": 120}
)

env.run([agent, "pass"])

last_action = None

print("\n=== CARROT LOOP TRACE ===\n")

for i, step in enumerate(env.steps):
    p = step[0]
    obs = p.get("observation", {}) or {}
    action = p.get("action")

    if action == last_action:
        continue
    last_action = action

    player = obs.get("player", 0)
    farms = obs.get("farms", [])
    farm = farms[player] if farms and player < len(farms) else {}

    private = obs.get("private", {}) or {}
    seeds = private.get("seeds", {}) or {}
    shed = private.get("shed", {}) or {}

    pos = farm.get("farmer", [4, 4])
    tiles = farm.get("tiles", [])
    x, y = pos

    tile = None
    if tiles and 0 <= y < len(tiles) and 0 <= x < len(tiles[y]):
        tile = tiles[y][x]

    print(
        f"step={i:3d} "
        f"day={obs.get('day')} "
        f"hour={obs.get('hour')} "
        f"money={farm.get('money')} "
        f"seeds={seeds.get('CARROT', 0)} "
        f"shed={shed.get('CARROT', 0)}"
    )
    print(f"  tile:   {tile}")
    print(f"  action: {action}")
    print()

print("Final reward:", env.steps[-1][0].get("reward"))
'@ | .\.venv\Scripts\python.exe -
```

La scelta di limitare la simulazione a 120 step consente di osservare più di un ciclo produttivo senza dover analizzare l'intera stagione. La stampa dei soli cambiamenti di azione riduce inoltre il rumore prodotto dai numerosi turni nei quali l'agente mantiene lo stesso comportamento.

### 7.3 Output osservato

L'esecuzione ha prodotto la seguente traccia:

```text
=== CARROT LOOP TRACE ===

step=  0 day=0 hour=0 money=3000.0 seeds=0 shed=0
  tile:   None
  action: {'farmer': ['PASS'], 'hands': [], 'market': []}

step=  1 day=0 hour=1 money=2980.0 seeds=1 shed=0
  tile:   None
  action: {'farmer': ['PLANT', 'CARROT'], 'hands': [], 'market': [['BUY_SEED', 'CARROT', 1]]}

step=  2 day=0 hour=2 money=2980.0 seeds=0 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 0, 'watered_today': False, 'consecutive_unwatered': 1, 'yield_units': 1, 'max_lifespan_step': 96, 'fertilized_until_day': -1}
  action: {'farmer': ['PLANT', 'CARROT'], 'hands': [], 'market': []}

step=  3 day=0 hour=3 money=2960.0 seeds=1 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 0, 'watered_today': True, 'consecutive_unwatered': 1, 'yield_units': 1, 'max_lifespan_step': 96, 'fertilized_until_day': -1}
  action: {'farmer': ['WATER'], 'hands': [], 'market': [['BUY_SEED', 'CARROT', 1]]}

step=  4 day=0 hour=4 money=2960.0 seeds=1 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 0, 'watered_today': True, 'consecutive_unwatered': 1, 'yield_units': 1, 'max_lifespan_step': 96, 'fertilized_until_day': -1}
  action: {'farmer': ['PASS'], 'hands': [], 'market': []}

step= 25 day=1 hour=1 money=2960.0 seeds=1 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 0, 'watered_today': True, 'consecutive_unwatered': 0, 'yield_units': 1, 'max_lifespan_step': 96, 'fertilized_until_day': -1}
  action: {'farmer': ['WATER'], 'hands': [], 'market': []}

step= 49 day=2 hour=1 money=2960.0 seeds=1 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 0, 'watered_today': True, 'consecutive_unwatered': 0, 'yield_units': 2, 'max_lifespan_step': 96, 'fertilized_until_day': -1}
  action: {'farmer': ['WATER'], 'hands': [], 'market': []}

step= 73 day=3 hour=1 money=2960.0 seeds=1 shed=0
  tile:   None
  action: {'farmer': ['HARVEST'], 'hands': [], 'market': []}

step= 74 day=3 hour=2 money=2960.0 seeds=0 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 3, 'watered_today': False, 'consecutive_unwatered': 1, 'yield_units': 1, 'max_lifespan_step': 168, 'fertilized_until_day': -1}
  action: {'farmer': ['PLANT', 'CARROT'], 'hands': [], 'market': []}

step= 75 day=3 hour=3 money=2940.0 seeds=1 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 3, 'watered_today': True, 'consecutive_unwatered': 1, 'yield_units': 1, 'max_lifespan_step': 168, 'fertilized_until_day': -1}
  action: {'farmer': ['WATER'], 'hands': [], 'market': [['BUY_SEED', 'CARROT', 1]]}

step= 97 day=4 hour=1 money=3010.0 seeds=1 shed=0
  tile:   {'kind': 'PLANT', 'crop': 'CARROT', 'planted_day': 3, 'watered_today': True, 'consecutive_unwatered': 0, 'yield_units': 1, 'max_lifespan_step': 168, 'fertilized_until_day': -1}
  action: {'farmer': ['WATER'], 'hands': [], 'market': [['SELL', 'CARROT', 2]]}

Final reward: 3010.0
```

### 7.4 Come leggere la traccia

L'output mette in relazione tre elementi: il momento della simulazione, lo stato osservato e l'azione prodotta dall'agente.

Il ciclo principale che emerge dall'esecuzione è:

```text
BUY_SEED
    ↓
PLANT
    ↓
WATER
    ↓
PASS
    ↓
WATER
    ↓
PASS
    ↓
HARVEST
    ↓
PLANT
    ↓
SELL
```

La baseline non si muove mai dalla casella iniziale. Tutta la produzione avviene quindi sulla stessa tile.

La traccia permette inoltre di osservare che il ciclo non è costituito da una semplice sequenza lineare di azioni. Alcune attività si sovrappongono: mentre una carota è in produzione, l'agente può avere già acquistato il seme per il ciclo successivo; mentre annaffia una nuova coltura, può contemporaneamente vendere il raccolto precedente.

Il comportamento complessivo deriva quindi dall'interazione tra poche regole locali applicate ripetutamente allo stato corrente.

### 7.5 Deduzioni dall'esecuzione

**Deduzione 1 — l'agente acquista in anticipo il seme successivo**

Dopo aver piantato il primo seme, il numero dei semi posseduti torna a zero.

La regola:

```text
se seeds == 0
    compra un seme
```

fa quindi acquistare immediatamente un nuovo seme.

Questo produce una piccola pipeline:

```text
carota in produzione
+
seme già disponibile per il ciclo successivo
```

Il comportamento non è stato codificato come piano esplicito; emerge dalla combinazione delle regole locali.

**Deduzione 2 — farmer e mercato agiscono nello stesso turno**

A `step=97` compare:

```text
action:
{
  'farmer': ['WATER'],
  'market': [['SELL', 'CARROT', 2]]
}
```

L'agente annaffia la nuova pianta mentre contemporaneamente vende il raccolto precedente.

Questo conferma che `farmer` e `market` sono due canali di azione indipendenti.

**Deduzione 3 — l'irrigazione influisce sulla resa**

Al giorno 2 la tile riporta:

```text
yield_units = 2
```

mentre nei giorni precedenti era:

```text
yield_units = 1
```

L'esecuzione mostra quindi concretamente che la gestione dell'irrigazione incide sulla resa della coltura.

**Deduzione 4 — il capitale segue un ciclo economico completo**

L'esecuzione parte da:

```text
money = 3000
```

Dopo gli acquisti di semi si arriva a:

```text
money = 2940
```

La vendita di due carote porta poi il capitale a:

```text
money = 3010
```

La baseline ha quindi completato un ciclo:

```text
capitale
→ acquisto input
→ produzione
→ raccolta
→ vendita
→ nuovo capitale
```

e contemporaneamente ha già avviato il ciclo produttivo successivo.

**Deduzione 5 — il costo osservato del seme non coincide con il valore statico nel codice**

In `state.py` la configurazione locale contiene:

```python
"CARROT": {
    "seed": 15,
    "max_yield_day": 3,
    ...
}
```

Nell'esecuzione reale, tuttavia, l'acquisto di un seme porta il capitale da:

```text
3000
```

a:

```text
2980
```

quindi la transazione osservata costa 20.

Il valore `15` non deve quindi essere interpretato come prezzo effettivo garantito del seme.

Nella E01 viene usato soltanto come soglia per controllare se il capitale è sufficiente a tentare l'acquisto. Nelle versioni successive sarà opportuno verificare se questa decisione debba utilizzare direttamente il prezzo osservato nel mercato.

**Deduzione 6 — funzionamento corretto non significa comprensione completa**

La stessa baseline aveva già:

- superato i test;
- completato 30 episodi locali;
- prodotto 0% di squalifiche;
- generato una submission valida;
- ottenuto una submission Kaggle `Complete`.

L'esecuzione osservabile ha però consentito di comprendere aspetti che questi controlli non evidenziavano, tra cui:

- il mantenimento automatico di un seme di riserva;
- la contemporaneità tra azioni del farmer e ordini di mercato;
- l'effetto dell'irrigazione sulla resa;
- la discrepanza tra costo statico del seme e costo osservato.

Per questo motivo la verifica di una versione non si conclude con la sola domanda:

> Il programma funziona?

Occorre anche poter rispondere a:

> Che cosa sta facendo realmente e perché produce quel risultato?

Questa traccia costituisce quindi il riferimento comportamentale della baseline E01 rispetto al quale saranno confrontate le evoluzioni successive.

---

## 8. Il comportamento emergente della baseline

La prima versione può quindi essere descritta come un piccolo automa economico:

```text
         ┌─────────────┐
         │ COMPRA SEME │
         └──────┬──────┘
                ↓
         ┌─────────────┐
         │   PIANTA    │
         └──────┬──────┘
                ↓
         ┌─────────────┐
         │  ANNAFFIA   │
         └──────┬──────┘
                ↓
         ┌─────────────┐
         │   ATTENDI   │
         └──────┬──────┘
                ↓
         ┌─────────────┐
         │  RACCOGLI   │
         └──────┬──────┘
                ↓
         ┌─────────────┐
         │    VENDI    │
         └──────┬──────┘
                │
                └──────────────→ nuovo ciclo
```

Il risultato non deriva da un modello di Machine Learning né da un LLM eseguito durante la partita.

È una **policy rule-based**: una serie deterministica di condizioni che trasformano lo stato osservato in un'azione.

L'aspetto agentico consiste nel ciclo:

```text
OSSERVA
   ↓
INTERPRETA LO STATO
   ↓
DECIDI
   ↓
AGISCI
   ↓
L'AMBIENTE CAMBIA
   ↓
OSSERVA DI NUOVO
```

Questo ciclo viene ripetuto fino alla fine dell'episodio.

---

## 9. L'infrastruttura di valutazione

Il software prodotto in E01 non contiene soltanto l'agente.

`src/agricola/evaluation/runner.py` costruisce un sistema sperimentale che può eseguire più episodi contro differenti avversari e aggregarne i risultati.

Il runner:

- alterna l'agente tra Player 0 e Player 1;
- conta vittorie, sconfitte e pareggi;
- registra il capitale finale;
- verifica il completamento degli episodi;
- registra eventuali squalifiche;
- misura separatamente il tempo della decisione dell'agente e il tempo complessivo della simulazione.

Questa infrastruttura è più importante della qualità della prima strategia, perché permette di porre una condizione precisa alle evoluzioni successive:

> una nuova strategia non è migliore perché sembra più sofisticata; è migliore se produce risultati misurabilmente migliori rispetto alla baseline.

Il tag:

```text
v0.1-e01-baseline
```

costituisce quindi non soltanto una versione del codice, ma il **punto zero sperimentale** contro cui confrontare le versioni successive.

---

## 10. Dalla struttura modulare alla submission Kaggle

Durante lo sviluppo il codice è distribuito in più moduli perché questo facilita comprensione, test ed evoluzione.

Kaggle richiede però una submission Python standalone.

Lo script:

```text
scripts/build_submission.py
```

legge quindi:

```text
state.py
actions.py
carrot_loop.py
```

rimuove gli import interni del package e incorpora i diversi componenti in un unico file:

```text
experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py
```

Il file generato contiene nello stesso sorgente:

```text
GameState
ActionBuilder
CarrotLoopAgent
agent()
```

ed è quindi indipendente dalla struttura locale del repository.

Questa distinzione consente di mantenere contemporaneamente:

```text
CODICE DI SVILUPPO
modulare, leggibile, testabile
        ↓
BUILD
        ↓
CODICE DI DELIVERY
singolo file standalone
```

La submission E01 è stata successivamente caricata sulla piattaforma Kaggle ed eseguita con successo, fornendo una verifica esterna della compatibilità del bundle prodotto.

---

## 11. Tre livelli distinti del progetto E01

Alla fine della prima iterazione il repository contiene quindi tre sistemi logicamente differenti.

### Agente

```text
GameState
    ↓
CarrotLoopAgent
    ↓
ActionBuilder
    ↓
agent()
```

È ciò che prende le decisioni durante la partita.

### Sistema di valutazione

```text
runner
    ↓
episodi
    ↓
metriche
    ↓
experiments/archive/e01/artifacts/baseline.json
```

Serve a stabilire quantitativamente quanto bene funziona una determinata strategia.

### Sistema di delivery

```text
codice modulare
    ↓
build_submission.py
    ↓
submission.py
    ↓
Kaggle
```

Serve a trasformare il progetto di sviluppo nell'artefatto richiesto dalla competizione.

Questa separazione permette di modificare soprattutto il primo livello nelle iterazioni successive, mantenendo relativamente stabili gli altri due.

---

## 12. Limiti osservati e aspetti da verificare

L'esecuzione diretta della baseline ha permesso di distinguere i limiti intenzionali della strategia E01 da alcuni aspetti tecnici che richiedono una verifica nelle versioni successive.

Il primo riguarda la gestione dei prezzi. Come osservato nel §7.5, il costo effettivo di un seme di carota durante l'esecuzione non coincide con il valore statico presente in `state.py`.

La E01 utilizza questo valore soprattutto come soglia per stabilire se il capitale disponibile consente di tentare l'acquisto. Una strategia più evoluta non dovrebbe però assumere che un valore hardcoded rappresenti il prezzo effettivo di mercato.

Le versioni successive dovranno quindi verificare se le decisioni economiche possano essere basate direttamente sui prezzi osservati nell'ambiente:

```text
valore statico
    ↓
stima utilizzata dalla baseline

prezzo osservato
    ↓
informazione corrente dell'ambiente
    ↓
decisione economica
```

La distinzione diventerà ancora più importante quando l'agente dovrà confrontare colture differenti, decidere quando acquistare o vendere e valutare la redditività delle diverse alternative.

Un secondo aspetto riguarda l'ambiente Python. Il repository adotta un layout `src/`, ma durante l'ispezione interattiva il package `agricola` non risultava installato nella `.venv`. Per eseguire direttamente gli esempi è stato quindi necessario aggiungere temporaneamente `src` a `PYTHONPATH`:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

Il benchmark e la submission non erano compromessi da questa situazione, ma l'esperienza evidenzia una differenza tra la struttura prevista dal progetto e l'ambiente di sviluppo effettivamente configurato. Nelle iterazioni successive sarà opportuno rendere riproducibile anche l'installazione locale del package, evitando che l'esecuzione interattiva dipenda da una configurazione temporanea della sessione PowerShell.

Restano infine i limiti intenzionali della strategia E01. `CarrotLoopAgent` utilizza soltanto una piccola parte dello stato già disponibile: non si muove, coltiva una sola casella, utilizza una sola coltura, vende immediatamente, non confronta alternative economiche e non reagisce al comportamento dell'avversario.

Questi aspetti non devono essere corretti tutti contemporaneamente. Costituiscono invece lo spazio sperimentale delle iterazioni successive.

Il criterio rimane quello stabilito con E01: ogni nuova capacità dovrà essere introdotta in modo osservabile e confrontata con la baseline attraverso la stessa infrastruttura di valutazione. In questo modo sarà possibile distinguere l'aumento della complessità del codice da un effettivo miglioramento del comportamento dell'agente.

---

## 13. Il punto di partenza per le evoluzioni successive

E01 usa una frazione minima dello spazio delle possibilità offerte da Kaggriculture.

La progressione successiva può essere letta come un aumento graduale delle capacità decisionali.

La baseline attuale conosce sostanzialmente:

```text
una casella
una coltura
un farmer immobile
vendita immediata
nessun avversario
```

Le evoluzioni potranno introdurre progressivamente:

```text
una casella
    ↓
più caselle
    ↓
movimento
    ↓
più colture
    ↓
confronto economico tra colture
    ↓
pianificazione temporale
    ↓
prezzi dinamici
    ↓
gestione del capitale
    ↓
espansione del terreno
    ↓
farm hands e animali
    ↓
osservazione dell'avversario
    ↓
strategia competitiva
```

La struttura creata in E01 è significativa proprio perché permette di introdurre queste capacità senza dover ripartire da zero.

`GameState` può diventare progressivamente più ricco nell'interpretazione dell'ambiente.

`CarrotLoopAgent` può essere sostituito o affiancato da strategie più evolute.

`ActionBuilder` può essere esteso con ulteriori azioni.

Il runner può continuare a utilizzare la stessa baseline come termine di confronto.

Il processo di build può continuare a generare lo stesso tipo di submission richiesto da Kaggle.

E01 costituisce quindi il **minimo sistema completo funzionante**: abbastanza semplice da essere compreso interamente, ma già strutturato in modo da rendere misurabili le evoluzioni successive.
