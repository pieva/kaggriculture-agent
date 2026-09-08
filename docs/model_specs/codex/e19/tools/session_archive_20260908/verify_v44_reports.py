from pathlib import Path
source=Path('scratch/verify_v29_external_reports.py').read_text(encoding='utf-8')
exec(compile(source.replace('v29_external_20260908','water_route_770_20260908'),__file__,'exec'))
