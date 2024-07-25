server = {
    'host': '127.0.0.1',
    'port': 30002,
    'progress_poll_delay': 1024,
    'progress_poll_interval': 1024,
    'verbose': True
}

image_latent = {
    'width': 1024,
    'height': 1024,
    'batch_size': 1,
    'batch_count': 10
}

prompt_positive = f"""
(score_9, score_8_up, score_7_up, source_anime, rating_all),
$$expressive_h$$,
$$common$$,
$$people$$,
$$posture_ref$$,
$$posture$$,
$$body$$,
$$body_sub$$,
$$character_lora$$,
$$perspective$$,
$$character$$,
$$facial_expression$$,
$$facial_expression_sub$$,
$$scene$$,
"""

prompt_negative = f"""
score_6, score_5, score_4, score_3, score_2, score_1, pony, 
worst quality, low quality, lowres, shoes, 
bad hands, extra fingers, distorted hands, distorted fingers, missing fingers, 
bad feet, distorted feet, distorted toes, missing toes, fewer digits, extra digits, 
bad anatomy, 
text, signature, watermark, logo,
(looking at viewer:1.5)
"""

posture_ref = f"""
<OvO des="list">
    <d a="1" src="file" base="config/sd/preset/0_posture/nsfw/">
        <i a="0" func="init">after.py</i>
        <i a="1" func="back">back.py</i>
        <i a="1">r18.py</i>
        <i a="1">expose.py</i>
        <i a="1">front.py</i>
        <i a="1">hand.py</i>
        <i a="1">lying.py</i>
        <i a="1">mouth.py</i>
        <i a="1">stand.py</i>
        <i a="1">top.py</i>
    </d>
</OvO>
"""

params_pos_1 = {
    'common': '',
    'expressive_h': '<lora:Expressive_H:1>,expressiveh',
    'character_lora': f"""
    <OvO des="list">
        <d src="file" base="./config/sd/preset/0_character/">
            <i a="1" arg="firefly.lora+cloth">hoyoverse/starrail.py</i>
        </d>
    </OvO>""",
    'character': '',
    'people': ['1girl, orgy, multiple boys'],
    'posture_ref': posture_ref,
    'posture': [],
    'body': [
        'half nude',
        'half nude, torn clothes',
        '(nude:0.7)',
        '(nude:0.9)',
        '(nude:1.1)',
        'lingerie, (nude:0.6)',
        'lingerie, (nude:0.8)',
        'bondage, (nude:0.7)',
        'bondage, (nude:0.9)',
        'bondage, (nude:1.1)'
    ],
    'body_sub': [],
    '_perspective': [
        'from back',
        'from side',
        '(from side:1.5)',
        'from above',
        'from below',
        'pov, close-up',
        'distant'
    ],
    'facial_expression': [
        'embarrassed',
        'embarrassed, (looking to the side:1.05)',
        'open mouth',
        'open mouth, tongue out',
        'black blindfold, open mouth'
    ],
    'facial_expression_sub': ['blush, (saliva trail:0.75)'],
    'scene': ['outdoors, night, (night sky:0.5), (fireflies:0.5), (light particles:0.1), aesthetic']
}

prompt = {
    "positive": prompt_positive,
    "negative": prompt_negative,
    "params_cycle": -1,
    "params_pos_1": params_pos_1,
}

ret = {
    'server': server,
    'image_latent': image_latent,
    'prompt': prompt,
    'sampler': {
        'name': 'Euler a',
        'steps': 26,
        'cfg_scale': 5,
        'seed': -1
    },
    'upscaler': {
        'enable': False,
        'scale': 1.25,
        'second_pass_steps': 10,
        'denoising_strength': 0.5,
        'name': 'ESRGAN_4x_Anime6B'
    },
    'adetailers': [
        {
            'enable': True,
            'model': 'face_yolov8n.pt',
            'denoising_strength': 0.33
        },
        {
            'enable': False,
            'model': 'hand_yolov8n.pt'
        }
    ],
    'options': {
        'colddown': 2,
        'use_async': True,
        'metadata_key': 'b_pox_b'
    },
    'extra': {
        'enable': False,
        'upscaler_1': 'ESRGAN_4x_Anime6B',
        'upscaling_resize': 1.25
    },
    'output_txt2img': {
        'file_format': 'D:/snapshot/character/hoyoverse/starrail/firefly/%Y%m%d/1/%H%M%S',
        'file_extension': 'png'
    }
}


def init(_: any, args: str):
    return ret
