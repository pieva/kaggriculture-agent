# E09-05B — REVIEW Correction Pass — Livestock Subsystem Ablation

## Obiettivo

Eseguire una **micro-correzione documentale** del REVIEW E09-05 prima della chiusura della fase E09.

Il REVIEW è sostanzialmente approvato e la conclusione sperimentale non deve essere riaperta:

> **E09 HYPOTHESIS CONFIRMED**

Questa attività serve esclusivamente a verificare e correggere due possibili incoerenze quantitative nel documento:

1. uso non uniforme di **Top 23** vs **Top 25** episodes;
2. riconciliazione completa del confronto paired **E09-01 vs E06**, dato che E09-01 risulta vincente in 21/30 episodi ma il testo quantifica esplicitamente solo 7 sconfitte severe.

**NON modificare codice produttivo.**
**NON modificare la strategia E09-01.**
**NON eseguire nuovi benchmark.**
**NON creare E10.**
**NON accedere a Kaggle.**

---

# 1. Fonti da utilizzare

Usa esclusivamente evidenze già disponibili nel repository, in particolare:

- `results/e09_livestock_ablation.json`
- `scratch/analyze_e09_review.py`
- `docs/versions/E09_review_livestock_ablation.md`
- eventuali risultati E06/E08 già inclusi nel dataset E09.

Non rieseguire il benchmark a 30 episodi.

Puoi eseguire lo script diagnostico esistente o piccoli comandi read-only per verificare i calcoli.

---

# 2. Correzione Top 23 / Top 25

Nel REVIEW compare una descrizione della distribuzione E09-01 con:

> **Top 23 Episodes (76.7%)**

mentre successivamente il confronto sui ricavi Melone utilizza una popolazione indicata come:

> **Top 25**

Queste due popolazioni potrebbero essere intenzionalmente diverse oppure potrebbe trattarsi di un errore documentale.

Verifica direttamente:

- criteri usati da `scratch/analyze_e09_review.py`;
- numero effettivo di episodi classificati come bottom;
- numero effettivo di episodi appartenenti al gruppo complementare;
- criterio eventualmente usato per il confronto `Melon Revenue`;
- media `Melon Revenue` realmente calcolata;
- eventuale differenza tra "Top episodes" e "Top revenue episodes".

## Regola

Non scegliere arbitrariamente 23 o 25.

Ricostruisci il calcolo e usa nel documento:

- denominatore corretto;
- criterio esplicito;
- valore medio corretto.

Se il REVIEW identifica **7 bottom episodes su 30**, il gruppo complementare naturale è **23 episodi**. Se il calcolo dei ricavi Melone usa invece un'altra selezione, deve essere denominata esplicitamente e motivata.

Evita espressioni generiche come `Top 25` se non corrispondono a una popolazione formalmente definita.

---

# 3. Riconciliazione E09-01 vs E06

Il REVIEW riporta:

> E09-01 supera E06 in **21 episodi su 30 (70.0%)**.

Questo lascia **9 episodi** in cui E09-01 non supera E06.

Il testo successivo quantifica:

> **7 sconfitte severe**

con:

- mean loss = **-$12,892.44**
- total severe losses = **-$116,032.00**

Verifica il confronto paired episodio per episodio e classifica tutti i 30 casi in:

```text
E09-01 > E06
E09-01 = E06
E09-01 < E06
```

Riporta:

- wins;
- ties;
- losses;
- somma dei delta positivi;
- somma dei delta negativi;
- mean gain nei wins;
- mean loss nei losses;
- delta totale;
- delta medio sui 30 episodi.

---

# 4. Verifica della categoria "7 severe losses"

Determina cosa rappresentano esattamente le 7 run già evidenziate.

Potrebbero essere:

- tutte le sconfitte;
- solo le sconfitte catastrofiche;
- bottom 7 E09-01;
- subset delle 9 non-vittorie.

Non assumere.

Verifica.

Se esistono altri 2 episodi non vincenti, documentali esplicitamente indicando:

- episode index;
- seed;
- opponent;
- E09-01 money;
- E06 money;
- paired delta;
- classificazione (`mild loss`, `tie` o altra categoria descrittiva giustificata).

La somma delle categorie deve riconciliare esattamente i **30 episodi**.

---

# 5. Controllo aritmetico complessivo

Verifica che:

```text
sum(paired_delta_i) / 30
```

sia coerente con:

```text
Mean(E09-01) - Mean(E06)
```

Valori di riferimento:

```text
E09-01 Mean = $22,899.20
E06 Mean    = $24,731.37
Expected mean delta ≈ -$1,832.17
```

La somma dei guadagni e delle perdite paired deve spiegare esattamente, salvo arrotondamenti, questo delta.

Se i valori precedentemente riportati:

- `+$61,067.00`
- `-$116,032.00`

non riconciliano correttamente il totale, correggili.

---

# 6. Non modificare la diagnosi salvo evidenza contraria

La diagnosi principale attuale è:

> La coda negativa E09-01 è **seed/state-specific**, non opponent-specific.

Failure mode principale:

> **Day 12 Q1 Land Expansion Cash Bottleneck — HIGH CONFIDENCE**

Failure mode secondario:

> **Rigid Seed Buying Cash Floor — MEDIUM CONFIDENCE**

Queste conclusioni restano valide salvo che il controllo quantitativo dimostri esplicitamente un errore.

Non trasformare questa correction pass in un nuovo REVIEW.

---

# 7. Candidate hypotheses

Mantieni le tre candidate hypotheses già individuate.

La raccomandazione del supervisore è però di considerare come candidata principale per il prossimo ciclo:

> **Prioritized Q1 Land Expansion Capital Buffer**

Motivazione:

- interviene direttamente sul failure mode con confidence HIGH;
- cerca di eliminare la coda negativa;
- preserva il ceiling elevato E09-01;
- mantiene 40 tile;
- mantiene Livestock OFF;
- evita di confondere il test modificando contemporaneamente crop mix o footprint.

Non creare ancora E10 e non implementare questa ipotesi.

---

# 8. Decisione sulla submission Kaggle

Non preparare una submission E09-01 in questa fase.

Motivazione da registrare, se coerente con la convenzione documentale:

> E09-01 ha dimostrato localmente un ceiling competitivo e ha confermato l'ipotesi di ablation, ma presenta ancora una coda negativa severa e un floor di $5,788. La causa è sufficientemente diagnosticata da giustificare un ulteriore esperimento locale prima di utilizzare una validazione Kaggle.

Questo non significa che E09-01 sia fallito.

Significa che:

- **l'ipotesi E09 è confermata**;
- E09-01 è una base sperimentale valida;
- non è ancora il candidato preferito per external validation.

---

# 9. File da aggiornare

Aggiorna, se necessario:

- `docs/versions/E09_review_livestock_ablation.md`
- `docs/PROJECT_STATE.md`
- `docs/NEW_SESSION.md`

Non modificare file produttivi.

Se la convenzione del repository lo prevede, puoi creare un breve documento correction pass, ad esempio:

`docs/versions/E09_review_correction_pass.md`

ma evita duplicazioni inutili se è sufficiente correggere il REVIEW principale.

---

# 10. Stato finale E09

Dopo la correzione, lo stato deve essere inequivocabile:

```text
E09-05 REVIEW APPROVED
E09 HYPOTHESIS CONFIRMED
E09-01 NOT SELECTED FOR KAGGLE SUBMISSION YET
NEXT EXPERIMENTAL QUESTION: Q1 expansion capital protection
```

Non dichiarare ancora E09 SHIPPED se il workflow del repository riserva SHIP a commit/tag/closure.

---

# 11. Git

Durante questa correction pass:

- `git status` consentito;
- `git diff` consentito;
- lettura log/tag consentita;
- NON fare commit;
- NON fare push;
- NON creare tag.

---

# STOP OBBLIGATORIO

Dopo aver corretto e verificato il REVIEW:

**FERMATI.**

NON creare E10.
NON implementare capital reserve.
NON modificare seed policy.
NON modificare footprint.
NON eseguire nuovi benchmark.
NON costruire submission.
NON accedere a Kaggle.
NON fare commit/push/tag.

Attendi la decisione del supervisore.

---

# Output finale richiesto

## 1. Top-group reconciliation
Spiega se il valore corretto è Top 23, Top 25 o due popolazioni diverse, riportando il calcolo corretto.

## 2. E09-01 vs E06 reconciliation
Riporta:

- wins;
- ties;
- losses;
- mean gain;
- mean loss;
- total gains;
- total losses;
- overall paired mean delta.

## 3. Missing/non-winning episodes
Identifica esplicitamente gli eventuali due episodi non spiegati dal precedente riferimento alle 7 severe losses.

## 4. REVIEW corrections
Elenca le correzioni effettuate al documento.

## 5. Verdict
Conferma o modifica:

> **E09 HYPOTHESIS CONFIRMED**

## 6. Next experimental question
Senza creare E10, registra:

> **Se E09-01 protegge il capitale necessario all'acquisto di Q1 al Giorno 12, gli episodi della coda negativa scompaiono senza ridurre le prestazioni degli episodi già forti?**

## 7. File modificati
Elenco completo.

Concludi con:

**E09 REVIEW CORRECTED — READY FOR SUPERVISOR DECISION**
