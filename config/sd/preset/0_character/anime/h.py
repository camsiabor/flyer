from scripts.common.collection import Collection

# zhuyuan =====================================================================================

tsubaki = {
    'C': {
        'App': """
            souryuu asuka langley, rebuild of evangelion,
            blonde hair, long hair,
            blue eyes, (multicolored eyes:$[rand|0.0~0.5]),
            """,
        'Plugsuit': """        
            plugsuit, (red plugsuit:$[rand|0.16~0.66]), (white plugsuit:$[rand|0.0~0.25]),        
            """,
    }
}

everyone = {
    'tsubaki': tsubaki,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
