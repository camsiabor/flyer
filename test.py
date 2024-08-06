import argparse
import asyncio
import logging
import time

from scripts.common.log import LogUtil
from scripts.sd.sc.box import SDBox
from scripts.sd.sc.sdwrap import SDWrap


async def sd_txt2img(cfg: str):
    box = SDBox(config=cfg)
    wrap = SDWrap(box=box).initiate()
    total = box.image_latent.batch_count
    for i in range(total):
        logging.info(f"[ {i + 1} / {total} ]-------------------------------------------------")
        await wrap.txt2img()


async def test():
    print('test')
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
    if args.preset == 'test':
        asyncio.run(test())
    else:
        asyncio.run(sd_txt2img(args.preset))
    time_end = time.perf_counter()
    logging.info(f"============= fin in {time_end - time_start:.2f} seconds =========== ")
