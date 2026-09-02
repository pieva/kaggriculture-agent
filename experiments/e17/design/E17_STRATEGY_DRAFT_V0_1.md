# E17 — Strategia di benchmark e ottimizzazione 3Q

- **Versione:** `DRAFT V0.1`
- **Data:** 2026-09-02
- **Fase:** `DEFINE`
- **Autorizzazione implementativa:** solo E17.0 dopo freeze; nessuna mutazione policy ancora autorizzata
- **Foundation:** C2.1

## 1. Obiettivo

E17 deve trasformare il miglioramento esterno dei modelli 3Q in un ciclo
di ottimizzazione causalmente attribuibile. Il problema non è più dimostrare
che tre quadranti possano funzionare: è distinguere quali meccanismi migliorano
robustezza competitiva, floor e rating Kaggle senza confondere produzione
nominale, contesa di mercato e azioni non eseguite.

La metrica finale di interesse è la prestazione competitiva esterna. Le
metriche locali sono surrogate che devono essere validate, non equivalenti al
rating Kaggle. Il documento è la guida comune per Codex, Antigravity e
Copilot; baseline, policy e implementazioni strategiche restano agent-local e
devono superare il gate di indipendenza.

### 1.1 Principio cardine — nessun archetipo preselezionato

E17 non cerca di trasformare Codex in `tetsuya`, `OceanMix` o `Crop Dusta`.
I tre profili sono punti osservati in uno spazio strategico multidimensionale:

- timing di Q1/Q2;
- distribuzione spaziale di crop e livestock;
- densità di asset e carico di servicing;
- numero e composizione di specie animali;
- numero e composizione di colture;
- velocità di reinvestimento e riserva di cassa;
- gestione della contesa di mercato;
- liquidazione e servicing terminale.

Nessun profilo identifica da solo l'effetto di una dimensione, perché ogni
replay combina più scelte contemporaneamente. Gli archetipi servono a definire
livelli plausibili dei fattori, non candidate da copiare integralmente.

La strategia sperimentale deve quindi:

1. misurare gli **effetti principali** modificando una sola dimensione;
2. misurare successivamente le **interazioni preregistrate** che hanno un
   meccanismo causale esplicito;
3. costruire una candidata composita soltanto con componenti promosse;
4. confrontare la composita con le singole linee, evitando il cherry-picking
   post-hoc delle caratteristiche migliori.

## 2. Evidenza di partenza

Il corpus E17 contiene nove replay unici dei tre player che erano Top 3 nello
snapshot di raccolta:

- `tetsuya`: Q1 D7, Q2 D10, 3Q distribuito, zero eventi di fuga derivati;
- `OceanMix`: Q1 D6, Q2 D11, livestock Q0/Q1 e Q2 crop-only, routing migliore;
- `Crop Dusta`: Q1 D5–D6, Q2 D8–D9, massima diversificazione, 31 eventi di fuga EOD derivati.

Le review Copilot e Antigravity convergono su ledger, indipendenza e ablation
monofattoriali. Restano non dimostrati:

- ottimalità globale di 3Q e 12 hands;
- causalità fra anticipo Q2 e rendimento;
- causalità fra layout disperso e fughe;
- vantaggio di CARROT, GOOSE o TOMATO;
- correlazione quantitativa tra denaro locale e rating Kaggle.

### Aggiornamento leaderboard 2026-09-02

Il nuovo snapshot visibile è:

```text
1. Crop Dusta  2917.8
2. tetsuya     2890.3
3. 3정훈       2878.5
```

`OceanMix` non compare nei primi sette visibili. Il passaggio di Crop Dusta
dal terzo al primo posto produce due conseguenze:

1. il corpus non deve più essere denominato Top 3 corrente, ma benchmark di
   tre archetipi raccolti da un precedente Top 3;
2. la frontiera ultra-precoce e diversificata di Crop Dusta deve essere
   testata obbligatoriamente prima della chiusura di E17, pur restando
   subordinata a ledger, isolamento causale e zero fughe.

Il cambio di rating non dimostra che D8, TOMATO, GOOSE o le fughe terminali
causino la leadership. Rafforza soltanto il valore informativo di RQ6 e vieta
di liquidare l'archetipo Crop Dusta sulla base del record 2–3 nei nove replay.

## 3. Baseline Codex congelata

| Artefatto | SHA-256 |
|---|---|
| `submission/submission_codex.py` | `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421` |
| `docs/governance/history/model_spec_c2/codex/freeze/submission_codex_v9_tournament.py` | `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421` |
| `src/agricola/strategy/codex/codex_3q_mixed_high_density.py` | `4D99C919B59DAE9B307C403FCF3198763B08FB9D15324AB8C937C4FC2B32090E` |
| `src/agricola/strategy/codex/codex_v9_routine_data.py` | `AC5819014EBB85ED86BA5D25D4F01DE46F9E4760465B7188DF11E69C8812F774` |
| `docs/model_specs/codex/configs/CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json` | `44DD0EC2F33C9EEEE74AE5676580DC833325AB969D8A9D262EC870FEAAAC6C99` |

Identità strategica:

```text
ROUTINE_LENGTH: 719
ROUTINE_ACTION_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
Q1: D6
Q2: D11
PEAK_HANDS: 12
PEAK_CROPS: 55
PEAK_ANIMALS: 19
MOVE_PER_PRODUCTIVE: 1.2477
ANIMAL_ESCAPES: 0
```

Questa baseline non può essere modificata in place. Ogni candidata E17 deve
avere nuovo ID, source, config, freeze e hash.

## 4. Domande causali ordinate

| ID | Domanda | Fattore manipolato | Fattori da congelare |
|---|---|---|---|
| RQ0 | Possiamo misurare gli esiti senza cambiare la policy? | sola telemetria | tutte le 719 azioni |
| RQ1 | Una guardia fill-aware WHEAT migliora il floor sotto contesa? | recovery di ordini WHEAT non eseguiti | timing Q, layout, mix, workforce |
| RQ2 | Compattare il bestiame in Q0/Q1 converte MOVE in produzione? | allocazione spaziale pasture/livestock | totale asset, timing Q, mix, workforce |
| RQ3 | Q2 a D10 produce un ciclo utile aggiuntivo? | solo timing acquisizione/attivazione Q2 | topologia scelta, mix, workforce |
| RQ4 | Una liquidazione inventory-aware riduce residui e varianza? | sola logica D26–D29 | produzione D0–D25 |
| RQ5 | Una nuova specie diversifica utilmente i ricavi? | una sola specie per run | timing, layout e altre specie |
| RQ6 | La frontiera Q2 D8 del leader aggiornato è serviceable senza fuga e senza collasso routing? | solo frontiera temporale | candidata migliore precedente |

L'ordine non implica che ogni fase debba essere eseguita: una fase si apre
solo se la precedente supera i propri gate o produce informazione sufficiente
per una preregistrazione revisionata.

RQ6 è ora un checkpoint obbligatorio di chiusura E17, non una promozione
automatica né il primo esperimento. Resta ultimo perché senza ledger e senza
una topologia serviceable il confronto D8/D10/D11 non sarebbe attribuibile.

### 4.1 Fattori e livelli minimi

| Fattore | Livelli iniziali | Origine osservativa | Outcome causali principali |
|---|---|---|---|
| Timing Q2 | D11, D10, D8 | OceanMix/V9, tetsuya, Crop Dusta | output addizionale, cash floor, travel, missed service |
| Topologia livestock | distribuita, compatta Q0/Q1, pienamente mista | tetsuya/V9, OceanMix, Crop Dusta | MOVE, azioni produttive, crop capacity, fughe |
| Crop diversity | 3, 4, 5 specie | V9, tetsuya/OceanMix, Crop Dusta | fill, ricavi, inventory risk, complessità routing |
| Animal diversity | 2, 3 specie | V9/OceanMix, tetsuya/Crop Dusta | feed burden, cicli ricavo, travel, servicing |
| Capitale | reinvestimento rapido, riserva liquida | tetsuya, OceanMix | giorno Q2, fill, resilienza alla contesa |
| Chiusura | schedule fisso, inventory-aware | V9, comportamento terminale Top 3 | invenduto, ultimo ciclo utile, rischio animale |

I livelli “3/4/5 specie” non autorizzano a cambiare simultaneamente l'intero
mix. Per i crop: baseline V9 → aggiunta/sostituzione CARROT → TOMATO in un
esperimento distinto. Per gli animali: baseline COW/SHEEP → GOOSE come singolo
contrasto. Quantità totali e capitale devono restare controllati quando il
fattore studiato è la diversificazione.

### 4.2 Interazioni preregistrabili dopo gli effetti principali

| Interazione | Meccanismo da verificare |
|---|---|
| timing × topologia | D8/D10 può essere utile solo con percorsi sufficientemente compatti |
| timing × servicing | l'output anticipato può essere annullato da feed/care mancati |
| diversificazione × mercato | più specie possono ridurre contesa o aumentare ordini inevasi |
| topologia × densità | la stessa disposizione può cambiare valore al variare del numero di animali |
| capitale × timing | la riserva può ritardare Q2 ma proteggere fill e operazioni essenziali |
| chiusura × livestock | il servicing terminale può avere rendimento marginale diverso per specie |

Nessuna interazione entra nel piano solo perché combina due vincitori
osservati. Deve essere motivata, preregistrata e confrontata con entrambi gli
effetti principali corrispondenti.

## 5. E17.0 — Measurement parity

### 5.1 Ledger minimo

Ogni comando deve produrre un record append-only con:

```text
episode_id, seed, seat, player_id
step, day, hour, unit_id
requested_command, requested_parameters
pre_state_fingerprint, post_state_fingerprint
cash_before, cash_after
inventory_before, inventory_after
tile_or_asset_before, tile_or_asset_after
outcome: EXECUTED | NOT_EXECUTED | UNKNOWN
outcome_evidence
quadrant_slot
policy_version, source_hash, config_hash, routine_hash
```

Per gli ordini di mercato aggiungere quantità richiesta, quantità attribuita
come eseguita, prezzo/cash delta osservato e motivo dell'eventuale `UNKNOWN`.
La copertura di registrazione deve essere 100%; la copertura di classificazione
executed deve essere riportata separatamente, senza convertire ambiguità in
successi o fallimenti.

### 5.2 Invarianti E17.0 Codex

```text
ACTION_PARITY: 719/719 per episodio compatibile
ACTION_SEQUENCE_SHA: invariato rispetto alla baseline
FINAL_OUTCOME_PARITY: esatto a parità di seed/seat/opponent
ERRORS: 0
FALLBACK_DELTA: 0
LEDGER_RECORD_COVERAGE: 100%
MARKET_OUTCOME_COVERAGE: 100% prima di E17.1
```

La telemetria deve restare fuori dal percorso decisionale. Qualsiasi delta di
azione o risultato blocca E17 e viene classificato come instrumentation bug.

### 5.3 Indipendenza degli altri agenti

Antigravity V4 e Copilot V2 restano baseline derivative. Prima di entrare nel
torneo E17 devono ciascuno produrre un decision-maker nativo, senza import o
copia di routine, planner, dispatcher o action table Codex/altro agente.

```text
NO_IMPORT_OTHER_AGENT_ROUTINE: REQUIRED
NO_COPY_OTHER_AGENT_ACTION_TABLE: REQUIRED
NO_IDENTICAL_ROUTINE_SHA: REQUIRED
PROVENANCE_DISCLOSURE: REQUIRED
```

## 6. Architettura del benchmark

### Livello A — Contract e instrumentation

- test unitari del ledger;
- validazione schema;
- parità azione-per-azione;
- replay di eventi noti, incluse le 31 transizioni EOD derivate.

### Livello B — Economia passiva

- opponent `INERT_PASS_POLICY`;
- misura ceiling produttivo, seed sensitivity e seat;
- non è evidenza competitiva sufficiente.

### Livello C — Contesa mirror

- candidata contro la propria freeze e contro Codex V9;
- misura cannibalizzazione, fill, seat e desincronizzazione;
- è il livello primario per E17.1.

### Livello D — Torneo indipendente

- si apre solo quando almeno due policy superano il gate di indipendenza;
- tutte le coppie, entrambi i seat, stessi seed preregistrati;
- nessuna policy derivativa può essere presentata come agente indipendente.

### Livello E — Validazione Kaggle

- una sola candidata promossa per checkpoint rilevante;
- source standalone e hash congelati prima dell'upload;
- descrizione con ID esperimento e singolo fattore modificato;
- rating e numero di episodi completati registrati nella stessa finestra di osservazione;
- nessun tuning retroattivo sui replay prodotti dalla candidata.

## 7. Seed policy preregistrata

### Development — già osservati, mai holdout

```text
26090101
26090102
26090103
1838889274
1619968655
710418712
562040596
```

### Holdout E17 — non eseguire prima del freeze della candidata

Generazione: primi 32 bit big-endian di
`SHA256("kaggriculture-e17-c2.1-holdout-v1:{i}")`, mascherati a 31 bit.

```text
207899150
1866713870
1953344146
412628772
157353689
352254289
```

### Final confirmation — usare una sola volta per candidata promossa

Generazione analoga con namespace `final-v1`:

```text
1182799305
1144076852
1172855418
1075728698
```

Ogni seed è eseguito in entrambi i seat. Nessun episodio fallito può essere
rimosso o sostituito; errori e opening failure restano nel denominatore.

## 8. Metriche obbligatorie

### Outcome

- final money: media, mediana, min, max, deviazione standard;
- win rate, margine medio e floor per opponent/seat;
- rating Kaggle separato dalle metriche locali.

### Temporalità e topologia

- step/giorno di Q1 e Q2;
- giorno primo output e payback per quadrante;
- crop, animali, strutture, weed e tile inattive per Q0/Q1/Q2 a fine giornata;
- distanza e MOVE attribuiti per ruolo/quadrante.

### Produzione e servizio

- productive actions, MOVE, PASS e rapporti;
- water, fertilize, feed, care, collect, harvest;
- starvation risk, fughe `DERIVED`, missed service e capacità hands;
- inventario prodotto, venduto e residuo.

### Mercato ed esecuzione

- requested/executed/unknown per tipo di ordine;
- fill rate, quantità e cash delta;
- fallimenti per stock, cash, prezzo, conflitto o causa non identificata;
- contesa e differenze per seat.

## 9. Gate

### Gate obbligatori per ogni candidata

```text
TECHNICAL_ERRORS == 0
ANIMAL_ESCAPES == 0
LEDGER_RECORD_COVERAGE == 100%
NO_POST_HOC_SEED_REMOVAL == true
SOURCE_CONFIG_FREEZE == true
```

### Target finali Codex E17

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR >= 90000
MOVE_PER_PRODUCTIVE <= 1.20
EXECUTED_MARKET_LEDGER_COVERAGE == 100%
```

Per un singolo esperimento è ammessa la classificazione `INFORMATIVE_ONLY`
se falsifica l'ipotesi senza superare i target. Non può però essere promosso
come submission.

## 10. Regole di isolamento e arresto

- una sola riga RQ può essere manipolata per candidata;
- tutti i parametri non dichiarati devono avere hash o diff invarianti;
- una fuga, un errore tecnico o una perdita sistematica di floor impone rollback;
- nessun branch su seed-ID o dati futuri;
- i replay Top 3 possono guidare ipotesi offline, mai decisioni runtime;
- dopo due fallimenti coerenti della stessa ipotesi, chiuderla o ridefinirne il meccanismo prima di altri run;
- nessuna combinazione di due varianti perdenti senza nuovo razionale causale.

## 11. Decisione richiesta per il freeze V0.1

Prima dell'implementazione E17.0 devono essere approvati:

1. schema del ledger e significato di `EXECUTED/NOT_EXECUTED/UNKNOWN`;
2. seed development, holdout e final confirmation;
3. livelli A–E e opponent ammessi;
4. gate assoluti e regole di non-inferiorità;
5. ordine RQ0→RQ6;
6. responsabilità separate dei tre agenti e gate di indipendenza.

Fino a quel freeze:

```text
E17_STATUS: DEFINE
POLICY_MUTATION: FORBIDDEN
KAGGLE_SUBMISSION: FORBIDDEN
NEXT_ALLOWED_WORK: REVIEW_AND_FREEZE_E17_STRATEGY
```
