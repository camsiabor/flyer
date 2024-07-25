from config.common import PresetCommon

firefly = {
    'L': '<lora:firefly_V3_pony:1>, firefly_(honkai:_star_rail)',
    'C': """
    (black_hairband:0.8), 
    (yellow_neckerchief:0.8), (black_jacket:0.8), 
    (sailor_jacket:0.8), (hair_intakes:0.8), (aqua_skirt:0.8)
    """,
}

everyone = {
    'firefly': firefly
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = PresetCommon.dict_pick(everyone, cmd, True)
    return picks
