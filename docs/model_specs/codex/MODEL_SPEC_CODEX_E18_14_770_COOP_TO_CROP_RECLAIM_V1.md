# MODEL_SPEC Codex E18.14 — 7-7-0 coop-to-crop reclaim

## Ipotesi

Il benchmark a topologia equivalente mostra che Giulio Ravasio e Jesse
Bullard chiudono con 14 animali, mentre E18.10 V2 chiude con 15: i 14 animali
da pascolo più l'oca nel coop. I leader raggiungono inoltre 62 crop di picco
contro circa 59, eseguono meno lavoro non-crop e più WATER/HARVEST.

E18.14 elimina esclusivamente il modulo coop/oca della routine V9 e riusa la
cella `(4,1)` come crop Strawberry. `BUILD_COOP` diventa `PLANT STRAWBERRY`
in-place quando il seed è già disponibile; l'ordine di acquisto dell'oca è
rimosso e i successivi PICKUP/PLACE oca non più eseguibili diventano PASS.
La cella entra poi nel ciclo WATER/HARVEST e nella protezione no-DIG di E18.10
V2. Nessun MOVE, worker, pascolo, cap COW/SHEEP o altra regola market cambia.

## Gate

Controllo E18.10 V2, sette seed development e due seat. Sono richiesti
topologia e fill `7-7-0` esatti, zero coop/oche finali, 14 animali finali,
attivazione una volta per match, zero override MOVE/errori/fallback/breach,
WATER e crop service almeno `+1%`, harvest non inferiore, money medio non
inferiore, worst matched almeno `-2%` e MOVE non oltre `+0,5%`.

Holdout, final-confirmation e upload Kaggle restano non autorizzati.

## Esito pre-gate — 2026-09-04

Sul seed development `180903001` la variante ottiene WATER `944` contro
`925` (`+2,05%`), crop service `1604` contro `1578` (`+1,65%`) e MOVE `3589`
contro `3603` (`-0,39%`). Tuttavia money scende da `89.841` a `87.196`
(`-2,94%`), PASS sale di 30 e il raccolto cresce soltanto da 580 a 582 unità.

Il meccanismo porta correttamente gli animali finali da 15 a 14, ma il lavoro
liberato dall'oca non viene ripianificato e il crop aggiuntivo non ripaga
l'economia rimossa. Variante respinta al pre-gate; matrice completa non
eseguita.
