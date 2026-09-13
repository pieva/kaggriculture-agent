from collections import Counter
from types import SimpleNamespace
from fixes_v53 import install,net_grain_orders
assert net_grain_orders([['SELL','WHEAT',1],['BUY_PRODUCT','WHEAT',2]])==[['BUY_PRODUCT','WHEAT',1]]
assert net_grain_orders([['SELL','WHEAT',3],['BUY_PRODUCT','WHEAT',1]])==[['SELL','WHEAT',2]]
assert net_grain_orders([['SELL','MILK',3],['BUY_PRODUCT','WHEAT',1]])==[['SELL','MILK',3],['BUY_PRODUCT','WHEAT',1]]
class Core:
 def __call__(self):pass
ANIMALS={'COW':{},'SHEEP':{},'GOOSE':{}}
c=Core();c.day=25;c.final_day=29;c.active={};c.farm={'tiles':[[{'animal':'SHEEP','fed_today':False,'consecutive_unfed':1}]],'money':1000};c.private={'shed':{'WHEAT':0},'inventories':[{'WHEAT':20}]}
c._services=lambda:[((0,0),[['FEED'],['CARE']],3,10,'SERVICE')];c._growth=lambda cash:['growth'];c._market_orders=lambda:[];c._quote=lambda item,side,n:30*n
install(c)
assert c._services()==[((0,0),[['FEED']],8,1,'BIOLOGICAL')]
assert c._growth(1000)==[]
assert c._market_orders()==[['BUY_PRODUCT','WHEAT',1]], 'Unassigned distant carried grain cannot replace the depot reserve'
c.active={0:dict(target=(0,0),steps=[(['FEED'],(0,0))])}
assert c._market_orders()==[],'An assigned feeding job already carrying wheat covers its ration'
c.farm['tiles'][0][0]['fed_today']=True
assert c._growth(1000)==['growth']
c.day=29;c.private['shed']={'WHEAT':3,'MILK':2,'COW':1}
assert c._market_orders()==[['SELL','MILK',2],['SELL','WHEAT',3]]
print('9 V53 boundary checks passed')
