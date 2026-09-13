"""Apply the recurring external placement/harvest calendar to the 8C9S arm."""
from pathlib import Path
import hashlib
from build_q0_pastures import BASE, POLICY

OUT = BASE.parent / 'submission_codex_e22_q0_8c9s_calendar_v2.py'

PATCH = '''
# D12: move the single sheep purchase from H2 to H1 so worker 1 can
# collect it at H2. Existing H2 hires retain their actual spawn positions.
_PLAN[264]['market'].append(['BUY_ANIMAL', 'SHEEP', 1])
_PLAN[265]['market'] = [([] if c[:2] == ['BUY_ANIMAL', 'SHEEP'] else c) for c in _PLAN[265]['market']]
_ROUTE = [
 ['PICKUP','SHEEP'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'],
 ['PLACE','SHEEP'], ['SOUTH'], ['EAST'], ['EAST'], ['DROP'],
 ['PICKUP','WHEAT',2], ['WEST'], ['FEED'], ['CARE'], ['WEST'],
 ['WEST'], ['FEED'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'],
 ['PLANT','WHEAT'], ['WATER']]
for _hour, _command in enumerate(_ROUTE, 2):
 _PLAN[264 + _hour - 1]['hands'][0] = _command
# Worker 6 keeps his original route and grain supply; delivery is now
# already done by worker 1. Reuse the old PLACE slot for sheep service.
_PLAN[268]['hands'][5] = ['PASS']
_PLAN[275]['hands'][5] = ['PASS']
_HARVEST_DAYS = {(4,1): {17,20,23,26,29}, (3,2): {17,20,23,26,29},
                 (2,3): {18,21,24,27,30}}
'''

def main():
    policy = POLICY.replace("_TARGETS =", PATCH + "\n_TARGETS =", 1)
    policy = policy.replace("if day < 29 and not tile['fed_today'] and inv.get('WHEAT', 0):",
        "if day + 1 in _HARVEST_DAYS[xy] and tile.get('yield_units', 0):\n    op = 'HARVEST'; tile['yield_units'] = 0\n   elif day < 29 and not tile['fed_today'] and inv.get('WHEAT', 0):")
    # Positive yields are harvested on calendar days, or on D30 as recovery;
    # no empty harvest request can displace care/feeding.
    policy = policy.replace("elif tile.get('yield_units', 0):", "elif day == 29 and tile.get('yield_units', 0):")
    policy = policy.replace("  return action\n", "  if day == 11 and hour == 10:\n   milk = private['inventories'][1].get('MILK', 0) if len(private['inventories']) > 1 else 0\n   if milk: action['market'].append(['SELL', 'MILK', milk])\n  return action\n")
    source = BASE.read_text(encoding='utf-8').split('class Agent:')[0]
    source = source.replace('E22 internal baseline: observed constant plan, s56165462 56165462.',
        'E22 Q0 8C9S calendar v2: recurring external placement and harvest days.')
    source = source.replace('Uses only current day/hour. No future observations or replay outcomes.',
        'Calendar from observed public actions; current-state service checks. No future data.')
    OUT.write_text(source + policy, encoding='utf-8')
    ns = {}; exec(OUT.read_text(encoding='utf-8'), ns)
    assert len(ns['_PLAN']) == 719 and len(ns['_ROUTE']) == 23
    print(OUT.name, hashlib.sha256(OUT.read_bytes()).hexdigest())

if __name__ == '__main__': main()
