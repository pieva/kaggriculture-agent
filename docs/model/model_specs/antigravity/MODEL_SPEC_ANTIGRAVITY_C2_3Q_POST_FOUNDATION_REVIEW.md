# MODEL_SPEC Antigravity C2.1 3Q V4.0 — Post-Foundation Review

- **Agent owner:** Antigravity
- **Versione:** `ANTIGRAVITY-C2-V4.0-3Q-HIGH-DENSITY-MEGA-CLUSTER`
- **Candidate ID:** `ANTIGRAVITY_C2_V4_0_3Q_HIGH_DENSITY`
- **Stato:** IMPLEMENTED / VALIDATED / POST-FOUNDATION ACTIVE (DERIVATIVE BASELINE WITH TERMINAL LIQUIDATION)
- **Data:** 2026-09-01
- **Foundation normativa corrente:** C2.1 riconciliata (`docs/model/ontology/ONTOLOGY_C2_1.md`, `docs/model/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md`, `docs/model/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md`)
- **Foundation storica:** C2 congelata
- **Engine:** `kaggle-environments` 1.32.7, `kaggriculture` 0.1.0
- **Engine fingerprint:** `4378b60f61a3af22ed875969e1be7e7f11af0b0e050b51aa80c0778c4113207d`

---

## 1. Scopo e confini

Questo MODEL_SPEC documenta l'architettura, i parametri e le prestazioni verificate della versione **Antigravity V4.0 3Q High-Density Mega-Cluster**, integrando gli esiti della riconciliazione finale della Foundation C2.1.

La versione V4.0 è un controller ad alta densità su tre quadranti (Q0, Q1, Q2) operante su un orizzonte di 719 step, integrato con:
1. la correzione causale dell'alimentazione al giorno 8 (step 195);
2. la procedura autonoma Antigravity di liquidazione terminale dello shed agli step 717-719.

Il documento è agent-local: ontologia, macchina a stati, feature e telemetria sono condivise con la Foundation C2.1; la sequenza operativa di base deriva dalla routine distillata dal benchmark pubblico Kaggle `104498819` e condivisa via `agricola.strategy.codex_v9_routine_data`.

---

## 2. Artefatti canonici, freeze e provenance

| Artefatto | Percorso | SHA-256 |
|---|---|---|
| Source controller | `src/agricola/strategy/antigravity/antigravity_3q_high_density_v4.py` | `FBB10689DB1C8B5D9C373C0CAE52E07BF7DE171D0BD6BDB23FFF0DB2AA462952` |
| Entry point agente | `src/agricola/strategy/antigravity/agent_c2_3q_v4.py` | `9228DE905A0A7970D8A567D84E04C94325453CF9BE9C054A1689EDFCE7E5D3B5` |
| Configurazione | `configs/model_spec_c2/ANTIGRAVITY_C2_V4_0_3Q_HIGH_DENSITY_CONFIG.json` | `040816C5186ADD37BBD6FB76D9AEC4DB23ECA4362E11B4061B6DAA6349B0B8B7` |
| Freeze standalone torneo | `results/model_spec_c2/antigravity/freeze/submission_antigravity_v4_tournament.py` | `5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872` |
| Submission standalone disco | `submission/submission_antigravity.py` | `5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872` |

### Provenance e identità della routine:
```text
ROUTINE_ORIGIN: agricola.strategy.codex_v9_routine_data (distillata da replay Kaggle pubblico 104498819)
ROUTINE_LENGTH: 719
PARENT_ROUTINE_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
BEHAVIORAL_DELTA_1: Causal feed patch step 195 (WHEAT min 4, rimozione acquisto COW)
BEHAVIORAL_DELTA_2: Terminal Shed Liquidation steps 717-719 (liquidazione dinamica delle scorte)
INDEPENDENCE_STATUS: DERIVATIVE_BASELINE_WITH_TERMINAL_LIQUIDATION_DELTA
```

---

## 3. Architettura operativa

### 3.1 Forma del controller
- **Modalità primaria:** `HIGH_DENSITY_ROUTINE_WITH_TERMINAL_LIQUIDATION`;
- **Indice temporale:** `observation.step` $[0 \dots 719]$;
- **Azione base:** emissione dei comandi della sequenza ad alta densità con copia profonda e fallback di sicurezza `PASS` in caso di step fuori range o anomalie;
- **Causal Patch D8 (Step 195):** forzatura dell'acquisto di almeno 4 WHEAT e soppressione dell'acquisto sostitutivo della COW fuggita;
- **Terminal Shed Liquidation (Steps 717-719):** scansione in tempo reale dell'inventario in `private.shed` e immissione prioritaria di ordini `SELL` per tutte le merci residue (MILK, WOOL, MELON, STRAWBERRY, FERTILIZER, WHEAT, EGG), monetizzando fino a +$1.800 di cassa netta.

### 3.2 Topologia 3Q, workforce e concentrazione zootecnica

| Proprietà | Valore implementato / osservato |
|---|---:|
| Quadranti posseduti | 3 (Q0 NW, Q1 NE, Q2 SW: 75 tile) |
| Attivazione media Q1 | Giorno 6 |
| Attivazione media Q2 | Giorno 11 |
| Main Farmer (W0) | 1 (permanente, respawn a shed EOD) |
| Farm Hands (W1..W12) | 12 (ingaggiati a gradino Fibonacci, contratto giornaliero) |
| Forza lavoro totale | 13 lavoratori attivi (saturazione 100% ruoli W0..W12) |
| Picco pascoli centrali | 19 (Chebyshev $\le 2$ attorno agli shed (4,4), (5,4), (4,5)) |
| Picco animali attivi | 19 (8 Mucche, 11 Pecore) |
| Picco colture attive | 55 tile |
| Azioni produttive per match | 2.842 |
| Azioni PASS per match | 677 |
| Rapporto `MOVE / Productive` | 1,2477 |
| Fughe di animali | 0 (su tutte le 60 partite totali disputate) |

---

## 4. Contratti causali consumati dalla Foundation C2.1

Antigravity V4.0 assume e rispetta rigorosamente i contratti causali verificati dell'engine:
1. **Disciplina HIRE:** l'unico costo per i lavoratori è l'addebito Fibonacci al commit dell'ordine `HIRE`. L'engine non applica alcun salario né decurtazione monetaria a EOD.
2. **Ciclo di Vita Hands:** i lavoratori assunti operano a $t+1$ e scadono incondizionatamente all'EOD, venendo rimossi a costo zero.
3. **Alimentazione e Fuga:** l'azione `FEED` (1 Wheat) azzera `consecutive_unfed`. Se un animale rimane non alimentato per 2 EOD consecutivi (`consecutive_unfed == 2`), fugge irrimediabilmente all'EOD.
4. **Disaccoppiamento Produzione Base:** l'output di base ($1$) viene erogato a scadenza biologica se l'animale non è fuggito; `FEED` non blocca il base output ma condiziona la riscossione del care bonus.
5. **Mercato Condiviso e Lockstep:** gli ordini concorrenti vengono risolti per slot in modo order-sensitive e seat-sensitive. Le quote sono comuni prima dei commit sequenziali; `_commit_unit(BUY_PRODUCT)` verifica cassa e capienza shed ma non blocca inventario a zero (può diventare negativo).
6. **Auto-drop EOD allo Shed:** a fine giornata l'inventario dei worker viene trasferito allo shed centrale fino al limite di `shedCapacity` (100). L'eccedenza viene distrutta (`shed_overflow_loss`).

---

## 5. Contratto osservativo e deliberazione agent-local

```text
SHARED_OBSERVATION_CONTRACT: src/agricola/core/observation_contract.py
SHARED_DELIBERATION_RUNTIME: NONE
```

Antigravity V4.0 non usa una macchina deliberativa condivisa. Adapter, clock e
tipi di osservazione risiedono nel contratto neutrale; routine, priorità e
liquidazione terminale restano agent-local.

---

## 6. Risultati sperimentali congelati

### 6.1 Suite passiva canonica (6 episodi)
```text
CANONICAL_FINAL_MONEY_MEAN:    133.257,00  (+1.237,67 vs Codex V9.0)
CANONICAL_FINAL_MONEY_MEDIAN:  120.777,00
CANONICAL_FINAL_MONEY_MIN:      77.691,00
CANONICAL_FINAL_MONEY_MAX:     183.139,00  (+1.800,00 vs Codex V9.0)
ANIMAL_ESCAPES:                         0
ERRORS / FALLBACKS:                   0 / 0
MOVE_PER_PRODUCTIVE:               1,2477
```

### 6.2 Suite holdout fuori campione Phase B + Phase C (12 episodi)
```text
HOLDOUT_FINAL_MONEY_MEAN:      139.437,33  (+1.483,00 vs Codex V9.0)
HOLDOUT_FINAL_MONEY_MEDIAN:    143.130,00
HOLDOUT_FINAL_MONEY_MIN:        77.691,00
HOLDOUT_FINAL_MONEY_MAX:       183.139,00
STD:                            28.097,47
ANIMAL_ESCAPES:                         0
```

### 6.3 Torneo Triangolare Ufficiale Post-3Q (42 Match Totali)
```text
RECORD GENERALE:               26 Vittorie, 2 Sconfitte, 0 Pareggi (Win Rate: 92,86%)
CAPITALE MEDIO:                $89.280,86
SCONTRO DIRETTO VS CODEX V9:   13 Vittorie - 1 Sconfitta (Margine: +$704,57 / match)
SCONTRO DIRETTO VS COPILOT 3Q: 13 Vittorie - 1 Sconfitta (Margine: +$704,57 / match)
ANIMAL_ESCAPES:                         0
```

### 6.4 Interpretazione metodologica del torneo
Il torneo a 42 match dimostra l'efficacia empirica della procedura di liquidazione terminale (+704,57/match di margine netto) applicata alla medesima routine di base. Poiché la tabella di azioni di base è condivisa con Codex V9 e Copilot V2, questo risultato è formalmente classificato come validazione di baseline derivativa e studio di ablazione, non come confronto tra tre strategie modellate in modo reciprocamente indipendente.

---

## 7. Punti di forza e limiti

### Punti di forza:
- Efficacia empirica della liquidazione terminale dello shed nello sfruttamento delle merci invendute a fine episodio.
- Massima densità operativa (2.842 azioni produttive, MOVE/prod 1,2477).
- Zero fughe di animali, zero errori e zero fallback su 60 match totali.
- Codice standalone congelato e riproducibile via SHA-256.

### Limiti aperti:
- Condivisione della tabella di azioni aperta (`ROUTINE_ACTIONS`) importata da `codex_v9_routine_data`.
- Sensibilità alla contesa simultanea nel mirror match (due routine identiche causano cannibalizzazione di mercato).
- Floor minimo nei seed avversi ($77.691), dipendente dalle oscillazioni stocastiche dei prezzi di mercato.
- Mancanza di ripianificazione dinamica in caso di infestazioni da weed su tile critiche.

---

## 8. Gate di indipendenza strategica

```text
ROUTINE_ORIGIN: agricola.strategy.codex_v9_routine_data (distilled from replay 104498819)
PARENT_ROUTINE_SHA256: C2466262E096B03CA330A1B0FDB2E5DEBE53C45F297E046113E007731051E7E4
BEHAVIORAL_DELTA: Causal feed patch step 195 (WHEAT min 4, remove COW) + Real-time Terminal Shed Liquidation steps 717-719
INDEPENDENCE_STATUS: DERIVATIVE_BASELINE_WITH_TERMINAL_LIQUIDATION_DELTA
NO_IMPORT_OTHER_AGENT_ROUTINE: FAIL
NO_COPY_OTHER_AGENT_ACTION_TABLE: FAIL
NO_IDENTICAL_ROUTINE_SHA: FAIL
NO_THIN_WRAPPER_AS_MODEL: FAIL
PROVENANCE_DISCLOSURE: PASS
STRATEGIC_INDEPENDENCE_GATE: FAIL
```

---

## 9. Target per la successiva iterazione sperimentale indipendente (E17+)

La sequenza sperimentale riprende da E17 con l'obiettivo di sviluppare una strategia pienamente indipendente, priva di dipendenze da tabelle di azioni altrui:

```text
HOLDOUT_MEAN >= 145000
HOLDOUT_MIN >= 100000
COMPETITIVE_MIRROR_MEAN >= 85000
ANIMAL_ESCAPES == 0
MOVE_PER_PRODUCTIVE <= 1.20
INDEPENDENT_ROUTINE_PROVENANCE == YES
NO_FOREIGN_ROUTINE_IMPORT == PASS
```

---

## 10. Regole di validazione, builder e freeze

1. La freeze standalone validata è: `results/model_spec_c2/antigravity/freeze/submission_antigravity_v4_tournament.py` (SHA-256: `5786AC521DDC0931539032ED1A4D642F75846911A078E8E8E82535C7F4757872`).
2. Lo script `scripts/build_submission_antigravity_v4.py` è l'unico autorizzato a rigenerare la freeze Antigravity V4.
3. La submission canonica `submission/submission_antigravity.py` è stata promossa dalla freeze accettata ed è byte-identica ad essa; ogni futura sostituzione richiederà autorizzazione e verifica SHA-256 esplicite.

---

**Fine di MODEL_SPEC Antigravity C2.1 3Q V4.0 — Post-Foundation Review.**
