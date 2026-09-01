# MODEL_SPEC Codex C2.1 3Q V9 — Post-Foundation Review

- **Agent owner:** Codex
- **Versione:** `CODEX-C2-V9.0-3Q-MIXED-HIGH-DENSITY`
- **Stato:** IMPLEMENTED / VALIDATED / POST-FOUNDATION ACTIVE
- **Data:** 2026-09-01
- **Foundation normativa corrente:** C2.1 riconciliata
- **Foundation storica:** C2 congelata
- **Engine:** `kaggle-environments` 1.32.7, `kaggriculture` 0.1.0
- **Engine fingerprint:** `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`

---

## 1. Scopo e confini

Questo MODEL_SPEC descrive l'implementazione Codex V9 effettivamente eseguita, non una policy ideale. La V9 è un controller 3Q ad alta densità basato su una routine open-loop di 719 step, con una correzione causale al feed del giorno 8 e fallback sicuro `PASS` fuori orizzonte. Il documento incorpora la chiusura della revisione Foundation C2.1.

Il documento è agent-local: ontologia, macchina a stati, feature e telemetria possono essere comuni; sequenza di azioni, priorità, cadenza, planner e routine restano proprietà esclusiva di Codex. Nessun altro agente può usare questa routine come base della propria implementazione se il risultato deve valere come confronto strategicamente indipendente.

## 2. Artefatti canonici e provenance

| Artefatto | Percorso | SHA-256 |
|---|---|---|
| Source controller | `src/agricola/strategy/codex_3q_mixed_high_density.py` | `21C58DD9F95F252380F6B700470FCB3D737CFCD9F0765EFAF984DB3B74090D1A` |
| Routine data | `src/agricola/strategy/codex_v9_routine_data.py` | `AC5819014EBB85ED86BA5D25D4F01DE46F9E4760465B7188DF11E69C8812F774` |
| Config | `configs/model_spec_c2/CODEX_C2_V9_0_3Q_MIXED_HIGH_DENSITY_CONFIG.json` | `44DD0EC2F33C9EEEE74AE5676580DC833325AB969D8A9D262EC870FEAAAC6C99` |
| Freeze standalone torneo | `results/model_spec_c2/codex/freeze/submission_codex_v9_tournament.py` | `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421` |
| Submission canonica corrente | `submission/submission_codex.py` | `AC541588EF9746F00C9FE6CDA378DB4DF793347CDB5FEE8FF2FCA5EC1847C421` |

Identità della sequenza strategica:

```text
ROUTINE_LENGTH: 719
ROUTINE_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
```

La routine deriva dalla distillazione sperimentale del replay Kaggle pubblico `104498819`, poi corretta e validata fuori campione. Questa provenienza va dichiarata; non equivale a riuso della routine privata di un altro agente del repository.

## 3. Architettura operativa

### 3.1 Forma del controller

- modalità primaria: `OPEN_LOOP_ROUTINE`;
- indice: `observation.step`;
- azione emessa: copia profonda della voce `ROUTINE_ACTIONS[step]`;
- guardia: `PASS` sicuro per step fuori range o observation non utilizzabile;
- patch causale: acquisto di una unità WHEAT aggiuntiva allo step 195 e rimozione dell'acquisto simultaneo della COW che sostituiva l'animale fuggito;
- assenza di apprendimento online e di replanning generale.

### 3.2 Topologia 3Q e densità

| Proprietà | Valore implementato/osservato |
|---|---:|
| Quadranti posseduti | 3 |
| Attivazione media Q1 | giorno 6 |
| Attivazione media Q2 | giorno 11 |
| Farmer permanenti | 1 |
| Hands di picco | 12 |
| Workforce totale di picco | 13 |
| Crop di picco | 55 |
| Animali di picco | 19 |
| Mix target config | 17 MELON, 27 STRAWBERRY, 12 WHEAT |
| Livestock target config | 6 COW, 11 SHEEP |

La differenza tra target configurato e picco osservato è registrata, non occultata: la correzione zero-escape elimina un acquisto COW e lascia il picco a 19 animali.

## 4. Contratto causale ed economico

La V9 assume e rispetta i seguenti fatti engine-verificati:

1. `HIRE` addebita il costo Fibonacci al commit dell'ordine; non esistono salario, wage floor o addebito ricorrente a EOD;
2. gli Hands diventano operativi alla transizione successiva e scadono a EOD;
3. il mercato è condiviso, dinamico e order-sensitive; quantità richiesta e prezzo quotato non garantiscono quantità e valore realizzati;
4. le azioni simultanee avversarie del medesimo slot non sono osservabili prima della risoluzione;
5. un animale fugge al secondo EOD consecutivo senza `FEED`;
6. la produzione base animale è separata dal feed, mentre il feed previene la fuga e condiziona il bonus di care;
7. gli overflow da `DROP` distruttivo o auto-drop EOD possono cancellare inventario.

La routine non usa come input online outcome futuri o telemetria post-hoc. I contatori di vendite, raccolte e ordini nel report descrivono richieste della routine salvo dove un ledger executed dichiara esplicitamente il contrario.

## 5. Contratto osservativo e deliberazione agent-local

```text
SHARED_OBSERVATION_CONTRACT: src/agricola/core/observation_contract.py
SHARED_DELIBERATION_RUNTIME: NONE
```

La V9 usa soltanto clock, snapshot, hashing e normalizzazione del contratto osservativo neutrale. La vecchia macchina condivisa di deliberazione è stata rimossa dopo la migrazione dei consumer e i test di parità. Planner, priorità e routine rimangono responsabilità esclusiva del MODEL_SPEC e del codice Codex.

## 6. Risultati congelati

### 6.1 Suite passiva canonica, 6 episodi

| KPI | Risultato |
|---|---:|
| Media final money | 132.019,33 |
| Mediana | 119.676 |
| Minimo | 77.542 |
| Massimo | 181.339 |
| Fughe | 0 |
| Errori/fallback | 0/0 |
| MOVE / productive | 1,2477 |

### 6.2 Holdout Phase B+C, 12 episodi

| KPI | Risultato |
|---|---:|
| Media final money | 137.954,33 |
| Mediana | 141.391 |
| Minimo | 77.542 |
| Massimo | 181.339 |
| Deviazione standard | 27.703,22 |
| Fughe | 0 |

### 6.3 Torneo V9 precedente, 42 match

Codex ha chiuso 28-0 contro le versioni allora congelate di Antigravity e Copilot, con media competitiva 106.836,43 e minimo 70.631. Questo risultato misura il vantaggio rispetto a quei candidati, non il confronto con le successive V4/V2 che hanno incorporato la routine Codex.

## 7. Diagnosi delle prestazioni

Punti di forza:

- densità produttiva elevata su tre quadranti;
- 2.842 azioni produttive nella telemetria di riferimento;
- rapporto `MOVE/productive` 1,2477;
- zero fughe dopo la correzione causale;
- bassa sensibilità al seat nel torneo precedente;
- submission standalone e hashabile, senza import dal repository.

Limiti:

- dipendenza temporale rigida e bassa reattività a weed, ordini respinti e stato avversario;
- floor passivo 77.542, inferiore al gate prudenziale 85K;
- replay specchio 46.251 per cannibalizzazione simmetrica del mercato;
- contatori requested non sempre equivalenti a quantità executed;
- una routine identica adottata dai rivali rende non identificabile il contributo della strategia nei confronti successivi.

## 8. Gate di indipendenza strategica

Per ogni futuro torneo dichiarato indipendente:

```text
NO_IMPORT_OTHER_AGENT_ROUTINE: REQUIRED
NO_COPY_OTHER_AGENT_ACTION_TABLE: REQUIRED
NO_IDENTICAL_ROUTINE_SHA: REQUIRED
NO_THIN_WRAPPER_AS_INDEPENDENT_MODEL: REQUIRED
PROVENANCE_DISCLOSURE: REQUIRED
```

Un nome di classe, una configurazione o una liquidazione terminale differente non rendono indipendente un agente che importa o copia la stessa tabella di azioni. Dataset, engine facts, schema di telemetria e benchmark Kaggle pubblici possono essere comuni; la derivazione della policy deve restare separata.

## 9. Target della prossima iterazione Codex

La V9.1 deve lavorare sul floor e sulla contesa, non sull'espansione nominale:

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR >= 90000
ANIMAL_ESCAPES == 0
MOVE_PER_PRODUCTIVE <= 1.20
EXECUTED_MARKET_LEDGER_COVERAGE == 100%
```

La via preferita è una routine ibrida: mantenere il nucleo denso validato e introdurre soltanto guardie causali su fill di mercato, stock WHEAT, weed e desincronizzazione.

## 10. Regole di validazione e promozione

Prima della promozione di una variante:

1. congelare source, config, routine e standalone con SHA-256;
2. verificare import isolato e parità azione-per-azione;
3. eseguire canonical, holdout e torneo seat-balanced su seed preregistrati;
4. registrare quantità richieste ed eseguite separatamente;
5. registrare fughe, overflow, errori e fallback;
6. non sovrascrivere `submission/submission_codex.py` mediante builder o test legacy;
7. non selezionare seed o match dopo aver osservato i risultati.

## 11. Stato della Foundation

Ontology, State Machine e Feature Model C2.1 sono stati riconciliati dopo i feedback indipendenti di Antigravity e Copilot. La revisione Foundation post-3Q è chiusa; la sequenza sperimentale riprenderà dal primo esperimento successivo a E16, senza usare la Foundation per omogeneizzare le strategie.

Il torneo di chiusura post-3Q ha confermato la stabilità tecnica ma non l'indipendenza strategica dei rivali correnti: Codex e Copilot sono equivalenti azione-per-azione, mentre Antigravity aggiunge liquidazione terminale alla stessa routine. I risultati sono quindi baseline di replica, non attribuzione a tre modelli indipendenti.

---

**Fine di MODEL_SPEC Codex C2.1 3Q V9 — Post-Foundation Review.**
