# Ripresa della sessione — ottimizzazione 770 dopo V48

Leggere prima la specifica della strategia e il nuovo report esterno.
Non avviare 662, non pubblicare nuove varianti e non trattare il rating cresciuto
come soluzione dei PASS. Il lavoro successivo è la diagnosi strumentata della
pianificazione e della capacità di lavoro, a parità di policy congelata.

## Riferimento pubblicato

V48 770, submission Kaggle **56101593**. File:
`submission/submission_codex_e18_770_v48_external.py`.
SHA-256: `57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`.
Policy invariata; nessuna nuova submission durante la revisione documentale.

## Aggiornamento esterno — coorte congelata

[Report replay e PASS](model_specs/codex/e19/reports/v48_external_pass_update_20260908/REPORT_V48_REPLAY_PASS_IT.html).
38 partite complete contro altri giocatori, fino all'episodio 106869264:
8 precedenti + 30 nuove, una partita self-play esclusa. Nessuna selezione per esito.
Rating letto all'inizio dell'acquisizione: **972,5**, contro 822,1 al primo controllo.
Non è un monitoraggio continuo; le partite successive al cutoff non sono incluse.

| Coorte | Vittorie / sconfitte | Cassa media V48 | PASS/giorno | PASS / slot disponibili |
|---|---|---:|---:|---:|
| Primi 8 | 5 / 3 | 90.826,75 | 35,50 | 14,64% |
| Nuovi 30 | 18 / 12 | 76.868,37 | 35,71 | 14,74% |
| Tutti 38 | 23 / 15 | 79.806,97 | 35,67 | 14,72% |

**Il rating cresce ma il problema PASS rimane invariato.** Gli avversari delle
stesse 38 partite hanno 27,27 PASS/giorno e quota 12,08%; non sono una coorte
Top770 e hanno dimensioni e strategie diverse. La cassa fra coorti non è una
misura controllata di miglioramento della policy, che è rimasta identica.

## Diagnosi operativa e prossima versione

- D2: 69 PASS in tutti i 38 replay; D11: 56 in tutti i casi. È un'indicazione
  di comportamento ripetitivo dell'avvio, non una prova completa della causa.
- D12–D15: 45,42 PASS/giorno; D16–D25: 27,68; D26–D30: 33,71.
- D29: media 76,34, intervallo 22–135. Picco 135 contro Sidharth Hulyalkar,
  episodio 106843637. D2 e D29 richiedono diagnosi separate.
- Il 73,25% dei PASS si concentra nelle ultime sei ore della giornata.
- 2,46 PASS/giorno avvengono su una casella con un servizio localmente
  disponibile e senza altri comandi attivi sulla stessa casella. La misura
  non certifica utilità economica né assenza di prenotazioni: è un punto di diagnosi.
- Nelle vittorie: 35,37 PASS/giorno; nelle sconfitte: 36,12. Non attribuire
  automaticamente le sconfitte a questa differenza.

**Priorità assoluta: PASS evitabili e coordinamento fra piano biologico e
manodopera, solo 770.** Riprodurre i picchi con motivi di rifiuto delle missioni,
carico previsto/realizzato e prenotazioni per persona. Proteggere raccolte,
FEED, CARE, WATER necessario e cassa. Non sostituire PASS con MOVE o servizi inutili.
662 e topologie alternative restano rinviate.

## Misurazione e riproducibilità

Il conteggio usa persone presenti prima del batch e 719 transizioni per replay.
Gli ordini PASS rivolti a lavoratori inesistenti sono esclusi: 0 per V48,
21 per gli avversari nell'intera coorte. Slot senza comando valido: 0 V48,
2 avversari. I servizi riusciti sono ricostruiti tramite engine; verificati
i saldi di entrambi i giocatori a ogni transizione dei 38 episodi.

Nuovi JSON grezzi: `data/replays/json/v48_update_20260908/`, conservati localmente
ed esclusi da Git. I primi 8 restano nel percorso originale indicato dalla
[coorte](model_specs/codex/e19/reports/v48_external_pass_update_20260908/cohort.json).
Profili, summary e manifest sono accanto al report e tracciati in Git.
Tutti i 38 casi e gli avversari osservati sono ora esposti, non holdout futuri.

Strumenti, dalla radice del repository con `.venv/Scripts/python.exe`:

- `docs/model_specs/codex/e19/tools/download_v48_update.py <episode_id> ...`
- `docs/model_specs/codex/e19/tools/analyze_v48_external_update.py`
- `docs/model_specs/codex/e19/tools/build_v48_external_update_report.py`

Gli identificativi sono congelati nell'analizzatore e nella coorte. I profili
sono cache dell'audit legate agli hash dei replay; se cambia la logica di audit,
produrre una nuova directory di analisi anziché riutilizzarli come nuovi risultati.

## Documentazione corrente

- [Foundation descrittiva](foundation/README.md): engine, ontologia, transizioni e feature.
- [Strategia Codex 770 e sorgenti](model_specs/codex/e19/MODEL_SPEC_CODEX_770_V48.md).
- [Piano di ottimizzazione e produzione](model_specs/codex/e19/design/V48_PLANNING_AND_BUILD_IT.md).
- [Registro di esposizione dei benchmark](../experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md).

La revisione documentale ha separato descrizioni e cronologia, documentato i
18 sorgenti del bundle e i formati di submission. Gli originali della Foundation
sono preservati nell'archivio di governance. Hash del bundle e sorgenti verificati;
nessuna modifica all'engine o alla strategia.

## Cronologia precedente

[Precedente punto di ripresa](history/v48_state_before_replay_update_20260908/NEW_SESSION.md).
