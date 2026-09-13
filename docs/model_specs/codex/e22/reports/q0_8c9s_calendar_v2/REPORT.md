# E22 · tre pascoli Q0, 8C9S

Braccio interno 8C9S contro E22 congelata, submission 56206528. Tre pascoli Q0 in (4,1), (3,2), (2,3), tutti occupati da pecore; restano le 8 mucche e le 6 pecore originarie. Non replica il caso 6C10S della submission 56165125, che lascia (4,1) vuoto. Il confronto misura il pacchetto strutture, sostituzione animali e servizio/vendite adattati, non il solo tipo di struttura.

Partite dirette a seed accoppiati nei due ruoli, una simulazione alla volta. Seed esposti 180911301–307; conferma 180912401–407 solo dopo il congelamento. Mercato condiviso: le vendite cambiano i prezzi di entrambi. KPI di flusso attribuiti al giorno dell’azione; cassa, animali e scorte alle osservazioni H24 (prima dell’ultima azione del giorno salvo D30 terminale). Prezzi giornalieri ponderati sulle unità effettivamente vendute; assenza vendite = dato mancante.

## Decisione

Non promuovere 8C9S calendario v2: il vantaggio non è regolare tra i seed. Margine medio +130.6, mediana -2324.0, vittorie 4/14; i due ruoli replicano lo stesso esito per seed e non costituiscono 14 osservazioni indipendenti. Questa è una decisione diagnostica sui risultati esposti, non un criterio statistico preregistrato. Non usare i seed 180912401–407 per questo candidato; restano riservati alla conferma di una futura variante congelata. Nessuna pubblicazione Kaggle. La replica 6C10S resta distinta e non implementata in questo braccio. Il calendario ripetuto nei replay esterni è documentato nel report delle traiettorie, ma non dimostra la convenienza del mix 8C9S.

| Fase | Vittorie | Margine medio | Mediana | Min | Max |
|---|---:|---:|---:|---:|---:|
| exposed | 4/14 | 130.6 | -2324.0 | -4802.0 | 10190.0 |

## KPI medi: candidato meno E22

| KPI | exposed |
|---|---:|
| labor | +0.0 |
| purchases | +600.0 |
| sales | +730.6 |
| purchase_cash:BUY_PRODUCT:WHEAT | +0.0 |
| bought_units:BUY_PRODUCT:WHEAT | +0.0 |
| harvested:WHEAT | +0.0 |
| harvested:MILK | +0.0 |
| harvested:WOOL | +64.0 |
| harvested:EGG | -78.0 |
| sales_cash:MILK | -53.7 |
| sales_cash:WOOL | +4965.9 |
| sales_cash:EGG | -4067.6 |
| sales_cash:FERTILIZER | -114.0 |

## Controlli e limiti

Caricatore reale da file per entrambi gli agenti, 720 stati e stato DONE. Audit cassa sulle 719 transizioni per entrambi i lati; controllo invariato per 719/719 azioni in ogni partita. Tre strutture e mix finale 8C9S verificati; zero fughe. Nessuna partita di conferma eseguita. Le quantità massime degli ordini SELL WOOL sono ampliate anche prima di D11: i primi dieci giorni conservano le azioni degli operai, ma non necessariamente identici incassi, per il regolamento per-unità del mercato condiviso. Questo braccio misura anche tale modifica alle vendite. Tutto il latte e la lana raccolti sono venduti; a D30 restano due unità di fertilizzante trasportate, nessun latte/lana/uova in magazzino, sugli operai o sulle caselle.

[Dashboard D1–D30](REPORT.html) · [CSV giornaliero](DAILY_KPI.csv) · [Protocollo](PROTOCOL.json) · [Sintesi](SUMMARY.json)

| Seed | Ruolo candidato | Cassa candidato | Cassa E22 | Margine |
|---|---:|---:|---:|---:|
| 180911301 | 0 | 108151.0 | 101336.0 | 6815.0 |
| 180911301 | 1 | 108151.0 | 101336.0 | 6815.0 |
| 180911302 | 0 | 52469.0 | 54793.0 | -2324.0 |
| 180911302 | 1 | 52469.0 | 54793.0 | -2324.0 |
| 180911303 | 0 | 87389.0 | 91700.0 | -4311.0 |
| 180911303 | 1 | 87389.0 | 91700.0 | -4311.0 |
| 180911304 | 0 | 130629.0 | 132927.0 | -2298.0 |
| 180911304 | 1 | 130629.0 | 132927.0 | -2298.0 |
| 180911305 | 0 | 84304.0 | 86660.0 | -2356.0 |
| 180911305 | 1 | 84304.0 | 86660.0 | -2356.0 |
| 180911306 | 0 | 79174.0 | 83976.0 | -4802.0 |
| 180911306 | 1 | 79174.0 | 83976.0 | -4802.0 |
| 180911307 | 0 | 107734.0 | 97544.0 | 10190.0 |
| 180911307 | 1 | 107734.0 | 97544.0 | 10190.0 |

## Calendario adottato e confronto con v1

Calendario esterno applicato alle tre pecore: (3,2) D11 H20, (4,1) D11 H21, (2,3) D12 H7. Raccolte delle prime due a D17/20/23/26/29; della terza a D18/21/24/27/30. Le ore di raccolta sfruttano i nostri percorsi e non copiano un intero piano avversario. Le raccolte con resa presente hanno precedenza sugli altri servizi nei giorni previsti; alimentazione e cure continuano negli slot disponibili. La v1 ritardava le prime due ultime raccolte a D30. Il collocamento anticipato nella stessa giornata non cambia da solo l’età produttiva nel motore. A D12 l’acquisto della pecora passa da H2 a H1, l’operaio 1 la colloca a H7 e consegna il latte a H11; l’operaio 6 conserva il percorso di alimentazione. Nessuna assunzione aggiuntiva. Due slot di raccolta fertilizzante D12 sono rimossi per far spazio al tragitto. La logica di vendita lana v1, inclusa quella precedente a D11, rimane invariata.

Rispetto alla v1, il margine contro E22 migliora in 0/14 partite; differenza media -222.6, mediana -206.0. Differenza media della sola cassa del candidato -149.3. Sono confronti su seed e ruoli accoppiati contro E22, non partite dirette v1-v2. La differenza dei margini comprende anche la variazione degli incassi del controllo nel mercato condiviso.

| Seed | Ruolo | Margine v1 | Margine v2 | Delta |
|---|---:|---:|---:|---:|
| 180911301 | 0 | +7075 | +6815 | -260 |
| 180911301 | 1 | +7075 | +6815 | -260 |
| 180911302 | 0 | -2060 | -2324 | -264 |
| 180911302 | 1 | -2060 | -2324 | -264 |
| 180911303 | 0 | -4109 | -4311 | -202 |
| 180911303 | 1 | -4109 | -4311 | -202 |
| 180911304 | 0 | -2092 | -2298 | -206 |
| 180911304 | 1 | -2092 | -2298 | -206 |
| 180911305 | 0 | -2092 | -2356 | -264 |
| 180911305 | 1 | -2092 | -2356 | -264 |
| 180911306 | 0 | -4626 | -4802 | -176 |
| 180911306 | 1 | -4626 | -4802 | -176 |
| 180911307 | 0 | +10376 | +10190 | -186 |
| 180911307 | 1 | +10376 | +10190 | -186 |

[Confronto v1 JSON](VS_V1.json). I controlli per casella, compresi ore e quantità, sono nei risultati di ogni partita.
