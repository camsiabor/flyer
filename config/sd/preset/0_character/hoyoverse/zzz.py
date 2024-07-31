from scripts.common.collection import Collection

# ellen joe =====================================================================================

ellen_joe = {
    'L': {
        'Pony': '<lora:ellen_joe_pony:0.925>,ellen_joe'
    },
    'C': """
    maid_headdress, 
    black_hair, colored_inner_hair, multicolored_hair, short_hair, two_tone_hair,
    (red eyes:0.9), mole_under_eye, ear_piercing, piercing, 
    (black_dress:0.9), frilled_dress,
    wrist_cuffs, puffy_short_sleeves,
    black_pantyhose,      
    """
}

# zhuyuan =====================================================================================

zhuyuan = {
    'L': {
        'Pony1': '<lora:Zhu_Yuan__ZZZ__Pony:0.7>, imtdzhuyuan',
        'Pony2': '<lora:zzz_zhuyuan_ponyXL:1>, zhuyuan',
    },
    'T': 'imtdzhuyuan',

    'C': {
        '1': """
        black hair, red hair,two tone hair,multicolored hair,streaked hair,bangs,ponytail,red eyes,
        cropped jacket, gloves, collared shirt, pants, necktie, bodysuit,uniform,police,
        """,
        '2': """
        black hair, red hair,two tone hair,multicolored hair,streaked hair,bangs,ponytail,red eyes,
        cropped jacket, gloves, collared shirt, pants, bodysuit,uniform,police,
        (green necktie:0.5), (blue jacket:0.5), 
        """,
        '3': """
        ponytail,streaked hair,black and red hair,
        orange eyes,blue jacket, green necktie,
        police uniform,,long sleeves,black vest,
        white shirt,collared shirt,
        black gloves,black pants, belt,
        """
    },
}

# everyone =====================================================================================

everyone = {
    'ellen_joe': ellen_joe,
    'zhuyuan': zhuyuan
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
