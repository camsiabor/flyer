import http
import os
import socketserver
import threading
import time

import gradio as gr
import yaml

import ui.common.console as uicon
from scripts import util
from scripts.service import image_process, video_process, net_process, text_process
from scripts.util import FileIO

cfg_gradio = {
    "port": 10005,
}

cfg_http = {
    "port": 10006,
}


@uicon.capture_wrap
def img_process_interface(
        src_dir, des_dir,
        resize,
        resize_fill_color, resize_fill_alpha,
        resize_remove_color, resize_remove_alpha, resize_remove_threshold,
        rembg_model,
        rembg_color, rembg_alpha,
        dir_depth
):
    # Convert string resize '512x512' into two integers
    resize_width, resize_height = map(int, resize.split('x'))
    # Check if directories exist, if not create
    if not os.path.exists(des_dir):
        os.makedirs(des_dir)

    if resize_fill_alpha < 0:
        resize_fill_color = ''
    else:
        resize_fill_color = resize_fill_color + hex(resize_fill_alpha)[2:].zfill(2)

    if resize_remove_alpha < 0:
        resize_remove_color = ''
    elif resize_remove_alpha == 0:
        resize_remove_color = 'auto'
    else:
        resize_remove_color = resize_remove_color + hex(resize_remove_alpha)[2:].zfill(2)

    if rembg_alpha <= 0:
        rembg_color = ''
    else:
        rembg_color = rembg_color + hex(rembg_alpha)[2:].zfill(2)

    image_process.process(
        src_dir=src_dir,
        des_dir=des_dir,
        resize_width=resize_width,
        resize_height=resize_height,
        resize_fill_color=resize_fill_color,
        resize_remove_color=resize_remove_color,
        resize_remove_threshold=resize_remove_threshold,
        rembg_model=rembg_model,
        rembg_color=rembg_color,
        recursive_depth=dir_depth,
    )
    return f"Processed images are saved in {des_dir}"


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
    with gr.Row():
        src_dir = gr.Textbox(label="Source Directory")
    with gr.Row():
        des_dir = gr.Textbox(label="Destination Directory")
    with gr.Row():
        resize = gr.Textbox(value="512x512", label="Resize (e.g., 512x512)")
        resize_fill_color = gr.ColorPicker(label="Resize Fill Color", value='#000000')
        resize_fill_alpha = gr.Slider(label="Resize Fill Alpha", value=-1, minimum=-1, maximum=255)
    with gr.Row():
        resize_remove_color = gr.ColorPicker(label="Resize Remove Color", value='#000000')
        resize_remove_alpha = gr.Slider(label="Resize Remove Alpha", value=-1, minimum=-1, maximum=255)
        resize_remove_threshold = gr.Number(label="Resize Remove Threshold", value=100)
    with gr.Row():
        rembg_model = gr.Dropdown(
            label="Remove Background Model  "
                  "| 'none' for no removing  "
                  "| first time executing takes a while  ",
            value="isnet-anime",
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
    with gr.Row():
        dir_depth = gr.Number(label="Recursive Depth", value=0)
        run_img = gr.Button("Run Image Processing")
    with gr.Row():
        result = gr.TextArea(label="Result")
    run_img.click(
        img_process_interface,
        inputs=[src_dir, des_dir,
                resize,
                resize_fill_color, resize_fill_alpha,
                resize_remove_color, resize_remove_alpha, resize_remove_threshold,
                rembg_model,
                rembg_color, rembg_alpha,
                dir_depth],
        outputs=[result]
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
        with gr.Column():
            text_src_path = gr.Textbox(label="Source Path", value="")
            text_des_path = gr.Textbox(label="Destination", value="")
            with gr.Group():
                with gr.Row():
                    num_src_start = gr.Number(value=0, label="Start (sec)")
                    num_src_end = gr.Number(value=0, label="End (sec)")
                    button_src_url = gr.Button("Fetch Source", variant="primary")
                with gr.Row():
                    text_result = gr.TextArea(label="Result")
        with gr.Column():
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


def tab_kohya_metadata():
    port = cfg_http.get('port', 10006)
    path = f'http://localhost:{port}/kohya-meta-viewer.html'
    iframe_html = f'<iframe src="{path}" width="100%" height="600"></iframe>'
    gr.HTML(iframe_html)
    pass


def webui():
    with gr.Blocks() as demo:
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
            tab_kohya_metadata()

        text_output = gr.Textbox(label="Console")

        def clear_output():
            uicon.capture_clear()
            text_output.value = '[clear]'

        clear_button = gr.Button("Clear Output")
        clear_button.click(clear_output)

    return demo


def browser_launch(port: int):
    import webbrowser
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:{port}")


def http_launch(port: int, directory: str):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"http server port: http://127.0.0.1/{port}")
        httpd.serve_forever()
    pass


def gradio_launch():
    app = webui()
    app.queue().launch(
        server_port=cfg_gradio.get('port', 10005),
        show_error=True,
        debug=True,
    )


def config_load():
    with open('./config/def.yaml', mode='r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == '__main__':

    cfg = config_load()
    cfg_http = cfg['http']
    cfg_gradio = cfg['gradio']

    port_http = cfg_http.get('port', 10006)
    port_gradio = cfg_gradio.get('port', 10005)

    if cfg_gradio.get('auto_open', True):
        threading.Thread(target=browser_launch, args=(port_gradio,)).start()

    if cfg_http.get('auto_open', True):
        threading.Thread(target=browser_launch, args=(port_http,)).start()

    http_directory = cfg_http.get('root', './page')
    threading.Thread(target=http_launch, args=(port_http, http_directory)).start()
    gradio_launch()
