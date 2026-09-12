# Pubblicazione 774 e disponibilità dati

12 settembre 2026. **774 E21 Repair2 pubblicata e Complete**, submission [56185961](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56185961). Punteggio iniziale 600: sola validazione, non misura competitiva. Il packaging finale delega alla stessa policy R2; caricatore Kaggle verificato con 2876 azioni identiche su quattro replay.

**Acquisizione e confronto programmati alle 17:00 Europe/Rome**, orario posticipato su richiesta del proprietario. Automazione attiva nella stessa conversazione, da disattivare dopo il singolo controllo. Se i replay 774 saranno pochi, il rapporto sarà esplicitamente preliminare; se assenti, sarà segnalata la lacuna.

| Modello esterno | Submission | Partite pubbliche complete nella history acquisita | Replay recenti verificati |
|---|---:|---:|---:|
| 770 V48 | 56101593 | 70 | 20 |
| 772 E20.1 loaderfix | 56142698 | 74 | 20 |
| 774 E21 Repair2 | 56185961 | Da acquisire al richiamo | In attesa |
| 775 E18.2, ripubblicata invariata | 56147218 | 74 | 20 |

Sono disponibili **60 replay completi dei riferimenti**, non l'intera cronologia scaricata come replay. La selezione usa i 20 più recenti per modello, senza filtro su vittoria o topologia. Ogni file ha ID, ruolo, avversario, hash, 720 stati, stato finale DONE e campi necessari per cassa, lavoratori, colture, animali, azioni, inventari e mercato. L'inventario conserva la topologia giornaliera.

Calcolo dei 22 KPI e parità di cassa verificati su un episodio per riferimento: **zero errori contabili**. Il controllo contabile di tutti gli episodi sarà eseguito nel rapporto programmato. Dati di dettaglio in DATA_PREFLIGHT.json e BASELINE_INVENTORY.json.

**Anomalia conservata:** la 775 termina 5-7-5 nell'episodio 108072534, 7-7-5 negli altri 19. La 770 termina 7-7-0 in 20/20; la 772 termina 7-7-2 in 20/20. Nessuna esclusione favorevole dell'anomalia.

La 772 esterna è E20.1, diversa dalla E20.2 locale del vecchio report. La 770 scelta è V48; la V51 visibile su Kaggle rimane una versione distinta e non è mescolata alla serie. Il confronto sarà descrittivo e distinguerà avversari, domanda e calendario dei negozi; non misura causalmente il valore della sola topologia.

Ricevuta: `../../artifacts/PUBLICATION_RECEIPT.json`. Procedura del richiamo: HANDOFF.md. Nessuna altra submission, simulazione, modifica della strategia, commit o push eseguita in questa pubblicazione.
