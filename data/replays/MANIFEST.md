# Catalogo replay benchmark

Endpoint Kaggle:

`https://www.kaggle.com/competitions/episodes/<EPISODE_ID>/replay.json`

Ultimo aggiornamento: 2026-09-01.

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

| Percorso | SHA-256 | Ruolo |
|---|---|---|
| `e17-discovery/104527555.json` | `25CD7C23EE8AE5FF83A80CD98F0314F25E3011D14636BD547A4341084E509BB7` | `DISCOVERY` |
| `e17-discovery/104541810.json` | `A1994D0D8F1224424AB7B95FEE6B72545ECE55E557819B07A24C5F382C4DE1D3` | `DISCOVERY` |
| `e17-discovery/104543983.json` | `EA1F53BD0BF8FE60264944A3A943F65B6F538A6C5C92BCC3E33D329AD01B7BAA` | `DISCOVERY` |
| `e17-discovery/104547425.json` | `2AED6EBB189D21B86705AD367FE3EAB1D67EBDBC4F301E19297BE5B04D509ED3` | `DISCOVERY` |
| `e17-discovery/104564762.json` | `5EAA3F6941A1364C326067DD81217BE6A68E8E44612586412830061F546DC21E` | `DISCOVERY` |
| `e17-discovery/104577270.json` | `D85695BBC9B56521CAA11945789B486208FC3DA66A55DCB66FD2A0658937B267` | `DISCOVERY` |
| `e17-discovery/104578185.json` | `D3179A6AF500E18BD398EE662178F9AD5F65846F68DD7620868A6B48533C4CB5` | `DISCOVERY` |
| `e17-discovery/104586335.json` | `74DE13CEC7D9F235A908A1BBAAA466BB733EBA04A551A9EC9C02DEC917B5B077` | `DISCOVERY` |
| `e17-discovery/104586487.json` | `6248287CE0C1E6B3C29936B8DE3E8907C05F36F15831D2210B255051F5EA883C` | `DISCOVERY` |
| `reference/101294736.json` | `6281FDD32497C9DB28E3D924AD8A55B12F841A5B1309164328679AA4F5EE8695` | `TRAINING_HISTORY` |
| `reference/101705751.json` | `79BE341C03A5F471BAAA28CF6419FF89D85C06FC88DE50901C5C1E3DA92AC6B3` | `TRAINING_HISTORY` |
| `reference/101717011.json` | `F298356EBE1BF9E7AAD4ACFF32A6114DB4F015F90F613E8E913565913494F3B9` | `TRAINING_HISTORY` |
| `reference/101971376.json` | `7AFDF3B8672C1828BF7520E8F5973F69AD11E8378155A77AA7C4B5EAF4480DB4` | `TRAINING_HISTORY` |
| `reference/103462357.json` | `668292C0012B69B09B072A96A8A24AFE315F203000239CBA5B377EAFD96602AA` | `TRAINING_HISTORY` |
| `reference/103464592.json` | `60701A7C56CABE3382382FB6BEC7BBE4E3226A3C023527847074A6BDC17E260E` | `TRAINING_HISTORY` |
| `reference/103473619.json` | `D9255994E7181724CEA5E93FEFD059C3E312EAAF5EB15095288715BDB90A9960` | `TRAINING_HISTORY` |
| `reference/103484828.json` | `36FD45C584D7B9434FB1F783BD61AADAA345B67B1A3EE02FEC436ACE0E4C4F49` | `TRAINING_HISTORY` |
| `reference/104498819.json` | `28BB77B8F6BEF86422354893C7CF9F7371C201EC6F1F379D4196D3AA841FE98B` | `TRAINING_HISTORY` |

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

## Baseline storiche ancora presenti

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
