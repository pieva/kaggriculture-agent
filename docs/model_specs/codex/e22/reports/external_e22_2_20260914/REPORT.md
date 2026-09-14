# E22.2 vs E22.1 — risultati esterni, 14 settembre 2026

Entrambe Complete. Rating dell’ultimo episodio nello storico congelato: **E22.2 1706,92**, **E22.1 2147,08** (delta −440,16). Sono osservazioni temporalmente datate, non rating stabilizzati.

| Versione | Episodi competitivi | Vittorie | Rating ultimo | Vittorie ultimi 20 | Cassa media ultimi 20 | Rating medio avversari ultimi 20 |
|---|---:|---:|---:|---:|---:|---:|
| E22.2 | 92 | 52 | 1706.92 | 9/20 | 90045.3 | 1754.8 |
| E22.1 | 151 | 74 | 2147.08 | 8/20 | 87833.1 | 2162.0 |

La percentuale di vittorie e la cassa grezza non provano superiorità di E22.2: affronta avversari mediamente più deboli (circa 407 punti in meno nel campione recente). Gli storici coprono durate diverse e includono la salita iniziale del rating. Un self-play per versione è escluso dalle medie. Nessun episodio non completato nello storico congelato.

## Errori evidenti e controlli

- **Due mucche mai collocate, in due replay E22.2 su 20** (108729054, 108777186): D2 H1 cassa 3, richiesti tre HIRE ma eseguiti due; operaio 3 assente alla costruzione D2 H6. D4 H24 PLACE COW fallisce sulla casella (2,4) priva di pascolo. Una mucca resta in magazzino; finale 7C9S. Il piano non recupera.
- E22.2: 18/20 finali 8C9S, 2/20 7C9S; **zero fughe**. E22.1: **tre fughe** complessive, 16/20 mix atteso; ulteriori problemi di costruzione/collocamento.
- In E22.2 si osservano 40 transizioni crop→weed dopo stress nel campione; sei PLANT senza effetto, spesso su infestanti non rimosse. Non confondere le caselle non irrigate al checkpoint con perdite certe.
- Giorni isolati senza alimentazione e comandi CARE/WATER/HARVEST senza effetto sono documentati per episodio; alcuni sono ridondanze, non errori fatali.
- Due fertilizzanti trasportati residui in ogni partita E22.2. Nessun residuo finale di latte/lana/uova, ma questo non implica vendita integrale: nei due casi con mucca bloccata si scartano 12 lane ciascuno (7 a D26 e 5 a D27) per saturazione del magazzino al refresh. Totale E22.2: 24 lane, 18 grani e 2 fertilizzanti scartati. E22.1 mostra overflow in 4/20 replay, con 25 lane, 11 latti e 19 uova persi. [Audit overflow](OVERFLOW.json).
- **Parità del bundle E22.2 su 14.380 azioni**, altrettante per E22.1; zero errori di riconciliazione della cassa su tutti gli 80 lati analizzati. Nessuna simulazione nuova, nessuna modifica alla policy.

## Lettura economica

La lana aumenta a 225 unità medie contro 158,1 di E22.1, ma il ricavo medio lana è 15.933,45 contro 15.444,20. Il confronto è descrittivo: prezzi e controparti differiscono. Il rapporto dei ricavi alle unità vendute è circa 71,20 contro 98,46 monete/lana (223,8 e 156,85 unità medie vendute). E22.2 rinuncia inoltre alle uova (ricavo medio E22.1 4.113,50). L’aumento di volume non si traduce in un aumento proporzionale di ricavi. Non attribuire tutto il divario di rating a una sola causa.

## Metodo

Storici completi acquisiti via EpisodeService/ListEpisodes; ultimi 20 incontri pubblici competitivi per submission, senza selezione per esito. 40 replay, 720 stati ciascuno, 80 ledger auditati. 22 KPI standard più nove coppie volumi/prezzo, immediatamente sotto la produzione associata: **40 pannelli**, selezione aggregata o singolo episodio. Mediana e min–max; prezzo realizzato ponderato sulle unità vendute in ogni partita/giorno, poi mediana tra le partite con vendite. Nessuna vendita = dato mancante, non zero. Cassa/consistenze al checkpoint 24D−1; flussi su tutti i batch. Nel grafico coltivate, la linea aggiuntiva tratteggiata mostra terreno sbloccato.

[Report interattivo](REPORT.html) · [CSV 22 KPI e prezzi](DAILY_22_KPI_PRICES.csv) · [Tutti gli esiti](ALL_RESULTS.csv) · [Diagnostica](DIAGNOSTICS.json) · [Catalogo e hash](COHORT.json) · [Protocollo](PROTOCOL.json) · [Top 2750–3000](../top_2750_3000_20260914/REPORT.html).
