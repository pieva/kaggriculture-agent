## 2026-09-12 — E20.8 / E20v40 pubblicata per verifica esterna

Su richiesta utente, ricondotta alla E20 la variante calendario comune con 8C/6S/2G (14 pascoli + 2 pollai, topologia pascoli761). Sorgenti/piani canonici in e20/tools/operational_calendar_{base,goose2}.py e e20/configs/e20v40; bundle `submission/submission_codex_e20_8_e20v40_calendar_2g.py`, SHA256 `3305aef93ac53aa805db01541feb7e79022df1f5e04a2f167d0e6c00b69c63a5`. Parità2876azioni e partita caricatore reale ruolo1 passate. Invio Kaggle confermato dalla UI, ora Complete con punteggio iniziale600.0 (non un rating stabilizzato); stato aggiornato in e20/reports/e20_8_release/PUBLICATION.json. [Scheda release](model_specs/codex/e20/E20_8_RELEASE.md), [report 22 KPI con prezzi](model_specs/codex/e20/reports/e20_8_three_calendars/REPORT.html). E21 conserva esperimenti e provenienza storici. Nessuna modifica strategica rispetto alla Goose2 V2 testata. Commit/push e riordino autorizzati dall’utente.

## 2026-09-12 — Ripristinate due oche: variante operativa 8C/6S/2G

Utente richiede sostituire due mucche con due oche e conferma il ripristino dopo aver chiarito la sovrapposizione dei grafici meloni. Implementata `model_specs/codex/e21/operational772_goose2_v2_policy.py`, sottoclasse della V8: conversione delle stesse caselle (6,3) e (4,5) in COOP/GOOSE. 16 caselle animali totali, 14 pascoli + 2 pollai; topologia dei soli pascoli **7-6-1**, non chiamarla letteralmente 772. Conservati calendario, rotte, aiutante e regole osservate di mercato. Primo tentativo escluso dal confronto: un BUILD_PASTURE nella sequenza originale lasciava una sola oca collocata; V2 converte anche quel comando. Entrambi i tentativi conservati.

Contro 775, stesso ruolo 0 e seed301/303: cassa con oche **85740/110220**, V8 senza oche **82342/106606**; delta **+3398/+3614**. Cassa 775 avversaria **87172/108171**; margini **−1432/+2049**, quindi una sconfitta e una vittoria. Due casi esposti, non prova di superiorità generale. Entrambi: 719 chiamate, zero errori, zero fughe, esatta geometria attesa con 8C/6S/2G, fragole4/20/33, due perdite colturali, parità contabile zero errori. Restano 3 lana in magazzino, 1 grano trasportato, semi3grano/3carota.

Meloni rispettati: V8 e controllo nativo 12 caselle da D1 a D10; 72 unità raccolte D11, perciò conteggio a fine D11 zero. V8 seed301 raccoglie fra H6 e H20; nuova variante entrambe le prove raccoglie72 a D11. Il grafico precedente aveva linee sovrapposte. [Nuovo report con 22 KPI per entrambi i seed](model_specs/codex/e21/reports/operational772_goose2_v2/REPORT.html), linee con stili distinti e annotazione meloni. MELONS.json, VERIFICATION.json, RESULTS.json, PROTOCOL.json e CSV; hash congelati verificati. Script run_operational772_goose2_v2.py e report_operational772_goose2.py. Nessuna pubblicazione, commit o push.

## 2026-09-12 — Adattamento operativo 772 implementato: V8, due casi verificati

Su richiesta «Allora facciamolo», completato il trasferimento delle visite alla geometria esatta della 772 pubblicata (10 mucche, 6 pecore, nessuna oca). Policy locale `model_specs/codex/e21/operational772_v8_policy.py`, compilatore `adapt_operational772_v2.py`, piani in `reports/operational772_v8`. [Report con 22 KPI e registro V1–V8](model_specs/codex/e21/reports/operational772_adaptation/REPORT.html). Aprire nel browser. Non ripartire dalla sola traduzione o dai vecchi dispatcher a priorità.

V8 conserva gli ordini originali delle giornate/lavoratori non coinvolti e tutto D1–D6 (144 turni identici). Riscrive visite sulle posizioni modificate, rifornimenti e mercato osservato; da D12 un aiutante aggiuntivo serve i due pascoli Q2 e recupera servizi mancanti. Corregge la posizione reale degli aiutanti durante pause/servizi: il punto di nascita diverso aveva spostato le semine. Questo era il difetto delle 31 fragole nelle V6/V7. Rettifica: la mucca persa in V5/V6 era NE (5,3) a D26 H24, non Q2.

Prove seriali contro 775 congelata, ruolo 0, seed esposti 180911301 e 180911303. Cassa V8/base772: **82342/80178** e **106606/65312**. Cassa avversaria rispettivamente V8/base: 87310/96530 e 106981/62688. V8 perde entrambi gli scontri; la base vince il secondo. Aumento di cassa non equivale a superiorità competitiva, perché cambia il mercato condiviso. Nessuna promozione o pubblicazione. Entrambi i casi V8: 719 chiamate, zero errori, zero fughe, geometria/specie finali identiche alla base, fragole D6/D9/D12=4/20/33, due perdite colturali. Hash congelati verificati. Ruolo opposto e seed riservati non provati.

Il controllo con la sequenza originale esatta (nativa 770, 8C/6S/3G) sul seed301 chiude a **95229 contro 83193**. Le precedenti ricostruzioni dell'esecutore nativo da 74–76 mila alteravano troppe visite: da V5 il controllo è quello registrato esatto. Non attribuire il divario di circa 13 mila solo alla specie animale. Restano difetti della V8: grano −1 a D12 e D18–D20; carote −3 a D27/D28 e −2 a D29 rispetto al controllo nativo; residui finali 3 lana in magazzino, 1 grano trasportato, semi 3 grano/3 carota sul seed301. Tutte le differenze in VERIFICATION.json. Quindi calendario quasi allineato, non esecuzione integralmente identica.

Artefatti completi in `artifacts/operational772_v8`, `artifacts/operational772_validation`, `artifacts/operational772_recorded_control`; confronto base301 in `artifacts/calendar772_c1`. Script `run_operational772_v8.py`, `validate_operational772_v8.py`, `report_operational772_adaptation.py`. V1 invalidata da ordine mercato vuoto; V2–V8 preservate e documentate. Log incompiuti V5 non affidabili per avanzamento indici, corretto da V6. Nessun commit/push/submission; 774 esclusa. La nota seguente «adattamento ancora da eseguire» è storica e superata.

## 2026-09-12 — Tradotta l'organizzazione operativa completa, prima dell'adattamento772

Utente richiede esplicitamente traduzione operativa evitandoaltro tweaking checonsuma crediti. Completata da tutti9replay comuni: [report interattivo giorno/lavoratore](model_specs/codex/e21/reports/common_operational_program/REPORT.html). Strumenti operational_program.py, translate_common_operations.py, verify_common_operations.py in e21. Compilatore traduce719turni del rappresentante107083439:6643comandi,3071visite,986ordini mercato, posizioni/inventari pre/post e rinnovi. Compiled_common_agent.py standalone restituisceesattamente leazioni, strictpositionsfailfast, senza dispatcher.

Verifica6471/6471azioni di9replay e719standalone, negativewrongpositionpass. **Verifica incrociata:5esterni hanno identici comandi lavoratori Eposizioni per719/719turni**:107083439,107150692,107341826,107382620,107923552. Cinquegruppi unitari5+1+1+1+1, nove includendomercato. Zeroerrori nei movimenti cardinali osservati, esclusirinnovi. Dati/provenienza inCOHORT,VALIDATION,CROSS_REPLAY_VERIFICATION,MANIFEST. Mercato primoturno BUYWHEAT13/SELL13/BUY13:ordini conservati senza compensazione; nonèstata inferitalaregolaprivataadattativa. Delta cassa postturnononèdiunsingoloordine.

**Traduzioneoperativa nativa completata; adattamento772 ancora da eseguire**, non chiamarequestauna772validata. ADAPTATION_772 elenca8posizioni differenti congiorni/lavoratori/comandi coinvolti: spezzare e riscrivere soloqueste visite, comprensivi percorsi, acquisti e consegne. Nativa14pascoli+3oche vs77210C/6S. Nonrimettere ilcalendario inun dispatcher generico. Nessunanuova simulazione:seedpubbliconull, validazionesuinputstorici esplicitamente distinta da runindipendente. Nessunapubblicazione/commit/push;774esclusa.

## 2026-09-12 — 772 calendario daD1: C3–C6 concluse, nessuna promozione

Utente conferma solo772 e autorizza procedere. Completate quattro nuove varianti, un caso ciascuna seed180911301 ruolo0 contro775; tutte fermate al primo gate temporale. [Report unico](model_specs/codex/e21/reports/calendar772_execution/REPORT.html), SUMMARY.json e report22KPI pervariante. C3 prioritàanimali7:4animali D1 ma10meloni/4grani. C4 riservaD1 solo cibo corrente e collocamenti impegnati:12meloni/7grani/4animali, cassa50; fragoleD6/D9/D12=0/7/30. C5 prioritàanimali7 soloD1,poi4:0/16/33fragole,cassa44219. C6 prioritàfragole7:stessi0/16/33,cassa22836, respinta. C3cassa24762,C4=40311, controllo772E20.1=80178. Tutte719calls,0coreerrors,geometriafinale772esatta10C/6S,zerofughe; perditecropC3/C4/C5/C6=2/2/5/3. Nessuna conferma sualtri seed né pubblicazione/commit/push. Fonti congelate verificate.

Diagnosi: C2 lasciava2animali D1 non eseguiti concash1004/free888aH17; C3 risolveprecedenza ma riservafutura bloccaseed. C4completaD1, poiD6 acquistoanimale400precedefragole e finanziamentotorna H18. C5/C6 ottengono33aD12 ma mancano trancheD6: non calendario comune realizzato. Prototipo solo attivazionealla scadenza e certificato giornaliero; manca prenotazione coordinata anticipata dicassa/caselle/rotte. Non continuare tweakinglocale di priorità. L'apertura originale772 D1–D10 giàallineata nei20pubblici èriferimento da conservare.774esclusa. Le note precedenti 'C3in corso' sono storiche.

## 2026-09-12 — Direzione corrente: solo772, esecuzione calendario daD1

Utente abbandona l'allineamento774 per concentrarsi sulla772,59tile crop disponibili contro picco comune58. Autorizza prosecuzione. In corso diagnosi e prova calendar772_d1_c3: una modifica aC2, priorità7 agli insediamenti animali in scadenza invece4. ReplayC2 D1 mostra2animali contro4previsti,19colture corrette,43PASS; aH17 denaro1004, fondo manutenzione116, disponibilità888, due offerte animali ancora presenti ma non eseguite. Lavori colturali brevi vincono il punteggio e allontanano lavoratori prima degli insediamenti. Nessuna modifica a prezzi, calendario, capacità o certificati. Gate temporale congelato invariato prima del test; aggiornare questo stato con risultati. Nessuna nuova774.

## 2026-09-12 — Calendario da D1: richiesta estesa a772 e774

Utente chiede prova sulla772, poi corregge: piano daD1, non allineamento tardivo D11/D12; chiede verifica dello stesso punto sulla774. [Audit40 replay pubblici](model_specs/codex/e21/reports/calendar_d1_alignment/REPORT.html), ANALYSIS.json e ALIGNMENT_REQUIREMENTS.json.772 semine identiche al comune D1-D10 in20/20;774 in4/20 ritarda già una fragola aD6. Tutte le774 aD12 seminano8meloni/12grani/1fragola contro0/11/13 comune. Entrambe divergono aD11.77419strutture lasciano56tile crop contro picco comune58: conservare774 impone adattare la quota grano, non copiare integralmente le quantità.

772 usata: E20.1 pubblicata loaderfix56142698 (10C/6S), nonE20.2. calendar772_c1 conserva apertura/dispatcher: un confronto completo seed180911301 ruolo0 contro775,66774 vs80178; stop su steeringutente, nessuna suite4casi conclusa. Primo falso stop del runner corretto:775 core_errors=null significa non disponibile; controlli e fonti conservati.

calendar772_d1 implementa calendario storico posizioni/date, organico e land daD1 sul dispatcher772; C1 fallisce con11animali e HARVEST prematuri. calendar772_d1_c2 corregge l'età minima HARVEST, calendario invariato:719calls,0coreerrors,772finale10C/6S identica alla base,0perditecrop/animali, ma fragoleD6/D9/D12=2/11/31 contro4/20/33, cassa30295 vs80178. Gate di realizzazione fallito; stop dopo uncaso, nessuna promozione. Report22KPI puliti UTF-8 nelle tre cartelle, generati da report_calendar772_d1.py; sorgenti congelati, protocollo, replay e audit conservati. La prova cambia apertura/esecuzione e organico, non è causalità pura del calendario. Non interpretare il risultato come calendario comune realizzato. Semi riservati inutilizzati, nessuna pubblicazione/commit/push.

Anche774 deve essere pianificata daD1: requisito adottato e verificato, **variante774 D1 non ancora implementata né validata**. Non trasferire automaticamente il prototipo772 che manca i tempi. La774 Repair2 pubblicata rimane immutata. ReportHTML sempre nel browser.

## 2026-09-12 — E21 calendario comune mantenendo774: C2 non promossa

Utente conferma di mantenere geometria774 e8C/9S/1G. Implementata diagnosi `docs/model_specs/codex/e21/calendar774_policy.py`: apertura Repair2 identica D1–D11, daD12 calendario33fragole/23grani, niente nuovi meloni, successione verso grano/carote, con trasferimento del dispatcher osservativo V48. Non è ablation pura del calendario; V51C resta la base770 separata.

C1 fallisce tecnicamente dopo265 chiamate per GOOSE assente dalle regole del controller770; sorgenti e replay conservati. C2 aggiunge la regola oca e completa4/4 casi (seed esposti180911301/303, due ruoli, contro775):719 chiamate, nessun errore core, prefisso identico, posizioni/specie finali esattamenteRepair2, pascolo vuoto(6,3) preservato e zero animali inutilizzati/fughe. Delta cassa contro Repair2: **−1956** sul301 e **−15156** sul303 in entrambi i ruoli; media−8556. Perdite crop per sete5 contro25 per caso, ma meno ricavi e piùPASS. La quota33fragole arriva aD15, non aD12. Gate economico fallito; candidata solo diagnostica, nessuna nuova pubblicazione, tuning successivo, commit o push. Seed180912401–407 non usati.

[Report22KPI e contabilità](model_specs/codex/e21/reports/calendar774_c2/REPORT.html), protocollo congelato, GATE.json, DIAGNOSIS.json e FINAL_VERIFICATION.json nella stessa cartella. Bundle pubblico Repair2 invariato, hash verificato. Preferenza dell'utente: **aprire sempre i reportHTML nel browser**, non nell'editor sorgente.

## 2026-09-12 — Base di riavvio definita: 770 V51C

Analisi successiva: [organizzazione comune e riesame del lavoro passato](model_specs/codex/e19/reports/restart770_20260912/COMMON_ORGANIZATION.md). Nove esterni condividono conteggi biologici D1–D30 e semine giornaliere; otto anche raccolti. 770 conta pascoli, non pollai: nel rappresentante107083439 a D16 ci sono 14 pascoli+4 pollai (3 pieni), quindi 17 animali su18 strutture. Controllo di località su un replay per lato, non coorte intera: richieste FEED+CARE nella stessa visita animale 165/185 esterno contro99/149 V51C. Non trattare richieste come esecuzioni o questi due casi come prova causale. Recuperate diagnosi precedenti: piano biologico già presente ma vincoli futuri incompleti; V51C modifica D29, divario D16–D25 già segnalato; vecchio corpus mostrava scelta WHEAT/CARROT condizionata mantenendo gli stessi slot. Non riproporre genericamente quelle analisi come mai fatte.

Scelta completata su richiesta dell'utente: **CODEX 770 V51C**, submission **56124996**, bundle `submission/submission_codex_e19_770_v51_candidate.py`, SHA256 `43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda`. Recuperato identico dal commit `977d5e064f2ef9808b4cd03d41c1276ba94348af`, ramo `codex/v51-benchmark-checkpoint`, worktree `C:/Users/pietr/.codex/worktrees/dd62/kaggriculture-agent`. Non ricominciare da V48 perdendo V49F e V51C; V50 respinta. V48 resta controllo storico, 775 riferimento competitivo. Non inferire superiorità esterna dal solo gate locale V51C.

[Baseline e screening esterni](model_specs/codex/e19/reports/restart770_20260912/REPORT.md): 182 replay locali completi deduplicati delle nostre partite, 13 avversari 770 stabili ai checkpoint D15–D25, due ulteriori 770 solo secondo il criterio finale. Nessuna 770 produttiva nei 42 replay V51C recuperati; Moomin and his farm è soltanto finale770. Corpus storico Top V51C recuperato nel worktree: 42 replay propri e tre gruppi leader, cinque replay ciascuno. Non confondere coorti diverse con scontri diretti, né screening locale con censimento di tutte le submission. Nessuna nuova policy, simulazione o pubblicazione in questa attività.

## 2026-09-12 — Direzione attuale: capitalizzare la 770

L'utente sceglie di riprendere il lavoro sulla **770**, non ulteriori variazioni della 775. La 775 resta controllo competitivo congelato. Leggere [ripresa 770 e inventario iniziale](model_specs/codex/e19/RESTART_770_20260912.md): ricostruire versioni e miglioramenti già incorporati prima di scegliere la base e una nuova modifica. Questa direzione supera le precedenti raccomandazioni di sviluppo sulla 775; non confondere V48 esterna con revisioni successive.

Acquisizione delle 17:00 completata: 80 replay, 20 per 770/772/774/775, audit senza errori. [Report finale](model_specs/codex/e21/reports/external_770_772_774_775/REPORT.html). Automazione di acquisizione PAUSED dopo il controllo. Le indicazioni sottostanti su acquisizione ancora programmata sono storiche.

## 2026-09-12 — E21 774 pubblicata, confronto esterno programmato

Richiesta utente: pubblicare 774 e dopo un'ora acquisire misure esterne e confrontare cassa/22 KPI con 770, 772, 775. **E21 Repair2 pubblicata, Complete, submission 56185961**. Bundle `submission/submission_codex_e21_774_repair2.py`, packaging corretto con ultimo callable esplicito e 2876 azioni identiche ai quattro replay R2. [Ricevuta](model_specs/codex/e21/artifacts/PUBLICATION_RECEIPT.json). 60 replay completi dei riferimenti acquisiti: 770 V48 56101593, 772 E20.1 loaderfix 56142698 (non E20.2 locale), 775 E18.2 56147218. Anomalia 775 episodio 108072534 finale575 conservata. [Stato dati](model_specs/codex/e21/reports/external_770_772_774_775/DATA_STATUS.md). Automazione heartbeat `774-acquisizione-e-confronto-esterno-dopo-un-ora` attiva alle 17:00 Europe/Rome del 12 settembre; leggere HANDOFF.md nella stessa cartella, acquisire anche774 e completare rapporto, poi PAUSED. Nessun altro upload, tuning, simulazione, commit o push autorizzato per quel richiamo. Originali preservati.

## 2026-09-12 — E21 774 corretta prima della pubblicazione

Su successiva richiesta esplicita dell'utente, completate correzioni e verifica della ricostruzione: **CODEX-E21-774-REPAIR2**, `docs/model_specs/codex/e21/artifacts/repaired774_v2.py`. [Report con 22 KPI](model_specs/codex/e21/reports/repair774_v2/REPORT.html). R1 conservata come tentativo fallito; R2 corregge acquisti/collocamenti, escursioni al pascolo rimosso, metadati, semine prive di acqua successiva e protegge consegne terminali. Quattro partite valide sui seed esposti 180911301/303, entrambi i ruoli; 8 mucche/9 pecore/1 oca, zero animali residui, zero fughe/errori/fallback, rientri delle tratte e acqua sul target verificati. Margini contro E18 −5164 e −4622: nessuna promozione competitiva. Persistono limiti di servizio crop fuori dal target. Nessuna pubblicazione, commit o push. Seed riservati 180912401–407 inutilizzati. Originale fixed774 e suo report preservati. Le precedenti istruzioni di sola consegna alla nuova chat sono storiche, superate dalla richiesta di correzione.

## Passaggio iniziale alla nuova chat: E21 774

Richiesta utente del 12 settembre 2026: salvare lo stato; aprira personalmente una nuova chat per E21. Prima ristudiare la vecchia 774 e confrontarla con la nuova impostazione di pianificazione biologica, missioni complete e analisi economica. Non avviare nuove versioni in questa chat.

**Leggere per primo [il brief E21](model_specs/codex/e21/NEW_SESSION_BRIEF.md)**: contiene base/hash E18, provenienza della 775 dalla routine V9, riferimenti reali alla vecchia 774, confronti proposti, diagnosi recenti e verifiche mancanti. E21 e un ramo diagnostico 774; E18 resta riferimento competitivo. E20 ferma a .7, massimo .10 se riaperta; nessuna prosecuzione automatica del vecchio obiettivo di battere E18. Nessuna nuova simulazione, submission, commit o push per questo passaggio. Le sezioni sottostanti sono storiche e subordinate a questa decisione.

---

## 2026-09-12 — Analisi prima di nuove versioni: routine animale E18/E20

Completata analisi descrittiva dei 14 diretti E18–E20.2 e revisione degli esperimenti storici. Report: `docs/model_specs/codex/e20/reports/livestock_routine_20260912/REPORT.md`, dati ANALYSIS.json. E18 mostra assegnazioni animali più persistenti e minori MOVE/PASS tardivi, ma FEED per animale quasi pari, CARE da distinguere dal bonus monetizzato; più perdite crop per sete. Molti tentativi E18 storici appartenevano alla 770, non alla 775 vincente. Raccomandazione: round mirato sulla E18 775 preservando rotte e topologia, prima audit PLANT→WATER D12–19 e separatamente CARE→bonus→vendita. Questi due audit marginali restano da svolgere: non confonderli con la presente normalizzazione descrittiva. Nessuna nuova versione, simulazione o submission in questa analisi. Attendere il seguito sulla scelta di sviluppo; limite E20.10 conservato per eventuale riapertura del ramo E20.

---

## 2026-09-12 — Selezione candidati per verifica esterna

E20.7 conclusa: 14 partite, margine medio −9662 contro E18, 0/7 seed positivi; NON ADOTTATA. Scelta complessiva E18; scelta esplorativa della serie E20: E20.2, nessuna revisione successiva supera i gate. Nessun upload eseguito. Bilancio: `docs/model_specs/codex/e20/reports/candidate_selection_20260912/REPORT.md`; dati SELECTION.json. Selezione allo stato E20.7; E20.8–E20.10 non generate. Resta il limite massimo E20.10, non proseguire indefinitamente né avviare E20.11. Le sezioni precedenti che richiedono continuazione senza limite o descrivono E20.7 in corso sono storiche e superate. Seed indipendenti 180912401–407 inutilizzati.

---

## Vincolo utente: fermarsi entro E20.10

Completare al massimo le versioni fino a E20.10, poi fermarsi e fare un bilancio unico dei tentativi e dei risultati. Non avviare E20.11 e non continuare indefinitamente a cercare il superamento di E18. La richiesta sostituisce la precedente prosecuzione senza limite; nessuna submission automatica.

---

## 2026-09-12 — E20.7: trasferimento controller E18 su 772 in corso

E20.6/v37 conclusa e NON ADOTTATA (-8979/-17966 di delta cassa medio nei due seed). Nessuno degli upgrade economici v33–v37 ha superato il proprio gate. Non cumularli. La ricostruzione contabile e la scoperta RNG negozi/infestanti restano risultati validi; non assumere che una regressione di due seed misuri un effetto a domanda invariata.

In corso E20.7/E20v39, bundle `submission_codex_e20_772_e20v39_candidate.py`, costruito da `tools/build_e20_v39.py` sul bundle E18 congelato. D1–D11 replica filtro BUILD_COOP di E20; 264 azioni esatte e primo D12 smoke passati. Da D12 usa il controller E18 e il meccanismo ereditato di cap/reclaim: rimuove pascoli (3,5),(3,6),(4,7), lascia (4,5),(4,6), converte i tre plot al grano; cap risorse COW/SHEEP 16, recupero servizi su PASS secondo logica E18. Cap resta attivo anche al terminale e non può tornare a 775. Una coop/oca dopo D11 è ammessa: target 772 riguarda i pascoli. Intervento architetturale esplicito, non ablation di una sola quotazione. Non include cambi v33–v37.

Runner seriale `tools/develop_e20_7.py`, stage `e20_7_controller_transfer`: 14 partite, tutti i seed esposti 180911301–307, entrambi i ruoli contro E18. Gate congelato in E20_7_PROTOCOL.json: margine diretto medio positivo, almeno 5/7 seed positivi mediando ruoli, stress/fughe medi non peggiori di E18; completezza, zero errori cap e topologia valida. Nessuno stop economico precoce; stop solo su errore tecnico conservando evidenza. Nuovi 180912401–407 ancora riservati e inutilizzati: potranno essere aperti solo con protocollo indipendente dopo passaggio del gate.

Il prototipo v38 è congelato ma NON SIMULATO: differiva già al BUILD_COOP D11 e non preservava l'apertura E20. v39 corregge l'allineamento dell'apertura prima di qualunque risultato economico. Non usare v38 come risultato sperimentale né per submission. Obiettivo utente ancora attivo: continuare fino a E20 migliore di E18 con evidenza indipendente, guidati dai flussi economici anziché dai PASS.

---

## 2026-09-12 — E20.6 in esecuzione, upgrade economici non ancora promossi

E20.4 riparata tecnicamente come E20v35: gate non passato (+2060 nel 301, -2678 nel 303). E20.5/E20v36 aggiunge alla proiezione il consumo dei negozi già pubblici: gate non passato (+2060, -17328). Tutti i quattro casi validi per variante completi, nessun accesso ai seed 180912401–407. I report delle revisioni sono nelle rispettive cartelle e REPORT_22_KPI.html è il formato leggibile a 22 pannelli.

Avviata E20.6/E20v37: base v36, rimuove soltanto il tetto storico minimo dalle valutazioni SELL, usando la somma delle quotazioni marginali correnti/condizionali fornite; BUY resta prudenziale al massimo storico. Le proiezioni non diventano denaro spendibile. Ipotesi: la domanda osservabile non può influire pienamente se il valore futuro resta tagliato al minimo storico del prodotto. Protocollo E20_6_PROTOCOL.json congelato, bundle v37 congelato; smoke senza __file__, prime 264 azioni identiche e primo D12 valido. In corso `tools/develop_e20_6.py`, stage `e20_6_conditional_sell`, quattro partite seriali sui seed diagnostici 301/303, entrambi i ruoli. Gate invariato: cassa media migliore in ciascun seed e nessun peggioramento biologico per caso. Confrontare anche v36 per isolare il contributo. Non modificare bundle/policy durante il test.

Obiettivo utente ancora aperto: proseguire diagnosi economica e upgrade finché E20 superi E18 in validazione indipendente; non limitarsi ai PASS. Nessuna variante successiva a E20.2 è stata adottata; E18 resta il riferimento. Non avviare processi di simulazione concorrenti. Mantenere tutti i tentativi e distinguere la run v34 tecnicamente invalida (264 chiamate) dalle v35+ valide e dal test sintetico a negozi invariati.

---

## 2026-09-12 — E20.4 in sviluppo: scelta economica grano/carote

Diagnosi E20.3 a negozi fissati conclusa: delta cassa -294/-294 (seed 301), -263/-604 (303), nessuna adozione. Il grande calo sul motore ufficiale è fortemente mediato dal diverso calendario dei negozi; non confondere l'esito sintetico con il ranking Kaggle. Report `e20/reports/e20_3_fixed_town_diagnostic/REPORT.md`.

Ricostruite 600 azioni esatte di E20.2 in ciascuno dei seed 301 e 303, senza errori core, leggendo portfolio_latest. Al D12 le valutazioni totali condizionali CARROT superano WHEAT (593 vs 511; 563 vs 527), ma il pianificatore a quote fisse non propone carote prima di D26. Dati in `e20/reports/e20_2_confirmation/CROP_OPTIONS.json`.

Generata e congelata E20.4/E20v34, base E20.2 invariata salvo scelta grano/carote per nuove semine e rinnovi D12–D25: usa CARROT se valore totale già calcolato maggiore del WHEAT, admission positiva, seme finanziabile e raccolto entro D29. Non adotta il mix 8/8. E20_4_PROTOCOL.json congelato prima dei risultati. Runner `tools/develop_e20_4.py` in corso serialmente: 4 candidate, seed 301/303 entrambi i ruoli; riusa e ricontrolla i due controlli integrali esatti precedenti. Gate: delta cassa medio positivo in ciascun seed e nessun aumento di stress/fughe per caso, oltre a completezza/prefisso/topologia. Allargare ai sette seed esposti soltanto se passa; nuovi 180912401–407 ancora inutilizzati. Non modificare la candidata durante il test. Obiettivo utente resta upgrade E20 fino a superare E18 con evidenza indipendente, fondato su cause economiche e non sul numero di PASS.

---

## 2026-09-12 — E20.3 respinta; scoperto accoppiamento RNG negozi/infestanti

E20v33 mix 8/8: delta cassa medio -13895 sul seed 301 e -1130 sul 303 rispetto a E20.2; peggioramento dello stress in alcuni casi del 303. NON ADOTTATA. Sul 301 la perdita è soprattutto ricavi fragole (-11959) nonostante raccolto maggiore (246 vs 243). Il modello non va ottimizzato assumendo PASS o quantità prodotta come causa automatica del reddito.

Scoperta verificata nel codice engine: `_end_of_day` usa lo stesso RNG per infestanti (una chiamata per casella vuota) e successiva estrazione del negozio. Cambiare policy può cambiare i negozi futuri anche a seed identico. Nel 301 E20.3 riceve BAKERY al D19 anziché la seconda SMOOTHIE_SHOP del controllo; cambia quindi la domanda delle fragole. Aggiunta nota a ENGINE_CONTRACT.md e salvate tutte le traiettorie in `e20/reports/e20_2_confirmation/TOWN_SCHEDULES.json`.

In corso `tools/diagnose_e20_3_fixed_town.py`, stage `e20_3_fixed_town_diagnostic`, sessione seriale: 2 controlli interi esatti e 4 varianti, stessi seed e ruoli, calendario dei negozi del controllo ripristinato a ogni refresh. È SOLO diagnosi sintetica per distinguere effetto della modifica da domanda; non è evidenza per una submission. I bundle non leggono i negozi futuri; ricevono solo osservazioni normali. L'engine installato non viene modificato su disco. Protocollo E20_3_FIXED_TOWN_PROTOCOL.json congelato. Nessuna nuova variante ulteriore avviata; dopo la diagnosi definire upgrade fondato sulla monetizzazione/domanda osservabile, poi validarlo sul motore invariato. Seed 180912401–407 ancora riservati e inutilizzati.

---

## 2026-09-12 — Conferma E20.2 conclusa; E20.3 in sviluppo

Torneo a tre completo: 42 partite valide, sette seed 180911301–307 ora esposti. E20.2 contro E18: margine medio -3539, 2/7 seed positivi; contro E19 +1138,7, 5/7 positivi. Decisione DO_NOT_SUBMIT_E20_2. Audit saldi completo, report 22 KPI in `model_specs/codex/e20/reports/e20_2_confirmation/REPORT.html`; dettagli contabili in CASH_GAP.md/JSON e decisione in SUBMISSION_DECISION.md.

E18 meno E20.2: maggiori ricavi +18290,7, maggiori acquisti -14422,4, maggiori assunzioni -329,4, differenza netta +3539. Circa 2679,7 nasce D12–19, solo 859,3 D20–30. Raccolto grano quasi uguale (316,7 vs 313,9), quindi i maggiori ricavi del grano non indicano maggiore produzione: E18 compra e vende più grano. Lana: raccolto 238 vs 137,9, ricavi +6407,1; latte ricavi quasi uguali. E20.2 acquista 10 mucche/6 pecore, E18 8/11 oltre a un'oca. Non attribuire la perdita ai PASS.

Avviata E20.3/E20v33, unica variazione sul portafoglio: 8 mucche/8 pecore, due pecore in Q2, stessa topologia 772 e resto di E20.2 invariato. Protocollo E20_3_PROTOCOL.json congelato, bundle v33 congelato. Screen sei partite seriali: seed 180911301 (prima perdita) e 180911303 (prima vittoria), due ruoli per candidata e un controllo esatto intero per seed. Runner `tools/develop_e20_3.py`, stage `e20_3_mix_development`; non lanciare simulazioni concorrenti. Richiesti delta cassa positivi in entrambi i seed e nessun peggioramento biologico per caso. Poi ampliare ai sette seed esposti, non chiamarli holdout. Nuovi seed 180912401–407 riservati e NON eseguiti. Non modificare policy/bundle/protocollo durante lo screen. Obiettivo utente: proseguire upgrade fondati su diagnosi economica fino a superare E18 in validazione indipendente; nessuna submission automatica.

---

## Obiettivo aggiornato dall'utente durante il torneo

Completare il confronto a tre in corso, poi spiegare il divario di cassa E20-E18 con riconciliazione di ricavi per prodotto, quantità raccolte/vendute, prezzi e tempi, acquisti, assunzioni, terra e scorte terminali. Non assumere PASS o manodopera come causa: erano soltanto un'ipotesi iniziale. Usare anche i casi vinti, non selezionare solo sconfitte. Generare e verificare upgrade E20 con interventi isolati fino a superare E18 in modo ripetibile su nuova validazione indipendente. Conservare la topologia 7-7-2 salvo indicazione successiva. Nessun risultato futuro è garantito; non promuovere sulla sola media o su seed usati per sviluppare. Nessuna submission automatica.

Strumenti preparati: `summarize_e20_2_confirmation.py` e `diagnose_e20_2_cash_gap.py`, da eseguire dopo il completamento del runner di conferma. Gli hash congelati della conferma non vanno modificati durante il torneo.

---

## 2026-09-12 — Torneo indipendente E20.2 / E18 / E19 in corso

Avviato stage `e20_2_confirmation`: 42 partite seriali, sette seed 180911301–307, tutte le coppie e scambio dei ruoli. Questi seed sono ora destinati alla conferma e vanno considerati esposti appena eseguiti; non riutilizzarli per selezionare varianti. Bundle congelati; criteri e hash in [E20_2_CONFIRMATION_PROTOCOL.json](model_specs/codex/e20/E20_2_CONFIRMATION_PROTOCOL.json).

Gate prima dei risultati: E20.2 deve avere margine diretto medio positivo contro ciascun riferimento, positivo in almeno 5/7 seed (ruoli mediati), senza peggiorare stress colture e fughe medi; esecuzioni complete e prive di errori core strumentati. Nessuna submission automatica. Runner riprendibile `tools/confirm_e20_2.py`; log `reports/e20_2_confirmation/RUN.log`, decisione finale attesa in `DECISION.json`. La voce storica sottostante sui seed inutilizzati si riferisce al precedente lavoro diagnostico.

---

## 2026-09-12 — E20.2 generata e verificata localmente

Congelata E20v32, base E20.1/E20v28, topologia 7-7-2. Da D20 esclude nuove offerte CARE quando il prezzo pubblico del prodotto animale è 1; non cambia FEED né sostituisce comandi con PASS. Ipotesi economica sul prezzo corrente, non garanzia di resa futura.

Otto rami completi (quattro controlli esatti e quattro candidate), seed diagnostici 180910201/203, entrambi i ruoli contro E18. 719 chiamate per agente, zero errori core E20, prefisso identico di 456 azioni; controlli identici nelle 263 transizioni successive. Topologia verificata, bundle eseguito senza __file__.

Delta cassa +2775/+4629 sul seed 201 e -907/-907 sul 203; media +1397,5. Margine medio +865. Stress colture e fughe non peggiorano; PASS cresce nel primo seed e cala nel secondo. Decisione DEVELOPMENT_SIGNAL_ONLY: nessuna promozione o submission. Due seed già esposti, non quattro repliche indipendenti; riservati 180911301–307 inutilizzati.

[Specifica E20.2](model_specs/codex/e20/E20_2_SPEC.md) e [report leggibile dei 22 KPI](model_specs/codex/e20/reports/e20_2/REPORT.html). Bundle submission_codex_e20_772_e20v32_candidate.py, SHA256 2e23faa7e581b0ab3a391da0e4707e49d04b6eebeaff4bdb495cacd9e91b317c. Verifica visiva HTML bloccata dalla policy del browser; dati e struttura verificati.

Ripresa: analizzare perché il seed 203 perde cassa e margine nonostante meno PASS, confrontando produzione, vendite e impiego del lavoro liberato. Completare le verifiche CARE/grano/FEED elencate sotto prima di formulare un nuovo intervento. La diagnosi preliminare ha contato 708 richieste CARE D20–30 in sette replay E20.1 (131 a prezzo minimo, nessuna prima del FEED o su animale già curato), ma non misura bonus persi o valore marginale. Non considerare chiuso l'audit del contratto. E18 resta il riferimento esterno; verificare la submission E18 del 10 settembre prima di eventuali nuovi invii.

---

## 2026-09-12 — Verifiche da fare dopo la revisione del contratto engine

Aggiornato [ENGINE_CONTRACT.md](foundation/ENGINE_CONTRACT.md) con vendite al
prezzo minimo, scambi concorrenti per unità, acquisti di grano/fertilizzante
e perdita del bonus CARE senza alimentazione nel giorno di produzione.
Il confronto del 12 settembre trova corrispondenza di contenuto fra i due
file principali locali e il sorgente ufficiale; non certifica la versione
distribuita sui server. I test precedenti usavano l'engine reale: le lacune
del documento non implicano che le simulazioni applicassero regole diverse.

**Prossimo lavoro: diagnosi su E18, E19 ed E20.1, con priorità D20–D30.**
E18 resta il riferimento esterno. Nessuna delle verifiche seguenti è stata
ancora completata o ne è stato quantificato l'impatto economico.

1. **CARE senza resa aggiuntiva.** Per animale, ricostruire CARE richieste
   ed eseguite, alimentazione, bonus accumulato/usato/perso, calendario di
   produzione, saturazione e raccolte. Quantificare cure senza beneficio
   per mancata alimentazione, capienza o fine partita, distinguendole dai
   comandi non eseguiti. Il filtro `care_can_add_yield` di E20.1 assume
   alimentazione futura e raccolta tempestiva: verificare quanto spesso
   queste ipotesi falliscono. Per attribuire valore marginale a una cura,
   non basta contare il prodotto finale: serve un confronto controfattuale.
2. **Costo previsto ed effettivo degli acquisti di grano.** Nel bundle E18
   è presente una stima di acquistabilità basata su denaro disponibile
   diviso prezzo osservato. Verificarne l'attivazione nella policy corrente
   e confrontare quantità richieste/eseguite, costo stimato/reale e riserva
   di cassa. Il prezzo di ogni acquisto usa lo stock meno uno e può cambiare
   durante il batch. Separare l'effetto del prezzo da capacità del deposito,
   ordini precedenti e concorrenza; verificare le corrispondenti logiche
   anche in E19/E20.1 senza presumere che siano identiche.
3. **Legame con FEED mancati e manodopera.** Collegare eventuali acquisti
   insufficienti a scorte disponibili, prelievi, trasporto e servizi FEED.
   Distinguere carenza di grano, grano presente ma non consegnato e servizio
   escluso dalla pianificazione. Misurare bonus CARE persi, stress/fughe,
   PASS e lavoro potenzialmente recuperabile; non dedurre causalità dalla
   sola coincidenza temporale.
4. **Quantificazione prima della modifica.** Usare inizialmente i replay
   diagnostici già disponibili. Registrare una singola ipotesi d'intervento
   prima dei nuovi risultati; confrontare controllo e variante dallo stesso
   stato, con memoria ricostruita e avversario libero di reagire. Valutare
   cassa, margine e traiettorie dei 22 KPI fino a D30. Richiedere 719 chiamate
   per agente, controlli esatti e assenza di errori core strumentati.

Il riordino commerciale H006 è già misurato: +18,5 di cassa e +34,5 di margine
medi su due seed con entrambi i ruoli, altri 21 KPI identici. Non estendere
questo risultato alle approssimazioni su acquisti o CARE e non ripetere lo
stesso esperimento senza una nuova ipotesi. Vendite al minimo e saturazione
durante il batch restano rilevanti per l'inferenza del mercato, non una prova
di errore nei ricavi accreditati dall'engine.

I seed 180911301–307 restano riservati e inutilizzati. Nessuna variante è
promossa con questa revisione documentale. Prima di una nuova submission,
verificare lo stato dell'E18 già inviata il 10 settembre come indicato sotto.

---

## 2026-09-10 - Chiusura sessione e nuova submission E18

Budget residuo ridotto: fermati gli esperimenti. Reinviato il bundle E18.2 V4D invariato (SHA256 c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7), migliore candidato esterno documentato. Kaggle mostra Pending al salvataggio; punteggio nuovo non ancora disponibile. Punteggi storici osservati: E18 1162,9 (reinvio precedente 1083,5), E19 V48 932,6, E20.1 922,8. Questi punteggi non sono il risultato del nuovo invio.

H001-H006 conclusi come diagnostici, nessuna variante promossa. H006 completo: +18,5 cassa e +34,5 margine medi su due seed/entrambi i ruoli; altri 21 KPI identici. E20v29-v31 restano esperimenti non adottati. Salvati codice, protocolli, risultati e replay compressi. Cache Python escluse da Git e mantenute: cancellazione bloccata dalla revisione automatica. Nessun dato sperimentale eliminato.

Ripresa: verificare prima lo stato della nuova E18 su Kaggle e aggiornare la ricevuta `model_specs/codex/evolution/E18_RESUBMISSION_20260910.json`; non reinviare alla cieca. Leggere il report H006_FULL prima di nuove modifiche. I seed 180911301-307 restano riservati e inutilizzati. Non confondere i piccoli guadagni commerciali H006 con un miglioramento della manodopera.

---

## 2026-09-10 — H006: quattro prosecuzioni complete verificate

Completate quattro prosecuzioni modificate e quattro controlli esatti fino a D30, E19 contro E18, seed 180910204 e 180910206, entrambi i ruoli. Tutti gli otto rami hanno 719 chiamate per agente, DONE/DONE e zero errori nei core strumentati; ogni controllo riproduce 263 transizioni complete dopo 456 azioni ricostruite per agente. Il forecast H006 e ricostruito dalla storia propria e coincide con le predizioni congelate.

Delta cassa terminale medio +18.5, intervallo [+17, +20]; delta margine medio +34.5, intervallo [+32, +37]. Due seed, non quattro repliche indipendenti. Beneficio iniziale esattamente conservato fino a D30: True. Lavoro, servizi e fattorie fisiche invariati in entrambi gli agenti: True. Differenza di cassa isolata negli incassi delle fragole, con uguali volumi/stock finali, altre vendite, acquisti e salari: True.

Sono disponibili le traiettorie dei 22 KPI di entrambi gli agenti, le differenze giornaliere e due grafici completi. Nessuna modifica o promozione dei modelli. Il campione e diagnostico gia esposto; i seed riservati restano inutilizzati. Questa verifica misura la persistenza di un singolo riordino D20 H1: non dimostra una regola utile ogni giorno, un miglioramento della manodopera o un vantaggio su altri avversari.

[Report e 22 KPI](model_specs/codex/evolution/reports/H006_FULL/REPORT.md).

---

## 2026-09-10 — H006: ricavi certi al prezzo minimo

H006 recupera le vendite proprie di prodotti non acquistabili gia al prezzo minimo come ricavi certi, senza stimare il volume concorrente. Soglie e campione invariati rispetto a H005.

Ricostruzioni identificate: 83 -> 116/420; previsioni: 31 -> 40/84. Errori storici 0, errori forecast 0, riordini selezionati 4, riordini negativi 0, delta cassa one-step totale 74.0. Decisione: **DIAGNOSTIC_ONLY_REQUIRES_FULL_CONTINUATIONS**, non adottato.

Passati 120 casi sintetici sul motore, inclusi casi di astensione per fragole e grano al minimo. Riprodotte 420 testimonianze e 84 previsioni senza D20/seguito e senza azioni o stato privato avversari; input e predizioni invariati. Le predizioni H005 restano identiche. Nessuna nuova partita completa, nessuna modifica ai tre modelli, nessun accesso ai seed riservati.

Gli errori sono misurati solo nei casi coperti del campione diagnostico gia esposto (sette seed, ruoli accoppiati). Le astensioni non sono successi. I prodotti che raggiungono il minimo durante il batch restano un limite del modello inverso; il presente esperimento non ne ricostruisce la saturazione.

[Report H006](model_specs/codex/evolution/reports/H006/REPORT.md).

---

## 2026-09-10 — H005: transazioni miste, copertura maggiore ma zero riordini

Completato il seguito preregistrato di H004, con SELL/BUY_PRODUCT/BUY_SEED/HIRE e soglia invariata. Sui medesimi 42 replay diagnostici: 83/420 ricostruzioni identificate (H004: 64), 31/84 previsioni (H004: 18), zero errori nei casi coperti. Tutte le previsioni sono not_first: E18 24, E19 7, E20.1 zero. Nessun riordino selezionato, nessun guadagno dimostrato: NON ADOTTATO.

Passati 24 test sintetici sul motore e riproduzione di 420 testimonianze/84 previsioni senza D20 o seguito, senza azioni/privato avversari, con input e hash predizioni invariati. Diagnosi: 116 residui incompatibili su latte/lana, 50 gia al prezzo minimo iniziale. Prossimo passo: nuovo protocollo per il ricavo certo dei prodotti non acquistabili gia al minimo e, separatamente, saturazione durante il batch. Nessuna modifica ai modelli o ai seed riservati; nessuna nuova partita o submission.

[Report H005](model_specs/codex/evolution/reports/H005/REPORT.md) · [Protocollo](model_specs/codex/evolution/H005_PROTOCOL.md).

---

## 2026-09-10 — H004: previsione da storia propria, utilita operativa zero

Test preregistrato su84situazioni del torneo diagnostico, cinque H1 precedenti D15-D19, nessun accesso ai seed riservati. Modello inverso da cassa/deposito propri, ordini propri e mercato pubblico, con consumo cittadino e costo HIRE ricostruiti. Enumera posizioni prima/uguale/dopo compatibili con ricavi; astensione per acquisti propri, floor, residuo negativo o ambiguita. Forecast con almeno2testimonianze univoche concordi, soglie congelate. Predizioni scritte/hashate prima di leggere le etichette D20 e payoff H003.

420testimonianze:64identificate,0errori storici;14ambigue,10floor,86residuo negativo,108ordini propri non supportati,138senza vendita fragole propria.18/84forecast coperti,0errori: tutti E18 e tutti not_first. E19/E20.1: astensione totale. Nessun riordino H003 selezionato, delta zero. **Non adottato: utilita operativa zero**, non considerare le astensioni successi o la precisione selettiva generalizzazione.

CHECKS: riprodotte420testimonianze e84forecast con D20/seguito rimossi e fattoria avversaria pubblica oscurata; azioni/privato avversari non passati al classificatore, input immutabili, hash predizioni invariato dopo valutazione. Non sono nuove partite complete. Prossimo passo tecnico: acquisti/vendite misti e gestione floor nel modello inverso, poi nuovo test temporale; nessun abbassamento post hoc delle soglie. Il residuo negativo puo derivare anche da floor, non solo acquisti avversari. [Report H004](model_specs/codex/evolution/reports/H004/REPORT.md) · [Protocollo](model_specs/codex/evolution/H004_PROTOCOL.md) · [Controlli](model_specs/codex/evolution/reports/H004/CHECKS.json).

---

## 2026-09-10 — H003: priorita nel batch e concorrenza

Proseguito il metodo a tre. Il mercato esegue gli ordini per posizione nella lista e quota le unita concorrenti in lockstep. H003 preregistrato: una tantum in D20 portare SELL STRAWBERRY davanti alle sole altre SELL precedenti, senza cambiare orario, quantita o lavoro. Condizione basata solo sugli ordini propri.

Scan diagnostico:42transizioni originali esattamente riprodotte,84decisioni,7seed/ruoli. E18 gia prima in28/28casi (non applicabile). E19 applicabile28:19positivi/9negativi, delta medio+29,1; E20.1:20positivi/8negativi,+33,4. Contro E18 14/14positivi per entrambi (+87,0/+87,1); contro altra versione media-28,7/-20,3. Nessuna generalizzazione dal solo avversario E18.

Quattro nuove prosecuzioni complete (due seed201/202 ruolo0), controlli H001/H002 riusati dopo hash: E19 cassa+202/+179, margine+377/+340; E20.1 cassa+157/+195, margine+292/+368. Stati fisici, servizi, stress e fughe identici; quantita fragole vendute identiche, delta cassa interamente incassi fragole, altre vendite/acquisti/salari invariati.719chiamate per agente, DONE/DONE, zero errori core strumentati, parita fino al trigger e controlli fino al terminale. E18 ramo non applicabile, controllo riusato.

Diagnosi retrospettiva: con fragole avversarie in posizione0 ci sono28positivi/0negativi; in posizione1,11/8; in posizione2,0/9. Non e un input osservabile contemporaneo: **H003 non adottata**. Prossimo passo: verificare se la storia osservata permette di stimare comportamento/ordine concorrente, senza usare nomi del modello o azioni avversarie future. Seed di validazione180911301-307 non toccati. [Report H003](model_specs/codex/evolution/reports/H003/REPORT.md) · [Protocollo](model_specs/codex/evolution/H003_PROTOCOL.md) · [22KPI](model_specs/codex/evolution/reports/H003/daily_22_kpi.csv).

---

## 2026-09-10 — H002: separati lavoro fisico e calendario delle vendite

Continuato il metodo a tre, riferimento E18. Scomposizione esatta dei ricavi sul torneo diagnostico42partite: E20.1 meno E19 contro E18 D20-D24, delta vendite-1229,4 = componente volumi+56,0 e componente prezzi realizzati-1285,4. Fragole-865,4 (+149,7 volumi; -1015,0 prezzi). Componente prezzi negativa in5/7seed. Analisi contabile, non attribuzione causale universale.

H002 preregistrato: omissione una tantum della prima richiesta SELL STRAWBERRY in D20; tre modelli, seed180910201/202, ruolo0, avversario reattivo. Sei situazioni, nove nuove prosecuzioni piu tre controlli H001 riusati dopo hash sorgente/bundle/engine. Parita controlli263stati/coppie azioni fino al terminale; trattamenti identici prima del trigger,719chiamate per agente, DONE/DONE, zero errori nei core dotati di contatore.

Delta cassa finale sui due seed: E18-391/-162 (margine-1100/-421); E19+93/+81; E20.1+126/+46. Stress e fughe invariati. In tutti i casi comandi di lavoro di entrambi gli agenti identici, stati fisici delle fattorie identici esclusa cassa, servizi effettivi identici; uguali quantita totali fragole vendute e stock terminale. Delta cassa interamente riconciliato con incassi fragole; altre vendite, acquisti e salari invariati. Primo SELL riuscito rinviato H1->H2, tranne E18seed202 H1->H3. **Nessuna promozione**: due seed, segno opposto fra modelli, nessuna regola universale di ritardo. Ora e verificato un effetto locale del calendario di vendita separato dal lavoro fisico.

Prossima ipotesi da formulare: prezzo ottenibile e concorrenza nelle finestre di vendita, con condizione osservabile, senza applicare un ritardo fisso a tutte le topologie. Il singolo rinvio non spiega tutto il divario medio fra versioni. Seed180911301-307 ancora riservati e non eseguiti. [Report H002](model_specs/codex/evolution/reports/H002/REPORT.md) · [Volumi e prezzi](model_specs/codex/evolution/reports/sales_20260910/REPORT.md) · [22KPI](model_specs/codex/evolution/reports/H002/daily_22_kpi.csv).

---

## 2026-09-10 — Metodo di evoluzione a tre: E18, E19, E20.1

E18 e il riferimento principale per lo sviluppo. Sospesa la successione di euristiche E20: costruito un banco diagnostico che separa traiettorie complete, interventi dallo stesso stato e validazione riservata. Riusate tutte le 42 partite e20_1_confirmation, sette seed ormai esposti, tutti gli accoppiamenti/ruoli; esportati i 22 KPI con identita dell avversario. Finestre senza doppio conteggio D15-D19, D20-D24, D25-D30, flussi di cassa riconciliati esattamente. E19 supera leggermente E18 nella media interna; questo non modifica il riferimento esterno, ma impedisce di assumere una superiorita universale. Contro E18, E20.1 perde 3397 di cassa media rispetto a E19 (migliora in 1/7 seed); D15-D24 il costo del lavoro e identico, il divario contabile e soprattutto nelle vendite.

H001 completato sui tre modelli, seed180910201 ruolo0: ricostruzione di 456 azioni per agente fino a D20; controlli riproducono esattamente le successive 263 coppie di azioni e 263 stati fino al terminale (escluso solo remainingOverageTime). Sei rami completi, 719 chiamate per agente, nessun errore nei core che espongono il contatore. Capsule con stato/configurazione/info seed, riferimenti alla storia e hash engine/bundle. Nessuno scambio di controller fra fattorie.

Intervento una tantum: omessa una richiesta HIRE nel primo batch D20, poi reazione libera di entrambi gli agenti. Delta cassa E18 +7930, E19 +4096, E20.1 +413. **Nessuna promozione**: E18 peggiora stress22->34 e fughe0->1; E19/E20.1 sono risultati locali su un solo seed. E18 resta a11 manovali in D20, E19 ed E20.1 recuperano12 entro H3: il trattamento non equivale alla stessa riduzione di capacita. Lettura competitiva supplementare post hoc: delta margine E18+4167, E19-5469, E20.1+5501; includere il margine esplicitamente nei futuri protocolli.

Seed180911301-307 riservati e non eseguiti. Prima di aprirli congelare candidato, hash, avversari e soglie. Prossimo passo: separare numero/orario/assegnazione della manodopera e spiegare il divario vendite con volumi, prezzi e tempi di consegna; nuovi interventi predefiniti e replicati sul campione diagnostico. [Banco e istruzioni](model_specs/codex/evolution/README.md) · [Analisi a tre](model_specs/codex/evolution/reports/diagnostic_20260910/REPORT.md) · [H001](model_specs/codex/evolution/reports/diagnostic_20260910/H001_REPORT.md).

---

## 2026-09-10 — E20v31: chiusura giornaliera D20-D29, non adottata

Sei confronti completi contro E18 su tre seed esposti, entrambi i ruoli. Servizi su colture/animali esistenti svincolati dalle code nelle ultime sei ore di D20-D29, con controlli di materiali e rientro conservati. Cassa media 61.571,7 -> 60.603,7 (-968; -1,57%); PASS D20-D30 251,3 -> 222,0 (-11,67%); MOVE 1654,3 -> 1693,7 (+2,38%). Coltivate: somma checkpoint 419,7 -> 427,7; stress intera partita 2,33 -> 2,00; zero fughe animali. Solo un seed migliora la cassa; ruoli invertiti identici. **E20v31 non adottata; E20.1 pubblicata invariata.**

Diagnosi baseline seed 180910101 ruolo0, 719 azioni identiche: 209 PASS; tentativi con viaggio/lavoro oltre il tempo in 167 opportunita, blocco coda in 132, materiali mancanti in 15, prenotati in 2, riserva rientro in 10, margine approvvigionamento in 3 (categorie sovrapposte). Solo tre opportunita di lavoratore libero H19-H24 hanno servizi preparabili ignorando le code. Non sono conteggi di PASS evitabili. La variante modifica anche assegnazioni gia eseguibili. Priorita successiva da verificare: costo dei percorsi/rifornimenti prima del finale, senza assumere che piu manovali o meno margine risolvano il problema.

Verifiche: 719 chiamate per entrambi in tutte le partite, DONE/DONE, zero errori core E20v31, topologia772, azioni D1-D19 identiche. [Report](model_specs/codex/e20/reports/labor_closing/REPORT.md) · [Diagnosi](model_specs/codex/e20/reports/labor_closing/DIAGNOSIS_SUMMARY.json).

---

## 2026-09-10 — E20v30: trasferimento mirato del lavoro residuo

Sei partite complete su tre seed gia esposti, entrambi i ruoli contro E18. E20v30 conserva tutte le azioni di E20v28: delta economico e operativo zero. Due trasferimenti provvisori di coda non cambiano il comportamento. **Non adottata**, E20.1 pubblicata invariata.

Diagnosi sul seed 180910101 ruolo0, 719 azioni riprodotte: 209 PASS D20-D30, 161 nelle ore22-24; 194 con preparazioni tutte rifiutate, 7 missioni in attesa di input, 3 con preparazione ma senza assegnazione, 5 senza tentativi. Non equivale a 209 PASS evitabili. Prossimo punto da verificare: rifiuti per tempo/materiali e pianificazione della chiusura giornaliera.

[Report](model_specs/codex/e20/reports/labor_transfer/REPORT.md) · [Traccia](model_specs/codex/e20/reports/labor_transfer/ADMISSION_DIAGNOSTIC.json).

---

Checkpoint precedenti:

## 2026-09-10 — Manodopera D20-D30: primo test concluso

E20v29: code ripianificate ogni ora D20-D29; D1-D19 e gestore terminale D30 invariati. Sei confronti appaiati contro E18 su tre seed gia esposti, ruoli invertiti identici. Cassa +680,7 (+1,11%), positiva in un solo seed; PASS D20-D30 251,3 -> 239,7, MOVE 1654,3 -> 1655,3, costo manovali 3765 -> 3767. Zero perdite animali ma stress 2,33 -> 3,00. **Non adottata**. E20.1 pubblicata invariata.

[Report](model_specs/codex/e20/reports/labor_d20_d30/REPORT.md) · [Dati e protocollo](model_specs/codex/e20/reports/labor_d20_d30/RESULT.json). Prossima ipotesi: trasferimento mirato del lavoro residuo a lavoratori liberi con minor costo di viaggio; non ancora implementato.

---

Checkpoint precedenti:

## 2026-09-10 — Prima coorte E20.1 esterna

Submission **56142698 Complete**, rating osservato alla prima acquisizione **944**. Congelati 22 replay: 21 competitivi e un self-play separato; escluso l'incontro Jessica Jennifer ancora in corso al cutoff. 12/21 vittorie, cassa media 84.022,24 contro 79.886,71, zero perdite animali E20.1 e topologia finale 772 in 21/21. Tutti 720 stati DONE/DONE, ledger riconciliati. Il report mostra i 22 KPI D1-D30 con mediana e banda min-max, CSV e catalogo hash.

[Report esterno](model_specs/codex/e20/reports/external_first_20260910/REPORT.html). Benchmark Top772: identita da chiarire con il proprietario; non presente nel registro o tra gli avversari della coorte. Non sostituire silenziosamente Top772 con Top770-002, gia consumato. Nessuna modifica alla policy o nuova submission in questa acquisizione.

---

Checkpoint precedenti:

# Stato del progetto — E20.1, correzione caricamento Kaggle

Aggiornamento 2026-09-10. Il primo invio E20v28 ha fallito la validazione (episodio 107444826): `NameError: name '__file__' is not defined`, alla prima chiamata. Il loader Kaggle usa un namespace exec senza quel campo; i precedenti test con runpy non riproducevano questa condizione.

Corretto soltanto il nome diagnostico passato a due compile dei moduli incorporati. Il bundle originale resta congelato. Nuovo file: `submission/submission_codex_e20_772_e20v28_loaderfix.py`, SHA256 `9d84c838de39c2c8df620a21db258ea4a4065a5a2b4f75288bde53218d71c9bb`.

Verifica: 2 test di regressione passati senza __file__ e senza letture di file; 719 azioni identiche per ciascuno dei due ruoli (1.438 totali) sui replay E20v28 seed 180910101, usando la funzione agent del bundle caricata con exec. Nessuna modifica alla strategia. Nuovo invio Kaggle: **Pending**; rating non disponibile.

Il risultato interno rimane: +6,16% nello sviluppo, -5,82% nella conferma indipendente contro E18; non promossa economicamente. La pubblicazione serve alla verifica esterna richiesta dal proprietario.

- [Ricevuta del fallimento](model_specs/codex/e20/artifacts/E20_1_EXTERNAL_PUBLICATION_RECEIPT.json)
- [Ricevuta del nuovo invio](model_specs/codex/e20/artifacts/E20_1_LOADERFIX_PUBLICATION_RECEIPT.json)
- [Verifica di parita](model_specs/codex/e20/reports/e20_1/LOADER_FIX_VALIDATION.json)
- [Report economico e 22 KPI](model_specs/codex/e20/reports/e20_1/REPORT.html)

---

Checkpoint precedenti (stati di pubblicazione storici):

## 2026-09-10 — E20.1 inviata per verifica esterna

Su richiesta esplicita del proprietario, caricato su Kaggle il bundle E20v28 congelato (target 772), SHA256 `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. Stato osservato: **Pending**, nessun rating ancora disponibile. Il mancato superamento del gate economico interno rimane registrato; questa pubblicazione e una verifica esterna sperimentale.

[Ricevuta](model_specs/codex/e20/artifacts/E20_1_EXTERNAL_PUBLICATION_RECEIPT.json) · [Submission Kaggle](https://www.kaggle.com/competitions/kaggriculture/submissions).

---

Checkpoint interno precedente (le indicazioni di mancata pubblicazione qui sotto sono storiche):

# Stato del progetto — E20.1, revisione del pianificatore

Lavoro del 2026-09-10 concluso. **Non promossa: il gate indipendente non è superato.** Nessuna nuova pubblicazione Kaggle. La candidata è E20v28, target 7–7–2: percorsi con tile lontani inseriti per primi a parità di urgenza e filtro dei CARE senza incremento produttivo possibile.

Sviluppo: 10 seed già noti, entrambi i ruoli; +6,16% rispetto a E19, 8/10 seed positivi, stress 2,30 per partita, zero perdite animali.

Conferma indipendente: 7 nuovi seed, 42 partite tra E18/E19/E20.1. Contro E18, delta E20.1−E19 -5,82%, 1/7 seed positivi, stress 3,79, perdite animali 0. Il risultato di sviluppo non sostituisce questa verifica.

| Modello | Vittorie / partite | Cassa media torneo |
|---|---:|---:|
| E18 | 20/28 | 60.978,89 |
| E19 | 13/28 | 61.443,11 |
| E20.1 | 9/28 | 59.671,43 |

## Artefatti e ripresa

- [Report finale E20.1](model_specs/codex/e20/reports/e20_1/REPORT.html).
- [Torneo e 22 KPI](model_specs/codex/e20/reports/e20_1_confirmation/REPORT.html).
- [Specifica](model_specs/codex/e20/E20_1_SPEC.md) e [protocollo](model_specs/codex/e20/E20_1_PROTOCOL.json).
- [Decisione verificata](model_specs/codex/e20/reports/e20_1/DECISION.json) e [verifica delle 42 partite](model_specs/codex/e20/artifacts/E20_1_CONFIRMATION_VERIFICATION.json).
- [Bundle E20.1](../submission/submission_codex_e20_772_e20v28_candidate.py).
- [Controllo 770 con lo stesso pianificatore](model_specs/codex/e20/reports/e20_1/topology_control/REPORT.html): controllo di ricerca, non nuova versione ufficiale E19.

SHA256 E20.1: `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. E18 V4D, E19 V48 e la precedente E20v18 restano congelati. Riferimento pubblicato invariato: submission Kaggle 56101593, V48 770.

Tutti i 17 seed usati in questa revisione sono ora esposti: non riutilizzarli come holdout dopo modifiche. Il gate è definito prima dei risultati e distingue cassa media, distribuzione per seed e fragilità biologica. Non promuovere una variante soltanto per il migliore seed o per il numero di WATER/PASS.

Su questo portatile usare un solo processo per i confronti ufficiali. Il solo stato finale DONE non basta: entrambi gli agenti devono ricevere 719 chiamate. Cinque tentativi incompleti del torneo e due del controllo 770 sono archiviati in `invalid_under_load`; sono stati ripetuti senza modificare modelli, seed o limiti di gioco. Non includerli nelle medie.

Il lettore dei replay deve ricostruire il campo condiviso `step` anche per il ruolo 1. Le traiettorie standard e i saldi derivano da ledger verificati. I replay compressi restano disponibili localmente e ignorati da Git.

[Checkpoint precedente E20v18](history/e20_1_before_20260910/PROJECT_STATE.md).
