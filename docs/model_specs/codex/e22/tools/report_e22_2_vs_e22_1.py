"""Name the selected frozen policies and reissue their verified paired comparison."""
import hashlib
import json
import re
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'docs/model_specs/codex/e22/reports/q0_8c9s_v1'
OUT = SOURCE.parent / 'e22_2_vs_e22_1'
FILES = {
    'E22.1': ('submission_codex_e22_s56165462_observed_v1.py', 'submission_codex_e22_1_pollai.py'),
    'E22.2': ('submission_codex_e22_q0_8c9s_internal_v1.py', 'submission_codex_e22_2_pascoli.py'),
}

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def relabel(text):
    text = text.replace('8C9S v1', 'E22.2').replace('8C9S', 'E22.2')
    text = text.replace('mix E22.2', 'mix 8C9S di E22.2')
    return re.sub(r'\bE22\b(?!\.)', 'E22.1', text)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    protocol = json.loads((SOURCE/'PROTOCOL.json').read_text(encoding='utf-8'))
    rows = json.loads((SOURCE/'RESULTS.json').read_text(encoding='utf-8'))
    assert {(r['seed'],r['seat']) for r in rows} == {(seed,seat) for seed in range(180911301,180911308) for seat in (0,1)}
    manifest = {}
    for model, (old_name,new_name) in FILES.items():
        old,new = ROOT/'submission'/old_name, ROOT/'submission'/new_name
        key = 'baseline' if model=='E22.1' else 'candidate'
        assert digest(old) == protocol['hashes'][key]
        if new.exists(): assert new.read_bytes() == old.read_bytes()
        else: new.write_bytes(old.read_bytes())
        manifest[model] = dict(bundle=str(new.relative_to(ROOT)), historical_bundle=str(old.relative_to(ROOT)),
                               sha256=digest(new), byte_identical=True,
                               mix={'COW':8,'SHEEP':6,'GOOSE':3} if model=='E22.1' else {'COW':8,'SHEEP':9},
                               status='published' if model=='E22.1' else 'internal',
                               submission=56206528 if model=='E22.1' else None)
    for r in rows:
        assert r['hashes'] == protocol['hashes']
        assert r['checks']['baseline_plan_parity']==719 and r['checks']['escapes']==0
        assert all(l['cash_parity_errors']==0 for l in r['ledgers'])
    for name in ['RESULTS.json','SUMMARY.json','VERIFICATION.json']:
        (OUT/name).write_bytes((SOURCE/name).read_bytes())
    protocol.update(models=manifest, data_reused=True, source_report=str(SOURCE.relative_to(ROOT)),
                    simulations_for_rename=0, note='E22.2 is original 8C9S v1, not calendar v2. Same code bytes and same 14 actual paired matches; no new simulations or publication.')
    (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    (OUT/'VERSIONS.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    registry = ROOT/'docs/model_specs/codex/e22/VERSIONS.json'
    registry.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    summary=json.loads((SOURCE/'SUMMARY.json').read_text(encoding='utf-8'))[0]
    stats = {model:dict(wins=sum((r['margin']>0 if model=='E22.2' else r['margin']<0) for r in rows),
        mean_cash=mean(r['rewards'][r['seat'] if model=='E22.2' else 1-r['seat']] for r in rows)) for model in FILES}
    (OUT/'COMPARISON.json').write_text(json.dumps(dict(models=stats,candidate_mean_margin=summary['mean_margin'],
        candidate_median_margin=summary['median_margin'],games=14,paired_seeds=7),indent=2),encoding='utf-8')
    explanation = ('E22.1 identifica E22 pubblicata, submission 56206528, con tre pollai Q0 e tre oche. '
        'E22.2 identifica la variante precedentemente chiamata 8C9S v1: tre pascoli Q0 e tre pecore in (4,1), (3,2), (2,3), mix totale 8 mucche e 9 pecore. '
        'La variante sperimentale con calendario esterno v2 non è E22.2. I nuovi nomi dei bundle sono copie byte per byte dei file verificati. '
        'Il report riutilizza le 14 partite seriali già concluse su 180911301–307 nei due ruoli, previa verifica degli hash: nessuna nuova simulazione è stata necessaria.')
    decision = ('E22.1 resta il riferimento pubblicato. E22.2 è la versione scelta per la configurazione con tre pascoli, ma resta interna: '
        f"vince 4/14 partite (due seed su sette), con margine medio +{summary['mean_margin']:.2f} e mediana {summary['median_margin']:.0f}. "
        'Il piccolo vantaggio medio non è regolare tra i seed. Nessuna pubblicazione e nessun uso dei seed di conferma 180912401–407.')
    (OUT/'DECISION.json').write_text(json.dumps(dict(decision=decision,selected_pollai='E22.1',selected_pascoli='E22.2',
        published_submission=56206528,confirmation_used=False),indent=2),encoding='utf-8')
    table = '| Versione | Q0 | Mix totale | Vittorie | Cassa media |\n|---|---|---|---:|---:|\n'
    for model in FILES:
        table += f"| {model} | {'3 pollai, 3 oche' if model=='E22.1' else '3 pascoli, 3 pecore'} | {'8C6S3G' if model=='E22.1' else '8C9S'} | {stats[model]['wins']}/14 | {stats[model]['mean_cash']:.2f} |\n"
    report=relabel((SOURCE/'REPORT.md').read_text(encoding='utf-8'))
    report=report.replace('# E22.1 · tre pascoli Q0, E22.2','# E22.2 contro E22.1',1)
    report=report.replace('\n\n','\n\n'+explanation+'\n\n'+table+'\n'+decision+'\n\n',1)
    (OUT/'REPORT.md').write_text(report,encoding='utf-8')
    (OUT/'DAILY_KPI.csv').write_text(relabel((SOURCE/'DAILY_KPI.csv').read_text(encoding='utf-8')),encoding='utf-8')
    page=relabel((SOURCE/'REPORT.html').read_text(encoding='utf-8'))
    page=page.replace('<title>E22.1 Q0 E22.2</title>','<title>E22.2 contro E22.1</title>')
    page=page.replace('<h1>E22.1 · tre pascoli Q0 · E22.2</h1>', '<h1>E22.2 contro E22.1</h1><p>'+explanation+'</p><p><b>Scelta:</b> '+decision+'</p>')
    cards='<section><h2>Versioni scelte</h2><table><tr><th>Versione</th><th>Configurazione</th><th>Vittorie</th><th>Cassa media</th></tr>'
    for model in FILES:
        cards+=f"<tr><td><b>{model}</b></td><td>{'3 pollai Q0 · 8 mucche, 6 pecore, 3 oche' if model=='E22.1' else '3 pascoli Q0 · 8 mucche, 9 pecore'}</td><td>{stats[model]['wins']}/14</td><td>{stats[model]['mean_cash']:,.2f}</td></tr>"
    cards+='</table><p><a href="VERSIONS.json">Identità e hash dei bundle</a> · <a href="COMPARISON.json">Dati di confronto</a></p></section>'
    page=page.replace('<label>Partita',cards+'<label>Partita',1)
    page=page.replace('</style>','table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:12px;border-bottom:1px solid #ddd}</style>',1)
    (OUT/'REPORT.html').write_text(page,encoding='utf-8')
    (OUT/'REISSUE_VERIFICATION.json').write_text(json.dumps(dict(source_hashes=protocol['hashes'],
        aliases_byte_identical=True,reused_games=14,new_simulations=0,paired_seeds=7,
        side_cash_transitions_verified=14*2*719,cash_errors=0,candidate_escapes=0),indent=2),encoding='utf-8')
    print(json.dumps(dict(models=stats,mean_margin=summary['mean_margin'],median_margin=summary['median_margin'],report=str(OUT/'REPORT.html'))),flush=True)

if __name__=='__main__': main()
