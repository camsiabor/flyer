# =======================================================
import os
import random
import sys
from datetime import datetime

import webuiapi

from scripts.common.serial import TypeList
from scripts.common.sim import Reflector, ConfigUtil
from scripts.common.textutil import TextUtil
from scripts.sd.sc.alias import HiResUpscalerEx

SEED_MAX = sys.maxsize // 142857


class SDServer:
    def __init__(
            self,
            name="",
            host="127.0.0.1",
            port=30001,
            progress_poll_delay=1,
            progress_poll_interval=6,
            verbose=False,
    ):
        self.name = name
        self.host = host
        self.port = port
        self.progress_poll_delay = progress_poll_delay
        self.progress_poll_interval = progress_poll_interval
        self.verbose = verbose


# =======================================================
class SDModel:
    def __init__(
            self,
            base="",
            vae="",
            refiner="",

    ):
        self.base = base
        self.vae = vae
        self.refiner = refiner


# =======================================================
class SDSampler:

    def __init__(
            self,
            name="Euler a",
            steps=20,
            cfg_scale=7,
            seed=-1,
            subseed=-1,
            scheduler=None,
    ):
        self.name = name
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.seed = seed
        self.subseed = subseed
        self.scheduler = scheduler


# =======================================================
class SDPrompt:
    def __init__(
            self,
            positive="",
            negative="",
            params_cycle: int = 0,
            params_prefix: str = "$$",
            params_suffix: str = "$$",
            params_pos_1: dict = None,
            params_pos_2: dict = None,
            params_pos_3: dict = None,
            params_neg_1: dict = None,
            params_neg_2: dict = None,
            params_neg_3: dict = None,
    ):
        self.positive = positive
        self.negative = negative

        self.params_cycle = params_cycle
        self.params_prefix = params_prefix
        self.params_suffix = params_suffix

        self.params_pos_1 = params_pos_1
        self.params_pos_2 = params_pos_2
        self.params_pos_3 = params_pos_3
        self.params_neg_1 = params_neg_1
        self.params_neg_2 = params_neg_2
        self.params_neg_3 = params_neg_3
        pass


    def infer(self):

        pos = self.positive
        neg = self.negative

        for i in range(1, 3):
            params = getattr(self, f"params_pos_{i}")
            if params is not None:
                pos = TextUtil.replace(
                    src=pos,
                    params=params,
                    cycle=self.params_cycle,
                    prefix=self.params_prefix,
                    suffix=self.params_suffix,
                )
            params = getattr(self, f"params_neg_{i}")
            if params is not None:
                neg = TextUtil.replace(
                    src=neg,
                    params=params,
                    cycle=self.params_cycle,
                    prefix=self.params_prefix,
                    suffix=self.params_suffix,
                )

        if self.params_cycle >= 0:
            self.params_cycle += 1
        else:
            self.params_cycle -= 1

        return pos, neg


# =======================================================
class SDUpscaler:
    def __init__(
            self,
            enable=False,
            scale=1.25,
            method=HiResUpscalerEx.ESRGAN_4x_Anime6B,
            second_pass_steps=10,
            denoising_strength=0.5,
            resize_x=0,
            resize_y=0,
    ):
        self.enable = enable
        self.method = method
        self.scale = scale
        self.resize_x = resize_x
        self.resize_y = resize_y
        self.second_pass_steps = second_pass_steps
        self.denoising_strength = denoising_strength


# =======================================================
class SDImage:
    def __init__(
            self,
            width=1024,
            height=1024,
            batch_size=1,
            batch_count=1,
    ):
        self.width = width
        self.height = height
        self.batch_size = batch_size
        self.batch_count = batch_count


# SDFile =======================================================
class SDFile:
    def __init__(
            self,
            dir_path="",
            dir_format="",
            file_path="",
            file_format="",
            file_extension="png",
    ):
        self.dir_path = dir_path
        self.dir_format = dir_format
        self.file_path = file_path
        self.file_format = file_format
        self.file_extension = file_extension

    def infer(self, index=-1):
        if self.dir_format:
            self.dir_path = datetime.now().strftime(self.dir_format)
            os.makedirs(self.dir_path, exist_ok=True)

        if index <= 0:
            index_str = ""
        else:
            index_str = "-" + str(index).zfill(2)

        if self.file_format:
            filename = datetime.now().strftime(self.file_format)
            self.file_path = f"{filename}{index_str}.{self.file_extension}"
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        else:
            self.file_path = f"{self.dir_path}/{datetime.now().strftime('%Y%m%d%H%M%S')}{index_str}.{self.file_extension}"

        return self


# SDOptions =======================================================


class SDOptions:

    def __init__(
            self,
            styles=None,
            tiling=False,
            do_not_save_grid=True,
            do_not_save_samples=True,
            use_async=True,
            save_metadata=True,
            colddown=0.1,

    ):
        if styles is None:
            styles = []
        self.styles = styles
        self.tiling = tiling
        self.do_not_save_grid = do_not_save_grid
        self.do_not_save_samples = do_not_save_samples
        self.use_async = use_async
        self.save_metadata = save_metadata
        self.colddown = colddown


# SDADetailer =======================================================

class SDADetailer:

    def __init__(
            self,
            enable=False,
            model=None,
            confidence=0.3,
            denoising_strength=0.4,
    ):
        self.enable = enable
        self.model = model
        self.prompt = SDPrompt()
        self.confidence = confidence
        self.denoising_strength = denoising_strength

    def to_api_obj(self):
        ad = webuiapi.ADetailer(
            ad_model=self.model,
            ad_prompt=self.prompt.positive,
            ad_negative_prompt=self.prompt.negative,
            ad_confidence=self.confidence,
            ad_denoising_strength=self.denoising_strength,
        )
        return ad


# =======================================================

class SDBox:

    def __init__(self):
        self.server = SDServer()
        self.model = SDModel()
        self.sampler = SDSampler()
        self.prompt = SDPrompt()
        self.upscaler = SDUpscaler()
        self.image_latent = SDImage()
        self.output = SDFile()
        self.adetailers = TypeList(SDADetailer)
        self.options = SDOptions()

    def load(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The file {config_path} does not exist.")
        config, _ = ConfigUtil.load_and_embed(
            config_path,
        )
        Reflector.from_dict(self, config)
        return self

    def initiate(self):
        Reflector.invoke_children(self, "initiate")
        return self

    def seeding(self):
        if self.sampler.seed >= 0:
            return self.sampler.seed
        return random.randint(0, SEED_MAX)

    def to_params(self):
        seed = self.seeding()

        p = {
            "width": self.image_latent.width,
            "height": self.image_latent.height,
            "batch_size": self.image_latent.batch_size,
        }

        pos, neg = self.prompt.infer()

        p.update({
            "prompt": pos,
            "negative_prompt": neg,
        })

        p.update({
            "sampler_name": self.sampler.name,
            "steps": self.sampler.steps,
            "cfg_scale": self.sampler.cfg_scale,
            "seed": seed,
        })

        # upscale
        if self.upscaler.enable:
            if not self.upscaler.method:
                self.upscaler.method = HiResUpscalerEx.ESRGAN_4x_Anime6B
            p.update({
                "enable_hr": True,
                "hr_upscaler": self.upscaler.method,
                "hr_second_pass_steps": self.upscaler.second_pass_steps,
                "denoising_strength": self.upscaler.denoising_strength,
            })

            if self.upscaler.scale > 1:
                p.update({"hr_scale": self.upscaler.scale, })

            if self.upscaler.resize_x > 0 and self.upscaler.resize_y > 0:
                p.update({
                    "hr_resize_x": self.upscaler.resize_x,
                    "hr_resize_y": self.upscaler.resize_y,
                })

        if len(self.adetailers) > 0:
            ads = []
            for one in self.adetailers:
                ad: SDADetailer = one
                if ad.enable:
                    ads.append(ad.to_api_obj())
            if len(ads) > 0:
                p.update({"adetailer": ads})

        # options
        p.update({
            "styles": self.options.styles,
            "tiling": self.options.tiling,
            "do_not_save_grid": self.options.do_not_save_grid,
            "do_not_save_samples": self.options.do_not_save_samples,
        })

        p.update({
            "use_async": self.options.use_async,
        })

        return p

# =======================================================
