import asyncio
import datetime
import logging

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
            progress_poll_interval: int = -1,
    ):
        self.box = box
        self.cli = cli
        self.logger = logging.getLogger(f'sdwrap{self.box.server.name}')
        self.log_perf = log_perf
        self.active = True
        self.work_count = IntAysnc()
        if log_perf:
            self.logger_perf = logging.getLogger(f'sdwrap{self.box.server.name}_perf')
        self.progress_thread = None
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
                # info = self.cli.get_progress()
                # info = await self.progress_internal_get()
                info = await loop.run_in_executor(None, self.cli.get_progress)
                progress = info.get('progress', 0) * 100
                eta_relative = info.get('eta_relative', 0)
                self.logger.info(f"{progress:.1f}% | eta: {eta_relative:.1f}")
            except Exception as e:
                self.logger.error(f"progress_loop error: {e}")
            finally:
                await asyncio.sleep(self.progress_poll_interval)

        self.logger.info("progress_loop end")

    @LogUtil.elapsed_async({"name": "txt2img"})
    async def txt2img(self, b: SDBox = None):
        try:
            if b is None:
                b = self.box
            params = b.to_params()
            await self.work_count.increment()
            result = await self.cli.txt2img(**params)

            if result.image:
                b.output.infer()
                result.image.save(b.output.file_path)
                self.logger.info(f"txt2img => {b.output.file_path}")
            else:
                self.logger.error(f"txt2img => {result.info}")
            return result
        finally:
            # print(1)
            await self.work_count.decrement()
