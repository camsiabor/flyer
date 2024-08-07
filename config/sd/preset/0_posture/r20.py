from scripts.common.collection import Collection
from scripts.sd.sc.mixup import QCon, QSee, QPos

# =====================================================================================

seeL = 0.6
seeU = 1.0

tryL = 0.3
tryU = 0.6

# =====================================================================================

act_fellatio = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'fellatio', 'blowjob', 'bj'],
    'suffix': {
        "see": [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back),
        ],
        "leg": ["", QPos.Leg.kneeling, QPos.Leg.squalting, QPos.Lying.all],
        "hand_2nd": ["", "", QPos.Hand.on_head_2nd, QPos.Hand.grab_hair_2nd],
        "hand_1st": [
            "",
            QPos.Hand.grab_breast_all,
            QPos.Finger.masturbation,
            QCon.weight(tryL, tryU, QPos.Arm.behind)
        ],
        "main": "(fellatio:$[rand|0.0~0.5])",
    },
    'content': {
        'fellatio': QPos.Mouth.fellatio,
    }
}

# breast =====================================================================================

act_breast = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'breast', 'breasts', 'titfuck', 'paizuri'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra),
        ],
        "pose": [
            "",
            QPos.Leg.kneeling, QPos.Leg.squalting, QPos.Lying
        ],
    },
    'content': {
        'grab': QPos.Hand.grab_breast_all,
        'titfuck': QPos.Breast.titfuck,
    }
}

# =====================================================================================

act_fingering = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'fingering', 'finger', ],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back_ass),
        ],
        'pose': [
            "", QPos.Leg.squalting, QPos.Lying
        ]
    },
    'content': [
        QPos.Finger.to_pussy_anal,
        [QPos.Finger.masturbation, QPos.Finger.to_mouth_2nd],
    ]
}

# =====================================================================================

act_pelvic = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'pussy', 'pelvic'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back_ass),
        ],
        'pose': [
            "",
            QPos.Lying.all,
            [QPos.Leg.split, QPos.Leg.standing, QPos.Leg.sitting],
            [QPos.Pelvic.top_down, QPos.Leg.kneeling, QPos.Leg.squalting],
        ],
        'hand': [
            "",
            QPos.Finger.masturbation,
            QPos.Hand.grab_breast_all,
            QCon.by(["pussy"], is_spread=True),
            QCon.by(["pussy"], is_spread=True, by_another=True),
        ],
        'cloth': [
            "",
            QCon.by(data=["skirt", "dress"], is_lift=True, by_self=True),
            QCon.by(data=["panties", "thong"], is_pull=True),
        ]
    },
    'content': {
        'pussy': [
            "pussy, pussy juice"
        ],
        'toy_pussy': [
            "dildo",
            "vibrator"
        ],
        'toy_anal': [
            "dildo",
            "vibrator"
        ]
    }
}

# =====================================================================================

act_ass = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'ass', 'anus', 'pelvic'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back, QSee.back_ass),
        ],
        'pose': [
            "",
            QPos.Lying.all,
            QPos.Pelvic.top_down_all,
            [QPos.Leg.squalting, QPos.Leg.wariza],
            [QPos.Pelvic.bent_over_desk, QPos.Leg.kneeling],
        ],
        'hand': [
            "",
            QPos.Hand.spread_anus,
            QPos.Hand.grab_ass_all,
            QPos.Pelvic.butt_spank,
        ],
        'cloth': [
            "",
            QCon.by(data=["panties", "thong"], is_pull=True),
        ]
    },
    'content': [
        'ass, (ass focus$[rand|0.1~0.2])'
    ]
}

act_toy = {
    'content': [

    ]
}

pos_ass = [
    1,
    "bent over desk, pov, skirt pulled down, panty pulled down, "
    "looking back, hands on ass, spread pussy, pussy, pussy juice, pov",
    1,
    "spreading own ass, from behind, pov",
    1,
    "from below, looking back, ass grab, ass focus, grabbing own ass, hand on own ass",
    1,
    "from below, spread anus, from behind, ass focus, anus peek, facing away, spread ass, grabbing own ass, ass grab",
    1,
    "(upside-down:1.05), bent over, ass, pussy, pussy juice, anus",
    1,
    "(anal object insertion), pussy, pussy juice, anus, dildo",
    1,
    "double penetration, anal, pussy, penetration",
    1,
    "imminent double penetration, anus, pussy, pussy juice",
    1,
    "enema,anal object insertion, sex toy, dildo",
    1,
    "from behind, sex toy, vaginal, dildo riding, squatting, feet",
    1,
    "butt plug, pussy, pussy juice",
    1,
    "anal tail, anal object insertion, anal, pussy, pussy juice ",
    1,
    "otk spanking, spanking, spanked, red butt, (pants pull:0.9), (panty pull:0.9), motion lines",
    1,
    "lying, on back, underwear, (panties), (panty pull),"
    "pussy, pussy juice, legs up, thighs"
]

pos_feet = [
    1,
    "cross leg, from side, feet, no shoes",
    1,
    "from below, feet, (foot focus:$[rand|0.65~1.0]), no shoes",
    1,
    "from back, back, wariza, w_sitting, feet, toes, (foot focus:$[rand|0.65~1.0])",
    1,
    "(holding cellphone:1.05), cellphone, holding, reflection, (female pov), "
    "legs up, (foot focus:$[rand|0.65~1.0]), feet, no shoes, "
    "pussy, breasts, navel, nipples, "
    "cellphone, toes, sitting",
    1,
    "(holding cellphone:1.05), cellphone, holding, reflection, (selfie), "
    "pussy, feet, toes, ass, anus, sitting, "
    "breasts, thighs, legs, soles ",
    1,
    "lying, on back, (feet), toes, no shoes, spread legs, ass",
    1,
    "footjob, feet, (toes:0.9), (cum on feet:$[rand|0.0~1.0])",
    1,
    "reverse footjob, feet, (toes:0.9), thighs, (cum on feet:$[rand|0.0~1.0])"
]

pos_expose = [
    1,
    "wariza, w_sitting, ass, ass_focus, feet",
    1,
    "wariza, w_sttiing, pov, from_above, paw pose",
    1,
    "(squatting), (paw pose), topless, bottomless",
    1,
    "(squatting), (paw pose), topless, bottomless, from above",
    1,
    "(squatting), no panties, spread knees, clothes lift, lifted by self, from below",
    1,
    "covering, breasts, navel, covering breasts, "
    "stomach, standing, groin, thigh gap, thighs ",
    1,
    "(squatting), armpits, arms up, arms behind head, "
    "breasts, thighs, spread legs, feet ",
]

pos_bdsm = [
    1,
    "(bdsm:$[rand|0.1~1.0]), (handcuffs), (chains), rope, submissive female",
    1,
    "(bdsm:$[rand|0.1~1.0]), (handcuffs), arms behind back, prone bone, arched back, submissive female",
    1,
    "(bdsm:$[rand|0.1~1.0]), (leash), (viewer holding leash)"
    "squatting, pussy, breasts, cum, long hair, submissive female,"
    "paw pose, spread legs, cum on body, pet play, cumdrip, cum on breasts, ",
    1,
    "(bdsm:$[rand|0.1~1.0]), (leash), (viewer holding leash), "
    "lying, pet play, submissive female",
    1,
    "(bdsm:$[rand|0.1~1.0]), "
    "otk spanking, spanking, spanked, red butt, "
    "(pants pull:0.9), (panty pull:0.9), motion lines",
    1,
    "(bdsm:$[rand|0.1~1.0]), human chair, female on all fours, submissive female",
    1,
    "(bdsm:$[rand|0.1~1.0]), whipping, submissive, whip marks, holding whip, submissive female",
    1,
    "(bdsm:$[rand|0.1~1.0]), wooden horse, pussy, pussy juice, sweat",
    1,
    "(bdsm:$[rand|0.1~1.0]), (bondage outfit:$[rand|0.8~1.05]), restrained",
    1,
    "(bdsm:$[rand|0.1~1.0]), cage, restrained",
]

pos_front = [
    "missionary, penetration, pov, grabbing another's breast",
    "missionary, penetration, pov, from above",
    "missionary, penetration, french kiss, faceless male",
    "missionary, (female pov), penetration",
    "standing missionary, penetration",
    "lying, arm up, spread legs, armpits, missionary, ejaculation, orgasm",
]

pos_standing = [
    1,
    "leaning forward, cleavage, hand on own hip",
    2,
    "standing sex, penetration",
    2,
    "standing sex, split, leg up, penetration",
    1,
    "standing double penetration, anal, pussy, penetration",
]

pos_top = [
    "cowgirl position, penetration, bottomless, pussy juice",
    "cowgirl position, penetration, grabbing own breast, bottomless, pussy juice",
    "reverse cowgirl position, penetration, slutty, bottomless, pussy juice",
    "reverse cowgirl position, penetration, grabbing ass, bottomless, pussy juice",
    "foggy, exposed pussy, vaginal, riding a dick, jizz oozing out of pussy, cum, orgasm, penetration",
    "girl on top, legs lock, penetration",
]

pos_lying = [
    2,
    "lying, on back, pov, arms up,arms bound, rope, head tilt, knees up, cunninggulus, waist grab",
    2,
    "lying, on back, from side, arms up,arms bound, rope, head tilt, knees up, cunninggulus, waist grab",
    2,
    "lying, on side, penetration, vaginal, pussy, pussy juice",
    1,
    "lying, on side, douable penetration, pussy, puusy juice",
    1,
    "lying, on side, closed eyes, sleeping, (cum on body:$[rand|0~1.0])",
    1,
    "lying, on side, closed eyes, sleeping, fetal position"
]

pos_doggy = [
    1,
    "bent over desk, pov, skirt pulled down, panty pulled down, "
    "looking back, hands on ass, doggystyle sex, "
    "pussy juice, penetration, pov",
    1,
    "top-down_bottom-up, "
    "pussy, pussy juice, ass, sex from behind, from back, back",
    1,
    "top-down bottom-up, face_focus, bottomless, all fours, sex from behind, penetration",
    1,
    "top-down bottom-up, face_focus, bottomless, front view, sex from behind, hand on head, penetration",
    1,
    "top-down bottom-up, from_side, penetration, hand on head",
    1,
    "lying on stomach, sex from behind, hand on head",
    1,
    "sex_from_behind, against wall, hands on wall, from back, from above",
    1,
    "sex from behind, from below",
    1,
    "doggy style, penetration, kneeling",
    1,
    "prone bone, penetration",
    1,
    "pressed against glass, bathroom, showering, mixed bathing, "
    "(breast press), breasts, nipples, stomach, "
    "sex from behind, standing sex, wet, pussy, vaginal, pussy juice, thighs, "
]

pos_back = [
    1,
    "from back, wariza, w_sitting, back, thighs, legs, feet",
    1,
    "(showering), wet, from behind, back, thighs, ass, breasts"
]

pos_sex_after = [
    1,
    "after sex, spread legs, peace sign, v hand, cum in pussy, cum on body, looking to the side",
    1,
    "after sex, spread legs, peace sign, v hand, spread pussy by own hand, "
    "cum in pussy, cum on body, open mouth, tongue out",
    1,
    "after sex, from back, ass, pussy, cum in pussy, cum on body, grab ass by own hands",
    1,
    "after sex, squatting, paw pose, cum in pussy, cum on body, open mouth, tongue out, pussy",
    1,
    "after sex, from behind, top-down_bottom-up, cum in pussy, cum on body, pussy, ass",
    1,
    "after sex, pov, (leash), (viewer holding leash), "
    "squatting, pussy, breasts, cum, long hair, looking at viewer, "
    "paw pose, spread legs, cum on body, pet play, cumdrip, cum on breasts, ",
    1,
    "after sex, multiple condoms, used condom, condom belt, condom, "
    "indecency, cum on body, cum on breasts, "
    "legs up, spread legs, "
]

pos_mouth_after = [
    1,
    "from above, pov, cum in mouth, cum on face, open mouth, tongue out, v hand, peace sign",
    1,
    "ahegao, peace sign, v hands, v, cum in mouth, cum on face",
]

acts = {

    'fellatio': act_fellatio,

    'breast': act_breast,
    'fingering': act_fingering,
    'pelvic': act_pelvic,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]

    elements = cmd.split('|')
    name_act = elements[0]
    pick_prefix = elements[1] if len(elements) >= 2 else None
    pick_content = elements[2] if len(elements) >= 3 else None
    pick_suffix = elements[3] if len(elements) >= 4 else None

    act = acts[name_act]

    prefix = act.get('prefix', '')
    content = act.get('content', '')
    suffix = act.get('suffix', '')

    if not pick_content:
        pick_content = next(iter(content))

    prefix_sum = ""
    suffix_sum = ""
    if prefix:
        prefix_ex = Collection.roll(prefix, [], pick_prefix)
        prefix_sum = ",".join(prefix_ex) + ","
    if suffix:
        suffix_ex = Collection.roll(suffix, [], pick_suffix)
        suffix_sum = "," + ",".join(suffix_ex)

    content_ex = Collection.roll(content, [], pick_content)

    if isinstance(content_ex, str):
        return f"{prefix_sum}{content_ex}{suffix_sum}"

    if isinstance(content_ex, list):
        content_sum = Collection.clamp(content_ex, prefix_sum, suffix_sum)
        return content_sum

    raise ValueError(f"Unknown content type: {content_ex}")
