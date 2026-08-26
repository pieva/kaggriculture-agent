# E07-07 — VERIFY Functional Closure

Stiamo lavorando al progetto **Kaggriculture Agent**.

La fase precedente:

`E07-06 — VERIFY Functional Utilization`

ha dimostrato che gran parte dell'architettura E07 è realmente esercitata, ma ha lasciato **tre questioni funzionali non ancora chiuse**:

1. semantica e utilizzo reale della workforce;
2. monetizzazione effettiva del livestock;
3. riconciliazione quantitativa del Wheat/feed loop.

La decisione corretta è pertanto:

> **CONTINUE FUNCTIONAL VERIFY — workforce semantics + livestock monetization + feed reconciliation**

Questa fase deve essere breve e strettamente diagnostica.

Non fare tuning prestazionale.

Non eseguire ancora il benchmark da 30 episodi.

---

# 1. Obiettivo

Chiudere empiricamente tre condizioni necessarie prima del Performance VERIFY:

```text
A. HIRE → worker realmente disponibile → lavoro eseguito
B. COW → MILK → HARVEST → inventory → SELL → cash
C. Wheat produced + stock = Wheat fed + Wheat sold + final stock
```

Non considerare una capability `PASS` sulla base della sola emissione dell'azione.

La prova deve essere ricavata dallo **stato reale dell'environment**.

---

# 2. Principio di verifica

Per ciascuna delle tre aree distinguere:

```text
ORDERED
ACCEPTED
STATE CHANGED
PRODUCTIVE
MONETIZED
```

Un ordine inviato ma senza cambiamento dello stato non costituisce evidenza di capability esercitata.

---

# 3. Workforce — verificare la semantica reale di HIRE

E07-06 riporta:

```text
29 daily HIRE orders
```

ma la telemetria per worker mostra soltanto:

- Farmer;
- Hand 1;

mentre:

- Hand 2 = 0;
- Hand 3 = 0.

Questa incoerenza deve essere risolta.

## 3.1 Environment inspection

Ispezionare direttamente l'implementazione di `HIRE`.

Determinare:

- costo;
- quantità;
- quando l'ordine viene applicato;
- durata del contratto;
- numero massimo di hands;
- eventuale scadenza giornaliera;
- eventuale rinnovo;
- eventuale sostituzione anziché accumulo;
- condizioni di rifiuto.

Citare nel report:

- modulo/file;
- funzione;
- frammento rilevante.

---

# 4. Workforce state trace

In un test minimo controllato registrare per almeno alcuni giorni:

| Day | Hour | HIRE sent | HIRE accepted | Cash | Hands before | Hands after |
|---:|---:|---:|---:|---:|---:|---:|

In particolare osservare:

```text
D0 H00
D0 H23
D1 H00
D1 H01
D1 H23
D2 H00
```

Estendere se necessario.

La domanda da risolvere è:

> **HIRE crea workforce permanente, giornaliera o temporanea?**

---

# 5. Workforce target audit

Dopo aver chiarito la semantica, verificare se:

```python
target_workers = 4
```

significa realmente:

```text
1 Farmer + 3 Hands simultaneamente
```

oppure se la configurazione E07 è concettualmente errata.

Produrre:

| Metric | Value |
|---|---:|
| Maximum simultaneous Farmer | |
| Maximum simultaneous Hands observed | |
| Maximum simultaneous total workers | |
| Cost per Hand | |
| Effective duration | |
| Total HIRE orders | |
| Accepted HIRE orders | |
| Rejected/redundant HIRE orders | |

---

# 6. Workforce utilization correction

La telemetria deve identificare i worker **reali**, non slot teorici.

Se esiste soltanto un Hand per volta, non produrre:

```text
Hand 2 = 0
Hand 3 = 0
```

come se fossero worker esistenti.

Distinguere:

```text
configured target
actual concurrent workforce
worker-days purchased
worker-hours available
worker-hours productive
```

Questa distinzione deve rimanere disponibile per il successivo benchmark.

---

# 7. Livestock — chiudere il ciclo economico

E07-06 ha verificato:

```text
BUY_ANIMAL
PICKUP
BUILD_PASTURE
PLACE
FEED
```

ma Milk production è rimasta `PARTIAL` e non è stata dimostrata una vendita reale di Milk.

Questo non è ancora un Livestock Cashflow Engine verificato.

Dobbiamo ottenere empiricamente:

```text
COW
 ↓
fed
 ↓
MILK generated
 ↓
HARVEST
 ↓
worker inventory
 ↓
shed
 ↓
SELL
 ↓
farm["money"] increase
```

---

# 8. Environment inspection — livestock yield

Ispezionare direttamente:

- condizione di produzione Milk;
- frequenza;
- quantità;
- ruolo di `fed_today`;
- `yield_units`;
- eventuale maturazione;
- azione necessaria per raccolta;
- destinazione dopo `HARVEST`.

Verificare anche se:

```text
HARVEST pasture
```

ha semantica diversa da:

```text
HARVEST crop
```

Non inferire il comportamento.

---

# 9. Minimal Milk Proof

Creare un test/script diagnostico minimo e riproducibile.

Deve arrivare ad almeno:

```text
milk_generated >= 1
milk_harvested >= 1
milk_sold >= 1
```

Registrare:

```text
cash_before_sell
milk_quantity
sell_price / realized proceeds
cash_after_sell
```

e verificare:

```text
cash_after_sell > cash_before_sell
```

Produrre la prova numerica.

---

# 10. Full-agent Milk Proof

Dopo il test minimo, eseguire E07 in un singolo episodio diagnostico.

Non basta che il meccanismo funzioni nello script isolato.

Deve essere esercitato dall'agente E07.

Registrare:

| Metric | Value |
|---|---:|
| Cows purchased | |
| Cows placed | |
| Cow-days fed | |
| Milk generated | |
| Milk harvested | |
| Milk deposited | |
| Milk sold | |
| Milk revenue | |
| Unsold Milk final | |

Criterio minimo:

```text
Milk sold > 0
AND
Milk revenue > 0
```

---

# 11. Sheep / Wool

Non forzare l'acquisto di Sheep soltanto per completare questa verifica.

Se la configurazione corrente non compra Sheep prima del cutoff:

```text
Wool = N/A
```

è accettabile.

Non cambiare herd mix per ottenere artificialmente un PASS.

La relativa ottimizzazione resta OPEN.

---

# 12. Wheat accounting — riconciliazione fisica

E07-06 riporta contemporaneamente:

```text
49 Wheat produced
66 FEED actions
49 Wheat sold
```

Questi valori richiedono riconciliazione.

Costruire un vero ledger Wheat.

---

# 13. Wheat ledger

Registrare separatamente:

### Sources

```text
initial_wheat
wheat_harvested
wheat_bought_as_product
other_wheat_sources
```

Non confondere:

```text
WHEAT seed
```

con:

```text
WHEAT harvested product
```

### Uses

```text
wheat_picked_up
wheat_fed
wheat_sold
wheat_remaining_worker_inventory
wheat_remaining_shed
other_wheat_losses
```

---

# 14. Conservation equation

Al termine deve essere possibile verificare:

```text
initial product Wheat
+ harvested Wheat
+ purchased product Wheat
=
fed Wheat
+ sold Wheat
+ final Wheat
+ explicitly identified losses
```

La differenza deve essere:

```text
0
```

oppure completamente spiegata dalla meccanica dell'environment.

---

# 15. FEED success semantics

Verificare inoltre se i precedenti:

```text
66 FEED
```

rappresentavano:

- azioni `FEED` inviate;
- azioni accettate;
- Wheat realmente consumato;
- oppure semplicemente task assegnati.

La telemetria deve distinguere almeno:

```text
feed_attempted
feed_successful
wheat_consumed
```

Non dichiarare `66 Wheat consumed` sulla base di 66 comandi emessi.

---

# 16. Correzioni consentite

Sono consentite esclusivamente correzioni necessarie a rendere coerente l'implementazione con le meccaniche reali appena verificate.

Esempi:

- HIRE interpretato erroneamente;
- telemetria workforce errata;
- Milk non raccolto;
- Milk non inviato al MarketBroker;
- FEED conteggiato come successo quando non consuma Wheat;
- Wheat ledger errato.

Non modificare per tuning:

- crop ratios;
- herd target;
- expansion day;
- cutoff economici;
- cash reserve;
- numero target di worker,

a meno che il valore sia **semanticamente impossibile** nell'environment.

---

# 17. Test

Aggiungere test mirati per le correzioni effettuate.

Eseguire:

```powershell
.venv\Scripts\pytest tests/
```

Tutta la suite E01–E07 deve restare verde.

---

# 18. Diagnostic smoke finale

Dopo le eventuali correzioni eseguire **un solo episodio E07 da 720 step**.

Registrare almeno:

### Economy

```text
Final Money
```

### Workforce

```text
peak simultaneous workers
worker-days
productive worker actions
movement
idle
HIRE cost
```

### Livestock

```text
cows
feed successful
Wheat consumed
Milk generated
Milk harvested
Milk sold
Milk revenue
```

### Wheat

```text
harvested
fed
sold
final stock
ledger delta
```

Non usare Final Money come criterio di tuning.

---

# 19. Acceptance criteria

## Workforce PASS

Solo se:

- semantica HIRE verificata;
- workforce concorrente reale misurata;
- telemetria coerente con lo stato dell'environment.

## Livestock PASS

Solo se E07 produce realmente:

```text
Milk sold > 0
Milk revenue > 0
```

## Feed PASS

Solo se:

```text
Wheat ledger delta == 0
```

o esiste una spiegazione verificata e documentata dell'eventuale differenza.

---

# 20. Decisione

### GO FOR PERFORMANCE VERIFY

Solo se:

```text
Workforce = PASS
Livestock monetization = PASS
Feed accounting = PASS
```

### CONTINUE BUILD

Se una delle tre capability resta bloccata da un bug implementativo.

### RETURN TO PLAN

Se una meccanica verificata dell'environment invalida una parte sostanziale della configurazione competitiva.

---

# 21. Documentazione

Creare:

```text
docs/versions/E07_verify_functional_closure.md
```

Aggiornare:

```text
docs/PROJECT_STATE.md
docs/NEW_SESSION.md
```

Aggiornare `E07_verify_functional_utilization.md` soltanto se necessario per correggere conclusioni fattualmente errate.

In particolare non lasciare documentato come `PASS` ciò che questa fase dimostra essere soltanto `PARTIAL`.

---

# 22. Git

Al termine mostrare:

```powershell
git status --short
git diff --stat
```

Non:

- commit;
- push;
- tag;
- build submission;
- Kaggle submission.

---

# 23. Output finale

Mostrare:

1. semantica reale di `HIRE`;
2. trace workforce;
3. peak simultaneous workforce;
4. worker-days / worker-hours;
5. lifecycle Milk verificato;
6. prova numerica `MILK → SELL → cash`;
7. Milk revenue nello smoke E07;
8. Wheat ledger completo;
9. `feed_attempted`;
10. `feed_successful`;
11. `wheat_consumed`;
12. conservation delta;
13. bug/correzioni effettuate;
14. risultato `pytest`;
15. Final Money diagnostico;
16. parametri ancora OPEN;
17. decisione finale.

**FERMARSI QUI.**

Non eseguire ancora il benchmark da 30 episodi.

Il Performance VERIFY inizierà soltanto dopo la chiusura empirica di workforce, livestock monetization e feed accounting.