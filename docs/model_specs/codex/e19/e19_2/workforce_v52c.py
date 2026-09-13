"""One fewer ordinary hand, with observed stress restoring baseline capacity."""
from dataclasses import replace

def install(core):
    original=core._market_orders
    core.v52_staffing_log=[]
    def market():
        if core.day<11 or core.day>=29:return original()
        stressed=any((t.get('animal') and t.get('consecutive_unfed',0)>=1)
                     or (t.get('crop') and t.get('consecutive_unwatered',0)>=2)
                     for row in core.farm['tiles'] for t in row if isinstance(t,dict))
        profile=core.profile
        cap=profile.maximum_hands if stressed else max(0,profile.maximum_hands-1)
        core.profile=replace(profile,maximum_hands=cap)
        try:orders=original()
        finally:core.profile=profile
        core.v52_staffing_log.append(dict(day=core.day+1,hour=core.hour+1,cap=cap,stress=stressed,hires=sum(o==['HIRE'] for o in orders)))
        return orders
    core._market_orders=market
