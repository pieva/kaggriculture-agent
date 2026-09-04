# Review Codex della strategia E17

- **Data:** 2026-09-02
- **Reviewer:** Codex
- **Decisione:** `ACCEPT_WITH_CHANGES`
- **Ambito:** B1, prima del freeze V1

## Valutazione

Il draft è metodologicamente adeguato: non preseleziona un archetipo, separa
effetti principali e interazioni, mantiene distinti discovery replay, runner
locali e Kaggle, e impone l'osservabilità prima dell'ottimizzazione. L'ordine
RQ0→RQ6 è accettabile, inclusa la frontiera D8 come checkpoint obbligatorio ma
non come candidata implicitamente promossa.

## Ledger

Lo schema minimo è completo come inventario di campi, ma prima del freeze deve
specificare la chiave di correlazione e l'autorità dell'esito:

1. aggiungere `command_id`, `batch_index` e `observation_step_received`;
2. definire `EXECUTED` solo con evento engine o delta di stato univocamente
   attribuibile al comando;
3. definire `NOT_EXECUTED` solo con evidenza negativa esplicita o scadenza
   osservabile della richiesta;
4. mantenere `UNKNOWN` quando più comandi possono spiegare lo stesso delta;
5. separare copertura dei record, copertura della classificazione e copertura
   del valore/quantità eseguita;
6. rendere l'audit delle fughe un ledger di transizioni EOD, con stato animale
   prima/dopo e classificazione `DERIVED`, senza assimilarlo a un comando.

Il ledger può essere condiviso perché misura, ma non deve fornire segnali alla
policy durante E17.0.

## Seed, holdout e opponent

I seed sono preregistrati e separati correttamente. Il freeze deve aggiungere:

- hash e entry point degli opponent `INERT_PASS_POLICY` e delle freeze mirror;
- matrice esplicita `seed × seat × opponent × livello`;
- quarantena del holdout: nessun report intermedio può esporre i risultati al
  decision-maker prima del freeze della candidata;
- definizione non ambigua di `COMPETITIVE_MIRROR >= 90000` (metrica, aggregato,
  seat e denominatore);
- divieto di sostituire episodi falliti, già presente e da riportare nel
  manifest macchina.

E17.0 può usare development e contract fixtures; non deve consumare holdout o
final confirmation per dimostrare la sola parità strumentale.

## Confondimento causale

Il controllo monofattoriale è valido. Per evitare confondimento residuo il
manifest di ogni candidata deve contenere un diff dei parametri e gli hash
degli invarianti. Quantità totali, workforce, densità, riserva e calendario di
servizio vanno congelati quando non sono il fattore manipolato. Le interazioni
si aprono solo dopo la misura separata di entrambi gli effetti principali.

## Indipendenza strategica

La regola è corretta. Occorre distinguere formalmente:

- Codex V9: `MEASUREMENT_PARITY`, nessuna sostituzione di baseline;
- Antigravity/Copilot: `NATIVE_BASELINE_CONSTRUCTION`, nuova provenance e
  nessun import/copia di routine altrui;
- E17.1+: `POLICY_OPTIMIZATION`, non autorizzata da questo prompt.

La costruzione nativa in E17.0 è una sostituzione della baseline derivativa,
non un effetto sperimentale da confrontare causalmente con RQ1–RQ6. Per ogni
baseline nativa servono test di determinismo, source/config freeze e routine
fingerprint differente da Codex; la parità 719/719 si applica solo alle
baseline dichiarate byte/comportamentalmente congelate.

## Correzioni indispensabili prima del freeze

1. Formalizzare schema ledger V1 e regole `EXECUTED/NOT_EXECUTED/UNKNOWN`.
2. Congelare opponent/entry point/hash e matrici dei livelli A–D.
3. Rendere machine-readable seed policy, gate e divieto di sostituzione.
4. Separare target comuni assoluti dai target agent-local; i target numerici
   Codex non devono diventare automaticamente gate degli altri agenti.
5. Esplicitare che E17.0 non usa holdout/final confirmation.
6. Esplicitare i tre diversi tipi di gate: parità Codex, riproducibilità delle
   baseline native, indipendenza strategica prima del torneo.

## Decisione

```text
LEDGER_COMPLETENESS: ACCEPT_WITH_CHANGES
SEED_POLICY: ACCEPT_WITH_CHANGES
HOLDOUT_POLICY: ACCEPT_WITH_CHANGES
OPPONENT_FREEZE: CHANGE_REQUIRED
CAUSAL_ISOLATION: ACCEPT
STRATEGIC_INDEPENDENCE: ACCEPT_WITH_CHANGES
DECISION: ACCEPT_WITH_CHANGES
BLOCKERS_TO_FREEZE: 6 correzioni sopra
POLICY_MUTATION_AUTHORIZED: NO
```
