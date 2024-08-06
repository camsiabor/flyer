from typing import List

from scripts.common.collection import Collection


# QShare ===================================================================================== #

class QShare:
    @staticmethod
    def weight(
            lower: float = 0.5,
            upper: float = 1.0,
            *args
    ) -> List[str]:
        prefix = '$[rand|'
        suffix = f'{lower}~{upper}]'
        ret = Collection.clamp(args, prefix, suffix, True)
        return ret

    pass


# QAngle ===================================================================================== #

class QAngle:
    back = [
        "from behind", "from back"
    ]
    extra = [
        "pov", "dutch angle", "foreshortening", "fisheye"
    ]
    common = [
        "from above", "from side", "from below"
    ]
    pass


# QPos ===================================================================================== #

class QPos:
    class Arm:
        up = [
            "arm up, armpit",
            "arms up, armpits",
            "arm up, arm behind head",
            "arms up, arms behind head",
        ]
        behind = [
            "arms behind back", "arms behind head",
        ]

    class Hand:
        on_head = [
            "hand on head", "hands on head",
            "hand on another's head", "hands on another's head",
        ]

    class Leg:
        top_down = [
            "top-down bottom-up"
        ]
        kneeling = [
            "kneeling", "kneeling, all fours", "on one knee"
        ]
        squalting = [
            "squatting", "squatting, spread legs"
        ]
        # Leg
        pass

        # QPos

    pass
