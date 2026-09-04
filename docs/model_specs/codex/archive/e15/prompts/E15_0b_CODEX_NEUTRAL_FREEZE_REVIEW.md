# E15.0b — Neutral Freeze Review pre-torneo — CODEX

## Obiettivo

Eseguire una review indipendente e rigorosamente **READ-ONLY** dell'intero freeze E15 prima di autorizzare M1.

Questa fase NON serve a:

- migliorare i modelli;
- correggere le submission;
- modificare il runner;
- modificare il piano del torneo;
- produrre nuovi benchmark;
- eseguire match.

Devi stabilire esclusivamente se il pacchetto E15 congelato è integro, coerente, riproducibile e sufficientemente neutrale da poter autorizzare il torneo.

Il tuo ruolo in questa fase è quello di **reviewer neutrale dell'infrastruttura**, non quello di partecipante Codex al torneo.

---

## 1. Safety — READ ONLY

Prima di qualsiasi verifica esegui:

```powershell
git status --short
git branch --show-current
git log -1 --oneline
```

VINCOLO ASSOLUTO:

**NON MODIFICARE ALCUN FILE.**

Non creare report nel repository.
Non creare script temporanei nel repository.
Non creare memory file.
Non aggiornare documentazione.

Se hai bisogno di calcoli temporanei, eseguili inline oppure fuori dal repository senza lasciare artefatti.

NON eseguire:

```text
git reset
git clean
git stash
git revert
```

NON fare:

- commit;
- push;
- Kaggle upload;
- build;
- rebuild;
- benchmark competitivo;
- M1;
- M2;
- M3.

NON correggere eventuali problemi trovati.

Documentali e fermati.

---

# 2. Artefatti da verificare

Esamina almeno:

```text
docs/model_specs/ONTOLOGY.md

docs/model_specs/antigravity/MODEL_SPEC.md
docs/model_specs/codex/MODEL_SPEC.md
docs/model_specs/copilot/MODEL_SPEC.md

experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py
submission/submission_codex.py
submission/submission_copilot.py

experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md

experiments/archive/e15/artifacts/freeze/ONTOLOGY_E15_FROZEN.md
experiments/archive/e15/artifacts/freeze/MODEL_SPEC_ANTIGRAVITY_E15_FROZEN.md
experiments/archive/e15/artifacts/freeze/MODEL_SPEC_CODEX_E15_FROZEN.md
experiments/archive/e15/artifacts/freeze/MODEL_SPEC_COPILOT_E15_FROZEN.md
experiments/archive/e15/artifacts/freeze/submission_antigravity_E15_FROZEN.py
experiments/archive/e15/artifacts/freeze/submission_codex_E15_FROZEN.py
experiments/archive/e15/artifacts/freeze/submission_copilot_E15_FROZEN.py

experiments/archive/e15/artifacts/P0_P1_ENVIRONMENT_AUDIT.md
experiments/archive/e15/artifacts/TOURNAMENT_PLAN.md
experiments/archive/e01/tools/run_e15_tournament.py
```

Individua inoltre l'eventuale report creato da Copilot durante E15.0a:

```text
E15_0a_OWNERSHIP_VERIFICATION_REPORT.md
```

o nome/path equivalente.

Individua anche eventuali altri file creati da Copilot durante E15.0a, incluso l'eventuale "memory file".

NON modificarli e NON eliminarli.

---

# 3. Verifica cardinalità ontologia e MODEL_SPEC

Verifica che:

```text
ONTOLOGY canonical registry = 64 concept_id
```

e che ciascun MODEL_SPEC frozen copra esattamente:

```text
64/64
```

Controlla:

- concept_id mancanti;
- concept_id extra;
- duplicati;
- `USED + PARTIAL + NOT_USED = 64`;
- eventuali `CONFLICT`.

Non rivalutare le scelte epistemiche dei tre modelli.

Non modificare ranking, impact, confidence o policy.

Questa verifica serve esclusivamente a confermare che il freeze rappresenti correttamente i tre modelli pre-match.

---

# 4. Verifica SHA256 del freeze

Ricalcola SHA256 direttamente dai sette file frozen.

Confrontali con:

```text
experiments/archive/e15/artifacts/freeze/FREEZE_MANIFEST.md
```

Gli hash dichiarati al momento del freeze sono:

```text
ONTOLOGY
5bab9c13cbf6d88b818ad6aca401fdb9bacc811d656dab4e39fe7d8c634e0bfa

MODEL_SPEC Antigravity
f4eb68d232586394ae83399ddc4405cf211ead57e3afa183c655611eb6943a46

MODEL_SPEC Codex
9e38dfe16b5e22b47df890abc105519920f5987de683e9da22638c0a5a57aed7

MODEL_SPEC Copilot
d08dde958f929dab1a28f6a92343618d4b31a5b3cc12cf10c6673c92900d0686

Submission Antigravity
629c017271891e0b7d7a4b0e655df40b0aac66ee8af1bc00d5718fb8bdfd404d

Submission Codex
fe269bf365dd7167644e5867ca857f1f77d4009f9ce66c0e2afa3e78d6a4c9f3

Submission Copilot
604bd6201df08b3c4dbfb00c2e49bf8963c7a32b6bba6e14c04d046e308b8abb
```

Per ogni artefatto indica:

```text
MATCH
MISMATCH
```

Se anche un solo frozen artifact non corrisponde al manifest:

NON correggere.
NON rigenerare il freeze.

Il verdict non può essere `ACCEPT_E15_FREEZE`.

---

# 5. Verifica source ↔ frozen

Confronta byte-for-byte o tramite SHA256:

```text
docs/model_specs/ONTOLOGY.md
↔ experiments/archive/e15/artifacts/freeze/ONTOLOGY_E15_FROZEN.md

docs/model_specs/antigravity/MODEL_SPEC.md
↔ frozen Antigravity MODEL_SPEC

docs/model_specs/codex/MODEL_SPEC.md
↔ frozen Codex MODEL_SPEC

docs/model_specs/copilot/MODEL_SPEC.md
↔ frozen Copilot MODEL_SPEC

experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py
↔ frozen Antigravity submission

submission/submission_codex.py
↔ frozen Codex submission

submission/submission_copilot.py
↔ frozen Copilot submission
```

Classifica ciascuna coppia:

```text
IDENTICAL
DIFFERENT_POST_FREEZE
```

Una differenza post-freeze NON implica automaticamente freeze invalido:

il frozen artifact resta il riferimento autoritativo.

Ma devi documentare qualsiasi differenza e verificare soprattutto che il runner utilizzi effettivamente l'artefatto congelato corretto.

---

# 6. Review dell'intervento Antigravity sulla candidate Copilot

Durante E15.0 Antigravity ha:

1. modificato `scripts/build_submission_copilot.py`;
2. ricostruito `submission/submission_copilot.py`;
3. verificato la candidate;
4. rigenerato il freeze.

Successivamente Copilot ha effettuato E15.0a e ha dichiarato:

```text
ACCEPT_FREEZE
```

confermando che la candidate congelata rappresenta fedelmente la propria strategia pre-match e che le modifiche erano packaging/build-only.

Verifica indipendentemente che questa conclusione sia plausibile sulla base degli artefatti disponibili.

NON devi rifare un audit strategico completo di Copilot.

Controlla però che non emerga evidenza contraria evidente, ad esempio:

- parametri strategici cambiati;
- classi sostituite;
- policy aggiunte;
- soglie cambiate;
- configurazioni alterate;
- logica decisionale diversa;
- componenti Copilot rimosse o sostituite.

Classifica:

```text
COPILOT_OWNERSHIP_ACCEPTANCE_CONFIRMED
COPILOT_OWNERSHIP_ACCEPTANCE_CONTRADICTED
COPILOT_OWNERSHIP_ACCEPTANCE_NOT_VERIFIABLE
```

---

# 7. Audit degli artefatti creati impropriamente in E15.0a

Il prompt E15.0a era READ-ONLY, ma Copilot ha dichiarato di aver creato:

- `E15_0a_OWNERSHIP_VERIFICATION_REPORT.md`;
- un "memory file".

Individua esattamente cosa è stato creato.

Per ogni file classifica:

```text
AUDIT_TRAIL_ONLY
POTENTIALLY_MUTATING_TOURNAMENT_STATE
UNKNOWN
```

Un report descrittivo che non viene letto dal runner e non modifica model/submission/freeze può essere classificato `AUDIT_TRAIL_ONLY`.

Verifica che nessun file creato da E15.0a:

- sia importato dal runner;
- sia incluso nelle submission;
- modifichi seed;
- modifichi freeze;
- modifichi MODEL_SPEC;
- modifichi strategie;
- modifichi configurazioni del torneo.

NON eliminare nulla.

---

# 8. Review P0/P1 environment audit

Esamina criticamente:

```text
experiments/archive/e15/artifacts/P0_P1_ENVIRONMENT_AUDIT.md
```

e verifica direttamente nell'environment le affermazioni principali.

Controlla almeno:

- ordine di inizializzazione P0/P1;
- ordine di esecuzione delle action;
- ordine di BUY;
- ordine di SELL;
- ordine di HIRE;
- market price update;
- eventuali risorse condivise;
- tie-breaking;
- RNG;
- consumo RNG;
- eventuale first-mover advantage;
- eventuale last-mover advantage;
- market order limits;
- action/order slot pressure.

Non assumere che il report Antigravity sia corretto.

Verificalo contro il codice dell'environment.

Assegna uno dei seguenti verdict:

```text
NO_MATERIAL_POSITION_BIAS_FOUND
POTENTIAL_POSITION_BIAS
MATERIAL_POSITION_BIAS_FOUND
INCONCLUSIVE
```

Se il risultato differisce dal report Antigravity, spiega esattamente perché.

---

# 9. Review RNG e seed

Verifica:

- inizializzazione RNG;
- relazione tra seed e traiettoria;
- eventuale consumo RNG dipendente dalle action degli agenti;
- se stesso seed in match differenti garantirebbe o meno traiettorie direttamente comparabili.

Conferma che i tre seed siano stati pre-dichiarati prima dei risultati:

```text
M1 = 1113294977
M2 = 3033283457
M3 = 3122977751
```

Verifica che siano:

- distinti;
- registrati nel `TOURNAMENT_PLAN.md`;
- associati ai match corretti;
- non modificati dinamicamente dal runner;
- non soggetti a reroll automatico.

---

# 10. Review del Tournament Plan

Esamina:

```text
experiments/archive/e15/artifacts/TOURNAMENT_PLAN.md
```

Deve dichiarare esattamente:

```text
M1: Antigravity P0 vs Codex P1
M2: Codex P0 vs Copilot P1
M3: Copilot P0 vs Antigravity P1
```

Ogni agente deve giocare:

```text
1 volta P0
1 volta P1
```

Verifica il criterio classifica:

Primary:

```text
numero vittorie head-to-head
```

Tie se tutti 1–1:

```text
aggregate signed final-money differential
```

con:

```text
D_i = Σ(final_money_i - final_money_opponent)
```

Non devono esserci:

- quarto match automatico;
- mirrored match automatici;
- reroll automatici;
- tie-break aggiunti dopo i risultati.

---

# 11. Review critica del runner

Esamina integralmente:

```text
experiments/archive/e01/tools/run_e15_tournament.py
```

Questa è una verifica prioritaria.

Devi stabilire con certezza quali file vengono realmente eseguiti.

## 11.1 Artefatti autoritativi

Il runner deve garantire che il match corrisponda alle submission congelate.

La soluzione preferibile è l'esecuzione diretta di:

```text
results/e15/freeze/submission_*_E15_FROZEN.py
```

oppure, se utilizza i file live:

```text
submission/submission_*.py
```

deve prima verificare SHA256 contro il manifest e rifiutarsi di eseguire in caso di mismatch.

NON accettare un runner che esegua silenziosamente una candidate live diversa dal freeze.

---

## 11.2 MODEL_SPEC e ontologia

Verifica che metadata e analisi futura facciano riferimento agli SHA256 frozen corretti.

Il runner NON deve modificare:

- ONTOLOGY;
- MODEL_SPEC;
- submission frozen;
- freeze manifest.

---

## 11.3 Invocazione esplicita

Verifica che:

```text
--match M1
--match M2
--match M3
```

o interfaccia equivalente richieda una scelta esplicita.

Importare il modulo NON deve avviare un match.

Eseguire `--validate` NON deve avviare un match.

Non deve esistere un comportamento implicito:

```text
run all matches
```

senza richiesta esplicita.

---

## 11.4 Seed enforcement

Verifica che:

```text
M1 -> 1113294977
M2 -> 3033283457
M3 -> 3122977751
```

siano hard-bound o comunque verificati.

L'utente non deve poter cambiare accidentalmente il seed attraverso un default ambiguo.

Non deve esserci reroll.

---

## 11.5 Output isolation

Verifica che M1, M2 e M3 scrivano in directory separate:

```text
results/e15/M1_antigravity_vs_codex/
results/e15/M2_codex_vs_copilot/
results/e15/M3_copilot_vs_antigravity/
```

e non sovrascrivano:

- freeze;
- risultati di altri match;
- E13/E14.

---

## 11.6 Metadata

Verifica che `match_metadata.json` registri almeno:

```text
match_id
seed
player_0
player_1
submission_0_sha256
submission_1_sha256
ontology_sha256
model_spec_0_sha256
model_spec_1_sha256
environment/version info
start timestamp
end timestamp
```

Gli hash devono corrispondere agli artefatti realmente eseguiti.

---

## 11.7 Replay e telemetry

Verifica che il runner preservi almeno:

```text
raw_replay.json
telemetry.json
summary.json
match_metadata.json
```

oppure equivalenti chiaramente documentati.

Il replay raw non deve essere distruttivamente trasformato.

Le metriche non osservabili NON devono essere inventate.

---

# 12. Controllo assenza di contaminazione post-freeze

Verifica se, dopo la creazione del freeze:

- MODEL_SPEC sono stati sostanzialmente modificati;
- submission sono state sostanzialmente modificate;
- strategy sono state modificate;
- runner usa file non congelati;
- seed sono cambiati;
- tournament plan è cambiato in modo sostanziale.

Distingui:

```text
HARMLESS_POST_FREEZE_CHANGE
MATERIAL_POST_FREEZE_CHANGE
NO_POST_FREEZE_CHANGE
UNKNOWN
```

Non correggere.

---

# 13. Non eseguire match

Puoi:

- leggere file;
- calcolare hash;
- confrontare file;
- importare/parlare staticamente del runner;
- usare modalità `--validate` SOLO se hai verificato dal codice che non esegua episodi;
- eseguire controlli statici/read-only.

NON puoi:

- eseguire M1;
- eseguire M2;
- eseguire M3;
- eseguire un match equivalente con gli stessi concorrenti;
- fare benchmark competitivo anticipato.

---

# 14. Criteri per ACCEPT_E15_FREEZE

Puoi assegnare:

```text
ACCEPT_E15_FREEZE
```

solo se TUTTE le condizioni seguenti sono soddisfatte:

1. 7/7 hash frozen corrispondono al manifest;
2. ontologia = 64 concept_id;
3. tre MODEL_SPEC frozen = 64/64;
4. ownership Copilot non è contraddetta;
5. eventuali file creati in E15.0a non mutano il torneo;
6. non emerge material P0/P1 bias incompatibile con il disegno a tre match;
7. seed sono corretti e immutabili;
8. tournament plan è coerente;
9. runner esegue esattamente gli artefatti frozen oppure ne verifica obbligatoriamente gli hash;
10. runner non esegue match implicitamente;
11. output dei match sono isolati;
12. metadata permettono la verifica della provenienza;
13. nessuna modifica post-freeze altera sostanzialmente uno dei concorrenti.

---

# 15. Verdict finale

Usa ESATTAMENTE uno:

```text
ACCEPT_E15_FREEZE
REJECT_E15_FREEZE
INCONCLUSIVE
```

### `ACCEPT_E15_FREEZE`

Solo se il torneo può essere autorizzato senza modifiche.

### `REJECT_E15_FREEZE`

Se trovi un problema concreto che compromette integrità, neutralità, provenienza o riproducibilità.

### `INCONCLUSIVE`

Se non disponi di evidenza sufficiente per stabilire che il freeze sia valido.

NON correggere il problema anche se è banale.

---

# 16. Risposta finale richiesta

Riporta esclusivamente:

## A. Verdict

```text
ACCEPT_E15_FREEZE
REJECT_E15_FREEZE
INCONCLUSIVE
```

## B. Freeze integrity

Tabella dei 7 artefatti:

```text
artifact | expected SHA256 | observed SHA256 | MATCH/MISMATCH
```

## C. Source ↔ frozen

Per ciascuno dei 7:

```text
IDENTICAL
DIFFERENT_POST_FREEZE
```

## D. Model audit

```text
Antigravity: 64/64
Codex: 64/64
Copilot: 64/64
```

con conteggi usage verificati.

## E. Copilot ownership

Uno tra:

```text
COPILOT_OWNERSHIP_ACCEPTANCE_CONFIRMED
COPILOT_OWNERSHIP_ACCEPTANCE_CONTRADICTED
COPILOT_OWNERSHIP_ACCEPTANCE_NOT_VERIFIABLE
```

## F. E15.0a extra artifacts

Elenco file individuati e classificazione.

## G. P0/P1 verdict

Uno tra:

```text
NO_MATERIAL_POSITION_BIAS_FOUND
POTENTIAL_POSITION_BIAS
MATERIAL_POSITION_BIAS_FOUND
INCONCLUSIVE
```

## H. RNG / seed review

Conferma o problema rilevato per:

```text
M1 1113294977
M2 3033283457
M3 3122977751
```

## I. Runner review

Riporta esplicitamente:

- quali submission esegue realmente;
- come verifica gli hash;
- se `--validate` è non competitivo;
- se ogni match richiede invocazione esplicita;
- se gli output sono isolati;
- se i metadata registrano gli hash degli artefatti realmente usati.

## J. Post-freeze contamination

Uno tra:

```text
NO_POST_FREEZE_CHANGE
HARMLESS_POST_FREEZE_CHANGE
MATERIAL_POST_FREEZE_CHANGE
UNKNOWN
```

## K. Blocking issues

Elenca soltanto problemi che impediscono l'avvio di M1.

Se nessuno:

```text
NONE
```

## L. Conferme finali

Riporta:

```text
NESSUN FILE MODIFICATO
NESSUN MATCH E15 ESEGUITO
NESSUN COMMIT
NESSUN PUSH
```

Infine:

```text
git status --short
```

Non modificare nulla.
Non correggere nulla.
Fermati e attendi approvazione.
