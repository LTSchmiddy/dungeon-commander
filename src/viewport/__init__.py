# import sys
# import os
# import threading
# import math
from typing import List, Dict

import interface_flask

from ansi2html import Ansi2HTMLConverter

import webview as wv
from webview.platforms import cef as wv_cef
# from webview.platforms import qt as wv_qt

from cefpython3 import cefpython as cef

import viewport.js_api
import viewport.bg_tasks
import viewport.window_manager
import viewport.cef_bindings

from settings import current
import std_handler

import anon_func as af

p_gui = current['window']['web-engine']
# p_gui = 'cef'
# p_gui = 'qt'
p_http_server = False
p_debug = False


main_window: wv.window.Window = None
window_is_alive = False

wv_cef.settings.update({
    'persist_session_cookies': True
})

# load_addr = interface_flask.get_blank_addr()
# if auto_load_ui:

windows = viewport.window_manager.WindowManager()

class HTMLStdout:
    html_converter = Ansi2HTMLConverter(inline=True)

    stream_html: str
    window: wv.window.Window

    def __init__(self, p_window: wv.window.Window):
        self.stream_html = ""
        self.window = p_window

    def write(self, data):
        if hasattr(self.window, 'js_py_console_write_stdout'):
            html_data = self.html_converter.convert(str(data), full=False)
            self.stream_html += html_data
            try:
                self.window.js_py_console_write_stdout(html_data)
            except Exception as e:
                std_handler.my_stdout.old_stdout.write(' - GUI CONSOLE GONE\n')
                std_handler.my_stdout.old_stdout.write(str(e) + "\n")
                del self.window.js_py_console_write_stdout
        else:
            std_handler.my_stdout.old_stdout.write(' - NO GUI CONSOLE\n')

    def flush(self):
        pass


def create_main_window(new_window: wv.window.Window):
    global main_window, p_gui

    if p_gui != 'cef':
        if current['window']['x'] is not None:
            new_window.initial_x = current['window']['x']

        if current['window']['y'] is not None:
            new_window.initial_y = current['window']['y']

    if current['window']['width'] is not None:
        new_window.initial_width = current['window']['width']

    if current['window']['height'] is not None:
        new_window.initial_height = current['window']['height']

    # new_console = HTMLStdout(new_window)

    def on_loaded():
        setattr(new_window, 'console',  HTMLStdout(new_window))
        std_handler.my_stdout.substreams.append(new_window.console)

        viewport.cef_bindings.set_unique(new_window, {
            "cef_console_init": af.func("", """
                new_window.console.stream_html = ""
                new_window.console.write(std_handler.my_stdout.get_all())
            """)
        })

    def on_window_closing():
        std_handler.my_stdout.substreams.remove(new_window.console)
        current['window']['x'] = new_window.x
        current['window']['y'] = new_window.y
        current['window']['width'] = new_window.width
        current['window']['height'] = new_window.height

    def on_window_closed():
        global main_window, window_is_alive
        window_is_alive = False


    new_window.loaded += on_loaded
    new_window.closing += on_window_closing
    new_window.closed += on_window_closed

    new_window.app_flags.append('editor')

    main_window = new_window



def start_viewport():
    global p_gui, p_http_server, p_debug, main_window, window_is_alive, windows
    window_is_alive = True

    load_addr = interface_flask.get_blank_addr()

    windows.new_window(load_addr, create_main_window)

    wv.start(viewport.bg_tasks.background_thread, main_window, gui=p_gui, debug=p_debug, http_server=p_http_server)
    # wv.start(debug=p_debug, http_server=p_http_server)

def confirm_prompt(message: str):
    global main_window

    return main_window.evaluate_js(f"window.confirm(`{message}`)")
    # return window.evaluate_js(f"console.log(`{message}`);")


def get_cef_instance_dict() -> Dict[str, wv_cef.Browser]:
    global main_window, window_is_alive

    if not window_is_alive and main_window is not None:
        # print ("ERROR: Window is not active.")
        return {}

    # if current['window']['web-engine'] != 'cef':
    #     print ("ERROR: Not using CEF Rendering.")
    #     return {}

    return main_window.gui.CEF.instances

def get_cef_instance_keys() -> List[str]:
    instance_dict = get_cef_instance_dict()
    return list(instance_dict.keys())


def get_cef_instance(instance_id: str = 'master') -> cef.PyBrowser:
    wv_instance = get_wv_cef_instance(instance_id)
    if wv_instance is None:
        return None

    return wv_instance.browser

def get_wv_cef_instance(instance_id: str = 'master') -> wv_cef.Browser:
    instance_dict = get_cef_instance_dict()

    if not instance_id in instance_dict:
        # print ("ERROR: CEF missing 'master' instance.")
        return None

    return instance_dict[instance_id]

def get_tk_cef_instance(instance_id: str = 'master') -> wv_cef.Browser:
    instance_dict = wv.platforms.tk_cef.BrowserView.instances

    if not instance_id in instance_dict:
        # print ("ERROR: CEF missing 'master' instance.")
        return None

    return instance_dict[instance_id]

# py.exec(`import webview as wv; import viewport; win2 = wv.create_window("other_window", html="Hi Alex", js_api=viewport.js_api.JsApi())`);
# await py.exec(`import webview as wv; `);