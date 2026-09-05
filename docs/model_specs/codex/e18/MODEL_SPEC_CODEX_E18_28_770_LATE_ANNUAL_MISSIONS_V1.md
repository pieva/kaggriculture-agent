# MODEL SPEC — Codex E18.28 770 Late Annual Missions V1

Stato: `DIAGNOSED_AND_SPECIFIED__NOT_IMPLEMENTED__NOT_PROMOTED`.
Data: 2026-09-05. Parent diagnostico: E18.27 V3, ancora non promosso.

## Obiettivo e vincoli

Su richiesta del proprietario, la prossima finestra di studio è D25-D30,
comprendendo nuova produzione annuale CARROT/WHEAT, non soltanto pulizia
terminale. Conservare 7-7-0, 14 pascoli, cap 14 risorse animali, massimo
12 hands più farmer. Nessuna modifica di apertura o ai trattamenti D10-D15.
Top770 è l'alias documentale del riferimento pubblico congelato.

## Evidenza e requisito

Top770 riusa 42 slot D26-D29 con azioni WATER/HARVEST identiche in cinque
replay: 6 sempre CARROT e 36 a scelta CARROT/WHEAT, equivalenti a 87 unità
spostate tra specie. Due semine D29 restano immature e non vanno replicate.
E18.27 non risemina dopo D25; i suoi crop calano da 61 a 51/39/29/0 in
D26-D29 e la workforce arriva a sole 3 persone D30.

La candidata deve prenotare missioni annuali complete di valore positivo:
disponibilità tile → seme → PLANT confermato → acqua → HARVEST maturo →
trasporto → DROP → SELL confermato. H24 terminale non è uno slot esecutivo.
CARROT e WHEAT maturano entrambi a età 2: D28 è l'ultimo limite agronomico
di semina, da anticipare per tile se la consegna/vendita non sta nel budget.

## Ablation previste, da costruire separatamente

| Fase | Trattamento | Controllo e fattore isolato |
|---|---|---|
| A | Chiusura delle missioni già esistenti e workforce richiesta | E18.27; nessuna nuova semina |
| B | Continuità annuale D26-D28 solo WHEAT, con missioni complete | A; effetto dei cicli aggiuntivi |
| C | Selettore economico CARROT/WHEAT, stesso routing e calendario B | B; sola composizione annuale |

L'assunzione è conseguenza delle missioni ammesse, non target da copiare.
Non modificare contemporaneamente ritiro Strawberry, blackout FEED/CARE o
raccolta Fertilizer. Questi restano trattamenti successivi e distinti.

Il selettore confronta ricavi marginali attesi del lotto, costo semi
(CARROT 20, WHEAT 10), disponibilità di Wheat per FEED, domanda pubblica
e carico logistico. Non usa reward futuri, prezzi finali realizzati, seed
o identità dell'avversario. Nessuna soglia può essere ricostruita con certezza
dai cinque replay; va preregistrata prima del gate di sviluppo.

## Verifica e gate

- Prima del motore: parità micro-test di maturazione, WATER, decay, capacità
  shed, confini di giornata, ultima azione eseguibile e DROP+SELL.
- Prefisso D1-D24 identico al controllo, compresi gli ordini di mercato;
  neutralizzare retroazioni del lookahead dei semi, già osservate in E18.27 V2.
- Sette seed development 180903001–180903007, seat 0/1; roster interno
  E18.16 e controlli congelati. E18.2/V4D resta controllo competitivo storico,
  non riferimento topologico. Dichiarare separatamente eventuali smoke.
- 770, cap 14 e 12 hands; zero errori/fughe aggiuntive; nessun doppio incarico
  o risorsa prenotata due volte. Non nascondere i difetti D10-D15 del parent.
- KPI D25-D30: tile per specie, coorti mature e vendute entro termine,
  produzione e ricavi per prodotto, costo semi/hire/feed, MOVE/PASS, overflow,
  ritardo HARVEST→DROP→SELL, residui trasportati/shed/tile, cassa netta finale.
- Valutare delta medio, per seed/seat e worst-case, oltre al confronto diretto
  con gli incumbent. Nessuna promozione per il solo aumento di output.

Le fasi sono specificate ma non implementate. Holdout/final-confirmation non
consumati; nessuna nuova submission o variante E18.28 costruita in questa fase.

Analisi e quantità:
`reports/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS_IT.md`.
