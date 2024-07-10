import asyncio
import datetime
import functools
import json
import logging
import time

from PIL.PngImagePlugin import PngInfo
from webuiapi import webuiapi

from scripts.common.atomic import IntAysnc, FloatAsync
from scripts.common.crypto import CryptoUtil
from scripts.sd.sc.box import SDBox


def sdwrap_aspect(logger_name="sd-perf"):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            wrap: SDWrap = args[0]
            start_time = time.perf_counter()
            colddown = wrap.box.options.colddown
            try:
                if colddown > 0:
                    await asyncio.sleep(colddown)
                await wrap.work_count.increment()
                result = await func(*args, **kwargs)  # Await the function execution
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                logger = logging.getLogger(logger_name)
                if wrap.verbose:
                    info = result.info
                    logger.info(f"prompt:\n{info.get('prompt', '')}")
                logger.info(f"{func.__name__} completed in {elapsed_time:.2f} seconds")

            except Exception as e:
                wrap.logger.error(f"error: {e}")
                raise e
            finally:
                await wrap.work_count.decrement()

            return result

        return wrapper

    return decorator


class SDWrap:

    @staticmethod
    def generate(conf: any):
        if isinstance(conf, SDBox):
            box = conf
        else:
            box = SDBox().load(conf).initiate()
        return SDWrap(box=box).initiate()

    def __init__(
            self,
            box: SDBox,
            cli: webuiapi.WebUIApi = None,
    ):
        self.box = box
        self.cli = cli
        self.logger = logging.getLogger(f'sd{self.box.server.name}')
        self.active = True
        self.colddown = FloatAsync()
        self.work_count = IntAysnc()

        self.verbose = box.server.verbose
        self.progress_poll_delay = box.server.progress_poll_delay
        self.progress_poll_interval = box.server.progress_poll_interval

        self.progress_thread = None
        pass

    def initiate(self):
        self.cli = webuiapi.WebUIApi(
            host=self.box.server.host,
            port=self.box.server.port,
            sampler=self.box.sampler.name,
            steps=self.box.sampler.steps,
        )
        self.cli.util_wait_for_ready()

        current = self.cli.util_get_current_model()

        if self.box.model.base:
            if current != self.box.model.base:
                self.cli.util_set_model(self.box.model.base)
                self.logger.info(f"switch model to {self.box.model.base} from {current}")
                self.cli.util_wait_for_ready()
        else:
            self.box.model.base = current

        self.logger.info(f"current model: {self.box.model.base}")

        if self.box.output_txt2img.dir_path:
            self.box.output_txt2img.dir_path = datetime.datetime.now().strftime("./output/%Y%m%d")

        if self.progress_thread is None and self.progress_poll_interval > 0:
            self.progress_thread = asyncio.create_task(self.progress_loop())

        return self

    def dormant(self):
        self.active = False
        return self

    # not working
    async def progress_internal_get(self):
        return await self.cli.async_post("/internal/progress", {})

    async def progress_loop(self):
        loop = asyncio.get_running_loop()
        while self.active:
            try:
                if await self.work_count.wait_until_gte(1) <= 0:
                    continue
                if not self.active:
                    break
                await asyncio.sleep(self.progress_poll_delay)
                info = await loop.run_in_executor(None, self.cli.get_progress)
                progress = info.get('progress', 0) * 100
                eta_relative = info.get('eta_relative', 0)
                state = info.get('state', {})
                job = state.get('job', "unknown")
                job_count = state.get('job_count', -1)
                text_info = state.get('text_info', "")
                sampling_step = state.get('sampling_step', -1)
                sampling_stpes = state.get('sampling_steps', -1)
                self.logger.info(
                    f"{job} | {progress:.1f}% | eta: {eta_relative:.1f} | step {sampling_step} / {sampling_stpes} | job_count: {job_count} | {text_info}")
            except Exception as e:
                self.logger.error(f"progress_loop error: {e}")
            finally:
                await asyncio.sleep(self.progress_poll_interval - self.progress_poll_delay)

        self.logger.info("progress_loop end")
        pass

    @staticmethod
    def meta_infer(
            b: SDBox,
            result: webuiapi.WebUIApiResult,
            index: int,
    ):
        png_info = PngInfo()
        if not b.options.metadata_keep:
            return png_info
        info = result.info

        infotexts = info.get("infotexts", [])
        if len(infotexts) <= 0:
            return png_info
        index = index - 1
        if index < 0:
            index = 0
        parameters = infotexts[index]
        full = json.dumps(info)

        metadata_dict = {
            "full": full,
            "parameters": parameters,
        }

        if b.options.metadata_encrypt:
            key = b.options.metadata_key
            if key is None or len(key) <= 0:
                raise ValueError("metadata_key is empty")
            metadata_dict = CryptoUtil.encrypt_dict(metadata_dict, b.options.metadata_key)
            png_info.add_text(CryptoUtil.DICT_HINT_DEF, json.dumps(metadata_dict))
        else:
            png_info.add_text("full", full)
            png_info.add_text("parameters", parameters)
        return png_info

    def save(self, b: SDBox, result: webuiapi.WebUIApiResult):

        if not result.images or len(result.images) == 0:
            self.logger.error(f"txt2img => {result.info}")
            return result

        img_count = len(result.images)
        if img_count > 1:
            img_index = 1
        else:
            img_index = 0
        for img in result.images:
            b.output_txt2img.infer(img_index)
            seed = result.info.get("seed", -1)
            png_info = SDWrap.meta_infer(
                b, result, img_index,
            )

            # save_start = time.perf_counter()
            img.save(b.output_txt2img.file_path, pnginfo=png_info)
            # save_end = time.perf_counter()
            # self.logger.info(f"save {b.output.file_path} in {save_end - save_start:.2f} seconds")

            img_index += 1
            self.logger.info(f"txt2img => {b.output_txt2img.file_path} | seed: {seed}")
        return result

    # txt2img ==================================================================================================
    @sdwrap_aspect()
    async def txt2img(self, b: SDBox = None):
        if b is None:
            b = self.box
        params = b.to_txt2img_params()
        result = await self.cli.txt2img(**params)
        return self.save(b, result)

    @sdwrap_aspect()
    async def extra(self, b: SDBox, *images):
        if len(images) <= 0:
            raise ValueError("images is empty")
        if b is None:
            b = self.box
        params = b.to_extra_params()
        params.update({
            "images": images
        })
        result = await self.cli.extra_batch_images(**params)
        return self.save(b, result, b.extra.save_metadata)
