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

async def test_wrap():
    conf = './config/sd/preset/zzz/phone.yaml'
    box = SDBox().load(conf).initiate()
    wrap = SDWrap(box=box).initiate()
    for i in range(box.image_latent.batch_count):
        await wrap.txt2img()


async def dev():
    c, p = ConfigUtil.load('./config/sd/preset/dev.yaml')
    print(c, p)
    pass


async def xml():
    import xml.etree.ElementTree as ET
    x = f"""<OvO>
        <a>power</a>
    </OvO>"""

    tree = ET.fromstring(x)
    print(tree)
    pass


# ==================================================================================================

if __name__ == '__main__':
    time_start = time.perf_counter()
    LogUtil.load('./config/log.yaml')

    asyncio.run(test_wrap())
    # asyncio.run(xml())
    # asyncio.run(dev())

    time_end = time.perf_counter()
    logging.info(f"============= fin in {time_end - time_start:.2f} seconds =========== ")
