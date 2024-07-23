from config.common import PresetCommon


def init(*_):
    data = [
        # "from back, looking back, standing",
        "lying, on side",
        "lying, on stomach",
        "lying, on stomach, pov, close-up",
        "lying, on back",
        "lying, on back, from above, front view",
    ]
    return PresetCommon.to_array(data)
