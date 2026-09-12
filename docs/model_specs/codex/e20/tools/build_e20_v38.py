"""Freeze an E18-controller transfer to the 772 topology; no V48 planner."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OVERLAY='''
# E20v38: retain the frozen E18 controller and enforce 772 from D12.
_E20_V38_PARENT_CREATE=create_agent
class E20V38Policy:
    def __init__(self,context):
        self.policy=_E20_V38_PARENT_CREATE(context)
        self.core=self.policy.codex_e18_capacity_governed_instance
        self.configured=False
    def __call__(self,observation,configuration=None):
        if observation['day']<11:return self.policy(observation,configuration)
        t=self.core
        if not self.configured:
            t.committed_reclaims={(3,5),(3,6),(4,7)}
            t._apply_reclaim_envelope()
            assert t.target_pastures_by_quadrant=={'Q0':7,'Q1':7,'Q2':2}
            t.livestock_resource_cap=16
            t.config['pre_q2_livestock_resource_cap']=16
            t.config['reclaimed_seed_backfill_units']=3
            t._transition(observation['day'],'RECLAIM_CROP','fixed_772_controller_transfer')
            self.configured=True
        try:
            t._observe_day(observation)
            # The inherited cap applies throughout the season; it must not
            # roll back to 775 when a blocked construction has no replacement.
            action=_e18_2.CodexE17TopologyCap662Agent.__call__(t,observation,configuration)
            if observation['day']<28 and t.mode=='RECOVERY':
                pressure=t.latest_opponent_pressure>=float(t.e18_config['reclaim_pressure_threshold'])
                severe=int(t.latest_own_capacity.get('hard_stress',0))>=2*int(t.e18_config['recovery_entry_stress'])
                count=len(_e18_2._positions(_e18_2._farm(observation)))
                t._route_idle_service(action,observation,tasks=t._recovery_tasks(observation),eligible=t._pass_workers(action,count),limit=int(t.e18_config['recovery_worker_limit']) if pressure or severe else 0)
            return action
        except Exception:
            t.error_count+=1
            raise
MODEL_VERSION='CODEX-E20-772-E20V38'
RELEASE_ID=MODEL_VERSION
BUILD_METADATA={'release_id':MODEL_VERSION,'base':'frozen E18.2 V4D','topology':'7-7-2','status':'LOCAL_EXPERIMENTAL_CONTROLLER_TRANSFER','uploaded':False}
def create_agent(run_context=None):return E20V38Policy(run_context)
_E20_V38_ACTIVE={}
def agent(observation,configuration=None):
    configuration=configuration or {}
    seat=int(observation.get('player',0));step=observation['day']*configuration.get('turnsPerDay',24)+observation['hour']
    previous=_E20_V38_ACTIVE.get(seat)
    policy=create_agent({'player_position':seat}) if previous is None or step<=previous[0] else previous[1]
    _E20_V38_ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
'''
def main():
    parent=ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'
    out=ROOT/'submission/submission_codex_e20_772_e20v38_candidate.py';assert not out.exists()
    source=parent.read_text(encoding='utf-8')+OVERLAY;compile(source,str(out),'exec');out.write_text(source,encoding='utf-8')
    m=dict(variant='E20v38',version='E20.7',status='LOCAL_FROZEN_CANDIDATE',uploaded=False,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),sources={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [parent,Path(__file__)]})
    out.with_suffix('.manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');print(out)
if __name__=='__main__':main()
