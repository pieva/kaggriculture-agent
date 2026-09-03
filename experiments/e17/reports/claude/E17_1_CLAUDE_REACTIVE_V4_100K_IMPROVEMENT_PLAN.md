# E17.1 — Claude reattivo: analisi del gap V3 e piano di miglioramento V4 (target indicativo 100k)

- **Data:** 2026-09-02
- **Stato:** AUTHORIZED PLAN / NOT EXECUTED — nessuna implementazione V4
  avviata. Nessun file di codice, config o test modificato per produrre
  questo documento.
- **Origine:** richiesta esplicita del proprietario — "Con i risultati
  mostrati, Claude non può considerarsi utile come competitor indipendente
  per il benchmark nello sviluppo degli altri agenti. Serve un piano per
  indirizzare il target dei 100k, altrimenti l'attività sarà interrotta."
- **Fonte primaria analizzata:** `experiments/e17/artifacts/derived/claude/E17_1_V3_DEV_BENCHMARK_VS_CODEX.json`
  (14 match unici Claude V3 vs Codex V9 black-box, dati raddoppiati per
  `CODEX_REACTIVE`), `experiments/e17/artifacts/derived/claude/E17_1_V3_METRICS.json`
- **Candidata analizzata:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V3`
  (`FROZEN_WITH_FAILED_GATES`)
- **Obiettivo di questo documento:** quantificare con precisione il gap
  residuo, distinguere ciò che è già misurato da ciò che è ancora ipotesi,
  e proporre un piano d'azione ordinato per una candidata V4 che avvicini
  il denaro medio conteso al target indicativo di **100.000**.

---

## 1. Quantificazione del gap (dato nuovo, non riportato nel report V3)

Il report di implementazione V3 cita il denaro medio conteso di Claude
(`13.540,86`) ma non aveva ancora calcolato il denaro medio dell'avversario
sugli stessi 14 match. Calcolato ora dagli stessi dati grezzi già prodotti
(`E17_1_V3_DEV_BENCHMARK_VS_CODEX.json`, campo `opponent_final_money`):

```text
Claude V3 — denaro medio conteso:        13.540,86
Codex V9  — denaro medio conteso:       142.577,93  (min 90.429, max 182.800)
Rapporto Codex / Claude:                     10,53×
```

**Osservazione critica:** questo rapporto (10,53×) non è migliorato rispetto
al gap osservato nell'esibizione a tre vie che aveva motivato l'attivazione
V3 (9,52×, V2 contro la stessa famiglia Codex, esibizione comune). Le otto
correzioni V3 (MODEL_SPEC Sezione 9.1) hanno migliorato il denaro assoluto
di Claude (+15,0% sul proprio storico) ma **non hanno intaccato la scala
relativa del problema**: Codex, nello stesso arco temporale e sulle stesse
condizioni di mercato condiviso, genera un ordine di grandezza di denaro in
più. Il target indicativo di 100.000 richiesto ora dal proprietario è
coerente con questa evidenza: è sotto il livello minimo osservato di Codex
(90.429) ma resta un moltiplicatore di **~7,4×** sul denaro attuale di
Claude (13.540,86) — un obiettivo ambizioso ma ancorato a un livello di
performance realmente dimostrato nello stesso ambiente, non arbitrario.

### 1.1 Limite metodologico del benchmark attuale

Lo strumento `run_claude_e17_1_v3_dev_benchmark_vs_codex.py` cattura oggi
**solo** lo stato terminale della farm di Claude (`crop_tiles_final`,
`weed_tiles_final`, `animals_final`, `unlocked_quadrants`) e il denaro
finale di entrambi. **Non cattura mai lo stato terminale della farm di
Codex** (quadranti sbloccati, tile coltivate, numero di `hands`, animali),
pur essendo questi dati già presenti nell'osservazione grezza restituita
dal motore per lo stesso match (`terminal[1 - seat]["observation"]["farms"][1 - seat]`
— stato pubblico del gioco, non sorgente/routine Codex; lo stesso tipo di
dato — "`hands max = 8` osservato... contro i 12 di Codex" — era già stato
usato legittimamente come evidenza black-box nel piano V2→V3). Di
conseguenza, l'unica evidenza sulla densità coltivata relativa (Codex
37-55 tile sostenute dal giorno 8, Claude 20-28) proviene da **un solo
seed** tracciato manualmente durante lo sviluppo V3 (Sezione 9.2 MODEL_SPEC,
seed `26090103`), non da una misurazione sistematica sui 14 match. Il
gap di 10,53× sul denaro è quindi **misurato con certezza**; la sua
scomposizione per causa (workforce? densità coltivata? bestiame? numero di
quadranti? efficienza di vendita?) **non lo è ancora**.

Anche il KPI `crop_tiles_final` di Claude (media `1,00` su 14 match,
Sezione 4.1 del report V3) non è utilizzabile come proxy di densità
sostenuta: è misurato all'ultimo step registrato (`terminal`), dopo la
finestra di liquidazione di fine partita (`liquidation_days_remaining=3`),
quando la policy vende/raccoglie deliberatamente tutto per convertirlo in
cassa. Un valore vicino a zero a fine episodio è atteso e non implica bassa
densità durante il resto della partita.

---

## 2. Cause candidate, ordinate per forza dell'evidenza

### 2.1 Overhead di movimento: confermato, dominante, ma con un tetto quantificabile (~3×, non 10×)

**Evidenza:** nel benchmark passivo V3, il `move_command_fraction` medio è
`68,58%` — sostanzialmente **invariato** rispetto a V2 (`68,8%`), nonostante
V3 abbia introdotto un tie-break di prossimità di quadrante
(`prefer_same_quadrant`, MODEL_SPEC Sezione 6.9). Scomponendo un run tipico
(`S26090101-P0`, 6.373 comandi): `MOVE` `68,76%`, `PASS` `6,09%`, azioni a
valore diretto (`WATER`+`HARVEST`+`PLANT`+`SELL`+`BUY_SEED`+`BUY_ANIMAL`+
`BUY_LAND`) **`18,3%`**, `HIRE` `3,95%` (overhead necessario, il motore
richiede riassunzione quotidiana di ogni hand). Circa tre quarti del
budget di turni-lavoratore (`turni_per_giorno × workforce`, fatto
`ENGINE_VERIFIED`) non produce valore economico diretto.

**Stato epistemico:** CONFERMATO per direzione e stabile su due iterazioni
consecutive (V2, V3) — il tie-break di sola preferenza non è bastato a
spostare la metrica. **Limite dichiarato esplicitamente**: anche
nell'ipotesi limite (movimento portato a zero, irrealistico), il budget di
azioni a valore passerebbe da `~18,3%` a al più `~59%` del totale — un
fattore di miglioramento del throughput produttivo di **~3,2×**, non `10×`.
Il movimento da solo non può spiegare né chiudere l'intero gap.

### 2.2 Soffitto di workforce: non ri-testato su V3, ultima misurazione risale a V2

**Evidenza storica (non V3):** nel piano V2→V3, `hands max = 8` osservato
contro `max_hands = 9` configurato (V2) e **12** di Codex, nella vecchia
esibizione a tre. V3 ha alzato `max_hands` a `15` per correggere la
trappola di cassa (MODEL_SPEC Sezione 9.1 punto 1), ma **nessuno strumento
ha ancora misurato quante `hands` Claude V3 riesce effettivamente a
mantenere sotto contesa reale**, né quante ne mantiene Codex nello stesso
match (dato disponibile black-box, Sezione 1.1).

**Stato epistemico:** IPOTESI NON VERIFICATA su V3. Priorità alta perché
economico da testare (richiede solo strumentazione, non riprogettazione).

### 2.3 Bestiame: recuperato in valore assoluto ma mai confrontato con Codex sotto contesa

**Evidenza:** `animals_final` medio di Claude nel benchmark conteso V3 è
`4,36` (Sezione 1, dati ricalcolati). Il valore corrispondente di Codex non
è mai stato misurato in questo benchmark (stesso limite di Sezione 1.1).

**Stato epistemico:** IPOTESI NON VERIFICATA. Priorità media.

### 2.4 Scala dei quadranti: non è una leva disponibile per questa iterazione

`target_quadrants = 3` è un vincolo architetturale esplicito del filone
sperimentale E17.1 "3Q" (il modulo Codex di riferimento è nominato
`codex_3q_mixed_high_density`, stessa famiglia di esperimento). Claude non
tenta mai il quarto quadrante (`SE`) per costruzione (`e17_reactive_3q_v3.py:915`,
`if len(feat.unlocked_quadrants) >= cfg.target_quadrants: ...`), e con ogni
evidenza raccolta finora anche Codex opera entro lo stesso limite. **Non è
quindi una causa candidata per il gap**: alzare `target_quadrants` oltre 3
uscirebbe dallo scope dell'esperimento E17.1 3Q e richiederebbe
un'autorizzazione esplicita separata, non è compresa in questo piano.

### 2.5 Fughe residue (18/14 run passivi): drag economico secondario, non dominante

Le fughe consumano capitale (perdita di un animale già pagato) ma la loro
scala (`18` eventi su 14 run) è ordini di grandezza troppo piccola per
spiegare un gap di `10×` sul denaro totale. Resta un difetto da chiudere
per igiene del gate `ANIMAL_ESCAPES == 0`, non per impatto atteso sul
target economico.

---

## 3. Piano V4, in ordine di priorità

| # | Intervento | Causa attaccata | Costo/rischio | Effetto atteso |
|---|---|---|---|---|
| 0 | Estendere lo strumento di benchmark conteso per catturare anche lo stato terminale osservabile di Codex (`hands`, `unlocked_quadrants`, tile coltivate/weed, animali) dalla stessa osservazione grezza già letta — puro black-box, nessuna lettura di sorgente | §1.1, prerequisito di §2.2/§2.3 | Bassissimo (nessuna modifica alla policy, solo al tool di misura) | Trasforma le ipotesi §2.2/§2.3 in evidenza misurata su tutti i 14 match, prima di scegliere quale leva implementare |
| 1 | Instradamento reale per worker: sostituire il tie-break di preferenza con un ordinamento spaziale della coda di opportunità per quadrante (es. percorso a serpentina o nearest-neighbor greedy per la sotto-lista di opportunità già filtrate per worker), misurato contro il KPI `move_command_fraction` come criterio di accettazione esplicito | §2.1 | Medio (riprogettazione della selezione opportunità, non dello schema di priorità) | `move_command_fraction` da `68,6%` verso un target esplicito `<45%`; secondo il tetto calcolato in §2.1, non oltre `~3×` sul throughput produttivo da solo |
| 2 | Ablation del soffitto di workforce: con i dati di #0, testare `max_hands` oltre `15` (e ritarare `hire_reserve` di conseguenza) **solo se** i dati mostrano Claude sistematicamente sotto il livello di Codex | §2.2 | Basso (parametro singolo, protocollo di ablation già consolidato) | Dipende dal gap misurato in #0; non stimabile prima |
| 3 | Logistica zootecnica proporzionale alla scala: se #0 mostra Claude strutturalmente sotto Codex sul numero di animali, rivedere `herd_per_worker_ratio`/`animal_purchase_reserve` in combinazione con #1 (più worker-turni liberi = più capacità di servicing) | §2.3 | Medio | Dipende dai dati di #0 |
| 4 | Chiusura dedicata delle fughe residue: tracciamento della sotto-finestra EOD (cambio giorno) per capire perché la prelazione d'urgenza esistente (`CRITICAL_PRIORITY_CEILING`) non le azzera anche con shed pieno | §2.5 | Basso | Gate `ANIMAL_ESCAPES == 0`, effetto economico atteso marginale |

**Sequenza consigliata e motivazione:**

1. **#0 prima di tutto, senza eccezioni.** Ripetere l'errore già commesso
   nel ciclo V2→V3 — implementare una correzione (§2.2 o §2.3) basata su
   un'ipotesi non verificata — rischia di ripetere il pattern osservato in
   Sezione 9.1 punto 7 del MODEL_SPEC V3 (regressione da modifica non
   validata sui dati reali). Il costo di #0 è quasi nullo (strumentazione,
   non policy) e converte due ipotesi intere da "plausibili" a "misurate"
   prima di scrivere una riga di codice della policy.
2. **#1 subito dopo**, indipendentemente dall'esito di #0: è l'unica causa
   già CONFERMATA (non ipotizzata) su due iterazioni consecutive, ha un
   tetto d'effetto quantificato (~3×) e non richiede ulteriori dati per
   essere motivata.
3. **#2, #3 dopo**, condizionati ai dati di #0 — non prima, per evitare di
   ritarare parametri economici "al buio" come già accaduto nel gap
   9,5× mai visto in sviluppo (piano V2→V3, Sezione 2.5).
4. **#4 in parallelo**, a basso rischio e indipendente dalle altre leve.

---

## 4. Valutazione onesta di fattibilità del target 100k

Il tetto quantificato per la sola leva #1 (movimento) è **~3,2×** sul
throughput produttivo, nell'ipotesi limite e irrealistica di movimento
azzerato. Combinando #1 con un margine di workforce (#2, effetto non
ancora stimabile ma verosimilmente in un ordine `1,3×-2×` sulla base del
precedente V2 "8 contro 12 hands") e con guadagni minori da #3/#4, una V4
ben eseguita può plausibilmente puntare a un **denaro medio conteso
nell'intervallo indicativo `40.000-80.000`** — un miglioramento sostanziale
(`3×-6×`) ma **non garantito a raggiungere `100.000` in una singola
iterazione**. Dichiararlo raggiunto senza averlo misurato ripeterebbe
esattamente l'errore di processo già commesso e corretto in V3 (MODEL_SPEC
Sezione 9.1 punto 7).

Questo piano non promette `100.000`: propone la sequenza di interventi con
il rapporto rischio/beneficio più favorevole per avvicinarsi al target,
con un checkpoint esplicito dopo #0+#1 (lo step a più alta confidenza) per
decidere, con dati reali e non ipotesi, se procedere a #2/#3 o se il gap
residuo richieda un'iterazione V5 con una leva non ancora identificata.

---

## 5. Prossimi passi operativi

1. Estendere `run_claude_e17_1_v3_dev_benchmark_vs_codex.py` (#0):
   aggiungere `opponent_unlocked_quadrants`, `opponent_crop_tiles_final`,
   `opponent_weed_tiles_final`, `opponent_animals_final`,
   `opponent_hands_final` leggendo `terminal[1 - seat]["observation"]["farms"][1 - seat]`,
   stesso schema di lettura già usato per il proprio stato. Nessuna
   modifica alla policy. Ri-eseguire sui 14 match development già
   autorizzati.
2. Analizzare i nuovi dati e aggiornare questo documento (Sezione 1.1) da
   "non misurato" a valori reali prima di procedere a #2/#3.
3. Implementare #1 (instradamento spaziale) come nuovo file
   `e17_reactive_3q_v4.py`, con nuovo MODEL_SPEC/config/test/tool,
   seguendo lo stesso protocollo V1→V2→V3 (diagnosi verificata,
   correzione, test, matrice completa a 7 seed ri-validata ad ogni
   modifica, benchmark conteso, report onesto anche in caso di mancato
   raggiungimento del target).
4. Solo dopo #1 e con i dati di #0, decidere se e come procedere su #2/#3,
   ad una leva per volta (protocollo di ablation causale singola già in
   uso).

---

## 6. Vincoli che restano validi per V4

Identici a quelli dichiarati per V3 (Sezione 6 del piano V3): nessun
import da `agricola.strategy.codex`/`antigravity`/`copilot` nella policy,
nessuna tabella di azioni indicizzata per step, nessun consumo di seed
holdout o final-confirmation, nessuna modifica a file di altri agenti o
alla submission canonica, nessun commit/push/upload Kaggle senza
autorizzazione esplicita. Il benchmark contro Codex resta rigorosamente
black-box (risultati e stato di gioco osservabile sì, sorgenti/routine
no) — l'estensione proposta al punto #0 di Sezione 5 rispetta questo
vincolo perché legge solo lo stato di gioco pubblico già restituito dal
motore per lo stesso match, mai codice o configurazione Codex.
