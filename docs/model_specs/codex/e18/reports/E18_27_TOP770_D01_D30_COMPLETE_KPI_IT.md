# E18.27 V3 vs Top770 — KPI completi D1-D30

Data di consolidamento: 2026-09-05. Formato grafico approvato dal proprietario
come standard per i confronti futuri. Nessuna modifica alla policy dell'agente.

- [Report grafico salvato, 14 pannelli](E18_27_TOP770_D01_D30_COMPLETE_KPI.html).
- [Standard comune e dizionario KPI](../../../../../experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V1_IT.md).
- [Dataset e audit delle strutture/specie](../artifacts/derived/E18_27_TOP770_D01_D30_COMPLETE_KPI.json).
- Generatore/audit: `../tools/build_e18_27_top770_complete_kpi.py`.

## Campione e lettura

E18.27 V3: 14 profili locali contro E18.16, sette seed development
180903001–180903007 × due seat. Top770: cinque replay pubblici congelati,
105405557, 105384058, 105398563, 105391568, 105565293, filtrati final-770.
Non è una selezione aggiornata del leaderboard e non contiene il replay
105717134, che termina con una topologia differente.

Mediane puntuali e bande min-max osservate, non intervalli di confidenza.
H24 = indice 24*D−1, pre-ultimo batch in D1-D29 e terminale in D30.
13 persone = 12 hands + farmer. Confronto descrittivo, non matched:
seed, avversari e prezzi pubblici/locali differiscono.

Pannelli: cassa, persone, totale colture, totale animali collocati, mucche,
pecore, oche, pascoli vuoti, meloni, grano, fragole, carote, pomodori,
ricoveri oche vuoti. Le specie a zero restano visibili. La tabella economica
e operativa prevista nello standard è un complemento: questa esportazione
salva i grafici già approvati, non pretende di ricalcolare tutti i KPI storici.

## Cosa significa «ricoveri oche vuoti»

È una tile `{"kind": "COOP"}` senza animale. Non è lo shed di magazzino,
non è un pascolo e non dimostra un'oca acquistata, fuggita o morta.
Nei 720 stati di ciascuno dei cinque replay: zero oche sulle tile, nello
shed e negli inventari. Il controllo completo rileva anche zero pomodori.
Il candidato locale non ha COOP nei checkpoint, né acquisti/collocamenti
di oche o semine di pomodori nei ledger eseguiti.

La seguente sequenza è identica nei cinque replay Top770. Coordinate `(x,y)`
zero-based, worker 0 = farmer, worker 1+ = hands; orari delle azioni applicate
al pre-stato, giorni/ore mostrati con numerazione 1-based.

| Momento | Tile | Unità | Azione e transizione |
|---|---|---|---|
| D11 H15 | (4,1) | 7 | BUILD_COOP: tile libera → COOP vuoto |
| D13 H06 | (4,1) | 6 | DIG: COOP vuoto → tile libera |
| D29 H08 | (4,1) | farmer | BUILD_COOP: tile libera → COOP vuoto |
| D29 H16 | (3,2) | farmer | BUILD_COOP: tile libera → COOP vuoto |

Di conseguenza il grafico H24 mostra un ricovero vuoto D11-D12 e due
D29-D30, zero negli altri giorni. Non sono tre ricoveri contemporanei.
La topologia 7-7-0 descrive qui i pascoli e non include questi COOP.

Nel motore locale ispezionato `BUILD_COOP` richiede una tile libera e
consuma un comando, senza addebito diretto di denaro o materiali; `DIG`
può rimuovere un COOP vuoto. Le infestanti spontanee vengono generate solo
sulle tile `None`: il COOP impedisce quindi lo spawn su quella tile.
Questo effetto è verificabile; l'intenzione strategica di Top770 non lo è.
È compatibile con una copertura temporanea anti-weed, ma anche con una
routine residua: non attribuire automaticamente né spreco né ottimalità.
Non produce uova senza oca e impedisce di coltivare lì fino alla rimozione.
L'impatto netto non è quantificato e richiederebbe un'ablazione matched.

Fonte delle regole: motore installato
`.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py`,
rami `_apply_unit_action` BUILD_COOP/DIG e `_spawn_weeds`. Per versioni future
verificare nuovamente le regole; non trasformare questa nota in una garanzia
sul motore remoto futuro.

## Traiettoria delle mucche

Nei primi dieci checkpoint la mediana locale è
`2,2,2,2,4,4,4,4,4,9`, quella Top770
`2,2,3,3,4,4,6,8,9,9`. Il riempimento Top770 è più progressivo e raggiunge
nove mucche D9 contro D10. È un'osservazione, non una prova che il solo
anticipo dei BUY/PLACE replicherebbe il risultato economico pubblico.

## Riproduzione e stato

Dal repository:

```powershell
.venv/Scripts/python.exe docs/model_specs/codex/e18/tools/build_e18_27_top770_complete_kpi.py
```

Il generatore verifica hash dei replay congelati, identità delle specie,
coerenza dei totali e assenza di oche anche fuori dai checkpoint; salva le
transizioni COOP per ogni episodio. L'export contiene i dati e il codice
grafico incorporati, con dipendenza D3 7.9.0 da CDN per la visualizzazione.

E18.27 V3 resta non promossa. La priorità di sviluppo E18.28 D25-D30 resta
quella già specificata; questo report non introduce nuove azioni di policy.
