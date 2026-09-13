# Stato del progetto

Aggiornato il13 settembre2026. Questo documento riassume il campione e la strategia corrente; la storia è in [EXPERIMENT_LOG](EXPERIMENT_LOG.md).

## Pubblicazione E22 e nuova direzione 770

Su autorizzazione esplicita dell'utente, **E22 è pubblicata e Complete**, submission **56206528**, bundle `submission_codex_e22_s56165462_observed_v1.py`, SHA256 `7abb5c797a16b76c80c352578012641aa081fb004c994e6bd7a9c3810bc3712a`. Prima dell'invio aggiunta funzione finale `agent` compatibile con il caricatore Kaggle, senza cambiare il piano; test del caricatore reale riproduce111.371/102.354 contro E20.9fix. [Registro](model_specs/codex/e22/reports/e22_release/PUBLICATION.json).

La direzione richiesta è una **nuova E19.2, base 770 V51C**, con personale reattivo e successive evoluzioni colturali. Il lavoro spiega3.597 su36.642monete del divario E22/V51C, circa10%: non è la causa principale. Sono avviate varianti interne separate per non confondere riduzione di spesa e perdita di produzione. Nessuna autorizzazione implicita a pubblicare E19.2 o a dichiarare raggiunto rating2000.

## Campione corrente: E20.9 / E20v44

E20.9 è il campione di sviluppo e verifica esterna. Il piano comune organizzato su base biologica, le correzioni di esecuzione e la diversificazione produttiva hanno prodotto un segnale esterno importante: **massimo1585 verificato nella traiettoria Kaggle della submission56202079**. Questa è la strada da consolidare. L’analisi esterna E22 è iniziata:33partite congelate,18vittorie e15sconfitte; rating all’ultima partita1352,08. Il contributo causale dei singoli interventi resta da distinguere.

Il massimo storico non è una stima stabilizzata né lo score corrente: durante la verifica la lista submission mostrava1320,8. La scelta di E20.9 come campione corrente non equivale a dichiararla vincente contro ogni versione in ogni campione.

- [Specifiche di pianificazione, strategia e adattamento](model_specs/codex/e20/e20_9/mod_specs.md).
- [Bundle congelato](../submission/submission_codex_e20_9_e20v44_late_tomato.py), SHA256 `56956735924f78d3d5502754425b207c67849ff217980e3c383add726b47debe`.
- [Pubblicazione e fonte Kaggle](model_specs/codex/e20/reports/e20_9_release/PUBLICATION.json), stato Complete, submission56202079.

## Scelte strategiche del campione E20.9

Il calendario comune è la base operativa: preservare una sequenza efficace di produzione e servizi, adattandola alla geometria e allo stato osservato. L’obiettivo è realizzare cassa da cicli completi, dalla semina o dal collocamento animale alla vendita, coprendo prima sopravvivenza e tempi biologici.

Il ramo chiamato772 usa effettivamente14pascoli7-6-1 e2pollai, con8mucche,6pecore,2oche. E20.9 elimina il giro iniziale di acquisto/vendita del grano, protegge il lavoro dello specialista animale e introduce due pomodori al posto delle fragole aD20–D21. La conversione viene ammessa con cassa sufficiente aD19 e considera crescita, servizi e consegna finale.

Diversificare l’offerta per uscire dalle fasi di prezzi decrescenti è una direttrice scelta. L’implementazione attuale è programmata, con controlli sullo stato; la rotazione dinamica guidata dai prezzi e dall’impatto delle nostre vendite è ancora una possibile evoluzione. Non presentarla come già implementata.

## Evidenza e limiti attuali

Bundle verificato:2876azioni identiche alla sorgente, reset e caricatore reale superati, quattro partite complete senza fughe. Il test locale sui due seed esposti era negativo rispetto aE18.2 (margine medio−1170,5); il salto esterno rende necessario studiare avversari e mercato, senza ignorare nessuna delle due evidenze. Il picco1585 non prova da solo che i pomodori siano la causa del vantaggio.

Restano copertura colturale e liquidazione imperfette: due perdite colturali nei test locali, scorte residue e resa finale non raccolta. La specifica distingue questi limiti dalle protezioni già operative.

## Prossima direzione

**E22: primo confronto interno autorizzato.** Replica del piano costante osservato di s56165462 56165462, distinta dalla submission 56166543 del precedente scontro diretto. Parità esatta in 20 replay (14.380 azioni). Isolata anche la correzione E20.9: il controllo PLACE già soddisfatto scartava i depositi di meloni quando la casella conteneva un animale. Il controllo ora riguarda solo gli item animali. Sorgente corretta e bundle interno separato; E20.9 pubblicata resta congelata. [Dossier con risultati e grafici](model_specs/codex/e22/reports/e22_replica_internal/REPORT.md).

[Pilota trigger dei top](model_specs/codex/e22/reports/top_trigger_pilot_20260913/REPORT.md): 30 profili di sei submission, più nove per replica. Fascia 2000–2500 come casi principali, Majkel1337 come confronto 3000+. Associazione negozio lana/scelta pecore replicata 9/9 dopo 15/15 esplorativi, senza attribuzione causale. Integrare diversificazione preventiva, numero di caselle e raccolte scaglionate con il valore d'uso del grano per gli animali. Audit grano valido per 28/30 profili; due discrepanze escluse e conservate. Nessun risparmio netto o incremento di rating dimostrato da questa analisi.

Su richiesta dell'utente è iniziata l'analisi **E22**: [prima verifica della chiusura, episodio108491899](model_specs/codex/e22/reports/closure_108491899/REPORT.md). Confermati due pomodori e due grano non raccolti, più un grano e tre lana in deposito. Una prova diagnostica sugli ultimi11turni recupera400monete con azioni avversarie fisse; non è una nuova policy né spiega il distacco complessivo. E20.9 resta il campione congelato.

**Mandato E22 aggiornato:** eliminati tutti i vincoli ereditati di topologia e pianificazione. Mix animale e colturale, numero di caselle per specie, espansione e metodo di pianificazione sono aperti. Il calendario comune è un riferimento, non un requisito. [Protocollo](model_specs/codex/e22/RESEARCH_PROTOCOL.md).

[Analisi avversari](model_specs/codex/e22/reports/opponent_strategy_20260913/REPORT.md): tutte le15sconfitte e18vittorie dello storico congelato,66profili economici verificati;10replay aggiuntivi confrontano cinque submission esatte su tre partite. Emergono sia piani quasi invarianti sia portafogli animali variabili e una strategia più variabile (Rheinmetall). Non è dimostrato che la rigidità sia la causa generale delle sconfitte. I divari maggiori nascono aD7–D11 eD20–D29; priorità a consegne dei meloni, cicli di fragole monetizzati e scelta del portafoglio. [Esploratore per specie](model_specs/codex/e22/reports/opponent_strategy_20260913/SPECIES_VARIABILITY.html). Gli avversari delle sconfitte hanno rating1362–1626: occorrerà validare anche vicino all'obiettivo2000.

E18.2 V4D e il piano comune nativo sono controlli; E20.8 e la774 comune sono riferimenti sperimentali. Non promuovere la774 solo per le vittorie locali. [Ultimo confronto dei quattro riferimenti, con E20.9](model_specs/codex/e21/reports/four_common_calendars/REPORT.html); [diagnosi locale E20.9](model_specs/codex/e20/reports/e20_9_release/REPORT.md).

## Organizzazione documentale

Preferenza dell'utente: mostrare i report HTML aprendoli nel browser visibile e lasciandoli disponibili, non soltanto come file nell'editor o link nella risposta.

[NEW_SESSION](NEW_SESSION.md) è solo il prompt di ripresa; questo file descrive scelte e stato corrente; [mod_specs.md](model_specs/codex/e20/e20_9/mod_specs.md) descrive ciò che il campione implementa; [EXPERIMENT_LOG](EXPERIMENT_LOG.md) conserva i tentativi. Le precedenti versioni estese dei due file di stato sono [archiviate](governance/history/session_snapshots/2026-09-13_before_simplification/README.md). Aggiornare le sezioni correnti, senza anteporre una nuova cronologia a ogni turno.
# 2026-09-13 — Esito dello screening E19.2

E22 pubblicata e Complete, submission **56206528**. La nuova linea E19.2 sulla 770 V51C ha quattro prototipi interni, **nessuno promosso**. [Report KPI D1–D30](model_specs/codex/e19/e19_2/REPORT.html), [specifica e protocollo](model_specs/codex/e19/e19_2/mod_specs.md).

V52A perde entrambi i test pur riducendo il lavoro; V52B introduce fughe animali; V52C riduce il lavoro medio da 7.222 a 5.107 ma perde 4/4, margine medio −3.809,5; V52D elimina cure senza valore biologico conservando il massimo originale, ma sul primo seed perde in entrambi i ruoli (−1.699, una fuga per partita). Secondo seed D annullato. Nel primo replay D la pecora (7,4) fugge al passaggio D26→D27 dopo un batch interamente PASS: serve diagnosticare la mancata ammissione dei servizi urgenti. Nessun errore Python nel core dei test C/D. Le modifiche del carico interagiscono con il coordinamento dei percorsi; una riduzione dei salari isolata non è una correzione sufficiente. Rotazioni nuove ancora non introdotte, genitore V51C intatto.
# 2026-09-13 — Priorità kiki yi2 e portafoglio contro saturazione

L'utente sceglie di approfondire kiki yi2 prima di evolvere ancora E19, associando mix animale e conversioni a pomodoro. [Dossier e grafici D1–D30](model_specs/codex/e22/reports/kiki_rotation_20260913/REPORT.html). Otto replay già acquisiti della submission 56137379, hash e contabilità di entrambi i giocatori verificati. Nessuna sostituzione/rimozione animale; collocamenti completati D12. Impronta di 17 coordinate comune a D20, ma 3 caselle sono pollai nel ramo 8C6S3G oppure pascoli nel ramo 6C10S. Quest'ultimo coincide nei tre casi con YARN_STORE prima della scelta D8 H2, mentre negli altri cinque casi compra COW. Associazione, non codice identificato né prova di superiorità della regola. Il motore non consente DIG su animale presente: distinguere investimento animale su spazi liberi da rotazione colturale. Base pomodori più aggiornata: E20.9fix interna, con conversioni programmate e fix PLACE; liquidazione finale ancora incompleta. Nessuna policy nuova o submission in questo approfondimento.
# 2026-09-13 — Kiki esteso: correggere l'ipotesi del solo negozio lana

[39 replay distribuiti nel tempo su 468 pubblici](model_specs/codex/e22/reports/kiki_variability_extended_20260913/REPORT.html): quattro mix a D20, 8C6S3G (26), 6C10S (9), 8C8S (3), 6C8S3G (1). Stesse 17 coordinate, due configurazioni dei tipi di struttura; scelte locali a D8 e D11–D12. YARN_STORE↔SHEEP D8 H2 ora 38/39, controesempio 107961405: la precedente evidenza 8/8 non è una regola completa. Nessun pomodoro nel campione, nessuna sostituzione di animali, una fuga. Approfondire i due momenti decisionali prima di trasferire una regola nella policy. Estensione osservazionale, nessuna modifica di candidato.
# 2026-09-13 — E22 in crescita e confronto E19.3 in corso

Utente riferisce **E22 score1769, posizione1689**, submission56206528 (episodio visualizzato108545568). Dato comunicato, non una verifica autonoma. Sospesa l'analisi degli avversari; in corso E19.3 V53, fix di scambi grano/alimentazione urgente/scorte accessibili/liquidazione, confronto con V51C, E22 ed E20.9fix. V53 resta interna, nessuna pubblicazione. [Inventario correzioni](model_specs/codex/e19/e19_2/FIX_INVENTORY_V53.md).
# 2026-09-13 — Picco E22 1961 comunicato dall'utente

E22 submission56206528 ha raggiunto **1961 prima della prima sconfitta**, secondo l'aggiornamento dell'utente. Non confondere il picco con lo score attuale dopo la sconfitta, non comunicato; obiettivo2000 non ancora raggiunto. Conservare E22 pubblicata invariata. Confronto E19.3 V53 in completamento, nessuna ragione emersa per sostituire E22.
# 2026-09-13 — Obiettivo 2000 raggiunto: E22 a 2024

Lo screenshot fornito dall'utente mostra **E22 score2024**, range600–2024, submission56206528. Traguardo2000 raggiunto; evidenza fornita dall'utente, non refresh autonomo. [Registro del traguardo](model_specs/codex/e22/reports/e22_release/MILESTONE_2000.json). **Mantenere E22 pubblicata invariata.**

Il lavoro E19.3 V53 è concluso:10partite seriali complete, zero fughe ma tutte perse; margine medio−992,5 controV51C (2partite),−38.828,5 controE22 (4),−22.491,5 controE20.9fix (4). Nove controlli mirati e regressione del casoD26 superati: la guardia salva la pecora dove il controllo riproduce la fuga. V53 non promossa e non pubblicata. [Report](model_specs/codex/e19/e19_2/reports/v53/REPORT.html) · [Decisione](model_specs/codex/e19/e19_2/reports/v53/DECISION.md). Eventuale prossimo esperimento770:8C6S contro9C5S su14pascoli, isolato dal pacchettoV53 e dalle rotazioni colturali; non ancora implementato.
# 2026-09-13 — Triangolare E19.2 V52C / E19.3 V53 / E22 concluso

Su scelta esplicita dell'utente, E19.2 identificaV52C (lavoro ridotto). [Report con graficiD1–D30](model_specs/codex/e19/e19_2/reports/triangle_v52c/REPORT.html). Dodici incontri su due seed esposti e due ruoli, otto nuovi e quattroV53–E22 riutilizzati con hash verificati. E19.3 batteV52C4/4 (+2.519,75 medio); E22 batteV52C4/4 (+35.498,75) eV53 4/4 (+38.828,5). Zero fughe in tutte le partite. V52C costa meno lavoro ma perde il diretto; controE22 limita maggiormente il distacco rispetto aV53. Non confondere le diverse economie generate da ciascuna coppia. V53 eV52C sono rami diversi daV51C, non prima/dopo del solo fix. Nessuna policy modificata o pubblicata; E22 resta riferimento.
# 2026-09-13 — E22 oltre2200; confronto puntuale con Sere1n

Screenshot utente:2232,2 in posizione1126 e, in altra rilevazione,2266nelGames. Non sono una nuova lettura live e la posizione non è attribuita al2266. [Analisi replay108551697](model_specs/codex/e22/reports/shared_plan_108551697/REPORT.md): E22 vince137.865–130.558 controSere1n56167820.712/719gruppi lavoratori identici; differenze soprattutto negli ordini di mercato. In due altri replaySere1n cambia ramo (6C10S/6C11S), con306/719 e218/719coincidenze. Evidenza di famiglia di piani condivisa, non prova della direzione di copia. Per E22 la replica dis5616546256165462 è nota e dichiarata. Nessuna modifica o pubblicazione.
