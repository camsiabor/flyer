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

    @staticmethod
    def select_one(
            select: dict,
            path_select: str,
            pick_prefix: str,
            pick_content: str,
            pick_suffix: str,
    ) -> str:
        prefix = select.get('prefix', None)
        content = select.get('content', {})
        suffix = select.get('suffix', None)

        prefix_sum = ""
        suffix_sum = ""
        if prefix:
            prefix_ex = Collection.roll(prefix, [], pick_prefix)
            prefix_sum = ",".join(prefix_ex) + ", "
        if suffix:
            suffix_ex = Collection.roll(suffix, [], pick_suffix)
            suffix_sum = ", " + ",".join(suffix_ex)

        if not pick_content:
            pick_content = next(iter(content))

        container = []
        content_ex = Collection.roll(content, container, pick_content)

        if isinstance(content_ex, list):
            content_sum = Collection.clamp(content_ex, prefix_sum, suffix_sum)
            return content_sum

        raise ValueError(f"Unknown content type: {content_ex}")

    @staticmethod
    def select(data: any, selector: any) -> any:
        if isinstance(selector, (list, tuple)):
            selector = selector[0]
        elements = selector.split('|')
        path_select = elements[0].strip()
        pick_prefix = elements[1] if len(elements) >= 2 else None
        pick_content = elements[2] if len(elements) >= 3 else None
        pick_suffix = elements[3] if len(elements) >= 4 else None
        select = Collection.dict_pick(data, path_select)
        ret = []
        for one in select:
            one = QCon.select_one(one, path_select, pick_prefix, pick_content, pick_suffix)
            if one is None or not one:
                continue
            if isinstance(one, str):
                ret.append(one)
                continue
            if isinstance(one, (list, tuple)):
                if len(one) == 1:
                    ret.append(one[0])
                else:
                    ret.extend(one)
                continue
            raise ValueError(f"Unknown type: {one}")

        if len(ret) == 1:
            ret = ret[0]

        return ret

    pass


# QAngle ===================================================================================== #

class QSee:
    common = [
        "from above", "from side", "from below", "front view",
    ]
    back = [
        "from behind", "from back"
    ]
    back_ass = [
        "ass, from behind", "ass, from back",
    ]
    extra = [
        "pov", "dutch angle", "foreshortening", "fisheye", "wall cross-section",
    ]
    cross_section_outer = [
        "wall cross-section"
    ]
    cross_section_inner = [
        "cross-section",
        "x-ray",
        "uterus",
        "internal cumshot",
        "multiple views",
    ]
    pass


# QPos ===================================================================================== #


class QPos:
    class Mouth:
        fellatio = [
            ["fellatio", "irrumatio"],
            "implied fellatio",
            "vacuum fellatio, blowjob face",
            "licking penis",
            "forced fellatio, irrumatio",
            "cheek bulge, irrumatio",
            "after fellatio",
            "oral_invitation",
            "kissing_penis",
            "stealth fellatio",
            "penis awe, penis shadow",
            ["penis_on_face", "penis_on_face,slapping with penis"],
            ["penis over eyes", "penis over one eye"],
            ["deepthroat", "deepthroat, (rolling eyes:$[rand|0.0~1.0])"],
            ["licking testicles", "testicle sucking", "testicle sucking,licking testicles"],
        ]

        feet = [
            "licking feet",
            "toe sucking",
        ]
        pass

    class Breast:
        titfuck = [
            "paizuri",
            "reverse paizuri",
            "paizuri on lap",
            "straddling paizuri",
            "cooperative paizuri"
            "simulated paizuri",
            [
                "paizuri invitation",
                "implied paizuri",
                "imminent paizuri",
                "after paizuri",
            ]
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

        grab_ass_1st = ["grabbing_own_ass", "hand_on_own_ass", "hand_on_own_hip"]
        grab_ass_2nd = ["grabbing_another's_ass", "hand_on_another's_ass", "hand_on_another's_hips"]
        grab_ass_all = [*grab_ass_1st, *grab_ass_2nd, "crotch_grab"]

        kabedon = [
            "kabedon",
            "kabedon on viewer",
            "foot kabedon",
        ]

        slap = [
            "slapping",
            "slap mark",
            "slap mark on face",
        ]

        pass

    class Finger:
        masturbation = [
            "masturbation", "female masturbation", "stealth masturbation",
        ]
        to_mouth_1st = [
            "finger to own mouth",
            "finger in own mouth",
            "hand to own mouth",
        ]
        to_mouth_2nd = [

            "finger to another's mouth",
            "finger in another's mouth",
            "finger in another's mouth, finger sucking",
            "finger in another's mouth, licking finger",
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

        pee = [
            "peeing, pee",
            "peeing, pee, drinking pee",
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

        dogeza = [
            "dogeza",
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

    class Feet:
        all = [
            "feet massage",
            "feet worship",
            "scorpion pose, top-down bottom-up",
        ]
        pass

    class Lying:
        all = [
            "lying",
            "lying, on back",
            ["lying, on stomach", "lying, the pose"],
            "lying, on side",
        ]
        pass

    class Leaning:
        all = [
            "leaning",
            "leaning_back",
            "leaning_on_object",
            "leaning_forward",
            "leaning_to_the_side",
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
            "cum in mouth, cum, (closed mouth:$[rand|1.1~1.3])",
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

        face = [
            "cum on face"
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
