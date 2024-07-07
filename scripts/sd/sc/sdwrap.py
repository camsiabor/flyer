import asyncio
import datetime
import json
import logging

from PIL.PngImagePlugin import PngInfo
from webuiapi import webuiapi

from scripts.common.atomic import IntAysnc
from scripts.common.sim import LogUtil
from scripts.sd.sc.box import SDBox


class SDWrap:

    def __init__(
            self,
            box: SDBox,
            cli: webuiapi.WebUIApi = None,
            log_perf: bool = False,
            progress_poll_delay: float = 0.5,
            progress_poll_interval: float = 5,
    ):
        self.box = box
        self.cli = cli
        self.logger = logging.getLogger(f'sd{self.box.server.name}')
        self.log_perf = log_perf
        self.active = True
        self.work_count = IntAysnc()
        if log_perf:
            self.logger_perf = logging.getLogger(f'sd{self.box.server.name}_perf')
        self.progress_thread = None
        self.progress_poll_delay = progress_poll_delay
        self.progress_poll_interval = progress_poll_interval

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

        if self.box.output.dir_path:
            self.box.output.dir_path = datetime.datetime.now().strftime("./output/%Y%m%d")

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
                self.logger.info(
                    f"{job} | {progress:.1f}% | eta: {eta_relative:.1f} | job_count: {job_count} | {text_info}")
            except Exception as e:
                self.logger.error(f"progress_loop error: {e}")
            finally:
                await asyncio.sleep(self.progress_poll_interval - self.progress_poll_delay)

        self.logger.info("progress_loop end")
        pass

    @staticmethod
    def meta_infer(b: SDBox, result, index):
        png_info = PngInfo()
        if not b.options.save_metadata:
            return png_info
        info = result.info
        full = json.dumps(info)
        png_info.add_text("full", full)
        infotexts = info.get("infotexts", [])
        if len(infotexts) <= 0:
            return png_info
        index = index - 1
        if index < 0:
            index = 0
        parameters = infotexts[index]
        png_info.add_text("parameters", parameters)
        return png_info

    def save(self, b: SDBox, result):

        if not result.images or len(result.images) == 0:
            self.logger.error(f"txt2img => {result.info}")
            return result

        img_count = len(result.images)
        if img_count > 1:
            img_index = 1
        else:
            img_index = 0
        for img in result.images:
            b.output.infer(img_index)
            png_info = SDWrap.meta_infer(b, result, img_index)
            img.save(b.output.file_path, pnginfo=png_info)
            img_index += 1
            self.logger.info(f"txt2img => {b.output.file_path}")
        return self

    # txt2img ==================================================================================================
    @LogUtil.elapsed_async({"name": "sd_perf"})
    async def txt2img(self, b: SDBox = None):
        try:
            if b is None:
                b = self.box
            params = b.to_params()
            await self.work_count.increment()
            result = await self.cli.txt2img(**params)
            return self.save(b, result)
        finally:
            # print(1)
            await self.work_count.decrement()
