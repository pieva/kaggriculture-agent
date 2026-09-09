# MODEL_SPEC Copilot E18 — Economic Recovery V5

```text
AGENT_OWNER: COPILOT
MODEL: Copilot E18 economic recovery V5
VERSION: COPILOT-E18.8-ECONOMIC-RECOVERY-V5
STATUS: ACTIVE BASELINE / IMPLEMENTED / VERIFIED AGAINST ENGINE CONTRACT / NOT A KAGGLE SUBMISSION
FOUNDATION_BASELINE: C2.1 reconciled
ROUND: E18
IMPLEMENTATION: src/agricola/strategy/copilot/e18_economic_recovery_v5.py
```

## 1. Obiettivo e ipotesi

L’obiettivo della linea Copilot E18 `economic recovery V5` è costruire una baseline solida e verificabile che rispetti il contratto reale del motore Kaggriculture, senza impiegare una strategia derivata da routine altrui o un wrapper inutile. La policy mira a generare un ciclo economico osservabile e coerente: `BUY_SEED` → `PLANT` → `WATER` → `HARVEST` → `SELL`, con una scelta iniziale di lavoro e produzione orientata alla stabilità del cash iniziale.

Le ipotesi sono le seguenti:

- Il motore è compatibile con un loop economico reale basato sui semi, la coltivazione, l’irrigazione e la vendita, come documentato in [docs/foundation/ENGINE_CONTRACT.md](../../foundation/ENGINE_CONTRACT.md), [docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md](../../foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md) e [docs/foundation/ontology/ONTOLOGY_C2_1.md](../../foundation/ontology/ONTOLOGY_C2_1.md).
- Le osservazioni pubbliche e private vere del turno sono quelle fornite dal contratto osservativo condiviso: `CodexObservationAdapter.parse(...)` in [src/agricola/core/observation_contract.py](../../../src/agricola/core/observation_contract.py).
- L’efficienza non dipende da un modello di avversario attivo: la policy è una baseline controllata, progettata per essere ripetibile, semplice da diagnosi e stabile su più seed.
- Non si sostengono posizioni oltre l’evidenza: questa versione non è una strategia massimamente reattiva né una submission finale. È la baseline attiva per la revisione documentale di Copilot E18.

## 2. Strategia

La strategia è una “carrot loop” con gestione minima del capitale e del personale. La linea funziona così:

1. Sempre all’inizio del giorno, la policy controlla la disponibilità di denaro, il numero di hands e il livello di semi sul conto privato.
2. Se il numero di hands è inferiore al target configurato (`hire_target = 2`) e la partita è nelle prime giornate (`early_hire_days = 3`), invoca `HIRE` in modo limitato.
3. La scelta della coltura preferita è inizialmente `CARROT`, ma la policy ri-evaluta il prezzo di mercato e sceglie la coltura con prezzo più alto tra i crop`WHEAT`, `CARROT`, `TOMATO`, `STRAWBERRY` e `MELON` quando i dati di mercato sono presenti.
4. Se mancano semi per la coltura scelta e il denaro è sufficiente, invoca `BUY_SEED` per 1 unità del tipo più conveniente.
5. Sulla griglia, la policy scorre le tile e individua azioni di:
   - `DIG` sulle tile `WEED`;
   - `WATER` sulle piantine che non sono state irrigate oggi;
   - `HARVEST` sulle piantine mature;
   - `PLANT` di nuova coltura sulle tile vuote, rispettando la disponibilità di semi.
6. Quando la shed contiene prodotti vendibili con prezzo noto, la policy invia ordini di `SELL` appena prima di altri comandi (o comunque in modo non invasivo rispetto al loop di coltivazione).
7. Il farmer e i hands vengono assegnati per vicinanza alla cella obiettivo per ridurre il movimento inutile.

Il piano operativo è a orizzonte breve e controllato: non esiste una previsione di mercato futura, nessun look-ahead su avversari e nessuna supposta “ottimalità” oltre il loop verificato. La politica enfatizza la stabilità del cash, la continuità dell’accumulo e la coerenza con il ciclo vitale della pianta.

## 3. Decisioni implementate

### 3.1 Feature realmente usate

La policy usa feature osservabili in tempo reale e le trasforma in azioni. In particolare:

- `observation` / snapshot di `farms`: posizione del farmer, hands, tile e cash;
- `private.seeds`: stock di semi privato;
- `private.shed`: merci raccolte e pronte per la vendita;
- `market.prices`: prezzi di mercato per la scelta del crop; fallback a `CARROT` se i prezzi mancano;
- `tile.kind`, `tile.crop`, `tile.planted_day`, `tile.yield_units`, `tile.watered_today` per decidere semina, irrigazione e raccolta;
- `clock.hour` e `clock.day` per gestire l’hiring e la scansione delle tile in tempi ragionevoli.

### 3.2 Criteri di scelta

Il codice applica un ordinamento e un ciclo di priorità semplice ma coerente:

1. vendere merci mature e vendibili in cassa;
2. effettuare `HIRE` se è ancora nei primi giorni e il personale è insufficiente;
3. acquistare semi se la riserva è vuota e abbastanza denaro è disponibile;
4. lavorare le tile in ordine di distanza dal farmer / mano di lavoro;
5. privilegiare `HARVEST` su `WATER` su `PLANT` per la maturità, la salute delle piante e la resa;
6. usare la `PLANT` solo su tile vuote e con semi disponibili;
7. se il budget o lo stato non permettono un’azione leghere, declinare con `PASS` o con fallback sicuro.

### 3.3 Vincoli e parametri principali

| Parametro | Valore attuale | Motivazione |
|---|---:|---|
| `family` | `CARROT_LOOP` | Rotazione economica basata su coltura stabile e semplice |
| `preferred_crop` | `CARROT` | Baseline conservativa, robusta e verificabile |
| `hire_target` | `2` | Fino a due hands per aumentare il throughput iniziale |
| `early_hire_days` | `3` | Limita il costo di assunzione alla fase iniziale |
| `turns_per_day` | `24` | Compatibile con il contratto del motore |
| `episode_steps` | `720` | Orizzonte standard della partita |

## 4. Reazioni e fallback

La policy gestisce i casi incerti in modo rigido e sicuro:

- Se i prezzi di mercato non sono disponibili, usa `CARROT` come default.
- Se la riserva di semi è esaurita ma il denaro è adeguato, compra 1 seme del crop attivo.
- Se un’azione lancia un’eccezione o la serializzazione del snapshot fallisce, la policy torna al fallback `SAFE_PASS`.
- Se si verifica un errore tecnico, incrementa `technical_errors` e `fallback_count` e ritorna a un comando do-nothing sicuro.
- Non esiste una logica di opponent-reactive vera: le azioni prima dell’early loop sono deterministiche e contengono un modello minimale di rischio economico, non di manipolazione avversaria.

## 5. Coerenza con la Foundation

Questa policy è coerente con la Foundation attiva C2.1:

- [docs/foundation/ENGINE_CONTRACT.md](../../foundation/ENGINE_CONTRACT.md): il modello rispetta l’ordine del turno, i limiti di mercato e la distinzione tra osservazione e esito reale.
- [docs/foundation/ontology/ONTOLOGY_C2_1.md](../../foundation/ontology/ONTOLOGY_C2_1.md): la policy usa concetti come `money`, `seeds`, `shed`, `tile.kind`, `tile.crop`, `planted_day`, `watered_today` senza inventare nuove leggi del dominio.
- [docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md](../../foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md): il loop di produzione e della crescita biologica segue il ciclo di semina, irrigazione, raccolta e vendita documentato.
- [docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md](../../foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md) e [docs/foundation/feature_model/FEATURE_CATALOG.md](../../foundation/feature_model/FEATURE_CATALOG.md): le feature usate sono osservabili o derivabili nello stato corrente; non si usano metriche post-hoc o future leak.

La discrepanza principale è che questa versione non attua ancora un modello robusto di reattività al comportamento dell’avversario. È una baseline economica valida e verificata, ma non una strategia massima di competitive play.

## 6. Stato di realizzazione

### 6.1 Implementato

- Baseline economica in runtime: `src/agricola/strategy/copilot/e18_economic_recovery_v5.py`
- Adattatore osservativo condiviso: `src/agricola/core/observation_contract.py`
- Configurazione attiva: `docs/model_specs/copilot/e18/configs/COPILOT_E18_8_ECONOMIC_RECOVERY_V5.json`
- Runner di benchmark: `docs/model_specs/copilot/e18/tools/run_copilot_e18_economic_recovery_v5_tournament.py`
- Archivio di evidenza: `docs/model_specs/copilot/e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json`

### 6.2 Parziale / futura evoluzione

- Nessuna logica reattiva contro l’avversario implementata in questa baseline.
- Nessun modello di scheduling avanzato di market, livestock o expansion multi-quadrant.
- Nessuna submission Kaggle autorizzata generata da questa policy.

### 6.3 Proposta futura

Una naturale evoluzione è una V6 “mild reactive baseline” che conserva la stabilità del loop economico e aggiunge una risposta controllata a segnali come overgrowth, domanda di mercato, stato delle tile e saturazione del personale, senza interrompere la solidità del ciclo di base.

## 7. File di implementazione

| File, con link relativo funzionante | Ruolo | Parte della strategia implementata | Categoria |
|---|---|---|---|
| [../../../src/agricola/strategy/copilot/e18_economic_recovery_v5.py](../../../src/agricola/strategy/copilot/e18_economic_recovery_v5.py) | Implementazione della politica e del loop di decisione. | `CopilotE18EconomicRecoveryV5Policy`, ciclo di hire-buys-seed-plant-water-harvest-sell, fallback sicuro. | Runtime |
| [../../../src/agricola/core/observation_contract.py](../../../src/agricola/core/observation_contract.py) | Contratto osservativo condiviso usato per normalizzare l’input. | Parsing dell’osservazione, clock, farm e private state. | Runtime |
| [../e18/configs/COPILOT_E18_8_ECONOMIC_RECOVERY_V5.json](e18/configs/COPILOT_E18_8_ECONOMIC_RECOVERY_V5.json) | Configurazione del candidato e parametri di policy. | `preferred_crop`, `hire_target`, `early_hire_days`, `turns_per_day`, `episode_steps`. | Configurazione |
| [../e18/tools/run_copilot_e18_economic_recovery_v5_tournament.py](e18/tools/run_copilot_e18_economic_recovery_v5_tournament.py) | Runner del benchmark per confronto diretto. | Esegue match contro Claude e Antigravity con le seed del range. | Builder / verifica |
| [../e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json](e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json) | Evidenza del benchmark sintetica. | Risultati consolidati, seed e controllo dei match. | Evidence / report |

Non sono stati identificati file di submission o bundle Kaggle “canonical” attivi per questa versione. I file di sviluppo e le evidenze sono stati separati dal runtime del motore e da eventuali pubblicazioni di benchmark, come richiesto dal processo di documentazione.

## 8. Benchmark e cronologia

### 8.1 Evidenza benchmark corrente

Il benchmark attualmente presente nel repository è registrato in [docs/model_specs/copilot/e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json](e18/artifacts/derived/E18_COPILOT_ECONOMIC_RECOVERY_V5_TOURNAMENT.json).

Sintesi:

- `COPILOT_E18_8`: 14 match, 14 vittorie, 0 sconfitte, media cassa `21232.71`.
- `CLAUDE_E18_2`: 14 match, 6 vittorie, 8 sconfitte, media cassa `11688.21`.
- `ANTIGRAVITY_E18_1`: 14 match, 1 vittoria, 13 sconfitte, media cassa `8667.93`.

Questa evidenza è compatibile con la dichiarazione di baseline attiva e stabile. È un benchmark di validazione del contratto e della solidità economica, non una certificazione di massima performance strategica o di submission production.

### 8.2 Storia documentale

- [docs/model_specs/copilot/README.md](README.md): indice attivo della linea Copilot e registro delle versioni attive e congelate.
- [docs/model_specs/copilot/MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md](MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md): revision pre-v5, conservata come documentazione storica e non attiva.

## 9. Discrepanze o parti non implementate

- Non esiste una logica di avversario realmente reattiva; il modello non osserva intenzioni o trend avversari in modo strategico.
- Non esiste una pipeline di submission o builder Kaggle canonicalizzato per questa versione.
- Non sono presenti test automatizzati dedicati a questa baseline; l’evidenza disponibile è la validazione del benchmark locale e la lettura del codice.
- La versione è stabilmente funzionante come baseline economica, ma non rappresenta il massimo confronto competitivo o il livello di complessità atteso per una cannonica top-tier policy.

## 10. Chiusura

Questa `MODEL_SPEC` descrive il modello attivo di Copilot E18 come una baseline controllata, coesa con la Foundation e verificabile nel codice. La strategia è semplice e robusta: costruire un loop di crescita e liquidi reali senza ricorrere a routine non attribuibili o a future-leakage. La prossima fase ragionevole, dopo la stabilizzazione documentale, è una V6 più reattiva ma comunque conservativa, che aumenti la capacità di adattamento senza compromettere il loop di base attualmente verificato.
