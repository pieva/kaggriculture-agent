# E17 — Torneo delta Claude V5 / Copilot 6-6-2 V3

- **Data:** 2026-09-03
- **Stato:** COMPLETE — 84/84 match development
- **Ruolo epistemico:** `DEVELOPMENT_ONLY_NON_QUALIFYING`
- **Target economico di riferimento:** denaro medio locale `100.000`
- **Holdout / final-confirmation:** non consumati
- **Artifact:**
  `experiments/e17/artifacts/derived/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3.json`
- **CSV per-run:**
  `experiments/e17/artifacts/derived/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3.csv`
- **Runner:**
  `experiments/e17/tools/common/run_e17_two_candidate_delta_tournament_v3.py`

> Il target `100.000` indica denaro terminale nella simulazione locale, non il
> rating o lo score mostrato dalla pagina Kaggle.

## 1. Protocollo

Il torneo confronta i due nuovi agenti con i rispettivi predecessori:

| Nuovo agente | Predecessore / controllo | Delta isolato |
|---|---|---|
| `CLAUDE_V5` | `CLAUDE_V3_CONTROL` | clustering home-quadrant |
| `COPILOT_662_V3` | `CODEX_662_V2_CONTROL` | service guard sugli acquisti animali |

La matrice è un round-robin completo fra quattro partecipanti: 6 pair, 7
seed development, 2 orientamenti di seat, per un totale di 84 match. Ogni
partecipante gioca 42 match. I delta primari nuovo/predecessore sono calcolati
anche sui due avversari condivisi, in modo da non confondere la qualità del
candidato con un diverso mix di opposizione.

I due controlli 6-6-2 risultano comportamentalmente identici nel corpus: per
Claude le 28 osservazioni contro i due controlli rappresentano quindi 14
condizioni seed/seat effettivamente distinte, replicate contro due label.
Questa duplicazione è dichiarata e non viene interpretata come evidenza
indipendente aggiuntiva.

La provenance conserva per le due policy 6-6-2 sia l'hash della sorgente
all'esecuzione sia l'hash verificabile al closeout. Dopo il torneo la V3 e la
V4 early-herd non ammessa sono state isolate nel namespace Copilot per
ripristinare il freeze byte-identico della V2; nessuna modifica
retroattivamente gli 84 risultati e la V4 non è presentata come benchmarkata.

## 2. Esito complessivo

| Agente | W-L-T | Denaro medio | Mediana | Min–max | σ |
|---|---:|---:|---:|---:|---:|
| `COPILOT_662_V3` | 29-1-12 | **114.586,40** | 123.207 | 53.746–158.463 | 33.586,94 |
| `CODEX_662_V2_CONTROL` | 29-1-12 | **114.586,40** | 123.207 | 53.746–158.463 | 33.586,94 |
| `CLAUDE_V5` | 9-33-0 | 13.926,07 | 14.549,50 | **78–23.555** | 4.546,37 |
| `CLAUDE_V3_CONTROL` | 5-37-0 | 13.638,98 | 13.159 | 7.861–18.563 | 2.356,58 |

La classifica aggregata da sola è fuorviante per Claude: V5 ha una media
leggermente superiore a V3 (`+2,10%`) ma una deviazione quasi doppia e un
collasso a `78`. Per il 6-6-2, invece, media, mediana, estremi e dispersione
sono identici fra V3 e V2.

## 3. Delta Claude V5

### 3.1 Avversari condivisi

Contro entrambi i controlli 6-6-2:

| KPI | Claude V5 | Claude V3 | Delta V5 |
|---|---:|---:|---:|
| Denaro medio | **14.318,50** | 13.192,79 | **+1.125,71 / +8,53%** |
| Peak hands | 11,29 | 11,86 | −4,82% |
| Peak crop | 32,86 | 31,36 | +4,78% |
| Peak animali | 4,07 | 5,14 | −20,83% |
| Animali finali | 3,36 | 4,71 | −28,79% |
| Pascoli/coops vuoti finali | 4,64 | 3,29 | **+41,30%** |
| MOVE | 3.811,36 | 4.297,07 | **−11,30%** |
| MOVE/produttive | 3,21 | 3,66 | **−12,23%** |
| Azioni produttive | 1.189,71 | 1.176,21 | +1,15% |
| PASS | 242,36 | 324,57 | −25,33% |
| Fughe/run | 1,71 | 1,93 | −11,11%, ma ancora non zero |

Il clustering fa ciò che promette localmente: riduce movimento e PASS e
aumenta leggermente crop e azioni produttive. Non cambia però la scala del
throughput economico. Il guadagno di efficienza logistica viene in parte
pagato con meno workforce, meno animali e più strutture zootecniche vuote.

Il segno non è stabile per seed:

| Seed | V5 | V3 | Delta |
|---:|---:|---:|---:|
| `26090101` | 16.891,00 | 12.308,00 | +37,24% |
| `26090102` | 15.560,00 | 9.332,50 | +66,73% |
| `26090103` | 14.636,50 | 17.825,00 | **−17,89%** |
| `1838889274` | 13.200,50 | 14.172,50 | **−6,86%** |
| `1619968655` | 12.281,50 | 13.705,00 | **−10,39%** |
| `710418712` | 12.513,00 | 12.987,00 | **−3,65%** |
| `562040596` | 15.147,00 | 12.019,50 | +26,02% |

Tre seed migliorano e quattro peggiorano. L'uplift aggregato dipende dai due
seed con guadagni più grandi e non costituisce ancora una leva robusta.

### 3.2 Testa-a-testa con V3

V5 vince 9 match su 14, ma il denaro medio è **inferiore**:

- V5: `13.141,21`;
- V3: `14.531,36`;
- delta V5: **−1.390,14 / −9,57%**;
- minimo V5: **78** sul seed `26090102`, seat 1;
- altri collassi: `2.740`, `3.791`, `3.894`.

Il W/L nasconde quindi una coda sinistra inaccettabile. Nei 42 match V5
raggiunge 3Q solo `28/42`; V3 raggiunge 3Q `42/42`. Contro V3, V5 arriva a
3Q appena `6/14`. Nei match che sbloccano Q2, il giorno medio è circa `16`,
contro `11,40` aggregato del predecessore. Le run bloccate a 2Q coincidono
con workforce ridotta e, nei casi peggiori, `28–37` weed.

### 3.3 Gap verso 100.000

Usando il confronto a opposizione condivisa:

- livello raggiunto: **14,32%** del target;
- gap residuo: **85.681,50**;
- moltiplicatore necessario: **6,98×**;
- contro il 6-6-2: `0-28`, con delta medio head-to-head `−118.311,14`;
- peak crop: `32,86` contro circa `59,93` del 6-6-2;
- azioni produttive: `1.189,71` contro circa `2.617,93`;
- MOVE/produttive: `3,21` contro `1,37`;
- peak animali: `4,07` contro `15`;
- fughe: positive contro zero del controllo.

La lacuna non è più principalmente il numero di hands: V5 arriva vicino a
12 quando non collassa. Il problema è trasformare workforce e superficie in
throughput completato e liquidato. Il clustering è un'ottimizzazione
secondaria; non sostituisce una catena economica ad alta densità.

### 3.4 Lavoro necessario per Claude

Ordine consigliato, con gate misurabili:

1. **Stabilizzare espansione e hiring:** `3Q = 100%`, Q2 entro circa D11,
   nessuna run sotto 8 hands. Prima correggere l'interazione fra clustering,
   soglia workforce e acquisto SW.
2. **Eliminare i collassi:** minimo development sopra `10.000` prima di
   ottimizzare la media; zero run con money `<5.000` o weed `>20`.
3. **Portare la produttività per run almeno a 2.000 azioni** e
   MOVE/produttive sotto `2,0`, poi verso `1,5`.
4. **Raddoppiare la densità crop effettiva:** peak crop prima `45`, poi
   `55+`, senza accumulo terminale non raccolto.
5. **Chiudere la zootecnia:** strutture costruite solo se riempibili,
   FEED/CARE prioritari, fughe a zero, oppure ablation crop-only esplicita.
6. **Liquidazione terminale state-driven:** HARVEST → DROP → SELL con
   controllo dell'inventario rimasto a step 719.
7. Procedere per milestone `25k → 50k → 75k → 100k`; un'altra singola
   ottimizzazione del routing non può plausibilmente fornire il `6,98×`.

**Decisione Claude:** V5 è una buona ablation di routing, ma non è promossa.
Va mantenuta come ramo di ricerca e corretta prima di qualsiasi holdout o
submission Kaggle.

## 4. Delta Copilot 6-6-2 V3

### 4.1 Risultato causale

Sui due avversari condivisi V3 e V2 producono:

- denaro medio identico: `132.217,68`;
- delta: **0 / 0,00%**;
- tutte le 13 metriche aggregate identiche;
- **28/28** profili per-run completi identici;
- **28/28** conteggi azione identici.

Nel testa-a-testa diretto:

- `1-1-12`;
- denaro medio identico: `79.323,86`;
- delta medio: `0`;
- un solo seed produce `±456` a seconda del seat; gli altri 12 match sono
  pareggi esatti.

La service guard è quindi **behaviorally inert nel dominio testato**. Non è
possibile attribuirle alcun miglioramento. La causa più probabile è che la
condizione non si attivi quando esistono ordini multi-unità rilevanti, oppure
che gli acquisti ridotti vengano recuperati nei turni successivi senza
cambiare lo stato terminale. Il controller non espone contatori di attivazione
o unità soppresse, quindi l'ipotesi non è direttamente falsificabile con la
telemetria corrente.

### 4.2 Target e robustezza

Contro Claude, entrambe le versioni superano il target:

- `132.217,68`, pari al `132,22%` del target;
- surplus `32.217,68`;
- 14/14 pascoli, 6-6-2, zero fughe e zero breach.

Contro un altro 6-6-2 equivalente, però, la media scende a `79.323,86`:

- gap self-play: `20.676,14`;
- incremento necessario: circa `+26,1%`.

Il target è quindi superato sotto opposizione Claude ma non in un regime di
forte contesa simmetrica. Questo spiega anche la dispersione elevata e rende
più importante il market-regime adattivo, ma la V3 attuale non lo realizza.

### 4.3 Lavoro necessario per la V3

1. Aggiungere telemetria causale: `service_guard_activations`,
   `animal_orders_seen`, `orders_throttled`, `animal_units_suppressed` e stato
   del backlog al momento dell'intervento.
2. Creare scenari development controllati che forzino separatamente
   `weed >= 18`, due pascoli vuoti e ordini animali multi-unità.
3. Richiedere un gate di attivazione: almeno una run con guard attiva e un
   delta di action stream spiegabile prima del torneo economico.
4. Misurare la leva contro contesa 6-6-2, dove manca `+26,1%` per 100k,
   senza rompere 14/14, zero fughe e liquidazione.
5. Se l'action stream resta identico, rimuovere la V3: una variante senza
   effetto aumenta soltanto superficie di manutenzione e rischio operativo.

**Decisione Copilot V3:** non promossa. Il 6-6-2 V2 resta il controllo e la
candidata Kaggle; V3 è una proposta non attivata, non un miglioramento.

## 5. Decisione complessiva

| Candidato | Delta causale | Target 100k | Decisione |
|---|---:|---:|---|
| Claude V5 | +8,53% shared, ma −9,57% diretto e collassi | 14,32%; manca 6,98× | ricerca, non promuovere |
| Copilot 6-6-2 V3 | **0,00%**, behaviorally identical | >100k vs Claude; 79,3k self-play | non promuovere; tenere V2 |

Nessuno dei due nuovi agenti giustifica una nuova submission. Il risultato
utile del round è diagnostico: Claude ha migliorato una componente reale ma
secondaria, mentre Copilot ha introdotto una guardia non osservabile nel
dominio development. Il prossimo lavoro deve essere strutturale per Claude e
di activation-first per Copilot, senza consumare holdout.
