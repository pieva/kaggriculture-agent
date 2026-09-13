# Quattro riferimenti: piano comune, 772 comune, 774 comune, E18.2 V4D

Report ricostruito dai replay già verificati, senza nuove simulazioni. Sei partite: tre calendari nel ruolo0 contro lo stesso bundle E18.2 V4D nel ruolo1, seed180911301 e180911303. Usiamo solo ruolo0 per tutti i candidati per avere un campione omogeneo: il nativo era disponibile in quel ruolo. Due scenari esposti, nessun holdout. Non è un torneo diretto fra i tre calendari.

| Calendario | Seed301: cassa / E18.2 | Seed303: cassa / E18.2 | Cassa media | Margine medio |
|---|---:|---:|---:|---:|
|Piano comune nativo|95229 / 83193|118740 / 102310|106984,5|+14233|
|772 fix + pomodori E20.9/v44|86034 / 87919|108177 / 108633|97105,5|−1170,5|
|774 comune V1|83239 / 79012|95262 / 86740|89250,5|+6374,5|

**La772 richiesta è E20.9/v44, con fix e pomodori: non prevale sulla E18.2 in queste prove.** Seed301:−1885; seed303:−456; media−1170,5, zero vittorie su due. La precedente media+308,5 apparteneva a E20.8, selezionata per errore nel primo report.

La cassa772 supera quella774 nei confronti separati di2795 e12915 (media7855). La774 ha invece margine migliore sulla propria E18.2 avversaria. Il rendimento dell’avversario cambia con produzione, scambi e domanda: la curva E18.2 non è una baseline di cassa fissa. Non usare una E18.2 estratta dalla partita774 per rivendicare un vantaggio diretto della772.

Nel report HTML sono presenti quattro curve. Per E18.2 si seleziona il contesto della partita: contro772 (default), contro il nativo o contro774. Le altre tre curve rimangono quelle delle rispettive partite contro E18.2. Il margine in tabella è sempre contro l’avversario della propria partita. Le righe E18.2 nei CSV hanno il campo context per distinguerle; REPORT_DATA.json conserva replay e hash.

Il piano comune nativo è il programma operativo registrato con geometria770,8mucche/6pecore/3oche; non un controller privato del competitor ricostruito. 772 con fix e pomodori indica E20.9/v44 con14pascoli761 e2pollai,8mucche/6pecore/2oche: apertura senza il giro iniziale del grano, due conversioni fragola→pomodoro D20/D21, servizi e consegna finale corretti. Bundle submission_codex_e20_9_e20v44_late_tomato.py; replay stage e20_9_development_d. Non è E20.8 né il prototipo v43. 774 comune indica E21 Common774 V1,18pascoli774 e1pollaio,8mucche/9pecore/1oca. E18.2 V4D è il bundle congelato `submission_codex_e18_2_capacity_governed_v4d.py`. Non sono geometrie/specie identiche.

22 KPI giornalieri, volumi venduti e prezzi realizzati ponderati immediatamente sotto la produzione associata, seguiti dal prezzo di mercato. Asse D1–D30. Un giorno senza vendita ha prezzo realizzato assente, non zero. Medie giornaliere fra i due seed; prezzi realizzati ponderati per quantità, senza media dei rapporti. E18.2 ha i propri dati di scorte private, azioni e vendite, non quelli del candidato.

Verifiche:720stati eDONE per partita; contabilità riconciliata; dati completi per12profili (due giocatori perpartita). Controllo sintattico JavaScript e integrità fonti. Nessuna verifica visiva browser, rispettato il precedente diniego URLpolicy. Nessuna modifica alle policy, submission, commit o push.
