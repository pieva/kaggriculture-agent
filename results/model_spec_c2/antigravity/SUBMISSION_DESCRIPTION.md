# Descrizione Tecnica: Antigravity C2 Dual-Quadrant (Q0+Q1) Full Livestock Candidate

**Versione:** `ANTIGRAVITY-C2-DUAL-Q0-Q1-90K-LIVESTOCK-V1.0`  
**Checkpoint Base:** `f391ee2`  
**Footprint Territoriale:** Doppio Quadrante (Q0 Nord-Ovest + Q1 Nord-Est) — Costo terra: $1,000.00 (Sbloccato Day 5-8 via Gated Liquidity)  
**Forza Lavoro:** 13 Lavoratori (Farmer W0 + 12 Braccianti W1..W12)  
**File Standalone di Submission:** `submission/submission_antigravity.py` e `submission/submission.py`  
**Configurazione Immutabile:** `configs/model_spec_c2/ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json`  

---

## 1. Visione e Architettura Generale

L'architettura **ANTIGRAVITY-C2-DUAL-Q0-Q1-LIVESTOCK** scala il modello compatto ad alta efficienza a quadrante singolo (Q0) sul quadrante adiacente Nord-Est (Q1), implementando la piena replica simmetrica sia per le colture che per l'allevamento zootecnico.

L'espansione è governata da una logica a flusso di cassa gated: lo sblocco di Q1 (`BUY_LAND` $1,000) e l'assunzione dei 6 lavoratori aggiuntivi avvengono non appena le prime colture garantiscono la copertura salariale. I braccianti dedicati di Q1 costruiscono le 6 stalle (`(6,4), (5,3), (6,3), (7,4), (5,2), (6,2)`) e popolano il quadrante con 3 Mucche e 3 Pecore (12 animali totali).

```text
TERRITORIO: Q0 (NW: x:0..4, y:0..4) + Q1 (NE: x:5..9, y:0..4)
LAND_COST: $1,000.00
COLTURE TOTALI: 16 (12 Meloni + 4 Fragole)
PASCOLI TOTALI: 12 (6 Pascoli Vacche + 6 Pascoli Pecore)
SHED MODULE TILES: Q0 -> (4,4), Q1 -> (5,4)
FORZA LAVORO: 13 (Farmer W0 + 12 Hands W1..W12)
FATTURATO LORDO MEDIO: $91,010.42 ($50,170.00 Colture + $40,840.00 Allevamento)
CAPITALE NETTO FINALE (Phase C Holdout): $66,630.67 (Picco: $87,740.00)
TASSO FUGHE ANIMALI: 0 (100% Safe)
```

---

## 2. Meccanismi Chiave di Ottimizzazione

### 1. Zootecnia a 12 Animali & Zero Fughe (`ANIMAL_ESCAPE = 0`)
- **Costruzione Pascoli e Specializzazione:** Assegnazione fissa dei ruoli zootecnici (`W4`/`W5` per Q0, `W10`/`W11` per Q1) con eleggibilità dinamica `BUILD_PASTURE` su tutte le coordinate simmetriche di Q1.
- **Stock Grano di Sicurezza:** Riserva fissa di 2 cicli di alimentazione ($2 \times \text{animali}$).
- **Resa Allevamento:** 136.50 unità di Latte e 95.83 unità di Lana per partita, con $40,840.00 di fatturato da bestiame.

### 2. Routine Orticola Dual-Quadrant (16 Tile)
- **Partizionamento Simmetrico:** 
  - Q0: 6 Meloni (`W1`, `W2`) + 2 Fragole (`W3`).
  - Q1: 6 Meloni (`W7`, `W8`) + 2 Fragole (`W9`).
- **Resa Orticola:** 157.42 Meloni + 82.58 Fragole (240 unità totali), con perfetta concimazione a ciclo chiuso.

### 3. Pipeline Finanziaria & Closed-Loop Fertilizer
- **Monetizzazione Bootstrap (D0..D5):** Vendita del concime raccolto nel capannone a \$70-\$130 per garantire la liquidità necessaria ai salari iniziali.
- **Concimazione Mirata (D6+):** Applicazione automatica del fertilizzante sulle colture irrigate non appena la cassa supera la soglia di sicurezza.

### 4. Capannone Multi-Tile & Partitioning Logistico
- **Routing Q0 vs Q1:** I lavoratori del modulo Q0 interagiscono con la cella `(4,4)`, mentre i lavoratori del modulo Q1 operano sulla cella `(5,4)`.

---

## 3. Roster e Mappatura dei Ruoli (13 Operatori)

| Worker ID | Ruolo | Modulo | Area Assegnata | Responsabilità |
| :---: | :---: | :---: | :---: | :---: |
| **W0 (Farmer)** | `RELIEF_LOGISTICS` | Q0 | Mappa completa | Logistica emergenza, stalle e supporto generale |
| **W1 (Hand 0)** | `CROP_PRIMARY_A` | Q0 | `[(0,0), (1,0), (2,0)]` | Meloni Nord Q0 |
| **W2 (Hand 1)** | `CROP_PRIMARY_B` | Q0 | `[(0,1), (1,1), (2,1)]` | Meloni Centro Q0 |
| **W3 (Hand 2)** | `CROP_EXPANSION` | Q0 | `[(0,2), (1,2)]` | Fragole Sud Q0 |
| **W4 (Hand 3)** | `LIVESTOCK_COW_Q0` | Q0 | `[(3,4), (4,3), (3,3)]` | Mucche Q0 |
| **W5 (Hand 4)** | `LIVESTOCK_SHEEP_Q0`| Q0 | `[(2,4), (4,2), (3,2)]` | Pecore Q0 |
| **W6 (Hand 5)** | `FERTILIZER_LOGISTICS`| Q0 | Modulo Q0 | Letame & concimazione Q0 |
| **W7 (Hand 6)** | `CROP_PRIMARY_A_Q1` | Q1 | `[(9,0), (8,0), (7,0)]` | Meloni Nord Q1 |
| **W8 (Hand 7)** | `CROP_PRIMARY_B_Q1` | Q1 | `[(9,1), (8,1), (7,1)]` | Meloni Centro Q1 |
| **W9 (Hand 8)** | `CROP_EXPANSION_Q1` | Q1 | `[(9,2), (8,2)]` | Fragole Sud Q1 |
| **W10 (Hand 9)**| `LIVESTOCK_COW_Q1` | Q1 | `[(6,4), (5,3), (6,3)]` | Mucche Q1 |
| **W11 (Hand 10)**| `LIVESTOCK_SHEEP_Q1`| Q1 | `[(7,4), (5,2), (6,2)]` | Pecore Q1 |
| **W12 (Hand 11)**| `FERTILIZER_LOGISTICS_Q1`| Q1 | Modulo Q1 | Letame & concimazione Q1 |

---

## 4. Benchmark e Risultati Ufficiali (12 Episodi / 720 Turni)

### Phase B (Semi Standard: 26090101, 26090102, 26090103)
- **Capitale Netto Finale Medio:** **\$63,922.33** (Picco: **\$81,693.00**)
- **Fatturato Lordo Medio:** **\$90,807.50**
- **Fughe Animali:** **0 (0.0%)**
- **Media Produzione:** 135.00 Latte / 95.67 Lana / 157.17 Meloni / 83.00 Fragole
- **Technical Pass:** **True** (100%)

### Phase C (Semi Holdout: 1838889274, 1619968655, 710418712)
- **Capitale Netto Finale Medio:** **\$66,630.67** (Picco: **\$87,740.00**)
- **Fatturato Lordo Medio:** **\$91,213.33**
- **Fughe Animali:** **0 (0.0%)**
- **Media Produzione:** 138.00 Latte / 96.00 Lana / 157.67 Meloni / 82.17 Fragole
- **Technical Pass:** **True** (100%)

---

## 5. Validazione e Parità Standalone

- **Suite Test Globale:** **209/209 test passati (100%)**
- **Test di Candidatura:** **6/6 passati** ([`tests/test_antigravity_75k_candidate.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_antigravity_75k_candidate.py))
- **Verifica Standalone vs Sorgente:** **100% Bit-Exact Equivalence**
