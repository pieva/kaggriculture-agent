# Prompt & Specification Tecnica: Antigravity C2 Tri-Quadrant (Q0+Q1+Q2) 90K+ Net Candidate

**ID Candidato:** `ANTIGRAVITY-C2-TRI-Q0-Q1-Q2-90K-NET-V1.0`  
**Obiettivo Economico:** **Capitale Netto Finale Medio $\ge \$90,000.00$** (con picco $> \$100,000.00$) e **Zero Fughe di Animali** (`ANIMAL_ESCAPE = 0`).  
**Baseline di Riferimento:** `f391ee2` / `ANTIGRAVITY-C2-DUAL-Q0-Q1-75K-V1.0` (Fatturato Lordo \$91,010.42, Netto Phase C \$66,630.67).  

---

## 1. Visione Architetturale e Razionale Strategico

L'architettura **Antigravity Tri-Quadrant Lean Cash-Crop** introduce un'espansione asimmetrica a 3 quadranti volta a massimizzare l'accumulo di cassa netta senza incorrere nell'esplosione salariale dettata dalla curva di Fibonacci (`_fib(n)`):

```text
QUADRANTE Q0 (NW: x:0..4, y:0..4):
- 6 Pascoli Attivi (3 Mucche + 3 Pecore)
- 8 Slot Colture (6 Meloni + 2 Fragole)
- Shed Access Tile: (4, 4)
- Lavoratori dedicati: W1..W6 (Hands 0..5)

QUADRANTE Q1 (NE: x:5..9, y:0..4) — Sbloccato Day 6-8 ($1,000):
- 6 Pascoli Attivi (3 Mucche + 3 Pecore)
- 8 Slot Colture (6 Meloni + 2 Fragole)
- Shed Access Tile: (5, 4)
- Lavoratori dedicati: W7..W12 (Hands 6..11)

QUADRANTE Q2 (SW: x:0..4, y:5..9) — Sbloccato Day 12-14 ($2,000):
- 0 Animali Aggiuntivi (Evita $4,200 di spesa tardiva e saturazione grano/shed)
- 8 Slot Colture ad Altissimo Rendimento (6 Meloni + 2 Fragole)
- Shed Access Tile: (4, 5)
- Lavoratore dedicato: W13 (Hand 12) per irrigazione e raccolta locale

FORZA LAVORO COMPLESSIVA:
- 14 Operatori (1 Farmer W0 + 13 Hands W1..W13)
- Salario giornaliero controllato: $609 - $986/giorno
- Evitata la barriera salariale dei 18 braccianti ($6,764/giorno)
```

---

## 2. Invarianti e Regole di Gestione Economica

1. **Gating di Liquidità per Q2 (`BUY_LAND` $2,000)**:
   - Sbloccabile solo tra **Day 12** e **Day 14**;
   - Condizione di ammissione: $\text{Cassa Attuale} + \text{Valore Merci in Magazzino} \ge \$3,500.00$;
   - Cassa liquida residua post-acquisto $\ge \$250.00$ per garantire il pagamento dei salari.

2. **Pianificazione Colturale Q2**:
   - **Meloni**: 1 ciclo completo (semina Day 14 $\rightarrow$ maturazione e raccolta Day 26). Resa attesa: $6 \times 12 = 72$ Meloni (\$32,400.00 lordi).
   - **Fragole**: Semina Day 14 $\rightarrow$ primo raccolto Day 18 $\rightarrow$ raccolta continua ogni 2 giorni fino al Day 30 (7 raccolti cumulativi). Resa attesa: $2 \times 14 = 28$ Fragole (\$5,040.00 lordi).

3. **Invarianza Zootecnica e Zero Fughe**:
   - I 12 animali (6 Mucche + 6 Pecore) rimangono tassativamente confinati in Q0 e Q1;
   - Riserva grano fissa di 2 cicli ($2 \times 12 = 24$ unità di grano);
   - Priorità assoluta di alimentazione (`loss_rank = 0`, hard deadline miss = 0).

4. **Shutdown di Fine Partita (Day 28-30)**:
   - Arresto delle semine a partire dal Day 26;
   - Smobilizzo completo di tutte le giacenze (latte, lana, meloni, fragole, grano eccedente, concime) su mercato e botteghe cittadine entro il Turno 720.

---

## 3. Matrice dei Ruoli della Forza Lavoro (14 Operatori)

| ID Operatore | Ruolo Operativo | Quadrante | Incarico Principale |
| :---: | :---: | :---: | :--- |
| **W0** (Farmer) | `RELIEF_LOGISTICS` | Q0/Q1/Q2 | Supporto emergenza, semine critiche, raccolta trans-quadrante |
| **W1** (Hand 0) | `CROP_ZONE_0` | Q0 | 3 Meloni Nord Q0 (`(0,0), (1,0), (2,0)`) |
| **W2** (Hand 1) | `CROP_ZONE_1` | Q0 | 3 Meloni Centro Q0 (`(0,1), (1,1), (2,1)`) |
| **W3** (Hand 2) | `CROP_ZONE_2` | Q0 | 2 Fragole Sud Q0 (`(0,2), (1,2)`) |
| **W4** (Hand 3) | `LIVESTOCK_COW_Q0` | Q0 | 3 Mucche Q0 (`(3,4), (4,3), (3,3)`) |
| **W5** (Hand 4) | `LIVESTOCK_SHEEP_Q0` | Q0 | 3 Pecore Q0 (`(2,4), (4,2), (3,2)`) |
| **W6** (Hand 5) | `FERTILIZER_LOGISTICS_Q0` | Q0 | Raccolta letame e concimazione Q0 |
| **W7** (Hand 6) | `CROP_ZONE_3` | Q1 | 3 Meloni Nord Q1 (`(9,0), (8,0), (7,0)`) |
| **W8** (Hand 7) | `CROP_ZONE_4` | Q1 | 3 Meloni Centro Q1 (`(9,1), (8,1), (7,1)`) |
| **W9** (Hand 8) | `CROP_ZONE_5` | Q1 | 2 Fragole Sud Q1 (`(9,2), (8,2)`) |
| **W10** (Hand 9) | `LIVESTOCK_COW_Q1` | Q1 | 3 Mucche Q1 (`(6,4), (5,3), (6,3)`) |
| **W11** (Hand 10) | `LIVESTOCK_SHEEP_Q1` | Q1 | 3 Pecore Q1 (`(7,4), (5,2), (6,2)`) |
| **W12** (Hand 11) | `FERTILIZER_LOGISTICS_Q1` | Q1 | Raccolta letame e concimazione Q1 |
| **W13** (Hand 12) | `CROP_ZONE_Q2` | Q2 | Gestione e irrigazione 8 colture Q2 (`x in 0..4, y in 7..9`) |
