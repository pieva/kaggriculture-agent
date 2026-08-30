# Prompt Operativi di Progetto (`docs/prompts/`)

## 1. Scopo della directory

La directory `docs/prompts/` raccoglie i mandati operativi, i prompt di indirizzo strategico, le specifiche metodologiche e i protocolli formali forniti agli agenti AI (Antigravity, Codex, Copilot) durante lo sviluppo e la sperimentazione del progetto **Kaggriculture**.

## 2. Policy di conservazione

La presenza dei file nel working tree segue una policy di razionalizzazione controllata per garantire pulizia, navigabilità ed efficienza di contesto:

- **Fasi storiche precedenti a E14 (E01–E13):** è conservato nel working tree **un solo prompt canonico per fase/esperimento**, selezionato in base al valore documentale effettivo (mandato fondativo, guida dell'implementazione effettiva o decisione metodologica conclusiva). Le micro-iterazioni e i prompt intermedi superati sono stati rimossi dal working tree.
- **Ciclo metodologico avanzato (E14–E16):** vige una policy **conservativa** (`KEEP`) che preserva tutti i prompt corrispondenti a passaggi e ruoli metodologici distinti (isolamento repository, ontologia, MODEL_SPEC indipendenti, review, freeze pre-torneo, training design, esecuzione, diagnosi forense e riparazione semantica).
- **Manutenzione e Dati Speciali:** sono conservati i prompt di manutenzione strutturale (`.venv`, cleanup controllato) e artefatti di riferimento empirico/dati (coordinate spaziali, ricostruzioni quantitative di replay).

> **Nota storica:** Tutti i prompt intermedi, preparatori e correttivi rimossi dal working tree rimangono integralmente tracciati e recuperabili in qualsiasi momento attraverso la **Git history** del repository (`git log -- docs/prompts/`).

---

## 3. Distinzione tra Prompt Canonici Storici ed E14–E16

### Prompt Canonici Storici (E01–E13)
Rappresentano la pietra miliare iniziale o la decisione architetturale chiave di ciascuna iterazione storica:
- **E01:** Mandato fondativo di progetto e baseline rule-based (`E01-01_define_plan.md`)
- **E02:** Avvio seconda iterazione e selezione dinamica basata sul ROI (`E02-01_start.md`)
- **E03:** Multi-tile scaling su cluster compatto 2×2 (`E03-01_start.md`)
- **E04:** Decisione di direzione sperimentale e gap analysis (`E04-02_Experimental_Direction_Decision.md`)
- **E05:** Analisi capacità HIRE e multi-worker scaling (`E05-01 — HIRE Capability & Experimental Design Analysis.md`)
- **E06:** Schedulazione water-first (`E06-01 — DEFINE Water-First Scheduling.md`)
- **E07:** Ricostruzione baseline competitiva configurabile (`E07-01 — DEFINE Competitive Baseline Reconstruction.md`)
- **E08:** Ottimizzazione scala produttiva (`E08-01_DEFINE_Productive_Scale_Optimization.md`)
- **E09:** Ablazione sottosistema livestock con correzione baseline (`E09-01B_define_revision_antigravity.md`)
- **E10:** Protezione capitale espansione Q1 e overnight Kaggle (`E10-01_kaggle_overnight_antigravity.md`)
- **E11:** Espansione massa produttiva 3× (`E11-01 — DEFINE — 3× Productive Mass Expansion.md`)
- **E12:** Centered hybrid farm scaling e integrazione livestock (`E12_define_centered_hybrid_farm_scaling.md`)
- **E13:** Analisi forense blind multi-agente su replay Kaggle (`E13_EPISODE_101971376_BLIND_FORENSIC_REPLAY_ANALYSIS.md`)

### Ciclo Metodologico Avanzato (E14–E16)
Documenta l'infrastruttura di cooperazione multi-modello, isolamento, freeze formale e diagnosi causale:
- **E14:** Isolamento repository per modello (`E14_01_*`), proposte ontologiche cross-model (`E14_02_*`), preparazione pre-torneo (`E14_7_E15_0_*`)
- **E15:** Freeze pre-torneo, review neutrale Codex (`E15_0b_*`), enforcement (`E15_0c_*`), certificazione finale (`E15_0d_*`), chiusura e commit (`E15_0e_*`, `CODEX_CLOSE_E15.md`)
- **Post-E15:** Verifica capacità modelli e revisione MODEL_SPEC (`POST_E15_*`)
- **E16:** Proposta di training design (`E16_TRAINING_DESIGN_PROPOSAL.md`), mandato di implementazione (`E16_IMPLEMENTATION_PROMPT.md`), esecuzione Stage A (`E16_STAGE_A_EXECUTION_ANTIGRAVITY.md`), diagnosi forense indipendente (`E16_STAGE_A_FORENSIC_DIAGNOSIS_ANTIGRAVITY.md`, `E16_STAGE_A_CODEX_FORENSIC_REVIEW_AND_REPAIR_SPEC.md`, `E16_A_R1_CODEX_FORENSIC_DIAGNOSIS_PROMPT.md`), chiarimento semantico irrigazione (`E16_WATERING_SEMANTIC_CLARIFICATION_AND_REPAIR_CODEX.md`), esecuzione replica corretta R1 (`E16_STAGE_A_R1_EXECUTION_ANTIGRAVITY.md`)

---

## 4. Elenco dei file conservati nel Working Tree

| File | Fase / Ambito | Ruolo / Descrizione |
|---|---|---|
| `ANTIGRAVITY_PROMPTS_CLEANUP_AND_DOCS_VERIFY.md` | Manutenzione | Prompt operativo di pulizia e verifica strutturale docs |
| `CODEX_CLOSE_E15.md` | E15 | Chiusura e sintesi torneo E15 (Codex) |
| `E01-01_define_plan.md` | E01 | Mandato fondativo Kaggriculture e baseline E01 |
| `E02-01_start.md` | E02 | Avvio iterazione E02 (selezione dinamica colture ROI) |
| `E03-01_start.md` | E03 | Avvio iterazione E03 (multi-tile scaling 2×2) |
| `E04-02_Experimental_Direction_Decision.md` | E04 | Decisione strategica direzione sperimentale E04 |
| `E05-01 — HIRE Capability & Experimental Design Analysis.md` | E05 | DEFINE capacità HIRE e multi-worker scaling |
| `E06-01 — DEFINE Water-First Scheduling.md` | E06 | DEFINE schedulazione water-first |
| `E07-01 — DEFINE Competitive Baseline Reconstruction.md` | E07 | DEFINE baseline competitiva configurabile |
| `E08-01_DEFINE_Productive_Scale_Optimization.md` | E08 | DEFINE ottimizzazione scala produttiva |
| `E09-01B_define_revision_antigravity.md` | E09 | DEFINE revisionato ablazione sottosistema livestock |
| `E10-01_kaggle_overnight_antigravity.md` | E10 | Mandato integrato overnight e protezione capitale Q1 |
| `E11-01 — DEFINE — 3× Productive Mass Expansion.md` | E11 | DEFINE espansione massa produttiva 3× |
| `E12_define_centered_hybrid_farm_scaling.md` | E12 | DEFINE centered hybrid farm scaling |
| `E12_TRUEBELIEF_101294736_FULL_REPLAY_ANALYSIS.md` | E12 (Dati) | Ricostruzione quantitativa completa replay episode 101294736 |
| `E13_EPISODE_101971376_BLIND_FORENSIC_REPLAY_ANALYSIS.md` | E13 | Analisi forense blind multi-agente episode 101971376 |
| `E14_01_antigravity_repository_model_isolation.md` | E14 | Isolamento repository e MODEL_SPEC (Antigravity) |
| `E14_01_codex_repository_model_isolation.md` | E14 | Isolamento repository e MODEL_SPEC (Codex) |
| `E14_01_copilot_repository_model_isolation.md` | E14 | Isolamento repository e MODEL_SPEC (Copilot) |
| `E14_02_antigravity_ontology_proposal.md` | E14 | Proposta ontologica cross-model (Antigravity) |
| `E14_02_codex_ontology_proposal.md` | E14 | Proposta ontologica cross-model (Codex) |
| `E14_02_copilot_ontology_proposal.md` | E14 | Proposta ontologica cross-model (Copilot) |
| `E14_7_E15_0_cleanup_freeze_tournament_prep.md` | E14/E15 | Cleanup, freeze pre-match e preparazione torneo |
| `E15_0b_CODEX_NEUTRAL_FREEZE_REVIEW.md` | E15 | Revisione neutrale pre-torneo freeze (Codex) |
| `E15_0c_FIX_FREEZE_ENFORCEMENT.md` | E15 | Correzione runner per enforcement del freeze |
| `E15_0d_CODEX_FINAL_FREEZE_CERTIFICATION.md` | E15 | Certificazione finale freeze (Codex) |
| `E15_0e_ANTIGRAVITY_CLOSE_STATE_COMMIT_PUSH.md` | E15 | Chiusura stato pre-torneo, cleanup e commit |
| `E16_A_R1_CODEX_FORENSIC_DIAGNOSIS_PROMPT.md` | E16 | Diagnosi forense E16-A-R1 (Codex) |
| `E16_IMPLEMENTATION_PROMPT.md` | E16 | Mandato generale di implementazione E16 |
| `E16_STAGE_A_CODEX_FORENSIC_REVIEW_AND_REPAIR_SPEC.md` | E16 | Revisione forense e specifica di riparazione (Codex) |
| `E16_STAGE_A_EXECUTION_ANTIGRAVITY.md` | E16 | Esecuzione Stage A (Antigravity) |
| `E16_STAGE_A_FORENSIC_DIAGNOSIS_ANTIGRAVITY.md` | E16 | Diagnosi forense Stage A (Antigravity) |
| `E16_STAGE_A_R1_EXECUTION_ANTIGRAVITY.md` | E16 | Esecuzione replica corretta Stage A-R1 (Antigravity) |
| `E16_TRAINING_DESIGN_PROPOSAL.md` | E16 | Proposta architetturale di training design E16 |
| `E16_WATERING_SEMANTIC_CLARIFICATION_AND_REPAIR_CODEX.md` | E16 | Chiarimento semantico watering e autorizzazione repair (Codex) |
| `KAGGRICULTURE_RICOSTRUZIONE_VENV_E_DOCUMENTAZIONE_Codex.md` | Manutenzione | Protocollo ricostruzione `.venv` riproducibile |
| `Kaggriculture_Q0_Q1_coordinates.xlsx` | Riferimento | Coordinate e mapping geometrico quadranti Q0/Q1 |
| `POST_E15_MODEL_CAPABILITY_CHECK.md` | Post-E15 | Controllo capacità operative modelli |
| `POST_E15_MODEL_SPEC_REVISION.md` | Post-E15 | Revisione indipendente MODEL_SPEC post-E15 |
