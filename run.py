import http
import socketserver
import threading
import time

import yaml

import webui
from scripts.common.cfg import ConfigUtil


def browser_launch(port: int):
    import webbrowser
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:{port}")


# noinspection PyUnresolvedReferences
def http_launch(port: int, directory: str):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.allow_reuse_address = True
            super().__init__(*args, directory=directory, **kwargs)

        def log_message(self, format, *args):
            # Override the log_message method to disable all logging
            pass

        def log_error(self, format, *args):
            # This will log only errors
            self.log_message(format, *args)

    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        print(f"http server: http://127.0.0.1:{port}")
        httpd.serve_forever()
    pass


def gradio_launch(global_cfg: dict):
    app = webui.init(global_cfg)
    allowed_paths = cfg_gradio.get('allowed_paths', ['/', '.'])
    app.queue().launch(
        server_port=cfg_gradio.get('port', 10005),
        show_error=True,
        debug=True,
        allowed_paths=allowed_paths,
    )


def config_load():
    with open('./config/def.yaml', mode='r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == '__main__':

    cfg_path = './config/def.yaml'
    cfg, _ = ConfigUtil.load_and_embed(cfg_path)
    cfg_http = cfg['http']
    cfg_gradio = cfg['gradio']

    ConfigUtil.store('cfg', cfg)
    ConfigUtil.store('cfg_http', cfg_http)
    ConfigUtil.store('cfg_gradio', cfg_gradio)

    port_http = cfg_http.get('port', 10006)
    port_gradio = cfg_gradio.get('port', 10005)

    if cfg_gradio.get('auto_open', True):
        threading.Thread(target=browser_launch, args=(port_gradio,)).start()

    if cfg_http.get('auto_open', True):
        threading.Thread(target=browser_launch, args=(port_http,)).start()

    http_directory = cfg_http.get('root', './page')
    if port_http >= 80:
        threading.Thread(target=http_launch, args=(port_http, http_directory)).start()

    if port_gradio >= 80:
        gradio_launch(cfg)
