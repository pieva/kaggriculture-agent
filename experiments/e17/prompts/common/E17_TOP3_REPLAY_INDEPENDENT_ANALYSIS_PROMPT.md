# Prompt operativo — E17 analisi indipendente replay Top 3

## Destinatari

Questo prompt deve essere eseguito **separatamente** da:

- Antigravity;
- Copilot.

All'avvio dichiara `AGENT_ID = antigravity` oppure
`AGENT_ID = copilot` e usa esclusivamente i percorsi assegnati al tuo
agente.

## Scopo

Analizzare in modo forense e quantitativo i nove replay del benchmark E17
per individuare:

1. le proprietà strategiche comuni agli agenti ai vertici della
   leaderboard;
2. le differenze persistenti fra tetsuya, OceanMix e Crop Dusta;
3. i gap osservabili rispetto al MODEL_SPEC e alla routine 3Q del proprio
   agente;
4. ipotesi sperimentali falsificabili per la ripresa della sequenza da
   E17.

Questa fase è **ANALYSIS ONLY**. Non modificare routine, submission,
Foundation, MODEL_SPEC, test, stato di progetto o log sperimentale. Non
avviare tornei e non dichiarare miglioramenti di score non misurati.

## Vincolo di indipendenza

L'analisi deve restare strategicamente indipendente.

- Non leggere il MODEL_SPEC dell'altro agente.
- Non leggere report, script o output E17 prodotti da Codex o dall'altro
  destinatario prima di aver chiuso e firmato il proprio report.
- Non importare, copiare o adattare routine di altri agenti.
- Non creare una routine di analisi condivisa con altri agenti.
- Se serve codice di estrazione, realizzalo autonomamente e salvalo solo
  nel namespace del tuo agente.
- È ammesso usare la Foundation comune come contratto semantico, non come
  fonte di conclusioni strategiche precostituite.

## Input obbligatori

Leggi integralmente:

1. `data/replays/json/json.md`;
2. `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`;
3. `docs/foundation/ontology/ONTOLOGY_C2_1.md`;
4. `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md`;
5. `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md`;
6. il MODEL_SPEC del tuo agente:
   - Antigravity:
     `docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md`;
   - Copilot:
     `docs/model_specs/copilot/MODEL_SPEC_COPILOT_C2_3Q_POST_FOUNDATION_REVIEW.md`.

Analizza tutti e soltanto questi replay E17:

- `data/replays/json/104527555.json`;
- `data/replays/json/104541810.json`;
- `data/replays/json/104543983.json`;
- `data/replays/json/104547425.json`;
- `data/replays/json/104564762.json`;
- `data/replays/json/104577270.json`;
- `data/replays/json/104578185.json`;
- `data/replays/json/104586335.json`;
- `data/replays/json/104586487.json`.

Non includere automaticamente altri `*.json` trovati nella directory.

## Controlli preliminari obbligatori

Prima dell'analisi:

1. verifica che i nove JSON siano validi e distinti per `EpisodeId`;
2. verifica `module_version`, numero di step e stato terminale;
3. riconcilia agenti e reward con `data/replays/json/json.md`;
4. registra eventuali discrepanze e fermati se una discrepanza rende il
   corpus ambiguo;
5. identifica con precisione il lato/player index di ogni agente in ogni
   replay.

## Analisi richiesta

### A. Ricostruzione cronologica per episodio

Per ciascun agente e replay ricostruisci almeno:

- denaro e variazione del denaro per giorno;
- tempi di sblocco di Q1, Q2 e Q3;
- distribuzione e densità d'uso dei quadranti;
- numero di farm hands e cadenza delle assunzioni;
- celle produttive attive per colture, pasture e coop;
- mix di colture e specie animali;
- build, acquisto, cura, alimentazione, raccolta e vendita;
- inventario, seed e stock rilevanti;
- ricorso a fertilizzante e continuità watering;
- weeds, celle inattive, strutture vuote e capacità inutilizzata;
- traffico, distanze, accentramento e possibili conflitti di routing;
- cadenza di liquidazione e comportamento terminale;
- principali breakpoint economici e operativi.

Usa milestone coerenti con l'evidenza disponibile. Non interpolare stati
mai osservati e non trasformare automaticamente l'ultimo snapshot di un
giorno in causa degli eventi del giorno successivo.

### B. Confronto fra i tre agenti Top 3

Separa:

1. pattern presenti in tutti e tre;
2. pattern presenti in due agenti;
3. scelte specifiche di un solo agente;
4. comportamento dipendente da avversario, seed o mercato;
5. strategie robuste fra vittorie e sconfitte;
6. strategie osservate soltanto in un singolo episodio.

Confronta in particolare:

- sequenza e timing di espansione 3Q;
- capitale trattenuto rispetto a capitale convertito in capacità;
- produttività marginale di hands, colture e livestock;
- centralizzazione rispetto a specializzazione per quadrante;
- densità produttiva, travel cost e servicing burden;
- stabilità della produzione nelle transizioni fra periodi;
- esposizione al mercato condiviso;
- differenze tra score finale, asset produttivi e liquidità terminale.

Evidenzia esplicitamente l'assenza di scontri diretti tetsuya–OceanMix e
non inferire da essa un ordinamento causale fra i due.

### C. Gap rispetto al proprio agente

Confronta le evidenze con il MODEL_SPEC e, se il percorso è identificato
senza ambiguità, con la submission 3Q corrente del tuo agente.

Per ogni gap indica:

- evidenza nei replay, con `EpisodeId`, player index, giorno e/o step;
- comportamento corrente del tuo modello;
- natura del gap: rappresentazione, policy, scheduling, routing,
  economia, servicing, liquidazione o implementazione;
- impatto atteso;
- confidenza `HIGH`, `MEDIUM` o `LOW`;
- informazione mancante che impedisce una conclusione più forte.

Non leggere né usare submission appartenenti agli altri agenti.

### D. Ipotesi per E17

Formula una short list prioritaria di ipotesi testabili. Ogni ipotesi deve
contenere:

1. meccanismo causale proposto;
2. evidenza osservativa a supporto e controevidenza;
3. singola modifica o fattore sperimentale;
4. baseline e controllo;
5. seed policy e numero minimo di repliche;
6. metrica primaria e metriche diagnostiche;
7. criterio di promozione;
8. criterio di falsificazione o rollback;
9. rischio di regressione;
10. costo informativo e priorità.

Non proporre un grande rewrite come primo esperimento. Privilegia
contrasti piccoli, interpretabili e reversibili.

## Disciplina epistemica

Etichetta ogni conclusione come:

- `OBSERVED`: direttamente misurata nel replay;
- `DERIVED`: calcolata deterministicamente da campi osservati;
- `INFERRED`: spiegazione plausibile ma non identificata causalmente;
- `UNKNOWN`: non determinabile dal corpus.

Vincoli:

- nessun cherry-picking: tutti i nove episodi devono essere rappresentati;
- non confondere reward dell'episodio e rating leaderboard;
- non usare il risultato della partita come unica misura di qualità;
- non trattare nove episodi osservazionali come prova definitiva;
- non usare informazioni future per costruire feature dichiarate online;
- non inventare prezzi, azioni, inventari o timing assenti;
- ogni numero importante deve essere riproducibile dal JSON.

## Output obbligatori e isolamento dei percorsi

### Se `AGENT_ID = antigravity`

Scrivi esclusivamente:

- `experiments/e17/artifacts/discovery/antigravity/E17_TOP3_REPLAY_METRICS.json`;
- `experiments/e17/reports/antigravity/E17_TOP3_REPLAY_ANALYSIS.md`;
- opzionale, se necessario:
  `experiments/e17/tools/antigravity/analyze_top3_replays.py`.

### Se `AGENT_ID = copilot`

Scrivi esclusivamente:

- `experiments/e17/artifacts/discovery/copilot/E17_TOP3_REPLAY_METRICS.json`;
- `experiments/e17/reports/copilot/E17_TOP3_REPLAY_ANALYSIS.md`;
- opzionale, se necessario:
  `experiments/e17/tools/copilot/analyze_top3_replays.py`.

Il JSON delle metriche deve contenere almeno:

- provenance e versione schema;
- hash SHA-256 dei nove input;
- metriche per episodio, agente, giorno e quadrante;
- milestone di espansione e workforce;
- metriche produttive, servicing, mercato e liquidazione;
- elenco esplicito dei campi non calcolabili.

Il report Markdown deve contenere almeno:

1. executive summary;
2. verifica corpus e metodologia;
3. nove schede episodio sintetiche;
4. confronto quantitativo Top 3;
5. pattern comuni e differenze;
6. gap rispetto al proprio agente;
7. ipotesi E17 ordinate per valore informativo;
8. rischi, limiti e unknowns;
9. raccomandazione del primo esperimento, senza implementarlo.

## Divieti operativi

- Non modificare i nove replay.
- Non cancellare o spostare file.
- Non modificare `submission/`.
- Non modificare la Foundation o i MODEL_SPEC.
- Non modificare `docs/PROJECT_STATE.md`, `docs/NEW_SESSION.md` o
  `docs/EXPERIMENT_LOG.md`.
- Non eseguire commit o push.
- Non avviare l'implementazione delle ipotesi.
- Non fare riconciliazione con l'altro agente in questa fase.

## Chiusura

Concludi indicando:

- percorsi degli output creati;
- test o controlli eseguiti;
- numero di episodi e step effettivamente processati;
- principale ipotesi consigliata per E17;
- eventuali blocker;
- conferma esplicita di non aver consultato output o routine degli altri
  agenti.

Fermati dopo la produzione degli artefatti di analisi indipendente.
