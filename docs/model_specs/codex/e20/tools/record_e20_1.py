"""Record the verified result and preserve the previous project handoff verbatim."""
import json
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'

def main():
    decision=json.loads((BASE/'reports/e20_1/DECISION.json').read_text())
    tournament=json.loads((BASE/'reports/e20_1_confirmation/data.json').read_text())
    d,c=decision['development'],decision['confirmation']
    archive=ROOT/'docs/history/e20_1_before_20260910';archive.mkdir(parents=True,exist_ok=True)
    for name in ['PROJECT_STATE.md','NEW_SESSION.md']:
        if not (archive/name).exists():shutil.copyfile(ROOT/'docs'/name,archive/name)
    def f(n):return f'{n:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
    lines=['# Stato del progetto — E20.1, revisione del pianificatore','',
        f"Lavoro del 2026-09-10 concluso. **{decision['status']}.** Nessuna nuova pubblicazione Kaggle. La candidata è E20v28, target 7–7–2: percorsi con tile lontani inseriti per primi a parità di urgenza e filtro dei CARE senza incremento produttivo possibile.",'',
        f"Sviluppo: 10 seed già noti, entrambi i ruoli; +{f(d['delta_percent_vs_E19'])}% rispetto a E19, {d['positive_seeds_vs_E19']}/10 seed positivi, stress {f(d['stress'])} per partita, zero perdite animali.",'',
        f"Conferma indipendente: 7 nuovi seed, 42 partite tra E18/E19/E20.1. Contro E18, delta E20.1−E19 {f(c['delta_percent_vs_E19'])}%, {c['positive_seeds_vs_E19']}/7 seed positivi, stress {f(c['stress'])}, perdite animali {c['animal_losses']}. Il risultato di sviluppo non sostituisce questa verifica.",'',
        '| Modello | Vittorie / partite | Cassa media torneo |','|---|---:|---:|']
    for m,v in tournament['summary'].items():lines.append(f"| {m} | {v['wins']}/{v['matches']} | {f(v['mean_cash'])} |")
    lines+=['','## Artefatti e ripresa','',
        '- [Report finale E20.1](model_specs/codex/e20/reports/e20_1/REPORT.html).',
        '- [Torneo e 22 KPI](model_specs/codex/e20/reports/e20_1_confirmation/REPORT.html).',
        '- [Specifica](model_specs/codex/e20/E20_1_SPEC.md) e [protocollo](model_specs/codex/e20/E20_1_PROTOCOL.json).',
        '- [Decisione verificata](model_specs/codex/e20/reports/e20_1/DECISION.json) e [verifica delle 42 partite](model_specs/codex/e20/artifacts/E20_1_CONFIRMATION_VERIFICATION.json).',
        '- [Bundle E20.1](../submission/submission_codex_e20_772_e20v28_candidate.py).',
        '- [Controllo 770 con lo stesso pianificatore](model_specs/codex/e20/reports/e20_1/topology_control/REPORT.html): controllo di ricerca, non nuova versione ufficiale E19.',
        '',f"SHA256 E20.1: `{decision['bundle_sha256']}`. E18 V4D, E19 V48 e la precedente E20v18 restano congelati. Riferimento pubblicato invariato: submission Kaggle 56101593, V48 770.",'',
        'Tutti i 17 seed usati in questa revisione sono ora esposti: non riutilizzarli come holdout dopo modifiche. Il gate è definito prima dei risultati e distingue cassa media, distribuzione per seed e fragilità biologica. Non promuovere una variante soltanto per il migliore seed o per il numero di WATER/PASS.',
        '', 'Su questo portatile usare un solo processo per i confronti ufficiali. Il solo stato finale DONE non basta: entrambi gli agenti devono ricevere 719 chiamate. Cinque tentativi incompleti del torneo e due del controllo 770 sono archiviati in `invalid_under_load`; sono stati ripetuti senza modificare modelli, seed o limiti di gioco. Non includerli nelle medie.',
        '', 'Il lettore dei replay deve ricostruire il campo condiviso `step` anche per il ruolo 1. Le traiettorie standard e i saldi derivano da ledger verificati. I replay compressi restano disponibili localmente e ignorati da Git.',
        '', '[Checkpoint precedente E20v18](history/e20_1_before_20260910/PROJECT_STATE.md).']
    for name in ['PROJECT_STATE.md','NEW_SESSION.md']:(ROOT/'docs'/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    log=ROOT/'docs/EXPERIMENT_LOG.md';title='## E20.1 — 2026-09-10: percorsi, CARE e conferma separata'
    text=log.read_text(encoding='utf-8')
    if title not in text:
        text+='\n\n'+title+'\n\n'+f"Cinque nuove ablation su dieci seed; E20v28 selezionata e congelata dopo il gate appaiato (+{f(d['delta_percent_vs_E19'])}% vs E19). Torneo indipendente di 42 partite: delta appaiato {f(c['delta_percent_vs_E19'])}%, seed positivi {c['positive_seeds_vs_E19']}/7. {decision['status']}. Controllo C770 verificato separatamente; tentativi interrotti sotto carico archiviati e ripetuti in isolamento. Nessuna nuova submission esterna.\n\n[Report finale](model_specs/codex/e20/reports/e20_1/REPORT.html) · [Specifica](model_specs/codex/e20/E20_1_SPEC.md).\n"
        log.write_text(text,encoding='utf-8')
    manifest=ROOT/'submission/submission_codex_e20_772_e20v28_candidate.manifest.json'
    m=json.loads(manifest.read_text());m.update(status='LOCAL_INDEPENDENT_GATE_PASSED' if decision['promoted'] else 'EXPERIMENTAL_INDEPENDENT_GATE_FAILED',
        independent_gate_passed=decision['promoted'],validation_report='docs/model_specs/codex/e20/reports/e20_1/REPORT.html')
    manifest.write_text(json.dumps(m,indent=2)+'\n')
    state=BASE/'reports/e20_1/RUN_STATE.json';s=json.loads(state.read_text());s.update(phase='complete',remaining=[],decision=decision['status']);state.write_text(json.dumps(s,indent=2)+'\n')
    (BASE/'reports/e20_1/topology_control/STATUS.json').write_text(json.dumps({'status':'COMPLETE_VERIFIED','cases':10},indent=2)+'\n')
    print(decision['status'])

if __name__=='__main__':main()
