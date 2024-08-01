from scripts.common.collection import Collection

sorasaki_hina = {
    'L': {
        'Pony': '<lora:Sorasaki_Hina_Pony:${n|$$lw$$|0.95}>,Hina_(Blue_Archive)',
    },
    'C': {
        'App': """
        halo, (black_horns:1.05),demon_girl,demon_horns,
        (white_hair:1.125), very_long_hair, ahoge, parted_bangs,
        purple_eyes,
        (demon_wings:${rand|0.0~0.75}),
        """,
        "Coat": """
        hairclip,
        black_coat, coat_on_shoulders, fur-trimmed_coat, 
        black_skirt, black_belt,  
        black_gloves, black_thighhighs, military_uniform
        """,
        "Dress": """
        wavy_hair, sidelocks, 
        hair_ribbon, black_ribbon,
        dangle_earrings, 
        necklace, pearl_necklace, 
        purple_dress, strapless_dress,
        elbow_gloves, purple_gloves, 
        purple_pantyhose        
        """
    },
}

# everyone =====================================================================================

everyone = {
    'hina': sorasaki_hina,
    'sorasaki_hina': sorasaki_hina,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
