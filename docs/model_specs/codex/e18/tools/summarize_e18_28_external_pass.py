"""Freeze a whole-submission diagnostic sample, including wins as controls."""

import json
import statistics
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
INPUT = BASE / 'artifacts/derived/e18_28_external_pass_20260905_v2'
OUT = BASE / 'artifacts/derived/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_V2.json'
REPORT = BASE / 'reports/E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_IT.md'


def mean(values):
    values = list(values)
    return statistics.mean(values) if values else None


def count(rows, section, key):
    return sum(r.get(section, {}).get(key, 0) for r in rows)


def cohort(profiles):
    def each(fn):
        return mean(fn(p) for p in profiles)
    reasons = Counter()
    for p in profiles:
        reasons.update(p['pass_summary']['reasons'])
    windows = {}
    for lo,hi in ((1,6),(7,12),(13,15),(15,30),(16,24),(25,30)):
        label = f'D{lo:02d}_D{hi:02d}'
        windows[label] = dict(
            ours=each(lambda p:sum(d.get('PASS',0) for d in p['action_daily'][lo-1:hi])),
            opponents=each(lambda p:sum(d.get('PASS',0) for d in p['opponent_action_daily'][lo-1:hi])),
            queue_finished=each(lambda p:p['pass_windows'][label]['reasons'].get('QUEUE_FINISHED',0)),
            scheduled_wait=each(lambda p:p['pass_windows'][label]['reasons'].get('WAIT_SCHEDULED_TURN',0)),
            blocked=each(lambda p:sum(v for k,v in p['pass_windows'][label]['reasons'].items() if k.startswith('BLOCKED'))),
            ours_share_pct=100*sum(sum(d.get('PASS',0) for d in p['action_daily'][lo-1:hi]) for p in profiles)/sum(sum(p['capacity_daily'][lo-1:hi]) for p in profiles),
            opponent_share_pct=100*sum(sum(d.get('PASS',0) for d in p['opponent_action_daily'][lo-1:hi]) for p in profiles)/sum(sum(p['opponent_capacity_daily'][lo-1:hi]) for p in profiles),
        )
    economic = [p for p in profiles if p['ledger'] and p['opponent_ledger']]
    ledger_metrics = {}
    for section, items in {
        'executed_actions':['CARE','FEED','WATER','FERTILIZE','HARVEST'],
        'harvested':['MILK','WOOL','STRAWBERRY','WHEAT','CARROT','MELON'],
        'sales_cash':['MILK','WOOL','STRAWBERRY','WHEAT','CARROT','MELON','FERTILIZER'],
        'sold_units':['MILK','WOOL','STRAWBERRY','WHEAT','CARROT','MELON','FERTILIZER'],
    }.items():
        for item in items:
            ledger_metrics[f'{section}:{item}'] = dict(
                ours=mean(count(p['ledger']['daily'],section,item) for p in economic),
                opponents=mean(count(p['opponent_ledger']['daily'],section,item) for p in economic),
            )
    return dict(n=len(profiles), unique_opponents=len({p['opponent'] for p in profiles}),
                reward=each(lambda p:p['reward']), opponent_reward=each(lambda p:p['opponent_reward']),
                gap=each(lambda p:p['reward']-p['opponent_reward']),
                pass_mean=each(lambda p:p['pass_summary']['total']),
                pass_min=min(p['pass_summary']['total'] for p in profiles),
                pass_max=max(p['pass_summary']['total'] for p in profiles),
                reasons_total=dict(reasons), windows=windows,
                cash_verified_n=len(economic), ledger_metrics=ledger_metrics,
                crop_deaths=sum(len(p['crop_starvation']) for p in profiles),
                crop_death_matches=sum(bool(p['crop_starvation']) for p in profiles),
                animal_losses=sum(len(p['ledger']['animal_escapes']) for p in economic),
                local_unique_opportunity_days={op:each(lambda p:p['pass_windows']['D15_D30']['unique_tile_days_by_op'].get(op,0)) for op in ['HARVEST','CARE','COLLECT_FERTILIZER','WATER','DROP']},
                terminal_carried_units=each(lambda p:sum(p['terminal']['carried'].values())),
                productive_unfinished_matches=sum(bool(p['productive_unfinished']) for p in profiles))


def main():
    profiles = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(INPUT.glob('*.json'))]
    assert len(profiles) == 30, len(profiles)
    assert len({p['source']['episode_id'] for p in profiles}) == 30
    groups = {label:cohort([p for p in profiles if label=='ALL' or p['result']==label]) for label in ('ALL','LOSS','WIN')}
    failure_cases = []
    for p in profiles:
        if p['result'] != 'LOSS' or len(p['crop_starvation']) < 5:
            continue
        replay=json.loads(Path(p['source']['path']).read_text(encoding='utf-8'))
        seat=p['seat']
        hiring=[]
        for index in range(241,265):
            obs=replay['steps'][index-1][seat]['observation']
            farm=obs['farms'][seat]
            hiring.append(dict(turn=obs['hour']+1,money=farm['money'],hands=len(farm['hands']),
                               hire_requests=sum(o[0]=='HIRE' for o in replay['steps'][index][seat]['action']['market'])))
        failure_cases.append(dict(episode=p['source']['episode_id'], D11_hiring=hiring,
                                  D11_unfinished_by_op=dict(Counter(r['opcode'] for e in p['productive_unfinished'] if e['day']==11 for r in e['rows'])),
                                  D11_queue_finished_by_worker=dict(Counter(e['worker'] for e in p['pass_events'] if e['day']==11 and e['reason']=='QUEUE_FINISHED')),
                                  crop_starvation=p['crop_starvation']))
    payload = dict(
        submission_id=56036993, version='E18.28 C', not_published_candidate='E18.29 B3',
        sampling='All 30 competitive complete episodes in the inspected game list; one self-test excluded. Frozen at episode 105876558; no Top770 selection.',
        groups=groups, sources=[p['source'] for p in profiles],
        failure_cases=failure_cases,
        opponent_loss_topologies=dict(Counter(str(p['opponent_daily'][-1]['pasture_topology']) for p in profiles if p['result']=='LOSS')),
        profiles_directory=str(INPUT),
        cash_audit_exceptions=[dict(episode=p['source']['episode_id'],error=p['ledger_error']) for p in profiles if p['ledger_error']],
        episodes=[{k:p[k] for k in ('opponent','seat','result','reward','opponent_reward','pass_summary','pass_windows','productive_unfinished','crop_starvation','terminal')} | {'episode':p['source']['episode_id']} for p in profiles],
        daily=[dict(day=day,**{label:{'PASS':mean(p['action_daily'][day-1].get('PASS',0) for p in profiles if label=='ALL' or p['result']==label),
                                         'cash':mean(p['daily'][day-1]['money'] for p in profiles if label=='ALL' or p['result']==label)} for label in ('ALL','LOSS','WIN')}) for day in range(1,31)],
    )
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines = ['# E18.28 C — diagnosi esterna dei PASS e delle sconfitte', '',
             'Campione congelato il 2026-09-05: submission **56036993**, tutti i 30 episodi competitivi completati mostrati nella cronologia, fino a **105876558**; escluso il self-test. Nessuna selezione per rating, avversario o topologia. E18.29 B3 non è pubblicata: questi risultati descrivono il parent E18.28 C.', '',
             '## Metodo e limiti', '',
             'Per ogni replay: 720 stati DONE/DONE, episodio e SHA-256 verificati; 719 decisioni ricostruite dal controller E18.28 senza cambiare lo stato registrato e confrontate integralmente con le azioni pubblicate. Nessun disaccordo. Non sono nuove simulazioni né stime controfattuali del punteggio. Il motivo del PASS è il ramo effettivo del dispatcher, non una deduzione dal grafico.', '',
             'Finestre assegnate al giorno pre-azione. PASS comprende ogni lavoratore già presente e ogni comando omesso; quota normalizzata sugli slot realmente disponibili. Un worker assunto nel batch non aggiunge retroattivamente uno slot. Gli avversari possono avere topologie/personale diversi: il confronto esterno è diagnostico, non una ablation causale.', '',
             'I flussi monetari e WATER/FEED/CARE/HARVEST vengono verificati nel motore sui batch registrati. Eventuali episodi con mancata riconciliazione restano nel campione PASS/score, ma sono esclusi dalle medie dei flussi verificati e segnalati sotto. Non si imputano valori zero. I vecchi derivati nella directory senza suffisso v2 sono preliminari e non vanno usati: V2 corregge la normalizzazione NORTH/SOUTH/EAST/WEST e conserva anche le eccezioni di audit.', '',
             'Nessuno dei 17 avversari vincitori ha esattamente la topologia finale Q0=7/Q1=7/Q2=0/Q3=0. Le cause del nostro dispatcher sono verificate sulla nostra 770; i divari di mix/ricavo avversario servono a formulare ipotesi, non a scegliere una topologia o quantificare guadagni ottenibili a parità di architettura.', '',
             '## Risultati — vittorie come controllo', '',
             '| Campione | N | Cassa nostra | Cassa avversaria | PASS nostri | Min–max PASS | PASS D15–D30 | % slot D15–D30 |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for label,g in groups.items():
        w=g['windows']['D15_D30']
        lines.append(f"| {label} | {g['n']} | {g['reward']:,.1f} | {g['opponent_reward']:,.1f} | {g['pass_mean']:,.1f} | {g['pass_min']}–{g['pass_max']} | {w['ours']:,.1f} | {w['ours_share_pct']:.2f}% |")
    lines += ['', '## Motivi osservati nelle sconfitte', '', '| Finestra | PASS nostri | Coda esaurita | Attesa orario | Prerequisito bloccato | PASS avversari | % slot nostri / avversari |','|---|---:|---:|---:|---:|---:|---:|']
    for label,w in groups['LOSS']['windows'].items():
        lines.append(f"| {label} | {w['ours']:.1f} | {w['queue_finished']:.1f} | {w['scheduled_wait']:.1f} | {w['blocked']:.1f} | {w['opponents']:.1f} | {w['ours_share_pct']:.2f}% / {w['opponent_share_pct']:.2f}% |")
    lines += ['', 'Coda esaurita non significa che tutta la farm non abbia lavoro: significa che la coda assegnata a quel worker non contiene più task produttivi. Attesa orario può essere intenzionale. Un blocco di prerequisito conta i PASS immediati, non tutti gli effetti futuri di un acquisto mancato.', '',
              '## Servizio, produzione e ricavi nelle sconfitte', '',
              f"Flussi verificati: {groups['LOSS']['cash_verified_n']}/{groups['LOSS']['n']} sconfitte.", '',
              '| KPI medio | E18.28 C | Avversari vincitori |', '|---|---:|---:|']
    for key,v in groups['LOSS']['ledger_metrics'].items():
        lines.append(f"| {key} | {v['ours']:,.2f} | {v['opponents']:,.2f} |")
    lines += ['', '## Opportunità locali: proxy, non denaro già recuperabile', '',
              'Conteggi deduplicati per giorno/tile/opcode in presenza di almeno un PASS D15–D30. Le categorie si sovrappongono: non sommarle. HARVEST può anticipare una raccolta già prenotata; WATER può essere deliberatamente omesso; CARE rende solo con FEED, maturazione, raccolta e vendita; fertilizzante richiede spazio nello shed e consegna. Nessun prezzo spot viene moltiplicato ingenuamente per il numero di PASS.', '',
              '| Tipo | Tile-giorni medi nelle sconfitte |', '|---|---:|']
    for key,value in groups['LOSS']['local_unique_opportunity_days'].items():
        lines.append(f'| {key} | {value:.2f} |')
    lines += ['', '## Episodi — campione completo', '', '| Replay | Esito | Avversario | Seat | Cassa nostra | Cassa avversaria | PASS | PASS D15–D30 | Morti crop |', '|---|---|---|---:|---:|---:|---:|---:|---:|']
    for p in profiles:
        s=p['source']; lines.append(f"| [{s['episode_id']}]({s['replay_url']}) | {p['result']} | {p['opponent']} | {p['seat']} | {p['reward']:,.0f} | {p['opponent_reward']:,.0f} | {p['pass_summary']['total']} | {p['pass_windows']['D15_D30']['total']} | {len(p['crop_starvation'])} |")
    lines += ['', '## Provenienza e recupero', '',
              'I 30 grezzi sono nei percorsi Downloads indicati dal manifest JSON; non sono stati copiati nel repository né cancellati. I link canonici consentono il recupero; verificare SHA-256 e ID prima del riuso. I derivati V2 conservano eventi PASS per worker/turno, stato locale, coda, ledger giornalieri e fonti. Questa raccolta è development/diagnostica, non holdout.', '',
              f'Dataset: `{OUT.relative_to(BASE)}`.', '', 'Eccezioni di riconciliazione:', '']
    for e in payload['cash_audit_exceptions']:
        lines.append(f"- Episodio {e['episode']}: `{e['error']}`. Flussi non utilizzati; PASS e score osservati restano validi.")
    lines += ['', '## Verifiche e stato', '',
              'Nessuna policy, topologia, config, piano o submission modificata. Nessun tuning sugli avversari pubblici, holdout, promozione, pulizia generale, commit o push. [Cause, casi critici e azioni prioritarie](E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md).', '']
    REPORT.write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'episodes':len(profiles),'losses':groups['LOSS']['n'],
                      'wins':groups['WIN']['n'],'cash_verified':groups['ALL']['cash_verified_n'],
                      'dataset':str(OUT),'report':str(REPORT)}))


if __name__=='__main__':
    main()
