# Indice artefatti Codex C2

Questo indice descrive la sola release Codex corrente. Le versioni transitorie
V6-V8, i prompt di attivazione e i builder obsoleti sono stati rimossi dopo
l'accettazione della revisione Foundation C2.1.

## ACTIVE

- `CODEX_V9_0_FINAL_REPORT_IT.md`: report completo corrente;
- `CODEX_V9_0_RESULTS.json` / `.csv`: suite canonica;
- `CODEX_V9_0_HOLDOUT_MANIFEST.md`: preregistrazione holdout;
- `CODEX_V9_0_HOLDOUT_RESULTS.json` / `.csv`: holdout congelato;
- `CODEX_V9_0_THREE_WAY_TOURNAMENT_MANIFEST.md`: torneo V9 precedente;
- `CODEX_V9_0_THREE_WAY_TOURNAMENT_RESULTS.json` / `.csv`: risultati del torneo precedente;
- `freeze/submission_codex_v9_tournament.py`: standalone V9 congelata, SHA-256 `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421`.

## DOCUMENTAZIONE CORRENTE

- `../../../../docs/model_specs/codex/MODEL_SPEC_CODEX_C2_3Q_POST_FOUNDATION_REVIEW.md`: MODEL_SPEC Codex corrente;
- `../foundation_revision/C2_1_POST_3Q_FOUNDATION_RECONCILIATION.md`: riconciliazione Foundation accettata;
- `../post_3q_closure_tournament/POST_3Q_CLOSURE_TOURNAMENT_REPORT_IT.md`: torneo di chiusura.

## BUILD E VERIFICA CORRENTI

- `scripts/build_submission_codex_v9.py`: builder corrente; per default scrive soltanto la freeze sotto `results/`, mentre i test devono passare un path temporaneo;
- `scripts/verify_submission_codex_v9.py`: verifica import isolato e parità 719/719;
- `tests/test_submission_codex_isolation.py`: parità V9 su file temporaneo, senza side effect sulla submission canonica.

## Submission canonica

`submission/submission_codex.py` è la sola submission Codex canonica corrente. La promozione è un'operazione release esplicita, mai un side effect di test o builder legacy.

I builder Codex precedenti e i relativi test di isolamento sono stati rimossi:
non possono più sovrascrivere la release corrente. La cronologia sperimentale
consolidata resta nel log di progetto e nei commit Git, senza duplicare qui
implementazioni non più supportate.
