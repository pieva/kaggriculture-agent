"""Same-visit succession with an insertion-based current-day certificate.

The fallback certifies the observed FEED/WATER obligations plus animal CARE as V29; it
does not relax them. Full active missions remain charged to their workers.
"""
from collections import Counter
from docs.model_specs.codex.e19.tools.daily_route_dispatch_770_v44 import install as previous
from docs.model_specs.codex.e19.tools.daily_routes_770_v44 import pack_routes, inputs

def install(core):
    previous(core)
    original=core._day_route_certificate
    stamp=None; calls=0
    core.renewal_certificate_log=[]
    def certificate(worker,job,services=None):
        nonlocal stamp,calls
        if original(worker,job,services):return True
        if core.day>=25:return False
        now=(core.day,core.hour)
        if stamp!=now:stamp,calls=now,0
        if calls>=max(16,4*len(core.positions)):return False
        calls+=1
        jobs=dict(core.active);jobs[worker]=job
        positions=list(core.positions)
        inventories=[Counter(v) for v in core.private['inventories']]
        budgets=[core.remaining for _ in positions]
        for w,j in jobs.items():
            budgets[w]-=len(j['steps'])
            for cmd,pos in j['steps']:
                if cmd[0] in {'NORTH','SOUTH','EAST','WEST'}:positions[w]=pos
                elif cmd[0]=='PICKUP':
                    inventories[w][cmd[1]]+=cmd[2]
                    if core.private['shed'].get(cmd[1],0)<cmd[2]:budgets[w]-=1
                elif cmd[0] in {'FEED','FERTILIZE','PLACE'}:inventories[w].subtract(inputs([cmd]))
                elif cmd[0]=='DROP':inventories[w].clear()
            if budgets[w]<0:return False
        required={}
        covered={tuple(j['target']) for j in jobs.values() if j['kind']!='DELIVER'}
        for target,cmds,priority,value,kind in (core._services() if services is None else services):
            if tuple(target) in covered:continue
            tile=core._tile(target)
            if not isinstance(tile,dict):continue
            cmds=[c for c in cmds if c[0] in {'FEED','CARE'} and tile.get('animal') or c[0]=='WATER' and tile.get('kind')=='PLANT']
            if cmds:required[tuple(target)]=(target,cmds,priority,1,'BIOLOGICAL')
        routes,unassigned=pack_routes(positions,inventories,core.sheds,list(required.values()),core.remaining,budgets)
        ok=not unassigned
        core.metrics['renewal_insertion_accept' if ok else 'renewal_insertion_reject']+=1
        if ok and len(core.renewal_certificate_log)<200:
            core.renewal_certificate_log.append(dict(day=core.day+1,hour=core.hour+1,worker=worker,target=job['target'],kind=job['kind'],obligations=len(required),budgets=budgets))
        return ok
    core._day_route_certificate=certificate
