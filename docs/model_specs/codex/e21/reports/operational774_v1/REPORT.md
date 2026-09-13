# E21 Common774 V1 — calendario comune applicato alla 774

Nuova base operativa costruita da OPERATIONS.json e PROGRAM.json del piano comune, con lo stesso esecutore della 772. Non deriva dalle correzioni locali Repair2/Repair3. Bundle `submission/submission_codex_e21_common774_v1.py`; nessuna pubblicazione, commit o push.

## Che cosa è stato trasferito

Conservati il programma delle giornate, l’ordine delle visite non coinvolte, semine e cicli biologici, ordini di mercato originari con adattamento alle scorte osservate, recupero delle posizioni e rientro finale. D1–D6: 144 azioni complete identiche al programma comune. D7 in avanti, esecuzione delle visite ricompilate dove cambiano posizione o specie. Non è il precedente dispatcher della 774 con qualche priorità aggiunta.

Geometria finale: **7-7-4 pascoli, 8 mucche, 9 pecore e 1 oca**. Il pascolo (6,3) resta vuoto, come nella Repair2; l’oca resta in (4,1). Quattro pecore Q2 servite da due lavoratori dedicati da D12, uno per colonna. La 772 operativa ne aggiungeva uno: questo costo è parte dell’adattamento, non un confronto a parità di personale.

## Adattamenti espliciti per capacità e percorsi

75 caselle sbloccate meno 18 pascoli e un pollaio lasciano **56 caselle agricole**, contro il picco di 58 del piano nativo. Impossibile conservarne integralmente tutte le quantità senza cambiare topologia o calendario. Si conservano le 33 fragole a D12 trasferendo le quattro serie di visite Q2:

| Origine agricola | Nuova posizione |
|---|---|
|(3,5)|(1,4)|
|(3,6)|(2,3)|
|(4,5)|(0,7)|
|(4,6)|(4,9)|

Le visite native ai due siti grano (0,7) e (4,9) sono escluse da D12, liberandoli per le fragole. Gli acquisti storici di semi non sono stati ancora ridimensionati integralmente: rimangono 11 semi di grano alla chiusura. La riserva di mangime usa lo stato osservato. Nessun pomodoro introdotto; nessuna correzione finanziaria E20.9 inclusa in questo confronto.

## Confronto contro E18 congelata

| Seed | Cassa Common774 | Cassa E18 avversaria | Margine | Cassa vecchia Repair2 | Cassa 772 E20.8 |
|---|---:|---:|---:|---:|---:|
|180911301|83239|79012|+4227|65391|85740|
|180911303|95262|86740|+8522|63410|110220|

Entrambi i ruoli danno gli stessi risultati: **4 vittorie in 4 partite, su 2 scenari esposti**, non quattro repliche indipendenti. Margine medio su E18 **+6374,5**. Rispetto alla vecchia774, cassa +17848/+31852, media +24850. Questa evidenza riguarda il pacchetto calendario e adattamento, non l’effetto isolato di un pascolo.

La cassa assoluta resta inferiore alla772 E20.8 nei due confronti separati, mentre il margine sulla E18 è maggiore: il mercato condiviso e le reazioni dell’avversario cambiano. Non è stato giocato un diretto Common774–772 e non si dimostra ancora superiorità esterna. Nessun seed riservato consumato.

## Allineamento e limiti residui

Topologia e portafoglio verificati; nessuna fuga. Meloni:12 caselle D1–D10, raccolta D11. Fragole:4 a D6,20 a D9,33 a D12. Perdite per sete **4**, contro25 della vecchia774: grano (9,0) aD16, fragola (8,2) aD22, fragola trasferita (4,9) aD25 e fragola (2,5) aD27. Le prime due sono già presenti nella772 operativa; due ulteriori eventi rimangono nell’adattamento774.

Restano grano2 e lana4 in deposito, semi grano11/carota3, una resa di grano sulla pianta; nessun prodotto trasportato. Queste scorte non sono vendite né cassa. La riduzione dei due siti di grano e le visite mancate non sono mascherate come pieno rispetto del calendario. In PARITY.json: allineamento giornaliero con il controllo nativo, metriche e code non completate; una coda incompleta va interpretata per operazione, non tutta come obbligazione biologica persa.

La candidata è un’applicazione concreta del piano comune adattato, **non ancora un’esecuzione integralmente allineata in ogni casella**. Prossimo lavoro: chiudere i due nuovi buchi di irrigazione, adeguare acquisti di semi e liquidazione finale, poi confronto congelato con772 e conferma su campione indipendente.

## Verifiche e report

Quattro partite complete, 719 chiamate per agente, contabilità riconciliata. Verifica standalone su tutte le osservazioni reali dei quattro replay (2876 azioni), reset episodio e caricatore reale in PARITY.json/LOADER.json. Il bundle non usa filesystem a runtime. Dettagli effettivi nei file di verifica.

REPORT.html:22 KPI, selettore scenario, volumi venduti e prezzi subito sotto la produzione associata, confronto con Repair2 e772 E20.8. CSV giornalieri allegati. Verifica JavaScript statica; visualizzazione browser non verificata per il precedente diniego URLpolicy, rispettato senza aggiramenti.
