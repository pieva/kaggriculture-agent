# E22 — baseline pubblicata

Submission **56206528**. Piano ricostruito dalle azioni pubbliche della submission **56165462**, episodio **108518933**; non è codice sorgente recuperato dal competitor.

## Strategia implementata

Un calendario di 719 azioni coordina espansione, coltivazioni, allevamenti, manodopera e vendite. La policy indicizza `_PLAN` con `day * 24 + hour` e restituisce una copia dell'azione. Fuori calendario restituisce PASS. Non usa prezzi, disponibilità di cassa o esiti delle azioni precedenti per ripianificare. Il risultato materiale può perciò variare quando una stessa azione non è eseguibile.

## File e integrità

- `submission/submission_codex_e22_s56165462_observed_v1.py`: bundle autonomo con funzione finale `agent`, compatibile con il caricatore Kaggle.
- `tools/build_compare_e22.py`: ricostruzione e diagnostica storica; richiede replay locali e avvia simulazioni se eseguito. Non usarlo come semplice controllo di compilazione.
- `reports/e22_release/PUBLICATION.json`: pubblicazione originale, hash e ID.
- `reports/e22_release/CLEANUP_VERIFICATION.json`: hash del file rinominato e parità delle 719 azioni.

La baseline rimane congelata. Ogni evoluzione avrà file, protocollo e risultati distinti. Le vecchie piste di ricerca sono materiale storico; stato e priorità risiedono in `docs/PROJECT_STATE.md` e `docs/NEW_SESSION.md`.
