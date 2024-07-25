from config.common import PresetCommon

pos_mouth = [
    "licking penis, fellatio, hand on head",
    "licking penis, fellatio, hand on head, pov, from above",
    "licking penis, nipples, from side, kneeling, hand on head,",
    "licking penis, deep throat",
    "licking penis, handjob, orgy",
    "licking penis, pov",
    "licking penis, pov, from above",
    "licking penis, bottomless, masturbation, squatting",
    "licking penis, bottomless, spread pussy by own hand",
    "licking penis, topless, grabbing own breast",
]

pos_breast = [
    3,
    "breast sex, titfucking, pov, breasts, nipple, penis",
]

pos_hand = [
    "female masturbation, grabbing own breast, bathing, topless",
    "female masturbation, spread legs, female masturation, spread pussy by self",
    "fingering, pussy, pussy juice",
    "fingering, pussy, pussy juice, ass, anal",
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

pos_front = [
    "missionary position, penetration, pov, grabbing another's breast",
    "missionary position, penetration, pov, from above",
    "missionary position, penetration, french kiss, faceless male",
    "standing missionary, penetration",
]

pos_standing = [
    3,
    "standing sex",
    3,
    "standing sex, split, leg up",
]

pos_top = [
    "cowgirl position, penetration, bottomless, pussy juice",
    "cowgirl position, penetration, grabbing own breast, bottomless, pussy juice",
    "reverse cowgirl position, penetration, slutty, bottomless, pussy juice",
    "reverse cowgirl position, penetration, grabbing ass, bottomless, pussy juice",
    "foggy, exposed_pussy,vaginal, riding a dick, jizz oozing out of pussy, cum, orgasm,",
    "girl on top, legs lock",
]

pos_lying = [
    2,
    "lying on back, pov, arms up,arms bound, rope, head tilt, knees up, cunninggulus, waist grab",
    2,
    "lying on back, from side, arms up,arms bound, rope, head tilt, knees up, cunninggulus, waist grab",
    2,
    "lying on side, penetration, vaginal",
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

pos_after = [
    1,
    "spread legs, peace sign, v hand, cum in pussy, cum on body, looking to the side",
    1,
    "spread legs, peace sign, v hand, spread pussy by own hand, "
    "cum in pussy, cum on body, open mouth, tongue out",
    1,
    "from back, ass, pussy, cum in pussy, cum on body, grab ass by own hands",
    1,
    "squat, paw pose, cum in pussy, cum on body, open mouth, tongue out, pussy",
    1,
    "from behind, top-down_bottom-up, cum in pussy, cum on body, pussy, ass",
    1,
    "from above, pov, cum in mouth, open mouth, tongue out, v hand, peace sign",
    1,
    "ahegao, peace sign, v hands, v",
]

poses = {

    # mouth
    "mouth": pos_mouth,
    "bj": pos_mouth,
    "blowjob": pos_mouth,

    # breast
    "breast": pos_breast,
    "chest": pos_breast,

    # hand
    "hand": pos_hand,
    "hj": pos_hand,

    # expose
    "expose": pos_expose,

    # front
    "front": pos_front,
    "missionary": pos_front,

    # standing
    "standing": pos_standing,
    "stand": pos_standing,

    # top
    "top": pos_top,
    "cowgirl": pos_top,

    # lying
    "lying": pos_lying,

    # back
    "back": pos_back,
    "doggy": pos_back,

}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = PresetCommon.dict_pick(poses, cmd, True)

    return PresetCommon.to_array(poses)
