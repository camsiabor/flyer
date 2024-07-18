import functools
import logging
import os
import time

from scripts.common.cfg import ConfigUtil
from scripts.common.sim import getv


# Logging =============================================================================== #

class LogUtil:
    @staticmethod
    def load(*config_path):
        cfg, cfg_path = ConfigUtil.load(*config_path)
        log_path = getv(cfg, "", "handlers", "file_handler", "filename")
        if not os.path.exists(log_path):
            log_dir_path = os.path.dirname(log_path)
            os.makedirs(log_dir_path, exist_ok=True)
        # noinspection PyUnresolvedReferences
        logging.config.dictConfig(cfg)
        return cfg, cfg_path

    @staticmethod
    def elapsed_async(opts: dict):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = await func(*args, **kwargs)  # Await the function execution
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                if opts is None:
                    logger = logging.RootLogger
                else:
                    logger = logging.getLogger(opts.get("name", "perf"))
                logger.info(f"{func.__name__} completed in {elapsed_time:.2f} seconds")
                return result

            return wrapper

        return decorator
