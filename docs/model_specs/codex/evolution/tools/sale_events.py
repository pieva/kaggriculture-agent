"""Expose verified sale timestamps from the existing settlement auditor."""
import inspect
from docs.model_specs.codex.e18.tools import build_e18_26_jesse_770_d30_closure as settlement

def audit_with_sales(replay,seat):
    source=inspect.getsource(settlement.audit)
    anchor='    days = [';assert source.count(anchor)==1
    source=source.replace(anchor,'    sale_events = []\n'+anchor)
    anchor='                ledger["sales_cash"][item] += price';assert source.count(anchor)==1
    source=source.replace(anchor,anchor+'\n                sale_events.append(dict(step=index,day=day+1,hour=previous[0]["observation"]["hour"]+1,item=item,price=price))')
    anchor='return {"daily": days,';assert source.count(anchor)==1
    source=source.replace(anchor,'return {"sale_events": sale_events, "daily": days,')
    scope=dict(settlement.__dict__);exec(compile(source,__file__,'exec'),scope)
    result=scope['audit'](replay,seat)
    assert len(result['sale_events'])==sum(sum(d['sold_units'].values()) for d in result['daily'])
    return result
