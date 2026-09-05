# MODEL_SPEC Codex E18.6 — 7-7-0 concentrata

## Identità

- candidate: `CODEX_E18_6_CONCENTRATED_770_THROUGHPUT_V1`;
- base: `CODEX-E18.2-CAPACITY-GOVERNED-V4D-V1`;
- ruolo: development-only, nessun upload Kaggle;
- ipotesi: concentrare quattordici pasture nei due quadranti già a regime è
  più efficiente di mantenere due pasture in Q2 come nella 6-6-2.

## Mutazione

La candidata mantiene sette pasture in Q0 e sette in Q1, con Q2 crop-only. Le
cinque celle pasture Q2 della E18.2 vengono convertite in-place a crop. Il
routing E18.2 resta autorevole: non viene riattivato il dispatcher globale
della E18.3 7-7-0 respinta. Soltanto un worker che si trova già su una cella
rimossa può tradurre il comando pasture in servizio colturale; un carrier può
essere deviato per completare il fill 14/14.

Il ciclo locale Q2 segue l'evidenza Top-3 più recente: Strawberry nella fase
centrale e Wheat nella fase tarda. Questa logica si applica soltanto alle
cinque celle recuperate e non modifica il calendario delle altre colture.

## Perché non si riusa E18.3 7-7-0

La vecchia variante aveva 3 pasture vuote medie, 14 perdite verificate,
402,36 unità raccolte, rapporto move/productive `1,4094` e money `-34,69%`
contro il controllo. Quel risultato misura anche un handoff globale
difettoso. E18.6 verifica la stessa intuizione geometrica senza quel
dispatcher.

## Gate development aggiornato

Quattordici match diretti contro E18.2, sette seed development e entrambi i
seat. I KPI incorporano il confronto aggiornato con Crop Dusta, Giulio
Ravasio e Top770:

- topologia effettiva `7-7-0` e fill 14/14 in 14/14;
- zero pasture Q2, breach, errori, fallback e perdite verificate;
- move/productive `≤1,20` e almeno `5%` migliore del controllo matched;
- productive `≥3.000` e almeno `+10%` sul controllo;
- harvested units `≥720` e almeno `+20%` sul controllo;
- harvested units per 1.000 move `≥200`;
- late unwatered/crop-tile almeno `10%` migliore del controllo;
- money medio non sotto il controllo oltre `5%` e nessun delta matched sotto
  `-5%`.

I gate sono congiuntivi. Un miglioramento geometrico non può compensare un
fallimento di throughput, lifecycle, economia o safety. Holdout e final
restano non consumati; nessun esito autorizza automaticamente un upload.

## Esito development

La matrice preregistrata di 14 match costruisce e riempie la topologia
`7-7-0` in 14/14, senza pasture Q2, errori, fallback o breach. La geometria è
quindi valida. Il trattamento è però respinto:

- record `0-14` e money `58.957,00` contro `71.104,43` (`-17,08%` sulle
  medie; delta matched medio `-16,69%`);
- move `3.603,79` contro `3.592,43` (`+0,32%`), quindi nessun risparmio;
- productive `2.643,07` contro `2.802,86` (`-5,70%`);
- move/productive `1,3635` contro `1,2817` (`+6,38%`, peggiore);
- PASS `850,14` contro `689,71` (`+23,26%`);
- harvest `560,36` contro `601,86` (`-6,90%`) e harvest/1.000 move
  `155,49` contro `167,54` (`-7,19%`);
- late unwatered/crop migliora solo del `2,09%`, sotto il target del 10%;
- 14 perdite verificate, una per match, riconducibili al cap 15 su 14 slot.

L'evidenza falsifica la V1, non ogni possibile 7-7-0: aggiungere il
quattordicesimo pascolo nei quadranti maturi evita di attivare Q2 per il
bestiame, ma conservare le rotte 7-7-5 non accorcia le move. Le azioni
zootecniche eliminate diventano soprattutto PASS, perché il piccolo lifecycle
Q2 in-place non genera abbastanza servizio e raccolto. Una futura 7-7-0 deve
quindi essere nativa nel routing e nel lifecycle, non un overlay geometrico.

La prima esecuzione completa, `6-5-0`, era invalida perché il carrier fill
sovrascriveva BUILD_PASTURE. È stata corretta soltanto la precedenza del
comando; soglie e seed non sono cambiati, e quel tentativo non è usato per la
decisione.

Decisione: `REJECTED_AT_DEVELOPMENT_GATE`; holdout/final non consumati,
nessuna submission o upload autorizzati.

## Diagnosi topology-matched con il Top 3

Il confronto successivo non mescola geometrie: include soltanto i profili
finali `7-7-0`. Nel corpus Top-3 congelato sono disponibili due profili di
Giulio Ravasio e quattro di Top770; Crop Dusta non ha equivalenti
esatti ed è escluso. Money locale e score live non vengono confrontati.

La tassonomia viene normalizzata come tutti i comandi unità diversi da MOVE e
PASS. Questo corregge un'incompatibilità precedente: `productive_actions`
locale esclude alcune azioni logistiche, mentre il replay benchmark le
include. Con la definizione comune il gap produttivo di E18.6 è `-7,5%`, non
`-20%`. Restano però gap specifici e robusti:

- comandi unità totali `+2,9%`, quindi non manca tempo-worker nominale;
- PASS `+60,5%` e move `+4,1%`;
- servizio crop `-18,1%`, con WATER `-22,0%` e HARVEST comandati `-16,7%`;
- crop tile-days D21–D30 `-10,7%` e late unwatered/crop `+24,5%`;
- harvest riusciti `-31,7%`, unità raccolte `-36,7%` e resa per harvest
  riuscito `-7,3%`;
- Codex chiude con 15 animali per 14 slot, gli equivalenti con 14.

Giulio e Top770 usano quasi lo stesso schedule anche nel loro head-to-head
`105398563`, dove entrambi terminano `7-7-0`: circa 3.315 comandi produttivi
normalizzati, 3.460 move, 530 PASS e 885 unità raccolte. La priorità causale
diventa quindi PASS → crop service locale, poi persistenza del lifecycle e
solo dopo completamento locale delle rotte. Cap animali 14 è una correzione
di safety separata; il tredicesimo worker resta un'ablation successiva.

Report e artifact:

- `docs/model_specs/codex/e18/reports/E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_IT.md`;
- `docs/model_specs/codex/e18/artifacts/derived/E18_6_770_MATCHED_TOP3_GAP_ANALYSIS_2026_09_04.json`.

## Asset

- source:
  `src/agricola/strategy/codex/codex_e18_concentrated_770_throughput.py`;
- config:
  `docs/model_specs/codex/e18/configs/CODEX_E18_6_CONCENTRATED_770_THROUGHPUT_V1.json`;
- runner:
  `docs/model_specs/codex/e18/tools/run_e18_6_concentrated_770_throughput_gate.py`;
- test:
  `docs/model_specs/codex/e18/tests/test_codex_e18_concentrated_770_throughput.py`;
- artifact:
  `docs/model_specs/codex/e18/artifacts/derived/E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_V1.json`;
- report:
  `docs/model_specs/codex/e18/reports/E18_6_CONCENTRATED_770_THROUGHPUT_DEV_GATE_REPORT_IT.md`.
