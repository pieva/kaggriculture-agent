"""Descriptive V51C cohort versus stable 770 opponents from our cached games."""
from restart770_comparison import *
def main():
    opponents=[g for g in read(OUT/'CANDIDATES.json') if g['production770']]
    rows=[];errors=[]
    for p in sorted((WORK/'docs/model_specs/codex/e19/reports/top_v51_20260909').glob('profile_V51C_*.json')):
        s=read(p)
        assert s['submission']==56124996 and not [e for e in s['cash_discrepancies'] if e['seat']==s['seat']] and s['net_cash_residual']==0
        rows.append(dict(group='V51C',episode=s['episode'],name=s['name'],sha256=s['sha256'],kpi=s['daily']))
    for g in opponents:
        try:
            p=OUT/f"external_{g['episode']}.json"
            if p.exists():s=read(p)
            else:
                raw=Path(g['raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
                s=profile(json.loads(raw),g['opponent_seat']);save(p,s)
            assert s['ledger']['cash_parity_errors']==0 and len(s['kpi'])==30
            rows.append(dict(group='Esterni 770',episode=g['episode'],name=g['opponent'],sha256=g['sha256'],kpi=s['kpi']))
            print('AUDITED',g['episode'],flush=True)
        except Exception as exc:errors.append(dict(episode=g['episode'],error=repr(exc)));print('ERROR',errors[-1],flush=True)
    save(OUT/'TRAJECTORY_ERRORS.json',errors)
    save(OUT/'TRAJECTORIES.json',rows)
    with (OUT/'TRAJECTORIES.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=['group','episode','name','day']+[k for k,_,_ in FIELDS]);writer.writeheader()
        for p in rows:
            for d,kpi in enumerate(p['kpi'],1):writer.writerow(dict(group=p['group'],episode=p['episode'],name=p['name'],day=d,**{k:kpi[k] for k,_,_ in FIELDS}))
    fig,axes=plt.subplots(6,4,figsize=(17,22),layout='constrained')
    fig.suptitle('770 V51C e avversari 770 delle nostre submission\nCoorti diverse, non appaiate · mediana e intervallo interquartile',fontsize=16)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for group,color in [('V51C','#216ec0'),('Esterni 770','#c46222')]:
            ps=[p for p in rows if p['group']==group];arr=np.array([[d[key] for d in p['kpi']] for p in ps])
            if not len(ps):continue
            ax.plot(range(1,31),np.median(arr,axis=0),label=f'{group} n={len(ps)}',color=color);ax.fill_between(range(1,31),np.quantile(arr,.25,axis=0),np.quantile(arr,.75,axis=0),color=color,alpha=.15)
        ax.set_title(label,fontsize=10);ax.set_ylabel(unit);ax.set_xlabel('Giorno');ax.grid(alpha=.2)
    for ax in list(axes.flat)[22:]:ax.axis('off')
    axes.flat[22].legend(*axes.flat[0].get_legend_handles_labels(),loc='center');fig.savefig(OUT/'V51C_EXTERNAL770_KPI22.png',dpi=110);plt.close(fig)
    p=OUT/'REPORT.md';text=p.read_text(encoding='utf-8').split('\n## Traiettorie fra coorti')[0]
    text+=f'\n## Traiettorie fra coorti\n\nConfronto disponibile: **{sum(r["group"]=="V51C" for r in rows)} replay V51C** già auditati contro **{sum(r["group"]=="Esterni 770" for r in rows)} profili avversari 770 produttivi**, auditati in questa analisi. Errori: {len(errors)}, conservati in TRAJECTORY_ERRORS.json. Sono coorti diverse: il grafico non misura superiorità a mercato o avversario invariati. Tutti i profili selezionati sono inclusi senza filtro economico.\n\n![22 KPI fra coorti](V51C_EXTERNAL770_KPI22.png)\n\nDati individuali D1–D30: TRAJECTORIES.csv e TRAJECTORIES.json. Il corpus V51C proviene dal report top_v51_20260909 nel worktree recuperato; i profili originali conservano hash e riconciliazione.\n'
    text+='\n| KPI medio giornaliero D16–D25 | V51C | Esterni 770 |\n|---|---:|---:|\n'
    for key in ['people','MOVE','PASS','WATER','FEED','CARE','crop_tiles','occupied_livestock_tiles','GOOSE']:
        vals=[np.mean([d[key] for p in rows if p['group']==g for d in p['kpi'][15:25]]) for g in ['V51C','Esterni 770']]
        text+=f'| {key} | {vals[0]:.2f} | {vals[1]:.2f} |\n'
    text+='\n**770 conta i pascoli, non tutti gli animali.** Nel grafico gli esterni hanno mediana di 3 oche durante la fase produttiva, mentre V51C ne ha zero: i pollai non cambiano la classificazione 770. Non interpretare FEED/CARE maggiori come maggiore copertura a parità di animali. I singoli mix sono nel CSV.\n\nNel corpus originale V51C resta documentata la discrepanza contabile di 1 sul lato avversario Scorpi, episodio 107183104; il lato V51C qui usato è riconciliato. Quel lato avversario non appartiene ai 13 profili selezionati.\n'
    p.write_text(text,encoding='utf-8');(OUT/'REPORT.html').write_text('<meta charset="utf-8"><title>Base V51C e confronto 770</title><style>body{font:17px/1.5 system-ui;max-width:1200px;margin:32px auto;padding:20px;color:#24354a}img{max-width:100%}td,th{padding:7px;border-bottom:1px solid #ddd}table{border-collapse:collapse}code{overflow-wrap:anywhere}</style>'+MarkdownIt().enable('table').render(text),encoding='utf-8')
    save(OUT/'MANIFEST.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='MANIFEST.json'})
    print('DONE',len(rows),errors,flush=True)
if __name__=='__main__':main()
