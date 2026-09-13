# E22 e Sere1n: piano condiviso o copie identiche?

## Risposta

E22 è dichiaratamente la replica delle azioni pubbliche osservate di s56165462, submission56165462. Nel replay indicato, Sere1n segue un ramo operativo quasi identico. Non possiamo stabilire da questi dati chi abbia copiato chi, né se tutti derivino direttamente da s56165462: è compatibile anche con un piano o codice pubblico comune precedente.

## Scontro indicato dall'utente

[Episodio108551697](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56206528&episodeId=108551697), seed53633339. E22 submission56206528 contro Sere1n submission56167820. Cassa137.865 contro130.558, differenza7.307.

- E22 coincide con il riferimento s56165462 in719/719azioni complete.
- I gruppi di comandi dei lavoratori E22/Sere1n coincidono in712/719turni:99,03%.
- Gli ordini di mercato coincidono in575/719turni:79,97%.
- L'azione completa coincide in573/719turni:79,69%.

Confronto esatto degli array: ordine, quantità e comandi vuoti o SELL0 contano nella metrica. Non è una misura di equivalenza economica delle azioni, né una prova di identità del codice.

A D20 Sere1n ha effettivamente13pascoli+3pollai e7mucche/6pecore/3oche, contro14pascoli+3pollai e8/6/3 diE22. La prima divergenza delle strutture è aD2H6: entrambi ordinano BUILD_PASTURE su(2,4), ma E22 ha28monete e Sere1n0; solo E22 costruisce. Stessi comandi non garantiscono lo stesso esito economico o produttivo.

Solo sette turni hanno comandi diversi dei lavoratori: D11H18 DROP/PASS; tre comandi di un lavoratore aD22H22–H24; tre COLLECT_FERTILIZER/CARE aD30. Gli ordini di mercato divergono già aD1H1. Non attribuiamo senza un'ablazione il vantaggio di7.307 a una singola differenza.

## Verifica su altri due replay della stessa submission Sere1n

Selezionati i due più recenti pubblici completati contro altri team, escluso il replay indicato, senza filtro su vittoria o configurazione. Confronto con il medesimo piano E22/s56165462:

| Episodio | Comandi lavoratori identici | Mix aD20 |
|---|---:|---|
|108551697, indicato|712/719 (99,03%)|7mucche,6pecore,3oche effettive|
|108552610|306/719 (42,56%)|6mucche,10pecore|
|108546494|218/719 (30,32%)|6mucche,11pecore|

Negli ultimi due casi rimangono33fragole e25grano aD20. Nel108552610, i comandi coincidono166/168turni aD1–D7, poi divergono nettamente. Quindi Sere1n non ripete sempre il ramo osservato controE22. I conteggi sono stati verificati nei replay; non abbiamo qui attribuito ogni differenza a scelta deliberata anziché esecuzione o perdita.

## Interpretazione

Abbiamo un'evidenza forte di piani strettamente imparentati, con un ramo comune molto preciso e alternative animali. È coerente con quanto già osservato per altre submission, dove alcuni calendari coincidevano in719/719gruppi di comandi. Non prova che tutti copino lo stesso autore né identifica l'origine del piano.

Per noi la provenienza è nota; per gli altri serve codice o una pubblicazione identificabile per attribuire la derivazione. Il rating diverso non contraddice l'affinità: rami selezionati, vendite, piccole differenze operative e storico degli avversari possono cambiare gli esiti. Questo dossier non dimostra un contributo causale separato di ciascuno.

Gli screenshot dell'utente mostrano2232,2 e posizione1126 nella classifica, e2266 nel pannelloGames in un'altra rilevazione. Sono evidenze distinte, non una nuova lettura live; non assegniamo posizione1126 al punteggio2266. Nel singolo episodio indicato, i metadati riportano il passaggio2023,83→2082,38: non è lo score attuale della submission.

Fonti locali: `EPISODE.json`, `replay.json`, `DIFFERENCES.json`, `opponent_history.json`, `REPLICATION.json` e i due replay aggiuntivi. Nessuna policy modificata, simulazione interna o submission effettuata.
