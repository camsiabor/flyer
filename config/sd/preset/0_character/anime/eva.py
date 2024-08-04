from scripts.common.collection import Collection

# zhuyuan =====================================================================================

asuka = {
    'C': {
        'App': """
        souryuu asuka langley, rebuild of evangelion,
        blonde hair, long hair,
        blue eyes, (multicolored eyes:${rand|0.0~0.5}),
        """,
        'Plugsuit': """        
        plugsuit, (red plugsuit:${rand|0.16~0.66}), (white plugsuit:${rand|0.0~0.25}),        
        """,
    }
}

rei = {
    'C': {
        'App': """
        ayanami rei, rebuild of evangelion,
        blue hair, short hair, headgear,
        red eyes, (multicolored eyes:${rand|0.0~0.5}),
        """,
        'Plugsuit': """        
        plugsuit, (blue plugsuit:${rand|0.1~0.5}), (white plugsuit:${rand|0.25~0.75}),        
        """,
        'PlugSuitBlack': """
        plugsuit, (black plugsuit:${rand|0.33~0.75}),        
        """,
        'School': """
        school uniform, (tokyo-3 middle school uniform:${rand|0.25~0.5}),
        ribbon, neck ribbon, red ribbon,
        shirt, white shirt, short sleeves,
        skirt    
        """,
    }
}

everyone = {
    'asuka': asuka,

    'rei': rei,
    'ayanami rei': rei,

}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
