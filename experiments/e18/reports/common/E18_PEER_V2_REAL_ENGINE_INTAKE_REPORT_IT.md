# E18 — intake real-engine delle peer V2

## Verdetto

Il round robin completo da `84` match separa nettamente reattività dichiarata
e capacità competitiva. Solo il controllo V4D supera tutti i gate: `42-0`,
denaro medio `125.490,40`, zero errori, fallback e perdite zootecniche.
Antigravity è escluso per decisione del proprietario e non compare nella
matrice.

| Agente | Record | Denaro medio | Regimi attivi | Perdite verificate | Verdetto |
|---|---:|---:|---:|---:|---|
| V4D control | 42-0 | 125.490,40 | 1 statico | 0 | unico PASS |
| E18.1 ablation | 28-14 | 104.516,71 | 1 (`6-6-2`) | 0 | fail dinamico |
| Claude E18.2 | 14-28 | 9.756,29 | 2 | 44 | fail economico/safety |
| Copilot E18.2 | 0-42 | 260,00 | 1 (`EXPANSION`) | 0 | fail catena produttiva/dinamica |

Il precedente artifact Copilot da 42 match era sintetico; questo report lo
sostituisce con esecuzioni reali nel motore. Claude dimostra divergenza
condizionata di azioni e architettura in `14/14` gruppi, ma il selector non
compensa una catena agricola fragile. Copilot resta a un solo profilo
architetturale e a denaro costante.

## Delta verso il target 100k

- V4D: `+25.490,40` (`125,49%` del target);
- E18.1: `+4.516,71` (`104,52%`);
- Claude E18.2: `-90.243,71` (`9,76%`);
- Copilot E18.2: `-99.740,00` (`0,26%`).

E18.1 conferma che modificare la topologia non basta: resta economicamente
valida contro peer deboli, ma perde tutti i `14` diretti con V4D. Claude e
Copilot sono utili come stressor architetturali, non come riferimenti
economici.

## Confine dell'evidenza

- sette seed development E18, entrambi i seat;
- sei coppie, `14` match per coppia;
- motore Kaggriculture reale, nessun KPI generato da formule;
- nessun seed holdout o final-confirmation consumato;
- nessuna promozione e nessuna submission automatica.

## Artefatti

- `artifacts/derived/common/E18_PEER_V2_REAL_ENGINE_INTAKE_V1.json`;
- `artifacts/derived/common/E18_PEER_V2_REAL_ENGINE_INTAKE_V1.csv`;
- `tools/common/run_e18_peer_v2_real_engine_intake.py`.
