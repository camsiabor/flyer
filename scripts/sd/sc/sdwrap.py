import datetime
import logging

from webuiapi import webuiapi

from scripts.common.sim import LogUtil
from scripts.sd.sc.box import SDBox


class SDWrap:

    def __init__(
            self,
            box: SDBox,
            cli: webuiapi.WebUIApi = None,
            log_perf: bool = False,
    ):
        self.box = box
        self.cli = cli
        self.logger = logging.getLogger(f'sdwrap{self.box.server.name}')
        self.log_perf = log_perf
        if log_perf:
            self.logger_perf = logging.getLogger(f'sdwrap{self.box.server.name}_perf')

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

        return self

    @LogUtil.elapsed_async({"name": "txt2img"})
    async def txt2img(self, b: SDBox = None):
        if b is None:
            b = self.box
        params = b.to_params()
        result = await self.cli.txt2img(**params)

        if result.image:
            b.output.infer()
            result.image.save(b.output.file_path)
            self.logger.info(f"txt2img => {b.output.file_path}")
        else:
            self.logger.error(f"txt2img => {result.info}")

        return result
