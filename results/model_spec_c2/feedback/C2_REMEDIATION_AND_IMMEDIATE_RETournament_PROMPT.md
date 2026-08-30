# C2 — Remediation indipendente e verifica immediata nel prossimo tournament

## Mandato

Hai completato il feedback indipendente sul round C2. Ora sei autorizzato a correggere **il tuo candidato C2** sulla base delle cause, degli errori e dei limiti che hai identificato nel tuo feedback e nelle evidenze C2.

L'obiettivo non è aprire C3 né riscrivere liberamente la strategia. L'obiettivo è:

1. correggere gli errori propri del candidato C2;
2. rendere effettivamente realizzati i meccanismi già dichiarati o necessari alla policy C2;
3. eseguire un preflight reale minimo;
4. congelare il candidato corretto;
5. renderlo immediatamente disponibile per il prossimo tournament C2 di verifica.

Il prossimo tournament è il test sperimentale delle correzioni. Evita una nuova campagna preparatoria o una proliferazione di gate/test non necessaria.

---

## Vincoli di indipendenza

- Lavora esclusivamente sul tuo candidato e sui suoi artefatti.
- Puoi usare: Foundation C2, MODEL_SPEC del tuo candidato, BUILD/VERIFY, tournament C2, failure review, feedback indipendente del tuo candidato, evidenze storiche già presenti nel repository e lesson learned comuni.
- **Non leggere i feedback indipendenti degli altri agenti.**
- Non copiare implementazioni o remediation degli altri candidati.
- Non modificare gli altri candidati.
- Non modificare Foundation C2 salvo autorizzazione esplicita successiva.
- Non avviare Kaggle.

---

## Principio di remediation

Correggi ciò che il tuo feedback ha identificato come responsabilità del tuo candidato, distinguendo:

```text
BUG / RUNTIME DEFECT
POLICY-REALIZATION DEFECT
MODEL_SPEC-TO-BUILD MISMATCH
STRATEGIC LIMITATION DEL CANDIDATO C2
```

Sono consentite modifiche necessarie a rendere il candidato C2 coerente, operativo e competitivo rispetto alla propria diagnosi.

Non introdurre feature estranee senza una catena causale documentata. Non trasformare la remediation in un redesign senza vincoli.

Per ogni modifica significativa registra:

```text
PROBLEMA C2
EVIDENZA
MODIFICA
MECCANISMO ATTESO
PREVISIONE VERIFICABILE NEL PROSSIMO TOURNAMENT
```

---

## Preflight minimo obbligatorio

Prima di dichiarare il candidato pronto, esegui un controllo real-engine breve e ad alto information gain.

### A. Runtime correctness

Verifica almeno P0 e P1 nel vero ambiente Kaggriculture:

- parsing corretto dell'observation reale;
- binding alla propria farm/player;
- nessuna eccezione interna;
- nessun fallback/fail-closed patologico;
- output valido per l'engine.

### B. Policy realization

Dimostra tramite **state transition**, non soltanto action dispatch, che il candidato riesce a uscire dallo stato iniziale e a realizzare i meccanismi essenziali della propria policy.

Non imporre artificialmente la stessa sequenza di opcode a tutti i candidati. Verifica gli effetti richiesti dal MODEL_SPEC e, dove la policy dipende da produzione agricola/economia, la raggiungibilità del ciclo produttivo ed economico.

### C. Evidenza

Registra almeno:

- error/fallback count;
- seat verificati;
- transizioni di stato osservate;
- active surface / productive state raggiunto;
- eventuale chiusura del primo ciclo economico se osservabile nel run necessario;
- qualsiasi failure residuo.

Il preflight deve essere sufficiente a evitare un altro candidato palesemente non operativo, ma **non deve diventare un nuovo tournament o una fase di tuning estesa**.

---

## Criterio `TOURNAMENT_READY`

Dichiara `TOURNAMENT_READY: YES` soltanto se:

1. il candidato gira correttamente nel real engine in P0 e P1;
2. error/fallback patologici sono zero;
3. sono osservate transizioni di stato coerenti con la policy;
4. i blocker identificati nel feedback del candidato sono stati corretti o esplicitamente falsificati dalle nuove evidenze;
5. non rimangono failure note che rendano il candidato non comparabile nel tournament.

Se una di queste condizioni fallisce:

```text
TOURNAMENT_READY: NO
```

spiega il blocker e fermati. Non mascherare il problema con fallback e non dichiarare readiness sulla sola base dei test verdi.

---

## Verifica tecnica

Esegui almeno:

```text
git diff --check
pytest
```

oltre al preflight real-engine descritto sopra.

Documenta risultati e comandi effettivamente eseguiti.

---

## Freeze e output

Aggiorna/crea gli artefatti necessari per rendere tracciabile la remediation del tuo candidato C2, mantenendo tutta la documentazione in italiano salvo identificatori, metriche, comandi e termini tecnici che richiedono l'inglese.

Produci un report di remediation del candidato sotto:

```text
results/model_spec_c2/remediation/<AGENT>_C2_REMEDIATION.md
```

Il report deve contenere:

1. failure/limiti C2 presi in carico;
2. modifiche effettuate;
3. mapping evidenza → modifica;
4. risultati dei test;
5. risultati del real-engine preflight P0/P1;
6. eventuali failure residui;
7. previsioni verificabili per il prossimo tournament;
8. elenco esatto dei file modificati;
9. stato finale `TOURNAMENT_READY`.

Non eseguire autonomamente il tournament comune: il tournament partirà quando tutti e tre i candidati avranno completato questa fase.

Termina con uno dei due stati:

```text
C2_REMEDIATION_COMPLETE
TOURNAMENT_READY: YES
```

oppure

```text
C2_REMEDIATION_INCOMPLETE
TOURNAMENT_READY: NO
```
