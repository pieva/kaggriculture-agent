# E22 · tre pascoli Q0, 8C9S

Braccio interno 8C9S contro E22 congelata, submission 56206528. Tre pascoli Q0 in (4,1), (3,2), (2,3), tutti occupati da pecore; restano le 8 mucche e le 6 pecore originarie. Non replica il caso 6C10S della submission 56165125, che lascia (4,1) vuoto. Il confronto misura il pacchetto strutture, sostituzione animali e servizio/vendite adattati, non il solo tipo di struttura.

Partite dirette a seed accoppiati nei due ruoli, una simulazione alla volta. Seed esposti 180911301–307; conferma 180912401–407 solo dopo il congelamento. Mercato condiviso: le vendite cambiano i prezzi di entrambi. KPI di flusso attribuiti al giorno dell’azione; cassa, animali e scorte alle osservazioni H24 (prima dell’ultima azione del giorno salvo D30 terminale). Prezzi giornalieri ponderati sulle unità effettivamente vendute; assenza vendite = dato mancante.

## Decisione

Non promuovere 8C9S v1: il vantaggio non è regolare tra i seed. Margine medio +353.1, mediana -2092.0, vittorie 4/14; i due ruoli replicano lo stesso esito per seed e non costituiscono 14 osservazioni indipendenti. Questa è una decisione diagnostica sui risultati esposti, non un criterio statistico preregistrato. Non usare i seed 180912401–407 per questo candidato; restano riservati alla conferma di una futura variante congelata. Nessuna pubblicazione Kaggle. La replica 6C10S resta distinta e non implementata in questo braccio. Il calendario ripetuto nei replay esterni è documentato nel report delle traiettorie, ma non dimostra la convenienza del mix 8C9S.

| Fase | Vittorie | Margine medio | Mediana | Min | Max |
|---|---:|---:|---:|---:|---:|
| exposed | 4/14 | 353.1 | -2092.0 | -4626.0 | 10376.0 |

## KPI medi: candidato meno E22

| KPI | exposed |
|---|---:|
| labor | +0.0 |
| purchases | +600.0 |
| sales | +953.1 |
| purchase_cash:BUY_PRODUCT:WHEAT | +0.0 |
| bought_units:BUY_PRODUCT:WHEAT | +0.0 |
| harvested:WHEAT | +0.0 |
| harvested:MILK | +0.0 |
| harvested:WOOL | +64.0 |
| harvested:EGG | -78.0 |
| sales_cash:MILK | +0.0 |
| sales_cash:WOOL | +5006.7 |
| sales_cash:EGG | -4067.6 |
| sales_cash:FERTILIZER | +14.0 |

## Controlli e limiti

Caricatore reale da file per entrambi gli agenti, 720 stati e stato DONE. Audit cassa sulle 719 transizioni per entrambi i lati; controllo invariato per 719/719 azioni in ogni partita. Tre strutture e mix finale 8C9S verificati; zero fughe. Nessuna partita di conferma eseguita. Le quantità massime degli ordini SELL WOOL sono ampliate anche prima di D11: i primi dieci giorni conservano le azioni degli operai, ma non necessariamente identici incassi, per il regolamento per-unità del mercato condiviso. Questo braccio misura anche tale modifica alle vendite. Tutto il latte e la lana raccolti sono venduti; a D30 restano due unità di fertilizzante trasportate, nessun latte/lana/uova in magazzino, sugli operai o sulle caselle.

[Dashboard D1–D30](REPORT.html) · [CSV giornaliero](DAILY_KPI.csv) · [Protocollo](PROTOCOL.json) · [Sintesi](SUMMARY.json)

| Seed | Ruolo candidato | Cassa candidato | Cassa E22 | Margine |
|---|---:|---:|---:|---:|
| 180911301 | 0 | 108375.0 | 101300.0 | 7075.0 |
| 180911301 | 1 | 108375.0 | 101300.0 | 7075.0 |
| 180911302 | 0 | 52663.0 | 54723.0 | -2060.0 |
| 180911302 | 1 | 52663.0 | 54723.0 | -2060.0 |
| 180911303 | 0 | 87495.0 | 91604.0 | -4109.0 |
| 180911303 | 1 | 87495.0 | 91604.0 | -4109.0 |
| 180911304 | 0 | 130786.0 | 132878.0 | -2092.0 |
| 180911304 | 1 | 130786.0 | 132878.0 | -2092.0 |
| 180911305 | 0 | 84498.0 | 86590.0 | -2092.0 |
| 180911305 | 1 | 84498.0 | 86590.0 | -2092.0 |
| 180911306 | 0 | 79246.0 | 83872.0 | -4626.0 |
| 180911306 | 1 | 79246.0 | 83872.0 | -4626.0 |
| 180911307 | 0 | 107832.0 | 97456.0 | 10376.0 |
| 180911307 | 1 | 107832.0 | 97456.0 | 10376.0 |
