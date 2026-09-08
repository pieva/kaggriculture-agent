"""Protect a mature wheat cycle from decay; preserve its replacement cycle."""
from docs.model_specs.codex.e19.tools.productive_continuity import install as install_essential

def install(core):
    install_essential(core,renew_wheat=True)
    services=core._services
    def deadline_services():
        out=[]
        for target,commands,priority,value,kind in services():
            tile=core._tile(target)
            if tile.get('crop')=='WHEAT' and ['HARVEST'] in commands:
                age=core.day-tile['planted_day']
                # WATER before HARVEST raises current yield; WATER after PLANT
                # protects the replacement. These are distinct obligations.
                if not tile.get('watered_today') and 2<=age<=4 and commands[0]!=['WATER']:
                    commands=[['WATER']]+commands
                # Final maximal-yield day precedes rapid step-wise decay.
                if age>=4:priority=3
                if core.final_day-core.day<4:
                    # The replacement must reach its actual max-yield age.
                    commands=commands[:commands.index(['HARVEST'])+1]
            out.append((target,commands,priority,value,kind))
        return out
    core._services=deadline_services
