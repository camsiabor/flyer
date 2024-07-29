from scripts.common.collection import Collection

# dousha =====================================================================================

shiori = {
    'white': {
        'L': {
            'Fuse': '<lora:shiori-white-pony-6-lokr-5-c-16-1-r11-000016:0.9>',
        },
        'C': {
            'Hat': """
            white beret, bow,
            light brown hair,(streaked hair:1.15),medium hair,
            hair ornament, two side up, (animal ears:1), (pink bow:0.55),  
            blue eyes, multicolored eyes,            
            choker,
            bare shoulders,
            white shirt,blue skirt,
            white thighhighs,
            european architecture,indoors,
            """
            ,
            'Hood': """
            hood_up, animal hood, 
            (light brown hair:1), (streaked hair:1.15), medium hair, 
            blue eyes, round eyes, beautiful eyes, multicolored eyes, 
            choker, 
            white shirt, blue skirt, white and blue short jacket, 
            white thighhighs, thigh strap, 
            """
        }
    }
}

# byb0 =====================================================================================


everyone = {
    # kankan shiori
    'kankan': shiori,
    'shiori': shiori,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
