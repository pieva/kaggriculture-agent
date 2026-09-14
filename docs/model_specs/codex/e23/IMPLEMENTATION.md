# E23 — varianti congelate del torneo a cinque

| Versione | Mix | Parent | Modifica al primo collocamento | Delta costo nominale animali |
|---|---|---|---|---:|
| E22.1 | 8C6S3G | Submission 56228842 | Controllo Q2 Grano | — |
| E22.2 | 8C9S | Submission 56231638 | Controllo fix Q2 Grano | — |
| E23.1 | 9C5S3G | E22.1 | (6,2): pecora → mucca, D10 H14 | −100 |
| E23.2 | 6C11S | E22.2 | (6,4), D8 H10 e (5,2), D8 H15: mucca → pecora | +200 |
| E23.3 | 7C10S | E22.2 | Solo (6,4), D8 H10: mucca → pecora | +100 |

Coordinate zero-based, giorni e ore qui one-based. 7C10S è l'intermedia scelta lungo questa sequenza: l'altra possibile intermedia, cambiando solo (5,2), non è un partecipante del torneo.

## Implementazione

I bundle sono autonomi e terminano con la funzione `agent`. Il generatore modifica gli ordini di acquisto, i pickup/trasferimenti e il collocamento della specie sulle tre caselle interessate. Mantiene il calendario base di percorsi, assunzioni e colture E22; nessun Q3 o pomodoro aggiunto. Tutte conservano Q2 Grano in (3,7).

Durante gli slot di servizio già previsti sulla casella evoluta, la priorità è alimentare, raccogliere il prodotto disponibile, curare e raccogliere il fertilizzante. Si usa soltanto l'osservazione corrente; lo stato locale viene proiettato fra i lavoratori dello stesso batch. Sulle pecore Q0 già trasformate in E22.2 resta la priorità alimentazione/cura/raccolta. Le vendite del prodotto modificato svuotano la disponibilità nelle finestre di vendita esistenti.

Le tre E23 condividono l'executor riparato E22.2: finanziamento delle assunzioni, recuperi esecutivi e di alimentazione, gestione delle semine e dello stress, protezione dall'overflow e chiusura D30. Il confronto E23.1/E22.1 include quindi anche queste correzioni. Il confronto non isola causalmente il solo numero di mucche e pecore. Il calendario nominale è preservato, mentre i recuperi condizionali dell'executor possono cambiare singole azioni.

Queste versioni sono evoluzioni E22 ispirate ai mix ricorrenti dei top; non copiano l'intero calendario dei top. La replica di una configurazione non garantisce lo stesso rendimento economico o rating.

## Verifica e protocollo

Sei collaudi complessivi, separati dal torneo: due per candidata, con posti invertiti. Verificate 4.314 azioni E23, determinismo, integrità di osservazioni e piano, mix attesi, zero fughe e assenza di prodotti animali raccolti residui nel magazzino o trasportati. Nel collaudo E23.1 restano tre unità di latte sulla nuova mucca: non sono state raccolte, quindi non vanno confuse con prodotti persi dal magazzino.

Torneo: dieci abbinamenti, sette semi esposti, posti invertiti, 140 incontri e 56 partite per versione. Dodici incontri completi del torneo iniziale a quattro sono riutilizzati dopo verifica degli hash. I file restano congelati durante il torneo. Una simulazione alla volta; audit dei due lati, contabilità riconciliata, replay e risultati persistenti. Nessuna pubblicazione Kaggle; semi riservati inutilizzati.

[Bundle e SHA256](reports/tournament5_v1/BUNDLES.json) · [Protocollo](reports/tournament5_v1/matches/PROTOCOL.json) · [Report](reports/tournament5_v1/REPORT.html) · [Diagnostica](reports/tournament5_v1/DIAGNOSTICS.json).
