"""Compile native daily worker visits into a 772-specific operational plan."""
from pathlib import Path
from collections import defaultdict
import json,hashlib
BASE=Path(__file__).resolve().parent
SOURCE=BASE/'reports/common_operational_program'
OUT=BASE/'reports/operational772_v1'
MOVE={'NORTH','SOUTH','EAST','WEST','PASS'}
ANIMAL_TARGETS={(1,4):(4,6),(4,1):(4,5),(3,2):(3,2),(2,3):None,(6,3):(6,3)}
SPECIES={(4,6):'SHEEP',(4,5):'COW',(3,2):'SHEEP',(6,3):'COW'}
CROP_TARGETS={(4,5):(4,1),(4,6):(2,3)}
def build(adapt=True):
    operations=json.loads((SOURCE/'OPERATIONS.json').read_text(encoding='utf-8'))
    original=json.loads((SOURCE/'PROGRAM.json').read_text(encoding='utf-8'))
    plans=defaultdict(lambda:defaultdict(list));changes=[]
    for op in operations:
        cmd=list(op['command']);name=cmd[0];pos=tuple(op['position_before']);tile=op['tile_before'];day=op['day'];worker=op['worker']
        if name in MOVE:continue
        # Animal pickup is supplied from the actual adapted placement command.
        if name=='PICKUP' and cmd[1] in {'COW','SHEEP','GOOSE'}:continue
        animal=(isinstance(tile,dict) and (tile.get('animal') or tile.get('kind') in {'PASTURE','COOP'})) or name in {'PLACE','BUILD_PASTURE','BUILD_COOP'}
        dest=pos
        if adapt:
            if animal and pos in ANIMAL_TARGETS:
                dest=ANIMAL_TARGETS[pos]
                if dest is None:
                    changes.append(dict(source_step=op['source_step'],worker=worker,position=pos,command=cmd,change='removed animal visit'));continue
                if dest in SPECIES and name=='PLACE':cmd=['PLACE',SPECIES[dest]]
                if name=='BUILD_COOP':cmd=['BUILD_PASTURE']
                if dest in {(4,5),(4,6)}:day=max(day,12)
            elif not animal and pos in CROP_TARGETS and day>=12:
                dest=CROP_TARGETS[pos]
            elif name=='BUILD_COOP' or name=='DIG' and isinstance(tile,dict) and tile.get('kind')=='COOP':
                changes.append(dict(source_step=op['source_step'],worker=worker,position=pos,command=cmd,change='removed temporary coop'));continue
        job=dict(position=list(dest),command=cmd,source_step=op['source_step'],source_day=op['day'],source_hour=op['hour'],changed=dest!=pos or cmd!=op['command'] or day!=op['day'])
        plans[day][worker].append(job)
        if job['changed']:changes.append(dict(original=op,adapted=job,day=day,worker=worker))
    # Balance only displaced visits into spare slots, preserving unchanged route ordering.
    # Greedy insertion uses distance and command count; it is a static compiler,
    # never a run-time priority dispatcher. Resource detours are measured separately.
    allocation=[]
    def cost(jobs):
        pos=(4,4);steps=0
        for j in jobs:
            p=tuple(j['position']);steps+=abs(pos[0]-p[0])+abs(pos[1]-p[1])+1;pos=p
        return steps
    for day,workers in plans.items():
        if not adapt:continue
        displaced=[]
        for w,jobs in workers.items():
            keep=[]
            for j in jobs:
                if j['changed']:displaced.append((w,j))
                else:keep.append(j)
            workers[w]=keep
        # Keep all consecutive commands of each changed physical visit together.
        bundles=[]
        for w,j in displaced:
            if bundles and bundles[-1][0]==w and bundles[-1][1][-1]['position']==j['position']:
                bundles[-1][1].append(j)
            else:bundles.append((w,[j]))
        for source,jobs in bundles:
            choices=[]
            for w,route in workers.items():
                for index in range(len(route)+1):
                    # Never split the commands of an existing visit.
                    if 0<index<len(route) and route[index-1]['position']==route[index]['position']:continue
                    trial=route[:index]+jobs+route[index:]
                    length=cost(trial)
                    choices.append(((max(0,length-24),length-cost(route),int(w!=source),length),w,index))
            _,w,index=min(choices)
            workers[w][index:index]=jobs
            allocation.append(dict(day=day,source_worker=source,worker=w,position=jobs[0]['position'],commands=[j['command'] for j in jobs],estimated_route_steps=cost(workers[w])))
    return dict(adapted=adapt,source_episode=original['episode'],days={str(d):{str(w):jobs for w,jobs in workers.items()} for d,workers in plans.items()},market_frames={f"{x['day']}:{x['hour']}":x['action'].get('market',[]) for x in original['frames']},changes=changes,allocation=allocation)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,flag in [('PLAN_772.json',True),('PLAN_NATIVE.json',False)]:
        (OUT/name).write_text(json.dumps(build(flag),ensure_ascii=False,indent=2),encoding='utf-8')
    print('Compiled native and adapted 772 plans')
if __name__=='__main__':main()
