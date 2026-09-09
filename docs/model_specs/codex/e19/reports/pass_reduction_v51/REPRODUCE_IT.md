# Riproduzione V51

Eseguire dalla radice del repository. Runtime usato in questa sessione:
`C:/Users/pietr/Projects/kaggriculture-agent/.venv/Scripts/python.exe`.
Il pacchetto del motore deve corrispondere a
`docs/foundation/ENGINE_SOURCE_MANIFEST.json`. I loader storici possono leggere
gli artefatti dal checkout originale, senza modificarlo.

```powershell
python -B -m pytest docs/model_specs/codex/e19/tests/test_committed_routes_v51.py docs/model_specs/codex/e19/tests/test_committed_routes_v51b.py docs/model_specs/codex/e19/tests/test_committed_routes_v51c.py -q
python -B docs/model_specs/codex/e19/tools/run_pass_reduction_v51.py --variant v51c --seed 180903003 --seat 0
python -B docs/model_specs/codex/e19/tools/run_pass_reduction_v51.py --variant v51c --seed 180903001 --seat 0
python -B docs/model_specs/codex/e19/tools/run_pass_reduction_v51.py --variant v51c --seed 180903002 --seat 0
python -B docs/model_specs/codex/e19/tools/run_matrix_v51.py development
python -B docs/model_specs/codex/e19/tools/build_v51_submission.py
python -B docs/model_specs/codex/e19/tools/verify_v51_parity.py docs/model_specs/codex/e19/reports/pass_reduction_v51/development_v51c_180903003_0.json
python -B docs/model_specs/codex/e19/tools/run_matrix_v51.py validation
```

La matrice rifiuta di aprire la fase successiva se i gate precedenti falliscono.
I due nuovi seed della validazione sono 260909201 e 260909202, entrambi i posti,
con una nuova esecuzione V49F abbinata a ogni caso. Non riutilizzare questi seed
come validazione non esposta dopo averne letto i risultati.

Solo dopo la fine delle altre simulazioni, eseguire serialmente:

Il comando `python -B docs/model_specs/codex/e19/tools/complete_v51.py` controlla
prima i risultati completi e avvia le due prove standard solo se i gate
strategici passano, quindi genera e sigilla il report. I comandi equivalenti
per i singoli passaggi sono:

```powershell
python -B docs/model_specs/codex/e19/tools/runtime_standard_v51.py submission/submission_codex_e19_770_v51_candidate.py v51c 180903001 0
python -B docs/model_specs/codex/e19/tools/runtime_standard_v51.py submission/submission_codex_e19_770_v51_candidate.py v51c 180903001 1
python -B docs/model_specs/codex/e19/tools/report_v51.py v51c
python -B docs/model_specs/codex/e19/tools/finalize_v51.py
```

Le simulazioni complete sono salvate come gzip JSON sotto `scratch/v51`
(directory ignorata da Git); le baseline esposte sotto `scratch/v49`.
Per rigenerare gli audit in un altro checkout servono questi file, indicati
dal campo `details` dei risultati. I JSON dei risultati, gli audit e i manifest
restano nella directory del report. A e B si riproducono con `--variant v51a`
e `--variant v51b`. Nessuno script esegue una submission esterna.
