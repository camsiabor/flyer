from scripts.common.collection import Collection

# Shoujo☆Kageki Revue Starlight

# 花柳香子
kaoruko_hanayagi = {
    'L': {
        'Pony': '<lora:Kaoruko_Hanayagi:0.9>, kaoruko',
    },
    'T': 'kaoruko',
    'C': {
        'Stage': """
        (blue hair:0.9), medium hair,
        (light brown eyes:0.9),
        stage outfit, pleated skirt, fur-trimmed jacket, 
        (yellow belt:0.8), 
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
