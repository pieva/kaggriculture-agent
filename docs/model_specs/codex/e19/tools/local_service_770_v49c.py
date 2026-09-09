"""770 V49C candidate: useful same-tile service after the normal dispatcher idles.

Only provisional route ownership may be bypassed. Active missions, carried
inputs, biological utility, remaining time and existing delivery guards remain.
No additional travel, investment, fertilizer collection or staffing changes.
"""
from copy import deepcopy
from types import FunctionType
from docs.model_specs.codex.e19.tools.daily_routes_770_v48 import yield_water_units, harvest_due
from docs.model_specs.codex.e19.tools.portfolio_workforce_v16 import care_value


def useful_commands(tile, commands, day, final_day, rules, quote):
    if not isinstance(tile,dict):return []
    result=[]
    for cmd in commands:
        op=cmd[0]
        if op=='FEED':
            if tile.get('animal') and day<final_day and not tile.get('fed_today'):result.append(cmd)
        elif op=='CARE':
            if (tile.get('animal') and (tile.get('fed_today') or ['FEED'] in result)
                    and care_value(tile,day,final_day,rules['ANIMALS'][tile['animal']],quote)>0):result.append(cmd)
        elif op=='WATER' and tile.get('kind')=='PLANT' and not tile.get('watered_today'):
            r=rules['CROPS'][tile['crop']]
            age=day-tile['planted_day']
            future=(age<r['first_yield_day']+(r['max_yield']-1)*r['interval']) if r['ongoing'] else age<=r['max_yield_day']
            needed=day<final_day and tile.get('consecutive_unwatered',0)>=1 and (future or tile.get('yield_units',0)>0)
            if needed or yield_water_units(tile,day,rules['CROPS'])>0:result.append(cmd)
        elif op=='HARVEST' and tile.get('yield_units',0)>0:
            if tile.get('animal'):result.append(cmd)
            elif tile.get('kind')=='PLANT':
                r=rules['CROPS'][tile['crop']];age=day-tile['planted_day']
                if age>=r['first_yield_day'] and (r['ongoing'] or age>=r['max_yield_day'] or harvest_due(tile,day)):
                    result.append(cmd)
    # Preserve productive WATER + HARVEST as one visit; don't water terminal
    # annuals unless the observed offer also includes collection.
    if day==final_day and ['WATER'] in result and ['HARVEST'] not in result:return []
    return result


def install(core):
    route_prepare=core._prepare_steps
    cells=dict(zip(route_prepare.__code__.co_freevars,(c.cell_contents for c in route_prepare.__closure__)))
    assert 'prepare' in cells and 'queues' in cells, 'Install once after the V48 scheduler'
    prepare=cells['prepare']
    services=core._services
    call=core.__class__.__call__
    rules=core.__call__.__func__.__globals__
    latest=[]
    core.v49_recovery_log=[]
    def observed_services():
        nonlocal latest
        latest=services()
        return latest
    core._services=observed_services
    def dispatch(self,obs,cfg):
        action=call(self,obs,cfg)
        commands=[action['farmer'],*action['hands']]
        claimed={tuple(j['target']) for j in self.active.values() if j['kind']!='DELIVER'}
        for worker,command in enumerate(commands):
            if command!=['PASS'] or worker in self.active or self.remaining!=1:continue
            target=tuple(self.positions[worker])
            if target in claimed:continue
            for pos,cmds,priority,value,kind in latest:
                if tuple(pos)!=target or kind not in {'SERVICE','BIOLOGICAL'}:continue
                tile=self._tile(target)
                if not isinstance(tile,dict) or not tile.get('animal') or not tile.get('fed_today'):continue
                useful=[c for c in useful_commands(tile,cmds,self.day,self.final_day,rules,self._quote) if c[0]=='CARE']
                if not useful:continue
                steps=prepare(worker,target,useful,buy=False,requirements=self._requirements()[0])
                if not steps or len(steps)!=1 or any(cmd[0] not in {'FEED','CARE','WATER','HARVEST'} for cmd,p in steps):continue
                self.active[worker]=dict(target=target,steps=steps,kind='SERVICE')
                cmd,pos=steps[0]
                commands[worker]=cmd
                self.previous[worker]=(cmd,pos,dict(self.private['inventories'][worker]))
                claimed.add(target)
                self.metrics['v49_local_recovery']+=1
                self.daily_metrics[self.day+1]['PASS']-=1
                self.daily_metrics[self.day+1][cmd[0]]+=1
                self.v49_recovery_log.append(dict(day=self.day+1,hour=self.hour+1,worker=worker,target=target,commands=deepcopy(useful)))
                break
        action['farmer'],action['hands']=commands[0],commands[1:]
        return action
    dispatch=FunctionType(dispatch.__code__,{**dispatch.__globals__,**rules,
        'useful_commands':useful_commands},dispatch.__name__,dispatch.__defaults__,dispatch.__closure__)
    core.__class__=type('LocalService770V49C',(core.__class__,),{'__call__':dispatch})
