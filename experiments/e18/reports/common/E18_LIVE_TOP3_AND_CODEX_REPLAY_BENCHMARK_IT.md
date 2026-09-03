# E18 — benchmark live Top 3 e Codex 6-6-2

## Verdetto

Il primo lotto live conferma il problema di reattività della 6-6-2 in modo
più forte del solo replay `105080066`: nei tre episodi Codex cambiano seed,
seat, avversario, score e hash dell'action stream, ma il fingerprint del ciclo
agricolo resta uno solo su tre. La policy produce sempre la stessa traiettoria
aggregata: `6-6-2`, picco di 60 colture, 496 crop-tile-days fra D21 e D30,
224 tile-days non irrigati, 49 uscite in weed, zero rotazioni e 586 unità
raccolte.

I tre leader correnti producono invece otto fingerprint distinti su otto replay.
Il segnale
comune non è una specifica rotazione, ma una capacità di servizio e raccolta
molto superiore: 872,5 unità medie contro 586 (`+286,5`, `+48,9%`) e 536,4
unità Wheat contro 286 (`+250,4`, `+87,5%`). Questo è il gap prioritario di
E18.

## Corpus e limite epistemico

Tutti i replay hanno `schema_version=1`, modulo `1.32.7`, 720 step,
`DONE/DONE`, Episode ID coerente e SHA-256 verificato.

| Cohort | Episodi target | Uso |
|---|---:|---|
| Codex 6-6-2 esterna | `105080066`, `105084394`, `105075696` | diagnosi su tre seed e tre avversari |
| Top 3 live | `105089826`, `105088610`, `105090557`, `105100853`, `105101421`, `105102327`, `105107425`, `105107748` | otto replay, entrambi i seat per ogni leader |

È evidenza di discovery consumata, non holdout. Rating leaderboard e denaro di
un episodio sono quantità diverse. Ogni agente copre entrambi i seat, ma il
numero di replay non è uniforme: due per Crop Dusta, tre per 3정훈 e sbol
ball. La media score non stima quindi la loro forza o il rendimento atteso.

## Confronto dei profili target

| Agente / episodio | Esito e score | Pascoli | Picco crop | Crop-days D21–30 | Non irrigati | Weed exits | Rotazioni | Raccolto | Wheat | Wheat / harvest |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Codex `105080066` | LOSS 59.861 | 6-6-2 | 60 | 496 | 224 | 49 | 0 | 586 | 286 | 2,860 |
| Codex `105084394` | LOSS 79.772 | 6-6-2 | 60 | 496 | 224 | 49 | 0 | 586 | 286 | 2,860 |
| Codex `105075696` | LOSS 124.497 | 6-6-2 | 60 | 496 | 224 | 49 | 0 | 586 | 286 | 2,860 |
| Crop Dusta `105089826` | LOSS 77.084 | 7-0-0 | 58 | 439 | 108 | 45 | 0 | 915 | 613 | 5,108 |
| 3정훈 `105088610` | WIN 67.557 | 7-7-0 | 62 | 515 | 198 | 37 | 2 | 886 | 478 | 3,025 |
| sbol ball `105090557` | WIN 58.769 | 7-7-0 | 62 | 513 | 201 | 39 | 2 | 884 | 540 | 3,017 |
| Crop Dusta `105100853` | WIN 88.934 | 8-4-3 | 60 | 351 | 157 | 44 | 0 | 773 | 488 | 4,738 |
| 3정훈 `105101421` | WIN 140.196 | 7-7-0 | 61 | 501 | 196 | 36 | 2 | 873 | 525 | 3,052 |
| sbol ball `105102327` | WIN 98.962 | 6-7-0 | 62 | 507 | 182 | 18 | 20 | 931 | 574 | 3,070 |
| 3정훈 `105107425` | LOSS 107.148 | 10-7-0 | 57 | 409 | 159 | 17 | 14 | 815 | 505 | 3,258 |
| sbol ball `105107748` | LOSS 94.236 | 10-7-0 | 58 | 487 | 181 | 25 | 10 | 903 | 568 | 3,087 |

Il fatto che Codex ottenga da 59.861 a 124.497 con la stessa traiettoria
agricola mostra anche perché lo score grezzo non basta a diagnosticare la
policy: il mercato e l'avversario valorizzano diversamente un piano che non si
adatta abbastanza.

## Delta medio Top 3 − Codex

| Metrica | Codex | Top 3 | Delta | Lettura |
|---|---:|---:|---:|---|
| Fingerprint ciclo unici | 1/3 | 8/8 | +7 | reattività strutturale assente in Codex |
| Topologie pascolo uniche | 1 | 5 | +4 | alcuni leader adattano anche l'architettura |
| Crop-tile-days D21–30 | 496 | 465,3 | -30,8 (-6,2%) | non serve occupare più a lungo la superficie |
| Tile-days non irrigati | 224 | 172,8 | -51,3 (-22,9%) | servizio late-game più efficace |
| Unità raccolte | 586 | 872,5 | +286,5 (+48,9%) | vero divario produttivo |
| Unità Wheat | 286 | 536,4 | +250,4 (+87,5%) | maggiore conversione finale |
| Wheat per evento di raccolta | 2,860 | 3,544 | +0,684 (+23,9%) | raccolta più matura/efficiente |
| Uscite in weed | 49 | 32,6 | -16,4 (-33,4%) | miglioramento comune, ma non uniforme |
| Rotazioni su colture vive | 0 | 6,3 | +6,3 | leva attiva in alcuni regimi, non universale |

Questi numeri correggono la prima ipotesi formulata sul solo Yusuf Murtaza.
La sua rotazione aggressiva Strawberry→Wheat è un meccanismo efficace, ma non
è condiviso dai tre leader correnti: Crop Dusta ha zero rotazioni nei due
episodi, 3정훈 ne ha due, mentre sbol ball passa da 2 a 20. Il segnale robusto
del lotto è invece raccogliere molto di più con meno backlog di irrigazione.

## Topologia: evidenza utile, non ancora causalità

Sette profili Top 3 su otto hanno `Q2=0`, ma Crop Dusta falsifica una
regola assoluta: Crop Dusta passa da `7-0-0` a `8-4-3`. 3정훈 resta `7-7-0`,
poi usa `10-7-0`; sbol ball passa da `7-7-0` a `6-7-0` e infine `10-7-0`.
I tre leader producono quindi cinque topologie. Questo sostiene la scelta di
trattare due pascoli Q2 come cap e non come minimo, ma soprattutto mostra che
la distribuzione può essere una decisione di regime.

Non dimostra quale topologia sia causalmente migliore. La 6-6-2 è la baseline
E18 congelata; la prima candidata deve isolare il ciclo colturale mantenendo
`14/14`. Il selettore `6-6-2 ↔ 7-7-0` va poi misurato come variazione distinta,
con una guardia esplicita e isteresi per evitare oscillazioni.

## Reattività all'avversario e progressione della submission

La progressione del rating della submission cambia il campione di avversari,
ma non è una feature online: né rating, né nome dell'agente, né storia degli
episodi precedenti compaiono nell'osservazione callable. Non va quindi
costruita una modalità speciale “rating 600” o “rating 2000”.

Il comportamento avversario è però parzialmente osservabile durante la
partita. `observation.farms` contiene per entrambi i player denaro, lavoratori,
quadranti sbloccati e tile pubblici; inventari, shed e seed restano privati.
L'agente può pertanto inferire progressivamente un regime da segnali quali:

- giorno di apertura Q1/Q2 e ritmo di assunzione;
- capitale pubblico, superficie crop, pascoli e animali;
- maturità delle colture, weed backlog e pressione di servizio;
- variazioni di prezzi e inventario del mercato condiviso;
- delta di stato che indicano espansione o liquidazione dell'avversario.

La pipeline Codex corrente non usa questa informazione. Il contratto
`CodexSnapshot` conserva soltanto `farm`, e il parser seleziona
`farms[player]`; la 6-6-2 usa a sua volta `_farm(observation)` sul solo player.
Esiste un vecchio `GameState.opponent_farm`, ma non alimenta il decision path
della baseline. Questa è una lacuna architetturale, non soltanto un parametro
da tarare.

E18 deve introdurre un `OpponentRegimeSnapshot` causale e privo di identità,
aggiornato entro l'episodio. Una prima macchina a stati controllabile può
distinguere `PASSIVE/LOW_PRESSURE`, `CROP_THROUGHPUT`,
`LIVESTOCK_EXPANSION` e `MARKET_CONTENTION`. Il regime può modificare riserva
di cassa, priorità di servizio, mix colturale e — soltanto dopo i gate — la
scelta fra `6-6-2` e `7-7-0`. Ogni transizione deve essere spiegabile da
feature osservate, avere soglie preregistrate e isteresi.

## Gap verso 100k e gate proposti

La media esterna Codex di questo piccolo lotto è 88.043,3: il gap aritmetico
verso 100.000 è 11.956,7 (`+13,6%`). Non è una stima causale. Il benchmark
locale simmetrico già congelato resta più prudente: 79.323,9, quindi
20.676,1 (`+26,1%`). E18 deve usare quest'ultimo per i gate development e i
replay soltanto per scegliere le metriche leading.

Prima del torneo economico, `CODEX-E18.1-REACTIVE-662-V1` dovrebbe dimostrare:

1. più di un fingerprint agricolo su fixture con pressione di servizio e
   mercato differenti;
2. decisioni spiegabili da stato osservato, non soltanto action count diverso;
3. riduzione dei late unwatered tile-days almeno verso la banda Top 3;
4. incremento del raccolto e delle unità Wheat senza aumento di weed exits;
5. classificazione opponent-aware diversa su fixture passive, crop-dense,
   livestock-dense e market-contention;
6. conservazione di riempimento `14/14`, zero fughe, zero breach e residuo
   terminale zero;
7. soltanto dopo questi gate, selettore topologico `6-6-2 ↔ 7-7-0`.

La copertura seat è ora completa per tutti e tre i leader. Il corpus è
sufficiente per formulare fixture, non per attribuire causalmente i delta
all'avversario o dichiarare ottimale una delle cinque topologie.

## Artefatti riproducibili

- `artifacts/discovery/E18_LIVE_TOP3_AND_CODEX_REPLAY_BENCHMARK_V1.json`;
- `artifacts/discovery/E18_LIVE_TOP3_AND_CODEX_REPLAY_PROFILES_V1.csv`;
- `tools/common/build_e18_live_replay_benchmark.py`;
- `tools/common/analyze_episode_105080066.py`.
