"""Observed-state fixes, preserving V51C topology and crop choices."""
from collections import Counter

def net_grain_orders(orders):
    sell=sum(o[2] for o in orders if o[:2]==['SELL','WHEAT'])
    buy=sum(o[2] for o in orders if o[:2]==['BUY_PRODUCT','WHEAT'])
    cancel=min(sell,buy)
    if not cancel:return orders
    remaining={'SELL':cancel,'BUY_PRODUCT':cancel};result=[]
    for o in orders:
        if len(o)>=3 and o[1]=='WHEAT' and o[0] in remaining:
            n=min(o[2],remaining[o[0]]);remaining[o[0]]-=n
            if o[2]>n:result.append([o[0],o[1],o[2]-n])
        else:result.append(o)
    return result

def install(core):
    services,growth,market=core._services,core._growth,core._market_orders
    def threatened():
        if not 11<=core.day<core.final_day:return []
        return [(x,y) for y,row in enumerate(core.farm['tiles']) for x,t in enumerate(row)
                if isinstance(t,dict) and t.get('animal') and not t.get('fed_today') and t.get('consecutive_unfed',0)>=1]
    def urgent_services():
        offers=services();targets=set(threatened())
        # Existing feeding jobs already own these obligations.
        targets-={tuple(j['target']) for j in core.active.values() if any(c[0]=='FEED' for c,p in j['steps'])}
        # Do not give two workers ownership of the same tile.
        targets-={tuple(j['target']) for j in core.active.values()}
        return [o for o in offers if tuple(o[0]) not in targets]+[(p,[['FEED']],8,1,'BIOLOGICAL') for p in sorted(targets)]
    def safe_growth(cash):
        # Delaying new investment is preferable to allowing a known escape.
        return [] if threatened() else growth(cash)
    def reserved_market():
        orders=market();targets=threatened()
        if targets:
            # Carried grain on unrelated crop routes is not available in the shed.
            # Reserve one observed depot ration for each uncovered urgent animal.
            covered={tuple(j['target']) for w,j in core.active.items()
                     if any(c[0]=='FEED' for c,p in j['steps']) and core.private['inventories'][w].get('WHEAT',0)>0}
            need=len(set(targets)-covered)
            stock=core.private['shed'].get('WHEAT',0)
            revised=[]
            for o in orders:
                if o[:2]==['SELL','WHEAT']:
                    n=min(o[2],max(0,stock-need))
                    if n:revised.append(['SELL','WHEAT',n])
                else:revised.append(o)
            bought=sum(o[2] for o in revised if o[:2]==['BUY_PRODUCT','WHEAT'])
            deficit=max(0,need-stock-bought)
            # Buy before other discretionary orders, using observed cash only.
            affordable=0
            for n in range(1,deficit+1):
                if core._quote('WHEAT','BUY',n)>core.farm['money']:break
                affordable=n
            if affordable:
                revised.insert(0,['BUY_PRODUCT','WHEAT',affordable])
                revised=revised[:10]
            orders=revised
        if core.day==core.final_day:
            # No later production: do not preserve inventory for future services.
            orders=[o for o in orders if o[0] not in {'BUY_PRODUCT','BUY_SEED','BUY_ANIMAL','BUY_LAND','SELL'}]
            animals=core.__call__.__func__.__globals__['ANIMALS']
            sales=[['SELL',k,n] for k,n in sorted(core.private['shed'].items()) if n>0 and k not in animals]
            orders=(sales+orders)[:10]
        return net_grain_orders(orders)
    core._services=urgent_services;core._growth=safe_growth;core._market_orders=reserved_market

class FixedPolicy:
    def __init__(self,policy):self.policy=policy
    def __getattr__(self,name):return getattr(self.policy,name)
    def __call__(self,observation,configuration):
        action=self.policy(observation,configuration)
        # Same-batch round trips were also present in the frozen opening.
        return dict(action,market=net_grain_orders(action.get('market',[])))
