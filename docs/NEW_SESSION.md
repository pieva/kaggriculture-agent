# NEW_SESSION — Kaggriculture

## Ripartenza operativa anti-PASS — stato aggiornato 2026-09-06

### Aggiornamento più recente — chiusura entro un'ora e prova dell'avvio

Il proprietario ha chiesto chiusura E18/770, controllo Q0/KPI, pubblicazione e
Git. Ha poi autorizzato esplicitamente **E18.32 V9 come controllo provvisorio,
NON benchmark E19**, se la policy comune non supera le verifiche. L'avvio può
avere poche impostazioni esplicite, non imporre una traiettoria medio-lunga.

Prove E18.33: V6 raggiunge 770 ma perde economia; V7 con avvio 2 COW/2 SHEEP
e colture brevi passa un solo smoke economico, non i KPI macro. La successiva
estensione V9 fino al rinnovo completo del primo ciclo è fallita su quattro
casi: il rilascio guidato dallo stato arriva troppo tardi e non dimostra
autonomia. Nessuna nuova policy comune è eleggibile; E19 non avviata.

Report corrente:
`docs/model_specs/codex/e18/reports/E18_CLOSEOUT_AND_BOOTSTRAP_20260906_IT.md`.
Nuova verifica diretta E18.32 V9: Q0 conserva 12 tile libere D11–D13 e il
settimo pascolo a D14. **E18.32 V9 pubblicata, submission 56056189, Complete**,
upload 2026-09-06 13:27:24 UTC. Solo controllo diagnostico autorizzato, non
benchmark E19. Non duplicare l'upload. Receipt:
`docs/model_specs/codex/e18/artifacts/derived/E18_32_KAGGLE_UPLOAD_RECEIPT_V9_20260906.json`.
V9 nativa estesa: rilascio D16–D17, media 40.227,25 (-51,28% contro E18.31
matched), nessuna 770, perdite e tempi di chiamata critici. Non promuoverla.
Prossimo intervento: separare gli impegni iniziali dalle nuove opportunità;
non attendere il rinnovo dell'ultima tile per autorizzare tutti gli investimenti.
97 test mirati passati. La cronologia seguente conserva i checkpoint precedenti.

### Mandato corrente: E18.33 — implementazione delle policy agricole comuni

Aggiornamento del proprietario: avviare l'implementazione e l'ottimizzazione
della E18/770 parametrica. **E19 è riservata alla successiva verifica 770/772/662
con le stesse policy**, solo dopo consolidamento della 770. Roadmap:
`docs/model_specs/codex/e19/MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md`.
Le traiettorie esterne servono come diagnosi di efficienza/produttività, non
come calendario o obiettivo numerico del controller.

Decisione più recente del proprietario: **unica policy per Q0, Q1 e Q2**.
Q1 differisce per disponibilità del terreno, non per programma; Q2 ha solo
colture quando il budget globale di pascoli è già assegnato. Aumentando quel
budget, deve proporre un pascolo con la stessa policy, senza date o coordinate
aggiunte a mano. Prima applicazione diagnostica Q0, Q1 controllo di trasferimento.

Audit, specifica e kernel completati; E18.33 ha un **prototipo nativo, non una
release eleggibile**. Non confondere le approssimazioni del prototipo con il
certificato economico e di capacità definito nella specifica.
Profilo pulito: target globale 14, capacità uniforme 7 per quadrante, massimo
tre quadranti e dodici manovali, pesi globali specie 9:5. Budget compatti per
ordine di disponibilità → 770; target 15 → 771 soltanto in test sintetico,
non nuova autorizzazione a cambiare topologia o pubblicare.

Confermati: target pascoli fissi, settimo Q0 a D14, mix per quadrante, raccolto
MELON anticipato a D11 senza spostare la risemina D14/15, vecchie code/organico,
blackout e PLANT limitati al programma. Nei sei replay E18.31 il 91,73% dei
PASS D5–D10 avviene comunque con Q0 pieno: non attribuire tutto alle tile vuote.
La configurazione nuova rifiuta chiavi legacy. **67 test passati**: 34 profilo,
22 kernel, 11 contratto motore/regressioni. Il prototipo non eredita controller
o piani storici, ma il modello economico e di capacità è ancora incompleto.
Non modificare baseline/config congelate per simulare una
pulizia che distruggerebbe riproducibilità.

Fonti normative correnti:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.md`,
`docs/model_specs/codex/e18/reports/E18_33_LEGACY_POLICY_AUDIT_20260906_IT.md`,
`docs/model_specs/codex/e18/configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json`.
Checkpoint implementativo e risultati, inclusi i fallimenti:
`docs/model_specs/codex/e18/reports/E18_33_NATIVE_POLICY_CHECKPOINT_20260906_IT.md`.
Codice: `e18_33_common_policy.py` e `e18_33_common_controller.py` nella dir tools.
Undici partite diagnostiche sul seed development 180903001, nessun nuovo Top.
V1–V3 un caso ciascuno; V4–V5 quattro casi ciascuno, due seat e due campioni.
V5: zero morti/fughe ma topologia effettiva **6-5-0** in tutti e quattro,
cassa media 71.869,25 contro E18.31 matched 82.560 (**-12,95%**), due missioni
terminali incomplete. PASS medi 892,25 contro 846,50; nessun gate superato.
Target di configurazione 770 NON significa 770 raggiunta. Le mucche rimangono
ritardate; non dichiarare risolta l'ottimizzazione. Nessun standalone E18.33.

Prossima implementazione: valore residuo e rollout del portafoglio nei due
scenari, certificato congiunto di manutenzione E crescita con finanziamento,
scorte, rotte e assunzioni, spiegazione dei rifiuti e chiusura completa.
La manutenzione non deve lasciare alla crescita soltanto gli spazi residui.
Usare stessa policy su tutti i quadranti, test Q0/invarianza e poi gate completo.
Vietato importare un piano storico o usarlo come fallback.
Scenari economici V1 preregistrati nella specifica: neutro con impatto dei propri
volumi e prudente sui prezzi osservati nella sola partita; incremento di cassa
positivo e finanziamento/capacità fattibili in entrambi. Congelare implementazione
e protocollo prima del gate, senza adattarli ai Top già consumati.
Nessuna nuova submission; le prove economiche E18.33 eseguite sono diagnostiche
e negative, non il gate completo. Nessun esperimento E19, upload o Git alignment.

### Ciclo precedente concluso: radici dei PASS ed E18.32

Il proprietario ha chiesto di verificare i residui delle traiettorie precedenti
e correggere i PASS iniziali con policy generali. Sviluppo **E18.32
DEMAND RELEASE V9** nel ciclo precedente, ora controllo interno congelato;
baseline immutabile E18.31 UNIFIED V11 pubblicata.
Non cambiare topologia, mix o benchmark; non pubblicare senza nuova richiesta.

Audit dei sei replay E18.31: 4.314/4.314 batch ricostruiti identici. PASS D5–D10:
77,45% coda esaurita, 16,60% attesa dell'ora nominale, 5,95% raccolta
fertilizzante in testa alla coda bloccata. Il piano agricolo E18.28 C conserva
orari, organico e calendario storico. I vecchi override di mercato sono invece
bypassati da UNIFIED: non confondere ereditarietà con esecuzione attiva.

V7: prima verifica su 28 casi, PASS D1–D10 -27,01%, cassa +0,188%, zero perdite,
ma un FEED e una lana in meno. Conservata come intermedia, non candidata finale.
V8 sulle prenotazioni esclusive non spiega/risolve quel FEED. V9 protegge la
liquidità della manutenzione: vietata la compattazione se il cibo già dovuto
dipende da incassi da consegnare. Include anche crescita nel certificato di
capacità, rientro tempestivo del latte e rilascio dei servizi confermati prima
che finisca il trasporto. Il calendario colturale resta controllo e fallback:
non dichiarare riscritta tutta la policy né risolti tutti i PASS.

Verifica completa V9: 28/28 safety pass, cassa media +0,230% (28/28 delta
positivi), PASS D1–D10 -24,91%, D5–D10 -21,99%. Mucche/colture giornaliere e
raccolti colturali/lana conservati. Massimo 12, tutti a 12 da D16 a D30.
71 test mirati pass. File corrente `submission/submission_codex_e18_32_770_v9.py`,
SHA-256 `4d2d32ac41b38af5f4f632ef9e8dd9af2ebd37f7e7bcb1795c2c31cda4e92789`.
Il file E18.32 senza `_v9` è l'intermedio V7. Parità V9 completata: quattro
casi, 2.876 batch identici source/standalone e tramite caricatore Kaggle;
massima chiamata misurata 0,819 s. Non conforme alla nuova policy comune.
Problema non integralmente risolto: D7/D9 invariati; D12 più PASS ma meno MOVE.
La successiva decisione E18.33 supera la prosecuzione dei soli adattamenti
di finanziamento/rilascio sulle vecchie code. Fonti di questo ciclo storico:
`docs/model_specs/codex/e18/MODEL_SPEC_CODEX_E18_32_770_READY_WORK_V1.md` e
`docs/model_specs/codex/e18/reports/E18_32_PASS_ROOTS_AND_VERIFICATION_20260906_IT.md`.
Nessun nuovo Top770 consumato, nessun upload/commit/push o pulizia dei raw.
Le informazioni E18.31 qui sotto descrivono il ciclo precedente e la baseline.

### Ciclo precedente: verifica pubblica e rotazione dei benchmark

Il proprietario ha autorizzato esplicitamente la pubblicazione diagnostica di
E18.31 UNIFIED V11. File costruito e verificato: 2.876 batch source/standalone
identici, stessa parità tramite caricatore Kaggle. SHA-256
`59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63`.
Upload completato il 2026-09-06 alle 08:35:23 UTC: submission **56050866**,
stato **Complete** verificato. Non reinviare. Receipt e primi replay pubblici
sono in `docs/model_specs/codex/e18/artifacts/derived/E18_31_KAGGLE_UPLOAD_RECEIPT_V11_20260906.json`.
Questa autorizzazione supera il precedente divieto di upload automatico, non
promuove il candidato e non dimostra risolti PASS/economia.

Report corrente V4: 22 pannelli, WATER/FEED/CARE riusciti separati. Jesse è
Top770-001, consumato; il report storico E18.31 è l'ultima chiusura, non nuovo
holdout. Nuovo autore selezionato e studiato: **Top770-002**, submission
56044235, quattro replay 770 su cinque e 16/16 checkpoint D15–D30 conformi
nei quattro. Unico ciclo diagnostico E18.31 concluso: anche Top770-002 è ora
consumato, non riutilizzarlo per release successive. Registro comune:
`experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md`.
Mantenere 770 e massimo 12 manovali nella release: nessuna modifica dell'agente
durante l'attesa. Le nuove ipotesi devono essere policy generali trasferibili
ad altre architetture, non obiettivi copiati da un benchmark.

Primo corpus E18.31 pubblico congelato: sei partite competitive, 5 WIN / 1 LOSS,
zero morti crop/fughe, tutti i ledger riconciliati. PASS D5–D10 medio 294,17;
mucche D8 7–8 e D9 8–9. Cassa media 103.311,17, non stimatore di superiorità
sul Top: avversari e prezzi diversi. Il nuovo benchmark ha tre oche, mix/cap
diverso e perdite biologiche; non copiarne la chiusura. Il grafico CARE rivela
un servizio intermittente nostro D19–D25 con FEED ancora presente: da studiare
come problema generale di assegnazione e valore marginale, senza cambiare 770.
Report corrente e prossime ipotesi:
`docs/model_specs/codex/e18/reports/E18_31_PUBLIC_TOP002_DIAGNOSTIC_20260906_IT.md`.
Due report V4 disponibili: chiusura storica interna e confronto pubblico n6/n4.
49 replay catalogati; rimossi 38 raw di solo screening (1.234.785.677 byte),
conservati gli 11 raw del ciclo corrente. Recupero con URL/hash nel riferimento
`docs/model_specs/codex/e18/reports/E18_31_PUBLIC_REPLAY_REFERENCE_20260906_IT.md`.
55 test mirati pass, QA grafici light/dark a tre larghezze pass. Nessun nuovo
commit/push e nessun intervento sugli altri agenti congelati.

Decisione del proprietario: l'eccesso di PASS è un sintomo del motore di
assegnazione, da riprogettare. Ciclo precedente: **E18.31 — assegnazione ed
espansione integrate**, baseline verificata E18.30 V2 da preservare.
Priorità aggiornata del proprietario: PASS e mucche sono un unico problema
di capacità produttiva, con diagnosi D5–D10 e policy generale D1–D30.
L'espansione delle mucche deve essere valutata come fonte di lavoro, fertilizzante
e ricavi per la manodopera libera, non dopo aver risolto separatamente i PASS.
Non passare ad altri filoni prima di avere verificato entrambi. Nessun tuning
sulle date o traiettorie Top770. I primi esperimenti E18.31 sono respinti:
meno PASS non basta se economia o sicurezza biologica peggiorano.
Checkpoint del ciclo **E18.31 UNIFIED V11**: 28/28 simulazioni interne con safety
pass; nei 14 confronti E18.16, PASS D5–D10 467,79 → 294,93, mucche D8 4 → 7
e D9 4 → 8, senza ridurre l'organico giornaliero D5–D10. Cassa media
81.976 → 81.965,64 (-0,013%): non promossa, entrambi i problemi non ancora
dichiarati risolti. Rimangono code esaurite e vincoli orari del piano legacy;
la nuova ammissione investimenti è unica, non ancora tutto il programma.
Dettagli e prossima diagnosi nello stato agente:
`docs/model_specs/codex/e18/reports/E18_31_UNIFIED_V11_CHECKPOINT_20260906_IT.md`.
La cronologia precedente è conservata in
`docs/history/NEW_SESSION_PRE_ANTI_PASS_20260905.md`, non è una seconda fonte
di istruzioni correnti. Stato sintetico: `docs/PROJECT_STATE.md`.

## Invarianti e controlli

- Topologia target esatta **7-7-0**, 14 pascoli, cap 14 animali e massimo
  12 manovali. Non variare topologia fino a una riduzione consistente del gap.
- Sola linea attiva Codex; Antigravity, Claude e Copilot restano congelati.
- Ultima pubblicata: **E18.31 UNIFIED V11**, submission **56050866**,
  `submission/submission_codex_e18_31_770.py`; non promossa, verifica esterna.
- Parent pubblico immutabile: **E18.28 C**, submission Kaggle **56036993**,
  `submission/submission_codex_e18_28_770.py`, SHA-256
  `8788f68c74b95c56c21feffba6fd5c49654d1c2dc5e71b5a0ca94800f988969d`.
  File immutabile, controllo parent, non incumbent promosso.
- **E18.29 B3** è development, non pubblicata e non promossa: guadagno locale
  +7,68% su 14 casi contro E18.16 rispetto al parent, PASS -26,78%, MOVE +8,09%.
  Resta una morte Strawberry D12 ereditata: gate mortalità assoluta fallito.
  Non confondere questi risultati interni con i replay pubblici E18.28.
- E18.16 ed E18.2 sono campioni interni; E18.2 resta riferimento esterno
  storico migliore indicato dal proprietario. Gli score nei vecchi report
  sono snapshot datati, non valori live.
- Top770 è l'alias documentale. ID/hash e identificativi tecnici congelati
  preservano la provenienza; non rinominare piani/config rompendo i loader.

## Evidenza di origine, non obiettivo da copiare

Corpus pubblico congelato a episodio 105876558: **30 partite competitive,
17 sconfitte e 13 vittorie, 30 avversari**, self-test escluso. Parità shadow
21.570/21.570 batch con E18.28 pubblicata; non simulazioni controfattuali.
PASS medi 1.573,7. Nelle sconfitte D15-D30: 746,3 PASS, di cui 622,8 code
esaurite (83,5%) e 123,5 attese pianificate; zero blocchi immediati in questa
finestra non esclude effetti indiretti di precedenti mancate esecuzioni.
Il fenomeno è presente anche nelle vittorie: PASS non spiega da solo l'esito.

In 105864674 e 105874761 le assunzioni D11 falliscono per cassa: rimangono
7 e 3 manovali. Nessun nuovo HIRE dopo H2 malgrado incassi successivi;
WATER/HARVEST rimangono assegnati a lavoratori assenti. I due casi totalizzano
32 morti crop. Non assumere che tutti i lavori siano recuperabili a fine giorno.

Flussi monetari verificati 29/30 (tutte le 17 sconfitte); un'eccezione da 81
in 105852748 resta N/D, non zero. Nessuna fuga nei 29 casi verificati.
Nessuno dei 17 vincitori avversari è exact770: gap economici descrittivi,
non stime di guadagno causalmente recuperabile a parità di architettura.
Le opportunità locali HARVEST/CARE/WATER/fertilizzante sono proxy sovrapposti,
non ricavi da sommare e non autorizzano missioni incomplete.

Fonti da leggere, sotto `docs/model_specs/codex/e18/`:

1. `reports/E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md`.
2. `reports/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_IT.md`.
3. `artifacts/derived/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_V2.json`
   e profili `artifacts/derived/e18_28_external_pass_20260905_v2/`.
   I profili senza suffisso v2 sono preliminari, non usare per conclusioni.
4. `MODEL_SPEC_CODEX_E18_29_770_ANTI_PASS_V3.md`.
5. `MODEL_SPEC_CODEX_E18_30_770_MISSION_DISPATCHER_V1.md`.

## Sequenza di sviluppo E18.30–E18.32 — cronologia, non nuovo mandato

1. Separare obiettivo economico, missione completa e azione; ledger unico di
   missioni con identità, prerequisiti, deadline, risorse e stato verificato.
2. Assegnare soltanto ai manovali osservati, rimettere nel pool i lavori orfani;
   un comando emesso non costituisce conferma di esecuzione. Nessuna assunzione
   soltanto prevista può aggiungere capacità al batch corrente.
3. Prima tranche isolata: nucleo di assegnazione e test di contratti/regressione.
   **Implementata: 25 test pass, incluso stress su 100 scenari sintetici.**
   File `docs/model_specs/codex/e18/tools/e18_30_mission_dispatcher.py`;
   report `docs/model_specs/codex/e18/reports/E18_30_MISSION_DISPATCHER_GATE_0_IT.md`.
   **Adattatore online E18.30 CROP_POOL V2 implementato e verificato.**
   44 test dedicati; suite completa 371 pass. OFF: 2.876 batch identici.
   POOL V1: gate economico pass, safety fail (una morte crop ereditata).
   V2: missione completa PLANT→WATER per obblighi pianificati a rischio;
   14/14 casi development migliori del parent, cassa media 81.976 contro
   74.491,57 (+10,05%), PASS D15–D30 -58,68%; zero morti/fughe/errori o
   missioni incomplete. Vittorie E18.16 5/14, parent 1/14: gap non risolto.
   E18.2 smoke: 69.768 contro parent 60.612, ma avversario 83.466 (0/2 vittorie).
   File `submission/submission_codex_e18_30_770.py` generato, NON pubblicato;
   parità source/standalone e caricatore Kaggle su quattro casi (2.876 batch
   per metodo). Nessun holdout consumato; HIRE/payroll non ancora modificato.
   Report autorevole:
   `docs/model_specs/codex/e18/reports/E18_30_RUNTIME_V2_CONSOLIDATED_20260906_IT.md`.
4. Congelare economia, mix e topologia del parent per la prima ablation.
   Mai ridurre PASS aggiungendo movimento, WATER inutile o lavoro senza vendita.
5. Confronto matched su sette seed development × due seat contro E18.16,
   smoke E18.2 e confronto delta con E18.28 C; E18.29 B3 controllo secondario.
   Misurare cassa finale/minima, mortality, servizio WATER/FEED, raccolti/vendite,
   PASS normalizzati, MOVE/productive, deadline mancate e missioni orfane.
   Test avversari/seed multipli; nessun tuning per episodio o Top770.
6. Non promuovere il nucleo isolato come agente funzionante. Prima del rilascio:
   safety senza nuove perdite, beneficio economico robusto, parità standalone
   e gate preregistrati; holdout non ancora consumato.

Prossima tranche: stress online generici di cassa/assunzioni parziali e confronto
più ampio E18.2; poi eventuale payroll/HIRE retry come ablation distinta.
Non ripetere l'integrazione già completata, non aspettare aggiornamenti dello
score per sviluppare, non pubblicare automaticamente in base al solo development.

## Verifica esterna e formato di analisi

Resta il processo concordato: sviluppo sui campioni interni completamente
ispezionabili; submission quotidiana del migliore sviluppo eleggibile per
verifica esterna, analisi quotidiana dei top per architetture/strategie.
Non forzare l'upload di una regressione o consumare holdout per rispettare
la cadenza. Non è una nuova autorizzazione a creare automazioni duplicate.

Grafici sempre **Top770 vs una sola versione**, D1-D30, standard V4 comune:
22 pannelli incluso WATER/FEED/CARE riusciti al giorno e separati, senza Cause PASS.
Conservare tutte le specie, cassa, personale, MOVE/PASS, mancata irrigazione,
perdite verificate, weed e ricoveri vuoti distinti. Affiancare tabelle KPI
economico-operativi e denominatori reali, non soltanto consistenze.
`experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V4_IT.md`.

## Organizzazione e chiusura

Strategie, specifiche, tool, test e dati Codex sotto `docs/model_specs/codex/e18/`;
`experiments/` contiene protocolli e materiale comune. Conservare anche risultati
negativi, fonti e audit. Eliminare solo cache riscaricabili catalogate e QA
rigenerabili, previa verifica hash/path; niente rimozione di evidenza unica.
Il monitor dei primi replay E18.28 è stato messo in pausa: questa chiusura
viene eseguita nella sessione attuale, senza duplicare commit o upload.
Checkpoint pubblicati su Git: `4a3b7fd`, freeze byte-identici `f036cd6`, nucleo
E18.30 `b8aaf70`. L'integrazione V2 e i risultati del 2026-09-06 sono nel working
tree; nessun nuovo commit/push/upload è implicito nei gate locali.
