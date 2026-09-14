# Chiusura E22 — 14 settembre 2026

Stato e ripresa: [E23](../../../e23/README.md). Snapshot della sessione precedente: [archivio](../../../../../archive/E22_NEW_SESSION_20260914.md).

Versionati: i due nuovi bundle, test, strumenti, report HTML/CSV, cataloghi dei replay, risultati e manifest. I profili esterni/top (65 file) sono cache locali riproducibili: percorsi e SHA256 in LOCAL_ARTIFACTS.json. Restano locali anche i replay compressi, i log e i tentativi scartati già ignorati; nessuna evidenza è stata cancellata.

Rigenerazione: recuperare prima i replay elencati nei COHORT.json tramite gli strumenti acquire_external_20260914.py / acquire_top_20260914.py e le modalità di accesso disponibili; analyze_external_20260914.py ricrea i profili esterni, acquire_top_20260914.py ricrea i profili top; align_diagnostics_20260914.py riconcilia la diagnostica e report_top_20260914.py rigenera l'atlante. I cataloghi congelati sono la fonte dei campioni e degli hash, non una nuova selezione della leaderboard. I report finali sono consultabili anche senza cache.

Le simulazioni locali hanno già superato i controlli documentati nei report; la chiusura ricontrolla i manifest, la compilazione Python e i dieci test delle correzioni E22.2. Le partite lunghe già passate non vengono ripetute per una modifica documentale.
