# E14 --- Repository Isolation, Independent MODEL_SPEC & Evidence Backfill --- Copilot

## Ruolo

Sei **Copilot**. Devi riorganizzare esclusivamente il tuo perimetro del
repository Kaggriculture e trasformare il tuo MODEL_SPEC in una
specifica indipendente, empiricamente verificabile e aperta
all'introduzione o riformulazione di parametri quando le evidenze
accumulate lo richiedono.

Questa fase è di **repository/model governance e analisi**, non di nuova
ottimizzazione della strategia. Non implementare nuove policy E14 solo
perché sembrano promettenti.

Repository root:

`C:\Users\pietr\Projects\kaggriculture-agent`

## Obiettivi

1.  Ridurre al minimo la contaminazione tra Antigravity, Codex e Copilot
    dal modello concettuale fino al bundle di submission.
2.  Creare/mantenere un MODEL_SPEC autonomo di Copilot.
3.  Riesaminare tutti i JSON/replay/risultati disponibili e ordinare i
    fattori del modello per **impatto economico atteso**, separando
    l'impatto dalla solidità dell'evidenza.
4.  Non trattare l'elenco corrente dei parametri come chiuso: puoi
    **aggiungere, eliminare, dividere, fondere o riformulare** parametri
    e relazioni causali quando esistono evidenze che mostrano nuove
    influenze o rendono inadeguata la formulazione precedente.
5.  Rendere il candidato costruibile in modo indipendente con output di
    submission fisso:

`submission_copilot.py`

## Vincoli di sicurezza

Prima di qualsiasi modifica esegui:

``` powershell
git status --short
git branch --show-current
git log -1 --oneline
```

Tratta il working tree locale come autorevole.

È vietato:

-   `git reset`
-   `git clean`
-   `git stash`
-   `git revert`
-   sovrascrivere gli output originali E13 in `results/e13/`
-   caricare submission su Kaggle
-   eseguire `git commit` o `git push` senza approvazione esplicita
-   modificare intenzionalmente il codice/policy degli altri due agenti
-   copiare nel tuo MODEL_SPEC le conclusioni o priorità degli altri
    agenti per ottenere convergenza artificiale

Non distruggere o perdere file esistenti. Se una migrazione comporta
rischi o riferimenti incrociati non chiari, preserva l'originale e
documenta il problema.

## Principio architetturale

Adotta:

> **shared infrastructure, isolated intelligence**

Possono restare condivisi solo componenti realmente neutrali e
deterministici: simulator/environment wrapper, parser, metriche comuni,
utility generiche, schema dei dati, test infrastrutturali.

Devono invece essere chiaramente isolati per agente:

-   MODEL_SPEC;
-   policy e logica decisionale specifica;
-   configurazioni/parametri;
-   test specifici del candidato;
-   risultati analitici;
-   script/build metadata specifici quando necessari;
-   bundle di submission.

Non duplicare indiscriminatamente l'infrastruttura comune. L'obiettivo è
minimizzare la contaminazione, non triplicare tutto il repository.

## Fase A --- Audit della struttura attuale

Prima di modificare file:

1.  mappa file e directory che appartengono al candidato Copilot;
2.  identifica dipendenze condivise legittime;
3.  identifica contaminazioni o dipendenze accidentali tra candidati;
4.  identifica riferimenti a `docs/model_specs/history/MODEL_SPEC_PRE_C2.md`;
5.  identifica come viene costruita oggi la submission di Copilot;
6.  identifica test e risultati che potrebbero rompersi a seguito della
    riorganizzazione.

Produci un breve piano di migrazione prima delle modifiche.

## Fase B --- Isolamento del repository

Riorganizza il repository con la minima modifica necessaria affinché il
candidato Copilot sia riconoscibile e costruibile autonomamente.

La struttura concreta deve essere decisa dopo l'audit: non forzare
directory inutili solo per rispettare uno schema teorico.

Il MODEL_SPEC specifico deve comunque avere una collocazione
inequivocabile, preferibilmente:

`docs/model_specs/copilot/MODEL_SPEC.md`

Preserva `docs/model_specs/history/MODEL_SPEC_PRE_C2.md` come artefatto storico finché la
migrazione e tutti i riferimenti non sono stati verificati. Non usarlo
più come specifica corrente condivisa.

Il processo di build deve produrre esattamente:

`submission_copilot.py`

Non rinominare questo output e non usare un nome generico
`submission.py` come artefatto finale del candidato.

Verifica che la generazione di questo file non legga accidentalmente
policy/configurazioni degli altri due candidati.

## Fase C --- Ricostruzione indipendente del MODEL_SPEC

Il MODEL_SPEC di Copilot non deve essere una semplice copia ripulita del
MODEL_SPEC storico.

Usa come fonti:

-   codice corrente del tuo candidato;
-   JSON e replay benchmark disponibili;
-   risultati sperimentali accumulati;
-   output E13 pertinenti;
-   metriche e ledger già prodotti;
-   test e ablation disponibili;
-   evidenze locali e Kaggle, mantenendo distinta la loro validità.

### L'elenco dei parametri è APERTO

Non assumere che i parametri presenti oggi rappresentino tutte le
variabili causalmente rilevanti.

Durante l'analisi devi chiederti:

-   esistono influenze osservabili non rappresentate nel modello?
-   un parametro corrente nasconde più meccanismi distinti?
-   due parametri rappresentano in realtà lo stesso meccanismo?
-   un parametro dovrebbe essere riformulato come rapporto, soglia,
    timing, priorità, interazione o variabile dinamica?
-   esistono effetti condizionali o interazioni tra parametri?
-   esistono variabili di throughput, costo opportunità, dispatch,
    movimento, inventory, feed, crop mix o reinvestimento che i dati
    mostrano come rilevanti ma che il MODEL_SPEC non rappresenta?
-   esistono parametri storici che i dati hanno falsificato come driver
    indipendenti e che devono essere rimossi o declassati?

Puoi quindi:

-   **ADD** --- introdurre un nuovo parametro/influenza;
-   **REFORMULATE** --- cambiare definizione o semantica;
-   **SPLIT** --- separare un parametro in più meccanismi;
-   **MERGE** --- fondere parametri ridondanti;
-   **DEPRECATE** --- mantenere traccia storica ma rimuovere dalla
    policy attiva;
-   **REMOVE** --- eliminare dal modello corrente se privo di utilità e
    adeguatamente documentato.

Ogni modifica alla tassonomia deve essere motivata da evidenze oppure
esplicitamente marcata come ipotesi da testare.

## Fase D --- Ranking per impatto ed evidenza

Dopo aver stabilito la tassonomia aggiornata, imponi un **ordinamento
totale** dei parametri/influenze per impatto economico atteso.

Non confondere:

-   **Impact**: capacità potenziale di modificare
    reward/revenue/compounding;
-   **Confidence**: forza dell'evidenza disponibile.

Per ogni elemento documenta almeno:

-   rank;
-   nome;
-   definizione operativa;
-   tipo: parameter / policy / interaction / derived metric /
    constraint;
-   stato tassonomico: retained / added / reformulated / split / merged
    / deprecated;
-   expected impact: Critical / High / Medium / Low;
-   confidence: High / Medium / Low;
-   evidence status;
-   meccanismo causale ipotizzato;
-   evidenze favorevoli;
-   controevidenze;
-   file/episode/seed/metriche di riferimento;
-   validità: LOCAL_ONLY / REPLAY_SUPPORTED / KAGGLE_SUPPORTED /
    LOCAL_KAGGLE_CONFLICT;
-   test necessario per aumentare o ridurre la confidence.

Usa per `evidence status`:

-   `CONFIRMED`
-   `SUPPORTED`
-   `WEAKLY_SUPPORTED`
-   `CONTRADICTED`
-   `FALSIFIED`
-   `NOT_TESTED`
-   `NOT_OBSERVABLE`

Un parametro può essere `Critical` ma avere `Low confidence`. Non
correggere il ranking per farlo sembrare più certo.

## Fase E --- Evidence backfill sui JSON

Riesamina le evidenze disponibili, privilegiando i dati grezzi rispetto
alle interpretazioni precedenti.

Per ogni parametro/influenza importante:

1.  cerca conferme;
2.  cerca **attivamente smentite e casi contrari**;
3.  identifica episodi/seed pertinenti;
4.  separa osservato, derivato e inferito;
5.  segnala quando un JSON non consente di stabilire causalità;
6.  evita di dedurre intenti interni del competitor;
7.  evita di trasformare correlazioni visuali/macroscopiche in policy
    equivalenti.

Le conclusioni E13 sono evidenze da utilizzare e verificare, non un
elenco chiuso di parametri. In particolare, tratta come vincolo empirico
il fatto che capacità fisica acquistata e throughput realizzato non
siano equivalenti, ma non assumere che WATER/dispatch sia da solo
sufficiente.

Mantieni separato il workstream **Local ↔ Kaggle Fidelity**: una
divergenza locale/Kaggle va classificata e segnalata, non compensata
introducendo arbitrariamente una nuova policy.

## Fase F --- Verifica tecnica

Dopo la riorganizzazione:

1.  esegui i test pertinenti;
2.  verifica gli import;
3.  verifica che il candidato Copilot non dipenda da file specifici
    degli altri agenti;
4.  costruisci la submission;
5.  verifica che l'output sia esattamente `submission_copilot.py`;
6.  esegui i test di submission disponibili;
7.  esegui `git diff --check`;
8.  mostra `git status --short`.

Non effettuare upload Kaggle.

## Deliverable obbligatori

Al termine devono esistere:

1.  MODEL_SPEC indipendente di Copilot;
2.  struttura repository isolata per quanto necessario;
3.  `submission_copilot.py`;
4.  tabella/ranking completo dei parametri e delle influenze;
5.  changelog tassonomico che mostri
    `ADD / REFORMULATE / SPLIT / MERGE / DEPRECATE / REMOVE`;
6.  evidence backfill con riferimenti ai JSON/episodi/risultati;
7.  elenco delle contaminazioni eliminate;
8.  elenco delle dipendenze condivise intenzionalmente mantenute;
9.  elenco dei punti non risolti e delle ipotesi che richiedono
    ablation;
10. report dei test/build.

## Stop condition

Non eseguire ancora la cross-review dei MODEL_SPEC degli altri agenti e
non modificare il loro modello.

Questa fase termina quando il tuo candidato è:

-   strutturalmente isolato;
-   costruibile autonomamente;
-   descritto da un MODEL_SPEC indipendente;
-   dotato di una tassonomia dei parametri aperta e giustificata dalle
    evidenze;
-   ordinato per impatto;
-   collegato alle evidenze accumulate;
-   pronto per la successiva **blind cross-review**.

Concludi mostrando:

1.  file creati/modificati;
2.  struttura finale rilevante;
3.  nome e path della submission;
4.  Top 10 del ranking di impatto;
5.  parametri aggiunti/riformulati/rimossi;
6.  principali evidenze confermanti;
7.  principali evidenze falsificanti;
8.  questioni aperte;
9.  test eseguiti e risultati;
10. `git status --short`.

Non fare commit o push.
