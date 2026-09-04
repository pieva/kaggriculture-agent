# E18 — benchmark latest contro E17 V4D

## Decisione

La regressione è confermata localmente e non è marginale.

L'esatto bundle E18.1 perde `14-0` contro
`submission_codex_e17_v4d.py`: `71.831,00` contro `89.760,57`, delta
`-17.929,57` (`-19,97%`). Sul pool comune Claude/Copilot/Antigravity E18.1
vale `125.983,74`, mentre V4D vale `143.486,45`: delta `-17.502,71`
(`-12,20%`). V4D vince anche tutti i 42 nuovi match contro il pool comune.

E18.1 resta una diagnostica architetturale, non una baseline competitiva. Per
la prossima versione, V4D deve tornare a essere il controllo economico. Non è
giustificato estendere o inviare un'altra variante 6-6-2/7-7-0 prima di aver
recuperato il gap.

## Protocollo

- bundle esatti:
  - `submission/submission_codex_e18_opponent_reactive_662_770.py`;
  - `submission/submission_codex_e17_v4d.py`;
- sette seed development E18 `180903001`-`180903007`;
- entrambi i seat;
- 14 match diretti;
- 42 match V4D contro gli stessi Claude E18.1, Copilot E18.1 e Antigravity
  E17 usati dal torneo a quattro;
- confronto E18 sul pool comune riusato dall'artifact congelato V2;
- 56 nuovi match, zero holdout/final.

Al primo tentativo il browser Kaggle autenticato non era leggibile a causa di
un controllo di sicurezza transitorio dell'app. Un nuovo accesso nella stessa
sessione è riuscito: lo snapshot pubblico mostra E18.1 a `825,4`, V4D a
`1.131,7` e la 6-6-2 E17.3 a `941,4`. Il delta E18.1/V4D è quindi `-306,3`
(`-27,07%`). Questo dato esterno corrobora il segno del benchmark locale ma
non ne modifica protocollo o risultati.

## Risultato diretto

| KPI | E18.1 latest | E17 V4D | Delta latest |
|---|---:|---:|---:|
| Record | 0-14 | 14-0 | — |
| Denaro medio | 71.831,00 | 89.760,57 | -17.929,57 (-19,97%) |
| Mediana | 68.931 | 95.159 | -26.228 |
| Range | 36.818-108.978 | 42.491-121.862 | — |
| Animali finali | 15,00 | 19,00 | -4 (-21,05%) |
| Crop finali | 13,43 | 14,86 | -1,43 (-9,62%) |
| Weed finali | 14,00 | 7,00 | +7 (+100%) |
| Crop tile-days | 1.278,14 | 1.252,86 | +25,29 (+2,02%) |
| Crop tile-days D21-D30 | 493,14 | 473,86 | +19,29 (+4,07%) |
| Weed tile-days | 63,00 | 15,00 | +48 (+320%) |
| Weed tile-days D21-D30 | 43,00 | 15,00 | +28 (+186,67%) |
| Azioni produttive | 2.617,43 | 2.787,86 | -170,43 (-6,11%) |
| PASS | 872,14 | 699,00 | +173,14 (+24,77%) |
| MOVE/produttiva | 1,374 | 1,291 | +6,46% peggiore |
| Perdite verificate | 0 | 0 | pari |
| Errori/fallback | 0/0 | 0/0 | pari |

Il delta per seed è seat-simmetrico e sempre favorevole a V4D: `5.673`,
`11.789`, `26.228`, `9.816`, `12.884`, `24.527`, `34.590`.

## Pool comune

| Avversario | E18.1 | V4D | Delta E18.1 |
|---|---:|---:|---:|
| Claude E18.1 | 139.404,57 | 157.262,86 | -17.858,29 (-11,36%) |
| Copilot E18.1 | 116.762,71 | 129.449,57 | -12.686,86 (-9,80%) |
| Antigravity E17 | 121.783,93 | 143.746,93 | -21.963,00 (-15,28%) |
| **Complessivo** | **125.983,74** | **143.486,45** | **-17.502,71 (-12,20%)** |

Non emerge un matchup in cui la latest compensi il sacrificio economico.

## Cosa cambia davvero

### 1. Il selector non è attivo nel confronto rilevante

Contro V4D E18.1 osserva sempre pressione `4,95`, sotto soglia `8`, e sceglie
`6-6-2` in 14/14. Anche nel torneo a quattro aveva scelto `6-6-2` in 42/42.
Il bundle è formalmente reattivo ma, nel pool corrente, si comporta come una
sola architettura statica.

### 2. Le cinque celle recuperate non compensano i cinque pascoli rimossi

E18.1 chiude con topologia piena `6-6-2` e 15 animali; V4D costruisce
`7-7-5`, riempie `7-6-5` e chiude con 19 animali complessivi. E18.1 ottiene
3,57 crop di picco in più e il 2,02% di crop tile-days in più, ma termina con
1,43 crop in meno e vende quantità richieste complessive leggermente inferiori.

Le azioni aggiuntive sulle colture sono soprattutto `WATER` (`+80`), mentre
gli `HARVEST` scendono di 9,43. Le celle recuperate assorbono servizio ma non
generano abbastanza raccolto terminale.

### 3. La manodopera liberata diventa inattività

Rispetto a V4D, E18.1 perde in media 170,43 azioni produttive e aggiunge
173,14 `PASS`, a movimenti quasi invariati (`-1,71`). È la falsificazione
diretta dell'ipotesi iniziale: ridurre l'allevamento non ha liberato lavoro
utilmente riallocato alle colture.

Le principali azioni eliminate sono `CARE -85`, `FEED -87` e
`COLLECT_FERTILIZER -69`; l'incremento `WATER +80` e `PLANT +5` non compensa
la produzione persa. Anche gli `HARVEST` calano.

### 4. La superficie aggiuntiva degrada in weed

E18.1 raddoppia le weed finali e quadruplica i weed tile-days. Sul seed
`180903007`, le weed compaiono già al D14 e arrivano a 14 al D30; V4D resta a
zero fino al D23 e termina a 7. Il gap monetario si amplia in parallelo:
E18.1/V4D passa da `14.568/16.443` al D14 a `84.223/118.813` al D30.

Questa evidenza collega la regressione alla capacità di servizio, non alla
semplice estensione coltivata.

## Implicazioni per la prossima versione

1. Ripristinare V4D come controllo economico e come default operativo.
2. Non usare `6-6-2` o `7-7-0` come obiettivo in sé. Una topologia più leggera
   è ammissibile solo se il controller dimostra ex ante capacità di servire e
   raccogliere le celle recuperate.
3. Introdurre un gate di conversione per ogni pascolo rimosso:
   `delta crop revenue + lavoro evitato > delta livestock revenue + nuovo
   backlog crop`.
4. Riallocare esplicitamente i worker liberati: un calo di azioni zootecniche
   non può trasformarsi in `PASS`.
5. Bloccare nuove celle crop quando weed/backlog o unwatered superano la
   capacità giornaliera; misurare harvest per crop tile-day, non superficie.
6. Calibrare il selector su replay Kaggle stabilizzati, ma mantenere un gate
   locale obbligatorio: nessuna regressione >5% contro V4D nel diretto e nel
   pool comune.

## Artefatti

- JSON: `docs/model_specs/codex/e18/artifacts/derived/E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1.json`;
- CSV: `docs/model_specs/codex/e18/artifacts/derived/E18_CODEX_LATEST_VS_E17_V4D_BENCHMARK_V1.csv`;
- runner: `docs/model_specs/codex/e18/tools/run_e18_latest_vs_e17_v4d_benchmark.py`;
- test: `docs/model_specs/codex/e18/tests/test_e18_latest_vs_e17_v4d_benchmark.py`.
