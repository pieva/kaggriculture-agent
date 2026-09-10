# Stato del progetto — E20.1, correzione caricamento Kaggle

Aggiornamento 2026-09-10. Il primo invio E20v28 ha fallito la validazione (episodio 107444826): `NameError: name '__file__' is not defined`, alla prima chiamata. Il loader Kaggle usa un namespace exec senza quel campo; i precedenti test con runpy non riproducevano questa condizione.

Corretto soltanto il nome diagnostico passato a due compile dei moduli incorporati. Il bundle originale resta congelato. Nuovo file: `submission/submission_codex_e20_772_e20v28_loaderfix.py`, SHA256 `9d84c838de39c2c8df620a21db258ea4a4065a5a2b4f75288bde53218d71c9bb`.

Verifica: 2 test di regressione passati senza __file__ e senza letture di file; 719 azioni identiche per ciascuno dei due ruoli (1.438 totali) sui replay E20v28 seed 180910101, usando la funzione agent del bundle caricata con exec. Nessuna modifica alla strategia. Nuovo invio Kaggle: **Pending**; rating non disponibile.

Il risultato interno rimane: +6,16% nello sviluppo, -5,82% nella conferma indipendente contro E18; non promossa economicamente. La pubblicazione serve alla verifica esterna richiesta dal proprietario.

- [Ricevuta del fallimento](model_specs/codex/e20/artifacts/E20_1_EXTERNAL_PUBLICATION_RECEIPT.json)
- [Ricevuta del nuovo invio](model_specs/codex/e20/artifacts/E20_1_LOADERFIX_PUBLICATION_RECEIPT.json)
- [Verifica di parita](model_specs/codex/e20/reports/e20_1/LOADER_FIX_VALIDATION.json)
- [Report economico e 22 KPI](model_specs/codex/e20/reports/e20_1/REPORT.html)

---

Checkpoint precedenti (stati di pubblicazione storici):

## 2026-09-10 — E20.1 inviata per verifica esterna

Su richiesta esplicita del proprietario, caricato su Kaggle il bundle E20v28 congelato (target 772), SHA256 `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. Stato osservato: **Pending**, nessun rating ancora disponibile. Il mancato superamento del gate economico interno rimane registrato; questa pubblicazione e una verifica esterna sperimentale.

[Ricevuta](model_specs/codex/e20/artifacts/E20_1_EXTERNAL_PUBLICATION_RECEIPT.json) · [Submission Kaggle](https://www.kaggle.com/competitions/kaggriculture/submissions).

---

Checkpoint interno precedente (le indicazioni di mancata pubblicazione qui sotto sono storiche):

# Stato del progetto — E20.1, revisione del pianificatore

Lavoro del 2026-09-10 concluso. **Non promossa: il gate indipendente non è superato.** Nessuna nuova pubblicazione Kaggle. La candidata è E20v28, target 7–7–2: percorsi con tile lontani inseriti per primi a parità di urgenza e filtro dei CARE senza incremento produttivo possibile.

Sviluppo: 10 seed già noti, entrambi i ruoli; +6,16% rispetto a E19, 8/10 seed positivi, stress 2,30 per partita, zero perdite animali.

Conferma indipendente: 7 nuovi seed, 42 partite tra E18/E19/E20.1. Contro E18, delta E20.1−E19 -5,82%, 1/7 seed positivi, stress 3,79, perdite animali 0. Il risultato di sviluppo non sostituisce questa verifica.

| Modello | Vittorie / partite | Cassa media torneo |
|---|---:|---:|
| E18 | 20/28 | 60.978,89 |
| E19 | 13/28 | 61.443,11 |
| E20.1 | 9/28 | 59.671,43 |

## Artefatti e ripresa

- [Report finale E20.1](model_specs/codex/e20/reports/e20_1/REPORT.html).
- [Torneo e 22 KPI](model_specs/codex/e20/reports/e20_1_confirmation/REPORT.html).
- [Specifica](model_specs/codex/e20/E20_1_SPEC.md) e [protocollo](model_specs/codex/e20/E20_1_PROTOCOL.json).
- [Decisione verificata](model_specs/codex/e20/reports/e20_1/DECISION.json) e [verifica delle 42 partite](model_specs/codex/e20/artifacts/E20_1_CONFIRMATION_VERIFICATION.json).
- [Bundle E20.1](../submission/submission_codex_e20_772_e20v28_candidate.py).
- [Controllo 770 con lo stesso pianificatore](model_specs/codex/e20/reports/e20_1/topology_control/REPORT.html): controllo di ricerca, non nuova versione ufficiale E19.

SHA256 E20.1: `83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1`. E18 V4D, E19 V48 e la precedente E20v18 restano congelati. Riferimento pubblicato invariato: submission Kaggle 56101593, V48 770.

Tutti i 17 seed usati in questa revisione sono ora esposti: non riutilizzarli come holdout dopo modifiche. Il gate è definito prima dei risultati e distingue cassa media, distribuzione per seed e fragilità biologica. Non promuovere una variante soltanto per il migliore seed o per il numero di WATER/PASS.

Su questo portatile usare un solo processo per i confronti ufficiali. Il solo stato finale DONE non basta: entrambi gli agenti devono ricevere 719 chiamate. Cinque tentativi incompleti del torneo e due del controllo 770 sono archiviati in `invalid_under_load`; sono stati ripetuti senza modificare modelli, seed o limiti di gioco. Non includerli nelle medie.

Il lettore dei replay deve ricostruire il campo condiviso `step` anche per il ruolo 1. Le traiettorie standard e i saldi derivano da ledger verificati. I replay compressi restano disponibili localmente e ignorati da Git.

[Checkpoint precedente E20v18](history/e20_1_before_20260910/PROJECT_STATE.md).
