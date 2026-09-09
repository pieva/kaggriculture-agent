"""Seal paired development/validation, runtime and source parity evidence."""
import gzip,hashlib,html,importlib,json,os,sys
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.analyze_pass_reduction_v51 import analyze,OUT

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(headers,rows):
    return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'

def plot(split,part):
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'scratch/v51/mplconfig'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels=[f"{c['seed']}\nposto {c['seat']}" for c in part['cases']]
    fig,axes=plt.subplots(3,1,figsize=(10,8),layout='constrained')
    for ax,key in zip(axes,['cash','pass_count','move']):
        values=[c['delta'][key] for c in part['cases']]
        bars=ax.bar(range(len(values)),values,color='#087d85')
        ax.axhline(0,color='#334450',linewidth=.8);ax.set_ylabel('Δ '+key)
        ax.bar_label(bars,fmt='%+.0f',padding=3)
        ax.margins(y=.25);ax.set_xticks(range(len(labels)),labels)
        ax.spines[['top','right']].set_visible(False)
    fig.suptitle('V51C − V49F · '+('sviluppo' if split=='development' else 'validazione su seed nuovi'))
    fig.savefig(OUT/f'{split}_comparison.svg')
    fig.savefig(ROOT/f'scratch/v51/{split}_comparison.png',dpi=120)
    plt.close(fig)
    return f'<img style="width:100%;height:auto" src="{split}_comparison.svg" alt="Differenze cash, PASS e MOVE per ciascun caso">'

def main():
    r=analyze('v51c');m=json.loads((OUT/'candidate_manifest.json').read_text())
    assert sha(ROOT/m['output'])==m['sha256']
    for p,h in m['sources'].items():assert sha(ROOT/p)==h,p
    frozen=[]
    for path in [ROOT/'docs/model_specs/codex/e19/artifacts/derived/v48_external_manifest.json',OUT.parent/'pass_reduction_v49_20260909/candidate_f_manifest.json',OUT.parent/'pass_reduction_v50/candidate_manifest.json']:
        baseline=json.loads(path.read_text())
        assert sha(ROOT/baseline['output'])==baseline['sha256']
        for p,h in baseline['sources'].items():assert sha(ROOT/p)==h,p
        frozen.append(baseline['sha256'])
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    expected=json.loads((ROOT/'docs/foundation/ENGINE_SOURCE_MANIFEST.json').read_text())['files']
    for name,h in expected.items():assert sha(Path(engine.__file__).parent/name)==h,name
    tests=ROOT/'scratch/v51/tests.log'
    assert '7 passed' in tests.read_text()
    scope=[]
    for split,part in r['partitions'].items():
        for case in part['cases']:
            seed,seat=case['seed'],case['seat']
            base=OUT.parent/'pass_reduction_v49_20260909' if split=='development' else OUT
            a=json.loads((base/f'{split}_v49f_{seed}_{seat}.json').read_text())
            b=json.loads((OUT/f'{split}_v51c_{seed}_{seat}.json').read_text())
            for p,h in b['candidate_sources'].items():assert sha(ROOT/'docs/model_specs/codex/e19/tools'/p)==h,p
            ra=json.load(gzip.open(ROOT/a['details'],'rt'))['replay']
            rb=json.load(gzip.open(ROOT/b['details'],'rt'))['replay']
            assert all(ra['steps'][i][seat]['action']==rb['steps'][i][seat]['action'] for i in range(1,673))
            scope.append(dict(split=split,seed=seed,seat=seat,d1_d28_identical=True,raw_sha256=sha(ROOT/b['details'])))
    runtimes=[json.loads(p.read_text()) for p in sorted(OUT.glob('runtime_v51c_*.json'))]
    parity=[json.loads(p.read_text()) for p in sorted(OUT.glob('parity_v51c_*.json'))]
    ready=r['status']=='LOCAL_CANDIDATE_ONLY' and len(runtimes)==2 and all(p['passed'] and p.get('recorded_action_parity') and p['bundle_sha256']==m['sha256'] for p in runtimes) and bool(parity) and all(p['mismatches']==0 and p['bundle_sha256']==m['sha256'] for p in parity)
    status='CANDIDATO LOCALE VERIFICATO — NON PUBBLICATO' if ready else r['status']+' — NON PUBBLICATO'
    sections=[]
    for split,part in r['partitions'].items():
        rows=[]
        for c in part['cases']:
            d=c['delta'];rows.append([c['seed'],c['seat'],*[f'{d[k]:+.2f}' for k in ['cash','pass_count','move','FEED','HARVEST']]])
        sections.append('<h2>'+('Sviluppo' if split=='development' else 'Validazione su seed nuovi')+'</h2>'+table(['Seed','Posto','Δ cash','Δ PASS','Δ MOVE','Δ FEED','Δ HARVEST'],rows))
        sections.append(table(['Metrica','Differenza media'],[[k,f'{v:+.4f}'] for k,v in part['mean_delta'].items()]))
        sections.append(table(['Criterio','Esito'],[[k,'PASS' if v else 'FAIL'] for k,v in part['gates'].items()]))
        sections.append(plot(split,part))
    sections.append('<h2>Runtime standard locale</h2>'+table(['Seed','Posto','Chiamate','Massimo (s)','Overage (s)','Esito'],[[p['seed'],p['seat'],p['calls'],f"{p['max_seconds']:.2f}",f"{p['overage']:.2f}",'PASS' if p['passed'] else 'FAIL'] for p in runtimes]))
    sections.append('<p>actTimeout=1 con budget di overage del motore: il massimo di una chiamata può superare un secondo. Prove seriali locali; nessuna equivalenza garantita con hardware Kaggle.</p>')
    text='''<!doctype html><html lang="it"><meta charset="utf-8"><title>V51 — verifica locale</title><style>body{font:17px/1.6 system-ui;max-width:1050px;margin:40px auto;padding:0 24px;color:#24323d}h1,h2{line-height:1.2}table{border-collapse:collapse;width:100%;margin:24px 0}td,th{text-align:right;padding:9px;border-bottom:1px solid #d8e0e5}td:first-child,th:first-child{text-align:left}th{background:#edf3f6}.status{padding:16px;background:#edf3f6;font-weight:bold}a{color:#006b7a}code{overflow-wrap:anywhere}</style><h1>V51C — percorsi eseguiti come pianificati</h1>'''
    text+='<p class="status">'+status+'</p><p>Confronto con V49F congelata. Il giorno 29 i servizi necessari sono impegnati in percorsi completi, con riserve di risorse, irrigazione prima della raccolta e assunzioni dimensionate sulle visite residue. I giorni 1–28 restano identici nei replay di sviluppo verificati.</p>'
    if 'validation' in r['partitions']:
        d=r['partitions']['validation']['mean_delta']
        text+=f'<p><strong>Validazione, differenze medie: cash {d["cash"]:+.2f}, PASS {d["pass_count"]:+.2f}, MOVE {d["move"]:+.2f}.</strong> Il seed 260909201 peggiora su cash e PASS; il beneficio medio dipende dal miglioramento sul secondo seed. I criteri restano quelli fissati prima della validazione.</p>'
    text+=''.join(sections)
    text+='<h2>Interpretazione e limiti</h2><p>A è stata scartata per la perdita di irrigazioni prima della raccolta; B per l’aumento dei PASS. C corregge entrambi i problemi. I due posti e i seed possono produrre traiettorie correlate: questi confronti non sono una stima statistica indipendente né dimostrano un miglioramento del punteggio pubblico. Il packing è greedy e non dimostra ottimalità. Le attività facoltative restano affidate al controllore ereditato.</p>'
    text+='<p>Le simulazioni comparative usano actTimeout=120 per separare la valutazione strategica dal runtime. '+('Il file finale è stato controllato separatamente con il limite standard.' if runtimes else 'Non sono state eseguite prove di runtime standard su V51C: la strategia non è stata promossa.')+' Nessuna submission esterna effettuata.</p><p>SHA256 del bundle: <code>'+m['sha256']+'</code></p>'
    text+='<p><a href="summary_v51c.json">Risultati completi</a> · <a href="candidate_manifest.json">Manifest del candidato</a> · <a href="PROTOCOL_IT.md">Protocollo</a> · <a href="REPRODUCE_IT.md">Riproduzione</a> · <a href="REPORT_V51A_IT.md">Revisione A</a> · <a href="REPORT_V51B_IT.md">Revisione B</a></p></html>'
    (OUT/'REPORT_V51_IT.html').write_text(text,encoding='utf-8')
    class Links(HTMLParser):
        def handle_starttag(self,tag,attrs):
            if tag in {'a','img'}:
                link=dict(attrs).get('href' if tag=='a' else 'src')
                if link and '://' not in link:assert (OUT/link).exists(),link
    Links().feed(text)
    result=dict(status=status,ready=ready,summary_status=r['status'],bundle_sha256=m['sha256'],runtime_cases=len(runtimes),parity_cases=len(parity),tests=7,tests_sha256=sha(tests),frozen_bundles=frozen,engine=expected,scope=scope,local_links_ok=True)
    (OUT/'final_integrity.json').write_text(json.dumps(result,indent=2))
    (OUT/'report_manifest.json').write_text(json.dumps({p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='report_manifest.json'},indent=2))
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
