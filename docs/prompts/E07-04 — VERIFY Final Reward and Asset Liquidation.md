# E07-04 — VERIFY Final Reward and Asset Liquidation

Stiamo lavorando al progetto **Kaggriculture Agent**.

Le fasi precedenti sono:

- `E07-01 — DEFINE Competitive Baseline Reconstruction`
- `E07-02 — VERIFY Competitive Evidence`
- `E07-03 — PLAN Configurable Competitive Baseline`

Prima di iniziare il BUILD dobbiamo verificare una meccanica fondamentale:

> **Che cosa contribuisce realmente al reward finale di Kaggriculture e quali asset possono essere convertiti in `farm["money"]` prima del termine dell'episodio?**

Questa verifica deve essere eseguita direttamente sul codice dell'environment installato localmente.

Non modificare il codice dell'agente.

---

# 1. Domande da risolvere

Verificare con precisione:

1. se il reward finale coincide con:
   ```python
   farm["money"]
   ```

2. se al termine dei 720 step vengono automaticamente valorizzati:
   - crops ancora sul terreno;
   - inventory;
   - livestock;
   - land acquistata;
   - structures;
   - altri asset;

3. quali asset possono essere venduti esplicitamente prima della fine;

4. quali asset non possono essere convertiti in cash;

5. se esistono:
   - `SELL_ANIMAL`;
   - vendita livestock tramite market;
   - refund;
   - resale value;
   - valore terminale automatico;

6. cosa accade all'inventory ancora presente al turno finale;

7. cosa accade agli animali ancora posseduti;

8. cosa accade alle colture:
   - mature;
   - immature;
   - non raccolte;

9. cosa accade a:
   - land;
   - pasture;
   - buildings/structures.

---

# 2. Verifica diretta dell'environment

Ispezionare almeno:

- `kaggle_environments.envs.kaggriculture.kaggriculture`;
- `interpreter`;
- reward calculation;
- action handling;
- market handling;
- livestock handling;
- final episode termination.

Individuare nel codice:

```text
reward assignment
farm["money"]
done / termination
market sale
animal purchase/sale
inventory
land
structures
```

Per ogni conclusione indicare:

- file/modulo;
- funzione;
- frammento rilevante;
- comportamento verificato.

---

# 3. Action Space

Produrre l'elenco reale delle azioni disponibili nell'environment.

Evidenziare in particolare se esistono realmente azioni equivalenti a:

```text
BUY_ANIMAL
SELL_ANIMAL
BUY_LAND
SELL_LAND
BUILD
SELL_STRUCTURE
SELL_PRODUCT
```

Non assumere l'esistenza di azioni derivate da README, discussioni o precedenti inferenze.

---

# 4. Terminal Value Audit

Creare la seguente tabella:

| Asset | Contributes automatically to final reward? | Can be liquidated? | Mechanism | Terminal risk |
|---|---|---|---|---|
| Cash | | | | |
| Crop inventory | | | | |
| Mature crops on field | | | | |
| Immature crops | | | | |
| Cows | | | | |
| Sheep | | | | |
| Land | | | | |
| Structures | | | | |

Usare esclusivamente valori:

- `YES`
- `NO`
- `CONDITIONAL`
- `UNVERIFIED`

---

# 5. Verifica sperimentale minima

Se utile e non invasivo, creare un piccolo script temporaneo o comando Python che dimostri almeno:

### Test A — Cash

Episodio terminato con cash noto.

Verificare:

```text
reward == farm["money"]
```

### Test B — Inventory

Terminare un episodio con prodotto ancora in inventory.

Verificare se il reward aumenta automaticamente del suo valore.

### Test C — Livestock

Terminare con almeno un animale posseduto.

Verificare se il suo valore contribuisce automaticamente al reward.

### Test D — Field asset

Terminare con crop non raccolto.

Verificare se produce terminal value.

Non modificare il codice applicativo dell'agente per eseguire questi controlli.

---

# 6. Rivalutazione dell'End-Game Policy E07

Sulla base dell'evidenza, rivalutare il PLAN E07.

In particolare verificare la correttezza delle affermazioni:

```text
sell-off totale inventory
sell-off totale animali
liquidazione asset Giorno 29–30
```

Classificare ciascuna come:

- `VALID`
- `PARTIALLY VALID`
- `INVALID`
- `UNVERIFIED`

Se la vendita degli animali non esiste, rimuovere esplicitamente questa ipotesi dal piano.

---

# 7. Distinguere produzione e scoring

Esplicitare nel rapporto che:

```text
productive capacity != final reward
```

e distinguere:

### Final Money

Cash realmente presente al termine.

### Farm Productive Capacity

Capacità dell'azienda di produrre cash nel tempo.

### Residual Asset Value

Valore economico teorico degli asset ancora presenti.

### Kaggle Reward

Valore effettivamente utilizzato dall'environment per il punteggio.

Indicare quali di questi coincidono e quali no.

---

# 8. Conseguenze per E07

Determinare come questa meccanica deve influenzare:

- livestock strategy;
- crop cutoff;
- market policy;
- inventory management;
- late-game reinvestment;
- land expansion;
- workforce hiring;
- end-game phase.

In particolare:

> se un asset non contribuisce al reward terminale e non può essere venduto, ogni investimento tardivo in quell'asset deve essere trattato come capitale immobilizzato.

---

# 9. Correzione documentale

Creare:

`docs/versions/E07_verify_final_reward.md`

Aggiornare, se necessario:

- `docs/plans/E07_Competitive_Baseline_Reconstruction.md`;
- `docs/versions/E07_plan_competitive_baseline.md`;
- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`.

Correggere eventuali riferimenti non validi a:

- vendita finale animali;
- terminal asset value;
- liquidazione automatica;
- reward.

Non modificare il codice dell'agente.

---

# 10. Decisione

Terminare con una delle seguenti:

### GO FOR BUILD

La meccanica terminale è chiara e il PLAN rimane valido.

### GO FOR BUILD WITH END-GAME CORRECTIONS

L'architettura E07 rimane valida ma la policy di liquidazione deve essere corretta.

### RETURN TO PLAN

La meccanica terminale cambia significativamente l'architettura proposta.

---

# 11. Output finale richiesto

Mostrare:

1. formula reale del reward finale;
2. elenco action space rilevante;
3. Terminal Value Audit;
4. risultato dei test sperimentali;
5. asset liquidabili;
6. asset non liquidabili;
7. eventuali claim precedenti errati;
8. nuova End-Game Policy;
9. modifiche apportate al PLAN;
10. decisione finale.

**FERMARSI QUI.**

Non:

- implementare E07;
- modificare `src/agricola/`;
- eseguire benchmark E07;
- creare submission;
- inviare submission Kaggle;
- creare tag.

Attendere la revisione prima del BUILD.