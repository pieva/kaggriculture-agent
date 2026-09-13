"""First E19.2 candidate: extend committed service routes to D12-D29."""
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
def main():
 parent=ROOT/'submission/submission_codex_e19_770_v51_candidate.py'
 text=parent.read_text(encoding='utf-8');assert hashlib.sha256(parent.read_bytes()).hexdigest()=='43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda'
 original=(HERE/'sources_v51c/committed_routes_v51c.py').read_text(encoding='utf-8')
 revised=original.replace('core.day!=28','not (11<=core.day<=28)').replace('day=29','day=core.day+1')
 assert original.count('core.day!=28')==3
 # Same route compilation and observed warehouse constraints used on D29;
 # expand the interval only. Preserve D1-D11 opening and D30 closure.
 assert text.count(repr(original))==1
 text=text.replace(repr(original),repr(revised)).replace("MODEL_VERSION='CODEX-E19-770-V51-CANDIDATE'","MODEL_VERSION='CODEX-E19.2-770-V52A-COMMITTED-SERVICES'")
 out=ROOT/'submission/archive/e19_rejected/submission_codex_e19_2_770_v52a.py';compile(text,str(out),'exec');out.write_text(text,encoding='utf-8')
 (HERE/'committed_routes_v52a.py').write_text(revised,encoding='utf-8')
 (HERE/'MANIFEST.json').write_text(json.dumps({'name':'E19.2 770 V52A','parent':'E19 770 V51C','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'file':str(out.relative_to(ROOT)),'change':'Committed observed-service routes and residual hiring from D12 through D29, previously D29 only. Same topology/mix/crop intentions; D30 closure unchanged.','status':'experimental, not submitted'},indent=2),encoding='utf-8')
 print(out)
if __name__=='__main__':main()
