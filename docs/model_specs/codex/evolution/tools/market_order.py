"""Observable, one-shot reordering confined to a leading SELL prefix."""
from copy import deepcopy

def reorder(action):
    orders=action.get('market',[])
    indices=[i for i,o in enumerate(orders) if o and o[0]=='SELL' and o[1]=='STRAWBERRY']
    if not indices:return deepcopy(action),'no_strawberry'
    index=indices[0]
    if index==0:return deepcopy(action),'already_first'
    if not all(o and o[0]=='SELL' for o in orders[:index]):return deepcopy(action),'blocked_by_non_sale'
    result=deepcopy(action);order=result['market'].pop(index);result['market'].insert(0,order)
    assert result.get('farmer')==action.get('farmer') and result.get('hands')==action.get('hands')
    return result,'reordered'
