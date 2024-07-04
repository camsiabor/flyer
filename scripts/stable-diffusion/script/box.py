import yaml


class SDBox:
    def __init__(
            self,
            host="127.0.0.1",
            port=30001,
            sampler_name="Eular a",
            sampler_steps=20,
            cfg_scale=7,
            model_target="nai3",
            prompt="",
            negative_prompt="low quality, worst quality",
            seed=-1,
            width=1024, height=1024,
            use_async=True,
    ):
        self.host = host
        self.port = port
        self.sampler_name = sampler_name
        self.sampler_steps = sampler_steps
        self.model_target = model_target
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.sampler_name = sampler_name
        self.cfg_scale = cfg_scale
        self.seed = seed
        self.width = width
        self.height = height
        self.use_async = use_async

    # generate function to clone the object
    def clone(self):
        return SDBox(
            host=self.host,
            port=self.port,
            sampler_name=self.sampler_name,
            sampler_steps=self.sampler_steps,
            cfg_scale=self.cfg_scale,
            model_target=self.model_target,
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            seed=self.seed,
            width=self.width,
            height=self.height,
            use_async=self.use_async,
        )

    @staticmethod
    def load_from_yaml(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            return SDBox(
                host=config.get('host', '127.0.0.1'),
                port=config.get('port', 30001),
                sampler_name=config.get('sampler_name', 'Eular a'),
                sampler_steps=config.get('sampler_steps', 20),
                cfg_scale=config.get('cfg_scale', 7),
                model_target=config.get('model_target', 'nai3'),
                prompt=config.get('prompt', ''),
                negative_prompt=config.get('negative_prompt', 'low quality, worst quality'),
                seed=config.get('seed', -1),
                width=config.get('width', 1024),
                height=config.get('height', 1024),
                use_async=config.get('use_async', True),
            )
