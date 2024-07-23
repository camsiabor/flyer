import asyncio
import logging
import time

from PIL import Image

from scripts.common.cfg import ConfigUtil
from scripts.common.log import LogUtil
from scripts.sd.sc.box import SDBox
from scripts.sd.sc.sdwrap import SDWrap


# ==================================================================================================


# ==================================================================================================

def test():
    png_file_path = './output/20240707/test_172049.png'
    with Image.open(png_file_path) as img:
        metadata = img.info  # This contains a dictionary of metadata, including text chunks
        print(metadata)


# ==================================================================================================

async def test_wrap(preset):
    box = SDBox().load(preset).initiate()
    wrap = SDWrap(box=box).initiate()
    for i in range(box.image_latent.batch_count):
        await wrap.txt2img()


async def dev():
    c, p = ConfigUtil.load('./config/sd/preset/dev.yaml')
    print(c, p)
    pass


# ==================================================================================================

if __name__ == '__main__':
    time_start = time.perf_counter()
    LogUtil.load('./config/log.yaml')

    # preset = './config/sd/preset/zzz/feet.yaml'
    preset = './config/sd/preset/v/vr/shiori/white.yaml'
    asyncio.run(test_wrap(preset))

    # asyncio.run(dev())

    time_end = time.perf_counter()
    logging.info(f"============= fin in {time_end - time_start:.2f} seconds =========== ")
