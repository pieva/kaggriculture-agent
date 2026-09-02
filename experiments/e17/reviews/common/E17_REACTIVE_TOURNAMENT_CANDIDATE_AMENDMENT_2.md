# E17.1 — Candidate amendment 2: development exhibition

- **Data:** 2026-09-02
- **Stato:** AUTHORIZED DEVELOPMENT EXHIBITION
- **Holdout:** NOT AUTHORIZED / NOT CONSUMED
- **Final confirmation:** NOT AUTHORIZED / NOT CONSUMED

Claude V2 ha completato sviluppo, test tecnici, audit di indipendenza e freeze,
ma il suo manifest dichiara `FROZEN_WITH_FAILED_GATES`. I gate non superati
sono: media development almeno 50.000, zero fughe animali derivate e
attivazione di tre quadranti in tutte le run.

Di conseguenza il torneo holdout definito in
`experiments/e17/design/E17_REACTIVE_THREE_WAY_TOURNAMENT_V1.md` resta
bloccato. Per ottenere evidenza diagnostica senza contaminare la prova futura,
è autorizzata un'esibizione non qualificante sui soli sette seed development
già consumati:

1. `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`;
2. `CODEX-E17.1-3Q-REACTIVE-GUARDED-V1`;
3. `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2`.

La matrice è seat-balanced:

```text
3 coppie × 7 seed development × 2 orientamenti = 42 match
```

Questa esibizione:

- non ammette Claude V2 al torneo ufficiale;
- non modifica alcuna policy o freeze;
- non autorizza selezione post-hoc di seed;
- non produce una submission Kaggle;
- non autorizza commit o push;
- deve riportare esplicitamente `DEVELOPMENT_ONLY_NON_QUALIFYING`.
