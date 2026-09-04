# MODEL_SPEC Codex E18.15 — 7-7-0 extra Q2 WATER hand

## Ipotesi

Nel benchmark exact `7-7-0` i top raggiungono 13 hands contro i 12 di Codex,
ma l'hiring aggiuntivo ha senso soltanto se il lavoro è già definito. E18.15
lascia integralmente a E18.10 V2 il farmer e i primi 12 hands; tra D15 e D19
aggiunge al massimo il tredicesimo hire giornaliero e assegna soltanto quel
worker a WATER sui crop vivi e secchi di Q2.

Il worker extra usa un target sticky, preferisce stress già accumulato e poi
distanza Manhattan, non attraversa altri quadranti, non esegue DIG/PLANT/
HARVEST e non modifica alcun comando dei worker provider. L'unica mutazione
market è un HIRE addizionale, con cash floor 3.000.

## Gate

Controllo E18.10 V2 sui sette seed development e due seat. Oltre a topologia
e fill `7-7-0` esatti, sono richiesti 13 hands osservati, zero override dei
worker provider/errori/fallback/breach, WATER almeno `+2%`, late unwatered per
crop almeno `-3%`, crop service almeno `+1%`, harvest non inferiore, MOVE
totali non oltre `+5%`, money medio non inferiore e worst matched almeno
`-5%`.

Holdout, final-confirmation e upload Kaggle restano non autorizzati.

## Esito pre-gate — 2026-09-04

La finestra finale D15–D19 sul seed development `180903001` produce 5 hire e
25 WATER del worker extra. Rispetto al controllo: WATER `946` contro `925`
(`+21`), crop service `1598` contro `1577`, MOVE `3659` contro `3602` e PASS
`881` contro `849`. Harvest (`243`), unità (`579`) e late unwatered (`0,4617`)
restano identici. Money scende da `87.834` a `86.669`: `-1.165`, esattamente
il costo dei cinque hire.

Il tredicesimo worker aumenta WATER senza creare output e sposta lavoro che il
provider avrebbe comunque completato. Variante respinta al pre-gate; matrice
completa non eseguita. Il gap WATER dei top va trattato come effetto di un
calendario crop e di rotte migliori, non come leva autonoma da sovrapporre.
