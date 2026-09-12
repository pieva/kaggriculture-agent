# E20.8 / E20v40 — calendario comune e due oche

Sviluppo ricondotto alla E20 su richiesta dell’utente. Derivata 772 con 8 mucche, 6 pecore e 2 oche: 14 pascoli + 2 pollai sulle stesse 16 caselle, topologia pascoli 7-6-1. Non cambiare la strategia nel trasferimento.

Sorgenti canoniche: tools/operational_calendar_base.py e tools/operational_calendar_goose2.py; piani e programma in configs/e20v40. Il bundle standalone submission/submission_codex_e20_8_e20v40_calendar_2g.py incorpora dati e codice, senza accesso a file o dipendenze esterne. build_e20_v40.py lo ricostruisce; verify_e20_v40.py verifica parità e caricatore.

Parità 2876/2876 azioni: due seed, entrambi i ruoli (ruolo1 su osservazioni specchiate). Ulteriore partita completa con caricatore Kaggle da file, ruolo1 seed180911301: 85740 contro87172, identica al caso speculare atteso. Risultati e prove in reports/e20_8_release.

Prove locali originarie seed301/303: 85740/110220 contro775 87172/108171. Una vittoria e una sconfitta; zero fughe, fragole4/20/33, due perdite colturali, residui finali ancora presenti. Pubblicazione per verifica esterna autorizzata, non promozione sulla base di un vantaggio dimostrato.

Report canonici: [22 KPI, vendite e prezzi](reports/e20_8_three_calendars/REPORT.html), [confronto con/senza oche](reports/e20_8_goose2/REPORT.html). I report e i replay originali sotto E21 restano evidenza storica: non spostarli rompendo hash e provenienza. Le copie E20 costituiscono i punti di ingresso correnti; nessuna simulazione è cambiata per effetto del riordino.

Stato Kaggle e identificativo in reports/e20_8_release/PUBLICATION.json. Non confondere la nuova E20.8 con la 772 E20.1 loaderfix56142698 o con E21 Repair2.
