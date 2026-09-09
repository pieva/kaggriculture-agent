from copy import deepcopy
import gzip,json,runpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.workforce_certificate_v50c import certified_additions


def main():
    r=json.load(gzip.open(ROOT/'scratch/v49/development_v49f_180903003_0.json.gz','rt'))['replay']
    p=runpy.run_path(str(ROOT/'submission/submission_codex_e19_770_v49f_candidate.py'))['create_agent']({'player_position':0})
    evidence=[]
    for i in range(1,675):
        o=deepcopy(r['steps'][i-1][0]['observation']);o.update(player=0,step=i-1)
        a=p(o,r['configuration']);assert a==r['steps'][i][0]['action'],i
        if o['day']!=28:continue
        maximum=sum(c==['HIRE'] for c in a['market'])
        if not maximum:continue
        core=p.core;offers=core._services();snap={}
        def trace(frame,event,arg):
            if frame.f_code is certified_additions.__code__ and event=='return':
                snap.update({k:deepcopy(v) for k,v in frame.f_locals.items() if k in ['count','budgets','costs','unassigned','pickups','warehouse','committed_pickups']})
            return trace
        sys.settrace(trace)
        result=certified_additions(core,offers,maximum,a['market'])
        sys.settrace(None)
        evidence.append(dict(hour=core.hour+1,result=result,active=deepcopy(core.active),final_attempt=snap))
    out=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v50/certificate_inspection.json'
    out.write_text(json.dumps(evidence,indent=2));print(json.dumps(evidence),flush=True)


if __name__=='__main__':main()
