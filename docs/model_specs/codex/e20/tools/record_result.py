"""Record final E20 state, preserving the previous shared checkpoint verbatim."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'docs/model_specs/codex/e20'

def main():
    data=json.loads((BASE/'reports/tournament/data.json').read_text())
    verification=json.loads((BASE/'artifacts/TOURNAMENT_VERIFICATION.json').read_text())
    assert verification['complete'] and data['match_count']==42
    qa=json.loads((BASE/'reports/tournament/qa.json').read_text())
    assert len(qa)==2 and all(r['panels']==22 and r['pairings']==3 and not r['errors'] and not r['overflow'] for r in qa)
    gate=json.loads((BASE/'artifacts/ECONOMIC_GATE.json').read_text())
    def fmt(v):return f'{v:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
    matched=data['matched_vs_E18']
    ranking=sorted(data['summary'],key=lambda m:(data['summary'][m]['wins'],data['summary'][m]['mean_cash']),reverse=True)
    lines=['# Stato del progetto — E20 772 e torneo E18/E19/E20','',
        'Lavoro del 2026-09-10: E20 realizzata e congelata; ottimizzazione economica development conclusa; torneo di 42 partite e report dei 22 KPI completati. Nessuna nuova pubblicazione Kaggle. Codex resta l’unica linea di sviluppo attiva.','',
        f"E20v18: 7–7–2, avvio E19 fino a D11, mucca Q2 (4,5) e pecora Q2 (4,6). Sei casi development: cassa media {fmt(gate['E20_mean'])} contro {fmt(gate['E19_mean'])} di E19 (+{fmt(gate['delta_percent'])}%). Parità completa sorgente/standalone; zero errori core e perdite animali nel gate.",'',
        f"Conferma separata sui sette seed del torneo: contro E18, E20 {fmt(matched['E20_mean'])} contro E19 {fmt(matched['E19_mean'])}; delta {fmt(matched['delta_mean'])}, positivo in {matched['positive_cases']}/{matched['cases']} casi. La superiorità development non va estesa automaticamente al torneo o a Kaggle.",'',
        '| Modello | Vittorie / partite | Cassa media torneo |','|---|---:|---:|']
    for m in ranking:
        v=data['summary'][m];lines.append(f"| {m} | {v['wins']}/{v['matches']} | {fmt(v['mean_cash'])} |")
    lines+=['','## Riferimenti','',
        '- [Report finale interattivo](model_specs/codex/e20/reports/tournament/REPORT.html) e [testo](model_specs/codex/e20/reports/tournament/REPORT.md).',
        '- [Specifica E20](model_specs/codex/e20/MODEL_SPEC_CODEX_E20_772.md).',
        '- [Registro delle 23 varianti e gate](model_specs/codex/e20/reports/DEVELOPMENT.md).',
        '- [Verifica delle 42 partite](model_specs/codex/e20/artifacts/TOURNAMENT_VERIFICATION.json).',
        '- [Bundle locale E20](../submission/submission_codex_e20_772_e20v18_candidate.py), hash `'+gate['bundle_sha256']+'`.',
        '- Riferimento pubblicato invariato: V48 770, submission Kaggle 56101593, hash `57e7155e69a4b0db43ccb22295a7172fc4d338999dae6a6e775081b67ecf7743`.',
        '', '## Indicazioni per la ripresa','',
        'Distinguere target e topologie effettive, produzione e incassi, PASS e servizi. La regressione idrica di E20 rispetto a E19 sul development è esplicita nel report; il superamento economico non certifica una maggiore robustezza delle colture.',
        '', 'Tutti i seed development e torneo sono ora esposti. Non riutilizzare il torneo come holdout indipendente dopo ulteriori modifiche. E18/E19 e il bundle E20 restano congelati; eventuali nuove revisioni richiedono nuove versioni e un nuovo campione di conferma.',
        '', 'Riproduzione dalla radice con `.venv/Scripts/python.exe`: runner E20, audit_results.py, verify_gate.py, verify_tournament.py, build_report.py; parametri e seed nel protocollo. I replay compressi sono conservati localmente e ignorati da Git; ledger, manifest e CSV sono tracciati.',
        '', '[Checkpoint precedente V48](history/e20_before_20260910/PROJECT_STATE.md).']
    text='\n'.join(lines)+'\n'
    archive=ROOT/'docs/history/e20_before_20260910';archive.mkdir(parents=True,exist_ok=True)
    for name in ['PROJECT_STATE.md','NEW_SESSION.md']:
        current=ROOT/'docs'/name
        if not (archive/name).exists():(archive/name).write_bytes(current.read_bytes())
        current.write_text(text,encoding='utf-8')
    index=ROOT/'docs/model_specs/codex/README.md'
    marker='## E20 — 7–7–2, 10 settembre 2026'
    if marker not in index.read_text(encoding='utf-8'):
        original=index.read_text(encoding='utf-8')
        head,tail=original.split('\n',1)
        addition='\n\n'+marker+'\n\n[Specifica E20](e20/MODEL_SPEC_CODEX_E20_772.md), [sviluppo](e20/reports/DEVELOPMENT.md) e [torneo finale con 22 KPI](e20/reports/tournament/REPORT.html). E20 è una candidata locale congelata; il riferimento pubblicato V48 resta invariato. Il report distingue il gate development dalla conferma su sette seed separati.\n'
        index.write_text(head+addition+'\n'+tail,encoding='utf-8')
    log=ROOT/'docs/EXPERIMENT_LOG.md'
    marker='## 2026-09-10 — E20 772, gate economico e torneo a tre'
    if marker not in log.read_text(encoding='utf-8'):
        with log.open('a',encoding='utf-8') as f:f.write('\n'+marker+'\n\n23 varianti esplorate; E20v18 congelata dopo +4,56% matched development su tre seed e due ruoli. Torneo completo di 42 partite su sette seed separati; report dei 22 KPI, ledger e CSV. Nessuna submission esterna. [Report](model_specs/codex/e20/reports/tournament/REPORT.md) · [Stato](PROJECT_STATE.md).\n')
    print(ROOT/'docs/PROJECT_STATE.md')

if __name__=='__main__':main()
