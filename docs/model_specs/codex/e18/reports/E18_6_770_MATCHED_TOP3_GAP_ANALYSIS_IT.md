# E18.6 — gap analysis 7-7-0 topology-matched

## Verdetto

Tenendo fissa la topologia finale `7-7-0`, il gap di E18.6 non è spiegato
dalla geometria. La candidata emette il `2,9%` di comandi unità in più del
pool Giulio/Jesse equivalente, ma produce `-18,1%` di servizio crop,
`+60,5%` PASS, `+4,1%` move e `-36,7%` unità raccolte. Il problema prioritario
è la conversione del tempo-worker in lifecycle crop locale.

Il confronto esatto contiene 14 profili locali Codex, due replay `7-7-0` di
Giulio e quattro di Jesse. Crop Dusta non presenta nessun `7-7-0` negli otto
profili del corpus congelato ed è quindi escluso, non approssimato con altre
topologie. La leaderboard è stata riverificata: Crop `3035,3`, Giulio
`2976,0`, Jesse `2963,4`.

## Confronto normalizzato

`Produttive normalizzate` significa ogni comando unità diverso da MOVE e
PASS. È la sola tassonomia confrontabile: il KPI locale `productive_actions`
esclude PICKUP/DROP/PLACE, quello dei replay li include. Money locale e score
Kaggle non vengono confrontati.

| KPI | Codex 770 | Giulio 770 | Jesse 770 | Pool 770 | Gap Codex |
|---|---:|---:|---:|---:|---:|
| Profili | 14 | 2 | 4 | 6 | — |
| Comandi unità | 7.519,0 | 7.305,0 | 7.305,0 | 7.305,0 | +2.9% |
| Move | 3.603,8 | 3.435,0 | 3.473,0 | 3.460,3 | +4.1% |
| PASS | 850,1 | 559,0 | 515,0 | 529,7 | +60.5% |
| Produttive normalizzate | 3.065,1 | 3.311,0 | 3.317,0 | 3.315,0 | -7.5% |
| Move/produttive normalizzato | 1,176 | 1,037 | 1,047 | 1,044 | +12.6% |
| Servizio crop | 1.575,1 | 1.921,0 | 1.925,0 | 1.923,7 | -18.1% |
| Altre produttive | 1.490,0 | 1.390,0 | 1.392,0 | 1.391,3 | +7.1% |
| PLANT | 217,0 | 243,0 | 243,0 | 243,0 | -10.7% |
| WATER | 913,0 | 1.168,0 | 1.172,0 | 1.170,7 | -22.0% |
| HARVEST comandati | 388,9 | 467,0 | 467,0 | 467,0 | -16.7% |
| DIG | 56,1 | 43,0 | 43,0 | 43,0 | +30.6% |
| Peak crop | 58,9 | 62,0 | 62,0 | 62,0 | -5.0% |
| Crop tile-days D21–D30 | 459,6 | 515,0 | 515,0 | 515,0 | -10.7% |
| Unwatered/crop D21–D30 | 0,478 | 0,383 | 0,384 | 0,384 | +24.5% |
| Harvest riusciti | 233,6 | 342,0 | 342,0 | 342,0 | -31.7% |
| Unità raccolte | 560,4 | 884,0 | 885,0 | 884,7 | -36.7% |
| Unità/harvest riuscito | 2,398 | 2,585 | 2,588 | 2,587 | -7.3% |
| Unità raccolte/1.000 move | 155,5 | 257,4 | 254,8 | 255,7 | -39.2% |
| Animali finali | 15,0 | 14,0 | 14,0 | 14,0 | +7.1% |

## Cosa fanno gli equivalenti Top-3

Giulio e Jesse condividono praticamente lo stesso schedule: `243` PLANT,
`1.168–1.172` WATER, `467` HARVEST e `43` DIG. Nell'episodio `105398563`
si affrontano direttamente con `7-7-0` entrambi e restano a sole sei azioni
produttive di distanza. Questo rende il pattern più credibile di una media
ottenuta mescolando topologie.

La progressione del pool esatto è:

| Fase | Move | PASS | Produttive | Move/prod. | PLANT | WATER | HARVEST |
|---|---:|---:|---:|---:|---:|---:|---:|
| D1–D10 | 779,0 | 235,7 | 666,3 | 1,169 | 63,0 | 252,0 | 32,0 |
| D11–D20 | 1.327,0 | 172,3 | 1.264,7 | 1,049 | 90,0 | 464,0 | 150,0 |
| D21–D30 | 1.354,3 | 121,7 | 1.384,0 | 0,979 | 90,0 | 454,7 | 285,0 |

Il lifecycle cresce invece di spegnersi: le produttive passano da `666` a
`1.265` e poi `1.384`, mentre i PASS scendono da `236` a `172` e `122`.
Il raccolto medio è Wheat `495,5`, Strawberry
`259,7`, Melon `72,0` e
Carrot `57,5`; Tomato non viene usato in questo
regime esatto.

## Gap causali candidati, in ordine

1. **Tassonomia prima del tuning.** Pubblicare sempre productive locale e
   normalizzata: il vecchio confronto Top-3 sovrastimava il gap perché
   confrontava definizioni diverse.
2. **PASS → servizio crop locale.** Mantenendo invariati topologia, market,
   worker e calendario, assegnare un solo task compatibile nello stesso
   cluster quando il provider produrrebbe PASS. Gate: PASS `≤600`, crop
   service `≥1.800`.
3. **Lifecycle persistente.** Il peak crop è vicino (`-5,0%`), ma i crop
   tile-days tardi sono `-10,7%`, gli harvest riusciti `-31,7%` e il tasso
   late-unwatered `+24,5%`. Servono deadline WATER/HARVEST age-aware e DIG
   soltanto con reimpianto finanziato. Gate: late crop tile-days `≥500`,
   unwatered/crop `≤0,42`, harvest riusciti `≥300`.
4. **Completamento locale delle rotte.** A parità di `7-7-0`, Codex fa
   `+4,1%` move. Dopo il PASS replacement, completare i task fattibili nel
   quadrante prima di un trasferimento. Gate: move `≤3.500`, rapporto
   normalizzato `≤1,10`.
5. **Cap animali esatto.** Portare il cap da 15 a 14: i leader chiudono con
   14 animali, Codex con 15 e una perdita verificata per match.
6. **Tredicesimo worker solo dopo.** I leader arrivano a 13 e Codex a 12,
   ma Codex emette già più comandi totali e molti più PASS. Aggiungere capacità
   prima di correggere lo scheduler rischia di aggiungere inattività; il
   confronto 12-vs-13 deve restare un'ablation separata.

## Limiti

La topologia è controllata, ma gli ambienti non lo sono: Codex gioca localmente
contro E18.2, Giulio e Jesse giocano replay live. Il confronto identifica gap
e ipotesi, non stima l'effetto causale di una modifica. Il prossimo esperimento
deve cambiare una sola priorità alla volta sulla nostra `7-7-0`, usando gli
stessi seed e seat del gate E18.6.
