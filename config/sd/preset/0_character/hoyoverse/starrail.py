from scripts.common.collection import Collection

# firefly =====================================================================================

firefly = {
    'L': '<lora:firefly_V3_pony:1>',
    'T': 'firefly_(honkai:_star_rail)',
    'C': """
    (black_hairband:0.8), 
    (yellow_neckerchief:0.8), (black_jacket:0.8), 
    (sailor_jacket:0.8), (hair_intakes:0.8), (aqua_skirt:0.8)
    """,
}
firefly['Coat'] = firefly['C']

# kafka =====================================================================================

kafka = {
    'L': "<lora:kafka xl v1:0.95>",
    'T': 'kafka hsr',
    'C': """    
    long hair,purple hair,purple eyes,eyewear on head,
    white shirt, jacket, black jacket, gloves, purple gloves,
    high-waist shorts, shorts, pantyhose under shorts,
    """
}
kafka['Coat'] = kafka['C']

# everyone =====================================================================================

everyone = {
    'kafka': kafka,
    'firefly': firefly
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
