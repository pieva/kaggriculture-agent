# Nuova sessione — Kaggriculture Agent

Continuiamo il progetto **Kaggriculture Agent**, usato come caso reale per verificare sul campo il metodo descritto nel libro *Lavorare con l'AI*.

## Stato raggiunto

La prima iterazione **E01** è completata dal punto di vista dello sviluppo, della validazione Kaggle e della documentazione.

Repository locale:

`C:\Users\pietr\Projects\kaggriculture-agent`

Repository GitHub:

`pieva/kaggriculture-agent`

Branch:

`main`

Tag della baseline:

`v0.1-e01-baseline`

Il repository è stato lasciato con working tree pulito e allineato con `origin/main`.

## E01 — cosa abbiamo fatto

Abbiamo utilizzato Google Antigravity con un workflow supervisionato:

`DEFINE → PLAN → REVIEW → BUILD → VERIFY → REVIEW → SHIP`

Antigravity ha prodotto una prima baseline rule-based denominata `CarrotLoopAgent`.

La struttura principale comprende:

- `GameState`, che interpreta l'osservazione dell'ambiente;
- `ActionBuilder`, che costruisce le azioni;
- `CarrotLoopAgent`, che implementa la strategia;
- `agent.py`, che costituisce l'entry point;
- infrastruttura di evaluation;
- script per evaluation e build della submission;
- test automatici;
- `submission/submission.py` standalone per Kaggle.

## Validazione Kaggle

La baseline è stata sottoposta realmente alla competizione Kaggriculture.

La submission Kaggle è stata accettata con successo e ha ottenuto uno score iniziale di **600.0**.

Abbiamo conservato gli screenshot:

- `E01-004_kaggle_submission_requirements.png`
- `E01-005_kaggle_submission_ready.png`
- `E01-006_kaggle_submission_successful.png`

## Benchmark locale

Abbiamo eseguito il benchmark locale ottenendo:

- 30 episodi;
- completion rate 100%;
- disqualification rate 0%;
- overall win rate 66,67%;
- 20 vittorie, 0 sconfitte, 10 pareggi;
- mean final money $3567.63;
- vittorie 100% contro `pass`;
- vittorie 100% contro `random`;
- 0% contro `starter`.

Il risultato è memorizzato in:

`results/e01_baseline.json`

## Esecuzione osservabile da PowerShell

Dopo la validazione abbiamo voluto capire realmente il codice generato, anziché limitarci a constatare che test e submission funzionassero.

Poiché il progetto utilizza un layout `src/`, per l'esecuzione interattiva è stato necessario impostare temporaneamente:

```powershell
$env:PYTHONPATH = "$PWD\src"
```

Abbiamo quindi eseguito direttamente la baseline e osservato la sequenza delle decisioni.

La traccia ha mostrato concretamente il ciclo:

`BUY_SEED → PLANT → WATER → PASS → HARVEST → PLANT → SELL`

Da questa osservazione sono emersi elementi importanti:

- viene utilizzata soltanto `CARROT`;
- il farmer resta sulla singola casella iniziale;
- il seme successivo viene acquistato anticipatamente;
- farmer e mercato possono effettuare azioni nello stesso turno;
- l'irrigazione influenza la resa;
- il raccolto viene venduto appena disponibile;
- una parte significativa dello stato disponibile non è ancora sfruttata;
- il costo del seme osservato durante l'esecuzione non coincide con un valore statico presente nella configurazione locale.

## Documentazione E01

Abbiamo creato:

`docs/versions/E01_baseline.md`

Il documento descrive:

- architettura della prima versione;
- responsabilità dei componenti;
- funzionamento della strategia;
- comandi PowerShell utilizzati;
- output dell'esecuzione osservabile;
- interpretazione della traccia;
- benchmark;
- rapporto tra struttura modulare e submission standalone;
- limiti osservati;
- punti di partenza per le evoluzioni successive.

Questo file inaugura una serie destinata a documentare progressivamente le versioni:

```text
docs/versions/E01_baseline.md
docs/versions/E02_....md
docs/versions/E03_....md
```

## Git

L'ultimo commit documenta l'esecuzione E01 e la validazione Kaggle.

Alla fine della sessione:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Non è stato creato un nuovo tag dopo la documentazione: `v0.1-e01-baseline` rimane il riferimento alla baseline software sottoposta a Kaggle.

# Prima di E02 — esecuzione osservabile dentro Antigravity

Prima di iniziare E02 voglio completare un ultimo esperimento metodologico su E01.

Abbiamo già eseguito e osservato la baseline manualmente da PowerShell.

Adesso voglio verificare se lo stesso processo di **VERIFY** può essere condotto direttamente attraverso Antigravity, senza impartire manualmente i comandi da una console PowerShell esterna.

Questa prova deve utilizzare **la stessa baseline E01**.

Non dobbiamo ancora introdurre alcuna evoluzione strategica.

## Obiettivo della prova

Chiederemo ad Antigravity di:

1. eseguire localmente la baseline E01;
2. produrre una traccia osservabile di un singolo episodio;
3. mostrare almeno:
   - step;
   - day;
   - hour;
   - money;
   - semi disponibili;
   - raccolto disponibile;
   - stato della tile;
   - azione del farmer;
   - azione di mercato;
   - reward finale;
4. rendere riconoscibile il ciclo `BUY_SEED → PLANT → WATER → HARVEST → SELL`;
5. spiegare eventuali problemi incontrati durante l'esecuzione;
6. non modificare la strategia.

Non suggeriamo preventivamente ad Antigravity come gestire il layout `src/` o il problema di importazione già incontrato con PowerShell.

Vogliamo verificare se identifica autonomamente il problema e come propone di risolverlo.

Qualunque modifica persistente al repository deve essere proposta prima e sottoposta ad approvazione umana.

## Evidenza da conservare

Se l'esecuzione riesce, conserviamo uno screenshot indicativamente come:

`docs/screenshots/E01-007_antigravity_observable_execution.png`

Dobbiamo poi confrontare l'esecuzione osservata attraverso Antigravity con quella già ottenuta manualmente da PowerShell.

L'obiettivo non è verificare nuovamente la strategia, ma verificare il **workflow di supervisione**:

`Coding Agent → esecuzione → osservazione → interpretazione umana`

Questa prova è particolarmente importante per *Lavorare con l'AI* perché permette di verificare se il Coding Agent accompagna effettivamente anche la fase **VERIFY**, e non soltanto **PLAN** e **BUILD**.

Solo dopo avere completato, documentato e discusso questa prova considereremo definitivamente terminata E01 dal punto di vista metodologico.

# Dopo la prova — apertura di E02

È stato preparato:

`docs/prompts/E02_start.md`

Questo sarà il prompt operativo da fornire ad Antigravity dopo la prova di esecuzione E01.

La prima attività di E02 sarà:

1. rileggere il repository;
2. confrontare codice e `docs/versions/E01_baseline.md`;
3. aggiornare `docs/PROJECT_STATE.md`;
4. aggiornare `docs/EXPERIMENT_LOG.md`;
5. non modificare ancora il codice;
6. proporre da 2 a 4 possibili evoluzioni incrementali;
7. associare a ciascuna un'ipotesi verificabile;
8. individuare le metriche confrontabili con E01;
9. raccomandare una sola evoluzione.

E02 dovrà essere **una modifica incrementale controllata**, non una riscrittura generale dell'agente.

Antigravity non deve implementarla finché non avremo esaminato e approvato il piano.

# Obiettivo della prossima sessione con ChatGPT

Procediamo in questo ordine:

1. prepariamo il prompt preciso per far eseguire E01 ad Antigravity;
2. osserviamo cosa fa Antigravity senza suggerirgli la soluzione tecnica;
3. analizziamo insieme l'esecuzione e gli eventuali problemi;
4. confrontiamo il risultato con l'esecuzione PowerShell già documentata;
5. decidiamo se aggiornare `E01_baseline.md`;
6. conserviamo lo screenshot `E01-007`;
7. chiudiamo definitivamente la verifica metodologica di E01;
8. forniamo ad Antigravity `E02_start.md`;
9. verifichiamo gli aggiornamenti a `PROJECT_STATE.md` ed `EXPERIMENT_LOG.md`;
10. analizziamo le alternative proposte per E02;
11. scegliamo l'ipotesi sperimentale;
12. esaminiamo il piano prima di autorizzare **BUILD**.

Voglio continuare a lavorare come supervisore e non come sviluppatore: Antigravity propone, esegue e implementa; noi analizziamo criticamente piani, azioni, codice, risultati ed evidenze.

L'obiettivo parallelo rimane verificare sul campo se questo workflow conferma, smentisce o richiede di precisare quanto abbiamo scritto in *Lavorare con l'AI* sullo sviluppo supervisionato con Coding Agent.
