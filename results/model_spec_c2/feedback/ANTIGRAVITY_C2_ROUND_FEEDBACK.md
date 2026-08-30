# FEEDBACK INDIPENDENTE SUL ROUND C2 — ANTIGRAVITY

- **Autore:** Antigravity
- **Ruolo:** Agente Modellatore e Strategico
- **Fase:** C2 Post-Tournament Forensic Feedback
- **Data:** 2026-08-30
- **Stato:** `C2_ROUND_FEEDBACK_COMPLETE`
- **Oggetto:** Analisi critica end-to-end del ciclo MODEL_SPEC → BUILD → VERIFY → TOURNAMENT C2

---

## 1. Introduzione ed Evidenza Osservata

Il `MODEL_SPEC TOURNAMENT C2` ha prodotto un quadro sperimentale anomalo e fortemente divergente dagli obiettivi strategici del progetto Kaggriculture:

```text
CODEX C2:       Mean final_money: $16,846.50 | Active surface: 9.17 tiles | 6W - 0L - 0T
ANTIGRAVITY C2: Mean final_money: $3,000.00  | Active surface: 0.00 tiles | 0W - 3L - 3T (720 PASS)
COPILOT C2:     Mean final_money: $3,000.00  | Active surface: 0.00 tiles | 0W - 3L - 3T (Stationary at spawn)
```

Il torneo ha dimostrato che due candidati su tre non erano in grado di realizzare alcuna operazione agricola nell'ambiente reale, mentre il terzo (Codex C2), pur funzionando end-to-end, si è attestato su livelli di monetizzazione e superficie attiva marcatamente inferiori sia ai target nominali (17 tile) sia ai massimi storici documentati nel progetto ($37.7k in E15-M2).

Questo documento analizza le cause profonde di questa discrepanza, articolando l'analisi a livello di failure tecnici, dinamica economica, Foundation C2, MODEL_SPEC, processi di verifica, autocritica e riforme metodologiche prioritarie.

---

## 2. Cause dei Failure Tecnici

### 2.1 Antigravity C2: Runtime Interface Mismatch e Silent Masking
- **Meccanismo del Guasto:** In `src/agricola/strategy/antigravity/c2_policy.py:186-187` e `339-340`, l'accesso allo stato privato è stato implementato come:
  ```python
  privates = observation.get("private", [])
  private = privates[player_index] if player_index < len(privates) else {}
  ```
  Nel runtime ufficiale di `kaggle_environments`, l'oggetto `observation["private"]` fornito al singolo agente è già il dizionario/Struct privato dell'agente chiamante (`privates[i]`), non la lista globale di tutti i giocatori (a differenza di `observation["farms"]`). Trattandosi di un dizionario con chiavi stringa, `len(privates)` restituiva 5 (il numero di chiavi), la condizione `0 < 5` risultava vera e `privates[0]` sollevava un `KeyError: 0` non gestito all'interno della policy.
- **Mascheramento:** Il wrapper `AntigravityC2Agent.__call__` conteneva un blocco `try...except Exception` che intercettava l'errore e restituiva `{"farmer": ["PASS"], "hands": [], "market": []}`, trasformando un bug fatale in un loop silenzioso di 720 turni di inattività.
- **Escape del Processo:** I test unitari in `tests/test_antigravity_c2.py` utilizzavano mock con `"private": [ {...} ]`, rispecchiando l'assunzione errata del codice anziché il runtime reale. Il gate di build verification non prevedeva l'esecuzione di un singolo step su un'istanza reale di `kaggle_environments.make("kaggriculture")`.

### 2.2 Copilot C2: Omissione di Bootstrap, Routing e Binding di Posizione
- **Meccanismo del Guasto:** Copilot C2 ha presentato tre difetti concorrenti:
  1. *Player Binding:* `CopilotC2Agent.__call__` invocava la policy con `player_index=0` fisso. Quando Copilot giocava come Player 1, leggeva lo stato di `farms[0]` (avversario) mentre le sue azioni venivano applicate a `farms[1]`.
  2. *Bootstrap Assente:* Il modulo emetteva permanentemente `market: []`. Partendo da zero semi nell'inventario iniziale, l'agente non ha mai acquistato sementi, rendendo irragiungibile la semina (`PLANT`).
  3. *Routing Assente:* La policy non conteneva alcuna logica di movimento (`NORTH`, `SOUTH`, `EAST`, `WEST`); il farmer è rimasto immobile a `(4, 4)`.
- **Origine Concettuale:** Copilot ha interpretato il MODEL_SPEC come una collezione di regole di classificazione locale della singola tile (is_harvest_ready, classify_lifecycle), tralasciando l'architettura esecutiva globale (movimento, acquisti, coordinamento worker).

---

## 3. Cause delle Prestazioni Economiche Deludenti (Analisi su Codex C2)

Codex C2 ha superato tutti i gate di esecuzione, ma ha ottenuto una media di **$16,846.50** e **9.17 tile attive**, contro un target nominale di 17 tile e un perimetro arabile disponibile di 50 tile (2 quadranti).

Le cause della limitazione economica risiedono in:
1. **Collo di Bottiglia nel Task Routing Nearest-Neighbor:** Codex ha riutilizzato l'infrastruttura di routing greedy di E16. Con 10 worker che concorrono sulle stesse tile centrali senza partizionamento spaziale per cluster o corsie, la quota di movimento improduttivo e latenza di transito ha saturato la capacità di lavoro prima di poter irrigare stabilmente 17 colture.
2. **Reinvestment e Pacing di Semina Monotonico:** La politica di riacquisto semi di Codex avveniva per colmare deficit puntuali con orizzonte a breve termine, anziché stabilire un polmone di semina massivo che saturasse istantaneamente le tile bonificate con `DIG`.
3. **Iper-Conservatorismo da Prevenzione Failure:** Il modello ha sacrificato la scala produttiva per garantire la compliance formale con il lifespan e l'irrigazione. Nessun tentativo di espansione verso il 3° quadrante è stato contemplato, mantenendo la farm confinata a una frazione marginale della sua capacità biologica teorica.

---

## 4. Adeguatezza della Foundation C2

Valutando la Foundation C2 alla luce dei risultati del round:

| Categoria | Giudizio | Evidenza |
|---|:---:|---|
| **Ontology C2** | **Adeguata** | Ha definito con precisione il vocabolario formale (6 stati, concetti CRP/INV/WRK). |
| **State Machine C2** | **Adeguata** | La transizione a 11 fasi ha modellato correttamente l'EOD e le deadline biologiche. |
| **Feature Model C2** | **Parzialmente Ambigua** | Ha specificato le sorgenti dei campi (`private.seeds`), ma non ha formalizzato lo schema top-level del container `observation` iniettato dall'engine Kaggle al callable dell'agente. |
| **Foundation vs Candidate Defect** | **Candidate Defect Dominant** | Non esiste alcuna evidenza che i failure di Antigravity, Copilot o il tetto economico di Codex derivino da prescrizioni errate della Foundation. I difetti sono interamente allocati nell'interpretazione dei MODEL_SPEC e nell'implementazione BUILD. |

---

## 5. Adeguatezza dei MODEL_SPEC: Local Correctness vs Full Policy

La discrepanza fondamentale del ciclo C2 risiede nella natura stessa dei MODEL_SPEC:

> **I MODEL_SPEC C2 sono stati redatti come specifiche di conformità su failure mode microscopici di E16, anziché come specifiche di una policy macro-economica completa e competitiva.**

- **Antigravity C2:** Ha focalizzato il MODEL_SPEC sull'azzeramento dei 5.804 no-op di harvest prematuro e sui recovery DIG, sottodimensionando l'architettura di integrazione runtime e la logica di espansione economica.
- **Copilot C2:** Ha ridotto il MODEL_SPEC a una pura funzione di decisione locale della singola tile, assumendo implicitamente che l'ambiente fosse già in uno stato produttivo con semi disponibili e worker posizionati.
- **Codex C2:** Ha mantenuto l'approccio più realistico incorporando il lifecycle all'interno di un agente completo (E16TrainingAgent), ma ha ereditato i limiti strutturali di scalamento di quella base.

---

## 6. Adeguatezza di BUILD e VERIFY

La fase di BUILD e VERIFY ha sofferto di un disallineamento critico degli incentivi di verifica:

```text
COSA HA OTTIMIZZATO IL PROCESSO:
  168 tests passed
  git diff --check clean
  TOURNAMENT_READY: YES
  Zero runtime crashes

COSA AVREBBE DOVUTO VERIFICARE:
  Real-engine execution (kaggle_environments)
  Transizioni di stato ambientali (seed -> crop -> yield -> cash)
  Superficie attiva > 0
  Assenza di loop fail-closed
```

La suite di test ha verificato che il codice compilasse e che i mock interni restituissero i valori attesi dai mock stessi (tautologia di verifica), eludendo l'integrazione con l'ambiente reale.

---

## 7. Perdita dell'Obiettivo Strategico e Uso delle Evidenze Storiche

Nelle iterazioni E11–E12 ed E15, il progetto aveva consolidato evidenze inequivocabili:
1. **La massa produttiva è la determinante primaria del punteggio:** policy con 25–35 tile e 10–12 worker generano $25k–$38k;
2. **La monetizzazione richiede reinvestimento tempestivo:** il cash floor deve finanziare cicli rapidi di semina e vendita;
3. **La prevenzione passiva genera povertà:** una farm che non rischia e non semina preserva $3,000 ma perde la partita.

Nel ciclo C2, la reazione forense al fallimento di E16 (dove i no-op di harvest consumavano il 90% delle azioni) ha innescato un **failure-prevention bias sistemico**. Tutti e tre i modelli si sono concentrati quasi esclusivamente su *cosa NON fare* (non raccogliere prima di first_yield_day, non lasciare tile a weed, non rischiare cassa), perdendo di vista il motore propulsivo di crescita economica e scalamento della superficie coltivata.

---

## 8. SELF-CRITIQUE (Critica del Contributo Antigravity)

Come agente Antigravity, riconosco le seguenti responsabilità dirette nell'esito del round C2:

1. **Assunzione Acritica del Contratto di Runtime:** Ho implementato `observation.get("private", [])` e `privates[player_index]` assumendo per simmetria con `farms` che `private` fosse una lista, senza consultare il codice sorgente dell'engine `kaggriculture.py` né i wrapper storici del repository (`src/agricola/core/state.py`).
2. **Tautologia nei Test di Build Verification:** Ho scritto la suite `tests/test_antigravity_c2.py` costruendo mock che riflettevano la mia implementazione difettosa (`"private": [ {...} ]`), auto-validando l'errore e dichiarando `TOURNAMENT_READY: YES` senza alcuna prova dinamica nell'ambiente reale.
3. **Uso Cieco del Fail-Closed:** Ho implementato un blocco `try...except` in `agent_c2.py` che ha intercettato il `KeyError` trasformando un failure bloccante in 720 turni di `PASS`, mascherando la completa inoperatività della policy.
4. **Disallineamento dei Parametri Biologici:** Nella tabella `CROPS` di `c2_policy.py`, ho hardcodato valori errati per Strawberry (`first_yield_day = 5` anziché 10) e Melon (`first_yield_day = 8` anziché 10). Se il `KeyError` non avesse bloccato l'agente a step 0, la policy avrebbe emesso harvest prematuri falliti al giorno 5 e 8, violando il principio cardine del mio stesso MODEL_SPEC.
5. **Livestock Incompleto:** Ho implementato la costruzione di pasture e l'acquisto di mucche, ma ho omesso l'azione `PICKUP COW` dallo shed, lasciando il comparto zootecnico strutturalmente disconnesso.

---

## 9. Critica del Processo Comune

Separando i livelli di responsabilità:

- **PROCESS DEFECT:** L'assenza di un gate vincolante di *Real-Engine Smoke Test* (esecuzione di almeno 48 step in `kaggle_environments` per dichiarare `TOURNAMENT_READY`) a livello di repository e protocollo sperimentale.
- **CANDIDATE DEFECT:**
  - *Antigravity:* Errore di tipo su `observation["private"]` e parametri biologici difettosi.
  - *Copilot:* Omissione di movement, market orders e binding `player_index`.
  - *Codex:* Bottleneck nel routing greedy e dimensionamento conservativo del working set (9.17 tile).
- **EXPERIMENTAL DESIGN DEFECT:** Il protocollo del tournament ha misurato con successo l'esito delle policy congelate; l'unico difetto è stato l'assenza di un sanity check pre-torneo che rigettasse i candidati inoperativi prima dell'esecuzione dei round formali.

---

## 10. Tre Modifiche Prioritarie al Processo Futuro

### MODIFICA 1: Introduzione Obbligatoria del "Real-Engine Smoke Gate (48-Step)"
- **PROBLEMA RISOLTO:** Impedisce che agenti con errori di interfaccia runtime, crash non gestiti o silent fail-closed loop possano essere dichiarati `TOURNAMENT_READY`.
- **EVIDENZA:** Antigravity C2 e Copilot C2 sarebbero stati rigettati istantaneamente allo step 0 della build verification.
- **RISULTATO ATTESO:** 100% dei candidati ammessi al torneo esegue azioni valide e interagisce con l'ambiente reale.
- **COME FALSIFICARLA:** Se un candidato supera il gate dei 48 step ma fallisce per incompatibilità runtime al torneo ufficiale, la modifica è insufficiente e la durata dello smoke va estesa.

### MODIFICA 2: Gate di Policy Realization basato su State Delta
- **PROBLEMA RISOLTO:** Distingue l'emissione sintattica di comandi (`action dispatch`) dalla reale modifica dello stato dell'ambiente (`state transition`).
- **EVIDENZA:** Copilot C2 ha emesso 586 DIG e 136 HARVEST a vuoto su una tile non coltivata senza mai consumare semi o modificare farm tiles.
- **RISULTATO ATTESO:** Per essere `TOURNAMENT_READY`, il candidato deve dimostrare telemetricamente entro i primi 48 step: `seed_consumed > 0`, `active_crop_surface > 0`, `water_applied > 0`.
- **COME FALSIFICARLA:** Se un candidato produce state delta positivi nello smoke test ma produce zero transizioni biologiche nel torneo completo.

### MODIFICA 3: Allineamento Centralizzato dei Contratti di Runtime e Biologia
- **PROBLEMA RISOLTO:** Elimina le divergenze e l'hardcoding manuale di dizionari `CROPS`, costanti biological e strutture `observation` nei singoli candidati.
- **EVIDENZA:** Antigravity C2 aveva Strawberry a 5 giorni anziché 10; Antigravity e Copilot avevano interpretazioni discordanti di `observation["private"]`.
- **RISULTATO ATTESO:** Tutti i candidati importano costanti e schema di parsing esclusivamente da `src/agricola/core/state.py` o dalla Foundation, garantendo parità biologica assoluta.
- **COME FALSIFICARLA:** Se emergono divergenze nelle definizioni biologiche tra candidate executables conformi all'import comune.

---

## 11. Risposta alla Domanda Finale Obbligatoria

> **Se potessi cambiare una sola decisione presa prima del tournament C2, quale cambieresti e perché?**

**Decisione da cambiare:**
Avrei reso obbligatorio, all'interno del file di specifica dei gate di build (`BUILD_VERIFICATION.md`), l'inserimento di un test di fumo vincolante di 48 step eseguito direttamente contro `kaggle_environments.make("kaggriculture")`, con assert su `action != PASS` e `active_crop_surface > 0`.

**Perché:**
Questa singola decisione avrebbe impedito sia ad Antigravity che a Copilot di ottenere il via libera con un falso `TOURNAMENT_READY: YES`. Avrebbe costretto Antigravity a correggere immediatamente la riga di accesso a `private` e i parametri biologici, e avrebbe costretto Copilot a implementare il bootstrap dei semi e il movimento prima del congelamento. Il torneo C2 avrebbe così costituito un confronto reale, informativo e ad alto valore scientifico fra tre policy agricole operative e complete, anziché un round dominato da failure di integrazione elementari.

---

```text
C2_ROUND_FEEDBACK_COMPLETE
NO_REMEDIATION_PERFORMED
```
