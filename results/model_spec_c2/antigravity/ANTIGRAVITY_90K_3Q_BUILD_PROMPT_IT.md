# SPECIFICA E PROMPT DI SVILUPPO ANTIGRAVITY C2 90K TRI-QUADRANT (3Q)

> **Modello**: Antigravity C2 Tri-Quadrant (3Q) Lean Cash-Crop Engine  
> **Versione Spec**: `ANTIGRAVITY-C2-TRI-Q0-Q1-Q2-90K-NET-V1.0`  
> **Obiettivo**: Espandere il motore a 3 Quadranti (Q0 NW + Q1 NE + Q2 SW = 75 tile) per massimizzare il Fatturato Lordo (>$110k, 212 meloni) e il Capitale Netto Finale, evitando la trappola salariale esponenziale di Fibonacci.

---

## 1. Prompt di Ingegnerizzazione Strategica

```text
Sei il motore decisionale strategico di Antigravity per la competizione Kaggriculture.
Implementa l'espansione a 3 Quadranti mantenendo il controllo assoluto sui costi salariali:

1. ARCHITETTURA DI ESPANSIONE TERRENI:
   - Q0 (NW: x:0..4, y:0..4): Bootstrap immediato al Day 0 (6 pascoli + 16 colture).
   - Q1 (NE: x:5..9, y:0..4): Sblocco al Day 6 ($1,000) con cashflow residuo >= $1,300 (6 pascoli + 16 colture).
   - Q2 (SW: x:0..4, y:5..9): Sblocco al Day 11 ($2,000) con cashflow residuo >= $2,300 (8 tile cash-crop ad alta resa).

2. GESTIONE DELLA FORZA LAVORO (LEAN 14 WORKERS):
   - W0: Farmer (Market coordinator & logistics).
   - W1..W6: Squadra specializzata Q0 (3 Colture, 2 Zootecnia, 1 Manure).
   - W7..W12: Squadra specializzata Q1 (3 Colture, 2 Zootecnia, 1 Manure).
   - W13 (Hand 12): Specialista dedicato Cash-Crop Q2 (ruolo CROP_ZONE_6).
   - Mantenere esattamente 13 Hands (14 lavoratori) per limitare i salari a $609/giorno senza assumere W14+ ($985+/giorno).

3. ALTA DENSITÀ COLTURALE E ROTAZIONE CHIUSA:
   - Rotazione su 54 slot colturali attivi: 212 Meloni + 86 Fragole raccolti a fine ciclo.
   - Irrigazione e semina sincronizzata a zone chiuse con reimpianto automatico.

4. MANDRIA ZOOTECNICA SIMMETRICA A ZERO FUGHE:
   - 12 Animali attivi: 6 Mucche + 6 Pecore.
   - Protocolli di alimentazione e mungitura/tosatura con 0 Animal Escapes su 720 turni.
```

---

## 2. Layout Spaziale delle Colture e Pascoli 3Q

- **Q0 Pascoli**: `(3,4), (4,3), (3,3), (2,4), (4,2), (3,2)` (3 Mucche, 3 Pecore)
- **Q1 Pascoli**: `(6,4), (5,3), (6,3), (7,4), (5,2), (6,2)` (3 Mucche, 3 Pecore)
- **Q2 Cash-Crop Zone 6**: `(0,5), (1,5), (0,6), (1,6), (0,7), (1,7), (0,8), (1,8)` (6 Meloni, 2 Fragole)
