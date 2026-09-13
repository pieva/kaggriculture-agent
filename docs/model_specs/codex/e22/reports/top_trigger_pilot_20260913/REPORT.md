# E22 — trigger osservabili nei top: fascia 2000–2500 o 3000+?

13 settembre 2026. **Conviene partire da casi leggibili fra 2000 e 2500, mantenendo un top oltre 3000 come confronto continuo.** Il pilota sostiene questa scelta per la maggiore stabilità delle successioni colturali dei modelli intermedi; non dimostra che i programmi migliori siano necessariamente indecifrabili. Il primo classificato condivide infatti un pattern animale replicabile con due modelli intermedi.

[Apri il dossier interattivo](REPORT.html): confronto delle fasce, replica dell'ipotesi e selettore delle alternative per casella, con lo stato precedente all'azione. [Decisioni CSV](DECISIONS.csv), [protocollo](PROTOCOL.json), [inventario dei replay](COHORT.json), [analisi dettagliata](ANALYSIS.json).

## Campionamento e limiti

La [classifica pubblica Kaggle](https://www.kaggle.com/competitions/kaggriculture/leaderboard), congelata in [leaderboard.json](leaderboard.json), contiene 784 team nella fascia 2000–2500 e 6 sopra 3000. Sono state selezionate le submission con score più vicino a 2000, 2250 e 2500 all'interno della fascia, più le prime tre oltre 3000. Per ciascuna, cinque partite pubbliche complete recenti contro altri team, senza filtro sul risultato o sulla topologia.

Totale: **30 osservazioni di giocatori in 29 replay distinti**; una partita coinvolge due modelli selezionati. Ulteriori nove replay sono stati acquisiti dopo il congelamento di una specifica ipotesi. I ranking sono quelli della fotografia, non aggiornamenti in tempo reale. Il campione è esplorativo e non rappresentativo di tutti i 784 modelli intermedi.

Sono state estratte transizioni colturali/animali e ordini di mercato, collegati alle osservazioni precedenti: prezzi, variazione dei prezzi, negozi, cassa, lavoro, occupazione propria e avversaria. I conteggi di semina richiedono una nuova coltura con planted_day coerente, evitando di confondere un tentativo fallito con una variazione di acqua. Non è stata ricostruita qui la cassa con una nuova simulazione del motore: è un'analisi degli stati e delle decisioni registrate, distinta dall'audit economico delle 33 partite E20.9.

## Quanto è leggibile la variabilità

| Modello | Score | Gruppi di comandi identici fra replay, media | Slot animali con alternative | Slot colturali con alternative |
|---|---:|---:|---:|---:|
| Olympus | 2000,2 | 77,3% | 4 | 20 |
| kiki yi2 | 2248,9 | 66,3% | 4 | 2 |
| spbforce | 2499,5 | 41,5% | 8 | 5 |
| Majkel1337 | 3228,9 | 19,8% | 7 | 132 |
| Mengfei Li | 3084,1 | 37,7% | 0 | 111 |
| THIRD FARM CLUB | 3049,7 | 25,2% | 5 | 120 |

Uno slot allinea la stessa casella e il numero progressivo della semina/collocamento, con almeno tre osservazioni e almeno due specie diverse. **Non è un ramo identificato del codice.** Se le cronologie divergono, lo stesso numero progressivo può rappresentare opportunità diverse. Le metriche servono a trovare casi ispezionabili, non a quantificare la complessità algoritmica. Le dieci coppie per modello condividono gli stessi cinque replay e non sono indipendenti.

La differenza colturale è netta nel pilota: kiki yi2 mantiene la sequenza meloni D1, fragole D6–D12 e carote finali D25–D28. I top distribuiscono semine di fragole, pomodori e altre colture su finestre più varie. Mengfei Li può cambiare il numero di animali pur non mostrando alternative di specie negli slot che soddisfano la regola di allineamento: zero slot non significa zero adattamento.

Olympus comprende un episodio deteriorato con pochi animali e meno fragole. Non attribuire tutte le differenze a scelte desiderate. Rating e complessità operativa non sono sinonimi; un calendario quasi fisso può vincere e un piano variabile può fallire.

## Pattern T1: domanda di lana e scelta delle pecore

**Decisione osservata:** ordine BUY_ANIMAL che include SHEEP a D8 H2 per Olympus e kiki yi2, oppure a D7 H7 per Majkel1337. **Segnale candidato:** YARN_STORE già presente nell'osservazione precedente.

Nel pilota la corrispondenza è 15/15: quattro casi con negozio e pecore, undici senza negozio e senza pecore in quel preciso ordine. La [regola è stata congelata](YARN_HYPOTHESIS.json), poi controllata su tre replay precedenti non ancora analizzati per ciascuna submission esatta. Esito: **9/9 coerenti**, con sei positivi e tre negativi. [Replica e fonti](YARN_REPLICATION.json).

Il riferimento temporale è il primo ordine studiato che espone la scelta, non il momento dimostrato in cui il programma la decide internamente. Per Majkel1337 la scelta positiva contiene sia una mucca sia una pecora; non è un passaggio esclusivo a sole pecore. Si misurano richieste emesse, non acquisti necessariamente riusciti: gli altri ordini dello stesso turno possono modificare la cassa disponibile prima del regolamento.

Un contrasto della stessa submission rende insufficiente la regola semplice “scegli il prodotto dal prezzo più alto”:

| kiki yi2, D8 H2 | Negozio lana | Prezzo lana | Prezzo latte | Scelta |
|---|---|---:|---:|---|
| [108483384](https://www.kaggle.com/competitions/episodes/108483384/replay.json), replica | sì | 200 | 210 | Pecora |
| [108487585](https://www.kaggle.com/competitions/episodes/108487585/replay.json), esplorazione | no | 195 | 194 | Mucca |

La domanda persistente ha una spiegazione economica concreta: il negozio di lana consuma lana; il motore consente più istanze dello stesso negozio. Fonte tecnica: `SHOPS` e `_town_consume` nel [codice ufficiale](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py), verificati nella copia locale.

**Conclusione circoscritta:** è un pattern comune replicato, compatibile con una previsione della domanda o una regola sui negozi. Non prova che il programma legga direttamente YARN_STORE: prezzi passati, trend e altri segnali correlati potrebbero produrre la stessa scelta. Non implica una regola valida per tutte le caselle, tutti i giorni o tutti i modelli. Le osservazioni aggiuntive sostengono la ripetibilità del pattern, non ne misurano l'efficacia economica.

## Pattern T2 da verificare: intensità della domanda e ampliamento dell'allevamento

spbforce, D13:

- Episodio108505403: a H1 ci sono **due YARN_STORE**, lana238 e cassa14101; acquista il quarto quadrante a H2 e raggiunge17pecore a D20.
- Episodio108503246: a H1 c'è **un YARN_STORE**, lana ancora238 e cassa14260; non amplia.

La cassa è persino maggiore nel secondo caso e il prezzo della lana è uguale. Il solo prezzo istantaneo o una soglia minima di cassa non separano queste due decisioni. La molteplicità dei negozi, il portafoglio già scelto e la futura produzione avversaria sono candidati da approfondire. Ci sono anche differenze di mix e cronologia precedenti: non è una prova causale del numero di negozi. Il pattern di espansione non è ancora stato replicato su un campione separato.

## Pattern T3 da verificare: investimento colturale selettivo e tempo residuo

spbforce, D19:

- Episodio108504264: pomodoro87 e cassa45259 a H1; acquisto del quarto quadrante a H2 e dieci caselle di pomodoro seminate nello stesso giorno.
- Episodio108505285: cassa maggiore46073, ma pomodoro64; nessuna espansione.

Qui il prezzo è coerente con la scelta, ma non è stata identificata una soglia. Numero di negozi, domanda per pomodori, spazio disponibile e orizzonte biologico possono entrare insieme nella decisione. Un solo caso positivo non basta per attribuire un trigger. Non confondere questo piano con le due conversioni programmate di E20.9.

## Ipotesi aggiunta dall'utente: diversificazione preventiva

Alla semina sono osservabili il mercato attuale e la storia, non il prezzo futuro alla maturazione. **Diversificare a priori mix animale, colture, numero di caselle e date di raccolta è quindi una candidata protezione contro saturazione e incertezza.** Il rischio riguarda sia la nostra offerta sia quella avversaria. Una coltura redditizia oggi può arrivare sul mercato insieme a una grande produzione concorrente.

È un'ipotesi E22 aperta, non una conclusione dimostrata dal pilota. I top variano molto, ma questo non dice se la diversificazione fosse decisa a priori o in risposta alle osservazioni. Colture diverse richiedono semi, acqua, fertilizzante, viaggi e tempi diversi; dividere il campo in quote uguali non è una strategia automaticamente robusta. Anche animali diversi possono richiedere servizi contemporanei.

Confronto da preparare prima dell'implementazione:

1. Portafoglio concentrato di controllo, scelto senza vincoli delle versioni precedenti.
2. Portafoglio diversificato preventivamente, con quote e raccolte scaglionate definite prima della partita; regole operative fattibili.
3. Stessa diversificazione iniziale con aggiustamenti successivi guidati da domanda osservata, produzione propria/avversaria e tempo utile al ciclo.

Misurare cassa finale e margine contro avversari, risultati peggiori oltre alla media, produzione effettivamente venduta, prezzi realizzati, ricavi marginali delle vendite, picchi di lavoro e residui. I confronti devono avere protocolli e semi accoppiati, ma l'effetto sul mercato condiviso e sulla risposta avversaria va conservato. Non scegliere la variante soltanto perché produce un numero maggiore di specie.

## Integrazione colture–animali: autoconsumo del grano

Su indicazione dell'utente, il confronto dei portafogli deve includere il mangime prodotto internamente. Nel motore FEED consuma **un grano per animale nutrito**, non carote, pomodori, fragole o meloni. Il beneficio potenziale del grano non è quindi soltanto la vendita: può coprire il fabbisogno animale e ridurre acquisti e rischio di liquidità.

Vanno separate due decisioni economiche. Per grano già disponibile, trattenerlo per FEED rinuncia al ricavo di vendita ma può evitare un acquisto successivo. Per decidere quante caselle seminare a grano, confrontare gli acquisti evitabili con costi incrementali di seme, servizi e trasporto e con il valore netto della migliore alternativa su terreno e lavoro. Non sommare due volte lo stesso costo opportunità né contare il grano autoconsumato anche come ricavo di vendita.

La disponibilità mensile non garantisce autosufficienza: servono scorte prima dei FEED e accesso degli addetti al deposito. Vendite e riacquisti possono essere razionali se prezzi o liquidità lo richiedono, oppure sprechi del calendario: occorre ricostruire la sequenza. Raccolto e acquisti si mescolano nelle scorte; non si attribuisce automaticamente tutta la razione a produzione propria. Anche il fertilizzante animale usato sulle colture ha un valore d'uso e una vendita alternativa, da includere nel ciclo integrato.

L'audit dedicato riconcilia grano iniziale + raccolto + comprato = venduto + FEED riusciti + stock finale + scarti al cambio di giornata. I risparmi netti richiedono poi un confronto della policy: la contabilità fisica non è già una stima causale degli acquisti evitati.

## Priorità operativa

**kiki yi2** per isolare una scelta animale su un calendario relativamente stabile; **spbforce** per capire quando una scelta di specie diventa un cambiamento del numero di caselle e un'espansione. **Majkel1337** come controllo forte: verificare se la stessa logica economica resta valida in un piano più variabile.

Non servono, in questa fase, decine di top3000 trattati tutti allo stesso livello. Servono contrasti informativi della stessa submission: stesso prezzo ma domanda diversa; stessa domanda ma prezzo diverso; cassa maggiore senza investimento; stesso mix ma lavoro o giorni residui diversi. Congelare una spiegazione prima di cercare i replay successivi e conservare i controesempi.

La scelta della fascia è operativa, non un nuovo vincolo: se un caso3000 offre contrasti più leggibili, va studiato. Nessuna variante E22 è stata implementata o pubblicata in questa analisi.

## Audit del grano: primi risultati

Bilancio fisico del grano e cassa verificati in 28/30 replay del pilota. Medie per partita; la spesa indica monete effettivamente pagate, non risparmi stimati.

|Modello|Replay|Raccolto|Comprato|Venduto|FEED|Spesa acquisti|
|---|---|---|---|---|---|---|
|Olympus|5|514.2|139.8|312.4|309.6|4812.8|
|kiki yi2|5|516.8|289.2|446.4|358.6|9404.8|
|spbforce|5|560.0|188.4|362.2|385.0|6744.4|
|Majkel1337|4|621.0|211.0|504.5|311.0|8035.5|
|Mengfei Li|5|514.4|173.0|374.6|308.6|6263.2|
|THIRD FARM CLUB|4|459.2|169.5|243.8|381.8|6340.2|

Tutti i sei modelli producono, in media, più grano dei FEED, ma comprano e vendono quantità rilevanti. Questo non dimostra sprechi: prezzi, liquidità e disponibilità temporale possono giustificare gli scambi. La priorità è verificare la scorta prima dei servizi animali, confrontando trattenimento, vendita e riacquisto nello stesso intervallo. Le quantità non identificano univocamente la provenienza delle razioni.

Esclusi soltanto da questa tabella Majkel1337/108488494 (discrepanza inventario di 2 unità al passo 690) e THIRD FARM CLUB/108500556 (residuo fisico di 14 unità). Le discrepanze della ricostruzione restano aperte; non sono perdite attribuite agli agenti. I confronti economici fra modelli sono descrittivi e non accoppiati.

Dati: [FEED_SUMMARY.json](FEED_SUMMARY.json), dettagli giornalieri in `feed_profiles/`. Nessun risparmio netto ancora stimato: serve un controfattuale che includa mercato, terreno, lavoro, semi e ricavi rinunciati.
