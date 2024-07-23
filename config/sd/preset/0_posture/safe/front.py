from config.common import PresetCommon


def init(*_):
    data = [
        "spread legs, hand on own face",
        "spread legs, hand on own chest",
        "hugging own legs",
    ]
    return PresetCommon.to_array(data)
