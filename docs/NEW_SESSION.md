[Checkpoint di ripresa e riproduzione](SESSION_CHECKPOINT_V51_20260909.md). Ramo di salvataggio: `codex/v51-benchmark-checkpoint`.

## Benchmark esterno V51C con i leader — 9 settembre 2026

Completati tre nuovi riferimenti, cinque replay ciascuno: Top770-004 Himanshu Kumar (4/5 finali 770), Top770-005 pensukesan (5/5), Top770-006 kanno (4/5). Corpus completi nei grafici Leader-V51-01/02/03; tutti i 15 replay inclusi. Controllo: V51C esterna n42. Confronto descrittivo, non appaiato; nuovi riferimenti ora esposti.

D16-D25: V51C PASS 27,08, MOVE 154,18, personale 13, WATER 35,06, CARE 11,61, costo assunzioni 376/giorno. Leader: PASS 4,16-8,48, MOVE circa 113, personale circa 11,67, WATER circa 44, CARE circa 17, costo circa 204. Il divario permane nel sottoinsieme 770. I mix biologici differiscono; evitare tagli ciechi di personale. Prossima priorita diagnostica: servizio e percorsi nella fase produttiva. Nessuna variante implementata durante il benchmark.

[Report benchmark e tre confronti da 22 KPI](model_specs/codex/e19/reports/top_v51_20260909/REPORT_TOP_V51_IT.html). Protocollo, catalogo, CSV e manifest nella stessa cartella.

## Submission esterna V51C: audit replay del 9 settembre 2026

Submission **56124996 Complete**, rating osservato **942,1**. Coorte congelata: 42 partite contro altri giocatori, 22 vittorie / 20 sconfitte, cassa media 79.977,83. Un self-play escluso. PASS medi 33,18/giorno (13,94% degli slot); D29 34,36 contro 76,34 nella coorte storica V48 (confronto non appaiato). Nessun obbligo biologico mancato a D29; restano deficit negli altri giorni. Nessuna fuga animale o perdita per decadimento. Il ledger rileva una differenza di 1 nella cassa dell'avversario Scorpi, episodio 107183104 step 566; cassa V51C riconciliata, risultati originali Kaggle conservati.

[Report KPI esterno](model_specs/codex/e19/reports/v51_external_20260909/REPORT_V51_REPLAY_KPI_IT.html), coorte, hash, CSV e diagnosi nella stessa cartella. Ricevuta aggiornata in `docs/model_specs/codex/e19/artifacts/derived/v51_external_publication_receipt.json`. Tutti questi episodi sono ora esposti. Nessuna nuova variante o submission prodotta durante questo audit. Il checkpoint locale seguente precede la pubblicazione; le sue frasi di mancato invio sono storiche.

# Ripresa della sessione — V51C candidata locale verificata

V51C impegna percorsi completi al giorno 29 e dimensiona le assunzioni sulle
visite residue. I sei casi di sviluppo passano: cash medio +345, PASS −53,
MOVE −34,33 rispetto a V49F; servizi e deficit non peggiorati. Bundle fissato:
`43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda`.
Parità sorgente/bundle/replay: 719 azioni. Sette test mirati passati.
La validazione 260909201/202 è stata aperta il 2026-09-09 13:45:22 UTC,
entrambi i posti; questi seed sono ora esposti. Risultati e protocollo in
`docs/model_specs/codex/e19/reports/pass_reduction_v51`. Nessuna submission.
Validazione completata: cash medio +64,50, PASS −45,50, MOVE −61; tutti i
gate aggregati passano, servizi e deficit invariati. Il seed 260909201 peggiora
su cash/PASS, quindi non affermare che ogni seed migliora. Le due prove seriali
standard passano, 719 azioni identiche per posto; overage 32,75/44,93 s su 60.
[Report finale](model_specs/codex/e19/reports/pass_reduction_v51/REPORT_V51_IT.html).
V51C è la nuova candidata locale; V49F resta baseline e V48 resta pubblicata.
Non riottimizzare su 260909201/202 trattandoli come nuovi holdout. Nessuna
submission eseguita, nessun commit/push. Bundle finale in
`submission/submission_codex_e19_770_v51_candidate.py`.

## Iterazione precedente V50

Ultima iterazione: [report V50](model_specs/codex/e19/reports/pass_reduction_v50/REPORT_V50_IT.html)
e [specifica V50 J respinta](model_specs/codex/e19/MODEL_SPEC_CODEX_770_V50.md).
11 prototipi, 17 simulazioni sui tre seed di sviluppo (posto 0). Nessuna V50
supera tutti i gate. J: cassa media +143,33 e PASS -52,33, ma MOVE +6,33 e
due FEED in meno nel campione. Non promuovere il bundle V50.
Nell'iterazione V50 i seed preregistrati 260909201/202 non erano stati aperti.
V49F supera le prove seriali del runtime standard nei due posti del seed
180903001: 719 azioni in parità, zero errori, overage 18,11 e 20,30 secondi
entro i 60 consentiti. JSON `runtime_v49f_*.json` nel report V50.
È una verifica locale, non una garanzia sull'hardware Kaggle.
Prossimo problema: far eseguire il piano di capacità verificato dal dispatcher,
invece di usare quel piano soltanto per ritardare le assunzioni.

## Baseline locale conservata

Leggere [MODEL_SPEC V49F](model_specs/codex/e19/MODEL_SPEC_CODEX_770_V49F.md),
[report con grafici](model_specs/codex/e19/reports/pass_reduction_v49_20260909/REPORT_V49_PASS_IT.html)
e [riproducibilità](model_specs/codex/e19/reports/pass_reduction_v49_20260909/REPRODUCE_IT.md).
V48 pubblicata e tutti i suoi sorgenti restano congelati. Non avviare 662 e
non pubblicare nuove varianti senza richiesta. Il rating non risolve i PASS.

La diagnosi riproduce 719/719 azioni del replay esposto 106843637. D2 include
un manovale assunto per eseguire solo 23 PASS. F elimina quell'assunzione,
compensa la diversa posizione di ingresso e rimuove due movimenti terminali
inutili. Lo sviluppo completo (tre seed, entrambi i posti) dà per ogni caso
−23 PASS, MOVE invariati e cassa +3. Anche le quattro coppie sui due seed nuovi
confermano lo stesso effetto. Tutti i gate locali passano: servizi, raccolte,
perdite e obblighi scoperti invariati. Dopo D2, tutte le azioni coincidono nei
dieci casi. Parità bundle/sorgenti: 719/719 nei due posti; 17 test superati.
Il `summary.json` mantiene separate le due partizioni.

Le revisioni A–E sono respinte e conservate: regressioni economiche, aumento
dei MOVE oppure errore di geometria. Nessuna modifica F guidata dai seed nuovi.
D11, D12–D15 e D29 rimangono aperti. Non dichiarare risolto il problema globale.
Timeout locale 120: runtime Kaggle non certificato. Nessuna nuova submission
e nessuna prova con avversari esterni non esposti.

## Contesto storico V48 preservato

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
