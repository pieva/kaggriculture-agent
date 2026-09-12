"""Add common-opponent diagnostics and a human-readable submission decision."""
import csv,hashlib,json
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];BASE=ROOT/'docs/model_specs/codex/e20'
OUT=BASE/'reports/e20_2_confirmation';ART=BASE/'artifacts/e20_2_confirmation'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    decision=read(OUT/'DECISION.json');protocol=read(BASE/'E20_2_CONFIRMATION_PROTOCOL.json')
    cases=[read(p) for p in ART.glob('*.kpi.json')];assert len(cases)==42
    matched=[]
    for seed in protocol['seeds']:
        values={m:mean(s['reward'] for c in cases if c['seed']==seed and {x['name'] for x in c['sides']}=={m,'E18'} for s in c['sides'] if s['name']==m) for m in ['E19','E20.2']}
        matched.append(dict(seed=seed,**values,delta=values['E20.2']-values['E19']))
    decision['common_opponent_E18']=dict(per_seed=matched,mean_delta=mean(x['delta'] for x in matched),positive_seeds=sum(x['delta']>0 for x in matched))
    (OUT/'DECISION.json').write_text(json.dumps(decision,indent=2)+'\n',encoding='utf-8')
    lines=['# E20.2: decisione sulla verifica esterna','', '**'+decision['decision']+'**. Nessuna submission eseguita.', '', '42 partite complete, sette seed indipendenti dallo sviluppo, tutti gli accoppiamenti e ruoli. E20.2 congelata prima dei risultati. La soglia interna richiede margine positivo contro ciascun riferimento in almeno 5/7 seed, media positiva e nessun aumento di stress colture o fughe medi.', '', '| Riferimento | Margine medio E20.2 | Seed positivi | Gate |','|---|---:|---:|---|']
    for name,v in decision['comparisons'].items():lines.append(f"| {name} | {v['mean_margin']:+.1f} | {v['positive_seeds']}/7 | {v['passed']} |")
    common=decision['common_opponent_E18']
    lines+=['',f"Contro lo stesso E18, E20.2 meno E19: {common['mean_delta']:+.1f} di cassa media; {common['positive_seeds']}/7 seed positivi. È una diagnosi aggiuntiva, non sostituisce le soglie congelate.", '', '| Seed | E19 contro E18 | E20.2 contro E18 | Differenza |','|---|---:|---:|---:|']
    for v in matched:lines.append(f"| {v['seed']} | {v['E19']:.1f} | {v['E20.2']:.1f} | {v['delta']:+.1f} |")
    lines+=['', '[Torneo e 22 KPI](REPORT.html) · [Protocollo](../../E20_2_CONFIRMATION_PROTOCOL.json) · [Decisione completa](DECISION.json)', '', 'I ruoli sono mediati entro seed, non trattati come campioni indipendenti. Le simulazioni locali e i tempi misurati non certificano il runtime o il punteggio Kaggle. I sette seed sono ora esposti. Nessuna variante è stata ottimizzata su questi risultati.']
    (OUT/'SUBMISSION_DECISION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    data=read(OUT/'data.json');assert len(data['fields'])==22 and data['match_count']==42 and len(data['pairings'])==3
    # Preserve opponent identity: seed/model/seat alone is not unique in a round robin.
    with (OUT/'daily_kpi.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['seed','model','opponent','seat','day']+[x['key'] for x in data['fields']]+['unlocked_tiles']);w.writeheader()
        for c in cases:
            for i,s in enumerate(c['sides']):
                for day,row in enumerate(s['kpi'],1):
                    w.writerow(dict(seed=c['seed'],model=s['name'],opponent=c['sides'][1-i]['name'],seat=s['seat'],day=day,**{x['key']:row[x['key']] for x in data['fields']},unlocked_tiles=row['unlocked_tiles']))
    for pair in data['pairings']:
        assert pair['matches']==14
        for series in pair['series'].values():
            assert all(len(series[f['key']])==30 for f in data['fields'])
    manifest=read(OUT/'manifest.json')
    for p in [Path(__file__),OUT/'DECISION.json',OUT/'SUBMISSION_DECISION.md',OUT/'REPORT.html',OUT/'data.json',OUT/'daily_kpi.csv',BASE/'tools/confirm_e20_2.py']:
        manifest['sources'][p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    manifest['static_validation']='22 metrics, 30 days, 3 pairings, 14 games each; PASS'
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('\n'.join(lines))
if __name__=='__main__':main()
