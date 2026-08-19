# E01 — Esecuzione osservabile e verifica della documentazione

La baseline E01 è stata completata, validata localmente e sottoposta con successo a Kaggle.

Prima di iniziare E02, esegui un'ultima attività di **VERIFY** sulla baseline E01 esistente.

## Obiettivo

Esegui localmente la baseline E01 direttamente attraverso Antigravity e rendi osservabile il comportamento di un singolo episodio completo.

Non modificare, migliorare o ottimizzare la strategia dell'agente.

Produci una traccia che permetta di comprendere le decisioni prese dall'agente durante l'episodio.

Per ogni step significativo mostra, per quanto disponibile nell'ambiente:

* step;
* day;
* hour;
* money;
* semi disponibili;
* raccolto disponibile;
* stato rilevante della tile;
* azione del farmer;
* azione di mercato.

Al termine mostra:

* reward finale;
* esito dell'episodio.

La traccia deve permettere di riconoscere concretamente il ciclo operativo dell'agente, comprese azioni come:

`BUY_SEED → PLANT → WATER → HARVEST → SELL`

## Esecuzione

Determina autonomamente come deve essere eseguito il repository esistente.

Se incontri problemi relativi ad ambiente, import, packaging, path, dipendenze o modalità di esecuzione:

1. identifica il problema;
2. spiegane la causa;
3. indica come lo hai risolto o come proponi di risolverlo.

Non effettuare modifiche persistenti al repository esclusivamente per consentire l'esecuzione senza aver prima spiegato perché siano necessarie.

Se per completare la prova fosse necessaria una modifica persistente al repository, fermati e richiedi l'approvazione umana prima di applicarla.

## Interpretazione dell'esecuzione

Dopo l'esecuzione, analizza la traccia prodotta e descrivi il comportamento effettivamente osservato.

Distingui chiaramente:

* ciò che deriva direttamente dalla traccia;
* ciò che deriva dall'analisi del codice;
* eventuali interpretazioni o deduzioni.

Non assumere che il comportamento previsto dal codice coincida necessariamente con quello osservato durante l'esecuzione.

## Verifica della documentazione

Dopo avere completato l'esecuzione, esamina:

`docs/versions/E01_baseline.md`

Confronta sistematicamente il documento con:

* il codice sorgente corrente di E01;
* l'esecuzione appena osservata;
* il comportamento effettivamente mostrato dalla traccia.

Individua eventuali affermazioni di `E01_baseline.md` che risultino:

* inesatte;
* incomplete;
* ambigue;
* non coerenti con il codice corrente;
* contraddette dall'esecuzione;
* chiarite in modo significativo dalla nuova evidenza osservativa.

Individua inoltre eventuali nuove evidenze emerse durante questa attività di VERIFY che possano migliorare sostanzialmente la documentazione della baseline.

Se `E01_baseline.md` risulta già accurato e sufficientemente completo, dichiaralo esplicitamente e non modificarlo.

Se ritieni invece utile aggiornarlo:

1. indica quali sezioni dovrebbero essere modificate;
2. spiega per quale evidenza concreta è necessario l'aggiornamento;
3. proponi le modifiche;
4. fermati prima di applicarle e attendi l'approvazione umana.

Non riscrivere inutilmente il documento e non modificarne struttura o interpretazione generale se le evidenze osservate non lo giustificano.

## Vincoli

Questa attività appartiene ancora a **E01**.

Non:

* introdurre una nuova strategia;
* ottimizzare l'agente;
* aggiungere nuove colture;
* aggiungere nuovi comportamenti;
* iniziare E02;
* effettuare refactoring non necessario;
* modificare i risultati del benchmark;
* modificare la submission Kaggle;
* effettuare modifiche persistenti non preventivamente approvate.

Lo scopo di questa attività è **verificare e osservare**, non sviluppare una nuova versione.

## Risultato atteso

Al termine presenta:

1. modalità utilizzata per eseguire E01;
2. traccia osservabile dell'episodio;
3. reward ed esito finale;
4. eventuali problemi incontrati durante l'esecuzione e relativa diagnosi;
5. interpretazione del comportamento osservato;
6. risultato del confronto tra codice, esecuzione e `docs/versions/E01_baseline.md`;
7. eventuali aggiornamenti proposti alla documentazione.

Non iniziare E02.

Fermati al termine della verifica e attendi la revisione umana.
