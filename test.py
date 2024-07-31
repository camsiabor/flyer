import argparse
import asyncio
import logging
import time

from PIL import Image

from scripts.common.directive import Directorate
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

async def test_wrap(cfg: str):
    box = SDBox(config=cfg)
    wrap = SDWrap(box=box).initiate()
    total = box.image_latent.batch_count
    for i in range(total):
        print(f"[ {i + 1} / {total} ]-------------------------------------------------")
        await wrap.txt2img()


async def dev():
    v = Directorate.load_and_embed('config/sd/preset/0_posture/nsfw/back.py')
    print(v)
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--preset', type=str, required=True, help='preset config path')
    return parser.parse_args()


# ==================================================================================================

if __name__ == '__main__':
    time_start = time.perf_counter()
    args = parse_args()
    LogUtil.load('./config/log.yaml')

    # preset = './config/sd/preset/zzz/feet.yaml'
    # preset = './config/sd/preset/v/vr/shiori/white.yaml'
    # preset = './config/sd/preset/hoyoverse/starrail/firefly.yaml'
    # preset = './config/sd/preset/safe.yaml'
    # preset = './config/sd/preset/nsfw.yaml'
    asyncio.run(test_wrap(args.preset))

    # asyncio.run(dev())

    time_end = time.perf_counter()
    logging.info(f"============= fin in {time_end - time_start:.2f} seconds =========== ")
