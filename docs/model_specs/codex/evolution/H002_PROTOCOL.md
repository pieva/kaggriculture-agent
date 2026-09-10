# H002 — momento di vendita delle fragole

Registrato dopo la scomposizione delle vendite, prima di osservare qualsiasi intervento H002. Tutti i modelli congelati: E18, E19, E20.1. Seed diagnostici180910201 e180910202 (primi due del campione), ruolo0; E18 contro E19, E19 contro E18, E20.1 contro E18. Sei situazioni, solo due seed distinti. Nessun accesso ai seed riservati di validazione.

Motivazione: nel confronto E20.1 meno E19 contro E18, D20-D24, delta vendite -1229,4 = componente volumi +56,0 e componente prezzi realizzati -1285,4. Fragole: -865,4 di vendite, +149,7 volumi e -1015,0 prezzi. Scomposizione contabile, non prova che il ritardo sia la causa.

Ipotesi da discriminare: il momento di vendita di una raccolta gia disponibile e sufficiente a modificare i ricavi, a parita di stato prima della decisione. Il segno non e presupposto: rinviare puo peggiorare il prezzo, migliorarlo o essere irrilevante. Non si attribuisce il divario fra topologie a un singolo test.

Checkpoint: inizio D20 (indice456). Trattamento: rimuovere una volta la prima richiesta SELL STRAWBERRY in D20 emessa dal modello. Se non esiste, registrare non applicabile, senza cercare un altro giorno. Nessuna vendita forzata al turno successivo: il controller puo riproporla o modificare la quantita. Quindi il trattamento e rinuncia a una richiesta corrente, non promessa di ritardo esatto di un ora. Non si modificano i comandi dei lavoratori. Gli agenti non accedono a osservazioni future.

Controlli: riproduzione esatta delle456azioni precedenti per agente e delle263azioni/stati successivi, escluso solo remainingOverageTime. Per seed201 si riusano i tre controlli H001 gia verificati se coincidono replay sorgente e hash dei due bundle e dell engine; seed202 viene verificato ex novo. Ogni trattamento deve riprodurre anche il seguito prima della prima modifica. 719chiamate, DONE/DONE, zero errori nei core dotati di contatore. Esecuzione singola in sequenza. Prova dinamica locale, non certificazione runtime Kaggle.

Misure primarie: cassa e margine sull avversario aD20,D22,D30; stress e fughe. Misure di meccanismo: primo turno effettivo SELL dopo l omissione, quantita e prezzo medio realizzato fragole, saldo fragole in deposito e inventari, vendite totali, acquisti e salari. Distinguere effetti iniziali da traiettorie successive. Nessuna promozione su due seed; qualsiasi regressione biologica impedisce di considerare il caso un miglioramento. Registrare tutti i sei esiti, inclusi nulli, non applicabili e negativi.
