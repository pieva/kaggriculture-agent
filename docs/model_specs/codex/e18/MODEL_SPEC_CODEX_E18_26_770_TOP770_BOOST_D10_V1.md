# MODEL SPEC — Codex E18.26 7-7-0 Top770 BoostD10 V1

## Stato

`GENERATED__TOP770_D10_CORE_MATCH__MATCHED_PARENT_DELTA_PASS__STRUCTURAL_GATE_FAIL__NO_UPLOAD`.

E18.26 aumenta il throughput D1–D10 mantenendo gli invarianti `7-7-0`, 14
pascoli, cap 14, mix obiettivo `9 COW + 5 SHEEP` e 12 hands massimi. Il
trattamento migliora E18.25 nel confronto interno matched, ma non è promosso:
la continuità FEED nella transizione D12–D14 non conserva ancora i 14 animali.

## Verifica sui Melon di Top770

L'ipotesi che Top770 non usi Melon è falsificata dai replay. Nei cinque replay
storici exact `7-7-0` (episodi `105405557`, `105384058`, `105398563`,
`105391568`, `105565293`) la composizione è invariabilmente:

- D1 e D5: `12 MELON + 7 WHEAT`;
- D10: `12 MELON + 20 STRAWBERRY + 5 WHEAT`;
- D15 e D20: `38 STRAWBERRY + 23 WHEAT`.

Anche il replay corrente ispezionato, episodio `105717134`, mostra 12 tile
`Melon (midgrowth)` a D10. I Melon spariscono tra D10 e D15; osservarne
l'assenza più tardi può quindi dare l'impressione che non siano mai usati.
Il profilo corrente di Top770 non è però più un comparatore exact `7-7-0`
(include pasture/coop e Goose), perciò il target controllato resta la coorte
storica omogenea.

### Estensione osservata fino a D20

L'episodio corrente `105717134` è stato normalizzato a fine D1/D5/D10/D15/D20
con mappa delle 100 celle. A D10 coincide ancora con il target crop storico
(`12 MELON + 20 STRAWBERRY + 5 WHEAT`) e occupa 13 slot zootecnici, ma usa
`5 COW + 4 SHEEP + 4 GOOSE` in `9 pasture + 4 coop`. Da qui le strategie si
separano:

- D15: 57 crop (`33 STRAWBERRY + 24 WHEAT`), 18 strutture zootecniche
  `11-7-0`, 17 animali e una coop vuota;
- D20: 58 crop (`33 STRAWBERRY + 25 WHEAT`), 17 strutture `10-7-0`, stessi 17
  animali; la coop vuota è stata reclamata in una tile Wheat;
- money: `3.233 → 19.149 → 48.939` a D10/D15/D20. D20 supera la mediana
  `44.350` della coorte exact `7-7-0`, ma resta nel suo range
  `42.922–61.251`; non è evidenza causale perché cambiano topologia, specie,
  seed, avversario e mercato.

La nuova osservazione conferma il ritiro completo dei Melon entro D15 e rende
utile un reclaim state-driven delle strutture vuote. Non modifica però i
vincoli della prossima release: il target resta `7-7-0`, 14 animali e
`38 STRAWBERRY + 23 WHEAT` a D15-D20. Report e dati completi:
`reports/TOP770_REPLAY_105717134_D01_D20_ANALYSIS_IT.md` e
`artifacts/derived/JESSE_BULLARD_REPLAY_105717134_D01_D20_2026_09_05.json`.

## Trattamento BoostD10

Rispetto a E18.25 il piano introduce:

- ciclo rapido delle sette Wheat iniziali nei giorni 3, 5, 7 e 9;
- WATER pieno fino a D10, con otto WATER Melon rinviati a D5 per allineare il
  totale osservato;
- crescita della capacità fino a 12 unità reali a D10;
- riuso, solo per E18.26, dei worker che completano i prefissi di unlock D7;
- ponte di liquidità Fertilizer D12–D13 per il payroll.

La nuova route D7 è opt-in (`d7_reuse_unlock_workers=true`): i piani
E18.18–E18.25 mantengono il comportamento legacy e i relativi hash congelati.

## Confronto D1–D10

| KPI pianificato | Top770 exact 7-7-0 | E18.25 | E18.26 |
|---|---:|---:|---:|
| PLANT | 63 | 51 | 63 |
| WATER | 254 | 186 | 254 |
| HARVEST | 32 | 18 | 30 |
| MOVE | 790 | 457 | 529 |
| azioni produttive | 670 | — | 598 |
| PASS | 221 | — | 570 |

E18.26 replica esattamente il nucleo identificato `PLANT/WATER` e resta a due
HARVEST dal riferimento. Non replica ancora l'intera action trace: MOVE,
produttive e PASS restano materialmente diversi. A D10, tuttavia, tutte le
quattro esecuzioni del gate raggiungono 11 hands e la composizione
`12 MELON + 20 STRAWBERRY + 5 WHEAT`.

Sotto contesa diretta con E18.25, D5 chiude temporaneamente con 5 invece di 7
Wheat per proteggere il rinnovo della manodopera; il deficit viene recuperato
entro D10. L'anticipo dei quattro semi a D4 rendeva D5 esatto ma azzerava la
liquidità per le assunzioni D5 ed è stato respinto.

## Gate interno

Seed `180903001`, entrambi i seat:

| Confronto | E18.26 | avversario | margine mediano |
|---|---:|---:|---:|
| diretto contro E18.25 | 63.096,0 | 61.269,5 | +1.826,5 |
| contro E18.16 | 54.364,5 | 81.283,5 | -26.919,0 |

Nel confronto matched con il risultato congelato di E18.25 contro E18.16,
E18.26 migliora di `+2.198/+2.080` nei due seat, `+2.139` in mediana. Zero
errori controller; topologia finale exact `7-7-0` in 4/4.

Il gate strutturale fallisce perché il doppio vincolo payroll/mangime dopo
l'unlock SW lascia, contro E18.16, tutti i 13 animali senza FEED in D12 e una
parte senza FEED in D13; sotto contesa il numero varia ma il failure mode
resta lo stesso. Il risultato finale è `6 COW + 5 SHEEP` contro E18.25 e
`6 COW + 3 SHEEP` contro E18.16, non `9+5`. E18.26 è quindi evidenza positiva
sul BoostD10, non una release né il candidato alla submission quotidiana.

## Prossima specifica

Aggiornamento di esecuzione: il successore E18.27 V3 è stato implementato e
verificato. Stato e problemi residui sono in
`MODEL_SPEC_CODEX_E18_27_770_D10_D15_CASHFLOW_V3.md`; il programma seguente
è conservato come preregistrazione della prima fase, non come build ancora
da avviare. E18.26 rimane invariata come controllo.

Decisione aggiornata del proprietario, 2026-09-05: prima ottimizzare D10-D15,
poi affrontare la chiusura entro D30 con un trattamento distinto. E18.26,
configurazione e piano restano congelati come controllo; questa sezione
descrive il successore e non una correzione già implementata.

Il gradino Top770 D11 viene soprattutto dai Melon: 72 unità raccolte in D11,
vendute 60 in D11 e 12 in D12. Noi raccogliamo 72 in D13 e vendiamo 36 in
D13 e 36 in D14. Il planner mantiene il default `melon_harvest_day=13`.
La riesecuzione invariata seat 0 contro E18.16 (reward 54761, zero errori)
conferma che sono raccoglibili da D11; dopo le azioni D11, 11 tile sono a
resa 6 e una a 5. Pareggiare PLANT/WATER non garantisce lo stesso servizio
per tile. L'incasso Melon locale 11.262 contro 14.267–16.717 Top770 è una
differenza osservata, non una misura causale del costo del ritardo.

Il ponte di liquidità e consegna fallisce: zero FEED D12, 8/13 D13; l'ultimo
batch D13 vende 36 Melon e compra cinque Wheat troppo tardi per il servizio
prima del refresh. Cinque animali scappano al cambio D14. L'assenza di nuovi
acquisti animali D14-D30, anche dopo il recupero della cassa, è un problema
distinto di mancata risposta del piano ai vuoti.

Prima fase: conservare D1-D9, preparare in D10 WATER/HARVEST e incasso
D11-D12, riservare payroll/mangime/consegne prima dell'espansione, riattivare
le tile liberate verso il target D15. Le regole D16-D30 restano invariate;
le conseguenze della prima fase vengono comunque misurate fino a fine game.
Il precedente harvest-first Wheat D13 resta una protezione di riserva e non
più la prima ipotesi. Gate:

1. D1-D9 invariato; D10 nel perimetro del trattamento con delta espliciti e
   target strutturali conservati. PLANT/WATER sono misure, non uguaglianze
   obbligatorie che prevalgono su maturazione e incasso;
2. ciclo WATER/HARVEST/consegna/SELL Melon verificato D11-D12, registrando
   resa, vendite eseguite, prezzi e cassa per turno;
3. FEED coperto su ogni animale presente D11-D15, zero fughe nell'intero
   episodio, `9 COW + 5 SHEEP` a D15 e finali, cap 14 e massimo 12 hands;
4. percorso verso D15 `38 Strawberry + 23 Wheat` senza sacrificare servizio
   e riserve; ogni pascolo vuoto ha decisione esplicita con margine/scadenza;
5. delta matched finale positivo contro E18.26 in entrambi i seat, con
   avversari congelati e successiva verifica sulla matrice development;
   tenere distinto il gate contro gli incumbent da quello contro il parent;
6. nessuna promozione/upload della candidata fallita né consumo di
   holdout/final-confirmation in questa fase diagnostica.

Seconda fase, sul migliore sviluppo D10-D15 verificato: pianificare a ritroso
da D30 ultimi raccolti, trasporto e vendita, poi dimensionare il personale.
Cutoff crop e servizi terminali devono dipendere dal ritorno entro fine game;
misurare Fertilizer, prodotti residui e reward matched senza alterare i gate
della prima fase. Non combinare i due trattamenti nel primo esperimento.

Diagnosi completa, sequenza per turno e protocollo di ripresa:
`reports/E18_26_D10_D15_CASH_FEED_DIAGNOSIS_AND_NEXT_PRIORITIES_IT.md`.

## Evidenza macro D21-D30 — acquisizione completa 2026-09-05

Il confronto completo dei cinque replay Top770 final-770 e dei due seat
E18.26 contro E18.16 conserva tutti i checkpoint precedenti e verifica ogni
saldo di cassa rieseguendo i batch registrati su copie isolate dello stato.
Il report canonico è `reports/E18_26_TOP770_D01_D30_CLOSURE_IT.md`, con
dataset `artifacts/derived/E18_26_JESSE_770_D01_D30_CLOSURE.json`.

Il dettaglio corregge la diagnosi delle consistenze: al cambio D14 scappano
cinque animali (13→8); la Sheep pianificata viene piazzata durante D14 (8→9).
Non ci sono acquisti di animali da D14 in poi e i cinque pascoli restano
vuoti fino al termine. La prima priorità aggiornata è proteggere D10-D15; il refill
va deciso sul margine realizzabile entro la fine, non soltanto sul posto vuoto.

Per gli sviluppi successivi: Top770 conserva 61 crop fino a D27, rimpiazza
gradualmente Strawberry con Wheat/Carrot da D23, compie 90 nuove semine brevi
in D21-D30 contro 46 e mantiene 12 persone fino a D30 contro le nostre 3.
Nell'ultima giornata compie 28 HARVEST contro 4 e realizza 5.122–8.562 netti,
contro -81/+70 delle azioni E18.26. Il servizio terminale deve quindi
prenotare raccolto, consegna e vendita prima di ridurre gli hands. In D21-D30
Codex non raccoglie/vende Fertilizer, mentre Top770 ne vende 131–140 unità.

La cassa finale è 54.364,5 mediana locale contro 75.629 Top770, con range
pubblico 59.508–120.267. Prezzi e avversari differiscono: i volumi e le
missioni sono il benchmark operativo, il delta cash pubblico non è causale.
Le due coop vuote costruite da Top770 a D29 non sono target Codex; restano
7-7-0 e cap 14, con una famiglia causale per ablation.

## Artefatti

- config: `configs/CODEX_E18_26_770_JESSE_BOOST_D10_V1.json`;
- planner: `tools/e18_18_capacity_trajectory_planner.py`;
- controller: `tools/e18_26_jesse_boost_d10_controller.py`;
- builder: `tools/build_e18_26_770_jesse_boost_d10_plan.py`;
- runner: `tools/run_e18_26_770_jesse_boost_d10_gate.py`;
- test: `tests/test_codex_e18_26_jesse_boost_d10_controller.py`;
- piano: `artifacts/derived/E18_26_770_JESSE_BOOST_D10_PLAN_V1.json`;
- gate: `artifacts/derived/E18_26_770_JESSE_BOOST_D10_GATE_V1.json`;
- report: `reports/E18_26_770_TOP770_BOOST_D10_GATE_REPORT_IT.md`.
