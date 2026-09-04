# MODEL_SPEC Codex E18.7 — 7-7-0 in-place crop service

## Identità

- candidate: `CODEX_E18_7_770_IN_PLACE_CROP_SERVICE_V1`;
- controllo: E18.6 `7-7-0`, non E18.2 `7-7-5`;
- ruolo: prima ablation topology-matched derivata dal confronto Giulio/Jesse;
- stato iniziale: development-only, nessun upload Kaggle.

## Variabile causale

La candidata sostituisce soltanto un comando provider `PASS` quando lo stesso
worker può eseguire immediatamente `HARVEST` o `WATER` sulla cella corrente.
È ammesso al massimo un override per quadrante e turno. Un HARVEST richiede
inventario vuoto; WATER è disabilitato nella fase terminale.

Restano congelati:

- topologia e fill `7-7-0`;
- market, calendario crop e 12 worker della E18.6;
- cap animali 15, incluso il difetto noto, per non introdurre una seconda
  variabile;
- ogni comando provider diverso da PASS;
- PLANT, DIG e qualsiasi movimento o routing cross-quadrant.

## Ipotesi

Il confronto topology-matched mostra che E18.6 emette più comandi totali del
pool Giulio/Jesse ma ha `+60,5%` PASS e `-18,1%` crop service. Un override
in-place può convertire inattività in servizio senza aggiungere move. Questa
V1 verifica il meccanismo più stretto; non cerca ancora di replicare l'intero
schedule dei leader.

## Gate preregistrato

Quattordici match development, sette seed, entrambi i seat, E18.7 contro
E18.6. Gate A causale:

- `7-7-0` esatta e fill 14/14 in 14/14 per entrambi;
- zero errori, fallback, breach, override non-PASS, route cross-quadrant e
  service distance maggiore di zero;
- perdite animali non superiori al controllo congelato;
- PASS almeno `-5%`, crop service almeno `+5%`, productive normalizzate almeno
  `+3%`;
- move non oltre `+1%` e move/productive normalizzato almeno `-3%`;
- harvest riusciti e unità raccolte almeno `+5%`;
- late unwatered/crop almeno `-5%`;
- money medio non peggiore oltre `5%`, nessun matched delta sotto `-10%`.

Gate B di convergenza Top-3, solo diagnostico in V1: PASS `≤600`, crop service
`≥1.800`, move `≤3.500`, rapporto normalizzato `≤1,10`, late crop tile-days
`≥500`, unwatered/crop `≤0,42`, harvest riusciti `≥300`.

Holdout, final e upload restano non autorizzati anche in caso di Gate A
positivo. La modifica successiva dipende dall'esito: lifecycle persistente
solo dopo un segnale causale sul PASS replacement.

## Esito development — 2026-09-04

Gate A `FAIL`, Gate B `FAIL`. La candidata ha sostituito esattamente due PASS
con due WATER in ogni episodio: PASS `846,93→844,93`, crop service
`1.574,93→1.576,93`. Move, harvest, unità raccolte, late unwatered e money sono
rimasti invariati. Il meccanismo è sicuro ma troppo stretto: l'inattività non è
spiegata da worker già posizionati su crop azionabili.

## Asset

- source:
  `src/agricola/strategy/codex/codex_e18_770_in_place_crop_service.py`;
- config:
  `docs/model_specs/codex/e18/configs/CODEX_E18_7_770_IN_PLACE_CROP_SERVICE_V1.json`;
- test:
  `docs/model_specs/codex/e18/tests/test_codex_e18_770_in_place_crop_service.py`.
