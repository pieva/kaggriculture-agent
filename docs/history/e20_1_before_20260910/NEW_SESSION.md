# Stato del progetto — E20 772 e torneo E18/E19/E20

Lavoro del 2026-09-10: E20 realizzata e congelata; ottimizzazione economica development conclusa; torneo di 42 partite e report dei 22 KPI completati. Nessuna nuova pubblicazione Kaggle. Codex resta l’unica linea di sviluppo attiva.

E20v18: 7–7–2, avvio E19 fino a D11, mucca Q2 (4,5) e pecora Q2 (4,6). Sei casi development: cassa media 96.405,3 contro 92.205,3 di E19 (+4,6%). Parità completa sorgente/standalone; zero errori core e perdite animali nel gate.

Conferma separata sui sette seed del torneo: contro E18, E20 61.943,1 contro E19 63.921,0; delta -1.977,9, positivo in 2/14 casi. La superiorità development non va estesa automaticamente al torneo o a Kaggle.

| Modello | Vittorie / partite | Cassa media torneo |
|---|---:|---:|
| E18 | 20/28 | 67.047,4 |
| E19 | 15/28 | 70.452,5 |
| E20 | 7/28 | 67.513,5 |

## Riferimenti

- [Report finale interattivo](model_specs/codex/e20/reports/tournament/REPORT.html) e [testo](model_specs/codex/e20/reports/tournament/REPORT.md).
- [Specifica E20](model_specs/codex/e20/MODEL_SPEC_CODEX_E20_772.md).
- [Registro delle 23 varianti e gate](model_specs/codex/e20/reports/DEVELOPMENT.md).
- [Verifica delle 42 partite](model_specs/codex/e20/artifacts/TOURNAMENT_VERIFICATION.json).
- [Bundle locale E20](../submission/submission_codex_e20_772_e20v18_candidate.py), hash `46d1c41c70605c14a7363908d6bc38d71e6ba387d7de9093ea8bd58dc7ce6f50`.
- Riferimento pubblicato invariato: V48 770, submission Kaggle 56101593, hash `57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`.

## Indicazioni per la ripresa

Distinguere target e topologie effettive, produzione e incassi, PASS e servizi. La regressione idrica di E20 rispetto a E19 sul development è esplicita nel report; il superamento economico non certifica una maggiore robustezza delle colture.

Tutti i seed development e torneo sono ora esposti. Non riutilizzare il torneo come holdout indipendente dopo ulteriori modifiche. E18/E19 e il bundle E20 restano congelati; eventuali nuove revisioni richiedono nuove versioni e un nuovo campione di conferma.

Riproduzione dalla radice con `.venv/Scripts/python.exe`: runner E20, audit_results.py, verify_gate.py, verify_tournament.py, build_report.py; parametri e seed nel protocollo. I replay compressi sono conservati localmente e ignorati da Git; ledger, manifest e CSV sono tracciati.

[Checkpoint precedente V48](history/e20_before_20260910/PROJECT_STATE.md).
