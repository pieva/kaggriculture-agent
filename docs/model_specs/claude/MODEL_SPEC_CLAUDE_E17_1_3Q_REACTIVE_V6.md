# MODEL_SPEC — Claude E17.1 3Q Reactive Independent V6

- **Policy ID:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V6`
- **Autore:** Claude (modeler indipendente)
- **Data:** 2026-09-03
- **Foundation:** C2.1 (RECONCILED)
- **Stato:** REJECTED — la correzione puntuale non generalizza; regressione
  development completa in Sezione 4
- **Predecessore:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V5` (matrice
  positiva contro Codex, `+3,31%`, ma collassi trovati dal torneo a due
  candidate contro Claude V3, min `78`)
- **Sorgente:** `src/agricola/strategy/claude/e17_reactive_3q_v6.py`
- **Config:** `docs/model_specs/claude/e17/configs/CLAUDE_E17_1_3Q_REACTIVE_V6.json`
- **Origine:** `experiments/e17/reports/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3_REPORT_IT.md`
  (round-robin a 4 partecipanti, 84 match; Claude V5 9-33-0 contro
  controlli 6-6-2, 3Q raggiunto solo 28/42, minimo `78`; testa-a-testa
  con V3: V5 vince 9/14 ma denaro medio inferiore, `-9,57%`, con collassi
  a `78/2.740/3.791/3.894`). Sezione "Lavoro necessario per Claude" punto
  1: *"Prima correggere l'interazione fra clustering, soglia workforce e
  acquisto SW."*

---

## 1. Diagnosi (riprodotta direttamente, non assunta dal report)

Il report del torneo misura il sintomo (collassi, 3Q mancato) ma non ha
accesso al codice per diagnosticarne la causa. Prima di scrivere qualunque
correzione, il match peggiore citato è stato riprodotto localmente:
`CLAUDE_V5` (seat 1) contro `CLAUDE_V3_CONTROL` (seat 0), seed `26090102`
— lo stesso seed/seat del minimo `78` riportato in Sezione 3.2 del
torneo.

### 1.1 Traccia giorno per giorno (V5, prima della correzione)

Campionando lo stato a fine giornata (non nell'istante del reset
giornaliero delle `hands`, che le azzera sempre per contratto motore
prima che quel turno le riassuma):

| Giorno | Denaro | Hands | Quadranti | Weed |
|---:|---:|---:|---|---:|
| 4 | 68 | 5 | NW, NE | 0 |
| 5 | 68 | **0** | NW, NE | 0 |
| 9 | 68 | 0 | NW, NE | 16 |
| 13 | 345 | 6 | NW, NE | 1 |
| 14 | 128 | 10 | NW, NE, SW | 1 |
| 15 | 78 | **0** | NW, NE, SW | 4 |
| 20 | 78 | 0 | NW, NE, SW | 33 |
| 29 (finale) | **78** | 0 | NW, NE, SW | 21 |

**Meccanismo identificato:** quando la cassa scende sotto
`hire_reserve` (150), `_hire_orders` smette correttamente di assumere
(comportamento voluto, protegge la riserva). Con `hands=0` resta solo il
farmer, il cui `home_quadrant` è sempre NW per costruzione (indice
worker `0`). Con il clustering attivo, il farmer resta confinato a NW:
le piante non innaffiate negli altri quadranti (NE, poi anche SW)
diventano `WEED` — `RECOVERY_DIG` ha priorità `5`, non è uno dei due
generi critici (`URGENT_WATER`, `FEED_NEEDED`) che possono attraversare
il confine di quadrante — e restano tali per il resto della partita.
Senza recupero di cassa da quei quadranti, la riserva non si ricostituisce
mai: una trappola auto-rinforzante che V3 (dispatch globale, senza
clustering) non innesca, perché il farmer solitario in V3 può comunque
raggiungere il problema peggiore ovunque sulla mappa.

Verifica di controllo: `CLAUDE_V3` vs `CLAUDE_V3` sullo stesso seed,
seat 1, non collassa (denaro `9.689`, comunque bloccato a `2Q`/`5 hands`
per una dinamica di contesa preesistente e indipendente, ma senza
morte da weed). `CLAUDE_V5` vs `CLAUDE_V5` sullo stesso seed, seat 1,
nemmeno collassa (`11.279`). Il collasso a `78` emerge specificamente
nell'incontro asimmetrico V5-vs-V3, quando la workforce di V5 tocca
zero in un momento sfavorevole.

---

## 2. Ipotesi V6

**H-CR6.1:** il clustering per quadrante (V5) non deve applicarsi quando
la workforce corrente è sotto la soglia minima già usata da
`_expansion_guard` per giudicare la prontezza di copertura dei quadranti
(`min_workers_per_quadrant * quadranti_sbloccati`). Sotto quella soglia,
il pool di lavoratori è troppo esiguo per permettersi di dedicarne una
parte a un solo quadrante; il dispatch deve tornare globale (comportamento
V3/V5-con-flag-disattivato) finché la workforce non si riprende.

Riusa una soglia già esistente e già validata (non introduce un nuovo
parametro arbitrario), applicandola a un secondo punto di decisione oltre
a quello originale.

---

## 3. Modifica implementata (unica variabile)

`src/agricola/strategy/claude/e17_reactive_3q_v6.py`, metodo `_decide`:

```python
workforce_ready_to_cluster = len(feat.worker_positions) >= (
    cfg.min_workers_per_quadrant * max(1, len(feat.unlocked_quadrants))
)
...
home_quadrant = (
    _home_quadrant_for(worker_index, feat.unlocked_quadrants)
    if cfg.cluster_by_home_quadrant and workforce_ready_to_cluster
    else None
)
```

Nessun'altra leva toccata: `_best_opportunity`, `_home_quadrant_for`,
il cap zootecnico (rimasto disattivato di default come in V5), la
guardia `_core_established`, il soffitto workforce, tutto invariato da
V5. Verificato con `diff` contro `e17_reactive_3q_v5.py`: solo rinomina
di identificatori più questo gate aggiuntivo.

### 3.1 Verifica diretta sul caso riprodotto

| | V5 (prima) | V6 (dopo) |
|---|---:|---:|
| Denaro (seed `26090102`, seat 1, vs V3) | 78 | **15.743** |
| Hands finali | 0 | 8 |
| Quadranti | NW, NE, SW (bloccato in pratica da giorno 15) | NW, NE, SW (pienamente operativo) |

---

## 4. Esito del benchmark

Il regression check V6 vs V3 è stato completato su tutti i sette seed
development e i due orientamenti di seat (`14` match):

- V6 `1-13`, media `1.538,50`, minimo `32`;
- V3 media `17.119,36`; delta V6 `-91,01%`;
- tredici run sotto `5.000` e 3Q raggiunto in appena `1/14`;
- zero errori tecnici, quindi il fallimento è strategico e non operativo.

La riparazione del caso seed `26090102`, seat 1, non generalizza. Un benchmark
black-box eseguito in parallelo su quattro seed development, due seat e due
controlli Codex conferma il rifiuto: `0-16`, denaro medio `622,88` contro
`144.654,75`, nessuna run a 3Q e zero errori tecnici. V6 è respinta e non
accede a holdout, submission o E18.

Risultati in
`docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V6_REJECTION_REPORT_IT.md`.

---

## 5. Portata e limiti dichiarati

Questa correzione risolve lo specifico meccanismo di collasso diagnosticato
(clustering + workforce esigua + weed non recuperabile). Non affronta le
altre cause del gap verso `100.000` già elencate dal torneo (Sezione
"Lavoro necessario per Claude", punti 2-7): produttività per run, densità
crop, chiusura della zootecnia, liquidazione terminale state-driven. Il
torneo stesso è esplicito: *"un'altra singola ottimizzazione del routing
non può plausibilmente fornire il 6,98×"* necessario. V6 è un prerequisito
di stabilità, non un tentativo di chiudere il gap economico.

---

## 6. Vincoli invariati

Identici a V5/V3: nessun import da `agricola.strategy.codex`/
`antigravity`/`copilot`, nessuna tabella di azioni indicizzata per step,
nessun consumo di seed holdout o final-confirmation. Il confronto diretto
V6 vs V3 è fra due versioni della stessa policy Claude (nessun vincolo
black-box si applica); il benchmark contro Codex resta rigorosamente
black-box.
