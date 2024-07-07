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


class ADetailerModel(str, Enum):
    face_yolov8n = "face_yolov8n.pt"
    face_yolov8s = "face_yolov8s.pt"
    hand_yolov8n = "hand_yolov8n.pt"
    person_yolov8n_seg = "person_yolov8n-seg.pt"
    person_yolov8s_seg = "person_yolov8s-seg.pt"
    yolov8x_worldv2 = "yolov8x-worldv2.pt"
    mediapipe_face_full = "mediapipe_face_full"
    mediapipe_face_short = "mediapipe_face_short"
    mediapipe_face_mesh = "mediapipe_face_mesh"
    mediapipe_face_mesh_eyes_only = "mediapipe_face_mesh_eyes_only"
