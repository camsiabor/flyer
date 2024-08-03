from scripts.common.collection import Collection

# Kaguya-sama: Love is War かぐや様は告らせたい～天才たちの恋愛頭脳戦

# 四宮輝夜
shinomiya_kaguya = {
    'L': {
        'Pony01': '<lora:kaguya-shinomiya-s3-ponyxl-lora-nochekaiser:${n|$$lw$$|0.925}>, kaguya shinomiya',
        'Pony02': '<lora:Shinomiya_Pony:${n|$$lw$$|0.95}>, Shinomiya_Kaguya',
    },
    'C': {
        'SchoolShort': """
        black_hair,sidelocks,folded_ponytail,parted_bangs,long_hair,
        (red_eyes:0.95),
        ribbon, (red ribbon:${rand|0.25~0.5}),
        black_dress,collared_dress,long_sleeves,black_sleeves,school_uniform,
        """,
        'School': """
        short hair,black hair,bangs,parted bangs,
        hair ribbon,sidelocks,folded ponytail,
        (red eyes:0.95),
        long sleeves, dress, (collarbone:${rand|0.0~0.01}),        
        (black dress:0.925), (white sailor collar:0.925), 
        ribbon, (red ribbon:0.975), (neck ribbon:0.95),
        school uniform, (shuuchiin academy school uniform:${rand|0.1~0.5}),
        """
    }

}

everyone = {
    'kaguya': shinomiya_kaguya,
    'shinomiya_kaguya': shinomiya_kaguya,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
