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
    'L': [
        "<lora:honkai-kafka-ponyxl-lora-nochekaiser:1>, kafka",
        "<lora:kafka xl v1:0.95>, kafka hsr",

    ],
    'T': [
        'kafka', 'kafka hsr',
    ],
    'C': {
        'Coat': """    
        long hair,purple hair,purple eyes,eyewear on head,
        white shirt, jacket, black jacket, gloves, purple gloves,
        high-waist shorts, shorts, black pantyhose under shorts,
        """,
        "Min": """
        long hair, purple hair, eyewear on head,
        purple eyes, 
        gloves, (purple gloves:0.5),  
        """,
        "Rand": """
        ((white shirt, jacket, black jacket, high-waist shorts, shorts, black pantyhose under shorts):${rand|0.15~0.9}),
        """
    },
}

# ruan mei =====================================================================================

ruan_mei = {
    'L': {
        'Pony': '<lora:Char-HonkaiSR-Ruanmei-Pony-V1:${n|$$lw$$|0.9}>, ruan mei (honkai: star rail),'
    },
    'C': {
        '0': """
            (brown hair:1.1), medium hair, hair ornament,
            (teal eyes:0.9), 
            necklace, bare shoulders, 
            detached collar, capelet,
            china dress, (green gloves:0.9),
            thigh strap,
            (plum flower:0.9),
            """,
    }

}

# yun li =====================================================================================

yun_li = {
    'L': {
        'Pony': '<lora:HSR_YL:${n|$$lw$$|1}>,HSR_YL',
    },
    'C': {
        '0': """
        short hair with long locks,
        hair between eyes,hair ornament,
        ponytail,low ponytail,double ponytail,
        dark blue hair, crown,
        yellow eyes, single earrings, 
        bare shoulders,sleeveless,sleeveless cheongsam,
        chinese dress,
        thigh strap,anklet,jewelry
        """
    }

}

# everyone =====================================================================================

everyone = {
    'kafka': kafka,
    'firefly': firefly,
    'ruan_mei': ruan_mei,
    'yun_li': yun_li,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
