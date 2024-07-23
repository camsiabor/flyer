from config.common import PresetCommon


def init(*_):
    data = [
        "on one knee, holding a pistol",
        "on one knee, holding a pistol in both hands",
        "on one knee, shouldering a rifle, holding a rifle",
        "on one knee, shouldering a rifle, holding a rifle, firing",
        "on one knee, shouldering a rifle, holding a rifle, aiming at viewer",
        # "lying prone while holding a rifle, prone aiming",
        # "lying prone while holding a rifle, prone aiming, firing",
    ]
    return PresetCommon.to_array(data)
