# MODEL_SPEC Codex E18.5 — ablation topologica 6-6-2

## Identità

- candidate: `CODEX_E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1`;
- base: `CODEX-E18.4-STATE-DRIVEN-772-V2`;
- ruolo: development-only, nessun upload Kaggle;
- unica variabile causale: topologia pasture `7-7-2 → 6-6-2` e cap `16 → 14`.

## Mutazione isolata

Vengono rimossi soltanto i target canonici `(3,2)` in Q0 e `(6,2)` in Q1.
Dispatcher locality/task-aging, ownership, carrier affinity, task generation,
Wheat reserve, crop targets, market ledger, harvest batching e liquidazione
restano invariati. Le due celle liberate non vengono convertite a crop in
questa ablation, per non confondere la misura di efficienza delle move.

Poiché il bootstrap E18.2 costruisce già tutti i quattordici pasture Q0/Q1
entro D10, la candidata applica durante il bootstrap un veto esclusivamente a
`BUILD_PASTURE` quando il worker è su `(3,2)` o `(6,2)`. Tutti gli altri
comandi bootstrap restano passthrough. Il veto è la minima mutazione necessaria
per rendere reale — e non soltanto dichiarativa — la topologia 6-6-2.

## Ipotesi

Ridurre di due i pasture target diminuisce la dispersione spaziale e il carico
FEED/CARE senza annullare il lavoro produttivo. La 6-6-2 è utile soltanto se il
guadagno non deriva da worker semplicemente inattivi.

## Gate primario — 14 match development, entrambi i seat

La 6-6-2 gioca contro E18.2 sugli stessi sette seed e seat del gate V2. Il
riferimento 7-7-2 è l'artifact congelato prodotto contro il medesimo E18.2;
questo evita di mettere due dispatcher V2 nello stesso episodio e mantiene
comune l'avversario economico:

- move medie almeno `5%` inferiori;
- move/productive almeno `5%` inferiore;
- productive action almeno `90%` della 7-7-2;
- topologia esatta 6-6-2 e fill 14/14 in 14/14;
- zero PASS su tile azionabile, route thrashing, errori, fallback e perdite;
- money, harvest e late weeds registrati ma non usati per compensare un fail
  del gate di efficienza.

Holdout e final restano non consumati. Un eventuale pass autorizza soltanto
una seconda analisi economica development, non una submission.

## Esito development

Il gate fallisce sui due criteri primari di efficienza. Nei 14 match la 6-6-2
registra `4.451,86` move contro `4.477,43` della 7-7-2 (`-0,57%`) e rapporto
move/productive `2,0026` contro `2,0192` (`-0,82%`): entrambi i delta sono
favorevoli, ma lontani dalla soglia `-5%`. Le productive action aumentano
leggermente (`2.223,07` contro `2.217,43`, `+0,25%`).

L'integrità passa integralmente: topologia esatta e fill 14/14 in 14/14,
zero PASS azionabili, thrashing, errori, fallback e perdite. Come osservazione
secondaria, money migliora del `4,09%`, harvest del `8,59%` e late weeds cala
del `40,08%`; tuttavia la candidata resta `0-14` contro E18.2. Decisione:
`REJECTED_AT_EFFICIENCY_GATE`, nessun holdout, final o upload.

## Verifica esterna successiva sul Top 3 corrente

L'analisi osservazionale del 2026-09-04 su 11 head-to-head recenti fra Crop
Dusta, Giulio Ravasio e Top770 conferma che il fallimento non è
risolvibile con un'altra riduzione geometrica. I leader registrano
`1,0099–1,2569` move/productive contro `2,0026` di E18.5, circa
`3.237–3.377` azioni produttive contro `2.223` e `887–917` unità raccolte
contro `513`.

Le topologie non convergono: Giulio e Top770 tengono sempre zero pasture in Q2,
mentre Crop Dusta — primo stabile — usa Q2 in 6/8 profili e sette geometrie
diverse. La conclusione congelata resta quindi valida ma più precisa: la
`6-6-2` produce un segnale favorevole non materiale; il vincolo dominante è
il throughput del ciclo colturale. La prossima linea raccomandata riparte da
E18.2/V4D con un lifecycle phase controller, non da questo dispatcher.

Report comune:
`experiments/e18/reports/common/E18_CURRENT_TOP3_STRATEGY_RECONSTRUCTION_2026_09_04_IT.md`.

## Asset

- source: `src/agricola/strategy/codex/codex_e18_state_driven_662_ablation.py`;
- config: `docs/model_specs/codex/e18/configs/CODEX_E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.json`;
- test: `docs/model_specs/codex/e18/tests/test_codex_e18_state_driven_662_ablation.py`;
- runner: `docs/model_specs/codex/e18/tools/run_e18_5_state_driven_662_ablation.py`;
- artifact: `docs/model_specs/codex/e18/artifacts/derived/E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_V1.json`;
- report: `docs/model_specs/codex/e18/reports/E18_5_STATE_DRIVEN_662_TOPOLOGY_ABLATION_REPORT_IT.md`.
