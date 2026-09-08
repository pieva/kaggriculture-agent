import json,re,subprocess
from pathlib import Path
out=Path('docs/model_specs/codex/e19/reports/v29_external_20260908')
for p in out.glob('*COMPLETE_KPI.html'):
    s=p.read_text(encoding='utf-8')
    data=re.search(r'<script id="kpi-data" type="application/json">(.*?)</script>',s,re.S).group(1)
    d=json.loads(data)
    assert len(d['metrics'])==22
    assert all(len(v)==30 and all(len(t)==3 and t[1]<=t[0]<=t[2] for t in v) for ss in d['series'].values() for v in ss.values())
    Path('scratch/complete_kpi_data.json').write_text(data,encoding='utf-8')
    Path('scratch/complete_kpi_runtime.js').write_text(re.findall(r'<script>(.*?)</script>',s,re.S)[-1],encoding='utf-8')
    check=Path('scratch/check_continuity_runtime.cjs').read_text(encoding='utf-8').replace('Top770-001',d['topLabel'])
    Path('scratch/check_v29_external.cjs').write_text(check,encoding='utf-8')
    subprocess.run(['node','scratch/check_v29_external.cjs'],check=True)
    print(p.name,'verified')
