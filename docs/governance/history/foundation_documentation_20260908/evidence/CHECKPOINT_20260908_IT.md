# Chiusura repository: V48 e priorità PASS

8 settembre 2026. Questo checkpoint consolida anche sorgenti, test e report
E18/E19 accumulati nelle sessioni precedenti. La policy V48 pubblicata è invariata.

- Aggiornati i tre documenti attivi C2.1, il manifest, README, stato progetto,
  ingresso nuova sessione e specifica E19. I documenti C1/C2 e i verbali frozen
  restano storici. Il supplemento operativo non cambia il contratto dell'engine
  e non dichiara una nuova revisione incrociata della foundation.
- Verificati i 18 hash dei sorgenti e l'hash della submission V48 rigenerata.
  Il builder ora preserva la validazione soltanto a parità di sorgenti e output.
  Verificati anche i byte nell'indice Git: gli attributi preservano i fine riga
  degli artefatti congelati. I warning di righe vuote finali negli strumenti
  storici non vengono corretti alterando i loro hash.
- Otto test: productive_water_v48 e crop_lifecycle_audit_v48, tutti superati.
- 268 artefatti voluminosi, 3.031.016.389 byte, conservati nei percorsi originali
  e verificati per hash; esclusioni Git esatte e inventario LOCAL_ARTIFACTS.
  Non sono inclusi nel clone remoto: vanno copiati a parte per riprodurre i run.
- 160 log compressi in `scratch/session_logs_20260908.zip`, verificato il numero
  di voci prima della rimozione dei log sciolti; cache pytest/ruff rimosse.
- Ricette e input scratch salvati in
  `docs/model_specs/codex/e19/tools/session_archive_20260908/` come archivio
  storico. I file scratch ancora referenziati dai vecchi strumenti restano
  disponibili localmente. Coorti e riepilogo nuovi Top hanno ora percorsi canonici.

I manifest dei report già prodotti descrivono i sorgenti al momento della
generazione. L'analizzatore Top ora legge lo stesso input dal percorso canonico:
il suo hash corrente differisce dal manifest storico. Nessun risultato è stato
ricalcolato o presentato come nuovo benchmark durante questa manutenzione.

Priorità e inventario runtime:
[V48_PLANNING_AND_BUILD_IT.md](../V48_PLANNING_AND_BUILD_IT.md).
Verifica ripetibile: `.venv/Scripts/python.exe scripts/verify_foundation_v48.py`.
