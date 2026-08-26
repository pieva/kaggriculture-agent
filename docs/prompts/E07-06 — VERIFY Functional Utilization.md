# E07-06 — VERIFY Functional Utilization

Stiamo lavorando al progetto **Kaggriculture Agent**.

La fase `E07-05 — BUILD Configurable Competitive Baseline` ha prodotto un primo smoke episode completo da 720 step con:

- `Final Money = $21,933`;
- nessuna disqualification;
- 4 worker raggiunti;
- Q1 acquistato;
- 50 tile possedute;
- 24 tile dichiarate produttive;
- livestock acquistato per `$2,600`;
- 125 eventi weeds;
- 148 worker idle;
- 256 movement;
- ricavi osservati quasi interamente da Melon e Carrot.

Il BUILD è strutturalmente funzionante, ma lo smoke **non dimostra ancora che tutte le capability E07 siano realmente operative**.

Questa fase deve verificare l'utilizzo funzionale della nuova architettura prima del benchmark statistico da 30 episodi.

Non fare tuning prestazionale.

---

# 1. Obiettivo

Rispondere alla domanda:

> **Le capability che definiscono E07 come baseline competitiva di seconda generazione vengono realmente esercitate durante un episodio, oppure alcune sono soltanto implementate/configurate senza produrre comportamento economico effettivo?**

Dobbiamo distinguere rigorosamente:

```text
IMPLEMENTED
    ≠
EXERCISED
    ≠
PRODUCTIVE
    ≠
PROFITABLE
```

In questa fase dobbiamo arrivare almeno a `EXERCISED`.

La redditività statistica verrà valutata successivamente.

---

# 2. Riprodurre lo smoke episode

Utilizzare lo stesso setup dello smoke E07-05, possibilmente con stesso opponent e seed/configurazione riproducibile.

Eseguire **un singolo episodio completo da 720 step** con telemetria diagnostica estesa.

Non eseguire ancora il benchmark da 30 episodi.

Registrare il Final Money, ma non usarlo come criterio principale di questa verifica.

---

# 3. Capability Matrix

Produrre al termine:

| Capability | Implemented | Exercised | Productive output observed | Evidence | Status |
|---|---:|---:|---:|---|---|
| Phase scheduling | | | | | |
| Workforce scaling | | | | | |
| Land expansion | | | | | |
| Q1 productive utilization | | | | | |
| Multi-crop | | | | | |
| Livestock purchase | | | | | |
| Pasture construction | | | | | |
| Animal placement | | | | | |
| Animal feeding | | | | | |
| Milk production | | | | | |
| Wool production | | | | | |
| Feed loop | | | | | |
| Market broker | | | | | |
| Inventory flush | | | | | |
| End-game policy | | | | | |

`Status`:

- `PASS`
- `PARTIAL`
- `FAIL`
- `N/A`

---

# 4. Livestock lifecycle audit

Questa è la priorità principale.

Il BUILD ha registrato `$2,600` di spesa livestock ma nessun ricavo Milk/Wool nello smoke summary.

Ricostruire l'intero lifecycle di ogni animale:

```text
BUY_ANIMAL
    ↓
inventory / shed
    ↓
BUILD_PASTURE
    ↓
PLACE
    ↓
FEED
    ↓
CARE, se richiesto
    ↓
product generation
    ↓
PICKUP / collection
    ↓
SELL
    ↓
cash
```

Adattare la sequenza alle reali meccaniche dell'environment.

Per ogni passaggio verificare se:

- viene pianificato;
- viene emessa l'azione;
- l'environment la accetta;
- cambia effettivamente lo stato.

---

# 5. Livestock inventory audit

Dopo ogni `BUY_ANIMAL` significativo registrare:

- animale acquistato;
- cash prima/dopo;
- contenuto shed/inventory;
- posizione;
- pasture disponibile;
- stato `PLACED / UNPLACED`.

Al termine verificare quanti animali sono:

- acquistati;
- collocati;
- alimentati;
- produttivi;
- rimasti inutilizzati.

Un animale acquistato ma mai `PLACE`d deve essere classificato come:

> **STRANDED CAPITAL**

---

# 6. Pasture audit

Verificare direttamente:

- quante `BUILD_PASTURE` vengono richieste;
- quante riescono;
- coordinate;
- worker utilizzato;
- momento della costruzione;
- animali effettivamente collocati.

Non considerare una tile "livestock tile" soltanto perché la configurazione la riserva teoricamente.

Deve esistere nello stato reale dell'environment.

---

# 7. Feed loop audit

Misurare:

```text
Wheat produced
Wheat available
Wheat consumed by livestock
Feed actions attempted
Feed actions successful
Feed misses
Animals requiring feed
```

Verificare se il feed loop è realmente:

- `SURPLUS`
- `BALANCED`
- `DEFICIT`
- `NOT ACTIVE`

Non utilizzare il precedente calcolo teorico `6 wheat tile → 9 wheat/day` come prova.

Usare la produzione osservata nell'episodio.

---

# 8. Livestock output audit

Registrare separatamente:

```text
MILK produced
MILK collected
MILK sold
MILK revenue

WOOL produced
WOOL collected
WOOL sold
WOOL revenue
```

Se Milk/Wool vengono prodotti ma non venduti, individuare il punto di blocco.

Se non vengono prodotti, individuare il primo passaggio fallito del lifecycle.

---

# 9. Land expansion audit

Verificare `BUY_LAND Q1` nello stato reale.

Registrare:

```text
day
step
cash_before
cash_after
owned_tiles_before
owned_tiles_after
```

Poi distinguere:

```text
owned Q1 tiles
productive Q1 tiles
actually worked Q1 tiles
harvested Q1 tiles
```

---

# 10. Q1 utilization

Calcolare almeno:

```text
Q1 utilization =
actually_worked_Q1_tiles / owned_Q1_tiles
```

e:

```text
Q1 productive utilization =
productive_Q1_tiles / owned_Q1_tiles
```

Specificare chiaramente la definizione usata.

Produrre anche il confronto:

| Area | Owned | Productive | Actually worked | Harvested |
|---|---:|---:|---:|---:|
| Q0 | | | | |
| Q1 | | | | |
| Total | | | | |

Se Q1 viene acquistato ma nessuna tile Q1 viene utilizzata produttivamente:

> `BUY_LAND = EXERCISED BUT NON-PRODUCTIVE`

Questo è un blocker funzionale da correggere prima del benchmark.

---

# 11. Crop allocation audit

Per ogni crop:

| Crop | Allocated tiles | Actually planted | Harvested | Units produced | Units sold | Revenue |
|---|---:|---:|---:|---:|---:|---:|
| Wheat | | | | | | |
| Melon | | | | | | |
| Carrot | | | | | | |

Separare Q0 e Q1 quando possibile.

Verificare se le 24 tile dichiarate attive vengono realmente utilizzate.

---

# 12. Weeds audit

Lo smoke E07-05 ha registrato:

`125 weeds`

Questo valore richiede diagnosi.

Determinare esattamente cosa rappresenta il contatore:

- eventi di comparsa;
- tile affette;
- turni con weeds;
- crop persi;
- altro.

Misurare:

- coordinate;
- crop interessata;
- fase;
- giorno;
- conseguenza produttiva;
- eventuale recuperabilità tramite `DIG`.

Non introdurre DIG in questa fase salvo che sia necessario correggere un bug funzionale.

L'obiettivo è stabilire se weeds costituisce:

- problema marginale;
- perdita produttiva significativa;
- blocker strutturale;
- candidato forte per E08+.

---

# 13. Workforce utilization audit

La telemetria precedente riportava:

- productive actions: 384;
- movement: 256;
- idle: 148.

Scomporre ora per singolo worker:

| Worker | Productive | Movement | Idle | Total | Productive % | Movement % | Idle % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Farmer | | | | | | | |
| Hand 1 | | | | | | | |
| Hand 2 | | | | | | | |
| Hand 3 | | | | | | | |

Verificare inoltre:

- distanza media per task;
- eventuali worker sistematicamente sottoutilizzati;
- conflitti;
- task starvation;
- distribuzione Q0/Q1.

Non concludere ancora che il numero ottimale sia 3, 4 o 5 worker.

---

# 14. Phase audit

Per ogni fase registrare:

| Phase | Start | End | Cash start | Cash end | Main investments | Main revenues |
|---|---:|---:|---:|---:|---|---|
| OPENING | | | | | | |
| SCALE | | | | | | |
| PRODUCE | | | | | | |
| LIQUIDATE | | | | | | |

Verificare che il cambio fase produca realmente un cambiamento di comportamento.

Una state machine che cambia soltanto etichetta senza modificare le decisioni deve essere classificata `PARTIAL`.

---

# 15. Market and liquidation audit

Verificare:

- prodotti entrati in inventory;
- prodotti venduti;
- quantità;
- ricavi;
- ordini respinti;
- inventory peak;
- inventory finale.

A fine episodio deve essere evidente:

```text
sellable inventory → cash
```

Se rimane inventory vendibile:

- quantità;
- prodotto;
- motivo.

---

# 16. Final asset snapshot

Al turno finale registrare:

```text
cash
inventory
animals
land
structures
mature crops
immature crops
```

Ricordare:

> Tutti gli asset diversi dal cash hanno valore terminale zero nel reward, salvo conversione preventiva attraverso una meccanica realmente disponibile.

Non sommare il loro valore teorico al Final Money.

---

# 17. Submission file audit

`git status` dopo E07-05 mostra:

```text
M submission/submission.py
```

ma il BUILD non doveva ancora preparare la submission.

Verificare:

```powershell
git diff -- submission/submission.py
```

Determinare:

- quale modifica è presente;
- quando è stata introdotta;
- se è conseguenza automatica di uno script;
- se appartiene realmente a E07;
- se deve essere mantenuta o ripristinata.

Non costruire una nuova submission.

Non inviare nulla a Kaggle.

Se la modifica è accidentale o prematura, ripristinare esclusivamente quella modifica senza alterare file validi precedenti.

---

# 18. Correzioni consentite

Se una capability risulta `FAIL` a causa di un bug implementativo evidente, è consentito correggere il BUILD.

Esempi:

- animali acquistati ma mai collocati;
- pasture non costruite per errore di action syntax;
- Milk/Wool prodotti ma mai raccolti;
- Q1 non utilizzato per errore nel tile allocator;
- telemetria errata.

Dopo ogni correzione:

```powershell
.venv\Scripts\pytest tests/
```

e ripetere lo smoke episode.

Non fare tuning quantitativo.

Non cambiare arbitrariamente:

- herd size;
- worker target;
- crop ratios;
- expansion day;
- cash reserve;

per migliorare Final Money.

Questi rimangono parametri OPEN.

---

# 19. Functional acceptance criteria

E07 supera questa fase se almeno:

### Required PASS

- phase scheduling;
- workforce scaling;
- land expansion;
- multi-crop;
- market broker;
- end-game/inventory flush.

### Required livestock PASS

Se livestock rimane parte della baseline E07:

- purchase;
- pasture;
- placement;
- feed;
- production;
- collection;
- sale.

Milk/Wool devono produrre almeno un output osservabile e vendibile.

### Required expansion PASS

Q1 deve avere almeno utilizzo produttivo reale.

Non è sufficiente possederlo.

---

# 20. Decisione

Terminare con una delle seguenti.

### GO FOR PERFORMANCE VERIFY

Tutte le capability strutturali fondamentali vengono realmente esercitate.

### CONTINUE BUILD

Una o più capability fondamentali sono implementate ma non funzionano ancora.

### RETURN TO PLAN

L'environment impedisce o rende incoerente una parte sostanziale dell'architettura.

---

# 21. Deliverable

Creare:

`docs/versions/E07_verify_functional_utilization.md`

Aggiornare:

- `docs/PROJECT_STATE.md`;
- `docs/NEW_SESSION.md`;

e, se sono state necessarie correzioni implementative:

- `docs/versions/E07_build_competitive_baseline.md`.

Non dichiarare E07 validated o shipped.

---

# 22. Output finale richiesto

Mostrare:

1. Capability Matrix;
2. livestock lifecycle completo;
3. feed audit;
4. Milk/Wool output;
5. Q1 utilization;
6. crop utilization;
7. weeds diagnosis;
8. workforce utilization per worker;
9. phase audit;
10. market/liquidation audit;
11. final asset snapshot;
12. esito audit `submission/submission.py`;
13. eventuali bug corretti;
14. risultato completo `pytest`;
15. Final Money del nuovo smoke, come dato diagnostico;
16. parametri ancora OPEN;
17. decisione finale.

**FERMARSI QUI.**

Non:

- eseguire benchmark da 30 episodi;
- fare tuning prestazionale;
- costruire submission;
- inviare submission Kaggle;
- creare tag;
- dichiarare E07 validated;
- dichiarare E07 shipped.

Attendere la revisione prima del Performance VERIFY.