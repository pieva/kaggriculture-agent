# E08-05B — REVIEW Correction Pass Productive Scale Optimization

## Contesto

Stiamo lavorando al progetto **Kaggriculture**, esperimento **E08 — Productive Scale Optimization**.

La fase **E08-05 REVIEW** è stata completata con decisione preliminare:

> `REVIEW COMPLETE — READY TO CLOSE E08`

La REVIEW è sostanzialmente valida, ma **NON è ancora approvata per la chiusura** perché contiene alcune affermazioni più forti delle evidenze disponibili e una proposta E09 che modifica troppe variabili contemporaneamente.

Questa fase è un **correction pass della REVIEW**, non una nuova fase sperimentale.

Documenti prioritari:

- `docs/versions/E08_review_productive_scale.md`
- `docs/versions/E08_verify_functional_utilization.md`
- `docs/versions/E08_verify_local_performance.md`
- `docs/versions/E08_verify_competitive_evidence.md`
- `results/e08_productive_scale.json`
- `results/e07_competitive_baseline.json`
- documentazione e risultati E06 disponibili
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Esamina anche il codice/telemetria solo quando necessario per stabilire l'origine esatta di una metrica.

---

# Obiettivo

Correggere la REVIEW E08 in quattro punti obbligatori:

1. eliminare definitivamente il falso `54.2% movement share` attribuito a E07;
2. verificare le metriche E06 e usare `N/A` quando non esiste una misurazione reale;
3. riconciliare esplicitamente `minimum cash = $339` vs `$177.40`;
4. riscrivere la raccomandazione E09 come **esperimento di ablazione livestock a singola variabile primaria**, senza contemporaneo redesign della scala, geometria o workforce.

NON modificare i risultati sperimentali originali.

NON modificare il codice della strategia.

NON iniziare E09.

---

# C1 — Correzione definitiva del 54.2%

Nella REVIEW compare ancora:

> `Movement Share E07 = 54.2% (est)`

Questa informazione è errata.

Il **54.2%** deriva dalla stima DEFINE:

- circa 52 azioni produttive/giorno;
- 96 worker-turn/giorno;
- `52 / 96 ≈ 54.2%`.

Rappresenta quindi:

> **estimated productive workload share**

NON:

> movement share.

Azioni obbligatorie:

- cerca tutte le occorrenze nella documentazione E08 in cui `54.2%` viene associato a movement E07;
- correggile;
- nella tabella E06/E07/E08 usa per E07 movement:
  - il valore realmente misurato, se esiste una telemetria comparabile;
  - altrimenti **`N/A`**.

NON usare:

- `54.2%`;
- `~54.2%`;
- `54.2% (est)`

come movement share E07.

Se il valore viene mantenuto altrove, deve essere etichettato esclusivamente come stima del **productive workload**.

---

# C2 — Audit delle metriche E06

La REVIEW riporta, tra le altre:

- E06 Movement Share `~32.0%`;
- E06 backlog `~0.0 tile/giorno`;
- E06 `9.0 tile (100% attive)`.

Questi valori devono essere considerati dati sperimentali soltanto se esiste una fonte misurata e verificabile.

Per ciascuna metrica E06 riportata nella tabella comparativa:

1. identifica il file sorgente;
2. identifica il campo, log o calcolo da cui deriva;
3. verifica che la metrica abbia la stessa definizione utilizzata in E08;
4. verifica che il protocollo sia sufficientemente comparabile.

Se non è possibile dimostrarlo:

> sostituisci il valore con **`N/A`**.

Non utilizzare stime intuitive basate sulla geometria o sul comportamento atteso.

In particolare:

- `9 tile target` può essere mantenuto se deriva dalla configurazione;
- `9.0 mean active / 100% active` richiede telemetria reale;
- `~32% movement` richiede telemetria reale;
- `~0 backlog` richiede telemetria reale.

La tabella deve distinguere chiaramente:

- **configuration fact**;
- **measured metric**;
- **N/A**.

---

# C3 — Riconciliazione cash `$339` vs `$177.40`

Nei documenti E08 compaiono due valori:

- **$339.00** minimum cash nella Functional Verify diagnostica;
- **$177.40** minimum cash nella REVIEW.

Determina esattamente l'origine dei due valori.

Verifica se:

- `$339` appartiene al singolo episodio diagnostico V1;
- `$177.40` rappresenta il minimo osservato sull'intero benchmark dei 30 episodi;
- oppure se uno dei valori deriva da un errore di calcolo/documentazione.

La REVIEW corretta deve indicare esplicitamente:

| Metrica | Scope | Valore | Fonte |
|---|---|---:|---|
| Minimum cash diagnostic | episodio V1 | ... | ... |
| Minimum cash benchmark | 30 episodi / episodio specifico | ... | ... |

Se `$177.40` è realmente osservato, chiarisci inoltre:

- se rappresenta una violazione del cash floor `$300`;
- quale tipo di azione ha causato la discesa;
- se il floor proteggeva soltanto gli acquisti sementi;
- se la discesa sotto `$300` era dovuta ad altre spese già consentite dalla strategia.

Non affermare contemporaneamente:

> "cash floor rispettato"

e

> "minimum cash $177.40"

senza spiegare lo scope della policy.

La conclusione deve stabilire se la liquidità è:

- `NOT MATERIAL`;
- `SECONDARY CONSTRAINT`;
- `STRONG CANDIDATE`;
- `DEMONSTRATED BOTTLENECK`.

Motivare esclusivamente con evidenze.

---

# C4 — Revisione del finding Workforce

La REVIEW attuale classifica:

> `Workforce Density & Layout = DEMONSTRATED BOTTLENECK`

Riesamina questa formulazione.

E08 dimostra certamente:

- movement molto elevato;
- backlog `plant_pending` elevato;
- mancato raggiungimento delle 40 tile realmente produttive.

Ma questi dati NON distinguono necessariamente fra:

1. numero assoluto di worker insufficiente;
2. layout troppo disperso;
3. scheduling inefficiente;
4. overhead livestock/feed;
5. combinazione dei fattori.

Pertanto non attribuire causalità al **numero di worker** se non isolata sperimentalmente.

Se necessario, riclassifica:

- **Movement / geographic dispersion** separatamente;
- **Workforce count sufficiency** separatamente.

Possibili livelli:

- `DEMONSTRATED`
- `STRONG CANDIDATE`
- `UNCONFIRMED`
- `NOT MATERIAL`

Una formulazione ammissibile, se coerente con i dati, è:

> E08 dimostra un problema di throughput operativo dell'architettura corrente, ma non dimostra che la causa sia semplicemente un numero insufficiente di worker.

---

# C5 — Livestock finding: mantenere il livello corretto di evidenza

La REVIEW riporta:

- spesa livestock/pascoli circa `$4,426`;
- ricavi latte/lana circa `$449`;
- saldo diretto circa `-$3,977`.

Verifica i valori nelle fonti.

Se confermati, mantienili come evidenza economica diretta.

Tuttavia distingui:

> **livestock subsystem has poor direct financial balance**

da:

> **livestock causes the E07/E08 performance collapse**

La seconda affermazione richiede un'ablazione causale che non è ancora stata eseguita.

Pertanto, salvo nuove evidenze già presenti nei dati:

> **Livestock overhead = STRONG CANDIDATE**

NON:

> demonstrated cause.

Non inventare una quota percentuale di worker-turn attribuibile al livestock se non direttamente misurata.

---

# C6 — Riscrittura della tabella E06 / E07 / E08

Aggiorna la tabella architetturale usando soltanto dati verificabili.

Struttura consigliata:

| Dimensione | E06 | E07 | E08 | Tipo evidenza / fonte |
|---|---:|---:|---:|---|
| Mean Final Money paired | | | | |
| Target crop tiles | | | | |
| Mean active tiles | | | | |
| Peak active tiles | | | | |
| Workforce | | | | |
| Livestock | | | | |
| Movement share | | | | |
| Plant backlog | | | | |
| Livestock direct net | | | | |

Usa **`N/A`** quando necessario.

Non utilizzare `~` per trasformare una stima in una misura.

Se una metrica proviene da un protocollo differente, indicarlo.

---

# C7 — E09: una sola variabile primaria

La proposta precedente E09 combinava:

- eliminazione livestock;
- eliminazione pascoli;
- ricompattamento a 16 tile;
- layout solo Q0;
- variazione workforce 2–3;
- nuovo target movement;
- nuovo target economico.

Questa configurazione NON consente attribuzione causale.

La raccomandazione E09 deve essere riscritta come **ablazione controllata del sottosistema livestock**.

## Domanda sperimentale raccomandata

Formulare in modo equivalente a:

> **A parità dell'architettura E07, quale effetto produce l'ablazione completa del sottosistema livestock e del relativo feed loop sulla performance economica e sull'efficienza operativa?**

## Variabile indipendente primaria

Una sola:

> **Livestock subsystem ON → OFF**

L'ablazione comprende esclusivamente gli elementi che esistono perché necessari al livestock:

- 4 Cows → 0;
- 2 Sheep → 0;
- pascoli dedicati → rimossi/non acquistati;
- FEED actions → rimosse;
- Wheat feed loop → rimosso o disattivato;
- acquisti/costi esclusivamente livestock → rimossi.

ATTENZIONE:

La rimozione del Wheat feed loop è parte dell'ablazione livestock perché dipende causalmente dal sottosistema eliminato; non deve però essere utilizzata per introdurre contemporaneamente un nuovo redesign generale della crop strategy.

---

# C8 — Variabili E09 da congelare

La raccomandazione deve mantenere, per quanto tecnicamente possibile, la struttura **E07**, non E08.

Congelare:

- target crop footprint E07: **24 tile**;
- 4 worker;
- acquisto Q1 / timing E07;
- geometria/layout E07, salvo tile fisicamente occupate da elementi livestock rimossi;
- task priority Water-First per le attività rimaste;
- crop policy E07, con il minimo adattamento necessario per le Wheat che non servono più al feed;
- liquidation policy;
- market policy;
- dispatcher/spatial policy E07;
- seed/opponent benchmark protocol.

NON introdurre in E09 DEFINE, salvo successiva approvazione:

- 16 tile;
- layout solo Q0;
- 2 worker;
- 3 worker;
- nuova espansione terreno;
- nuova geometria ottimizzata;
- nuovo dispatcher;
- ulteriori crop optimization.

L'obiettivo E09 deve essere isolare il valore causale dell'ablazione livestock.

---

# C9 — Baseline E09

Definisci una sola baseline primaria sperimentale.

La baseline naturale deve essere **E07**, perché E09 deve rappresentare:

> E07 con livestock ON  
> vs  
> E09 con livestock OFF

con il resto mantenuto il più possibile invariato.

E06 resta:

> riferimento architetturale/economico secondario.

Non usare contemporaneamente E06 ed E07 come "baseline primaria".

Per il benchmark futuro utilizzare valori derivati dallo stesso protocollo paired.

---

# C10 — Metriche raccomandate E09

La REVIEW corretta deve raccomandare almeno:

## Economiche

- Mean Final Money;
- Median;
- Standard Deviation;
- delta E09 − E07;
- breakdown per opponent.

## Operative

- movement share;
- productive/action share;
- idle share;
- `plant_pending`;
- `needs_water`;
- `harvest_ready`;
- mean/peak active crop tiles.

## Ablation accounting

- livestock purchase cost eliminato;
- pasture cost eliminato;
- feed/Wheat cost eliminato;
- milk/wool revenue perso;
- worker actions liberate, se misurabili;
- movement associato al sottosistema eliminato, se misurabile.

Non fissare ancora come requisito arbitrario:

- `<35% movement`;
- `>$24,000 Mean Final Money`.

Questi possono essere riferimenti diagnostici, non criteri necessari di successo dell'ablazione.

Il criterio primario E09 dovrà essere il confronto causale con E07.

---

# C11 — Decisione E08 invariata

Salvo che l'audit trovi errori sostanziali nei risultati:

- E08 resta **falsificato**;
- E08 resta **NON candidata a Kaggle**;
- codice, risultati e documentazione E08 devono essere conservati come evidenza sperimentale;
- E06 resta la baseline competitiva shipped attiva;
- E07/E08 restano esperimenti diagnostici.

NON effettuare rollback.

NON cancellare file E08.

---

# Deliverable

Aggiorna:

`docs/versions/E08_review_productive_scale.md`

Inserisci una sezione esplicita:

> `Review Correction Pass`

oppure integra le correzioni mantenendo tracciabile ciò che è stato rettificato.

Crea inoltre:

`docs/versions/E08_review_corrections.md`

con una tabella:

| Finding originale | Problema | Evidenza verificata | Correzione |
|---|---|---|---|

Deve includere obbligatoriamente:

1. `54.2% E07 movement`;
2. metriche E06 non misurate;
3. `$339 vs $177.40`;
4. workforce causality;
5. livestock causality;
6. redesign E09 multi-variabile → ablazione controllata.

Aggiorna:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

---

# Git

Al termine esegui:

```powershell
git status --short
git diff --stat
```

NON eseguire:

- commit;
- push;
- tag.

---

# Output finale richiesto

## E08-05B REVIEW Correction Pass

### 1. Correzioni applicate
Sintesi.

### 2. E07 54.2% correction
Conferma definitiva.

### 3. E06 metric audit
Valori confermati e valori convertiti a `N/A`.

### 4. Cash reconciliation
Spiegazione `$339` / `$177.40`.

### 5. Workforce finding
Cosa è dimostrato e cosa no.

### 6. Livestock finding
Bilancio economico e livello di causalità.

### 7. Corrected E06/E07/E08 table
Solo metriche verificabili.

### 8. Corrected E09 recommendation
Una sola variabile primaria: livestock ON → OFF.

### 9. E08 final decision
Conferma o eventuale revisione.

### 10. Deliverable
File creati/aggiornati.

### 11. Git status e diff
Output completo.

### 12. Decisione

Usa una sola:

- `REVIEW CORRECTED — READY TO CLOSE E08`
- `REVIEW STILL INCONCLUSIVE — SUPERVISION REQUIRED`

---

# STOP OBBLIGATORIO

Al termine:

**FERMATI.**

NON iniziare E09 DEFINE.

NON modificare la strategia.

NON effettuare rollback.

NON inviare submission Kaggle.

NON eseguire commit, push o tag.

Attendi esplicita approvazione per la chiusura E08 e per la successiva definizione E09.
