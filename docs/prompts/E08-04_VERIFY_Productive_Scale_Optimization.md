# E08-04 — VERIFY Productive Scale Optimization

## Contesto

Stiamo lavorando al progetto **Kaggriculture**, esperimento **E08 — Productive Scale Optimization**.

Stato delle fasi:

- **E08-01 DEFINE**: completato e approvato;
- **E08-02 PLAN**: completato e approvato;
- **E08-03 BUILD**: completato e approvato;
- fase corrente: **E08-04 VERIFY**.

Documenti di riferimento prioritari:

- `docs/versions/E08_define_productive_scale.md`
- `docs/plans/E08_Productive_Scale_Optimization.md`
- `docs/versions/E08_plan_productive_scale.md`
- `docs/versions/E08_build_productive_scale.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Documentazione E07 da usare come baseline e riferimento metodologico:

- `docs/versions/E07_verify_functional_utilization.md`
- `docs/versions/E07_verify_local_performance.md`
- `docs/versions/E07_verify_competitive_evidence.md`
- `docs/plans/E07_Competitive_Baseline_Reconstruction.md`
- `results/e07_competitive_baseline.json`
- `scripts/benchmark_e07_performance.py`

Baseline economiche:

- **E07 Mean Final Money = $15,364.57** → baseline primaria E08;
- **E06 Mean Final Money = $25,180.30** → riferimento secondario, NON criterio minimo di successo.

---

# Obiettivo della VERIFY

Verificare se l'aumento della scala produttiva da **24 a 40 tile**:

1. viene realmente realizzato nel comportamento dell'agente;
2. è sostenibile dal punto di vista operativo;
3. non introduce nuovi colli di bottiglia gravi;
4. migliora la prestazione economica rispetto a E07;
5. recupera, eventualmente, parte del gap rispetto a E06.

La VERIFY deve separare nettamente:

- **funzionalità e utilizzo reale della capacità produttiva**;
- **prestazione economica**;
- **interpretazione diagnostica**.

NON modificare il codice della strategia durante la VERIFY, salvo correzioni strettamente necessarie per consentire l'esecuzione dei test/benchmark e solo se si tratta di bug tecnici evidenti. Qualunque modifica alla logica strategica invalida il confronto e richiede di fermarsi.

---

# Regola fondamentale

La VERIFY deve misurare la catena:

> **40 configured → planted → maintained → harvested → valore economico**

Non considerare soddisfatto il requisito E08 solo perché esistono 40 coordinate configurate.

Una tile deve essere considerata produttiva solo se risulta effettivamente utilizzata nel ciclo agricolo.

---

# Fase V1 — Functional & Utilization Verification

Esegui una verifica funzionale dedicata prima del benchmark economico.

## V1.1 — Test automatici

Esegui:

```powershell
.venv\Scripts\python.exe -m pytest tests/
```

Registra:

- numero totale test;
- passed;
- failed;
- durata.

Criterio:

> 100% pass.

Se falliscono test esistenti o E08, fermati e classifica il problema prima di proseguire.

---

## V1.2 — Verifica scala produttiva

Esegui uno o più episodi diagnostici controllati sufficienti a osservare l'intero ciclo di espansione Q1.

Misura almeno:

- `configured_crop_tiles_count`;
- `peak_productive_tiles`;
- `mean_daily_productive_tiles`;
- numero massimo di tile:
  - configurate;
  - seminate;
  - attive;
  - raccolte, se disponibile;
- giorno in cui viene raggiunto il picco produttivo;
- eventuale differenza tra target 40 e utilizzo reale.

Criterio architetturale primario:

> E08 deve dimostrare di poter utilizzare realmente fino a **40 tile produttive**, non soltanto configurarle.

Se il picco resta materialmente sotto 40, identifica il collo di bottiglia.

Non modificare la strategia durante questa fase.

---

## V1.3 — Progressione Day 12–15

Verifica specificamente la fase di espansione.

Registra per Day 12, 13, 14 e 15:

- cash disponibile;
- Q1 acquistato/non acquistato;
- numero tile Q1 configurate;
- numero tile Q1 effettivamente seminate;
- acquisti sementi eseguiti;
- eventuali acquisti bloccati dal cash floor;
- backlog di planting;
- backlog di watering.

Verifica che:

- `BUY_LAND` Q1 avvenga secondo la policy prevista;
- lo staggered purchasing sia effettivamente distribuito;
- non esistano acquisti duplicati;
- il feed loop Wheat non venga compromesso;
- il cash floor non venga violato dalla logica degli acquisti sementi.

---

## V1.4 — Cash floor

Misura:

- `minimum_cash`;
- giorno del minimo;
- eventuali eventi che portano il saldo vicino a $300;
- eventuali acquisti bloccati dal floor.

Distinguere:

- violazione del floor da parte della logica E08;
- calo del cash dovuto ad altre azioni già presenti nella strategia E07.

Non dichiarare automaticamente fallita E08 se il cash scende sotto $300 per cause esterne allo staggered purchasing: documentare l'origine.

---

## V1.5 — Workforce utilization

Per l'episodio o gli episodi diagnostici, misura:

- productive/action turns;
- movement turns;
- idle turns;
- totale turni;
- percentuali corrispondenti.

Calcola almeno:

```text
productive_share = productive_turns / total_turns
movement_share   = movement_turns / total_turns
idle_share       = idle_turns / total_turns
```

Il valore `<38% movement share` è esclusivamente un **target diagnostico E08**.

NON confrontarlo con 54.2%, perché 54.2% era una stima del carico produttivo, non una baseline E07 del movimento.

Se possibile, confronta con una movement share E07 solo se ricavabile da dati reali già registrati o replicabili con lo stesso strumento.

---

## V1.6 — Spatial partitioning

Verifica che il partizionamento implementato venga effettivamente rispettato.

Misura, se la telemetria lo consente:

- task eseguiti da worker 0–1 in Q0;
- task eseguiti da worker 2–3 in Q1;
- cross-boundary Water Assist;
- numero/frequenza degli attraversamenti;
- eventuali worker sistematicamente sovraccarichi;
- eventuali worker sistematicamente idle.

L'obiettivo non è dimostrare che ogni worker resti rigidamente nel proprio quadrante, ma che il partizionamento riduca movimenti inutili senza creare backlog.

---

## V1.7 — Backlog

Misura per episodio diagnostico:

- `needs_water`;
- `harvest_ready`;
- `plant_pending`.

Riporta almeno:

- picco;
- media, se disponibile;
- giorni in cui il backlog raggiunge i massimi;
- backlog residuo verso la fine dell'episodio.

Interpretazione:

- WATER backlog elevato → scala superiore alla capacità operativa o dispatcher inefficiente;
- HARVEST backlog elevato → superficie gestita ma valore non monetizzato tempestivamente;
- PLANT backlog elevato → espansione nominale ma non realmente produttiva.

---

# Deliverable V1

Crea:

`docs/versions/E08_verify_functional_utilization.md`

Il documento deve includere:

1. test automatici;
2. verifica delle 40 tile;
3. progressione Day 12–15;
4. cash floor;
5. worker utilization;
6. spatial partitioning;
7. backlog;
8. anomalie;
9. decisione:

- `FUNCTIONAL VERIFY PASS`
- `FUNCTIONAL VERIFY PASS WITH WARNINGS`
- `FUNCTIONAL VERIFY FAIL`

Se emerge un **FAIL strutturale** che rende il benchmark economico non significativo, fermati prima di V2 e chiedi supervisione.

---

# Fase V2 — Performance Verification

Solo se V1 non produce un fail strutturale, esegui il benchmark economico ufficiale.

## V2.1 — Protocollo

Usa un benchmark **paired da 30 episodi** con lo stesso protocollo E07:

- 10 × `pass`;
- 10 × `random`;
- 10 × `starter`;
- stessi seed usati per E07/E06, se disponibili;
- stessa configurazione ambiente;
- stesso numero di step;
- stessa modalità di raccolta risultati.

NON cambiare seed/opponent per favorire E08.

Se esiste già uno script E07 riutilizzabile, preferisci estenderlo o parametrizzarlo senza alterare il protocollo.

---

## V2.2 — Metriche economiche

Calcola per E08:

- Mean Final Money;
- Median Final Money;
- Standard Deviation con `ddof=1`;
- Min;
- Max;
- Completion Rate;
- Disqualification Rate;
- Win / Draw / Loss, se disponibile;
- breakdown per opponent.

Confronta con E07:

> E07 Mean Final Money = **$15,364.57**

Calcola:

```text
absolute_delta = E08_mean - E07_mean
percentage_delta = absolute_delta / E07_mean * 100
```

Confronta anche con E06:

> E06 Mean Final Money = **$25,180.30**

Calcola il gap residuo:

```text
gap_to_E06 = E06_mean - E08_mean
```

e, se utile:

```text
gap_recovered_vs_E07 =
(E08_mean - E07_mean) / (E06_mean - E07_mean) * 100
```

Non trasformare E06 nel criterio minimo di successo.

---

## V2.3 — Breakdown per opponent

Per ciascuno di:

- `pass`;
- `random`;
- `starter`;

riporta almeno:

- mean;
- median;
- standard deviation;
- differenza E08 − E07;
- percentuale di miglioramento/peggioramento.

Segnala se il miglioramento aggregato dipende da un solo tipo di avversario.

---

## V2.4 — Outlier e stabilità

Identifica:

- episodi anomali;
- crolli di liquidità;
- casi con mancato raggiungimento delle 40 tile;
- episodi con backlog eccezionale;
- episodi con movement share eccezionale;
- episodi con Final Money molto distante dalla media.

Non rimuovere outlier dal benchmark ufficiale.

Puoi analizzarli separatamente, ma i 30 episodi devono restare tutti nel risultato aggregato salvo errori tecnici documentati.

---

# Fase V3 — Correlazione tra utilizzo e risultato economico

Se la telemetria lo consente senza modificare la strategia, associa per episodio almeno:

- Final Money;
- peak productive tiles;
- mean productive tiles;
- movement share;
- idle share;
- peak WATER backlog;
- peak HARVEST backlog;
- peak PLANT backlog;
- minimum cash.

L'obiettivo non è produrre un modello statistico complesso, ma capire se il risultato economico sembra coerente con l'utilizzo operativo.

Esempi di interpretazione:

- più tile ma stessa/peggiore resa → possibile saturazione operativa;
- 40 tile + backlog basso + miglioramento economico → conferma forte;
- 40 tile + movement alto + backlog alto + miglioramento modesto → scala corretta ma dispatcher da ottimizzare;
- tile sotto target + cash floor spesso bloccante → problema di espansione/liquidità;
- tile sotto target + idle alto → problema di scheduling/layout.

---

# Criteri di valutazione E08

La decisione VERIFY deve considerare congiuntamente funzionalità ed economia.

## Successo forte

Indicativamente:

- 100% completion;
- 0 squalifiche;
- 40 tile realmente raggiunte o molto prossime in modo stabile;
- backlog sotto controllo;
- movement share compatibile con la scala;
- E08 Mean Final Money > E07 in modo materialmente significativo;
- recupero apprezzabile del gap verso E06.

## Successo parziale / risultato diagnostico utile

Esempi:

- E08 > E07 ma con backlog/movement elevato;
- E08 usa 40 tile ma migliora poco economicamente;
- E08 non raggiunge sempre 40 tile ma individua chiaramente un nuovo collo di bottiglia;
- forte miglioramento su alcuni opponent ma regressione su altri.

Questi casi NON vanno automaticamente classificati come fallimento: devono alimentare REVIEW.

## Fallimento

Esempi:

- regressione economica netta rispetto a E07;
- incapacità sistematica di utilizzare la nuova superficie;
- backlog strutturale grave;
- instabilità / disqualifications;
- espansione Q1 non sostenibile;
- starvation del feed loop;
- bug operativi che rendono il benchmark non confrontabile.

---

# Deliverable V2

Crea:

`docs/versions/E08_verify_local_performance.md`

Includi:

1. protocollo;
2. risultati aggregati;
3. confronto E08 vs E07;
4. confronto secondario E08 vs E06;
5. breakdown per opponent;
6. outlier;
7. stabilità;
8. relazione con metriche operative;
9. conclusione economica.

Se viene generato un file JSON risultati, salvarlo in `results/` con naming coerente E08.

---

# Deliverable V3 — Competitive Evidence

Dopo il benchmark locale, prepara un breve documento di sintesi:

`docs/versions/E08_verify_competitive_evidence.md`

Deve rispondere esplicitamente a queste domande:

1. L'aumento da 24 a 40 tile ha corretto il principale limite osservato in E07?
2. Le 40 tile vengono realmente sfruttate?
3. La workforce di 4 worker è ancora sufficiente?
4. Lo spatial partitioning riduce il costo operativo o introduce nuovi colli di bottiglia?
5. Lo staggered purchasing limita l'espansione?
6. Quanto gap E07→E06 è stato recuperato?
7. Qual è il principale collo di bottiglia rimasto dopo E08?
8. Le evidenze supportano:
   - mantenimento E08;
   - ottimizzazione incrementale E09;
   - rollback/variante?

NON modificare ancora il codice per E09.

---

# Documentazione di stato

Al termine della VERIFY aggiorna:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Registra:

- esito V1;
- esito benchmark V2;
- principali metriche;
- confronto E07/E08/E06;
- nuovo collo di bottiglia;
- decisione proposta per REVIEW.

---

# Git

Al termine esegui:

```powershell
git status --short
git diff --stat
```

NON eseguire commit.

NON eseguire push.

NON creare tag.

---

# Kaggle

Questa fase riguarda la VERIFY locale.

NON inviare ancora una nuova submission Kaggle.

NON aprire browser.

NON tentare autenticazioni Kaggle.

La decisione sull'eventuale submission E08 verrà presa nella fase REVIEW/SHIP.

---

# Output finale richiesto

Restituisci un report con questa struttura:

## E08-04 VERIFY Productive Scale Optimization

### 1. Functional Verify
- test;
- productive tiles;
- Day 12–15;
- cash floor;
- workforce;
- partitioning;
- backlog;
- esito V1.

### 2. Performance Benchmark
- protocollo;
- Mean / Median / SD;
- completion / DQ;
- breakdown opponent;
- esito V2.

### 3. Confronto E08 vs E07
- delta assoluto;
- delta percentuale;
- interpretazione.

### 4. Confronto secondario E08 vs E06
- gap residuo;
- gap recuperato;
- interpretazione.

### 5. Diagnostica del collo di bottiglia
- utilizzo terreno;
- movement;
- idle;
- backlog;
- cash;
- eventuale nuovo limite dominante.

### 6. Outlier / anomalie
Elenco verificabile degli episodi o comportamenti anomali.

### 7. Deliverable creati
Elenco file.

### 8. Git status e diff
Riporta:
- `git status --short`
- `git diff --stat`

### 9. Decisione VERIFY

Usa una sola delle seguenti:

- `VERIFY PASS — GO FOR REVIEW`
- `VERIFY PASS WITH WARNINGS — GO FOR REVIEW`
- `VERIFY FAIL — SUPERVISION REQUIRED`

---

# STOP OBBLIGATORIO

Al termine della VERIFY:

**FERMATI.**

NON iniziare REVIEW.

NON modificare la strategia.

NON avviare E09.

NON inviare submission Kaggle.

NON eseguire commit, push o tag.

Attendi esplicita approvazione prima della fase successiva.
