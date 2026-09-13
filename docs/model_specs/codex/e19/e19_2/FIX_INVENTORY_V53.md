# E19.3 V53 — inventario dei fix e confronto

Richiesta utente: sospendere la ricerca esterna, integrare nella E19 i fix individuati e confrontare con E22 ed E20.9fix prima di scegliere lo sviluppo successivo e un test esterno.

## Correzioni applicate

1. **Scambi di grano opposti nello stesso turno.** Il replay V51C contiene ripetutamente SELL WHEAT 1 insieme a BUY_PRODUCT WHEAT 1 (D1), e anche SELL 1/BUY 2. V53 compensa le quantità opposte preservando l'ordine degli altri comandi. Non elimina vendite e acquisti distanziati nel tempo: possono essere necessari o economicamente sensati.
2. **Alimentazione urgente separata dai servizi facoltativi.** Con un animale già non alimentato nel giorno precedente, da D12 al penultimo giorno, il pianificatore propone FEED puro ad alta priorità se la casella non è già assegnata. Non obbliga a completare CARE/HARVEST/fertilizzante per poter alimentare. Non assegna lo stesso bersaglio a due lavoratori.
3. **Accessibilità del grano e tutela prima della crescita.** Il problema riprodotto nella V52D ha una pecora non alimentata a D26, deposito vuoto e lavoratori con scorte altrove. La mera somma di tutto il grano trasportato non copre un servizio urgente. V53 riserva nel deposito le razioni per animali a rischio, salvo quelli già affidati a una missione FEED con grano trasportato; integra scorte con cassa osservata e rinvia nuove proposte di crescita mentre resta il rischio. Restano invariati numero massimo di lavoratori e loro gestione ordinaria.
4. **Liquidazione terminale delle scorte osservate.** Nell'ultimo giorno sospende acquisti di prodotti, semi, animali e terreno, vendendo lo stock effettivamente nel deposito senza riserve per produzione futura. Conserva il pianificatore di raccolta/consegna e le sue verifiche del tempo residuo. Questo non promette di raccogliere ogni resa rimasta sulle caselle.

## Fix già presenti o non trasferibili letteralmente

- Il bug E20.9 `PLACE` saltato su un accesso al deposito occupato da un animale è nel diverso esecutore del calendario E20. La sorgente V51C non contiene quella condizione e usa DROP per le consegne del pianificatore. Nei test precedenti vendeva già 72 meloni: non si dichiara risolto un difetto qui non riprodotto.
- La rimozione del lavoratore inattivo D2 è già presente in V51C e viene conservata.
- V51C ha già protezioni su raccolte, consegne finali, successioni grano/carota, verifiche dei servizi e percorsi D29. Il confronto serve a verificare gli esiti delle nuove correzioni senza azzerare questi meccanismi.

## Esclusioni motivate

V52A/B/C/D sono state respinte: non vengono incorporate le estensioni globali dei percorsi, il taglio del cap o la modifica di CARE. I pomodori di E20.9fix sono una scelta colturale, non un fix indipendente dalla geometria: integrarli adesso impedirebbe di separarne l'effetto. Costituiscono un'ipotesi di sviluppo successiva al confronto richiesto. Non si importa una regola sui negozi dagli avversari.

## Validazione

Nove casi mirati verificano compensazione degli scambi, priorità FEED, tutela della crescita, scorta accessibile e vendita terminale. Le prove di partita sono seriali e passano dal caricatore reale dei file Kaggle, 720 step. Due seed esposti (180911301/303): controllo V51C nel ruolo 0; E22 ed E20.9fix in entrambi i ruoli. Registri economici di entrambi i giocatori, perdite animali e residui finali. Quattro partite contro ogni riferimento rappresentano due scenari con ruoli invertiti, non quattro seed indipendenti.

I manifest e il protocollo registrano gli hash. I candidati precedenti rimangono congelati. Tutti i dieci confronti sono stati completati, senza fughe ma con margini negativi; V53 non viene promossa. La regressione mirata sullo stato V52D di D26 riproduce i 24 comandi del controllo e la fuga; installando soltanto la protezione sullo stesso stato la pecora sopravvive. [Decisione](reports/v53/DECISION.md), [regressione](reports/v53/STARVATION_REGRESSION.json).

E22 è già pubblicata come56206528. L'ultimo aggiornamento dell'utente è il picco1961 prima della prima sconfitta; lo score corrente dopo quella sconfitta non è stato comunicato e non viene dedotto.
