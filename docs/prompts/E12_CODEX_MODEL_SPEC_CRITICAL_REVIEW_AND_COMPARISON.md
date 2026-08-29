# E12 — CODEX INDEPENDENT CRITICAL REVIEW: BENCHMARK JSON vs MODEL_SPEC

## Obiettivo

Eseguire una **seconda revisione critica indipendente** di `docs/MODEL_SPEC.md`, usando come evidenza primaria i replay JSON presenti in:

`docs/benchmark/`

Questa attività deve replicare il lavoro già svolto da Antigravity, ma in modo indipendente, così da confrontare due agenti sullo stesso materiale.

Non modificare strategy.
Non creare nuove mode.
Non fare benchmark.
Non fare tuning.
Non rebuildare submission.
Non fare upload Kaggle.
Non fare commit/push.

Scopo:

> verificare quali claim di `MODEL_SPEC.md` siano supportati, solo parzialmente supportati, misti, non supportati, contraddetti o non osservabili dai replay competitivi disponibili.

---

# Regola di indipendenza

## Prima fase: blind review

Nella prima fase NON leggere:

- `results/benchmark/MODEL_SPEC_CRITICAL_REVIEW.md`
- `results/benchmark/MODEL_SPEC_EVIDENCE_MATRIX.csv`
- eventuali walkthrough/artefatti prodotti da Antigravity

Devi arrivare autonomamente a:

- classificazione dei claim;
- evidenze;
- controesempi;
- livelli di confidenza;
- patch plan.

Usa invece:

1. tutti i JSON raw in `docs/benchmark/`
2. `docs/MODEL_SPEC.md`
3. `results/benchmark/BENCHMARK_REGISTRY.md`
4. `results/benchmark/CROSS_COMPETITOR_ANALYSIS.md`
5. `results/benchmark/NEXT_MODEL_DELTA.md`
6. `results/e12/x114/COUNTERFACTUAL_LOG.md`
7. eventuali risultati X1.12/X1.13 solo se necessari per verificare claim causali o implementazioni precedenti

I JSON raw sono la fonte primaria.

---

# Principio metodologico

Separare sempre:

### OBSERVED
Fatti direttamente leggibili nei replay.

### INFERRED
Interpretazioni compatibili con i replay ma non dimostrate.

### CAUSAL CLAIM
Affermazioni che richiedono un counterfactual / BUILD / esperimento.

Non trattare correlazioni come causalità.

Cercare attivamente:

- controesempi;
- replay che indeboliscono una regola;
- differenze tra competitor;
- differenze tra seed;
- claim troppo generali;
- claim non misurabili dai replay;
- osservazioni trasformate impropriamente in target.

---

# Ipotesi da auditare

Analizzare almeno:

1. Workforce Capacity First
2. workforce size
3. workforce timing
4. workforce utilization
5. backlog avoidance
6. Productive Surface First
7. Dense Engine Before Expansion
8. Land Discipline
9. Q1 conditional expansion
10. Q2 conditional only / not priority
11. livestock as economic engine
12. fixed livestock targets are invalid
13. multi-engine monetization
14. Deployable Capital
15. horizon-aware shutdown
16. HIRE based on marginal monetizable throughput
17. crop-maintenance priority
18. physical utilization vs economic utilization
19. market/logistics efficiency
20. Wheat BUY_PRODUCT / SELL loop

Se `MODEL_SPEC.md` contiene altri claim rilevanti, includerli.

---

# Workforce

Verificare:

- quanti Hands vengono realmente usati dai competitor;
- quando vengono assunti;
- durata e stabilità della workforce;
- quanto output economico è associato alla workforce;
- movimento vs azioni produttive;
- eventuali competitor forti con workforce inferiore;
- se X1.14 falsifica `more Hands -> more money`;
- se il claim più corretto sembra essere capacity, timing, utilization o value-per-action.

Non concludere “serve più workforce” solo dai peak Hands.

---

# Land

Verificare:

- Q0-only competitività;
- timing e valore apparente di Q1;
- presenza/assenza Q2;
- rapporto tra superficie sbloccata e superficie produttiva;
- se l'espansione precede o segue una forte monetizzazione;
- se `Dense Engine Before Expansion` regge davvero;
- se `Land Discipline` è osservazione o inferenza.

IMPORTANTE:

Se nel batch sono presenti nuovi replay Q2, includerli integralmente nell'analisi.

Non assumere che Q2 sia negativo solo perché assente nei replay precedenti.

---

# Productive surface / weeds / backlog

Misurare e confrontare:

- peak productive tiles;
- mean productive tiles se ricostruibile;
- weeds tile-days;
- harvested-empty;
- unwatered;
- saturazione;
- rendimento finale.

Tenere conto esplicitamente della controevidenza X1.14:

- weeds molto ridotte;
- final money peggiore.

Valutare se “clean field” sia causa, proxy, correlazione o semplice condizione locale.

---

# Livestock

Verificare:

- presenza in ogni replay;
- Cow / Sheep / Goose / altre specie;
- quantità e timing;
- SELL Milk / Wool / Egg / Fertilizer;
- differenze tra competitor;
- ruolo relativo rispetto ai crop.

Controllare che configurazioni come `7 Cow / 4 Sheep` restino `OBSERVED_REFERENCE`, non target.

---

# Multi-engine monetization

Verificare se i replay sostengono davvero una architettura multi-engine.

Analizzare per competitor:

- SELL per commodity;
- BUY_PRODUCT;
- BUY_SEED;
- BUY_ANIMAL;
- timing monetizzazione;
- distribuzione dei canali di revenue;
- eventuale dipendenza da una singola commodity.

Non confondere “più tipi di vendita” con “maggiore profitto”.

---

# Deployable Capital

Verificare:

- se è direttamente osservabile;
- se può essere derivato;
- quali proxy possono essere usati;
- cash trajectory;
- investimenti imminenti;
- idle cash apparente.

Se non è misurabile direttamente, deve restare `INFERRED` o essere riformulato.

---

# Market / Wheat loop

Prestare particolare attenzione alla nostra policy:

- BUY_PRODUCT Wheat molto alto;
- SELL Wheat molto alto;
- comportamento diverso dai competitor.

Se possibile ricostruire:

- quantità;
- timing;
- prezzi;
- P/L;
- inventario;
- flusso BUY → uso → SELL.

Se i prezzi non sono ricostruibili dai replay, NON chiamarlo “waste”.

Classificarlo come domanda aperta / ledger necessario.

---

# Endgame

Verificare per ciascun competitor:

- ultimo HIRE;
- riduzione workforce;
- stop land/animal/seed investment;
- liquidazione;
- selling;
- declino superficie;
- cash conversion;
- PASS/movimento finale.

Classificare `horizon-aware shutdown` solo sulla base di evidenza comparata.

---

# X1.14 come controevidenza causale

Usare questi risultati:

| Variante | Seed 0 | Seed 421521921 |
|---|---:|---:|
| X1.12 baseline | 42,491 | 48,313 |
| workforce aggressive | 39,301 | 36,238 |
| workforce + crop priority | 31,585 | 35,537 |
| + livestock brake | 31,744 | 35,654 |

Seed `1273000467`:

- X1.12 = 43,021
- workforce aggressive = 54,228

Quindi verificare criticamente:

> Workforce Capacity First potrebbe essere condizionale e non universale.

Non assumere questa conclusione come vera: valutarla.

---

# Classificazione

Per ogni claim usare:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `MIXED`
- `NOT_SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVABLE`

Aggiungere:

- confidence: LOW / MEDIUM / HIGH
- evidence type: OBSERVED / INFERRED / CAUSAL_REQUIRED

---

# Output prima fase

Creare:

`results/benchmark/CODEX_MODEL_SPEC_CRITICAL_REVIEW.md`

e:

`results/benchmark/CODEX_MODEL_SPEC_EVIDENCE_MATRIX.csv`

La review deve contenere:

1. Executive verdict
2. Evidence base
3. Hypothesis-by-hypothesis audit
4. Cross-competitor matrix
5. Claims currently too strong
6. Claims strongly supported
7. Counterexamples
8. Not observable claims
9. Causal claims requiring counterfactual
10. Recommended MODEL_SPEC patch plan
11. Claims that should remain unchanged
12. Open questions
13. Confidence limitations

Il patch plan deve usare:

- `KEEP`
- `DOWNGRADE`
- `REFRAME`
- `REMOVE`
- `NEEDS_MORE_EVIDENCE`

NON applicare il patch.

---

# Seconda fase: confronto con Antigravity

Solo DOPO aver salvato la review indipendente:

leggere:

- `results/benchmark/MODEL_SPEC_CRITICAL_REVIEW.md`
- `results/benchmark/MODEL_SPEC_EVIDENCE_MATRIX.csv`

Produrre:

`results/benchmark/CODEX_VS_ANTIGRAVITY_MODEL_REVIEW.md`

Confrontare:

1. claim con stessa classificazione;
2. claim con classificazione diversa;
3. differenze di interpretazione causale;
4. evidenze usate da uno e non dall'altro;
5. possibili errori di parsing;
6. possibili sovra-generalizzazioni;
7. dove uno dei due agenti è più prudente;
8. dove uno dei due agenti è più assertivo;
9. quali divergenze richiedono controllo umano;
10. quali divergenze richiedono nuovi replay o counterfactual.

Per ogni divergenza importante indicare:

- Antigravity verdict
- Codex verdict
- raw evidence
- recommended human resolution

---

# Vincoli assoluti

- NO strategy changes
- NO MODEL_SPEC modification
- NO new mode
- NO X1.15
- NO benchmark run
- NO parameter tuning
- NO submission rebuild
- NO Kaggle upload
- NO commit
- NO push
- NO web
- NO raw JSON modifications

---

# Final report

Riportare:

1. replay analizzati;
2. nuovi replay eventualmente rilevati;
3. numero totale claim;
4. conteggio:
   - SUPPORTED
   - PARTIALLY_SUPPORTED
   - MIXED
   - NOT_SUPPORTED
   - CONTRADICTED
   - NOT_OBSERVABLE
5. cinque claim più solidi;
6. cinque claim più deboli;
7. principali contraddizioni con X1.14;
8. principali divergenze rispetto ad Antigravity;
9. file creati;
10. file modificati;
11. `git status --short`.

Chiudere con:

`CODEX MODEL_SPEC CRITICAL REVIEW: COMPLETE`

`INDEPENDENT REVIEW: COMPLETE`

`CODEX VS ANTIGRAVITY COMPARISON: COMPLETE`

`STRATEGY CODE: NOT MODIFIED`

`MODEL_SPEC: NOT MODIFIED — PATCH PLAN ONLY`
