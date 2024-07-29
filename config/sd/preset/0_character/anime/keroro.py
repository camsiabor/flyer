from scripts.common.collection import Collection

# zhuyuan =====================================================================================

zhuyuan = {
    'L': '<lora:Zhu_Yuan__ZZZ__Pony:0.7>',
    'T': 'imtdzhuyuan',
    'C': """
    black hair, red hair,two tone hair,multicolored hair,streaked hair,bangs,ponytail,red eyes,
    cropped jacket, gloves, collared shirt, pants, necktie, bodysuit,uniform,police,
    """,
    'C01': """
    black hair, red hair,two tone hair,multicolored hair,streaked hair,bangs,ponytail,red eyes,
    cropped jacket, gloves, collared shirt, pants, bodysuit,uniform,police,
    (green necktie:0.5), (blue jacket:0.5), 
    """,

    'L02': '<lora:zzz_zhuyuan_ponyXL:1>',
    'T02': 'zhuyuan',
    'C02': """
    ponytail,streaked hair,black and red hair,
    orange eyes,blue jacket, green necktie,
    police uniform,,long sleeves,black vest,
    white shirt,collared shirt,
    black gloves,black pants, belt,
    """

}

everyone = {
    'zhuyuan': zhuyuan
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(everyone, cmd, True)
    return picks
