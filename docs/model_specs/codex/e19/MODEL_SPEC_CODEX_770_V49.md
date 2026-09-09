# Codex 770 V49 — recupero locale e carico biologicamente ammissibile

**Candidata A respinta sul gate economico, non pubblicata.** La release Kaggle rimane V48, submission
56101593. Questa specifica descrive solo le modifiche della V49; strategia,
limiti ereditati e i 18 sorgenti della baseline sono documentati nella
[MODEL_SPEC V48](MODEL_SPEC_CODEX_770_V48.md).

La successiva [V49B](MODEL_SPEC_CODEX_770_V49B.md) restringe il recupero
all'ultimo comando del giorno e limita la riduzione dell'organico richiesto.
Questi sorgenti e il bundle A rimangono conservati per riprodurre la regressione.

## Diagnosi e obiettivo

Ridurre attese evitabili senza sostituirle con spostamenti o servizi inutili.
La diagnosi ricostruisce le 719 decisioni V48 sul replay esposto 106843637 e
registra PASS, posizione, inventario, missioni attive, offerte, tentativi di
preparazione, certificati e prenotazioni per persona. Le categorie di rifiuto
non sono automaticamente cause economiche provate. Dove l'evidenza non basta,
la causa rimane parzialmente ignota.

L'avvio D1–D11 resta identico: D2=69 PASS e D11=56 nel caso diagnosticato.
Tutti i 69 PASS di D2 e 55 di D11 sono già presenti nella tabella fissa
`ROUTINE_ACTIONS` del teacher; un PASS D11 è aggiunto dagli override. La
provenienza è verificata sul codice incorporato, non inferita dai conteggi.
La V49 non modifica il teacher né pretende di averne risolto il surplus di
capacità. D12–D15 sono trattati dal recupero locale; il miglioramento va misurato
e non assunto. D29 presenta una seconda causa verificabile nel codice:
il calcolo delle assunzioni aggiunge lavoro sui terreni liberi anche quando
nessuna coltura ammessa può più raggiungere la prima maturazione.

## Strategia implementata

1. Eseguire il dispatcher V48 normalmente, con i certificati e tutte le
   missioni già attive. Se una persona libera riceve PASS, cercare nell'ultima
   lista di offerte un servizio sulla sua casella. Non richiamare il planner
   per creare nuove offerte durante il recupero.
2. La casella non deve essere bersaglio di un'altra missione attiva. Le
   prenotazioni provvisorie delle code territoriali possono essere superate,
   ma i vincoli interni di preparazione e consegna restano applicati.
3. Eseguire soltanto FEED, CARE con beneficio futuro e alimentazione compatibile,
   WATER per rischio produttivo o incremento di resa e HARVEST maturo offerto
   dalla policy. Tutta la visita deve stare nel tempo residuo. Gli input devono
   essere già trasportati: una preparazione con MOVE/PICKUP viene rifiutata.
   Nessuna nuova semina, investimento, raccolta fertilizzante o FERTILIZE viene
   introdotta dal recupero. L'acqua terminale richiede una raccolta nella visita.
4. Nel calcolo delle assunzioni, disabilitare il solo carico speculativo delle
   nuove colture quando `day + min(first_yield_day) > final_day` per le specie
   ammesse. Non togliere il lavoro delle missioni attive né i servizi osservati.
   La condizione dipende dall'orizzonte biologico, non da una data copiata da
   un benchmark. Con la configurazione standard interviene su D29.

Il recupero non aumenta il percorso della missione aggiunta. Questo non implica
che i MOVE complessivi della partita siano matematicamente invarianti: le
traiettorie successive possono cambiare e devono superare il gate appaiato.
Analogamente, meno assunzioni riducono anche gli slot disponibili: il report
mostra sia PASS assoluti sia la loro quota, oltre alla spesa di manodopera.

## Informazioni e limiti

Clock e orizzonte: TMP-01–09; maturità e resa: CRP-03–15; acqua: CAR-01–03;
input e legalità: ELG-08–16; prenotazioni: POL-RES e contesto delle missioni.
Sono informazioni osservate o derivate dallo stato corrente. La telemetria
di esito non entra nelle decisioni. La Foundation corrente è identificata dal
[manifest C2.1](../../../foundation/FOUNDATION_C2_1_MANIFEST.md).

Questa candidata corregge due difetti circoscritti. Non ottimizza integralmente
organico, piano colturale e capacità su più giorni; non riconfigura l'avvio
assistito; non dimostra che ogni PASS residuo sia inevitabile. Il piano
giornaliero può ancora contenere prenotazioni inadeguate e lavoro distante.
Rimane il limite del carico approssimato per le colture ancora ammissibili.

## Inventario dei file

Il [manifest della candidata](reports/pass_reduction_v49_20260909/candidate_manifest.json)
elenca hash e percorso di ciascuno dei 21 sorgenti runtime e del builder.
Comprende tutti i 18 sorgenti V48, riutilizzati senza modifiche, più:

| Responsabilità | File |
|---|---|
| Ingresso sorgente, installazione V48 e correzioni | [policy_770_v49.py](tools/policy_770_v49.py) |
| Utilità biologica e recupero dei servizi locali | [local_service_770_v49.py](tools/local_service_770_v49.py) |
| Correzione dell'orizzonte nel carico per le assunzioni | [workload_770_v49.py](tools/workload_770_v49.py) |
| Build standalone in namespace isolato | [build_v49_submission.py](tools/build_v49_submission.py) |
| Artefatto standalone | [submission_codex_e19_770_v49_candidate.py](../../../../submission/submission_codex_e19_770_v49_candidate.py) |
| Telemetria non deliberativa e ricostruzione replay | [pass_diagnostic_v49.py](tools/pass_diagnostic_v49.py) |
| Provenienza dei PASS della routine assistita | [attribute_v49_opening.py](tools/attribute_v49_opening.py) |
| Run appaiato e matrice con partizioni esplicite | [run_pass_reduction_v49.py](tools/run_pass_reduction_v49.py), [run_v49_matrix.py](tools/run_v49_matrix.py) |
| Obblighi post-azione, stock perso, carico previsto/realizzato | [audit_v49_obligations.py](tools/audit_v49_obligations.py) |
| Parità bundle/sorgente e integrità baseline | [verify_v49_parity.py](tools/verify_v49_parity.py) |
| Integrità dell'engine e parità con ledger storici originali | [verify_artifacts_v49.py](tools/verify_artifacts_v49.py) |
| Report e figure rigenerabili | [build_pass_reduction_v49_report.py](tools/build_pass_reduction_v49_report.py) |
| Test dei confini biologici e dell'isolamento | [test_pass_reduction_v49.py](tests/test_pass_reduction_v49.py) |

I test della V48 sull'acqua produttiva e sull'audit del ciclo biologico restano
parte della verifica. Builder e runtime non leggono i replay esterni né il
checkout originale. Gli analizzatori possono leggere i grezzi originali in
`C:/Users/pietr/Projects/kaggriculture-agent` senza modificarli.

## Confronti e stato dei gate

Il [protocollo](reports/pass_reduction_v49_20260909/PROTOCOL_IT.md) separa
sviluppo (sei coppie, seed storici), trasferimento su seed nuovi (quattro coppie)
e validazione esterna, non eseguita. Tutti i controlli locali usano V4D, già
esposto. Nessun autore Top consumato viene presentato come nuovo holdout.

Gli esiti effettivi, comprese regressioni per caso, sono nel
[report](reports/pass_reduction_v49_20260909/REPORT_V49_PASS_IT.html) e nel
[riepilogo macchina](reports/pass_reduction_v49_20260909/summary.json).
La riduzione sul primo caso di sviluppo non è una promozione. I benchmark
estesi utilizzano un timeout locale ampliato dopo run con azioni assenti;
la conformità ai tempi Kaggle non è certificata. Nessuna nuova submission.
