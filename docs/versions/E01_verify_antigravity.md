# Evidenza VERIFY E01 — Esecuzione Locale ed Ispezione Comportamentale

Attività di **VERIFY** sulla baseline E01 eseguita direttamente tramite Antigravity.

Nessuna modifica, ottimizzazione o refactoring è stata apportata alla strategia dell'agente o al codice sorgente del repository.

---

## 1. Modalità Utilizzata per Eseguire E01

L'esecuzione dell'episodio completo (720 turni) è avvenuta direttamente dall'ambiente di esecuzione Antigravity tramite il virtual environment isolato `.venv` (Python 3.12).

### Procedura Eseguita:
1. Invocazione dell'engine `kaggle_environments` tramite script scratch non persistente:
   ```python
   import kaggle_environments
   env = kaggle_environments.make("kaggriculture", configuration={"episodeSteps": 720})
   env.run(["src/agricola/agent.py", "pass"])
   ```
2. Ispezione diretta dell'array `env.steps` (che contiene l'intera cronologia di observation ed action per tutti i 720 turni).
3. Estrazione dello stato del terreno, inventario semi, magazzino shed, capitale liquido ed azioni emesse.

---

## 2. Diagnosi ed Eventuali Problemi Incontrati

### Problema Incontrato (Tentativo Iniziale Custom Step Loop):
Durante un primo test di tracciamento mediante un ciclo custom `for step in range(720): env.step(...)`, al raggiungimento dello step 719 l'ambiente ha sollevato la seguente eccezione:
```text
kaggle_environments.errors.FailedPrecondition: Environment done, reset required.
```

### Causa:
Nel framework `kaggle-environments`, quando viene eseguito l'ultimo turno dell'episodio (step 719 su 720 step totali), l'engine imposta internamente `env.done = True`. Qualsiasi successiva chiamata a `env.step()` fallisce perché l'episodio si è già concluso e richiede un `reset()`.

### Soluzione Adottata:
Utilizzo dell'API nativa ed ufficiale dell'engine: `env.run([agent, opponent])`. Il metodo `run()` gestisce autonomamente il ciclo di vita dell'episodio senza sollevare eccezioni di fine partita e memorizza l'intera storia degli stati e delle azioni nell'oggetto `env.steps`.
**Nessuna modifica al codice del repository è stata necessaria per questa soluzione.**

---

## 3. Traccia Osservabile dell'Episodio

Di seguito è riportata la traccia significativa del primo ciclo operativo completo (Step 0..97) e degli step finali fino al termine della stagione (Step 719).

```text
=== EPISODE TRACE: CARROT LOOP BASELINE (720 STEPS) ===

Step   0 (Day  0, Hr  0) | Money: $3000.0 | Seeds: {'CARROT': 0} | Shed: {'CARROT': 0} | Tile: EMPTY                                              | Farmer: ['PASS']         | Market: []
Step   1 (Day  0, Hr  1) | Money: $2980.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: EMPTY                                              | Farmer: ['PLANT', 'CARROT'] | Market: [['BUY_SEED', 'CARROT', 1]]
Step   2 (Day  0, Hr  2) | Money: $2980.0 | Seeds: {'CARROT': 0} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=False)   | Farmer: ['PLANT', 'CARROT'] | Market: []
Step   3 (Day  0, Hr  3) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=True)    | Farmer: ['WATER']        | Market: [['BUY_SEED', 'CARROT', 1]]
Step  24 (Day  1, Hr  0) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=False)   | Farmer: ['PASS']         | Market: []
Step  25 (Day  1, Hr  1) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=True)    | Farmer: ['WATER']        | Market: []
Step  48 (Day  2, Hr  0) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=False)   | Farmer: ['PASS']         | Market: []
Step  49 (Day  2, Hr  1) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=True)    | Farmer: ['WATER']        | Market: []
Step  72 (Day  3, Hr  0) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=0, watered=False)   | Farmer: ['PASS']         | Market: []
Step  73 (Day  3, Hr  1) | Money: $2960.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: EMPTY                                              | Farmer: ['HARVEST']      | Market: []
Step  74 (Day  3, Hr  2) | Money: $2960.0 | Seeds: {'CARROT': 0} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=3, watered=False)   | Farmer: ['PLANT', 'CARROT'] | Market: []
Step  75 (Day  3, Hr  3) | Money: $2940.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=3, watered=True)    | Farmer: ['WATER']        | Market: [['BUY_SEED', 'CARROT', 1]]
Step  96 (Day  4, Hr  0) | Money: $2940.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 2} | Tile: PLANT(crop=CARROT, planted_day=3, watered=False)   | Farmer: ['PASS']         | Market: []
Step  97 (Day  4, Hr  1) | Money: $3010.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=3, watered=True)    | Farmer: ['WATER']        | Market: [['SELL', 'CARROT', 2]]

... [Cicli intermedi identici fino a fine stagione] ...

Step 697 (Day 29, Hr  1) | Money: $3564.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=27, watered=True)   | Farmer: ['WATER']        | Market: []
Step 719 (Day 29, Hr 23) | Money: $3564.0 | Seeds: {'CARROT': 1} | Shed: {'CARROT': 0} | Tile: PLANT(crop=CARROT, planted_day=27, watered=True)   | Farmer: ['PASS']         | Market: []
```

---

## 4. Reward ed Esito Finale

- **Esito finale dell'episodio**: `status: DONE` (720/720 turni completati senza errori o disconnessioni).
- **Capitale finale (`money`)**: **`3564.0`**
- **Ricompensa finale (`reward`)**: **`3564.0`**

### Relazione tra `reward` e `money`:
Nell'ambiente di simulazione `kaggriculture` gestito da `kaggle-environments`, la funzione di ricompensa dell'engine definisce il `reward` del giocatore facendolo coincidere esattamente con il suo capitale disponibile:
$$\text{reward} = \text{farm["money"]}$$

- `money` è il capitale liquido contenuto nella struttura dati dell'azienda agricola (`observation["farms"][player]["money"]`).
- `reward` è il valore restituito dall'engine (`step[0]["reward"]`) e utilizzato dalla leaderboard di Kaggle per determinare il punteggio e l'esito della partita.

Per lo specifico episodio eseguito, sia il capitale finale `money` che il `reward` ufficiale dell'ambiente sono pari in modo univoco a **`3564.0`**.

---

## 5. Interpretazione del Comportamento Osservato

### 5.1 Ciò che deriva direttamente dalla traccia (Osservazioni Empiriche):
1. **Sequenza del ciclo**: È chiaramente visibile l'intera catena operativa `BUY_SEED → PLANT → WATER → HARVEST → SELL`.
2. **Tempo di lavorazione**: La carota richiede 3 giorni di crescita (piantata a Day 0, pronta per il raccolto a Day 3 Hour 1).
3. **Resa del raccolto e vendita**: Alla raccolta a Day 3, vengono depositati 2 unità di carote nel magazzino `shed`, che vengono vendute a Day 4 Hour 1 per un ricavo lordo di +$70.0 (portando la liquidità da $2940.0 a $3010.0, net profit di +$10.0 rispetto al capitale iniziale).
4. **Costo reale del seme**: L'ordine `BUY_SEED` detrae esattamente $20.0 dal capitale liquido (portando il denaro da $3000.0 a $2980.0).

### 5.2 Ciò che deriva dall'analisi del codice:
1. In `src/agricola/baseline/carrot_loop.py`, l'agente esegue prima il controllo sul magazzino per vendere, poi verifica se `seeds["CARROT"] == 0` per emettere l'ordine `BUY_SEED`, ed infine controlla lo stato della casella per piantare, annaffiare o raccogliere.
2. L'agente non si muove mai dalla casella `(4, 4)` iniziale.

### 5.3 Interpretazioni e Deduzioni:
1. **Pipeline del seme di riserva**: Quando l'agente pianta il seme posseduto alla casella vuota, l'inventario `seeds` scende temporaneamente a 0. Al turno successivo la regola `seeds == 0` acquista immediatamente 1 seme di riserva. In questo modo, l'agente mantiene sempre un seme in attesa mentre la carota corrente cresce, consentendo di ri-piantare all'istante (nello stesso turno di disponibilità del terreno) appena avviene il raccolto.
2. **Parallelismo Farmer / Mercato**: Nello Step 97 si osserva che l'azione del farmer è `['WATER']` e contemporaneamente l'azione di mercato è `[['SELL', 'CARROT', 2]]`. Ciò conferma che il contadino e il canale di mercato sono due vettori di comando indipendenti nello stesso turno.

---

## 6. Risultato del Confronto con `docs/versions/E01_baseline.md`

Il documento [`docs/versions/E01_baseline.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E01_baseline.md) è stato esaminato e confrontato sistematicamente con:
- il codice sorgente corrente del repository;
- l'esecuzione appena effettuata;
- la traccia osservata.

### Esito del confronto:
Il documento [`E01_baseline.md`](file:///c:/Users/pietr/Projects/kaggriculture-agent/docs/versions/E01_baseline.md) risulta **estremamente accurato, coerente e sufficientemente completo**.
Non sono emerse inesattezze strutturali, contraddizioni con il codice sorgente o interpretazioni errate del comportamento della baseline.

Dichiaro quindi esplicitamente che **`docs/versions/E01_baseline.md` è già sufficientemente accurato e non richiede modifiche**.
