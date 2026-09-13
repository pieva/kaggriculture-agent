# E20.9 / E20v44 — apertura protetta e due pomodori tardivi

Candidata generata, **sperimentale e non promossa sopra E20.8**. Nessuna submission, commit o push in questo turno. Derivata772: pascoli7-6-1, due pollai, 8C/6S/2G invariati. Il report HTML mantiene i22 KPI e colloca volumi venduti e prezzi immediatamente sotto il grafico delle caselle/animali che producono quel bene, tutti con asse D1–D30.

## Intervento

D1 H1: BUY13/SELL13/BUY13 grano diventa BUY13. Conserva la disponibilità netta iniziale di grano e rimuove un giro di scambi; modifica comunque il mercato condiviso. Non è una prenotazione universale della cassa né un recupero generico di HIRE falliti.

Su20 aperture esterne riprodotte per48turni con mosse avversarie registrate, il controllo E20.8 riproduce esattamente la cassa D1 in20/20. Nei3 casi critici108338031/108367424/108428840, E20.9 lascia26 a fineD1 invece0, assume3aiutanti D2H1 e conserva4animali a fineD2 invece2. Il seed pubblico ènull: usato seed301 esposto. Questa è una regressione diagnostica, non una riproduzione integrale o un confronto con avversario reattivo. Non dimostra che nessuna futura apertura possa fallire.

Due caselle fragola(3,7),(4,8) sono convertite a pomodoro rispettivamente D20/D21. Acquisto di2semi aD19 solo con cassa osservata>=1000; costo100. Non attendere l’ultima settimana: prima resa del pomodoro dopo8giorni. Allocazione fissa esplorativa, non decisione già ottimizzata sui prezzi. Si riutilizzano i passaggi agricoli esistenti per acqua e raccolto; lo specialista interviene D20,D21,D29,D30, preservando i recuperi FEED D22–D28. Raccolta finale ammessa solo se rimane tempo per consegnare e vendere.

## Risultati appaiati contro E18 congelata

| Seed | E20.8 cassa / margine | Correzioni senza pomodori cassa / margine | E20.9 cassa / margine |
|---|---:|---:|---:|
|180911301|85740 / −1432|85648 / −1524|86034 / −1885|
|180911303|110220 / +2049|110131 / +1961|108177 / −456|

Entrambi i ruoli per scenario danno gli stessi esiti. Sono2seed esposti, non4scenari indipendenti; nessun holdout consumato. Il controllo senza pomodori include sia la modifica al grano sia il rientro anticipato finale: non isola da solo la modifica finanziaria.

E20.9 contro E20.8: **+294 / −2043 cassa**, media−874,5; margine medio peggiora di1479. E20.9 contro correzioni senza pomodori: **+386 / −1954**, media−784. In301 aumenta la nostra cassa ma cresce ancora di più quella avversaria: non equivale a progresso competitivo. Quattro sconfitte su quattro contro E18; il controllo E20.8 ne vince due.

Pomodori:4unità vendute per partita, incassi310/817 e prezzo medio77,50/204,25. Fragole:23590/45335 incassi contro23521/48096 del controllo senza pomodori. Nel secondo scenario il prezzo alto dei pomodori non compensa il valore delle fragole sacrificate e gli effetti indiretti sul resto della fattoria e sul mercato. La cassa totale non è attribuibile al solo nuovo prodotto. L’ipotesi di diversificazione rimane utile, ma una sostituzione fissa non è ancora una politica redditizia validata.

Tutti i12 casi del confronto finale:720stati/DONE,719azioni peragente, contabilità verificata senza discrepanze, zero fughe, mix finale corretto. E20.9 semina2pomodori e raccoglie/vende4unità entroD30. Rimangono2unità di resa sulle piante di pomodoro non raccolte: non sono raccolto venduto né cassa. Residui:1grano e3lana in deposito, semi3grano/3carota; due perdite colturali preesistenti (grano D16, fragola D22) non risolte. Non chiamare questa una correzione di tutte le fragilità.

## Tentativi conservati

- v41/stagea: scartato, due fughe di mucche; missioni pomodoro ogni giorno assorbivano lo specialista animale.
- v42/stageb: zero fughe nei2casi completati, ma2pomodori trasportati alla chiusura; suite interrotta e artefatti preservati.
- v43/stagec: anticipo rientro, rimane1pomodoro trasportato; dodici casi completi, controllo Finance riutilizzato nel confronto finale.
- v44/staged: ammissione della raccolta comprensiva del rientro; quattro casi completi, nessun pomodoro raccolto rimasto in inventario/deposito. Due rese sulle piante restano non raccolte. Bundle E20.9 congelato.

## Decisione

Tenere E20.8 come riferimento esterno. E20.9 è il candidato richiesto per studiare robustezza e diversificazione, ma **non consigliato per sostituire automaticamente il migliore pubblicato**. Passo successivo: separare la sola correzione D1 dai rientri finali, poi valutare la conversione con resa vendibile residua, prezzo realizzato atteso e lavoro disponibile. Non convertire in base al solo prezzo spot. Fermarsi comunque entro E20.10 per riesame dei tentativi.

Parità del bundle e caricatore reale in PARITY.json/LOADER.json; dati e provenienza in REPORT_DATA.json e manifest del bundle. Controllo sintattico del report effettuato separatamente; verifica visiva browser non eseguita per precedente diniego URLpolicy, senza aggiramenti.
