import sys
import os
import threading
import time
import shutil
from types import FunctionType
from typing import Dict, List, Any

import webview as wv
import viewport
import interface_flask

import anon_func as af
import settings
import settings.paths
from cefpython3 import cefpython as cef
from viewport.bg_tasks import bg_startup
import std_handler

unique_bound_properties = [
    'expose_js_function',
    'cef_exec',
    'cef_ns_exec',
    'cef_run',
    'cef_ns_run',
    'uid',
    'cef_console_init',
]

global_bound_properties = {
    # 'std_handler__main_stdout': std_handler.my_stdout.get_all,
    # 'std_handler__main_stdout_as_html': std_handler.my_stdout.get_html,
    # 'std_handler__main_stdout_updated': std_handler.my_stdout.get_html_updated,
    'wvOPEN_DIALOG': lambda: wv.OPEN_DIALOG,
    'wvFOLDER_DIALOG': lambda: wv.FOLDER_DIALOG,
    'wvSAVE_DIALOG': lambda: wv.SAVE_DIALOG
}


# If the CEF window is going to be frequently checking a property or value,
# update that value here, using the CEF api, instead of the pywebview JS Bridge.
# performs much better, and prevents a number of bugs and errors.

def update_all_on_window(window):
    global global_bound_properties

    set_unique(window, global_bound_properties)

def update_all():
    global global_bound_properties

    for uid, window in viewport.windows.items():
        if not hasattr(window, 'cef'):
            continue
        bindings: cef.JavascriptBindings = window.cef.GetJavascriptBindings()
        for key, value in global_bound_properties.items():
            bindings.SetProperty(key, value())
        bindings.Rebind()


def update_match(param: FunctionType):
    global global_bound_properties

    for uid, window in viewport.windows.items():
        bindings: cef.JavascriptBindings = window.cef.GetJavascriptBindings()
        for key, value in global_bound_properties.items():
            if param(key, value):
                bindings.SetProperty(global_bound_properties, value())
        bindings.Rebind()


def update(prop_names: List[str]):
    global global_bound_properties

    for uid, window in viewport.windows.items():
        bindings: cef.JavascriptBindings = window.cef.GetJavascriptBindings()
        for i in prop_names:
            bindings.SetProperty(global_bound_properties, global_bound_properties[i]())
        bindings.Rebind()

def set_manual(props: Dict[str, Any]):
    for uid, window in viewport.windows.items():
        bindings: cef.JavascriptBindings = window.cef.GetJavascriptBindings()
        for key, value in props:
            bindings.SetProperty(key, value)
        bindings.Rebind()


def set_unique(this_window: (wv.window.Window, cef.PyBrowser, str), functions: Dict[str, Any]):
    cef_main = None
    if isinstance(this_window, wv.window.Window):
        if hasattr(this_window, 'cef'):
            cef_main = this_window.cef
        else:
            cef_main = viewport.get_cef_instance(this_window.uid)

    elif isinstance(this_window, cef.PyBrowser):
        cef_main = this_window

    elif isinstance(this_window, str):
        cef_main = viewport.get_cef_instance(this_window)

    if cef_main is None:
        return

    bindings: cef.JavascriptBindings = cef_main.GetJavascriptBindings()
    for key, value in functions.items():
        if isinstance(value, FunctionType):
            bindings.SetFunction(key, value)
        else:
            bindings.SetProperty(key, value)
    bindings.Rebind()

__all__ = ('global_bound_properties', 'unique_bound_properties', 'update', 'update_all', 'set_unique', 'set_manual')
