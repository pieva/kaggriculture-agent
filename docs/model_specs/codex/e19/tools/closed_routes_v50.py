"""Insertion packing charges the final depot trip during each insertion."""
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import route_cost,distance,protected_order


def closed_cost(start,route,sheds,inventory,initial_output=False):
    cost=route_cost(start,route,sheds,inventory)
    output=initial_output or any(inventory.values()) or any(c[0] in {'HARVEST','COLLECT_FERTILIZER'} for o in route for c in o[1])
    if output:
        end=route[-1][0] if route else start
        cost+=min(distance(end,s) for s in sheds)+1
    return cost


def pack_routes(positions,inventories,sheds,offers,budget,budgets=None,initial_outputs=()):
    routes=[[] for _ in positions];unassigned=[]
    for offer in sorted(offers,key=lambda o:(-o[2],o[0])):
        choices=[]
        for w,start in enumerate(positions):
            old=closed_cost(start,routes[w],sheds,inventories[w],w in initial_outputs)
            for slot in range(len(routes[w])+1):
                candidate=routes[w][:slot]+[offer]+routes[w][slot:]
                if not protected_order(candidate):continue
                cost=closed_cost(start,candidate,sheds,inventories[w],w in initial_outputs)
                if cost<=(budget if budgets is None else budgets[w]):choices.append((cost-old,cost,w,slot,candidate))
        if not choices:unassigned.append(offer);continue
        _,_,w,slot,route=min(choices,key=lambda c:c[:4]);routes[w]=route
    return routes,unassigned
