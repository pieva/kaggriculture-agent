# E07-02 — VERIFY Competitive Evidence

Stiamo lavorando al progetto **Kaggriculture Agent**.

La fase `E07-01 — DEFINE Competitive Baseline Reconstruction` ha prodotto:

`docs/versions/E07_define_competitive_baseline.md`

La ricognizione ha evidenziato un forte divario architetturale fra E06 e le strategie competitive individuate.

**Non procedere ancora al PLAN.**

Prima dobbiamo verificare rigorosamente che le evidenze utilizzate per costruire la `E07 Competitive Reference Configuration` siano reali, tracciabili, coerenti e sufficienti a giustificare i parametri proposti.

Questa fase è:

> **E07-02 — VERIFY Competitive Evidence**

Non modificare il codice dell'agente.

---

# 1. Obiettivo

Verificare tutte le affermazioni sostanziali contenute in:

`docs/versions/E07_define_competitive_baseline.md`

con particolare attenzione alle affermazioni quantitative e alle policy attribuite agli agenti competitivi.

La domanda di verifica è:

> **La Competitive Reference Configuration proposta da E07-01 deriva effettivamente da evidenze pubbliche verificabili oppure contiene assunzioni, generalizzazioni o sintesi non sufficientemente supportate?**

Non cercare di confermare il risultato precedente.

Cercare attivamente anche evidenze che lo contraddicano.

---

# 2. Verifica delle fonti SRC-01...SRC-06

Per ciascuna fonte indicata nel DEFINE:

- `SRC-01`
- `SRC-02`
- `SRC-03`
- `SRC-04`
- `SRC-05`
- `SRC-06`

identificare la fonte pubblica effettiva.

Per ogni fonte produrre:

| ID | Tipo | Titolo / Repository / Discussion | Autore | URL | Data, se disponibile | Accessibile | Note |
|---|---|---|---|---|---|---|---|

Non è sufficiente scrivere genericamente:

- "Kaggle Discussion";
- "GitHub";
- "strategy posts";
- "leaderboard analysis".

Serve un riferimento verificabile.

Se una delle `SRC-xx` del DEFINE non può essere ricostruita con precisione, marcarla:

**UNVERIFIED**

e identificare tutte le conclusioni che dipendono da essa.

---

# 3. Audit delle affermazioni quantitative

Verificare individualmente almeno le seguenti affermazioni presenti nel DEFINE.

## Land

- agenti competitivi: `50–75 tile`;
- utilizzo di `2–3 quadranti`;
- `BUY_LAND` sincronizzato con eventi di liquidità;
- acquisto Q1 circa Giorno 12;
- eventuale collegamento con raccolto Meloni Giorno 12–14.

## Workforce

- standard competitivo `3–5 worker`;
- burst hiring;
- `HIRE` a `hour == 0`;
- eventuale vantaggio documentato delle 24 ore complete di lavoro;
- schedule Giorno 1 / 6 / 12.

## Livestock

- configurazione competitiva circa `8 cows + 4 sheep`;
- proposta E07 `4 cows + 2 sheep`;
- fabbisogno di feed;
- affermazione `1 wheat/day per animal`;
- produzione e valore economico di latte/lana.

## Crops

- wheat come feed;
- melon come cash crop;
- carrot come flex crop;
- crescita wheat `1 day`;
- allocazioni proposte:
  - 6 wheat;
  - 12 melon;
  - 6 carrot.

## Market

- massimo `10 ordini/turno`;
- inventory/storage cap `100`;
- priorità:
  `Milk/Wool > Melon > Carrot`;
- eventuale price decay;
- vantaggio del buffering degli ordini.

## Scheduling

- ciclo:
  `Opening → Scale → Produce → Liquidate`;
- stop Melon Giorno 25;
- liquidazione Giorno 29–30;
- vendita finale degli animali.

## Structures

- utilizzo competitivo di `WELL`;
- utilizzo competitivo di `BARN`;
- costo e funzione;
- proposta WELL Giorno 5 con cash > `$500`.

---

# 4. Evidence Ledger

Creare un ledger completo.

Formato:

| Claim ID | Claim | Value / Policy | Evidence class | Exact source | Location | Status | Confidence |
|---|---|---|---|---|---|---|---|

`Evidence class` deve essere esclusivamente:

- `CODE`
- `EPISODE`
- `AUTHOR`
- `OFFICIAL`
- `INFERENCE`

`Status` deve essere:

- `VERIFIED`
- `PARTIALLY VERIFIED`
- `UNVERIFIED`
- `CONTRADICTED`

Per il codice indicare almeno:

`repository → file → funzione/classe/righe o frammento pertinente`

Per Kaggle Discussion:

`discussion → post/comment pertinente`

Per documentazione ufficiale:

`document/page/section`

Per replay:

`episode → step/day/hour pertinente`

---

# 5. Non confondere environment mechanics e competitive strategy

Separare rigorosamente:

### Environment facts

Esempi:

- costo `BUY_LAND`;
- costo `HIRE`;
- growth time;
- feed requirement;
- storage limit;
- durata episodio;
- azioni consentite.

Devono preferibilmente essere verificati direttamente nel codice/documentazione ufficiale dell'environment.

### Competitive observations

Esempi:

- un agente compra Q1 al Giorno 12;
- mantiene quattro cows;
- assume tre hands;
- utilizza 12 melon tile.

### Strategic inference

Esempio:

> "Gli agenti competitivi comprano Q1 dopo il primo liquidity event."

Questa può essere una conclusione valida soltanto se supportata da più osservazioni.

Non trasformare un comportamento di un singolo repository in uno "standard competitivo".

---

# 6. Verifica indipendente dell'environment

Ispezionare direttamente l'environment Kaggriculture disponibile nel progetto e/o la documentazione ufficiale.

Verificare almeno:

- dimensione mappa;
- quadranti;
- costi land;
- costi workforce;
- costo ricorrente workforce, se presente;
- livestock mechanics;
- feed mechanics;
- crop growth;
- watering;
- market mechanics;
- inventory;
- structures;
- durata episodio;
- valore finale/reward;
- comportamento degli asset al termine dell'episodio.

Registrare i valori reali.

Questi valori devono diventare la base per l'audit economico successivo.

---

# 7. Audit della superficie E07 proposta

Il DEFINE propone:

- 2 quadranti;
- 50 tile;
- 6 wheat;
- 12 melon;
- 6 carrot.

Questo assegna esplicitamente:

`6 + 12 + 6 = 24 tile`

ma dichiara un territorio target di `50 tile`.

Determinare:

- quali sono le restanti 26 tile;
- se sono coltivate;
- se sono destinate a livestock;
- se sono strutture;
- se sono buffer/path;
- se rimangono inutilizzate;
- se il numero `50` indica semplicemente terreno posseduto e non terreno produttivo.

Non accettare una configurazione con land allocation non definita.

---

# 8. Audit economico della Competitive Reference Configuration

Prima di implementarla, verificare se la configurazione proposta è almeno economicamente plausibile.

Ricostruire i principali cash flow.

Considerare almeno:

### Costs

- seeds;
- `HIRE`;
- eventuali wages;
- `BUY_LAND`;
- livestock;
- feed;
- structures;
- altri costi operativi.

### Revenues

- crops;
- milk;
- wool;
- livestock liquidation;
- altri prodotti.

Ricostruire indicativamente:

`Opening → Scale → Produce → Liquidate`

utilizzando **solo meccaniche reali dell'environment**.

Non inventare prezzi fissi se il mercato è dinamico.

Quando il prezzo non è determinabile a priori:

- indicare range osservabile oppure dipendenza;
- non produrre falsa precisione.

---

# 9. Audit della capacità operativa

Verificare se:

`1 Farmer + 3 Hands`

può realmente gestire:

- 50 tile possedute;
- crop operations;
- watering;
- harvesting;
- planting;
- 4 cows;
- 2 sheep;
- feeding;
- movement;
- eventuali structures;
- market actions.

Valutare la capacità in termini di:

- azioni necessarie;
- movement;
- frequenza delle operazioni;
- vincolo di 720 step;
- eventuali colli di bottiglia.

Non assumere che possedere 50 tile significhi poterle utilizzare efficientemente.

---

# 10. Audit del feed

Verificare esplicitamente la relazione proposta:

`6 wheat tile ↔ 6 animals`

e l'affermazione:

`1 wheat/day per animal`

Determinare:

- produzione effettiva per wheat tile;
- growth cycle;
- harvest frequency;
- quantità richiesta dagli animali;
- eventuale inventory buffer;
- sostenibilità nel tempo.

Concludere con uno dei seguenti stati:

- `FEED SURPLUS`
- `FEED BALANCED`
- `FEED DEFICIT`
- `INSUFFICIENT EVIDENCE`

---

# 11. Confronto tra agenti reali

Per ogni repository/agente pubblico sufficientemente verificabile, creare una riga:

| Agent | Land | Productive tiles | Workers | Crops | Cows | Sheep | Structures | Expansion timing | End-game | Performance |
|---|---:|---:|---:|---|---:|---:|---|---|---|---|

Non riempire celle non documentate con valori inferiti.

Usare `N/D`.

Questo confronto deve permetterci di distinguere:

**pattern ricorrenti**

da:

**configurazioni appartenenti a un singolo agente**.

---

# 12. Rivalutazione delle Confidence

Rivalutare tutte le confidence assegnate nel DEFINE.

Non mantenere `HIGH` solo perché era già presente.

Regola orientativa:

### HIGH

Più fonti indipendenti oppure codice/episodi direttamente verificabili e convergenti.

### MEDIUM

Una fonte forte oppure più evidenze indirette coerenti.

### LOW

Inferenza plausibile ma scarsamente documentata.

### UNVERIFIED

Evidenza non recuperabile o non verificabile.

---

# 13. Competitive Reference Configuration v2

Solo dopo l'audit, produrre una versione corretta:

## E07 Competitive Reference Configuration v2

Usare:

| Parameter | E07-01 proposal | Verified evidence | Revised proposal | Confidence | Change reason |
|---|---|---|---|---|---|

È consentito modificare qualsiasi valore del DEFINE precedente.

È consentito anche concludere che alcuni parametri debbano rimanere indeterminati fino al PLAN o a un test locale.

Non cercare di preservare artificialmente `HybridLivestockClusterROIAgent`.

Se l'evidenza suggerisce un'architettura diversa, proporla.

---

# 14. Decisione finale

Il VERIFY deve terminare con una delle seguenti decisioni:

### GO FOR PLAN

La configurazione è sufficientemente supportata e coerente.

### GO FOR PLAN WITH OPEN PARAMETERS

L'architettura è supportata, ma alcuni valori devono essere determinati sperimentalmente durante PLAN/BUILD.

### RETURN TO DEFINE

Le evidenze non supportano sufficientemente la configurazione.

### REJECT COMPETITIVE RECONSTRUCTION

La reconnaissance non dimostra che il cambio di baseline sia giustificato.

Motivare la decisione.

---

# 15. Deliverable

Creare:

`docs/versions/E07_verify_competitive_evidence.md`

Aggiornare inoltre:

- `docs/versions/E07_define_competitive_baseline.md`

solo se necessario per correggere affermazioni dimostrate false o non verificabili;

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;

registrando chiaramente lo stato E07.

Non cancellare le evidenze del DEFINE originale: eventuali correzioni devono essere tracciabili.

---

# 16. Vincoli

Durante E07-02:

**NON:**

- modificare il codice dell'agente;
- creare il nuovo agente;
- creare implementation plan;
- eseguire benchmark E07;
- creare submission;
- inviare a Kaggle;
- creare tag;
- dichiarare E07 shipped.

È consentito eseguire script o piccoli controlli esplorativi **solo se non modificano l'agente** e servono a verificare le meccaniche dell'environment.

---

# 17. Output finale richiesto

Al termine mostrare:

1. fonti `SRC-01...06` effettivamente verificate;
2. fonti non verificabili;
3. claim `CONTRADICTED` o `UNVERIFIED`;
4. meccaniche reali dell'environment rilevanti;
5. confronto fra configurazioni competitive reali;
6. audit superficie;
7. audit feed;
8. audit economico;
9. audit capacità workforce;
10. `Competitive Reference Configuration v2`;
11. differenze rispetto alla proposta E07-01;
12. decisione:
   - `GO FOR PLAN`,
   - `GO FOR PLAN WITH OPEN PARAMETERS`,
   - `RETURN TO DEFINE`,
   - oppure `REJECT COMPETITIVE RECONSTRUCTION`.

**FERMARSI DOPO LA DECISIONE.**

Attendere la revisione prima di qualsiasi implementazione.