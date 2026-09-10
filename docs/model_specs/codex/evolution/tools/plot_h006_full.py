"""Standalone plots of all paired daily KPI deltas, without role aggregation."""
import csv
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
OUT=ROOT/'docs/model_specs/codex/evolution/reports/H006_FULL'
with (OUT/'delta_22_kpi.csv').open() as f:
    rows=list(csv.DictReader(f))
for model in ['E19','E18']:
    fig,axes=plt.subplots(6,4,figsize=(16,18),layout='constrained')
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for seed,color in [('180910204','#126b9b'),('180910206','#b4511e')]:
            for target,style in [('0','-'),('1','--')]:
                rr=sorted([r for r in rows if r['model']==model and r['seed']==seed and r['target_seat']==target],key=lambda r:int(r['day']))
                assert len(rr)==30
                ax.plot([int(r['day']) for r in rr],[float(r[key]) for r in rr],color=color,linestyle=style,label=f'{seed[-3:]} / ruolo E19 {target}')
        ax.set_title(label,fontsize=10)
        ax.set_ylabel('Delta '+unit,fontsize=8)
        ax.set_xlim(19,30)
        ax.set_xticks([20,22,24,26,28,30])
        ax.grid(alpha=.2)
    for ax in list(axes.flat)[len(FIELDS):]:ax.set_visible(False)
    handles,labels=axes.flat[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower right',bbox_to_anchor=(.98,.035),fontsize=10)
    fig.suptitle(f'H006 — {model}: intervento meno controllo, 22 KPI\nDue seed diagnostici, ruoli accoppiati; D30 terminale',fontsize=16)
    fig.savefig(OUT/f'{model}_delta_22_kpi.png',dpi=130)
    plt.close(fig)
p=OUT/'REPORT.md'
s=p.read_text(encoding='utf-8').split('\n## Grafici delle differenze')[0]
p.write_text(s.rstrip()+'\n\n## Grafici delle differenze\n\nLe quattro linee mantengono separati seed e ruoli; le linee sovrapposte indicano valori coincidenti.\n\n![E19](E19_delta_22_kpi.png)\n\n![E18](E18_delta_22_kpi.png)\n',encoding='utf-8')
