"""Read-only instrumented V5 decision audit; no benchmark-fitted policy."""
import hashlib
import importlib
import json
from pathlib import Path

from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as gate
from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController

BASE = Path(__file__).resolve().parents[1]


def main():
    output = BASE/'artifacts/derived/E18_33_V5_ADMISSION_TRACE_20260906.json'
    assert not output.exists()
    config = json.loads((BASE/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V1.json').read_text())
    engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    rows = []
    class Trace(CommonController):
        def __call__(self, obs, cfg):
            result = super().__call__(obs, cfg)
            if self.hour in (0, 6, 12, 18):
                free_cash = self.farm['money']-self.maintenance_floor
                growth = self._growth(free_cash)
                rows.append(dict(day=self.day+1,hour=self.hour+1,money=self.farm['money'],
                    hands=len(self.positions)-1,maintenance_floor=self.maintenance_floor,
                    animal_values=self.animal_values,crop_values=self.crop_values,
                    quotes=self.market['prices'],owned=dict(self._owned()),
                    active=[dict(worker=w,kind=j['kind'],target=j['target'],remaining=len(j['steps'])) for w,j in self.active.items()],
                    growth_offers=len(growth),animal_offers=sum(g[-1]=='NEW_ANIMAL' for g in growth),
                    animal_feasible=sum(self._prepare_steps(w,t,c,buy=True) is not None for w in range(len(self.positions)) if w not in self.active for t,c,_,_,k in growth if k=='NEW_ANIMAL'),
                    action=result))
            return result
    gate.MissionRuntimeController = lambda plan,seat,variant:Trace(config,engine.market_price,engine.MARKET_PARAMS,seat)
    sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'tools/e18_33_common_controller.py',BASE/'tools/e18_33_common_policy.py')}
    print('V5 native diagnostic loaded',flush=True)
    match=gate.run_one('CROP_POOL','E18.16',180903001,0)
    output.write_text(json.dumps(dict(source_sha256=sources,rows=rows,match=match),indent=2)+'\n',encoding='utf-8')
    print(output,flush=True)


if __name__=='__main__':
    main()
