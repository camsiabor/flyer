# =======================================================
import os

import yaml

from scripts.common.sim import Reflector


class SDServer:
    def __init__(
            self,
            host="127.0.0.1",
            port=30001,
            use_async=True,
    ):
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
            active=False,
            scale=1,
            method="ESRGAN_4x_Anime6B",
    ):
        self.active = active
        self.scale = scale
        self.method = method


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
            dirpath="",
            filepath="",
    ):
        self.filepath = filepath
        self.dirpath = dirpath


# =======================================================

class SDBox:

    def __init__(self):
        self.server = SDServer()
        self.model = SDModel()
        self.sampler = SDSampler()
        self.prompt = SDPrompt()
        self.upscaler = SDUpscaler()
        self.latent_image = SDImage()
        self.output = SDFile()

    def from_yaml(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")

        with open(path, mode='r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            Reflector.from_dict(self, data)

        """
        for key, value in data.items():
            if hasattr(self, key):
                attr = getattr(self, key)
                if isinstance(attr, (SDServer, SDModel, SDSampler, SDPrompt, SDUpscaler, SDImage, SDFile)):
                    setattr(self, key, attr.__class__(**value))
                else:
                    setattr(self, key, value)
        """
        return self

# =======================================================
