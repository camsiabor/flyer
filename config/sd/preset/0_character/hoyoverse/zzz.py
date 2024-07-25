from config.common import PresetCommon

zhuyuan = {
    'L': '<lora:Zhu_Yuan__ZZZ__Pony:0.7>,imtdzhuyuan',
    'C': """
    black hair,red hair,two tone hair,multicolored hair,streaked hair,bangs,ponytail,red eyes,
    cropped jacket,gloves,blue jacket,green necktie,collared shirt,pants,bodysuit,uniform,police,
    """,

    'L02': '<lora:zzz_zhuyuan_ponyXL:1>,zhuyuan',
    'C02': """
    ponytail,streaked hair,black and red hair,
    orange eyes, green necktie,
    police uniform,blue jacket,long sleeves,black vest,
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
    picks = PresetCommon.dict_pick(everyone, cmd, True)
    return picks
