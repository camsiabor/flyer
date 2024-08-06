from typing import List

from scripts.common.collection import Collection


# QShare ===================================================================================== #

class QCon:
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

class QSee:
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
    class Mouth:
        class Fellatio:
            all = [
                "implied fellatio"
                "fellatio",
                "vacuum fellatio, blowjob face",
                "licking penis",
                "forced fellatio, irrumatio",
                "deep throat",
                "licking testicles",
                "after fellatio",
            ]

    class Breast:
        titfuck = [
            "paizuri, titfucking, nipples, penis",
            "paizuri, titfucking, nipples, penis, breasts squeezed together, fellatio, licking penis"
        ]

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
        head_1st = ["hand on head", "hands on head", ]
        head_2nd = ["hand on another's head", "hands on another's head", ]
        head_all = [*head_1st, *head_2nd]

        breast_1st = ["grabbing own breast", "hand on own chest"]
        breast_2nd = ["grabbing another's breast"]
        breast_all = [*breast_1st, *breast_2nd]

        hair_2nd = ["grabbing_another's_hair", "pulling_another's_hair"]

        handjob = [
            "handjob", "double handjob", "reach-around", "nursing handjob", "two-handed handjob"
        ]

        masturbation = [
            "masturbation", "female masturbation"
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

    class Lying:
        all = [
            "lying",
            "lying, on back",
            "lying, on stomach",
            "lying, on side",
        ]
        # QPos

    pass
