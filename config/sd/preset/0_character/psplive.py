from scripts.common.collection import Collection

# dousha =====================================================================================

dousha = {
    'sunglass': {
        'L': '<lora:dousha-glass-pony-6-lokr-5-c16-1-b6-r2-000006:0.85>',
        'Coat': """
            DoushaCoat,
            long hair,streaked hair,multicolored hair,side braid, panda ears, 
            eyewear on head, 
            blue eyes, 
            scarf,
            blue coat,white dress, off shoulder, 
            thigh strap, 
            """,
        'Bare': """
            DoushaBare,
            long hair,streaked hair,multicolored hair,side braid, panda ears,              
            blue eyes, 
            scarf, ribbon,
            white dress, bare shoulder, 
            thigh strap,
            """
    }
}

# byb0 =====================================================================================

byb0 = {
    'game': {

    }
}

everyone = {
    'byb0': byb0,
    'dousha': dousha,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
