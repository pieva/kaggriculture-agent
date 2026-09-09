# Codex 770 V49D — correzione prudente del carico di manodopera

Revisione respinta dal gate MOVE: media +6,33 sui sei confronti, pur con
cassa media +183,33. Non pubblicata. La release Kaggle rimane V48,
submission 56101593. [Risultati e gate](reports/pass_reduction_v49_20260909/REPORT_V49_PASS_IT.html).

## Diagnosi e strategia implementata

La V48 aggiunge al carico per le assunzioni un termine fino a quattro ore per
casella libera finanziabile, anche quando nessuna coltura ammessa può più
maturare. Nell'orizzonte standard questo avviene in D29. La V49D usa le regole
delle specie e il termine effettivo della partita: se tutte le specie soddisfano
`day + first_yield_day > final_day`, ricalcola il carico senza quel termine.
Missioni attive e servizi osservati restano inclusi.

La riduzione del target di manovali viene limitata a **uno rispetto al target
che il vecchio estimatore calcolerebbe sullo stesso stato**. È una protezione
sperimentale contro l'imprecisione del costo dei percorsi. Non è una prova che
l'organico rimanente sia ottimo, né elimina tutto il sovradimensionamento.
Limiti di cassa, ordini, assunzioni e riserve del controller restano applicati.

Il dispatcher è integralmente V48: nessuna sostituzione diretta di PASS,
nessun recupero locale aggiunto, nessun nuovo servizio o spostamento. La
correzione agisce solo sulla stima che determina le assunzioni. Le azioni
D1–D28 devono restare identiche sui confronti standard appaiati. D2, D11 e
D12–D15 non sono corretti da questa candidata.

## Revisioni respinte e limiti

La diagnosi del replay V48 esposto 106843637 riproduce tutte le 719 decisioni,
con inventari, posizioni, missioni, offerte, rifiuti e prenotazioni per persona.
I 69 PASS D2 sono nella routine fissa; D11 ne contiene 55 più un override.
I rifiuti osservati dopo l'avvio non equivalgono a evitabilità dimostrata.

Sono conservate tre revisioni respinte sullo sviluppo: [A](MODEL_SPEC_CODEX_770_V49.md)
recupera servizi locali e riduce più ampiamente il carico; [B](MODEL_SPEC_CODEX_770_V49B.md)
limita visita e organico; [C](MODEL_SPEC_CODEX_770_V49C.md) recupera solo CARE.
La loro utilità locale non protegge l'intera traiettoria di cassa e produzione.
D isola quindi l'effetto delle assunzioni, senza recuperi locali.

La soluzione è parziale: non ricostruisce un piano ottimo semina–maturazione–
raccolta per l'intero mese, non ridimensiona l'avvio assistito e non elimina
tutte le prenotazioni inefficienti. Un singolo caso può avere più PASS pur
riducendo MOVE e aumentando la cassa; il report espone ogni differenza.

## File e feature

Foundation corrente: [manifest C2.1](../../../foundation/FOUNDATION_C2_1_MANIFEST.md).
Strategia e 18 sorgenti ereditati invariati: [MODEL_SPEC V48](MODEL_SPEC_CODEX_770_V48.md).
[Manifest D](reports/pass_reduction_v49_20260909/candidate_d_manifest.json):
hash di tutti i 20 sorgenti runtime e del builder.

| Responsabilità | File |
|---|---|
| Ingresso e installazione dopo la V48 | [policy_770_v49d.py](tools/policy_770_v49d.py) |
| Orizzonte colturale e target prudente dell'organico | [workload_770_v49d.py](tools/workload_770_v49d.py) |
| Builder standalone | [build_v49d_submission.py](tools/build_v49d_submission.py) |
| Artefatto separato | [submission_codex_e19_770_v49d_candidate.py](../../../../submission/submission_codex_e19_770_v49d_candidate.py) |
| Diagnosi delle decisioni | [pass_diagnostic_v49.py](tools/pass_diagnostic_v49.py) |
| Provenienza dell'avvio | [attribute_v49_opening.py](tools/attribute_v49_opening.py) |
| Run e matrice | [run_pass_reduction_v49.py](tools/run_pass_reduction_v49.py), [run_v49_matrix.py](tools/run_v49_matrix.py) |
| Obblighi, stock e capacità per persona | [audit_v49_obligations.py](tools/audit_v49_obligations.py) |
| Parità delle azioni e integrità | [verify_v49_parity.py](tools/verify_v49_parity.py), [verify_artifacts_v49.py](tools/verify_artifacts_v49.py) |
| Report e figure appaiate | [build_pass_reduction_v49_report.py](tools/build_pass_reduction_v49_report.py) |
| Test dei confini biologici | [test_pass_reduction_v49.py](tests/test_pass_reduction_v49.py) |

Clock/orizzonte TMP-01–09 e prima maturità CRP-03–10 sono derivati online.
Superficie libera, costo dei semi, cassa, persone, missioni e offerte sono
osservati o contesto della policy. Il limite di una persona è una scelta
sperimentale, non un fatto dell'engine. Nessun esito futuro guida il calcolo.

Il modulo sostituisce soltanto il metodo di mercato all'interno delle closure
ereditate, preservando ritenzione del fertilizzante e guardia terminale.
Gli assert del builder/installatore richiedono un solo punto di modifica.

## Verifiche e interpretazione

[Protocollo](reports/pass_reduction_v49_20260909/PROTOCOL_IT.md): D completa
tre seed di sviluppo × due posti, con cassa media +183,33 e MOVE medi +6,33.
Il gate MOVE fallisce e D non viene estesa ai seed nuovi. Il summary principale
riguarda F, non D. Tutte le correzioni A–D precedono l'apertura della validazione.

I confronti estesi usano `actTimeout=120` dopo
run concorrenti con azioni assenti. Gate runtime Kaggle non certificato;
nessuna validazione con avversari esterni non esposti. Le posizioni abbinate
non sono repliche statisticamente indipendenti.
