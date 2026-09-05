# MODEL_SPEC Codex E18.10 — 7-7-0 WATER-before-DIG guard

## Variabile causale

Controllo: E18.9, stessa topologia e fill `7-7-0`. E18.10 modifica soltanto
il trattamento di un crop vivo nei cinque target reclaimed durante la finestra
di rotazione D20–D23:

- se E18.6 avrebbe richiesto DIG e il crop è unwatered, emette WATER sul tile
  corrente;
- se il crop è già watered, sopprime DIG come E18.9;
- HARVEST e DIG delle weed restano invariati.

Non sono ammessi routing, override di comandi provider non locali, variazioni
di market, worker, cap animali o topologia.

## Ipotesi

E18.9 ha prodotto il primo segnale positivo: late crop tile-days `+4,93%`,
harvest `+2,33%`, unità `+2,78%`, money `+0,48%`. Il suo lieve peggioramento
unwatered (`+0,41%`) suggerisce che il crop preservato debba ricevere WATER
invece di restare inattivo quando il DIG viene bloccato.

## Gate preregistrato

Quattordici match development, sette seed, entrambi i seat, E18.10 contro
E18.9:

- esatta `7-7-0` piena 14/14, zero errori/fallback/breach;
- conversione DIG→WATER attiva in tutti i match, zero route mutation e
  override provider;
- WATER e crop service almeno `+1%`, PASS almeno `-1%`;
- late unwatered/crop almeno `-2%`;
- harvest riusciti e unità raccolte almeno `+1%`;
- late crop tile-days non inferiori al controllo, DIG non superiori;
- move non oltre `+1%`, money medio non peggiore oltre `2%`, peggior matched
  delta almeno `-5%`, perdite animali non superiori al controllo.

Gate B Top-3 resta diagnostico: PASS `<=600`, crop service `>=1.800`, move
`<=3.500`, ratio `<=1,10`, late crop tile-days `>=500`, unwatered/crop
`<=0,42`, harvest riusciti `>=300`.

Holdout, final e upload restano non autorizzati.

## Esito V1 — invalidata dal safety gate

La matrice ha rivelato che la conversione inserita nella task queue poteva
sostituire un comando provider non-PASS sul target `(4,5)`, che è anche un
accesso al magazzino. La candidata chiudeva con un pascolo Q0 vuoto e tre
perdite verificate per match (`0/14` fill esatti), quindi V1 è `INVALID` e
respinta indipendentemente dai KPI crop favorevoli. La V2 sposta il WATER a
valle del provider e consente esclusivamente `PASS→WATER` in-place.
