# Codex V9/E17 — Guida al runtime e collegamento con la Foundation C2.1

- **Stato:** ACTIVE / AS-BUILT
- **Data:** 2026-09-02
- **Policy descritta:** `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`
- **Release esterna:** `CODEX-E17.0-EXTERNAL-CONTROL-V1`
- **Scopo:** spiegare il codice realmente eseguito e la sua relazione con la Foundation, senza attribuire al runtime capacità che non possiede.

## 1. Kaggle e Kaggriculture da zero

### 1.1 Che cos'è un agente Kaggle

In questa competizione un agente non è un programma che avvia autonomamente
una partita. È una funzione Python che Kaggle chiama ripetutamente mentre
l'ambiente di gioco gestisce la partita.

Il contratto minimo è:

```python
def agent(observation, configuration=None):
    return action
```

- `observation` è lo stato che l'agente può vedere prima della decisione;
- `configuration` contiene le costanti della partita;
- `action` è il batch di comandi richiesto dall'agente per quel turno.

La funzione non restituisce denaro, vittoria o score. Restituisce soltanto la
prossima azione. È l'engine Kaggriculture che applica le azioni dei giocatori,
fa avanzare il tempo e calcola lo stato e il risultato successivi.

### 1.2 Che cosa viene caricato su Kaggle

Per la submission viene caricato **un solo file Python standalone**:

```text
submission/submission_codex.py
```

“Standalone” significa che il file contiene tutto il codice e tutti i dati
necessari alla policy. Non può dipendere dal fatto che su Kaggle esistano le
directory locali `src/`, `docs/`, `scripts/` o `experiments/`.

La submission corrente importa soltanto `deepcopy` dalla libreria standard e
incorpora direttamente:

- identificativo della release;
- hash della routine;
- 719 batch di azioni;
- classe `CodexV9StandaloneAgent`;
- factory `create_agent`;
- funzione pubblica `agent`.

Tutti gli altri file del repository servono a progettare, generare, verificare
e documentare quel singolo artefatto.

### 1.3 Osservazione in ingresso

Un'osservazione reale dell'ambiente contiene questi campi principali:

```python
{
    "step": 0,
    "day": 0,
    "hour": 0,
    "player": 0,
    "farms": [...],
    "private": {
        "inventories": [...],
        "seeds": {...},
        "shed": {...},
    },
    "market": {
        "inventory": {...},
        "prices": {...},
    },
    "town": {...},
    "remainingOverageTime": ...,
}
```

In particolare:

- `step`, `day` e `hour` identificano il momento della partita;
- `player` identifica il seat della nostra policy;
- `farms[player]` contiene denaro, farmer, hands, tile e quadranti del giocatore;
- `private` contiene inventari, semi e shed privati;
- `market` contiene prezzi e disponibilità pubbliche pre-risoluzione;
- `town` descrive lo stato dei negozi e del centro cittadino.

La configurazione dell'ambiente contiene, tra l'altro, 720 stati massimi, 24
turni al giorno, board 10×10, capacità shed 100 e massimo 10 ordini di mercato
per turno. La V9 riceve questa configurazione ma non la usa nel decision path.

### 1.4 Azione restituita

L'azione è un dizionario con tre canali:

```python
{
    "farmer": ["NORTH"],
    "hands": [
        ["WATER"],
        ["HARVEST"],
    ],
    "market": [
        ["SELL", "WHEAT", 1],
        ["HIRE"],
    ],
}
```

- `farmer` contiene il singolo comando del farmer principale;
- `hands` contiene, per posizione, il comando richiesto a ciascun assistente;
- `market` contiene gli ordini economici dello step.

Questo è un **batch di richieste**. Dopo aver ricevuto anche il batch
dell'avversario, l'engine decide quali richieste sono valide, le applica nel
suo ordine causale e produce la prossima osservazione. Un ordine presente nel
dizionario non è quindi automaticamente un ordine eseguito.

### 1.5 Episodio, turni e risultato

Una partita è chiamata `episode`. Con `episodeSteps = 720` l'agente viene
chiamato 719 volte, sugli step da 0 a 718; lo stato conclusivo occupa l'ultimo
passaggio dell'episodio.

Alla fine l'engine produce uno `status` e un `reward` economico. Nei test locali
il reward corrisponde al risultato economico usato per confrontare le policy.
Kaggle usa poi i risultati delle partite per aggiornare il rating mostrato nella
leaderboard. Il rating Kaggle, per esempio `996`, non è il denaro finale di una
singola partita.

### 1.6 Glossario minimo

| Termine | Significato nel progetto |
|---|---|
| Engine / ambiente | Il programma Kaggriculture che applica le regole del gioco. |
| Policy / agente | La funzione che, data un'osservazione, sceglie un'azione. |
| Step | Un singolo istante decisionale; è l'indice usato dalla V9. |
| Episode | Una partita completa. |
| Seed | Valore che rende riproducibile la componente casuale di una partita locale. |
| Seat | Posizione del giocatore, normalmente 0 oppure 1. |
| Replay | Registrazione di osservazioni, azioni e risultati di un episode già giocato. |
| Builder | Script che trasforma file sorgente in un artefatto generato. |
| Freeze | Copia immutabile identificata da hash e usata come baseline. |
| Submission | Singolo file standalone caricato sulla piattaforma. |
| Telemetria | Misure raccolte durante l'esecuzione, senza decidere le azioni. |
| Ledger | Registro che collega una richiesta allo stato prima e dopo la risoluzione. |
| Reward | Risultato economico di un singolo episode. |
| Rating | Valore aggregato mostrato dalla leaderboard Kaggle. |

## 2. Chi chiama cosa

### 2.1 Catena su Kaggle

```text
Kaggle importa submission_codex.py
        |
        v
il modulo esegue _DEFAULT_AGENT = create_agent()
        |
        v
per ogni step Kaggle chiama agent(observation, configuration)
        |
        v
agent chiama _DEFAULT_AGENT(observation, configuration)
        |
        v
CodexV9StandaloneAgent.__call__ seleziona e restituisce il batch
        |
        v
Kaggriculture combina i batch dei giocatori e aggiorna lo stato
        |
        v
allo step seguente Kaggle richiama agent con la nuova observation
```

La V9 standalone non apre file, non esegue test e non chiama il ledger durante
la partita. Tutte queste attività avvengono prima dell'upload o nei benchmark
locali.

Le funzioni principali e i loro valori di ritorno sono:

| Funzione | Chiamata da | Restituisce |
|---|---|---|
| `build_submission_codex_v9(output_path)` | CLI o test | Un oggetto `Path` che indica il file standalone scritto. |
| `load_v9_config(path)` | `create_v9_agent` | Un `dict` contenente una copia della config validata. |
| `create_v9_agent(...)` | Runner e test locali | Una funzione `policy` chiamabile, dotata anche di riferimenti alla telemetria. |
| `CodexThreeQDistilledRoutineAgent.__call__(...)` | Wrapper `policy` sorgente | Il `dict` dell'azione per lo step corrente. |
| `telemetry_snapshot()` | Report e runner locali | Un `dict` di contatori e KPI passivi. |
| `create_agent()` nella submission | Import del modulo o test | Un oggetto `CodexV9StandaloneAgent`. |
| `agent(...)` nella submission | Kaggle, una volta per step | Il `dict` dell'azione richiesto all'engine. |
| `instrument_policy(policy, ledger)` | Runner E17 | Una nuova policy-wrapper che restituisce le stesse azioni e aggiorna il ledger. |
| `ledger.metrics()` | Runner E17 a fine episode | Un `dict` di copertura, outcome, hash ed errori tecnici. |
| `main()` nei builder/verificatori | Interprete Python da riga di comando | Codice di uscita `0` se il processo termina correttamente; un errore interrompe l'esecuzione. |

In Python, `__call__` rende un oggetto utilizzabile come una funzione. Per
questo `_DEFAULT_AGENT(observation, configuration)` esegue in realtà il metodo
`CodexV9StandaloneAgent.__call__`.

### 2.2 Catena nei test locali

Il runner locale crea l'ambiente con:

```python
env = make(
    "kaggriculture",
    configuration={"episodeSteps": 720, "turnsPerDay": 24, "seed": seed},
)
env.run([candidate, opponent])
```

`env.run` svolge localmente il ruolo che avrà Kaggle: chiama entrambe le policy,
passa le osservazioni, raccoglie i batch e fa avanzare l'engine. In E17 il
candidate può essere avvolto dal ledger, ma il wrapper deve restituire la
stessa azione della policy non strumentata.

## 3. Quali file sono sorgenti e quali devono essere generati

### 3.1 File mantenuti manualmente

| File o famiglia | Chi lo mantiene | Funzione |
|---|---|---|
| `docs/foundation/**` | Gruppo di revisione | Regole e linguaggio condivisi; non è codice di submission. |
| `docs/model_specs/codex/MODEL_SPEC_*.md` | Codex, con review | Descrive strategia, assunzioni, target e limiti. |
| `docs/model_specs/codex/configs/*.json` | Codex | Config dichiarativa e provenance. |
| `src/agricola/strategy/codex/codex_3q_mixed_high_density.py` | Codex | Controller sorgente leggibile e telemetria passiva. |
| `src/agricola/core/observation_contract.py` | Foundation comune | Adapter neutrale per snapshot validate. |
| `src/agricola/core/e17_ledger.py` | Infrastruttura E17 comune | Misura richieste ed effetti senza scegliere azioni. |
| `scripts/*.py` | Repository | Builder e verificatori riproducibili. |

Questi file non si rigenerano a ogni test. Si modificano soltanto quando cambia
intenzionalmente il modello, il contratto o il processo di build.

### 3.2 File generati

| Ordine | File | Generato da | Input | Consumatore/output |
|---:|---|---|---|---|
| 1 | `src/agricola/strategy/codex/codex_v9_routine_data.py` | `scripts/build_codex_v9_routine_data.py` | `data/replays/json/104498819.json` | Tabella di 719 batch e `ROUTINE_SHA256`. |
| 2 | `docs/governance/history/model_spec_c2/codex/freeze/submission_codex_v9_tournament.py` | `scripts/build_submission_codex_v9.py` | Routine generata | Standalone congelato per test e torneo locale. |
| 3 | `submission/submission_codex.py` | Passaggio esplicito di release | Standalone verificato più metadata della release E17 | Unico file caricato su Kaggle. |
| 4 | `experiments/e17/artifacts/runs/codex/e17_0/*.json*` | `run_e17_0_codex_parity.py` | Policy, seed, opponent e ledger | Evidenza per singola run. |
| 5 | `experiments/e17/artifacts/derived/codex/E17_0_METRICS.json` | Lo stesso runner | Risultati delle run | Sintesi del gate E17.0. |

Il replay al punto 1 è un **input salvato**, non un file prodotto dal builder.
Il builder lo legge ma non lo modifica.

### 3.3 Che cosa è obbligatorio

Per caricare una submission è obbligatorio soltanto:

```text
submission/submission_codex.py
```

Per poterla considerare riproducibile e affidabile nel progetto richiediamo
anche routine generata, freeze, test di isolamento/parità, hash, MODEL_SPEC ed
evidenza sperimentale. Kaggle non li richiede, ma senza di essi non sapremmo con
certezza quale strategia stiamo caricando.

## 4. Come si costruisce e si verifica

I comandi seguenti partono dalla root del repository in PowerShell:

```powershell
$env:PYTHONPATH = "src"

# 1. Rigenera la tabella: eseguire solo se si intende cambiare la routine.
.\.venv\Scripts\python.exe scripts\build_codex_v9_routine_data.py

# 2. Genera per default il freeze da torneo, non la submission canonica.
.\.venv\Scripts\python.exe scripts\build_submission_codex_v9.py

# 3. Verifica isolamento e parità del file E17 già promosso.
.\.venv\Scripts\python.exe experiments\e17\tools\codex\verify_e17_external_submission.py

# 4. Esegue i test di build temporanea e parità sorgente/standalone.
.\.venv\Scripts\python.exe -m pytest tests\test_submission_codex_isolation.py -q
```

I primi due comandi scrivono file e non vanno eseguiti come semplice controllo.
I test costruiscono invece una submission temporanea e verificano che il file
canonico non venga sovrascritto accidentalmente.

Il builder V9 corrente non produce da solo l'esatta release E17 canonica con i
suoi metadata. La promozione a `submission/submission_codex.py` è un'operazione
di release separata e controllata. Automatizzare questa promozione senza
perdere la protezione contro sovrascritture accidentali è un miglioramento di
manutenibilità ancora aperto.

## 5. Risposta breve sulla V9

La V9/E17 corrente non è un planner che ricalcola la strategia a ogni turno. È
una policy deterministica **open-loop** che usa `observation.step` come indice di
una sequenza congelata di 719 batch di azioni. La sequenza è stata distillata
dal replay pubblico `104498819` e contiene una sola correzione causale applicata
al volo allo step 195.

La Foundation C2.1 non produce quella sequenza e non decide colture, animali,
topologia o timing. Fornisce invece:

1. i fatti verificati dell'engine;
2. il vocabolario comune del dominio;
3. il modello delle transizioni e delle guardie;
4. la classificazione delle feature e della loro provenienza;
5. una proiezione runtime neutrale dell'osservazione.

Il `MODEL_SPEC` Codex è il ponte strategico tra Foundation e codice. La routine
è l'implementazione agent-local della strategia; il ledger E17 è il livello di
misura che verifica, dopo la richiesta, ciò che l'engine rende osservabile come
eseguito, non eseguito o non attribuibile.

## 6. Flusso end-to-end

```text
EVIDENZA PUBBLICA
replay 104498819.json
        |
        v
build_codex_v9_routine_data.py
        |
        v
ROUTINE_ACTIONS[0..718]  ---->  MODEL_SPEC + config dichiarativa
        |                                |
        +---------------+----------------+
                        v
             controller Codex sorgente
              legge observation.step
                        |
                        v
            deepcopy(ROUTINE_ACTIONS[step])
                        |
               patch causale step 195
                        |
                        v
              batch di azioni richieste
                        |
                        v
                     ENGINE
                        |
                        v
                osservazione successiva
                        |
                        v
          ledger E17 requested/executed/unknown
                        |
                        v
             metriche e nuova evidenza
```

La Foundation sta **sopra e attorno** a questo flusso come contratto di
significato e validazione. Non è una dipendenza che il file Kaggle deve
importare per ogni decisione.

## 7. I componenti, in ordine di lettura

| Componente | Responsabilità reale | Entra nel decision path? |
|---|---|---:|
| `scripts/build_codex_v9_routine_data.py` | Estrae 719 azioni dal replay pubblico e calcola l'hash logico della tabella. | Solo in build |
| `src/agricola/strategy/codex/codex_v9_routine_data.py` | Contiene la tabella immutabile delle azioni. Non va modificato a mano. | Sì |
| `docs/model_specs/codex/configs/CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json` | Dichiara identità, target e envelope del modello. | Solo quattro campi sono validati all'avvio |
| `src/agricola/strategy/codex/codex_3q_mixed_high_density.py` | Seleziona l'azione per step, applica la patch e raccoglie telemetria passiva. | Sì |
| `src/agricola/core/observation_contract.py` | Valida e normalizza clock, player, farm, private state, market e configurazione in snapshot hashabili. | **No, non nella V9 corrente** |
| `src/agricola/core/e17_ledger.py` | Registra richieste ed evidenza pre/post, classificando gli outcome senza modificare la policy. | No, è strumentazione fail-open |
| `submission/submission_codex.py` | Copia standalone minima per Kaggle: routine, selettore per step e patch. | È il runtime esterno |

## 8. Che cosa accade a ogni chiamata

Nel controller sorgente `CodexThreeQDistilledRoutineAgent.__call__`:

1. `configuration` viene ignorata;
2. `step` viene letto da `observation` e convertito in intero;
3. `_observe_state` legge il resto dell'osservazione per telemetria passiva;
4. il batch `ROUTINE_ACTIONS[step]` viene copiato con `deepcopy`;
5. allo step 195 viene applicata la correzione feed/animale;
6. `_attribute_action` conta opcode, raccolti e vendite **richiesti**;
7. il batch viene restituito all'engine.

Il `deepcopy` è necessario: la patch e qualsiasi manipolazione successiva non
devono mutare la tabella congelata, che altrimenti cambierebbe il comportamento
dei turni o degli episodi successivi.

La factory di sviluppo `create_v9_agent` racchiude la chiamata in un
`try/except`: un errore inatteso produce `PASS` e incrementa i contatori di
errore/fallback. Il file standalone Kaggle è più piccolo: gestisce con `PASS`
solo gli step fuori intervallo e assume che l'osservazione Kaggle sia valida.

## 9. La routine come insieme di parametri

Nel parallelo con un modello deterministico, la tabella di 719 batch è il
principale insieme di parametri appresi/distillati. Ogni batch ha tre canali:

```python
{
    "farmer": [COMANDO, ...],
    "hands": [[COMANDO, ...], ...],
    "market": [[ORDINE, ...], ...],
}
```

La tabella grezza contiene 8.640 comandi. La patch dello step 195 elimina un
ordine `BUY_ANIMAL COW`, quindi la policy effettiva emette 8.639 comandi per
episodio. La composizione grezza principale è:

| Famiglia | Richieste nella tabella |
|---|---:|
| MOVE (`NORTH/SOUTH/EAST/WEST`) | 3.546 |
| Azioni produttive | 2.842 |
| `PASS` | 676 |
| `SELL` | 439 |
| `HIRE` | 301 |
| `BUY_PRODUCT` | 268 |
| `BUY_SEED` | 100 |
| `BUY_ANIMAL` | 12 grezze, 11 effettive dopo la patch |
| `BUY_LAND` | 2 |

I due acquisti di terra sono richiesti agli step 150 e 265, cioè
rispettivamente al giorno 6, ora 6 e al giorno 11, ora 1 con 24 turni al giorno.
Da qui derivano i profili osservati di attivazione Q1 e Q2.

Questi conteggi sono richieste della policy, non prova automatica di esecuzione.
Ordini di mercato, movimenti e azioni sulle tile possono fallire o produrre un
effetto diverso in funzione dello stato risolto dall'engine.

## 10. La correzione causale dello step 195

Lo step 195 corrisponde al giorno 8, ora 3. Nel replay distillato il batch
conteneva, tra gli ordini di mercato:

- `BUY_PRODUCT WHEAT 3`;
- `BUY_ANIMAL COW 1`;
- `BUY_ANIMAL SHEEP 2`.

La patch porta il WHEAT richiesto ad almeno 4 e rimuove l'acquisto della COW.
L'interpretazione causale è: destinare la capacità marginale alla continuità
del feed, invece di ricomprare l'animale perso. Questa è una modifica della
policy Codex, non una regola della Foundation.

## 11. Collegamento preciso con i layer della Foundation

| Layer Foundation | Che cosa vincola | Come compare nella V9/E17 | Che cosa non decide |
|---|---|---|---|
| Engine Contract | Regole, costanti, schema delle azioni, costi e ordine di risoluzione. | Forma dei batch; clock 24 turni/giorno; interpretazione di hire, feed, mercato e acquisto terra. | La sequenza ottima. |
| Ontology C2.1 | Significato condiviso di quadrante, workforce, coltura, animale, mercato, fuga e capacità. | Nomi e KPI usati dal MODEL_SPEC, dalla telemetria e dal ledger. | Mix colturale o zootecnico. |
| State Machine C2.1 | Precondizioni, transizioni e ordine causale richiesta → risoluzione → stato successivo. | Validazione della routine e classificazione degli outcome E17. | Routing e cadenza della routine. |
| Feature Model C2.1 | Separa feature online, contesto di policy, telemetria post-hoc e outcome. | Definisce perché requested, executed, derived e unknown non sono intercambiabili. | Quali feature la V9 debba usare. |
| Observation Contract runtime | Normalizza e valida una snapshot neutrale con hash e clock coerente. | Disponibile come infrastruttura comune per policy reattive e test. | Non è importato dalla V9/standalone corrente. |

La conformità attuale è quindi soprattutto **semantica, sperimentale e di
audit**. Non è corretto affermare che la V9 consumi clock, snapshot e hashing
del contratto osservativo: il decision path usa direttamente soltanto
`observation.step`.

## 12. Config dichiarativa e comportamento effettivo

La config descrive target come tre quadranti, workforce 13, mix di colture,
livestock e finestre di attivazione. Il loader corrente valida soltanto:

- `candidate_id`;
- `model_spec_version`;
- `quadrants_owned == 3`;
- `workforce_total == 13`.

Gli altri valori non parametrizzano dinamicamente le 719 azioni. Sono envelope,
target e provenance del modello congelato. Perciò modificare, per esempio,
`q2_activation_min_day` nel JSON **non** anticipa Q2: occorre cambiare o
rigenerare la policy e validare la nuova sequenza.

## 13. Telemetria sorgente e ledger E17

La telemetria integrata nel controller osserva stato e richieste senza scegliere
azioni. Misura, fra l'altro, massimo numero di quadranti, hands, animali e
colture, giorni di attivazione Q1/Q2, azioni richieste e vendite richieste.

La stima interna delle fughe è volutamente debole: conta una diminuzione degli
animali al cambio di giorno. Non dimostra da sola la causa. Il ledger E17 la
etichetta infatti come evidenza `DERIVED_EOD_ESCAPE`, non come comando eseguito.

Il ledger opera fuori dal decision path:

```text
observation_t + action_request_t + observation_t+1
                         |
                         v
          EXECUTED / NOT_EXECUTED / UNKNOWN / DERIVED
```

Prima invoca la policy; poi registra il batch e, alla snapshot successiva,
prova ad attribuirne gli effetti. Un errore del ledger non cambia l'azione
selezionata (`fail-open`).

Il gate E17.0 su 6 run ha verificato:

| Misura | Risultato |
|---|---:|
| Parità delle azioni | 4.314 / 4.314 |
| Parità degli outcome | 6 / 6 |
| Record ledger | 51.834 = 8.639 × 6 |
| Copertura di registrazione | 100% |
| Copertura minima di classificazione complessiva | 88,05% |
| Copertura minima di classificazione mercato | 18,91% |
| Fughe EOD derivate | 0 |
| Errori tecnici | 0 |

Il 100% riguarda la **registrazione**, non la certezza di esecuzione. In 272
step la routine grezza emette più ordini di mercato; con il solo delta aggregato
dello stato successivo il ledger non può attribuire in modo univoco ogni fill.
Questi casi restano correttamente `UNKNOWN`.

## 14. Perché la submission non incorpora tutta la Foundation

`submission/submission_codex.py` deve essere autonoma. Contiene la tabella, il
selettore per step e la patch, ma non MODEL_SPEC, adapter osservativo, telemetria
o ledger. Questa separazione è intenzionale:

- la Foundation definisce il contratto;
- il MODEL_SPEC dichiara la strategia e i target;
- il source controller offre implementazione e diagnostica;
- la submission contiene il minimo necessario all'esecuzione esterna;
- gli strumenti E17 verificano che la riduzione standalone non cambi le azioni.

L'hash `ROUTINE_SHA256` identifica la tabella grezza; l'hash della sequenza
effettivamente emessa identifica invece anche la patch. I due hash rispondono a
domande diverse e non devono essere confusi.

## 15. Limiti tecnici da portare in E17

1. **Reattività nulla della baseline:** lo stato osservato non cambia la scelta,
   salvo l'indice temporale.
2. **Config non eseguibile:** quasi tutti i target descrivono la routine ma non
   la governano.
3. **Observation Contract non adottato:** la prossima policy reattiva dovrà
   consumare snapshot validate oppure documentare un adapter equivalente.
4. **Attribuzione mercato debole:** gli ordini multipli impediscono la prova
   individuale del fill; servono serializzazione, identificatori o inferenza
   più forte ma conservativa.
5. **Fallback diverso:** il wrapper sorgente protegge da osservazioni anomale;
   lo standalone assume il contratto Kaggle valido.
6. **Generalizzazione:** una sequenza distillata da replay può essere robusta,
   ma resta esposta a contesa, weed, fill e desincronizzazioni non previste.

## 16. Direzione architetturale consigliata

E17 non dovrebbe sostituire subito la routine con un planner generale. La via
più verificabile è mantenere la V9 come controllo e aggiungere una sola guardia
causale per esperimento:

```text
snapshot normalizzata
        |
        +--> condizione della singola guardia falsa --> azione V9 congelata
        |
        `--> condizione vera --> variante locale preregistrata
                                   |
                                   v
                            ledger + confronto A/B
```

In questa evoluzione l'Observation Contract entrerebbe finalmente nel decision
path, il Feature Model direbbe quali segnali sono leciti al decision time, la
State Machine definirebbe precondizioni ed effetti attesi, e il ledger
distinguerebbe richiesta da realizzazione. La scelta strategica della guardia
resterebbe Codex e quindi indipendente dagli altri agenti.

## 17. Percorso di lettura in dieci minuti

1. Sezioni 1–4 di questa guida: contratto Kaggle, file e build.
2. Sezioni 5–16: architettura V9, Foundation, ledger e limiti.
3. `MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`: intenzione, target e
   risultati congelati.
4. `codex_3q_mixed_high_density.py`: circa 300 righe di controller e telemetria.
5. `observation_contract.py`: forma candidata dell'input neutrale per una policy
   reattiva.
6. `e17_ledger.py`: prova post-action e limiti di attribuzione.
7. `submission_codex.py`: verificare che il runtime Kaggle sia soltanto la
   proiezione standalone della policy.

La tabella da 7.847 righe non va letta riga per riga: è un artefatto generato.
Va analizzata con conteggi, hash, milestone temporali e diff tra varianti.

---

**Conclusione:** la Foundation ha reso il modello spiegabile e auditabile, ma
la V9 non la usa ancora come base di deliberazione online. E17 è il passaggio in
cui i concetti della Foundation possono diventare, uno alla volta, guardie
reattive misurabili senza perdere la baseline che ha prodotto il salto esterno.
