# MODEL_SPEC Codex E18.8 — 7-7-0 adjacent crop queue

## Identità e controllo

- candidata: `CODEX_E18_8_770_ADJACENT_CROP_QUEUE_V1`;
- controllo: E18.6, stessa topologia e fill `7-7-0`;
- evidenza causale precedente: E18.7 ha trovato soltanto due WATER in-place
  per episodio, senza effetto su harvest, move o money;
- ruolo: development-only, nessun upload Kaggle.

## Unica mutazione

Un worker per quadrante e turno può sostituire esclusivamente un provider
`PASS` con un servizio crop immediato o con un singolo passo verso un crop
adiacente nello stesso quadrante. La missione dura al massimo fino al servizio
successivo ed è cancellata appena il provider riprende il worker con un comando
non-PASS. Sono ammessi solo HARVEST e WATER su crop esistenti.

Restano congelati topologia, fill, market, calendario crop, 12 worker, cap
animali 15, PLANT, DIG e tutti i comandi provider non-PASS. Sono vietati routing
cross-quadrant e assegnazioni oltre distanza Manhattan 1.

## Gate preregistrato

Quattordici match development, sette seed, entrambi i seat, E18.8 contro E18.6.
Gate A causale:

- `7-7-0` piena in 14/14 per entrambi, zero errori/fallback/breach;
- trattamento attivo in tutti i match, zero override non-PASS e cross-quadrant,
  distanza massima osservata `<=1`;
- PASS almeno `-5%`, crop service almeno `+5%`, productive normalizzate almeno
  `+3%`;
- move non oltre `+3%`, move/productive normalizzato non peggiore del controllo;
- harvest riusciti e unità raccolte almeno `+5%`, late unwatered/crop almeno
  `-5%`;
- money medio non peggiore oltre `5%`, peggior matched delta almeno `-10%`,
  perdite animali non superiori al controllo.

Gate B Top-3 resta diagnostico: PASS `<=600`, crop service `>=1.800`, move
`<=3.500`, rapporto normalizzato `<=1,10`, late crop tile-days `>=500`,
unwatered/crop `<=0,42`, harvest riusciti `>=300`.

Holdout, final e upload restano non autorizzati.

## Esito development — 2026-09-04

Gate A `FAIL`, Gate B `FAIL`; record `0–14`. PASS cala `852,64→705,50` e il
late unwatered rate migliora `0,4783→0,4393`, ma `1.132/1.372` missioni sono
cancellate dal provider. Move sale `+2,50%`, harvest riusciti scendono
`233,14→158,64`, unità raccolte `559,64→400,86`, money matched medio `-15,59%`
(worst `-24,12%`). La coda adiacente è respinta: anche un passo locale rompe
la continuità delle traiettorie ad alto valore.
