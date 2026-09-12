# Contratto dell'engine — come funziona Kaggriculture

Kaggriculture è un simulatore in cui due giocatori gestiscono fattorie separate
e commerciano nello stesso mercato. L'**engine** è il programma che applica
le regole: riceve le azioni delle policy, modifica lo stato della partita e
calcola il risultato. Questo documento descrive quelle regole; la scelta
della strategia appartiene alle MODEL_SPEC.

## Partita, tempo e risultato

La configurazione predefinita prevede una griglia 10×10 per giocatore,
3.000 unità di denaro iniziali e 24 turni per giornata. Ogni fattoria parte
con il quadrante nord-ovest disponibile e un agricoltore permanente.

L'orizzonte nominale è di 30 giorni. Nell'ambiente verificato, i 720 stati
registrati comprendono l'inizializzazione: ci sono 719 transizioni d'azione.
Il giorno e l'ora nel codice partono da zero; i report li possono presentare
come D1 e H1. Per analizzare una scadenza occorre distinguere lo stato prima
delle azioni, quello dopo le azioni e quello dopo il cambio di giornata.

Il risultato finale è il **denaro presente in cassa**. Terreni, strutture,
animali e prodotti invenduti non vengono convertiti automaticamente in
denaro alla fine. Il campo `reward` contiene la cassa finale; l'eventuale
rating della classifica Kaggle è una misura distinta, esterna a questo engine.

## Cosa vede e cosa invia la policy

La policy riceve lo stato pubblico delle fattorie, del mercato e della città,
oltre alle proprie informazioni private, come semi, deposito e inventari.
Non vede il deposito privato dell'avversario. Il seed risolto dell'episodio
viene conservato nel replay, ma non è fornito nell'osservazione della policy.

Ogni turno può inviare un comando per l'agricoltore, un comando per ciascun
manovale e una lista di ordini di mercato. Il limite predefinito è dieci
ordini di mercato per turno; gli ordini oltre il limite vengono ignorati.
Le risorse disponibili e lo stato della casella determinano se un comando
produce un effetto: inviare un'azione non significa che sia stata eseguita.

## File da consegnare a Kaggle

La submission contiene il **programma che prende le decisioni**, non un CSV
di previsioni, i replay o l'intero repository. La guida ufficiale documenta
due formati:

| Formato | Contenuto |
|---|---|
| File singolo | Un file Python autosufficiente; la guida usa il nome `main.py`. |
| Archivio `.tar.gz` | `main.py` alla radice, insieme ai moduli e agli eventuali dati necessari all'esecuzione. |

Struttura di un pacchetto con più file:

```text
submission.tar.gz
├── main.py
├── planner.py
└── data/
    └── parameters.json
```

`main.py` deve essere direttamente nella radice dell'archivio, non dentro
una cartella contenitore. Moduli e dati sono facoltativi: servono solo se
richiamati dal programma. La guida documenta anche l'invio dell'artefatto
prodotto da un notebook. Questi formati sono descritti nelle
[istruzioni ufficiali di submission](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/AGENTS.md#submit-your-agent).

### Struttura del programma Python

Il punto d'ingresso è una funzione `agent(observation, configuration)` che
riceve lo stato e la configurazione e restituisce un dizionario di azioni.
Questo esempio mostra l'interfaccia, ma non una strategia produttiva:

```python
def agent(observation, configuration):
    player = observation["player"]
    farm = observation["farms"][player]
    return {
        "farmer": ["PASS"],
        "hands": [["PASS"] for _ in farm["hands"]],
        "market": [],
    }
```

| Campo restituito | Struttura |
|---|---|
| `farmer` | Un comando per l'agricoltore, ad esempio `["WATER"]`. |
| `hands` | Una lista di comandi nell'ordine dei manovali presenti. |
| `market` | Una lista di ordini, ad esempio `[["BUY_SEED", "WHEAT", 1]]`. |

Il dizionario deve contenere valori serializzabili, non oggetti del planner.
Le funzioni di supporto possono organizzare pianificazione e stato interno;
non sostituiscono questo punto d'ingresso. Nel file singolo del progetto,
`agent` viene definita dopo le funzioni di supporto anche per compatibilità
con il caricatore locale.

### Dallo sviluppo al file consegnato

Nel progetto, il builder può incorporare più sorgenti in un solo file Python.
Il numero di file usati per sviluppare la policy è quindi distinto dal numero
di file da caricare. I nomi versionati in `submission/` identificano gli
artefatti locali; il nome `main.py` identifica l'ingresso del pacchetto documentato.

Il programma consegnato deve trovare tutto ciò che usa nell'artefatto o
nell'ambiente di esecuzione. Percorsi del computer di sviluppo, file in
`scratch/` e import dal repository locale non vengono trasferiti automaticamente.
README, MODEL_SPEC, test, manifest di audit e replay restano documenti di
sviluppo: non sono input necessari al simulatore.

Prima dell'invio si verifica l'artefatto risultante: caricamento, formato
delle azioni, esecuzione nei due posti di gioco e rispetto dei limiti di tempo
della configurazione. Per i bundle del progetto si controlla anche la parità
con la policy sorgente. Builder e artefatto concreto sono elencati nella MODEL_SPEC.

## Ordine di esecuzione di un turno

L'ordine dell'engine è rilevante per le decisioni:

1. Controlla le richieste di semina rispetto ai semi disponibili. Se per
   una coltura le richieste complessive superano i semi, blocca tutte le
   semine di quella coltura nel turno.
2. Applica le azioni dell'agricoltore e poi quelle dei manovali.
3. Processa gli ordini dei giocatori nel mercato condiviso.
4. Applica il consumo di prodotti da parte della città.
5. Applica il decadimento delle piante arrivate a fine vita.
6. Se il turno chiude la giornata, esegue l'aggiornamento giornaliero.
7. Aggiorna giorno e ora e, al termine dell'episodio, assegna il risultato.

Un acquisto al mercato o una nuova assunzione non possono quindi finanziare
o eseguire retroattivamente un'azione di campo nello stesso turno.

## Terreno, movimento e strutture

La griglia è divisa in quattro quadranti. Acquistare terreno sblocca le
caselle; i costi successivi sono 1.000, 2.000 e 4.000. L'engine non impone
topologie come 7-7-0: sono scelte delle policy.

Le persone si muovono di una casella in direzione nord, sud, est o ovest.
Possono occupare la stessa casella e attraversare anche terreno non acquistato,
ma su terreno bloccato non possono coltivare o costruire. L'accesso al deposito
centrale è un'eccezione: funziona dalle quattro caselle centrali adiacenti
anche quando appartengono a quadranti bloccati.

Una casella può essere vuota, contenere una pianta, un'infestante o una struttura.
Le oche richiedono un pollaio; mucche e pecore un pascolo. Costruire una
struttura e collocarvi un animale sono azioni separate. `DIG` rimuove piante,
infestanti o strutture vuote; non rimuove una struttura occupata da un animale.

## Colture e cicli biologici

Il tempo biologico deriva dalla data di semina. Le colture si dividono in
quelle a raccolta unica e quelle con un numero limitato di produzioni successive.
I tempi seguenti sono età della pianta in giorni, non giorni assoluti di partita.

| Coltura | Costo seme | Prima resa | Produzione |
|---|---:|---:|---|
| Grano | 10 | 2 | Raccolta unica; l'acqua può aumentare la resa fino all'età 4. |
| Carota | 20 | 2 | Raccolta unica; l'acqua può aumentare la resa fino all'età 3. |
| Melone | 80 | 10 | Raccolta unica; finestra di bonus acqua alle età 6–12, con limite di resa. |
| Pomodoro | 50 | 8 | Quattro produzioni programmate, una al giorno. |
| Fragola | 100 | 10 | Quattro produzioni programmate, una ogni due giorni. |

`PLANT` consuma un seme dalla riserva privata comune: non occorre trasportare
i semi. `HARVEST` trasferisce la resa nell'inventario della persona. Nelle
colture a raccolta unica rimuove anche la pianta; nelle altre la lascia sul terreno.

**Acqua e sopravvivenza.** Due giorni consecutivi senza acqua trasformano
la pianta in infestante. Una nuova semina parte già con un giorno di carenza:
deve quindi essere irrigata il giorno stesso per superare il primo refresh.
Le irrigazioni successive alla prima nello stesso giorno non hanno effetto.

**Acqua e resa.** Nelle colture a raccolta unica, irrigare nella finestra
utile aggiunge resa, entro il limite della specie. Il fertilizzante raddoppia
quel bonus per i giorni in cui è attivo e la pianta viene irrigata. Per
pomodoro e fragola, acqua e fertilizzante insieme aumentano la resa della
produzione programmata; l'acqua da sola non aggiunge produzioni al calendario.

**Fine del ciclo.** Una pianta non rimane produttiva indefinitamente.
Quando scatta il decadimento, perde un'unità disponibile ogni due turni e
diventa infestante quando la resa residua si esaurisce. Nelle colture a
produzione ripetuta conta il numero di produzioni programmate, non quante
volte il giocatore ha raccolto. Irrigare una pianta esaurita non riavvia il ciclo.

## Animali: alimentazione, cura e raccolta

| Animale | Costo | Struttura | Prima produzione | Intervallo | Prodotto massimo presente |
|---|---:|---|---:|---:|---:|
| Oca | 300 | Pollaio | 4 giorni | 1 giorno | 4 uova |
| Mucca | 400 | Pascolo | 8 giorni | 2 giorni | 6 latte |
| Pecora | 500 | Pascolo | 6 giorni | 3 giorni | 6 lana |

L'animale va acquistato, prelevato dal deposito, trasportato e collocato
sulla struttura adatta. `FEED` consuma grano nell'inventario della persona;
`CARE` fornisce cura. Entrambi hanno effetto al massimo una volta al giorno.

Due giorni consecutivi senza alimentazione fanno fuggire l'animale; la
struttura resta vuota. Un animale appena collocato parte senza giorni di
carenza e può sopravvivere alla prima giornata senza alimentazione.

La cura accumula un bonus soltanto nelle giornate in cui l'animale è anche
alimentato. Al refresh, una produzione programmata usa il bonus accumulato
in precedenza se l'animale è alimentato; poi viene accantonato il bonus della
cura del giorno appena concluso. L'ordine conta: quella cura non aumenta
retroattivamente la produzione appena avvenuta. Il prodotto presente sulla
casella è limitato, quindi rimandare la raccolta può sprecare nuova resa.

Se l'animale sopravvive a una giornata senza alimentazione che coincide con
una produzione programmata, produce comunque l'unità base, entro il limite
di prodotto presente, ma non usa il bonus CARE accumulato: quel bonus viene
azzerato e perso. Nelle giornate senza produzione programmata il bonus
precedente resta invece accantonato. Una cura senza alimentazione non
aggiunge nuovo bonus.

Ogni animale sopravvissuto rende disponibile una unità di fertilizzante al
refresh. La disponibilità non si accumula per più giorni; per ottenerla
occorre eseguire `COLLECT_FERTILIZER`.

## Manodopera e logistica

L'agricoltore permanente rimane nella partita; i manovali vengono assunti
per la giornata. Ogni persona può eseguire un comando a turno, compresi
spostamenti, prelievi e consegne: queste attività competono con i servizi
biologici per lo stesso tempo disponibile.

Il costo delle assunzioni cresce con la sequenza 1, 1, 2, 3, 5, 8, …,
moltiplicata per `farmHandCostMult`. Il conteggio riparte ogni giorno.
I manovali entrano presso il deposito e vengono rimossi alla fine della giornata.

Semi e oggetti seguono percorsi differenti. I semi sono disponibili direttamente
per la semina; grano per gli animali, fertilizzante e animali da collocare
devono essere nell'inventario della persona. I prodotti raccolti vanno
trasferiti al deposito per essere venduti.

Il deposito contiene di default al massimo 100 oggetti, esclusi i semi.
`PICKUP` trasferisce oggetti alla persona; `DROP` scarica tutto e può perdere
l'eccedenza. `PLACE` verso il deposito trasferisce la quantità ammessa dalla
capacità e lascia il resto nell'inventario. Anche lo scarico automatico di
fine giornata elimina l'eccedenza: gli inventari personali non aggirano il limite.

## Mercato e città

I due giocatori condividono scorte e prezzi del mercato. Semi e animali hanno
costi definiti dalle rispettive regole; i prezzi dei prodotti dipendono dalle
scorte. Le vendite aumentano lo stock del mercato soltanto quando il prezzo
della singola unità è maggiore di 1. **Il prezzo minimo è 1:** una vendita
a quel prezzo toglie comunque il prodotto dal deposito e accredita il denaro,
ma non aumenta lo stock del mercato. Gli acquisti di prodotti e il consumo
della città riducono lo stock. Il prezzo osservato non è quindi una costante
garantita per tutte le unità o per i turni successivi; la variazione dello
stock pubblico non basta a ricostruire le quantità vendute al prezzo minimo.

`BUY_PRODUCT` permette di acquistare soltanto **grano (`WHEAT`) e fertilizzante
(`FERTILIZER`)**. Per ogni unità il prezzo viene calcolato sullo stock del
mercato diminuito di uno, cioè sul livello successivo al prelievo; una vendita
è invece quotata sullo stock prima dell'aggiunta. Semi e animali si acquistano
con gli ordini separati `BUY_SEED` e `BUY_ANIMAL`, ai rispettivi costi fissi.

Gli ordini vengono elaborati per posizione nelle liste: prima gli ordini
in posizione 0 dei due giocatori, poi quelli in posizione 1, e così via.
Per ogni posizione, `HIRE` e `BUY_LAND` sono eseguiti una sola volta, in ordine
di giocatore. Gli scambi rimanenti procedono **una unità per giocatore alla
volta**: vengono prima calcolati entrambi i prezzi sullo stesso stock ancora
non modificato dagli scambi di quella coppia, poi vengono applicate le due
operazioni. Per gli acquisti resta valida la quotazione sullo stock meno uno.
Il ciclo continua fino all'esaurimento o all'interruzione degli ordini a
quella posizione; soltanto allora passa alla posizione successiva.

Denaro, disponibilità nel deposito e capacità possono limitare l'esecuzione.
Un'operazione che non può proseguire interrompe quell'ordine, senza impedire
di esaminare gli ordini successivi. Riordinare la lista può quindi cambiare
i prezzi realizzati anche mantenendo identici prodotti, quantità e turno.

La città consuma periodicamente prodotti; nuovi negozi possono
essere attivati durante la partita, anche duplicando un tipo già presente.
I ritmi di consumo e di apertura sono parametri della configurazione.

## Cosa succede a fine giornata

Per ogni fattoria, il refresh esegue nell'ordine:

1. Controllo idrico e produzioni programmate delle piante.
2. Controllo alimentare, produzioni e bonus degli animali.
3. Possibile nascita casuale di infestanti sulle caselle vuote sbloccate.
4. Scarico degli inventari nel deposito, con perdita dell'eccedenza.
5. Ritorno dell'agricoltore al deposito, rimozione dei manovali e reset delle assunzioni.

Successivamente può essere aperto un nuovo negozio. La probabilità predefinita
di infestante su una casella vuota è 0,005 per refresh: oltre alla morte o al
decadimento delle piante, anche il terreno lasciato vuoto può produrre infestanti.

## Dove sono definite le regole

Il codice è pubblico nel
[repository ufficiale Kaggle: ambiente Kaggriculture](https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture).
I file principali sono
[`kaggriculture.py`](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py)
per l'esecuzione delle regole e
[`kaggriculture.json`](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.json)
per configurazione e schema dell'interfaccia.

La descrizione è verificata sul pacchetto locale `kaggle-environments` e non
certifica da sola che il server Kaggle non abbia ricevuto aggiornamenti.
Le configurazioni degli episodi possono modificare i valori predefiniti.
Nel confronto del 12 settembre 2026, il contenuto dei due file principali
locali coincide con quello del ramo ufficiale `master` scaricato per la
verifica. Il ramo può cambiare: questo confronto non identifica da solo
la versione eseguita dal server in una specifica partita.

| Fonte nel pacchetto `kaggle_environments/envs/kaggriculture/` | Responsabilità |
|---|---|
| `kaggriculture.py`: `interpreter`, `_initialize` | Inizializzazione, ordine delle fasi e conclusione dell'episodio. |
| `kaggriculture.py`: `_apply_unit_action` | Legalità ed effetti delle azioni delle persone. |
| `kaggriculture.py`: `CROPS`, `ANIMALS`, `_new_plant`, `_new_animal` | Costanti delle specie e stato iniziale. |
| `kaggriculture.py`: `_decay_plants`, `_daily_refresh_plants`, `_daily_refresh_animals` | Crescita, servizi, produzione e perdite biologiche. |
| `kaggriculture.py`: `_process_market`, `_commit_unit`, `_town_consume` | Scambi, prezzi e consumo della città. |
| `kaggriculture.py`: `_end_of_day`, `_drop_inventories_to_shed` | Chiusura giornaliera e logistica automatica. |
| `kaggriculture.json` | Parametri, valori predefiniti e schema dell'interfaccia. |
| `README.md` del pacchetto | Guida del gioco; in caso di ambiguità verificare il codice. |

Gli hash delle fonti lette sono in [ENGINE_SOURCE_MANIFEST.json](ENGINE_SOURCE_MANIFEST.json).
Il [verbale storico di riconciliazione](../governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md)
conserva le verifiche precedenti. È evidenza di audit, non l'introduzione al gioco.


## Nota di verifica 2026-09-12: RNG delle infestanti e negozi

Nel sorgente locale ufficiale 1.32.7, `_end_of_day` inizializza un solo `random.Random((seed * 1_000_003) ^ day)`. Per ciascuna fattoria aggiorna piante e animali, poi `_spawn_weeds` estrae un numero casuale soltanto per le caselle `None`. Dopo entrambe le fattorie, lo stesso RNG sceglie il nuovo negozio quando previsto dal calendario.

**Uno stesso seed, con policy diverse, non garantisce la stessa sequenza di negozi.** Il numero di caselle vuote dopo il refresh dipende dalle azioni e può spostare l'estrazione del negozio. La diversa domanda dei negozi può cambiare i ricavi di prodotti non direttamente interessati dalla modifica. I negozi sono osservazioni pubbliche correnti; la policy non conosce i negozi futuri.

Conseguenza per gli esperimenti: il delta sul motore invariato è l'effetto totale della modifica, comprensivo della variazione di questa traiettoria. Non chiamarlo effetto a domanda invariata. Per separare il meccanismo operativo dalla domanda si può aggiungere una simulazione diagnostica con il calendario dei negozi mantenuto al controllo, chiaramente etichettata come sintetica e non utilizzabile per promozione o submission. I controlli senza intervento devono ancora riprodurre esattamente lo stato originale. Servono verifiche indipendenti sufficientemente ampie sul motore invariato; non selezionare una policy perché ottiene negozi favorevoli in pochi seed.
