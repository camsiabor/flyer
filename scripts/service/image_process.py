import concurrent
import io
import os
import time
import traceback
from pathlib import Path

import rembg
from PIL import Image, ImageOps, PngImagePlugin
from PIL import ImageFile
from moviepy.video.io.VideoFileClip import VideoFileClip

from scripts import util
from scripts.common.crypto import CryptoUtil
from scripts.common.sim import Reflector, NumUtil

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessParams:

    def __init__(
            self,
            src_dir="", des_dir="",
            src_file="", des_file="",
            src_img_active=False, src_img=None, des_img=None,
            output_prefix="", output_suffix="", output_extension="",
            chop_active=False, chop_left=0, chop_right=0, chop_upper=0, chop_lower=0,
            resize_width=768, resize_height=1024,
            resize_width_scale=1.0, resize_height_scale=1.0, resize_scale_use=False,
            resize_fill_color="", resize_fill_alpha=-1,
            resize_remove_color="", resize_remove_alpha=-1,
            resize_remove_threshold=100,
            resize_exec=True,
            rembg_model="",
            rembg_color="", rembg_alpha=-1,
            rotation="",
            recursive_depth=None,
            rembg_session=None,
            crypto_enable=False,
            crypto_key="",
    ):
        self.src_dir = src_dir
        self.des_dir = des_dir
        self.src_file = src_file
        self.des_file = des_file
        self.src_img = src_img
        self.des_img = des_img
        self.src_img_active = src_img_active

        self.output_prefix = output_prefix
        self.output_suffix = output_suffix
        self.output_extension = output_extension

        # chop
        self.chop_active = chop_active
        self.chop_left = chop_left
        self.chop_right = chop_right
        self.chop_upper = chop_upper
        self.chop_lower = chop_lower

        # reszie
        self.resize_width = int(resize_width)
        self.resize_height = int(resize_height)
        self.resize_width_scale = float(resize_width_scale)
        self.resize_height_scale = float(resize_height_scale)
        self.resize_scale_use = bool(resize_scale_use)
        self.resize_fill_color = resize_fill_color
        self.resize_fill_alpha = resize_fill_alpha

        self.resize_remove_color = resize_remove_color
        self.resize_remove_alpha = resize_remove_alpha
        self.resize_remove_threshold = resize_remove_threshold

        self.resize_exec = bool(resize_exec)

        # rembg
        self.rembg_model = rembg_model
        self.rembg_color = rembg_color
        self.rembg_alpha = rembg_alpha

        self.rotation = rotation
        if recursive_depth is None:
            recursive_depth = 0
        self.recursive_depth = int(recursive_depth)
        self.rembg_session = rembg_session

        # box key
        self.crypto_ensable = crypto_enable
        self.crypto_key = crypto_key
        pass

    def clone(self):
        return Reflector.clone(self)

    def des_file_infer(self, change=True):
        if not self.src_file:
            raise Exception("missing source file")
        if self.des_file:
            self.des_dir = os.path.dirname(self.des_file)
        if not self.des_dir:
            raise Exception("missing destination directory")

        file_name = os.path.basename(self.src_file)
        file_ext = os.path.splitext(file_name)[1]
        file_name = os.path.splitext(file_name)[0]

        if self.output_prefix:
            file_name = self.output_prefix + file_name
        if self.output_suffix:
            file_name = file_name + self.output_suffix
        if self.output_extension:
            file_name = file_name + "." + self.output_extension
        else:
            file_name = file_name + file_ext
        ret = os.path.join(self.des_dir, file_name)
        if change:
            self.des_file = ret
        return ret


def color_distance(color1, color2):
    # Calculate the Euclidean distance between two colors
    r1, g1, b1 = color1[0], color1[1], color2[2]
    r2, g2, b2 = color2[0], color2[1], color2[2]
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def color_to_transparent(image, target_str, threshold=100):
    # Split the image into individual color channels

    if target_str == 'auto' or target_str == 'def':
        target = color_4_corners(image)
    else:
        target = util.color_string_to_tuple(target_str)

    if len(target) >= 4 and target[3] <= 0:
        return None

        # Get the pixel data from the image
    pixel_data = image.load()

    # Iterate over each pixel
    width, height = image.size
    for y in range(height):
        for x in range(width):
            # Check if the pixel color is similar to the target color
            p = pixel_data[x, y]
            distance = color_distance(p, target)
            if distance <= threshold:
                # Set the pixel to transparent
                pixel_data[x, y] = (0, 0, 0, 0)

    return image


def color_get_most_used(image):
    # Get the colors and their counts
    colors = image.getcolors(image.size[0] * image.size[1])

    # Sort the colors by count in descending order
    sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)

    # Return the most used color
    most_used_color = sorted_colors[0][1]
    return most_used_color


def color_merge_alpha(color, alpha):
    if alpha < 0:
        return ''
    if alpha == 0:
        return 'auto'
    if color is None or len(color) == 0:
        color = '#000000'
    return color + hex(alpha)[2:].zfill(2)


def color_4_corners(image):
    # Get the color values of the four corners
    width, height = image.size
    top_left_color = image.getpixel((0, 0))
    top_right_color = image.getpixel((width - 1, 0))
    bottom_left_color = image.getpixel((0, height - 1))
    bottom_right_color = image.getpixel((width - 1, height - 1))

    # Determine the most frequent color among the corners
    colors = [top_left_color, top_right_color, bottom_left_color, bottom_right_color]
    background_color = max(set(colors), key=colors.count)

    return background_color


def mp4_to_png(p: ImageProcessParams):
    if p.des_dir:
        os.makedirs(p.des_dir, mode=0o777, exist_ok=True)
    else:
        raise Exception("missing destination directory")
    clip = VideoFileClip(p.src_file)
    num_digits = len(str(int(clip.duration * clip.fps)))
    for i, frame in enumerate(clip.iter_frames()):
        frame_image = Image.fromarray(frame)
        p.output_prefix = p.output_prefix or "frame_"
        p.output_suffix = p.output_suffix or "png"
        filename = f"{p.des_dir}/{p.output_prefix}{i:0{num_digits}d}.{p.output_suffix}"
        frame_image.save(filename)


def background_remove(p: ImageProcessParams):
    if p.rembg_session is None:
        return

    if p.src_img_active:
        # Process the image object specified by p.src_img
        src_composite = p.src_img['composite']
        src_img_bytes = io.BytesIO()
        src_composite.save(src_img_bytes, format='PNG')

        data_out = rembg.remove(src_img_bytes.getvalue(), session=p.rembg_session)
        # p.des_img = Image.frombytes('RGBA', src_composite.size, data_out)
        p.des_img = Image.open(io.BytesIO(data_out))
        p.src_img['composite'] = p.des_img
        return

    print("[rembg] {} ---> {}".format(p.src_dir, p.des_dir))

    if p.des_dir:
        os.makedirs(p.des_dir, mode=777, exist_ok=True)

    if p.des_file:
        files = [Path(p.src_file)]
    else:
        pngs = Path(p.src_dir).glob('*.[pP][nN][gG]')
        jpgs = Path(p.src_dir).glob('*.[jJ][pP][gG]')
        jpegs = Path(p.src_dir).glob('*.[jJ][pP][eE][gG]')
        files = list(pngs) + list(jpgs) + list(jpegs)

    p.rembg_color = color_merge_alpha(p.rembg_color, p.rembg_alpha)

    rgba_color = util.color_string_to_tuple(p.rembg_color)

    index = 0
    total = util.file_count(p.src_dir)
    for file in files:
        input_path = str(file)

        if p.des_file:
            output_path = p.des_file
        else:
            output_path = str(p.des_dir + os.path.sep + (file.stem + file.suffix))

        p_file = ImageProcessParams(src_file=input_path, des_file=output_path)
        img, input_path = open_image(p_file)
        input_path = str(input_path)
        output_path = str(output_path)
        if img is not None:
            img.close()

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                data_in = i.read()
                data_out = rembg.remove(data_in, session=p.rembg_session)
                o.write(data_out)
                index = index + 1
                print("[rembg] [{}/{}] {}".format(index, total, output_path))

                # Fill with RGBA color
                background_fill(output_path, rgba_color)

    if total > 0:
        print("")


def background_fill(image_path, bg_color):
    image = Image.open(image_path)
    width, height = image.size
    background = Image.new('RGBA', (width, height), bg_color)
    background.paste(image, (0, 0), mask=image.convert('RGBA'))
    background.save(image_path)
    pass


def open_image(p: ImageProcessParams):
    if not p.src_file:
        raise Exception("missing source file")
    _, ext = os.path.splitext(p.src_file)
    image = Image.open(p.src_file)
    if ext.lower() in ['.jpg', '.jpeg']:
        new_file = os.path.splitext(p.src_file)[0] + '.png'
        image.save(new_file, 'PNG')
        image.close()
        p.src_file = new_file
        if p.des_file:
            p.des_file = p.des_file_infer()
        image = Image.open(new_file)
    return image, p.src_file


def resize_image(p: ImageProcessParams):
    image = None

    if p.src_img_active:  # Process the image object specified by p.src_img
        image = p.src_img['composite']

    if p.src_file:
        image, p.src_file = open_image(p)

    image_info = image.info
    if p.crypto_ensable:
        image_info = CryptoUtil.encrypt_dict(image_info, p.crypto_key)

    image = image.convert('RGBA')

    if image is None:
        raise Exception("missing source image (src_img or src_file)")

    # Add chop functionality
    if p.chop_active:
        if p.chop_left <= -1 or p.chop_left >= image.width:
            p.chop_left = 0
        if p.chop_right <= -1 or p.chop_right >= image.width:
            p.chop_right = image.width
        if p.chop_upper <= -1 or p.chop_upper >= image.height:
            p.chop_upper = 0
        if p.chop_lower <= -1 or p.chop_lower >= image.height:
            p.chop_lower = image.height
        image = image.crop((p.chop_left, p.chop_upper, p.chop_right, p.chop_lower))

    p.resize_remove_color = color_merge_alpha(p.resize_remove_color, p.resize_remove_alpha)

    if util.str_exist(p.resize_remove_color):
        image_ex = color_to_transparent(image, p.resize_remove_color, p.resize_remove_threshold)
        if image_ex is not None:
            image = image_ex

    if p.resize_scale_use:
        resize_width = round(image.width * p.resize_width_scale)
        resize_height = round(image.height * p.resize_height_scale)
        resize_width = NumUtil.odd_to_even(resize_width)
        resize_height = NumUtil.odd_to_even(resize_height)
    else:
        resize_width = p.resize_width
        resize_height = p.resize_height

    if resize_width <= 0:
        resize_width = image.width
    if resize_height <= 0:
        resize_height = image.height

    ratio = image.width / image.height
    to_ratio = resize_width / resize_height

    p.resize_fill_color = color_merge_alpha(p.resize_fill_color, p.resize_fill_alpha)
    if p.resize_fill_color == 'auto' or p.resize_fill_color == 'def':
        color_tuple = color_4_corners(image)
    else:
        color_tuple = util.color_string_to_tuple(p.resize_fill_color)

    if resize_width == image.width and resize_height == image.height:
        new_width = image.width
        new_height = image.height
    else:
        if ratio > to_ratio:
            new_width = resize_width
            new_height = round(new_width / ratio)
        else:
            new_height = resize_height
            new_width = round(new_height * ratio)

    # Resize the image while maintaining the aspect ratio
    resized_image = image.resize((new_width, new_height))

    # Create a new image with the desired dimensions and transparent background
    padded_image = Image.new("RGBA", (resize_width, resize_height), color_tuple)

    # fill color
    """
    if color_tuple[3] > 0:
        draw = ImageDraw.Draw(padded_image)
        draw.rectangle([(0, 0), (to_width, to_height)], fill=color_tuple)
    """

    # Calculate the padding offsets
    x_offset = (resize_width - new_width) // 2
    y_offset = (resize_height - new_height)

    # Paste the resized image onto the padded image with transparent pixels
    padded_image.paste(resized_image, (x_offset, y_offset))

    if "flip" in p.rotation:
        if "flip_h" in p.rotation:
            padded_image = ImageOps.mirror(padded_image)
        if "flip_v" in p.rotation:
            padded_image = ImageOps.flip(padded_image)

    # Save the padded image with transparent pixels

    padded_image.info = image_info

    if p.src_img_active:
        p.des_img = padded_image

    if p.src_file:
        if p.des_file.endswith('png'):
            image_info_obj = PngImagePlugin.PngInfo()
            for key, value in image_info.items():
                image_info_obj.add_text(key, value)
            padded_image.save(p.des_file, format='PNG', pnginfo=image_info_obj)
        else:
            padded_image.save(p.des_file)

    return padded_image


def resize_job(p: ImageProcessParams, index: int, total: int, ):
    try:
        resize_image(p)
        print("[resize] [{}/{}] {}".format(index, total, p.des_file))
    except Exception:
        print(traceback.format_exc())


def resize_directory(p: ImageProcessParams):
    print("[resize] {} ---> {} ".format(p.src_dir, p.des_dir))

    os.makedirs(p.des_dir, mode=0o777, exist_ok=True)

    file_list = []
    for filename in os.listdir(p.src_dir):
        filename = filename.lower()

        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            p.output_prefix = p.output_prefix or ""
            image_path = os.path.join(p.src_dir, filename)
            output_path = os.path.join(p.des_dir, p.output_prefix + filename)
            file_list.append((image_path, output_path))

    total = len(file_list)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for index, (image_path, output_path) in enumerate(file_list, start=1):
            p_file = p.clone()
            p_file.src_file = image_path
            p_file.des_file = p_file.des_file_infer()
            future = executor.submit(
                resize_job,
                p_file,
                index, total
            )
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("An error occurred while processing an image:", str(e))

    if total > 0:
        print("")


def process_single_file(p: ImageProcessParams):
    if p.des_file and os.path.isdir(p.des_file):
        # Set des_dir to be the same directory as des_file
        p.des_dir = os.path.dirname(p.des_file)
        os.makedirs(p.des_dir, exist_ok=True)

    if not p.des_file and os.path.isdir(p.des_dir):
        # Set des_file to be the same filename as src_file but in the des_dir directory
        p.des_file = p.des_file_infer()

    if p.des_file:
        os.makedirs(os.path.dirname(p.des_file), exist_ok=True)

        print("[img-process] src: {}, des: {}".format(p.src_file, p.des_file))

        if p.resize_scale_use:
            print(f"[img-process] resize scale: {p.resize_width_scale}x{p.resize_height_scale} |"
                  f" fill: {p.resize_fill_color} | remove: {p.resize_remove_color}")
        else:
            print(f"[img-process] resize: {p.resize_width}x{p.resize_height} |"
                  f" fill: {p.resize_fill_color} | remove: {p.resize_remove_color}")

        if p.rembg_model and p.rembg_model != "none":
            print("[img-process] rembg_model: {} | fill {}".format(p.rembg_model, p.rembg_color))

        if p.rembg_session is not None:
            background_remove(p)
            if p.resize_exec:
                resize_job(p, 1, 1)
        elif p.resize_exec:
            resize_job(p, 1, 1)
    else:
        raise Exception("missing destination file or directory")
    pass


def process_single_image(p: ImageProcessParams):
    if p.rembg_session is not None:
        background_remove(p)

    if p.resize_exec:
        resize_image(p)

    pass


def process_directory(p: ImageProcessParams):
    sep_count = p.src_dir.count(os.path.sep)

    if p.des_dir:
        os.makedirs(p.des_dir, exist_ok=True)

    for root, dirs, files in os.walk(p.src_dir):
        # Calculate the current depth
        depth = root.count(os.path.sep) - sep_count

        # Skip if max_depth is specified and the current depth exceeds it
        if p.recursive_depth is not None and depth > p.recursive_depth:
            # print("[img-process] max recursive depth reached {} > {}".format(depth, recursive_depth))
            continue

        dir_name = os.path.basename(root)
        if depth <= 0:
            des_path = p.des_dir
        else:
            des_path = str(os.path.join(p.des_dir, dir_name))

        print("[img-process] root: {}, depth: {}, max depth: {}".format(root, depth, p.recursive_depth))
        print("[img-process] name: {}, to: {}".format(dir_name, des_path))
        print("[img-process] resize: {}x{} | fill: {} | remove: {}"
              .format(p.resize_width, p.resize_height, p.resize_fill_color, p.resize_remove_color))
        print("[img-process] rembg_model: {} | fill {}".format(p.rembg_model, p.rembg_color))

        p_subdir = p.clone()
        p_subdir.src_dir = root
        p_subdir.des_dir = des_path
        if p.rembg_session is None:
            if p.resize_exec:
                resize_directory(p_subdir)
        else:
            background_remove(p_subdir)
            if p.resize_exec:
                p_subdir.src_dir = des_path
                resize_directory(p_subdir)
    pass


def process(p: ImageProcessParams):
    start_time = time.time()

    try:

        if p.src_file:
            _, src_file_ext = os.path.splitext(p.src_file)
            if src_file_ext.lower() in ['.mp4']:
                mp4_to_png(p)
                return f"video to png saved to {p.des_dir}"

        if p.rembg_model == "def" or p.rembg_model == "default":
            p.rembg_model = "isnet-anime"

        if p.rembg_model == "" or p.rembg_model == "none" or p.rembg_model == "null":
            p.rembg_session = None
        else:
            p.rembg_session = rembg.new_session(model_name=p.rembg_model)

        if p.src_img_active:
            process_single_image(p)
            return f"image processed"

        if p.src_file:
            process_single_file(p)
            return f"file processed saved to {p.des_file}"

        if p.src_dir and p.des_dir:
            process_directory(p)
            return f"directory processed saved to {p.des_dir}"

        raise Exception("missing source file or directory")

    finally:
        elapsed_time = time.time() - start_time
        print(f"[img-process] elapsed time: {elapsed_time} seconds")
