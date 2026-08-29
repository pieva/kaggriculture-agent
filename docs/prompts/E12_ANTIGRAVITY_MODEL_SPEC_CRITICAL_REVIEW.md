# E12 — ANTIGRAVITY CRITICAL REVIEW: BENCHMARK JSON vs MODEL_SPEC

## Obiettivo

Eseguire una **revisione critica esclusivamente analitica** di `docs/MODEL_SPEC.md` confrontandolo con i replay JSON presenti in:

`docs/benchmark/`

Questa attività NON deve produrre alcun nuovo modello operativo, NON deve modificare la strategy, NON deve creare una nuova mode, NON deve ottimizzare parametri e NON deve preparare submission Kaggle.

Scopo unico:

> verificare quali affermazioni, regole, trigger, target e interpretazioni presenti in `MODEL_SPEC.md` siano realmente supportati dai replay competitivi disponibili, quali siano solo inferenze plausibili, quali siano sovra-generalizzazioni e quali siano contraddette dall'evidenza.

## Principio metodologico

Trattare i replay JSON come **evidenza primaria**.

Trattare:
- `MODEL_SPEC.md`
- `PROJECT_STATE.md`
- `NEW_SESSION.md`
- risultati X1.12/X1.13/X1.14
- analisi precedenti

come **interpretazioni secondarie**.

Non assumere che una conclusione già presente nel repository sia corretta solo perché documentata.

Cercare anche e soprattutto:
- controesempi;
- incoerenze;
- correlazioni spurie;
- causalità non dimostrate;
- target trasformati impropriamente da osservazioni;
- regole troppo rigide;
- generalizzazioni da singolo competitor o singolo seed.

## Input principali

Leggere:
1. tutti i replay JSON presenti in `docs/benchmark/`;
2. `docs/MODEL_SPEC.md`;
3. `results/benchmark/BENCHMARK_REGISTRY.md`;
4. `results/benchmark/CROSS_COMPETITOR_ANALYSIS.md`;
5. `results/benchmark/NEXT_MODEL_DELTA.md`;
6. `results/e12/x114/COUNTERFACTUAL_LOG.md`, se presente;
7. solo se necessario, i risultati X1.12/X1.13 per verificare come una regola sia stata implementata o falsificata.

Non usare fonti web.
Non usare Kaggle online.
Non modificare i JSON raw.

## 1. Workforce

Verificare criticamente:
- i competitor forti usano davvero più Hands della nostra policy?
- il numero di Hands è una causa plausibile del risultato o solo una correlazione?
- quando vengono assunti?
- quanto è stabile la workforce nel tempo?
- esistono competitor efficaci con meno Hands?
- X1.14 falsifica l'idea semplice `more Hands -> more money`?
- quali condizioni sembrano rendere redditizia una workforce maggiore?

Classificare separatamente:
- workforce size;
- workforce timing;
- utilization;
- productive actions per Hand;
- movement/logistics overhead;
- backlog avoidance.

## 2. Land discipline

Verificare:
- Q0-only può essere economicamente competitivo?
- Q1 è necessario, utile o soltanto frequente nei top replay?
- esiste evidenza sufficiente per una regola di espansione?
- `Q2 not priority` è supportato o deriva solo dall'assenza nei replay correnti?
- la frase “land count is endogenous to economic capacity” è osservata, inferita o troppo forte?

Non trasformare assenza di Q2 in prova che Q2 sia negativo.

## 3. Productive surface

Verificare:
- relazione fra peak/mean productive tiles e final money;
- weeds;
- harvested-empty;
- unwatered;
- densità produttiva;
- tempi di saturazione;
- eventuali competitor che monetizzano bene senza saturare superficie.

Distinguere chiaramente `physical utilization` da `economic utilization`.

Tenere conto dell'esito X1.14: meno weeds non ha prodotto automaticamente più final money.

## 4. Livestock

Verificare:
- livestock è realmente un componente comune dei replay forti?
- quali specie sono ricorrenti?
- la quantità di animali varia molto?
- esiste evidenza per un trigger generalizzabile?
- quale parte del vantaggio può derivare da Milk/Wool/Egg/Fertilizer?
- è possibile distinguere causalmente il valore del livestock dal resto del sistema?

Verificare esplicitamente che `7 Cow / 4 Sheep` resti correttamente classificato come osservazione di riferimento e NON target.

## 5. Multi-engine monetization

Verificare se i replay sostengono davvero la tesi:

> crop + livestock + fertilizer + other products > single-engine policy

Analizzare:
- SELL per commodity;
- BUY_PRODUCT;
- BUY_SEED;
- BUY_ANIMAL;
- inventario, se ricostruibile;
- timing delle vendite;
- contributo dei diversi engine.

Non assumere che numero di canali di vendita implichi automaticamente migliore performance.

## 6. Capital deployment

Verificare criticamente il concetto di `Deployable Capital`.

Chiedersi:
- è direttamente misurabile dai replay?
- quali proxy sono disponibili?
- cash basso dei competitor indica davvero investimento efficiente?
- cash alto può essere razionale in alcune fasi?
- quale evidenza distingue capitale “idle” da capitale tenuto per un acquisto imminente?

Se il concetto non è direttamente osservabile, mantenerlo `INFERRED`.

## 7. Market / Wheat loop

Prestare attenzione speciale al comportamento già osservato nella nostra policy:
- BUY_PRODUCT Wheat molto elevato;
- SELL Wheat molto elevato;
- differenza forte rispetto ai competitor.

Verificare dai JSON quanto è possibile ricostruire:
- numero operazioni;
- quantità;
- timing;
- eventuale prezzo;
- eventuale profit/loss.

Se i replay non contengono prezzi sufficienti, dichiarare esplicitamente che il danno economico NON è ancora dimostrato.

Non chiamarlo “waste” senza ledger.

## 8. Endgame

Confrontare:
- riduzione HIRE;
- stop investimenti;
- vendita inventario;
- riduzione superficie produttiva;
- liquidazione;
- azioni finali.

Valutare se esiste sufficiente evidenza per un principio di `horizon-aware shutdown` e con quale livello di confidenza.

# Analisi cross-competitor

Non produrre soltanto descrizioni per episodio.

Costruire una matrice con righe = ipotesi MODEL_SPEC e colonne = replay.

Per ciascuna ipotesi usare una delle categorie:
- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `MIXED`
- `NOT_SUPPORTED`
- `CONTRADICTED`
- `NOT OBSERVABLE`

Esempi:
- Workforce Capacity First
- Dense Engine Before Expansion
- Land Discipline
- Productive Surface First
- Multi-engine Monetization
- Livestock as economic engine
- Deployable Capital
- Horizon-aware shutdown
- Backlog avoidance
- Q2 conditional only
- HIRE based on marginal monetizable throughput

# Distinguere osservazione da causalità

Per ogni conclusione importante separare:

### OBSERVED
Fatto direttamente visibile nei JSON.

### INFERRED
Interpretazione coerente con i replay ma non direttamente dimostrata.

### CAUSAL CLAIM
Affermazione che richiederebbe un counterfactual o un esperimento.

Non elevare automaticamente `INFERRED` a `ADOPTED`.

# Confronto con X1.14

Usare X1.14 come controevidenza sperimentale.

Ricordare:
- baseline X1.12:
  - seed 0 = `$42,491`
  - seed 421521921 = `$48,313`
- workforce aggressive:
  - `$39,301`
  - `$36,238`
- crop priority:
  - `$31,585`
  - `$35,537`
- weeds scendono fortemente ma il money peggiora;
- seed `1273000467` mostra invece un caso favorevole:
  - workforce aggressive `$54,228`
  - X1.12 `$43,021`

Conclusione da verificare criticamente:

> Workforce Capacity First non è un invariante universale; potrebbe essere una policy condizionale dipendente dal valore marginale del lavoro.

Non assumere che questa formulazione sia già corretta: valutarla.

# Output richiesti

Creare:

`results/benchmark/MODEL_SPEC_CRITICAL_REVIEW.md`

con:
1. Executive verdict
2. Evidence base
3. Hypothesis-by-hypothesis audit
4. Cross-competitor matrix
5. Claims currently too strong
6. Claims supported by multiple replay
7. Claims contradicted by counterexamples
8. Claims not observable from current data
9. Causal claims requiring BUILD/counterfactual
10. Recommended MODEL_SPEC edits
11. What should NOT be changed yet
12. Open questions for next benchmark batch

Creare anche:

`results/benchmark/MODEL_SPEC_EVIDENCE_MATRIX.csv`

con almeno:
- claim_id
- claim
- episode_id
- competitor
- evidence
- classification
- confidence
- notes

# Modifica di MODEL_SPEC

NON modificare subito `docs/MODEL_SPEC.md`.

Prima produrre la review.

Alla fine, proporre un **patch plan**, non applicarlo.

Il patch plan deve classificare ogni modifica proposta come:
- `KEEP`
- `DOWNGRADE`
- `REFRAME`
- `REMOVE`
- `NEEDS_MORE_EVIDENCE`

Solo dopo approvazione umana si potrà aggiornare MODEL_SPEC.

# Vincoli assoluti

- NO strategy changes
- NO new mode
- NO X1.15
- NO benchmark execution
- NO parameter tuning
- NO submission rebuild
- NO Kaggle upload
- NO commit
- NO push
- NO web
- NO modification of raw replay JSON
- NO automatic MODEL_SPEC rewrite

Questa è una attività di **critical evidence review**, non di BUILD.

# Verifica finale

Riportare sinteticamente:
1. replay analizzati;
2. claim MODEL_SPEC analizzati;
3. quanti:
   - SUPPORTED
   - PARTIALLY_SUPPORTED
   - MIXED
   - NOT_SUPPORTED
   - CONTRADICTED
   - NOT OBSERVABLE
4. cinque claim più solidi;
5. cinque claim più deboli;
6. eventuali contraddizioni con X1.14;
7. file creati;
8. file modificati;
9. `git status --short`.

Chiudere con:

`MODEL_SPEC CRITICAL REVIEW: COMPLETE`

`STRATEGY CODE: NOT MODIFIED`

`MODEL_SPEC: NOT MODIFIED — PATCH PLAN ONLY`
