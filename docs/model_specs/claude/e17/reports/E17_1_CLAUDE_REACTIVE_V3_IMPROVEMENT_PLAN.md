# E17.1 — Claude reattivo: analisi dell'esibizione e piano di miglioramento V3

- **Data:** 2026-09-02
- **Stato:** AUTHORIZED PLAN / NOT EXECUTED — benchmark Codex black-box
  autorizzato; nessuna implementazione V3 avviata
- **Autorizzazione:** `experiments/e17/reviews/common/E17_CLAUDE_V3_BLACK_BOX_CODEX_BENCHMARK_AUTHORIZATION.md`
- **Fonte primaria analizzata:** `experiments/e17/reports/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`
- **Fonti secondarie:** `experiments/e17/reviews/common/E17_REACTIVE_TOURNAMENT_CANDIDATE_AMENDMENT_2.md`,
  `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V2_IMPLEMENTATION_REPORT.md`,
  `docs/model_specs/claude/MODEL_SPEC_CLAUDE_E17_1_3Q_REACTIVE_V2.md`
- **Candidata analizzata:** `CLAUDE-E17.1-3Q-REACTIVE-INDEPENDENT-V2`
  (`FROZEN_WITH_FAILED_GATES`, non ammessa al torneo)
- **Obiettivo di questo documento:** identificare cause radice e un piano
  d'azione ordinato per una candidata V3 che chiuda il gap economico di
  circa un ordine di grandezza osservato nell'esibizione development a tre.

Questo documento registra analisi e piano per una sessione futura. Nessun
file di codice, config o test è stato modificato per produrlo.

---

## 1. Quantificazione del gap

Dall'esibizione development (`DEVELOPMENT_ONLY_NON_QUALIFYING`, 42/42 match,
seat-balanced, 7 seed development, holdout non consumato):

```text
Codex V9 / Codex reattivo — denaro medio: 112.149,21
Claude V2                  — denaro medio:  11.777,64
Rapporto: 112.149,21 / 11.777,64 ≈ 9,52×
```

Claude V2 ha perso tutti e 28 i match contro le due varianti Codex (`0–0–28`
in entrambi i testa-a-testa), pur raggiungendo 3Q in 28/28 run sotto contesa
(contro 13/14 nel benchmark passivo isolato). Il gate tecnico, di
indipendenza e di reattività restano validi; il problema è integralmente
economico e di densità produttiva.

**Osservazione di processo:** l'intero sviluppo V1→V2 è stato calibrato
esclusivamente contro `INERT_PASS_POLICY`, un avversario che non compra, non
vende e non compete per lo stesso mercato. L'esibizione è la prima evidenza
reale sotto contesa, e mostra un pattern di fallimento diverso e più grave
di quello osservato in sviluppo passivo. Questo è di per sé un reperto
metodologico: il benchmark passivo non era sufficiente a prevedere il
comportamento sotto contesa.

---

## 2. Cause radice, ordinate per forza dell'evidenza

### 2.1 La guardia `core_established` è aggirabile e non misura densità reale (causa primaria)

**Evidenza:** Q1 mediano a **D2** (più precoce del bug D0 della V1 in
termini di sostanza economica, anche se sintatticamente "dopo" la guardia),
con **2,29 tile coltivate finali medie** contro **13,93** di Codex, e tile
`NON_PRODUCTIVE` per quadrante al **80-83%** contro il 56-68% di Codex.

**Meccanismo:** `core_min_harvest_requests=4` conta *richieste* `HARVEST`
proprie, non superficie coltivata satura. Il WHEAT ha `yield_units=1` già
al momento della semina (`_new_plant`, fatto `ENGINE_VERIFIED`) e
`first_yield_day=2`. Piantare anche solo 4 tile di WHEAT al giorno 0 rende
legale l'`HARVEST` di tutte e 4 esattamente al giorno 2, indipendentemente
da quanto Q0 sia effettivamente saturo rispetto a `crop_target_fill_ratio`
(0.55). La guardia si sblocca per conteggio di eventi rapidi su una sola
specie a ciclo breve, non per densità produttiva del nucleo.

**Stato epistemico:** CONFERMATA per meccanismo (verificabile leggendo
l'engine); non ancora confermata per attribuzione quantitativa esatta sui
ledger dell'esibizione (i ledger dei 42 match non sono stati ancora
ispezionati riga per riga da questa sessione).

### 2.2 Soffitto di workforce troppo basso e mai raggiunto sotto contesa

**Evidenza:** `hands max = 8` osservato contro `max_hands = 9` configurato
(V2) e i **12** di Codex.

**Meccanismo ipotizzato:** la configurazione di cassa (`hire_reserve`,
`land_purchase_reserve`) è stata tarata unicamente contro un avversario che
non compete per prezzi o inventory di mercato. Il motore condivide
`market.prices` e `market.inventory` fra i due giocatori; un avversario che
compra/vende attivamente altera la disponibilità e il prezzo realizzato per
Claude in modo mai osservato durante lo sviluppo.

**Stato epistemico:** IPOTESI PLAUSIBILE, non verificata direttamente. Da
testare confrontando i prezzi realizzati (`MKT-47`/telemetria post-hoc) nei
match dell'esibizione contro quelli dei run passivi allo stesso seed.

### 2.3 Il ratchet zootecnico, combinato col soffitto di workforce, ha quasi azzerato il bestiame

**Evidenza:** **1,00 animale finale medio** contro **19,00** di Codex, pur
con un tetto teorico (`herd_size_workforce_divisor=2`, `max_hands=8`
osservato) di 4 capi.

**Meccanismo ipotizzato:** la media osservata (1,00) è sotto il tetto
teorico (4), quindi il limitatore dominante non è il cap ma il ratchet
"zero rischio" (`max_at_risk_animals_for_new_purchase=0`) unito a una
logistica `FEED`/`PLACE_ANIMAL_NEEDED` a singolo worker per volta
(un'unica opportunità `PLACE_ANIMAL_NEEDED` generata per chiamata,
MODEL_SPEC V2 Sezione 6.2) che non tiene il passo quando il gregge cresce
anche di poco.

**Stato epistemico:** IPOTESI, non ancora verificata sui ledger
dell'esibizione. Coerente con la correzione V1→V2 che ha eliminato le fughe
(obiettivo raggiunto: 2/28 nell'esibizione) ma probabilmente con
un'overcorrection sul lato della crescita del gregge.

### 2.4 Overhead di movimento ancora alto in termini assoluti

**Evidenza:** **MOVE/azione produttiva = 2,9719** contro **1,2473** di
Codex (metrica diversa dalla "quota MOVE sul totale comandi" usata nei
report V1/V2 propri, quindi non direttamente comparabile con le cifre
77,4%/68,8% già misurate — stesso fenomeno, denominatore diverso).

**Meccanismo ipotizzato:** la persistenza dei target (fix V2) elimina
l'oscillazione a bassa priorità ma non introduce alcun clustering spaziale:
ogni worker cerca la migliore opportunità sull'intera board ad ogni
riassegnazione, senza preferenza per la propria zona corrente.

**Stato epistemico:** CONFERMATA per direzione (Claude resta ~2,4× peggio
di Codex su questa metrica anche dopo il fix V2), non ancora scomposta per
causa specifica (routing vs densità insufficiente che allunga le distanze
medie tra opportunità).

### 2.5 Lo sviluppo non ha mai misurato la contesa di mercato

**Evidenza:** nessuna — è un'assenza di evidenza, non un reperto. Tutti gli
strumenti di validazione Claude (`run_claude_e17_1_validation.py`,
`run_claude_e17_1_v2_validation.py`) usano esclusivamente
`INERT_PASS_POLICY` come avversario, per vincolo del protocollo di sviluppo
originale.

**Implicazione:** qualunque ritaratura di soglie (§2.2) fatta di nuovo solo
contro l'avversario inerte rischia di ripetere l'errore metodologico
V1→V2 (tarare su un segnale che non riproduce le condizioni del torneo).

---

## 3. Piano V3, in ordine di priorità

| # | Intervento | Causa attaccata | Target atteso | Confidenza |
|---|---|---|---|---|
| 1 | Sostituire/affiancare `core_min_harvest_requests` con una guardia di **fill ratio reale** (Q0 deve avvicinarsi a `crop_target_fill_ratio` prima di autorizzare `BUY_LAND`, non solo N richieste harvest) | §2.1 | tile coltivate finali/quadrante da 2,29 a >10 | Alta (meccanismo verificato sull'engine) |
| 2 | Aggiungere al protocollo di sviluppo un benchmark contro Codex V9 congelato come **avversario** (mai come sorgente di codice/routine), sui soli seed development, prima di ritarare qualunque soglia economica | §2.2, §2.5 | evidenza di sviluppo realistica prima del prossimo freeze | Alta (necessario metodologicamente, indipendentemente dall'effetto numerico) |
| 3 | Alzare `max_hands` verso 12-16 e ritarare `hire_reserve`/`land_purchase_reserve` **sul nuovo benchmark contendente** (non su quello passivo) | §2.2 | hands max da 8 a 12+ | Media (dipende dall'esito di #2) |
| 4 | Verificare sui ledger dell'esibizione se il ratchet zootecnico o la logistica `FEED`/`PLACE_ANIMAL_NEEDED` è il vincolo dominante sulla crescita del gregge, poi intervenire di conseguenza (es. dedicare un worker al servicing zootecnico oltre una soglia di gregge, o allentare `max_at_risk_animals_for_new_purchase` a 1 solo dopo aver rinforzato la logistica) | §2.3 | animali finali da 1 a 8-10, fughe restare a 0 | Media (ipotesi non ancora verificata) |
| 5 | Introdurre clustering spaziale: assegnazione di una "zona di casa" per worker/giorno invece di ricerca globale ad ogni riassegnazione | §2.4 | MOVE/produttiva da 2,97 verso ≤1,5 | Media (probabile ma non isolabile dagli altri effetti finché §1 e §3 non sono corretti) |

**Sequenza consigliata e motivazione:**

1. **#1 prima di tutto**: senza una guardia di densità reale, ogni altra
   ritaratura (workforce, gregge, movimento) verrebbe misurata su
   un'espansione territoriale già patologicamente prematura, ripetendo
   l'errore di attribuzione già commesso una volta (V1: guardia assente;
   V2 prima correzione: guardia aggirabile).
2. **#2 subito dopo, prima di #3**: ritarare soglie di cassa senza un
   benchmark contendente ripeterebbe esattamente l'errore metodologico che
   ha prodotto il gap di 9,5× mai visto in sviluppo. Richiede una decisione
   esplicita del proprietario, perché amplia l'uso del frozen Codex V9 da
   "avversario di torneo" a "avversario anche in sviluppo Claude" — non
   ancora autorizzato dai documenti letti finora.
3. **#3, #4, #5 dopo**, con ablation a una leva per volta (protocollo del
   repository), verificando ciascuna ipotesi sui ledger prima di
   implementare la correzione corrispondente, non assumendola.

## 4. Autorizzazione ricevuta: benchmark di sviluppo contro Codex, black-box

**Decisione del proprietario (2026-09-02):** autorizzato l'uso di Codex
(V9 e/o reattivo, congelati) come avversario anche nel benchmark di
**sviluppo** Claude, non solo nel torneo/esibizione comune — chiudendo il
punto aperto di Sezione 5 (versione precedente di questo documento).
Vincolo esplicito dato dal proprietario: **black-box**.

```text
CODEX_AS_DEVELOPMENT_OPPONENT: AUTHORIZED
SCOPE: risultati e comportamento osservabile di Codex durante il match
PROHIBITED: leggere sorgenti o routine Codex (codex_3q_mixed_high_density.py,
            codex_v9_routine_data.py, codex_e17_reactive_guarded.py,
            i relativi MODEL_SPEC/config) per qualunque scopo, inclusa la
            semplice comprensione della struttura del progetto
```

Regole operative che questa sessione seguirà per rispettare il vincolo:

1. **Il file di policy Claude (`e17_reactive_3q_v3.py`) non importa e non
   leggerà mai `agricola.strategy.codex`.** L'audit di indipendenza
   automatico (identico nello spirito a quello di V1/V2) continua a
   scansionare esclusivamente il sorgente della policy, non gli strumenti
   di orchestrazione dei match.
2. **Lo strumento di benchmark** (nuovo, sotto `docs/model_specs/claude/e17/tools/`)
   può importare **solo il punto d'ingresso pubblico** della factory Codex
   (stesso pattern già usato dallo strumento comune di esibizione,
   `experiments/e17/tools/common/run_e17_reactive_three_way_development_exhibition.py`,
   per istanziare un opponent callable da passare a
   `kaggle_environments.run(...)`) — mai altri simboli interni.
3. **Nessuna lettura di file sorgente/config/MODEL_SPEC Codex** in questa o
   nelle prossime sessioni per determinare il nome della factory: verrà
   ricavato esclusivamente dalla riga di import già presente nello
   strumento comune di esibizione (lettura della sola riga di import, non
   della logica interna), oppure chiesto direttamente al proprietario se
   non recuperabile così.
4. **Osservabile e utilizzabile per la diagnosi:** azioni finali eseguite
   da Codex (dal replay/osservazione di gioco), denaro finale, stato tile,
   quadranti sbloccati, animali, timing — esattamente le stesse categorie
   di dato già usate in `E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION_REPORT_IT.md`.
5. **Non utilizzabile:** qualunque euristica, soglia o struttura dedotta
   leggendo il codice Codex. Un apprendimento comportamentale generico
   ("l'avversario raggiunge 3Q al giorno 6", "mantiene ~12 hands") è
   evidenza di benchmark legittima; una soglia o una sequenza copiata dal
   sorgente non lo è.

## 5. Prossimi passi operativi (per la prossima sessione)

1. Individuare il punto d'ingresso pubblico di Codex V9 e/o reattivo
   leggendo **solo la riga di import** dello strumento comune di
   esibizione, senza aprire alcun file sorgente Codex.
2. Costruire `docs/model_specs/claude/e17/tools/run_claude_e17_1_v3_dev_benchmark_vs_codex.py`:
   esegue Claude V3 (in sviluppo) contro Codex V9/reattivo come avversario
   black-box sui soli seed development, seat-balanced, registrando le
   stesse categorie di KPI già usate nell'esibizione.
3. Ispezionare i ledger dei 42 match dell'esibizione già eseguita
   (`experiments/e17/artifacts/derived/common/E17_REACTIVE_THREE_WAY_DEVELOPMENT_EXHIBITION.json`
   e CSV collegato — dati Claude V2 propri e comportamento Codex
   osservabile, non sorgenti) per trasformare le ipotesi §2.2-§2.4 da
   plausibili a verificate.
4. Implementare la correzione #1 (guardia di densità, Sezione 3) per
   prima, come nuovo file `e17_reactive_3q_v3.py` con nuovo MODEL_SPEC,
   config, test e tool, seguendo lo stesso protocollo usato per V1→V2
   (diagnosi verificata, correzione, test, benchmark, report, senza
   consumare holdout).
5. Ritarare cassa/workforce (#3) e verificare le ipotesi zootecniche/di
   movimento (#4, #5) usando il nuovo benchmark contendente, ad una leva
   per volta.

---

## 6. Vincoli che restano validi per V3

Ereditati dai documenti di governance e autorizzazione versionati:
nessun import da `agricola.strategy.codex`/`antigravity`/`copilot` **nella
policy**, nessuna tabella di azioni indicizzata per step, nessun consumo di
seed holdout o final-confirmation, nessuna modifica a file di altri agenti
o alla submission canonica, nessun commit/push/upload Kaggle senza
autorizzazione esplicita. L'uso di Codex come avversario black-box nello
strumento di benchmark di sviluppo è ora autorizzato (Sezione 4) con i
vincoli operativi lì elencati.
