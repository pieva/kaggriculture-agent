# PROMPT COMUNE — MODEL_SPEC C2 PERFORMANCE ITERATION

## Mandato

Il **MODEL_SPEC Tournament C2 non è concluso**.

Il retournament ha dimostrato che i tre candidati sono ora tecnicamente eseguibili e confrontabili, ma **l'obiettivo prestazionale che ha motivato C2 non è stato raggiunto**.

Lo stato corretto è:

```text
C2_RETournament_VALID: YES
C2_PERFORMANCE_OBJECTIVE_ACHIEVED: NO
C2_ITERATION_REQUIRED: YES
```

Questo mandato è comune ad **Antigravity, Codex e Copilot**.

Ogni agente deve ora rivedere **autonomamente il proprio MODEL_SPEC C2**, formulare una nuova ipotesi causale, implementarla e verificarla. Non si apre C3 e non si effettua alcun invio Kaggle.

L'obiettivo non è correggere altri bug già risolti, ma **ottenere un miglioramento economico misurabile**.

---

## 1. Evidenza comune da assumere come punto di partenza

Il retournament C2 integrato è valido:

- 9/9 episodi completati;
- completion rate 100%;
- 0 errori;
- 0 fallback;
- audit riproducibile: 12.942 / 12.942 decisioni;
- suite repository: 175 test passati.

### Ranking economico

| Rank | Candidato | W-L-T | Mean | Median | Std (`ddof=1`) | Min | Max |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | Antigravity C2 | 5-1-0 | $16.671 | $16.969,50 | $1.616,36 | $13.783 | $18.347 |
| 2 | Codex C2 | 4-2-0 | $15.156 | $14.619 | $1.300,92 | $14.267 | $17.691 |
| 3 | Copilot C2 | 0-6-0 | $4.154 | $4.225,50 | $201,38 | $3.793 | $4.332 |

Ulteriori evidenze:

| Candidato | Superficie massima | Primo revenue step |
|---|---:|---:|
| Antigravity | 17 | 65 |
| Codex | 24 | 53 |
| Copilot | 4 | 73 |

Confronto descrittivo con il C2 originale:

- Antigravity: +$13.671 / +455,70%;
- Codex: −$1.690,50 / −10,03%;
- Copilot: +$1.154 / +38,47%.

Il delta Codex rispetto al torneo originale **non deve essere interpretato causalmente**, perché sono cambiati anche gli avversari.

---

## 2. Interpretazione obbligatoria

Il retournament dimostra:

1. **runtime realization risolta**;
2. **policy realization verificabile**;
3. **economic closure presente** per tutti, ma molto debole per Copilot;
4. **competitive capacity ancora insufficiente**.

Il risultato non autorizza la chiusura di C2.

Il lavoro svolto su C2 era finalizzato al miglioramento delle prestazioni economiche. Il migliore dei tre candidati produce soltanto **$16.671 medi**, quindi resta sotto i riferimenti storici locali dell'ordine di **$21k–$23k**.

Di conseguenza:

> Un candidato tecnicamente corretto ma economicamente inferiore ai riferimenti precedenti non costituisce successo C2.

Un'altra evidenza deve essere trattata con particolare attenzione:

> Codex raggiunge una superficie massima di 24 tile, contro 17 di Antigravity, ma ottiene un Mean Final Money inferiore.

Pertanto è vietato assumere senza verifica che:

```text
più superficie => più profitto
```

La nuova revisione deve studiare la relazione tra almeno:

```text
productive mass
×
service capacity
×
productive continuity
×
harvest throughput
×
market monetization
×
capital reinvestment
=
economic performance
```

Questa formulazione è un quadro diagnostico, **non una soluzione prescritta**.

---

## 3. Obiettivo prestazionale del prossimo round

### Soglia minima C2

Il prossimo candidato deve puntare a:

```text
Mean Final Money > $23.000
```

sul protocollo comune di tournament.

Questa è la **soglia minima di successo del prossimo round C2**, scelta per richiedere un miglioramento rispetto ai riferimenti storici locali, non soltanto rispetto agli altri candidati C2.

Il riferimento strategico di lungo periodo resta molto superiore, nell'ordine di $50k–$75k, ma non deve essere usato per nascondere il criterio immediato e falsificabile del prossimo round.

### Regola

Un agente non può dichiarare successo perché:

- batte un altro agente;
- supera $3.000;
- completa il ciclo economico;
- raggiunge più tile;
- passa tutti i test;
- realizza correttamente il MODEL_SPEC.

Il criterio economico comune è:

```text
C2_NEXT_ROUND_SUCCESS:
Mean Final Money > $23.000
```

---

## 4. Compito individuale di ciascun agente

Ogni agente deve rivedere **il proprio candidato**, non quello degli altri.

Sono autorizzati:

- revisione del proprio MODEL_SPEC C2;
- revisione della propria configurazione;
- revisione della propria policy;
- nuovi test specifici;
- nuova telemetry necessaria a verificare l'ipotesi;
- preflight sul motore reale.

Non sono autorizzati:

- modifiche alla Foundation C2 salvo identificazione documentata di un blocker realmente comune;
- modifiche ai candidati degli altri agenti;
- tuning dopo aver visto risultati del prossimo torneo;
- modifica di seed/protocollo per favorire il proprio candidato;
- invio Kaggle;
- apertura di C3;
- dichiarazione unilaterale di vittoria.

---

## 5. DEFINE obbligatorio prima del BUILD

Prima di modificare codice, ogni agente deve produrre una diagnosi del proprio risultato corrente.

La diagnosi deve rispondere almeno a queste domande.

### 5.1 Dove si perde il valore?

Quantificare, per quanto consentito dalla telemetry:

- superficie posseduta;
- superficie attiva;
- superficie effettivamente mantenuta;
- tile perse/inattive;
- tempo tra PLANT e primo HARVEST;
- continuità WATER;
- throughput HARVEST;
- replant;
- inventory accumulation;
- SELL;
- liquidità;
- reinvestimento;
- workforce;
- movimento;
- eventuale livestock;
- capacità inutilizzata.

Non è obbligatorio che tutte queste metriche siano già disponibili.

Se una metrica necessaria manca, l'agente deve dichiararlo e può aggiungere la telemetry minima necessaria.

### 5.2 Perché il proprio MODEL_SPEC si ferma al livello osservato?

Distinguere almeno:

```text
CAPACITY_LIMIT
SERVICE_LIMIT
ROUTING_LIMIT
BIOLOGICAL_LIMIT
CAPITAL_LIMIT
MARKET_LIMIT
WORKFORCE_LIMIT
LAND_UTILIZATION_LIMIT
LIVESTOCK_LIMIT
OTHER
```

Non è necessario selezionare tutte le categorie.

Devono essere selezionate soltanto quelle sostenute dall'evidenza.

### 5.3 Qual è il meccanismo dominante?

Ogni agente deve formulare una propria ipotesi causale principale.

Formato obbligatorio:

```text
HYPOTHESIS_ID:
OBSERVED_PROBLEM:
EVIDENCE:
CAUSAL_MECHANISM:
MODEL_CHANGE:
EXPECTED_INTERMEDIATE_EFFECT:
EXPECTED_ECONOMIC_EFFECT:
FALSIFICATION_CONDITION:
```

La nuova versione deve essere costruita attorno a questa ipotesi.

---

## 6. Libertà strategica

Non viene prescritta la soluzione.

Ogni agente può decidere autonomamente se intervenire, per esempio, su:

- productive surface;
- land expansion;
- workforce;
- worker allocation;
- routing;
- crop mix;
- lifecycle;
- replant;
- market;
- capital allocation;
- livestock;
- shed/inventory;
- timing;
- endgame;
- combinazioni di questi elementi.

Questi sono esempi, non una checklist.

### Vincolo fondamentale

Ogni modifica significativa deve avere una catena esplicita:

```text
EVIDENZA
→
IPOTESI CAUSALE
→
MODIFICA DEL MODEL_SPEC
→
MODIFICA DELLA POLICY
→
EFFETTO INTERMEDIO ATTESO
→
EFFETTO ECONOMICO ATTESO
→
CRITERIO DI FALSIFICAZIONE
```

Sono vietate modifiche puramente esplorative prive di previsione verificabile.

---

## 7. Productive mass non equivale a superficie massima

Il prossimo MODEL_SPEC deve distinguere esplicitamente almeno:

```text
OWNED_SURFACE
ACTIVE_SURFACE
SERVICEABLE_SURFACE
PRODUCTIVE_SURFACE
MONETIZED_OUTPUT
```

L'agente può usare nomi tecnici differenti se già canonici nel proprio modello.

Il punto metodologico è obbligatorio:

> Una tile acquistata o piantata non conta come capacità economica se la policy non riesce a mantenerla, raccoglierla e monetizzarne l'output.

Il confronto Antigravity 17 vs Codex 24 deve essere utilizzato come evidenza per evitare l'ottimizzazione cieca della sola superficie.

---

## 8. Previsione preregistrata

Prima del BUILD definitivo, ogni agente deve congelare una previsione.

Minimo obbligatorio:

```text
EXPECTED_DIRECTION_FINAL_MONEY: UP
TARGET_MEAN_FINAL_MONEY: > 23000
```

Aggiungere almeno **due metriche intermedie** direttamente collegate alla propria ipotesi.

Esempio astratto:

```text
METRIC_A:
CURRENT_VALUE:
EXPECTED_VALUE_OR_DIRECTION:
WHY_CAUSAL:

METRIC_B:
CURRENT_VALUE:
EXPECTED_VALUE_OR_DIRECTION:
WHY_CAUSAL:
```

Non usare metriche decorative.

Le metriche devono poter falsificare il meccanismo proposto.

---

## 9. BUILD

Dopo il DEFINE:

1. aggiornare il proprio `MODEL_SPEC_*_C2.md`;
2. aggiornare configurazione/policy necessarie;
3. aggiornare o aggiungere test;
4. mantenere compatibilità con il runner comune;
5. non modificare gli altri candidati;
6. non modificare il protocollo comune.

Ogni cambiamento significativo deve essere tracciato nel report.

---

## 10. VERIFY individuale

La verifica individuale deve dimostrare soltanto che il nuovo modello:

- funziona nel motore reale;
- funziona come P0;
- funziona come P1;
- non produce errori/fallback patologici;
- realizza il nuovo meccanismo;
- produce gli effetti intermedi preregistrati almeno nella misura osservabile durante il preflight.

### Importante

Il preflight **non deve essere usato come torneo privato**.

Non eseguire una ricerca iterativa sui seed comuni del tournament.

Non ottimizzare ripetutamente la policy sui tre seed ufficiali.

Il preflight serve a verificare il meccanismo, non a stimare artificialmente il risultato del torneo.

---

## 11. Gate `TOURNAMENT_READY`

Un candidato può dichiarare:

```text
TOURNAMENT_READY: YES
```

soltanto se:

1. MODEL_SPEC aggiornato;
2. ipotesi causale congelata;
3. previsione economica congelata;
4. P0 real-engine PASS;
5. P1 real-engine PASS;
6. error/fallback sotto controllo;
7. almeno gli effetti intermedi essenziali della nuova policy sono osservabili;
8. test specifici PASS;
9. `git diff --check` PASS;
10. nessun blocker noto rende il candidato non comparabile.

Il gate non significa:

```text
PERFORMANCE_SUCCESS
```

Significa soltanto:

```text
VALID_CANDIDATE_FOR_NEXT_C2_TOURNAMENT
```

---

## 12. Report individuale

Ogni agente deve produrre:

```text
results/model_spec_c2/performance_iteration/<AGENT>_C2_PERFORMANCE_ITERATION.md
```

Il documento deve essere scritto in italiano.

Struttura minima:

```text
1. Stato iniziale
2. Diagnosi quantitativa
3. Collo di bottiglia dominante
4. Ipotesi causale
5. Revisione del MODEL_SPEC
6. Modifiche implementate
7. Previsioni preregistrate
8. Preflight P0/P1
9. Test
10. Limiti residui
11. Freeze degli artifact
12. Stato finale
```

Chiudere con:

```text
C2_PERFORMANCE_ITERATION_COMPLETE: YES|NO
TOURNAMENT_READY: YES|NO
TARGET_MEAN_FINAL_MONEY: >23000
```

---

## 13. Indipendenza tra agenti

Antigravity, Codex e Copilot lavorano sullo stesso dataset comune del retournament, ma devono sviluppare **la propria interpretazione e il proprio modello**.

Possono leggere:

- Foundation C2;
- proprio MODEL_SPEC;
- proprio codice;
- risultati comuni del retournament;
- raw replay/telemetry comuni;
- proprio feedback e remediation precedenti;
- documentazione storica comune del progetto.

Non devono leggere, prima di congelare la propria revisione:

- il nuovo MODEL_SPEC revisionato dagli altri agenti;
- il nuovo report `performance_iteration` degli altri agenti;
- le nuove implementazioni degli altri candidati.

Questo preserva la diversità del MODEL_SPEC Tournament.

---

## 14. Nessun torneo autonomo

Quando un agente conclude:

```text
C2_PERFORMANCE_ITERATION_COMPLETE: YES
TOURNAMENT_READY: YES
```

deve fermarsi.

Non deve:

- eseguire il tournament comune;
- modificare il runner comune;
- confrontare il proprio candidato sui seed ufficiali;
- inviare a Kaggle.

Il nuovo tournament sarà autorizzato soltanto quando tutti i candidati previsti avranno concluso la propria iterazione.

---

## 15. Criterio del prossimo tournament

Il prossimo torneo dovrà mantenere, salvo blocker tecnico documentato:

- stesso formato pairwise;
- stessi tre seed condivisi;
- 720 step;
- presenza dei candidati in entrambi i seat secondo il protocollo già adottato;
- stessa raccolta di raw replay e telemetry;
- stesso calcolo di Mean, Median, Std `ddof=1`, Min, Max;
- audit di riproducibilità.

Il confronto principale dovrà essere:

```text
NEW C2 VERSION
vs
C2 RETOURNAMENT REMEDIATED
vs
HISTORICAL LOCAL REFERENCE
```

Non soltanto:

```text
AGENT A vs AGENT B vs AGENT C
```

---

## 16. Regola di successo e continuazione

Il prossimo round produce due possibili stati.

### Caso A — almeno un candidato supera la soglia

```text
Mean Final Money > $23.000
```

Allora:

```text
C2_PERFORMANCE_IMPROVEMENT_ACHIEVED: YES
```

Il risultato dovrà essere sottoposto a REVIEW prima di decidere il passo successivo.

### Caso B — nessun candidato supera la soglia

Allora:

```text
C2_PERFORMANCE_IMPROVEMENT_ACHIEVED: NO
C2_ITERATION_REQUIRED: YES
```

Non chiudere C2 soltanto perché il torneo è tecnicamente valido.

Le evidenze del nuovo round devono alimentare una nuova revisione dei modelli.

---

## 17. Divieti finali

Durante questa iterazione:

```text
NO C3
NO KAGGLE
NO POST-HOC TUNING SUI SEED DEL TOURNAMENT
NO MODIFICHE AI CANDIDATI ALTRUI
NO PERFORMANCE CLAIM BASATO SOLO SU PREFLIGHT
NO SUCCESS CLAIM BASATO SOLO SU TEST PASS
NO SUCCESS CLAIM BASATO SOLO SUL RANKING RELATIVO
```

L'obiettivo è esplicito:

> **Rivedere i MODEL_SPEC C2 finché il tournament non dimostra un miglioramento economico reale, misurabile e riproducibile.**

