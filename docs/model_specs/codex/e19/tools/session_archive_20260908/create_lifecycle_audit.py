from pathlib import Path
root=Path.cwd()
base=root/'docs/model_specs/codex/e19/tools'
old=(root/'docs/model_specs/codex/e18/tools/e18_29_crop_service_audit.py').read_text(encoding='utf-8')
old=old.replace('"""Verify crop water deaths at actual day refresh, not H24 snapshots."""','"""Classify legacy dry-to-weed events by lifecycle; does not change policy."""')
old=old.replace('        after = recorded', '''        post_units = deepcopy(farm)
        step = previous['day'] * 24 + previous['hour']
        engine._decay_plants(farm, step)
        after = recorded''')
old=old.replace('enumerate(farm["tiles"])','enumerate(post_units["tiles"])')
old=old.replace('                    events.append(','''                    rules = engine.CROPS[tile['crop']]
                    last_day = (tile['planted_day'] + rules['first_yield_day']
                                + (rules['max_yield'] - 1) * rules['interval']) if rules['ongoing'] else None
                    future = bool(last_day is not None and last_day > previous['day'])
                    decayed = farm['tiles'][y][x].get('kind') == 'WEED'
                    events.append(''')
old=old.replace('crop=tile["crop"],','''crop=tile["crop"],
                            held_units_after_actions=tile['yield_units'],
                            future_production=future,
                            last_production_day=None if last_day is None else last_day+1,
                            physical_cause='decay' if decayed else 'water_refresh',
                            productive_loss=bool(tile['yield_units']>0 or future),
                            tile_after_actions=deepcopy(tile),''')
(base/'crop_lifecycle_audit_v48.py').write_text(old,encoding='utf-8')
s=(base/'run_daily_routes_770_v48.py').read_text(encoding='utf-8')
s=s.replace("OUT=BASE/'artifacts/derived/portfolio_succession_20260907'","OUT=BASE/'artifacts/derived/lifecycle_audit_770_20260908'")
s=s.replace('    policy.core.acknowledge_terminal(','''    from docs.model_specs.codex.e19.tools.crop_lifecycle_audit_v48 import crop_service_audit as lifecycle_audit
    lifecycle={label:lifecycle_audit(replay,pos) for label,pos in [('candidate',seat),('v4d',1-seat)]}
    frozen=json.loads((BASE/'artifacts/derived/portfolio_succession_20260907'/f'{variant}_{seed}_{seat}.json').read_text(encoding='utf-8'))
    assert sides == frozen['sides'], 'Frozen replay results changed'
    policy.core.acknowledge_terminal(''')
s=s.replace('result=dict(renewal_certificate_log=', 'result=dict(lifecycle_audit=lifecycle, frozen_sides_equal=True, renewal_certificate_log=')
s=s.replace('(OUT/f\'{variant}_{seed}_{seat}.json\').write_text(json.dumps(result,indent=2)+\'\\n\')','(OUT/f\'{variant}_{seed}_{seat}.json\').write_text(json.dumps(result,indent=2)+\'\\n\',encoding="utf-8")')
(base/'run_lifecycle_audit_v48.py').write_text(s,encoding='utf-8')
