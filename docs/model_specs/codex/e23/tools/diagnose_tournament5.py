"""Summarize execution fidelity and animal-product inventory balances."""
import json,statistics as st
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e23/reports/tournament5_v1'
EXPECTED={'E22G':{'COW':8,'SHEEP':6,'GOOSE':3},'E22S':{'COW':8,'SHEEP':9},'E23G':{'COW':9,'SHEEP':5,'GOOSE':3},'E23S':{'COW':6,'SHEEP':11},'E23M':{'COW':7,'SHEEP':10}}

def main():
 rows=[json.loads(p.read_text()) for p in sorted((OUT/'matches').glob('E*.json'))];details=[]
 for r in rows:
  for seat,k in enumerate(r['players']):
   p=r['profiles'][seat];t=p['terminal'];bought=sum((Counter(d['bought_units']) for d in p['ledger']['daily']),Counter())
   remainder={prod:p['totals']['harvested'].get(prod,0)+bought[prod]-p['totals']['sold_units'].get(prod,0)-t['shed'].get(prod,0)-t['carried'].get(prod,0) for prod in ['MILK','WOOL','EGG']}
   assert all(n>=0 for n in remainder.values())
   q2=[e for e in p['harvest_events'] if e['x']==3 and e['y']==7 and e['day']==30 and e['gain'].get('WHEAT')]
   details.append(dict(match=r['id'],policy=k,seat=seat,expected_mix=r['checks'][seat]['mix']==EXPECTED[k],actual_mix=r['checks'][seat]['mix'],escapes=len(p['ledger']['animal_escapes']),unfed=len(p['unfed']),max_consecutive_unfed=max([e['consecutive'] for e in p['unfed']]+[0]),crop_stress=len(p['crop_starvation']),failed_actions=dict(Counter(e['command'][0] for e in p['failed_actions'])),terminal_tile_yield=t['tile_yield_units'],terminal_shed=t['shed'],terminal_carried=t['carried'],animal_inventory_difference=remainder,q2_wheat_harvest=sum(e['gain']['WHEAT'] for e in q2),cash_parity_errors=p['ledger']['cash_parity_errors']))
 summary={}
 for k in EXPECTED:
  rs=[r for r in details if r['policy']==k]
  if not rs:continue
  summary[k]=dict(n=len(rs),expected_mix_games=sum(r['expected_mix'] for r in rs),escapes=sum(r['escapes'] for r in rs),unfed=sum(r['unfed'] for r in rs),max_consecutive_unfed=max(r['max_consecutive_unfed'] for r in rs),crop_stress=sum(r['crop_stress'] for r in rs),q2_wheat_harvest_games=sum(r['q2_wheat_harvest']==2 for r in rs),animal_inventory_difference=dict(sum((Counter(r['animal_inventory_difference']) for r in rs),Counter())),mean_terminal_tile_yield={prod:st.mean(r['terminal_tile_yield'].get(prod,0) for r in rs) for prod in ['MILK','WOOL','EGG']})
 result=dict(matches=len(rows),summary=summary,details=details,meaning='Animal inventory difference = harvested + bought - sold - terminal carried/shed; positive differences require inspection of replay overflow. Tile yield is unharvested and excluded. Unfed counts animal/day events, not escapes.')
 (OUT/'DIAGNOSTICS.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
