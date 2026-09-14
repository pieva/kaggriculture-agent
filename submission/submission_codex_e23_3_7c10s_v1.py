"""E23M: local E23 v1, fixed portfolio on repaired E22 routes. No future information."""
import base64,zlib,json,copy
_PLAN=json.loads(zlib.decompress(base64.b64decode('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')))

_TARGETS = {(2, 3), (3, 2), (4, 1), (6, 4)}
_EVOLVED = {(6, 4)}
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
