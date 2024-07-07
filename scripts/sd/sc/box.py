# =======================================================
import os
import random
import sys
from datetime import datetime

import yaml

from scripts.common.sim import Reflector
from scripts.sd.sc.alias import HiResUpscalerEx

SEED_MAX = sys.maxsize // 142857


class SDServer:
    def __init__(
            self,
            name="",
            host="127.0.0.1",
            port=30001,
    ):
        self.name = name
        self.host = host
        self.port = port


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
            scheduler=None,
    ):
        self.name = name
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.seed = seed


# =======================================================
class SDPrompt:
    def __init__(
            self,
            positive="",
            negative="low quality, worst quality, bad anatomy",
    ):
        self.positive = positive
        self.negative = negative


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
            colddown=1.0,

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
        self.options = SDOptions()

    def from_yaml(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        with open(path, mode='r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            Reflector.from_dict(self, data)
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

        p.update({
            "prompt": self.prompt.positive,
            "negative_prompt": self.prompt.negative,
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
