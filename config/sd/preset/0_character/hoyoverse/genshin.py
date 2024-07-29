from scripts.common.collection import Collection

# zhuyuan =====================================================================================


clorinde = {
    'L': '<lora:clorinde_pony:0.9>,clorinde_(genshin_impact)',
    'T': 'clorinde_(genshin_impact)',
    'C': """
    white gloves,tricorne,black pantyhose,
    pencil skirt,black jacket,fold-over boots,
    ascot,thigh strap,white shirt,underbust,blue cape
    """,
}

everyone = {
    'clorinde': clorinde
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
