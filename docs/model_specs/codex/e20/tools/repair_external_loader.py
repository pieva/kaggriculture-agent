"""Preserve the frozen experiment and repair only its exec-loader filename."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OLD = ROOT / 'submission/submission_codex_e20_772_e20v28_candidate.py'
NEW = OLD.with_name('submission_codex_e20_772_e20v28_loaderfix.py')


def build():
    assert hashlib.sha256(OLD.read_bytes()).hexdigest() == '83d3f548a3a704c60ad27dd61dfc1e9badf230c1129623161f965025878e3ba1'
    lines = OLD.read_text(encoding='utf-8').splitlines(keepends=True)
    changed = 0
    for i, line in enumerate(lines):
        if line.lstrip().startswith('exec(compile(') and 'str(Path(__file__))' in line:
            lines[i] = line.replace('str(Path(__file__))', "'<e20-embedded>'")
            changed += 1
    assert changed == 2
    assert not NEW.exists()
    NEW.write_text(''.join(lines), encoding='utf-8')
    manifest = dict(variant='E20v28', repair='exec loader without __file__',
                    parent_sha256=hashlib.sha256(OLD.read_bytes()).hexdigest(),
                    sha256=hashlib.sha256(NEW.read_bytes()).hexdigest(),
                    uploaded=False, independent_gate_passed=False)
    NEW.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    build()
