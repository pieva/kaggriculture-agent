# MODEL_SPEC C2 — ANTIGRAVITY

- **Modeler:** `ANTIGRAVITY`
- **Fase:** Model Foundation C2 Tournament Build
- **Stato:** CANDIDATE C2 / NOT FROZEN / TOURNAMENT_READY
- **Data:** 2026-08-30
- **Upstream Foundation:**
  - `docs/model/ontology/ONTOLOGY_C2.md`
  - `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2.md`
  - `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2.md`
- **Fonte diagnostica primaria:** Forensic Diagnosis E16 A-R1 (`E16_A_R1_CROP_ATTAINMENT_FORENSIC_DIAGNOSIS.md`) e Tile Lifecycle Audit (`E16_TILE_LIFECYCLE_FEATURE_AUDIT.md`)

---

## 1. Scopo e ipotesi operativa

### 1.1 Domanda causale centrale
> **Quali meccanismi hanno causato le prestazioni insufficienti delle policy E15/E16 e quali interventi decisionali concreti, fondati sull'evidenza forense e sulla Foundation C2, garantiscono la massima efficacia operativa e monetizzazione?**

### 1.2 Ipotesi causale di Antigravity (C2 Core Hypothesis)
La grave sotto-performance osservata nelle precedenti generazioni di policy (incluso il collasso di crop target attainment dal 100% nominale a $<50\%$ effettivo) **non è derivata da scarsità di semi, carenza idrica aggregata o vincoli di mercato**, ma da una triplice patologia di dispatching e lifecycle:

1. **Premature HARVEST Action Waste:** emissione compulsiva di comandi `HARVEST` su colture immature aventi `yield_units > 0` ma $\text{age} < \text{first\_yield\_day}$ (89.86% di tentativi di harvest falliti, 5.804 no-op);
2. **Permanent WEED Sinks:** assenza totale di azioni `DIG` di recupero su tile infestate (`LOST_WEED`), che trasformava ogni perdita accidentale in un sink permanente e sterilizzava la superficie produttiva;
3. **Mancata Clearance Preventiva di Fine Ciclo:** mancata rimozione programmata (`preventive_dig_action`) delle colture ongoing esaurite (`RETIREMENT_DUE`), che bloccavano le posizioni fino al decadimento naturale a weed.

**Intervento operativo C2:** implementare un'architettura decisionale rigorosamente fondata sul lifecycle a 6 stati di Foundation C2:
- Gate formale di harvest basato su `CRP-10` (`harvest_ready`);
- Clearance preventiva e recovery attivo via `DIG` (`preventive_dig_action` e `recovery_dig_action`);
- Replant immediato a latenza minima su `EMPTY_ASSIGNED`;
- Protezione idrica day-0 su nuove semine (`consecutive_unwatered = 1`).

---

## 2. Evidenza utilizzata

L'ipotesi di Antigravity C2 si fonda sull'evidenza empirica consolidata del dataset E16 A-R1 (28 episodi, 49.261 osservazioni tile-step):

1. **Failure Rate di HARVEST:** 5.804 tentativi di harvest su 6.459 sono falliti (89.86%); il 100% dei fallimenti (5.804/5.804) era dovuto a raccolta antecedente `first_yield_day`;
2. **Evoluzione del Decadimento a WEED:** 314 su 329 ingressi in stato `WEED` provenivano da piante vive per cause deterministiche e prevenibili (disidratazione a EOD o lifespan decay); solo 3 casi derivavano da spawn stocastico su tile vuote;
3. **Assenza di Recovery:** 0 azioni `DIG` eseguite nel trattamento E16, con conseguente blocco irreversibile delle tile contaminate;
4. **Disponibilità Risorse vs Esecuzione:** in configurazioni rappresentative come A07 (target 17 colture), la farm raggiungeva 15/17 colture attive a step 18, per poi collassare a 1 sola coltura attiva a fine partita, con 16 semi giacenti inutilizzati e 357 harvest prematuri falliti.

---

## 3. Diagnosi causale prioritaria

```text
Premature HARVEST Dispatch (5,804 no-ops) + No-DIG Policy
                           ↓
              Saturazione slot di movimento/azione
                           ↓
        Ritardo nell'irrigazione & perdita a EOD
                           ↓
              Generazione irreversibile di WEED
                           ↓
       Nessun Replant / Sterilizzazione del Working-Set
                           ↓
                 Crollo Attainment (< 50%)
```

Antigravity stabilisce come **priorità P0 assoluta** la risoluzione di questa catena causale distruttiva.

---

## 4. Meccanismi NON prioritari (Deprioritized Scope)

In ossequio al principio di parsimonia sperimentale, Antigravity dichiara esplicitamente non prioritari in C2:
- **Espansione al 3° quadrante (Q2):** mantenuta la focalizzazione stabile su 2 quadranti (50 tile) con perimetro arabile compatto;
- **Ottimizzazione dinamica delle curve di prezzo di mercato:** l'acquisto seed e l'assunzione worker operano su ordini standard con cash floor di sicurezza;
- **Scalamento multi-specie livestock aggressivo:** mantenimento di un comparto zootecnico conservativo proporzionato alle sole strutture già attive, per evitare crowding out della superficie arabile.

---

## 5. Feature C2 consumate e Consumer Mapping

| feature_id | Nome Feature C2 | Sorgente Runtime | Punto di calcolo | Fase decisionale | Ruolo nel MODEL_SPEC | Fallback Behavior |
|---|---|---|---|---|---|---|
| `TMP-01` | `step_current` | `observation.step` | Step loop | Global | Controllo timeout / endgame | `canonical_step` |
| `TMP-02` | `day_current` | `observation.day` | Step loop | Global | Controllo calendari biologici | `step // 24` |
| `TMP-03` | `hour_current` | `observation.hour` | Step loop | Action phase | Deadline pre-EOD | `step % 24` |
| `FRM-01` | `farm_money_current` | `farm.money` | Step start | Market / Dispatch | Valutazione affordability e cash floor | `0.0` |
| `FRM-02` | `tile_grid_raw` | `farm.tiles` | Step start | Pre-action | Snapshot coordinate perimetro | Matrice vuota |
| `FRM-03` | `working_set_member` | Configurazione interna | Step start | Tile classification | Filtro posizioni operative arabili | Posizioni Q0/Q1 |
| `CRP-01` | `tile_kind` | `tile.kind` | Per-tile inspection | Task generator | Identificazione `PLANT`, `WEED`, `None`, ecc. | `OUT_OF_SCOPE` |
| `CRP-02` | `crop_id_and_rules` | `tile.crop` + `CROPS` | Per-tile inspection | Task generator | Recupero `first_yield_day`, interval, ongoing | Default WHEAT |
| `CRP-03` | `planted_day` | `tile.planted_day` | Per-tile inspection | Task generator | Calcolo età biologica | `day_current` |
| `CRP-04` | `crop_age_days` | `day - planted_day` | Per-tile inspection | Task generator | Verifica maturità | `0` |
| `CRP-05` | `yield_units` | `tile.yield_units` | Per-tile inspection | Task generator | Quantità raccoglibile | `0` |
| `CRP-06` | `watered_today` | `tile.watered_today` | Per-tile inspection | Water dispatch | Predicato di bisogno idrico giornaliero | `False` |
| `CRP-07` | `consecutive_unwatered` | `tile.consecutive_unwatered` | Per-tile inspection | Water dispatch | Rilevazione urgenza critica EOD loss | `1` |
| `CRP-08` | `max_lifespan_step` | `tile.max_lifespan_step` | Per-tile inspection | Decay inspection | Prevenzione decadimento terminale | `9999` |
| `CRP-09` | `tile_lifecycle_state` | Classifier C2 | Per-tile inspection | Orchestratore task | Assegnazione task per stato canonico | `OUT_OF_SCOPE` |
| `CRP-10` | `harvest_ready` | Predicato C2 | Task generator | Harvest dispatch | Abilitazione tassativa comando `HARVEST` | `False` |
| `CRP-11` | `care_due` | Predicato C2 | Task generator | Water dispatch | Allerta manutenzione ordinaria | `False` |
| `CRP-12` | `water_loss_at_eod_if_unserved` | Predicato C2 | Task generator | Water dispatch | Prioritizzazione massima emergenza idrica | `False` |
| `INV-01` | `seed_inventory` | `private.seeds` | Step start | Plant / Market | Controllo disponibilità semina | `{}` |
| `INV-02` | `shed_inventory` | `private.shed` | Step start | Market / Feed | Rifornimento mangime e vendita | `{}` |
| `INV-03` | `worker_inventory` | `private.inventories` | Per-worker | Worker dispatch | Gestione carico, drop e pickup | `{}` |
| `WRK-01` | `unit_positions` | `farm.farmer` + `farm.hands` | Step start | Routing | Calcolo distanze Manhattan | `[(4,4)]` |
| `WRK-02` | `workforce_headcount` | `1 + len(hands)` | Step start | Market HIRE | Scalamento capacità operativa | `1` |

---

## 6. Regole decisionali e Policy C2

### 6.1 Algoritmo di Arbitraggio dei Task (Priority Hierarchy)

Per ciascun worker disponibile, l'assegnazione dell'azione segue una gerarchia deterministica non ambigua:

1. **Scarico Inventario Critico (Shed Drop):** se il worker trasporta beni non-feed, o se l'inventario totale $\ge 5$, o se trasporta WHEAT senza animali bisognosi, transito e scarico allo shed (`(4,4)`);
2. **Emergenza Idrica Day-0 / EOD Loss (`CRP-12`):** prioritizzazione assoluta di `WATER` su tile con `consecutive_unwatered + 1 >= 2` per prevenire la morte deterministica a EOD;
3. **Raccolta Matura (`CRP-10` `harvest_ready == True`):** esecuzione di `HARVEST` esclusivamente su tile che hanno superato `first_yield_day` con resa $>0$;
4. **Bonifica e Clearance (`DIG` Policy):**
   - *Preventive DIG:* rimozione programmata su tile `RETIREMENT_DUE` (colture ongoing esaurite);
   - *Recovery DIG:* bonifica correttiva su tile `LOST_WEED`;
5. **Manutenzione Idrica Ordinaria (`CRP-11` `care_due == True`):** irrigazione standard su piante attive non ancora bagnate nella giornata;
6. **Semina e Replant (`PLANT` su `EMPTY_ASSIGNED`):** allocazione immediata di nuovi semi su tile libere nel working-set;
7. **Servizio Zootecnico (Feed & Care):** alimentazione (`FEED`) e cura (`CARE`) degli animali presenti;
8. **Posizionamento Logistico / Patrol:** avvicinamento al centro operativo dello shed per essere pronti al tick successivo.

---

## 7. Dettaglio delle Policy di Settore

### 7.1 Tile Lifecycle Policy (`CRP-09`)
Ogni coordinata $[x, y]$ del perimetro di lavoro viene classificata deterministicamente secondo la precedenza C2:
- `OUT_OF_SCOPE`: tile non appartenente ai quadranti posseduti o assegnata a strutture;
- `LOST_WEED`: `tile.kind == "WEED"` $\implies$ genera task `recovery_dig_action`;
- `RETIREMENT_DUE`: `tile.kind == "PLANT"` con ciclo produttivo esaurito $\implies$ genera task `preventive_dig_action`;
- `HARVEST_READY`: `harvest_ready(tile, day) == True` $\implies$ genera task `HARVEST`;
- `GROWING`: `tile.kind == "PLANT"` in accrescimento $\implies$ genera task `WATER` se `care_due`;
- `EMPTY_ASSIGNED`: `tile is None` $\implies$ genera task `PLANT`.

### 7.2 HARVEST Policy (`CRP-10`)
$$\text{Emetti HARVEST} \iff \text{tile.kind} == \text{PLANT} \land \text{tile.yield\_units} > 0 \land (\text{day} - \text{tile.planted\_day}) \ge \text{first\_yield\_day}$$
- **Non-ongoing (Wheat, Melon):** dopo HARVEST la tile torna `None` $\implies$ transizione a `EMPTY_ASSIGNED` $\implies$ nuovo `PLANT` indipendente;
- **Ongoing (Strawberry):** dopo HARVEST la pianta azzera lo yield e torna in `GROWING`; se è stata raggiunta l'ultima produzione utile, la pianta transita in `RETIREMENT_DUE`.

### 7.3 DIG Policy (Preventive vs Recovery)
- **Preventive DIG:** emesso su `RETIREMENT_DUE` prima che intervengano i tick di decadimento;
- **Recovery DIG:** emesso su `LOST_WEED` per liberare il terreno infestato e restituirlo al ciclo produttivo;
- *Invariante:* la bonifica restituisce la tile a `EMPTY_ASSIGNED`, abilitando immediatamente la successiva semina.

### 7.4 WATER Policy
- Rispetto rigoroso del Day-0: le nuove semine hanno `consecutive_unwatered = 1` e vengono irrigate prioritariamente nello stesso giorno di planting;
- Monitoraggio della deadline EOD (`hour >= turnsPerDay - 4`): escalation dell'urgenza idrica per azzerare i missed-water.

### 7.5 Workforce e Routing Policy
- Scalamento progressivo dei Farm Hands fino a 10 worker attivi;
- Riconoscimento di `worker_multi_occupancy`: nessun blocco o ricalcolo artificiale per co-locazione;
- Assegnazione dei task basata su distanza Manhattan minima e prenotazione atomica (`reserved_targets`) per evitare contese ridondanti tra worker nello stesso step.

### 7.6 Inventory ed Endgame Policy
- Nessun obbligo di rientro manuale dei worker a EOD (drop automatico verificato);
- Gestione della capienza shed: liquidazione programmata a mercato (`SELL`) prima di raggiungere la saturazione di 100 unità;
- Shutdown window negli ultimi 48 step: interruzione delle semine a lungo ciclo per massimizzare la conversione in liquidità monetaria.

---

## 8. Failure Containment

1. **Assenza di Semi:** se `private.seeds[crop] == 0`, la tile `EMPTY_ASSIGNED` attende l'approvvigionamento senza bloccare gli altri worker;
2. **Cassa Insufficiente:** blocco cautelativo degli ordini di acquisto se `farm.money < operating_cash_floor` ($300);
3. **Mancata Raggiungibilità:** se una tile è temporaneamente non servibile, il dispatcher assegna il task alternativo a priorità inferiore;
4. **Tile Contaminata:** l'infestazione `WEED` attiva immediatamente il task `recovery_dig_action` evitando il blocco permanente.

---

## 9. Previsioni Verificabili (Pre-registered Predictions)

Prima dell'esecuzione dei test di validazione, Antigravity pre-registra le seguenti previsioni:

- **P1 (Harvest Correctness):** il numero di tentativi di harvest prematuri falliti crollerà a **0** (o $<1\%$ per soli edge cases di fine giornata);
- **P2 (Working-Set Persistence):** il tasso di mantenimento della superficie colturale attiva rimarrà stabilmente sopra l'80% per l'intera durata dell'episodio;
- **P3 (WEED Elimination):** la persistenza di tile `WEED` nel working-set si ridurrà di oltre il 90% grazie all'azione tempestiva di `recovery_dig_action`;
- **P4 (Replant Latency):** la latenza media di ripiantumazione su tile raccolte scenderà da oltre 22 step a $<5$ step;
- **P5 (Productive Action Share):** la frazione di azioni direttamente produttive aumenterà grazie all'azzeramento dei no-op da harvest prematuro;
- **P6 (Watering Continuity):** l'indice di continuità idrica si manterrà $\ge 0.95$;
- **P7 (Crop Target Attainment):** il crop target attainment corretto supererà la soglia di gate del **80%** (rispetto al 47% di E16 A07);
- **P8 (Final Money):** il saldo monetario terminale medio rifletterà la completa conversione dell'output biologico in cassa, superando stabilmente i livelli di E16.

---

## 10. Metriche di Verifica

Le previsioni saranno validate attraverso il protocollo standard:
- `premature_harvest_count` (Target: 0);
- `crop_target_attainment` (Target: $\ge 0.80$);
- `active_crop_surface` (Target: $\ge 15$ stabili);
- `watering_continuity` (Target: $\ge 0.95$);
- `lost_tile_persistence` (Target: $< 10$ step);
- `final_money` (Misurata a fine simulazione).

---

## 11. Assunzioni e Limiti

- Si assume che l'ambiente rispetti rigorosamente i parametri di `CROPS` (first_yield_day, interval, recipe);
- Si assume che la simulazione locale mantenga piena fedeltà con l'interpreter ufficiale Kaggle;
- L'allocazione a 2 quadranti è assunta come perimetro sufficiente per la validazione C2; l'estensione al 3° quadrante è differita alle fasi successive.

---

## 12. POST-TOURNAMENT REVIEW CONTRACT

Al termine del torneo a tre, Antigravity si impegna formalmente a:
1. Ricevere ed esaminare integralmente i log e le telemetrie di **tutti e tre i concorrenti** (Antigravity, Codex, Copilot);
2. Applicare a ciascun modello la medesima analisi causale disaggregata:
   $$\text{Risultato} \longrightarrow \text{Meccanismo Osservato} \longrightarrow \text{Decisione MODEL\_SPEC} \longrightarrow \text{Spiegazione Causale} \longrightarrow \text{Modifica Proposta}$$
3. Rifiutare qualsiasi razionalizzazione basata unicamente sul `final_money` complessivo, separando la validità dei meccanismi dall'efficienza di monetizzazione.

---

**Fine del MODEL_SPEC C2 Antigravity.**
