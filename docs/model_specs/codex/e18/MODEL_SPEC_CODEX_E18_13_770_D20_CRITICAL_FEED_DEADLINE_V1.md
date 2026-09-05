# MODEL_SPEC Codex E18.13 — 7-7-0 D20 critical FEED deadline

## Ipotesi

La perdita verificata di E18.10 V2 non dipende dal cap 15. Nel seed
development tracciato, il COW `(2,4)` chiude D20 non alimentato e muore al
confine D20→D21. Il worker 7 raggiunge `(2,4)` all'ora 20 con un Wheat, ma il
provider lo fa ripartire `EAST` senza eseguire FEED.

E18.13 modifica soltanto quel tipo di stato, senza codificare worker o tile:
D20, ora almeno 20, worker già su COW/SHEEP non alimentato con
`consecutive_unfed>=1`, Wheat portato e comando finale MOVE. Il MOVE viene
ritardato di un turno e sostituito da FEED in-place. Nessuna nuova rotta,
market, cap, worker o regola crop è ammessa.

## Gate

Controllo E18.10 V2 sui sette seed development e i due seat. Sono richiesti
attivazione esattamente una volta per match, zero perdite/errori/fallback,
fill/topologia `7-7-0` esatti, FEED non inferiore, MOVE non oltre `+0,5%`, crop
lifecycle non peggiore di `0,5%`, money medio non inferiore e worst matched
almeno `-2%`.

Holdout, final e upload Kaggle restano bloccati.

## Esito development gate — 2026-09-04

La correzione elimina tutte le perdite (`0` contro `14`) con un solo override
per match e conserva fill/topologia esatti. Le medie sono favorevoli: money
`+0,33%`, WATER `+0,11%`, crop service `+0,07%`, late unwatered `-0,82%` e
unità `+0,19%`; MOVE aumenta di `+0,13%`.

Gate A fallisce però il vincolo di coda: record `6–8`, delta money matched
medio `-0,37%` e peggiore `-2,85%`. La rotta recupera il ritardo entro D21 H1;
la diagnosi successiva mostra che la coda negativa deriva soprattutto dal
preservare anche il quindicesimo animale di buffer nello shed, non da un
ritardo persistente. E18.16, applicando cap 14 insieme allo stesso FEED, porta
il worst a `-0,95%` e passa Gate A. E18.13 resta respinta standalone.
