"""Separate within-game animal replacement from between-game portfolio selection."""
import hashlib,json,sys
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
BASE=ROOT/'docs/model_specs/codex/e22/reports/top_trigger_pilot_20260913'
OUT=ROOT/'docs/model_specs/codex/e22/reports/kiki_rotation_20260913'
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit
from analyze_trigger_pilot import features,counts

def main():
    OUT.mkdir(exist_ok=True)
    games=[g for g in json.loads((BASE/'COHORT.json').read_text(encoding='utf-8'))['games'] if g['name']=='kiki yi2']
    games += [g for g in json.loads((BASE/'YARN_REPLICATION.json').read_text(encoding='utf-8'))['rows'] if g['name']=='kiki yi2']
    assert len({g['episode'] for g in games})==len(games)==8
    rows=[]
    for g in games:
        raw=(ROOT/g['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
        r=json.loads(raw);seat=g['seat'];history=defaultdict(list);events=[];purchases=[];removals=[];daily=[];crop_history=defaultdict(list)
        for i in range(719):
            b=r['steps'][i][seat]['observation'];a=r['steps'][i+1][seat]['observation'];action=r['steps'][i+1][seat]['action']
            for order in action.get('market',[]):
                if order and order[0]=='BUY_ANIMAL':purchases.append(dict(step=i,order=order,features=features(r,i,seat)))
            for y,row in enumerate(b['farms'][seat]['tiles']):
                for x,t in enumerate(row):
                    old=t if isinstance(t,dict) else {};t2=a['farms'][seat]['tiles'][y][x];new=t2 if isinstance(t2,dict) else {}
                    if old.get('animal') and old.get('animal')!=new.get('animal'):
                        removals.append(dict(day=b['day']+1,hour=b['hour']+1,cell=[x,y],species=old['animal'],unfed=old.get('consecutive_unfed',0),fed=old.get('fed_today'),next_species=new.get('animal')))
                    if new.get('animal') and (new.get('animal'),new.get('placed_day'))!=(old.get('animal'),old.get('placed_day')):
                        e=dict(day=b['day']+1,hour=b['hour']+1,cell=[x,y],species=new['animal'],previous_species=history[(x,y)][-1]['species'] if history[(x,y)] else None,features=features(r,i,seat))
                        history[(x,y)].append(e);events.append(e)
                    if new.get('crop') and (new.get('crop'),new.get('planted_day'))!=(old.get('crop'),old.get('planted_day')):
                        crop_history[(x,y)].append(dict(day=b['day']+1,species=new['crop']))
        for day in range(1,31):
            o=r['steps'][day*24-1][seat]['observation'];farm=o['farms'][seat]
            structures=[[x,y,t['kind']] for y,row in enumerate(farm['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('kind') in ['PASTURE','COOP']]
            daily.append(dict(day=day,own=counts(farm),opponent=counts(o['farms'][1-seat]),prices=o['market']['prices'],shops=dict(Counter(o['town']['unlocked_shops'])),cash=farm['money'],structures=structures))
        ledger=audit(r,seat)
        opponent=audit(r,1-seat)
        result=dict(episode=g['episode'],seat=seat,path=g['path'],sha256=g['sha256'],purchases=purchases,placements=events,removals=removals,replacements=[e for e in events if e['previous_species'] and e['previous_species']!=e['species']],crop_histories=[dict(cell=list(cell),sequence=seq) for cell,seq in crop_history.items()],daily=daily,ledger=ledger,opponent_ledger=opponent)
        rows.append(result)
        print(g['episode'],'replacements',len(result['replacements']),'removals',len(removals),'buys',[(p['features']['day'],p['order']) for p in purchases],flush=True)
    (OUT/'ANALYSIS.json').write_text(json.dumps(dict(submission=56137379,sample='5 exploratory + 3 already-used replication replays; no new holdout',rows=rows),ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
