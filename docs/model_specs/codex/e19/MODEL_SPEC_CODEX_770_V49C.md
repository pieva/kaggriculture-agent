# Codex 770 V49C — recupero conservativo della cura animale

Candidata locale respinta: sul seed 180903003 posto 0, cassa 60.764 contro
62.931 e PASS 1.111 contro 1.076. Non estesa né validata. La pubblicazione rimane V48, submission 56101593.
Il [report](reports/pass_reduction_v49_20260909/REPORT_V49_PASS_IT.html) documenta
risultati, gate e fallimenti delle revisioni precedenti. Nessuna nuova submission.

## Strategia effettiva

Eseguire normalmente l'intera policy V48. Soltanto nell'ultimo tick disponibile
del giorno, una persona libera che riceve PASS può eseguire CARE sulla casella
occupata, se l'animale è già alimentato, non è stato curato e può ancora usare
il bonus in una produzione futura entro l'orizzonte. Il bonus pendente non deve
essere saturo. La cura deve essere presente nelle offerte osservate del planner.

Non intervenire su missioni attive né su bersagli reclamati da altre missioni.
Superare soltanto le prenotazioni provvisorie territoriali; utilizzare la
preparazione interna V48 per verificare fattibilità e input. La visita deve
consistere in un unico comando, senza movimento o prelievo. Registrarla come
missione normale, con acknowledgement e aggiornamento dei KPI.

La V49C non modifica assunzioni, semine, FEED, WATER, raccolte o consegne del
dispatcher. Gli effetti futuri della cura possono comunque cambiare stock,
prezzi e decisioni: per questo cassa, MOVE e perdite devono essere misurati
sull'intera partita, non dedotti dall'utilità locale.

## Motivazione e limiti

La diagnosi V48 sul replay 106843637 riproduce 719/719 decisioni. D2: 69 PASS
già nella routine fissa; D11: 55 nella routine e un ulteriore override. Nei
giorni successivi coesistono rifiuti delle prenotazioni, input mancanti e
assenza di offerte. Il carico di semina conteggiato per assumere può essere
fuori orizzonte biologico in D29.

La [revisione A](MODEL_SPEC_CODEX_770_V49.md) prova un recupero locale più ampio
e rimuove quel carico impossibile; fallisce il gate economico. La
[revisione B](MODEL_SPEC_CODEX_770_V49B.md) restringe le correzioni ma perde
cassa e aumenta MOVE nel caso problematico. Entrambe sono conservate e respinte.
C deriva esclusivamente dai casi di sviluppo, prima di aprire i seed nuovi.

La riduzione attesa con C è piccola. Non risolve l'organico dell'avvio,
D12–D15 né il picco D29; non realizza una pianificazione completa della capacità
lungo i cicli biologici. Non affermare che tutti i PASS residui siano inevitabili.

## Sorgenti, feature e riproducibilità

La Foundation corrente è identificata dal [manifest C2.1](../../../foundation/FOUNDATION_C2_1_MANIFEST.md).
La strategia ereditata e i suoi 18 sorgenti sono nella [MODEL_SPEC V48](MODEL_SPEC_CODEX_770_V48.md).
Il [manifest C](reports/pass_reduction_v49_20260909/candidate_c_manifest.json)
elenca tutti i 20 sorgenti runtime e il builder con hash.

| Responsabilità | File |
|---|---|
| Ingresso sorgente | [policy_770_v49c.py](tools/policy_770_v49c.py) |
| Recupero CARE finale con utilità biologica osservabile | [local_service_770_v49c.py](tools/local_service_770_v49c.py) |
| Builder standalone | [build_v49c_submission.py](tools/build_v49c_submission.py) |
| Artefatto separato | [submission_codex_e19_770_v49c_candidate.py](../../../../submission/submission_codex_e19_770_v49c_candidate.py) |
| Diagnosi PASS e provenienza avvio | [pass_diagnostic_v49.py](tools/pass_diagnostic_v49.py), [attribute_v49_opening.py](tools/attribute_v49_opening.py) |
| Benchmark | [run_pass_reduction_v49.py](tools/run_pass_reduction_v49.py), [run_v49_matrix.py](tools/run_v49_matrix.py) |
| Audit per obbligo, stock e carico per persona | [audit_v49_obligations.py](tools/audit_v49_obligations.py) |
| Parità e integrità | [verify_v49_parity.py](tools/verify_v49_parity.py), [verify_artifacts_v49.py](tools/verify_artifacts_v49.py) |
| Report e KPI | [build_pass_reduction_v49_report.py](tools/build_pass_reduction_v49_report.py) |

Le feature decisioni sono clock residuo, posizione, flag fed/cared, bonus
pendente, calendario biologico e missioni/prenotazioni correnti. Nessun esito
futuro o prezzo non osservato entra nel recupero. La funzione care_value V48
valuta una possibilità produttiva, non garantisce un ricavo marginale.

## Gate

Protocollo e partizioni nel [PROTOCOL_IT](reports/pass_reduction_v49_20260909/PROTOCOL_IT.md).
La revisione C è stata fermata sullo screen esposto 180903003 posto 0:
60.764 di cassa e 1.111 PASS contro 62.931 e 1.076 della V48.
Nessun seed nuovo è stato usato per C. Il summary principale riguarda F,
non questa revisione respinta. Nessuna validazione con autori esterni non esposti.
Timeout locale ampliato per i confronti: gate runtime Kaggle non certificato.
