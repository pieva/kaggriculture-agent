# Top770 770 / E18.26 — traiettorie e valorizzazione D1-D30

Coorte invariata: Top770 105405557, 105384058, 105398563, 105391568, 105565293; E18.26 BoostD10 contro E18.16, seed development 180903001, entrambi i seat. Topologia finale pasture 7-7-0; nessuna policy modificata.

## Metodo e verifiche

30 checkpoint H24 per profilo (indice 24 × D − 1). Cassa = farm.money; a D30 coincide esattamente con il reward. Personale = hands assunti + farmer, inclusi gli agenti fuori griglia. Campioni, hash, reward e dati D1-D20 coincidono con il confronto congelato.

Ogni batch registrato è rieseguito su una copia dello stato precedente: azioni unità, poi mercato simultaneo dei due giocatori. Sono stati verificati 719 batch per profilo, 5.033 batch complessivi e 10.066 saldi di cassa, senza scarti. Vendite e acquisti sono fill effettivi, non richieste. I flussi per giornata sono attribuiti al giorno prima dell'azione: il confine differisce di un'azione rispetto ai checkpoint H24.

Linee = mediane per checkpoint; fasce = minimo–massimo osservato, non intervalli di confidenza. La mediana può cambiare episodio lungo la curva. Il pubblico e il locale hanno seed, avversari e prezzi diversi: il confronto economico è descrittivo, non un effetto causale.

## Cassa e consistenze

Nelle coppie il primo dato è E18.26, il secondo Top770. Le parentesi riportano il range osservato.

| D | Cassa noi / Top770 | Persone | Crop totali | Strawberry | Wheat | Carrot | Pascoli vuoti |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 52 / 74 [74–75] | 6 / 6 | 19 / 19 | 0 / 0 | 7 / 7 | 0 / 0 | 0 / 0 |
| 2 | 303 / 261 [260–263] | 5 / 5 | 19 / 19 | 0 / 0 | 7 / 7 | 0 / 0 | 0 / 2 |
| 3 | 507 / 125 [124–126] | 5 / 5 | 19 / 19 | 0 / 0 | 7 / 7 | 0 / 0 | 0 / 1 |
| 4 | 40 / 150 [150–153] | 6 / 6 | 19 / 19 | 0 / 0 | 7 / 7 | 0 / 0 | 0 / 1 |
| 5 | 66 / 891 [891–901] | 6 / 5 | 19 / 19 | 0 / 0 | 7 / 7 | 0 / 0 | 0 / 0 |
| 6 | 305 / 999 [999–1.012] | 6 / 6 | 19 / 19 | 2 / 4 | 5 / 3 | 0 / 0 | 0 / 0 |
| 7 | 105 / 922 [922–997] | 10 / 9 | 24 / 31 | 7 / 12 | 5 / 7 | 0 / 0 | 0 / 5 |
| 8 | 613 / 706 [706–788] | 9 / 9 | 29 / 37 | 12 / 16 | 5 / 9 | 0 / 0 | 0 / 3 |
| 9 | 308 / 1.323 [1.311–1.482] | 11 / 11 | 34 / 37 | 17 / 20 | 5 / 5 | 0 / 0 | 0 / 0 |
| 10 | 1.451 / 3.878 [3.766–4.020] | 12 / 12 | 37 / 37 | 20 / 20 | 5 / 5 | 0 / 0 | 0 / 0 |
| 11 | 1.128 / 18.935 [18.470–20.248] | 9 / 12 | 37 / 34 | 20 / 21 | 5 / 13 | 0 / 0 | 0 / 1 |
| 12 | 236 / 17.997 [17.285–20.000] | 9 / 12 | 51 / 58 | 29 / 38 | 10 / 20 | 0 / 0 | 0 / 1 |
| 13 | 9 / 21.743 [20.477–23.518] | 12 / 10 | 39 / 62 | 29 / 38 | 10 / 24 | 0 / 0 | 0 / 0 |
| 14 | 11.630 / 22.590 [21.089–24.135] | 9 / 11 | 44 / 59 | 29 / 38 | 15 / 21 | 0 / 0 | 5 / 2 |
| 15 | 11.728 / 25.489 [24.065–28.071] | 10 / 11 | 52 / 61 | 29 / 38 | 23 / 23 | 0 / 0 | 5 / 0 |
| 16 | 11.414 / 28.583 [26.973–33.448] | 13 / 13 | 52 / 61 | 29 / 38 | 23 / 23 | 0 / 0 | 5 / 0 |
| 17 | 12.615,5 [12.612–12.619] / 32.708 [30.984–41.670] | 13 / 13 | 52 / 61 | 29 / 38 | 23 / 23 | 0 / 0 | 5 / 0 |
| 18 | 15.807 [15.788–15.826] / 35.779 [34.066–46.696] | 13 / 13 | 52 / 61 | 29 / 38 | 23 / 23 | 0 / 0 | 5 / 0 |
| 19 | 20.855 [20.797–20.913] / 42.594 [40.590–55.820] | 13 / 13 | 52 / 61 | 29 / 38 | 23 / 23 | 0 / 0 | 5 / 0 |
| 20 | 24.186,5 [24.077–24.296] / 44.350 [42.922–61.251] | 13 / 13 | 52 / 61 | 29 / 38 | 23 / 23 | 0 / 0 | 5 / 0 |
| 21 | 27.292 [27.123–27.461] / 48.489 [46.700–67.882] | 13 / 13 | 52 / 61 | 26 / 38 | 26 / 23 | 0 / 0 | 5 / 0 |
| 22 | 31.606 [31.334–31.878] / 54.210 [48.320–77.513] | 13 / 13 | 52 / 61 | 23 / 38 | 29 / 23 | 0 / 0 | 5 / 0 |
| 23 | 33.013 [32.708–33.318] / 58.965 [48.934–83.548] | 13 / 13 | 52 / 61 | 20 / 34 | 32 / 27 | 0 / 0 | 5 / 0 |
| 24 | 35.464,5 [35.100–35.829] / 61.366 [49.439–87.112] | 13 / 13 | 52 / 61 | 17 / 26 | 35 / 35 | 0 / 0 | 5 / 0 |
| 25 | 39.358,5 [38.873–39.844] / 62.330 [49.522–91.208] | 13 / 13 | 52 / 61 | 13 / 22 | 39 / 39 | 0 / 0 | 5 / 0 |
| 26 | 44.078,5 [43.434–44.723] / 63.636 [50.320–95.626] | 12 / 12 | 42 / 61 | 12 / 18 | 30 / 29 [29–39] | 0 / 14 [4–14] | 5 / 0 |
| 27 | 46.060 [45.537–46.583] / 65.633 [51.551–101.662] | 12 / 12 | 28 / 61 | 9 / 18 | 19 / 17 [17–39] | 0 / 26 [4–26] | 5 / 0 |
| 28 | 48.230 [47.706–48.754] / 66.347 [51.910–105.358] | 9 / 12 | 20 / 59 | 9 / 15 | 11 / 6 [6–40] | 0 / 38 [4–38] | 5 / 0 |
| 29 | 53.694,5 [53.173–54.216] / 70.410 [54.147–111.616] | 10 / 12 | 0 / 27 | 0 / 0 | 0 / 0 [0–25] | 0 / 27 [2–27] | 5 / 0 |
| 30 | 54.364,5 [53.968–54.761] / 75.629 [59.508–120.267] | 3 / 12 | 0 / 2 | 0 / 0 | 0 / 0 [0–2] | 0 / 2 [0–2] | 5 / 0 |

## Sequenza macro di chiusura

1. **Mantenere capacità fino a D27.** Top770 conserva 61 crop a D21-D27. E18.26 ne conserva 52 soltanto fino a D25 e scende a 42/28/20 a D26/D27/D28. Il ritiro delle Strawberry Top770 inizia a D23, con 38/34/26/22/18/18/15/0 a D22-D29; Codex avvia il ritiro già a D21 su una base di sole 29 tile.
2. **Rimpiazzare colture lunghe con cicli brevi.** Top770 semina ancora 90 tile Wheat+Carrot in D21-D30; noi 46 Wheat. Il totale raccolto della famiglia è invariato nei cinque replay (345 unità), con due combinazioni: 246 Wheat + 99 Carrot oppure 333 Wheat + 12 Carrot. Le nuove Carrot compaiono a D26. La selezione è compatibile con un adattamento al valore relativo, ma dai replay non si ricostruisce con certezza la sua funzione decisionale.
3. **Mantenere lavoro per consegne e vendite finali.** Top770 tiene 12 persone da D26 a D30 (11 hands + farmer); E18.26 passa a 9/10/3 nelle ultime tre giornate. Top770 esegue 28 HARVEST a D30, Codex 4. Nessuno semina in D30; Top770 ha semine residuali in D29 che lasciano due crop terminali, perciò il suo cutoff non va copiato senza verificare maturazione e consegna.
4. **Il bestiame rimane produttivo fino al termine.** Top770 conserva 9 Cow + 5 Sheep e non subisce fughe; Codex chiude con 6 + 3. Gli animali non sono liquidabili tramite SELL: solo i prodotti venduti entrano nel reward. Il modello deve prenotare ultimo raccolto e consegna, e valutare il costo del servizio che non può più generare ricavi entro il termine.

## Produzione e vendite effettive D21-D30

| KPI | E18.26, mediana [range] | Top770, mediana [range] |
|---|---:|---:|
| Semine completate Wheat+Carrot | 46 | 90 |
| Raccolto Wheat+Carrot, unità | 276 | 345 |
| Raccolto Strawberry, unità | 72 | 189 |
| Strawberry vendute, unità | 84 | 189 |
| Milk venduto, unità | 54 | 135 |
| Wool venduta, unità | 18 | 72 |
| Fertilizer venduto, unità | 0 | 139 [131–140] |
| HARVEST eseguiti, crop e bestiame | 144 | 285 |
| WATER eseguiti | 342 | 450 |
| PASS richiesti | 509,5 [509–510] | 115 |
| Costo assunzioni D21-D30 | 2.488 | 3.040 |
| Flusso netto delle azioni D30 | -5,5 [-81–70] | 6.149 [5.122–8.562] |

Il locale raccoglie 72 Strawberry ma ne vende 84, grazie allo stock precedente; Top770 raccoglie/vende 189. Allo stesso modo le unità vendute non sono sempre uguali alla produzione della medesima finestra. Il minore output locale riguarda anche FEED/CARE, continuità del bestiame e Fertilizer: in D21-D30 non viene richiesto alcun COLLECT_FERTILIZER da E18.26.

## Variabilità economica a produzione uguale

| Episodio Top770 | Milk venduto | Incasso Milk | Prezzo medio Milk | Strawberry vendute | Incasso Strawberry | Cassa D30 |
|---|---:|---:|---:|---:|---:|---:|
| 105405557 | 135 | 1.707 | 12,6 | 189 | 22.164 | 80.320 |
| 105384058 | 135 | 1.503 | 11,1 | 189 | 4.176 | 59.508 |
| 105398563 | 135 | 30.308 | 224,5 | 189 | 15.488 | 120.267 |
| 105391568 | 135 | 1.795 | 13,3 | 189 | 20.324 | 75.629 |
| 105565293 | 135 | 731 | 5,4 | 189 | 5.694 | 67.447 |

L'incasso Milk varia da 731 a 30.308 a parità di 135 unità vendute: è una prova diretta dell'effetto del prezzo realizzato. Le Strawberry vendute sono sempre 189, con incassi da 4.176 a 22.164. Non si deve attribuire il range della cassa soltanto alla scelta Carrot/Wheat.

## Pascoli vuoti: correzione della diagnosi D20

L'analisi ai soli checkpoint D13/D14 vedeva 13→9 e aveva ipotizzato quattro perdite più un animale mai aggiunto. Il dettaglio per turno corregge questa lettura: nello step 312, cambio di D14, scappano cinque animali (3 Cow + 2 Sheep), dopo due giornate senza FEED. Il numero scende realmente 13→8; durante D14 viene piazzata una Sheep già prevista, risalendo a 9. Non viene comprato alcun animale da D14 in poi. I cinque pascoli restano vuoti per tutti i 17 checkpoint D14-D30, cioè 85 posti-giornata osservati. Top770 non subisce fughe.

Il refill automatico va valutato sul margine atteso entro D30, includendo primo yield (8 giorni Cow, 6 Sheep), feed, cura, trasporto e cash disponibile. Nei replay locali i prezzi Milk/Wool diventano molto bassi: prevenire la fuga non equivale a dimostrare conveniente qualsiasi acquisto tardivo. Ogni posto vuoto deve comunque avere una decisione esplicita, una scadenza e una motivazione economica, senza cambiare la topologia.

## Residui terminali e priorità successive

Top770 conserva 1 Wheat nello shed, 12 Fertilizer trasportati e due crop con yield registrato pari a 2 unità (non necessariamente mature). Codex ha shed e crop vuoti ma conserva 4 Wheat negli inventari. Il reward è soltanto cash: questi residui non vengono automaticamente valorizzati. La perfezione della pulizia terminale ha un impatto minore dei divari osservati in volume prodotto e venduto.

Priorità per una prossima release, da isolare nei confronti interni:

1. Proteggere il ponte D11-D14 con precedenza a raccolto/consegna Melon-Wheat e obblighi FEED, finanziando le scadenze prima del lavoro marginale; evitare le cinque fughe.
2. Inserire controllo giornaliero dei posti vuoti con piano di refill e verifica del tempo di rientro; nessun posto dimenticato dal dispatcher.
3. Mantenere il plateau crop e costruire cicli brevi D23-D28 con WATER, HARVEST e vendita prenotati; selezionare Wheat/Carrot usando margine e fattibilità, non il solo prezzo corrente.
4. Prenotare raccolti/trasporto/vendite D29-D30 prima di ridurre gli hands. Il taglio deve essere conseguenza delle missioni esaurite. Recuperare anche il flusso Fertilizer e interrompere FEED/CARE privi di ritorno entro il termine.

Nota di topologia: i replay Top770 sono 7-7-0 per i pascoli finali, con 15-16 strutture pasture transitorie a D11-D14. Inoltre costruiscono due coop vuote in D29, ancora vuote a D30 e senza Goose. I grafici distinguono i pascoli vuoti dalle coop; queste costruzioni non sono un target da importare nella nostra 770.

Dataset completo: `docs/model_specs/codex/e18/artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json`.
