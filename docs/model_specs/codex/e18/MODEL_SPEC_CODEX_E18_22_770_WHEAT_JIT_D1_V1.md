# MODEL SPEC — Codex E18.22 7-7-0 Wheat JIT D+1 V1

## Stato

`GENERATED__PARENT_DELTA_PASS__INCUMBENT_GATE_FAIL__NO_UPLOAD`.

E18.22 eredita piano, route, retry executor, netting Wheat e guard dei pickup
in-flight da E18.21. La sola modifica è l'orizzonte di procurement Wheat: dal
D11 gli acquisti sono limitati alle obbligazioni worker pendenti oggi, nello
step corrente e a D+1. La quota attribuibile soltanto a D+2 viene rimossa.

Il delta diretto contro E18.21 è forte e passa in entrambi i seat. Il gap da
E18.16 si riduce, ma resta troppo ampio per autorizzare Gate 1 completo,
holdout, final-confirmation o upload Kaggle.

## Ipotesi causale

Il parent acquistava Wheat attraverso D+2, mentre la vendita proteggeva solo
il fabbisogno fino a D+1. Il risultato era una sequenza cross-turn nella quale
la quota anticipata veniva acquistata, resa nuovamente vendibile e poi
ricomprata. E18.20 eliminava soltanto l'overlap nello stesso batch; E18.21
proteggeva correttamente i pickup in-flight, ma non chiudeva il ciclo D+2.

Proteggere la scorta anticipata era già risultato antieconomico. E18.22 evita
quindi di crearla: calcola il fabbisogno D0–D+1 per worker, sottrae il Wheat
presente nello shed e usa il risultato come cap complessivo di
`BUY_PRODUCT WHEAT`.

## Trattamento

Da D11, dopo i guard E18.20/E18.21:

1. ricostruire i `PICKUP WHEAT` ancora pendenti oggi per worker;
2. includere i pickup emessi nello step ma non ancora eseguiti;
3. aggiungere le obbligazioni complete di D+1;
4. sottrarre il Wheat corrente nello shed;
5. limitare gli acquisti Wheat alla carenza risultante;
6. preservare ordine e quantità di ogni altro ordine.

Non vengono introdotte riserve persistenti né modifiche a seed, animali,
workforce, land, route o lifecycle.

## Invarianti

- piano E18.18 hash
  `844113c8971ccf3840758cd9d35449e01bc766a1d4b890c7fd8ab29c177410a1`;
- topologia `7-7-0`, 14 pascoli pieni;
- `9 COW + 5 SHEEP`, cap risorse 14;
- 12 hands al picco;
- zero overlap Wheat nello stesso batch da D11;
- nessuna mutazione delle traiettorie;
- zero errori controller.

## Evidenza pre-gate

### Delta causale contro E18.21

Seed `180903001`, entrambi i seat:

| Seat E18.22 | E18.22 | E18.21 | Margine |
|---:|---:|---:|---:|
| 0 | 76.966 | 74.673 | +2.293 |
| 1 | 76.793 | 74.846 | +1.947 |

Mediana E18.22 `76.879,5` contro E18.21 `74.759,5`: delta `+2.120`
(`+2,84%`). Topologia e composizione finali sono esatte; errori zero.

E18.22 rimuove 4.308 unità nominali D+2 per seat nel confronto diretto. Le
richieste eseguite scendono da circa `SELL 1.795 / BUY 1.650` del parent a
`SELL 362 / BUY 215`. I FEED saltati scendono da 14 a 7 in questo matchup.

### Confronto con l'incumbent E18.16

| Seat E18.22 | E18.22 | E18.16 | Margine |
|---:|---:|---:|---:|
| 0 | 52.379 | 79.284 | -26.905 |
| 1 | 51.704 | 77.693 | -25.989 |

Mediana E18.22 `52.041,5` contro `78.488,5`, delta `-26.447`
(`-33,70%`). Rispetto allo smoke E18.21 il candidato guadagna 507 punti
assoluti e il gap mediano si riduce di 663 punti circa, ma il gate incumbent
resta `FAIL`.

Contro E18.16 E18.22 richiede `SELL 365 / BUY 220`, ormai paragonabili a
`SELL 415–417 / BUY 469` dell'incumbent. Rimuove 4.299 unità nominali D+2 per
seat e riduce i FEED saltati da 19 a 12 senza comprare più scorta.

## Diagnosi residua e prossima leva

Il mercato Wheat non è più il differenziale principale. Nel replay contro
E18.16 il candidato registra ancora per seat:

- 11 `PLANT` saltati;
- 102 `WATER` saltati;
- 40 `HARVEST` saltati;
- 80 `FERTILIZE` saltati;
- 36 `PICKUP` saltati;
- 12 `FEED` saltati.

I 102 WATER possono includere azioni già soddisfatte e gli 80 FERTILIZE sono
opzionali. In questa fase i 40 HARVEST e gli 11 PLANT erano ancora soltanto
proxy da classificare, non perdite economiche dimostrate.

## Aggiornamento diagnostico E18.23–E18.24

La classificazione successiva corregge l'interpretazione iniziale:

- le 11 `PLANT` sono richieste D11 verso la SW ancora bloccata;
- al primo passaggio `WATER` utile, tutte le 11 tile sono già occupate contro
  E18.16, quindi le richieste sono duplicati obsoleti e non semine perse;
- sugli 80 `HARVEST` respinti nei due seat, 65 incontrano `TILE_EMPTY` e 15
  `TILE_WEED`, anch'essi prevalentemente task superati dallo stato;
- anticipare il JIT Wheat a D10 non libera capitale: le cinque unità acquistate
  sono già necessarie entro D+1 e lo sblocco SW resta a D12 H1.

E18.23 ed E18.24 sono pertanto respinte. E18.22 resta il miglior sviluppo
post-E18.18; la prossima leva deve aumentare i cicli di coltura completati e
monetizzati, in particolare D21–D30, tramite un nuovo planner e non tramite un
altro recupero locale dei comandi respinti.

## Artefatti

- config: `configs/CODEX_E18_22_770_WHEAT_JIT_D1_V1.json`;
- controller: `tools/e18_22_wheat_jit_d1_controller.py`;
- test: `tests/test_codex_e18_22_wheat_jit_d1_controller.py`;
- runner: `tools/run_e18_22_770_wheat_jit_d1_gate.py`;
- risultati: `artifacts/derived/E18_22_770_WHEAT_JIT_D1_PRE_GATE_V1.json`;
- report: `reports/E18_22_770_WHEAT_JIT_D1_PRE_GATE_REPORT_IT.md`.
