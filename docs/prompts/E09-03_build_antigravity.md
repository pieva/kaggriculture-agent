# E09-01 — BUILD — Livestock Subsystem Ablation

## Stato approvato

Il DEFINE revisionato di **E09-01 — Livestock Subsystem Ablation** è approvato.

La catena sperimentale vincolante è:

```text
E07: 24 tile + Livestock ON
        |
        | Productive Scale
        v
E08: 40 tile + Livestock ON
        |
        | Livestock Ablation
        v
E09-01: 40 tile + Livestock OFF
```

### Baseline primaria
**E08 — 40 tile — Livestock ON**

Mean Final Money di riferimento: **$11,880.30**.

### Treatment
**E09-01 — 40 tile — Livestock OFF**

### Riferimento secondario
**E07 — 24 tile — Livestock ON**, Mean Final Money **$13,320.37**.

E07 NON è la baseline causale dell'ablation.

---

# Obiettivo di questa fase

Questa fase è **BUILD**.

Implementa una variante E09-01 che parta dalla configurazione E08 e rimuova esclusivamente il comportamento strategico attivo relativo al livestock.

La domanda sperimentale resta:

> **Se togliamo il livestock da E08 e non cambiamo nient'altro, il footprint da 40 tile torna a produrre valore?**

BUILD deve produrre una variante tecnicamente corretta e testabile.

**Non eseguire ancora il benchmark comparativo completo E08/E09-01.**
**Non costruire ancora la submission Kaggle.**
**Non accedere a Kaggle.**

---

# 1. Verifica iniziale obbligatoria

Prima di modificare qualsiasi file:

1. esegui `git status`;
2. verifica branch e HEAD;
3. verifica il tag `v0.8-e08-productive-scale`;
4. rileggi:
   - `docs/versions/E09_define_livestock_ablation.md`;
   - `docs/PROJECT_STATE.md`;
   - i file della strategia E08;
   - i test pertinenti;
   - il runner/benchmark E08;
5. conferma quale classe/configurazione rappresenta esattamente E08 a 40 tile.

Se il working tree contiene esclusivamente le modifiche documentali del DEFINE approvato, preservale.

Se trovi modifiche al codice produttivo non previste, fermati e segnala il problema.

---

# 2. Principio di implementazione

E09-01 è una **controlled ablation**.

Deve cambiare una sola dimensione:

```text
Livestock ON -> Livestock OFF
```

Tutto il resto deve restare semanticamente equivalente a E08.

NON utilizzare BUILD come occasione per:

- ottimizzare crop selection;
- modificare il footprint;
- modificare lo scaling;
- cambiare priorità Water-First;
- modificare workforce;
- modificare land expansion;
- cambiare worker partitioning;
- introdurre nuove euristiche;
- modificare soglie economiche non direttamente livestock;
- correggere backlog;
- ottimizzare movimento;
- rifattorizzare parti non necessarie;
- introdurre comportamenti osservati nei competitor.

Eventuali opportunità emerse durante BUILD vanno annotate per esperimenti successivi.

---

# 3. Strategia E09-01

Crea una variante chiaramente identificabile della strategia E08.

Segui le convenzioni di naming già presenti nel repository.

Il nome deve rendere evidente che si tratta della variante:

**40 tile + Livestock OFF**

Preferisci una nuova classe/modulo derivato o equivalente che consenta di mantenere E08 intatto e confrontabile.

NON sovrascrivere il comportamento E08.

E08 deve poter essere rieseguito senza checkout storico o modifiche manuali.

---

# 4. Ablation obbligatoria

Disabilita esclusivamente il comportamento strategico attivo relativo al livestock.

L'implementazione deve garantire:

## 4.1 Acquisto animali

E09-01 non deve emettere:

- `BUY_ANIMAL COW`;
- `BUY_ANIMAL SHEEP`;
- equivalenti azioni di acquisto livestock.

Target livestock:

```text
target_cows = 0
target_sheep = 0
```

o soluzione semanticamente equivalente.

---

## 4.2 Pasture

E09-01 non deve costruire nuovi pasture per il livestock.

Nessuna azione deliberata:

```text
BUILD_PASTURE
```

deve essere generata dalla strategia E09-01.

Non alterare artificialmente eventuali stati preesistenti dell'environment.

---

## 4.3 Placement

E09-01 non deve:

- prelevare animali per placement;
- trasportare animali;
- eseguire `PLACE COW`;
- eseguire `PLACE SHEEP`;
- produrre azioni equivalenti.

---

## 4.4 Feed

E09-01 non deve:

- cercare animali unfed;
- prelevare Wheat per alimentazione;
- muoversi verso pasture per alimentazione;
- eseguire `FEED`.

Il contatore/telemetria `wheat_fed` deve restare a zero negli episodi E09-01, salvo eventi esterni non controllati dall'agente.

---

## 4.5 Feed safety buffer

Rimuovi la riserva Wheat dedicata esclusivamente al livestock.

Per E09-01:

```text
feed_safety_buffer = 0
```

o equivalente.

Il Wheat non deve essere trattenuto per alimentare animali che la strategia non acquista.

NON modificare altre regole di vendita del Wheat.

---

## 4.6 Livestock harvest

E09-01 non deve dedicare worker a:

- harvesting di pasture;
- raccolta di Milk;
- raccolta di Wool;
- trasporto di prodotti livestock;
- deposito di prodotti livestock.

Attenzione: non disabilitare genericamente `HARVEST` se la stessa action è usata anche dalle colture.

L'ablation deve essere contestuale al livestock.

---

## 4.7 Vendite livestock

E09-01 non deve produrre Milk/Wool attraverso la propria strategia e non deve contenere decisioni economiche attive necessarie esclusivamente alla produzione livestock.

Disabilita la logica specifica di vendita:

- `MILK`;
- `WOOL`;

solo nella misura necessaria all'ablation.

Non alterare la liquidation/market policy degli altri prodotti.

---

# 5. Footprint E08: VINCOLO CRITICO

E09-01 deve mantenere il footprint produttivo da **40 tile** di E08.

NON tornare alla configurazione E07 da 24 tile.

Verifica nel codice quali tile costituiscono esattamente la configurazione E08 e preserva:

- footprint;
- espansione;
- ownership assumptions;
- worker spatial partitioning.

Le tile che in E08 erano coinvolte nel livestock non devono essere eliminate dal footprint solo perché il livestock è OFF.

Devono rimanere disponibili alla strategia secondo il comportamento naturale della configurazione E08 privata del ramo livestock.

Se ciò richiede una scelta non definita dal DEFINE e comporterebbe una nuova strategia colturale, NON inventarla: fermati e documenta l'ambiguità.

---

# 6. Variabili congelate

Verifica esplicitamente che E09-01 mantenga rispetto a E08:

- **40 tile**;
- **4 worker**;
- 1 Farmer + 3 Hands;
- timing delle assunzioni;
- espansione Q1 al Giorno 12;
- costo/condizione `BUY_LAND` invariati;
- spatial partitioning invariato;
- Water-First priority:
  `WATER > HARVEST > PLANT`;
- crop policy invariata;
- seed/planting policy invariata;
- market policy non-livestock invariata;
- liquidation policy invariata;
- movement logic non-livestock invariata;
- fallback invariati;
- condizioni economiche non-livestock invariate.

Nel report BUILD crea una tabella:

| Dimensione | E08 | E09-01 | Stato |
|---|---|---|---|
| Footprint | 40 | 40 | FROZEN |
| Livestock | ON | OFF | ABLATED |
| Workforce | ... | ... | FROZEN |
| ... | ... | ... | ... |

---

# 7. Test strutturali obbligatori

Aggiungi test specifici E09-01.

I test devono dimostrare almeno:

1. nessun acquisto COW;
2. nessun acquisto SHEEP;
3. nessun `BUILD_PASTURE`;
4. nessun livestock placement;
5. nessun `FEED`;
6. nessuna riserva Wheat per feed;
7. nessuna task livestock harvest;
8. nessuna gestione Milk/Wool deliberata;
9. footprint E08 da 40 tile preservato;
10. workforce invariata;
11. Water-First invariato;
12. land expansion invariata;
13. crop behavior non-livestock non accidentalmente disabilitato.

Preferisci test mirati e deterministici.

Non rendere i test dipendenti dal benchmark completo.

---

# 8. Regression suite

Dopo l'implementazione:

1. esegui i nuovi test E09-01;
2. esegui l'intera suite esistente con `pytest`;
3. verifica che E08 e le strategie precedenti non siano state alterate;
4. controlla che non siano comparsi errori o regressioni.

Tutti i test devono passare prima di dichiarare BUILD completato.

---

# 9. Smoke test consentito

È consentito un **solo smoke test tecnico breve**, se necessario, per verificare che:

- E09-01 sia istanziabile;
- l'environment accetti le azioni;
- non avvengano crash/disqualification immediati;
- il logging necessario al futuro VERIFY funzioni.

Lo smoke test NON deve essere interpretato come risultato sperimentale.

NON eseguire ancora il benchmark paired da 30 episodi.

NON confrontare ancora formalmente E08/E09-01.

---

# 10. Preparazione del VERIFY

Predisponi, senza eseguire il benchmark completo, il supporto necessario al futuro VERIFY.

Il VERIFY dovrà confrontare:

```text
E08 40t Livestock ON
vs
E09-01 40t Livestock OFF
```

su 30 episodi paired:

- 10 `pass`;
- 10 `random`;
- 10 `starter`;
- stessi seed;
- stesso ordine;
- stessa configurazione environment.

Se serve un nuovo runner, puoi predisporlo durante BUILD, ma NON eseguire il benchmark completo.

Il runner futuro deve poter registrare almeno:

## Performance
- Final Money E08;
- Final Money E09-01;
- paired delta;
- Mean Final Money;
- Median;
- sample SD (`ddof=1`);
- mean paired delta;
- median paired delta;
- paired W/D/L.

## Robustezza
- Completion;
- Disqualification;
- breakdown per opponent.

## Meccanismo
- Worker Movement Share;
- `plant_pending`;
- capitale speso livestock;
- ricavi livestock;
- Wheat feed/reserve;
- eventuali metriche già disponibili sull'utilizzo produttivo delle tile.

Non inventare telemetrie invasive se richiedono modifiche comportamentali.

---

# 11. Entrypoint e submission

Durante BUILD:

- NON cambiare ancora l'entrypoint produttivo `src/agricola/agent.py` verso E09-01, salvo che la convenzione del repository richieda esplicitamente un entrypoint separato per test locali;
- NON sostituire la submission E08;
- NON eseguire `build_submission.py`;
- NON creare ZIP/package Kaggle;
- NON aprire Kaggle;
- NON aprire browser.

La promozione di E09-01 a submission candidate avverrà solo dopo VERIFY.

---

# 12. Documentazione

Crea o aggiorna il documento BUILD secondo la convenzione del repository, ad esempio:

```text
docs/versions/E09_build_livestock_ablation.md
```

oppure integra il documento E09 esistente se questa è la convenzione corrente.

Documenta:

1. classe/modulo E09-01;
2. differenze esatte da E08;
3. comportamento livestock rimosso;
4. variabili congelate;
5. test aggiunti;
6. regression suite;
7. eventuale smoke test;
8. supporto predisposto per VERIFY;
9. questioni aperte.

Aggiorna `PROJECT_STATE.md` e `NEW_SESSION.md` coerentemente.

Lo stato finale deve essere:

```text
E09-01 BUILD COMPLETED — READY FOR VERIFY
```

solo se tutti i test passano e non restano ambiguità bloccanti.

---

# 13. Git

Durante questa fase:

- puoi ispezionare `git diff`;
- puoi eseguire `git status`;
- NON fare commit;
- NON fare push;
- NON creare tag.

Il commit verrà autorizzato dopo REVIEW/SHIP secondo il workflow del progetto.

---

# STOP OBBLIGATORIO

Dopo aver completato BUILD:

**FERMATI.**

NON avviare autonomamente VERIFY.

In particolare:

- NON eseguire il benchmark paired da 30 episodi;
- NON interpretare performance da smoke test;
- NON modificare ulteriormente la strategia in base allo smoke test;
- NON costruire submission;
- NON accedere a Kaggle;
- NON fare commit/push/tag.

Attendi l'approvazione del supervisore.

---

# Output finale richiesto

Restituisci un report strutturato con:

## 1. Stato iniziale
- branch;
- HEAD;
- working tree;
- baseline E08 individuata.

## 2. Implementazione E09-01
- classe/modulo creato;
- relazione con E08;
- metodo usato per l'ablation.

## 3. Ablation effettiva
Tabella delle componenti livestock:

| Componente | E08 | E09-01 |
|---|---|---|
| Animal purchase | ON | OFF |
| Pasture build | ON | OFF |
| Placement | ON | OFF |
| Feed | ON | OFF |
| Feed buffer | ON | OFF |
| Livestock harvest | ON | OFF |
| Milk/Wool handling | ON | OFF |

## 4. Variabili congelate
Tabella E08/E09-01 che dimostri che tutto il resto è invariato.

## 5. Test
- nuovi test;
- risultato test E09-01;
- risultato full regression suite.

## 6. Smoke test
Se eseguito, riportare esclusivamente validità tecnica, senza interpretazione prestazionale.

## 7. VERIFY readiness
Confermare che il confronto paired E08/E09-01 può essere eseguito senza ulteriori modifiche comportamentali.

## 8. File modificati
Elenco completo.

## 9. Questioni aperte
Eventuali rischi o ambiguità residue.

## 10. Raccomandazione

Concludere esclusivamente con una delle due formule:

**READY FOR E09-01 VERIFY**

oppure

**NOT READY FOR E09-01 VERIFY**

motivando eventuali blocchi.

---

# Principio finale

E09-01 BUILD non deve cercare di creare un agente migliore.

Deve creare **E08 meno livestock**.

Se durante BUILD emerge la tentazione di migliorare qualcos'altro, non farlo.

La validità dell'esperimento dipende dal fatto che, al momento del VERIFY, possiamo attribuire la differenza osservata a una sola modifica:

> **Livestock ON → Livestock OFF.**
