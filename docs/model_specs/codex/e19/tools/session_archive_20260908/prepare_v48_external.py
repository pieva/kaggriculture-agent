from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_v29_submission.py').read_text(encoding='utf-8').replace('v29','v48').replace('V29','V48')
(p/'build_v48_submission.py').write_text(s,encoding='utf-8')
s=(p/'run_daily_routes_770_v48.py').read_text(encoding='utf-8')
s=s.replace("OUT=BASE/'artifacts/derived/portfolio_succession_20260907'","OUT=BASE/'artifacts/derived/v48_external_parity_20260908'")
s=s.replace("BUNDLE=ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'","BUNDLE=ROOT/'submission/submission_codex_e18_770_v48_external.py'")
s=s.replace('    install(policy.core)','    # Scheduler is already installed by the standalone bundle.')
s=s.replace('    policy.core.acknowledge_terminal(','''    frozen=json.loads((BASE/'artifacts/derived/portfolio_succession_20260907'/f'{variant}_{seed}_{seat}.json').read_text(encoding='utf-8'))
    assert sides == frozen['sides'], 'Standalone bundle differs from frozen V48'
    policy.core.acknowledge_terminal(''')
(p/'run_v48_external_parity.py').write_text(s,encoding='utf-8')
