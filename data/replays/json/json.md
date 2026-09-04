# JSON dei replay Kaggriculture

Questa è la cartella canonica del catalogo replay. I JSON grezzi sono cache
temporanee riscaricabili e sono esclusi da Git; il catalogo ne conserva Episode
ID, origine e SHA-256. Config, metriche derivate, freeze e ledger generati dai
runner restano nei rispettivi namespace e non devono essere copiati qui.

Regole:

- per i replay conservati localmente, nome file obbligatorio:
  `<EPISODE_ID>.json`;
- un solo file per Episode ID, senza suffissi `copy`, `new` o `replay`;
- prima dell'analisi verificare `info.EpisodeId`, schema, 720 step e stato
  terminale dei due player;
- registrare qui origine, SHA-256, ruolo epistemico e uso previsto;
- i replay sono evidenza offline: non possono essere feature online;
- un replay già usato per formulare o tarare una policy non è holdout.

Endpoint Kaggle:

`https://www.kaggle.com/competitions/episodes/<EPISODE_ID>/replay.json`

Ultimo aggiornamento: 2026-09-04.

## E18 — ciclo colturale e servizio della 6-6-2

Il replay `105080066.json` apre E18 come evidenza di training esterna. Il
primo corpus live aggiunge due replay Codex e otto episodi dei tre leader
correnti. Gli undici file grezzi sono stati rimossi dopo il freeze; restano
riscaricabili ed esclusi da Git, mentre metriche, timeline, hash e report
derivati sono versionati.

| Episode | SHA-256 | Ruolo | Seat Codex | Avversario | Score Codex | Score avversario | Esito | Seed |
|---:|---|---|---:|---|---:|---:|---|---:|
| `105080066` | `7AAEE0B4F43FFA5187C37FE8AEFF3FB9892D482CA20506C69B0C905552513F2C` | `E18_TRAINING_EVIDENCE` | P0 | Yusuf Murtaza | 59.861 | 77.364 | LOSS | 335.991.485 |
| `105084394` | `92715897D1D4EA495893C4ACEA757DE2B92AD5C422ABFF2CA32D5A3595911F5D` | `E18_TRAINING_EVIDENCE` | P1 | misaka12435 | 79.772 | 97.479 | LOSS | 1.111.570.727 |
| `105075696` | `516A4F8C218CCB7307BD5AF8860D1068A1A5571E609D8FF6175CB1BD4556B514` | `E18_TRAINING_EVIDENCE` | P0 | DhanaLakshmiMalla | 124.497 | 144.588 | LOSS | 880.107.967 |

Integrità verificata sugli undici replay: `schema_version=1`, gioco `0.1.0`, modulo
`1.32.7`, 720 step e stato terminale `DONE/DONE`. Origine per ogni file:
`https://www.kaggle.com/competitions/episodes/<EPISODE_ID>/replay.json`.

Uso autorizzato: analisi del ciclo `PLANT → WATER → HARVEST/DIG`, confronto
del backlog di servizio, rotazione late-game e liquidazione. Non è holdout e
non può essere presentato come validazione E18. L'analisi è in
`experiments/e18/reports/common/E18_EPISODE_105080066_CROP_LIFECYCLE_FORENSICS_IT.md`.

### Riferimenti esterni E18.2 da riacquisire

La submission Codex E18.2 `55991397` ha due sconfitte segnalate dal
proprietario negli episodi `105194141` e `105196165`. Le topologie avversarie
osservate sono complessivamente `6-6-2` e `6-7-0`; l'associazione puntuale fra
Episode ID e geometria non è congelata senza rilettura del replay.

I JSON non sono presenti nel working tree e non sono stati usati dal torneo
causale E18.3. SHA-256, seat, seed, score e identità dell'avversario restano
`PENDING_REACQUISITION`; prima di un'analisi frame-by-frame vanno riscaricati
dall'endpoint canonico e verificati. Il loro ruolo è
`EXTERNAL_DIAGNOSTIC_NOT_HOLDOUT`.

### E18.2 — replay recenti analizzati il 2026-09-04

La submission Codex E18.2 `55991397` è completa a rating `1215,9`. I quattro
replay più recenti al momento della rilevazione sono stati acquisiti,
verificati e analizzati; non sono holdout e i JSON grezzi non vengono
versionati.

| Episode | SHA-256 | Seat Codex | Avversario | Score Codex | Score avversario | Esito | Seed |
|---:|---|---:|---|---:|---:|---|---:|
| `105365487` | `A37225AD492D717562780627F04407A193F970E5EBEA0897EC6269E655DEBDE3` | P1 | Victor Hotz | 84.131 | 65.279 | WIN | 470.412.718 |
| `105355836` | `4C4B3DAD13B5830F90F1DE372152DC0607851E963B68D44617985276CD221D8F` | P0 | Emre Kurubaş | 49.202 | 59.609 | LOSS | 176.537.003 |
| `105331333` | `708F38AA0675C7CB744FDD8C39AAB6756E6226D628C6591B6934C41EF9F55874` | P1 | moonzfxs | 73.514 | 79.208 | LOSS | 1.802.484.503 |
| `105323917` | `942FEFC8098BB94A7C70FF4876611B084561E8827528276C6CA1427D13BAB3E1` | P1 | moonzfxs | 56.272 | 55.493 | WIN | 140.933.205 |

Integrità: `schema_version=1`, gioco `0.1.0`, modulo `1.32.7`, 720 step e
`DONE/DONE` in `4/4`. Report derivato:
`docs/model_specs/codex/e18/reports/E18_2_RECENT_KAGGLE_REPLAY_ANALYSIS_2026_09_04_IT.md`.

### Lotti Top 3 live acquisiti

Snapshot pubblico del 2026-09-03: `Crop Dusta` 2958,7; `3정훈` 2948,1;
`sbol ball` 2929,8.

| Team | Episode | SHA-256 | Seat | Avversario | Score | Score avversario | Esito | Seed |
|---|---:|---|---:|---|---:|---:|---|---:|
| Crop Dusta | `105089826` | `AEECD456138E4D68AA4B6B8A45D87EEB5C3E65854ADE950775B55A198674AF39` | P1 | 古德拜吃 | 77.084 | 83.358 | LOSS | 723.315.666 |
| 3정훈 | `105088610` | `F91D6DB6D6060DA2B930EA519C453C2BE33DA4ABA3C1731DC66C9D1B1F622AC3` | P1 | lilishyxf | 67.557 | 66.741 | WIN | 1.226.496.326 |
| sbol ball | `105090557` | `4070E283C0BA385BA5B70B68DCCD5127751A1ABDE157C3E26FE1FDC4EA1793B2` | P1 | senkin13 | 58.769 | 58.349 | WIN | 61.231.092 |
| Crop Dusta | `105100853` | `16005ED98E9E8ACA878F69C0335311E26CEE385635F00730ABDC895E065327A7` | P0 | gogogo | 88.934 | 71.752 | WIN | 1.381.221.242 |
| 3정훈 | `105101421` | `CC67346508AE25E28EA383921858019FD6F1C99E1D8AD21C8DB507F9656FD1E9` | P1 | Giulio Ravasio | 140.196 | 137.280 | WIN | 1.478.222.190 |
| sbol ball | `105102327` | `38BE4D52332E78E655C3D2F846E14D7BB7D2F9D7EF79B4966C446A00AD7E53AE` | P1 | Knight of Favonius | 98.962 | 94.575 | WIN | 1.849.936.055 |
| 3정훈 | `105107425` | `DEAA14B2DDC296960C523ECE827FFC8059CC539736500D3A3761C8F74151CB81` | P0 | Giulio Ravasio | 107.148 | 112.519 | LOSS | 2.015.767.011 |
| sbol ball | `105107748` | `5B12DFC3D46647D2D290B31E3B6C052FB877AF0624D60B966378B7F89C484ABA` | P0 | sky machine | 94.236 | 96.092 | LOSS | 76.877.491 |

Gli otto replay Top 3 sono acquisiti e analizzati. Ogni leader copre entrambi
i seat; 3정훈 e sbol ball hanno tre episodi ciascuno, Crop Dusta due. I file
grezzi sono stati rimossi dopo aver conservato qui gli SHA-256 e aver
verificato gli artefatti derivati. Il benchmark è in
`experiments/e18/reports/common/E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_IT.md`.

### Pulizia replay completata

Il 2026-09-03 il proprietario ha autorizzato la rimozione di tutti i replay
grezzi, perché recuperabili dall'endpoint Kaggle. Sono stati rimossi 29 JSON,
pari a 765,18 MiB nel working tree; il conteggio locale corrente è zero.

| Gruppo | File rimossi | MiB | Stato |
|---|---:|---:|---|
| E18 cache riscaricabile (`105*`) | 11 | 336,74 | rimossa; derivati E18 conservati |
| Training history (`101*`, `103*`, `104498819`) | 9 | 155,90 | rimossa dal HEAD; catalogo conservato |
| E17 Top-3 discovery (`104527555`–`104586487`) | 9 | 272,54 | rimossa dal HEAD; metriche e report conservati |

Una rimozione dal working tree non elimina automaticamente i blob dalla
cronologia `.git`. La storia non è stata riscritta: per recuperare anche quello
spazio servirebbe un'operazione distruttiva distinta, non autorizzata. Un nuovo
download va verificato contro lo SHA-256 catalogato prima del riuso.

## Codex E17.1 reattivo su Kaggle

- submission Kaggle: `559631298`;
- candidate: `submission/submission_codex_e17_reactive.py`;
- ruolo: `EXTERNAL_DIAGNOSTIC`, non holdout;
- campione acquisito e analizzato: 10 episodi, 5 vittorie e 5 sconfitte;
- copertura seat: 5 episodi P0 e 5 episodi P1;
- diversità: 10 seed e 10 avversari distinti;
- integrità: filename/Episode ID coerenti, 720 step e `DONE/DONE` in 10/10.

I dieci JSON grezzi di questo campione non sono versionati: dopo il freeze
delle metriche derivate sono stati rimossi perché pesanti e integralmente
riscaricabili dall'endpoint Kaggle usando gli Episode ID sotto. Gli SHA-256
permettono di verificare una nuova acquisizione byte per byte.

L'analisi principale è completata in
`docs/model_specs/codex/e17/reports/E17_REACTIVE_EXTERNAL_REPLAY_BENCHMARK_IT.md`.
Confronta, dal giorno di apertura Q2 a D28, animal-tile-days, specie, quota
crop e movimento di Q2 rispetto a Q0. D29 è separato per non confondere la
topologia produttiva con la liquidazione terminale. Il risultato centrale è
Q2/Q0 `63,29%`, con zero fughe e un solo action-stream richiesto nei dieci
episodi; le quattro traiettorie strutturali osservate riflettono differenze di
stato senza una divergenza della sequenza di comandi.

| Episode | SHA-256 | Seat | Avversario | Score Codex | Score avversario | Esito | Seed |
|---:|---|---:|---|---:|---:|---|---:|
| `104857899` | `4510BE03B969C5B74F8ABF16A1EFDEC59A28E3DB9E10C17CE0E9DA38EC644614` | P0 | Venneth | 63.709 | 75.505 | LOSS | 1.517.744.047 |
| `104860472` | `88AE4B6801C388CA58681957E9E8132AB9F8233BB19247347E51006EE130CA32` | P1 | Artyom Sayapin | 97.285 | 111.893 | LOSS | 1.614.219.005 |
| `104863004` | `20F6AB66E805E9F3DED05272236FA9A8C4969270C73D8D528BEF3CAE5E980BF8` | P1 | seowoohyeon | 120.014 | 124.145 | LOSS | 813.713.601 |
| `104863880` | `85F8EAFD5C12ED0AD8F179BA14CB6F05D28860C519B839C190A32AB2086FD0D3` | P1 | tongmian1314 | 42.850 | 44.785 | LOSS | 1.531.511.900 |
| `104864729` | `41A9C8B8378B52258B2A828160281481C8222014298A58FCC31BC7FF291029B5` | P1 | Jose Santiago Echevarria | 68.449 | 65.424 | WIN | 1.569.994.068 |
| `104865577` | `1F085D0B35F0A46726614B1D033831B47AE5A98983174F4EF0C19760EF8FB2C6` | P0 | Dante Dyches-Chandler | 78.228 | 71.949 | WIN | 1.807.770.918 |
| `104866465` | `D81C6B2B6BC2B4E45AD66679BA1A1FCC0CEF1D6F0D8052294781B8005F8D2CB7` | P0 | xubenzheng | 86.857 | 66.584 | WIN | 326.166.254 |
| `104867319` | `7C5925C62E380CA3DD70548FA3053E19E92CE865344BE16EA728D740DC20AE72` | P1 | Joseph Franck | 101.913 | 110.973 | LOSS | 1.123.713.816 |
| `104868160` | `0AF742E0AAD069531A53DDE05464735C1ACB3274F2A2319D8D4ABF31F487DE1F` | P0 | Operator-X | 83.846 | 55.433 | WIN | 68.591.884 |
| `104869022` | `5989D506B7570DA31D1625DC055D267DB2B0D2586210BD431DF1402A43D623D6` | P0 | SireeshLimbu | 44.936 | 34.785 | WIN | 785.063.514 |

Lo score medio Codex è `78.808,7`; nelle sconfitte è `85.154,2`, mentre
nelle vittorie è `72.463,2`. L'inversione dimostra che l'esito relativo non
può sostituire le metriche economiche e topologiche del benchmark.

## E17 — benchmark osservazionale Top 3

Corpus di discovery composto da **9 episodi Kaggriculture unici**. La
classifica osservata al momento della raccolta era:

1. `tetsuya` — rating leaderboard 2947.0;
2. `OceanMix` — rating leaderboard 2875.8;
3. `Crop Dusta` — rating leaderboard 2869.0.

Proprietà comuni verificate:

- `schema_version = 1`;
- `version = 0.1.0`;
- `module_version = 1.32.7`;
- 720 step, 24 turni/giorno, 30 giorni;
- stato finale `DONE / DONE` per tutti gli episodi;
- corrispondenza esatta tra nome file ed `info.EpisodeId`;
- nessun duplicato nel corpus;
- dimensione complessiva approssimativa: 272.54 MiB.

### Integrità e ruolo epistemico

Origine di ogni replay: endpoint Kaggle indicato sopra, acquisito prima del
freeze E17. I file sono input offline immutabili e non possono essere usati
come feature online.

| Replay / cache | SHA-256 | Ruolo |
|---|---|---|
| `104527555.json` | `25CD7C23EE8AE5FF83A80CD98F0314F25E3011D14636BD547A4341084E509BB7` | `DISCOVERY` |
| `104541810.json` | `A1994D0D8F1224424AB7B95FEE6B72545ECE55E557819B07A24C5F382C4DE1D3` | `DISCOVERY` |
| `104543983.json` | `EA1F53BD0BF8FE60264944A3A943F65B6F538A6C5C92BCC3E33D329AD01B7BAA` | `DISCOVERY` |
| `104547425.json` | `2AED6EBB189D21B86705AD367FE3EAB1D67EBDBC4F301E19297BE5B04D509ED3` | `DISCOVERY` |
| `104564762.json` | `5EAA3F6941A1364C326067DD81217BE6A68E8E44612586412830061F546DC21E` | `DISCOVERY` |
| `104577270.json` | `D85695BBC9B56521CAA11945789B486208FC3DA66A55DCB66FD2A0658937B267` | `DISCOVERY` |
| `104578185.json` | `D3179A6AF500E18BD398EE662178F9AD5F65846F68DD7620868A6B48533C4CB5` | `DISCOVERY` |
| `104586335.json` | `74DE13CEC7D9F235A908A1BBAAA466BB733EBA04A551A9EC9C02DEC917B5B077` | `DISCOVERY` |
| `104586487.json` | `6248287CE0C1E6B3C29936B8DE3E8907C05F36F15831D2210B255051F5EA883C` | `DISCOVERY` |
| `101294736.json` | `6281FDD32497C9DB28E3D924AD8A55B12F841A5B1309164328679AA4F5EE8695` | `TRAINING_HISTORY` |
| `101705751.json` | `79BE341C03A5F471BAAA28CF6419FF89D85C06FC88DE50901C5C1E3DA92AC6B3` | `TRAINING_HISTORY` |
| `101717011.json` | `F298356EBE1BF9E7AAD4ACFF32A6114DB4F015F90F613E8E913565913494F3B9` | `TRAINING_HISTORY` |
| `101971376.json` | `7AFDF3B8672C1828BF7520E8F5973F69AD11E8378155A77AA7C4B5EAF4480DB4` | `TRAINING_HISTORY` |
| `103462357.json` | `668292C0012B69B09B072A96A8A24AFE315F203000239CBA5B377EAFD96602AA` | `TRAINING_HISTORY` |
| `103464592.json` | `60701A7C56CABE3382382FB6BEC7BBE4E3226A3C023527847074A6BDC17E260E` | `TRAINING_HISTORY` |
| `103473619.json` | `D9255994E7181724CEA5E93FEFD059C3E312EAAF5EB15095288715BDB90A9960` | `TRAINING_HISTORY` |
| `103484828.json` | `36FD45C584D7B9434FB1F783BD61AADAA345B67B1A3EE02FEC436ACE0E4C4F49` | `TRAINING_HISTORY` |
| `104498819.json` | `28BB77B8F6BEF86422354893C7CF9F7371C201EC6F1F379D4196D3AA841FE98B` | `TRAINING_HISTORY` |
| Kaggle `104857899` (cache non versionata) | `4510BE03B969C5B74F8ABF16A1EFDEC59A28E3DB9E10C17CE0E9DA38EC644614` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104860472` (cache non versionata) | `88AE4B6801C388CA58681957E9E8132AB9F8233BB19247347E51006EE130CA32` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104863004` (cache non versionata) | `20F6AB66E805E9F3DED05272236FA9A8C4969270C73D8D528BEF3CAE5E980BF8` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104863880` (cache non versionata) | `85F8EAFD5C12ED0AD8F179BA14CB6F05D28860C519B839C190A32AB2086FD0D3` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104864729` (cache non versionata) | `41A9C8B8378B52258B2A828160281481C8222014298A58FCC31BC7FF291029B5` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104865577` (cache non versionata) | `1F085D0B35F0A46726614B1D033831B47AE5A98983174F4EF0C19760EF8FB2C6` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104866465` (cache non versionata) | `D81C6B2B6BC2B4E45AD66679BA1A1FCC0CEF1D6F0D8052294781B8005F8D2CB7` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104867319` (cache non versionata) | `7C5925C62E380CA3DD70548FA3053E19E92CE865344BE16EA728D740DC20AE72` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104868160` (cache non versionata) | `0AF742E0AAD069531A53DDE05464735C1ACB3274F2A2319D8D4ABF31F487DE1F` | `EXTERNAL_DIAGNOSTIC` |
| Kaggle `104869022` (cache non versionata) | `5989D506B7570DA31D1625DC055D267DB2B0D2586210BD431DF1402A43D623D6` | `EXTERNAL_DIAGNOSTIC` |

| Episode ID | Agente A | Score A | Agente B | Score B | Risultato finale | Margine | Seed |
|---:|---|---:|---|---:|---|---:|---:|
| `104527555` | **tetsuya** | 81,050 | Driz Lo | 52,953 | tetsuya vince | +28,097 | 1,528,678,515 |
| `104541810` | **tetsuya** | 109,204 | QQ Farming | 97,241 | tetsuya vince | +11,963 | 1,966,088,317 |
| `104543983` | **Crop Dusta** | 83,634 | **tetsuya** | 76,264 | Crop Dusta vince | +7,370 | 782,592,907 |
| `104547425` | **OceanMix** | 114,361 | **Crop Dusta** | 106,328 | OceanMix vince | +8,033 | 394,646,827 |
| `104564762` | Driz Lo | 90,185 | **Crop Dusta** | 87,152 | Driz Lo vince | +3,033 | 1,014,643,766 |
| `104577270` | yukino | 90,053 | **OceanMix** | 86,580 | yukino vince | +3,473 | 620,836,918 |
| `104578185` | **tetsuya** | 119,754 | **Crop Dusta** | 114,881 | tetsuya vince | +4,873 | 533,536,224 |
| `104586335` | **Crop Dusta** | 64,811 | **OceanMix** | 51,238 | Crop Dusta vince | +13,573 | 1,554,265,238 |
| `104586487` | **OceanMix** | 77,962 | Driz Lo | 75,760 | OceanMix vince | +2,202 | 1,015,196,962 |

### Copertura dei tre agenti target

| Agente target | Episodi | Vittorie | Sconfitte | Score medio | Score mediano | Differenziale medio |
|---|---:|---:|---:|---:|---:|---:|
| tetsuya | 4 | 3 | 1 | 96,568.00 | 95,127.00 | +9,390.75 |
| OceanMix | 4 | 2 | 2 | 82,535.25 | 82,271.00 | -1,702.75 |
| Crop Dusta | 5 | 2 | 3 | 91,361.20 | 87,152.00 | +1,000.80 |

### Struttura del campione

- 4 episodi sono scontri diretti fra agenti della Top 3;
- 5 episodi oppongono un agente Top 3 a un agente esterno;
- tetsuya e Crop Dusta si affrontano due volte, con record 1–1;
- OceanMix e Crop Dusta si affrontano due volte, con record 1–1;
- non è presente uno scontro diretto tetsuya–OceanMix;
- il campione è adatto alla discovery e alla formulazione di ipotesi, non
  alla stima causale definitiva o alla dichiarazione di un optimum.

Gli score della tabella sono i punteggi finali degli episodi, non i rating
della leaderboard. Poiché i due agenti condividono mercato e dinamica di
partita, ogni confronto deve distinguere osservazione, inferenza e causa.

## Baseline storiche catalogate — file grezzi rimossi

| Periodo | Profilo annotato | Episode ID | Nota storica |
|---|---|---:|---|
| pre-30/8 | Q0 | `101717011` | Codex vs Alexander Sokolov; score Codex 50,420 |
| pre-30/8 | Q1 | `101294736` | Codex vs truebelief; score Codex 86,297 |
| pre-30/8 | Q1 | `101705751` | Codex vs Dr. Mikholae; score Codex 90,137 |
| pre-30/8 | espansione | `101971376` | Codex vs Harith Al-Ani; score Codex 133,049 |
| 30/8 | Q0 | `103484828` | Antigravity vs LuCcc; score Antigravity 56,772; attenzione alla periodicità |
| 30/8 | Q2 | `103473619` | Antigravity vs Gordeev; score Antigravity 88,648 |
| 30/8 | Q2 | `103462357` | Antigravity vs Dipin; score Antigravity 95,496 |
| 30/8 | Q3 | `103464592` | Antigravity vs Petar; score Antigravity 95,475 |
| 1/9 | 3Q | `104498819` | Codex vs keiz; score Codex 158,575 |

## Replay rimossi dal working tree

Restano recuperabili dalla cronologia Git, ma non fanno parte del corpus
attivo:

- `101462495.json` — Crop Dusta vs Ryo Hasegawa;
- `101761797.json` — Ryo Hasegawa vs Crop Dusta;
- `101891362.json` — Subramanya vs Crop Dusta;
- `104515697.json` — Antigravity vs zzy123123; annotato come caso di
  buco centrale.

Il replay `55929317.json` è stato escluso perché apparteneva a ConnectX.
Il replay Kaggriculture `104533574.json` è stato escluso per mantenere il
corpus E17 a nove episodi con copertura più equilibrata dei tre agenti
target.

La seconda copia E12 di `101294736.json` era stata rimossa dopo verifica di
identità SHA-256. Oggi l'entry canonica è questa riga di catalogo; nessuna copia
grezza è conservata nel working tree.
