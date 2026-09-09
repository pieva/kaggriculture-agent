# Protocollo V49 — 2026-09-09

Baseline V48 congelata: SHA-256
`57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`.
Ambito solo 770; nessuna pubblicazione Kaggle.

La prima diagnosi usa il replay esposto 106843637 (massimo D29 nella coorte
congelata) e il controllo locale 180903001, posto 0. Non sono holdout.
Ricostruzione V48 sul replay: inserire `step=i-1`, che il runner Kaggle passa
all'agente ma non conserva nello stesso modo nel JSON. Esigere parità di tutte
le 719 azioni prima di interpretare i motivi. Il primo tentativo senza questo
clock non riproduceva D1–D11 ed è stato corretto, non usato come evidenza.

Ipotesi 1: servizi utili locali rimangono bloccati da prenotazioni provvisorie.
Recupero solo dopo PASS, senza altre missioni attive sulla casella, senza nuovi
spostamenti né acquisti. Non aggiungere raccolta fertilizzante, servizi esauriti
o irrigazione finale senza raccolta. Ablazione local_only conservata separata.

Ipotesi 2: il termine `free_tiles * 4` delle assunzioni attribuisce lavoro a
semine che nessuna specie ammessa può portare alla prima maturazione entro
fine partita. Disattivare solo questo termine quando l'orizzonte biologico è
impossibile; conservare missioni attive e servizi osservati nel carico.

Sviluppo: seed 180903001–180903003, entrambi i posti, V48 e V49 contro V4D
(controllo interno già esposto). Il primo caso ha orientato le due modifiche;
tutti i sei confronti rimangono sviluppo, anche quelli eseguiti dopo il freeze.

Validazione locale da aprire dopo il freeze: seed 260909101 e 260909102,
entrambi i posti, stesso controllo V4D. Non usare i risultati per correggere
silenziosamente V49: qualsiasi correzione successiva richiede nuova partizione.
Questi seed nuovi verificano trasferimento locale; V4D NON è un avversario
indipendente. Il gate esterno con autori non esposti rimane NON eseguito.
Non aprire nuovi autori Top e non riutilizzare gli autori consumati come prove
di competitività della candidata.

Gate dichiarati prima della matrice estesa: tutte le partite complete, zero
errori/missioni incompiute; riduzione media PASS assoluti e quota slot;
MOVE medi non superiori; cassa media non inferiore e nessun caso sotto −2%;
nessun aumento di perdite colturali produttive o fughe animali; nessuna
riduzione aggregata di FEED, CARE o HARVEST riusciti. WATER va interpretato con
perdite e stock: il conteggio non dimostra la copertura. Registrare anche le
singole regressioni, senza nasconderle nella media. Il gate completo di
copertura dei servizi necessari richiede l'audit per obbligo e rimane distinto.

Parità bundle/sorgenti: confronto di tutte le azioni su replay locali nei due
posti; riproducibilità degli hash V48 prima e dopo. Runtime: misurazione senza
telemetria separata dalle prove diagnostiche; niente conclusioni sui limiti
Kaggle dai tempi strumentati o da esecuzioni concorrenti.

Grafici appaiati D1–D30: PASS, quota slot, MOVE, cassa, manodopera, FEED, CARE,
WATER, HARVEST, colture, animali e perdite. Dettagli per persona e causa nel
JSON diagnostico; non equiparare rifiuto osservato a evitabilità dimostrata.

Correzione del runner prima della validazione: la prima matrice concorrente
ha prodotto azioni assenti e quindi non è un confronto valido. Log conservato
in `scratch/v49/matrix_development.log`. Ripetizione degli stessi casi con
`actTimeout=120` per misurare il comportamento senza confonderlo con il timeout
della macchina locale. Nessuna variazione delle regole biologiche/economiche
e nessuna correzione della candidata. I tempi misurati NON superano per questo
il gate Kaggle: la prova offline concorrente ha osservato una chiamata di
40,25 secondi e 106,15 secondi oltre la soglia di un secondo. Gate runtime
standard NON certificato. I primi casi diagnostici erano al timeout standard.

Revisione B prima di aprire la validazione: V49 A perde 1.763 di cassa sul seed
180903003 posto 0 (−2,80%), con differenze biologiche già prima di D29; non è
lecito attribuire tutta la regressione alle assunzioni. Conservati sorgenti,
bundle e sei confronti A. La revisione B ammette solo servizi di un comando
all'ultimo tick del giorno, evitando che il recupero impegni ore successive;
limita inoltre a uno il decremento del target di manovali rispetto al vecchio
estimatore quando il carico di semina è fuori orizzonte. È una protezione
sperimentale, non un certificato di capacità. Stessi gate e stessi casi di
sviluppo; seed 260909101/102 ancora non aperti al momento della correzione.

Revisione C, sempre prima della validazione: B sul medesimo caso perde 924 di
cassa (−1,47%) e aggiunge 19 MOVE; non viene estesa né promossa. C mantiene
intatta la gestione V48 delle assunzioni e recupera soltanto CARE utile
nell'ultimo tick, su animale già alimentato. Non recupera HARVEST né impegna
ore successive. La riduzione è intenzionalmente limitata: non corregge i
picchi D2, D11, D12–D15 e D29 nel loro complesso. Il carico di semina fuori
orizzonte rimane un difetto diagnosticato, con correzioni A/B respinte.

Anche C è respinta sullo sviluppo: 60.764 contro 62.931 di cassa e 1.111 contro
1.076 PASS. La revisione D isola la sola correzione prudente delle assunzioni
(massimo un manovale in meno nel target quando nessuna semina può maturare),
senza alcun recupero locale e senza cambiare il dispatcher. Prima di aprire
i seed nuovi si verifica sullo sviluppo anche la parità delle azioni D1–D28.
Non attribuire a D le riduzioni locali di CARE/HARVEST osservate in A.

D completa sei confronti: cassa media +183,33 ma MOVE medi +6,33; il gate
MOVE non passa. Nessun seed di validazione aperto. La diagnosi dell'avvio
identifica in D2 il manovale logico 3: assunto H1, 23 PASS e nessun lavoro.
La rimozione richiede correggere il punto di ingresso: il manovale fisico 3
nasce in (5,5), mentre il logico 4 nasceva in (4,4). Il primo prototipo E non
lo compensava e cambia le caselle lavorate: è scartato come errore di
rimappatura, senza attribuire a una migliore policy la sua cassa di 120.715.

F assume tre manovali; quello fisico 3 raggiunge (4,4) con WEST/NORTH e svolge
il lavoro del logico 4 due tick dopo. Gli ultimi due comandi di quel piano
sono PASS. Si eliminano due MOVE terminali del logico 2, senza successivi
lavori/consegne, compensando il transito iniziale. Nessun nuovo servizio.
Guardie sul formato di routine, configurazione standard, cassa e quattro
HIRE iniziali. Stessi gate e seed; validazione ancora non aperta durante
questa correzione. Confrontare anche lo stato biologico alla fine di D2.

Freeze F dopo lo screen 180903003 posto 0: cassa 62.934 contro 62.931,
PASS 1.053 contro 1.076, MOVE 3.488 invariati. Due test mirati della rimappatura
superati. `run_v49_final.py` completa lo sviluppo, controlla i gate preliminari
prima dell'apertura e registra `validation_opened.json` con hash della candidata.
Nessuna ulteriore modifica della policy F in base ai seed di validazione.

Chiusura: sei coppie di sviluppo e quattro di validazione completate senza
errori o missioni incomplete. In ogni coppia F elimina 23 PASS, conserva i
MOVE e aumenta la cassa di 3. I servizi riusciti, le raccolte, le perdite e i
deficit osservati restano invariati. Tutti i gate locali preregistrati passano.
Nei dieci replay, fattoria e inventari coincidono dopo D2 (salvo la cassa);
nessuna differenza nelle azioni o nelle caselle successive. Parità del bundle
719/719 nei due posti. 17 test superati; hash della V48 e del motore invariati.
La promozione resta limitata a candidata locale: gate runtime Kaggle non
certificato e avversari esterni non esposti non testati.
