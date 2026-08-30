# COPILOT C2 ROUND FEEDBACK

## Perimetro

Questo feedback è indipendente, retrospettivo e non costituisce remediation. Sono stati
esaminati la sintesi comune C2, Foundation C2, i tre MODEL_SPEC, le build verification,
i test pertinenti, i risultati del tournament, i replay Copilot e le evidenze E15/E16
disponibili. Non sono stati letti feedback di altri agenti e non sono stati modificati
codice, Foundation, MODEL_SPEC, configurazioni, test o risultati.

## 1. Risposta sintetica

Il round C2 ha prodotto due candidati sostanzialmente non operativi e un candidato
funzionante ma sottodimensionato perché ha separato la correzione di meccanismi locali
dalla dimostrazione che tali meccanismi componessero una policy economica completa nel
runtime reale.

La Foundation ha reso disponibili i concetti necessari; il processo successivo ha
privilegiato la correttezza di classificatori, action eligibility e interfacce. Non ha
imposto che ogni candidato partisse dallo stato iniziale reale, operasse sulla propria
farm in entrambi i seat, creasse superficie produttiva e chiudesse almeno un ciclo
economico. Per Codex ciò ha consentito una policy reale ma conservativa; per Antigravity
e Copilot ha consentito di certificare `TOURNAMENT_READY` senza policy realization.

## 2. Cause dei failure tecnici

### Antigravity

Il runtime espone `observation["private"]` al singolo agente come `dict`; il candidato
lo ha trattato come lista multi-player e ha tentato `privates[player_index]`. Il
`KeyError: 0` è stato intercettato dal fail-closed e ha prodotto `PASS` per 720 step.

Il controllo mancante era un real-engine smoke con la struttura di observation reale,
con contatore esplicito di eccezioni/fallback. I test hanno invece usato fixture
`"private": [{...}]`, riproducendo la stessa assunzione errata del codice. Il failure
è quindi un **BUILD ERROR** intercettabile da un **VERIFY ERROR**; non dimostra una
lacuna della Foundation.

### Copilot

Copilot aveva tre blocker indipendenti:

1. l'entrypoint invocava sempre `decide_actions(..., player_index=0)`, anche nelle
   observation P1; leggeva quindi `farms[0]` e le sue decisioni venivano eseguite sulla
   propria `farms[1]`;
2. il candidate restituiva invariabilmente `market: []`, mentre l'inizializzazione
   reale ha seed pari a zero; `PLANT` era quindi irraggiungibile;
3. mancavano target spaziali, routing e qualunque percorso che restituisse
   `NORTH`/`SOUTH`/`EAST`/`WEST`.

I replay confermano tutti e tre: Copilot come P1 resta a `(4,4)` per 720 step, ha zero
seed iniziali e zero market order, zero `PLANT`, zero `MOVE` e superficie attiva media
zero. In alcune partite le azioni `WATER`/`HARVEST`/`DIG` riflettono lo stato
dell'avversario letto come P0, non una transizione sulla farm Copilot.

I controlli che avrebbero dovuto intercettare il problema erano: test P0/P1 con
mutazione isolata della propria farm, smoke real-engine con seed iniziali zero, e
assertion su acquisto seed, cambio posizione e prima `PLANT` riuscita. Non erano
obbligatori; i test controllavano principalmente classificazione, action dispatch e
shape dell'output. Il failure è una combinazione di **MODEL_SPEC INTERPRETATION**
(policy locale assunta come policy completa), **BUILD ERROR** e **VERIFY ERROR**.

### Assunzioni non verificate accettate

- che un MODEL_SPEC focalizzato sul working-set già esistente fosse sufficiente dalla
  inizializzazione standard;
- che un agent callable, con unit test verdi, usasse il contract observation reale;
- che il positional-effect trascurabile rendesse superflua la verifica di
  `observation.player`;
- che emettere una action fosse proxy di un'azione accettata e produttiva;
- che mercato, seed bootstrap, routing e monetizzazione potessero restare “secondari”
  senza trasformare la policy in una catena incompleta.

## 3. Perché Codex ha funzionato ma ha ottenuto solo $16,846.50 e 9.17 tile medie

Codex è l'unico candidato C2 che ha connesso bootstrap, acquisto seed, movement,
planting, WATER, HARVEST, vendita e revenue. Il risultato prova policy realization,
non adeguatezza strategica.

La scala osservata resta limitata per ragioni già visibili negli artefatti:

1. **Perimetro deliberatamente ristretto.** Il MODEL_SPEC Codex fissa un working set
   di 17, due quadranti, quattro COW e cinque pasture; lascia `UNCHANGED` routing,
   land, market/cash e workforce. È una correzione lifecycle isolata, non una nuova
   politica di capacità.
2. **Superficie realizzata inferiore al piano.** Il target 17 produce 9.17 tile attive
   medie e 53.9% attainment. Il lifecycle corretto elimina una causa di degrado, ma non
   garantisce il rimpiazzo continuo o la serviceability su tutto il set.
3. **Routing e workforce rimangono vincoli operativi.** La stessa build Codex dichiara
   nearest-task routing, workforce e market/livestock come colli possibili. E16 R1
   misurava movement share tra 0.606 e 0.677 e gap persistenti persino con piena
   workforce; questo supporta routing/capacità come amplificatori, non come causa unica.
4. **Replant/market pacing non sono stati trattati.** E16 R1 attribuiva l'attainment
   di circa 47--50% anche a replant pacing, seed purchasing e shutdown. Codex conserva
   il floor 300, l'infrastruttura E16 e un gate PLANT che verifica una fase successiva,
   non la futura serviceability.
5. **Perdita di continuità con le evidenze E15.** E15 aveva già mostrato che, superata
   la soglia di maintenance, `state_capacity_alignment`, conversione inventory-to-cash,
   capitale e sell-through diventano discriminanti. C2 ha concentrato l'ipotesi sulla
   prevenzione del failure E16 e ha sospeso il trattamento esplicito di quegli elementi.

Non è corretto dedurre che più superficie sarebbe automaticamente più profitto: E15
mostra non monotonicità oltre la soglia operativa. È però corretto concludere che C2 non
ha verificato né ottimizzato l'allineamento tra dimensione del set, throughput, capitale,
livestock e monetizzazione che avrebbe potuto convertire una policy funzionante in
performance competitiva.

## 4. Adeguatezza della Foundation C2

### FOUNDATION MISSING INFORMATION

**Nessuna evidenza di informazione fondamentale mancante per spiegare i due failure.**
La Foundation descriveva seed inventory, market orders, posizioni worker, movimento,
azioni locali, lifecycle, cash, inventario e vendita. La State Machine esplicitava
inoltre che `PLANT` richiede seed, che il market processa `BUY_SEED`/`SELL`, e che
`action_eligible_now` è distinto da `serviceable_before_deadline`.

### FOUNDATION AMBIGUITY

**Evidenza limitata, non causa radice.** La Foundation dichiara
`serviceable_before_deadline` `PARTIALLY_KNOWN`, e alcune metriche aggregate non sono
formula-complete. Ciò limita la pretesa di una pianificazione ottimale o di metriche
complete, ma non impediva un bootstrap, l'uso del player corretto, un routing Manhattan
semplice o test real-engine di transizioni.

### MODEL_SPEC INTERPRETATION

I concorrenti hanno interpretato la disponibilità dei concetti Foundation come evidenza
sufficiente di realizzazione. In realtà la Foundation è descrittiva e consumer-neutral:
non seleziona target, non impone una strategia, non compra seed e non dimostra che i
consumer usino correttamente i dati.

### BUILD ERROR

Antigravity ha violato il runtime contract di `private`; Copilot ha violato il binding
del player e omesso interi percorsi operativi. Questi problemi sono a valle della
Foundation.

### VERIFY ERROR

Nessun gate obbligava a dimostrare nel vero environment che i concetti Foundation
fossero letti, collegati alle decisioni e produttivi.

### STRATEGIC ERROR

La strategia C2 comune ha trattato il bottleneck E16--premature HARVEST e WEED
irreversibile--come priorità quasi esclusiva. Era una correzione causale legittima, ma
non equivaleva a una strategia competitiva completa, soprattutto dopo E15.

## 5. Adeguatezza dei MODEL_SPEC

I tre MODEL_SPEC non hanno avuto lo stesso grado di completezza:

| Candidate | Trattamento effettivo |
|---|---|
| Antigravity | Dichiarava un ciclo ricco: routing, seed/market, replant, livestock e vendita; la realizzazione runtime è fallita prima di provarlo. |
| Codex | Collegava lifecycle a una policy E16 esistente, incluso mercato e routing, ma dichiarava invariati i driver economici e di capacità. |
| Copilot | Specificava una policy locale di prevenzione per tile già occupate; mercato rimaneva invariato e nessun bootstrap/routing/economic closure era contrattualizzato. |

Il processo ha quindi trattato tutti come “specifiche di policy agricole complete” per
la dichiarazione `TOURNAMENT_READY`, mentre almeno Copilot era esplicitamente un insieme
di meccanismi locali condizionati a seed, tile e working set preesistenti. Codex era
eseguibile end-to-end perché ereditava infrastruttura E16, ma il suo scope ristretto non
era progettato per massimizzare la crescita economica. Antigravity era formalmente
ambizioso ma non ha dimostrato fedeltà al runtime.

La divergenza è dunque sostanziale: non un confronto tra tre ipotesi complete di
performance, ma tra una correzione locale incompleta, una correzione lifecycle innestata
su infrastruttura preesistente e una policy ampia non integrata correttamente.

## 6. Adeguatezza di BUILD e VERIFY

BUILD e VERIFY hanno implicitamente ottimizzato per:

```text
tests pass
interfaces valid
action generated
no local semantic regression
```

Non hanno dimostrato:

```text
policy works in the real initialized environment
own-farm state transitions occur
productive surface grows
the economic loop closes
```

I gate mancanti, in ordine causale, erano:

1. **Runtime-contract / two-seat gate:** tipo e ownership di `private`, uso di
   `observation.player`, e isolamento della propria `farm` in P0/P1.
2. **Bootstrap gate:** da zero seed, presenza e risultato di `BUY_SEED`, quindi seed
   delta, movement e `PLANT` riuscita.
3. **Realization gate:** transizioni osservate `DIG -> empty`, `PLANT -> crop`,
   `WATER -> survival`, `mature crop -> HARVEST -> inventory`, `SELL -> cash`.
4. **Economic/capacity gate:** superficie produttiva non zero e monitoraggio di
   attainment, throughput e monetizzazione nel 720-step reale.
5. **Fail-closed observability gate:** ogni fallback durante VERIFY deve risultare
   visibile e invalidare la readiness se sostituisce la policy.

Il runner del torneo ha misurato action count e active surface, rendendo il failure
visibile dopo la freeze. Il processo non ha trasformato queste metriche in prerequisiti
prima della freeze.

## 7. Perdita dell'obiettivo strategico e uso delle evidenze storiche

La perdita di obiettivo avviene nella traduzione da E16 a C2. E16 forniva una causa
primaria concreta--HARVEST prematuro più assenza DIG--e C2 ha correttamente reso questa
causa dominante. Ma E15 aveva già stabilito una seconda condizione: superata la soglia
di maintenance, massa produttiva da sola non discrimina; conta la qualità di
monetizzazione e l'allineamento di stato/capacità.

Segnali concreti:

- Codex ha fissato il target 17 come “candidate operating region” e ha lasciato
  invariati routing, market/cash, land e workforce.
- Copilot ha qualificato market e seed scarcity come non prioritari e non ha previsto
  acquisizione, vendita o reinvestimento; ciò ha eliminato il ciclo economico anziché
  isolarne una variabile.
- Antigravity ha pre-registrato target operativi ambiziosi, ma VERIFY non ha esercitato
  il contract che avrebbe mostrato la failure prima del torneo.
- E15 aveva dimostrato nel candidato Copilot precedente un working set 25--28, 9 hands
  e circa 300 SELL; C2 non ha richiesto di preservare nessuno di questi percorsi
  essenziali mentre sostituiva la policy.

Questo non prova che tutte le lesson learned storiche siano state ignorate: Codex ha
riusato bootstrap, seed buying, hires, routing e vendite E16, e ha applicato il
correttivo lifecycle. Prova che l'evidenza fu usata selettivamente per prevenire il
failure più misurabile, senza un gate che preservasse la continuità con le capacità
economiche già dimostrate.

## 8. SELF-CRITIQUE

Il mio contributo Copilot C2 ha contribuito direttamente al risultato in quattro modi:

1. Ho definito il candidate come policy preventiva locale, pur accettando la label
   `TOURNAMENT_READY`. “Plant if seed exists” non è un piano di inizializzazione.
2. Ho lasciato `market` invariato e l'ho implementato come lista permanentemente vuota,
   rendendo impossibile l'acquisizione delle risorse iniziali.
3. Ho scritto una policy senza working-set target, routing o MOVE, quindi nessuna
   condizione poteva trasformare lo spawn in accesso a una tile produttiva.
4. Ho verificato la logica con fixture P0 e test di action output, senza testare il
   binding del player reale né gli effetti runtime di una policy P1.

La decisione più grave non è stata soltanto l'hardcoded `player_index=0`, che è un bug
di BUILD. È stata la decisione MODEL_SPEC/VERIFY di considerare completa una policy
senza bootstrap e senza chiusura economica. Quel difetto avrebbe lasciato il candidato
non operativo anche dopo la correzione del player index.

## 9. Critica del processo comune

| Categoria | Finding |
|---|---|
| PROCESS DEFECT | `TOURNAMENT_READY` ha certificato conformità locale e invocabilità senza richiedere policy realization end-to-end nell'ambiente inizializzato. |
| PROCESS DEFECT | La fase competitiva ha consentito di dichiarare sottosistemi “non prioritari” senza verificare che la loro assenza non spezzasse un prerequisito del loop. |
| EXPERIMENTAL DESIGN DEFECT | Il preflight non ha richiesto un minimo smoke P0/P1 con metriche di effetto; la telemetria outcome-aware era disponibile solo dopo il tournament. |
| CANDIDATE DEFECT | Antigravity ha errato il contract `private`; Copilot ha omesso bootstrap/routing e letto il player errato; Codex ha mantenuto un envelope economico/capacitivo ristretto. |
| NO EVIDENCE OF DEFECT | Non emerge una causa radice Foundation-level per i failure di Antigravity e Copilot: i dati e le transizioni necessarie erano già disponibili. |
| NO EVIDENCE OF DEFECT | Il mancato mirror automatico P0/P1 non è la causa: l'effetto di posizione dell'ambiente era trascurabile. Ciò non sostituisce il test di correttezza `observation.player`. |

## 10. Tre modifiche prioritarie

### 1. Modifica: rendere obbligatorio un `real-engine realization smoke` P0 e P1 per ogni candidato

**PROBLEMA RISOLTO:** intercetta contract mismatch, player-state binding errato,
fail-closed nascosto e policy che non supera l'inizializzazione reale.

**EVIDENZA:** Antigravity passa fixture/lista ma fallisce con `private` dict; Copilot
come P1 legge P0. Entrambi avrebbero fallito prima del torneo con una sola esecuzione
per seat.

**RISULTATO ATTESO:** nessun candidato ottiene `TOURNAMENT_READY` se non produce
almeno una transizione sul proprio stato o se attiva fallback.

**COME FALSIFICARLA:** eseguire un candidato noto difettoso e verificare che il gate lo
rifiuti; eseguire un candidato conforme in entrambi i seat e verificare che il gate non
produca falsi rifiuti.

### 2. Modifica: aggiungere al MODEL_SPEC un `initial-state-to-value contract`

**PROBLEMA RISOLTO:** impedisce che una policy locale venga presentata come policy
agricola completa quando i suoi prerequisiti (seed, tile, workforce, inventario) non
sono creati dal candidate.

**EVIDENZA:** Copilot richiede seed per `PLANT` ma ne possiede zero e non può comprarli.
E15 aveva già dimostrato che bootstrap, workforce, market e sell-through sono parte
della performance effettiva.

**RISULTATO ATTESO:** ogni MODEL_SPEC dichiara una catena verificabile dal vero stato
iniziale a superficie produttiva e, se mira a competitività, a revenue; i sottosistemi
deferiti devono avere una prova che non siano prerequisiti della catena.

**COME FALSIFICARLA:** sottoporre un MODEL_SPEC senza acquisizione seed ma con zero
seed iniziali; il contract deve risultare incompleto e impedire la readiness. Un
MODEL_SPEC che usa risorse iniziali non nulle può dimostrare esplicitamente tale
precondizione.

### 3. Modifica: sostituire il readiness basato su dispatch con un ledger minimo di transizioni e un gate di continuità economica

**PROBLEMA RISOLTO:** evita che action count, unit test o completion mascherino no-op e
che il corretto lifecycle venga valutato senza massa produttiva o monetizzazione.

**EVIDENZA:** Copilot emette 119.2 WATER, 136.2 HARVEST e 586.2 DIG medi con superficie
zero e cash invariato. Codex realizza il loop ma solo 9.17/17 tile medie, mentre E15
indica che capacity alignment e sell-through restano decisivi dopo la soglia operativa.

**RISULTATO ATTESO:** VERIFY misura `requested`, `accepted/no-op/failed`, tile/seed/
inventory/cash delta e active-surface trajectory; readiness richiede le transizioni
essenziali dichiarate e un criterio minimo di continuità, non un optimum economico.

**COME FALSIFICARLA:** su un replay con `DIG` dispatch ma nessun `WEED -> empty`, il
ledger deve classificarlo no-op e il gate deve fallire; su un loop reale deve collegare
acquisizione, PLANT, WATER, maturità, HARVEST e revenue senza confondere il solo action
count con successo.

## 11. Decisione singola che cambierei

Se potessi cambiare una sola decisione prima del tournament C2, cambierei la condizione
del master prompt che permetteva `TOURNAMENT_READY: YES` dopo test specifici e smoke
generico, sostituendola con l'obbligo di un **real-engine smoke di inizializzazione in
P0 e P1 che richieda almeno una transizione produttiva sulla propria farm**.

È una decisione concreta e a basso costo: avrebbe respinto Antigravity per il
`private` contract e Copilot per player binding/bootstrap nello stesso gate, senza
richiedere un torneo, tuning o una nuova Foundation. Avrebbe anche reso esplicito che
un candidato lifecycle-correct ma economicamente non inizializzabile non è pronto al
confronto competitivo.

```text
C2_ROUND_FEEDBACK_COMPLETE
NO_REMEDIATION_PERFORMED
```
