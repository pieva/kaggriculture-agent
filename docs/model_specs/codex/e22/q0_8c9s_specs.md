# E22.2 — Pascoli (già 8C9S v1)

Aggiornamento 13 settembre: bundle invariato inviato a Kaggle su richiesta esplicita per verifica esterna, stato Complete, submission **56212495**. [Revisione e registro](reports/e22_2_release/PUBLICATION.json). Le decisioni interne sotto precedono questo mandato.

Nome scelto dall'utente: **E22.2 — Pascoli**. Bundle mnemonico `submission/submission_codex_e22_2_pascoli.py`, copia byte per byte del bundle v1 descritto sotto. Il controllo pubblicato **56206528** prende il nome **E22.1 — Pollai**, bundle `submission/submission_codex_e22_1_pollai.py`. [Report E22.2 contro E22.1](reports/e22_2_vs_e22_1/REPORT.html). Nessuna modifica alla policy o nuova simulazione per la rinomina. La variante con calendario esterno v2 rimane un esperimento distinto e non assume il nome E22.2.

Controllo congelato: submission **56206528**, bundle `submission/submission_codex_e22_s56165462_observed_v1.py`, invariato. Variante autonoma: `submission/submission_codex_e22_q0_8c9s_internal_v1.py`; funzione finale `agent`, verificata dal caricatore reale.

## Intervento

Le costruzioni D11 H15/H19/H20 diventano PASTURE nelle coordinate (2,3), (3,2), (4,1). Le tre oche diventano pecore: due acquisti D11, uno D12, costo aggiuntivo complessivo 600. Conservati otto bovini e sei ovini originari, movimenti, assunzioni, colture, acquisti di grano. La domanda nominale di alimento non cambia: una unità per capo al giorno per entrambe le specie. Nei 14 test acquisti di grano, raccolto di grano, latte e costo lavoro coincidono con il controllo.

Negli slot stazionari dei tre pascoli la policy usa l'osservazione corrente: alimentare se necessario e il lavoratore ha grano, curare se non già curato, raccogliere resa presente, raccogliere fertilizzante; a D30 priorità alla raccolta. Uno stato locale proiettato evita duplicazioni quando più operai servono la stessa casella nello stesso turno. Restano invariati i percorsi e il numero degli slot: una raccolta può sostituire una raccolta di fertilizzante, non aggiunge un operaio. La variante non è un ripianificatore generale: non recupera automaticamente acquisti o percorsi falliti.

PICKUP/PLACE GOOSE diventano SHEEP; consegne EGG diventano WOOL. Le finestre di vendita delle uova diventano finestre lana e i limiti SELL WOOL diventano 100. Quest'ultima modifica vale anche prima di D11 e può cambiare gli incassi del mercato per-unità prima delle costruzioni: non rivendicare parità economica dei primi dieci giorni. Il confronto isola il pacchetto 8C9S con servizio/vendite adattati, non un puro effetto della struttura.

## Risultati e decisione

14 partite seriali: seed 180911301–307, entrambi i ruoli. Vittorie 4/14 (2/7 seed), media +353,14, mediana −2.092, intervallo −4.626 / +10.376. Ruoli con risultati identici; sette osservazioni per seed, non quattordici indipendenti.

Produzione: lana 225 contro 161, uova 0 contro 78, latte 245 per entrambi. Latte e lana raccolti completamente venduti. Zero fughe, mix finale 8C9S in ogni partita, zero errori contabili su 20.132 transizioni lato-partita. Restano due unità di fertilizzante trasportate a D30. Non promuovere v1 per insufficiente regolarità economica; i seed 180912401–407 rimangono non usati. Nessuna pubblicazione.

[Report KPI D1–D30](reports/q0_8c9s_v1/REPORT.md), [dashboard](reports/q0_8c9s_v1/REPORT.html), [verifica](reports/q0_8c9s_v1/VERIFICATION.json), [traiettorie esterne](reports/external_pasture_trajectories/REPORT.md).

## Riproduzione

Usare il Python del checkout originale `.venv/Scripts/python.exe`, scrivendo soltanto nella worktree corrente. Eseguire nell'ordine `tools/build_q0_pastures.py`, `tools/compare_q0_pastures.py`, `tools/verify_q0_pastures.py`, `tools/report_q0_pastures.py`. Il confronto riusa risultati soltanto se gli hash corrispondono; una sola simulazione alla volta. `tools/analyze_external_pastures.py` legge i replay congelati dal percorso originale indicato nel codice e produce l'audit delle sei varianti Q0. Non avvia simulazioni.

La replica 6C10S è distinta e non implementata: 56165125 e 56205921 lasciano (4,1) vuoto e hanno lo stesso modulo di servizio Q0; 56171606 arriva a 6C10S dopo una fuga in (5,2), pur avendo popolato tutti e tre i nuovi pascoli. Tutti i riferimenti esterni sono submission numeriche.
