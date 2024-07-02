import os

import webuiapi


async def test_webuiapi():
    os.makedirs('output', mode=0o777, exist_ok=True)

    client = webuiapi.WebUIApi(
        host='127.0.0.1',
        port=30001,
        sampler='Euler a',
        steps=20,
    )

    model_target = ''
    model_current = client.util_get_current_model()
    if model_current != '':
        client.util_set_model('')

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
    )

    print(result.info)

    result.image.save('output/test.png')

    print('done')




if __name__ == '__main__':
    test_webuiapi()
