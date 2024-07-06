from enum import Enum


# import webuiapi
# from webuiapi import HiResUpscaler


class HiResUpscalerEx(str, Enum):
    none = "None"
    Latent = "Latent"
    LatentAntialiased = "Latent (antialiased)"
    LatentBicubic = "Latent (bicubic)"
    LatentBicubicAntialiased = "Latent (bicubic antialiased)"
    LatentNearest = "Latent (nearest)"
    LatentNearestExact = "Latent (nearest-exact)"
    Lanczos = "Lanczos"
    Nearest = "Nearest"
    ESRGAN_4x = "R-ESRGAN 4x+"
    LDSR = "LDSR"
    ScuNET_GAN = "ScuNET GAN"
    ScuNET_PSNR = "ScuNET PSNR"
    SwinIR_4x = "SwinIR 4x"
    # extra
    ESRGAN_4x_Anime6B = "R-ESRGAN 4x+ Anime6B"
