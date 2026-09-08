# V48: pianificazione, produzione e priorità PASS

Checkpoint 2026-09-08. Riferimento pubblicato: submission Kaggle **56101593**,
`submission/submission_codex_e18_770_v48_external.py`.
SHA-256: `57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`.
La policy rimane congelata. La prossima versione deve affrontare prima di tutto
il disallineamento tra capacità della manodopera e lavoro biologico eseguibile.
Ambito: **770**; 662 e altre topologie restano rinviate.

## Evidenza e limiti

Nei casi locali V48, D15–D25: PASS medi 28,79 e MOVE 150,24; nel nuovo corpus
Subin di cinque replay: PASS 6,91 e MOVE 111. Il corpus Subin comprende quattro
770 e un 10-7-0: non è un confronto causale a parità di partita o topologia.
Le medie non spiegano da sole i picchi. Il difetto PASS non è risolto.
V48 locale: 6/6 vittorie su V4D, seed di sviluppo già riutilizzati.
Prima coorte esterna congelata: 5/8 vittorie, rating osservato 822,1; non prova
superiorità rispetto a V29. Rating e numero di replay non sono aggiornati in tempo reale.

Il registro `experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md`
è obbligatorio: tutti i dodici nuovi autori sono esposti; Top770-003 è consumato
nel ciclo V48. Non usare questi replay come holdout della prossima versione.

## Prossima versione: piano di lavoro e gate

1. Ricostruire ogni PASS per persona, giorno e ora, iniziando da D12–D13 e
   dai picchi successivi. Registrare posizione, capacità residua, assegnazione,
   lavori biologici dovuti, candidati scartati e motivo del vincolo.
2. Distinguere attesa biologica senza lavoro utile, sovracapacità assunta,
   lavoro utile irraggiungibile entro la scadenza, risorse mancanti, prenotazioni
   o priorità che bloccano un lavoro fattibile. Finché non c'è prova, causa ignota.
3. Collegare il calendario semina–maturazione–raccolta–successione alle ore
   necessarie di WATER, FEED, CARE, raccolta e trasferimento. Dimensionare le
   persone prima dell'espansione; verificare carico previsto e realizzato.
4. Proteggere continuità delle colture, rese, servizi animali, cassa e scadenze;
   assegnare lavoro locale utile prima del PASS. La casualità non sostituisce
   un piano fattibile. Non abbassare PASS producendo MOVE o WATER inutili.
5. Confrontare contro V48 congelata con stessi seed/posti per la diagnosi,
   poi seed nuovi e avversari non esposti per la validazione. Riportare PASS
   assoluti, quota sulle azioni, per persona, per causa, picchi e fasi del mese.
   La promozione richiede riduzione dei PASS evitabili senza regressioni
   sistematiche di cassa, perdite biologiche e copertura dei servizi.

Questo è un protocollo da implementare e verificare, non una correzione già validata.

## Catena effettiva del runtime

Il builder parte da `daily_route_scheduler_770_v48.py`, visita le dipendenze
ImportFrom e incorpora 16 moduli più due sorgenti base. Non tutti i file V18–V47
presenti nella directory sono dipendenze della submission V48.

- `biological_plan_770_v48.py`: piano biologico.
- `daily_routes_770_v48.py`: lavori e percorsi giornalieri.
- `daily_route_dispatch_770_v48.py`: esecuzione e guardie.
- `daily_route_scheduler_770_v48.py`: inserimento dei lavori nel piano.
- `portfolio_workforce_v16.py` e `portfolio_scheduler_v16.py`: manodopera e scheduling ereditati.
- Moduli portfolio V14: successione, esecuzione, governo, batch, concorrenza,
  logistica, piano giornaliero, limiti e chiusura; `productive_continuity.py`.
- Core parametrico `submission_codex_e19_control_770_v2.py` e avvio assistito
  `submission_codex_e18_770_assisted_start_v1_candidate.py`.

Elenco completo, verificato contro il manifest della pubblicazione:

| Sorgente dalla radice repository | SHA-256 |
|---|---|
| `docs/model_specs/codex/e19/tools/productive_continuity.py` | `889c65462c4e71af75f181480f9cdb39eec91a0bb59c6cf85d0e6c9175388dc7` |
| `docs/model_specs/codex/e19/tools/portfolio_succession_v14.py` | `d2dd5c455278f8d125a5817b1d5050910578a12c4aa24efe3ede90574a58f111` |
| `docs/model_specs/codex/e19/tools/portfolio_execution_v14.py` | `45ad7773338f40bcd32295876055c3927b80bee18ca660af907f72f0cad01dab` |
| `docs/model_specs/codex/e19/tools/portfolio_governed_v14.py` | `5c0e68f232607ae119de49557e6ebceb224a7f664974941423bb61e2a78bba18` |
| `docs/model_specs/codex/e19/tools/portfolio_batched_v14.py` | `d59f8255d7beff846a6d9987c5d262df4f56d714add658ae0a557b722abba403` |
| `docs/model_specs/codex/e19/tools/portfolio_concurrent_v14.py` | `856cedecc6252fbeaba0e1dfa5e274347ac4d6f19b1dbae7a801304ec2c7bb7a` |
| `docs/model_specs/codex/e19/tools/portfolio_logistics_v14.py` | `12841c3a2dbb013797af066e7dc3d3aff64823e3a545b1ac6bee22e80ca1b556` |
| `docs/model_specs/codex/e19/tools/portfolio_day_plan_v14.py` | `1ab3b77847f1c781e3942c720026d755c32f7feb3cda70cdaa0149fbcfa3aada` |
| `docs/model_specs/codex/e19/tools/portfolio_bounded_v14.py` | `fdcc78cd7c650ea66b4d790dd8a01d895e7b86911b3c77e8be62f4b0ef2f67ff` |
| `docs/model_specs/codex/e19/tools/portfolio_terminal_v14.py` | `a5ec6d9237b512e62450a8820f77bd598f64e7286c0a3782d7fea98958a206cf` |
| `docs/model_specs/codex/e19/tools/portfolio_workforce_v16.py` | `d8cf5a78e02bae2c2f21f2ed0e13626ce3b7744f0e8d342d1c2587782a90b7db` |
| `docs/model_specs/codex/e19/tools/portfolio_scheduler_v16.py` | `2f06605fab1b3b0893b2b24fe3e9f0ed131439f2cbf3802d80d57b5a69d214f1` |
| `docs/model_specs/codex/e19/tools/biological_plan_770_v48.py` | `8b324aaee858c95ae42340e1f988794859d9b15d5264c8df2a54672d445710ac` |
| `docs/model_specs/codex/e19/tools/daily_routes_770_v48.py` | `5dad34caa1efa934b94016580c44ce067e67cca9c5f19e9d721138f0f6c94d53` |
| `docs/model_specs/codex/e19/tools/daily_route_dispatch_770_v48.py` | `540456d66df0d5d6abc314499b64dfdfbea22121a99eacf14747b4229fbcc28a` |
| `docs/model_specs/codex/e19/tools/daily_route_scheduler_770_v48.py` | `15945f5bb4d03e23bc01c1336d13c2271a9894a138b06489ed907d943590dce0` |
| `submission/submission_codex_e19_control_770_v2.py` | `73d27802df67901afdf71c7f27230b1527b9a145557340274238285db6a033ef` |
| `submission/submission_codex_e18_770_assisted_start_v1_candidate.py` | `23d997e76b521f173e1972e79b763e0428b95f1076c08c32a234f51c53fad4a5` |

## Produzione, test e analisi

Percorsi tools seguenti relativi a `docs/model_specs/codex/e19/tools/`.

| Passo | File / input |
|---|---|
| Bundle standalone | `build_v48_submission.py` |
| Benchmark locale congelato | `run_daily_routes_770_v48.py` |
| Parità standalone | `run_v48_external_parity.py` |
| Audit biologico | `crop_lifecycle_audit_v48.py`, `run_lifecycle_audit_v48.py` |
| Diagnosi acqua residua | `run_residual_water_diagnostic_v48.py` |
| Report confronto versioni | `build_productive_water_770_report.py` |
| KPI condivisi | `build_assisted_complete_kpi.py`, `complete_kpi_template.html`, `build_succession_routes_770_report.py` |
| Nuovi Top | `analyze_new_top_v48.py`, `summarize_new_top_v48.py`, `build_new_top_v48_report.py` |
| Coorti Top | `../artifacts/derived/new_top_cohorts.json` |
| Test | `docs/model_specs/codex/e19/tests/test_productive_water_v48.py`, `tests/test_crop_lifecycle_audit_v48.py` dalla radice |

Gli audit Top dipendono anche da
`docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py`,
`build_e18_26_jesse_770_d30_closure.py` nella stessa directory e
`experiments/e18/tools/common/replay_daily_operational_kpi.py`.
Il generatore KPI storico E18 è `docs/model_specs/codex/e18/tools/build_e18_27_top770_complete_kpi.py`.

Eseguire dalla radice con `.venv/Scripts/python.exe`, nell'ordine analizzatore,
riepilogo fasi, builder report per rigenerare l'analisi Top. I replay grezzi
e i run locali devono essere disponibili: un clone Git da solo non li contiene.
Per il bundle usare il builder e verificare l'hash pubblicato; la ricevuta di
pubblicazione è separata dal build e non autorizza una nuova submission.

## Provenance e conservazione

Manifest e ricevuta: `docs/model_specs/codex/e19/artifacts/derived/`
`v48_external_manifest.json`, `v48_external_publication_receipt.json`.
Prima coorte: `v48_external_20260908/first_cohort.json` nella stessa directory.
Analisi Top: `docs/model_specs/codex/e19/reports/new_top_v48_20260908/`:
`census.json`, `profiles.json`, `cohorts.json`, `phase_summary.json`, `manifest.json`
e quattro report completi D01–D30.
L'inventario `docs/foundation/evidence/LOCAL_ARTIFACTS_20260908.json` elenca i
file voluminosi conservati localmente, con hash e dimensione. Per trasferire
gli esperimenti a un altro computer occorre trasferire anche tali file.
Le ricette originarie sono archiviate in `tools/session_archive_20260908/`.

## Semantica dei KPI biologici

L'audit V48 distingue 20 eventi con prodotto detenuto o produzione futura
da due eventi su fragola esaurita e vuota dopo l'ultima raccolta. Irrigare
quest'ultima avrebbe soltanto rinviato WEED: non è un recupero produttivo.
I vecchi conteggi di mortalità non riclassificati non sono direttamente
comparabili. Separare piante presenti, produttive, esaurite, stock perso,
infestanti e servizio necessario. Il numero di WATER da solo non misura copertura.
