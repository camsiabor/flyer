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
                (grey hair:0.95), (purple eyes:0.95), twintails, hair ribbon
            """,
            'Cloth': """
                (white and purple dress:0.95), 
                long sleeves, belt
            """,
            'Capelet': """
                (black capelet:0.95), 
                (green strap:0.95), (white and purple dress:0.95), 
                long sleeves, belt
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


everyone = {
    'tsubaki': tsubaki,
    'keroro': keroro,
    'black_clover': black_clover,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
