from scripts.common.collection import Collection

# Shoujo☆Kageki Revue Starlight

# 花柳香子
kaoruko_hanayagi = {
    'L': {
        'Pony': '<lora:Kaoruko_Hanayagi:0.8>, kaoruko',
    },
    'T': 'kaoruko',
    'C': {
        'Stage': """
        (blue hair:0.9), medium hair,
        (light brown eyes:0.9), (multicolored eyes:$[rand|0.1~0.25]),
        (stage outfit:$[rand|0.5~1.0]), pleated skirt, (fur-trimmed jacket${rand|0.5~1.0]), 
        (yellow belt:0.8), 
        """,
        'School': """
        (blue hair:0.9), medium hair,
        (light brown eyes:0.9), (multicolored eyes:$[rand|0.1~0.25]),
        (school uniform:$[rand|0.75~1.0]),
        (red bowtie:$[rand|0.7~0.9]), 
        (white shirt:$[rand|0.8~1.0]), (grey skirt:$[rand|0.8~1.0]), 
        (gray jacket:$[rand|0.5~1.0]), 
        (pleated skirt:0.9),
        """
    }

}

everyone = {
    # kaoruko hanayagi
    'kaoruko': kaoruko_hanayagi,
    'kaoruko_hanayagi': kaoruko_hanayagi,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
