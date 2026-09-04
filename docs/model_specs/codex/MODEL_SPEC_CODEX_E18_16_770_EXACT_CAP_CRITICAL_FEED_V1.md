# MODEL_SPEC Codex E18.16 — 7-7-0 exact cap + critical FEED

## Ipotesi

Il difetto zootecnico osservato ha due metà collegate. Il controller ammette
15 risorse COW/SHEEP per 14 pascoli e compra il quindicesimo animale a D12 H3;
poi, al confine D20→D21, perde un COW non alimentato e usa il surplus come
rimpiazzo. E18.12 dimostra che il cap 14 sopprime l'acquisto ma non la morte;
E18.13 dimostra che il FEED sopprime la morte ma lascia il surplus e fallisce
la coda economica standalone.

E18.16 combina esclusivamente i due lati della stessa invariante: massimo 14
risorse COW/SHEEP e un solo MOVE D20 ritardato per FEED in-place sul pascolo
critico, quando il worker ha già Wheat. Nessuna altra rotta, azione market,
worker o regola crop cambia.

## Gate preregistrato

Controllo E18.10 V2, sette seed development e due seat. Sono richiesti:

- topologia e fill finali `7-7-0` esatti in 14/14;
- massimo 14 risorse COW/SHEEP osservate e almeno un ordine clampato per match;
- un solo override FEED e zero perdite/errori/fallback/breach per match;
- nessuna mutazione oltre al clamp `BUY_ANIMAL` e al singolo FEED;
- money medio non inferiore e worst matched almeno `-2%`;
- MOVE non oltre `+0,5%` e KPI crop non peggiori di `0,5%`.

Gate B conserva i target assoluti Top-3. Holdout, final-confirmation e upload
Kaggle restano bloccati.

## Esito development gate — 2026-09-04

Gate A passa integralmente; Gate B Top-3 fallisce. In 14/14 match E18.16 non
supera mai 14 risorse, attiva il clamp e il singolo FEED, conserva fill e
topologia esatti e registra zero perdite contro le 14 del controllo.

Money medio `65.817,07` contro `65.049,21` (`+1,18%`), matched `+0,67%`, worst
matched `-0,95%`, record `8–6`. MOVE `+0,13%`, PASS `-0,20%`, WATER `+0,11%`,
late unwatered `-0,82%` e unità `+0,19%`. Il cap 14 elimina quindi la coda
negativa del solo FEED e viene acquisito insieme alla safety D20 come nuova
base di ricerca `7-7-0`. Nessuna promozione o azione Kaggle è autorizzata.
