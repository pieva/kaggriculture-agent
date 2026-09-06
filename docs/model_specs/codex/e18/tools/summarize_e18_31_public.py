"""Reproducible first external diagnostic and recoverable public-source catalog."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[3]
DERIVED=BASE/'artifacts/derived'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def rollup(profile, start=1, stop=30):
    daily=profile['ledger']['daily'][start-1:stop]
    counters={k:Counter() for k in ('requested_actions','executed_actions','sales_cash','purchase_cash','sold_units','harvested','bought_units','planted')}
    for row in daily:
        for key,value in counters.items():
            value.update(row[key])
    slots=sum(counters['requested_actions'].values())
    sales=sum(counters['sales_cash'].values())
    purchases=sum(counters['purchase_cash'].values())
    payroll=sum(d['hire_cash'] for d in daily)
    net=sales-purchases-payroll-sum(d['land_cash'] for d in daily)+sum(d['unit_cash_delta'] for d in daily)
    result={k:dict(v) for k,v in counters.items()}
    result.update(slots=slots,sales=sales,purchases=purchases,payroll=payroll,net=net,
                  pass_share=100*counters['requested_actions']['PASS']/slots,
                  net_per_100_slots=100*net/slots)
    return result


def summarize(profiles):
    rows=[]
    for p in profiles:
        rows.append(dict(episode=p['episode_id'],seat=p['seat'],opponent=p['opponent'],
                         reward=p['reward'],opponent_reward=p['opponent_reward'],
                         win=p['reward']>p['opponent_reward'],
                         crop_deaths=len(p['crop_starvation']),animal_escapes=len(p['ledger']['animal_escapes']),
                         final_topology=p['topology_daily'][-1]['pasture_topology'],
                         cow_d8=p['daily'][7]['animals']['COW'],cow_d9=p['daily'][8]['animals']['COW'],
                         periods={f'D{a:02}_D{b:02}':rollup(p,a,b) for a,b in ((1,30),(1,15),(5,10),(16,30),(25,30))}))
    group=dict(n=len(rows),wins=sum(r['win'] for r in rows),
               cash_mean=mean(r['reward'] for r in rows),cash_median=median(r['reward'] for r in rows),
               cash_min=min(r['reward'] for r in rows),cash_max=max(r['reward'] for r in rows),
               crop_deaths=sum(r['crop_deaths'] for r in rows),animal_escapes=sum(r['animal_escapes'] for r in rows),
               periods={},daily=[])
    for period in rows[0]['periods']:
        values=[r['periods'][period] for r in rows]
        group['periods'][period]={k:mean(v[k] for v in values) for k in ('slots','sales','purchases','payroll','net','pass_share','net_per_100_slots')}
        for kind in ('requested_actions','executed_actions','sales_cash','purchase_cash','sold_units','harvested','bought_units','planted'):
            keys=set().union(*(v[kind] for v in values))
            group['periods'][period][kind]={k:mean(v[kind].get(k,0) for v in values) for k in sorted(keys)}
    for day in range(30):
        stock=[p['daily'][day] for p in profiles]
        group['daily'].append(dict(day=day+1,
            **{k:mean(s[k] for s in stock) for k in ('money','people','crop_tiles','occupied_livestock_tiles')},
            crops={k:mean(s['crops'][k] for s in stock) for k in stock[0]['crops']},
            animals={k:mean(s['animals'][k] for s in stock) for k in stock[0]['animals']}))
    return dict(summary=group,profiles=rows)


def main():
    ours=read(DERIVED/'E18_31_EXTERNAL_SUBMISSION_FIRST6_20260906.json')
    top=read(DERIVED/'E18_31_EXTERNAL_TOP002_FULL_20260906.json')
    selected=[p for p in top['profiles'] if p['exact770_final'] and p['exact770_d15_d30_share']>=.8]
    assert len(ours['profiles'])==6 and len(selected)==4 and top['stable_preliminary']
    result=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),
                candidate=summarize(ours['profiles']),top002=summarize(selected),
                top002_screened_n=5,excluded=[p['episode_id'] for p in top['profiles'] if p not in selected],
                matched=False,holdout=False,incumbent_promoted=False)
    output=DERIVED/'E18_31_PUBLIC_TOP002_SUMMARY_20260906.json'
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

    catalog={}
    for source in sorted(DERIVED.glob('E18_31_EXTERNAL_*.json')):
        payload=read(source)
        for p in payload['profiles']:
            key=str(p['episode_id'])
            item=catalog.setdefault(key,{k:p[k] for k in ('episode_id','sha256','bytes','url','cache_path')})
            assert item['sha256']==p['sha256']
            item.setdefault('derived_sources',[]).append(source.name)
    keep={p['episode_id'] for p in ours['profiles']+top['profiles']}
    for item in catalog.values():
        path=Path(item['cache_path'])
        assert path.resolve().parent==(ROOT/'data/replays/json').resolve()
        if path.exists():
            assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        item['retain_raw_for_current_study']=item['episode_id'] in keep
    catalog_output=DERIVED/'E18_31_PUBLIC_REPLAY_RECOVERY_CATALOG_20260906.json'
    catalog_output.write_text(json.dumps(dict(created_at_utc=result['created_at_utc'],
        recovery='GET canonical URL; verify SHA-256 before use. Raw cache is ignored by Git.',
        episodes=list(catalog.values())),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    reference=BASE/'reports/E18_31_PUBLIC_REPLAY_REFERENCE_20260906_IT.md'
    lines=['# E18.31 — riferimento e recupero replay pubblici', '',
           'Acquisizione 2026-09-06. Le identità dei benchmark sono nel registro comune.',
           'Cache grezza esclusa da Git. Conservare ora i sei replay E18.31 e tutti i',
           'cinque del nuovo riferimento, incluso il non-770. Gli altri 38 download',
           'di screening sono riscaricabili e possono essere eliminati dopo verifica.',
           'Le sintesi topologiche, tutti i risultati negativi e gli hash rimangono.', '',
           'Catalogo macchina: `../artifacts/derived/E18_31_PUBLIC_REPLAY_RECOVERY_CATALOG_20260906.json`.',
           'Per recuperare: GET del link canonico, poi verifica SHA-256; se cambia,',
           'non sovrascrivere la provenienza congelata. La disponibilità futura',
           'di Kaggle non è garantita. Nessun replay di self-test nel campione.', '',
           '| Episodio | Cache prevista | Download canonico | SHA-256 |',
           '|---|---|---|---|']
    for item in catalog.values():
        disposition='Conservata per studio' if item['retain_raw_for_current_study'] else 'Eliminabile dopo verifica'
        lines.append(f"| {item['episode_id']} | {disposition} | [replay]({item['url']}) | `{item['sha256']}` |")
    reference.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(summary=str(output),catalog=str(catalog_output),
        source_count=len(catalog),retain_raw_count=len(keep)),ensure_ascii=False))
    for key in ('candidate','top002'):
        s=result[key]['summary']
        print(key,json.dumps({k:v for k,v in s.items() if k not in ('periods','daily')}))
        for period,p in s['periods'].items():
            print(period,json.dumps({k:p[k] for k in ('net','sales','payroll','pass_share','net_per_100_slots')}),
                  json.dumps({k:p['requested_actions'].get(k,0) for k in ('PASS','MOVE')}),
                  json.dumps({k:p['executed_actions'].get(k,0) for k in ('WATER','FEED','CARE','FERTILIZE')}))


if __name__=='__main__':
    main()
