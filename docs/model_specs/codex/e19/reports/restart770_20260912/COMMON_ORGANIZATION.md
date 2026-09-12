# Organizzazione produttiva comune e riesame della ricerca 770

## Che cosa occupa un’oca

L’oca occupa una casella COOP (pollaio), che è a tutti gli effetti spazio sottratto alle colture. La sigla 770 conta soltanto i PASTURE in Q0/Q1/Q2; il KPI occupied_livestock_tiles conta caselle con animali, comprese le oche. Nessuna oca è fuori griglia.

Nel rappresentante 107083439 a D16 risultano **14 pascoli pieni e 4 pollai, di cui 3 occupati**: 17 caselle con animali, ma **18 caselle destinate a strutture di allevamento**. Non identificare quindi né 14 né 17 con l’intero ingombro. Coordinate in COMMON_ORGANIZATION.json. Questa verifica strutturale puntuale riguarda quel replay, non certifica automaticamente il layout degli altri otto.

## Calendario comune osservato

Nove dei tredici esterni hanno gli stessi conteggi giornalieri di tutte le cinque colture e tre specie animali per D1–D30. Tutte le semine giornaliere coincidono nei nove; le quantità raccolte coincidono in otto. Le richieste di azioni giornaliere formano invece cinque gruppi (5+1+1+1+1): non è dimostrata l’identità del codice o delle azioni a ogni ora.

| Fase | Organizzazione osservata nel rappresentante 107083439 |
|---|---|
| D1–D10 | Avvio con 12 meloni e 7 grani; espansione fino a 20 fragole. |
| D11–D12 | Raccolta di 72 meloni a D11; a D12, 33 fragole, 21 grani, 8 mucche, 6 pecore e 3 oche. |
| D13–D20 | 33 fragole; grano rinnovato ogni giorno, circa 24–25 caselle. Organico variabile: 10 persone D13–15, 11 D16, 12 D18, 11 D20. |
| D21–D24 | Fine progressiva delle fragole e aumento del grano: a D24, 20 fragole e 38 grani. |
| D25–D28 | Successione verso carote: 4 a D25, 18 a D26, 29 a D27. Le semine D25–28 sono 4/14/11/2. |
| D29–D30 | Niente nuove semine; raccolte e liquidazione, mantenendo 12 persone anche D30. |

Il meccanismo plausibile è un calendario di raccolte e rinnovi coordinato con servizi ricorrenti e organico giornaliero, non la semplice scelta di un numero di animali. Non abbiamo ricostruito la regola decisionale privata né dimostrato un cap dei MOVE.

## Località: controllo puntuale

Confronto diagnostico di un replay per lato, D16–D25. Una visita è la permanenza consecutiva sulla stessa coordinata dello stesso indice lavoratore nel giorno. Si contano richieste di servizio, non esecuzioni riuscite; visite e ritorni comprendono anche deposito e altre caselle. Nessuna inferenza statistica sull’intera coorte da questi due casi.

| Misura | Esterno 107083439 | V51C 107218201 |
|---|---:|---:|
| entries | 1222.00 | 1696.00 |
| repeated_entries | 113.00 | 204.00 |
| services_per_service_visit | 2.08 | 1.81 |
| animal_services_per_visit | 3.21 | 2.79 |
| animal_service_visits | 185.00 | 149.00 |
| animal_visits_with_feed_and_care | 165.00 | 99.00 |

## Perché il lavoro precedente non ha chiuso il divario

1. **I riferimenti non erano un’unica strategia 770.** E18.14 studiava due riferimenti senza oche; il tentativo di rimuovere l’oca dalla nostra routine e sostituirla con una fragola perse il 2,94% nel pre-gate e fu respinto. Oggi il gruppo dominante usa tre oche; già il benchmark V51 del 9 settembre mostrava 2,4–3 oche medie nei tre gruppi leader. Generalizzare la sigla 770 al mix animale non è giustificato. Non è dimostrato che la V51 discenda dalla patch E18.14 respinta.

2. **Il calendario era stato riconosciuto, ma non interamente tradotto in percorsi vincolanti.** Il piano biologico del 7 settembre dichiarava già visite FEED+CARE, rinnovi, 23 grani/38 fragole e responsabilità territoriali. Dichiarava anche il limite: pesi approssimativi, territori morbidi e fattibilità del giorno corrente, senza garanzia del carico futuro. Avere gli obiettivi colturali non equivale a riuscire a servirli.

3. **Le ultime correzioni validate affrontavano finestre limitate.** V49F corregge l’assunzione improduttiva D2; V51C impegna percorsi completi a D29. Il checkpoint V51 del 9 settembre segnalava ancora D16–D25 come problema principale. Le correzioni restano utili ma non risolvono per costruzione l’intera fase produttiva.

4. **Il vecchio studio aveva già trovato un adattamento selettivo.** Nella diagnosi carote del 5 settembre, 36 dei 42 slot annuali cambiavano WHEAT/CARROT fra replay, conservando tempi, lavoratori e servizi. La scelta era compatibile con prezzi e negozi osservati, senza identificare una soglia. Quindi piano stabile e adattamento possono convivere. Quel corpus è diverso dai nove replay attuali: l’identità di questi ultimi non annulla l’evidenza precedente.

5. **Il recupero della conoscenza era incompleto.** In questo checkout mancavano V49–V51 e il relativo checkpoint, conservati in un altro worktree/ramo. Nelle risposte iniziali abbiamo riproposto analisi già fatte e lasciato temporaneamente V48 come riferimento più recente verificato. Il recupero di V51C e dei report corregge questa discontinuità; non prova una causa tecnica delle sconfitte, ma spiega parte del rischio di ripetere il lavoro.

Queste sono lacune documentate e limiti di trasferimento, non una prova causale unica. I prezzi delle fragole spiegano una parte importante del divario di ricavi fra coorti: non attribuire tutta la cassa all’organizzazione locale.

## Conseguenza per la ripresa

La base resta V51C congelata. Il prossimo esperimento deve partire da una diagnosi del suo dispatcher D12–D25, confrontando visite complete, rifornimenti, rinnovi e scadenze con il calendario osservato. Prima di modificare il mix, occorre distinguere una missione mai ammessa, una visita frammentata e una produzione completata ma venduta male. La presenza delle oche è una differenza concreta da quantificare separatamente, non una patch da sommare automaticamente a un nuovo routing.

Nessuna nuova policy o simulazione in questa analisi. I confronti puntuali non sostituiscono un audit di tutti i lavoratori dei 55 profili.

## Fonti precedenti recuperate

- [E18.14, ipotesi oca → fragola e pre-gate fallito](../../../e18/MODEL_SPEC_CODEX_E18_14_770_COOP_TO_CROP_RECLAIM_V1.md).
- [Piano biologico già implementato e suoi limiti](../biological_plan_770_20260907/PIANO_BIOLOGICO_770_D1_D25_IT.md).
- [Diagnosi carote e scelta condizionata](../../../e18/reports/E18_27_TOP770_D25_D30_CARROT_DIAGNOSIS_IT.md).
- Checkpoint V51: C:/Users/pietr/.codex/worktrees/dd62/kaggriculture-agent/docs/SESSION_CHECKPOINT_V51_20260909.md, commit 977d5e064f2ef9808b4cd03d41c1276ba94348af.
