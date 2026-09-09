"""Check report completeness and local links; seal delivered evidence hashes."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'


class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.images=[]

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
        if tag=='img':self.images.append(attrs['src'])


def main():
    report=OUT/'REPORT_V49_PASS_IT.html'
    parsed=Links();parsed.feed(report.read_text(encoding='utf-8'))
    for link in parsed.links+parsed.images:
        if '://' not in link:assert (OUT/link.split('#')[0]).exists(),link
    assert len(parsed.images)==30,len(parsed.images)
    summary=json.loads((OUT/'summary.json').read_text())
    assert summary['selected_variant']=='v49f'
    assert summary['development']['n']==6 and summary['validation']['n']==4
    assert {p['seat'] for p in summary['parity']}=={0,1}
    assert all(p['actions']==719 and p['mismatches']==0 for p in summary['parity'])
    equivalence=json.loads((OUT/'opening_equivalence.json').read_text())
    assert len(equivalence)==10
    assert all(r['d2_closed_farm_and_private_equal'] for r in equivalence)
    opened=json.loads((OUT/'validation_opened.json').read_text())
    assert opened['candidate_sha256']==summary['candidate_sha256']
    manifest={p.relative_to(ROOT).as_posix():dict(bytes=p.stat().st_size,
        sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='report_manifest.json'}
    result=dict(report=report.relative_to(ROOT).as_posix(),images=len(parsed.images),
        local_links_ok=True,paired_cases=10,parity_seats=[0,1],
        candidate_sha256=summary['candidate_sha256'],files=manifest)
    (OUT/'report_manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='files'}))


if __name__=='__main__':main()
