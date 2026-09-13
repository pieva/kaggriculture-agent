"""Serial, preregistered E20.9 component tests; no publication."""
import json,hashlib,sys,gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools import run_experiment as runner
from docs.model_specs.codex.e20.tools.operational_calendar_v42 import Agent
from docs.model_specs.codex.e20.tools.audit_results import run as audit
BASE=ROOT/'docs/model_specs/codex/e20';STAGE='e20_9_development_b'

def frozen(name,seat):
    p=ROOT/'submission'/('submission_codex_e18_2_capacity_governed_v4d.py' if name=='E18' else 'submission_codex_e20_8_e20v40_calendar_2g.py')
    ns={'__name__':'_frozen'};exec(compile(p.read_text(encoding='utf-8'),str(p),'exec'),ns)
    return ns['create_agent']({'player_position':seat})

def main():
    out=BASE/'reports'/STAGE;out.mkdir(parents=True,exist_ok=True)
    files=[Path(__file__),BASE/'tools/operational_calendar_v42.py',BASE/'tools/operational_calendar_base.py',BASE/'tools/operational_calendar_goose2.py']+list((BASE/'configs/e20v40').glob('*.json'))
    protocol={'seeds':[180911301,180911303],'roles':[0,1],'models':['Tomato','Finance','Reference'],'opponent':'E18 frozen775','stage':STAGE,
      'interventions':'Finance replaces first BUY13/SELL13/BUY13 with BUY13. Tomato adds two crop missions at (3,7),(4,8) from D20 with first harvest >=8 days, late cutoff D21; 1000 current cash admission D19. Same 8C6S2G livestock.',
      'gate':'Technical:719 calls, no unknown commands, expected761/8C6S2G, zero animal escapes, tomato placed/watered/harvested/sold by D30. Economic: report paired cash and margin; no automatic promotion on two exposed seeds.',
      'sources':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    p=out/'PROTOCOL.json'
    if p.exists():assert json.loads(p.read_text())==protocol
    else:p.write_text(json.dumps(protocol,indent=2)+'\n',encoding='utf-8')
    runner.policy=lambda name,seat: Agent({'player_position':seat},tomatoes=name=='Tomato') if name in ['Tomato','Finance'] else frozen(name,seat)
    for model in protocol['models']:
        for seed in protocol['seeds']:
            for seat in protocol['roles']:
                names=[model,'E18'] if seat==0 else ['E18',model]
                m=runner.run((STAGE,*names,seed));assert all(x['calls']==719 for x in m['runtime']),m['runtime']
                p=BASE/'artifacts'/STAGE/f'{names[0]}_{names[1]}_{seed}.json';audit(p)
                k=json.loads(p.with_suffix('.kpi.json').read_text());s=k['sides'][seat]
                print('CHECK',model,seed,seat,'cash',s['reward'],'losses',sum(x['verified_animal_losses'] for x in s['kpi']),
                      'tomato',sum(x['sold_units'].get('TOMATO',0) for x in s['ledger']['daily']),flush=True)
                if '--smoke' in sys.argv:return
if __name__=='__main__':main()
