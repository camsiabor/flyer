from scripts.common.collection import Collection

# firefly =====================================================================================

firefly = {
    'L': '<lora:firefly_V3_pony:1>, firefly_(honkai:_star_rail)',
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
            (brown hair:1.15), medium hair, hair ornament,
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

# fei xiao =====================================================================================

fei_xiao = {
    'L': {
        'Pony01': '<lora:feixiao-pony:${n|$$lw$$|0.95}>,FEI XIAO',
        'Pony02': '<lora:SH_HSR_Feixiao_Civ:${n|$$lw$$|0.7}>,SH_HSR_Feixiao,',
    },
    'C': {
        'App': """
            (white hair:0.95), very long hair, 
            gradient hair, (teal hair tips:0.95), high ponytail, 
            forehead mark, 
            (aquamarine eyes:0.95), (red eyeliner:0.95), 
            animal ears, earring, 
            """,
        '01':
            """FEI XIAO REGULAR WEAR""",
        'Coat': """
            white coat, open clothes, long sleeves,
            teal dress, chinese clothes,             
            belt, gloves, 
            thigh strap, 
            """,
        'Bare': """
            bare shoulders, long sleeves, 
            tattoo, (back tattoo:0.1), 
            teal dress, chinese clothes,             
            belt, gloves, 
            thigh strap, 
            """,
        "Shoe":
            "black footwear,knee boots"
    }
}

# everyone =====================================================================================

everyone = {
    'kafka': kafka,
    'firefly': firefly,
    'ruan_mei': ruan_mei,
    'yun_li': yun_li,
    'fei_xiao': fei_xiao,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
