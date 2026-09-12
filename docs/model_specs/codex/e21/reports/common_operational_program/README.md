# Organizzazione operativa comune: traduzione eseguibile

- Programma completo D1–D30 del rappresentante107083439:719azioni congiunte,6643comandi lavoratori,3071visite,986ordini mercato.
- compiled_common_agent.py: crea agente con create_agent({'player_position':seat}); restituisce direttamente l'azione per giorno/ora. Il controllo rigido delle posizioni blocca l'esecuzione se le rotte divergono. Nessun dispatcher a priorità.
- PROGRAM.json e nove program_*.json.gz: sequenze orarie compilate. OPERATIONS/ VISITS/ MARKET inJSON eCSV documentano posizioni, comandi, inventari e ordini esatti. Il rinnovo giornaliero non è trattato come movimento né persistenza dell'identità dei lavoratori.
- Verifica di serializzazione:6471/6471azioni dei nove replay,719/719 dal programmaPython standalone; posizione deliberatamente errata correttamente rifiutata.
- Verifica incrociata non tautologica: stesso programma lavoratori e stesse posizioni719/719 su5replay indipendenti:107083439,107150692,107341826,107382620,107923552. I programmi lavoratori formano5gruppi(5+1+1+1+1); includendo il mercato9gruppi. Zero discrepanze fra comandi cardinali e spostamenti osservati, escluse transizioni giornaliere.
- Market: conservati tutti gli ordini nell'ordine originale, compresiBUY/SELL/BUY nello stesso turno. Le quantità sono la traccia osservata, non la regola adattativa privata inferita. Contabilità giornaliera già verificata in OBSERVED_ACCOUNTING.json; il delta cassa del turno non è attribuito a un singolo ordine.
- ADAPTATION_772.json:8posizioni differenti, tutte le giornate e i lavoratori interessati. La traduzione conserva la struttura nativa14pascoli+3oche; non è ancora una772 adattata.
- Nessuna simulazione economica nuova: seed pubblico null, verifiche sulle osservazioni storiche. Nessuna modifica al bundle pubblicato.

Rigenerazione: eseguire translate_common_operations.py, poi verify_common_operations.py dal repository con laPython. ReportHTML:aprire nel browser; selettori giorno/lavoratore mostrano i dati completi.
