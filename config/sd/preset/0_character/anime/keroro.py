from scripts.common.collection import Collection

# zhuyuan =====================================================================================

alisa_southerncross = {
    'L': [
        # animagine-3.1
        '<lora:alisa southerncross e1:0.55>, (alisa southerncross:0.985)',
        # pony
        '<lora:alisasr:0.75>, alisasr',

    ],
    'T': 'alisa southerncross',
    'C': """
    orange hair, (low twintails:1.05), long hair,
    hair ornament, (blue hair bobble:0.8),
    black fake animal ears, cat ears,
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
