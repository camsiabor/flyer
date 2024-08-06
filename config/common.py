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
        prefix = ""
        suffix = ""
        if lower >= 0 and upper >= 0:
            prefix = "("
            if lower == upper:
                suffix = f":{lower})"
            else:
                suffix = f':$[rand|{lower}~{upper}])'
        ret = Collection.clamp(args, prefix, suffix, True)
        return ret

    pass

    @staticmethod
    def by(
            data: list,
            is_lift: bool = False,
            is_pull: bool = False,
            is_spread: bool = False,
            is_aside: bool = False,
            by_self: bool = False,
            by_another: bool = False,
    ) -> List[str]:
        prefix = ""
        suffix = ""
        if is_aside:
            prefix += " aside "
        if is_lift:
            suffix += " lift, lifted "
        if is_pull:
            suffix += " pull, pulled "
        if is_spread:
            prefix += "spread "
            suffix += ", spread"
        if by_self:
            suffix += " by self "
        if by_another:
            suffix += " by another "
        ret = Collection.clamp(data, prefix, suffix)
        return ret


# QAngle ===================================================================================== #

class QSee:
    back = [
        "from behind", "from back"
    ]
    back_ass = [
        "from behind, ass", "from back, ass",
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
            pass

        pass

    class Breast:
        titfuck = [
            "paizuri, titfucking, nipples, penis",
            "paizuri, titfucking, nipples, penis, breasts squeezed together, fellatio, licking penis"
        ]
        pass

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
        pass

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

        spread_pussy = ["spread pussy", ]
        spread_anus = ["spread anus", "spread ass"]
        spread_all = [*spread_anus, *spread_pussy, *spread_pussy]

        pass

    class Finger:
        masturbation = [
            "masturbation", "female masturbation"
        ]
        to_mouth_1st = [
            "finger to own mouth",
            "finger in own mouth"
        ]
        to_mouth_2nd = [
            "finger to another's mouth",
            "finger in another's mouth"
        ]
        to_pussy = [
            "implied fingering",
            "fingering",
            "fingering through clothes",
        ]
        to_anal = [
            "anal fingering"
        ]
        to_pussy_anal = [*to_pussy, *to_anal]
        pass

    class Pelvic:
        rub = ["crotch rub"]
        pass

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
        up = [
            "leg up", "legs up", "leg lift", "legs lift"
        ]
        split = [
            "standing, standing split, standing on one leg"
        ]
        lock = [
            "leg lock"
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

    pass


# QCloth ===================================================================================== #

class QCloth:
    outer = [
        "clothes", "shirt", "skirt", "dress", "bra",
    ]
    lingerie = [
        "lingerie", "bra", "panties", "thong"
    ]
    pass
