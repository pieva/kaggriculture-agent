"""Remove only animal care with no remaining biological value; preserve staffing."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent

def main():
    parent=ROOT/'submission/submission_codex_e19_770_v51_candidate.py'
    text=parent.read_text(encoding='utf-8')
    assert hashlib.sha256(parent.read_bytes()).hexdigest()=='43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda'
    source=(HERE/'sources_v51c/biological_plan_770_v48.py').read_text(encoding='utf-8')
    old="(core.day<27 or care_value(t,core.day,core.final_day,r,core._quote)>0)"
    new="(core.day<11 or productive_care_value(t,core.day,core.final_day,r,core._quote)>0)"
    assert source.count(old)==1 and text.count(repr(source))==1
    helper='''
def productive_care_value(tile,day,final_day,rule,quote):
    # The coming refresh consumes the previous bonus before storing today's care.
    # Preserve care on production eve even if the current bonus is saturated.
    age=day+1-tile['placed_day']
    consumes=age>=rule['first_yield_day'] and (age-rule['first_yield_day'])%rule['interval']==0
    observed=dict(tile)
    if consumes:observed['pending_care_bonus']=0
    return care_value(observed,day,final_day,rule,quote)

'''
    revised=source.replace(old,new).replace('def biological_calendar(',helper+'def biological_calendar(',1)
    text=text.replace(repr(source),repr(revised)).replace("MODEL_VERSION='CODEX-E19-770-V51-CANDIDATE'","MODEL_VERSION='CODEX-E19.2-770-V52D-VALUED-CARE'")
    out=ROOT/'submission/archive/e19_rejected/submission_codex_e19_2_770_v52d.py'
    compile(text,str(out),'exec');out.write_text(text,encoding='utf-8')
    (HERE/'biological_plan_v52d.py').write_text(revised,encoding='utf-8')
    (HERE/'MANIFEST_V52D.json').write_text(json.dumps(dict(file=str(out.relative_to(ROOT)),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(parent.read_bytes()).hexdigest(),status='experimental, not submitted',change='From D12 omit CARE when stored bonus is saturated or no reachable production remains. Same staffing maximum, routes, topology, feeding and crop rotation as V51C.'),indent=2),encoding='utf-8')
if __name__=='__main__':main()
