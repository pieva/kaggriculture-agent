# E17.2 — Readiness della submission Kaggle Codex V4D

Data: 2026-09-02

Release: `CODEX-E17.2-V4D-D28-KAGGLE-CANDIDATE-V1`

Stato: `READY_FOR_OWNER_UPLOAD`

## File da caricare

`submission/submission_codex_e17_v4d.py`

- entry point: `agent`;
- dimensione: `433.331` byte;
- SHA-256:
  `2792244CA71115E6CAAFDFC942B6D9AAAF09B95FC717A5B182D07A31D9717CD7`;
- copia di freeze: byte-identica;
- dipendenze dal repository locale: nessuna a runtime.

Le submission precedenti `submission_codex.py` e
`submission_codex_e17_reactive.py` non sono state sovrascritte.

## Policy inclusa

Il bundle incorpora la catena completa congelata:

1. routine 3Q V9 come provider iniziale;
2. guardia Wheat/feed;
3. adattamento ai regimi di mercato;
4. dispatcher state-driven di servicing e routing;
5. liquidazione terminale V3;
6. batching V4D con rilascio dei carrier Wheat soltanto dopo il feed completo.

L'handoff globale D27 non è incluso: la relativa ablation ha fallito i gate
economici. La release mantiene D28.

## Evidenza precedente alla release

- sviluppo inerte: `135.096,83` contro `134.351,33`, `+0,555%`, positivo 6/6;
- stress su quattro regimi: `124.090,17` contro `123.199,54`, `+0,723%`;
- confronti multi-regime non negativi: `24/24`;
- MOVE/service multi-regime: `2,922` contro `2,967`;
- zero fughe, errori, fallback, residui vendibili o violazioni non-SELL;
- holdout e final confirmation non consumati.

Queste misure sono development evidence, non una previsione calibrata del
rating Kaggle. La submission serve precisamente a verificare la validità
esterna contro avversari non controllati.

## Verifica standalone

- import con Python isolato (`-I`): `PASS`;
- parità azione per azione: `4.314/4.314`;
- parità reward terminale: `6/6`;
- seed: tre development, entrambi i seat;
- errori e fallback: `0`;
- bundle e freeze: stesso SHA-256.

## Descrizione Kaggle consigliata

`Codex E17.2 V4D D28 — reactive 3Q service routing with post-feed capacity batching; +0.72% across controlled dev regimes, 24/24 matched gains, zero escapes.`

## Dopo l'upload

Registrare nel manifest l'ID della submission, l'ora di avvio e gli snapshot
del rating senza confrontarli direttamente con il reward locale. Dopo
l'assestamento, scaricare un piccolo corpus di replay unici per verificare:

- frequenza e cause effettive degli override;
- resa del batching sotto contesa reale;
- quota livestock e capacità di Q2;
- output raccolto, depositato e venduto;
- eventuali fughe o residui terminali.
