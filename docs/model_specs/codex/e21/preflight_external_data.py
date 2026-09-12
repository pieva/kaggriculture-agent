"""Verify archived inputs and exercise the 22-KPI ledger on each reference."""
import hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
OUT=BASE/'reports/external_770_772_774_775'
def main():
    from docs.model_specs.codex.e20.tools.analyze_first_external import profile
    from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
    data=json.loads((OUT/'INVENTORY.json').read_text())
    results={}
    for model,spec in data['models'].items():
        for g in spec['games']:
            raw=(ROOT/g['raw_path']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==g['sha256'] and g['complete'] and not g['missing_observation_fields']
        g=spec['games'][0];r=json.loads((ROOT/g['raw_path']).read_bytes())
        s=profile(r,g['seat'])
        assert len(s['kpi'])==30 and all(all(key in day for key,_,_ in FIELDS) for day in s['kpi'])
        (OUT/f"preflight_profile_{g['episode']}.json").write_text(json.dumps(s,separators=(',',':')))
        results[model]={'replays_verified':len(spec['games']),'ledger_sample_episode':g['episode'],
                        'cash_parity_errors':s['ledger']['cash_parity_errors'],'kpi_count':len(FIELDS),'days':30}
    (OUT/'DATA_PREFLIGHT.json').write_text(json.dumps(results,indent=2)+'\n')
    (OUT/'BASELINE_INVENTORY.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(results))
if __name__=='__main__':main()
