"""E23G: local E23 v1, fixed portfolio on repaired E22 routes. No future information."""
import base64,zlib,json,copy
_PLAN=json.loads(zlib.decompress(base64.b64decode('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')))

_TARGETS = {(6, 2)}
_EVOLVED = {(6, 2)}
_SERVICE = {'FEED', 'CARE', 'HARVEST', 'COLLECT_FERTILIZER', 'PASS'}

class PublishedAgent:
    def __init__(self, context=None): pass
    def __call__(self, obs, cfg=None):
        day,hour=int(obs['day']),int(obs['hour'])
        i=day*24+hour
        if not 0<=i<len(_PLAN):
            return {'farmer':['PASS'],'hands':[],'market':[]}
        action=copy.deepcopy(_PLAN[i])
        farm=obs['farms'][int(obs['player'])]
        projected={}
        for w,(pos,cmd) in enumerate(zip([farm['farmer']]+farm['hands'],[action['farmer']]+action['hands'])):
            xy=tuple(pos)
            if xy not in _TARGETS or not cmd or cmd[0] not in _SERVICE:continue
            if xy not in projected:projected[xy]=copy.deepcopy(farm['tiles'][pos[1]][pos[0]])
            tile=projected[xy]
            if not isinstance(tile,dict) or not tile.get('animal'):continue
            inv=obs['private']['inventories'][w]
            op='PASS'
            if day<29 and not tile.get('fed_today') and inv.get('WHEAT',0):
                op='FEED';tile['fed_today']=True
            elif xy in _EVOLVED and tile.get('yield_units',0):
                op='HARVEST';tile['yield_units']=0
            elif day<29 and not tile.get('cared_today'):
                op='CARE';tile['cared_today']=True
            elif tile.get('yield_units',0):
                op='HARVEST';tile['yield_units']=0
            elif tile.get('fertilizer_available'):
                op='COLLECT_FERTILIZER';tile['fertilizer_available']=False
            cmd[:]=[op]
        for order in action['market']:
            if len(order)>2 and order[0]=='SELL' and order[1] in ('MILK',):
                order[2]=100
        return action

class Agent(PublishedAgent):
    """E23 evolution v1: observation-based recovery, with the published routes intact."""

    def __call__(self, obs, cfg=None):
        action = super().__call__(obs, cfg)
        day, hour = int(obs['day']), int(obs['hour'])
        index = day * 24 + hour
        if not 0 <= index < len(_PLAN):
            return action
        cfg = cfg or {}
        farm = obs['farms'][int(obs['player'])]
        private = obs['private']
        tiles = copy.deepcopy(farm['tiles'])
        shed = dict(private['shed'])
        inventories = copy.deepcopy(private['inventories'])
        seeds = dict(private['seeds'])
        commands = [action['farmer']] + action['hands']
        positions = [farm['farmer']] + farm['hands']
        size = int(cfg.get('boardSize', 10))
        access = {(size // 2 - 1, size // 2 - 1),
                  (size // 2, size // 2 - 1),
                  (size // 2, size // 2), (size // 2 - 1, size // 2)}
        products = ('MILK', 'WOOL', 'EGG', 'MELON', 'STRAWBERRY',
                    'CARROT', 'TOMATO', 'FERTILIZER', 'WHEAT')
        advance_wheat_seed = False
        wheat_replanted = False
        # Project stock and same-tile service in worker execution order.
        for worker, (pos, cmd) in enumerate(zip(positions, commands)):
            x, y = pos
            tile = tiles[y][x]
            inv = inventories[worker]
            op = cmd[0]
            animal = tile.get('animal') if isinstance(tile, dict) else None
            # Three closing slots at D16 (9,0) used WATER/HARVEST/PLANT,
            # leaving the new seed to die unwatered at the refresh. Harvest
            # the already mature wheat one slot earlier, then plant and water.
            if day == 15 and tuple(pos) == (9, 0):
                if hour == 21 and op == 'WATER' and isinstance(tile, dict) and tile.get('crop') == 'WHEAT' and day - tile.get('planted_day', day) >= 2 and tile.get('yield_units', 0):
                    cmd[:] = ['HARVEST']
                    advance_wheat_seed = True
                elif hour == 22 and op == 'HARVEST' and tile is None:
                    cmd[:] = ['PLANT', 'WHEAT']
                elif hour == 23 and op == 'PLANT' and isinstance(tile, dict) and tile.get('crop') == 'WHEAT' and tile.get('planted_day') == day:
                    cmd[:] = ['WATER']
            # This strawberry has no D22 visit. Water on D21 and retain its
            # fruit for the next collection, instead of losing the whole plant.
            if day == 20 and tuple(pos) == (8, 2) and op == 'HARVEST' and isinstance(tile, dict) and tile.get('crop') == 'STRAWBERRY' and not tile.get('watered_today'):
                cmd[:] = ['WATER']
            op = cmd[0]
            # Clear a weed in an existing idle slot before PLANT, when available,
            # so that the scheduled watering slot is preserved as well.
            weed = tile == 'WEED' or isinstance(tile, dict) and tile.get('kind') == 'WEED'
            if op == 'PASS' and weed and hour < 23 and index + 1 < len(_PLAN):
                following = [_PLAN[index + 1]['farmer']] + _PLAN[index + 1]['hands']
                if worker < len(following) and following[worker][0] == 'PLANT':
                    cmd[:] = ['DIG']
            # D2 emergency financing can consume the last shed grain. Worker 2
            # returns to the central cow after the scheduled grain purchases.
            # Feed there, then use the sheep's idle service slot to catch up:
            # both animals eat and the route rejoins its calendar at H16.
            if day == 1 and worker == 2 and tuple(pos) == (4, 4) and animal == 'COW':
                if hour == 12 and not tile.get('fed_today'):
                    cmd[:] = ['PICKUP', 'WHEAT', 2]
                elif hour == 13 and not tile.get('fed_today') and inv.get('WHEAT'):
                    cmd[:] = ['FEED']
                elif hour == 14:
                    cmd[:] = ['WEST']
                op = cmd[0]
            if op == 'PLANT' and tile == 'WEED':
                cmd[:] = ['DIG']
            elif op == 'PLANT' and isinstance(tile, dict) and tile.get('kind') == 'WEED':
                cmd[:] = ['DIG']
            elif op == 'WATER' and tile is None and hour > 0:
                prev = [_PLAN[index - 1]['farmer']] + _PLAN[index - 1]['hands']
                if worker < len(prev) and prev[worker][0] == 'PLANT':
                    cmd[:] = list(prev[worker])
            if animal and day < 29 and (
                op == 'PASS' or
                op == 'CARE' and tile.get('cared_today') or
                op == 'FEED' and (tile.get('fed_today') or not inv.get('WHEAT')) or
                op == 'HARVEST' and not tile.get('yield_units')
            ):
                if not tile.get('fed_today') and inv.get('WHEAT', 0):
                    cmd[:] = ['FEED']
                elif not tile.get('cared_today'):
                    cmd[:] = ['CARE']
                else:
                    cmd[:] = ['PASS']
            if op == 'PASS' and isinstance(tile, dict) and tile.get('kind') == 'PLANT' and not tile.get('watered_today'):
                cmd[:] = ['WATER']
            # The final refresh is not executed: explicitly deliver idle workers' stock.
            if day == 29 and tuple(pos) in access and sum(inv.values()) and op == 'PASS':
                cmd[:] = ['DROP']
            op = cmd[0]
            if op == 'PLANT':
                crop = cmd[1]
                if tile is not None or seeds.get(crop, 0) <= 0:
                    cmd[:] = ['PASS']
                else:
                    seeds[crop] -= 1
                    tiles[y][x] = {'kind': 'PLANT', 'crop': crop, 'watered_today': False}
                    if day == 15 and hour == 22 and tuple(pos) == (9, 0) and crop == 'WHEAT':
                        wheat_replanted = True
            elif op == 'DIG' and not animal and tile != 'LOCKED':
                tiles[y][x] = None
            elif op == 'PICKUP' and tuple(pos) in access:
                item = cmd[1]
                n = min(shed.get(item, 0), int(cmd[2]) if len(cmd) > 2 else 1)
                shed[item] = shed.get(item, 0) - n
                inv[item] = inv.get(item, 0) + n
            elif op == 'FEED' and animal and not tile.get('fed_today') and inv.get('WHEAT', 0):
                inv['WHEAT'] -= 1
                tile['fed_today'] = True
            elif op == 'CARE' and animal:
                tile['cared_today'] = True
            elif op == 'WATER' and isinstance(tile, dict) and tile.get('kind') == 'PLANT':
                tile['watered_today'] = True
            elif op == 'COLLECT_FERTILIZER' and animal and tile.get('fertilizer_available'):
                inv['FERTILIZER'] = inv.get('FERTILIZER', 0) + 1
                tile['fertilizer_available'] = False
            elif op == 'FERTILIZE' and isinstance(tile, dict) and tile.get('kind') == 'PLANT' and inv.get('FERTILIZER'):
                inv['FERTILIZER'] -= 1
            elif op == 'HARVEST' and isinstance(tile, dict) and tile.get('yield_units', 0):
                crop = tile.get('crop')
                first = {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 8, 'STRAWBERRY': 10, 'MELON': 10}
                if animal or crop in first and day - tile.get('planted_day', day) >= first[crop]:
                    item = {'COW': 'MILK', 'SHEEP': 'WOOL', 'GOOSE': 'EGG'}.get(animal, crop)
                    inv[item] = inv.get(item, 0) + tile['yield_units']
                    tile['yield_units'] = 0
                    if crop in ('WHEAT', 'CARROT', 'MELON'):
                        tiles[y][x] = None
            elif op == 'DROP' and tuple(pos) in access:
                for item, n in inv.items():
                    shed[item] = shed.get(item, 0) + n
                inv.clear()
            elif op == 'PLACE' and len(cmd) > 1:
                item = cmd[1]
                if item in ('COW', 'SHEEP', 'GOOSE') and isinstance(tile, dict) and tile.get('kind') == ('COOP' if item == 'GOOSE' else 'PASTURE') and not animal and inv.get(item):
                    inv[item] -= 1
                    tile['animal'] = item
                elif tuple(pos) in access:
                    n = min(inv.get(item, 0), int(cmd[2]) if len(cmd) > 2 else 1)
                    inv[item] = inv.get(item, 0) - n
                    shed[item] = shed.get(item, 0) + n
        market = action['market']
        # Move the seed purchase with the earlier sowing. Otherwise the two
        # other D16 H23 requests consume the available seeds before worker 10.
        if advance_wheat_seed and len(market) < int(cfg.get('maxMarketOrdersPerTurn', 10)):
            market.append(['BUY_SEED', 'WHEAT', 1])
        if wheat_replanted:
            for order in market:
                if len(order) > 2 and order[:2] == ['BUY_SEED', 'WHEAT']:
                    order[2] -= 1
                    break
            market[:] = [o for o in market if not (len(o) > 2 and o[2] == 0)]
        # Unit actions precede the market. Finance the hiring batch before HIRE,
        # using only stock still in the shed after this turn's pickups.
        hires = sum(bool(order) and order[0] == 'HIRE' for order in market)
        a, b = 1, 1
        costs = []
        for n in range(int(farm['hires_today']) + hires):
            costs.append(a * int(cfg.get('farmHandCostMult', 1)))
            a, b = b, a + b
        deficit = max(0, sum(costs[int(farm['hires_today']):]) - farm['money'])
        extra = []
        if deficit and hires:
            for item in products:
                # A unit sells for at least one credit, including under adverse prices.
                n = min(shed.get(item, 0), int(deficit + .999999))
                if n:
                    extra.append(['SELL', item, n])
                    shed[item] -= n
                    deficit -= n
                if deficit <= 0:
                    break
        # Close the day with room for all carried harvest, rather than silently
        # discarding wool at the automatic inventory return. Reserve next-day grain.
        if hour >= 22:
            stock = sum(shed.values()) + sum(sum(inv.values()) for inv in inventories)
            excess = max(0, stock - int(cfg.get('shedCapacity', 100)))
            for order in market:
                if len(order) > 2 and order[0] == 'SELL':
                    excess -= min(shed.get(order[1], 0), order[2])
            for item in products:
                reserve = 24 if item == 'WHEAT' and day < 29 else 0
                n = min(max(0, shed.get(item, 0) - reserve), max(0, excess))
                if n:
                    extra.append(['SELL', item, n])
                    excess -= n
        limit = int(cfg.get('maxMarketOrdersPerTurn', 10))
        # Existing orders retain their relative order. Never truncate planned hires.
        action['market'] = extra[:max(0, limit - len(market))] + market
        if day == 29:
            for item in products:
                if shed.get(item, 0) and len(action['market']) < limit:
                    action['market'].append(['SELL', item, 1000])
        return action


def create_agent(context=None):
    return Agent(context)


_AGENT = Agent()


def agent(observation, configuration=None):
    return _AGENT(observation, configuration)
