"""Use the same serial paired protocol, with per-tile calendar gates."""
import compare_q0_pastures as runner

runner.CAND = runner.ROOT / 'submission/submission_codex_e22_q0_8c9s_calendar_v2.py'
runner.OUT = runner.OUT.parent / 'q0_8c9s_calendar_v2'
runner.ART = runner.ART.parent / 'q0_8c9s_calendar_v2'
runner.INTERVENTION = ('8C9S v2: recurring external placement days/hours and harvest days. '
    'D12 worker 1 delivers sheep at H7, purchase moved H2 to H1; worker 6 retains feeding route. '
    'No additional hires; two fertilizer collection slots dropped on D12; milk delivery shifted to H11 with sale. '
    'V1 market logic otherwise retained, including early widened wool sale limits. Cow/other sheep placements unchanged.')

def calendar_checks(game, seat):
    expected = {(4,1): (11,21,[17,20,23,26,29]), (3,2): (11,20,[17,20,23,26,29]),
                (2,3): (12,7,[18,21,24,27,30])}
    records = []
    for xy, (pd, ph, hd) in expected.items():
        x,y = xy
        placement, harvests = [], []
        for i in range(719):
            before = game['steps'][i][seat]['observation']['farms'][seat]
            after = game['steps'][i+1][seat]['observation']['farms'][seat]
            old, new = before['tiles'][y][x], after['tiles'][y][x]
            if isinstance(new,dict) and new.get('animal') == 'SHEEP' and (not isinstance(old,dict) or not old.get('animal')):
                placement.append([i//24+1,i%24+1])
            action = game['steps'][i+1][seat]['action']
            if isinstance(old,dict) and old.get('animal')=='SHEEP' and old.get('yield_units',0)>0:
                if any(tuple(pos)==xy and cmd==['HARVEST'] for pos,cmd in zip([before['farmer']]+before['hands'],[action['farmer']]+action['hands'])):
                    harvests.append(dict(day=i//24+1,hour=i%24+1,units=old['yield_units']))
        assert placement == [[pd,ph]], (xy,placement)
        assert [h['day'] for h in harvests] == hd, (xy,harvests)
        records.append(dict(x=x,y=y,placement=placement[0],harvests=harvests))
    return records

runner.CANDIDATE_CHECKS = calendar_checks

if __name__ == '__main__': runner.main()
