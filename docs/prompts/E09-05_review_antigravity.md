# E09-05 — REVIEW — Livestock Subsystem Ablation

## Stato approvato

La fase **E09-04 VERIFY — Livestock Subsystem Ablation** è approvata.

E09-05 è esclusivamente una fase di **REVIEW diagnostico**.

**NON modificare la strategia.**
**NON ottimizzare E09-01.**
**NON creare E10.**
**NON costruire o inviare submission Kaggle.**
**NON fare commit, push o tag.**

L'obiettivo è interpretare rigorosamente l'evidenza prodotta dal benchmark paired e identificare quale problema resta da risolvere.

---

# 1. Evidenza VERIFY da preservare

Dataset principale:

`results/e09_livestock_ablation.json`

Confronto causale primario:

```text
E08 — 40 tile — Livestock ON
vs
E09-01 — 40 tile — Livestock OFF
```

Il benchmark VERIFY ha rieseguito le varianti sugli stessi 30 episodi/semi.

Per il confronto causale E08/E09-01 devono quindi essere utilizzati **i valori paired prodotti da questa esecuzione**, non i valori storici E08 provenienti da benchmark precedenti.

## Risultati paired correnti

### E08
- Mean Final Money: **$11,468.53**
- Median Final Money: **$9,994.00**
- Sample SD (`ddof=1`): **$6,643.06**
- W/D/L: **27 / 0 / 3**
- Win Rate: **90.0%**

### E09-01
- Mean Final Money: **$22,899.20**
- Median Final Money: **$27,672.00**
- Sample SD (`ddof=1`): **$7,892.99**
- Min / Max: **$5,788 / $28,408**
- W/D/L: **30 / 0 / 0**
- Win Rate: **100.0%**

### Delta causale
- Mean delta: **+$11,430.67**
- Relative delta: **+99.67%**
- Median delta: **+$17,678**
- Paired wins E09-01 vs E08: **26/30 (86.7%)**

Il precedente valore storico E08:

**$11,880.30**

deve restare documentato come risultato del precedente benchmark E08, ma **non deve sostituire il valore paired $11,468.53 nel test causale E09**.

---

# 2. Riferimenti secondari

## E07
E07 resta un riferimento storico secondario:

- 24 tile
- Livestock ON
- paired VERIFY current mean: **$12,578.73**

E09-01:

- 40 tile
- Livestock OFF
- mean: **$22,899.20**

Delta secondario:

**+$10,320.47 (+82.05%)**

Non usare E07 come baseline causale.

---

## E06 — Shipped Baseline

E06 è il riferimento competitivo interno più importante:

### E06
- Mean Final Money: **$24,731.37**
- Sample SD: **$1,859.19**
- Median: **$25,847.00**
- Min: **$22,180**
- Max: **$27,873**
- W/D/L: **30 / 0 / 0**

### E09-01
- Mean Final Money: **$22,899.20**
- Sample SD: **$7,892.99**
- Median: **$27,672.00**
- Min: **$5,788**
- Max: **$28,408**
- W/D/L: **30 / 0 / 0**

Ulteriore evidenza già riportata dal VERIFY:

> E09-01 supera E06 in **21 episodi su 30 (70.0%)**.

Questo apparente contrasto è il centro diagnostico del REVIEW:

> **E09-01 vince frequentemente contro E06 e ha una mediana maggiore, ma perde sulla media a causa di una forte coda negativa.**

---

# 3. Obiettivi del REVIEW

Il REVIEW deve rispondere rigorosamente a tre domande.

## Q1 — L'ablation livestock è causalmente confermata?

Verifica che i dati supportino davvero la conclusione:

> **Il livestock è un structural value sink nella configurazione E08 da 40 tile.**

Controlla:

- paired deltas;
- distribuzione dei paired deltas;
- risultati per opponent;
- eventuali eccezioni;
- episodi in cui E08 batte E09-01;
- possibili confondenti;
- correttezza dell'implementazione rispetto al DEFINE.

Distingui:

### effetto diretto
- capitale non speso in animali;
- feed buffer rimosso;
- perdite livestock eliminate.

### effetto indiretto
- maggiore capitale per seed;
- maggiore utilizzo delle crop tile;
- worker actions liberate;
- movement liberato;
- maggiore capacità di watering/harvesting/planting.

Non limitarti al saldo economico diretto.

---

# 4. Audit della varianza E09-01

Questa è la priorità diagnostica principale.

E09-01 presenta:

```text
Mean   = $22,899.20
Median = $27,672.00
SD     = $7,892.99
Min    = $5,788
Max    = $28,408
```

La distanza enorme Mean/Median e la SD molto elevata indicano una distribuzione fortemente asimmetrica o multimodale.

Identifica esattamente gli episodi che generano la coda negativa.

Per ogni episodio E09-01 estrai almeno:

- episode index;
- seed;
- opponent;
- Final Money;
- E08 Final Money sullo stesso seed;
- E06 Final Money sullo stesso seed;
- delta E09-01 − E08;
- delta E09-01 − E06.

Ordina gli episodi E09-01 dal peggiore al migliore.

---

# 5. Identificazione degli outlier

Non applicare automaticamente una definizione statistica arbitraria.

Esamina almeno:

- bottom 5 episodi;
- episodi sotto $10,000;
- episodi sotto la media;
- eventuali cluster naturali della distribuzione.

Calcola, se utile e direttamente derivabile dai dati:

- quartili;
- IQR;
- coefficient of variation;
- trimmed mean;
- mean senza bottom 1 / bottom 3 / bottom 5;
- opponent-specific means;
- opponent-specific medians;
- opponent-specific SD.

Queste statistiche servono a capire la struttura della distribuzione, NON a rimuovere episodi dal risultato ufficiale.

La metrica ufficiale resta quella sui 30 episodi completi.

---

# 6. Diagnosi per opponent

Verifica se la coda negativa è:

- concentrata contro `pass`;
- concentrata contro `random`;
- concentrata contro `starter`;
- oppure dipendente soprattutto dal seed.

Per ogni opponent produci:

| Opponent | N | Mean | Median | SD | Min | Max |
|---|---:|---:|---:|---:|---:|---:|

per almeno:

- E06;
- E08;
- E09-01.

Confronta inoltre i paired deltas E09-01/E08 ed E09-01/E06 per opponent.

---

# 7. Diagnosi degli episodi deboli

Per gli episodi E09-01 peggiori, usa la telemetria già presente nel JSON e nel runner.

Cerca differenze rispetto agli episodi E09-01 forti in:

- seed spending;
- seed purchases;
- crop allocation;
- Melon planting;
- Melon revenue;
- Carrot revenue;
- Wheat revenue;
- active productive tiles;
- `plant_pending`;
- watering;
- harvesting;
- movement share;
- worker utilization;
- idle actions;
- cash trajectory, se disponibile;
- timing di `BUY_LAND`;
- timing delle assunzioni;
- eventuali failure/fallback;
- inventory finale;
- liquidation;
- altre metriche già registrate.

Non aggiungere nuova strumentazione al codice produttivo durante REVIEW.

Se una metrica necessaria non è disponibile, dichiararlo.

---

# 8. Verificare l'ipotesi "40 tile recuperati"

Il risultato E09-01 modifica l'interpretazione di E08.

E08 aveva mostrato:

```text
24 tile + livestock ON
        ↓
40 tile + livestock ON
performance peggiora
```

E09-01 mostra:

```text
40 tile + livestock OFF
performance quasi raddoppia rispetto a E08
```

Valuta quindi rigorosamente questa conclusione:

> **E08 non ha dimostrato che 40 tile siano intrinsecamente inefficienti; ha dimostrato che la configurazione 40 tile + livestock era inefficiente.**

Verifica però se i dati consentono davvero di affermare che il footprint da 40 tile è produttivamente sfruttato in E09-01.

Usa:

- tile utilization;
- planting;
- harvest;
- revenue;
- backlog;
- movement;
- altre metriche disponibili.

Se i 40 tile sono ancora parzialmente inutilizzati, dichiararlo.

---

# 9. Confronto strutturale E06 vs E09-01

Questo confronto deve essere trattato con particolare attenzione.

E06 ha:

- media superiore;
- SD molto più bassa;
- minimo molto più alto.

E09-01 ha:

- mediana superiore;
- massimo superiore;
- 21/30 paired wins contro E06;
- ma media inferiore.

La domanda non è semplicemente:

> quale agente è migliore?

La domanda è:

> **Perché E09-01 produce risultati superiori nella maggioranza degli episodi ma subisce pochi episodi abbastanza negativi da perdere sulla media?**

Costruisci una tabella degli episodi in cui:

```text
E09-01 < E06
```

e analizza la dimensione delle perdite.

Confrontala con gli episodi:

```text
E09-01 > E06
```

e la dimensione dei guadagni.

Calcola almeno:

- numero paired wins/losses/ties;
- mean gain nei paired wins;
- mean loss nei paired losses;
- max gain;
- max loss;
- contribution dei bottom episodes al delta medio complessivo.

---

# 10. Verifica di possibili failure modes

Senza modificare il codice, determina se gli episodi deboli sembrano associati a uno o più failure mode ricorrenti.

Possibili categorie da verificare, NON da assumere:

- insufficiente watering capacity;
- backlog di planting;
- movimento eccessivo;
- worker partitioning inefficiente;
- espansione Q1 prematura;
- seed/cash allocation instabile;
- dipendenza da market dynamics;
- crop mix fragile;
- timing di harvest/liquidation;
- worker contention;
- idle/fallback behavior;
- incapacità di sfruttare uniformemente i 40 tile.

Classifica i failure mode solo se supportati dai dati.

Per ciascuno indica:

- evidenza;
- episodi coinvolti;
- metriche che lo supportano;
- livello di confidenza: HIGH / MEDIUM / LOW.

---

# 11. Nessuna ottimizzazione durante REVIEW

È fondamentale separare:

```text
diagnosi
```

da:

```text
soluzione
```

Durante E09-05:

- NON cambiare soglie;
- NON cambiare crop ratios;
- NON cambiare footprint;
- NON cambiare worker assignment;
- NON cambiare Water-First;
- NON cambiare land expansion;
- NON reintrodurre livestock;
- NON implementare fallback;
- NON creare una nuova strategia.

Puoi formulare **candidate hypotheses** per l'esperimento successivo, ma non implementarle.

---

# 12. Candidate hypotheses per il prossimo esperimento

Solo dopo l'analisi, elenca al massimo **3 candidate hypotheses**.

Per ciascuna:

1. failure mode osservato;
2. evidenza quantitativa;
3. singola variabile che potrebbe essere modificata;
4. risultato atteso;
5. rischio di confondimento.

NON scegliere automaticamente la soluzione più complessa.

Preferisci ipotesi che:

- affrontino la coda negativa;
- preservino i punti di forza E09-01;
- modifichino una sola dimensione;
- siano verificabili con paired benchmark.

Non assegnare ancora un ID E10 definitivo se l'evidenza non giustifica una scelta.

---

# 13. Documentazione REVIEW

Crea:

`docs/versions/E09_review_livestock_ablation.md`

seguendo la convenzione del repository.

Il documento deve includere almeno:

1. Executive finding;
2. conferma/falsificazione dell'ipotesi E09;
3. confronto paired E08/E09-01;
4. distinzione E08 paired vs E08 historical;
5. distribuzione E09-01;
6. tabella episodi ordinati;
7. analisi bottom episodes;
8. breakdown per opponent;
9. confronto E06/E09-01;
10. diagnosi dei failure mode;
11. interpretazione del footprint 40 tile;
12. limiti dell'evidenza;
13. candidate hypotheses;
14. raccomandazione per il prossimo passo.

Aggiorna:

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;

allo stato:

```text
E09-05 REVIEW COMPLETED
```

solo dopo aver completato l'analisi.

---

# 14. Correzione terminologica

Nel REVIEW evita formulazioni eccessivamente forti non supportate.

La conclusione:

> `LIVESTOCK IS A STRUCTURAL VALUE SINK IN E08 CONFIGURATION`

è accettabile solo specificando:

> **nell'architettura e nelle condizioni testate di E08**

Non generalizzare a:

- livestock in Kaggriculture in assoluto;
- ogni strategia livestock;
- ogni configurazione di footprint;
- ogni opponent/environment.

La conclusione è locale all'esperimento.

---

# 15. Git e Kaggle

Durante REVIEW:

- puoi leggere repository e risultati;
- puoi creare script diagnostici in `scratch/` se strettamente necessari;
- puoi aggiornare documentazione;
- NON modificare codice produttivo;
- NON modificare entrypoint;
- NON costruire submission;
- NON accedere a Kaggle;
- NON aprire browser;
- NON fare commit;
- NON fare push;
- NON creare tag.

---

# STOP OBBLIGATORIO

Al termine del REVIEW:

**FERMATI.**

NON iniziare il prossimo esperimento.

NON implementare candidate hypotheses.

NON creare E10 autonomamente.

NON eseguire nuovi benchmark produttivi.

NON inviare submission Kaggle.

Attendi la decisione del supervisore.

---

# Output finale richiesto

Restituisci un report sintetico ma quantitativamente completo:

## 1. Verdict E09
Una delle seguenti:

**E09 HYPOTHESIS CONFIRMED**

oppure

**E09 HYPOTHESIS FALSIFIED**

oppure

**E09 RESULT INCONCLUSIVE**

con motivazione.

## 2. Causal evidence
Riporta il confronto paired E08/E09-01.

## 3. Variance diagnosis
Spiega quantitativamente perché Mean e Median E09-01 divergono.

## 4. Bottom episodes
Tabella degli episodi responsabili della coda negativa.

## 5. Opponent analysis
Determina se il problema è opponent-specific o seed/state-specific.

## 6. E06 comparison
Spiega perché E09-01 vince 21/30 episodi ma perde sulla media.

## 7. Failure modes
Elenco ordinato dei failure mode supportati dall'evidenza con confidence level.

## 8. 40-tile interpretation
Stabilisci cosa possiamo e non possiamo concludere sul productive scaling.

## 9. Candidate hypotheses
Massimo tre, senza implementazione.

## 10. File modificati
Elenco completo.

## 11. Raccomandazione
Indica quale domanda sperimentale dovrebbe affrontare il prossimo ciclo, senza implementarlo.

Concludi con:

**READY FOR SUPERVISOR DECISION**

---

# Principio metodologico finale

E09-01 ha già dimostrato un grande miglioramento rispetto a E08.

Il REVIEW non deve cercare ulteriori motivi per dichiararlo vincente.

Deve spiegare il problema ancora irrisolto:

> **Perché E09-01 è migliore di E06 nella maggioranza degli episodi, ma alcuni episodi molto deboli abbassano la sua media sotto E06?**

Questa diagnosi deve guidare il prossimo esperimento.
