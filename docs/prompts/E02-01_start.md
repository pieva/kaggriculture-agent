# E02 — Avvio della seconda iterazione supervisionata

Continuiamo il progetto Kaggriculture Agent dal repository corrente.

La prima iterazione E01 è completata e consolidata.

Prima di proporre o implementare qualsiasi evoluzione, analizza il repository
esistente e ricostruisci lo stato effettivo del progetto.

## Stato di partenza

E01 ha prodotto:

- una baseline rule-based `CarrotLoopAgent`;
- una struttura modulare con `GameState`, `ActionBuilder`, strategia ed entry point;
- un sistema locale di valutazione;
- un processo di build della submission standalone;
- test automatici;
- una submission Kaggle accettata ed eseguita con successo;
- il tag Git `v0.1-e01-baseline`;
- la documentazione tecnica e comportamentale in
  `docs/versions/E01_baseline.md`.

La baseline è stata inoltre eseguita localmente in modo osservabile.

La traccia ha permesso di verificare concretamente il ciclo:

`BUY_SEED → PLANT → WATER → PASS → HARVEST → PLANT → SELL`

e di individuare alcuni aspetti rilevanti per le evoluzioni successive:

- il farmer rimane sulla singola casella iniziale;
- viene utilizzata soltanto la coltura `CARROT`;
- il seme del ciclo successivo viene acquistato in anticipo;
- farmer e mercato possono agire nello stesso turno;
- l'irrigazione modifica la resa;
- la strategia vende immediatamente il raccolto;
- una parte significativa delle informazioni disponibili in `GameState`
  non viene ancora utilizzata;
- il costo effettivamente osservato del seme non coincide con il valore
  statico presente nella configurazione locale;
- l'esecuzione interattiva ha richiesto temporaneamente l'aggiunta di
  `src` a `PYTHONPATH`.

## Prima attività

Prima di modificare il codice:

1. leggi il repository corrente;
2. leggi `docs/versions/E01_baseline.md`;
3. verifica che la documentazione corrisponda al codice effettivo;
4. aggiorna `docs/PROJECT_STATE.md` allo stato realmente raggiunto;
5. aggiorna `docs/EXPERIMENT_LOG.md` con i risultati finali di E01,
   compresa la verifica Kaggle e l'esecuzione osservabile;
6. non modificare ancora il codice dell'agente.

## Progettazione di E02

Dopo l'aggiornamento della documentazione, proponi il piano per E02.

E02 deve essere una singola evoluzione controllata della baseline, non una
riscrittura generale dell'agente.

Prima di scegliere l'evoluzione:

- analizza quali capacità dell'ambiente sono già rappresentate dal codice
  ma non utilizzate dalla strategia;
- identifica da 2 a 4 possibili evoluzioni incrementali;
- per ciascuna indica quale ipotesi sperimentale permetterebbe di verificare;
- indica quali metriche E01 consentono il confronto;
- raccomanda quale modifica introdurre per prima e spiega perché.

Non implementare E02 finché il piano non è stato sottoposto a revisione
umana e approvato.

Manteniamo il metodo supervisionato:

`DEFINE → PLAN → REVIEW → BUILD → VERIFY → REVIEW → SHIP`
