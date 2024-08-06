from config.common import QCon, QSee, QPos
from scripts.common.collection import Collection

seeL = 0.6
seeU = 1.0

tryL = 0.3
tryU = 0.6

suf = {
    '+*'
}

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
        "leg": ["", QPos.Leg.kneeling, QPos.Leg.squalting, QPos.Lying],
        "hand_2nd": ["", "", QPos.Hand.head_2nd, QPos.Hand.hair_2nd],
        "hand_1st": [
            "",
            QPos.Hand.breast_all,
            QPos.Finger.masturbation,
            QCon.weight(tryL, tryU, QPos.Arm.behind)
        ],
        "main": "(fellatio:$[rand|0.0~0.5])",
    },
    'content': QPos.Mouth.fellatio,
}

# breast =====================================================================================

act_breast = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'breast', 'breasts', 'titfuck', 'paizuri'],
    'suffix': [
        [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, ),
        ],
        ["", QPos.Leg.kneeling, QPos.Leg.squalting, QPos.Lying],
    ],
    'content': [
        QPos.Hand.breast_all,
        QPos.Breast.titfuck,
    ]
}

# =====================================================================================

act_fingering = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'fingering', 'finger', ],
    'suffix': [
        [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back_ass),
        ],
        ["", QPos.Leg.squalting, QPos.Lying],
    ],
    'content': [
        QPos.Finger.to_pussy_anal,
        [QPos.Finger.masturbation, QPos.Finger.to_mouth_2nd],
    ]
}

# =====================================================================================

act_pussy = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'pussy'],
    'suffix': [
        [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back_ass),
        ],
        [
            "",
            QPos.Lying,
            [
                QPos.Leg.top_down, QPos.Leg.kneeling,
                QPos.Leg.squalting, QPos.Leg.split
            ],
        ],
    ],
    'content': [
        QPos.Hand.spread_all,
        QCon.by(data=["skirt", "dress"], is_lift=True, by_self=True),
        QCon.by(data=["panties", "thong"], is_pull=True),
    ]
}

pos_pussy = [
    1,
    "lying, arm up, spread legs, pussy, pussy juice, armpits",
    1,
    "spread legs, from below, anus, pussy, pussy juice",
    1,
    "spread pussy, spread legs, looking to the side, v hand, pussy juice",
    1,
    "female masturbation, grabbing own breast, bathing, topless",
    1,
    "female masturbation, spread legs, female masturation, spread pussy by self",
    1,
    "skirt lift, lifted by self, bottomless, no panties, from below, pussy juice",
    1,
    "squatting, spread legs, pussy, pussy juice",
    1,
    "(vaginal object insertion), pussy, pussy juice, dildo",
    1,
    "(crotch rub:1.05), nipples, breasts, pussy, "
    "female masturbation, pussy juice, masturbation, cleft of venus",
    1,
    "pussy, pussy juice, split, leg up, "
    "standing, standing split, standing on one leg, ",
    1,
    "pussy, pussy juice, split, leg up, "
    "standing, standing split, standing on one leg, "
    "(vaginal object insertion), dildo",

]

pos_ass = [
    1,
    "top-down bottom-up, face_focus, bottomless, all fours",
    1,
    "top-down bottom-up, face_focus, bottomless, front view",
    1,
    "top-down bottom-up, bottomless, from_side",
    1,
    "top-down bottom-up, from behind, ass, bottomless, pussy, pussy juice, navel, ponytail",
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
    'finger': act_fingering,
    'pussy': act_pussy,
}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    act = acts[cmd]
    suffix = act.get('suffix', '')
    content = act.get('content', '')
    suffix_ex = Collection.roll(suffix, [])
    content_ex = Collection.roll(content, [])
    ret = ",".join(suffix_ex) + "," + content_ex
    return ret
