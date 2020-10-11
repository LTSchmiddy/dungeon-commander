from types import FunctionType
from typing import Dict
import interface_flask

import webview as wv
from webview.platforms import cef as wv_cef
from cefpython3 import cefpython as cef

import viewport
from viewport import js_api, bg_tasks
from viewport.cef_bindings.callback import *

from settings import current
import anon_func as af


from viewport.window_manager import child_constructors

class WindowManager(Dict[str, wv.window.Window]):
    children = child_constructors

    def new_window(
        self,
        address: str,
        asm_func: FunctionType,
        window_name: str = "Dungeon Commander",
        jsApi: js_api.JsApi = js_api.JsApi(),
        window_args: dict=None,
        asm_func_args: dict=None
    ):
        if asm_func_args is None:
            asm_func_args = {}
        if window_args is None:
            window_args = {}

        new_window: wv.window.Window = wv.create_window (
            window_name,
            interface_flask.get_addr(address),
            js_api=jsApi,
            **window_args
        )


        def _expose_js_method(bind_func: cef.JavascriptCallback, callback: (cef.JavascriptCallback, None) = None):
            setattr(new_window, f"js_{bind_func.GetFunctionName()}", lambda *args, **kwargs: bind_func.Call(*args, **kwargs))

            if isinstance(callback, cef.JavascriptCallback):
                callback.Call()

        def onshown():
            pass
            _cef = viewport.get_cef_instance(new_window.uid)
            _wv_cef = viewport.get_wv_cef_instance(new_window.uid)


            setattr(new_window, 'cef', _cef)
            setattr(new_window, 'wv_cef', _wv_cef)

            print('on_shown')
            viewport.cef_bindings.set_unique(new_window, {
                "expose_js_function": _expose_js_method,
                "cef_exec": cef_exec,
                "cef_ns_exec": cef_ns_exec,
                "cef_run": cef_run,
                "cef_ns_run": cef_ns_run,
                "cef_call": cef_call,
                "cef_ns_call": cef_ns_call,
                "uid": new_window.uid,
            })

        new_window.shown += onshown

        new_window.closed += af.func((), "del self[new_window.uid]")
        asm_func(new_window, **asm_func_args)

        setattr(new_window, 'factory', asm_func.__name__)

        self[new_window.uid] = new_window
        return new_window

    def destroy_window(self, key):
        self[key].destroy()
