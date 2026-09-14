"""E23S: local E23 v1, fixed portfolio on repaired E22 routes. No future information."""
import base64,zlib,json,copy
_PLAN=json.loads(zlib.decompress(base64.b64decode('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')))

_TARGETS = {(2, 3), (3, 2), (4, 1), (6, 4), (5, 2)}
_EVOLVED = {(6, 4), (5, 2)}
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
            if len(order)>2 and order[0]=='SELL' and order[1] in ('WOOL',):
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
