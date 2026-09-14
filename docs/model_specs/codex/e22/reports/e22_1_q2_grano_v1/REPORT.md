# E22.1 Q2 Grano v1

Pubblicata: submission 56228842, stato Complete.

Il pollaio vuoto in (3,7), previsto a D29 H5, è sostituito da grano seminato D28 H8 dopo l'ultima raccolta di fragole. Due unità raccolte D30 H10, consegnate e vendute a H22. Restano 8 mucche, 6 pecore e 3 oche nei pollai Q0.

Il lavoratore 10 serve anche il grano adiacente (4,7); a D28 si recuperano un DIG a fine ciclo e un'irrigazione non produttiva, a D30 si accorpa la consegna e si usano gli slot inattivi. Nessuna assunzione né costo di lavoro aggiuntivo. Seme aggiuntivo: 10. Il lavoratore 6 usa la vecchia azione BUILD_COOP per WATER. Il piano fino a D27 resta identico.

## Test del bundle effettivo

- Parità con l'intervento diagnostico: 14.380 azioni; risposte indipendenti e caricamento senza __file__.
- 20 partite complete nel loader Kaggle contro avversari registrati: cassa finale esattamente uguale al test dal checkpoint; +2 grani raccolti e venduti per partita, senza nuove fughe e senza rimanenze aggiuntive.
- Incremento medio cassa nei 20 scenari: **+68.15**, minimo +32, massimo +83; positivi 20/20. Costi e prezzi effettivi già inclusi.
- 14 confronti diretti con i due file reali, sette semi esposti e due lati: **14/14 vittorie**, margine medio **+73.43**, mediano +74.00. Mix 8C6S3G, zero fughe; raccolta finale aggiuntiva verificata 14/14.
- Ledger contabili e azioni verificati; semi riservati non usati. I sette seed con due lati non costituiscono 14 osservazioni indipendenti. Il piccolo incremento locale non implica un aumento garantito del rating esterno.

SHA256: `5db3ef642ddf8cac5a8797ee92baea40a7caa6ab9eb1908db482b7fdc3c4b18a`. Bundle: `submission_codex_e22_1_q2_grano_v1.py`.

[22 KPI, volumi e prezzi](REPORT.html) · [Dati CSV](DAILY_22_KPI_PRICES.csv) · [Risultati](RESULTS.json) · [Protocollo](PROTOCOL.json) · [Confronto grano/carote e percorso](../e22_1_q2_coop_20260914/REPORT.html).
