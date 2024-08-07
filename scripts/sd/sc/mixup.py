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
        fellatio = [
            "implied fellatio",
            "fellatio",
            "vacuum fellatio, blowjob face",
            "licking penis",
            "forced fellatio, irrumatio",
            "deep throat",
            "licking testicles",
            "after fellatio",
            "oral_invitation",
        ]
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
        v_sign = [
            "peace sign, v, v hand",
            "peace sign, v, v hands",

        ]

        on_head_1st = ["hand on head", "hands on head", ]
        on_head_2nd = ["hand on another's head", "hands on another's head", ]
        on_head_all = [*on_head_1st, *on_head_2nd]

        chest_1st = ["hand on own chest"]

        grab_breast_1st = [
            "grabbing own breast",
            "grabbing own breast",
        ]
        grab_breast_2nd = [
            "grabbing another's breast",
            "guided breast grab",
        ]
        grab_breast_all = [*grab_breast_1st, *grab_breast_2nd]

        grab_hair_2nd = ["grabbing_another's_hair", "pulling_another's_hair"]

        handjob = [
            "handjob", "double handjob", "reach-around", "nursing handjob", "two-handed handjob"
        ]

        spread_pussy = ["spread pussy", "spread pussy"]
        spread_anus = ["spread anus", "spread ass"]
        spread_all = [*spread_pussy, *spread_anus]

        grab_ass_1st = ["grabbing_own_ass", "hand_on_own_ass"]
        grab_ass_2nd = ["grabbing_another's_ass", "hand on another's ass"]
        grab_ass_all = [*grab_ass_1st, *grab_ass_2nd, "crotch_grab"]

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
        top_down = [
            "top-down bottom-up",
        ]

        cat_stretch = [
            "cat stretch, stretch",
            "top-down bottom-up, cat stretch, stretch",
        ]

        cunnilingus = ["cunnilingus"]

        anilingus = ["anilingus, rimjob"]

        rub = [
            # 素股 / 臀推
            "grinding",
            "crotch rub",
        ]

        pussy_juice = [
            "pussy juice", "pussy juice trail"
        ]

        toy_dildo = [
            "dildo_under_clothes",
            "dildo_under_panties",
            "dildo_machine"
        ]

        toy_vibrator = [
            "egg_vibrator",
            "remote_control_vibrator",
            "vibrator_on_nipples",
            "vibrator_under_clothes",
            "vibrator_under_panties",
        ]

        toy_pussy = [
            "dildo",
            "sex machine",
            "sex toy pull",
            ["vibrator", "egg vibrator"],
            ["clitoris leash", "nipple leash"],
            ["crotch rope", "wooden horse"],
        ]

        toy_anal = [
            "dildo",
            ["vibrator", "egg vibrator"],
            ["anal bead", "anal bead pull"],
            ["anal tail", "fake tail"],
            "anal hook",
            "butt plug",
        ]

        top_down_all = [
            "top-down bottom-up, face_focus",
            "top-down bottom-up, face_focus, front view",
            "top-down bottom-up, from_side",
            "top-down bottom-up, from behind, ass",
        ]

        bent_over_desk = [
            "bent over desk",
            "bent over desk, (looking back:$[rand|0.5~1.0])"
        ]

        upside_down = [
            "(upside-down:$[rand|1.0~1.1]), bent over",
        ]

        butt_spank = [
            "spanked, spanking",
            "spanked, spank_mark",
            "spanked, otk spanking, spanking, red butt",
        ]


        pass

    class Leg:
        wariza = [
            "wariza, w_sitting",
            "wariza, w_sitting, feet",
        ]
        kneeling = [
            "kneeling",
            "kneeling, feet",
            "kneeling, all fours",
            "kneeling, all fours, feet",
            "on one knee",
            "on one knee, feet",
        ]
        squalting = [
            "squatting, open legs",
            "squatting, open legs, thighs, feet",
        ]
        up = [
            "leg up", "legs up",
            "leg lift", "legs lift",
        ]
        split = [
            "standing, standing split, standing on one leg"
        ]
        lock = [
            "leg lock",
            "leg lock, feet",
        ]
        sitting = [
            "sitting",
            "sitting, spread legs, m legs",
            "convenient leg",
            # 側身坐
            "yokozuwari",
            "sitting on lap",
            "sitting_backwards",
            "sitting, knees_together_feet_apart",
            # 斜倚
            "reclining",
        ]

        standing = [
            "standing",
            "pigeon-toed",
        ]

        # Leg
        pass

    class Lying:
        all = [
            "lying",
            "lying, on back",
            ["lying, on stomach", "lying, the pose"],
            "lying, on side",
        ]
        pass

    class Sex:
        missionary = [
            "missionary",
            "standing missionary",
        ]

        cowgirl = [
            "cowgirl position",
            "squatting cowgirl position",
            "reverse cowgirl position",
            "reverse squatting cowgirl position",
            "foggy, riding a dick",
            "girl on top, legs lock",
            # 素股 / 臀推
            "grinding",
        ]

        # suspended congress
        carrying_sex = [
            'lifting person, hands under legs, ass grab',
            'lifting person, hands under legs, ass grab, arms around neck, leg lock',
            'reverse suspended congress, sex from behind, spread legs, pussy',
            'wheelbarrow, sex from behind, arm support, legs lift, walking on hands',
        ]


        pass

    class Tool:
        choker = [
            "choker",
            "choker, neck bell",
        ]

        leash = [
            "leash",
            "chain leash",
            "leash in mouth",
            "viewer holding leash",
            "leash pull",
        ]

        choker_leash = Collection.list_cross(
            ["", *choker],
            ["", *leash]
        )

        whip = [
            "whipping, whip mark",
            "chain whip, whipping, whip mark",
            "vine whip, whipping, whip mark"
        ]
        pass

    class Cum:
        mouth = [
            "cum on face",
            "cum on face, cum on hair",
            "cum on face, swallowing",
            "cum in mouth",
            "cum in mouth, cum on face"
            "cum on tongue",
        ]

        pussy = [
            "cum in pussy",
            "cum in pussy, cum overflow",
        ]

        ass = [
            "cum in ass",
            "cum in ass, cum overflow"
        ]

        breast = [
            "cum on breasts",
            "cum on breasts, cum on body"
        ]

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