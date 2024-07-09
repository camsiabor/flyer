import json
import os

import gradio as gr
import pandas
from PIL import Image
from PIL import ImageDraw

import ui.common.console as uicon
from scripts import util
from scripts.common.crypto import CryptoUtil
from scripts.common.sim import ConfigUtil
from scripts.service import image_process, video_process, net_process, text_process
from scripts.service.image_process import ImageProcessParams
from scripts.util import FileIO

cfg_gradio = {
    "port": 10005,
}

cfg_http = {
    "port": 10006,
}


def img_process_interface(
        src_dir, des_dir,
        src_file, des_file,
        src_img_active, src_img, des_img,
        output_prefix, output_suffix, output_extension,
        chop_active, chop_left, chop_right, chop_upper, chop_lower,
        resize,
        resize_fill_color, resize_fill_alpha,
        resize_remove_color, resize_remove_alpha, resize_remove_threshold,
        rembg_model,
        rembg_color, rembg_alpha,
        rotation,
        recursive_depth,
        crypto_enable, crypto_key,
):
    resize_width, resize_height = map(int, resize.split('x'))

    if crypto_enable and len(crypto_key) <= 0:
        cfg = ConfigUtil.retrieve('cfg')
        crypto_key = cfg.get('box_key', '')

    params = ImageProcessParams(
        # src & des
        src_dir=src_dir, des_dir=des_dir,
        src_file=src_file, des_file=des_file,
        src_img_active=src_img_active, src_img=src_img, des_img=des_img,
        # output
        output_prefix=output_prefix, output_suffix=output_suffix, output_extension=output_extension,
        # chop params
        chop_active=chop_active,
        chop_left=chop_left, chop_right=chop_right,
        chop_upper=chop_upper, chop_lower=chop_lower,
        # resize params
        resize_width=resize_width, resize_height=resize_height,
        resize_fill_color=resize_fill_color, resize_fill_alpha=resize_fill_alpha,
        resize_remove_color=resize_remove_color, resize_remove_alpha=resize_remove_alpha,
        resize_remove_threshold=resize_remove_threshold,
        rotation=rotation,
        # rembg params
        rembg_model=rembg_model,
        rembg_color=rembg_color, rembg_alpha=rembg_alpha,
        # extra
        recursive_depth=recursive_depth,
        # crypto
        crypto_enable=crypto_enable, crypto_key=crypto_key,
    )

    ret = image_process.process(params)

    if params.src_img_active and params.des_img is not None:
        img_processed = params.des_img
        params.des_img = {
            'background': img_processed,
            'layers': [img_processed],
            'composite': img_processed,
        }

    return ret, params.des_img


@uicon.capture_wrap
def media_to_wav_interface(src_file, des_file):
    video_process.convert_mp4_to_wav(src_file, des_file)
    return f"Converted WAV file is saved as {des_file}"


@uicon.capture_wrap
def media_split_interface(src_dir, des_dir, divider, file_ext):
    video_process.duration_split(src_dir, des_dir, divider, file_ext)
    return f"Videos split successfully into {des_dir}"


@uicon.capture_wrap
def media_duration_sum_interface(directory):
    total_sec = video_process.duration_sum(directory)
    t = util.format_time(total_sec)
    return f"Total Duration: {t}"


def image_metadata_interface(image):
    if image is None:
        return "", "", None

    box_key = ConfigUtil.retrieve('cfg').get('box_key', '')
    meta = image.info
    is_encrypt = CryptoUtil.encrypt_probe(meta)
    if is_encrypt:
        meta = CryptoUtil.decrypt_dict(meta, box_key)
    meta_full = json.dumps(meta, indent=4)
    meta_parameters = meta.get('parameters', '')
    if is_encrypt:
        meta_full = f"encrypt:\n{meta_full}"

    return meta_parameters, meta_full, image


def image_batch_metadata_interface(image_dir, text_remove):
    if not os.path.isdir(image_dir):
        return "Directory not found", pandas.DataFrame()
    image_index = 1
    data = []
    removes = text_remove.split('|')
    box_key = ConfigUtil.retrieve('cfg').get('box_key', '')
    for filename in os.listdir(image_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(image_dir, filename)
            try:
                with Image.open(image_path) as img:
                    meta = img.info
                    is_encrypt = CryptoUtil.encrypt_probe(meta)
                    if is_encrypt:
                        meta = CryptoUtil.decrypt_dict(meta, box_key)
                    meta_parameters = meta.get('parameters', '')
                    meta_parameters = meta_parameters.split('Negative prompt:')[0].strip()
                    for remove in removes:
                        meta_parameters = meta_parameters.replace(remove, '')
                    meta_parameters = f"```\n{meta_parameters}\n```"

                    color = 'orange' if is_encrypt else 'white'
                    image_path_markdown = f"""
<div style='text-align: center;'>
    <img src="file/{image_path}" alt="{filename}" style="max-width: 200px; max-height: 200px; display: block; margin-left: auto; margin-right: auto;">
    <div style='color: {color}; font: 0.9em; '>{img.width} x {img.height}</div>
    <div style='color: {color}; font: 0.7em; '>{filename}</div>
</div>
"""

                    index_info = f"<span style='color: {color};'>{image_index}</span>"
                    data.append({
                        'Image Path': image_path_markdown,
                        'Metadata': meta_parameters,
                        'Index': index_info
                    })
                    image_index += 1
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue  # Skip files that cannot be opened as images

    frames = pandas.DataFrame(data)
    return "Processed successfully", frames


def media_fetch_interface(
        src, des, t_start, t_end,
):
    output_path, ret = net_process.fetch_by_yt_dlp(
        src, des,
        t_start, t_end,
    )
    if output_path is None:
        return ret, None

    return output_path.resolve(), output_path


@uicon.capture_wrap
def text_process_interface(
        src_dir, des_dir,
        file_ext, recursive_depth, buffer_size,
        action
):
    def callback(src_file, des_file, _):
        text_process.to_utf8(src_file, des_file, buffer_size)

    if action == "to_utf_8":
        FileIO.walk_des(
            src_dir=src_dir,
            des_dir=des_dir,
            callback_dir=None,
            callback_file=callback,
            file_ext=file_ext,
            depth_limit=recursive_depth,
            callback_args=buffer_size,
        )
        return f"Text files in {src_dir} are converted to UTF-8 and saved in {des_dir}"

    return f"Invalid action selected: {action}"


def tab_image_process():
    def chop_change(preview, left, right, upper, lower):
        bg = preview['background']
        n = Image.new('RGBA', bg.size, (0, 0, 0, 0))
        if left < 0 or left > bg.width:
            left = 0
        if right < 0 or right > bg.width:
            right = bg.width
        if upper < 0 or upper > bg.height:
            upper = 0
        if lower < 0 or lower > bg.height:
            lower = bg.height
        if right < left:
            right = left
        if lower < upper:
            lower = upper
        draw = ImageDraw.Draw(n)
        draw.rectangle([left, upper, right, lower], outline='red', width=1)
        preview['layers'] = [n]
        return preview

    with gr.Row():
        with gr.Tab("Directory"):
            src_dir = gr.Textbox(label="Source Directory")
            des_dir = gr.Textbox(label="Destination Directory")
        with gr.Tab("Single File Path"):
            src_file = gr.Textbox(label="Source File")
            des_file = gr.Textbox(label="Destination File")
        with gr.Tab("Single Image"):
            with gr.Column(scale=1):
                src_img_active = gr.Checkbox(label="Source Image Active", value=False)
                src_img = gr.ImageEditor(
                    label="Source Image", type="pil",
                    sources=["upload", "clipboard"],
                )
            with gr.Column(scale=1):
                des_img = gr.ImageEditor(
                    label="Destination Image", type="pil",
                    sources=["upload", "clipboard"]
                )
    with gr.Row():
        with gr.Tab("Resize"):
            with gr.Row():
                resize = gr.Textbox(value="768x1024", label="Resize (e.g., 512x512)")
                resize_fill_color = gr.ColorPicker(label="Resize Fill Color", value='#000000')
                resize_fill_alpha = gr.Slider(label="Resize Fill Alpha", value=-1, minimum=-1, maximum=255)
            with gr.Row():
                resize_remove_color = gr.ColorPicker(label="Resize Remove Color", value='#000000')
                resize_remove_alpha = gr.Slider(label="Resize Remove Alpha", value=-1, minimum=-1, maximum=255)
                resize_remove_threshold = gr.Number(label="Resize Remove Threshold", value=100)
        with gr.Tab("Remove Background"):
            with gr.Row():
                rembg_model = gr.Dropdown(
                    label="Remove Background Model  "
                          "| 'none' for no removing  "
                          "| first time executing takes a while  ",
                    value="none",
                    choices=[
                        "none",
                        "u2net",
                        "u2netp",
                        "u2net_human_seg",
                        "u2net_cloth_seg",
                        "silueta",
                        "isnet-general-use",
                        "isnet-anime",
                        "sam"
                    ]
                )
                rembg_color = gr.ColorPicker(label="Remove Background Color")
                rembg_alpha = gr.Slider(label="Remove Background Alpha", value=-1, minimum=-1, maximum=255)
        with gr.Tab("Chop"):
            with gr.Row():
                chop_active = gr.Checkbox(label="Chop Active", value=False)
                chop_left = gr.Number(label="Chop Left", value=-1)
                chop_right = gr.Number(label="Chop Right", value=-1)
                chop_upper = gr.Number(label="Chop Upper", value=-1)
                chop_lower = gr.Number(label="Chop Lower", value=-1)
            with gr.Row():
                chop_preview = gr.ImageEditor(label="Chop Preview", type="pil")
            chop_inputs = [chop_preview, chop_left, chop_right, chop_upper, chop_lower]
            chop_outputs = [chop_preview]
            chop_left.change(chop_change, chop_inputs, chop_outputs)
            chop_right.change(chop_change, chop_inputs, chop_outputs)
            chop_upper.change(chop_change, chop_inputs, chop_outputs)
            chop_lower.change(chop_change, chop_inputs, chop_outputs)
            pass
        with gr.Tab("Output"):
            output_prefix = gr.Textbox(label="Output Prefix")
            output_suffix = gr.Textbox(label="Output Suffix")
            output_extension = gr.Textbox(label="Output Extension")
            pass
        with gr.Tab("Mask"):
            pass
        with gr.Tab("Crypto"):
            crypto_enable = gr.Checkbox(label="Crypto Enable", value=True)
            crypto_key = gr.Textbox(label="Crypto Key", value="")
            pass
    with gr.Row():
        recursive_depth = gr.Number(label="Recursive Depth", value=0)
        rotation = gr.Dropdown(
            label="Rotation",
            value="none",
            choices=[
                "none",
                "flip_horizontally",
                "flip_vertically",
                "flip_horizontally_flip_vertically",
            ]
        )
        run_img = gr.Button("Run Image Processing")
    with gr.Row():
        result = gr.TextArea(label="Result")

    run_img.click(
        fn=uicon.capture_wrap(func=img_process_interface, num_result=2),
        inputs=[
            src_dir, des_dir,
            src_file, des_file,
            src_img_active, src_img, des_img,
            output_prefix, output_suffix, output_extension,
            chop_active, chop_left, chop_right, chop_upper, chop_lower,
            resize,
            resize_fill_color, resize_fill_alpha,
            resize_remove_color, resize_remove_alpha, resize_remove_threshold,
            rembg_model,
            rembg_color, rembg_alpha,
            rotation,
            recursive_depth,
            crypto_enable, crypto_key,
        ],
        outputs=[
            result, des_img
        ]
    )


def tab_video_to_wav():
    src_file = gr.Textbox(label="Source Video File")
    des_file = gr.Textbox(label="Destination WAV File")
    run_wav = gr.Button("Convert to WAV")
    result = gr.TextArea(label="Result")
    run_wav.click(media_to_wav_interface, inputs=[src_file, des_file], outputs=[result])


def tab_media_split():
    split_src_dir = gr.Textbox(label="Source Directory")
    split_des_dir = gr.Textbox(label="Destination Directory")
    divider = gr.Number(label="Divider", value=2)
    file_ext = gr.Textbox(label="File Extension", value="wav")
    run_split = gr.Button("Split Video")
    result = gr.TextArea(label="Result")
    run_split.click(
        media_split_interface,
        inputs=[split_src_dir, split_des_dir, divider, file_ext],
        outputs=[result]
    )


def tab_media_sum_duration():
    sum_dir = gr.Textbox(label="Directory")
    run_sum = gr.Button("Sum Media Duration")
    result = gr.TextArea(label="Result")
    run_sum.click(media_duration_sum_interface, inputs=[sum_dir], outputs=[result])


def tab_media_fetch():
    with gr.Row():
        with gr.Column(scale=1):
            text_src_path = gr.Textbox(label="Source Path", value="")
            text_des_path = gr.Textbox(label="Destination", value="")
            with gr.Group():
                with gr.Row():
                    num_src_start = gr.Number(value=0, label="Start (sec)")
                    num_src_end = gr.Number(value=0, label="End (sec)")
                    button_src_url = gr.Button("Fetch Source", variant="primary")
                with gr.Row():
                    text_result = gr.TextArea(label="Result")
        with gr.Column(scale=1):
            audio_src = gr.Audio(
                label="Source",
                interactive=True,
                show_download_button=True,
            )

    button_src_url.click(
        fn=uicon.capture_wrap(func=media_fetch_interface, num_result=2),
        inputs=[
            text_src_path, text_des_path,
            num_src_start, num_src_end,
        ],
        outputs=[
            text_result, audio_src,
        ]
    )


def tab_text():
    src_dir = gr.Textbox(label="Source Directory")
    des_dir = gr.Textbox(label="Destination Directory")
    file_ext = gr.Textbox(label="File Extension", value="txt")
    recursive_depth = gr.Number(label="Recursive Depth", value=0)
    buffer_size = gr.Textbox(label="Buffer Size", value="512 * 1024")
    action = gr.Dropdown(label="Action", choices=["to_utf_8", ], value="to_utf_8")
    result = gr.TextArea(label="Result")
    run = gr.Button("Text Process")
    run.click(
        text_process_interface,
        inputs=[
            src_dir, des_dir,
            file_ext, recursive_depth, buffer_size,
            action
        ],
        outputs=[result]
    )
    pass


def tab_meta_viewer(cfg):
    port = cfg.get('http', {}).get('port', 10006)
    path_base = f'http://localhost:{port}'
    with gr.Tab("Lora Meta"):
        path = f'{path_base}/kohya-meta-viewer.html'
        iframe_html = f'<iframe src="{path}" width="100%" height="600"></iframe>'
        gr.HTML(iframe_html)
    with gr.Tab("Image Meta"):
        with gr.Row():
            with gr.Column(scale=1):
                file_upload = gr.Image(label="Image", interactive=True, type="pil")
            with gr.Column(scale=2):
                meta_parameters = gr.Textbox(label="Parameters")
                meta_full = gr.Textbox(label="Full")
        with gr.Row():
            image_display = gr.Image()
        file_upload.change(
            fn=image_metadata_interface,
            inputs=[file_upload],
            outputs=[
                meta_parameters,
                meta_full,
                image_display
            ]
        )
    with gr.Tab("Image Meta Batch"):
        image_dir = gr.Textbox(label="Image Directory")
        text_remove = gr.TextArea(label="Remove")
        run_button = gr.Button("Read")
        images_df = gr.Dataframe(
            label="Images and Metadata",
            datatype="markdown",
        )
        result_text = gr.TextArea(label="Result")
        run_button.click(
            fn=image_batch_metadata_interface,
            inputs=[image_dir, text_remove],
            outputs=[result_text, images_df]
        )

    pass


def init(cfg):
    with gr.Blocks() as app:
        with gr.Tab("Image"):
            tab_image_process()

        with gr.Tab("Extract Video Sound"):
            tab_video_to_wav()

        with gr.Tab("Media Fetch"):
            tab_media_fetch()

        with gr.Tab("Media Split"):
            tab_media_split()

        with gr.Tab("Media Duration"):
            tab_media_sum_duration()

        with gr.Tab("Text"):
            tab_text()

        with gr.Tab("Metadata"):
            tab_meta_viewer(cfg)

        text_output = gr.Textbox(label="Console")

        def clear_output():
            uicon.capture_clear()
            text_output.value = '[clear]'

        clear_button = gr.Button("Clear Output")
        clear_button.click(clear_output)

    return app
