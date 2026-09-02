# Prompt operativo Antigravity — Pulizia controllata `docs/prompts/` e verifica struttura `docs/`

## Ruolo
Operi come agente di manutenzione documentale del repository **Kaggriculture**.

Questa attività è deliberatamente limitata per evitare interferenze con il lavoro sperimentale corrente di Codex su E16.

Il supervisore umano gestirà personalmente la rimozione delle directory obsolete individuate. Tu **NON devi cancellare directory** e **NON devi estendere autonomamente la pulizia ad altre aree del repository**.

## Obiettivo
Eseguire esclusivamente due attività:
1. **Razionalizzare `docs/prompts/`**, riducendo i prompt storici non più utili nel working tree.
2. **Razionalizzare `docs/versions/`**, preservando l'evidenza sperimentale e le decisioni non consolidate altrove, ma rimuovendo le micro-iterazioni puramente operative e superate.
3. **Dopo la pulizia manuale delle directory effettuata dal supervisore**, verificare che la struttura residua di `docs/` sia coerente e che non esistano riferimenti rotti evidenti.

## Vincoli non negoziabili
NON modificare:
- codice sorgente;
- test;
- `results/` e in particolare `results/e16/`;
- MODEL_SPEC;
- ontology;
- freeze artifacts;
- tournament artifacts;
- policy sperimentali;
- configurazioni degli esperimenti;
- artefatti della forensic diagnosis E16 prodotti da Codex;
- `PROJECT_STATE.md`, `NEW_SESSION.md` o `EXPERIMENT_LOG.md`, salvo richiesta esplicita successiva.

NON fare:
- NON cancellare directory.
- NON spostare o rinominare directory.
- NON creare una nuova tassonomia generale di `docs/`.
- NON fare refactoring documentale fuori da `docs/prompts/` e `docs/versions/`.
- NON modificare contenuti E14–E16 salvo eventuale indice dei prompt.
- NON toccare file modificati da Codex o da altre attività concorrenti.
- NON eseguire commit finché non hai completato tutte le verifiche.

In caso di dubbio su un file: **KEEP**.

## Regola di conservazione dei prompt

### Fasi storiche precedenti a E14
Per ogni fase/esperimento storico conserva nel working tree **un solo prompt canonico**, scelto in base al valore documentale effettivo:
- mandato finale della fase;
- prompt che ha guidato la versione effettivamente implementata;
- oppure prompt che documenta la decisione metodologica conclusiva.

Non scegliere automaticamente l'ultimo file solo perché più recente.

I prompt intermedi, duplicati, preparatori o correttivi completamente superati possono essere rimossi dal working tree: restano recuperabili nella Git history.

### E14–E16
Applica una policy **conservativa** per i prompt legati a:
- ontologia;
- MODEL_SPEC indipendenti;
- review;
- freeze;
- torneo;
- training design;
- execution;
- forensic analysis;
- repair.

Default:
```text
KEEP
```

Non consolidare prompt che rappresentano ruoli o passaggi metodologici distinti. Rimuovi un prompt E14–E16 solo se è un duplicato manifesto o chiaramente accidentale, documentandone la motivazione.


## Regola di conservazione di `docs/versions/`

`docs/versions/` contiene una stratificazione di micro-iterazioni sperimentali. Non deve essere trattata come una directory da cancellare integralmente.

### E01–E13

Per ogni esperimento/fase conserva soltanto i documenti che abbiano ancora almeno una delle seguenti funzioni:

- evidenza sperimentale quantitativa non consolidata altrove;
- risultato o confronto significativo;
- audit/forensic analysis con valore metodologico;
- decisione sperimentale importante;
- validazione esterna;
- sintesi conclusiva necessaria per ricostruire cosa è stato appreso.

Sono candidati alla rimozione:

- specifiche di micro-iterazioni ormai superate;
- documenti puramente operativi;
- piani intermedi;
- preparazioni di submission ormai storiche;
- istruzioni di implementazione replicate altrove;
- versioni X1.x/Xn.x il cui contenuto utile è già consolidato in `EXPERIMENT_LOG`, documenti conclusivi o altre fonti canoniche.

Non assumere che ogni file `X1.x` debba essere eliminato: valuta il contenuto.

### E14–E16

Applica anche qui una policy conservativa:

```text
KEEP
```

Preserva documenti che appartengono al nuovo ciclo metodologico basato su ontologia, MODEL_SPEC, freeze, tournament/training evidence, execution, forensic diagnosis e repair.

### Principio di sicurezza

Prima di eliminare un file da `docs/versions/`, verifica se costituisce l'unica fonte documentale di un risultato, una metrica, una decisione o un'analisi significativa.

Se non puoi dimostrare che l'informazione importante è consolidata altrove:

```text
KEEP_UNCERTAIN
```

La Git history è archivio storico, ma non deve essere usata come giustificazione per eliminare evidenza sperimentale non consolidata.


## Workflow obbligatorio

### STEP 0 — Preflight
Esegui:
```powershell
git branch --show-current
git status --short
git log -1 --oneline
```

Se trovi modifiche concorrenti, non toccarle e non includerle nel commit.

### STEP 1 — Inventory `docs/prompts/`
Per ogni file determina:
- nome;
- fase/esperimento;
- agente destinatario;
- ruolo;
- stato proposto:
  - `KEEP_CANONICAL`
  - `KEEP_METHOD`
  - `DELETE_HISTORICAL_REDUNDANT`
  - `KEEP_UNCERTAIN`
- breve motivazione.

### STEP 2 — Pulizia autorizzata
Procedi esclusivamente dentro:
```text
docs/prompts/
```

Per le fasi pre-E14:
- mantieni un solo prompt canonico per fase/esperimento quando possibile;
- elimina prompt intermedi chiaramente superati;
- conserva ciò che non puoi classificare con sufficiente sicurezza.

Per E14–E16:
- conserva i prompt metodologicamente distinti;
- non comprimere proposal/review/freeze/execution/forensic/repair in un unico file.

### STEP 3 — Inventory e razionalizzazione `docs/versions/`

Inventaria tutti i file di `docs/versions/`.

Per ciascuno determina almeno:

- nome;
- esperimento/fase;
- tipo di documento;
- informazione/evidenza distintiva;
- presenza o assenza di consolidamento altrove;
- stato proposto:
  - `KEEP_EVIDENCE`
  - `KEEP_METHOD`
  - `DELETE_OPERATIONAL_REDUNDANT`
  - `KEEP_UNCERTAIN`
- breve motivazione.

Procedi quindi alla pulizia secondo la policy sopra definita.

L'obiettivo NON è raggiungere un numero prefissato di file, ma eliminare la stratificazione operativa preservando la memoria sperimentale utile.

### STEP 4 — Indice dei prompt
Se esiste un README/indice in `docs/prompts/`, aggiornalo. Altrimenti crea:
```text
docs/prompts/README.md
```

Deve contenere:
1. scopo della directory;
2. policy di conservazione;
3. distinzione tra prompt canonici storici e prompt metodologici E14–E16;
4. elenco sintetico dei file conservati;
5. nota che i prompt rimossi restano disponibili tramite Git history.

### STEP 5 — Verifica post-pulizia di `docs/`
Il supervisore umano eliminerà personalmente le directory obsolete già individuate.

Dopo tale intervento:
- inventaria le directory immediatamente sotto `docs/`;
- NON cancellarne altre;
- verifica soltanto:
  - directory vuote;
  - nomi chiaramente incoerenti;
  - riferimenti Markdown evidenti a directory/file che non esistono più;
  - link relativi rotti nei documenti attivi;
  - README/indici che citano directory rimosse.

Se individui problemi fuori da `docs/prompts/`, riportali come `FOLLOW-UP` e non intervenire automaticamente, salvo link/indice chiaramente innocuo e strettamente documentale.

## Verifica riferimenti
Classifica i riferimenti trovati come:
- `ACTIVE_REFERENCE`
- `HISTORICAL_REFERENCE`
- `BROKEN_REFERENCE`
- `BENIGN_TEXT_REFERENCE`

Correggi automaticamente solo riferimenti chiaramente rotti nella documentazione attiva e non protetta.

Non riscrivere retroattivamente report sperimentali storici solo per eliminare una menzione.

## Verifiche finali
Esegui almeno:
```powershell
git diff --check
git status --short
```

Non lanciare benchmark o episodi.

## Commit
Questa attività deve restare in un commit autonomo e reversibile.

Commit suggerito:
```text
chore: consolidate historical prompts
```

Prima del commit verifica che:
- siano inclusi solo file relativi alla pulizia documentale autorizzata;
- non siano inclusi output/modifiche di Codex;
- non siano inclusi file sperimentali;
- non siano incluse accidentalmente altre modifiche concorrenti.

Se non puoi isolare con sicurezza il commit, **NON fare commit**.

## Report finale
Riporta:
1. numero iniziale di file in `docs/prompts/`;
2. numero finale;
3. prompt mantenuti per fase storica;
4. prompt E14–E16 mantenuti;
5. file rimossi da `docs/prompts/`;
6. file dubbi mantenuti per prudenza;
7. numero iniziale e finale di file in `docs/versions/`;
8. file `docs/versions/` mantenuti come evidenza/metodo;
9. file `docs/versions/` rimossi come micro-iterazioni operative ridondanti;
10. eventuali `KEEP_UNCERTAIN` in `docs/versions/`;
11. verifica delle directory `docs/` dopo la pulizia manuale;
12. riferimenti rotti trovati;
13. correzioni effettuate;
14. follow-up consigliati ma NON eseguiti;
15. esito `git diff --check`;
16. eventuali test eseguiti;
17. commit creato, se creato;
18. `git status --short` finale.

## Stop condition
Dopo la pulizia di `docs/prompts/`, la razionalizzazione prudenziale di `docs/versions/` e la verifica post-pulizia di `docs/`:

**FERMATI.**

Non avviare ulteriori razionalizzazioni o refactoring del repository. Attendi la revisione del supervisore.
