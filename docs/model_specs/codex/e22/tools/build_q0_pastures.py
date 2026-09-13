"""Build a standalone, narrow 8C9S arm without changing frozen E22."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'submission/submission_codex_e22_s56165462_observed_v1.py'
OUT = ROOT / 'submission/submission_codex_e22_q0_8c9s_internal_v1.py'

POLICY = '''
# Three original Q0 construction slots: D11 H15, H19, H20.
for _i in (254, 258, 259):
 _a = _PLAN[_i]
 _commands = [_a['farmer']] + _a['hands']
 assert sum(c == ['BUILD_COOP'] for c in _commands) == 1
 for _c in _commands:
  if _c == ['BUILD_COOP']: _c[0] = 'BUILD_PASTURE'
for _a in _PLAN:
 for _c in [_a['farmer']] + _a['hands'] + _a['market']:
  if len(_c) > 1:
   if _c[1] == 'GOOSE': _c[1] = 'SHEEP'
   elif _c[1] == 'EGG': _c[1] = 'WOOL'

_TARGETS = {(4, 1), (3, 2), (2, 3)}
_SERVICE = {'FEED', 'CARE', 'HARVEST', 'COLLECT_FERTILIZER', 'PASS'}

class Agent:
 def __init__(self, context=None): pass
 def __call__(self, obs, cfg=None):
  day, hour = int(obs['day']), int(obs['hour'])
  i = day * 24 + hour
  if not 0 <= i < len(_PLAN):
   return {'farmer': ['PASS'], 'hands': [], 'market': []}
  action = copy.deepcopy(_PLAN[i])
  farm = obs['farms'][int(obs['player'])]
  private = obs['private']
  commands = [action['farmer']] + action['hands']
  projected = {}
  for w, (pos, cmd) in enumerate(zip([farm['farmer']] + farm['hands'], commands)):
   xy = tuple(pos)
   if xy not in _TARGETS or cmd[0] not in _SERVICE: continue
   if xy not in projected:
    projected[xy] = copy.deepcopy(farm['tiles'][pos[1]][pos[0]])
   tile = projected[xy]
   if not isinstance(tile, dict) or tile.get('animal') != 'SHEEP': continue
   inv = private['inventories'][w]
   # Keep all routes and hiring slots. Repurpose stationary goose service
   # slots for the sheep's actual state; grain demand stays one/head/day.
   op = 'PASS'
   if day < 29 and not tile['fed_today'] and inv.get('WHEAT', 0):
    op = 'FEED'; tile['fed_today'] = True
   elif day < 29 and not tile['cared_today']:
    op = 'CARE'; tile['cared_today'] = True
   elif tile.get('yield_units', 0):
    op = 'HARVEST'; tile['yield_units'] = 0
   elif tile.get('fertilizer_available'):
    op = 'COLLECT_FERTILIZER'; tile['fertilizer_available'] = False
   cmd[:] = [op]
  # Existing wool/egg sale windows now clear wool, including extra sheep
  # output; product PLACE EGG above becomes PLACE WOOL for D30 delivery.
  for order in action['market']:
   if len(order) > 2 and order[:2] == ['SELL', 'WOOL']: order[2] = 100
  return action

def create_agent(context=None): return Agent(context)
_AGENT = Agent()
def agent(observation, configuration=None):
 return _AGENT(observation, configuration)
'''

def main():
    original = BASE.read_bytes()
    source = original.decode('utf-8').split('class Agent:')[0]
    source = source.replace('E22 internal baseline: observed constant plan, s56165462 56165462.',
                            'E22 Q0 internal v1: 8 cows and up to 9 sheep; frozen control 56206528.')
    source = source.replace('Uses only current day/hour. No future observations or replay outcomes.',
                            'Uses current observations for the three converted animal tiles. No future data.')
    OUT.write_text(source + POLICY, encoding='utf-8')
    assert BASE.read_bytes() == original
    print(OUT, hashlib.sha256(OUT.read_bytes()).hexdigest())

if __name__ == '__main__': main()
