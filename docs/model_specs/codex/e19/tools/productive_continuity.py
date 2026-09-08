"""Local ablations: distinguish compulsory service and preserve wheat rotations.

The frozen policy remains untouched. No top replay coordinates or dates are
used. The real engine gate must assess both production and biological safety.
"""

def install(core, renew_wheat=False):
    certificate=core._day_route_certificate
    def essential_certificate(worker,job,services=None):
        services=core._services() if services is None else services
        required=[]
        for target,commands,priority,value,kind in services:
            # Keep all observed FEED/WATER obligations, not only today's urgent
            # ones. Optional production work remains in the actual scheduler.
            commands=[c for c in commands if c[0] in {'FEED','WATER'}]
            if commands:required.append((target,commands,priority,value,kind))
        return certificate(worker,job,required)
    core._day_route_certificate=essential_certificate
    if renew_wheat:
        services=core._services
        def renewal_services():
            out=[]
            for target,commands,priority,value,kind in services():
                tile=core._tile(target)
                if tile.get('crop')=='WHEAT' and ['HARVEST'] in commands:
                    # A replacement short cycle must still mature before the
                    # horizon and be funded by observed cash, not future sales.
                    if core.final_day-core.day>=3 and core.farm['money']>=core.maintenance_floor+10:
                        commands=[c for c in commands if c[0]!='WATER']+[['PLANT','WHEAT'],['WATER']]
                out.append((target,commands,priority,value,kind))
            return out
        core._services=renewal_services
