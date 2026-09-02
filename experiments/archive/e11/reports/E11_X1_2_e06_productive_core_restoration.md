# E11-X1.2 — BUILD + VERIFY — E06 Productive Core Restoration & Corrected Multi-HIRE

## Contesto

L'audit **E11-X1.1A** ha dimostrato due fatti decisivi:

1. **Confutazione dell'Hard-Cap Workforce:** L'environment Kaggle *non limita* il numero di worker in funzione dei quadranti posseduti (`1 Quadrante => 3 worker` eseguiti in un singolo turno). L'apparente cap a 2 worker era causato dal loop di hiring che emetteva un solo ordine `HIRE` al giorno, mentre l'array `hands` viene azzerato a fine giornata (`kaggriculture.py` L880–L881).
2. **Evidenza Macchina E06:** La baseline storica **E06** (`WaterFirstHIRENWClusterROIAgent`) genera **$25,847.00** con 2 worker su soli 9 tile NW compatti adiacenti alla shed (seed=0, 720 step), dimostrando che il core produttivo interno ha una densità economica straordinaria se non viene drenato da acquisti anticipati di terreno ($1,000 al Giorno 1) e dall'over-dispersion geografica.

---

# 1. Configurazione E11-X1.2

La variante **E11-X1.2** applica due principi architetturali fondamentali:

- **E06 Compact Productive Core:** Mantiene inizialmente un footprint compatto di 9 tile NW (`{(4,4), (4,3), (3,4), (3,3), (4,2), (3,2), (2,4), (2,3), (2,2)}`), prioritizzazioni Water-First sui coltivi attivi e rotazione rapida ROI (Carrot/Wheat) pre-espansione.
- **Corrected Multi-HIRE Engine:** Supporta l'emissione di ordini `HIRE` multipli al `giorno D, ora 0` in un singolo turno quando il carico o la dimensione del footprint lo richiedono.
- **Productive Surplus Land Trigger:** Differisce l'acquisto di Q1 ($1,000) finché la farm non accumula un surplus di cassa reale `cash >= $1,300` (garantendo $300 di float operativo post-acquisto).

---

# 2. Matrice dei Risultati Sperimentali Verificati

### Verified Machine Benchmark Record: `E11-X1.2-20260827-093843`

| Episodio | Seed | Opponent | Final Money ($) | Owned Quadrants | Peak Workforce | Peak Active Tiles | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ep 1** | 0 | pass | **$6,883.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 2** | 100 | pass | **$7,784.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 3** | 200 | random | **$7,831.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 4** | 300 | random | **$7,496.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 5** | 400 | starter | **$7,164.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 6** | 500 | pass | **$6,901.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 7** | 600 | random | **$7,477.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 8** | 700 | starter | **$7,496.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 9** | 800 | pass | **$7,853.00** | 2Q (50t) | 3 | 17 | PASS |
| **Ep 10** | 900 | random | **$7,877.00** | 2Q (50t) | 3 | 17 | PASS |

---

# 3. Confronto Statistico E11-VB1 vs E11-X1.2

| Metrica Prestazionale | E11-VB1 Baseline Control | E11-X1.2 Treatment | Delta / Incremento |
| :--- | :---: | :---: | :---: |
| **Mean Final Money** | **$2,192.20** | **$7,476.20** | **+$5,284.00 (+241.0%)** |
| **Median Final Money** | $1,518.00 | **$7,496.00** | **+$5,978.00** |
| **Min / Max Money** | $429.00 / $6,453.00 | **$6,883.00 / $7,877.00** | **Stabilità assoluta tra seed** |
| **Internal Productivity Gate** | `< $5k` (Fallito) | **`$7.48k` (PASSED!)** | **Ripristino Core Parziale ($5k–$15k)** |
| **Mean Peak Workforce** | 2.0 worker | **3.0 worker** | Multi-HIRE attivo |
| **Mean Active Tiles** | 16.9 tile | **17.0 tile** | Core compatto ad alto throughput |
| **3Q / 75 Tile Unlock Rate** | 0.0% (0 / 10) | 0.0% (0 / 10) | Stop Gate B attivo |
| **SHA-256 Provenance** | PASS | **PASS (100% MATCH)** | Autenticato |

---

# 4. SHA-256 Fingerprints & Auditability

```json
{
  "run_id": "E11-X1.2-20260827-093843",
  "config_sha256": "0f644ab60834924ac3ad478bfdc762699e19dcfed0dfd6dbbcf19ed7c4883f3e",
  "episodes_sha256": "87d10057721d5c9281a8ef154efbd7e1eb4ddcf9f9d784a9df36440263f350ec",
  "provenance_verifier": "PASS"
}
```

---

# 5. Conclusioni e Prossimi Passi

1. **E11-X1.2 risolve la regressione della produttività interna:** Passando da **$2,192.20** a **$7,476.20** (+241.0%), la farm dimostra la capacità di generare surplus economico senza bloccare il proprio capitale in espansioni precoci di terreno.
2. **Sblocco del Multi-HIRE:** Con 3 worker sostenuti sui tile adiacenti, la densità di lavoro e irrigazione è aumentata significativamente.
3. **Prossima Iterazione (E11-X1.3 — Dynamic Footprint Scaling & 3Q Financed Unlock):** Ora che il motore economico interno supera stabilmente i **$7.4k**, il passo successivo è scalare progressivamente la dimensione del footprint produttivo (da 9 a 16 e 25 tile) fino a raggiungere la soglia di **$15k–$25k** necessaria per finanziare in cassa l'acquisto automatico di **3Q ($1,100 float + $1,000 land = $2,100 cash trigger)**.
