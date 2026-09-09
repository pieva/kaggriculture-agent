# MODEL_SPEC Antigravity E19.1 — Hybrid Livestock V1

```text
AGENT_OWNER: ANTIGRAVITY
MODEL: Antigravity E19.1 Hybrid Livestock V1
VERSION: ANTIGRAVITY-E19.1-HYBRID-LIVESTOCK-V1
CANDIDATE_ID: ANTIGRAVITY_E19_1_HYBRID_LIVESTOCK_V1
STATUS: DEVELOPMENT_CANDIDATE (Unfreezing line from FROZEN_PERFORMANCE_GAP)
ROUND: E19
FOUNDATION_BASELINE: C2.1 reconciled
ENGINE: kaggle-environments 1.32.7, kaggriculture 0.1.0
IMPLEMENTATION_RUNTIME:
  - src/agricola/strategy/antigravity/antigravity_e19_hybrid_livestock_v1.py
CONFIG_FILE:
  - docs/model_specs/antigravity/configs/ANTIGRAVITY_E19_1_HYBRID_LIVESTOCK_V1.json
```

---

## 1. Obiettivo e ipotesi

### 1.1 Risultato perseguito
L'obiettivo di **Antigravity E19.1 Hybrid Livestock V1** è superare definitivamente il tetto economico asintotico delle sole colture ($10.000–$15.000), colmando il divario prestazionale con Codex attraverso l'introduzione di un **motore zootecnico causale ad alto margine** (`COW`, `SHEEP`, `MILK`, `WOOL`, `FERTILIZER`) integrato con colture cash ad alto rendimento (`MELON`, `WHEAT`), pur preservando:
1. **Piena autonomia e causalità decisionale**: zero dipendenze da replay open-loop statici o routine preconfezionate (a differenza di Codex V9 a 719 step o V48 assistita fino a D11). Ogni decisione è calcolata online a partire dallo stato osservato via `CodexObservationAdapter`.
2. **On-Tile Capacity Governor proprietario**: estensione dell'overlay E18.2 per intercettare qualsiasi lavoratore in movimento o in attesa su celle con compiti insoddisfatti (alimentazione bestiame, mungitura, diserbo, irrigazione, raccolta), convertendo lo step in lavoro produttivo a spostamento zero.
3. **Garanzia di zero fughe (*Zero-Escape Feed Loop*)**: coordinamento rigoroso tra produzione di grano, stock nello shed e alimentazione quotidiana per azzerare le penalizzazioni da abbandono animale.

### 1.2 Ambito e contesto operativo
- **Orizzonte temporale**: 30 giorni di simulazione, 24 turni orari per giorno (720 step complessivi).
- **Topologia operativa**: gestione a due quadranti principali (Q0 Nord-Ovest, Q1 Nord-Est sbloccato a D5 con $1.400) con espansione opzionale in Q2 (Sud-Ovest).
- **Cluster zootecnico compatto**: 6 pascoli posizionati nelle immediate adiacenze della capanna centrale `(4, 4)` (distanza Manhattan $\le 3$: celle `(3, 3), (3, 4), (4, 3)` in Q0 e `(5, 4), (5, 3), (6, 3)` in Q1), minimizzando i tempi di transito logistico.
- **Portafoglio biologico**:
  - Bestiame: target nominale di 4 `COW` (produzione `MILK` a prezzo base $160 ogni 2 giorni) e 2 `SHEEP` (produzione `WOOL` a base $200 ogni 3 giorni).
  - Colture: `WHEAT` (foraggio vitale per bestiame e cassa costante, ciclo 2-4 giorni), `CARROT` (liquidità iniziale D0-D5), `MELON` (cash crop principale D6-D18 a base $250).

### 1.3 Risoluzione del divario e stato della linea
La linea Antigravity, posta in `FROZEN_PERFORMANCE_GAP` il 2026-09-04 a causa della saturazione economica del modello *crop-only* (media ~$11.300), viene formalmente **riaperta e scongelata** come **Candidate E19.1**. L'introduzione della zootecnia ad alto margine e delle colture da reddito fornisce la leva causale necessaria a scalare oltre i $40.000–$60.000.

---

## 2. Strategia

### 2.1 Topologia del Cluster Zootecnico Centrale
Per evitare l'errore storico di dispersione su grandi distanze Manhattan, i pascoli sono raggruppati in un cluster compresso:
- **Pascoli Q0**: `(3, 3)`, `(3, 4)`, `(4, 3)`.
- **Pascoli Q1**: `(5, 4)`, `(5, 3)`, `(6, 3)`.
Tutti i pascoli risiedono a distanza Manhattan di 1-3 celle dallo shed `(4, 4)`. Questa vicinanza garantisce che le operazioni di prelievo foraggio (`PICKUP WHEAT`) e somministrazione (`FEED`), nonché il deposito del latte/lana (`DROP`), richiedano un tempo di trasferimento quasi nullo.

### 2.2 Motore Zootecnico e Ciclo di Vita degli Animali
1. **Costruzione pascoli (`BUILD_PASTURE`)**: il caposquadra (*Farmer*), quando non impegnato in compiti prioritari e disponendo di terreno libero nelle coordinate del cluster, costruisce i pascoli previsti.
2. **Approvvigionamento bestiame (`BUY_ANIMAL`)**: il mercato acquista mucche e pecore solo se:
   - Esistono pascoli costruiti non ancora occupati.
   - Lo stock di grano (`shed.WHEAT` + sementi) supera il fabbisogno giornaliero sommato al buffer di sicurezza ($\ge \text{animali} + 4$).
   - La liquidità residua dopo l'acquisto rispetta la riserva inviolabile di $300,00.
3. **Insediamento animale (`PICKUP` + `PLACE`)**: il Farmer preleva l'animale depositato nello shed e si reca sul pascolo libero per eseguire l'azione `PLACE`.
4. **Mungitura e tosatura (`HARVEST`)**: non appena un animale accumula prodotto (`yield_units > 0`), qualsiasi lavoratore libero prioritariamente raggiunge la cella ed esegue `HARVEST`.
5. **Cura e fertilizzante (`CARE`, `COLLECT_FERTILIZER`)**: gli animali curati incrementano la qualità della resa; il fertilizzante viene raccolto e monetizzato.

### 2.3 Protocollo Alimentare a Zero Fughe (*Zero-Escape Feed Protocol*)
L'engine determina la fuga di un animale al secondo fine giornata (`EOD`) consecutivo senza alimentazione. Per prevenire qualsiasi fuga con certezza matematica:
- **Priorità Assoluta 0**: ogni giorno, tutti gli animali con `fed_today == False` generano un task `FEED` a priorità massima.
- **Logistica di prelievo**: i lavoratori verificano il proprio inventario; se sprovvisti di grano, fanno scalo immediato allo shed `(4, 4)` per eseguire `["PICKUP", "WHEAT", 3]` prima di convergere sull'animale.
- **Acquisto di emergenza**: se per fluttuazioni di resa il grano nello shed scende sotto il fabbisogno giornaliero, il modulo di mercato emette ordini immediati di `BUY_PRODUCT WHEAT`.

### 2.4 Portafoglio Colturale e Calendario a 3 Fasi
- **Fase 1: Avvio e Liquidità Veloce (D0–D5)**:
  - Concentrata su Q0: rotazione rapida di Carote e Grano per alimentare la cassa iniziale, sostenere le assunzioni a costo Fibonacci e raggiungere $1.400 per sbloccare Q1.
- **Fase 2: Insediamento Zootecnico e Colture da Reddito (D6–D18)**:
  - Sblocco Q1, insediamento cluster pascoli e acquisto progressivo di mucche e pecore.
  - Assegnazione dei campi liberi di Q1 a Meloni (`MELON`, maturazione a giorno 12, prezzo $250) e Grano per foraggio.
- **Fase 3: Regime Produttivo e Monetizzazione (D19–D26)**:
  - Stop acquisto animali a D20. Mungitura e tosatura continue.
  - Sospensione semina meloni a D18; transizione a grano e carote veloci.
- **Fase 4: Chiusura e Liquidazione Terminale (D27–D30)**:
  - Stop a qualsiasi semina e acquisto fondiario.
  - Svuotamento completo dello shed: vendita incondizionata (`SELL`) di ogni unità di latte, lana, melone, carota, fertilizzante e grano residuo.
  - Raccolta di tutti i prodotti rimasti sui campi prima del turno 720.

### 2.5 Governance Finanziaria e della Forza Lavoro
- **Riserva di cassa (*Cash Floor*) di $300,00**: nessuna spesa facoltativa (terra, animali, semi extra) può ridurre la cassa al di sotto di questa soglia, salvaguardando le assunzioni quotidiane e il mangime.
- **Assunzioni a costo di Fibonacci a Ora 0**: la squadra scala fino a 4-6 braccianti in base alla presenza di animali e compiti inevasi.

---

## 3. Decisioni implementate e Architettura On-Tile

### 3.1 Feature utilizzate (Foundation C2.1)
Le decisioni si basano sulle feature estratte da `CodexObservationAdapter`:
- `clock.day`, `clock.hour`
- `farm.money`, `farm.tiles[y][x]` (`kind`, `animal`, `fed_today`, `yield_units`, `crop`, `planted_day`, `watered_today`, `fertilizer_available`)
- `farm.unlocked_quadrants`, `farm.farmer`, `farm.hands`
- `private.shed`, `private.seeds`, `private.inventories`

### 3.2 Upgraded On-Tile Capacity Governor
L'algoritmo controlla ogni lavoratore la cui azione prevista sia uno spostamento (`MOVE_OPCODES`: `PASS`, `NORTH`, `SOUTH`, `EAST`, `WEST`). Se il lavoratore si trova su una cella con un compito utile non conteso e il suo carico è < 2 unità:
1. Se la cella ospita un animale non sfamato e il lavoratore ha grano nello zaino: esegue `["FEED"]`.
2. Se la cella ha prodotto animale o vegetale maturo: esegue `["HARVEST"]`.
3. Se la cella ha fertilizzante disponibile: esegue `["COLLECT_FERTILIZER"]`.
4. Se la cella ha un'erbaccia: esegue `["DIG"]`.
5. Se la cella ha una pianta in crescita non irrigata: esegue `["WATER"]`.
6. Se la cella ospita un animale non curato: esegue `["CARE"]`.

Questo recupero è a **costo di spostamento rigorosamente nullo** ($\Delta x + \Delta y = 0$), garantendo un recupero sistematico di efficienza operativa.

---

## 4. Evidenza dei Test e Verificabilità

La correttezza del modello è validata attraverso la suite di test dedicata:
- [tests/test_antigravity_e19_hybrid_livestock.py](../../../tests/test_antigravity_e19_hybrid_livestock.py):
  - Verifica inizializzazione e parametri.
  - Verifica costruzione pascoli e collocazione animali (`BUILD_PASTURE` -> `PLACE`).
  - Verifica protocollo alimentare zero-escape (`FEED`).
  - Verifica intercettazione dell'on-tile capacity governor.
  - Verifica tutela della riserva di cassa ($300).
  - Smoke test reale con simulatore `kaggle-environments` su 48 passi.
