# MODEL_SPEC Codex E18.9 — 7-7-0 live-crop rotation guard

## Ipotesi causale

Il confronto exact-770 mostra rispetto a Giulio/Jesse: DIG `+30,6%`, late crop
tile-days `-10,7%`, harvest riusciti `-31,7%`. E18.8 ha inoltre dimostrato che
aggiungere routing ai PASS rompe le missioni del provider. E18.9 non muove
worker: sopprime soltanto il DIG calendarizzato nei giorni 20–23 quando uno dei
cinque target reclaimed contiene ancora un crop vivo.

HARVEST, WATER e DIG delle weed restano invariati. Restano congelati topologia
e fill `7-7-0`, market E18.6 (incluso il batch Wheat), worker 12, cap animali 15
e tutte le traiettorie del provider.

## Gate preregistrato

Quattordici match development, sette seed, entrambi i seat, E18.9 contro E18.6:

- esatta `7-7-0` piena 14/14 per entrambi; zero errori/fallback/breach;
- guard attiva in tutti i match, zero route mutation e override provider;
- DIG almeno `-10%`, late crop tile-days almeno `+5%`;
- harvest riusciti e unità raccolte almeno `+5%`;
- move non oltre `+1%`, PASS non oltre `+1%`, late unwatered non peggiore oltre
  `2%`;
- money medio non peggiore oltre `3%`, peggior matched delta almeno `-7,5%`;
- perdite animali non superiori al controllo.

Gate B Top-3 è soltanto diagnostico: PASS `<=600`, crop service `>=1.800`, move
`<=3.500`, ratio `<=1,10`, late crop tile-days `>=500`, unwatered/crop `<=0,42`,
harvest riusciti `>=300`.

Holdout, final e upload restano non autorizzati.

## Esito development — 2026-09-04

Gate A `FAIL` per soglie quantitative non raggiunte, Gate B `FAIL`; nessuna
promozione. Il segnale è però positivo e stabile: record `10–4`, money medio
`+0,48%`, worst matched `-0,95%`, DIG `-5,47%`, late crop tile-days `+4,93%`,
harvest riusciti `+2,33%`, unità raccolte `+2,78%`. Move `+0,21%` e late
unwatered `+0,41%` restano quasi neutri. È la migliore candidata di ricerca
770 corrente; il passo successivo deve trasformare il DIG protetto in WATER
in-place quando necessario, senza introdurre routing.
