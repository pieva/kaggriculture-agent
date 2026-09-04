# E18 — intake delle candidate Claude e Copilot

## Decisione di apertura

Nessuna delle nuove candidate viene ammessa direttamente al torneo E18.
Entrambe le linee sono utili come ablation, ma **non implementano la leva
causale emersa dall'episodio 105080066**: rotazione di colture vive,
consapevolezza della scadenza e cadenza di raccolta orientata alla resa.

Questa è una decisione development-only. Holdout, final-confirmation e
submission Kaggle non sono stati usati.

## Claude

### V5

V5 riduce movimento tramite clustering home-quadrant e migliora V3 del 3,31%
nella matrice Claude dedicata. Nel torneo comune il segno non è robusto:
`+8,53%` contro avversari condivisi, ma `-9,57%` nel testa-a-testa con V3,
collassi fino a 78 e soltanto `28/42` run a 3Q. Il livello economico resta
circa 14k, molto lontano da 100k.

Rispetto al gate lifecycle E18:

- individua `URGENT_WATER`, `HARVEST_READY` e `RECOVERY_DIG`;
- `RECOVERY_DIG` riguarda weed già formata, non Strawberry viva da ruotare;
- non usa `max_lifespan_step`;
- raccoglie quando `yield_units > 0` e l'età supera `first_yield`, senza un
  target di resa per harvest;
- lo shutdown è una soglia fissa a cinque giorni residui.

V5 può essere un controllo di routing, non la candidata lifecycle E18.

### V6

V6 è già respinta: media 1.538,50 contro 17.119,36 del riferimento, `1-13`,
13/14 run sotto 5k e 3Q in 1/14. Inoltre la sua stessa documentazione segnala
che le piante fuori dal servizio urgente possono convertirsi in weed. Non è
ammissibile neppure come controllo economico principale.

### Requisito per una Claude E18

Serve un nuovo freeze autonomo che aggiunga `KEEP/HARVEST/DIG/REPLANT` sulle
piante vive, usi la scadenza osservata e dimostri su fixture che non raccoglie
Wheat prematuramente. Non basta cambiare il clustering.

## Copilot

### 6-6-2 V3

La service guard V3 è equivalente al controllo Codex: delta economico 0,00%,
28/28 profili completi e 28/28 conteggi azione identici. Il modulo non espone
una policy colturale alternativa; sovrappone una guardia di mercato alla
stessa base 6-6-2. Di conseguenza eredita integralmente il difetto lifecycle
osservato su Kaggle.

### 6-6-2 V4

V4 anticipa il gregge ed è un prototipo tecnico non benchmarkato e non
ammesso. Anche questa leva agisce sul mercato animale, non su rotazione,
scadenza o resa del raccolto. Non può essere usata per testare l'ipotesi E18.

### Native crop-only

La Native V1 resta l'unico riferimento Copilot realmente indipendente e ha
buoni gate tecnici, ma è stata valutata soltanto contro inert e produce circa
8,9k. Può essere usata per studiare il dispatch crop-only; prima del torneo
deve però aggiungere telemetria su harvest yield, weed exit e rotazione live.

### Requisito per una Copilot E18

Serve una candidata indipendente oppure un overlay dichiaratamente Codex che
modifichi davvero l'action stream nelle fixture lifecycle. Un wrapper che
tocca soltanto gli ordini animali non è sufficiente.

## Gate comune di ammissione

Prima del benchmark economico ogni candidata Claude/Copilot deve fornire:

1. entry point callable, config separata e hash del freeze;
2. fixture `late Strawberry → DIG → Wheat → WATER → HARVEST`;
3. divergenza prevista dall'action stream rispetto al controllo;
4. `starved_to_weed=0` nelle fixture e riduzione di `expired_to_weed`;
5. resa media Wheat per harvest almeno 3,5 nel micro-benchmark;
6. invarianti 6-6-2, 14/14 e zero fughe per le linee mixed-farming;
7. test sui soli seed development E18.

## Fonti

- `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V5_DEVELOPMENT_REPORT_IT.md`;
- `docs/model_specs/claude/e17/reports/E17_1_CLAUDE_REACTIVE_V6_REJECTION_REPORT_IT.md`;
- `experiments/e17/reports/common/E17_TWO_CANDIDATE_DELTA_TOURNAMENT_V3_REPORT_IT.md`;
- `src/agricola/strategy/claude/e17_reactive_3q_v5.py`;
- `src/agricola/strategy/claude/e17_reactive_3q_v6.py`;
- `src/agricola/strategy/copilot/e17_topology_662_candidates.py`;
- `src/agricola/strategy/copilot/e17_native_3q.py`.
