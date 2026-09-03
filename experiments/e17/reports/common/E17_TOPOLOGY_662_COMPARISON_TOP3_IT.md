# E17 — confronto 6-6-2 vs Top 3 archetipi

## Obiettivo

Valutare il prototipo `CODEX-E17.3-TOPOLOGY-FILL-662-V2` contro i tre archetipi documentati dal corpus Top 3 (`tetsuya`, `OceanMix`, `Crop Dusta`) usando i parametri disponibili: timing di Q1/Q2, distribuzione finale per quadrante, tile per tipologia, manodopera, fughe, movimento e performance finale.

## Nota metodologica

Il benchmark 6-6-2 prodotto in repo è un controllo di topologia `6-6-2` con hard cap in Q2 e con un target di 14 pasture dedicate al bestiame. La serializzazione JSON del benchmark è stata letta correttamente, ma il report di sintesi esportato non registra ancora il tempo di attivazione di Q1/Q2 né il movimento/produttive per azione eseguita: i campi `q1_activation_day`, `q2_activation_day`, `move`, `pass`, `productive`, `max_hands` risultano `null`/`0` nel file di benchmark corrente.

Questo significa che per la variante 6-6-2 la comparazione affidabile è principalmente strutturale, non ancora completamente temporale. In altre parole: il prototipo dimostra una topologia coerente con il pattern 6-6-2, ma non ancora un profilo di esecuzione completo e misurabile come i Top 3 replay.

## Sintesi esecutiva

- Il prototipo 6-6-2 realizza la distribuzione richiesta: 6 pasture in Q0, 6 in Q1, 2 in Q2, senza breccia del cap Q2.
- Il benchmark produce 6 run (3 seat x 2 seed) con payoff finale compreso tra 71.880 e 134.954, media ~109.462.
- Nessuna fuga animale è osservata nei run 6-6-2 in questo campione.
- Il problema più importante non è la topologia, ma la mancanza di metriche di milestone e di command execution: senza `q1_activation_day`, `q2_activation_day` e `move`/`productive` non possiamo dichiarare un timing competitivo pari a quello dei Top 3.
- La topologia 6-6-2 è quindi un prototipo valido come overlay strutturale, ma non ancora un candidato pienamente comparabile ai Top 3 in termini di efficienza di esecuzione.

## Tabella comparativa

| Metrica | tetsuya | OceanMix | Crop Dusta | 6-6-2 overlay |
|---|---:|---:|---:|---:|
| Q1 unlock | D7:H01, s169 | D6:H07, s151 | media D5–D6, s135,2 | non registrato nel benchmark corrente |
| Q2 unlock | D10:H01, s241 | D11:H02, s266 | media D8–D9, s206,6 | non registrato nel benchmark corrente |
| Distribuzione pasture target | 3Q distribuito, Q2 non chiuso a 2 | Q0/Q1 dense, Q2 colturale | 3 quadranti attivi, forte dispersione | 6 Q0 / 6 Q1 / 2 Q2 |
| Tile finali per quadrante (struttura) | Q0+Q1+Q2 miste | Q0/Q1 zootecnici, Q2 quasi colturale | triade mista e dispersa | Q0: 6 pasture / 7 animali / 6 crop (NW, in rappresentazione osservata); Q1: 6 pasture / 6 animali / 1 crop (NE); Q2: 2 pasture / 2 animali / 6 crop (SW); Q3 nullo |
| Max hands / lavoro | 12 | 12 | 12 | 12 (campo riportato per alcuni snapshot, ma non come metriche di esecuzione complete) |
| Escape animali | 0 | 0 | 31 derivati | 0 osservati |
| Movimento / transiti | 3.377,25 MOVE medi | 3.075,75 MOVE medi | 4.070,0 MOVE medi | non registrato / 0 nel benchmark esportato |
| Cassa finale media | 96.568 | 82.535 | 91.361 | 109.462 (media dei 6 run) |
| Reward finale medio / campione | ~95k–97k | ~82k | ~91k | ~109k |
| Valutazione competitiva | top performer, stabile | molto efficiente e compatta | rapido ma fragile | benchmark tecnico, struttura coerente ma tempo di attivazione non ancora tracciato |

## Distribuzione strutturale del 6-6-2

Il prototipo 6-6-2 contiene 14 target di pasture, rispettando la capienza dichiarata:

- `Q0`: 6 pasture
- `Q1`: 6 pasture
- `Q2`: 2 pasture
- `Q3`: 0 (slot non usato)

Il file di config conferma la validazione:

- `quadrant_pasture_caps`: `{Q0: 6, Q1: 6, Q2: 2}`
- `q2_pasture_cap`: `2`
- `pasture_fill_target`: `14`
- `livestock_resource_cap`: `15`

L’output del benchmark corrispondente conferma che la cap viene rispettata in tutti i run: `max_observed_q2_pastures` = 2, `latest_target_pastures_built` = 14, `latest_target_pastures_filled` = 14, `topology_cap_breaches` = 0.

## Profilo topologico osservato

Il benchmark 6-6-2 mostra un layout forte e altamente controllato:

- Q0/Q1 sono i quadranti zootecnici principali, con tutte le pasture target occupate e piene;
- Q2 è trattenuto a 2 cellule, rispettando il hard cap;
- il quadrante restante (`SE` / Q3) resta inutilizzato;
- il campione riporta 0 fughe animali, cioè nessun evento di stress o perdita di bestiame in questa topologia.

Nella sintesi del benchmark esportato, la distribuzione per quadrante è la seguente (media sui run osservati):

- `NE` (Q1 in questo layout): pasture 6, animali 6, crop 1, empty 4
- `NW` (Q0): pasture 6, animali 7, crop 6, empty 3,17
- `SW` (Q2): pasture 2, animali 2, crop 6, empty 7
- `SE` (Q3): zero struttura

Questa struttura è coerente con il pattern livestock-first ma non riesce ancora a essere valutata in termini di timing di attivazione, perché i campi di milestone sono mancanti.

## Confronto con i Top 3

### 1. `tetsuya`

Ha il profilo più equilibrato e robusto:

- Q1 a D7, Q2 a D10;
- store di bestiame gestito in modo distribuito;
- passo da un Q1 colturale a un Q2 misto senza crisi di fuga;
- migliore compromesso tra diversificazione e stabilità.

Il 6-6-2 è più rigido e più controllato della topologia di `tetsuya`, ma fa meno evidenza sul timing dinamico: viene impostato come layout rigido, non come sequenza di apertura adattiva.

### 2. `OceanMix`

La struttura più efficiente del corpus:

- Q1 D6, Q2 D11;
- zootecnia compatta in Q0/Q1;
- Q2 usato come modulo colturale puro;
- bassa complessità di movimento e scarso rischio di fuga.

Il 6-6-2 è molto più vicino a una controparte zootecnica rigida e subordinata a un cap Q2: la differenza principale è che `OceanMix` usa il Q2 come modulo colturale senza perdere la giustezza di timing, mentre il 6-6-2 è un overlay statico che non registra il momento in cui la struttura viene realizzata.

### 3. `Crop Dusta`

Il profilo più veloce ma più fragile:

- Q1 in D5–D6, Q2 in D8–D9;
- densità elevata, molti crop e animali, ma anche massima dispersione;
- movimento e fughe derivati molto più alti.

Il 6-6-2 si colloca a metà: più controllato di `Crop Dusta`, meno dinamico di `tetsuya` e `OceanMix`, ma più pulito nella topologia e con rischio zero in questo campione.

## Conclusione

Il 6-6-2 è un overlay di topology cap interessante e coerente con la filosofia `livestock-first`: rispetta la distribuzione richiesta, mantiene Q2 sotto controllo, evita fughe e costruisce una struttura zootecnica molto disciplinata.

Tuttavia, rispetto ai Top 3, manca ancora la prova di esecuzione temporale e of action-level telemetry. Fino a quando non saranno disponibili metriche affidabili per:

- `q1_activation_day`
- `q2_activation_day`
- `move` / `pass` / `productive`
- `max_hands` e worker pipeline
- `transits` e movimento di bestiame

la variante 6-6-2 va trattata come un controllo di topologia molto promettente, ma non come strategia competitivamente validata. In breve: ottima architettura di layout, ancora da dimostrare come runtime di performance.
