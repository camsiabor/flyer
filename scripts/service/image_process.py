import concurrent
import os
import time
from pathlib import Path

import rembg
from PIL import Image, ImageOps

from scripts import util


class ImageProcessParams:

    def __init__(
            self,
            src_dir, des_dir,
            src_file="", des_file="",
            resize_width=768, resize_height=1024,
            resize_fill_color="", resize_remove_color="",
            resize_remove_threshold=100,
            resize_exec=True,
            rembg_model="", rembg_color="",
            rotation="",
            recursive_depth=None,
    ):
        self.src_dir = src_dir
        self.des_dir = des_dir
        self.src_file = src_file
        self.des_file = des_file
        self.resize_width = int(resize_width)
        self.resize_height = int(resize_height)
        self.resize_fill_color = resize_fill_color
        self.resize_remove_color = resize_remove_color
        self.resize_remove_threshold = resize_remove_threshold
        self.resize_exec = bool(resize_exec)
        self.rembg_model = rembg_model
        self.rembg_color = rembg_color
        self.rotation = rotation
        if recursive_depth is None:
            recursive_depth = 0
        self.recursive_depth = int(recursive_depth)

    def clone(self):
        return ImageProcessParams(
            self.src_dir, self.des_dir,
            self.src_file, self.des_file,
            self.resize_width, self.resize_height,
            self.resize_fill_color, self.resize_remove_color,
            self.resize_remove_threshold,
            self.resize_exec,
            self.rembg_model, self.rembg_color,
            self.rotation,
            self.recursive_depth
        )


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


def background_remove(p: ImageProcessParams, session):
    if session is None:
        return

    print("[rembg] {} ---> {}".format(p.src_dir, p.des_dir))

    os.makedirs(p.des_dir, mode=777, exist_ok=True)

    files = Path(p.src_dir).glob('*.[pP][nN][gG]')

    rgba_color = util.color_string_to_tuple(p.rembg_color)

    index = 0
    total = util.file_count(p.src_dir)
    for file in files:
        input_path = str(file)
        output_path = str(p.des_dir + os.path.sep + (file.stem + file.suffix))

        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                data_in = i.read()
                data_out = rembg.remove(data_in, session=session)
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


def resize_image(p: ImageProcessParams):
    image = Image.open(p.src_file)
    image = image.convert('RGBA')

    if util.str_exist(p.resize_remove_color):
        image_ex = color_to_transparent(image, p.resize_remove_color, p.resize_remove_threshold)
        if image_ex is not None:
            image = image_ex

    ratio = image.width / image.height
    to_ratio = p.resize_width / p.resize_height

    color_tuple = util.color_string_to_tuple(p.resize_fill_color)

    if ratio > to_ratio:
        new_width = p.resize_width
        new_height = round(new_width / ratio)
    else:
        new_height = p.resize_height
        new_width = round(new_height * ratio)

    # Resize the image while maintaining the aspect ratio
    resized_image = image.resize((new_width, new_height))

    # Create a new image with the desired dimensions and transparent background
    padded_image = Image.new("RGBA", (p.resize_width, p.resize_height), color_tuple)

    # fill color
    """
    if color_tuple[3] > 0:
        draw = ImageDraw.Draw(padded_image)
        draw.rectangle([(0, 0), (to_width, to_height)], fill=color_tuple)
    """

    # Calculate the padding offsets
    x_offset = (p.resize_width - new_width) // 2
    y_offset = (p.resize_height - new_height)

    # Paste the resized image onto the padded image with transparent pixels
    padded_image.paste(resized_image, (x_offset, y_offset))

    if "flip" in p.rotation:
        if "flip_h" in p.rotation:
            padded_image = ImageOps.mirror(padded_image)
        if "flip_v" in p.rotation:
            padded_image = ImageOps.flip(padded_image)

    # Save the padded image with transparent pixels
    padded_image.save(p.des_file)


def resize_job(p: ImageProcessParams, index: int, total: int, ):
    resize_image(p)
    print("[resize] [{}/{}] {}".format(index, total, p.des_file))


def resize_directory(p: ImageProcessParams):
    print("[resize] {} ---> {} ".format(p.src_dir, p.des_dir))

    if p.resize_width <= 0:
        p.resize_width = 768

    if p.resize_height <= 0:
        p.resize_height = 1024

    os.makedirs(p.des_dir, mode=0o777, exist_ok=True)

    file_list = []
    for filename in os.listdir(p.src_dir):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(p.src_dir, filename)
            output_path = os.path.join(p.des_dir, filename)
            file_list.append((image_path, output_path))

    total = len(file_list)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for index, (image_path, output_path) in enumerate(file_list, start=1):
            p_file = p.clone()
            p_file.src_file = image_path
            p_file.des_file = output_path
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


def process(p: ImageProcessParams):
    start_time = time.time()

    try:

        if p.resize_width <= 0:
            p.resize_width = 768
        if p.resize_height <= 0:
            p.resize_height = 1024

        os.makedirs(p.des_dir, mode=0o777, exist_ok=True)

        sep_count = p.src_dir.count(os.path.sep)

        if p.rembg_model == "def" or p.rembg_model == "default":
            p.rembg_model = "isnet-anime"

        if p.rembg_model == "" or p.rembg_model == "none" or p.rembg_model == "null":
            rembg_session = None
        else:
            rembg_session = rembg.new_session(model_name=p.rembg_model)

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
            if rembg_session is None:
                if p.resize_exec:
                    resize_directory(p_subdir)
            else:
                background_remove(p_subdir, rembg_session)
                if p.resize_exec:
                    p_subdir.src_dir = des_path
                    resize_directory(p_subdir)
    finally:
        elapsed_time = time.time() - start_time
        print(f"[img-process] elapsed time: {elapsed_time} seconds")
