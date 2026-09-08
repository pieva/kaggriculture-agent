# Nuovi Top / V48: analisi completata — 2026-09-08

## Checkpoint operativo 2026-09-08: V48 e PASS

**Priorità assoluta della prossima versione: ridurre i PASS evitabili attraverso la pianificazione biologica e della manodopera, solo 770.** V48 pubblicata (56101593) resta congelata; nessuna nuova variante o pubblicazione in questo checkpoint.

[Stato, piano, inventario completo dei sorgenti e riproduzione](foundation/V48_PLANNING_AND_BUILD_IT.md). I checkpoint precedenti sono storici; i nuovi Top sono ormai esposti e non costituiscono holdout.


Report principale: docs/model_specs/codex/e19/reports/new_top_v48_20260908/REPORT_NUOVI_TOP_V48_IT.html
12 autori sottoposti a screening, un nuovo Top770 qualificato: Top770-003 (Subin An), 4/5; conservato anche il quinto 10-7-0. Registro comune aggiornato: tutti esposti/consumati per questo ciclo, non riutilizzabili come holdout. Quattro report completi 22 KPI e verifica DOM superata (grafici, tabelle, legenda, selezione giorno), UTF8 e hash.

Conclusione: conservare pianificazione biologica e ottimizzare prima percorsi/personale su 770. Prima alternativa proposta per un test futuro: 10-7-0, Q2 agricolo; non implementata e non provata causalmente superiore. D15-D25 Subin corpus completo n5: MOVE 111 vs V48 150,24; PASS 6,91 vs 28,79; WATER 44,27 vs35,12; CARE16,8 vs12; persone11,53 vs13; infestanti0 vs2,15. Corpus diversi: non inferire rating dalla cassa.

Suliman 10-7-0 daD11 in3/3 ma con perdite animali. Matthew biforca prima della chiusura: 3x770, 2x11-7-0 aD15 ->10-7-0 aD16 ->10-7-1 aD29. Subin4x770 e1x10-7-0 stabiliD15-D30. Tutti13 replay approfonditi sbloccano e usanoQ2 entroD12. Censimento contiene layout, date semine/collocamento e cronologia. Causa economica della scelta tra template ancora non dimostrata; non copiare quote/date senza test. Nessuna modifica V48/pubblicazione aggiuntiva.

---

# V48: primi otto incontri esterni — 2026-09-08

Submission 56101593 Complete; rating osservato 822,1. Otto incontri non self-play: 5 vittorie, 3 sconfitte, tutti 720 stati DONE/DONE. Replay congelati integralmente in docs/model_specs/codex/e19/artifacts/derived/v48_external_20260908; first_cohort.json include hash e risultati. Non è ancora dimostrata superiorità su V29/V4D. Diagnosi KPI dei replay ancora da eseguire.

Lavoro Top in corso: registro storico verificato, autori esposti esclusi. Screening acquisito in new_top_screen_20260908; scratch/new_top_cohorts.json elenca 12 autori. Subin An 4/5 finali 770, Matthew 3/5 escluso dal criterio finale storico. Nuova indicazione utente: confrontare anche D15 e stabilizzazione Q2, separare assetto produttivo e chiusura. Non cambiare retroattivamente criterio senza documentarlo. Dettagli quantitativi variability.json e variability_diagnosis.json. Suliman 10-7-0 da D11 in 3/3; SpaTaro ha anche perdite animali a D20-D21, non tutta variabilità è ottimizzazione. Nuovi report comparativi ancora da completare; nessuna policy modificata.

---

# V48 pubblicata per benchmark esterno — 2026-09-08

Submission Kaggle None, stato osservato Pending. File `submission\submission_codex_e18_770_v48_external.py`, SHA256 `57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`. URL: https://www.kaggle.com/competitions/kaggriculture/submissions
Policy V48 invariata. Bundle di 16 moduli verificati contro hash congelati; partita completa standalone seme 180903001 posizione 0 identica nei sides al riferimento, 719 chiamate, zero errori/incomplete. I sei benchmark locali della policy restano validi. Attendere i replay esterni per valutare generalizzazione; il punteggio locale non implica rating Kaggle. Nessuna variante 662. Diagnosi aperta: perdite produttive D16–D23, separandole da due fragole esaurite D28 senza produzione persa.

---

# Rettifica audit V48 — 2026-09-08

La fragola [2,9] D28 seme 180903003 è raccolta a H24 ed esaurita. WATER ritarda l'infestante di una sola azione, senza altra resa. Non correggere la policy per questo caso. Sei replay rieseguiti con sides integralmente uguali ai congelati. Audit V48: 22 vecchi eventi, 20 con prodotto/potenziale residuo, 2 esauriti e vuoti. I vecchi conteggi delle altre versioni NON sono riclassificati e non sono comparabili a quello nuovo. V48 resta candidata locale, non pubblicata. Solo 770.

Report: docs/model_specs/codex/e19/reports/lifecycle_audit_770_20260908/REPORT_AUDIT_BIOLOGICO_V48_IT.html
Prossimo passo: diagnosticare gli eventi produttivi del registro; separare scadenza del raccolto, acqua e costo del rinnovo. Non elevare priorità su piante senza prodotto e senza produzioni future.

---

# V48: WATER produttivo prima di HARVEST — 2026-09-08

Decisione: V48 candidata locale migliorativa di V47, nessuna pubblicazione. Cassa +1.486 (+1,64%), 6/6 vittorie vs 4/6. Grano raccolto D28–D30 38,67->51,67; carote 21,33->32, entrambe maggiormente vendute. Residuo: fragola [2,9] a D28 sul seme 180903003 muore in entrambe le posizioni, portando le perdite idriche da 20 a 22. Questo e un caso diagnostico, non una coordinata/seed da codificare nella policy: profilare il percorso e il carico residuo prima di alzare ancora le priorita. V41 mantiene cassa superiore ma margine competitivo/superficie e mortalita peggiori; resta controllo. Nove report V48 verificati via DOM, dati UTF8 e SHA256.

Solo 770. V48 deriva da V47. A D28–D30 conserva WATER prima del raccolto in scadenza sulle annuali non ancora irrigate, in finestra di resa e sotto massimo. Incremento stimato +1/+2 limitato al massimo osservato; valore della visita aggiornato al prezzo corrente. Offre HARVEST breve a priorita inferiore e impedisce che il lavoro WATER+HARVEST non fattibile degeneri in solo WATER. Prime consistenze, ledger e KPI D1–D27 verificati uguali a V47.

- v41: cassa 94704.33, V4D 91364.00, margine relativo 3.66%, vittorie 6/6; perdite idriche 26, animali 0, infestanti mediane D30 20.0.
  Raccolte/vendite D28–D30: {'WHEAT': {'harvested': 50.33, 'sold_units': 48, 'sales_cash': 2489.33}, 'CARROT': {'harvested': 0, 'sold_units': 0, 'sales_cash': 0}}
- v45: cassa 90576.00, V4D 86554.67, margine relativo 4.65%, vittorie 4/6; perdite idriche 20, animali 0, infestanti mediane D30 23.0.
  Raccolte/vendite D28–D30: {'WHEAT': {'harvested': 41.67, 'sold_units': 54, 'sales_cash': 2793.33}, 'CARROT': {'harvested': 22, 'sold_units': 22, 'sales_cash': 1932.67}}
- v47: cassa 90719.00, V4D 86610.67, margine relativo 4.74%, vittorie 4/6; perdite idriche 20, animali 0, infestanti mediane D30 23.0.
  Raccolte/vendite D28–D30: {'WHEAT': {'harvested': 38.67, 'sold_units': 46, 'sales_cash': 2372.33}, 'CARROT': {'harvested': 21.33, 'sold_units': 21.33, 'sales_cash': 1889}}
- v48: cassa 92205.33, V4D 86751.33, margine relativo 6.29%, vittorie 6/6; perdite idriche 22, animali 0, infestanti mediane D30 23.0.
  Raccolte/vendite D28–D30: {'WHEAT': {'harvested': 51.67, 'sold_units': 61.67, 'sales_cash': 3166.33}, 'CARROT': {'harvested': 32, 'sold_units': 32, 'sales_cash': 2797.33}}

Quattro test mirati passati: resa acqua limitata, visita completa/ripiego, invarianza prima di D28, divieto ripiego solo WATER. Sei casi di sviluppo (tre semi nelle due posizioni), non validazione indipendente. Report 22 KPI e tabella quantita/prezzi; nessuna pubblicazione automatica.

Report: `docs/model_specs/codex/e19/reports/productive_water_770_20260908/v48_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# V47: servizi finali e protezione idrica D28–D29 — 2026-09-08

Decisione finale: V47 corregge tutte le 12 perdite finali V46, ma migliora V45 di soli 143 di cassa media (+0,16%); sul seme 003 perde 694 contro V4D vs 60 di V45. Non promossa/pubblicata. Prossimo intervento concreto: daily_routes_770_v47.offers_with_routes trasforma ogni harvest_due in solo HARVEST, togliendo anche WATER produttivo su annuali. Motore WATER (.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture/kaggriculture.py) aumenta resa +1/+2 nella finestra ceil(max_yield_day/2)..max_yield_day se non irrigata e sotto max. Conservare questo WATER prima di HARVEST, con raccolta breve di ripiego quando entrambi non stanno nel tempo residuo. Impatto non ancora misurato: non attribuire l'intero divario a questo meccanismo. Otto report completi V47 verificati via DOM, dati/UTF8/hash.

Solo 770. V47 deriva da V46 e aggiunge protezione WATER per piante gia stressate a D28–D29 (priorita 8 e recupero fuori area), escludendo PLANT/DIG. V46 aveva aggiunto 12 perdite idriche finali (10 carote, 2 fragole) rispetto a V45. V46 deriva da V45: prolunga piano/percorsi/certificato/dispatch fino a D29. CARE da D28 solo se care_value prevede una produzione utile entro fine partita; FEED conservato. Nessuna nuova annuale pianificata da D27. D30 riprende gestione terminale precedente. Consistenze, ledger giornalieri e KPI operativi D1–D27 verificati identici a V45.

- v41: cassa 94704.33, V4D 91364.00, scarto 3.66%, vittorie 6/6; perdite animali 0, idriche 26, infestanti mediane D30 20.0.
  Medie D28–D30: {'FEED': 8.22, 'CARE': 2.22, 'WATER': 8, 'HARVEST': 18.89, 'MOVE': 148.89, 'PASS': 48.11}
- v45: cassa 90576.00, V4D 86554.67, scarto 4.65%, vittorie 4/6; perdite animali 0, idriche 20, infestanti mediane D30 23.0.
  Medie D28–D30: {'FEED': 6.56, 'CARE': 1.11, 'WATER': 7.56, 'HARVEST': 20.44, 'MOVE': 136.67, 'PASS': 38.11}
- v46: cassa 90436.67, V4D 86652.33, scarto 4.37%, vittorie 4/6; perdite animali 0, idriche 32, infestanti mediane D30 25.0.
  Medie D28–D30: {'FEED': 8.89, 'CARE': 1.78, 'WATER': 9.56, 'HARVEST': 19.56, 'MOVE': 119.44, 'PASS': 46.67}
- v47: cassa 90719.00, V4D 86610.67, scarto 4.74%, vittorie 4/6; perdite animali 0, idriche 20, infestanti mediane D30 23.0.
  Medie D28–D30: {'FEED': 8.44, 'CARE': 1, 'WATER': 9.56, 'HARVEST': 20.22, 'MOVE': 126.11, 'PASS': 39.11}

Sette test mirati passati: quattro V46 su CARE/FEED/terminale, tre V47 su finestre temporali, esclusione nuove semine e ordine protetto dei percorsi. Sei casi di sviluppo, tre semi nelle due posizioni. Report completo 22 KPI e tabella raccolte/vendite/prezzi D28–D30. Nessuna promozione automatica o pubblicazione; V29 resta submission pubblicata.

Report: `docs/model_specs/codex/e19/reports/final_water_770_20260908/v47_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# V46: servizi pianificati fino a D29 — 2026-09-08

Solo 770. V46 deriva da V45: prolunga piano/percorsi/certificato/dispatch fino a D29. CARE da D28 solo se care_value prevede una produzione utile entro fine partita; FEED conservato. Nessuna nuova annuale pianificata da D27. D30 riprende gestione terminale precedente. Consistenze, ledger giornalieri e KPI operativi D1–D27 verificati identici a V45.

- v41: cassa 94704.33, V4D 91364.00, scarto 3.66%, vittorie 6/6; perdite animali 0, idriche 26, infestanti mediane D30 20.0.
  Medie D28–D30: {'FEED': 8.22, 'CARE': 2.22, 'WATER': 8, 'HARVEST': 18.89, 'MOVE': 148.89, 'PASS': 48.11}
- v45: cassa 90576.00, V4D 86554.67, scarto 4.65%, vittorie 4/6; perdite animali 0, idriche 20, infestanti mediane D30 23.0.
  Medie D28–D30: {'FEED': 6.56, 'CARE': 1.11, 'WATER': 7.56, 'HARVEST': 20.44, 'MOVE': 136.67, 'PASS': 38.11}
- v46: cassa 90436.67, V4D 86652.33, scarto 4.37%, vittorie 4/6; perdite animali 0, idriche 32, infestanti mediane D30 25.0.
  Medie D28–D30: {'FEED': 8.89, 'CARE': 1.78, 'WATER': 9.56, 'HARVEST': 19.56, 'MOVE': 119.44, 'PASS': 46.67}

Quattro test mirati passati su CARE utile/non utile, FEED D29 e delega terminale D30. Sei casi di sviluppo, tre semi nelle due posizioni. Report completo 22 KPI e tabella raccolte/vendite/prezzi D28–D30. Nessuna promozione automatica o pubblicazione; V29 resta submission pubblicata.

Report: `docs/model_specs/codex/e19/reports/final_services_770_20260908/v46_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# V45: ponte pianificato D26–D27 — 2026-09-08

Decisione: V45 migliora V44 in tutti i sei casi (+2.851 di cassa media, +3,25%), nessuna pubblicazione. Rispetto a V41 conserva piu superficie e minore mortalita idrica ma cassa e vittorie inferiori. Prossimo punto: raccolte e servizi D28–D30, dove riprende la vecchia chiusura; preservare il recupero D26–D27. PASS D26–D27 sale, mentre MOVE scende molto e servizi aumentano: non ottimizzare uno solo dei contatori.

Solo 770. V45 deriva da V44: prolunga pianificazione biologica, percorsi, dispatch e certificato fino a D27 incluso. A D26 nuove colture annuali solo se maturano entro D29 con D30 disponibile per raccolta/vendita: carote. A D27 nessuna nuova annuale soddisfa il margine. D28–D30 vecchia chiusura. Consistenze, ledger e KPI operativi D1–D25 verificati identici a V44 sui sei casi.

Analisi iniziale: il divario finale V44/V41 non e solo operativo; D26–D30 latte raccolto 49,33 vs 56,33, venduto 66,33 vs 69,33, prezzo realizzato circa 122 vs 159. La tabella report distingue volume e prezzo nel mercato condiviso.

- v41: cassa 94704.33, V4D 91364.00, scarto 3.66%, vittorie 6/6; animali persi 0, perdite idriche 26, infestanti mediane D30 20.0.
  Medie D26–D27: {'FEED': 10.67, 'CARE': 10.33, 'WATER': 23, 'PLANT': 2.5, 'MOVE': 189.17, 'PASS': 20}
- v44: cassa 87724.83, V4D 86642.67, scarto 1.25%, vittorie 4/6; animali persi 0, perdite idriche 20, infestanti mediane D30 26.5.
  Medie D26–D27: {'FEED': 9.67, 'CARE': 9.5, 'WATER': 22.5, 'PLANT': 0, 'MOVE': 200, 'PASS': 12}
- v45: cassa 90576.00, V4D 86554.67, scarto 4.65%, vittorie 4/6; animali persi 0, perdite idriche 20, infestanti mediane D30 23.0.
  Medie D26–D27: {'FEED': 13.67, 'CARE': 13, 'WATER': 36, 'PLANT': 5.33, 'MOVE': 152.33, 'PASS': 25.83}

Tre test mirati passati: ciclo carote a D26, rifiuto semine tarde D27, delega chiusura D28. Sei casi di sviluppo (tre semi, due posizioni), non validazione indipendente. Report completi 22 KPI, tabelle quantità/prezzi e hash sorgenti. Nessuna pubblicazione o promozione automatica; V29 resta pubblicata, V33 riferimento storico.

Report: `docs/model_specs/codex/e19/reports/closure_bridge_770_20260908/v45_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# V44: servizi oltre rinnovi provvisori — 2026-09-08

Decisione finale: V44 non promossa. V41 resta migliore economicamente in questa prova. Divario medio di cassa V44/V41: -2.190 al checkpoint D25, -6.980 al termine. Più superficie e minore sete non bastano: studiare raccolte, valore del portafoglio e chiusura senza attribuire causalità ai soli saldi di cassa. Infestanti D30 aumentano a 26,5; CARE D21–D25 peggiora a 11,8. Cinque report completi verificati tramite DOM (22 grafici, tabella e interazioni), UTF-8 e SHA256.

Solo 770. V42 estende protezione V41 a WATER delle colture gia stressate: un caso, cassa 97,290 vs V4D 112,257, zero perdite idriche e animali ma D25 coltivate 39. V43 recupera fuori area solo se il percorso previsto arriva tardi: un caso, cassa 70,555 vs 72,615, zero perdite ma D25 coltivate 38. Nessuna delle due estesa a sei casi.

V44 torna a V41: quando prepara un servizio esistente, filtra dalla coda precedente le proposte NEW_ non ancora ammesse. Permette quindi WATER/FEED ecc. anche oltre un rinnovo provvisorio, conservando ordine fra servizi e priorita originali. Nessuna modifica calendario, recupero fuori area o chiusura D26+. Le proposte non vengono cancellate dal piano.

- v41: cassa 94704.33, V4D 91364.00, scarto 3.66%, vittorie 6/6; perdite animali 0, idriche 26, coltivate mediane D25 44.0, infestanti D30 20.0.
  Medie D21–D25: {'MOVE': 161, 'PASS': 19.2, 'weed_tiles': 3.2, 'WATER': 29.47, 'FEED': 13.53, 'CARE': 12.2, 'PLANT': 6}
- v44: cassa 87724.83, V4D 86642.67, scarto 1.25%, vittorie 4/6; perdite animali 0, idriche 20, coltivate mediane D25 50.0, infestanti D30 26.5.
  Medie D21–D25: {'MOVE': 158.87, 'PASS': 17.53, 'weed_tiles': 4.13, 'WATER': 33.47, 'FEED': 13.73, 'CARE': 11.8, 'PLANT': 6.47}

Undici test mirati passati (4 V42, 3 V43, 4 V44). Sei casi di sviluppo, tre semi nelle due posizioni, non indipendenti. Report completo 22 KPI e manifest SHA256. Nessuna submission o promozione automatica: V33 resta riferimento e V29 pubblicata. Valutare tutti i KPI e la cassa relativa prima della scelta.

Report: `docs/model_specs/codex/e19/reports/water_route_770_20260908/v44_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# V41: protezione mirata FEED durante i rinnovi — 2026-09-08

Solo 770, richiesta prosegui. V40 protegge tutte le visite FEED/CARE nel packing (prima delle altre visite) e dispatcher (priorita 8): screen seed001 seat0, cassa 71,796 vs 92,029 V4D, zero perdite animali ma 7 idriche. Scartata, non estesa a sei casi. V41 limita questa protezione agli animali con consecutive_unfed>=1 e non ancora nutriti. Recupero della visita completa fuori area sin dal mattino per questi animali. Mantiene rinnovi V39, calendario acqua V38 e chiusura precedente D26+.

- v33: cassa 89624.33, V4D 91882.00, delta -2.46%, vittorie 2/6; perdite animali 0, idriche 42, coltivate D25 56.0, infestanti D30 22.5.
- v38: cassa 86395.00, V4D 84022.00, delta 2.82%, vittorie 6/6; perdite animali 0, idriche 18, coltivate D25 34.0, infestanti D30 26.0.
- v39: cassa 87540.00, V4D 83530.67, delta 4.80%, vittorie 4/6; perdite animali 4, idriche 16, coltivate D25 46.0, infestanti D30 19.0.
- v41: cassa 94704.33, V4D 91364.00, delta 3.66%, vittorie 6/6; perdite animali 0, idriche 26, coltivate D25 44.0, infestanti D30 20.0.

v39 medie D21–D25: {'MOVE': 164.07, 'PASS': 15.27, 'weed_tiles': 2.4, 'WATER': 30.4, 'FEED': 13.2, 'CARE': 11, 'PLANT': 6.67}

v41 medie D21–D25: {'MOVE': 161, 'PASS': 19.2, 'weed_tiles': 3.2, 'WATER': 29.47, 'FEED': 13.53, 'CARE': 12.2, 'PLANT': 6}

Sei casi di sviluppo: tre semi, entrambe le posizioni. Sei test packing/ordine/budget passati (V40 e V41). Report completo con 22 KPI contro Top770-001, V33, V38, V39; hash sorgenti verificati. Nessuna promozione automatica o submission. V33 resta riferimento e V29 pubblicata. Verificare regressioni acqua, superficie, PASS e competitivita prima di promuovere; il recupero di FEED non equivale a soluzione globale.

Report: `docs/model_specs/codex/e19/reports/animal_service_770_20260908/v41_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# V39: rinnovo delle fragole esaurite — 2026-09-08

ATTENZIONE: V39 non promossa. Quattro perdite animali a D23 (semi 001 e 003, entrambe le posizioni), contro zero V33/V38; vittorie 4/6 contro 6/6 V38. Rinnovi migliorano ma copertura FEED/CARE regredisce. Prossimo intervento: proteggere esecuzione dei servizi animali nel carico dei rinnovi.

Solo 770. V39 deriva da V38: rinnovo di perenni esaurite anche senza prodotto residuo/visita esistente; ciclo breve WHEAT/CARROT scelto sul margine corrente per giorno quando le fragole non arrivano a produzione. Il ciclo breve deve maturare con un giorno residuo. Nessuna eliminazione anticipata di produzioni future o prodotto da raccogliere. Acqua V38 conservata. Chiusura D26+ precedente.

- v33: cassa 89624.33, V4D 91882.00, delta -2.46%, vittorie 2/6; morti idriche 42, coltivate D25 56.0, infestanti D30 22.5.
- v38: cassa 86395.00, V4D 84022.00, delta 2.82%, vittorie 6/6; morti idriche 18, coltivate D25 34.0, infestanti D30 26.0.
- v39: cassa 87540.00, V4D 83530.67, delta 4.80%, vittorie 4/6; morti idriche 16, coltivate D25 46.0, infestanti D30 19.0.

Sei casi, tre semi 180903001–003 nelle due posizioni, gia usati nello sviluppo. Dieci test passati (4 nuovi sul rinnovo, 3 calendario V38, 3 certificato V32). Report completi con 22 KPI e confronto Top770-001, V33, V38; hash sorgenti verificati. Nessuna nuova submission; V33 resta riferimento, V29 pubblicata. Il confronto per KPI e fase resta necessario: il recupero del grano non prova di aver risolto servizi e chiusura carote.

Report: `docs/model_specs/codex/e19/reports/spent_renewal_770_20260908/v39_TOP770_D01_D30_COMPLETE_KPI.html`.

---

# Continuazione V33: prevenzione acqua V38 — 2026-09-08

Solo 770, nessun invio. V34–V37 provano recuperi/priorità urgenti ma non sono promosse.
V38 conserva le priorità V33 e distribuisce l'acqua delle fragole in due gruppi
alternati D12–D25, senza rinviare fabbisogni già necessari.
Sei casi: V38 cassa 86,395 / V4D 84,022 (+2.82%), 6/6 vittorie, 18 morti idriche;
V33 89,624.33 / 91,882 (-2.46%), 2/6 vittorie, 42 morti idriche.
Risultato misto: cassa -3.6%, superficie finale in calo, infestanti D30 26 vs 22.5.
V33 resta riferimento; V38 candidato da integrare con la successione D22–D25,
non nuova versione pubblicata. Prefisso, topologia, completamento e contabilità verificati.
Report completi: docs/model_specs/codex/e19/reports/biological_deadlines_770_20260908/.
Dettagli delle prove e runtime in NEW_SESSION.md. 662 e V29 pubblicata non modificate.

# Ottimizzazione 770 V32/V33 — 2026-09-08

Successione raccolta–risemina sbloccata con un certificato giornaliero a inserimento
nei percorsi, dopo prove V30/V31 insufficienti. V33 include anche CARE nel controllo alternativo.
Sei casi completi ciascuna, D1–D11 invariato, topologia 770 invariata:
V29 cassa 74,993 / 54 morti idriche / grano mediano D23 4;
V32 cassa 92,755 / 54 morti idriche / grano D23 23;
V33 cassa 89,624.33 / 42 morti idriche / grano D23 17.
Relativo contro V4D: -5.49%, +0.92%, -2.46%. Nessuna perdita animali/inventario o errore core.
V33 ramo di lavoro sui servizi; V32 controllo. Nessuna promozione o pubblicazione:
irrigazione, infestanti, esecuzione dei servizi prenotati e chiusura carote restano aperti.
Report: docs/model_specs/codex/e19/reports/renewal_certificate_770_20260908/.
V29 esterna e 662 non modificate. Dettagli e verifiche in NEW_SESSION.md.

# V29: primo benchmark esterno — 2026-09-08

Submission 56093101 Complete, rating osservato 860.3 (provvisorio).
Prime 11 partite completate del pannello acquisito: 5 vittorie / 6 sconfitte;
cassa media 91,930.27 contro 91,169.36, delta mediano -474.
Zero PLANT richiesti/eseguiti D21 e D22 in tutte le 11 partite. Grano mediano
23 a D20, 12 a D21, 8 a D22, 3 a D23; coltivate 61 -> 36. Morti idriche: 68.
Due report completi, contro avversari appaiati e contro Top770-001 storico:
docs/model_specs/codex/e19/reports/v29_external_20260908/.
Replay originali, profili giornalieri, risultati e hash archiviati. Nessuna modifica policy o nuova submission.
Questo benchmark conferma il difetto di successione e non costituisce promozione della V29.

# V29 inviata a Kaggle — 2026-09-08 (stato precedente)

Autorizzazione esplicita user: "ok, pubblicalo cosi vediamo un confronto esterno".
Eseguito UN invio tramite UI Kaggle, account Pietro Valocchi, competizione
kaggriculture. Stato verificato Pending, score nonancora disponibile,
submissionID nonesposto neldettaglio osservato. NON inviare duplicati.
URL https://www.kaggle.com/competitions/kaggriculture/submissions
File submission/submission_codex_e18_770_v29_external.py,853609bytes.
SHA256 fa7e3fa7df0d5f02e7937e9940ca66f411154b1059a577790d970fb41e6ec71c.
Bundle stdlib15moduli, sorgente core/assisted incorporati. SchedulerAST legge
sorgente embedded senza filelocali, importinnamespaceprivato. Ultimadef agent.
719azioni identiche originalV29 usando osservazioni complete replayV26seat0.
Manifest sorgenti verificato controhashrunV29; politica invariata.
Builder tools/build_v29_submission.py; manifest/parity/receipt in artifacts/derived/
v29_external_manifest.json, v29_external_parity.json,v29_external_receipt.json.
Pubblicazione SOLOdiagnostica, non promozione locale; nessuna modifica662.
TabKaggle mantenutadisponibile. Nessun monitoraggio automatico creato.

---

# Successioni V27–V29: esperimenti non promossi — 2026-09-08

Richiesta procedi dopo auditD21: implementati impegni persistenti raccolta->risemina.
V27 registra target/identita ciclo alla scadenza, mantiene pending attraverso
giorni e raccolta; NEW_CROP su casella liberata entra codeprio4, replan su ready
cambiato. Risolto solo meccanismo, NONprestazione. Hardqueue causa deadlock.
V28 permette servizi mentre testaNEW_CROP nonammessa. V29 scheduler filtra
NEW_CROP suvuoto/WEED dai servizi esistenti passati alcertificato: candidato
mantiene propriaWATER. Non e risolto problema generalecapacita/calendario.

18run:3revisioni x6casi180903001–003entrambiseat. PrefissoD1–11identico,
719chiamate tutti,0errori. Tretest regressione passati (V27,V28 osservazioni
reali;V29filtro certificato mantiene acqua candidata ed esistente).
Nessuna modifica policyhashate precedenti. V29usa adapterV28, schedulerV29.
Pending impiegati nelpianoD12–25; D26closureereditata, NOcalendariocarote.

Cassa/relativo/mortiacquatotali:
V26 68520/+3,03%/18
V27 72093/−14,42%/134
V28 75140/−1,41%/42
V29 74993/−5,49%/54
TuttiNONPROMOSSI. V29D21/D22ZEROSEMINEinognicaso; grano12/8nelprimo.
L'obiettivo mantenerecontinuita NONraggiunto. Nonvantareimpegnipersistenti
come soluzione. V18restariferimento. Nessunupload.

Report completo:
docs/model_specs/codex/e19/reports/succession_routes_770_20260908/daily_routes_v29_TOP770_D01_D30_COMPLETE_KPI.html
IncludeV18/V25/V26/V27/V28/V29, tabellePLANT/D21/D22, tuttecolture e
regressioni esplicite. UTF8verificato, manifest/hash eDOM22grafici verificati.
Generator tools/build_succession_routes_770_report.py.
Codice daily_routes_770_v27/v28, daily_route_scheduler_770_v27/v28/v29,
run_daily_routes_770_v27/v28/v29. Result portfolio_succession_20260907.
Nessunaltromodello oltreV29. Prossimo studio: capacita antecedente scadenze,
carico sincronizzato raccolti/risemine e acqua, non ulteriore priorita cieca.

---

# V26 audit grano D21 e codifica — 2026-09-08

Corretto mojibake nel generatore build_harvest_deadlines_770_report.py:
UTF-8 esplicito, riparate ricodifiche CP1252 ripetute, rigenerati3reportV18/V25/V26.
Verificati titolo, assenza marcatori corrotti, manifest e DOM. Policyimmutate.
Audit docs/model_specs/codex/e19/reports/wheat_d21_v26_20260908/ANALISI_GRANO_D21_IT.md
ReplayV26esistente, strumentazione esatta fino528. Sei casi granoD20=22,
D21=9,D22=6; raccoltoD21=38unita,D22=9; zeroPLANT entrambiigiorni.
Nonmorte: HARVEST lascia vuoto. D21MOVE185PASS16 (ultime3ore).
Causa: raccolto priorita6 separato daNEW_ROTATION, semina tornaNEW_CROPprio0,
nonentra nelle codepercorsi (solo servizi e rinnovi di pianteancorapresenti).
Nessuna capacita ereditata dalraccolto, queuegate blocca nuove destinazioni.
D21proposte14target,77preparefattibili,0certificati respinti/0semine;
D22proposte21target,0preparefattibili. Chiamategate1405/2110NONlavoridistinti.
Prossimo: prenotazione successiva HARVEST->PLANT/WATER concapacita e finestra
chiusura, nonaltroaumento ciecopriorita. Nessunmodello nuovo inquestoturno.

---

# V26 prevenzione decadimento — 2026-09-08

Richiesta avviare nuova versione preventiva eseguita SOLO770, nuova V26
sperimentale, NON promossa. Deriva daV25; nessuna modifica a file hashati storici.
Codice tools/daily_routes_770_v26.py e daily_route_scheduler_770_v26.py;
runner run_daily_routes_770_v26.py; eredita biological_plan_770_v25.
Funzione harvest_due: prodotto>0 e max_lifespan_step entro prossimo inizio
giorno. Raccolta pureHARVEST priorità6 nel packing/scoring; non sovrascritta
conNEW_ROTATION, supera vincoli coda; missioni attive noninterrotte.
NienteDIGcosmetico. Non implementato calendario carote, né garanzia persistente
completa scadenze di tutti i servizi. Precedenza raccolto può sottrarre acqua.

6run completi, 3test mirati passati, prefissoD1–11 identico,719chiamate tutti,
0errori/missioni residue/fughe/prodotti raccolti dispersi. Maxcall1,974s,
overagemax1,177s entrobudget60. Risultati derivati portfolio_succession_20260907.
Cassa mediaV26 68520,33 vsV25 83032,67; avversario66503vs76011,33;
relativo+3,03vs+9,24%. Mortiacqua18vs6totali. Quindi NONpromossa.

Audit un caso180903001seat0, replay completo daily_routes_v26_audit_20260908;
sides identici aoriginale. audit_v26_decay.py confronta conV25:
23decadimenti conprodotto (19grano4fragole)→ZERO; acqua1→3;
fragole esaurite giàvuote chediventanoWEED17→35. WeedstockD17 7→0,
D25 13→5, D30 30→26. CaroteD25 9→1. NONgeneralizzare zero decay oltre
auditunico. Migliore protezione raccolto non equivale a prevenzione completa
WEED o miglior partita; serve capacità servizi + riuso produttivo in tempo.

Report completo e decisione:
docs/model_specs/codex/e19/reports/harvest_deadlines_770_20260908/daily_routes_v26_TOP770_D01_D30_COMPLETE_KPI.html
Include V18/V25/V26, decadimento separato in decay_audit.json. Generatore
build_harvest_deadlines_770_report.py. Manifest/hash e DOM22grafici verificati.
V18 resta riferimento sperimentale. Nessun upload. Nessuna nuova variante
aggiuntiva dopoV26; prossimo studio integra raccolte, acqua e successioni.

---

# Audit seconda metà V25 — 2026-09-08

Analisi richiesta completata, nessuna modifica policy.
Report docs/model_specs/codex/e19/reports/late_month_770_20260908/ANALISI_INFESTANTI_CAROTE_IT.md
Replay V25 seed180903001seat0 in artifacts/derived/daily_routes_v25_audit_20260908:
sides identici originale; strumentazione719azioni identiche in audit.json.
41nuovi eventiWEED:19grano scaduto con prodotto,4fragole scadute con prodotto,
17fragole svuotate dopo ultimo raccolto,1fragola mancanza acqua. Finale30weed.
Il vecchio indicatore crop_starvation SOLOACQUA non cattura perdite perdecadimento.
D17H5otto grani seminatiD12 diventanoWEED, raccolto daassicurareD16 (84PASS).
D29H1quattordici fragole giàvuote diventanoWEED: nonconfondere conraccoltipersi.
Carote001:5PLANTD23,4D24,1D27; D26preferenza economica grano121,13vs94,54;
D27carote94,54vsgrano86,54 ma1semina; D28zeroaccettazioni crescita572rifiuti
certificato (chiamateripetute NONmissioni distinte). Seme003D26pianta14GRANO.
Prossimo: garantire HARVEST separata da NEW_ROTATION e pianificare successione
D23–D30 con capacità e finestre carote. Nessun nuovo modello implementato.

---

# Aggiornamento osservato del piano V25 — 2026-09-08

Richiesta eseguita: invalidazione piano biologico su (giorno, terra sbloccata,
numero persone osservate); code percorsi invalidate anche su nuova terra.
Intenzioni precedenti preservate, nessuna cancellazione delle missioni attive.
Solo770, D1–D11 identico; casualità e 662 ferme. Nessun upload/promozione.
Nuovi moduli immutabili: tools/biological_plan_770_v25.py,
daily_routes_770_v25.py, daily_route_scheduler_770_v25.py,
run_daily_routes_770_v25.py. Derivati V22; V23/V24 non incorporati.

Sei casi completati 180903001–003 entrambe posizioni vsV4D. 719chiamate,
0errori/missioni residue/fughe/perdite prodotti raccolti. 1fragola persa per
acqua in ogni caso (totale6), quindi non promossa. Maxcall0,485s.
6test passati inclusa regressione su osservazioni reali: stessa apertura,
61intenzioni già aD12H3, owners distribuiti dopo assunzioni, intenzioni stabili.
Report HTML verificato DOM22grafici/legenda/giorni e manifest hash.

a V22→V25: PASS D12 126→33, D13 53→39; superficieD12 36→56, D13 61→61.
D16–24 PASS57,33→50,78 MOVE118,11→125,78 WATER35,33→35,44
FEED13,44→13,78 CARE12,22→12,44. WeedsD30 28,33→27,33.
SuperficieD25 54→48, D28 26→29. Cassa91268,33→83032,67;
avversario87293,67→76011,33; relativo+4,55→+9,24%. Non successo globale.
Per seme V25 cash100203/102591/46304, identiche posizioni.
Terzo seme peggiora da68220 a46304: regressione da approfondire.
V18 resta riferimento sperimentale; V25 correzione locale da cui studiare
incarichi persistenti e scadenze, senza presentarla come versione migliore.

Report completo:
docs/model_specs/codex/e19/reports/plan_refresh_770_20260908/daily_routes_v25_TOP770_D01_D30_COMPLETE_KPI.html
Generatore tools/build_plan_refresh_770_report.py; include V18/V22/V25 e
analisi esplicita delle regressioni, tutte le colture, contabilità e servizi.
Risultati artifacts/derived/portfolio_succession_20260907/daily_routes_v25_*.

---

# Audit PASS V22 D12–D13 — 2026-09-08

Analisi richiesta, nessuna modifica policy. Report:
docs/model_specs/codex/e19/reports/pass_d12_d13_20260908/ANALISI_PASS_D12_D13_IT.md
Audit orario esatto seed180903001/seat0, azioni identiche fino a312.
D12 PASS126 (119 senza missione,7 attesa PICKUP) vsTop20;
D13 PASS53 (52 senza missione,1 attesa PLANT) vsTop25. Totali identici6casi.
BUG VERIFICATO: observe_plan V18 invalidato solo a cambio giorno.
D12 BUY_LAND H2, SW osservato H3 ma intenzioni ferme36 fino aH24;
D13 diventano61. Anche owners biologici rimangono tutti0 dopo assunzioni,
mentre codeV22 si aggiornano: incoerenza di livelli. Non ancora corretto.
D13 48/53PASS nelle ultime6ore. FEED/CARE14 entrambi i giorni.
Non tutti i terreni asciutti hanno WATER dovuto secondo needs_water.
Prossima modifica: invalidazione eventi terra/personale + incarichi persistenti
con scadenze e redistribuzione fattibile. Impatto causale marginale dei singoli
fix da misurare, non presumere119PASS tutti recuperabili. Solo770.

---

# Percorsi giornalieri 770 V20–V24 — 2026-09-07

Completata richiesta «Procediamo»: percorsi giornalieri per lavoratore,
rifornimenti per più visite, ripianificazione sulle assunzioni osservate e
recupero urgente. Casualità disattivata. Solo 770; 662 sospesa.
Apertura assistita D1–D11 identica, chiusura D26–D30 ereditata da V18.
NESSUNA PROMOZIONE, nessun upload: V18 resta riferimento sperimentale.

30 partite (5 versioni x 3 semi 180903001–003 x entrambe posizioni), più un
replay diagnostico esatto V22. Tutte 719 chiamate, zero errori core e missioni
residue; questi controlli NON escludono omissioni di servizi biologici.
26 test mirati passati; report DOM: 22 grafici, 30 giorni, legenda e selezione
verificati. Hash manifest/fonti/output verificati. Nessuna QA visiva browser.

Cassa media / avversario / perdite colture totali sui sei casi:
V18 90613,17 / 88667 / 0
V20 70422,83 / 77474,83 / 42
V21 85672,33 / 88918 / 78
V22 91268,33 / 87293,67 / 6
V23 88320,33 / 87323,67 / 12
V24 75027,67 / 76223 / 12
Zero fughe e inventario raccolto disperso per tutti.
V22: coltivate D13=61, D15=61, D20=55, D25=54 (mediane).
D16–D24 MOVE 118,11 vs V18 160,56, ma PASS 57,33 vs32,07;
CARE12,22 vsTop14, FEED13,44 vsTop14, WATER35,33 vsTop46.
Infestanti D30 media28,33 vsV18 20,17. Non cherry-pick cassa/superficie.

Codice immutabile hashato: docs/model_specs/codex/e19/tools/
daily_routes_770_v20.py ... v24.py, daily_route_scheduler_770_v*.py,
run_daily_routes_770_v*.py. Non modificare policy già misurate.
Risultati: artifacts/derived/portfolio_succession_20260907/daily_routes_v*.
Report completo principale:
docs/model_specs/codex/e19/reports/daily_routes_770_20260907/daily_routes_v22_TOP770_D01_D30_COMPLETE_KPI.html
Generatore: tools/build_daily_routes_770_report.py (sei report incl. V18).

Diagnosi precisa V22: tutti i sei casi perdono fragola (9,4) per acqua a D22.
Replay completo caso180903001/seat0 in artifacts/derived/daily_routes_v22_audit_20260907/replay.json;
sides identici al caso originario. d22_execution_audit.json contiene copia
profonda delle missioni e code orarie, azioni verificate fino al passo528.
Non è semina tardiva: fragola piantata giorno interno6, asciutta D21 e D22,
WEED a D23. WATER in coda worker7 a H3, worker12 a H7, non assegnato a H13;
mai avviata missione (9,4). A H19 unici liberi worker2/10, distanze10/8,
sei tick residui: soccorso tardivo impossibile da loro.
Il ricalcolo perde garanzia di completamento dell'impegno urgente.
Prossimo passo: prenotazione persistente di tempo per scadenze biologiche,
trasferimento solo con fattibilità verificata, gestione osservata di attese
input/ritorni deposito. Non altra modifica cieca alle priorità né jitter.
V23 allinea conto percorso ai ritorni effettivi al deposito; V24 anticipa
soccorso a metà giornata includendo target attivi, ma entrambe peggiorano
le perdite. Nessuna modifica ulteriore implementata dopo questo audit.

---

# Esperimento impegni/spareggio casuale 770 — 2026-09-07

Richiesta «Procedi» dopo proposta: prima correggere impegni/rinnovi/aging,
poi confronto stessa policy senza/con spareggio casuale. Completato esperimento
V19 in due bracci, NON promosso. Solo770, D1–D11 invariato e chiusuraD26 invariata.

Codice tools/commitments_770_v19.py e commitment_scheduler_770_v19.py;
runner run_commitments_770_v19.py. Rango rinnovo sopraHARVEST semplice, rango
riempimento pascolo sopra servizio ordinario, promozione limitata delle nuove
missioni in attesa. Jitter SHA256(seed,giorno,worker,target,kind,commands), sotto
rango/rinnovo/costo/valore/attesa; soloequivalenze, stabile nelgiorno, missioni
attive non rimescolate. Seedspareggio=seedpartita, un campione per ciascun seme.

12runV19 (3semi180903001–003 entrambe posizioni per braccio),8test mirati passati.
Tutte719chiamate/caso,0errori core/missioni residue/perdite biologiche/fughe/
prodotti raccolti dispersi. Casuale max1,858s, overage0,858s entro budget60.
File risultati artifacts/derived/portfolio_succession_20260907/
commitment_v19_fixed_* e commitment_v19_random_*. Moduli hashati immutabili.

Cassa media V18 90.613,17 / fissa68.149,17 / casuale73.293,50.
Avversario V18 88.667 / fissa75.321,17 / casuale88.620,67.
Scarto relativo V18+2,1949%, fissa−9,5219%, casuale−17,2953%.
Casuale aumenta cassa in4/6casi controfissa, ma peggiora confronto relativo;
non adottare casualità né promuovere entrambe rispettoV18.

Entrambe riempiono i2pascoli entroD13 tutti6casi. GranoD22 V18=1tutti,
fissa7–12, casuale6–12: NON garantisce continuitàTop23.
D16–D24 CARE V18 11,15→7,8entrambe; MOVE160,56→183,43fissa/183,22casuale;
FEED12→12,19/12,35 su14animali anziché12. PASS32,07→19,31/20,59.
InfestantiD30 20,17→13,5/16,67. Riempire mandria/rinnovare senza organizzare
intero lavoro sottrae servizi produttivi: non concludere che14animali siano
intrinsecamente troppi o che basti aumentare il jitter.

Report22KPI e diagnosi: reports/commitments_random_770_20260907/
commitment_v19_random_TOP770_D01_D30_COMPLETE_KPI.html; anche bracciofixed eV18.
Generatore build_commitments_random_report.py, filtro usaV18 come controllo
(non la vecchia base65k). Manifest74fonti/7output verificato; DOM22pannelli,
tabella/legenda/tastiera validati. Nessuna QA visiva browser, upload o modifica
bundle. Next: vero piano giornaliero dei percorsi/servizi e capacità dei rinnovi,
non altra variazione dei ranghi. 662 sospesa.

---

# Audit V18 2026-09-07 — difetti del piano confermati

Utente segnala2pascoli vuoti, quasi azzeramento grano, WATER bassi. Riprodotto
180903001 seat0 con parità esatta sides. Audit e replay in E19/artifacts/derived/
biological_v18_gap_audit_20260907, spiegazione DIAGNOSI_IT.md. NEW_ANIMAL viene
proposto con cassa/valore positivi e percorsi individualmente preparabili ma
non raggiunge mai il certificato: rango0 sotto SERVICE. Nessun animale comprato
né posto dopoD11. D15rotazioni proposte271volte ma non certificate: HARVEST
SERVICE priority4 ha rango3 vs NEW_ROTATION priority4 rango2. Rinnovo non atomico;
nuova semina dopo raccolta ricade a rango0. D22grano1casella in tutti6casi,
non zero letterale. Nel caso acqua omessa secondo needs_water dopo ultimaazione:
2annualiD16,1D20,3D21; zero morti. WATER minori dipendono anche da meno superficie
ed età/mix. FEED12/giornoD16–D24 significa12animali serviti: mancano2animali,
non necessariamente2FEED sulla mandria esistente. Nessuna nuova policy in questo
audit. Prossimo: impegni con slot riservati per pascoli/rinnovi, non altra quota.

---

# Piano biologico solo770 — checkpoint 2026-09-07

Ultime istruzioni: ridurre reattività; pianoD1–D25, chiusuraD26–D30 distinta;
662 sospesa. Con «Procedi» costruiti calendario e prototipiV17/V18. Per isolare
la modifica, entrambi mantengono il prefisso assistitoD1–D11: NON presentare
l'apertura come riscritta o l'intero piano futuro come certificato.

Codice congelato tools/biological_plan_770_v17.py / v18.py +
biological_scheduler_770_v17.py / v18.py; runner run_biological_770_v17.py/v18.py.
Intenzioni casella23W/38S finoD25 (ipotesi770 ispirata al Top già esposto),
calendario da età biologica con eventi oltreD25, aree serpentine pesate4animale
2altro aggiornate ai lavoratori osservati, preferenza territoriale morbida,
prelievi di grano per più animali dell'area. V18 sostituisce il vecchio filtro
economico nelle nuove semine/rinnovi pianificati, dà priorità giornalieraFEED,
limita preferenza territoriale a2azioni equivalenti. DaD26 chiusuraV16.
Calendario NON equivale a packing futuro di tutti i percorsi: certificato
nuove missioni resta FEED/WATER osservati del giorno. Questa lacuna è dichiarata.

Dodici run completi (6V17+6V18): semi180903001–003 entrambe posizioni, V4D.
V17 respinta: cassa75.275 ma avversario103.369, servizi peggiori.
V18: sei vittorie locali su sei; cassa90.613,17 vs avversario88.667 (+2,1949%).
V16 cassa75.354,83, scarto relativo−11,569%. V18 +20,25%cassa rispettoV16.
Zero perdite colture per acqua, fughe, prodotti raccolti dispersi, errori core,
missioni residue.719chiamate/caso, max0,376s. Superato SOLO filtro locale;
nessuna release/submission/promozione esterna, bundle congelati invariati.

D16–D24 V16→V18: MOVE184,48→160,56; FEED10,15→12; CARE9,63→11,15.
Regressioni: PASS12,04→32,07; WATER29,59→26,04; HARVEST18,48→17,74.
Coltivate medianaD15 42→47,D20 40→43, maD28 44→34,5.
Infestanti medieD25 5→5,83; D30 8,83→20,17. Non dichiarare risolti
manodopera/servizi/superficie; chiusura peggiora e deve ricevere portafoglio
compatibile. Prossimo lavoro necessario: packing reale dei picchi del ciclo,
servizi residui e continuità del piano fino alla liquidazione.

Report22KPI: reports/biological_plan_770_20260907/portfolio_v18_TOP770_D01_D30_COMPLETE_KPI.html.
Piano leggibile: stessa cartella/PIANO_BIOLOGICO_770_D1_D25_IT.md;
CALENDARIO_RIFERIMENTO_770_D1_D25.json è storicoTop, non azioni eseguibili.
Report distingueD12–D25/D26–D30, tutte5colture, V16/V17/V18/Top.
Generatore tools/build_biological_770_report.py. Manifest75fonti/9output verificato;
6test dei calendari/aree,12simulazioni, runtimeDOM22pannelli/tabella/legenda/
tastiera verificato. Nessuna QA visiva browser. Non modificare adapter già
hashati nei risultati; nuova versione se si continua.

---

# Correzioni manodopera 2026-09-07 — V16 supera filtro locale

Richiesta «Procediamo con le correzioni»: implementate V15 e V16, sei casi ciascuna
(semi180903001–003 entrambe posizioni, V4D avversario). D1–D11 identico, nessun
bundle di submission modificato, nessun upload o trasferimento alla662.

Adapter: tools/portfolio_workforce_v15.py e v16.py (ack prima della validazione;
annulla raccolti impossibili, preserva reimpianto successivo a raccolta riuscita;
valore CARE anche dopo FEED). Scheduler_v15.py ripristina priorità raccolte e
fallback produttivo locale. V15 fallisce: quattro perdite colture, cassa66.664,
scarto relativo -26,43%. V16 certifica nuovi impianti/rotazioni ma assegna servizi
esistenti direttamente; urgenze biologiche prima di raccolte scadenti e rinnovi;
CARE in moneta totale anziché diviso per attesa, come gli altri servizi.

V16 cassa75.354,83 vs V14 66.131,67 (+13,95%); scarto relativo -11,569% vs -25,005%.
Avversario85.213,17 vs88.181,33. Supera filtro locale anche rispetto alla base
65.065/-19,504%, ma non è una release esterna. Zero crop starvation, fughe,
prodotti raccolti dispersi, errori core e missioni residue. Tutte719chiamate/caso,
max0,522s; zeroHARVEST falliti D12–D30 vs622V14. Nei sei casi V16 non è servita
l'invalidazione correttiva, poiché i raccolti impossibili non sono stati richiesti.

Medie giornaliere D16–D24 V14→V16: CARE2,11→9,63; HARVEST11,81→18,48;
FERTILIZE0,56→4,41; PASS37,74→12,04; MOVE163,85→184,48 (REGRESSIONE).
Infestanti medieD30 19,33→8,83. Superficie medianaD13 58→47,D15 59→42,D20 50→40.
Cassa seme002 peggiora rispettoV14: non attribuire successo uniforme al campione.
Restano percorsi, capacità produttiva, fragole/grano e conversione carote.

Runner run_portfolio_v15.py / v16.py; risultati nella directory
artifacts/derived/portfolio_succession_20260907. Moduli congelati con hash:
NON editarli, creare versione successiva. Report completo22KPI:
reports/workforce_revision_20260907/portfolio_v16_TOP770_D01_D30_COMPLETE_KPI.html.
Generatore build_workforce_revision_report.py; manifest73fonti/7output verificato.
22test mirati passati (workforceV15/V16 +V14), dodici simulazioni complete,
DOM22pannelli/tabella/legenda/tastiera verificato; nessuna QA visiva browser.

---

# Audit manodopera 2026-09-07 — nuove cause verificate V14

Utente segnala CARE/PASS/infestanti/irrigazione e insufficiente visione complessiva.
Riprodotto caso180903001 seat0 con parità esatta sides originale. D16–D30:
601PASS tutti senza missione, 62 con budget ricerca esaurito; 78PASS D16–D27
su animale non curato. 140HARVEST falliti su WEED: manca invalidazione HARVEST
quando il raccolto scompare. 28infestazioni da decadimento (13W6S9C), zero acqua.
Diagnosi completa: reports/portfolio_revision_20260907/ANALISI_MANODOPERA_V14_IT.md.
Dati e replay: artifacts/derived/portfolio_v14_operations_audit_20260907.
Nessuna modifica alla policy in questo audit. Prossimo: invalidazione missioni,
valore CARE isolato, scadenze di raccolta, fallback produttivo e pianificazione
completa del lavoro. Non attribuire tutti i PASS al budget né tutte le WEED all'acqua.

---

# Checkpoint 2026-09-07 — portafoglio V14 testato, non promosso

Completata la campagna locale V1–V14 richiesta con «procedi». Congelato D1–D11
(prefisso di 264 azioni identico); invariati i bundle di submission. Ogni variante
ha sei casi, semi 180903001–003 nelle due posizioni, contro V4D: nessun nuovo
replay esterno, nessun upload. Il corpus storico Top001 resta descrittivo.

Report completo 22 KPI e analisi di tutte le colture / tre fasi:
`docs/model_specs/codex/e19/reports/portfolio_revision_20260907/portfolio_v14_TOP770_D01_D30_COMPLETE_KPI.html`.
La cartella contiene confronti V1–V14, summary.json e manifest con hash verificati.
Generatore: tools/build_portfolio_revision_report.py nella directory E19.

V14: cassa media 66.131,67 vs base 65.065 (+1,64%); avversario 88.181,33 vs
80.830; scarto relativo peggiora da -19,5039% a -25,0049%. Due colture perse
per acqua sui sei casi, zero fughe, zero prodotti raccolti dispersi nel deposito.
Superficie mediana D13=58, D15=59, D20=50, D28=47. A D20 mediane W12/S38;
a D28 carote mediana zero. Fragole D16–D24: 34,41 caselle medie vs base23,89,
ma raccolte105 unità vs130,33. Questo impedisce di considerare risolto il problema:
isolare adesso produzioni mancate, acqua/fertilizzante/raccolta, rinnovi grano e
conversioni terminali; non confondere superficie e rendimento.

V14 completa tutte719 chiamate/caso, massimo0,922s, nessun errore core o missione
residua. V12 espande ma smette di agire: non promossa, runtime non registrato;
V13 introduce budget deterministico e audit runtime. V11 aveva cassa69.118,5
ma scarto relativo peggiore della base; non scegliere per sola cassa assoluta.

Ultimo runner: tools/run_portfolio_v14.py; installatore portfolio_terminal_v14.py
con catena *_v14.py. Dati: artifacts/derived/portfolio_succession_20260907.
Non modificare moduli congelati dopo il run: gli hash sono parte della verifica.
V14 mantiene cicli completi; rispetta trasferimento automatico inventari a fine
giornata, ma consegna finale esplicita (nessun ultimo refresh); conserva WATER
annuale che aumenta il raccolto finale e toglie servizi senza beneficio finale.
I nuovi impianti partono consecutive_unwatered=1: MAI rinviare la prima acqua.

Validazione: 18 test mirati (test_portfolio_v14.py + test_portfolio_logistics.py),
sei simulazioni complete, riconciliazione inventari, hash fonti/output e runtime
DOM del report. Nessuna verifica visiva browser: file:// era bloccato dalla policy.
Nessuna promozione a riferimento e nessun trasferimento della variante alla662.

---

# In corso 2026-09-07 — revisione del portafoglio dopo D11

Richiesta attiva del proprietario: «procedi» alla revisione del piano colturale
D12–D30, mantenendo il prefisso assistito D1–D11. Implementate e testate revisioni
locali progressive portfolio_v1…v9; portfolio_v10 in simulazione al momento
di questo checkpoint. Non pubblicato né promosso alcun modello.

Codice in toolsE19: portfolio_succession*.py (DP successioni, costo lavoro,
fertilizzazione e autoconsumo; V6 corregge date dei raccolti e scorte),
portfolio_execution*.py (servizi biologici separati, rinnovi certificati),
portfolio_governed.py (scala proporzioni osservate all'apertura sulla superficie
coltivabile del profilo), portfolio_batched.py (servizi combinati con fallback
breve), portfolio_concurrent.py (urgenze reali distinte dai servizi differibili).
V10 usa copie *_v10.py e corregge le unità del punteggio: profitto totale invece
di profitto medio giornaliero confrontato erroneamente con valori totali dei
servizi. Il vecchio prototipo non è un riferimento promosso.

Runner run_portfolio*.py: 3 semi180903001–003 x entrambe posizioni controV4D,
720stati, prefisso264azioni verificato, eccezioni callback raccolte/assertite,
KPI/ledger/operational_daily/perdite/missioni finali. Dati:
artifacts/derived/portfolio_succession_20260907/portfolio_vN_seed_seat.json.
Ogni prova registra hash del codice. Non modificare gli adapter già in esecuzione
né i loro moduli dipendenti; congelati per riproducibilità.

V7 mantiene più grano, ma cassa insufficiente: medianeD15 W16/S25, D20 W17/S29;
V8 combinando CARE migliora alcuni incassi ma perde superficie agricola.
V9 distingue urgenze e non-urgenze. Nessuna delle prime9 revisioni soddisfa
insieme piano agricolo e confronto economico. Non presentare miglioramenti
isolati come successo. Dati definitivi da aggregare, non inventare numeri.

Test mirati disponibili test_portfolio_*.py: successioni, orizzonte, raccolta
anticipata visibile dopoWATER, fertilizzante, autoconsumo, niente credito per
acquisti passati, quote proporzionali, servizi combinati/fallback deduplicati.
V10:13testpassati. test_portfolio_batched.py è passato dopo integrazione del
campo final_day mancante nella fixture (nessun difetto live del controller).

Builder build_portfolio_revision_report.py attualmente include V1…V9 e deve
essere aggiornato per V10 prima dell'esecuzione finale. Crea un report22pannelli
per ciascuna variante vsTop001, tabella di tutte5colture per3fasi, economia
comparata alla base sugli stessi6casi, gate locale e manifest. Top001 già esposto,
nessun nuovo benchmark esterno. Ancora da verificare dopo il build finale.
Browserfile:// resta bloccato: non aggirare né dichiarare verifica visiva.

---

# Checkpoint 2026-09-07 — controllo integrato della gestione storica 770

Alla richiesta «Quindi adesso che si fa?» eseguito un controllo dell'intero
portafoglio: stessa candidata congelata, assisted_days=30, quindi nessun
passaggio al core D12, filtro osservato 770 per tutta la partita. Sei casi
180903001–003 entrambe le posizioni vs V4D, 720 stati; prefisso264azioni
paritario, topologia sempre entro7–7–0 e finale esattamente770, zero errori
callback e fallback del teacher. Non è una nuova versione parametrica.

Base sugli stessi6casi: cassa65.065 vs80.830, scarto-19,50%, zero crop starvation.
Controllo storico770: cassa72.328 vs85.845,33, scarto-15,746%; 132crop starvation
(22perpartita), zero fughe animali. Anche gli avversari V4D hanno132perdite;
non attribuire le perdite al filtro senza ulteriore evidenza. Nessuna promozione.
Primo caso D12:54coltivate,24grano,22fragole,8meloni; base34. L'espansione non è
impedita dalla sola topologia; differenze di selezione e percorsi del core
restano da isolare. Teacher non replica le carote finali del Top.

Script run_teacher_770_d30.py e build_teacher_770_control_report.py sotto toolsE19.
Dati artifacts/derived/teacher_770_d30_20260907/. Report completo22pannelli in
reports/teacher_770_control_20260907/CONTROLLO_V4D_770_Top770_001_D01_D30_COMPLETE_KPI.html.
summary.json include tutte5colture × fasiD12–15/D16–24/D25–29, superficie media,
semine e raccolti. Report con economia base/controllo e confronto Top001;
nessun nuovo benchmark esterno. Hash/fonti/punti30giorni e runtimeDOM22pannelli,
tabella,legenda,tastiera,click verificati. Nessuna verifica visiva browser.

Direzione per prossimo lavoro: pianificazione del portafoglio e successioni
complete con durata, lavoro ricorrente e raccolta/consegna; ammissione delle
missioni compatibile con servizi essenziali; diagnosi di ogni coltura in ogni
fase. Nessuna nuova ablation isolata sul grano come proxy del successo totale.
AvvioD1–D11 e submission congelate rimangono i riferimenti già validati.

---

# Checkpoint 2026-09-07 — correzione della diagnosi: portafoglio intero

Il proprietario ha segnalato che il problema è già l'espansione D12–D13,
non solo il rinnovo del grano, e riguarda anche fragole e carote. Riconosciuta
analisi iniziale troppo ristretta: leggere insieme tutti i grafici prima delle
ablation. D12–D15: base 14 casi, semine medie grano0/fragole3,71/pomodori5/meloni3;
Top001 grano31/fragole17/pomodori0/meloni0. La fase carote finale è insufficiente.
Traccia base seed180903001 seat0 paritaria: D13 H1 cassa libera17.244, offerte
su27destinazioni per tutte le colture, valori positivi ma classifica favorevole
a melone/fragola/pomodoro rispetto al grano. La selezione valuta un ciclo e
il percorso iniziale, non successioni complete. Certificato percorsi restrittivo.

Creati trace_wheat_expansion.py, wheat_reserved_continuity.py e relativo runner.
Prova certificato anche sulle missioni economiche, con alternative brevi
FEED/WATER: sei casi finiti, non promossa. Risultati e diagnosi completa in
reports/portfolio_transition_20260907/DIAGNOSI_PORTAFOGLIO_IT.md e
reserved_summary.json sotto e19. Dati corretti artifacts/derived/wheat_reserved_20260907.
Primo prototipo con indice s[5] errato INVALIDATO esplicitamente nel vecchio
productive_continuity_20260907; non usare i suoi wheat_reserved_*.json.
Runner corretto cattura e verifica anche eccezioni fuori dal contatore core.
Nessuna pubblicazione né modifica alle submission congelate.

---

# Checkpoint 2026-09-07 — continuità del grano dopo D11

Correzione del proprietario confermata: il grano spiega circa l'81% del divario
medio di terre coltivate a D15 e D20 (14 assistita V1 contro 5 Top770-001).
Il core separa raccolta annuale e nuova semina, senza continuità garantita della
rotazione; la raccolta matura non ha priorità di scadenza. Il certificato di
nuova crescita include anche servizi opzionali. Non attribuire tutto a Q2 o
alle fragole. Zero crop starvation non esclude decadimento naturale del grano.

Quattro prove locali, ciascuna 3 semi x 2 posizioni contro V4D, fino D30;
prefisso D1-D11 invariato e verificato. Nessuna versione promossa o pubblicata.
Base sui medesimi 6 casi: cassa 65.065, relativo V4D -19,50%.
- essential: certificato limitato a FEED/WATER osservati, anche non urgenti;
  cassa 69.643, relativo -28,57%, zero perdite biologiche. Più superficie,
  ma ancora zero grano a D20.
- essential_renewal: raccolta collegata a risemina; cassa 65.553, relativo
  -31,99%, zero perdite biologiche; mediana grano D15=11, D20=5.
- wheat_deadline: scadenza raccolta e acqua pre-raccolta; cassa 70.376,
  relativo -26,38%; grano D15/D20=13, ma 4 fughe animali: SCARTATA.
- wheat_safe: priorità biologica sopra quella economica; cassa 70.711,
  relativo -29,21%; 2 crop starvation e 2 fughe: SCARTATA nonostante il nome.

Diagnosi operativa: occorre coordinare raccolta-risemina e percorsi senza
ritardare alimentazione/irrigazione. Forzare priorità o allentare il solo
certificato non basta. Le prove non replicano ancora Top770 e non migliorano
il confronto economico relativo con V4D.

Script e adapter in docs/model_specs/codex/e19/tools/: productive_continuity,
wheat_continuity, wheat_safe_continuity e relativi run_*.py.
Dati in artifacts/derived/productive_continuity_20260907/ sotto e19.
Report in reports/productive_continuity_20260907/: quattro HTML COMPLETE KPI,
22 pannelli ciascuno, 30 giorni, confronto separato con Top770-001; summary.json
con risultati, manifest.json con hash fonti/output. Builder:
build_productive_continuity_report.py. Test adapter 3 passati, dati/hash e DOM
(22 pannelli, tabella, legenda, tastiera, selezione) verificati. Nessuna verifica
visiva browser; resta il blocco URL file:// già documentato.

---
# Checkpoint 2026-09-07 — formato COMPLETE KPI richiesto dal proprietario

Il proprietario intendeva un cruscotto come E18_27_TOP770_D01_D30_COMPLETE_KPI.html,
non soltanto il report narrativo della transizione. Creati due report separati
nuova770 assistita V1 vs Top770-001 e vs Top770-002, standardV4.1:22 pannelli,
mediana/min-max, tooltip e pin del giorno, legenda interattiva, tabella completa,
flussi economici e quantità per prodotto. Due agenti per report. Pannello03
include coltivate e superficie sbloccata; H24 coerente col riferimento storico.

Cartella: docs/model_specs/codex/e19/reports/assisted_770_complete_kpi_20260907/.
File: E18_770_ASSISTED_Top770-001_D01_D30_COMPLETE_KPI.html e corrispondente002.
14 run locali riprodotti senza modificare strategia, con parità completa dei
KPI/ledger/risultati precedenti; aggiunti dati operativi H24. Top001: per i KPI
operativi mancanti riusati gli aggregati congelati E18_28_C_TOP770_D01_D30_KPI_19,
stessi5episodi e parità di tutte le serie comuni verificata. Top002:4profili
precedentemente selezionati, operational_daily già disponibili. Nessun nuovo
benchmarkesterno o upload. Registrato riuso delle fonti.

Script build_assisted_complete_kpi.py, run_assisted_770_complete.py,
complete_kpi_template.html in toolsE19. Dati30giorni×23chiavi×2agenti verificati;
test DOM locale:22pannelli,31righetabella,legenda,tastiera,selezionegiorno superati.
Browser Use ha bloccato l'apertura file:// per URL policy; non aggirare con altri
strumenti. Consegnati link perché l'utente possa aprirli. Nessuna verifica visiva
nel browser dichiarata. I precedenti report narrativi restano approfondimenti.

---

# Checkpoint 2026-09-07 — studio transizione D11–D15

Richiesta: studiare la transizione, senza nuova pubblicazione. Diagnosi su
770 assistita V1 congelata: D12 inizia con 25 irrigazioni urgenti, cash15.420
vs maintenance floor54 nel caso seed180903001 seat0. Priorità biologica
assoluta del core dirige i primi lavoratori verso WATER; 192 MOVE (su289
comandi), 25 WATER, 6 CARE e zero nuove piantagioni. La V4D nello stesso caso
esegue 130 MOVE,46 WATER,19 CARE,21 piantagioni, ma espande anche il bestiame
oltre770. Evidenza di potenziale problema di coordinamento percorsi, non prova
che tutti i vincoli possano essere allentati. Assunzioni osservate D12 H1=0,
H2=6,H3=7,H4=12 manovali; terreno acquistato H2 senza semine nello stesso giorno.

Due ablation, tre semi180903001–003 entrambe le posizioni, finoD30:
- CARE value: prezzo spot marginale prodotto/ritardo alla prossima produzione,
proxy conservativa del bonus futuro mancante da _services. Non cambia D12:
CARE6,PLANT0. Cassa media64.626,5 vs base65.065; relativoV4D -22,11% vs -19,50%.
Non promossa. Non è una dimostrazione contro ogni possibile modello del CARE.
- PASS-to-WATER D11: nessun PASS utilizzabile sulla coltura non irrigata,
zero sostituzioni e risultati identici alla base in6/6. È controllo nullo.
Base strumentata riprodotta integralmente con parità dei dati di entrambi i lati.
Nessuna perdita biologica, errore o missione residua nelle prove.

Report `docs/model_specs/codex/e19/reports/transition_study_20260907/REPORT_TRANSIZIONE_D11_D15_IT.html`.
Script `study_transition.py`, `study_transition_water.py` e
`build_transition_study_report.py` nella cartella tools E19. Tracce orarie D12–D15
in artifacts/derived/transition_study_20260907, con posizioni/inventari/missioni,
valori e riserve. Nessuna strategia congelata modificata o pubblicata.
Prossimo intervento proposto: organizzare visite vicine e preparare il passaggio
in funzione degli obblighi eseguibili, conservando la sicurezza e il risultato
D11; verificare crescita D12–D15 e rendimento relativo finoD30.

I checkpoint seguenti sono cronologia precedente.

---

# Checkpoint 2026-09-07 — nuova 770 assistita, report Top770 D1–D30

Estesa la candidata 770 assistita V1 invariata fino a D30: 14 partite locali
contro V4D, 7 semi di sviluppo, entrambe le posizioni. Tutti i prefissi D1–D11
coincidono con quelli già verificati. Contabilità riconciliata per entrambi i
lati; nessun errore del core, morte di coltura, fuga animale o missione terminale
residua. Topologia finale 770 in tutti i casi. Cassa media candidata 58.157,79
vs V4D 74.445,43: -21,88%, 0/14 vittorie. Il buon avvio non basta alla chiusura.

Report richiesto rispetto agli stessi Top770-001 (5) e Top770-002 (4), senza
nuovi replay esterni: confronto storico descrittivo, separato dal diretto locale.
D12 fragole candidata21 vs Top38/32,5; CARE candidata da12 D11 a6 D12.
D20 fragole24,71 vs38/32,5; nuova770 grano0 e meloni3. Il punto da studiare
ora è il passaggio al core D12–D15, servizi, ammissione crescita e mix colture.
Non modificata o pubblicata alcuna strategia durante il report.

Report: `docs/model_specs/codex/e19/reports/assisted_770_top770_d30_20260907/REPORT_NUOVA_770_VS_TOP770_D1_D30_IT.html`.
Runner/generatore: `docs/model_specs/codex/e19/tools/run_assisted_770_d30.py`
e `build_assisted_770_top_report.py`. Quattro grafici incorporati, cinque tabelle,
aggregati e manifest delle fonti e degli output. Registro di riuso Top aggiornato.

I checkpoint seguenti sono cronologia precedente; la limitazione a D11 della
770 è superata da questa verifica D30, quella della 662 resta invariata.

---

# Checkpoint 2026-09-07 — avvio assistito D11 comune 770/662

Il proprietario ha limitato l'obiettivo all'avvio Q0 e al salto di cassa D11;
la prosecuzione nelle topologie target è rinviata. Create due candidate locali
`submission_codex_e18_770_assisted_start_v1_candidate.py` e
`submission_codex_e19_662_assisted_start_v1_candidate.py`, non pubblicate.
Governatore ibrido esplicito: V4D guida le azioni fino a fine D11, filtrando
pascoli oltre il budget parametrico e pollai; da D12 subentra il core comune
V2 congelato, con vecchio bootstrap disattivato. Non presentare questo come
apprendimento autonomo del portafoglio da parte del core.

28 prefissi real-engine (7 semi di sviluppo, entrambe le posizioni e target),
720 step di orizzonte preservati, 264 batch eseguiti. In tutti: 12 meloni D1,
72 unità raccolte D11, 54 vendute D11, 20 fragole D10. Delta cassa medio D11
770 +13.026; 662 +12.766,57: uguale alla V4D nella stessa partita, 28/28.
Topologie D11 7-7-0 e 6-6-0, nessuna violazione di capacità o fuga di animali.
I ricavi sono diversi dai precedenti +16k perché l'altra fattoria ora ha
anch'essa un'apertura produttiva: confrontare sempre il mercato della partita.

Verifica harness: 4 casi di parità dei KPI/flussi contro i replay V2 consolidati.
Parità sorgente/bundle 265 azioni per caso (264 + prima chiamata D12), tre
unit test passati. D12 testata solo interfaccia; rendimento successivo,
completamento 662 e robustezza fuori campione non verificati.
Report: `docs/model_specs/codex/e19/reports/assisted_start_20260907/REPORT_AVVIO_ASSISTITO_D11_IT.html`.
Strumenti in `docs/model_specs/codex/e19/tools/assisted_start.py`,
`run_assisted_start.py`, `build_assisted_start.py`, `build_assisted_start_report.py`.
La V4D competitiva rimane byte-identica. Nessuna nuova submission o benchmark esterno.

I checkpoint seguenti sono cronologia precedente.

---

# Checkpoint 2026-09-07 — report KPI 770 e 662 contro V4D

Completati due report locali su Q0 e trend D1–D30, 14 partite dirette per
modello contro il bundle campione E18.2 V4D. Sono la 770 controllo V2 e la
662 E19 V2, stesso core; nessuna strategia modificata o pubblicata qui.
Azioni e ricavi riprodotti esattamente dai gate congelati; contabilità di
entrambi i lati riconciliata. Nessun nuovo campione esterno consumato.

Report HTML autosufficienti e Markdown in
`docs/model_specs/codex/e19/reports/kpi_v4d_20260907/`:
`REPORT_770_VS_V4D_IT.html` e `REPORT_662_VS_V4D_IT.html`.
Cassa diretta: 770 59.612 vs V4D 109.677 (−45,65%); 662 63.487 vs V4D
117.808 (−46,11%). Le due V4D sono avversari effettivi delle rispettive
partite; non mescolare i loro mercati come identici.

Q0 iniziale: parametrici 18 WHEAT + 3 CARROT vs V4D 7 WHEAT + 12 MELON,
stessi 2 COW/2 SHEEP. Primo raccolto meloni D16 vs D11 in tutti i casi.
Fragole D10: 770 0,29; 662 1; V4D circa 20. La guida attuale esclude
MELON dal bootstrap e blocca il bestiame fino al primo raccolto.
Ipotesi Q0 supportata, non causa unica dimostrata: studiare anche transizione
verso fragole, crescita bestiame e capacità di lavoro. La vecchia variante
V19 a pesi WHEAT:MELON 1:2 era già fallita: non ripeterla come soluzione
inedita. Scomposizione contabile, controevidenze e proposte nei report.

I checkpoint seguenti sono cronologia precedente.

---

# Checkpoint 2026-09-07 — ripristino competitivo E18.2 V4D

Il proprietario ha respinto i risultati E19 e richiesto una nuova submission
invariata di `submission/submission_codex_e18_2_capacity_governed_v4d.py`.
Invio effettuato: Kaggle Complete, score iniziale 600,0; validazione seed 0
superata, nessuna partita classificata ancora visibile. Recupero di classifica
non ancora dimostrato. Ricevuta
`docs/model_specs/codex/e19/artifacts/derived/E18_2_V4D_RESUBMISSION_20260907.json`.
E19 Complete con score 697,2, posizione osservata 4316; vecchia V4D 1162,9.
Non confondere lo score storico con quello della nuova submission.

E19 aveva già perso tutte le 28 partite locali (0/14 contro E18.16 e 0/14
contro E18.2/V4D). Il +7,76% contro una 770 parametrica debole non era un
criterio competitivo adeguato. Prima di altre release sperimentali, studiare
il divario e ripartire dalla V4D, con parametrizzazione incrementale e gate
competitivo contro il riferimento forte. Nessun nuovo tuning in questo turno.
Report: `docs/model_specs/codex/e19/reports/E19_EXTERNAL_REGRESSION_AND_V4D_ROLLBACK_20260907_IT.md`.
I checkpoint seguenti sono cronologia precedente.

---

# Checkpoint 2026-09-07 — E19.1 parametrica 662 V2 inviata

La nuova istruzione «Sviluppa la E19 allora» supera il prerequisito E18.
E19.1 V2 sviluppata e inviata a Kaggle; ricevuta attuale Pending in
`docs/model_specs/codex/e19/artifacts/derived/E19_V2_KAGGLE_PUBLICATION_20260907.json`.
Bundle `submission/submission_codex_e19_1_662_v2.py`, SHA256
`ba0a4780a0d25bc3535d842f6e40bb1ae9954e5da181b46cea28e62f0b1474bc`.

28/28 topologia 662 popolata, zero perdite biologiche/errori/missioni residue.
Cassa media 68.348,71: +7,760% vs 770 sullo stesso core corretto,
+10,994% vs vecchia E18 V24, −13,208% vs E18.31 storica.
Parità 2.876 azioni e loader Kaggle; 90 test core/E19 passati.
Fix condiviso: riserva l'intera quantità dei PICKUP pendenti, incluso surplus.
Controllo `submission_codex_e19_control_770_v2.py` congelato e testato 28 casi;
non pubblicato, non promosso a E18 finale. V1 E19 conservata, non pubblicata.

Report: `docs/model_specs/codex/e19/reports/E19_DEVELOPMENT_20260907_IT.md`.
Prossimo passo: benchmark esterni sulla E19 congelata; nessun nuovo campione
Top usato in sviluppo. Non dichiarare parità ai Top o promozione incumbent.
I checkpoint seguenti sono cronologia precedente, non lo stato corrente.

---

# PROJECT_STATE — Kaggriculture

## Checkpoint corrente — 2026-09-07, gate parametrico non superato

Richiesti finalizzazione/pubblicazione E18 770 e successiva E19 662 sullo
stesso core. **Mandato non completato: nessuna nuova pubblicazione, E19 non
avviata.** L'autorizzazione agli upload è presente; manca l'idoneità tecnica
ed economica, non una conferma del proprietario.

E18.33 V24 è una candidata locale verificata, non il riferimento finale.
Gate completo: 28/28 770 popolate, zero morti/fughe, cinque missioni terminali
incomplete; cassa media 61.579 contro E18.31 matched 78.750,29 (-21,80%).
COW D10 mediana 7 contro 9, PASS D5–D10 318,5 contro 294,93. Nessuna
equivalenza con Top770 dimostrata. V22 estesa fallisce anch'essa: -19,57%,
tre fughe, una morte crop, una missione incompleta e 24/28 770 popolate.

Correzione V24: FEED/WATER essenziali restano candidabili se cura, raccolto
o consegna rendono impossibile la visita completa. PASS totali -27,61% vs
V22, MOVE +8,02%: non è un beneficio economico. Core senza piani legacy;
avvio selezionato per le prove V2, due COW/due SHEEP e WHEAT/CARROT fino al
primo raccolto. Avvii alternativi e varianti economiche respinti e preservati.

86 test mirati passati. Bundle V24 verificato source/standalone/file-loader
su quattro casi, 2.876 batch per metodo; massimo standalone 0,8019 s, massimo
nel gate concorrente 1,6000 s. File
`submission/submission_codex_e18_33_770_v24_candidate.py`: **non caricare come
finale**. Decisione separata dal manifest congelato:
`docs/model_specs/codex/e18/artifacts/derived/E18_33_V24_RELEASE_DECISION_20260907.json`.
Report completo:
`docs/model_specs/codex/e18/reports/E18_PARAMETRIC_RELEASE_WORKLOG_20260907_IT.md`.
Ultima pubblicata resta E18.32 V9 / 56056189, controllo provvisorio legacy.
Nessun nuovo Top consumato, nessun commit/push. Quanto segue è cronologia.

## Stato operativo — 2026-09-06, integrazione anti-PASS

### Checkpoint più recente — avvio esteso e pubblicazione provvisoria

**E18.32 V9 pubblicata: 56056189, Complete**, upload 13:27:24 UTC. È il
controllo provvisorio esplicitamente autorizzato, NON il benchmark E19;
calendario legacy ancora presente. Receipt separato dal manifest congelato:
`docs/model_specs/codex/e18/artifacts/derived/E18_32_KAGGLE_UPLOAD_RECEIPT_V9_20260906.json`.
La policy comune E18.33 rimane non eleggibile. Bootstrap minimo V7: uscita
D4 H9, un solo smoke economico positivo; estensione V9 al rinnovo del primo
ciclo: uscita D16–D17, quattro casi, cassa media 40.227,25, nessuna 770.
97 test mirati passati, ma gate simulato fallito: test unitari non equivalgono
a qualità della traiettoria. Sono aperti capacità futura e budget computazionale.
Q0 del controllo V9: dodici tile libere D11–D13, settimo pascolo in D14.
Report corrente: `docs/model_specs/codex/e18/reports/E18_CLOSEOUT_AND_BOOTSTRAP_20260906_IT.md`.
E19 non avviata. Stato/sorgenti/prove da conservare integralmente; nessun nuovo
Top consumato. Le sezioni successive sono cronologia, non stato di upload corrente.

### Checkpoint precedente — prototipo V5

Mandato corrente: **E18.33 — policy comune pascoli/colture per tutti i quadranti**.
Audit e specifica definiti, profilo pulito, kernel e adattatore nativo realizzati;
**prototipo diagnostico non eleggibile**, certificato economico/capacità incompleto.
Q0 prima verifica, Q1 controllo di trasferimento: niente programmi diversi.
Target corrente 14, capacità uniforme 7 per quadrante, massimo 12 manovali;
Q2 riceverà un pascolo se il target aumenta e l'investimento è fattibile,
senza nuova data/coordinata. Variazione a 15 solo test di contratto, non live.
Specifiche e audit:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.md`,
`docs/model_specs/codex/e18/reports/E18_33_LEGACY_POLICY_AUDIT_20260906_IT.md`.
67 test passati e undici partite diagnostiche. V5, quattro casi: cassa media
71.869,25 contro E18.31 matched 82.560 (-12,95%), zero morti/fughe, ma topologia
6-5-0 invece di 770 e due missioni terminali incomplete. Nessun gate superato.
Il prototipo non importa i controller/piani legacy; manca la valutazione
congiunta del portafoglio, della capacità e della crescita. Config e baseline
storiche preservate. Nessun nuovo upload/commit/push o benchmark consumato.
Checkpoint: `docs/model_specs/codex/e18/reports/E18_33_NATIVE_POLICY_CHECKPOINT_20260906_IT.md`.
E19 è roadmap subordinata al consolidamento E18: confronto 770/772/662 con
le stesse policy e soli parametri diversi, non esperimenti già avviati.

Ciclo precedente alla pubblicazione: **E18.32 DEMAND RELEASE V9**, ottimizzazione
interna dei PASS. Diagnosi riproducibile su sei replay E18.31: 4.314 batch
identici. Confermati calendario e roster storici attivi, non i vecchi override
di mercato. V7 migliora i PASS ma perde un FEED/lana; V9 protegge il ciclo
fertilizzante → incasso → grano prima di ammettere percorsi compattati.
V9: 28/28 safety, PASS D1–D10 -24,91%, D5–D10 -21,99%, cassa +0,230%; tutte
le 28 coppie positive, stessa crescita delle mucche e raccolti crop/lana.
71 test mirati pass; D7/D9 restano aperti, nessuna dichiarazione di soluzione
completa. File corrente `submission/submission_codex_e18_32_770_v9.py`;
non considerare V7 il candidato finale. Parità V9 completata su quattro casi,
2.876 batch per metodo source/standalone e file-loader. Conservata come
controllo: calendario legacy ancora presente, non conforme al nuovo mandato.
Specifica: `docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_32_770_READY_WORK_V1.md`.
Diagnosi: `docs/model_specs/codex/e18/reports/E18_32_PASS_ROOTS_AND_VERIFICATION_20260906_IT.md`.
Il blocco seguente conserva il quadro storico della pubblicazione E18.31,
precedente a E18.32 V9, e il controllo del nuovo sviluppo.

Aggiornamento più recente: E18.31 UNIFIED V11 inviata su richiesta del
proprietario per verifica esterna; Kaggle **Complete**, submission **56050866**,
upload 2026-09-06 08:35:23 UTC. Non duplicare l'upload. Standalone
verificato su quattro casi / 2.876 batch per metodo, SHA-256
`59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63`.
Resta non promossa. Reporting V4 a 22 pannelli con CARE separato da FEED.
Registro anti-riutilizzo aggiornato: Top770-001 e Top770-002 consumati dopo
il loro ciclo. Nuovo riferimento 56044235: quattro exact770 su cinque;
grafici pubblici E18.31 n6 contro Top770-002 n4, senza modifiche alla release.
Corpus E18.31: 5 WIN / 1 LOSS, zero perdite biologiche, sei ledger riconciliati;
PASS D5–D10 294,17, mucche D8 7–8 e D9 8–9. Campione iniziale, non promozione.
Diagnosi: `docs/model_specs/codex/e18/reports/E18_31_PUBLIC_TOP002_DIAGNOSTIC_20260906_IT.md`.
CARE intermittente D19–D25, scorta grano e capacità produttiva D5–D10 sono
ipotesi da validare internamente, senza tuning sul nuovo Top né cambio di mix.
Pulizia: 38 raw di screening rimossi con catalogo URL/hash; 11 raw conservati
per lo studio corrente. 55 test mirati e QA V4 a tre larghezze/light-dark pass.

**Linea attiva Codex, target 770, cap 14 animali / massimo 12 manovali.**
Antigravity, Claude e Copilot congelati. Priorità autorizzata: riprogettare
assegnazione e ciclo di vita delle missioni, non cambiare topologia.
Principio conservato da E18.32: **PASS ed espansione mucche come decisione integrata**;
non aspettare una soluzione autonoma dei PASS prima di creare lavoro produttivo.

| Ruolo | Versione | Stato |
|---|---|---|
| Ultima pubblicata | E18.31 UNIFIED V11 / 56050866 | Complete, verifica esterna; non promossa |
| Parent pubblico | E18.28 C / 56036993 | immutabile, controllo storico; non promossa |
| Controllo development | E18.29 B3 | +7,68% matched locale, mortalità residua; non pubblicata |
| Baseline sviluppo verificata | E18.30 CROP_POOL V2 | runtime integrato, 44 test dedicati / 371 suite; gate 14/14 economico e safety pass, standalone verificato; NON pubblicata |
| Controllo E18.32 | E18.31 UNIFIED V11 | 28 casi congelati, ultima pubblicata 56050866; non promossa |
| Controllo interno | E18.32 DEMAND RELEASE V9 | Verificata e non pubblicata; conserva il programma legacy, non conforme al nuovo mandato |
| Sviluppo corrente — gate fallito | E18.33 COMMON RESOURCE POLICY V1 / prototipo nativo V5 | Kernel e adattatore senza piani storici, 67 test; economia, exact770 e missioni terminali non superati |
| Roadmap subordinata | E19 PARAMETRIC VALIDATION | Stesso codice su 770/772/662 solo dopo E18 consolidata; nessun esperimento avviato |
| Controlli | E18.16, E18.2 | benchmark interni e riferimento esterno storico |

Corpus E18.28 congelato: 30 replay (17 LOSS, 13 WIN), 21.570 batch shadow
identici al pubblicato, ledger 29/30 verificati inclusi tutti i LOSS. Nelle
sconfitte, D15-D30 746,3 PASS medi: 83,5% code esaurite, 16,5% attese.
Due fallimenti payroll/HIRE D11 lasciano WATER/HARVEST a manovali assenti.
Analisi completa, limiti e prossime azioni:
`docs/model_specs/codex/e18/reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md`.

Non estrapolare score correnti dai report storici e non presentare la riduzione
dei PASS come guadagno economico acquisito. E18.29 non risolve il difetto
strutturale. E18.30 V2: 81.976 contro parent 74.491,57 (+10,05%), PASS -30,47%,
PASS D15–D30 -58,68%, MOVE +7,83%; zero perdite su 14 casi E18.16 e due E18.2.
Vittorie E18.16 5/14 (parent 1/14), E18.2 0/2: non incumbent promosso.
V1 resta conservata come safety fail; V2 risolve la morte crop con PLANT→WATER
completo, non con eccezioni per seed. Nessuna modifica a HIRE o crescita mucche.
E18.31 supera il congelamento iniziale delle mucche: verificare insieme capacità
libera, investimento, alimentazione, organico e ricavi. Nessun tuning su Top770.
V11: 14 confronti E18.16 appaiati (sette seed, due seat), cassa media 81.965,64
contro 81.976; 7/14 delta positivi. Controllo E18.2 matched disponibile solo su
un seed/due seat: +14,73%, non estendere agli altri dodici casi candidati.
Diagnostica supplementare con negozi allineati: +811,57 medi, 5/7 seed positivi;
non sostituisce il simulatore originale o la verifica esterna. PASS residui e
vantaggio economico non robusto: rimanere sullo stesso problema, non promuovere.
Checkpoint corrente:
`docs/model_specs/codex/e18/reports/E18_31_UNIFIED_V11_CHECKPOINT_20260906_IT.md`.
Report: `docs/model_specs/codex/e18/reports/E18_30_RUNTIME_V2_CONSOLIDATED_20260906_IT.md`.

Handoff autorevole: `docs/NEW_SESSION.md`. Specifica di sviluppo corrente:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_32_770_READY_WORK_V1.md`.
Reporting comune V4: due curve, Top770 vs candidata, 22 pannelli e KPI operativi;
WATER, FEED e CARE riusciti distinti.
Processo: confronto interno, migliore candidata eleggibile pubblicata ogni giorno
e analisi strategica quotidiana dei top; upload E18.31 autorizzato ed eseguito.

La cronologia precedente e i vecchi stati CURRENT sono archiviati in
`docs/history/PROJECT_STATE_PRE_ANTI_PASS_20260905.md`; non sono priorità attive.
La Foundation non viene alterata per mascherare difetti di implementazione:
restano separati capacità strutturale/servibile, scorte, cassa e deadline.
Closeout e verifiche: `docs/model_specs/codex/e18/reports/E18_ANTI_PASS_CHECKPOINT_20260905_IT.md`.
Checkpoint `4a3b7fd`, freeze byte-identici `f036cd6` e nucleo `b8aaf70` pubblicati
su origin/main. Integrazione V2 nel working tree; nuova submission solo come file
locale verificato, nessun upload/commit/push in questa tranche.


## 2026-09-07 — confronto storico V4C richiesto dal proprietario

Creato `docs/model_specs/codex/e19/reports/v4c_top770_20260907/REPORT_V4C_VS_TOP770_IT.html`.
V4C interpretata letteralmente come E17.2 V4C, distinta da E18.2 V4D;
richiesta asincrona di disambiguazione senza risposta al completamento.
Sei casi storici INERT_PASS riprodotti con parità di azioni/ricavi; confronto
descrittivo con Top770-001 (5 replay) e Top770-002 (4 replay 770).
V4C ha topologia finale 7-7-5, 8 COW/10 SHEEP/1 GOOSE: non confrontabile
come efficienza a parità di risorse o ranking. Nessuna strategia modificata.
