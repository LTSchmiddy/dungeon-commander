import sys
import os
import threading
import time
import shutil



import webview as wv
import viewport
from viewport.js_api import cef_bindings
import interface_flask

import settings
import settings.paths
from cefpython3 import cefpython as cef
from viewport.bg_tasks import bg_startup

import string

# update_seek_bar = CallJS("update-seek-bar.js")


# cef_run_props_thread = True

def background_thread(window: wv.window):
    import db
    # cef_props_thread = threading.Thread(None, target=update_cef_properties, args=tuple([.5]))
    while viewport.get_cef_instance() is None:
        pass

    cef_props_thread = threading.Thread(None, target=update_cef_properties_thread)
    cef_bindings.declare_cef_callbacks()
    cef_props_thread.start()

    viewport.window.load_url(interface_flask.get_main_addr())

    # cef_main = viewport.get_cef_instance()
    while viewport.window_is_alive:
        time.sleep(.5)


def update_cef_properties_thread(freq: float = 0.5):
    while viewport.window_is_alive:
        cef_bindings.update_cef_properties()
        time.sleep(freq)