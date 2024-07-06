# =======================================================

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
    server: SDServer
    model: SDModel
    sampler: SDSampler
    prompt: SDPrompt
    latent_image: SDImage
    output: SDFile
