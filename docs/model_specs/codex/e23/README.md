# E23 — ripresa aggiornata del 14 settembre 2026

## Pubblicazioni E23 — 14 settembre 2026

E23.1 9C5S3G **56238382** ed E23.3 7C10S **56238389** pubblicate su richiesta dell'utente, entrambe Complete, score iniziale 600. Bundle identici a quelli del torneo, hash verificati. Risultati esterni da acquisire; non reinviare. Registro: `docs/model_specs/codex/e23/EXTERNAL_SUBMISSIONS_20260914.json`. Promemoria in NEW_SESSION: pubblicare E23.2 6C11S il 15 settembre e salvare ID/link/stato; nessuna automazione.


> Handoff 2026-09-14: stato operativo in `docs/NEW_SESSION.md`. Report finale: http://127.0.0.1:8771/tournament5_v1/REPORT.html . Prossimo mandato: indicatori osservabili per colmare il gap con i top, usando i dati salvati; budget da concordare prima di nuove simulazioni. Checkpoint analitico verificato in `docs/model_specs/codex/e23/ANALYSIS_CHECKPOINT.zip`.


## Implementazione e torneo locale

**Torneo a cinque completato: 140/140 incontri, 56 per versione.** Classifica: E22.1 8C6S3G **40** vittorie; E23.1 9C5S3G **34**; E22.2 8C9S **30**; E23.3 7C10S **24**; E23.2 6C11S **12**. Nessun pareggio. 7C10S batte 6C11S 12–2 (+1.432,43 monete medie), ma perde contro E22.2 4–10 (−916 medie). Nessuna E23 supera il proprio genitore nei confronti diretti aggregati. Questi risultati non promuovono una nuova campionessa.

Verificati 280 lati: mix attesi e due grani Q2 raccolti in tutti; zero fughe, discrepanze contabili o differenze di ricompensa invertendo i posti. Prodotti animali raccolti tutti riconciliati con vendite/scorte, senza differenze inventariali; E23.1 lascia tre latti non raccolti sulla mucca aggiunta. [Verifica finale](reports/tournament5_v1/VERIFICATION.json) · [Implementazione](IMPLEMENTATION.md). Nessuna submission E23 pubblicata; semi riservati inutilizzati. Le note sotto mantengono la cronologia dello sviluppo.

**Estensione richiesta dall'utente: torneo a cinque.** Aggiunta **E23.3 7C10S**, passaggio intermedio 8C9S → 7C10S → 6C11S. Solo (6,4) diventa pecora a D8 H10; (5,2) rimane mucca. Due collaudi aggiuntivi: mix corretto, zero fughe, +147 monete rispetto a E22.2 sul primo seme in entrambi i posti; 1.438 azioni verificate. Le prime due E23 restano byte-identiche.

Riferimenti correnti: [torneo a cinque](reports/tournament5_v1/REPORT.html) · [5 bundle congelati](reports/tournament5_v1/BUNDLES.json) · [collaudi 7C10S](reports/tournament5_v1/PILOT_VERIFICATION.json). **140 incontri**, 10 abbinamenti × 7 semi × 2 posti; 56 partite per versione. Riutilizzati i 12 incontri già completi del torneo a quattro. Da qui il runner usa `--five`; risultati vecchi conservati come provenienza. Il report a quattro resta storico e parziale.

Ramo di sviluppo: `codex/e23-evolution-tournament`, checkout `C:/Users/pietr/Projects/kaggriculture-agent`.

Implementate E23.1 **9C5S3G** ed E23.2 **6C11S**, evoluzioni delle ultime E22 Q2 Grano. Stessi percorsi e colture; cambia il mix al primo collocamento, con servizi adattati e vendite del prodotto modificato nelle finestre esistenti. Entrambe ereditano le correzioni esecutive E22.2. E23.2 conserva D8 H15 in (5,2), senza spostare la rotta a H16 come nel replay di riferimento. Nessun Q3 o pomodoro aggiunto.

[Bundle, parent e hash](reports/tournament4_v1/BUNDLES.json) · [Verifica dei quattro collaudi](reports/tournament4_v1/PILOT_VERIFICATION.json) · [Torneo a quattro](reports/tournament4_v1/REPORT.html).

Controlli congelati: E22.1 **56228842**, E22.2 **56231638**, byte-identici ai file della worktree E22. Quattro collaudi completati: mix corretti, zero fughe, 2.876 azioni E23 riprodotte fedelmente, nessuna mutazione delle osservazioni o del piano. Torneo ufficiale: 6 abbinamenti × 7 semi esposti × 2 posti = **84 partite**, seriali e riprendibili. Il report indica quanti incontri sono completati. Nessuna pubblicazione Kaggle. Semi riservati non utilizzati.

## Nuovo gruppo di confronto vicino a 3000

La richiesta successiva supera la precedente priorità data a Khalid: rifatto il gruppo su tutti gli undici team fra 2950 e 3000 nella classifica live del 14 settembre. Screening di 55 replay-lato e conferma separata di nove replay. Selezionati **Catalyst 56218385, Thomas Tschinkel 56222223 e Deodims & Co 56223630**. Sui loro 24 replay, 23/24 condividono le stesse 17 coordinate animali a D20 e 23/24 il nucleo 33 fragole/25 grani; zero rimozioni animali. I calendari non sono invarianti e i rami secondari restano documentati.

[Gruppo di confronto e configurazioni](reports/near3000_20260914/BENCHMARK_SET.md). Questo è il riferimento corrente per la scelta dei top E23; l'approfondimento precedente sotto resta storico.

Il NEW_SESSION presente nel checkout main è antecedente alla chiusura E22. La documentazione aggiornata è in `C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent/docs/NEW_SESSION.md`, ramo `codex/e22-2-pascoli-release`. Leggere quella ripresa e i relativi report prima di sviluppare E23. Non confondere gli originali con le successive pubblicazioni.

## Stato delle submission

- E22.1 Q2 Grano: **56228842**, snapshot 14 settembre 12:51 UTC **1909,43**, sotto 2000.
- E22.2 fix precedente: **56228129**, snapshot 12:54 UTC **1835,33**.
- Ultima E22.2 fix Q2 Grano: **56231638**, pubblicata Complete alle 13:09:30 UTC secondo il registro della worktree. Non attribuirle il rating della precedente versione; risultati successivi non acquisiti in questa analisi.
- Il pollaio Q2 (3,7) è già eliminato nelle versioni Q2 Grano, sostituito dalla successione fragola → grano.

## Mandato E23

Trovare configurazioni comuni e ripetitive nei top 2750–3000 da replicare e verificare. Studiare successioni colturali e scelte di allevamento per contenere saturazione e produzione destinata a prezzi in calo, collegando domanda, offerta, tempi produttivi, servizi e vendite. Non ripartire dal vecchio esperimento dei soli tre pascoli Q0: è già stato eseguito.

## Nuovo approfondimento

[Ricorrenze e prezzi](reports/recurrence_20260914/REPORT.md): rianalizzati i 25 replay dell'atlante esistente, tutti gli hash verificati e 750 mappe colturali giornaliere riconciliate con l'atlante.

- **56220723 (2814,1 alla selezione):** riferimento più regolare. Mix 8C6S3G oppure 9C5S3G; scelta mucca/pecora in (6,2). Conversioni fragola → grano D22 (5 caselle), D23 (1), D24 (7), uguali nelle coordinate in tutti i cinque replay. In due replay semina dieci pomodori Q3 a D19, con primo collocamento H5 e tre PIZZA_SHOP presenti; negli altri tre nessun pomodoro. Quest'ultimo contrasto non identifica ancora il trigger.
- **56218579 (2937,3):** nucleo comune di fragole/grano, ma mix animale variabile, fino a 22 pecore; un caso con venti pomodori. Utile per distinguere il calendario comune dalle estensioni.
- **56212183 (2750,9):** successioni molto ripetitive e scelta oche/pecore Q0, con perdite e collocamenti mancati da tenere distinti dalle scelte.
- La maggiore stabilità della lana resta da verificare per regime di domanda. Nel campione intero D12–D30, la caduta massima media dai picchi giornalieri è 81,8% per lana, 74,0% latte e 72,2% fragole. Sono prezzi di checkpoint, non prezzi realizzati o prove causali.

Questa analisi precedeva l'implementazione riportata in apertura. La frequenza identifica candidati replicabili; non basta a dimostrare che riducano la saturazione o migliorino il rating.
