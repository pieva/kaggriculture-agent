"""D29 route ownership respects grain already carried or committed."""
from collections import Counter
from types import FunctionType
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import route_cost,inputs,protected_order


def pack_supplied(positions,inventories,sheds,offers,budget,budgets,warehouse):
    routes=[[] for _ in positions];unassigned=[];used=Counter()
    def need(route,w):
        result=Counter()
        for offer in route:result.update(inputs(offer[1]))
        return result-Counter(inventories[w])
    for offer in sorted(offers,key=lambda o:(-int(o[2]==8),-int(bool(inputs(o[1]))),-o[2],o[0])):
        choices=[]
        for w,start in enumerate(positions):
            old=route_cost(start,routes[w],sheds,inventories[w]);old_need=need(routes[w],w)
            for slot in range(len(routes[w])+1):
                candidate=routes[w][:slot]+[offer]+routes[w][slot:]
                if not protected_order(candidate):continue
                demand=used-old_need+need(candidate,w)
                if any(n>warehouse.get(item,0) for item,n in demand.items()):continue
                cost=route_cost(start,candidate,sheds,inventories[w])
                if cost<=(budget if budgets is None else budgets[w]):choices.append((cost-old,cost,w,slot,candidate,demand))
        if not choices:unassigned.append(offer);continue
        _,_,w,slot,route,used=min(choices,key=lambda c:c[:4]);routes[w]=route
    return routes,unassigned


def install(core):
    services=core._services;original=services.__globals__['pack_routes']
    core.v50_route_log=[]
    def packed(positions,inventories,sheds,offers,budget,budgets=None):
        if core.day!=28:return original(positions,inventories,sheds,offers,budget,budgets)
        warehouse=Counter(core.private['shed'])
        for job in core.active.values():
            for cmd,pos in job['steps']:
                if cmd[0]=='PICKUP':warehouse[cmd[1]]-=cmd[2]
        routes,unassigned=pack_supplied(positions,inventories,sheds,offers,budget,budgets,warehouse)
        core.v50_route_log.append(dict(day=29,hour=core.hour+1,workers=len(positions),unassigned=len(unassigned),warehouse=dict(warehouse)))
        return routes,unassigned
    core._services=FunctionType(services.__code__,dict(services.__globals__,pack_routes=packed),services.__name__,services.__defaults__,services.__closure__)
