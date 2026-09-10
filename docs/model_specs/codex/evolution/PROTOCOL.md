# Metodo di evoluzione a tre — protocollo iniziale

Riferimento principale: E18 V4D 775. Controlli strutturali: E19 V48 770 ed E20.1 V28 772. I file di submission sono congelati, nessun nuovo candidato viene promosso da questa attivita.

## Campioni e criteri

Il torneo e20_1_confirmation (42 partite, sette seed 180910201-207) diventa diagnostico perche i risultati sono gia stati esaminati. Analisi su tutti i casi, nessuna esclusione per risultato. Separare avversario, ruolo e seed; mediare i ruoli dentro il seed. La migliore prestazione esterna di E18 rimane un riferimento di progetto, non una conclusione dimostrata da questo torneo interno.

La futura validazione usera sette nuovi seed 180911301-307, congelati qui prima di nuove modifiche. Non vengono eseguiti ne consultati ora. Prima di aprirli occorre congelare hash del candidato, ipotesi, controlli, avversari, budget e soglie. Una volta consultati diventano esposti. Il test esterno successivo deve registrare versione, coorte completa e avversari effettivi; Top772 non viene sostituito con Top770.

## Ripartenza fedele

Una capsula contiene riferimento e hash del replay, engine/versione/hash, configurazione, info inclusa la seed, stato completo dei due giocatori e indice di ripartenza. La memoria dei controller si ricostruisce rieseguendo la loro storia osservata, verificando ogni azione. Non si trasferisce un controller su una fattoria generata da un altro modello e non si copiano alla cieca closure Python.

Prima di accettare un effetto causale, la prosecuzione senza intervento deve riprodurre ogni azione e ogni stato del replay fino al terminale. Si esclude dal confronto solo remainingOverageTime, che dipende dal tempo di esecuzione e viene preservato come informazione osservata. Le prove locali misurano la dinamica del gioco, non certificano il limite temporale Kaggle. Entrambi gli avversari reagiscono dopo l intervento; non si riproducono le loro azioni future registrate.

## Esperimento H001: una richiesta HIRE iniziale

Selezione prima dei risultati dell intervento: seed minimo del campione, 180910201; ruolo 0; E18 contro E19, E19 contro E18, E20.1 contro E18. Stato all inizio di D20, indice456. Ciascun modello parte dal proprio stato e viene confrontato con se stesso. Non e una classifica causale fra modelli.

Trattamento: eliminare soltanto l ultima richiesta HIRE dal primo batch che ne contiene in D20. Nessun acquisto aggiunto, nessuna cancellazione successiva. Il controller puo recuperare l assunzione nei turni seguenti. Ipotesi: la disponibilita di un lavoratore nelle prime ore influenza costi e sequenza; il segno economico non e presupposto. Si misurano assunzioni/costi, servizi, MOVE/PASS, cassa e stress a D20, D22 e terminale. L effetto comprende eventuali cambi di assegnazione e reazioni dell avversario; non isola il salario puro.

Controllo: nessun intervento, parita esatta fino al terminale. Tutte le condizioni devono avere 719 chiamate per controller tra ricostruzione e seguito e zero errori nei core che espongono il contatore. L intervento e scelto usando soltanto l azione corrente. I risultati futuri sono disponibili al ricercatore solo per la valutazione.

Questo esperimento su un seed per modello collauda il banco: anche un guadagno non autorizza una promozione. Il registro deve distinguere risultato nullo, guadagno, perdita e prova non valida. Un esperimento successivo deve dichiarare un meccanismo e una previsione verificabile, prima di cambiare codice.
