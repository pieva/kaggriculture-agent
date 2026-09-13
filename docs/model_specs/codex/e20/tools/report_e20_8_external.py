"""Self-contained KPI and product market report for the frozen external cohort."""
import csv,hashlib,json,sys
from pathlib import Path
from statistics import mean,median
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
OUT=ROOT/'docs/model_specs/codex/e20/reports/external_e20_8_20260913'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
def net(d):return sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta']
def main():
    inv=read(OUT/'INVENTORY.json');games=[read(OUT/'profiles'/f"{g['episode']}.json") for g in inv['models']['E20.8']['games']]
    assert len(games)==20 and not read(OUT/'AUDIT_ERRORS.json')
    hist=read(OUT/'history_56191695.json')
    episodes=sorted([e for e in hist['episodes'] if e.get('state')=='COMPLETED' and e.get('type')=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2],key=lambda e:(e['createTime'],e['id']))
    ratings=[]
    for e in episodes:
        own=next(a for a in e['agents'] if a['submissionId']==56191695);opp=next(a for a in e['agents'] if a['submissionId']!=56191695)
        ratings.append(dict(episode=e['id'],time=e['endTime'],rating=own.get('updatedScore'),opponent_rating=opp.get('initialScore'),margin=own['reward']-opp['reward']))
    summary=dict(n=20,wins=sum(g['own']['reward']>g['opponent']['reward'] for g in games),draws=sum(g['own']['reward']==g['opponent']['reward'] for g in games),
        cash_mean=mean(g['own']['reward'] for g in games),cash_median=median(g['own']['reward'] for g in games),margin_mean=mean(g['own']['reward']-g['opponent']['reward'] for g in games),
        opponent_rating_mean=mean(next(a['initialScore'] for a in g['metadata']['agents'] if a['submissionId']!=56191695) for g in games),
        crop_losses_mean=mean(len(g['own']['crop_starvation']) for g in games),animal_losses=sum(sum(k['verified_animal_losses'] for k in g['own']['kpi']) for g in games),
        rating=ratings[-1]['rating'],history_games=len(ratings),history_wins=sum(r['margin']>0 for r in ratings),observed_at_utc=inv['observed_at_utc'])
    phases=[]
    for name,lo,hi in [('D1–11',0,11),('D12–19',11,19),('D20–29',19,29),('D30',29,30)]:
        for side in ['own','opponent']:
            vals=[]
            for g in games:
                ld=g[side]['ledger']['daily'][lo:hi];ks=g[side]['kpi'][lo:hi]
                vals.append(dict(net=sum(net(d) for d in ld),sales=sum(sum(d['sales_cash'].values()) for d in ld),purchases=sum(sum(d['purchase_cash'].values()) for d in ld),hires=sum(d['hire_cash'] for d in ld),PASS=sum(k['PASS'] for k in ks),MOVE=sum(k['MOVE'] for k in ks),crops=mean(k['crop_tiles'] for k in ks)))
            phases.append(dict(phase=name,side=side,**{k:mean(v[k] for v in vals) for k in vals[0]}))
    products=sorted({b['product'] for g in games for b in g['market']});product_rows=[]
    for product in products:
        for side in ['own','opponent']:
            bs=[b for g in games for b in g['market'] if b['product']==product]
            units=sum(b[side+'_sold'] for b in bs);rev=sum(b[side+'_revenue'] for b in bs)
            product_rows.append(dict(product=product,side=side,units_mean=units/20,revenue_mean=rev/20,weighted_price=rev/units if units else None,floor_units_mean=sum(b[side+'_floor_sales'] for b in bs)/20))
    refs={}
    refdir=ROOT/'docs/model_specs/codex/e21/reports/external_770_772_774_775/profiles_1700'
    for p in refdir.glob('*.json'):
        r=read(p)
        if r['model'] in ['772','775']:refs.setdefault(r['model'],[]).append(r['profile']['kpi'])
    def kpi_aggregate(ss):return {key:[median(s[d][key] for s in ss) for d in range(30)] for key,_,_ in FIELDS}
    data=dict(summary=summary,ratings=ratings,fields=FIELDS,products=products,phases=phases,product_summary=product_rows,
        references={k:kpi_aggregate(v) for k,v in refs.items()},games=[])
    daily_export=[];market_export=[]
    for g in games:
        packed={p:[] for p in products}
        for b in g['market']:
            packed[b['product']].append([b[k] for k in ['step','day','hour','own_sold','opponent_sold','own_revenue','opponent_revenue','price_before','price_after_trades','price_after_town','own_bought','opponent_bought','own_floor_sales','opponent_floor_sales','town_consumption']])
        data['games'].append(dict(episode=g['episode'],seat=g['seat'],opponent_name=g['teams'][1-g['seat']],cash=g['own']['reward'],opponent_cash=g['opponent']['reward'],
            topology=g['final_topology'],kpi={side:{key:[r[key] for r in g[side]['kpi']] for key,_,_ in FIELDS} for side in ['own','opponent']},market=packed))
        for side in ['own','opponent']:
            for r in g[side]['kpi']:daily_export.append(dict(episode=g['episode'],side=side,day=r['day'],**{key:r[key] for key,_,_ in FIELDS}))
        market_export.extend(dict(episode=g['episode'],own_seat=g['seat'],**b) for b in g['market'])
    for name,rows in [('DAILY_22_KPI.csv',daily_export),('MARKET_BATCHES.csv',market_export),('PRODUCT_SUMMARY.csv',product_rows),('PHASES.csv',phases)]:
        with (OUT/name).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    save(OUT/'SUMMARY.json',summary);save(OUT/'REPORT_DATA.json',data)
    template=Path(__file__).with_name('e20_8_external_template.html').read_text(encoding='utf-8')
    (OUT/'REPORT.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')),encoding='utf-8')
    print(json.dumps(summary,indent=2));print(json.dumps(product_rows,indent=2));print(json.dumps(phases,indent=2))
if __name__=='__main__':main()
