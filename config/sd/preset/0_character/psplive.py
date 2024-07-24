from config.common import PresetCommon

byb0 = {
    'game': {

    }
}

everyone = {
    'byb0': byb0
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = PresetCommon.dict_pick(everyone, cmd, True)
    return picks
