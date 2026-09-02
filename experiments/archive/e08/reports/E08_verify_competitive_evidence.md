# VERIFY Report — E08 Competitive Evidence Synthesis (`E08-04 / V3`)

**Date:** 2026-08-26  
**Phase:** VERIFY (Phase V3 — Competitive Evidence Synthesis)  
**Status:** `VERIFY COMPLETED`  
**Decision Proposal for REVIEW:** **`ROLLBACK E08 SCALE — STRATEGIC RECONSTRUCTION FOR E09`**  

---

## 1. Synthesis Answers to Core Experimental Questions

### Q1. L'aumento da 24 a 40 tile ha corretto il principale limite osservato in E07?
**NO.** Sebbene l'intento fosse quello di sfruttare il terreno acquistato in Q1, aumentare nominalmente le tile a 40 ha **peggiorato la prestazione economica** (-10.81% vs E07, -$1,440.07 Mean Final Money). La causa principale è l'effetto di diluizione geografica dei lavoratori.

### Q2. Le 40 tile vengono realmente sfruttate?
**NO.** La telemetria mostra che la media giornaliera di tile coltive attive è di sole **13.84 tile/giorno** (su 40 configurate), con un picco medio di **22.93 tile**. Oltre il 42% delle 40 tile configurate è rimasto non seminato per mancanza di turni produttivi.

### Q3. La workforce di 4 worker è ancora sufficiente per 40 tile + pascoli?
**NO.** Con 4 worker (1 Farmer + 3 Hands) responsabili contemporaneamente di:
- 5 pascoli (gestione mucche/pecore, alimentazione quotidiana con grano, mungitura/tosatura);
- 40 tile coltive distribuite su 50 tile totali (Q0+Q1);
- viaggi verso lo shed (4,4) e il mercato;  
i lavoratori accumulano un **movement share del 61.6%** (1,234 turni di spostamento su 2,002 totali).

### Q4. Lo spatial partitioning riduce il costo operativo o introduce nuovi colli di bottiglia?
Lo spatial partitioning ha evitato collisioni e viaggi incoerenti, ma la presenza del **Cross-Boundary Water Assist** e la necessità di alimentare gli animali in Q0 hanno costretto i lavoratori a frequenti traversate cross-boundary per evitare perdite per erbacce (WEED), vanificando il risparmio nei movimenti.

### Q5. Lo staggered purchasing limita l'espansione?
Lo staggered purchasing ha svolto correttamente la sua funzione di protezione (prevenendo il fallimento della cassa), ma la spesa totale in sementi (**$3,978.00**) ha drenato capitale liquido senza che i raccolti di Meloni venissero completati in tempo prima della fine del gioco.

### Q6. Quanto gap E07→E06 è stato recuperato?
**-12.34%.** Il gap non solo non è stato recuperato, ma si è **ampliato di $1,440.07** rispetto a E07 e di **$13,107.37** rispetto ad E06 ($24,987.67).

### Q7. Qual è il principale collo di bottiglia rimasto dopo E08?
Il collo di bottiglia dominante è la **bassa produttività netta dell'allevamento/pascoli in E07/E08** unita alla **dispersione geografica del footprint**:
1. L'allevamento (4 Mucche, 2 Pecore, 5 pascoli) consuma ~40% dei turni totali dei lavoratori ed il grano prodotto, ma genera entrate marginali.
2. In E06, l'agente senza allevamento concentrava 2 lavoratori su 9 tile di Meloni ad altissima densità (scadenza irrigazione rapida, zero movimenti inutili), generando **$24,987.67**.

### Q8. Le evidenze supportano il mantenimento di E08, un'ottimizzazione incrementale E09, o un rollback/variante?
Le evidenze supportano un **ROLLBACK della scala a 40 tile** e raccomandano per E09 una **Ristrutturazione Strategica Focalizzata sull'Alto ROI**:
- Eliminare o ridimensionare drasticamente l'allevamento a bassa resa.
- Re-focalizzare la forza lavoro su una griglia coltiva ultra-densa di Meloni/Carote ad altissimo ROI, riducendo al minimo i tempi di spostamento.

---

## 2. Quantitative Summary Matrix (E05 vs E06 vs E07 vs E08)

| Metric | E05 Multi-Worker | E06 Water-First | E07 Competitive | E08 Productive Scale | Delta E08 vs E07 | Delta E08 vs E06 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Strategy Class** | `HIRENWCluster` | `WaterFirstHIRENW` | `HybridLivestock` | `HybridLivestock` | — | — |
| **Configured Tiles** | 9 tiles | 9 tiles | 24 tiles | **40 tiles** | +16 tiles | +31 tiles |
| **Workers** | 2 workers | 2 workers | 4 workers | **4 workers** | 0 | +2 workers |
| **Mean Final Money** | **$21,480.87** | **$24,987.67** | **$13,320.37** | **$11,880.30** | **-$1,440.07 (-10.8%)** | **-$13,107.37 (-52.5%)** |
| **Median Money** | $21,442.00 | $25,847.00 | $10,262.00 | **$9,790.50** | **-$471.50 (-4.6%)** | **-$16,056.50** |
| **Movement Share** | ~35.0% | ~32.0% | 54.2% | **61.6%** | +7.4% | +29.6% |
| **Plant Pending Backlog** | Low | Low | 14.9/day | **18.0/day** | +3.1/day | High |
| **Win Rate vs Opponents** | 100.0% | 100.0% | 93.3% | **93.3%** | 0.0% | -6.7% |

---

## 3. Proposal for REVIEW Phase

- **Status Proposal:** **`VERIFY FAIL — GO FOR REVIEW`**
- **Recommendation for E09:** Abandon the 40-tile spatial dilution model. Design **E09 Crop ROI Concentration & Livestock Streamlining** to eliminate structural workforce friction and recover the competitive performance level of E06 ($25,000+).

---

<!-- END OF DOCUMENT -->
