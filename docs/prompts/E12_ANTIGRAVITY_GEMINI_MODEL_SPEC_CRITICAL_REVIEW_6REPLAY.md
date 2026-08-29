# E12 — ANTIGRAVITY/GEMINI CRITICAL REVIEW v2: 6 REPLAY, Q2 COUNTEREVIDENCE, MODEL_SPEC

## Obiettivo

Rieseguire la **critical evidence review di `docs/MODEL_SPEC.md` da zero sull'intero corpus corrente di 6 replay JSON**, includendo esplicitamente i tre nuovi replay di top player che superano `$100k` e utilizzano Q2.

Questa review sostituisce analiticamente la precedente review Antigravity basata su soli 3 replay.

NON preservare automaticamente le conclusioni della review precedente.

Scopo:

> verificare nuovamente ogni claim rilevante di `MODEL_SPEC.md` alla luce di un campione che contiene sia strategie compatte Q0/Q1 sia strategie top con Q2, distinguendo osservazione, inferenza e causalità.

Questa è una attività di **critical evidence review**, non di BUILD.

---

# Corpus obbligatorio

Analizzare tutti i JSON raw presenti in:

`docs/benchmark/`

Il corpus corrente deve includere almeno questi 6 episodi:

### Batch iniziale
- `101294736.json`
- `101705751.json`
- `101717011.json`

### Nuovi replay Q2
- `101462495.json`
- `101761797.json`
- `101891362.json`

Prima di iniziare, verificare effettivamente quali JSON sono presenti nella directory e riportare il corpus reale analizzato.

I tre nuovi replay Q2 sono stati aggiunti deliberatamente come **controevidenza** rispetto al campione iniziale.

---

# Regola fondamentale: re-audit, non append

NON limitarti ad aggiungere tre righe alla review precedente.

Ogni claim deve essere **riclassificato da zero sui 6 replay**.

In particolare, NON assumere più come valide le precedenti conclusioni:

- `Q2 not priority`
- `Q0+Q1 sufficient envelope`
- `Dense Engine Before Expansion`
- `Land Discipline`

Devono essere nuovamente verificate.

---

# Fonti e gerarchia dell'evidenza

## Evidenza primaria
1. replay JSON raw in `docs/benchmark/`

## Evidenza secondaria
2. `docs/MODEL_SPEC.md`
3. `results/benchmark/BENCHMARK_REGISTRY.md`
4. `results/benchmark/CROSS_COMPETITOR_ANALYSIS.md`
5. `results/benchmark/NEXT_MODEL_DELTA.md`
6. `results/e12/x114/COUNTERFACTUAL_LOG.md`
7. risultati X1.12/X1.13, solo se necessari

## Review precedenti

La precedente review Antigravity può essere letta **solo dopo aver ricostruito l'evidenza sui 6 replay**, per identificare quali conclusioni cambiano a causa dei nuovi dati.

NON usare la review precedente come fonte primaria.

---

# Non leggere ancora la review Codex

Per mantenere il confronto il più indipendente possibile, durante questa review NON leggere:

- `results/benchmark/CODEX_MODEL_SPEC_CRITICAL_REVIEW.md`
- `results/benchmark/CODEX_MODEL_SPEC_EVIDENCE_MATRIX.csv`
- `results/benchmark/CODEX_VS_ANTIGRAVITY_MODEL_REVIEW.md`

Questi file saranno confrontati solo in una fase successiva, dopo il salvataggio della nuova review Antigravity/Gemini.

Se vengono accidentalmente visualizzati tramite search/discovery, dichiararlo esplicitamente.

---

# Principio metodologico

Per ogni claim distinguere:

### OBSERVED
Fatto direttamente ricostruibile dai replay.

### INFERRED
Interpretazione coerente con i replay ma non direttamente dimostrata.

### CAUSAL_REQUIRED
Affermazione che richiede BUILD/counterfactual/esperimento.

Non confondere:

- correlazione con causalità;
- frequenza con optimality;
- assenza di comportamento con prova della sua negatività;
- presenza nei top con necessità universale;
- risultato di un singolo seed con regola generale.

---

# Claim da riesaminare

Auditare almeno:

1. Workforce Capacity First
2. fixed workforce count
3. workforce timing
4. workforce utilization
5. productive actions per Hand
6. movement/logistics overhead
7. backlog avoidance
8. Productive Surface First
9. physical utilization vs economic utilization
10. clean field / weed minimization
11. Dense Engine Before Expansion
12. Land Discipline
13. Q0-only viability
14. Q1 conditional expansion
15. Q2 not priority
16. Q2 conditional high-ceiling branch
17. livestock as economic engine
18. fixed livestock targets
19. multi-engine monetization
20. Deployable Capital
21. HIRE based on marginal monetizable throughput
22. crop-maintenance priority
23. horizon-aware shutdown
24. market/logistics efficiency
25. Wheat BUY_PRODUCT / SELL loop

Aggiungere altri claim se emergono da `MODEL_SPEC.md`.

---

# 1. Analisi Q2 — priorità alta

Questa è la principale novità del corpus.

Per ciascuno dei tre nuovi replay Q2 ricostruire almeno:

- competitor;
- final money;
- quadranti acquistati;
- giorno/turno acquisto Q1;
- giorno/turno acquisto Q2;
- cash prima e dopo l'espansione;
- Hands prima/dopo;
- productive tiles prima/dopo;
- crop/livestock mix prima/dopo;
- weeds/backlog prima/dopo;
- monetizzazione prima/dopo;
- eventuale tempo necessario per rendere produttiva la nuova superficie;
- peak productive tiles;
- final productive footprint.

Domande:

- Q2 viene acquistato presto o dopo una base economica già forte?
- l'espansione è immediatamente produttiva?
- viene accompagnata da aumento workforce?
- viene accompagnata da aumento livestock/crop?
- il capitale viene convertito rapidamente in superficie/produzione?
- i replay Q2 superano davvero il ceiling dei replay Q0/Q1?
- esistono costi/backlog visibili dopo l'espansione?
- cosa distingue Q2 efficace da semplice acquisto di terra?

NON concludere automaticamente:

`Q2 -> >100k`

Il replay mostra associazione, non causalità.

---

# 2. Riformulazione potenziale del land model

Verificare criticamente tre formulazioni alternative:

### A
`Q2 not priority`

### B
`Dense Engine Before Expansion`

### C
`Land expansion is conditional on expected value of additional productive capacity`

Valutare quale sia meglio supportata dal corpus completo.

Testare anche questa possibile formulazione:

> `Q2 is a conditional high-ceiling branch, not a fixed target and not a structurally rejected option.`

Classificarla senza assumerla come vera.

---

# 3. Workforce

Confrontare tutti e 6 i competitor:

- peak Hands;
- mean Hands;
- HIRE count;
- timing;
- Hands al momento delle espansioni;
- output economico;
- productive footprint;
- movement;
- task produttivi;
- backlog.

Tenere conto di X1.14:

- più workforce peggiora sui due seed obbligatori;
- migliora fortemente sul seed `1273000467`.

Verificare quindi se il claim corretto sia:

- workforce size;
- workforce timing;
- workforce utilization;
- value per Hand;
- capacità condizionale;
- combinazione di questi fattori.

`more Hands -> more money` deve essere considerato falsificato salvo nuova evidenza molto forte.

---

# 4. Weeds / clean field / crop SLA

La review precedente aveva già trovato controevidenza.

Con i 6 replay verificare:

- weed tile-days;
- final money;
- productive surface;
- expansion;
- crop maintenance;
- harvested-empty;
- unwatered.

Integrare X1.14:

> weeds drasticamente ridotte non hanno prodotto automaticamente maggiore final money.

Determinare se clean field sia:

- obiettivo;
- constraint operativo;
- proxy;
- effetto collaterale di buona scheduling;
- non causalmente determinabile.

---

# 5. Livestock

Confrontare tutti i 6 replay:

- Cow;
- Sheep;
- Goose;
- altre specie;
- timing;
- pasture;
- Milk;
- Wool;
- Egg;
- Fertilizer;
- relazione con crop engine;
- relazione con espansione Q1/Q2.

Verificare due claim distinti:

### Fixed livestock target
es. `7 Cow / 4 Sheep`

### Livestock as economic engine

Non confonderli.

---

# 6. Multi-engine monetization

Per ogni replay costruire una vista sintetica dei canali economici:

- crop sales;
- Milk;
- Wool;
- Egg;
- Fertilizer;
- altre commodity;
- BUY_PRODUCT;
- BUY_SEED;
- BUY_ANIMAL;
- eventuale concentrazione revenue.

Domanda critica:

> i top >100k vincono perché hanno più engine, oppure perché monetizzano meglio una combinazione specifica?

Se la causalità non è ricostruibile, dichiararlo.

---

# 7. Economic vs physical utilization

Confrontare:

- productive tiles;
- final money;
- weeds;
- Hands;
- livestock;
- quadranti;
- SELL;
- movimento;
- inventory/cash trajectory.

Verificare se:

> `physical utilization != economic utilization`

sia uno dei claim realmente robusti sul corpus completo.

---

# 8. Deployable Capital

Rivalutare sui replay Q2.

Q2 offre un caso utile perché permette di osservare:

- accumulo cash;
- acquisto terra;
- working capital successivo;
- attivazione superficie.

Verificare se `Deployable Capital` diventa più osservabile con questi replay oppure resta un costrutto inferito.

Non trasformare cash basso in prova automatica di efficienza.

---

# 9. Market / Wheat loop

Confrontare nostra policy e competitor dove i dati lo consentono:

- BUY_PRODUCT Wheat;
- SELL Wheat;
- quantità;
- timing;
- eventuali prezzi;
- inventario.

Non chiamare il nostro loop `waste` senza ledger economico.

Se i nuovi replay permettono una ricostruzione migliore, segnalarlo.

---

# 10. Endgame

Confrontare tutti e 6:

- ultimo HIRE;
- ultimi BUY_SEED / BUY_ANIMAL / BUY_LAND;
- riduzione workforce;
- liquidazione;
- SELL;
- declino productive surface;
- cash conversion.

Rivalutare `horizon-aware shutdown`.

---

# X1.14 come evidenza sperimentale

Usare:

| Variante | Seed 0 | Seed 421521921 |
|---|---:|---:|
| X1.12 baseline | 42,491 | 48,313 |
| workforce aggressive | 39,301 | 36,238 |
| workforce + crop priority | 31,585 | 35,537 |
| + livestock brake | 31,744 | 35,654 |

Seed `1273000467`:

- X1.12 = `$43,021`
- workforce aggressive = `$54,228`

Questo è un vero counterfactual della nostra policy e deve avere peso maggiore di una semplice correlazione cross-competitor per i claim che testa direttamente.

---

# Matrice cross-competitor

Creare una matrice aggiornata sui 6 replay.

Per ogni claim:

- episodio;
- competitor;
- evidence;
- classification;
- confidence;
- evidence type.

Classificazioni:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `MIXED`
- `NOT_SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVABLE`

Confidence:

- `LOW`
- `MEDIUM`
- `HIGH`

Evidence type:

- `OBSERVED`
- `INFERRED`
- `CAUSAL_REQUIRED`

---

# Output

NON sovrascrivere la precedente review a 3 replay.

Creare:

`results/benchmark/ANTIGRAVITY_MODEL_SPEC_CRITICAL_REVIEW_6REPLAY.md`

e:

`results/benchmark/ANTIGRAVITY_MODEL_SPEC_EVIDENCE_MATRIX_6REPLAY.csv`

La review deve contenere:

1. Executive verdict
2. Corpus and provenance
3. What changed from 3 to 6 replay
4. Hypothesis-by-hypothesis audit
5. Q2 deep analysis
6. Cross-competitor matrix
7. Claims strengthened by new replay
8. Claims weakened by new replay
9. Claims reversed by new replay
10. Claims still not observable
11. X1.14 causal counterevidence
12. Recommended MODEL_SPEC patch plan
13. What should NOT be changed yet
14. Open questions
15. Confidence limitations

---

# Patch plan — non applicare

NON modificare `docs/MODEL_SPEC.md`.

Produrre soltanto un patch plan con:

- `KEEP`
- `DOWNGRADE`
- `REFRAME`
- `REMOVE`
- `NEEDS_MORE_EVIDENCE`

Prestare particolare attenzione a:

- Q2 not priority
- Q2 conditional high-ceiling branch
- Dense Engine Before Expansion
- Land Discipline
- Workforce Capacity First
- clean field
- livestock economic engine
- multi-engine monetization
- physical vs economic utilization
- Deployable Capital
- HIRE marginal throughput

---

# Confronto con la vecchia review Antigravity

Dopo aver completato e salvato la nuova review:

leggere la precedente:

- `results/benchmark/MODEL_SPEC_CRITICAL_REVIEW.md`
- `results/benchmark/MODEL_SPEC_EVIDENCE_MATRIX.csv`

Creare una sezione esplicita:

## Evidence-driven verdict changes

Per ogni claim cambiato indicare:

- old verdict (3 replay);
- new verdict (6 replay);
- quale nuovo replay/evidenza ha causato il cambiamento;
- se il cambiamento deriva da vera controevidenza o solo da maggiore incertezza.

Questo serve a mostrare come il modello concettuale cambia quando arrivano nuovi esempi competitivi.

---

# NON confrontare ancora Codex

Non leggere gli artefatti Codex fino al completamento della review Antigravity/Gemini.

Il confronto Codex vs Antigravity sarà fatto separatamente dopo.

---

# Vincoli assoluti

- NO strategy changes
- NO MODEL_SPEC modification
- NO new mode
- NO X1.15
- NO benchmark execution
- NO tuning
- NO submission rebuild
- NO Kaggle upload
- NO commit
- NO push
- NO web
- NO modification raw JSON
- NO automatic patch application

---

# Verifica finale

Riportare:

1. replay analizzati;
2. competitor;
3. final money;
4. uso Q0/Q1/Q2;
5. claim auditati;
6. conteggio:
   - SUPPORTED
   - PARTIALLY_SUPPORTED
   - MIXED
   - NOT_SUPPORTED
   - CONTRADICTED
   - NOT_OBSERVABLE
7. cinque claim più solidi;
8. cinque claim più deboli;
9. claim che hanno cambiato verdetto rispetto alla review 3-replay;
10. conclusione specifica su Q2;
11. conclusione specifica su workforce;
12. conclusione specifica su clean field;
13. file creati;
14. file modificati;
15. `git status --short`.

Chiudere con:

`ANTIGRAVITY 6-REPLAY MODEL_SPEC CRITICAL REVIEW: COMPLETE`

`Q2 COUNTEREVIDENCE: INCLUDED`

`STRATEGY CODE: NOT MODIFIED`

`MODEL_SPEC: NOT MODIFIED — PATCH PLAN ONLY`
