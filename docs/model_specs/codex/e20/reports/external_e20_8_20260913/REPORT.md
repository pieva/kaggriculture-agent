# E20.8: verifica esterna dei 22 KPI e dei prezzi

Submission **56191695**, E20.8/E20v40; SHA256 `3305aef93ac53aa805db01541feb7e79022df1f5e04a2f167d0e6c00b69c63a5`. Derivata dalla 772: 8 mucche, 6 pecore, 2 oche, 14 pascoli (761) e 2 pollai. Non confondere con E20.1 772 o E20.2 locale.

[Apri il report interattivo](REPORT.html). 22 pannelli, selezione singola partita, riferimenti storici opzionali e curve per tutti i nove prodotti. Per ciascun prodotto: quantità vendute, prezzi unitari realizzati ponderati e prezzo di mercato. Selezionando una partita si può passare dalla giornata al singolo turno.

## Campione e risultato

Acquisizione congelata: 2026-09-13T06:03:29.258039+00:00. Ultimi 20 episodi pubblici completi non self-play, scelti solo per data/ID. Tutti acquisiti e verificati; nessun caso escluso per esito. La cronologia completa restituisce 70 episodi pubblici e 41 vittorie. Sono match esterni con avversari diversi, non un torneo appaiato né una prova causale delle due oche.

| Indicatore | Esito |
|---|---:|
| Rating al cutoff | 1364.9 |
| Vittorie ultimi 20 | 9/20 |
| Cassa media / mediana | 71388.45 / 75549.50 |
| Margine medio | -24679.90 |
| Rating medio avversari prima della partita | 1380.8 |
| Fughe animali | 9 in tre partite |
| Perdite crop per sete medie | 2,3 |

Il rating è nettamente superiore ai riferimenti precedenti osservati, ma gli ultimi avversari hanno rating medio 1380,8: il campione storico 772/775 affrontava avversari medi circa 908/1030. Le casse dei corpus non vanno lette come effetto della versione. Nel campione recente il margine medio è ancora negativo e tre collassi pesano molto.

## Difetto concreto di avvio, da correggere prima di altro tuning

Episodi **108338031, 108367424, 108428840**. Tutti completano D1 con 12 meloni, 7 grani, 4 animali e cassa zero. I flussi D1 coincidono: 26 grani venduti per 764, 31 comprati per 922; acquisti animali 1800, semi 1030, assunzioni 12. Con 3000 iniziali: 3000 + 764 − 922 − 1800 − 1030 − 12 = 0.

A D2 H1 chiedono tre HIRE con zero cassa: nessuno viene assunto. I lavoratori previsti dal calendario mancano, il FEED viene compromesso e si verificano due fughe nel refresh D2 e un’altra a D12. Topologia finale 500, non 761; cassa finale 26882, 23136 e 21660. Il problema si presenta in entrambi i ruoli. La contabilità ricostruita dimostra i mancati HIRE e la sequenza osservata; non è ancora una prova che una particolare patch risolva l’intera cascata.

Il replay 108327320 completa la stessa apertura produttiva ma vende il grano per 728 e lo compra per 854: resta con 32 di cassa. La differenza iniziale di 32 è sufficiente a distinguere disponibilità finanziaria per D2, ma non autorizza una riserva universale di 32 senza verificare obbligazioni, prezzi e ordine delle transazioni.

Le altre 17 partite raggiungono 761: cassa media 79770,06 e margine medio −1576. Questa segmentazione è diagnostica, fatta dopo gli esiti; il risultato ufficiale del campione rimane quello su tutte le 20. Non nascondere i tre fallimenti né sostituire la media principale con quella filtrata.

## Prezzi e ricavi

Tutte le medie seguenti includono le 20 partite. Prezzo = incassi totali / quantità totali vendute; non media aritmetica dei prezzi giornalieri. Il grano include rivendite di prodotto acquistato: non equivale a produzione agricola.

| Prodotto | Unità vendute medie | Incassi medi | Prezzo ponderato | Unità medie vendute a 1 |
|---|---:|---:|---:|---:|
| CARROT | 70.80 | 6005.95 | 84.829802259887 | 0.00 |
| EGG | 47.60 | 2638.20 | 55.424369747899156 | 0.00 |
| FERTILIZER | 298.70 | 13897.30 | 46.525945764981586 | 20.95 |
| MELON | 64.80 | 12619.75 | 194.74922839506172 | 0.00 |
| MILK | 205.45 | 11920.50 | 58.02141640301777 | 59.60 |
| STRAWBERRY | 201.35 | 20876.45 | 103.68239384156941 | 43.05 |
| TOMATO | 0.00 | 0.00 | n/a | 0.00 |
| WHEAT | 368.10 | 14370.65 | 39.04007063298017 | 0.00 |
| WOOL | 139.55 | 17029.10 | 122.02866356144752 | 36.75 |

Latte: prezzo medio ottenuto 58,02 contro 90,35 degli avversari; fragole 103,68 contro 126,50. Anche i volumi venduti sono inferiori: il deficit di ricavi è circa 8788,5 sul latte e 12552,3 sulle fragole. Il campione segnala un problema combinato di produzione, disponibilità e calendario delle vendite, non solo di prezzo. Circa il 29% del latte venduto, il 21% delle fragole e il 26% della lana viene ceduto a prezzo 1. Questo non prova che ritardare la vendita avrebbe migliorato il risultato.

### Meccanismo verificato per turno

- Le vendite sopra 1 aumentano lo stock pubblico; quelle a 1 no. Gli acquisti BUY_PRODUCT lo riducono.
- I negozi consumano dopo gli scambi e possono sostenere il prezzo.
- Per entrambi i giocatori si registrano unità e quotazioni effettive: gli ordini non riusciti non diventano vendite.
- Il grafico dettagliato separa prezzo prima scambi, dopo gli scambi di entrambi e dopo il consumo dei negozi. Il delta non è attribuito solo al nostro agente.
- Quotazioni per unità in lockstep: ordini e priorità dell’avversario contano. Non si stima un controfattuale di rinvio delle vendite da una correlazione.

Cassa di entrambi verificata in ogni transizione; prezzi e stock riprodotti dopo scambi e consumo per **719 × 20 = 14380 batch**, senza differenze. Le singole transazioni sono nei CSV della cartella profiles; MARKET_BATCHES.csv aggrega per turno, prodotto e lato, con acquisti, stock, consumo e vendite al minimo.

## Riesame della vecchia 774 e confronto strategico

Letti NEW_SESSION e il brief E21. Gli sviluppi del 12 settembre hanno già superato il brief iniziale: la 774 è stata ricostruita, corretta, pubblicata e poi accantonata a favore del trasferimento del calendario operativo alla 772. Nessuna nuova E21 è implementata in questa analisi.

| Passaggio | Che cosa effettivamente faceva | Lezione rispetto alla pianificazione attuale |
|---|---|---|
| Vecchia 774 storica | Eseguibile storico non recuperato; ramo superstite rimane RECOVERY e non attiva reclaim | Non presentare ricostruzioni moderne come replica esatta dell’esperimento storico |
| Fixed774 ricostruita | Togliendo (4,7) riempie il pascolo Q1 prima vuoto: restano 19 animali; visite animali convertite anche in PASS, pecora in deposito | Un cap geometrico non elimina coerentemente animale, acquisto e lavoro |
| Repair2 | 8C/9S/1G, acquisti/placement coerenti, escursioni eliminate, acqua successiva sul target e consegna terminale protetta | Miglioramento tecnico, ma copertura biologica locale e non pianificazione generale; cassa inferiore nei due seed esposti |
| Calendario 774 C2 | Obiettivi di colture con dispatcher osservativo da D12 | Raggiunge quote tardi, perde ricavi: pianificare la quantità non basta senza visite e finanziamento nei tempi |
| E20.8 attuale | Calendario operativo tradotto e adattato, rotte e visite, 8C/6S/2G | Forte segnale esterno; i replay mostrano che una missione deve prenotare anche la cassa del giorno successivo |

La prossima ipotesi utile emerge dai replay: proteggere la fattibilità dell’avvio D2 rispetto ai prezzi realmente eseguiti, mantenendo gli impegni del calendario. Prima di una nuova versione ricostruire costi obbligatori, ordini di grano, sequenza di vendita/acquisto e comportamento quando un HIRE fallisce. Non ripartire dal tweaking dei pesi né da una nuova topologia. Nessuna patch applicata qui.

Fonti locali: [audit Fixed774](../../../e21/reports/audit_fixed774/REPORT.md), [Repair2](../../../e21/reports/repair774_v2/REPORT.md), [traiettorie e limite di ricostruzione](../../../e21/reports/trajectory_774_772_775/REPORT.md), [calendario operativo](../../../e21/reports/common_operational_program/REPORT.html).

## Limiti e stato

Rating fotografato al cutoff, non una previsione di stabilità. I fallimenti non sono timeout: replay completi DONE/DONE, con mancata realizzazione del piano. I KPI MOVE/PASS includono richieste per aiutanti eventualmente assenti, secondo la definizione standard: nei collassi non interpretarli come lavoro fisico realmente disponibile. Non inferire zero errori interni della policy dai soli replay. Nessuna simulazione nuova, submission, modifica di strategia, commit o push.
