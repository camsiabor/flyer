from scripts.common.collection import Collection

# zhuyuan =====================================================================================

asuka = {
    'C': {
        'Plugsuit': """
        souryuu asuka langley, rebuild of evangelion,
        blonde hair, long hair,
        blue eyes, (multicolored eyes:${rand|0.0~0.5}),
        plugsuit, (red plugsuit:${rand|0.16~0.66}), (white plugsuit:${rand|0.0~0.25}),        
        """
    }
}

everyone = {
    'asuka': asuka,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
