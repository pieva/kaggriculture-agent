"""Closed routes with shared depot stock and carried-input constraints."""
from collections import Counter
from docs.model_specs.codex.e19.tools.closed_routes_v50 import closed_cost
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import inputs,protected_order


def need(route,inventory):
    demand=Counter()
    for offer in route:demand.update(inputs(offer[1]))
    return demand-Counter(inventory)


def pack_routes(positions,inventories,sheds,offers,budget,budgets=None,initial_outputs=(),warehouse=None):
    routes=[[] for _ in positions];unassigned=[];used=Counter()
    # Serve scarce carried inputs before filling their owners with other work.
    for offer in sorted(offers,key=lambda o:(-int(o[2]==8),-int(bool(inputs(o[1]))),-o[2],o[0])):
        choices=[]
        for w,start in enumerate(positions):
            old=closed_cost(start,routes[w],sheds,inventories[w],w in initial_outputs)
            old_need=need(routes[w],inventories[w])
            for slot in range(len(routes[w])+1):
                candidate=routes[w][:slot]+[offer]+routes[w][slot:]
                if not protected_order(candidate):continue
                demand=used-old_need+need(candidate,inventories[w])
                if warehouse is not None and any(n>warehouse.get(item,0) for item,n in demand.items()):continue
                cost=closed_cost(start,candidate,sheds,inventories[w],w in initial_outputs)
                if cost<=(budget if budgets is None else budgets[w]):choices.append((cost-old,cost,w,slot,candidate,demand))
        if not choices:unassigned.append(offer);continue
        _,_,w,slot,route,used=min(choices,key=lambda c:c[:4]);routes[w]=route
    return routes,unassigned
