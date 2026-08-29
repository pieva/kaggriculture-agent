# E12 — GITHUB COPILOT INDEPENDENT CRITICAL REVIEW: 6 REPLAY vs MODEL_SPEC

## Obiettivo

Eseguire una **terza review indipendente** di `docs/MODEL_SPEC.md` confrontandolo con tutti i replay JSON raw presenti in:

`docs/benchmark/`

La review deve essere svolta nel **working tree locale corrente** del repository Kaggriculture e deve essere esclusivamente analitica.

Non modificare strategy, submission, MODEL_SPEC o ambiente Python.

Lo scopo è confrontare successivamente la lettura di GitHub Copilot con quelle di Codex e Antigravity/Gemini sullo stesso corpus competitivo.

---

# STOP — ENVIRONMENT SAFETY

La `.venv` è stata appena riparata e verificata.

## Ambiente canonico corrente

- Python validato: `3.12.13`
- `.venv`: `C:\Users\pietr\Projects\kaggriculture-agent\.venv`
- fonte canonica dipendenze: `pyproject.toml`
- `requires-python = ">=3.10,<3.14"`
- `kaggle-environments == 1.32.7` attualmente funzionante
- `pip check`: passato
- smoke X1.12:
  - seed 0 = `$42,491`
  - seed 421521921 = `$48,313`
  - source/submission equivalent

## Divieti assoluti sull'ambiente

NON:

- cancellare `.venv`;
- ricreare `.venv`;
- creare un'altra virtualenv;
- cambiare interprete Python;
- usare Python globale al posto della `.venv`;
- eseguire `pip install`;
- eseguire `pip uninstall`;
- aggiornare pip;
- modificare `pyproject.toml`;
- modificare requirements/dependency files;
- modificare PATH;
- cambiare interpreter settings del workspace;
- installare estensioni;
- eseguire setup/bootstrap;
- tentare di “riparare” dipendenze;
- usare package manager alternativi.

Se un comando Python fosse necessario, usare esclusivamente:

```powershell
.\.venv\Scripts\python.exe
```

Se la `.venv` non funziona, **FERMATI E SEGNALA IL PROBLEMA**.

Non tentare alcuna riparazione.

Questa task non richiede modifiche all'ambiente.

Principio:

> `Repository configuration → canonical .venv → verification`

Non introdurre stato environment specifico di Copilot.

---

# Working tree safety

Il working tree contiene numerose modifiche preesistenti.

NON:

- revert;
- reset;
- checkout di file;
- clean;
- stash;
- switch branch;
- creare branch;
- creare worktree;
- formattare automaticamente file esistenti;
- applicare fix non richiesti.

Prima di lavorare eseguire soltanto:

```powershell
git branch --show-current
git status --short
git log -1 --oneline
```

Usare lo stato corrente come read-only context.

---

# Corpus obbligatorio

Analizzare tutti i JSON raw presenti in:

`docs/benchmark/`

Il corpus corrente deve includere almeno:

- `101294736.json`
- `101705751.json`
- `101717011.json`
- `101462495.json`
- `101761797.json`
- `101891362.json`

I primi tre rappresentano strategie Q0/Q1 osservate in precedenza.

Gli ultimi tre sono stati aggiunti deliberatamente come controevidenza: sono replay di top player che superano `$100k` e utilizzano anche Q2.

Verificare il corpus reale prima dell'analisi.

Non modificare i JSON raw.

---

# BLIND REVIEW

Questa deve essere una review indipendente.

Prima di completare e salvare la tua analisi NON leggere:

- `results/benchmark/MODEL_SPEC_CRITICAL_REVIEW.md`
- `results/benchmark/MODEL_SPEC_EVIDENCE_MATRIX.csv`
- `results/benchmark/ANTIGRAVITY_MODEL_SPEC_CRITICAL_REVIEW_6REPLAY.md`
- `results/benchmark/ANTIGRAVITY_MODEL_SPEC_EVIDENCE_MATRIX_6REPLAY.csv`
- `results/benchmark/CODEX_MODEL_SPEC_CRITICAL_REVIEW.md`
- `results/benchmark/CODEX_MODEL_SPEC_EVIDENCE_MATRIX.csv`
- `results/benchmark/CODEX_VS_ANTIGRAVITY_MODEL_REVIEW.md`

Non usare search globale indiscriminata che possa mostrare accidentalmente questi artefatti.

Se li visualizzi accidentalmente, dichiaralo nella review.

Puoi leggere:

1. JSON raw;
2. `docs/MODEL_SPEC.md`;
3. `results/benchmark/BENCHMARK_REGISTRY.md`;
4. `results/benchmark/CROSS_COMPETITOR_ANALYSIS.md`;
5. `results/benchmark/NEXT_MODEL_DELTA.md`;
6. `results/e12/x114/COUNTERFACTUAL_LOG.md`;
7. X1.12/X1.13 solo se necessario.

---

# Principio metodologico

Per ogni claim distinguere:

### OBSERVED
Direttamente ricostruibile dai replay.

### INFERRED
Interpretazione compatibile con l'evidenza ma non dimostrata.

### CAUSAL_REQUIRED
Richiede counterfactual/BUILD/esperimento.

Non confondere:

- correlazione e causalità;
- comportamento frequente e comportamento ottimo;
- comportamento di un top player e requisito universale;
- assenza e prova di negatività;
- superficie fisica e valore economico.

---

# Claim da auditare

Analizzare almeno:

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

Aggiungere claim rilevanti presenti in MODEL_SPEC se necessario.

---

# Q2 — analisi prioritaria

Per i replay Q2 ricostruire almeno:

- final money;
- competitor;
- quadranti;
- timing Q1;
- timing Q2;
- cash intorno all'espansione;
- workforce intorno all'espansione;
- productive tiles prima/dopo;
- livestock/crop mix;
- backlog/weeds;
- velocità di attivazione nuova superficie;
- monetizzazione successiva;
- peak productive footprint.

Valutare indipendentemente queste formulazioni:

### A
`Q2 not priority`

### B
`Dense Engine Before Expansion`

### C
`Land expansion is conditional on expected value of additional productive capacity`

### D
`Q2 is a conditional high-ceiling branch, not a fixed target and not a structurally rejected option`

Non assumere che D sia corretta perché proposta da un altro agente.

---

# Workforce

Confrontare sui 6 replay:

- peak/mean Hands;
- HIRE timing;
- workforce durante Q1/Q2;
- utilization;
- movement;
- productive actions;
- economic output;
- backlog.

Integrare il counterfactual X1.14:

| Variante | Seed 0 | Seed 421521921 |
|---|---:|---:|
| X1.12 baseline | 42,491 | 48,313 |
| workforce aggressive | 39,301 | 36,238 |
| workforce + crop priority | 31,585 | 35,537 |
| + livestock brake | 31,744 | 35,654 |

Seed `1273000467`:

- X1.12 = `$43,021`
- workforce aggressive = `$54,228`

Quindi `more Hands -> more money` non può essere assunto.

---

# Clean field / weeds

Verificare:

- weed tile-days;
- harvested-empty;
- unwatered;
- productive footprint;
- money.

X1.14 mostra che ridurre fortemente weeds può peggiorare final money.

Classificare quindi clean field come possibile:

- objective;
- constraint;
- proxy;
- scheduling side effect;
- non-causal observable.

---

# Livestock e multi-engine

Confrontare:

- Cow;
- Sheep;
- Goose;
- pasture;
- Milk;
- Wool;
- Egg;
- Fertilizer;
- crop sales;
- timing.

Separare rigorosamente:

`fixed livestock target`

da:

`livestock as economic engine`

e verificare:

`multi-engine monetization`

senza assumere che maggiore varietà implichi automaticamente maggiore profitto.

---

# Physical vs economic utilization

Verificare se il corpus sostiene:

> `physical utilization != economic utilization`

Confrontare superficie, workforce, backlog, livestock, market activity e final money.

---

# Deployable Capital

Verificare se i replay Q2 permettono di osservare meglio:

cash → land purchase → working capital → activation → monetization.

Se non direttamente misurabile, mantenere il concetto come inferenza.

---

# Wheat / market loop

Analizzare la forte differenza già osservata nella nostra policy:

- BUY_PRODUCT Wheat elevato;
- SELL Wheat elevato.

Ricostruire ledger solo se i raw replay contengono dati sufficienti.

NON chiamare il loop `waste` senza prova economica.

---

# Endgame

Confrontare:

- ultimo HIRE;
- ultimi investimenti;
- riduzione workforce;
- SELL;
- liquidation;
- productive decline;
- cash conversion.

Auditare `horizon-aware shutdown`.

---

# Classificazione

Per ogni claim:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `MIXED`
- `NOT_SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVABLE`

Aggiungere:

- confidence: `LOW / MEDIUM / HIGH`
- evidence type: `OBSERVED / INFERRED / CAUSAL_REQUIRED`

---

# Output blind review

Creare esclusivamente:

`results/benchmark/COPILOT_MODEL_SPEC_CRITICAL_REVIEW_6REPLAY.md`

`results/benchmark/COPILOT_MODEL_SPEC_EVIDENCE_MATRIX_6REPLAY.csv`

La review deve contenere:

1. Executive verdict
2. Corpus and provenance
3. Hypothesis-by-hypothesis audit
4. Q2 deep analysis
5. Cross-competitor matrix
6. Strongest claims
7. Weakest claims
8. Counterexamples
9. Not observable claims
10. X1.14 causal counterevidence
11. Recommended MODEL_SPEC patch plan
12. What should NOT change
13. Open questions
14. Confidence limitations
15. Environment integrity statement

Patch plan:

- `KEEP`
- `DOWNGRADE`
- `REFRAME`
- `REMOVE`
- `NEEDS_MORE_EVIDENCE`

NON applicarlo.

---

# FASE 2 — confronto inter-agent

Solo DOPO avere salvato la review indipendente Copilot, leggere gli artefatti disponibili di:

- Codex;
- Antigravity precedente;
- Antigravity/Gemini 6-replay, se già presente.

Creare:

`results/benchmark/COPILOT_VS_CODEX_VS_ANTIGRAVITY_MODEL_REVIEW.md`

Per ogni divergenza importante riportare:

- claim;
- Copilot verdict;
- Codex verdict;
- Antigravity/Gemini verdict, se disponibile;
- raw evidence;
- possibile causa della divergenza;
- recommended human resolution.

Distinguere:

- divergenza dovuta a parsing;
- divergenza dovuta al corpus;
- divergenza interpretativa;
- divergenza causale;
- semplice differenza di confidence.

Non scegliere automaticamente un “vincitore”.

---

# Vincoli assoluti

- NO `.venv` changes
- NO Python environment changes
- NO dependency changes
- NO strategy changes
- NO MODEL_SPEC modification
- NO submission modification
- NO new mode
- NO X1.15
- NO benchmark execution
- NO parameter tuning
- NO Kaggle upload
- NO commit
- NO push
- NO branch/worktree changes
- NO raw JSON modification
- NO web

---

# Verifica finale

Riportare:

1. conferma `.venv` untouched;
2. replay analizzati;
3. claim auditati;
4. conteggio classificazioni;
5. cinque claim più solidi;
6. cinque claim più deboli;
7. conclusione Q2;
8. conclusione workforce;
9. conclusione clean field;
10. divergenze principali con gli altri agenti;
11. file creati;
12. file modificati;
13. `git status --short`.

Chiudere con:

`COPILOT 6-REPLAY MODEL_SPEC CRITICAL REVIEW: COMPLETE`

`CANONICAL .VENV: UNTOUCHED`

`STRATEGY CODE: NOT MODIFIED`

`MODEL_SPEC: NOT MODIFIED — PATCH PLAN ONLY`
