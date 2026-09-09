# Codex 770 V49F — avvio con tre manovali operativi in D2

Candidata separata, non pubblicata. La release Kaggle rimane V48, submission
56101593. [Report completo, KPI e gate](reports/pass_reduction_v49_20260909/REPORT_V49_PASS_IT.html).

## Strategia implementata

La diagnosi del piano assistito congelato identifica un manovale assunto
all'inizio di D2 che esegue esclusivamente 23 PASS. La V49F evita tale
assunzione e rimappa il lavoro del quarto manovale logico sul terzo fisico.
L'intervento è specifico del piano assistito 770 verificato, non una regola
generale per stabilire l'organico di qualsiasi fattoria.

Il punto di ingresso dipende dall'indice del manovale. Il terzo fisico nasce
in (5,5), mentre il quarto logico nasceva in (4,4). Il primo raggiunge (4,4)
con WEST/NORTH e riproduce il lavoro del secondo con due tick di ritardo.
Gli ultimi due comandi del piano logico sono PASS: nessun lavoro attraversa
il refresh. Due movimenti terminali dell'altro manovale, senza lavori o
consegne successive, sono eliminati. Il transito aggiunto ha uno scopo e
viene compensato eliminando altrettanto transito inutile.

L'agricoltore e gli altri lavori rimangono quelli del piano. Al termine di
D2 si verificano equivalenza di fattoria e inventari e risparmio di tre unità
di cassa, dovuto alla scala dei costi di assunzione (7 contro 4). Si misura
se questa piccola differenza di cassa produca ulteriori divergenze successive.
Nessuna osservazione sintetica o persona inesistente viene fornita al planner.

Il recupero si abilita soltanto in D2 H1 con configurazione standard 10×10,
24 turni/giorno e 720 stati, nessun manovale presente, cassa sufficiente alle
quattro assunzioni originali e batch composto proprio da quattro HIRE.
In caso contrario rimane la V48. Assert sulla routine e sui comandi rendono
visibili eventuali incompatibilità, invece di scartare silenziosamente lavoro.

## Diagnosi, tentativi e limiti

Replay esposto 106843637: 719/719 decisioni V48 riprodotte, PASS per persona,
posizione, inventario, missioni, offerte, certificati e prenotazioni.
Tutti i 69 PASS D2 erano nella tabella fissa; D11 ne aveva 55 più un override.
Le cause dopo l'avvio rimangono in parte ignote: un rifiuto con prenotazione
non certifica da solo che la missione fosse utile e fattibile.

Le revisioni A–C con recuperi locali falliscono i gate economici. D isola la
correzione delle assunzioni fuori orizzonte, ma aumenta i MOVE medi. E omette
la diversa posizione iniziale del manovale rimappato: è scartata per errore
di geometria; il suo incremento di cassa non è evidenza di miglioramento.
I risultati e i sorgenti sono conservati e separati dalla candidata F.

F corregge una parte del picco D2. Non risolve D11, D12–D15 e D29, né ottimizza
la capacità lungo tutti i cicli biologici. Il carico di semina fuori orizzonte
rimane diagnosticato, con modifiche respinte. L'organico e il dispatcher dopo
questo giorno rimangono V48. Non dichiarare risolto l'intero problema PASS.

## Inventario e feature

Foundation corrente: [manifest C2.1](../../../foundation/FOUNDATION_C2_1_MANIFEST.md).
Strategia ereditata e 18 sorgenti invariati: [MODEL_SPEC V48](MODEL_SPEC_CODEX_770_V48.md).
Il [manifest F](reports/pass_reduction_v49_20260909/candidate_f_manifest.json)
elenca tutti i 19 sorgenti runtime e il builder con hash.

| Responsabilità | File |
|---|---|
| Installazione V48 e adattatore del piano D2 | [policy_770_v49f.py](tools/policy_770_v49f.py) |
| Builder standalone | [build_v49f_submission.py](tools/build_v49f_submission.py) |
| Artefatto | [submission_codex_e19_770_v49f_candidate.py](../../../../submission/submission_codex_e19_770_v49f_candidate.py) |
| Diagnosi e provenienza dei PASS | [pass_diagnostic_v49.py](tools/pass_diagnostic_v49.py), [attribute_v49_opening.py](tools/attribute_v49_opening.py) |
| Benchmark e apertura della partizione nuova | [run_pass_reduction_v49.py](tools/run_pass_reduction_v49.py), [run_v49_final.py](tools/run_v49_final.py) |
| Equivalenza dopo D2 | [verify_opening_equivalence_v49f.py](tools/verify_opening_equivalence_v49f.py) |
| Obblighi e carico previsto/realizzato | [audit_v49_obligations.py](tools/audit_v49_obligations.py) |
| Parità e integrità | [verify_v49_parity.py](tools/verify_v49_parity.py), [verify_artifacts_v49.py](tools/verify_artifacts_v49.py) |
| Test della rimappatura | [test_opening_770_v49f.py](tests/test_opening_770_v49f.py) |
| Report e figure | [build_pass_reduction_v49_report.py](tools/build_pass_reduction_v49_report.py) |

Feature: clock TMP-01–09, posizione, manovali presenti, cassa e costo delle
assunzioni, più piano noto della routine congelata come contesto di policy.
Conoscere i comandi del proprio piano non significa conoscere gli stati futuri
del gioco. Nessun replay o esito futuro è letto dal runtime della candidata.

## Verifiche

Esito: tutte le sei coppie di sviluppo e le quattro sui seed nuovi danno
−23 PASS, MOVE invariati e cassa +3. D2 passa da 69 a 46 PASS. Servizi,
raccolte, perdite e obblighi scoperti sono invariati; tutti i gate locali
passano. Dopo D2, nessuna differenza nelle azioni e nelle caselle dei dieci
casi. Parità standalone/sorgenti 719/719 nei due posti e 17 test superati.
Rimane una candidata locale, con i limiti di certificazione qui sotto.

[Protocollo](reports/pass_reduction_v49_20260909/PROTOCOL_IT.md): tre seed di
sviluppo × due posti, poi due seed nuovi × due posti contro V4D già esposto.
Freeze prima dell'apertura, registrato in `validation_opened.json`. Nessuna
modifica guidata dalla validazione. Stato effettivo dei gate nel
[summary](reports/pass_reduction_v49_20260909/summary.json).

I posti non sono repliche indipendenti. Il timeout locale ampliato evita di
confondere azioni assenti del banco di prova con il comportamento della policy;
non certifica il runtime Kaggle. Nessun avversario esterno non esposto è stato
usato e nessuna nuova submission è stata pubblicata.
