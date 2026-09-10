"""Reconcile counterfactual branches and report observed economic mechanisms."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.audit_results import run as audit
BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/diagnostic_20260910';ART=BASE/'artifacts/H001'
MODELS=['E18','E19','E20.1']
def main():
    rows=[]
    for model in MODELS:
        conditions={}
        for condition in ['control','omit_one_hire']:
            p=ART/f'{model}_{condition}.json';meta=json.loads(p.read_text());assert all(x['calls']==719 and x['core_errors'] in [0,None] for x in meta['runtime'])
            audit(str(p));k=json.loads(p.with_suffix('.kpi.json').read_text());s=k['sides'][0]
            assert k['replay_sha256']==meta['replay_sha256'],'Stale KPI cache: regenerate the audit for this replay'
            with gzip.open(p.with_suffix('.replay.json.gz'),'rt') as f:r=json.load(f)
            result=dict(reward=s['reward'],losses=len(s['ledger']['animal_escapes']),stress=len(s['crop_starvation']),verification=meta['verification'],intervention=meta['intervention'],windows={})
            result['opponent_reward']=k['sides'][1]['reward']
            result['D20_hands_after_first_batches']=[len(r['steps'][i][0]['observation']['farms'][0]['hands']) for i in [457,458,459,479]]
            for label,end in [('D20',20),('D20-D22',22),('D20-D30',30)]:
                ds=s['ledger']['daily'][19:end]
                result['windows'][label]=dict(cash=r['steps'][min(end*24,719)][0]['observation']['farms'][0]['money'],hires=sum(d['hires'] for d in ds),wages=sum(d['hire_cash'] for d in ds),sales=sum(sum(d['sales_cash'].values()) for d in ds),purchases=sum(sum(d['purchase_cash'].values()) for d in ds),**{a:sum(d['requested_actions'].get(a,0) for d in ds) for a in ['MOVE','PASS']},**{a:sum(d['executed_actions'].get(a,0) for d in ds) for a in ['WATER','FEED','CARE']})
            conditions[condition]=result
        control=conditions['control'];treatment=conditions['omit_one_hire']
        assert control['verification']['suffix_states']==263 and control['verification']['suffix_action_batches']==263
        delta=treatment['reward']-control['reward']
        biological_regression=treatment['losses']>control['losses'] or treatment['stress']>control['stress']
        rows.append(dict(model=model,conditions=conditions,delta_cash=delta,result='zero' if delta==0 else 'gain' if delta>0 else 'loss',biological_regression=biological_regression,decision='REJECT_BIOLOGICAL_REGRESSION' if biological_regression else 'LOCAL_RESULT_REQUIRES_REPLICATION',adopted=False))
    (OUT/'H001_RESULT.json').write_text(json.dumps(dict(experiment='H001',purpose='method_pilot_not_promotion',rows=rows),indent=2)+'\n')
    lines=['# H001: una richiesta di assunzione in meno all avvio di D20','', 'Un seed per modello (180910201), ciascuno dal proprio stato originale. Prova del banco, non selezione di un candidato o confronto causale fra topologie. Il trattamento rimuove una richiesta HIRE una sola volta; le assunzioni successive restano libere.', '', '| Modello | Cassa controllo | Cassa intervento | Delta | Esito |','|---|---:|---:|---:|---|']
    for r in rows:lines.append(f'| {r["model"]} | {r["conditions"]["control"]["reward"]:.0f} | {r["conditions"]["omit_one_hire"]["reward"]:.0f} | {r["delta_cash"]:+.0f} | {r["result"]} |')
    lines+=['', 'Lettura competitiva supplementare, aggiunta dopo il pilota: anche l avversario reagisce e cambia cassa. Il margine non era un criterio preselezionato di H001 e va esplicitato nei protocolli successivi.', '', '| Modello | Delta cassa avversario | Delta margine sullo stesso avversario |','|---|---:|---:|']
    for r in rows:
        opponent_delta=r['conditions']['omit_one_hire']['opponent_reward']-r['conditions']['control']['opponent_reward']
        lines.append(f'| {r["model"]} | {opponent_delta:+.0f} | {r["delta_cash"]-opponent_delta:+.0f} |')
    lines+=['','## Reazione immediata delle assunzioni','','Numero di manovali dopo i primi tre batch e prima dell ultimo batch di D20; farmer escluso. Questo distingue il mancato recupero del lavoratore da una diversa sequenza di assunzione.','','| Modello | Condizione | Dopo H1 | Dopo H2 | Dopo H3 | Prima H24 |','|---|---|---:|---:|---:|---:|']
    for r in rows:
        for condition,s in r['conditions'].items():
            lines.append('| '+r['model']+' | '+condition+' | '+' | '.join(map(str,s['D20_hands_after_first_batches']))+' |')
    for label in ['D20','D20-D22','D20-D30']:
        lines+=['',f'## {label}: intervento meno controllo','','| Modello | Cassa | Assunzioni | Salari | Vendite | Acquisti | MOVE | PASS | WATER | FEED | CARE |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for r in rows:
            a=r['conditions']['control']['windows'][label];b=r['conditions']['omit_one_hire']['windows'][label]
            lines.append('| '+r['model']+' | '+' | '.join(f'{b[k]-a[k]:+.0f}' for k in ['cash','hires','wages','sales','purchases','MOVE','PASS','WATER','FEED','CARE'])+' |')
    lines+=['','## Sicurezza e validita','','| Modello | Stress controllo / intervento | Fughe controllo / intervento |','|---|---:|---:|']
    for r in rows:
        a=r['conditions']['control'];b=r['conditions']['omit_one_hire'];lines.append(f'| {r["model"]} | {a["stress"]} / {b["stress"]} | {a["losses"]} / {b["losses"]} |')
    lines+=['', 'Interpretazione del pilota: il guadagno di E18 non e accettabile come miglioramento, perche aumenta lo stress e compare una fuga animale. Il risparmio di salario e soltanto 144: la maggior parte del delta terminale deriva dalle vendite successive. E19 ed E20.1 recuperano rapidamente l organico; qui il trattamento cambia soprattutto la sequenza. I segni economici positivi non dimostrano una regola generalizzabile.',
            '', 'Il prossimo test deve separare numero di manovali, orario di disponibilita e assegnazione dei percorsi. Ogni nuova condizione va definita prima dei risultati e ripetuta su piu seed, senza accedere ai seed di validazione riservati.']
    lines+=['', 'Tutti e tre i controlli ricostruiscono 456 azioni per agente e riproducono le 263 coppie di azioni e i 263 stati successivi fino al terminale. Ogni ramo completa 719 chiamate per agente senza errori nei core che espongono il contatore. Si ignora nella parita solo il budget di tempo residuo, che dipende dal runtime. La prova non certifica il timeout della submission.', '', 'Gli agenti conservano le rispettive memorie ricostruite dalla propria storia e reagiscono alle osservazioni modificate. L intervento comprende cambi di assegnazione, rifornimenti, produzione e reazione dell avversario: non e una misura isolata del valore salariale di un lavoratore.', '', 'Nessuna promozione. Ogni effetto va replicato su un campione diagnostico piu ampio prima di trasformarlo in una regola. [Dati](H001_RESULT.json) - [Protocollo](../../PROTOCOL.md).']
    (OUT/'H001_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print([(r['model'],r['delta_cash']) for r in rows])
if __name__=='__main__':main()
