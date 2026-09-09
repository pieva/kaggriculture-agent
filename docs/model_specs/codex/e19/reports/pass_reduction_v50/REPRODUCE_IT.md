# Riproduzione V50

Tutti i comandi partono dalla radice del repository. `python` indica
l'ambiente locale verificato; in questa sessione è stato usato
`C:/Users/pietr/Projects/kaggriculture-agent/.venv/Scripts/python.exe` con `-B`.
Il motore deve corrispondere al manifest Foundation già fissato per V48/V49F.

I sorgenti sono in `docs/model_specs/codex/e19/tools`. La baseline F e i suoi
dati sono nella directory di report V49; non vengono sovrascritti. I risultati
V50 sono in questa directory. I replay gzip, gli inventari delle sonde e i
log sono in `scratch/v50`, ignorato da Git ma presente nel workspace. Copiare
anche quella directory per trasferire integralmente la sessione.

```powershell
python -B docs/model_specs/codex/e19/tools/route_causality_v50.py
python -B docs/model_specs/codex/e19/tools/inspect_certificate_v50.py
python -B docs/model_specs/codex/e19/tools/run_pass_reduction_v50.py --variant v50j --seed 180903003 --seat 0
python -B docs/model_specs/codex/e19/tools/run_matrix_v50.py v50j screen
python -B docs/model_specs/codex/e19/tools/analyze_pass_reduction_v50.py v50j
```

Il primo comando legge il replay esterno già esposto 106843637, con controllo
SHA, dal worktree o dal checkout originale in `C:/Users/pietr/Projects`.
Le sonde non vengono mai eseguite dalla candidata durante una partita.
Gli script di simulazione accettano i prototipi v50a–v50k. `screen` esegue
180903001/0 e 180903002/0; il terzo seed viene eseguito dal comando singolo.
Lo stage `development` eseguirebbe i tre posti 1, ma non è stato usato:
nessuna variante ha superato i gate sui tre seed al posto 0.

Il file standalone della revisione J respinta è riproducibile con:

```powershell
python -B docs/model_specs/codex/e19/tools/build_v50_submission.py
python -B docs/model_specs/codex/e19/tools/verify_v50_parity.py docs/model_specs/codex/e19/reports/pass_reduction_v50/development_v50j_180903003_0.json
```

Le prove runtime sono **seriali**, senza altre simulazioni concorrenti,
con actTimeout=1 e overage standard. Verificano anche la parità con le azioni
dei replay V49F già registrati. Non sono una submission né una garanzia di
equivalenza con l'hardware Kaggle.

```powershell
python -B docs/model_specs/codex/e19/tools/runtime_standard_v50.py submission/submission_codex_e19_770_v49f_candidate.py v49f 180903001 0
python -B docs/model_specs/codex/e19/tools/runtime_standard_v50.py submission/submission_codex_e19_770_v49f_candidate.py v49f 180903001 1
python -B -m pytest docs/model_specs/codex/e19/tests/test_workforce_certificate_v50.py -q
python -B docs/model_specs/codex/e19/tools/build_pass_report_v50.py v50j
python -B docs/model_specs/codex/e19/tools/verify_pass_report_v50.py
```

Le matrici comportamentali usano actTimeout=120 e mantengono separate le
misure runtime. I JSON `summary_v50*.json` riportano tutti i gate e i deficit
per caso; `*_obligations.json` contiene gli audit con hash del replay e del
codice di misura. Il manifest della candidata identifica il bundle J e i
suoi 23 sorgenti runtime più il builder. È un artefatto respinto.

I seed 260909201/202 sono preregistrati ma **non aperti**. Anche quelli
260909101/102 restano esposti dalla V49 e non sono stati riciclati come holdout.
Nessun nuovo avversario esterno è stato consultato o usato per validare V50.

`integrity.json` e `report_manifest.json` verificano gli hash dei riferimenti,
la parità D1–D28 dei 17 replay, i due runtime standard e i link del report.
