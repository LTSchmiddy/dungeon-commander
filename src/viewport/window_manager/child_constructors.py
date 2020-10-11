import interface_flask

import webview as wv
from webview.platforms import cef as wv_cef
from cefpython3 import cefpython as cef

from viewport import js_api, bg_tasks, window_manager

import anon_func as af
import game

def child_editor(new_window: wv.window.Window):
    new_window.resize(900, 700)

    new_window.app_flags.append('editor')

    # new_window.loaded += af.func("", """
    #
    # """)