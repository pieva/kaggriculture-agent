# E18.3 — ablation interna Codex delle topologie

## Verdetto

Nessuna delle topologie ridotte è candidabile. Il torneo real-engine da 70
match mostra che ottenere la geometria finale desiderata non basta: tutti i
cinque bracci costruiscono esattamente il proprio target in 14/14 episodi, ma
`7-7-2`, `6-6-2`, `7-7-0` e `6-7-0` perdono rispettivamente il `14,31%`,
`42,98%`, `34,69%` e `40,31%` rispetto al controllo E18.2 matched.

Il solo `7-7-5`, che è un passthrough del provider V4D e quindi il controllo
negativo dell'ablation, resta vicino a E18.2: `92.552,71` contro `93.318,71`,
delta `-0,82%`. Nessuna submission è autorizzata.

## Disegno sperimentale

- cinque geometrie fisse: `7-7-5`, `7-7-2`, `6-6-2`, `7-7-0`, `6-7-0`;
- stesso provider V4D e stessa logica di filtro/handoff per ogni geometria
  ridotta;
- controllo congelato `CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1`;
- sette seed development E18 preregistrati, entrambi i seat;
- 14 match per braccio, 70 totali;
- nessun Claude, Copilot o Antigravity;
- nessun holdout, final confirmation, replay o segnale Kaggle usato dal
  runner.

L'esperimento separa tre proprietà che prima erano confuse: topologia
costruita, riempimento dei pascoli e capacità di trasformare i tile liberati
in un ciclo agricolo servito fino alla raccolta.

## Risultati

| Topologia | Money | Controllo matched | Delta | Peak crop | Crop-days D21–D30 | Weed-days D21–D30 | Crop abbandonate | Harvest unit | Animali finali | Pascoli target vuoti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7-7-5 | 92.552,71 | 93.318,71 | -0,82% | 55 | 473,86 | 15,00 | 45,00 | 614,29 | 19,00 | 1,00 |
| 7-7-2 | 71.572,21 | 83.522,79 | -14,31% | 48 | 339,36 | 131,64 | 53,00 | 479,86 | 15,93 | 1,00 |
| 6-6-2 | 58.411,64 | 102.445,64 | -42,98% | 45 | 233,64 | 283,57 | 62,79 | 306,93 | 12,00 | 2,00 |
| 7-7-0 | 64.696,57 | 99.065,50 | -34,69% | 47 | 259,86 | 230,50 | 60,86 | 402,36 | 11,00 | 3,00 |
| 6-7-0 | 55.192,43 | 92.464,43 | -40,31% | 43 | 232,71 | 261,93 | 65,93 | 331,79 | 10,00 | 3,00 |

Il valore basso di unwatered tile-days nei bracci ridotti non è un successo:
deriva soprattutto dalla scomparsa prematura delle colture. Nel `6-6-2`, per
esempio, gli unwatered late scendono a `97,79` contro `231,14`, ma i crop-days
si dimezzano (`233,64` contro `473,00`), le weed-days salgono da `15,21` a
`283,57` e le unità raccolte calano da `601,29` a `306,93`.

Anche la crescita terminale conferma il difetto di ciclo: il `6-6-2` guadagna
solo `21.261,07` fra D22 e D30 contro `47.247,00` del controllo matched; il
`6-7-0` si ferma a `17.327,86` contro `41.122,29`.

## Perché E17 6-6-2 ed E18.1 non hanno funzionato

### E17 6-6-2

La baseline E17 raggiungeva correttamente `14/14` pascoli, zero fughe e circa
`59,93` crop di picco, ma nel confronto simmetrico valeva soltanto
`79.323,86`, già `20.676,14` sotto il target 100k. La topologia era dunque
corretta come vincolo strutturale, non validata come soluzione economica.

L'ablation nuova aggiunge la prova causale mancante: la sola riduzione a
`6-6-2` non libera automaticamente lavoro utile. Quando si filtrano le
missioni V4D senza riscrivere lo scheduler, si costruiscono comunque i 14
target ma se ne riempiono in media solo 12, si perdono due animali a episodio,
il picco crop scende a 45 e i crop-days late si dimezzano. Il problema non è
quindi il cap Q2 in sé: è l'assenza di una ripianificazione completa delle
missioni dopo il cambio di geometria.

### E18.1

E18.1 perdeva il diretto V4D `71.831,00` contro `89.760,57` (`-19,97%`) e su
Kaggle lo snapshot disponibile era `825,4` contro `1.131,7` di V4D. Il
selector osservava l'avversario, ma nella matrice controllata finiva sempre in
`6-6-2`: era una scelta iniziale congelata, non un'architettura capace di
ripianificare durante l'episodio.

I KPI spiegano il divario: E18.1 aveva più superficie crop di picco
(`58,57` contro `55`) e più crop-days late (`493,14` contro `473,86`), ma
eseguiva il `6,11%` di azioni produttive in meno, aggiungeva il `24,77%` di
`PASS` e portava i weed tile-days totali da 15 a 63 (`+320%`). I tile erano
presenti, ma non ricevevano servizio e raccolta con la cadenza necessaria.

## Collegamento con le sconfitte esterne di E18.2

Nei due replay esterni indicati dal proprietario (`105194141` e `105196165`,
submission `55991397`) E18.2 perde contro avversari osservati con topologie
`6-6-2` e `6-7-0`. Questa è evidenza contestuale importante, ma non dimostra
che ridurre Q2 sia di per sé la causa della vittoria.

L'ablation falsifica proprio quella lettura semplice: i nostri `6-6-2` e
`6-7-0` raggiungono la forma richiesta e perdono comunque dal 40% al 43% di
money. L'inferenza più compatibile con tutti i dati è che i competitor
monetizzino le stesse geometrie con una pipeline diversa: riempimento
coordinato, missioni persistenti, conservazione delle colture, raccolta e
liquidazione. I replay grezzi non sono nel working tree e restano
riscaricabili; perciò questa sezione separa esplicitamente l'osservazione
utente dall'evidenza causale locale.

## Decisione architetturale

Non va costruita E18.4 come un altro filtro sopra la timeline open-loop di
V4D. La prossima candidata deve avere uno scheduler nativo state-driven:

1. planner di topologia con stato desiderato per tile e isteresi;
2. missioni persistenti `BUILD → BUY/PICKUP → PLACE → FEED` per i pascoli;
3. ledger di risorse e prenotazioni, così che ogni animale/seme e ogni worker
   abbiano un incarico verificabile;
4. coda crop con deadline derivate da maturità, acqua e lifespan, non da un
   semplice ordine statico;
5. transizione di geometria ammessa solo se i worker liberati ricevono
   incarichi che portano a esecuzioni osservate, non soltanto comandi non
   `PASS`;
6. gate dinamici su crop-days D21–D30, weed-days, crop abbandonate, unità
   raccolte e crescita D22→D30, oltre a money e topologia.

Il primo obiettivo non è scegliere fra `6-6-2` e `6-7-0`: è far sì che una
riduzione controllata da `7-7-5` a `7-7-2` resti entro il `-5%` economico e
mantenga almeno il 95% delle unità raccolte del controllo. Solo dopo ha senso
testare transizioni più aggressive.

## Artifact

- `docs/model_specs/codex/e18/artifacts/derived/E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.json`;
- `docs/model_specs/codex/e18/artifacts/derived/E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.csv`;
- `docs/model_specs/codex/e18/tools/run_e18_3_labor_conserving_topology_ablation.py`;
- `docs/model_specs/codex/e18/configs/CODEX_E18_3_LABOR_CONSERVING_TOPOLOGY_ABLATION_V1.json`.

