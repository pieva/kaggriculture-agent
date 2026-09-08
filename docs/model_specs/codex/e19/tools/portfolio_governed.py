"""Expand the observed opening mix before allowing the terminal succession."""
from collections import Counter
from docs.model_specs.codex.e19.tools.portfolio_execution_v7 import install as install_execution


def proportional_targets(weights, capacity):
    total=sum(weights.values())
    if not total:return {}
    targets={c:capacity*n//total for c,n in weights.items()}
    order=sorted(weights,key=lambda c:(-(capacity*weights[c]%total),c))
    for c in order[:capacity-sum(targets.values())]:targets[c]+=1
    return targets


def install(core):
    install_execution(core)
    growth=core._growth
    rules=core.__call__.__func__.__globals__['CROPS']
    weights={}
    targets={}
    core.portfolio_governance={}

    def governed_growth(cash):
        nonlocal weights,targets
        present=Counter(t['crop'] for row in core.farm['tiles'] for t in row if isinstance(t,dict) and t.get('kind')=='PLANT')
        if not weights:
            weights=dict(present)
            size=len(core.farm['tiles'])
            capacity=(size//2)**2*core.profile.maximum_quadrants-core.profile.target
            targets=proportional_targets(weights,capacity)
        long_crops=[c for c in weights if rules[c]['ongoing']]
        active=bool(long_crops) and any(core.day+rules[c]['first_yield_day']<=core.final_day for c in long_crops)
        offers=growth(cash)
        options=core.portfolio_latest
        _,reserved=core._requirements()
        gaps={c:max(0,targets[c]-present[c]-reserved[c]) for c in targets}
        scale=max([1]+[r['admission_value'] for r in options.values()])
        core.portfolio_governance=dict(weights=weights,targets=targets,deficits=gaps,active=active)
        if not active:return offers
        result=[]
        for target,commands,priority,value,kind in offers:
            if kind=='NEW_CROP':
                crop=next(c[1] for c in commands if c[0]=='PLANT')
                if gaps.get(crop,0)<=0:continue
                value=scale*gaps[crop]/max(1,targets[crop])
            elif kind=='NEW_ROTATION':
                tile=core._tile(target)
                previous=tile.get('crop')
                if previous in weights and not rules[previous]['ongoing'] and options.get(previous,{}).get('admission_value',0)>0:
                    following=next(c[1] for c in commands if c[0]=='PLANT')
                    commands=[['PLANT',previous] if c[0]=='PLANT' else c for c in commands]
                    value+=options[previous]['admission_value']-options[following]['admission_value']
                    core.portfolio_proposed_ends[(tuple(target),previous,core.day)]=options[previous]['end']
            result.append((target,commands,priority,value,kind))
        return result
    core._growth=governed_growth
