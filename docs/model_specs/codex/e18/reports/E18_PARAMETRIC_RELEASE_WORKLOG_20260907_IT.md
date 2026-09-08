# Consolidamento parametrico 770 e successiva E19 662

**Esito corrente: nessuna versione finale eleggibile; nessun nuovo upload,
E19 non avviata.** Il lavoro ha prodotto una candidata V24 autosufficiente e
verificata per parità, ma non ha soddisfatto il mandato di finalizzazione.

| Gate completo, 28 casi | V22, avvio breve | V24, servizio essenziale | E18.31 controllo |
|---|---:|---:|---:|
| Cassa finale media | 63.342,54 | 61.579,00 | 78.750,29 |
| Delta cassa vs controllo | -19,57% | -21,80% | — |
| 770 popolata terminale | 24/28 | 28/28 | — |
| Perdite colturali / fughe | 1 / 3 | 0 / 0 | — |
| Missioni terminali incomplete | 1 | 5 | — |
| COW D10, mediana | 5 | 7 | 9 |
| PASS D5–D10, media | 437,36 | 318,50 | 294,93 |

V24 rispetto a V22: PASS totali medi 1.015 contro 1.402,04 (-27,61%),
MOVE 4.094,61 contro 3.790,61 (+8,02%). I benefici di sicurezza e assegnazione
sono reali nelle prove, ma non costituiscono un beneficio economico acquisito.
Soltanto due dei sette delta medi per seed V24 sono positivi. Questi sono
confronti interni appaiati, non una misura di equivalenza con Top770.

Bundle V24: `submission/submission_codex_e18_33_770_v24_candidate.py`.
Parità su due seed/due seat, 2.876 azioni per metodo, file-loader incluso;
massimo standalone 0,8019 s. Nel gate concorrente il massimo osservato è
1,6000 s: le condizioni di carico vanno distinte, nessuna garanzia universale.
86 test mirati superati. Decisione di non rilascio separata dai manifest
immutabili: `artifacts/derived/E18_33_V24_RELEASE_DECISION_20260907.json`.

Mandato del 2026-09-07: finalizzare la E18 parametrica con governance iniziale,
pubblicare il riferimento 770 e quindi avviare e pubblicare la prima E19 662
con lo stesso core. Questa richiesta autorizza entrambe le pubblicazioni;
i vecchi divieti di upload nei checkpoint non sono una richiesta di conferma.
La qualità richiesta resta da dimostrare: nessuna rinomina della E18.32 legacy.

## Protocollo di sviluppo

Primo screening: seed development 180903001, entrambi i seat, E18.16 e
E18.2/V4D. Tutti i casi e i fallimenti conservati. Selezione successiva solo
dopo estensione ai sette seed development, parità standalone e controllo del
tempo per chiamata. Nessun nuovo Top consumato durante il tuning interno.
E19 parte dopo il consolidamento e la pubblicazione della 770, cambiando K
da 7 a 6 a target 14, con codice identico. Il mandato corrente richiede
pubblicazione prima dei futuri benchmark esterni, superando la sequenza della
vecchia roadmap che richiedeva già conferma esterna prima dell'avvio E19.

Per il rilascio verificare: 770 effettiva con animali vivi, zero perdite
biologiche, contabilità riconciliata, nessun errore o missione terminale
incompleta, cap 14 e 12 manovali, runtime sotto il budget del motore,
confronto economico appaiato con E18.31/E18.32 e traiettorie quotidiane.
Un solo smoke positivo o una topologia terminale corretta non dimostrano
comparabilità dei KPI con Top770.

## Varianti e risultati iniziali

- V10: avvio breve V2 2 COW/2 SHEEP, WHEAT/CARROT fino al primo raccolto.
  Cache delle quotazioni per osservazione. Quattro casi completati, 770 e zero
  perdite in tutti; cassa 87.160 / 85.118 / 84.581 / 81.224. Quattro COW a D10:
  non è ancora risolto il ritardo di crescita.
- V11: cache dei valori colturali e calcolo unico delle riserve incrementali.
  Decisioni e cassa identiche al controllo, un caso; massimo 2,363 s.
- V13: riuso dei requisiti e certificati di rotta equivalenti per colture.
  Un caso identico anche nell'hash delle azioni; massimo 0,460 s, media 0,0305 s.
- V12: sola governance iniziale 3 COW/1 SHEEP sul core V11. Quattro casi,
  cassa 75.092 / 68.818 / 62.341 / 67.428. Respinta, non miglioramento.
- V14: portafoglio colturale cronologico con consumi dei soli negozi osservati,
  due scenari e impatto marginale sui ricavi già impegnati. Quattro casi:
  59.028 / 59.028 / 73.822 / 73.822. Respinta; matematica verificata con test,
  ma non prova di miglioramento del controller. Modulo separato preservato.
- V15: avvio breve con sole CARROT, core V13. Quattro casi:
  56.271 / 54.267 / 41.914 / 43.436. Respinta, non selezionare il solo anticipo
  delle mucche come criterio economico.
- V16: guadagno assoluto prima del rendimento per azione, avvio V2 invariato.
  Prime due prove 70.173 / 56.619 contro E18.16, sette COW a D10 ma economia
  inferiore. Non selezionata.
- V17: HARVEST -> PLANT -> WATER annuale nella stessa visita. Respinta:
  peggioramento economico e una fuga nel primo confronto E18.16. L'omissione
  di WATER prima del raccolto è inoltre scorretta nelle finestre annuali:
  il motore incrementa la resa durante WATER, non soltanto al refresh.
- V18: approvvigionamento FEED accessibile al lavoratore. Non selezionata:
  i casi contro E18.2 restano inferiori al controllo; più PASS.
- V19: governance di dotazione iniziale con pesi WHEAT:MELON 1:2. Quantità
  derivate dall'area inizialmente disponibile, quote animali e pesi; rilascio
  a dotazione osservata, senza maturazione e senza riavvio per nuovo terreno.
  Profilo V7, schema v3; test di invarianza/validazione/rilascio passati.
  Rilascio D4 H16 sul primo caso, cassa 60.828 contro E18.16 e 57.245 contro
  E18.2, entrambi i seat. Respinta sul piano economico.
- V20: precedenza indiscriminata agli obblighi. Più FEED/CARE, ma solo 11
  animali nel primo confronto e 81.003 di cassa: crescita nuovamente bloccata.
- V21: priorità alle scadenze di resa biologica. Quattro casi, media
  57.041,25 (-30,91%), nessuna 770 finale, una missione incompleta. Respinta.
- V22: controllo breve esteso ai sette seed, core ottimizzato e supporto
  opzionale dello schema v3 inattivo nel profilo selezionato V2. **Respinto.**
  Ventotto casi: cassa 63.342,54 contro E18.31 78.750,29 (-19,57%), tre fughe,
  una perdita colturale, una missione incompleta, 24/28 topologie popolate 770.
  COW D10 mediana 5 contro 9; PASS D5-D10 437,36 contro 294,93.
  Parità su due seed/due seat: 2.876 azioni identiche source/standalone e
  file-loader, massimo standalone 0,5023 s. Parità non significa qualità.
  Durante il gate parallelo massimo osservato 1,562 s: non attestare un limite
  assoluto sotto un secondo per qualsiasi condizione di carico.
  Il salvataggio del solo flag finale ha generato OSError 22. Tutte le 28
  partite erano già presenti: originale preservato, recupero verificato in
  `E18_CLOSEOUT_GATE_V22_RECOVERED_20260907.json`, nessuna partita ripetuta.
- V23: servizio essenziale separato dalla visita opzionale quando questa non
  entra nel tempo residuo. Sul seed 180903003 contro E18.16, entrambe le fughe
  eliminate: 49.621/48.822 contro 31.399/32.034 di V22; PASS 1.085/1.103
  contro 1.402/1.416. Non è una dimostrazione di idoneità economica generale.
- V24: affinamento del servizio essenziale: nessun turno fittizio di acquisto
  quando il grano è già accessibile. Tre test mirati verificano FEED nell'ultimo
  slot, WATER senza la fertilizzazione opzionale e rifiuto di rotte impossibili.
  Gate completo 28 casi e parità su quattro casi conclusi, senza cambiare
  governance o core durante le rispettive simulazioni. Esito nella tabella
  iniziale: non eleggibile nonostante la sicurezza biologica.
- V25: sola governance 3 COW/1 SHEEP sul medesimo core V24. Quattro casi,
  69.054/69.054 contro E18.16, 46.048/46.048 contro E18.2. Respinta.
- V26: profilo 4 COW/0 SHEEP sul core V24, prima prova del profilo V5.
  Quattro casi: 56.939 in entrambi i seat contro E18.16, 47.525 in entrambi
  contro E18.2. Media 52.232 (-36,73% contro E18.31 matched). Respinta.

I profili V4/V5/V6/V7 sono candidati, non configurazioni promosse.
V11/V13 preservano la policy V7; non dichiararli nuovo modello economico.

42 test kernel/contratto/avvio/capacità/portafoglio superati prima di V17;
86 test mirati completi passati sul core V24.
Il builder parametrico è preparato per produrre un bundle autosufficiente con
hash del core e del profilo; la creazione del file non equivale a un upload.
Nessun nuovo upload eseguito finora. Nessun esperimento E19 avviato finora.
Valutazione consolidata di tutte le prove, escluso il duplicato originale
recuperato V22: `artifacts/derived/E18_33_RELEASE_FINAL_ASSESSMENT_20260907.json`.
La selezione finale è vuota. Gli upload restano autorizzati dal proprietario,
ma le condizioni di qualità richieste non sono state raggiunte.

## Limiti strutturali ancora aperti

La verifica delle rotte è giornaliera, non un certificato completo del
portafoglio futuro. Il rilascio del bootstrap non dimostra autonomia. Il
controller ha ancora una stima approssimata del costo-opportunità colturale,
del lavoro futuro e della crescita; la comparabilità con Top770 non è provata.
Non promuovere una correzione di sicurezza o una riduzione dei PASS sulla base
dei soli test: i gate economici includono tutti i seed, inclusi quelli negativi.
