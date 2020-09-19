# import sys
# import os
# import threading
# import math
from typing import List, Dict

import interface_flask

import webview as wv
from webview.platforms import cef as wv_cef
# from webview.platforms import qt as wv_qt

from cefpython3 import cefpython as cef

import viewport.js_api
import viewport.bg_tasks

from settings import current

p_gui = current['window']['web-engine']
# p_gui = 'cef'
# p_gui = 'qt'
p_http_server = False
p_debug = True


window: wv.window = None
# windowThread = None
window_is_alive = False


def create_main_window(auto_load_ui: bool = True, window_name: str = "Dungeon Commander"):
    global window

    wv_cef.settings.update({
        'persist_session_cookies': True
    })

    load_addr = interface_flask.get_blank_addr()
    if auto_load_ui:
        load_addr = interface_flask.get_main_addr()

    window = wv.create_window(window_name, load_addr, js_api=js_api.JsApi())
    # window2 = wv.create_window("other_window", html="Hi Alex", js_api=js_api.JsApi())

    if p_gui != 'cef':
        if current['window']['x'] is not None:
            window.initial_x = current['window']['x']

        if current['window']['y'] is not None:
            window.initial_y = current['window']['y']

    if current['window']['width'] is not None:
        window.initial_width = current['window']['width']

    if current['window']['height'] is not None:
        window.initial_height = current['window']['height']


    window.loaded += on_loaded
    window.closing += on_window_closing
    window.closed += on_window_closed

def create_child_window():
    pass


def start_viewport():
    global p_gui, p_http_server, p_debug, window, window_is_alive
    window_is_alive = True
    wv.start(viewport.bg_tasks.background_thread, window, gui=p_gui, debug=p_debug, http_server=p_http_server)
    # wv.start(debug=p_debug, http_server=p_http_server)

def confirm_prompt(message: str):
    global window
    return window.evaluate_js(f"window.confirm(`{message}`)")
    # return window.evaluate_js(f"console.log(`{message}`);")


def on_loaded():
    # pass
    js_api.process_js_bindings()

def on_window_closing():
    current['window']['x'] = window.x
    current['window']['y'] = window.y
    current['window']['width'] = window.width
    current['window']['height'] = window.height



def on_window_closed():
    global window, window_is_alive
    window_is_alive = False


def get_cef_instance_dict() -> Dict[str, wv_cef.Browser]:
    global window, window_is_alive

    if not window_is_alive and window is not None:
        # print ("ERROR: Window is not active.")
        return {}

    if current['window']['web-engine'] != 'cef':
        print ("ERROR: Not using CEF Rendering.")
        return {}

    return window.gui.CEF.instances

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

# py.exec(`import webview as wv; import viewport; win2 = wv.create_window("other_window", html="Hi Alex", js_api=viewport.js_api.JsApi())`);
# await py.exec(`import webview as wv; `);