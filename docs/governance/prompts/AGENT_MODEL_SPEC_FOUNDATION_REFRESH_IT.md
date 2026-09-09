# Prompt — revisione MODEL_SPEC sulla Foundation aggiornata

Destinatari: Antigravity, Claude e Copilot, ciascuno per il proprio modello.
Inviare lo stesso testo separatamente a ciascun agente.

---

Leggi la Foundation aggiornata e rivedi la MODEL_SPEC del tuo modello affinché descriva chiaramente la tua strategia e i file che la implementano. Lavora in autonomia sulla tua documentazione, mantenendo le tue scelte strategiche e verificandole contro il codice effettivo.

## Letture richieste

Dalla radice del repository, leggi nell'ordine:

1. `README.md`, per il metodo e il processo di benchmark, incluso il collegamento al report grafico dei KPI.
2. `docs/foundation/README.md` e `docs/foundation/FOUNDATION_C2_1_MANIFEST.md`, per identificare i documenti correnti.
3. `docs/foundation/ENGINE_CONTRACT.md`.
4. `docs/foundation/ontology/ONTOLOGY_C2_1.md`.
5. `docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md`.
6. `docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md` e `docs/foundation/feature_model/FEATURE_CATALOG.md`.
7. `docs/model_specs/README.md`, `docs/PROJECT_STATE.md` e il README della tua directory `docs/model_specs/<agent>/`.
8. La tua MODEL_SPEC di riferimento e i sorgenti, configurazioni, builder e verifiche che ne realizzano il comportamento.

Le copie C1/C2 e gli archivi sono provenienza storica: usa come riferimento la Foundation corrente indicata dal manifest. La MODEL_SPEC Codex può essere consultata come esempio di struttura documentale, senza assumerne la strategia come requisito comune.

## Revisione richiesta

Identifica esplicitamente modello, versione e implementazione descritti. Se esistono più candidate, chiarisci quale documenti e il suo stato, senza presentare una candidata congelata o respinta come attiva. Conserva le specifiche storiche congelate: quando necessario, crea una revisione documentale distinta nella tua directory e collegala dal tuo README.

La MODEL_SPEC deve spiegare:

- **Obiettivo e ipotesi:** risultato perseguito, ambito, assunzioni e limiti.
- **Strategia:** come pianifichi produzione, investimenti, risorse e manodopera; orizzonte del piano e condizioni di revisione.
- **Decisioni:** feature realmente usate, criteri di scelta, priorità fra azioni concorrenti, vincoli e principali parametri con la loro motivazione.
- **Reazioni:** gestione di imprevisti, carenze, conflitti, fallback e chiusura della partita.
- **Coerenza con la Foundation:** collega regole e concetti pertinenti e separali dalle tue scelte strategiche. Segnala eventuali discrepanze fra specifica, codice e Foundation.
- **Stato di realizzazione:** distingui comportamento implementato, realizzazione parziale e proposta futura. Non descrivere un'intenzione progettuale come capacità già presente.

Inserisci una sezione **File di implementazione** con una tabella:

| File, con link relativo funzionante | Ruolo | Parte della strategia implementata | Categoria |
|---|---|---|---|
| Percorso effettivo | Responsabilità concreta | Sezione o decisione corrispondente | Runtime / configurazione / builder / submission / test |

Ricostruisci l'elenco partendo dall'entry point e dalle dipendenze effettive, includendo i moduli condivisi o ereditati realmente utilizzati. Elenca singolarmente i file: non sostituire l'inventario con un nome di directory o un wildcard. Distingui i sorgenti dal bundle generato e dagli strumenti di verifica; non attribuire alla versione descritta file di vecchie candidate che non vengono utilizzati. Se un file manca o una dipendenza non è verificabile, dichiaralo.

Mantieni risultati dei benchmark, cronologia e prossime attività nei rispettivi report o registri, con collegamenti dalla MODEL_SPEC. Il report KPI è evidenza diagnostica: rispetta lo stato di esposizione dei corpus e distingui osservazioni, inferenze e ipotesi da verificare.

## Consegna e verifica

Aggiorna la tua MODEL_SPEC e il relativo indice. Questa richiesta riguarda la documentazione: conserva runtime, configurazioni, Foundation condivisa e artefatti congelati; eventuali correzioni del codice o nuove strategie vanno descritte come proposte separate. Non avviare benchmark, tuning o submission per questa revisione.

Verifica che ogni file inventariato esista, che i link siano risolvibili e che le descrizioni corrispondano al codice letto. Non dichiarare test eseguiti se hai soltanto consultato i file di test.

Nella risposta finale riporta il link alla MODEL_SPEC rivista, i documenti modificati, una breve descrizione della tua strategia, il numero di file censiti per categoria e le eventuali discrepanze o parti ancora non implementate. Indica le verifiche realmente svolte.
