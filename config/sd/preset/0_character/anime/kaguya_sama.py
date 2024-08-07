from scripts.common.collection import Collection

# Kaguya-sama: Love is War かぐや様は告らせたい～天才たちの恋愛頭脳戦

# 四宮輝夜
# (collarbone:$[rand|0.0~0.01])
shinomiya_kaguya = {
    'L': {
        'Pony00': '<lora:kaguya-shinomiya-s3-ponyxl-lora-nochekaiser:$[n|$$lw$$|0.85]>, kaguya_shinomiya',
        'Pony01': '<lora:loveiswarXL2:$[n|$$lw$$|0.85]>, shinomiya_kaguya',
        'Pony02': '<lora:Shinomiya_Pony:$[n|$$lw$$|0.9]>, Shinomiya_Kaguya',
    },
    'C': {
        'School00': """
            black hair,hair ribbon,
            neck ribbon,
            (red eyes:0.95),
            (white sailor collar:0.95), (red ribbon:0.95),
            (black dress:0.975), long sheeves,
            """,
        'School01': """
            black_hair,sidelocks,folded_ponytail,parted_bangs,long_hair,
            (red_eyes:0.95),
            ribbon, (red ribbon:$[rand|0.25~0.5]),
            black_dress,collared_dress,long_sleeves,black_sleeves,school_uniform,
            """,
        'School02': """
            short hair, (black_hair:0.9), bangs,parted bangs,
            hair ribbon, (red_hair_ribbon:0.55), sidelocks,folded ponytail,
            (red_eyes:0.95),
            long sleeves, dress,         
            (black_dress:0.925), (white_sailor_collar:0.925), 
            ribbon, (neck_ribbon:0.95), (red_neck_ribbon:0.95),
            school uniform, (shuuchiin academy school uniform:$[rand|0.1~0.5]),
            """

    }
}

hayasaka_ai = {
    'L': {
        'Pony': "<lora:ai-hayasaka-s3-ponyxl-lora-nochekaiser:$[n|$$lw$$|0.9]>,ai hayasaka",
    },
    'C': {
        'App': """
            blonde hair, hair between eyes, bangs, sidelocks,side ponytail,
            hair ornament, hair scrunchie, blue scrunchie,
            (blue eyes:0.95), 
            """,
        'School': """
            school uniform, (shuuchiin academy school uniform:$[rand|0.1~0.5]),
            shirt, sweater, cardigan, long sleeves, 
            clothes around waist, sweater around waist, cardigan around waist,
            """,
        'School02': """
            school uniform, (shuuchiin academy school uniform:$[rand|0.1~0.5]),
            shirt, (white shirt:0.95), long shirt, long sleeves, 
            sweater, (black sweater:0.95),  
            (brown cardigan:0.95), cardigan around waist,
            """,
        'Maid': """
            shirt, long sleeves, dress, 
            white shirt, collared shirt, 
            apron, maid, maid headdress, 
            ascot, waist apron,
            """,
        'Shoe': """
            shoes, socks, black socks
            """
    },
}

chika_fujiwara = {
    'L': {
        'Pony': "<lora:chika-fujiwara-s3-ponyxl-lora-nochekaiser:$[n|$$lw$$|0.9]>, chika fujiwara"
    },
    'C': {
        'App': """
            long hair, (pink hair:0.95), 
            bangs, blunt bangs, 
            bow, hair bow, (black bow:0.95),
            (blue eyes:0.95),
            (large breasts:0.9),
            """,
        'School': """             
            school uniform, (shuuchiin academy school uniform:$[rand|0.1~0.5]),
            dress, (black dress:0.95), long sleeves, 
            sailor collar, (white sailor collar:0.95), 
            ribbon, (red ribbon:0.95), neck ribbon, 
            """
    }
}

everyone = {
    'kaguya': shinomiya_kaguya,
    'shinomiya_kaguya': shinomiya_kaguya,

    'hayasaka': hayasaka_ai,
    'hayasaka_ai': hayasaka_ai,

    'chika': chika_fujiwara,
    'chika_fujiwara': chika_fujiwara,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
