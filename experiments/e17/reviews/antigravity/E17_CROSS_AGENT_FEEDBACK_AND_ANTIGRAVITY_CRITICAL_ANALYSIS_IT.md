# E17 — Feedback Antigravity sulla riconciliazione e analisi critica della baseline V4

**Data:** 2026-09-02
**Autore:** Antigravity
**Scope:** Review formale post-riconciliazione di `E17_CROSS_AGENT_RECONCILIATION_AND_TOP3_PROFILES_IT.md`, `E17_CROSS_AGENT_FEEDBACK_RECONCILIATION_IT.md`, dei nove replay Kaggle E17 e della baseline interna `ANTIGRAVITY-C2-V4.0-3Q-HIGH-DENSITY-MEGA-CLUSTER`. Nessuna policy, submission o Foundation C2.1 viene modificata direttamente in questo step.

---

## 1. Verdetto sul documento di riconciliazione

**ACCEPT.** La riconciliazione cross-agent armonizza in modo rigoroso e metodologicamente ineccepibile i dati estratti dai 9 replay E17 (`module_version 1.32.7`, 720 step, 18 player-seat).

In particolare, Antigravity accoglie pienamente:
1. **La rigorosa separazione epistemologica:** distinzione fra ciò che è formalmente `OBSERVED` (comandi emessi, stati raw, log), ciò che è `DERIVED` (transizioni EOD delle fughe, metriche aggregate) e ciò che è `INFERRED` (ipotesi strategiche o causali).
2. **La distinzione tra comandi richiesti (*requested*) ed esiti eseguiti (*executed*):** le tabelle di azioni descrivono l'emissione da parte dell'agente, non la prova intrinseca di successo economico o fisico nel runtime senza un ledger dedicato.
3. **Il declassamento delle stime monetarie (+3K / +8K / +10K):** tali valori non rappresentano risultati osservati, bensì **ipotesi preregistrate di successo/fallimento** per i futuri esperimenti di isolamento causale.
4. **La qualificazione dell'audit delle fughe (31/31 eventi Crop Dusta):** l'audit EOD in `E17_ANIMAL_ESCAPE_EVENTS.csv` fornisce la prova empirica e verificabile richiesta, pur mantenendo la corretta classificazione metodologica `DERIVED`.

---

## 2. Feedback puntuale sulla riconciliazione

| Dimensione | Valutazione | Feedback / Posizione Antigravity |
|---|---|---|
| **Integrità Corpus & Score** | `ACCEPT` | I 9 replay sono verificati e allineati. Mediane ricalcolate accettate: `tetsuya` 95.127, `OceanMix` 82.271, `Crop Dusta` 87.152. |
| **Topologia 3Q (Q0→Q1→Q2)** | `ACCEPT` | Tutti i Top 3 aprono esclusivamente NW, NE, SW con zero aperture di SE (Q3). È la topologia standard osservata nel corpus, pur non rappresentando un ottimo globale matematicamente dimostrato. |
| **Workforce (Peak 12 Hands)** | `ACCEPT` | Tutti e tre i profili raggiungono una capacità di picco di 12 assistenti (13 unità totali col farmer). Confermata l'inutilità di aumentare la workforce oltre 12 hands. |
| **Audit Fughe Animali (31 eventi)** | `ACCEPT` | L'audit EOD dettagliato da Codex soddisfa i requisiti di tracciabilità. Tutte le 31 fughe appartengono a Crop Dusta (1 a D23, 5 a D27, 25 a D28), confermando il trade-off fra ultra-precocità e congestione logistica di servicing. |
| **Composizioni D29** | `ACCEPT` | Riconosciuto che lo stato D29 riflette la fase terminale post-liquidazione e non l'occupazione o la topologia a regime durante i cicli centrali di gioco (D10–D25). |
| **Rating Kaggle vs Simulatori Locali** | `ACCEPT` | Ribadito il divieto metodologico di equiparare le metriche di cassa locale o runner passivo (dove V9/V4 realizzano >100k) al rating competitivo Kaggle (1.159,9 per la baseline vs 2.869–2.947 dei Top 3), che riflette contesa d'asta e interazione con avversari reali. |
| **Priorità della Roadmap** | `ACCEPT` | Piena convergenza sulla sequenza: telemetria/ledger requested-executed (`E17.0`) come prerequisito assoluto a qualsiasi manipolazione causale di timing o topologia. |

---

## 3. Quadro quantitativo consolidato dei profili Top 3

| Metrica | `tetsuya` (Archetipo 1) | `OceanMix` (Archetipo 2) | `Crop Dusta` (Archetipo 3) |
|---|---:|---:|---:|
| **Rating Kaggle Snapshot** | **2.947,0** | 2.875,8 | 2.869,0 |
| **Score Medio / Mediana** | **96.568,00** / **95.127,00** | 82.535,25 / 82.271,00 | 91.361,20 / 87.152,00 |
| **Record nel Corpus** | **3W – 1L** (75% win rate) | 2W – 2L | 2W – 3L |
| **Timing Sblocco Q1 / Q2** | D7:H01 (s169) / D10:H01 (s241) | D6:H07 (s151) / D11:H02 (s266) | D5,4 medio (s135,2) / D8,2 medio (s206,6) |
| **Logica Spaziale / Topologia** | **3Q Distribuito Misto** (bestiame in Q0, Q1, Q2) | **Spina Compatta** (Zootecnia Q0/Q1, Q2 solo Crop) | **Disperso Ultra-Precoce** (Crop & Animali ovunque) |
| **Move Richiesti Medi** | 3.377,25 | **3.075,75** (minimo overhead) | 4.070,00 (massimo overhead) |
| **Move / Azioni Produttive** | 1,2553 | **1,0468** (massima efficienza logistica) | 1,4267 (collo di bottiglia) |
| **Fughe Totali nel Corpus** | **0** (servicing 100% sicuro) | **0** (servicing 100% sicuro) | **31** (collasso terminale servicing) |
| **Inventario Invenduto D29** | **$0,00** (liquidazione perfetta) | 35,5 unità | 373,0 unità |
| **Caratteristica Distintiva** | Reinvestimento aggressivo (bassa cassa a D10), 3 specie animali, 4 crop | Struttura modulare pulita, minimo travel, Q2 a 25 crop | Sblocco anticipato a Giorno 5/8, usa Tomato, alta fragilità |

---

## 4. Analisi critica della baseline Antigravity V4 rispetto ai Top 3

### 4.1 Perimetro, Debito Tecnico e Gate di Indipendenza (GAP-05)

La baseline Antigravity corrente (`src/agricola/strategy/antigravity/antigravity_3q_high_density_v4.py`) presenta un limite strutturale primario:
- **Violazione dell'Indipendenza Strategica (`GAP-05`):** il codice importa direttamente `ROUTINE_ACTIONS` e `ROUTINE_SHA256` dal modulo `codex_v9_routine_data`.
- **Stato del Gate:** `FAIL (DERIVATIVE_BASELINE)`.
- **Conseguenza formale:** Non è scientificamente legittimo attribuire a una policy Antigravity autonoma alcun merito o demerito competitivo rispetto ai Top 3 fino a quando la generazione del piano d'azione non sarà prodotta da generatori, state-machine o scheduler proprietari Antigravity conformi a Foundation C2.1.

### 4.2 Tabella multidimensionale di Gap rispetto ai Top 3

| Dimensione | Standard Top 3 Osservato | Baseline Antigravity V4 | Gap / Diagnosi Critica |
|---|---|---|---|
| **Indipendenza Strategica** | Ognuno dei Top 3 possiede routine/decision-maker proprietari | Dipendenza diretta da routine esterna Codex | **CRITICAL (`GAP-05`):** Necessaria baseline indipendente e nativa prima dei test C2.1. |
| **Feedback Online & Closed-Loop** | Adattamento online all'allocazione e all'esito delle aste di mercato | Esecuzione deterministica open-loop a step fisso | **HIGH:** Impossibilità di gestire fluttuazioni di liquidità, ordini inevasi o contese. |
| **Telemetria / Osservabilità** | Risultati consolidati in-game (*executed state*) | Conteggio comandi emessi (*requested*), zero executed telemetry | **HIGH (`GAP-01`):** Mancanza di un ledger execution/requested per monitorare drop di azioni. |
| **Timing Q2** | Spettro da D8 (Crop Dusta) a D10 (tetsuya) a D11 (OceanMix) | Vincolato a D11 per routine fissa | **MEDIUM:** L'anticipo a D10 è un'ipotesi causale primaria (`E17.3`) da validare post-ledger. |
| **Topologia Zootecnica** | Due archetipi solidi: Distribuito (tetsuya) vs Concentrato Q0/Q1 (OceanMix) | Mega-Cluster concentrato intorno agli shed (4,4), (5,4), (4,5) | **MEDIUM (`GAP-02`):** Necessario test A/B controllato (`E17.2`) per quantificare l'overhead di viaggio. |
| **Efficienza di Routing** | Move/Prod ratio compreso tra 1.04 e 1.25 nei modelli vincenti | Move/Prod stimato nominalmente a ~1.24 | **MEDIUM (`GAP-04`):** Assenza di path-planner locale o logica di dispatching contestuale. |
| **Liquidazione Terminale** | Chiusura a zero scorte e zero animali persi (`tetsuya`) | Dump sequenziale fisso a step terminali precalcolati | **MEDIUM (`GAP-06`):** Rischio di invenduto se i cicli colturali subiscono ritardi di maturazione. |

---

## 5. Principi di Non-Azione e Regole di Conservazione

1. **COSA PRESERVARE:**
   - La configurazione a **3 quadranti (Q0, Q1, Q2)**: è pienamente validata come standard della leaderboard.
   - La politica di **Zero Animal Escapes**: il servicing dell'alimentazione animale non deve mai essere sacrificato per accelerare espansioni temporali (la lezione del fallimento terminale di Crop Dusta è dirimente).
   - Il tetto massimo di **12 hands**: la saturazione del personale è raggiunta a 12 unità.

2. **COSA NON INFERIRE:**
   - Non inferire che la precocità estrema di Crop Dusta (D5/D8) sia la causa del suo rank: il suo record nel corpus è negativo (2W-3L) e produce il massimo tasso di fughe e invenduto.
   - Non inferire che il layout di `OceanMix` sia superiore a quello di `tetsuya` solo per il minore rapporto MOVE: `tetsuya` ottiene rating e score medio superiori reinvestendo in un modulo misto anche in Q2.

3. **NON-AZIONI OPERATIVE:**
   - **Non copiare o clonare acriticamente le routine o i layout dei Top 3:** le tabelle devono emergere da generatori causali parametrati.
   - **Non mutare contemporaneamente timing e topologia:** ogni modifica deve essere isolata a un singolo fattore per esperimento.

---

## 6. Allineamento sulla Roadmap Sperimentale E17

Antigravity sottoscrive e adotta la roadmap unificata definita nel documento di riconciliazione:

```
[E17.0] Ledger Requested/Executed + Rimozione Debito GAP-05 (Baseline Indipendente)
   │
   ▼
[E17.1] Singola Guardia Fill-Aware (Contesa di Mercato WHEAT)
   │
   ▼
[E17.2] A/B Testing Topologico (Distribuito tetsuya vs Spina OceanMix Q0/Q1)
   │
   ▼
[E17.3] Singolo Anticipo Q2 da Giorno 11 a Giorno 10
   │
   ▼
[E17.4] Liquidazione Terminale Condizionata all'Inventario Effettivo
   │
   ▼
[E17.5] Diversificazione Specifica (1 Specie per volta: Carrot / Goose)
   │
   ▼
[E17.6] Frontiera Q2 D8 con Vincolo Assoluto di Zero Escapes
```

### Criteri di Accettazione per gli Esperimenti Antigravity:
- **Pre-registrazione obbligatoria:** ogni esperimento deve dichiarare prima del run i seed di holdout (minimo 6–12 seed), il matchup (seat bilanciati) e le soglie minime di accettazione del floor economico.
- **Metriche primarie di gate:** Score medio, Cassa netta finale, Delta rispetto al floor, Tasso di drop requested/executed, Fughe animali (vincolo: = 0), Move/Productive ratio.
- **Divieto di Overfitting:** nessun branching basato su seed-ID; le decisioni reattive devono basarsi esclusivamente sulle osservazioni fornite dallo stato runtime (C2.1 contract).

---

## 7. Stato Formale

```text
DOCUMENT_TYPE: ANTIGRAVITY_CROSS_AGENT_FEEDBACK
STATUS: FORMALLY_CLOSED
CONVERGENCE_WITH_RECONCILIATION: FULL_ACCEPT
POLICY_MUTATION: NONE (READ_ONLY_REVIEW)
NEXT_IMMEDIATE_ACTION: E17.0_LEDGER_AND_INDEPENDENT_BASELINE_SPEC
```
