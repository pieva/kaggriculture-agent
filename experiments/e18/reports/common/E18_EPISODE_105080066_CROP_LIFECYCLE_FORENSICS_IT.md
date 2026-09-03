# E18 — forensics del ciclo colturale nell'episodio 105080066

## Verdetto

L'episodio **non supporta** la formulazione semplice «Codex abbandona prima la
superficie coltivata». Codex mantiene più crop-tile-days late-game e pianta
fino a D28 effettivo, un giorno dopo Yusuf. Supporta invece una diagnosi più
precisa:

> la 6-6-2 Codex mantiene superficie nominale, ma gestisce peggio il ciclo di
> vita delle colture: meno irrigazione, troppe piante lasciate scadere o
> morire, nessuna rotazione aggressiva Strawberry→Wheat e raccolta del grano a
> resa media troppo bassa.

Il risultato è 59.861 contro 77.364: `-17.503`, pari a `-22,6%` rispetto a
Yusuf. Replicare tutto questo delta porterebbe Codex soltanto a 77.364; per il
target 100k resterebbero ancora 22.636.

## Identità ed epistemologia

- Episode `105080066`, seed `335991485`, 720 step, `DONE/DONE`;
- P0 Pietro Valocchi 59.861; P1 Yusuf Murtaza 77.364;
- SHA-256 raw `7AAEE0B4F43FFA5187C37FE8AEFF3FB9892D482CA20506C69B0C905552513F2C`;
- ruolo `E18_TRAINING_EVIDENCE`, non holdout;
- nel report `D1..D30` è il giorno mostrato dall'interfaccia, cioè
  `observation.day + 1`.

Le quantità raccolte sono ricostruite dalle transizioni di stato e dagli
acknowledgement delle azioni. I valori degli ordini SELL sono conservati nel
JSON derivato soltanto come richieste, non come vendite necessariamente
eseguite; non sono usati per attribuire causalmente il gap monetario.

## L'architettura è analoga, non identica

| Metrica finale | Codex | Yusuf |
|---|---:|---:|
| Apertura del terzo quadrante | D12 | D11 |
| Pascoli totali | 14 | 14 |
| Pascoli Q0-Q1-Q2 | **6-6-2** | **7-6-1** |
| Pascoli occupati | 14 | 13 |
| Peak crop | 60 a D13 | 61 a D27 |

Quindi la topologia da sola non spiega il risultato. Codex realizza perfino
il vincolo più severo — 14/14 occupati e 6-6-2 esatta — ma Yusuf trasforma una
superficie comparabile in più output colturale.

## Dove nasce il vantaggio economico

Fino a D20 Yusuf è dietro di 5.071. A D21 passa avanti di 3.978: swing
giornaliero di 9.049. Nello stesso giorno raccoglie 60 unità di melon, mentre
Codex non raccoglie melon. È una forte associazione temporale, non una stima
controfattuale del valore causale.

| Giorno | Cash Codex | Cash Yusuf | Gap Yusuf-Codex |
|---:|---:|---:|---:|
| D20 | 26.132 | 21.061 | -5.071 |
| D21 | 29.130 | 33.108 | +3.978 |
| D24 | 40.299 | 49.958 | +9.659 |
| D25 | 41.480 | 55.689 | +14.209 |
| D28 | 47.101 | 66.854 | +19.753 |
| D30 | 59.861 | 77.364 | +17.503 |

La differenza sui melon non è quantità totale ma efficienza e timing:

| Melon | Codex | Yusuf |
|---|---:|---:|
| Tile piantate | 20 | 15 |
| Unità raccolte | 88 | 90 |
| Resa per tile piantata | 4,40 | 6,00 |
| Uscite fallite | 5 | 0 |
| Batch principali | 72 a D11; 16 a D22 | 30 a D11; 60 a D21 |

Yusuf ottiene più output con il 25% di tile seminate in meno e concentra il
secondo incasso un giorno prima.

## Il vero delta: rotazione Strawberry→Wheat

Yusuf usa `DIG` su 27 Strawberry ancora vive e le sostituisce con Wheat.
Codex non esegue mai questa rotazione: lascia 25 Strawberry scadere e altre 5
morire per starvation.

| Crop mix EOD | Codex | Yusuf |
|---|---|---|
| D21 | 41 Strawberry / 9 Wheat / 8 Melon | 27 Strawberry / 26 Wheat |
| D24 | 27 Strawberry / 25 Wheat | 14 Strawberry / 42 Wheat |
| D27 | 20 Strawberry / 36 Wheat | **1 Strawberry / 60 Wheat** |
| D30 | 13 Strawberry | 3 Wheat |

L'effetto sull'output è ampio:

| Output acked | Codex | Yusuf | Delta Yusuf |
|---|---:|---:|---:|
| Unità totali raccolte | 586 | 829 | **+243 / +41,5%** |
| Wheat | 286 | 504 | **+218 / +76,2%** |
| Strawberry | 212 | 235 | +23 |
| Melon | 88 | 90 | +2 |
| Resa media per harvest Wheat | 2,860 | 3,818 | **+33,5%** |

Yusuf non vince perché conserva più piante in ogni snapshot: vince perché
trasforma più rapidamente le perenni non più convenienti in cicli Wheat
completamente raccoglibili prima della chiusura.

## Servizio e piante perse

Tra D21 e D30 Codex ha 496 crop-tile-days contro 467: **+6,2% di superficie**.
Nonostante questo vantaggio nominale, esegue 118 WATER in meno e accumula 63
unwatered tile-days in più.

| D21-D30 | Codex | Yusuf | Delta Yusuf |
|---|---:|---:|---:|
| PLANT richieste | 64 | 85 | +21 |
| WATER richieste | 314 | 432 | +118 |
| HARVEST richieste | 226 | 246 | +20 |
| Unwatered crop-tile-days EOD | 224 | 161 | -63 |
| Piante finite in weed per scadenza | 35 | 9 | -26 |
| Piante finite in weed per starvation | 14 | 0 | -14 |
| Rotazioni deliberate con DIG | 0 | 27 | +27 |

Le 49 conversioni Codex a weed contro 9 sono il segnale più forte di
abbandono operativo. Il problema non è il conteggio dei tile piantati: è la
capacità di servirli, scegliere quando estirparli e raccoglierli prima della
scadenza.

## Chiusura

L'immagine terminale non va letta come prova che Yusuf abbia «smesso di
coltivare»: a D30 ha soltanto 3 Wheat e 2 weed perché ha quasi completato la
liquidazione. Codex chiude con 13 Strawberry e 14 weed. Il residuo visivo
Codex è quindi peggiore, non più produttivo.

## Implicazioni per E18

La prima linea causale E18 deve restare dentro gli invarianti 6-6-2, ma
aggiungere fixture specifiche per il ciclo colturale:

1. **Rotation guard:** in base a giorni residui, resa disponibile e valore
   atteso, decidere `KEEP/HARVEST/DIG/REPLANT` per Strawberry e Tomato.
2. **Harvest cadence:** evitare Wheat raccolto troppo presto; gate iniziale
   `mean Wheat units/harvest >= 3,5` senza aumentare weed.
3. **Expiry-aware queue:** `max_lifespan_step`, `yield_units` e backlog idrico
   devono precedere nuove semine e lavoro zootecnico non urgente.
4. **Late Wheat completion:** ogni Wheat piantato nella finestra finale deve
   avere un piano osservabile di irrigazione e raccolta entro D30.
5. **Gates di sicurezza:** 6-6-2, 14/14, zero fughe; `starved_to_weed=0` e
   forte riduzione di `expired_to_weed` sui seed development.

La topologia non va cambiata in questo round. Va cambiata la politica che
decide quali colture meritano ancora servizio e quando una perenne deve
lasciare spazio a un ciclo breve.

## Asset riproducibili

- raw locale: `data/replays/json/105080066.json`;
- analyzer: `experiments/e18/tools/common/analyze_episode_105080066.py`;
- summary: `experiments/e18/artifacts/discovery/E18_EPISODE_105080066_LIFECYCLE_ANALYSIS_V1.json`;
- timeline: `experiments/e18/artifacts/discovery/E18_EPISODE_105080066_DAILY_TIMELINE_V1.csv`;
- azioni per giorno: `experiments/e18/artifacts/discovery/E18_EPISODE_105080066_ACTIONS_BY_DAY_V1.csv`.
