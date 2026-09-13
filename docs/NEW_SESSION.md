# Ripresa — E22.2 pubblicata, 13 settembre 2026

## Stato corrente

- **E22.1 — Pollai**, controllo pubblicato **56206528**: tre pollai Q0 con oche; totale 8 mucche, 6 pecore, 3 oche. Bundle `submission/submission_codex_e22_1_pollai.py`.
- **E22.2 — Pascoli**, submission **56212495**, stato **Complete** verificato su Kaggle: originale 8C9S v1; pecora in ciascuno dei tre pascoli (4,1), (3,2), (2,3), totale 8 mucche e 9 pecore. Bundle `submission/submission_codex_e22_2_pascoli.py`, hash `df6991a5619f09e91bef6b6ac7034ade10f87c59e577d49c19cf197cd5cd2dcd`.
- **Calendario esterno v2**: esperimento distinto, non selezionato e non pubblicato.

[Registro versioni](model_specs/codex/e22/VERSIONS.json) · [Pubblicazione](model_specs/codex/e22/reports/e22_2_release/PUBLICATION.json) · [Revisione](model_specs/codex/e22/reports/e22_2_release/REVIEW.md).

Il primo score visualizzato per E22.2 è 600,0: dato iniziale, non valutazione stabilizzata. Episodio osservato disponibile: 108620991. Il prossimo lavoro utile è analizzare un campione esterno di E22.2 confrontandolo con E22.1; attendere il mandato dell’utente prima di avviare nuove simulazioni, modifiche strategiche o pubblicazioni.

## Evidenze e limiti

[Confronto E22.2 contro E22.1](model_specs/codex/e22/reports/e22_2_vs_e22_1/REPORT.html): 14 partite seriali, seed esposti 180911301–307 in entrambi i ruoli. E22.2 vince 4/14, media margine +353,14, mediana −2.092. I ruoli danno esiti identici: sette seed indipendenti. Nessuna superiorità interna regolare dimostrata; pubblicazione diagnostica esplicitamente richiesta dall’utente.

Revisione del file pubblicato: parità di 10.066 azioni con caricatore reale, determinismo, osservazioni immutate, zero fughe/errori contabili e tutto il latte/lana raccolto venduto. Restano giorni isolati senza alimentazione, due fertilizzanti residui e assenza di recupero generale dalle divergenze di cassa/stato. Le vendite lana cambiano anche prima di D11. I seed 180912401–407 sono ancora riservati e non usati.

[Traiettorie esterne](model_specs/codex/e22/reports/external_pasture_trajectories/REPORT.html): sei replay con tre pascoli, calendario ricorrente. [Calendario v2](model_specs/codex/e22/reports/q0_8c9s_calendar_v2/REPORT.html): implementato e verificato, ma margine medio +130,57, peggiore di v1 di 222,57; non scelto. La ricorrenza non prova ottimalità.

## Repository e riproduzione

Codice, report e verifiche sono versionati. I replay grezzi compressi rimangono locali, conservati senza cancellazioni, con [manifest](model_specs/codex/e22/reports/e22_2_release/LOCAL_ARTIFACTS.json). Gli strumenti e i requisiti per rigenerare i report sono descritti nel [README](model_specs/codex/e22/README.md). Non modificare automaticamente il checkout originale.

[Stato progetto](PROJECT_STATE.md) · [Registro esperimenti](EXPERIMENT_LOG.md) · [Contesto precedente archiviato](governance/history/session_snapshots/2026-09-13_e22_2_release/NEW_SESSION.md).
