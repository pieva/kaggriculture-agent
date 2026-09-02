# Verifica e pulizia post-release esterna E17

- **Data:** 2026-09-02
- **Responsabile integrazione:** Codex
- **Verdetto:** `PASS_WITH_LOCAL_CACHE_DEBT`

## Perimetro

La verifica chiude il riordino del repository dopo il caricamento della
submission `CODEX-E17.0-EXTERNAL-CONTROL-V1`. Non introduce mutazioni della
policy e non autorizza E17.1.

## Decisioni di pulizia

1. `submission/submission_copilot.py` è stato rimosso. Era una copia
   byte-identica della candidate Codex, con lo stesso SHA-256
   `0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`,
   e non rappresentava la baseline nativa Copilot.
2. `submission/` contiene ora un solo artefatto canonico:
   `submission/submission_codex.py`.
3. La baseline nativa Copilot resta preservata nei percorsi agent-local:
   source in `src/agricola/strategy/copilot/e17_native_3q.py`, config, freeze,
   runner e report in `experiments/e17/`. Per decisione del proprietario non
   verrà caricata su Kaggle.
4. La directory locale ignorata `scratch/`, i `__pycache__` e `.ruff_cache`
   sono stati rimossi. `.pytest_cache` e `.pytest_temp` restano non rimovibili
   per ACL Windows, ma sono ignorati da Git e non fanno parte del prodotto.
5. Antigravity è in pausa per esaurimento crediti; non vengono eseguiti tornei
   locali incompleti. Lo sviluppo attivo proseguirà con Codex dopo la
   stabilizzazione del rating esterno.

## Stato esterno osservato

La submission Kaggle `559588638` è attiva. Gli screenshot forniti dal
proprietario mostrano il passaggio da `600` a `996`, pari a `+396`. Il dato è
classificato `OBSERVED / INTERIM`: nello snapshot più recente è ancora
presente un episodio in corso e non esiste ancora uno score stabile.

## Gate rieseguiti

```text
MIGRATION_ROWS: 1058
MIGRATION_PRESENCE_FAILURES: 0
E17_JSON_FILES_VALID: 70/70
ACTIVE_MARKDOWN_FILES: 66
ACTIVE_LOCAL_LINKS: 36/36
FILES_GE_90_MIB: 0
STANDALONE_IMPORT: PASS
BEHAVIORAL_PARITY: 719/719 PASS
TEST_SUITE: 62/62 PASS
SUBMISSION_DIRECTORY_CANONICAL_FILE_COUNT: 1
```

Gli hash immutabili di Ontology C2.1, State Machine C2.1, Feature Model C2.1,
observation contract e routine module Codex coincidono con il freeze. La
submission mantiene SHA-256
`0428A6244C28E064BEDCEDC21C793D50A7C3231B8B7ADADF154BF40667833FC6`.

## Decisione operativa

```text
E17_EXTERNAL_SUBMISSION: LIVE_SCORE_STABILIZING
E17_1_AUTHORIZED: NO
ACTIVE_DEVELOPMENT_AGENT: CODEX_ONLY
NEXT_ACTION: WAIT_FOR_STABLE_EXTERNAL_RATING
```

Il valore intermedio `996` non sostituisce il precedente riferimento V9
`1159,9`, non dimostra regressione o miglioramento causale e non va usato per
selezionare post-hoc una nuova combinazione di leve.
