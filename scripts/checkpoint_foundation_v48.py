"""One-time documentation checkpoint; run from repository root."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
B = Path('docs/model_specs/codex/e19')
if Path('docs/foundation/V48_PLANNING_AND_BUILD_IT.md').exists():
    raise SystemExit('Historical one-time migration already applied; use verify_foundation_v48.py.')
def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
def append(p, text):
    s = p.read_text(encoding='utf-8')
    if 'Checkpoint operativo 2026-09-08: V48 e PASS' not in s:
        write(p, s + '\n\n## Checkpoint operativo 2026-09-08: V48 e PASS\n\n' + text + '\n')

# Preserve useful session recipes before cleaning disposable scratch output.
archive = B/'tools/session_archive_20260908'
archive.mkdir(exist_ok=True)
for p in Path('scratch').iterdir():
    if p.is_file() and p.suffix in {'.py', '.cjs', '.js', '.json', '.html'}:
        shutil.copy2(p, archive/p.name)
write(archive/'README.md', '''# Ricette storiche della sessione

Snapshot dei file operativi precedentemente presenti in scratch. Conservati per
provenance, non sono entry point supportati: alcuni generatori modificano file,
aggiungono checkpoint o dipendono dai percorsi scratch originali. Non eseguirli
in blocco. Usare la catena canonica in docs/foundation/V48_PLANNING_AND_BUILD_IT.md.
''')
shutil.copy2(Path('scratch/new_top_cohorts.json'), B/'artifacts/derived/new_top_cohorts.json')
p=B/'tools/analyze_new_top_v48.py'
write(p,p.read_text(encoding='utf-8').replace("ROOT/'scratch/new_top_cohorts.json'", "B/'artifacts/derived/new_top_cohorts.json'"))
shutil.copy2(Path('scratch/summarize_new_top.py'), B/'tools/summarize_new_top_v48.py')

manifest=json.loads((B/'artifacts/derived/v48_external_manifest.json').read_text(encoding='utf-8'))
inventory=[]
for name,h in manifest['sources'].items():
    p=Path(name)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==h, name
    inventory.append(f'| `{p.as_posix()}` | `{h}` |')
doc='''# V48: pianificazione, produzione e priorità PASS

Checkpoint 2026-09-08. Riferimento pubblicato: submission Kaggle **56101593**,
`submission/submission_codex_e18_770_v48_external.py`.
SHA-256: `57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`.
La policy rimane congelata. La prossima versione deve affrontare prima di tutto
il disallineamento tra capacità della manodopera e lavoro biologico eseguibile.
Ambito: **770**; 662 e altre topologie restano rinviate.

## Evidenza e limiti

Nei casi locali V48, D15–D25: PASS medi 28,79 e MOVE 150,24; nel nuovo corpus
Subin di cinque replay: PASS 6,91 e MOVE 111. Il corpus Subin comprende quattro
770 e un 10-7-0: non è un confronto causale a parità di partita o topologia.
Le medie non spiegano da sole i picchi. Il difetto PASS non è risolto.
V48 locale: 6/6 vittorie su V4D, seed di sviluppo già riutilizzati.
Prima coorte esterna congelata: 5/8 vittorie, rating osservato 822,1; non prova
superiorità rispetto a V29. Rating e numero di replay non sono aggiornati in tempo reale.

Il registro `experiments/e18/reports/common/E18_TOP770_BENCHMARK_ROTATION_REGISTER_IT.md`
è obbligatorio: tutti i dodici nuovi autori sono esposti; Top770-003 è consumato
nel ciclo V48. Non usare questi replay come holdout della prossima versione.

## Prossima versione: piano di lavoro e gate

1. Ricostruire ogni PASS per persona, giorno e ora, iniziando da D12–D13 e
   dai picchi successivi. Registrare posizione, capacità residua, assegnazione,
   lavori biologici dovuti, candidati scartati e motivo del vincolo.
2. Distinguere attesa biologica senza lavoro utile, sovracapacità assunta,
   lavoro utile irraggiungibile entro la scadenza, risorse mancanti, prenotazioni
   o priorità che bloccano un lavoro fattibile. Finché non c'è prova, causa ignota.
3. Collegare il calendario semina–maturazione–raccolta–successione alle ore
   necessarie di WATER, FEED, CARE, raccolta e trasferimento. Dimensionare le
   persone prima dell'espansione; verificare carico previsto e realizzato.
4. Proteggere continuità delle colture, rese, servizi animali, cassa e scadenze;
   assegnare lavoro locale utile prima del PASS. La casualità non sostituisce
   un piano fattibile. Non abbassare PASS producendo MOVE o WATER inutili.
5. Confrontare contro V48 congelata con stessi seed/posti per la diagnosi,
   poi seed nuovi e avversari non esposti per la validazione. Riportare PASS
   assoluti, quota sulle azioni, per persona, per causa, picchi e fasi del mese.
   La promozione richiede riduzione dei PASS evitabili senza regressioni
   sistematiche di cassa, perdite biologiche e copertura dei servizi.

Questo è un protocollo da implementare e verificare, non una correzione già validata.

## Catena effettiva del runtime

Il builder parte da `daily_route_scheduler_770_v48.py`, visita le dipendenze
ImportFrom e incorpora 16 moduli più due sorgenti base. Non tutti i file V18–V47
presenti nella directory sono dipendenze della submission V48.

- `biological_plan_770_v48.py`: piano biologico.
- `daily_routes_770_v48.py`: lavori e percorsi giornalieri.
- `daily_route_dispatch_770_v48.py`: esecuzione e guardie.
- `daily_route_scheduler_770_v48.py`: inserimento dei lavori nel piano.
- `portfolio_workforce_v16.py` e `portfolio_scheduler_v16.py`: manodopera e scheduling ereditati.
- Moduli portfolio V14: successione, esecuzione, governo, batch, concorrenza,
  logistica, piano giornaliero, limiti e chiusura; `productive_continuity.py`.
- Core parametrico `submission_codex_e19_control_770_v2.py` e avvio assistito
  `submission_codex_e18_770_assisted_start_v1_candidate.py`.

Elenco completo, verificato contro il manifest della pubblicazione:

| Sorgente dalla radice repository | SHA-256 |
|---|---|
'''+ '\n'.join(inventory)+'''

## Produzione, test e analisi

Percorsi tools seguenti relativi a `docs/model_specs/codex/e19/tools/`.

| Passo | File / input |
|---|---|
| Bundle standalone | `build_v48_submission.py` |
| Benchmark locale congelato | `run_daily_routes_770_v48.py` |
| Parità standalone | `run_v48_external_parity.py` |
| Audit biologico | `crop_lifecycle_audit_v48.py`, `run_lifecycle_audit_v48.py` |
| Diagnosi acqua residua | `run_residual_water_diagnostic_v48.py` |
| Report confronto versioni | `build_productive_water_770_report.py` |
| KPI condivisi | `build_assisted_complete_kpi.py`, `complete_kpi_template.html`, `build_succession_routes_770_report.py` |
| Nuovi Top | `analyze_new_top_v48.py`, `summarize_new_top_v48.py`, `build_new_top_v48_report.py` |
| Coorti Top | `../artifacts/derived/new_top_cohorts.json` |
| Test | `docs/model_specs/codex/e19/tests/test_productive_water_v48.py`, `tests/test_crop_lifecycle_audit_v48.py` dalla radice |

Gli audit Top dipendono anche da
`docs/model_specs/codex/e18/tools/build_e18_26_jesse_770_d20_trajectories.py`,
`build_e18_26_jesse_770_d30_closure.py` nella stessa directory e
`experiments/e18/tools/common/replay_daily_operational_kpi.py`.
Il generatore KPI storico E18 è `docs/model_specs/codex/e18/tools/build_e18_27_top770_complete_kpi.py`.

Eseguire dalla radice con `.venv/Scripts/python.exe`, nell'ordine analizzatore,
riepilogo fasi, builder report per rigenerare l'analisi Top. I replay grezzi
e i run locali devono essere disponibili: un clone Git da solo non li contiene.
Per il bundle usare il builder e verificare l'hash pubblicato; la ricevuta di
pubblicazione è separata dal build e non autorizza una nuova submission.

## Provenance e conservazione

Manifest e ricevuta: `docs/model_specs/codex/e19/artifacts/derived/`
`v48_external_manifest.json`, `v48_external_publication_receipt.json`.
Prima coorte: `v48_external_20260908/first_cohort.json` nella stessa directory.
Analisi Top: `docs/model_specs/codex/e19/reports/new_top_v48_20260908/`:
`census.json`, `profiles.json`, `cohorts.json`, `phase_summary.json`, `manifest.json`
e quattro report completi D01–D30.
L'inventario `docs/foundation/evidence/LOCAL_ARTIFACTS_20260908.json` elenca i
file voluminosi conservati localmente, con hash e dimensione. Per trasferire
gli esperimenti a un altro computer occorre trasferire anche tali file.
Le ricette originarie sono archiviate in `tools/session_archive_20260908/`.

## Semantica dei KPI biologici

L'audit V48 distingue 20 eventi con prodotto detenuto o produzione futura
da due eventi su fragola esaurita e vuota dopo l'ultima raccolta. Irrigare
quest'ultima avrebbe soltanto rinviato WEED: non è un recupero produttivo.
I vecchi conteggi di mortalità non riclassificati non sono direttamente
comparabili. Separare piante presenti, produttive, esaurite, stock perso,
infestanti e servizio necessario. Il numero di WATER da solo non misura copertura.
'''
write(Path('docs/foundation/V48_PLANNING_AND_BUILD_IT.md'),doc)
for p,body in [
 (Path('docs/foundation/ontology/ONTOLOGY_C2_1.md'), 'Distinguere capacità disponibile, lavoro biologico dovuto, lavoro fattibile e attesa. PASS è un esito osservabile, non prova di assenza di lavoro. Piante produttive, esaurite e prodotto detenuto sono concetti distinti. Le categorie diagnostiche di policy non sono nuove regole dell’engine.'),
 (Path('docs/foundation/state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md'), 'Gli audit devono ricostruire azione e successivo refresh nella sequenza dell’engine: raccolta finale, esaurimento, decadimento e perdita idrica non sono equivalenti. Il calendario previsto dal planner va confrontato con le transizioni effettive; una previsione non è un evento osservato.'),
 (Path('docs/foundation/feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md'), 'Telemetria richiesta per il prossimo modello: PASS per persona/ora e motivo verificato, lavoro dovuto/fattibile/scartato, tempo di servizio e viaggio, carico previsto/realizzato, copertura dei servizi e perdite produttive. Le previsioni usano solo stato e regole disponibili al decision time; i replay futuri sono esclusivamente evidenza offline. Queste feature diagnostiche sono proposte, non tutte implementate.')]:
    append(p,body+'\n\nPianificazione e inventario downstream: [V48 e priorità PASS](../V48_PLANNING_AND_BUILD_IT.md). Nessuna modifica alle costanti dell’engine; supplemento operativo alla baseline riconciliata.')
p=Path('docs/foundation/FOUNDATION_C2_1_MANIFEST.md')
s=p.read_text(encoding='utf-8')
import re
for rel in ['ontology/ONTOLOGY_C2_1.md','state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md','feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md']:
    h=hashlib.sha256((p.parent/rel).read_bytes()).hexdigest().upper()
    s=re.sub(r'(`'+re.escape(rel)+r'` \| `)[A-F0-9]+',lambda m:m[1]+h,s)
s=s.replace('La revisione Foundation post-3Q è chiusa. La sequenza sperimentale riprende dal primo esperimento successivo a E16, normalmente E17.', 'La baseline post-3Q resta riconciliata. Stato operativo al 2026-09-08: V48 pubblicata; prossima versione 770 dedicata ai PASS evitabili. Gli hash sopra includono il supplemento operativo del 8 settembre, non attestano una nuova revisione incrociata.')
write(p,s)
append(p,'Catena completa e protocollo: [V48 e priorità PASS](V48_PLANNING_AND_BUILD_IT.md). Le baseline C1/C2 e i verbali storici rimangono congelati.')
for path in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md','docs/model_specs/codex/README.md','docs/model_specs/codex/e19/MODEL_SPEC_CODEX_E19_PARAMETRIC_VALIDATION_DRAFT.md','README.md']:
    p=Path(path)
    import os
    link=os.path.relpath('docs/foundation/V48_PLANNING_AND_BUILD_IT.md',p.parent).replace('\\','/')
    text=f'## Checkpoint operativo 2026-09-08: V48 e PASS\n\n**Priorità assoluta della prossima versione: ridurre i PASS evitabili attraverso la pianificazione biologica e della manodopera, solo 770.** V48 pubblicata (56101593) resta congelata; nessuna nuova variante o pubblicazione in questo checkpoint.\n\n[Stato, piano, inventario completo dei sorgenti e riproduzione]({link}). I checkpoint precedenti sono storici; i nuovi Top sono ormai esposti e non costituiscono holdout.\n\n'
    s=p.read_text(encoding='utf-8'); first,sep,rest=s.partition('\n')
    write(p,first+'\n\n'+text+rest)

# Exact exclusions: retain evidence on disk rather than upload gigabytes of ledgers.
paths=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines()
local=[]
for name in paths:
    p=Path(name)
    if '/artifacts/derived/' in name and p.suffix=='.json' and p.stat().st_size>1_000_000:
        local.append(dict(path=name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),storage='local-preserved; copy this path to restore on another checkout'))
write(Path('docs/foundation/evidence/LOCAL_ARTIFACTS_20260908.json'),json.dumps(local,indent=2))
p=Path('.gitignore')
write(p,p.read_text(encoding='utf-8')+'\n# Local forensic ledgers; exact catalog: docs/foundation/evidence/LOCAL_ARTIFACTS_20260908.json\n.ruff_cache/\n'+''.join('/'+x['path']+'\n' for x in local))
print('Documented sources:',len(inventory),'local evidence files:',len(local),'bytes:',sum(x['bytes'] for x in local))
