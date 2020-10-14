from typing import Dict

import ctypes
import threading
from queue import Queue

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import os
import platform
import logging as _logging

from cefpython3 import cefpython as cef
from webview.platforms import cef as CEF

from .browser_view import BrowserView, BrowserViewCall
from .cef_frame import CefFrame

from webview.guilib import forced_gui_
from webview.serving import resolve_url
from webview.util import parse_api_js, interop_dll_path, parse_file_type, inject_base_uri, default_html, js_bridge_call
from webview.js import alert
from webview.js.css import disable_text_select
from webview.localization import localization
import webview as wv

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"

renderer = 'tk_cef'

tk_roots: Dict[str, tk.Tk] = {}
child_queue = Queue()

def tk_master_loop(main_window: wv.window.Window):
    global tk_roots, child_queue

    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {}
    if MAC:
        settings["external_message_pump"] = True
    cef.Initialize(settings=settings)

    tk_roots[main_window.uid] = tk.Tk()
    main_app = BrowserView(main_window, tk_roots[main_window.uid])
    main_app.browser_frame.embed_browser()


    # while 'master' in BrowserView.instances.keys():
    while True:

        if not child_queue.empty():
            tk_construct_child(child_queue.get_nowait())

        for uid, app in BrowserView.instances.items():
            while not app.call_queue.empty():
                next_call: BrowserViewCall = app.call_queue.get_nowait()
                # print('attempting call')
                next_call.call()
                # print('call attempt complete')


            if app.is_alive:
                app.update()
                app.update_idletasks()


        if not main_app.is_alive:
            break


    # Once the master is closed, all of the children need to be closed as well:
    for uid, app in BrowserView.instances.items():
        if app.is_alive:
            app.destroy()

    CEF.shutdown(False)


def tk_construct_child(child_window: wv.window.Window):
    tk_roots[child_window.uid] = tk.Tk()
    child = BrowserView(child_window, tk_roots[child_window.uid])
    child.browser_frame.embed_browser()

    # child_thread = threading.Thread(None, child.mainloop, name=f'{child_window.uid} mainloop')
    # child_thread.start()

    return child
    # return child, child_thread



def create_window(window: wv.window.Window):
    global tk_roots

    if window.uid == 'master':
        tk_master_loop(window)

    else:
        child_queue.put(window)


def _get_window(uid: str) -> BrowserView:
    return BrowserView.instances[uid]

def create_file_dialog(dialog_type, directory, allow_multiple, save_filename, file_types, uid):
    return None




def set_title(title, uid):
    # def _set_title():
    #     window.Text = title

    tk_window = _get_window(uid)

    print('call created')

    return tk_window.main_thread_call(tk_window.root.title, (title,))

def show(uid):
    tk_window = _get_window(uid)
    tk_window.main_thread_call(tk_window.root.deiconify)



def hide(uid):
    tk_window = _get_window(uid)
    tk_window.main_thread_call(tk_window.root.withdraw)


def toggle_fullscreen(uid):
    tk_window = _get_window(uid)
    tk_window.main_thread_call(tk_window.toggle_fullscreen)


def set_on_top(uid, on_top):
    tk_window = _get_window(uid)
    tk_window.on_top = on_top


def resize(width, height, uid):
    tk_window = _get_window(uid)
    print('do resize')
    tk_window.main_thread_call(tk_window.root.geometry, (f"{width}x{height}",))



def move(x, y, uid):
    tk_window = _get_window(uid)
    tk_window.main_thread_call(tk_window.root.geometry, (f"+{x}+{y}",))


def minimize(uid):
    tk_window = _get_window(uid)
    tk_window.main_thread_call(tk_window.root.iconify)


def restore(uid):
    tk_window = _get_window(uid)
    tk_window.main_thread_call(tk_window.root.deiconify)


def destroy_window(uid):
    tk_window = _get_window(uid)
    # tk_window.browser_frame.browser.js_result_semaphore.release()
    tk_window.main_thread_call(tk_window.root.destroy)

def get_position(uid):
    tk_window = _get_window(uid)
    geo: str = tk_window.main_thread_call(tk_window.root.geometry)
    return int(geo.split('+')[1]), int(geo.split('+')[2])

def get_size(uid):
    tk_window = _get_window(uid)
    geo: str = tk_window.main_thread_call(tk_window.root.geometry)
    print(geo)
    return int(geo.split('x')[0]), int(geo.split('x')[1].split('+')[0])


# CEF Calls:
def evaluate_js(script, uid):
    return CEF.evaluate_js(script, uid)

def load_url(url, uid):
    window = BrowserView.instances[uid]
    window.loaded.clear()

    CEF.load_url(url, uid)

def load_html(content, base_uri, uid):
    CEF.load_html(inject_base_uri(content, base_uri), uid)


def get_current_url(uid):
    return CEF.get_current_url(uid)

