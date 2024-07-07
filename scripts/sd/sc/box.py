# =======================================================
import os
import random
import sys
from datetime import datetime

import yaml

from scripts.common.sim import Reflector
from scripts.sd.sc.alias import HiResUpscalerEx


class SDServer:
    def __init__(
            self,
            name="",
            host="127.0.0.1",
            port=30001,
            use_async=True,
    ):
        self.name = name
        self.host = host
        self.port = port
        self.use_async = use_async


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
    ):
        self.enable = enable
        self.scale = scale
        self.method = method
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

    def infer(self):
        if self.dir_format:
            self.dir_path = datetime.now().strftime(self.dir_format)
            os.makedirs(self.dir_path, exist_ok=True)

        if self.file_format:
            filename = datetime.now().strftime(self.file_format)
            self.file_path = f"{filename}.{self.file_extension}"
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        else:
            self.file_path = f"{self.dir_path}/{datetime.now().strftime('%Y%m%d%H%M%S')}.{self.file_extension}"

        return self


# SDOptions =======================================================


class SDOptions:

    def __init__(
            self,
            do_not_save_grid=True,
    ):
        self.do_not_save_grid = do_not_save_grid

    """
    enable_hr=False,
        denoising_strength=0.7,
        firstphase_width=0,
        firstphase_height=0,
        hr_scale=2,
        hr_upscaler=HiResUpscaler.Latent,
        hr_second_pass_steps=0,
        hr_resize_x=0,
        hr_resize_y=0,
        prompt="",
        styles=[],
        seed=-1,
        subseed=-1,
        subseed_strength=0.0,
        seed_resize_from_h=0,
        seed_resize_from_w=0,
        sampler_name=None,  # use this instead of sampler_index
        scheduler=None,
        batch_size=1,
        n_iter=1,
        steps=None,
        cfg_scale=7.0,
        width=512,
        height=512,
        restore_faces=False,
        tiling=False,
        do_not_save_samples=False,
        do_not_save_grid=False,
        negative_prompt="",
        eta=1.0,
        s_churn=0,
        s_tmax=0,
        s_tmin=0,
        s_noise=1,
        override_settings={},
        override_settings_restore_afterwards=True,
        script_args=None,  # List of arguments for the script "script_name"
        script_name=None,
        send_images=True,
        save_images=False,
        alwayson_scripts={},
        controlnet_units: List[ControlNetUnit] = [],
        adetailer: List[ADetailer] = [],
        roop: Roop = None,
        reactor: ReActor = None,
        sag: Sag = None,
        sampler_index=None,  # deprecated: use sampler_name
        use_deprecated_controlnet=False,
        use_async=False,
        """

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
        return random.randint(1, sys.maxsize - 1)

    def to_params(self, use_async=True):
        seed = self.seeding()
        p = {
            "prompt": self.prompt.positive,
            "negative_prompt": self.prompt.negative,
            "sampler_name": self.sampler.name,
            "steps": self.sampler.steps,
            "cfg_scale": self.sampler.cfg_scale,
            "seed": seed,
            "width": self.image_latent.width,
            "height": self.image_latent.height,
            "use_async": use_async,
        }

        if self.upscaler.enable and self.upscaler.scale > 1:
            if not self.upscaler.method:
                self.upscaler.method = HiResUpscalerEx.ESRGAN_4x_Anime6B
            p.update({
                "enable_hr": self.upscaler.enable,
                "hr_scale": self.upscaler.scale,
                "hr_upscaler": self.upscaler.method,
                "hr_second_pass_steps": self.upscaler.second_pass_steps,
                "denoising_strength": self.upscaler.denoising_strength,
            })

        return p

# =======================================================
