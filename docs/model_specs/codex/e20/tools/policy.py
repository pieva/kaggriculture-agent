"""E20: frozen V48 opening and routes, two explicitly reserved E18 Q2 plots."""
from dataclasses import replace
import ast
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parents[5]
VARIANTS={
    'E20v1': dict(positions=((3,5),(4,5)), species=('COW','SHEEP'), start=11),
    'E20v2': dict(positions=((3,5),(4,5)), species=('COW','COW'), start=11),
    'E20v3': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11),
    'E20v4': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True),
    'E20v5': dict(positions=((3,5),(4,5)), species=('COW','SHEEP'), start=11, preserve=True),
    'E20v6': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=13, preserve=True),
    'E20v7': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, hands=13),
    'E20v8': dict(positions=((3,5),(4,5)), species=('COW','SHEEP'), start=11, preserve=True, hands=14),
    'E20v9': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, teacher_hours=24),
    'E20v10': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, teacher_hours=8),
    'E20v11': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, teacher_hours=12),
    'E20v12': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, q2crop='MELON'),
    'E20v13': dict(positions=((3,5),(4,5)), species=('COW','SHEEP'), start=11, preserve=True, q2crop='MELON'),
    'E20v14': dict(positions=((4,5),(4,6)), species=('SHEEP','SHEEP'), start=11, preserve=True),
    'E20v15': dict(positions=((3,5),(3,6)), species=('SHEEP','SHEEP'), start=11, preserve=True),
    'E20v16': dict(positions=((3,6),(4,6)), species=('SHEEP','SHEEP'), start=11, preserve=True),
    'E20v17': dict(positions=((4,6),(4,7)), species=('SHEEP','SHEEP'), start=11, preserve=True),
    'E20v18': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True),
    'E20v19': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, q2care=False),
    'E20v20': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, q2care_price=100),
    'E20v21': dict(positions=((3,5),(4,5)), species=('SHEEP','SHEEP'), start=11, preserve=True, q2care_until=17),
    'E20v22': dict(positions=((3,5),(3,6)), species=('COW','SHEEP'), start=11, preserve=True),
    'E20v23': dict(positions=((3,5),(3,6)), species=('SHEEP','SHEEP'), start=11, preserve=True, q2care=False),
    'E20v24': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, water_deadline=True),
    'E20v25': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, water_rescue=True),
    'E20v26': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True),
    'E20v27': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, useful_care=True),
    'E20v28': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True),
    'E20v29': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_hourly_routes=True),
    'E20v30': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_transfer=True),
    'E20v31': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_closing=True),
    'E20v32': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_care_floor=True),
    'E20v33': dict(positions=((4,5),(4,6)), species=('SHEEP','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_care_floor=True, animal_mix=(('COW',8),('SHEEP',8))),
    'E20v34': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_care_floor=True, economic_short_cycle=True),
    'E20v35': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_care_floor=True, economic_short_cycle=True),
    'E20v36': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_care_floor=True, economic_short_cycle=True, observed_demand=True),
    'E20v37': dict(positions=((4,5),(4,6)), species=('COW','SHEEP'), start=11, preserve=True, remote_first=True, useful_care=True, late_care_floor=True, economic_short_cycle=True, observed_demand=True, conditional_sell=True),
}

SHOP_PRODUCTS={'BAKERY':('EGG','WHEAT'),'PIZZA_SHOP':('MILK','TOMATO','WHEAT'),
    'BRUNCH_SPOT':('EGG','WHEAT','STRAWBERRY'),'YARN_STORE':('WOOL',),
    'ICE_CREAM_SHOP':('STRAWBERRY','MILK','WHEAT'),'PET_CAFE':('CARROT',),
    'SMOOTHIE_SHOP':('STRAWBERRY','MILK'),'FARMERS_MARKET':('WHEAT','CARROT','TOMATO','STRAWBERRY')}

def observed_town_demand(core,item,day):
    """Conditional demand from current public shops only, at configured intervals."""
    if item=='FERTILIZER' or day<=core.day:return 0
    configuration=core.e20_configuration
    start=core.day*core.turns+core.hour;end=start+(day-core.day)*core.turns
    interval=max(1,int(configuration.get('townShopSellInterval',4)))
    center=max(1,int(configuration.get('townCenterSellInterval',24)))
    per_event=sum((2 if len(SHOP_PRODUCTS.get(s,()))==1 else 1) for s in core.e20_observation.get('town',{}).get('unlocked_shops',[]) if item in SHOP_PRODUCTS.get(s,()))
    return per_event*(end//interval-start//interval)+(end//center-start//center)

class ObservedDemandPolicy:
    def __init__(self,policy):self.policy=policy;self.core=policy.core
    def __call__(self,observation,configuration=None):
        self.core.e20_observation=observation;self.core.e20_configuration=configuration or {}
        return self.policy(observation,configuration)

def choose_short_cycle(core,intended,rules,cash):
    """Use existing conditional valuations only for a wheat/carrot planting choice."""
    if intended!='WHEAT' or not 11<=core.day<25:return intended
    options=getattr(core,'portfolio_latest',{})
    wheat,carrot=options.get('WHEAT'),options.get('CARROT')
    if not wheat or not carrot or cash<rules['CROPS']['CARROT']['seed']:return intended
    if carrot['end']>core.final_day-1 or carrot['admission_value']<=0:return intended
    return 'CARROT' if carrot['total']>wheat['total'] else intended

def care_can_add_yield(tile,day,final_day,rule):
    """Zero-gain filter; assumes future feeding and timely collection, not future prices."""
    if tile.get('cared_today'):return False
    def produces(d):
        age=d-tile['placed_day']
        return age>=rule['first_yield_day'] and (age-rule['first_yield_day'])%rule['interval']==0
    if not any(produces(d) for d in range(day+2,final_day+1)):return False
    # Today's bonus is stored AFTER the next refresh's production.
    pending=0 if produces(day+1) else tile.get('pending_care_bonus',0)
    return pending<rule['max_held']-1

def care_market_allows(day,prices,product):
    """Experimental spot-price gate; no claim about prices at future production."""
    price=prices.get(product)
    return day<19 or price is None or price>1

def productive_water_deadline(day,tile,commands,rules,turns=24,final_day=29):
    """Protect an existing crop that can survive and still produce this season."""
    if not (11<=day<29 and isinstance(tile,dict) and tile.get('kind')=='PLANT'
            and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today')
            and any(c[0]=='WATER' for c in commands)
            and not any(c[0] in {'PLANT','DIG'} for c in commands)):
        return False
    lifespan=tile.get('max_lifespan_step',-1)
    if lifespan>=0 and lifespan<=(day+1)*turns:return False
    r=rules[tile['crop']]
    first=tile['planted_day']+r['first_yield_day']
    last=first+(r['max_yield']-1)*r['interval'] if r['ongoing'] else tile['planted_day']+r['max_yield_day']
    return first<=final_day and (tile.get('yield_units',0)>0 or day<=last)

def create_agent(context=None, variant='E20v1'):
    cfg=VARIANTS[variant]
    bundle=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))
    if cfg.get('observed_demand'):
        parent_source=(ROOT/'submission/submission_codex_e18_770_v48_external.py').read_text()
        tree=ast.parse(parent_source)
        candidates=[n.args[0].value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='compile' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and n.args[0].value.startswith('"""Observation-driven crop succession experiment')]
        assert len(candidates)==1
        succession_source=candidates[0]
        anchor="            inventory=core.market['inventory'][c]+supply"
        assert succession_source.count(anchor)==1
        succession_source=succession_source.replace(anchor,anchor+'-observed_town_demand(core,c,d)')
        succession=sys.modules['_v48pkg.portfolio_succession_v14']
        succession.observed_town_demand=observed_town_demand
        scope=dict(succession.__dict__)
        exec(compile(succession_source,'<e20-demand>','exec'),scope)
        succession.install.__code__=scope['install'].__code__
    if cfg.get('water_rescue') or cfg.get('remote_first'):
        routes=sys.modules['_v48pkg.daily_routes_770_v48']
        route_source=(ROOT/'docs/model_specs/codex/e19/tools/daily_routes_770_v48.py').read_text()
        route_source=route_source.replace('docs.model_specs.codex.e19.tools.','_v48pkg.')
        if cfg.get('water_rescue'):
            old='rescue=rescue or final_water_deadline(core.day,tile,commands)'
            assert route_source.count(old)==1
            route_source=route_source.replace(old,old+" or productive_water_deadline(core.day,tile,commands,core.__call__.__func__.__globals__['CROPS'],core.turns,core.final_day)")
            routes.productive_water_deadline=productive_water_deadline
        if cfg.get('remote_first'):
            old='sorted(offers,key=lambda o:(-o[2],o[0]))'
            assert route_source.count(old)==1
            route_source=route_source.replace(old,'sorted(offers,key=lambda o:(-o[2],-min(distance(p,o[0]) for p in positions),o[0]))')
        if cfg.get('late_hourly_routes'):
            assert route_source.count('core.hour//6')==2
            route_source=route_source.replace('core.hour//6','(core.hour if core.day>=19 else core.hour//6)')
        if cfg.get('late_closing'):
            anchor='            rescue=rescue or final_water_deadline(core.day,tile,commands)'
            assert route_source.count(anchor)==1
            route_source=route_source.replace(anchor,anchor+"\n            rescue=rescue or (19<=core.day<29 and core.remaining<=6 and commands and all(c[0] in {'FEED','WATER','CARE','HARVEST','COLLECT_FERTILIZER','FERTILIZE'} for c in commands))")
        if cfg.get('late_transfer'):
            anchor='        core.daily_route_state=dict(day=core.day+1,remaining={str(w):list(q) for w,q in queues.items()})'
            assert route_source.count(anchor)==1
            transfer="""        if 19<=core.day<29:
            for worker in range(len(core.positions)):
                if worker in core.active or queues.get(worker):continue
                choices=[]
                for donor,queue in queues.items():
                    if donor==worker:continue
                    route=[by_target[t] for t in queue if t in by_target and t not in claimed]
                    start=core.positions[donor]
                    active=core.active.get(donor)
                    if active and active['steps']:start=active['steps'][-1][1]
                    inv=core.private['inventories'][donor]
                    before=route_cost(start,route,core.sheds,inv)
                    for index,offer in enumerate(route):
                        target,commands,priority,value,kind=offer
                        if kind!='SERVICE' or target in claimed:continue
                        steps=prepare(worker,target,commands)
                        if steps is None or len(steps)>core.remaining-1:continue
                        after=route_cost(start,route[:index]+route[index+1:],core.sheds,inv)
                        saving=before-after-len(steps)
                        if saving>0:choices.append((-priority,-saving,len(steps),target,donor))
                if choices:
                    _,saving,cost,target,donor=min(choices)
                    queues[donor].remove(target)
                    queues[worker]=[target]
                    core.daily_route_log.append(dict(day=core.day+1,hour=core.hour+1,event='late_transfer',worker=worker,donor=donor,target=target,estimated_saved_steps=-saving,recipient_steps=cost))
"""
            route_source=route_source.replace(anchor,transfer+anchor)
        route_scope=dict(routes.__dict__)
        exec(compile(route_source,str(Path(__file__)),'exec'),route_scope)
        routes.install.__code__=route_scope['install'].__code__
        routes.pack_routes.__code__=route_scope['pack_routes'].__code__
    module=sys.modules['_v48pkg.biological_plan_770_v48']
    source=(ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py').read_text()
    source=source.replace('docs.model_specs.codex.e19.tools.','_v48pkg.')
    if cfg.get('useful_care'):
        old="(core.day<27 or care_value(t,core.day,core.final_day,r,core._quote)>0)"
        assert source.count(old)==1
        source=source.replace(old,'care_can_add_yield(t,core.day,core.final_day,r)')
        module.care_can_add_yield=care_can_add_yield
    if cfg.get('late_care_floor'):
        old='care_can_add_yield(t,core.day,core.final_day,r)'
        assert source.count(old)==1
        source=source.replace(old,"(care_can_add_yield(t,core.day,core.final_day,r) and care_market_allows(core.day,core.market.get('prices',{}),r['product']))")
        module.care_market_allows=care_market_allows
    if cfg.get('economic_short_cycle'):
        old="            tile=core._tile(pos)\n            if core.day>=25:"
        assert source.count(old)==1
        source=source.replace(old,"            tile=core._tile(pos)\n            intended=choose_short_cycle(core,intended,rules,cash)\n            if core.day>=25:")
        module.choose_short_cycle=choose_short_cycle
    if not cfg.get('preserve'):
        source=source.replace("targets={'WHEAT':23,'STRAWBERRY':38}","targets={'WHEAT':23,'STRAWBERRY':36}")
        source=source.replace("if pos in intentions or isinstance(tile,dict)","if pos in core.e20_reserved or pos in intentions or isinstance(tile,dict)")
    source=source.replace("if pos in claims:continue\n            tile=core._tile(pos)","if pos in core.e20_reserved or pos in claims:continue\n            tile=core._tile(pos)")
    source=source.replace("result=[o for o in offers if o[4]=='NEW_ANIMAL']", "result=[o for o in offers if o[4]=='NEW_ANIMAL' and tuple(o[0]) not in core.e20_reserved and o[0][1]<5]")
    needle="                    if t.get('yield_units',0):commands.append(['HARVEST']);value+=core._quote(r['product'],'SELL',t['yield_units'])"
    if any(k in cfg for k in ['q2care','q2care_price','q2care_until']):
        assert source.count(needle)==1
        source=source.replace(needle,"                    if pos in core.e20_reserved and (not core.e20_care or core._quote(r['product'],'SELL',1)<core.e20_care_price or core.day>=core.e20_care_until):commands=[c for c in commands if c[0]!='CARE']\n"+needle)
    if cfg.get('q2crop'):
        needle='        calendar=[]'
        assert source.count(needle)==1
        source=source.replace(needle,"        for pos in intentions:\n            if pos[1]>=5 and pos not in core.e20_reserved:intentions[pos]=core.e20_q2crop\n"+needle)
    needle='        return result\n    def planned_prepare'
    addition='''        if core.day>=core.e20_start:
            for pos,species in core.e20_reserved.items():
                tile=core._tile(pos)
                if pos in claims or tile=='LOCKED' or isinstance(tile,dict) and tile.get('animal'):continue
                price=rules['ANIMALS'][species]['cost']
                if cash<price+core._quote('WHEAT','BUY',2):continue
                if isinstance(tile,dict) and tile.get('kind')=='PLANT':continue
                commands=[['DIG']] if isinstance(tile,dict) and tile.get('kind')=='WEED' else []
                if not isinstance(tile,dict) or tile.get('kind')!='PASTURE':commands.append(['BUILD_PASTURE'])
                commands += [['PLACE',species],['FEED'],['CARE']]
                result.append((pos,commands,4,core.animal_values[species]['gain'],'NEW_ANIMAL'))
        return result
    def planned_prepare'''
    assert source.count(needle)==1
    source=source.replace(needle,addition)
    scope=dict(module.__dict__)
    exec(compile(source,str(Path(__file__)),'exec'),scope)
    # Preserve the function references already imported by the frozen bundle.
    module.install.__code__=scope['install'].__code__
    original=bundle['_base'].create_agent
    def base(context):
        p=original(context)
        if cfg.get('conditional_sell'):
            conservative=p.core.envelope.conservative
            def conditional(item,operation,unit_quotes):
                return sum(unit_quotes) if operation=='SELL' else conservative(item,operation,unit_quotes)
            p.core.envelope.conservative=conditional
        if cfg.get('water_deadline'):
            routes=sys.modules['_v48pkg.daily_routes_770_v48']
            terminal_deadline=routes.final_water_deadline
            def deadline(day,tile,commands):
                return terminal_deadline(day,tile,commands) or productive_water_deadline(
                    day,tile,commands,p.core.__call__.__func__.__globals__['CROPS'],p.core.turns,p.core.final_day)
            routes.final_water_deadline=deadline
        p.core.profile=replace(p.core.profile,target=16,maximum_hands=cfg.get('hands',12),mix_weights=cfg.get('animal_mix',(('COW',9+cfg['species'].count('COW')),('SHEEP',5+cfg['species'].count('SHEEP')))))
        p.core.e20_reserved=dict(zip(cfg['positions'],cfg['species']))
        p.core.e20_start=cfg['start']
        p.core.e20_q2crop=cfg.get('q2crop')
        p.core.e20_care=cfg.get('q2care',True)
        p.core.e20_care_price=cfg.get('q2care_price',0)
        p.core.e20_care_until=cfg.get('q2care_until',30)
        # Keep the assisted opening's 770 governor exactly as E19 through D11.
        return p
    bundle['_base'].create_agent=base
    policy=bundle['create_agent'](context)
    if cfg.get('observed_demand'):policy=ObservedDemandPolicy(policy)
    if 'teacher_hours' not in cfg:return policy
    return Q2TeacherBridge(policy,cfg['teacher_hours'])

class Q2TeacherBridge:
    """Finish the bounded E18 Q2 opening, then hand observed state to V48."""
    def __init__(self,policy,hours):
        self.policy=policy
        self.hours=hours
        self.core=policy.core
        self.configured=False

    def __call__(self,obs,cfg):
        p=self.policy
        if obs['day']==11 and obs['hour']<self.hours:
            if not self.configured:
                t=p.teacher.codex_e18_capacity_governed_instance
                t.dense_targets=frozenset(pos for pos in t.dense_targets if pos[1]<5 or pos in p.core.e20_reserved)
                t._apply_reclaim_envelope()
                t.livestock_resource_cap=16
                t.config['pre_q2_livestock_resource_cap']=16
                p.profile=p.core.profile
                self.configured=True
            p.assisted_days=12
        else:p.assisted_days=11
        return p(obs,cfg)
