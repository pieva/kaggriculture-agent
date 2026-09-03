# Model spec — Codex E18.3 Labor-Conserving Topology Ablation V1

## Identità e ruolo

- model spec: `CODEX-E18.3-LABOR-CONSERVING-TOPOLOGY-ABLATION-V1`;
- ruolo: `DEVELOPMENT_ONLY_CAUSAL_ABLATION`;
- provider comune: `CODEX-E17.2-POST-FEED-CAPACITY-BATCHED-ROUTING-V4D-D28`;
- controllo economico: `CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1`;
- topologie: `7-7-5`, `7-7-2`, `6-6-2`, `7-7-0`, `6-7-0`;
- feature online: soltanto osservazione pubblica e stato privato proprio;
- memoria cross-episode: assente;
- holdout/final confirmation: non consumati.

Questa famiglia non è una candidata di release. Serve a isolare l'effetto
della geometria da quello dello scheduler e a impedire che una somiglianza
visiva con i top agent venga scambiata per equivalenza strategica.

## Contratto causale

Il braccio `7-7-5` restituisce esattamente l'azione del provider ed è il
controllo negativo. Gli altri bracci modificano soltanto:

- sottoinsieme fisso dei 19 target pascolo V4D;
- cap alle acquisizioni zootecniche;
- backfill semi per i tile recuperati;
- assegnazione dei worker liberati a riempimento e servizio crop.

Le celle pascolo sono annidate: ogni topologia ridotta è un sottoinsieme del
`7-7-5`. Il runner usa gli stessi sette seed E18 e i due seat per ogni
braccio, sempre contro lo stesso controllo E18.2.

## Invarianti

- nessuna azione su un pascolo esterno al target;
- nessun superamento del cap Q2 del braccio;
- nessun worker liberato può terminare il batch in `PASS`;
- telemetria separata per topologia costruita, pascoli riempiti, handoff e
  servizio crop;
- eccezioni fail-closed a `PASS` con contatore errori/fallback;
- nessun segnale derivato da rating, identità avversario o storia Kaggle.

## Esito

I cinque bracci costruiscono esattamente la topologia prevista in 14/14
match. Il `7-7-5` resta entro `-0,82%` dal controllo; ogni topologia ridotta
fallisce il gate economico e di ciclo. Nessun braccio supera tutti i gate e
`submission_authorized=false` nell'artifact congelato.

La famiglia dimostra che il semplice handoff sintattico (`worker != PASS`) non
equivale a lavoro produttivo eseguito. La prossima linea deve sostituire la
timeline open-loop con missioni persistenti e feedback sull'esecuzione.

