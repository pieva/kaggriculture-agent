# E22 — approcci comuni e variabilità degli avversari di E20.9

13 settembre 2026. Mandato: spazio di ricerca libero da vincoli ereditati di topologia, portafoglio e pianificazione. [Protocollo E22](../../RESEARCH_PROTOCOL.md). Nessuna modifica al campione E20.9.

**Prima conclusione: la rigidità del nostro piano è un'ipotesi da verificare, ma non è dimostrata come causa generale delle sconfitte. Ci battono sia piani quasi invarianti sia strategie con configurazioni variabili. La variabilità più interessante da isolare è la scelta del portafoglio, che può convivere con percorsi e tempi molto stabili.**

[Dossier visuale interattivo](REPORT.html): selezione delle 33 partite, mappe D10/D20/D29, cassa, organico, colture e animali, con volumi venduti e prezzi immediatamente sotto ciascuna produzione. [Tabella completa](OPPONENTS.csv), [aggregati](SUMMARY.json), [repliche della stessa submission](VARIABILITY.json).

## Campione e score

[Esploratore della variabilità per specie](SPECIES_VARIABILITY.html): tre traiettorie per ciascun avversario, numero di caselle per mucche/pecore/oche e per ogni coltura, pascoli e pollai, occupazione complessiva e strutture vuote. Il selettore D1–D30 confronta conteggi e mappe dello stesso giorno nelle tre partite. [Serie CSV per specie e quadrante](SPECIES_TILES.csv).

Storico congelato della submission **56202079**: 34 episodi completati, dei quali 33 pubblici contro altri team e un'autopartita esclusa. E20.9 ottiene **18 vittorie e 15 sconfitte**. Rating aggiornato nell'ultima partita del campione **1352,08**, massimo precedente **1584,88**. Non è una stima stabilizzata: lo storico evolve dopo il congelamento.

Nelle 15 sconfitte, rating iniziale degli avversari **1361,99–1626,35**; distacco economico medio **8345,07**, mediano **7384**. Nessun avversario delle sconfitte è prossimo a 2000. Questo campione identifica debolezze del campione corrente, non condizioni sufficienti a ottenere rating 2000. La cassa finale è distinta dal rating Kaggle.

Tutti i 33 replay sono completi. Ricostruiti i registri economici di entrambi i giocatori: 66 profili con verifica della cassa sulle transizioni e riconciliazione del saldo mensile, senza errori. Fonti: [storico](history_56202079.json), [inventario con hash e identità](COHORT.json), [API nel codice ufficiale Kaggle](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/api.py). I metadati sono acquisiti dall'endpoint EpisodeService/ListEpisodes; ogni inventario identifica il replay pubblico utilizzato.

## Quanto sono diversi fra loro

La geometria seguente conta i pascoli nei quadranti Q0/Q1/Q2/Q3 a D20. I pollai sono separati; la stessa distribuzione per quadrante non implica stesse coordinate o stesso numero di animali vivi.

| Famiglia osservata | Sconfitte E20.9 | Esempi | Osservazione |
|---|---:|---|---|
| 10/7/0/0 | 6 | Sam-wiz, darcy132, CoorDi, Roumak Das | Maggiore concentrazione di pascoli a nord; mix di mucche e pecore |
| 7/7/0/0 | 7 | Denis Revenko, s56165462, John Stupid | Da nessuna oca a tre oche, con pollai distinti dai pascoli |
| 9/3/0/0 | 1 | EnricRovira | Cinque pollai, 4 mucche/7 pecore/5 oche a D20 |
| 5/5/4/0 | 1 | Rheinmetall | Animali anche a sud e portafoglio colturale diverso |

**14/15 comprano terreni a D7 e D12**; Rheinmetall a D6 e D9. Nove hanno esattamente 33 fragole e 25 grani a D20. Nei rimanenti cambiano soprattutto numero di fragole, occupazione animale e, nel caso Rheinmetall, presenza di meloni tardivi. In questo campione le famiglie più frequenti condividono una cronologia produttiva molto simile.

Il confronto con le vittorie evita di proclamare una geometria vincente per definizione: la 10/7 compare in **8 partite, 6 sconfitte e 2 vittorie nostre**; la 7/7 in **9 partite, 7 sconfitte e 2 vittorie nostre**. Queste non sono prove controllate: rating, mercato e qualità di esecuzione cambiano. Inoltre Sam-wiz compare con due submission diverse, una battuta e una vincente: non sono repliche dello stesso modello.

**Somiglianza del lavoro:** darcy132 (108474414), CoorDi (108481627) e Roumak Das (108483657) emettono gli stessi **719/719 gruppi di comandi dei lavoratori**. Kevin E R MILLE e Chika Komari coincidono in 718/719. Gli ordini di mercato non sono inclusi in questa misura. Questa evidenza è compatibile con una base di pianificazione comune; non identifica il codice interno né prova l'assenza di ramificazioni non attivate.

## Quanto cambia la stessa submission

Per separare diversità fra modelli e adattamento entro il modello sono stati acquisiti **10 replay aggiuntivi**: per cinque rappresentanti, la stessa submission esatta nella sconfitta contro E20.9 e nelle due partite pubbliche precedenti contro altri team. Selezione esplorativa per coprire geometrie e portafogli osservati; nessun filtro sul risultato delle partite aggiuntive. Le tre coppie confrontate per modello non sono indipendenti.

| Avversario / submission | Gruppi di comandi identici fra replay | Evidenza a D20 |
|---|---:|---|
| Sam-wiz / 56159600 | 82,6–100% | 17 pascoli con 9 mucche/8 pecore, oppure 14 pascoli e 3 pollai con 8 mucche/5 pecore/3 oche. Sempre 33 fragole/25 grani |
| s56165462 / 56166543 | 99,4–99,6% | Sempre 14 pascoli/3 pollai, 8 mucche/6 pecore/3 oche, 33 fragole/25 grani |
| Denis Revenko / 55940657 | 99,4–100% | Geometria invariata, 10 mucche/4 pecore oppure 8 mucche/6 pecore; 37–38 fragole/23 grani |
| EnricRovira / 56193537 | 25,0–79,1% | Pollai 5, 4, 0; mix e occupazione variabili. Un replay perde due animali fra D2 e D3 |
| Rheinmetall / 56167101 | 18,4–20,9% | 12–16 strutture a D20, colture e animali diversi; in un replay anche 3 caselle di pomodoro |

s56165462 conserva **geometria, colture e composizione animale identiche in tutti i 30 snapshot giornalieri** dei tre replay. Eppure a D20 il prezzo delle fragole varia da **1 a 225**, quello del latte da **15 a 120**: nel campione non emerge una scelta colturale sensibile a queste differenze di mercato. Anche gli ordini di mercato registrati coincidono nei 719 turni.

Denis conserva la geometria per tutti i 30 giorni ma varia la specie animale in alcune caselle: è un esempio concreto di variabilità del portafoglio con lavoro quasi invariato. Sam-wiz mostra configurazioni alternative; due replay hanno addirittura tutti i comandi dei lavoratori identici, il terzo diverge prevalentemente nel ramo animale. Non possiamo ancora identificare il segnale che attiva queste scelte: prezzi, composizione avversaria, ruolo o altri elementi osservati.

Rheinmetall è il caso più diverso dal calendario comune: variazione di strutture, colture e percorsi. È il candidato più utile per studiare un'organizzazione alternativa, ma una variabilità elevata non è di per sé un vantaggio competitivo. EnricRovira rende evidente il rischio interpretativo: il replay con pochi animali contiene un deterioramento precoce, quindi una parte della differenza di stato è una perdita di capacità, non necessariamente una scelta desiderata.

Per distinguere scelta da fallimento, gli stati finali devono essere collegati a comandi emessi, risorse disponibili ed esito delle azioni. Le percentuali di coincidenza misurano identità dell'intero gruppo di comandi del turno: non sono percentuali di singole azioni né misure di qualità.

## Dove si forma il distacco economico

Media delle 15 sconfitte. Il valore è il flusso netto della fase dell'avversario meno il nostro, comprensivo di vendite, acquisti, lavoro e terreni; positivo significa che perdiamo terreno.

| Fase | Vantaggio netto avversario |
|---|---:|
| D1–D6 | −450 |
| D7–D11 | **+5716** |
| D12–D19 | −1194 |
| D20–D29 | **+5354** |
| D30 | −1081 |

La chiusura incompleta già verificata è reale, ma l'ultimo giorno recuperiamo mediamente parte del divario. Non è la fase principale in cui nasce la sconfitta.

| Prodotto | Unità vendute E20.9 / avversario | Prezzo medio ponderato E20.9 / avversario | Ricavo medio aggiuntivo avversario |
|---|---:|---:|---:|
| Melone | 66,0 / 72,1 | 187,7 / 218,3 | +3340 |
| Fragola | 215,7 / 255,3 | 146,3 / 147,2 | +6024 |
| Lana | 153,2 / 169,7 | 108,3 / 113,5 | +2663 |
| Latte | 241,6 / 231,8 | 111,8 / 117,6 | +260 |
| Carota | 75,0 / 25,5 | 52,3 / 59,9 | −2397 |
| Uova | 56,0 / 23,5 | 53,8 / 55,8 | −1697 |
| Pomodoro | 4,0 / 0,0 | 127,0 / — | −508 |

Questi sono ricavi lordi, non contributi netti isolati; il registro completo include grano e fertilizzante, acquisti e costi. In particolare il grano venduto può provenire da acquisti e rivendite: non va equiparato a produzione agricola.

**Meloni:** a D11 noi vendiamo in media 30 unità, gli avversari 55,6; a D12 noi 36, loro 11,9. Parte della differenza è dunque nel tempo di consegna e monetizzazione, non soltanto nel numero di caselle. L'avversario Rheinmetall ha una successione differente: queste medie non sono un calendario universale.

**Fragole:** il prezzo medio ponderato è quasi uguale, mentre gli avversari vendono circa il 18,4% di unità in più. Prima ipotesi: conservano e monetizzano più cicli utili. La nostra diversificazione in carote, uova e pomodori genera ricavi reali, ma in questo campione non compensa tutti i mancati ricavi delle altre produzioni. Questo non dimostra che diversificare sia sbagliato: bisogna confrontare rese marginali, tempi, domanda e costo del lavoro.

## Cosa significa per E22 e per l'obiettivo 2000

1. **Non congelare una topologia finale.** Confrontare liberamente le configurazioni osservate e alternative nuove. La prevalenza di 10/7 e 7/7 non costituisce un vincolo progettuale.
2. **Separare portafoglio e lavoro.** Verificare se una scelta osservata delle specie o dei cicli produttivi può usare percorsi stabili senza perdere capacità operativa. Denis e Sam-wiz sono riferimenti per questa domanda.
3. **Misurare il ciclo fino alla vendita.** D7–D11 e D20–D29 sono i primi intervalli da approfondire: consegne dei meloni e continuità delle fragole hanno segnali economici più grandi del solo residuo finale.
4. **Studiare la variabilità utile.** Seguire i punti di divergenza di Rheinmetall ed EnricRovira e distinguere scelta esplicita, reazione a un vincolo e degrado. Non usare una metrica di diversità come obiettivo.
5. **Validare contro avversari più forti e diversi.** Dopo ipotesi congelate e prove locali controllate, un campione vicino a rating 2000 dovrà verificare ciò che questo gruppo 1362–1626 non può dimostrare.

E20.9 introduce una conversione fragola→pomodoro programmata con ammissione sulla cassa: non implementa già una selezione dinamica della coltura dai prezzi. E22 resta nella fase di analisi; nessun nuovo algoritmo è dichiarato vincente e nessuna submission è stata effettuata.
