from scripts.common.collection import Collection

# zhuyuan =====================================================================================


clorinde = {
    'L': '<lora:clorinde_pony:0.9>,clorinde_(genshin_impact)',
    'T': 'clorinde_(genshin_impact)',
    'C': """
    white gloves,tricorne,black pantyhose,
    pencil skirt,black jacket,fold-over boots,
    ascot,thigh strap,white shirt,underbust,blue cape,     
    """,
}

emilie = {
    'L': {
        'Pony': '<lora:Emilie_Genshin_Impact_Pony:$[n|$$lw$$|0.8]>, EmilieGI'
    },
    'C': {
        'App': """
        short hair, (blonde hair:0.95), multicolored hair, hat, 
        (purple eyes:0.95), 
        glasses, (semi-rimless eyewear:0.1),
        (elbow gloves:0.6), (black gloves:0.6), 
        dress,
        """
    }
}

everyone = {
    'clorinde': clorinde,
    'emilie': emilie,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
