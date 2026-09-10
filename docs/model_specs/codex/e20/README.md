# E20 — 772

## E20.1 — revisione del pianificatore

- [Report finale della revisione](reports/e20_1/REPORT.html)
- [Torneo E18 / E19 / E20.1 e 22 KPI](reports/e20_1_confirmation/REPORT.html)
- [Specifica E20.1](E20_1_SPEC.md) e [protocollo](E20_1_PROTOCOL.json)
- [Sviluppo appaiato](reports/e20_1/development/REPORT.html), [ablation](reports/e20_1/screen/REPORT.html), [controllo 770](reports/e20_1/topology_control/REPORT.html)
- [Bundle E20v28](../../../../submission/submission_codex_e20_772_e20v28_candidate.py)

La decisione di promozione è nel report finale e in `reports/e20_1/DECISION.json`.
Il congelamento del bundle e il superamento dello sviluppo non certificano il risultato fuori campione.

Su questo portatile usare **un solo processo di simulazione** per i confronti ufficiali.
Il solo stato DONE non basta: ogni agente deve ricevere tutte le 719 chiamate.
I tentativi interrotti sotto carico sono conservati in `invalid_under_load` e non entrano nelle medie.
Gli aggregatori rifiutano esecuzioni incomplete. Non modificare i limiti di tempo del gioco per superare il controllo.

Per riprodurre E20.1 in uno stage nuovo, usare gli stessi comandi sotto con i modelli
`E18 E19 E20.1`, i seed `180910201`–`180910207` e `--workers 1`.
`verify_confirmation.py` verifica il corpus canonico; `summarize_e20_1.py` produce il report di decisione.

## E20 iniziale — E20v18

- [Report finale: 42 partite, 22 KPI](reports/tournament/REPORT.html)
- [Report Markdown](reports/tournament/REPORT.md) e [CSV D1–D30](reports/tournament/daily_kpi.csv)
- [Specifica](MODEL_SPEC_CODEX_E20_772.md)
- [23 varianti e selezione](reports/DEVELOPMENT.md)
- [Gate economico](artifacts/ECONOMIC_GATE.json)
- [Verifica torneo](artifacts/TOURNAMENT_VERIFICATION.json)
- [Protocollo congelato](VALIDATION_PROTOCOL.json)
- [Bundle locale](../../../../submission/submission_codex_e20_772_e20v18_candidate.py)

Il gate development passa (+4,56%); il torneo separato non conferma il
vantaggio. E20 non è promossa a sostituta di E19 e non è pubblicata su Kaggle.
E18 vince più partite; E19 ha la cassa media più alta nell'intero torneo.

## Riproduzione

Eseguire dalla radice, con `.venv/Scripts/python.exe`.
I runner conservano le cache esistenti. Per ripetere le simulazioni senza
sovrascrivere l'evidenza congelata usare una directory di stage nuova:

```powershell
.venv/Scripts/python.exe docs/model_specs/codex/e20/tools/run_experiment.py --stage reproduction --models E18 E19 E20 --seeds 180910101 180910102 180910103 180910104 180910105 180910106 180910107 --workers 1
.venv/Scripts/python.exe docs/model_specs/codex/e20/tools/audit_results.py reproduction
.venv/Scripts/python.exe docs/model_specs/codex/e20/tools/build_report.py reproduction
```

Il torneo canonico è nello stage `tournament`; `verify_tournament.py`
verifica quel corpus locale. `verify_gate.py` verifica la parità completa
fra candidata e standalone e il confronto economico development.
I replay compressi sono locali e ignorati da Git; JSON dei risultati,
ledger, CSV e manifest sono tracciati. Servono i replay locali per
rieseguire la verifica transizione per transizione.

Test: `python -m pytest docs/model_specs/codex/e20/tests/test_e20_contract.py -q`.
QA HTML: `node docs/model_specs/codex/e20/tools/qa_report.cjs <report.html>`;
richiede il runtime Playwright usato anche dagli altri report del repository.
