"""Regression checks for observed recovery and profile restoration."""
from dataclasses import dataclass
from types import SimpleNamespace
from workforce_v52c import install
@dataclass(frozen=True)
class Profile:
    maximum_hands:int=12
def run(day,tile,expected):
    c=SimpleNamespace(day=day,hour=0,farm={'tiles':[[tile]]},profile=Profile())
    original=c.profile
    c._market_orders=lambda:[['HIRE'] for _ in range(c.profile.maximum_hands)]
    install(c)
    assert len(c._market_orders())==expected
    assert c.profile is original
for day,tile,expected in [(10,{},12),(11,{},11),(28,{},11),(29,{},12),
                          (15,{'animal':'COW','consecutive_unfed':1},12),
                          (15,{'crop':'WHEAT','consecutive_unwatered':2},12),
                          (15,{'crop':'WHEAT','consecutive_unwatered':1},11)]:run(day,tile,expected)
print('7 workforce boundary/recovery checks passed')
