# MODEL_SPEC Codex E18.12 — 7-7-0 exact livestock cap

## Ipotesi

Il pool Top-3 equivalente `7-7-0` chiude con 14 pascoli pieni e 14 animali.
E18.10 V2 usa invece un cap risorse pari a 15 per 14 slot e registra una
perdita verificata in ogni match. E18.12 elimina esclusivamente il buffer in
transito: `livestock_resource_cap = pasture_fill_target = 14`.

Worker, routing, ciclo crop, topologia e ordini non animali restano invariati.
La sola mutazione ammessa è il clamp degli ordini `BUY_ANIMAL` oltre la
quattordicesima risorsa COW/SHEEP già su tile, shed, inventario o pianificata.

## Gate

Controllo E18.10 V2, sette seed development, entrambi i seat. Sono richiesti:

- `7-7-0` e fill 14/14 in tutti i match;
- zero perdite verificate, errori, fallback e breach;
- massimo 14 risorse zootecniche osservate;
- nessuna regressione di WATER, lifecycle crop, harvest e MOVE oltre `0,5%`;
- money medio non inferiore e worst matched non sotto `-2%`.

Holdout, final e upload Kaggle restano non autorizzati.

## Esito spot-check — 2026-09-04

Il cap funziona strutturalmente. Nel controllo le risorse COW/SHEEP arrivano a
14 a D12 H2; a D12 H3 il provider statico emette ancora
`BUY_ANIMAL SHEEP 1`. Il buffer ereditato porta il cap a 15 e lascia passare
l'ordine, creando il surplus nello shed. E18.12 blocca quell'acquisto e i
tentativi successivi: tra D19 e D20 mantiene 14 risorse, tutte sui pascoli,
contro 15 del controllo (`14` collocate più `1` nello shed).

La perdita D20→D21 resta però `1`, perché è causata dal mancato FEED del COW
in `(2,4)`. Dopo la perdita E18.12 scende a 13, compra il rimpiazzo e torna a
14 entro D21 H23; per questo money e fill finali dello spot sono identici al
controllo, che aveva comprato il surplus prima e poi lo usa come rimpiazzo.

Decisione aggiornata: il cap 14 è accettato come invariante semantica delle
future `7-7-0`, non come miglioramento standalone. La safety FEED resta una
causa separata da risolvere o misurare nel candidato successivo.
