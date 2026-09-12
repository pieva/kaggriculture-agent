# E20.2 / E20v32: CARE al prezzo minimo

Protocollo prima delle nuove simulazioni. Base E20.1/E20v28, topologia 7-7-2,
stesso avvio e stessa politica di assunzione. Unica variazione: da D20
escludere CARE dalle nuove offerte di servizio quando il prezzo pubblico
del prodotto animale e 1. Conservare FEED, HARVEST e COLLECT_FERTILIZER.
Non sostituire direttamente CARE con PASS dopo la pianificazione: il tempo
liberato deve essere disponibile al pianificatore. Le missioni gia attive
mantengono la loro gestione ordinaria.

Motivazione diagnostica: nei sette replay E20.1 contro E18, ruolo 0,
D20-D30, 131 delle 708 richieste CARE avvengono con prodotto al prezzo minimo;
nessuna precede FEED o ripete una cura gia fatta. Questo non prova che CARE
sia improduttiva: il prezzo puo risalire prima della produzione/vendita.
Non e una correzione dell'engine, ma un esperimento di allocazione del lavoro.
Nessuna modifica della quotazione BUY o adozione del selettore H006.

Validazione diagnostica su seed gia esposti 180910201 e 180910203, entrambi
i ruoli contro E18. Quattro controlli E20.1 devono ricostruire esattamente
456 azioni per agente e 263 transizioni successive; quattro candidate
devono conservare il prefisso fino a D20 H1, poi reagire liberamente fino a
D30. Usare il bundle congelato senza __file__ per la candidata. Richiedere
719 chiamate per agente, DONE/DONE, zero errori core E20, topologia entro
7-7-2 a ogni passo. E18 non espone il contatore core.

Confrontare cassa, margine, stress/fughe, CARE/FEED/PASS e tutti i 22 KPI.
Segnale positivo solo se migliora la cassa media senza peggioramento biologico;
riportare ogni seed e ruolo e non trattare i ruoli come repliche indipendenti.
Non selezionare altre soglie dopo gli esiti. Anche se positiva, E20.2 resta
candidata diagnostica: nessuna submission, nessuna promozione e nessun uso
dei seed riservati 180911301-307 in questo lavoro.
