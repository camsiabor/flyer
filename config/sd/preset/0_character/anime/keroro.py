from scripts.common.collection import Collection

# zhuyuan =====================================================================================

alisa_southerncross = {
    'L': {
        'XL': '<lora:alisa southerncross e1:0.8>',
        'Pony': '',
    },
    'T': 'alisa southerncross',
    'C': """
    orange hair, twintails, long hair, hair ornament, 
    fake animal ears, cat ears, 
    red eyes, 
    skirt, long sleeves, 
    black pantyhose, 
    """,
}

everyone = {
    'alisa': alisa_southerncross,
    'alisa_southerncross': alisa_southerncross
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
