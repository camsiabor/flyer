from scripts.sd.sc.mixup import QCon, QSee, QPos

# =====================================================================================

seeL = 0.6
seeU = 1.0

tryL = 0.3
tryU = 0.6

# =====================================================================================

pussy_cum = {
    'cum': QPos.Cum.pussy,
    'hand': [
        "",
        QPos.Hand.spread_pussy,
    ],
    'sign': [
        "",
        QPos.Hand.v_sign,
    ],
    'face': [
        "",
        "(ahegao:$[rand|0.6~1.0])",
        "(looking to the side:$[rand|1.0~1.3])",
    ]
}

pussy_penetrate = [
    "penetration, pussy",
    "penetration, pussy, pussy juice",
    "penetration, pussy, jizz oozing out of pussy",
]

holding_cellphone = [
    "(holding cellphone:$[rand|1.0~1.2]), cellphone, holding",
    "(holding cellphone:$[rand|1.0~1.2]), cellphone, holding, reflection, (female pov)",
]

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
        '0': QPos.Mouth.fellatio,
        'phone': holding_cellphone,
        'after': {
            'hand': [
                "",
                "v hand, peace sign",
            ],
            'eye': [
                "",
                "ahegao",
                "(looking to the side:1.1)"
            ],
            'cum': QPos.Cum.mouth,
        }
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
            QPos.Lying.all,
            QPos.Leg.kneeling,
            QPos.Leg.squalting,
            [
                "imminent breast grab",
                "carrying, carried breast rest, breast rest",
                "breast press",
                "breast press, against glass",
                "breasts squeezed together",
                "face between breasts",
                "licking nipple",
                "breast sucking",
                "nipple tweak",
                "tweaking own nipple",
                "breast pump",
                "breast poke",
                "breast lift",
                "breast massage",
            ]
        ],
        "breast": [
            "breast", "breasts"
        ]
    },
    'content': {
        'grab': QPos.Hand.grab_breast_all,
        'titfuck': QPos.Breast.titfuck,
        'after': QPos.Cum.breast,
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
    'content': {
        '0': QPos.Finger.to_pussy_anal,
        'mas': QPos.Finger.masturbation,
        'mouth': [QPos.Finger.to_mouth_2nd, "licking hand"],
    }
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
            [QPos.Leg.split, QPos.Leg.standing, ],
            [QPos.Leg.sitting, QPos.Leg.squalting],
            [QPos.Pelvic.top_down, QPos.Pelvic.bent_over_desk],
            [QPos.Leg.kneeling],
            [QPos.Pelvic.upside_down, QPos.Pelvic.cat_stretch],
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
        '0': [
            "pussy, pussy juice"
        ],
        'toy_pussy': {
            'insert': 'vaginal object insertion',
            'toy': QPos.Pelvic.toy_pussy,
        },
        'toy_anal': {
            'insert': 'anal object insertion, anus',
            'toy': QPos.Pelvic.toy_anal,
        },
        'lick_ass': QPos.Pelvic.anilingus,
        'lick_pussy': QPos.Pelvic.cunnilingus,
    }
}

# =====================================================================================

act_missionary = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'missionary', 'front'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra),
        ],
        'hand': [
            "",
            QPos.Hand.grab_breast_all,
            QPos.Arm.up,
        ],
        'kiss': [
            "",
            "french kiss",
            "hand on another's knee",
            [
                QCon.by(["pussy"], is_spread=True),
                QCon.by(["pussy"], is_spread=True, by_another=True),
            ]
        ],
        'pussy': pussy_penetrate,
    },
    'content': {
        '0': QPos.Sex.missionary,
        'after': pussy_cum,
    }

}

# =====================================================================================

act_cowgirl = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'cowgirl', 'reverse_cowgirl', 'top'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back_ass),
        ],
        'hand': [
            "",
            QPos.Hand.grab_breast_all,
            QPos.Hand.grab_ass_2nd,
            [
                QCon.by(["pussy"], is_spread=True),
                QCon.by(["pussy"], is_spread=True, by_another=True),
            ]
        ],
        'pussy': pussy_penetrate,
    },
    'content': {
        '0': QPos.Sex.cowgirl,
        'phone': holding_cellphone,
        'after': pussy_cum,
    }

}

# =====================================================================================

act_butt = {
    'group': 'act',
    'rating': 18,
    'tag': ['act', 'butt', 'ass', 'anus', 'pelvic'],
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
            [QPos.Pelvic.bent_over_desk, QPos.Leg.kneeling, QPos.Pelvic.cat_stretch],
            [
                QPos.Pelvic.upside_down,
                "carrying, carrying over shoulder, girl on top"
            ],
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
    'content': {
        '0': 'ass, (ass focus$[rand|0.1~0.2])',
        'vaginal': [
            'vaginal, penetration',
            'imminent penetration',
        ],
        'anal': [
            "anal penetration",
            "imminent anal",
            "double penetration",
            "imminent double penetration",
        ],
        'toy': QPos.Pelvic.toy_anal,
        'phone': holding_cellphone,
    }
}

# =====================================================================================

act_feet = {
    'group': 'act',
    'rating': 17,
    'tag': ['act', 'foot', 'feet'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back),
        ],
        'pose': [
            "",
            QPos.Lying.all,
            [QPos.Leg.wariza, QPos.Leg.sitting],
        ],
        'leg': [
            "",
            "crossed legs",
            "crossed ankles",
            "hugging own legs",
            QPos.Leg.up,
        ],
        'foot': [
            '(feet:$[rand|0.8~1.0]), (toes:$[rand|0.8~1.0]), no shoes',
            '(feet:$[rand|0.8~1.0]), (toes:$[rand|0.8~1.0]), no shoes, (foot focus:$[rand|0.0~0.2])',
        ]
    },
    'content': {
        '0': [
            ","
        ],
        'footjob': [
            'footjob',
            'reverse footjob'
        ],
        'phone': holding_cellphone,
        'after': [
            'cum, cum on feet'
        ]
    }
}

# =====================================================================================

act_pet = {
    'group': 'act',
    'rating': 17,
    'tag': ['act', 'animal', 'pet_play', 'pet'],
    'suffix': {
        'see': [
            "",
            QCon.weight(seeL, seeU, QSee.common, QSee.extra, QSee.back),
        ],
        'hand': [
            "",
            "animal pose",
            "paw pose",
            "claw pose",
            "licking hand",
        ],
        'pose': [
            "",
            QPos.Lying,
            QPos.Pelvic.cat_stretch,
            QPos.Leg.kneeling,
            QPos.Leg.wariza,
            QPos.Leg.squalting,
        ],
        'tool': [
            "",
            QPos.Tool.choker_leash,
        ],
        'ass': [
            "",
            "anal tail",
            "fake tail",
        ],
        'play': [
            '(pet play:$[rand|0.5~1.0]), (submissive female:$[rand|0.0~0.5])'
        ]
    },
    'content': {
        '0': [
            ","
        ],
        'fellatio': QPos.Mouth.fellatio,
        'spank': QPos.Pelvic.butt_spank,
        'whip': QPos.Tool.whip,
        'bondage': ["bondage"],
    }
}

# =====================================================================================

act_standing_sex = {
    'group': 'act',
    'rating': 17,
    'tag': ['act', 'standing_sex'],
    'suffix': {
        'stand': ['standing sex, penetration'],
        'pose': [
            'split, leg up',
            'split, leg up, standing on one leg',
            ['', 'double penetration', 'orgy'],
            QPos.Sex.carrying_sex,
            [
                'against wall, sex from behind',
                'arm grab, arm held back, sex from behind, doggystyle'
            ],
        ],
        'hand': [
            '',
            QPos.Hand.grab_breast_all,
            QPos.Arm.up,
        ]
    },
    'content': {
        '0': [
            ",",
        ]
    }
}

# =====================================================================================





# =====================================================================================

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

act = {
    'bj': act_fellatio,
    'fellatio': act_fellatio,
    'breast': act_breast,
    'finger': act_fingering,
    'fingering': act_fingering,
    'pelvic': act_pelvic,
    'ass': act_butt,
    'butt': act_butt,
    'feet': act_feet,
    'cowgirl': act_cowgirl,
    'missionary': act_missionary,
    'standing_sex': act_standing_sex,
    'pet': act_pet,
}

ex = {

}

everything = {
    'act': act,
    'ex': ex,
}


def init(_: any, args: any):
    ret = QCon.select(everything, args)
    return ret
