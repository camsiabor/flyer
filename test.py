import asyncio
import logging
import time

from PIL import Image

from scripts.common.sim import LogUtil
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

async def test_wrap():
    conf = './config/sd/preset/pony/belle.yaml'
    box = SDBox().from_yaml(conf).initiate()
    wrap = SDWrap(box=box).initiate()
    for i in range(box.image_latent.batch_count):
        await wrap.txt2img()


# ==================================================================================================

if __name__ == '__main__':
    time_start = time.perf_counter()
    LogUtil.load_yaml('./config/log.yaml')

    asyncio.run(test_wrap())

    time_end = time.perf_counter()
    logging.info(f"============= fin in {time_end - time_start:.2f} seconds =========== ")
