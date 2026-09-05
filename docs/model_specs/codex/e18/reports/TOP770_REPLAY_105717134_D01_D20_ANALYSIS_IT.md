# Top770 — analisi replay 105717134 fino a D20

## Verdetto

L'analisi è ora persistita con provenienza, checkpoint e mappa tile-per-tile.
Il risultato principale è che bisogna distinguere due strategie di Top770:

- la coorte storica omogenea exact `7-7-0`, che resta il riferimento
  controllato per lo sviluppo Codex;
- l'episodio corrente `105717134`, che conserva lo stesso opening crop fino a
  D10 ma evolve verso un layout di slot zootecnici `10-7-0`, con coop e Goose.

Il replay corrente non giustifica un cambio di topologia per Codex. Rafforza
invece tre elementi trasferibili: opening con 12 Melon, ritiro completo dei
Melon entro D15 e reclaim state-driven delle strutture zootecniche vuote.

## Provenienza e perimetro

| Campo | Valore |
|---|---:|
| Submission | `55994794` |
| Episodio | `105717134` |
| Seed | `1386178497` |
| Player osservato | Top770, player 2 |
| Avversario | keiz |
| Esito mostrato | Loss, rating `2995 (-4)` |
| Checkpoint | fine D1, D5, D10, D15 e D20 |

Il rating `2995` non è il risultato economico della farm. Ogni checkpoint è
stato letto a turno `24/24`; le 100 celle della seconda farm sono state
normalizzate dagli attributi visibili del visualizer. I conteggi dei farmhand
sono soltanto le unità presenti sulla griglia: un agente in città non compare.

## Traiettoria osservata nel replay corrente

| Giorno | Money | Crop | Slot zootecnici | Animali | Slot per quadrante | Farmhand + farmer visibili |
|---|---:|---|---|---|---|---:|
| D01 | 74 | M12 + W7 = 19 | 4 pasture | C2 + S2 = 4 | 4-0-0 | 5 + 1 |
| D05 | 890 | M12 + W7 = 19 | 6 pasture | C4 + S2 = 6 | 6-0-0 | 3 + 0 |
| D10 | 3.233 | M12 + S20 + W5 = 37 | 9 pasture + 4 coop | C5 + S4 + G4 = 13 | 6-7-0 | 8 + 1 |
| D15 | 19.149 | S33 + W24 = 57 | 13 pasture + 5 coop | C5 + S8 + G4 = 17 | 11-7-0 | 10 + 1 |
| D20 | 48.939 | S33 + W25 = 58 | 13 pasture + 4 coop | C5 + S8 + G4 = 17 | 10-7-0 | 11 + 1 |

`M/S/W` indicano Melon, Strawberry e Wheat; `C/S/G` indicano Cow, Sheep e
Goose. Il conteggio per quadrante include pasture e coop perché misura le
celle sottratte alle colture.

### Lifecycle e servizio crop

| Giorno | Sprout | Midgrowth | Ready | Fertilized | Watered crop | Dry crop |
|---|---:|---:|---:|---:|---:|---:|
| D01 | 19 | 0 | 0 | 0 | 19 | 0 |
| D05 | 15 | 4 | 0 | 0 | 7 | 12 |
| D10 | 24 | 13 | 0 | 0 | 34 | 3 |
| D15 | 20 | 26 | 11 | 4 | 38 | 19 |
| D20 | 7 | 40 | 11 | 23 | 31 | 27 |

Il dato più netto è la transizione D10-D15: i 12 Melon spariscono tutti, viene
aperto Q2 e la capacità viene riallocata a Strawberry/Wheat. Tra D15 e D20 il
numero di crop sale soltanto da 57 a 58, ma la fertilizzazione passa da 4 a
23 tile. A D20 restano 27 crop asciutte su 58: la maggiore densità animale non
elimina la pressione di servizio sulle colture.

## Confronto con il Top770 exact 7-7-0

Il riferimento controllato contiene cinque episodi:
`105405557`, `105384058`, `105398563`, `105391568`, `105565293`.

| Giorno | Replay corrente | Top770 exact 7-7-0 | Delta strutturale corrente |
|---|---|---|---|
| D10 | M12 + S20 + W5; 13 animali | M12 + S20 + W5; 13 animali | stesso volume, ma 4 Cow sostituite da 4 Goose/coop |
| D15 | S33 + W24; 18 strutture; 17 animali | S38 + W23; 14 pasture; 14 animali | +4 strutture = -4 crop; una coop è vuota |
| D20 | S33 + W25; 17 strutture; 17 animali | S38 + W23; 14 pasture; 14 animali | +3 strutture = -3 crop; la coop vuota è stata reclamata |

L'opening crop è identico fino a D10. La biforcazione è zootecnica: la coorte
exact `7-7-0` arriva a D15/D20 con `9 Cow + 5 Sheep` e 61 crop
(`38 Strawberry + 23 Wheat`); il replay corrente sacrifica tre tile crop per
tre animali aggiuntivi e introduce quattro Goose.

### Dinamica economica

| Intervallo/checkpoint | Replay corrente | Top770 exact 7-7-0 |
|---|---:|---:|
| Money D10 | 3.233 | 3.766–4.020 |
| Money D15 | 19.149 | 24.065–28.071 |
| Crescita D10→D15 | +15.916 | +20.296…+24.178 |
| Money D20 | 48.939 | 42.922–61.251; mediana 44.350 |
| Crescita D15→D20 | +29.790 | +17.173…+33.180 |

La variante corrente resta indietro fino a D15, poi recupera e a D20 supera
la mediana economica della coorte exact `7-7-0`, restando dentro il suo range.
È un segnale interessante sulla monetizzazione animale/Goose, ma non è una
stima causale: cambiano topologia, specie, seed, avversario e mercato.

## Cosa trasferire alla prossima versione Codex

1. Congelare il nucleo E18.26 D1-D10 e il target crop
   `12 Melon + 20 Strawberry + 5 Wheat`.
2. Rendere esplicito il ritiro di tutti i 12 Melon tra D11 e D15; non basta
   replicare la fotografia D10.
3. Mantenere il target normativo exact `7-7-0`: 14 animali, `9 Cow + 5 Sheep`,
   e 61 crop `38 Strawberry + 23 Wheat` a D15-D20.
4. Implementare il reclaim di una struttura vuota come regola state-driven:
   nel replay corrente la coop vuota a D15 viene convertita in Wheat entro
   D20. La regola deve restare generica e non introdurre coop in Codex.
5. Conservare harvest-first e FEED hard nella transizione D11-D14. Il profilo
   exact `7-7-0` esegue in D11-D20 `90 PLANT`, `464 WATER`, `150 HARVEST`,
   `5 DIG`, `1.329 MOVE`, `171 PASS` e `1.264` azioni produttive.
6. Non importare nella prossima release il mix Goose o il layout `10-7-0`:
   sono una futura ablation separata, ammessa soltanto dopo la riduzione del
   gap mantenendo il lock topologico deciso.

## Artefatti riusabili

- evidenza normalizzata e mappe: `artifacts/derived/JESSE_BULLARD_REPLAY_105717134_D01_D20_2026_09_05.json`;
- confronto storico exact `7-7-0`: `artifacts/derived/E18_18_770_COMPOSITION_COMPARISON_2026_09_04.json`;
- specifica corrente: `MODEL_SPEC_CODEX_E18_26_770_TOP770_BOOST_D10_V1.md`.

Le mappe nell'artefatto conservano per ogni cella posizione, coltura, stadio,
acqua, fertilizzazione, struttura, animale, badge di resa e agente visibile.
