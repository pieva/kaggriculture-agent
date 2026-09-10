"""Exercise Kaggle's exec namespace, which does not supply __file__."""
from pathlib import Path
from unittest.mock import patch
import pytest

ROOT = Path(__file__).resolve().parents[5]


@pytest.mark.parametrize('seat', [0, 1])
def test_exec_loader_without_file_or_filesystem(seat):
    path = ROOT / 'submission/submission_codex_e20_772_e20v28_loaderfix.py'
    source = path.read_text(encoding='utf-8')
    scope = {}
    with patch('builtins.open', side_effect=AssertionError('file access')), \
         patch('io.open', side_effect=AssertionError('file access')):
        exec(compile(source, '<kaggle-exec>', 'exec'), scope)
        assert '__file__' not in scope
        policy = scope['create_agent']({'player_position': seat})
    assert policy.core.seat == seat
    assert policy.core.e20_reserved == {(4, 5): 'COW', (4, 6): 'SHEEP'}
