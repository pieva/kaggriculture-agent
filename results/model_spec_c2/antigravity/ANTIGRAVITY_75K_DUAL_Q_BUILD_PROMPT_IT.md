# Mandato Operativo: Costruzione e Validazione della Candidata Antigravity 75K Dual-Quadrant Q0+Q1 (ANTIGRAVITY-C2-DUAL-Q0-Q1-75K)

## 1. Obiettivo Strategico ed Economico

Sviluppare, validare ed emettere la nuova candidata ufficiale **ANTIGRAVITY-C2-DUAL-Q0-Q1-75K** basata sull'architettura a due quadranti (**Q0 + Q1**), clonando in modo speculare il modulo ad alta efficienza zootecnica e orticola di Q0 ($56k–$57k) nel quadrante nord-est (Q1) attivato in modo cashflow-gated al Day 7–8.

### Obiettivi Quantitativi
- **Target Economico Medio Fase B (6 episodi):** **$\ge \$75.000,00$**
- **Minimo Capitale Finale per Singolo Episodio:** **$\ge \$68.000,00$**
- **Fughe di Animali (Animal Escapes):** **0** (su tutti gli episodi)
- **Hard Deadline Misses (WATER/FEED):** **0**
- **Technical Pass:** **YES** (100% determinismo, zero errori non gestiti)
- **Zero Regressioni:** 100% di conformità nella test suite globale del repository.

---

## 2. Vincoli Operativi Inderogabili

```text
LOCAL_DETERMINISTIC_REPLAY_AUTHORIZED: YES
MODEL_SPEC_MODIFICATION_AUTHORIZED: NO
FOUNDATION_MODIFICATION_AUTHORIZED: NO
ENGINE_MODIFICATION_AUTHORIZED: NO
TOURNAMENT_AUTHORIZED: NO
KAGGLE_UPLOAD_OR_RUN_AUTHORIZED: NO
COMMIT_AUTHORIZED: NO
PUSH_AUTHORIZED: NO
```

---

## 3. Architettura Dual-Quadrant (Q0 + Q1)

### Specifiche di Footprint e Geometria

```text
TERRITORY: Q0 (NW) + Q1 (NE)
QUADRANTS_OWNED: 2 (Q0 al Day 0, Q1 sbloccato al Day 7-8 via BUY_LAND a $1.000)
LAND_EXPANSION_COST: $1.000,00 (solo Q1; Q2 e Q3 disabilitati)
TOTAL_PRODUCTIVE_TILES: 48 (36 colture + 12 pascoli)
SHED_POSITION: (4, 4) (condiviso al centro)
TOTAL_WORKFORCE: 13 (Farmer W0 + 6 Braccianti Q0 + 6 Braccianti Q1)
TOTAL_LIVESTOCK: 6 COW + 6 SHEEP (3+3 in Q0, 3+3 in Q1)
TOTAL_CROP_MIX: 18 MELON / 16 STRAWBERRY / 2 WHEAT
```

### Roster e Specializzazione dei 13 Ruoli

| Worker | Ruolo | Dominio Territoriale | Responsabilità |
|---|---|---|---|
| **W0** | `RELIEF_LOGISTICS` | Centro / Globale | Gestione shed, vendite mercato, coorti, soccorso hard |
| **W1** | `CROP_ZONE_0` | Q0 Zone 0 (`(0,0)..(2,1)`) | Irrigazione e raccolta 6 tile Zone 0 |
| **W2** | `CROP_ZONE_1` | Q0 Zone 1 (`(3,0)..(3,3)`) | Irrigazione e raccolta 6 tile Zone 1 |
| **W3** | `CROP_ZONE_2` | Q0 Zone 2 (`(0,2)..(3,4)`) | Irrigazione e raccolta 6 tile Zone 2 |
| **W4** | `LIVESTOCK_COW_Q0` | Q0 Pascoli COW (`(0,4), (1,4), (2,4)`) | Alimentazione prioritaria, cura, mungitura 3 vacche Q0 |
| **W5** | `LIVESTOCK_SHEEP_Q0` | Q0 Pascoli SHEEP (`(4,0), (4,1), (4,2)`) | Alimentazione prioritaria, cura, tosatura 3 pecore Q0 |
| **W6** | `FERTILIZER_LOGISTICS_Q0` | Q0 Pascoli e Colture | Raccolta concime e applicazione su colture Q0 |
| **W7** | `CROP_ZONE_3` | Q1 Zone 3 (`(9,0)..(7,1)`) | Irrigazione e raccolta 6 tile Zone 3 |
| **W8** | `CROP_ZONE_4` | Q1 Zone 4 (`(6,0)..(6,3)`) | Irrigazione e raccolta 6 tile Zone 4 |
| **W9** | `CROP_ZONE_5` | Q1 Zone 5 (`(9,2)..(6,4)`) | Irrigazione e raccolta 6 tile Zone 5 |
| **W10** | `LIVESTOCK_COW_Q1` | Q1 Pascoli COW (`(9,4), (8,4), (7,4)`) | Alimentazione prioritaria, cura, mungitura 3 vacche Q1 |
| **W11** | `LIVESTOCK_SHEEP_Q1` | Q1 Pascoli SHEEP (`(5,0), (5,1), (5,2)`) | Alimentazione prioritaria, cura, tosatura 3 pecore Q1 |
| **W12** | `FERTILIZER_LOGISTICS_Q1` | Q1 Pascoli e Colture | Raccolta concime e applicazione su colture Q1 |

---

## 4. Regole di Ammissione e Attivazione Q1

1. **Finestra di Valutazione:** Dal Day 6 al Day 9.
2. **Criterio di Ammissione:**
   - `Day <= 9` (payback cutoff zootecnico).
   - Cassa disponibile + vendite prospettiche $\ge \$2.800,00$.
   - Riserva operativa minima post-sblocco garantita.
3. **Esecuzione dell'Espansione:**
   - Emette `["BUY_LAND"]` sul mercato a inizio giornata.
   - Il target di forza lavoro sale a 13.
   - I braccianti W7..W12 vengono assunti a ogni nuovo Day non appena la cassa lo consente.
   - Vengono costruiti i 6 pascoli di Q1 e acquistati 2 COW + 2 SHEEP (poi scalati a 3+3).
   - Vengono acquistati e piantati i semi per le 18 tile di Q1.

---

## 5. Invarianti di Sicurezza e Contenimento Spaziale

- **Isolamento Territoriale dei Braccianti:** I lavoratori W1..W6 non generano task né si spostano in Q1 ($x \ge 5$). I lavoratori W7..W12 non generano task né si spostano in Q0 ($x < 5$).
- **Binding Atomico dei Feed Owner:** Ogni cluster (COW Q0, SHEEP Q0, COW Q1, SHEEP Q1) ha un proprietario dedicato. Il task `FEED` richiede grano a bordo o prelievo batch atomico dallo shed dimensionato sul `due_feed_set`.
- **Precedenza Feed:** L'alimentazione precede tassativamente scarico merci o concimazione.
- **Ciclo Chiuso Fertilizzante:** Applicato nello stesso giorno esclusivamente su meloni e fragole irrigate.

---

## 6. Piano Sperimentale

1. **Fase A (Regressione e Baseline):** Verifica non-regressione sui moduli esistenti.
2. **Fase B (Suite di Validazione Ufficiale):** 6 episodi su Seeds `26090101`, `26090102`, `26090103` per entrambi i Seat 0 e 1 (Target medio: $\ge \$75.000$).
3. **Fase C (Suite di Conferma Seed AG):** 6 episodi su Seeds `1838889274`, `1619968655`, `710418712` per entrambi i Seat 0 e 1.

---

## 7. Artefatti Richiesti

- Configurazione: `configs/model_spec_c2/ANTIGRAVITY_C2_75K_DUAL_Q_CONFIG.json`
- Modulo Config: `src/agricola/strategy/antigravity/c2_75k_config.py`
- Policy Dual: `src/agricola/strategy/antigravity/antigravity_dual_q0_q1.py`
- Agent Adapter: `src/agricola/strategy/antigravity/agent_c2_75k.py`
- Packager: `scripts/build_submission_antigravity_75k.py` e `submission/submission_antigravity_75k.py`
- Verifier Standalone: `scripts/verify_antigravity_75k_submission.py`
- Test Suite: `tests/test_antigravity_75k_candidate.py`
- Benchmark: `scripts/benchmark_antigravity_75k.py`
- Dataset Risultati: `results/model_spec_c2/antigravity/ANTIGRAVITY_75K_RESULTS.csv` e `.json`
- Rapporto Finale Validazione (16 Sezioni in Italiano): `results/model_spec_c2/antigravity/ANTIGRAVITY_75K_FINAL_REPORT_IT.md`
