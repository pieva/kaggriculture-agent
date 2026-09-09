# Codex 770 V50 — percorsi e capacità di lavoro in D29

**Revisione J respinta nello sviluppo, non pubblicabile come miglioramento validato.**
Baseline locale V49F;
release pubblicata sempre V48, submission 56101593. Gli esiti effettivi sono
nel [report](reports/pass_reduction_v50/REPORT_V50_IT.html) e nel
[summary J](reports/pass_reduction_v50/summary_v50j.json).

Tre seed di sviluppo, posto 0: cassa media +143,33 e PASS medi -52,33, ma
MOVE medi +6,33 e due FEED in meno nel campione. Falliscono i gate MOVE,
servizi e obblighi biologici. Non estesa all'altro posto né ai seed nuovi.
Il bundle è conservato solo per riproduzione e revisione. Nessuna variante
V50 supera tutti i controlli; V49F resta la candidata locale di riferimento.

## Modifica rispetto a V49F

La correzione dell'avvio D2 di V49F è ereditata integralmente. L'intervento
nuovo riguarda esclusivamente D29 (giorno engine 28). Non modifica D12–D15,
non usa il seed come feature e non legge replay o esiti futuri nel runtime.

Il packing dei percorsi tiene conto del grano e degli altri input già
trasportati da ciascuna persona, delle scorte nel deposito e dei prelievi
impegnati dalle missioni attive. Inserire una visita non può prenotare due
volte le stesse scorte. Le visite con input vengono distribuite prima di
riempire quei lavoratori con altro lavoro, conservando la precedenza dei
servizi protetti e gli stessi budget di tempo e costi di viaggio.

Per ogni batch di nuove assunzioni in D29 si cerca un packing dei servizi
biologici osservati e delle raccolte, prima con i lavoratori già presenti e
poi con incrementi fino al numero originariamente richiesto. Si considerano
le posizioni d'ingresso reali, il tick prima dell'ingresso dei nuovi manovali,
le missioni già impegnate, le scorte dopo le vendite e i prelievi prenotati.
Gli acquisti non ancora osservati non diventano inventario disponibile.
Se nessun packing passa, rimangono le assunzioni della baseline.

Il carico verificato include FEED, CARE, WATER e HARVEST. Le attività
facoltative FERTILIZE e COLLECT_FERTILIZER non giustificano da sole nuovi
manovali nel certificato, ma restano disponibili nel dispatcher reale.
Le missioni già ammesse vengono addebitate integralmente, comprese quelle
attività. Nessun nuovo ordine di acquisto o vendita viene introdotto.

## Significato e limiti della verifica di capacità

Il certificato prova l'esistenza di un piano per il carico incluso, usando
lo stato osservato. Non impone al dispatcher di seguire quel piano e non
garantisce capacità per tutto il futuro ciclo produttivo. Il vincolo di
rientro è quello ereditato da V49F: dipende da fine partita, cassa e stock
proiettato; lo scarico automatico notturno resta soggetto al limite del deposito.
Gli audit dei replay, non il solo certificato, determinano il superamento
dei gate economici, biologici, di inattività e movimento.

L'ordinamento dei servizi può cambiare raccolte, scorte intermedie e mercato.
Non promettere equivalenza dopo D29. Le azioni D1–D28 devono invece coincidere
con V49F nei controlli di parità. La riduzione dei MOVE non è dedotta dal
packing: viene misurata sul mese intero.

## Diagnosi e prove

Replay esposto 106843637: 719/719 azioni V48 riprodotte. Le sonde senza il
filtro dei percorsi individuano 8/8/6/11/10 slot PASS con almeno una visita
fattibile in D12/13/14/15/29. Sono opportunità condizionate, non un conteggio
di PASS sicuramente eliminabili. Le precedenti categorie di rifiuto con
prenotazione non vanno interpretate come prova causale completa.

Questa iterazione comprende 11 prototipi e 17 simulazioni di sviluppo;
H, J e K sono state provate sui tre seed. Gli esiti negativi restano visibili.
L'inferenza operativa è che limitare l'organico sulla base di un piano
possibile non basta: il dispatcher può spendere la capacità in altro modo,
richiedere assunzioni tardive e lasciare servizi scoperti. La prossima
revisione deve collegare il piano verificato alle assegnazioni realmente
eseguite, conservando l'audit dei servizi e senza consumare altri holdout
prima di superare lo sviluppo.

[Protocollo](reports/pass_reduction_v50/PROTOCOL_IT.md): tre seed di sviluppo,
entrambi i posti; partizione nuova preregistrata 260909201/202 da aprire solo
dopo il freeze e i gate di sviluppo. V4D rimane un controllo interno esposto.
I seed 260909101/102 della V49 sono ormai esposti. Nessun autore esterno nuovo
usato e nessuna submission. I posti non sono repliche statistiche indipendenti.

## Inventario

La [Foundation C2.1](../../../foundation/FOUNDATION_C2_1_MANIFEST.md) e il suo
manifest del motore restano il riferimento. Strategia ereditata:
[V48](MODEL_SPEC_CODEX_770_V48.md), [V49F](MODEL_SPEC_CODEX_770_V49F.md).
Il [manifest della candidata](reports/pass_reduction_v50/candidate_manifest.json)
elenca tutti i sorgenti effettivamente inclusi, il builder e gli hash.

| Responsabilità | Sorgente |
|---|---|
| Installazione e adattatore di avvio ereditato | [policy_770_v50.py](tools/policy_770_v50.py) |
| Packing con inventari e scorte condivise | [input_routes_v50.py](tools/input_routes_v50.py) |
| Limite osservato alle nuove assunzioni | [workforce_certificate_v50h.py](tools/workforce_certificate_v50h.py) |
| Posizioni d'ingresso (unico helper usato del prototipo A) | [workforce_certificate_v50.py](tools/workforce_certificate_v50.py) |
| Bundle standard-library | [submission_codex_e19_770_v50_candidate.py](../../../../submission/submission_codex_e19_770_v50_candidate.py) |
| Builder | [build_v50_submission.py](tools/build_v50_submission.py) |
| Sonde offline | [route_causality_v50.py](tools/route_causality_v50.py) |
| Simulazioni e gate | [run_pass_reduction_v50.py](tools/run_pass_reduction_v50.py), [analyze_pass_reduction_v50.py](tools/analyze_pass_reduction_v50.py) |
| Parità e runtime | [verify_v50_parity.py](tools/verify_v50_parity.py), [runtime_standard_v50.py](tools/runtime_standard_v50.py) |
| Test | [test_workforce_certificate_v50.py](tests/test_workforce_certificate_v50.py) |

Feature: tempo residuo TMP-01–09; posizioni, inventari, scorte, cassa e
ordini osservati; missioni attive e servizi derivati dalla V48. Nessun nuovo
modello di prezzi, nessun accesso alle informazioni private dell'avversario.
