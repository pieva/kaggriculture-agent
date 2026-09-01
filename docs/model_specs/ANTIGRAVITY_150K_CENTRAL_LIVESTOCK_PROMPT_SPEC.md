# ANTIGRAVITY 150K+ "CENTRAL MEGA-CLUSTER & STRAWBERRY-DOMINANT" SPECIFICATION

> **Riferimento Benchmark**: Replay Kaggle Ufficiale Episodio `104498819` (Seed `562040596`)  
> **Top Competitor**: `keiz` — Capitale Finale Netto: **$158,575.00**  
> **Target Antigravity 150K**: Capitale Finale Netto Medio $\ge \$140,000.00$, Picco $\ge \$155,000.00$, Animal Escapes = 0.

---

## 1. Executive Summary & Forensic Analysis

Dall'analisi forense dissezionata del match `104498819.json` tra `keiz` ($158,575) e la precedente versione di Antigravity ($51,875, ora $83,272 su questo seed), sono emerse le determinanti matematiche del punteggio d'élite:

1. **Predominanza Zootecnica ad Altissima Resa (20 Animali)**:
   - `keiz` non compete principalmente sulle colture ma schiera **20 animali attivi**: 8-9 Mucche, 11 Pecore, 1 Oca.
   - Rese record: **261 Lana** ($62.6k) + **242 Latte** ($38.7k) + **351 Concime venduto** ($14.0k) + **21 Uova** ($1.0k) = **$116,340.00** di solo fatturato zootecnico.
2. **Geometria a Mega-Cluster Centrale (Adiacenza al Capanno)**:
   - I 20 pascoli sono costruiti tutti al centro della mappa (`x=2..7, y=1..7`) a ridosso dell'intersezione dei tre quadranti (`(4,4)`, `(5,4)`, `(4,5)`).
   - Distanza di routing tra capanno, stalle e animali = 0 o 1 passo. Azzeramento dei tempi morti di trasporto.
3. **Rivoluzione Colturale: "Strawberry-Dominant" vs "Melon-Heavy"**:
   - `keiz` alloca **38 tile a Fragola (`ST`)**, **9 tile a Grano (`WH`)** e solo **8 tile a Melone (`ME`)**.
   - La Fragola (`ongoing: True`) produce 4 unità ogni 2 giorni senza mai morire: fino a 10 cicli di raccolta (40+ fragole per pianta) a costo di risemina e lavorazione pari a ZERO.
4. **Autosufficienza Alimentare (Local Wheat Farming)**:
   - 9 tile di Grano autoprodotto generano 54 unità di foraggio ogni 4 giorni a un costo seme di $10 ($1.67/unità), sostituendo gli acquisti di mercato a $25.00 (-93% costi vivi).
5. **Monetizzazione Sistematica del Concime**:
   - Vendita continua di tutto il concime prodotto (351 unità vendute a ~$40 l'una = $14,040.00 liquidità netta).
6. **Efficienza Salariale Rigida (12 Hands / 13 Operai)**:
   - `keiz` mantiene esattamente 12 hands (13 lavoratori con il farmer), fermandosi prima dell'esplosione salariale del 14° e 15° lavoratore ($376/giorno contro $609+/giorno).

---

## 2. Architettura del Mega-Cluster Centrale

### 2.1 Coordinate dei 20 Pascoli Centrali
Tutti i pascoli risiedono nella corona centrale a ridosso dei 3 capanni di quadrante:
- **Modulo Q0 (NW)**: `(4,3), (4,2), (3,3), (3,4), (2,4), (3,2)` (4 Mucche, 2 Pecore)
- **Modulo Q1 (NE)**: `(5,2), (6,2), (5,3), (6,3), (5,4), (6,4), (7,4)` (4 Mucche, 3 Pecore)
- **Modulo Q2 (SW)**: `(3,5), (4,5), (3,6), (4,6), (4,7), (5,5)` + `(4,1)` Oca (1 Oca, 6-7 Pecore)

### 2.2 Piano Colturale ad Alta Frequenza (Strawberry-Dominant)
- **Fragole (36-38 tile)**: collocate sui tile intermedi dei 3 quadranti. Semina scaglionata Day 1-3 (Q0), Day 7-8 (Q1), Day 12-13 (Q2). Produzione ininterrotta ogni 48 ore fino al Day 30.
- **Grano (8-9 tile)**: rotazione rapida (4 giorni) per alimentare a costo zero la mandria.
- **Meloni (6-8 tile)**: concentrati solo nei primi 6 slot di Q0 piantati a Day 0 e raccolti a Day 12.

---

## 3. Ripartizione dei 13 Ruoli Operativi (12 Hands)

1. **W0 (Farmer - Relief & Center Logistics)**: coordinamento centrale a `(4,4)`, supporto semine e alimentazione mandria.
2. **W1..W3 (Crop Specialists Q0)**: gestione delle fragole e grano di Q0.
3. **W4..W6 (Livestock Specialists Q0)**: mungitura 4 mucche, tosatura 2 pecore, deposito latte/lana/concime nel capanno `(4,4)`.
4. **W7..W9 (Crop Specialists Q1)**: gestione delle fragole e grano di Q1.
5. **W10..W12 (Livestock Specialists Q1)**: gestione 4 mucche e 3 pecore di Q1, deposito nel capanno `(5,4)`.
6. **W13 (Multi-Disciplinary Sheep & Q2 Specialist)**: gestione delle 7 pecore di Q2 e raccolta foraggio grano, deposito nel capanno `(4,5)`.

---

## 4. Benchmark e Target di Convalida

- **Ambiente**: 12 episodi ufficiali (Phase B e Phase C Holdout) su motore Kaggriculture 720 turni.
- **KPI Economici**:
  - Capitale Netto Finale Medio $\ge \$130,000.00$
  - Picco Massimo $\ge \$150,000.00$
  - Lana venduta $\ge 200$ unità
  - Latte venduto $\ge 200$ unità
  - Fragole vendute $\ge 180$ unità
  - Concime venduto $\ge 250$ unità
  - Animal Escapes = 0 (Zero tolleranza)
