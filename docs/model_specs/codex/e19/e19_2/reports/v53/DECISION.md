# Decisione dopo il confronto E19.3 V53

**Non pubblicare V53 e non sostituire E22.** Tutti i dieci confronti completi sono persi da V53, pur senza fughe animali. Due seed esposti, nessuna pretesa di stimare il rating:

| Riferimento | Partite | Vittorie V53 | Margine medio V53 |
|---|---:|---:|---:|
| E19 V51C | 2 | 0 | −992,5 |
| E22 | 4 | 0 | −38.828,5 |
| E20.9fix | 4 | 0 | −22.491,5 |

V53 integra correzioni funzionali: elimina gli scambi di grano opposti nello stesso turno, dà precedenza al FEED urgente, protegge le scorte accessibili e vende lo stock terminale. Il pacchetto non migliora il risultato economico rispetto al genitore: non chiamarlo una versione superiore o stabile per la classifica. I difetti e le protezioni vanno distinti dalla loro efficacia complessiva nel pianificatore e nel mercato condiviso.

**Aggiornamento conclusivo: E22 ha raggiunto2024, superando l'obiettivo2000**, come mostra lo screenshot fornito dall'utente al termine dei test. [Evidenza](../../../../e22/reports/e22_release/MILESTONE_2000.json). La submission56206528 rimane invariata; il precedente picco1961 è superato. Non è una lettura autonoma aggiornata della classifica.

## Prima ipotesi interna selezionata

Se si prosegue sulla 770, il prossimo esperimento deve isolare **8 mucche e 6 pecore invece di 9 e 5**, mantenendo 14 pascoli, stesso terreno, esecutore e colture. Non aggiungere pollai né pomodori nella stessa ablazione. Provare la modifica sul genitore congelato e valutarne separatamente l'interazione con il pacchetto V53, che è risultato regressivo: non assumerlo come nuova base obbligatoria.

Motivazione osservata nei quattro confronti V53–E22: V53 vende 119 lana contro 161; differenza media dei ricavi lana 10.192,5. Le fragole hanno un altro divario importante (9.500), ma sono un esperimento diverso su calendario e monetizzazione. Il portafoglio 8C6S non garantisce di recuperare la differenza: contano anche tempi di collocamento, alimentazione, cure e prezzo futuro. Non si deduce una regola reattiva definitiva dai soli prezzi realizzati.

L'esperimento sul mix viene prima di un trigger dinamico: misura il valore marginale dello scambio mucca/pecora su identico impianto. In seguito si potrà confrontare una scelta basata su domanda attesa e offerta propria/avversaria, mantenendo un controllo fisso. Le conversioni a pomodoro di E20.9fix restano una seconda ipotesi separata.

## Condizione per il test esterno

Non inviare una nuova E19 solo perché contiene fix. Prima servono un vantaggio interno rispetto al genitore, assenza di regressioni funzionali e un confronto più ampio sui seed di conferma. E22 è già il test esterno attivo e ha raggiunto l'obiettivo2000; nessun reinvio o variazione di E22 è necessario per questo confronto.
