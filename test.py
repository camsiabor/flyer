import asyncio
import os

import webuiapi

from scripts.sd.sc import alias


async def test_webuiapi():
    os.makedirs('output', mode=0o777, exist_ok=True)

    host = '127.0.0.1'
    port = 30001
    sampler = 'Euler a'
    steps = 26

    client = webuiapi.WebUIApi(
        host=host, port=port,
        sampler=sampler, steps=steps,
    )

    model_target = 'waiANINSFWPONYXL'
    model_current = client.util_get_current_model()
    print("current model: ", model_current)

    """
    if model_current not in model_target:
        client.util_set_model(model_target)
        print(f'switch model to ${model_target} from ${model_current}')
    """

    result = await client.txt2img(

        # prompt
        prompt="1girl, solo",
        negative_prompt='low quality, worst quality',
        # sampler
        sampler_name='Euler a',
        steps=20,
        cfg_scale=7,
        seed=1003,
        # latent image
        width=1024,
        height=1024,

        # async
        use_async=True,

        hr_scale=1.25,
        hr_upscaler=alias.HiResUpscalerEx.ESRGAN_4x_Anime6B.value,
        # hr_upscaler= alias.HiResUpscalerEx.ESRGAN_4x_Anime6B,

    )

    # webuiapi.HiResUpscaler

    print(result.info)

    result.image.save('output/test.png')

    print('done')


def test():
    v = alias.HiResUpscalerEx.Latent.value
    print(v)


if __name__ == '__main__':
    # test()
    asyncio.run(test_webuiapi())
