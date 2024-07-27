from scripts.common.collection import Collection

# mouth =====================================================================================

pos_mouth = [

]

# breast =====================================================================================

pos_breast = [
    "grabbing own breast",
]

pos_hand = [
    "implied fingering",
    "finger in another's mouth, open mouth",
]

pos_pussy = [
    1,
    "lying, arm up, spread legs, armpits",
    1,
    "spread legs, from below,  ",
    1,
    "spread  spread legs, looking to the side, v hand, ",
    "skirt lift, lifted by self, panties",
    1,
    "squatting, spread legs,  ",
    1,
    "(vaginal object insertion),  ",
    1,
    "(crotch rub:1.05), nipples, breasts,  "
    "female masturbation, masturbation, cleft of venus",
    1,
    " split, leg up, "
    "standing, standing split, standing on one leg, ",
    1,
    " split, leg up, "
    "standing, standing split, standing on one leg, "
    "(vaginal object insertion)",

]

pos_ass = [
    1,
    "top-down bottom-up, face_focus, bottomless, all fours",
    1,
    "top-down bottom-up, face_focus, bottomless, front view",
    1,
    "top-down bottom-up, from_side",
    1,
    "top-down bottom-up, from behind, ass, bottomless,  navel",
    1,
    "bent over desk, pov",
    1,
    "looking back, hands on ass, pov",
    1,
    "from below, looking back, ass grab, grabbing own ass, hand on own ass",
    1,
    "from below, spread  from behind, ass focus,  peek, facing away, spread ass, grabbing own ass, ass grab",
    1,
    "(upside-down:1.05), bent over, ass, ",
]

pos_feet = [
    1,
    "from side, "
    "cross leg, feet, no shoes",
    1,
    "from below, "
    "cross leg, feet, no shoes",
    1,
    "from below, feet, foot focus, no shoes",
    1,
    "sitting, "
    "(holding cellphone:1.05), (reflection:1.05), (female pov:1.05), "
    "legs up, foot focus, feet, toes, no shoes, ",
    1,
    "lying, "
    "(holding cellphone:1.05), (reflection:1.05), (female pov:1.05), "
    "legs up, foot focus, feet, toes, no shoes, ",
    1,
    "sitting, "
    "(holding cellphone:1.05), (reflection:1.05), (selfie:1.05), "
    "thighs, legs, feet, toes, foot focus ",
    1,
    "lying, on back, (feet), toes, no shoes, spread legs, ass"
]

pos_expose = [
    "wariza, w_sitting, ass, ass_focus, feet",
    "wariza, w_sttiing, pov, from_above, paw pose",
    "(squatting), (paw pose), topless, bottomless",
    "(squatting), (paw pose), topless, bottomless, from above",
    "(squatting), no panties, spread knees, clothes lift, lifted by self, from below",
]

pos_front = [
    "leaning forward, hand on own hip, pov, close-up",
]

pos_standing = [
    2,
    "standing sex",
    2,
    "standing sex, split, leg up",
    1,
    "standing double  anal,  ",
]

pos_top = [
    "cowgirl position,  bottomless, ",
    "cowgirl position,  grabbing own breast, bottomless, ",
    "reverse cowgirl position,  slutty, bottomless, ",
    "reverse cowgirl position,  grabbing ass, bottomless, ",
    "foggy, exposed_vaginal, riding a dick, jizz oozing out of  cum, orgasm,",
    "girl on top, legs lock",
]

pos_lying = [
    1,
    "lying, on back, pov, arms up,arms bound, rope, head tilt, knees up",
    1,
    "lying, on back, from side, arms up,arms bound, rope, head tilt, knees up, cunninggulus, waist grab",
    1,
    "lying, on side",
    1,
    "lying, on stomach, pov, close-up",
    1,
    "lying, on stomach, pov, close-up"
]

pos_back = [
    1,
    "bent over desk, pov, skirt pulled down, panty pulled down, "
    "looking back, hands on ass, doggystyle sex, "
    " pov",

    1,
    "top-down bottom-up, from behind, ass, bottomless,  navel",
    1,
    "lying on stomach, sex from behind, hand on head",
    1,
    "sex_from_behind, against wall, hands on wall, from back, from above",
    1,
    "sex from behind, from below",
    1,
    "doggy style,  kneeling",
]

pos_after = [
    1,
    "after sex, spread legs, peace sign, v hand, cum in  cum on body, looking to the side",
    1,
    "after sex, spread legs, peace sign, v hand, spread pussy by own hand, "
    "cum in  cum on body, open mouth, tongue out",
    1,
    "after sex, from back, ass,  cum in  cum on body, grab ass by own hands",
    1,
    "after sex, squatting, paw pose, cum in  cum on body, open mouth, tongue out, pussy",
    1,
    "after sex, from behind, top-down_bottom-up, cum in  cum on body,  ass",
    1,
    "after sex, from above, pov, cum in mouth, open mouth, tongue out, v hand, peace sign",
    1,
    "after sex, ahegao, peace sign, v hands, v",
    1,
    "after sex, pov, (leash), (viewer holding leash), "
    "squatting,  breasts, cum, long hair, looking at viewer, "
    "paw pose, spread legs, cum on body, pet play, cumdrip, cum on breasts, "
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

    # pussy
    "pussy": pos_pussy,

    # ass
    "ass": pos_ass,

    # feet
    "feet": pos_feet,
    "foot": pos_feet,
    "footjob": pos_feet,
    "fj": pos_feet,

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

    # after
    "after": pos_after,
    "sex_after": pos_after,

}


def init(_: any, args: any):
    cmd = args
    if isinstance(cmd, (list, tuple)):
        cmd = cmd[0]
    picks = Collection.dict_pick(poses, cmd, True)
    picks_weight = Collection.list_unpack(picks)

    return picks_weight
