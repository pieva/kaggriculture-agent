# E17 Analisi Indipendente Replay Top 3 — Antigravity

- **Agent ID:** `antigravity`
- **Fase:** E17 Replay Discovery & Independent Analysis
- **Data:** 2026-09-01
- **Ambito:** Analisi quantitativa e forense dei 9 replay benchmark E17 (Top 3: `tetsuya`, `OceanMix`, `Crop Dusta`)
- **Stato:** COMPLETE / INDEPENDENT PASS CLOSED
- **Foundation di riferimento:** Model Foundation C2.1 ([FOUNDATION_C2_1_MANIFEST.md](../../../../docs/foundation/FOUNDATION_C2_1_MANIFEST.md), [ONTOLOGY_C2_1.md](../../../../docs/foundation/ontology/ONTOLOGY_C2_1.md), [KAGGRICULTURE_STATE_MACHINE_C2_1.md](../../../../docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md), [KAGGRICULTURE_FEATURE_MODEL_C2_1.md](../../../../docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md))
- **MODEL_SPEC di riferimento:** [MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md](../../../../docs/model_specs/antigravity/MODEL_SPEC_ANTIGRAVITY_C2_3Q_POST_FOUNDATION_REVIEW.md)
- **Catalogo benchmark:** `data/replays/MANIFEST.md`
- **Dataset metriche strutturato:** [E17_TOP3_REPLAY_METRICS.json](../../artifacts/discovery/antigravity/E17_TOP3_REPLAY_METRICS.json)
- **Script di estrazione:** [analyze_top3_replays.py](../../tools/antigravity/analyze_top3_replays.py), [print_summary.py](../../tools/antigravity/print_summary.py)

---

## 1. Executive Summary

L'analisi indipendente condotta sui 9 replay benchmark E17 rivela la struttura strategica, temporale ed economica dei vertici della leaderboard Kaggle (rating al momento della raccolta: `tetsuya` 2947.0, `OceanMix` 2875.8, `Crop Dusta` 2869.0).

### Principali scoperte quantitative `[OBSERVED]` / `[DERIVED]`:

1. **Topologia 3Q Universale (Q0 + Q1 + Q2):**
   - Tutti e 9 gli episodi mostrano l'adozione esclusiva della configurazione a 3 quadranti (`NW`, `NE`, `SW`), con esattamente 75 tile sbloccate e **zero sblocchi di Q3 (`SE`)** in qualsiasi partita o agente `[OBSERVED]`.
   - Il timing di sblocco temporale medio varia nettamente tra agenti:
     - `Crop Dusta`: Sblocco ultra-precoce: **Q1 a Giorno 5.4 (Step 132.8)** e **Q2 a Giorno 8.2 (Step 204.8)** `[OBSERVED]`.
     - `OceanMix` / `Driz Lo` / `yukino` / `QQ Farming`: Sblocco sincronizzato: **Q1 a Giorno 6.0 (Step 151.0)** e **Q2 a Giorno 11.0 (Step 266.0)** `[OBSERVED]`.
     - `tetsuya`: Sblocco specializzato: **Q1 a Giorno 7.0 (Step 169.0)** e **Q2 a Giorno 10.0 (Step 241.0)** `[OBSERVED]`.

2. **Famiglia Architetturale OceanMix / Driz Lo / yukino / QQ Farming:**
   - Condividono la medesima macro-routine (12 Melon, 185-195 Wheat, 33-38 Strawberry, 9-13 Carrot; 6-7 Cow, 6-11 Sheep; peak hands: 12; Move/Prod ratio $\sim 1.04$). Le differenze tra loro sono limitate a micro-variazioni di selling terminale o priorità di mercato per seat order `[OBSERVED]`.
   - **Distribuzione spaziale terminale:** Concentrano il 100% degli animali nei quadranti Q0 e Q1 (6-7 capi in Q0, 7 capi in Q1), lasciando **Q2 con 0 animali e 25/25 tile libere/non coltivate a fine match** `[OBSERVED]`.

3. **La strategia dominante di `tetsuya` (Leader di Rating & Score):**
   - `tetsuya` ottiene lo score medio più elevato del corpus (**$96.568,00**, record 3W–1L, picco $119.754):
     - **Reinvestimento integrale precoce:** fino al Giorno 10 trattiene pochissima cassa liquida ($452–$1.174 al D10 vs $15.400–$17.191 di OceanMix), convertendo tutto in asset prima del D11 `[OBSERVED]`.
     - **Mix zootecnico distribuito anche in Q2:** a fine match mantiene 6-7 animali in Q0 (Cows + Sheep), 2 in Q1, e **6-7 animali in Q2 (Sheep + Goose)** `[OBSERVED]`.
     - **Zero Animal Escapes e Zero Unsold Inventory:** 0 fughe di animali su 4 match e valore dell'inventario invenduto finale pari esattamente a **$0,00** in tutti i match `[OBSERVED]`.

4. **Il paradosso di `Crop Dusta` (Alta varianza & Fragilità logistica):**
   - `Crop Dusta` sperimenta layout dispersi e mix insoliti (l'unico a piantare Tomato, fino a 67 Carrot e 8 Oche), ma subisce **31 fughe di animali totali** (media 6.2 fughe/match) per mancato servicing tempestivo causato dall'elevato travel overhead (Move/Prod ratio di **1.4267**, $>4.070$ passi/match) `[OBSERVED]`.

---

## 2. Verifica del corpus e metodologia

### 2.1 Integrità e provenance dei 9 replay E17

Tutti i nove replay specificati sono stati verificati e processati integralmente.

| Episode ID | SHA-256 (Primi 16 caratteri) | Module Version | Steps | Stato Terminale | Seed | Seat 0 (P0) | Score P0 | Seat 1 (P1) | Score P1 | Vincitore |
|---:|---|---|---:|:---:|---:|---|---:|---|---:|---|
| `104527555` | `25cd7c23ee8a49c9` | `1.32.7` | 720 | `DONE / DONE` | 1528678515 | **tetsuya** | 81.050 | Driz Lo | 52.953 | tetsuya (+28.097) |
| `104541810` | `a1994d0d8f123cb2` | `1.32.7` | 720 | `DONE / DONE` | 1966088317 | **tetsuya** | 109.204 | QQ Farming | 97.241 | tetsuya (+11.963) |
| `104543983` | `ea1f53bd0bf83e20` | `1.32.7` | 720 | `DONE / DONE` | 782592907 | **Crop Dusta** | 83.634 | **tetsuya** | 76.264 | Crop Dusta (+7.370) |
| `104547425` | `2aed6ebb189d3d3a` | `1.32.7` | 720 | `DONE / DONE` | 394646827 | **OceanMix** | 114.361 | **Crop Dusta** | 106.328 | OceanMix (+8.033) |
| `104564762` | `5eaa3f6941a1eb75` | `1.32.7` | 720 | `DONE / DONE` | 1014643766 | Driz Lo | 90.185 | **Crop Dusta** | 87.152 | Driz Lo (+3.033) |
| `104577270` | `d85695bbc9b5f9fe` | `1.32.7` | 720 | `DONE / DONE` | 620836918 | yukino | 90.053 | **OceanMix** | 86.580 | yukino (+3.473) |
| `104578185` | `d3179a6af500c6d5` | `1.32.7` | 720 | `DONE / DONE` | 533536224 | **tetsuya** | 119.754 | **Crop Dusta** | 114.881 | tetsuya (+4.873) |
| `104586335` | `74de13cec7d9bebe` | `1.32.7` | 720 | `DONE / DONE` | 1554265238 | **Crop Dusta** | 64.811 | **OceanMix** | 51.238 | Crop Dusta (+13.573) |
| `104586487` | `6248287ce0c13636` | `1.32.7` | 720 | `DONE / DONE` | 1015196962 | **OceanMix** | 77.962 | Driz Lo | 75.760 | OceanMix (+2.202) |

---

## 3. Schede sintetiche dei 9 episodi con Sblocco Temporale e Breakdown Quadranti

### Episodio 1: `104527555` — `tetsuya` (P0, $81.050) vs `Driz Lo` (P1, $52.953)
- **Seed:** 1528678515 | **Margine:** +$28.097 per tetsuya | **Matchup:** Top 3 vs External
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`tetsuya`): Q1 Sblocco = **Giorno 7 (Step 169)** | Q2 Sblocco = **Giorno 10 (Step 241)**
  - P1 (`Driz Lo`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
- **Breakdown Tile Terminali per Quadrante (25 tile per quadrante) `[OBSERVED]`:**
  - **P0 (`tetsuya`):**
    - `Q0_NW`: Non coltivate: 17 (Libere: 17, Weeds: 0) | Colture: 0 | **Animali: 8** (`COW:4, SHEEP:4`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 17, Weeds: 1) | **Colture: 4** (`CARROT:3, WHEAT:1`) | **Animali: 3** (`SHEEP:3`)
    - `Q2_SW`: Non coltivate: 21 (Libere: 20, Weeds: 1) | Colture: 0 | **Animali: 4** (`GOOSE:1, SHEEP:3`)
  - **P1 (`Driz Lo`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:2, SHEEP:5`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0

### Episodio 2: `104541810` — `tetsuya` (P0, $109.204) vs `QQ Farming` (P1, $97.241)
- **Seed:** 1966088317 | **Margine:** +$11.963 per tetsuya | **Matchup:** Top 3 vs External
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`tetsuya`): Q1 Sblocco = **Giorno 7 (Step 169)** | Q2 Sblocco = **Giorno 10 (Step 241)**
  - P1 (`QQ Farming`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`tetsuya`):**
    - `Q0_NW`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:4, SHEEP:3`)
    - `Q1_NE`: Non coltivate: 20 (Libere: 20, Weeds: 0) | **Colture: 3** (`WHEAT:3`) | **Animali: 2** (`SHEEP:2`)
    - `Q2_SW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`GOOSE:1, SHEEP:5`)
  - **P1 (`QQ Farming`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:2, SHEEP:5`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0

### Episodio 3: `104543983` — `Crop Dusta` (P0, $83.634) vs `tetsuya` (P1, $76.264)
- **Seed:** 782592907 | **Margine:** +$7.370 per Crop Dusta | **Matchup:** Scontro Diretto Top 3 (#1 vs #3)
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`Crop Dusta`): Q1 Sblocco = **Giorno 6 (Step 155)** | Q2 Sblocco = **Giorno 9 (Step 223)**
  - P1 (`tetsuya`): Q1 Sblocco = **Giorno 7 (Step 169)** | Q2 Sblocco = **Giorno 10 (Step 241)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`Crop Dusta`):**
    - `Q0_NW`: Non coltivate: 17 (Libere: 15, Weeds: 2) | **Colture: 1** (`WHEAT:1`) | **Animali: 5** (`COW:3, SHEEP:2`) | Strutture vuote: 2 (`PASTURE:2`)
    - `Q1_NE`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 5** (`COW:1, GOOSE:4`) | Strutture vuote: 1 (`PASTURE:1`)
    - `Q2_SW`: Non coltivate: 19 (Libere: 18, Weeds: 1) | **Colture: 2** (`CARROT:1, STRAWBERRY:1`) | **Animali: 4** (`COW:4`)
  - **P1 (`tetsuya`):**
    - `Q0_NW`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:4, SHEEP:3`)
    - `Q1_NE`: Non coltivate: 23 (Libere: 23, Weeds: 0) | Colture: 0 | **Animali: 2** (`COW:2`)
    - `Q2_SW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`GOOSE:5, SHEEP:1`)

### Episodio 4: `104547425` — `OceanMix` (P0, $114.361) vs `Crop Dusta` (P1, $106.328)
- **Seed:** 394646827 | **Margine:** +$8.033 per OceanMix | **Matchup:** Scontro Diretto Top 3 (#2 vs #3)
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`OceanMix`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
  - P1 (`Crop Dusta`): Q1 Sblocco = **Giorno 5 (Step 122)** | Q2 Sblocco = **Giorno 8 (Step 203)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`OceanMix`):**
    - `Q0_NW`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:5, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:4, SHEEP:3`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0
  - **P1 (`Crop Dusta`):**
    - `Q0_NW`: Non coltivate: 16 (Libere: 16, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`) | Strutture vuote: 3 (`PASTURE:3`)
    - `Q1_NE`: Non coltivate: 17 (Libere: 17, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:2, SHEEP:4`) | Strutture vuote: 2 (`PASTURE:2`)
    - `Q2_SW`: Non coltivate: 23 (Libere: 23, Weeds: 0) | Colture: 0 | **Animali: 2** (`SHEEP:2`)

### Episodio 5: `104564762` — `Driz Lo` (P0, $90.185) vs `Crop Dusta` (P1, $87.152)
- **Seed:** 1014643766 | **Margine:** +$3.033 per Driz Lo | **Matchup:** External vs Top 3
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`Driz Lo`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
  - P1 (`Crop Dusta`): Q1 Sblocco = **Giorno 5 (Step 122)** | Q2 Sblocco = **Giorno 8 (Step 203)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`Driz Lo`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:3, SHEEP:4`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0
  - **P1 (`Crop Dusta`):**
    - `Q0_NW`: Non coltivate: 17 (Libere: 16, Weeds: 1) | **Colture: 3** (`TOMATO:3`) | **Animali: 5** (`COW:5`)
    - `Q1_NE`: Non coltivate: 15 (Libere: 12, Weeds: 3) | **Colture: 5** (`TOMATO:5`) | **Animali: 1** (`COW:1`) | Strutture vuote: 4 (`PASTURE:4`)
    - `Q2_SW`: Non coltivate: 18 (Libere: 15, Weeds: 3) | **Colture: 2** (`TOMATO:2`) | **Animali: 5** (`GOOSE:5`)

### Episodio 6: `104577270` — `yukino` (P0, $90.053) vs `OceanMix` (P1, $86.580)
- **Seed:** 620836918 | **Margine:** +$3.473 per yukino | **Matchup:** External vs Top 3
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`yukino`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
  - P1 (`OceanMix`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`yukino`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:3, SHEEP:4`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0
  - **P1 (`OceanMix`):**
    - `Q0_NW`: Non coltivate: 16 (Libere: 16, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:4, SHEEP:3`) | Strutture vuote: 2 (`COOP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:5, SHEEP:2`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0

### Episodio 7: `104578185` — `tetsuya` (P0, $119.754) vs `Crop Dusta` (P1, $114.881)
- **Seed:** 533536224 | **Margine:** +$4.873 per tetsuya | **Matchup:** Scontro Diretto Top 3 (#1 vs #3)
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`tetsuya`): Q1 Sblocco = **Giorno 7 (Step 169)** | Q2 Sblocco = **Giorno 10 (Step 241)**
  - P1 (`Crop Dusta`): Q1 Sblocco = **Giorno 6 (Step 155)** | Q2 Sblocco = **Giorno 8 (Step 212)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`tetsuya`):**
    - `Q0_NW`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:4, SHEEP:3`)
    - `Q1_NE`: Non coltivate: 19 (Libere: 19, Weeds: 0) | **Colture: 4** (`CARROT:2, WHEAT:2`) | **Animali: 2** (`COW:2`)
    - `Q2_SW`: Non coltivate: 19 (Libere: 18, Weeds: 1) | Colture: 0 | **Animali: 6** (`GOOSE:1, SHEEP:5`)
  - **P1 (`Crop Dusta`):**
    - `Q0_NW`: Non coltivate: 16 (Libere: 14, Weeds: 2) | **Colture: 1** (`TOMATO:1`) | **Animali: 4** (`COW:3, SHEEP:1`) | Strutture vuote: 4 (`PASTURE:4`)
    - `Q1_NE`: Non coltivate: 15 (Libere: 15, Weeds: 0) | **Colture: 1** (`STRAWBERRY:1`) | **Animali: 5** (`COW:3, SHEEP:2`) | Strutture vuote: 4 (`PASTURE:4`)
    - `Q2_SW`: Non coltivate: 23 (Libere: 17, Weeds: 6) | **Colture: 2** (`TOMATO:2`) | Animali: 0

### Episodio 8: `104586335` — `Crop Dusta` (P0, $64.811) vs `OceanMix` (P1, $51.238)
- **Seed:** 1554265238 | **Margine:** +$13.573 per Crop Dusta | **Matchup:** Scontro Diretto Top 3 (#3 vs #2)
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`Crop Dusta`): Q1 Sblocco = **Giorno 5 (Step 122)** | Q2 Sblocco = **Giorno 8 (Step 203)**
  - P1 (`OceanMix`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`Crop Dusta`):**
    - `Q0_NW`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 3** (`COW:1, GOOSE:2`) | Strutture vuote: 4 (`PASTURE:4`)
    - `Q1_NE`: Non coltivate: 21 (Libere: 20, Weeds: 1) | Colture: 0 | **Animali: 3** (`GOOSE:3`) | Strutture vuote: 1 (`PASTURE:1`)
    - `Q2_SW`: Non coltivate: 21 (Libere: 21, Weeds: 0) | **Colture: 1** (`CARROT:1`) | **Animali: 3** (`GOOSE:3`)
  - **P1 (`OceanMix`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:3, SHEEP:4`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0

### Episodio 9: `104586487` — `OceanMix` (P0, $77.962) vs `Driz Lo` (P1, $75.760)
- **Seed:** 1015196962 | **Margine:** +$2.202 per OceanMix | **Matchup:** Top 3 vs External
- **Sblocchi Temporali `[OBSERVED]`:**
  - P0 (`OceanMix`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
  - P1 (`Driz Lo`): Q1 Sblocco = **Giorno 6 (Step 151)** | Q2 Sblocco = **Giorno 11 (Step 266)**
- **Breakdown Tile Terminali per Quadrante `[OBSERVED]`:**
  - **P0 (`OceanMix`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 17, Weeds: 1) | Colture: 0 | **Animali: 7** (`COW:3, SHEEP:4`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0
  - **P1 (`Driz Lo`):**
    - `Q0_NW`: Non coltivate: 19 (Libere: 19, Weeds: 0) | Colture: 0 | **Animali: 6** (`COW:4, SHEEP:2`)
    - `Q1_NE`: Non coltivate: 18 (Libere: 18, Weeds: 0) | Colture: 0 | **Animali: 7** (`COW:3, SHEEP:4`)
    - `Q2_SW`: Non coltivate: 25 (Libere: 25, Weeds: 0) | Colture: 0 | Animali: 0

---

## 4. Confronto quantitativo Top 3

### 4.1 Tabella comparativa macro-metrica

| Macro-Metrica | `tetsuya` (4 Ep) | `OceanMix` (4 Ep) | `Crop Dusta` (5 Ep) | `Driz Lo` (3 Ep) | `yukino` (1 Ep) | `QQ Farming` (1 Ep) |
|---|---:|---:|---:|---:|---:|---:|
| **Score Medio E17** `[OBSERVED]` | **$96.568,00** | $82.535,25 | $91.361,20 | $72.966,00 | $90.053,00 | $97.241,00 |
| **Record nel Corpus** `[OBSERVED]` | **3W – 1L (75,0%)** | 2W – 2L (50,0%) | 2W – 3L (40,0%) | 1W – 2L (33,3%) | 1W – 0L (100%) | 0W – 1L (0%) |
| **Sblocco Medio Q1 (Giorno / Step)** `[OBSERVED]` | **D7,0 (Step 169,0)** | **D6,0 (Step 151,0)** | **D5,4 (Step 132,8)** | **D6,0 (Step 151,0)** | **D6,0 (Step 151,0)** | **D6,0 (Step 151,0)** |
| **Sblocco Medio Q2 (Giorno / Step)** `[OBSERVED]` | **D10,0 (Step 241,0)** | **D11,0 (Step 266,0)** | **D8,2 (Step 204,8)** | **D11,0 (Step 266,0)** | **D11,0 (Step 266,0)** | **D11,0 (Step 266,0)** |
| **Sblocco Q3 (SE)** `[OBSERVED]` | **MAI (0%)** | **MAI (0%)** | **MAI (0%)** | **MAI (0%)** | **MAI (0%)** | **MAI (0%)** |
| **Move / Productive Ratio** `[OBSERVED]` | 1,2553 | **1,0468** | 1,4267 | 1,0143 | 1,0374 | 0,9734 |
| **Fughe di Animali Totali** `[OBSERVED]` | **0 (0,0/m)** | **0 (0,0/m)** | **31 (6,2/m)** | **0 (0,0/m)** | **0 (0,0/m)** | **0 (0,0/m)** |
| **Inventario Invenduto Medio ($)** `[OBSERVED]` | **$0,00** | $35,50 | $373,00 | $15,00 | $161,00 | $60,00 |

---

### 4.2 Sblocco Temporale e Distribuzione Finale Tile per Quadrante

Questa tabella sintetizza il **tempo di sblocco di Q1 e Q2** e la **media delle tile terminali** (su 25 tile per quadrante) per ciascun partecipante nei tre quadranti sbloccati:

| Agente | Sblocco Q1 `[OBSERVED]` | Sblocco Q2 `[OBSERVED]` | Quadrante | Non Coltivate / Libere `[OBSERVED]` | Colture Attive `[OBSERVED]` | Animali Vivi `[OBSERVED]` | Strutture Vuote `[OBSERVED]` |
|---|:---:|:---:|:---:|---:|---:|---:|---:|
| **`tetsuya`** | **Giorno 7 (Step 169)** | **Giorno 10 (Step 241)** | **Q0 (NW)** | **17,8** (Libere: 17,8, Weeds: 0,0) | **0,0** | **7,2** (Cow: 4,0, Sheep: 3,2) | 0,0 |
| | | | **Q1 (NE)** | **20,0** (Libere: 19,8, Weeds: 0,2) | **2,8** (Wheat: 1,5, Carrot: 1,2) | **2,2** (Sheep: 1,8, Cow: 0,5) | 0,0 |
| | | | **Q2 (SW)** | **19,5** (Libere: 19,0, Weeds: 0,5) | **0,0** | **5,5** (Goose: 2,0, Sheep: 3,5) | 0,0 |
| **`OceanMix`** | **Giorno 6 (Step 151)** | **Giorno 11 (Step 266)** | **Q0 (NW)** | **18,0** (Libere: 18,0, Weeds: 0,0) | **0,0** | **6,5** (Cow: 4,2, Sheep: 2,2) | 0,5 |
| | | | **Q1 (NE)** | **18,0** (Libere: 17,8, Weeds: 0,2) | **0,0** | **7,0** (Cow: 3,8, Sheep: 3,2) | 0,0 |
| | | | **Q2 (SW)** | **25,0** (Libere: 25,0, Weeds: 0,0) | **0,0** | **0,0** (Zero strutture) | 0,0 |
| **`Crop Dusta`** | **Giorno 5,4 (Step 132,8)** | **Giorno 8,2 (Step 204,8)** | **Q0 (NW)** | **16,8** (Libere: 15,8, Weeds: 1,0) | **1,0** (Tomato: 0,8, Wheat: 0,2) | **4,6** (Cow: 3,2, Sheep: 0,8, Goose: 0,6) | **2,6** |
| | | | **Q1 (NE)** | **17,4** (Libere: 16,6, Weeds: 0,8) | **1,2** (Tomato: 1,0, Strawb: 0,2) | **4,2** (Cow: 1,4, Sheep: 1,6, Goose: 1,2) | **2,2** |
| | | | **Q2 (SW)** | **20,8** (Libere: 18,8, Weeds: 2,0) | **1,4** (Tomato: 0,8, Carrot: 0,4, Strawb: 0,2) | **2,8** (Goose: 2,2, Cow: 0,8, Sheep: 0,4) | 0,0 |
| **`Driz Lo`** | **Giorno 6 (Step 151)** | **Giorno 11 (Step 266)** | **Q0 (NW)** | **19,0** (Libere: 19,0, Weeds: 0,0) | **0,0** | **6,0** (Cow: 4,0, Sheep: 2,0) | 0,0 |
| | | | **Q1 (NE)** | **18,0** (Libere: 18,0, Weeds: 0,0) | **0,0** | **7,0** (Cow: 2,7, Sheep: 4,3) | 0,0 |
| | | | **Q2 (SW)** | **25,0** (Libere: 25,0, Weeds: 0,0) | **0,0** | **0,0** (Zero strutture) | 0,0 |
| **`yukino`** | **Giorno 6 (Step 151)** | **Giorno 11 (Step 266)** | **Q0 (NW)** | **19,0** (Libere: 19,0, Weeds: 0,0) | **0,0** | **6,0** (Cow: 4,0, Sheep: 2,0) | 0,0 |
| | | | **Q1 (NE)** | **18,0** (Libere: 18,0, Weeds: 0,0) | **0,0** | **7,0** (Cow: 3,0, Sheep: 4,0) | 0,0 |
| | | | **Q2 (SW)** | **25,0** (Libere: 25,0, Weeds: 0,0) | **0,0** | **0,0** (Zero strutture) | 0,0 |
| **`QQ Farming`** | **Giorno 6 (Step 151)** | **Giorno 11 (Step 266)** | **Q0 (NW)** | **19,0** (Libere: 19,0, Weeds: 0,0) | **0,0** | **6,0** (Cow: 4,0, Sheep: 2,0) | 0,0 |
| | | | **Q1 (NE)** | **18,0** (Libere: 18,0, Weeds: 0,0) | **0,0** | **7,0** (Cow: 2,0, Sheep: 5,0) | 0,0 |
| | | | **Q2 (SW)** | **25,0** (Libere: 25,0, Weeds: 0,0) | **0,0** | **0,0** (Zero strutture) | 0,0 |

---

## 5. Pattern comuni, differenze e inferenze causali

### 5.1 Pattern comuni a tutti e tre gli agenti Top 3 `[OBSERVED]`
1. **Rifiuto categorico del 4° Quadrante (Q3):** nessun agente compra mai il quarto quadrante (`SE`). La superficie totale rimane fissa a 75 tile (Q0 + Q1 + Q2).
2. **Saturazione della Workforce a 12 Farm Hands (13 Worker totali):** tutti gli agenti raggiungono il picco di 12 Farm Hands con progressione giornaliera.
3. **Pilastro Melon a 12 tile:** tutti piantano esattamente 12-16 sementi di Melon a inizio partita nel quadrante iniziale Q0, monetizzandole tra il D10 e il D13.
4. **Allevamento misto dominante Cow + Sheep:** tutti gli agenti fanno largo affidamento sulla combinazione Mucca (latte ogni 2 giorni) e Pecora (lana ogni 3 giorni).

### 5.2 Pattern condivisi da due agenti `[OBSERVED]`
1. **Zero Animal Escapes (`tetsuya` + `OceanMix`):** entrambi garantiscono il 100% di continuità alimentare, azzerando le perdite di capitale zootecnico.
2. **Timing Q1=D6, Q2=D11 (`OceanMix` + `Driz Lo` + `yukino`):** cadenza di espansione sincronizzata con il ciclo di maturazione del Melon.
3. **Impiego mirato delle Oche (`tetsuya` + `Crop Dusta`):** presenza di Goose per integrare la produzione di Egg e Fertilizer biologico.

### 5.3 Scelte specifiche ed idiosincratiche `[OBSERVED]`
1. **`tetsuya`:**
   - Reinvestimento integrale precoce (cassa al D10 $< \$1.200$).
   - Sbilanciamento marcato verso le Pecore (8-10 Sheep vs 4-6 Cow).
   - Liquidazione perfetta: 0 unità invendute in tutti i match.
2. **`OceanMix`:**
   - Mega-cluster ipercentrato su Q0/Q1 (zero strutture in Q2).
   - Minimo move overhead assoluto (Move/Prod $\sim 1.04$).
   - Forte orientamento verso le Mucche (fino a 10 Cow).
3. **`Crop Dusta`:**
   - Espansione anticipata aggressiva (Q1 a D5, Q2 a D8).
   - Uso esclusivo di Tomato (10-16 tile).
   - Layout disperso e grave vulnerabilità logistica (31 fughe di animali totali).

---

## 6. Gap rispetto al proprio agente (Antigravity V4.0)

| ID Gap | Evidenza Replay E17 | Comportamento Attuale Antigravity V4 | Natura del Gap | Impatto Atteso | Confidenza | Informazione Mancante / Unknown |
|---|---|---|---|---|:---:|---|
| **GAP-01** | `tetsuya` investe il 100% della cassa entro il D10 (cassa D10 $\approx \$700$) accelerando Q2 al D10 e saturando Sheep/Strawberry | Antigravity accumula $15k di liquidità fino al D11 per comprare Q2 in un timing fisso standard | **Politica di Capitale & Reinvestimento** | **ALTO (+8.000 / match)** | `HIGH` | Elasticità dei prezzi su acquisti semi anticipati |
| **GAP-02** | `tetsuya` alloca 10 Sheep e 4-6 Cow massimizzando la lana, con 40 Strawberry e 0 Carrot | Antigravity usa 8 Cow e 11 Sheep con mix colturale ereditato da Codex V9 | **Mix Produttivo & Specializzazione** | **MEDIO (+4.000 / match)** | `HIGH` | Curve di prezzo Wool vs Milk in match ad alta contesa |
| **GAP-03** | `Crop Dusta` dimostra che anticipare Q2 al Giorno 8 aumenta drasticamente la capacità produttiva lorda, ma fallisce per starvation dei worker | Antigravity attende il D11 per attivare Q2 | **Timing Espansione Fondiaria** | **ALTO (+10.000 / match se stabilizzato)** | `MEDIUM` | Fabbisogno esatto di worker per servire Q2 anticipato senza fughe |
| **GAP-04** | `OceanMix` ottiene Move/Prod ratio di 1.04 confinando tutte le 18 strutture in Q0/Q1 vicino allo shed | Antigravity distribuisce strutture anche in Q2, con Move/Prod ratio di 1.2477 | **Routing & Topologia Zootecnica** | **MEDIO (+3.000 / match in slot utili)** | `HIGH` | Trade-off tra spazio arabile in Q0/Q1 e travel overhead |
| **GAP-05** | Tutti i Top 3 usano tabelle e sequenze proprietarie indipendenti | Antigravity V4 è formalmente una baseline derivativa con dipendenza da `codex_v9_routine_data` | **Indipendenza Strategica & Proprietà Intellettuale** | **STRATEGICO / QUALIFICANTE** | `HIGH` | Nessuna (requisito primario E17) |

---

## 7. Ipotesi per E17 ordinate per valore informativo

### Ipotesi 1 (Priorità 1 - Massima): Anticipo del Reinvestimento di Capitale e Sblocco Q2 a Giorno 10 (`H-E17-CAP-REINVEST`)
1. **Meccanismo causale proposto:** Reinvestire immediatamente il ricavo delle vendite di Wheat/Melon nei giorni 7-10 per sbloccare Q2 al Giorno 10 (anziché D11) e comprare 2 capi di bestiame addizionali 24 ore prima genera un ciclo biologico extra di produzione e anticipa il cashflow espansivo.
2. **Evidenza a supporto & controevidenza:**
   - *Supporto:* `tetsuya` adotta esattamente questa politica in tutti i 4 match, raggiungendo lo score medio di $96.568.
   - *Controevidenza:* se i prezzi di vendita del grano scendono per contesa, la liquidità al D10 potrebbe non bastare per Q2 + HIRE contemporanei.
3. **Singola modifica sperimentale:** Modifica del calendario di spesa nei giorni 8-10 con anticipo dell'ordine `BUY_LAND (Q2)` al tick $t=216$ (D9-EOD / D10-start).
4. **Baseline e Controllo:** Antigravity V4.0 (Q2 sbloccato a D11, step 264).
5. **Seed policy & Repliche:** 12 seed holdout canonici (Phase B + C) $\times$ 2 seat (24 match totali).
6. **Metriche:** Primaria: `final_money_outcome`. Diagnostiche: cassa al D10, giorno primo output Q2, animal escapes count.
7. **Criterio di promozione:** $\Delta \text{Mean} \ge +\$3.000$, zero animal escapes.
8. **Criterio di falsificazione / rollback:** Qualsiasi fuga di animale o $\Delta \text{Mean} < 0$.
9. **Rischio di regressione:** Basso (variazione limitata a 24 step di anticipo).
10. **Costo informativo & Priorità:** Costo basso, priorità **MASSIMA**.

---

### Ipotesi 2 (Priorità 2): Ottimizzazione del Mix Zootecnico 10-Sheep / 4-Cow (`H-E17-SHEEP-CONCENTRATION`)
1. **Meccanismo causale proposto:** Spostare il rapporto del bestiame verso le Pecore (10 Sheep / 4 Cow anziché 11 Sheep / 8 Cow) riduce il fabbisogno giornaliero di Wheat per `FEED` (la pecora produce lana ogni 3 giorni ma richiede solo 1 feed al giorno, con un margine netto per unità di mangime superiore se il prezzo del latte declina).
2. **Evidenza a supporto & controevidenza:**
   - *Supporto:* `tetsuya` vince EP 104527555 e EP 104541810 con 10 Sheep e 4 Cow.
   - *Controevidenza:* `OceanMix` raggiunge $114k in EP 104547425 puntando su 10 Cow.
3. **Singola modifica sperimentale:** Riconfigurazione degli ordini `BUY_ANIMAL` nei giorni 4-9 per attestarsi su target 10 Sheep, 4 Cow, 1 Goose.
4. **Baseline e Controllo:** Antigravity V4.0 (8 Cow, 11 Sheep).
5. **Seed policy & Repliche:** 12 seed holdout canonici $\times$ 2 seat (24 match).
6. **Metriche:** Primaria: `final_money_outcome`. Diagnostiche: `feed_market_expenditure`, ricavo Wool vs Milk.
7. **Criterio di promozione:** $\Delta \text{Mean} \ge +\$2.000$.
8. **Criterio di falsificazione:** $\Delta \text{Mean} \le 0$.
9. **Rischio di regressione:** Basso.
10. **Costo informativo & Priorità:** Costo basso, priorità **ALTA**.

---

### Ipotesi 3 (Priorità 3): Compattazione Spaziale Q0/Q1 Mega-Cluster (`H-E17-COMPACT-ROUTING`)
1. **Meccanismo causale proposto:** Limitare tutti i pascoli alle sole coordinate di Q0 e Q1 (entro Manhattan distance $\le 3$ dallo shed) ed eliminare le strutture in Q2 riduce i passi di movimento per turno da $\sim 3.300$ a $< 3.000$, convertendo $\sim 300$ passi in azioni `WATER` o `FERTILIZE`.
2. **Evidenza a supporto & controevidenza:**
   - *Supporto:* `OceanMix` e `Driz Lo` registrano Move/Prod di 1.04 e 0 fughe confinando tutto il bestiame in Q0/Q1.
   - *Controevidenza:* Rallenta l'attivazione di Q2 se Q0/Q1 saturano lo spazio arabile per il grano.
3. **Singola modifica sperimentale:** Riposizionamento delle tile `PASTURE` dalle coordinate di Q2 alle coordinate perimetrali di Q1.
4. **Baseline e Controllo:** Layout V4.0 (19 pasture estese in Q2).
5. **Seed policy & Repliche:** 12 seed holdout canonici (24 match).
6. **Metriche:** Primaria: `move_to_productive_ratio`. Secondaria: `final_money_outcome`.
7. **Criterio di promozione:** `move_to_productive_ratio` $\le 1.10$ senza calo di resa zootecnica.
8. **Criterio di falsificazione:** Riduzione del numero di tile coltivabili a Strawberry/Wheat tale da deprimere il fatturato.
9. **Rischio di regressione:** Medio.
10. **Costo informativo & Priorità:** Costo medio, priorità **MEDIA**.

---

### Ipotesi 4 (Priorità 4): Generatore di Routine Indipendente End-to-End (`H-E17-INDEPENDENT-SYNTHESIZER`)
1. **Meccanismo causale proposto:** Sostituire la tabella statica importata da Codex con una routine generata e compilata interamente tramite il solver locale Antigravity (ottimizzazione a vincoli lineari su griglia e period ledger), garantendo il superamento del gate di indipendenza senza calo di densità.
2. **Evidenza a supporto & controevidenza:**
   - *Supporto:* Necessario per superare il gate di indipendenza strategica formale di E17.
   - *Controevidenza:* Rischio di regressione operativa o violazione di guardie se il solver ha discrepanze di routing.
3. **Singola modifica sperimentale:** Compilazione di `antigravity_independent_routine_v1.py` tramite solver proprietario.
4. **Baseline e Controllo:** Baseline derivativa V4.0.
5. **Seed policy & Repliche:** 12 seed holdout + suite passiva (36 match).
6. **Metriche:** Indipendenza SHA-256 (`PASS`), `final_money_outcome`, zero fughe, zero errori.
7. **Criterio di promozione:** Score medio holdout $\ge \$139.437$ (pari o superiore alla baseline derivativa).
8. **Criterio di falsificazione:** Score holdout $< \$130.000$ o insorgenza di errori/fughe.
9. **Rischio di regressione:** Alto.
10. **Costo informativo & Priorità:** Costo alto, priorità **FONDAMENTALE MA SEQUENZIATA**.

---

## 8. Rischi, limiti e unknowns

1. **Rischio di Overfitting sui 9 Replay:** Nove episodi costituiscono un campione informativo di discovery eccellente per la comprensione qualitativa e dei vincoli, ma non una misura esaustiva dell'intero spazio stocastico di Kaggle `[UNKNOWN]`.
2. **Asimmetria di Seat:** Il vantaggio di Seat 0 nel commit contemporaneo degli ordini di mercato impone di validare ogni futuro esperimento sempre su entrambi i seat (Seat 0 e Seat 1 speculari) `[DERIVED]`.
3. **Vulnerabilità alla Contesa nei Mirror:** Due agenti con routine identiche che tentano acquisti massicci di semi al medesimo turno causano rimbalzi di prezzo e mancate esecuzioni `[OBSERVED]`.

---

## 9. Raccomandazione del primo esperimento per E17

Si raccomanda formalmente di avviare la sequenza sperimentale E17 con l'**Ipotesi 1 (`H-E17-CAP-REINVEST`)**:
- **Motivazione:** È il contrasto più piccolo, pulito, causale e interpretabile; richiede solo l'anticipo del timing di reinvestimento e sblocco di Q2 dal Giorno 11 al Giorno 10, direttamente ispirato alla proprietà vincente di `tetsuya`.
- **Nessuna modifica implementativa viene eseguita in questa fase**, conformemente al mandato di **ANALYSIS ONLY**.

---

**Fine di E17_TOP3_REPLAY_ANALYSIS.md (Report Antigravity indipendente aggiornato).**
