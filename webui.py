import gradio as gr
from PIL import Image
from PIL import ImageDraw

import ui.common.console as uicon
from scripts import util
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
):

    resize_width, resize_height = map(int, resize.split('x'))

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
            recursive_depth
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


def tab_kohya_metadata(cfg):
    port = cfg.get('http', {}).get('port', 10006)
    path = f'http://localhost:{port}/kohya-meta-viewer.html'
    iframe_html = f'<iframe src="{path}" width="100%" height="600"></iframe>'
    gr.HTML(iframe_html)
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

        with gr.Tab("Kohya Metadata"):
            tab_kohya_metadata(cfg)

        text_output = gr.Textbox(label="Console")

        def clear_output():
            uicon.capture_clear()
            text_output.value = '[clear]'

        clear_button = gr.Button("Clear Output")
        clear_button.click(clear_output)

    return app
