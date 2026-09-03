# E17 — Sintesi parametrica Top 3 (tetsuya / OceanMix / Crop Dusta) per il piano statico V4

- **Data:** 2026-09-02
- **Fonte primaria:** `experiments/e17/reports/common/E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`
  (riconciliazione cross-agent Antigravity/Copilot/Codex, 9 replay, `ACCEPT`/`ACCEPT_WITH_CHANGES`, chiusa)
- **Scopo:** estrarre i parametri medi osservati sui tre top player come base
  per il "piano statico" V4 (target architetturale prima di renderlo
  reattivo), invece del mio ricalcolo indipendente e più grezzo dai soli
  replay JSON (che non aveva timing di sblocco, traiettoria di cassa per
  giorno, né topologia per quadrante).
- **Avvertenza esplicita ereditata dalla fonte:** "3Q e picco 12 hands sono
  configurazioni comuni osservate, non ottimi dimostrati." Le tre
  architetture sono **distinte**, non varianti dello stesso profilo —
  vedi Sezione 3.

---

## 1. Tabella di sintesi — parametri medi

| Parametro | tetsuya | OceanMix | Crop Dusta | **Media Top3** | Claude V3 (nostro, conteso) |
|---|---:|---:|---:|---:|---:|
| Sblocco Q1 (giorno) | D7 | D6 | D5,4 | **D6,1** | non misurato per giorno |
| Sblocco Q2/SW (giorno) | D10 | D11 | D8,2 | **D9,7** | non misurato per giorno |
| Terzo quadrante extra (Q3) | mai | mai | mai | **mai** | mai (per costruzione, `target_quadrants=3`) |
| Peak hands | 12 | 12 | 12 | **12** | 8 (terminale) |
| Peak crop medio (tile) | 58,0 | 61,0 | 60,6 | **59,9** | non confrontabile (terminale contaminato da liquidazione) |
| Peak animali medio | 15,0 | 14,25 | 16,8 | **15,35** | 4,36 (terminale) |
| Denaro finale medio | 96.568 | 82.535 | 91.361 | **90.155** | 13.541 |
| MOVE / azioni produttive | 1,2553 | 1,0468 | 1,4267 | **1,243** | ~2,18 (68,6% MOVE ⇒ rapporto MOVE/produttivo ≈ 0,686/0,183 — non direttamente comparabile, metriche diverse, vedi Sezione 4) |
| Specie crop usate | 4 | 4 | 5 | **4,3** | 4 (WHEAT/CARROT/MELON/TOMATO) |
| Specie animali usate | 3 | 2 | 3 | **2,7** | 3 (SHEEP/COW/GOOSE, mai tutte piazzate insieme) |
| Fughe derivate (criterio EOD) | 0 | 0 | 31 | 10,3 (mediana 0) | 18 (su 14 run, non 1 solo episodio) |
| Inventario finale invenduto medio | 0 | 35,5 | 373 | 136,2 | non misurato |

**Lettura per il piano statico:** il target architetturale più difendibile
non è la media aritmetica dei tre (che mischia archetipi incompatibili fra
loro), ma un **profilo scelto esplicitamente**, perché la fonte mostra che
`hands=12` e `3Q` sono comuni ai tre ma la **topologia zootecnica** e il
**timing** sono le variabili che li differenziano e li rendono
economicamente competitivi in modi diversi (Sezione 3).

---

## 2. Traiettoria di cassa per giorno (media per episodio)

| Giorno | tetsuya | OceanMix | Crop Dusta |
|---|---:|---:|---:|
| D5 | n/d | n/d | 131 |
| D10 | 871,75 | 15.820,75 | 7.073 |
| D15 | 13.898 | 26.126 | 19.369 |
| D20 | 52.483 | 49.138 | n/d |
| D29 (finale) | 96.568 | 82.535 | 91.361 |

**Osservazione diretta per la diagnosi già fatta in questa sessione:**
`tetsuya` ha cassa **quasi nulla a D10** (871,75, range 452–1.174) — un
profilo di reinvestimento aggressivo, non di riserva liquida — eppure NON
collassa, a differenza dei nostri tentativi V4 che con cassa bassa sono
collassati ripetutamente. La differenza non è "quanta cassa tenere di
riserva" in astratto, ma la **sequenza esatta e la taglia degli impegni di
spesa** (nessun costo Fibonacci-per-hand ricorrente di questa scala nella
loro architettura, o un ritmo di crescita della workforce molto più
graduale di un salto a 11-12 in poche chiamate). `OceanMix` all'opposto
mantiene una riserva molto più alta a D10 (15.820,75) prima di aprire Q2 —
un profilo prudente. Questi sono due modi opposti e ENTRAMBI validi di
gestire la stessa cassa iniziale: non esiste un singolo "livello di
riserva corretto" indipendente dall'architettura complessiva.

---

## 3. Tre architetture distinte, non un unico target

| Archetipo | Bestiame | Q2/SW | Rapporto MOVE/produttive | Rischio |
|---|---|---|---|---|
| **tetsuya** — 3Q distribuito | Distribuito su tutti e 3 i quadranti (7/2,25/5,75 finale) | D10, modulo misto da subito | 1,2553 (medio) | Basso: 0 fughe, inventario finale 0 |
| **OceanMix** — spina compatta | Concentrato solo in Q0/Q1 (~7 ciascuno); Q2 **esclusivamente colturale** (25 crop, 0 animali) | D11, il più tardo | **1,0468 (migliore)** | Basso: 0 fughe, minor travel assoluto |
| **Crop Dusta** — espansione anticipata | Misto in tutti e 3 i quadranti, ma diluito e fragile (3,6/4/3 finale) | **D8,2 (il più precoce)** | 1,4267 (peggiore) | **Alto: 31 fughe, 373 invenduto** |

Questo è il motivo per cui la Sezione 9 della fonte raccomanda di
**separare le variabili** (timing Q2, topologia zootecnica, diversificazione,
chiusura) e testarle causalmente una alla volta, non di copiare un profilo
intero. Per il nostro piano statico V4, i due candidati **sicuri** (zero
fughe in entrambi) sono:

- **Profilo "distribuito" (tetsuya):** bestiame su tutti i quadranti,
  Q2 a D10, reinvestimento aggressivo con cassa minima.
- **Profilo "spina compatta" (OceanMix)":** bestiame concentrato in
  Q0/Q1, Q2 crop-only, riserva di cassa più alta, minor travel.

`Crop Dusta` (Q2 a D8) è il più aggressivo sul timing ma il meno
`serviceable`: **non raccomandato come primo target** vista la nostra
storia recente di collassi da sovra-estensione.

---

## 4. Topologia per quadrante nel tempo (crop `C` / animali `A` / inattive `I`, su 25 tile/quadrante)

| Agente | Giorno | Q0 | Q1 | Q2 |
|---|---|---|---|---|
| tetsuya | D10 | C18/A7/I0 | C22,75/A2,25/I0 | C15/A1,75/I8,25 |
| tetsuya | D15 | C18/A7/I0 | C22,75/A2,25/I0 | C17,25/A5,75/I2 |
| tetsuya | D29 | C1/A7/I17 | C3,5/A2,25/I19,25 | C0,25/A5,75/I19 |
| OceanMix | D10 | C14,75/A6,75/I3,5 | C18/A7/I0 | locked |
| OceanMix | D15 | C17,75/A7,25/I0 | C17,75/A7/I0,25 | C25/A0/I0 |
| OceanMix | D29 | C0/A7,25/I17,75 | C0/A7/I18 | C0/A0/I25 |
| Crop Dusta | D10 | C17,4/A6,4/I1,2 | C20,4/A4/I0,6 | C20,4/A1,4/I3,2 |
| Crop Dusta | D15 | C17,8/A7,2/I0 | C18,8/A5,6/I0,6 | C20,8/A2,8/I1,4 |
| Crop Dusta | D29 | C1,4/A3,6/I20 | C1,2/A4/I19,8 | C1,4/A3/I20,6 |

**D29 rappresenta la fase di liquidazione**, non la densità stagionale — i
valori `C` crollano ovunque a fine partita, esattamente come osservato nel
nostro stesso `crop_tiles_final≈1,00` (Sezione 1.1 del piano V4). Questo
conferma che il confronto corretto per la densità coltivata va fatto su
D10/D15, non sul dato terminale — un'accortezza metodologica che avevamo
già dedotto empiricamente ma che qui è confermata su un corpus esterno
indipendente.

---

## 5. Implicazioni dirette per il piano statico V4

1. **Target hands = 12, non 15 e non un salto immediato.** Tutti e tre i
   top raggiungono lo stesso picco (12); nessuno lo supera. Il nostro
   tentativo di puntare a 11 immediatamente da D0 ha ricreato la trappola
   di cassa. I top lo raggiungono presumibilmente in modo graduale — non
   abbiamo ancora la cadenza esatta giorno-per-giorno del loro `hands`
   (solo il picco), quindi questo resta da inferire o testare.
2. **Target animali = 14-17 (media 15,35), non 19-20.** Il nostro
   precedente riferimento a Codex V9 (19 animali) è il **valore più alto
   del confronto**, non il tipico. I tre top competitivi usano 14-17.
3. **Timing Q2 = D9-D10 per i profili sicuri** (tetsuya D10, OceanMix
   D11); D8 (Crop Dusta) è il profilo fragile e va evitato come primo
   target.
4. **Scegliere esplicitamente un archetipo prima di implementare**, non
   una media: raccomando **OceanMix (spina compatta)** come primo target
   statico, perché ha il miglior rapporto MOVE/produttive (1,0468, il più
   efficiente in assoluto) e zero fughe con la topologia più semplice da
   replicare (bestiame confinato a 2 quadranti, esattamente come il nostro
   `max_quadrants_for_livestock=2` già fa) — il minor numero di variabili
   nuove da introdurre rispetto alla V3 già stabile.
5. **La cassa "di riserva" non è un numero universale**: va dimensionata
   in funzione della cadenza di spesa complessiva dell'archetipo scelto,
   non tarata isolatamente come abbiamo fatto finora.

Questa sintesi sostituisce, come riferimento quantitativo per il piano
statico, il mio calcolo indipendente sui replay grezzi (che mancava di
timing di sblocco e traiettoria di cassa) riportato nella conversazione
precedente a questo documento.
