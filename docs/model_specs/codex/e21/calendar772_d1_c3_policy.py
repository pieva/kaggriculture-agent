"""D1 observed-state execution of a frozen historical biological timetable.

The timetable contains dates and locations, never future prices or observations.
This diagnostic changes opening execution as well as calendar and staffing.
"""
from pathlib import Path
from dataclasses import replace
import json
import runpy

ROOT = Path(__file__).resolve().parents[4]
CALENDAR_PATH = Path(__file__).parent/'reports/calendar772_d1/CALENDAR.json'


def create_agent(context=None):
    data = json.loads(CALENDAR_PATH.read_text(encoding='utf-8'))
    bundle = runpy.run_path(str(ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py'))
    planner = bundle['create_agent'](context)
    planner.assisted_days = 0
    core = planner.core
    old_services, old_market = core._services, core._market_orders
    crops = core.__call__.__func__.__globals__['CROPS']
    animals = {tuple(x['position']):x for x in data['animals']}
    goals = {}
    for row in data['plants']:
        goals.setdefault(tuple(row['position']), []).append(row)
    for rows in goals.values():
        rows.sort(key=lambda r:r['day'])
    harvest = {(tuple(r['position']), r['day']) for r in data['harvest']}
    core.calendar_events = []
    completed = set()

    def services():
        result = []
        for pos, commands, priority, value, kind in old_services():
            tile = core._tile(pos)
            if isinstance(tile, dict) and tile.get('crop'):
                commands = [c for c in commands if c[0] != 'HARVEST']
                due = any(p == tuple(pos) and d <= core.day and d >= tile['planted_day'] for p,d in harvest)
                if tile.get('yield_units', 0) and due and core.day >= tile['planted_day'] + crops[tile['crop']]['first_yield_day']:
                    commands.append(['HARVEST'])
                    priority = max(priority, 4)
            if commands:
                result.append((pos, commands, priority, value, kind))
        offered = {tuple(o[0]) for o in result}
        claims = {tuple(j['target']) for j in core.active.values() if j['kind'] != 'DELIVER'}
        for y,row in enumerate(core.farm['tiles']):
            for x,tile in enumerate(row):
                pos = (x,y)
                if pos in offered or pos in claims or not isinstance(tile,dict) or not tile.get('crop') or not tile.get('yield_units',0):
                    continue
                if core.day >= tile['planted_day'] + crops[tile['crop']]['first_yield_day'] and any(p == pos and tile['planted_day'] <= d <= core.day for p,d in harvest):
                    result.append((pos,[['HARVEST']],4,1,'SERVICE'))
        return result

    def growth(cash):
        result = []
        if core.day >= 28:
            return result
        claims = {tuple(j['target']) for j in core.active.values() if j['kind'] != 'DELIVER'}
        for pos, row in animals.items():
            if core.day < row['day'] or pos in claims:
                continue
            tile = core._tile(pos)
            if tile == 'LOCKED' or isinstance(tile, dict) and tile.get('animal'):
                continue
            if isinstance(tile, dict) and tile.get('kind') == 'PLANT':
                continue
            commands = [['DIG']] if isinstance(tile, dict) and tile.get('kind') == 'WEED' else []
            if not isinstance(tile, dict) or tile.get('kind') != 'PASTURE':
                commands.append(['BUILD_PASTURE'])
            commands += [['PLACE', row['species']], ['FEED'], ['CARE']]
            cost = 400 if row['species'] == 'COW' else 500
            if cash >= cost + core._quote('WHEAT', 'BUY', 1):
                result.append((pos, commands, 7, 1, 'NEW_ANIMAL'))
        for pos, rows in goals.items():
            due = [r for r in rows if r['day'] <= core.day]
            if not due or pos in claims:
                continue
            goal = due[-1]
            if (pos,goal['day']) in completed:
                continue
            if pos in animals and core.day >= animals[pos]['day']:
                continue
            tile = core._tile(pos)
            crop = goal['crop']
            if tile == 'LOCKED' or cash < crops[crop]['seed']:
                continue
            commands = []
            if isinstance(tile, dict):
                if tile.get('kind') == 'WEED':
                    commands = [['DIG']]
                elif tile.get('crop'):
                    if tile['planted_day'] >= goal['day']:
                        completed.add((pos,goal['day']))
                        continue
                    rule = crops[tile['crop']]
                    if core.day < tile['planted_day'] + rule['first_yield_day']:
                        continue
                    if tile.get('yield_units', 0):
                        commands.append(['HARVEST'])
                    if rule['ongoing']:
                        # Never remove an unexhausted perennial to catch up.
                        end = tile['planted_day'] + rule['first_yield_day'] + (rule['max_yield']-1)*rule['interval']
                        if core.day < end:
                            continue
                        commands.append(['DIG'])
                else:
                    continue
            if core.day + crops[crop]['first_yield_day'] > core.final_day-1:
                continue
            commands += [['PLANT', crop], ['WATER']]
            result.append((pos, commands, 4, 1, 'NEW_CROP'))
        return result

    def market():
        target = data['daily'][core.day]
        core.profile = replace(core.profile, maximum_hands=target['people']-1)
        orders = [o for o in old_market() if o[0] not in ('HIRE', 'BUY_LAND')]
        budget = float(core.farm['money'])
        for order in orders:
            op, item, quantity = order
            if op == 'SELL':
                budget += core._quote(item, 'SELL', quantity)
            elif op == 'BUY_PRODUCT':
                budget -= core._quote(item, 'BUY', quantity)
            elif op == 'BUY_SEED':
                budget -= crops[item]['seed']*quantity
            elif op == 'BUY_ANIMAL':
                budget -= (400 if item == 'COW' else 500)*quantity
        if core.remaining > 3:
            for i in range(len(core.farm['hands']), target['people']-1):
                a,b = 1,1
                for _ in range(i):
                    a,b = b,a+b
                cost = a*core.hire_mult
                if len(orders) >= 10 or budget < cost:
                    break
                orders.append(['HIRE'])
                budget -= cost
        count = len(core.farm['unlocked_quadrants'])
        cost = 1000*2**(count-1)
        if count < target['land'] and len(orders) < 10 and budget >= cost + core.feed_reserve:
            orders.append(['BUY_LAND'])
        return orders

    core._services = services
    core._growth = growth
    core._market_orders = market
    return planner
