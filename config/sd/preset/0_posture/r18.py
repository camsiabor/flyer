from config.common import PresetCommon

pos_front = [
    "missionary position, penetration, pov, grabbing another's breast",
    "missionary position, penetration, pov, from above",
    "missionary position, penetration, french kiss, faceless male",
    "standing missionary, penetration",
]

pos_breast = [
    "breast sex, titfucking, pov, breasts, nipple, penis",
]

pos_back = [
    1,
    "top-down bottom-up, face_focus, bottomless",
    1,
    "top-down bottom-up, face_focus, bottomless, front view",
    1,
    "top-down bottom-up, bottomless, from_side",
    1,
    "bent over desk, pov, skirt pulled down, panty pulled down, "
    "looking back, hands on ass, pussy, pussy juice, pov",
    1,
    "bent over desk, pov, skirt pulled down, panty pulled down, "
    "looking back, hands on ass, doggystyle sex, "
    "pussy juice, penetration, pov",
    1,
    "lying on stomach, sex from behind, hand on head",
    1,
    "sex_from_behind, against wall, hands on wall, from back, from above",
    1,
    "sex from behind, from below",
    1,
    "doggy style, kneeling",
]

pos_expose = [
    "squatting, no panties, spread knees, clothes lift, lifted by self, from below",
    "squatting",
    "skirt lift, lifted by self, bottomless, no panties, from below",
    "spreading own ass, from behind, pov",
    "spread pussy, spread legs, looking to the side, v hand, pussy juice",
    "wariza, w_sitting, ass, ass_focus, feet",
    "wariza, w_sttiing, pov, from_above",
]

pos_after = [

]

poses = {
    # front
    "front": pos_front,
    "missionary": pos_front,
    # back
    "back": pos_back,
    "doggy": pos_back,
    # expose
    "expose": pos_expose,
    # breast
    "breast": pos_breast,
    "chest": pos_breast,
}


def init(_: any, __: any):
    data = [
        "squatting, no panties, spread knees, clothes lift, lifted by self, from below",
        "squatting",
        "skirt lift, lifted by self, bottomless, no panties, from below",
        "spreading own ass, from behind, pov",
        "spread pussy, spread legs, looking to the side, v hand, pussy juice",
        "wariza, w_sitting, ass, ass_focus, feet",
        "wariza, w_sttiing, pov, from_above",
    ]

    PresetCommon.dict_pick(poses, )

    return PresetCommon.to_array(data)
