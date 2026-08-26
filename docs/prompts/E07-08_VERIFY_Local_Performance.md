# E07-08 — VERIFY Local Performance

Procedi con la fase **E07-08 — VERIFY Local Performance**.

Le fasi precedenti hanno portato alla decisione:

> GO FOR PERFORMANCE VERIFY

E07-07 ha chiuso empiricamente i tre blocker funzionali:

- Workforce = PASS
- Livestock monetization = PASS
- Feed accounting = PASS

La nuova baseline E07 è quindi sufficientemente funzionante per essere sottoposta al primo benchmark prestazionale controllato.

Questa fase è esclusivamente di **VERIFY**.

NON fare tuning durante il benchmark.  
NON modificare i parametri E07 per migliorarne il risultato.  
NON costruire o inviare submission Kaggle.

---

## 1. Obiettivo

Rispondere alla domanda:

> La nuova baseline competitiva E07 produce localmente un miglioramento reale rispetto alle baseline precedenti e, indipendentemente dal risultato aggregato, quali componenti economiche spiegano la sua performance?

E07 rappresenta un salto architetturale rispetto a E06 e introduce contemporaneamente:

- land expansion;
- workforce scaling;
- multi-crop;
- livestock;
- feed loop;
- market brokerage;
- phase scheduling;
- end-game management.

Questo benchmark NON deve attribuire causalità alle singole componenti.

Deve stabilire se la nuova configurazione, nel suo complesso, costituisce una baseline migliore sulla quale avviare E08+.

---

## 2. Baseline di confronto

Confrontare almeno:

### E07

Agente corrente:

`HybridLivestockClusterROIAgent`

con configurazione E07 corrente, invariata rispetto alla chiusura E07-07.

### E06

Baseline locale shipped precedente.

Usare esattamente la configurazione E06 già validata.

### E05

Includere anche E05 se il benchmark locale precedente è riproducibile con la stessa metodologia.

E05 è importante come ulteriore riferimento perché la sua validazione Kaggle è stata finora migliore di E06.

Non utilizzare il ranking Kaggle corrente come metrica del benchmark locale.

---

## 3. Congelare E07 prima del benchmark

Prima dell'esecuzione registrare la configurazione esatta E07.

Produrre una tabella:

| Parameter | Value |
|---|---:|
| target_quadrants | |
| productive_tiles | |
| wheat_tiles | |
| melon_tiles | |
| carrot_tiles | |
| target_workers | |
| target_cows | |
| target_sheep | |
| expansion timing | |
| cash reserve | |
| livestock cutoffs | |
| crop cutoffs | |
| liquidation timing | |
| market policy | |

Questa configurazione deve restare **immutata per tutti i 30 episodi**.

Non modificare parametri dopo aver osservato risultati intermedi.

---

## 4. Benchmark protocol

Usare la metodologia standard già utilizzata nel progetto per E01–E06.

Eseguire:

> **30 episodi per agente**

con gli stessi opponent e la stessa distribuzione utilizzata nei benchmark precedenti.

Se il protocollo corrente è:

- 10 × `pass`
- 10 × `random`
- 10 × `starter`

mantenerlo.

Usare gli stessi seed tra E05/E06/E07 quando tecnicamente possibile.

Questo è importante per ottenere un confronto paired più informativo.

Registrare esplicitamente:

- opponent;
- seed;
- agente;
- completion;
- disqualification;
- win/draw/loss;
- final money.

---

## 5. Prima verifica: comparabilità

Prima di lanciare tutti gli episodi verificare che:

- E05;
- E06;
- E07

possano essere eseguiti attraverso lo stesso runner e con la stessa interpretazione di:

```text
reward = farm["money"]
```

Se E05 non è direttamente riproducibile senza modificare la baseline storica, NON ricostruirla arbitrariamente.

In quel caso:

- benchmark E07 vs E06;
- utilizzare E05 soltanto come riferimento storico documentato;
- dichiarare la limitazione.

---

## 6. Metriche primarie

Per ogni agente calcolare:

- Completion Rate;
- Disqualification Rate;
- Wins;
- Draws;
- Losses;
- Win Rate;
- Mean Final Money;
- Standard Deviation con `ddof=1`;
- Median Final Money;
- Minimum Final Money;
- Maximum Final Money.

Produrre:

| Agent | Completion | DQ | W/D/L | Win Rate | Mean Final Money | SD | Median | Min | Max |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|

---

## 7. Breakdown per opponent

Produrre per ciascun agente:

| Agent | Opponent | N | Mean Final Money | SD | Median | W/D/L |
|---|---|---:|---:|---:|---:|---|

Non nascondere eventuali regressioni contro uno specifico opponent dietro la media complessiva.

---

## 8. Delta rispetto alle baseline

Calcolare almeno:

```text
E07 - E06
E07 - E05
```

quando E05 è comparabile.

Per Mean Final Money riportare:

```text
absolute delta
percentage delta
```

Esempio:

```text
Δ = Mean(E07) - Mean(E06)

Δ% = Δ / Mean(E06) × 100
```

Fare lo stesso almeno per:

- Median;
- Win Rate.

Non utilizzare le precedenti proiezioni teoriche `$35k–$45k`.

---

## 9. Paired comparison

Se vengono utilizzati gli stessi seed e opponent, produrre anche un confronto paired E07 vs E06.

Per ogni episodio:

```text
delta_i = FinalMoney_E07 - FinalMoney_E06
```

Calcolare:

- mean paired delta;
- median paired delta;
- numero episodi con E07 > E06;
- numero episodi con E07 = E06;
- numero episodi con E07 < E06.

Produrre:

| Comparison | Better | Equal | Worse | Mean Δ | Median Δ |
|---|---:|---:|---:|---:|---:|
| E07 vs E06 | | | | | |

Non è necessario introdurre test statistici sofisticati se non sono già parte del workflow.

Se viene calcolato un test statistico, documentarne metodo e limiti.

---

## 10. Diagnostica economica E07

Per E07 raccogliere anche le metriche diagnostiche aggregate introdotte durante BUILD/VERIFY.

Almeno:

### Land

- `BUY_LAND` count;
- expansion day/step;
- owned tiles;
- productive tiles;
- Q1 worked tiles;
- Q1 harvests;
- utilization ratio.

### Workforce

- HIRE attempted;
- HIRE accepted;
- HIRE cost;
- peak simultaneous workers;
- worker-days;
- productive actions;
- movement;
- idle;
- productive %;
- movement %;
- idle %.

Ricordare la meccanica verificata:

> HIRE crea hands giornalieri temporanei che scadono a mezzanotte.

Non interpretare gli hands come asset permanenti.

---

## 11. Crop economics

Per E07 aggregare per crop:

| Crop | Harvested units | Sold units | Revenue | Unsold final |
|---|---:|---:|---:|---:|
| Wheat | | | | |
| Melon | | | | |
| Carrot | | | | |

Quando possibile riportare anche:

- seeds purchased;
- seed cost;
- crop revenue;
- gross crop contribution.

Non inventare costi non direttamente ricostruibili.

---

## 12. Livestock economics

Questa è una metrica essenziale.

Aggregare almeno:

- cows purchased;
- sheep purchased;
- livestock purchase cost;
- pasture actions/cost, se applicabile;
- feed actions;
- Wheat consumed;
- Milk generated;
- Milk harvested;
- Milk sold;
- Milk revenue;
- Wool generated;
- Wool sold;
- Wool revenue.

Calcolare quando possibile:

```text
observed livestock cash contribution
=
Milk revenue
+ Wool revenue
- directly attributable livestock costs
```

NON chiamarlo ROI completo se non include tutti i costi indiretti, come worker time, movement e opportunity cost delle Wheat tile.

---

## 13. Correzione del Wheat ledger

Prima di utilizzare il Wheat accounting come metrica economica, verificare una cosa rimasta concettualmente ambigua in E07-07.

Il report precedente ha scritto:

```text
128 Wheat harvested
+ 54 Wheat seeds purchased
= 182 Wheat sources
```

Verificare direttamente nell'environment se:

```text
WHEAT seed
```

e:

```text
WHEAT harvested product
```

sono realmente lo stesso inventory item consumabile tramite `FEED`.

Se sono stock distinti, NON sommare i semi al Wheat prodotto.

In quel caso utilizzare la conservation equation corretta per il solo prodotto Wheat:

```text
initial Wheat product
+ harvested Wheat product
+ purchased Wheat product
=
fed Wheat
+ sold Wheat
+ final Wheat product
+ verified losses
```

Documentare la semantica verificata.

Questa è una correzione della metrica, NON tuning dell'agente.

---

## 14. Capital deployment

Per E07 aggregare:

- starting cash;
- minimum cash;
- final cash;
- seed spending;
- HIRE spending;
- livestock spending;
- land spending;
- structures spending;
- total directly observed investment.

Identificare inoltre il timing medio degli investimenti principali.

L'obiettivo è capire:

> quanto capitale E07 immobilizza e quanto riesce a riconvertirne in cash entro il turno 720.

---

## 15. Terminal asset audit

Per ogni episodio E07 registrare al termine:

- final inventory;
- cows;
- sheep;
- mature crops;
- immature crops;
- land;
- structures.

Questi asset non devono essere aggiunti al Final Money.

Produrre però una diagnostica del capitale terminale non monetizzato.

Non assegnare un valore monetario teorico agli asset non liquidabili.

Utilizzare invece indicatori fisici:

```text
unsold inventory units
remaining livestock
mature crops remaining
immature crops remaining
unused productive capacity
```

---

## 16. Phase economics

Per E07 aggregare per:

```text
OPENING
SCALE
PRODUCE
LIQUIDATE
```

almeno:

- cash all'ingresso;
- cash all'uscita;
- investimenti principali;
- revenue osservato.

Verificare se `LIQUIDATE` produce effettivamente conversione inventory → cash.

---

## 17. Variabilità

E07 è più complesso di E06.

Quindi non guardare soltanto la media.

Analizzare:

- SD;
- min/max;
- episodi peggiori;
- eventuali outlier;
- eventuali episodi in cui la strategia non riesce a scalare.

Identificare i **3 episodi E07 peggiori** per Final Money e produrre una breve diagnosi per ciascuno.

Fare lo stesso per i **3 migliori**, se utile a capire quali condizioni favoriscono E07.

---

## 18. Nessun tuning durante VERIFY

Regola fondamentale.

Durante i 30 episodi NON modificare:

- target workers;
- crop allocation;
- herd size;
- expansion timing;
- cutoffs;
- cash reserve;
- task priorities;
- market policy.

Se emerge un problema:

1. registrarlo;
2. completare il benchmark se tecnicamente possibile;
3. proporlo come candidato E08+.

Non correggere E07 a metà benchmark salvo bug che renda i risultati tecnicamente invalidi.

Se emerge un bug invalidante:

> STOP BENCHMARK

Documentare il problema e usare:

`RETURN TO BUILD`.

---

## 19. Interpretazione del risultato

Al termine classificare E07 in una delle seguenti categorie.

### A — NEW BASELINE CONFIRMED

E07 migliora in modo sostanziale il riferimento locale e non presenta regressioni strutturali critiche.

### B — PROMISING BUT UNTUNED

E07 non supera ancora chiaramente il riferimento, ma mostra componenti economicamente produttive e gap identificabili che rendono sensato ottimizzarla.

### C — ARCHITECTURALLY VALID, ECONOMICALLY WEAK

Le capability funzionano, ma il costo complessivo della configurazione produce una regressione significativa.

### D — BASELINE REJECTED

La configurazione E07 è strutturalmente o economicamente inadatta come base per E08+.

Non forzare `NEW BASELINE CONFIRMED`.

---

## 20. Candidate variables E08+

Dopo aver completato il benchmark, identificare le variabili che spiegano maggiormente il gap.

Possibili candidati:

- productive land size;
- BUY_LAND timing;
- workforce target;
- daily HIRE policy;
- crop allocation;
- Wheat allocation;
- livestock size;
- livestock purchase timing;
- feed allocation;
- movement/pathing;
- weeds/DIG;
- market timing;
- crop cutoff;
- end-game liquidation.

Classificarli per:

```text
HIGH
MEDIUM
LOW
```

come priorità sperimentale.

NON assegnare ancora automaticamente E08, E09, ecc.

---

## 21. Deliverable

Creare:

`docs/versions/E07_verify_local_performance.md`

Il documento deve contenere almeno:

1. Benchmark Objective
2. Frozen E07 Configuration
3. Benchmark Protocol
4. Comparability Check
5. Overall Results
6. Opponent Breakdown
7. E07 vs E06
8. E07 vs E05, se comparabile
9. Paired Analysis
10. Land Diagnostics
11. Workforce Diagnostics
12. Crop Economics
13. Livestock Economics
14. Wheat Accounting
15. Capital Deployment
16. Phase Economics
17. Terminal Asset Audit
18. Variability / Outliers
19. Performance Diagnosis
20. Candidate Variables E08+
21. VERIFY Decision

Aggiornare:

- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Non dichiarare ancora E07 shipped.

---

## 22. Scratch e submission

Gli script diagnostici presenti in:

`scratch/`

possono essere utilizzati durante VERIFY.

NON considerarli automaticamente artefatti da versionare o spedire.

Verificare inoltre lo stato di:

`submission/submission.py`

ma:

- non costruire una nuova submission;
- non inviare nulla a Kaggle;
- non modificare la submission per adattarla ai risultati del benchmark.

La pulizia degli artefatti verrà decisa in REVIEW/SHIP.

---

## 23. Test prima del benchmark

Prima del benchmark eseguire:

`.venv\Scripts\pytest tests/`

La suite deve restare completamente verde.

Se fallisce:

> STOP

e diagnosticare prima di generare risultati prestazionali.

---

## 24. Output finale richiesto

Mostrare almeno:

1. configurazione E07 congelata;
2. risultato pytest;
3. protocollo effettivamente eseguito;
4. tabella E05/E06/E07;
5. breakdown per opponent;
6. delta E07 vs E06;
7. delta E07 vs E05, se comparabile;
8. paired comparison;
9. land utilization E07;
10. workforce utilization E07;
11. crop revenue breakdown;
12. livestock cost/revenue breakdown;
13. semantica corretta del Wheat ledger;
14. capital deployment;
15. terminal asset diagnostics;
16. tre episodi peggiori E07 e relativa diagnosi;
17. principali cause della performance;
18. candidate variables E08+;
19. `git status --short`;
20. `git diff --stat`;
21. decisione VERIFY.

Decisione finale esclusivamente tra:

- `NEW BASELINE CONFIRMED`
- `PROMISING BUT UNTUNED`
- `ARCHITECTURALLY VALID, ECONOMICALLY WEAK`
- `BASELINE REJECTED`

FERMARSI QUI.

NON:

- fare tuning;
- modificare E07 sulla base dei risultati;
- costruire submission;
- inviare submission Kaggle;
- fare commit;
- fare push;
- creare tag;
- dichiarare E07 shipped.

Attendere la revisione prima di REVIEW/SHIP o della definizione del prossimo esperimento.
