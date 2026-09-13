"""Descriptive E22 strategy inventory; inherited topology is not a selection rule."""
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/opponent_strategy_20260913'


def main():
    from docs.model_specs.codex.e20.tools.analyze_first_external import profile
    cohort=json.loads((OUT/'COHORT.json').read_text(encoding='utf-8'))
    dest=OUT/'profiles';dest.mkdir(exist_ok=True)
    for g in cohort['games']:
        path=dest/f"{g['episode']}.json"
        if path.exists():continue
        raw=(ROOT/g['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
        r=json.loads(raw);assert g['complete']
        for i,step in enumerate(r['steps']):step[0]['observation']['step']=i
        sides={}
        for side,seat in [('own',g['seat']),('opponent',1-g['seat'])]:
            p=profile(r,seat);assert p['ledger']['cash_parity_errors']==0
            topology=[];maps=[]
            for d in range(1,31):
                farm=r['steps'][d*24-1][seat]['observation']['farms'][seat]
                cells=[dict(x=x,y=y,kind=t['kind'],animal=t.get('animal'),crop=t.get('crop'),planted_day=t.get('planted_day'))
                       for y,row in enumerate(farm['tiles']) for x,t in enumerate(row) if isinstance(t,dict)]
                topology.append([c for c in cells if c['kind'] in ('PASTURE','COOP')])
                maps.append(cells)
            p['topology']=topology;p['maps']=maps
            p['commands']=[json.dumps([s[seat]['action'].get('farmer'),s[seat]['action'].get('hands')],separators=(',',':')) for s in r['steps'][1:]]
            p['opening_command_hash']=hashlib.sha256('\n'.join(p['commands'][:144]).encode()).hexdigest()
            p['land_days']=[d['day'] for d in p['ledger']['daily'] if d['land_cash']>0]
            p['totals']={k:dict(sum((Counter(d[k]) for d in p['ledger']['daily']),Counter()))
                         for k in ['planted','harvested','sold_units','sales_cash','purchase_cash']}
            p['totals'].update({k:sum(d[k] for d in p['ledger']['daily']) for k in ['hire_cash','land_cash','unit_cash_delta']})
            assert abs(3000+sum(p['totals']['sales_cash'].values())-sum(p['totals']['purchase_cash'].values())-p['totals']['hire_cash']-p['totals']['land_cash']+p['totals']['unit_cash_delta']-p['reward'])<0.01
            sides[side]=p
        path.write_text(json.dumps(dict(**g,**sides),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        print('AUDITED',g['episode'],ascii(g['name']),flush=True)


if __name__=='__main__':main()
