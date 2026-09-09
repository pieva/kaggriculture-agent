# Riproduzione della diagnosi e della candidata V49F

Eseguire dalla radice del repository. I comandi qui sotto usano `python` come
segnaposto dell'ambiente locale: in questa sessione è stato usato
`C:/Users/pietr/Projects/kaggriculture-agent/.venv/Scripts/python.exe`, con `-B`.
Il motore deve corrispondere ai tre hash della Foundation, verificati in
`integrity.json`. Non serve collegarsi a Kaggle per ripetere le prove locali.

## Artefatti e provenienza

- `candidate_f_manifest.json`: hash della candidata, dei 19 sorgenti runtime
  e del builder. V48 e i suoi 18 sorgenti sono verificati separatamente.
- `diagnostic_106843637.json`, `opening_attribution.json`: diagnosi strumentata
  e provenienza dei PASS del piano assistito sul replay esposto.
- `diagnostic_pass_events.csv`: tutti i PASS del replay diagnosticato con
  inventario, missione e tentativi, senza dover aprire il gzip.
- `external_worker_pass.csv`: 38 replay già esposti, conteggi per giorno/persona.
- `development_*.json`, `validation_*.json`: risultati completi, ledger,
  comandi riusciti, persone presenti e tempi. I file delle revisioni respinte
  rimangono distinti da quelli F.
- `*_obligations.json`: deficit osservati, perdite, slot per persona e
  checkpoint di percorso previsto/lavoro impegnato/comandi realizzati.
  I checkpoint sovrapposti non vanno sommati.
- `validation_opened.json`: momento di apertura dei due seed nuovi e hash
  congelato. L'avversario V4D era già esposto; i posti non sono repliche indipendenti.
- `opening_equivalence.json`, `parity_v49f_*.json`, `integrity.json`: verifiche
  degli stati, di tutte le azioni del bundle e della baseline storica.
- `summary.json`, `REPORT_V49_PASS_IT.html`, `figures/`: gate e grafici finali F.
  `REJECTED_V49A_IT.html` e `rejected_a_summary.json` riguardano solo A.
- `report_manifest.json`: inventario e hash dei file consegnati nel report,
  dopo il controllo dei link e della completezza delle prove.

I replay grezzi delle simulazioni e i dettagli strumentati sono file gzip in
`scratch/v49/`, esclusi da Git ma presenti in questo workspace. Ogni risultato
indica il percorso; gli audit ne registrano l'hash. Per trasferire la sessione
insieme ai dati grezzi copiare anche questa directory. Le simulazioni locali
sono rigenerabili. Il replay esterno originale e i ledger storici, se assenti
dal worktree, vengono letti dal checkout originale indicato negli script;
nessun file di quel checkout viene modificato.

## Comandi

Gli script sono in `docs/model_specs/codex/e19/tools/`. Diagnosi e builder:

```powershell
python -B docs/model_specs/codex/e19/tools/pass_diagnostic_v49.py --episode 106843637
python -B docs/model_specs/codex/e19/tools/attribute_v49_opening.py
python -B docs/model_specs/codex/e19/tools/build_v49f_submission.py
```

Per rigenerare un caso, scegliere `v48` o `v49f`, il seed e il posto:

```powershell
python -B docs/model_specs/codex/e19/tools/run_pass_reduction_v49.py --variant v49f --seed 180903003 --seat 0 --split development --no-telemetry
```

Matrice completa: sviluppo sui seed 180903001, 180903002, 180903003; validazione
sui seed 260909101 e 260909102. Entrambe le policy, posti 0 e 1, per ciascun seed.
`run_v49_final.py` è l'orchestrazione originale: assume già presenti tutte le
baseline di sviluppo e lo screen F 180903003/0, verifica lo sviluppo e poi apre
la partizione nuova. Rieseguirlo ora non rende nuovamente non esposti quei seed
e sovrascrive il timestamp: conservare il record originale dell'apertura.

Verifica e generazione del report, dopo la matrice:

```powershell
python -B docs/model_specs/codex/e19/tools/verify_v49_parity.py docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909/development_v49f_180903001_0.json
python -B docs/model_specs/codex/e19/tools/verify_v49_parity.py docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909/development_v49f_180903001_1.json
python -B docs/model_specs/codex/e19/tools/verify_opening_equivalence_v49f.py
python -B docs/model_specs/codex/e19/tools/verify_artifacts_v49.py
python -B docs/model_specs/codex/e19/tools/build_pass_reduction_v49_report.py v49f
python -B docs/model_specs/codex/e19/tools/verify_report_v49.py
```

I log `scratch/v49/tests.log` (15 test) e `tests_f.log` (2 test) sono registrati
per hash in `integrity.json`. I due nuovi file di test sono
`test_pass_reduction_v49.py` e `test_opening_770_v49f.py` nella directory tests
di e19; i test di regressione preesistenti sono rimasti invariati.

## Limiti del banco di prova

Il timeout delle matrici è `actTimeout=120`. I primi tentativi concorrenti
al timeout standard hanno prodotto azioni assenti: sono esclusi dai confronti
e conservati nei log. I tempi concorrenti e quelli strumentati non certificano
il limite Kaggle. Non è stata eseguita una validazione con avversari esterni
non esposti, né una nuova pubblicazione. La candidata risolve il lavoratore
interamente inattivo di D2; gli altri picchi PASS rimangono aperti.
