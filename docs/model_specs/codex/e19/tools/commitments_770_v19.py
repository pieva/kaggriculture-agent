"""Protected commitments, bounded aging and optional reproducible tie breaking."""
from hashlib import sha256
from docs.model_specs.codex.e19.tools.biological_plan_770_v18 import install as install_previous


def stable_tie(seed, day, worker, target, kind, commands):
    key=repr((int(seed),day,worker,tuple(target),kind,tuple(tuple(c) for c in commands))).encode()
    return int.from_bytes(sha256(key).digest()[:8],'big') / 2**64


def commitment_rank(tile, commands, kind, priority, age):
    ops={c[0] for c in commands}
    if ('FEED' in ops and tile.get('consecutive_unfed',0)>=1 or
        'WATER' in ops and tile.get('consecutive_unwatered',0)>=1):
        return 8
    if kind=='NEW_ROTATION' and 'HARVEST' in ops and 'PLANT' in ops:
        return 7
    if kind=='NEW_ANIMAL' and tile.get('kind')=='PASTURE' and not tile.get('animal'):
        return 6
    if kind=='SERVICE' and priority==4:
        return 5
    if kind.startswith('NEW_') and age>=24:
        return 5
    if 'FEED' in ops:
        return 4
    if kind=='SERVICE':
        return 3
    return 1+min(1,age//12)


def install(core):
    install_previous(core)
    first_seen={}
    growth=core._growth
    acknowledge=core._acknowledge
    def key(target,commands,kind):
        tile=core._tile(target)
        tile=tile if isinstance(tile,dict) else {}
        crop=next((c[1] for c in commands if c[0]=='PLANT'),None)
        return (tuple(target),kind,crop,tile.get('kind'),tile.get('planted_day'),tile.get('placed_day'))
    def registered_growth(cash):
        offers=growth(cash)
        if core.day<25:
            for target,commands,priority,value,kind in offers:
                first_seen.setdefault(key(target,commands,kind),core.day*24+core.hour)
        return offers
    def acknowledged():
        placements=[tuple(target) for cmd,target,before in core.previous.values() if cmd[0] in {'PLANT','PLACE'}]
        acknowledge()
        for target in placements:
            tile=core._tile(target)
            if isinstance(tile,dict) and (tile.get('planted_day')==core.day or tile.get('placed_day')==core.day):
                for k in list(first_seen):
                    if k[0]==target:del first_seen[k]
    def score(worker,target,commands,priority,value,kind,steps):
        cost=len(steps)+2*int(worker!=core._planned_owner(target))
        tile=core._tile(target);tile=tile if isinstance(tile,dict) else {}
        age=max(0,core.day*24+core.hour-first_seen.get(key(target,commands,kind),core.day*24+core.hour))
        rank=commitment_rank(tile,commands,kind,priority,age)
        tie=stable_tie(core.commitment_seed,core.day,worker,target,kind,commands) if core.commitment_random else 0
        # Randomness is below ALL biological, route, value and waiting criteria.
        return (rank,int(kind=='NEW_ROTATION'),-cost,value/max(1,len(steps)),min(age,48),tie,-worker,tuple(-n for n in target))
    core._growth=registered_growth
    core._acknowledge=acknowledged
    core._commitment_score=score
    core.commitment_random=False
    core.commitment_seed=0
