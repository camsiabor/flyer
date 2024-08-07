from scripts.common.collection import Collection

# tsubaki (H) =====================================================================================

tsubaki = {
    'C': {
        'App': """
            souryuu asuka langley, rebuild of evangelion,
            blonde hair, long hair,
            blue eyes, (multicolored eyes:$[rand|0.0~0.5]),
            """,
        'Plugsuit': """        
            plugsuit, (red plugsuit:$[rand|0.16~0.66]), (white plugsuit:$[rand|0.0~0.25]),        
            """,
    }
}

# keroro =====================================================================================

keroro = {
    'alisa': {
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
}

# black_clover =====================================================================================

black_clover = {
    'noelle_silva': {
        'L': {
            'Pony': '<lora:noellesilva-pdxl-nvwls-v1:$[n|$$lw$$|0.95]>, noelle silva',
        },
        'C': {
            'App': """
                (grey hair:0.95), twintails, 
                hair ribbon, (purple ribbon:0.9),
                (purple eyes:0.95)                
            """,
            'Cloth': """
                (white and purple dress:0.95), long sleeves, belt
            """,
            'Capelet': """                                 
                (black capelet:0.95), (green strap:0.95), 
                (white and purple dress:0.95), long sleeves, 
                belt
            """,
            'Armor': """
                crown, head wings, wings, halo, strapless, 
                armored dress, gauntlets, (blue thighhighs:0.95)
            """,
            "Mermaid": """
                mermaidnoelle, mermaid, 
                tiara, choker, bikini armor, bare shoulders, scales
            """,
        }
    }
}

# bleach =====================================================================================

bleach = {
    # Riruka Dokugamine
    'riruka': {
        'L': {
            'Pony': "<lora:RirukaDokugamine:$[n|$$lw$$|0.9]>, RirukaDokugamine",
        },
        'C': {
            'App': """long hair, (magenta eyes:0.85), twintails, (magenta hair:0.85)""",
            'Cloth': """
                hat, fur hat,                
                dress, (black dress:0.9), 
                (bow:0.1), (striped:0.9),
                gloves, (white gloves:0.95),
                thighhighs, zettai ryouiki,                            
                """,
            'Shoe': """thigh boots, (black boots:0.9)"""
        }
    }
}

# ============================================================================================

everyone = {
    'bleach': bleach,
    'black_clover': black_clover,
    'keroro': keroro,
    'tsubaki': tsubaki,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
