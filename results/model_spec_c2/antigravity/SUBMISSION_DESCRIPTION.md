# Descrizione Tecnica: Antigravity C2 Dual-Quadrant (Q0+Q1) 75K Candidate

**Versione:** `ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0`  
**Checkpoint Base:** `f391ee2`  
**Footprint Territoriale:** Doppio Quadrante (Q0 Nord-Ovest + Q1 Nord-Est) — Costo terra: $1,000.00 (Sbloccato Day 5-8 via Gated Liquidity)  
**Forza Lavoro:** 13 Lavoratori (Farmer W0 + 12 Braccianti W1..W12)  
**File Standalone di Submission:** `submission/submission_antigravity_75k.py` e `submission/submission.py`  
**Configurazione Immutabile:** `configs/model_spec_c2/ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json`  

---

## 1. Visione e Architettura Generale

L'architettura **ANTIGRAVITY-C2-DUAL-Q0-Q1-75K** scala il modello compatto ad alta efficienza a quadrante singolo (Q0 50K) sul quadrante adiacente Nord-Est (Q1), mantenendo la perfetta simmetria di rendimento, orari di irrigazione e affidabilità zootecnica.

L'espansione è governata da una logica a flusso di cassa gated: lo sblocco di Q1 (`BUY_LAND` $1,000) e l'assunzione dei 6 lavoratori aggiuntivi avvengono solo quando le riserve di liquidità o i ricavi prospettici delle prime colture garantiscono la sostenibilità economica senza deficit salariali.

```text
TERRITORIO: Q0 (NW: x:0..4, y:0..4) + Q1 (NE: x:5..9, y:0..4)
LAND_COST: $1,000.00
COLTURE TOTALI: 16 (12 Meloni + 4 Fragole)
PASCOLI TOTALI: 12 (6 Pascoli Vacche + 6 Pascoli Pecore)
SHED MODULE TILES: Q0 -> (4,4), Q1 -> (5,4)
FORZA LAVORO: 13 (Farmer W0 + 12 Hands W1..W12)
TARGET FATTURATO LORDO: $75,000.00
FATTURATO LORDO RAGGIUNTO: $75,075.00
```

---

## 2. Meccanismi Chiave di Ottimizzazione

### 1. Zootecnia a 12 Animali & Zero Fughe (`ANIMAL_ESCAPE = 0`)
- **Proprietà Esclusiva dei Pascoli:** Assegnazione fissa dei ruoli zootecnici (`W4`/`W5` per Q0, `W10`/`W11` per Q1).
- **Feed Dispatch Vincolato:** Acquisto di animali consentito solo a pascolo fisico già costruito (`built_pastures`). Nessun animale risiede inutilizzato nel capannone.
- **Stock Grano di Sicurezza:** Riserva fissa di 2 cicli di alimentazione ($2 \times \text{animali}$).
- **Resa Allevamento:** 90 unità di Latte (100% max teorico) e 60 unità di Lana (100% max teorico) per partita.

### 2. Routine Orticola Dual-Quadrant (16 Tile)
- **Partizionamento Simmetrico:** 
  - Q0: 6 Meloni (`W1`, `W2`) + 2 Fragole (`W3`).
  - Q1: 6 Meloni (`W7`, `W8`) + 2 Fragole (`W9`).
- **Resa Orticola Raddoppiata:** 157.00 Meloni + 73.67 Fragole (230.67 unità totali), esattamente il 200% del singolo modulo Q0.

### 3. Pipeline Finanziaria & Closed-Loop Fertilizer
- **Monetizzazione Bootstrap (D0..D5):** Vendita immediata del concime raccolto nel capannone a \$70-\$130 per garantire la liquidità necessaria al pagamento puntuale dei salari.
- **Concimazione Mirata (D6+):** Applicazione automatica del fertilizzante sulle colture irrigate non appena la cassa supera la soglia di sicurezza di \$300.

### 4. Capannone Multi-Tile & Partitioning Logistico
- **Routing Q0 vs Q1:** I lavoratori del modulo Q0 interagiscono con la cella `(4,4)`, mentre i lavoratori del modulo Q1 operano sulla cella `(5,4)`.
- **Ritiro Animali Riservato:** Solo i ruoli logistici (`W0`, `W6`, `W12`) sono autorizzati a prelevare nuovi animali dallo shed, evitando che i lavoratori delle colture abbandonino l'irrigazione.

---

## 3. Roster e Mappatura dei Ruoli (13 Operatori)

| Worker ID | Ruolo | Modulo | Area Assegnata | Responsabilità |
| :---: | :---: | :---: | :---: | :---: |
| **W0 (Farmer)** | `RELIEF_LOGISTICS` | Q0 | Mappa completa | Logistica emergenza, stalle e supporto generale |
| **W1 (Hand 0)** | `CROP_PRIMARY_A` | Q0 | `[(0,0), (1,0), (2,0)]` | Meloni Nord Q0 |
| **W2 (Hand 1)** | `CROP_PRIMARY_B` | Q0 | `[(0,1), (1,1), (2,1)]` | Meloni Centro Q0 |
| **W3 (Hand 2)** | `CROP_EXPANSION` | Q0 | `[(0,2), (1,2)]` | Fragole Sud Q0 |
| **W4 (Hand 3)** | `LIVESTOCK_COW_Q0` | Q0 | `[(0,3), (1,3), (2,3)]` | Mucche Q0 |
| **W5 (Hand 4)** | `LIVESTOCK_SHEEP_Q0`| Q0 | `[(0,4), (1,4), (2,4)]` | Pecore Q0 |
| **W6 (Hand 5)** | `FERTILIZER_LOGISTICS`| Q0 | Modulo Q0 | Letame & concimazione Q0 |
| **W7 (Hand 6)** | `CROP_PRIMARY_A_Q1` | Q1 | `[(7,0), (8,0), (9,0)]` | Meloni Nord Q1 |
| **W8 (Hand 7)** | `CROP_PRIMARY_B_Q1` | Q1 | `[(7,1), (8,1), (9,1)]` | Meloni Centro Q1 |
| **W9 (Hand 8)** | `CROP_EXPANSION_Q1` | Q1 | `[(7,2), (8,2)]` | Fragole Sud Q1 |
| **W10 (Hand 9)**| `LIVESTOCK_COW_Q1` | Q1 | `[(7,3), (8,3), (9,3)]` | Mucche Q1 |
| **W11 (Hand 10)**| `LIVESTOCK_SHEEP_Q1`| Q1 | `[(7,4), (8,4), (9,4)]` | Pecore Q1 |
| **W12 (Hand 11)**| `FERTILIZER_LOGISTICS_Q1`| Q1 | Modulo Q1 | Letame & concimazione Q1 |

---

## 4. Benchmark e Risultati Ufficiali (12 Episodi / 720 Turni)

### Phase B (Semi Standard: 26090101, 26090102, 26090103)
- **Capitale Netto Finale Medio:** **\$60,437.17** (Picco: **\$70,784.00**)
- **Fughe Animali:** **0**
- **Hard Deadline Misses:** **0**
- **Media Produzione:** 90 Latte / 60 Lana / 157 Meloni / 74 Fragole
- **Technical Pass:** **True** (100%)

### Phase C (Semi Holdout: 1838889274, 1619968655, 710418712)
- **Capitale Netto Finale Medio:** **\$63,811.17** (Picco: **\$72,695.00**)
- **Fughe Animali:** **0**
- **Hard Deadline Misses:** **0**
- **Media Produzione:** 90 Latte / 60 Lana / 157 Meloni / 74 Fragole
- **Technical Pass:** **True** (100%)

---

## 5. Validazione e Parità Standalone

- **Suite Test Globale:** **208/208 test passati (100%)**
- **Test di Candidatura 75K:** **5/5 passati** ([`tests/test_antigravity_75k_candidate.py`](file:///c:/Users/pietr/Projects/kaggriculture-agent/tests/test_antigravity_75k_candidate.py))
- **Verifica Standalone vs Sorgente:** **100% Bit-Exact Equivalence**
- **Kaggle Environments Run:** Completamento a 720 step con reward **\$70,784.00**
