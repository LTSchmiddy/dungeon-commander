import os
import json
import anon_func as af

from typing import Type
import game

# import viewport

from viewport.js_api import JsApi
import viewport

# "".is
from viewport.js_api.modules import file, std, mod_settings, campaign


def create_api_modules(api: Type[JsApi]):
    create_base_module(api)
    file.create_files_module(api)
    std.create_std_module(api)
    mod_settings.create_settings_module(api)
    campaign.create_campaign_module(api)



def create_base_module(api: Type[JsApi]):
    # General Methods:
    def pyprint(self, msg):
        print(msg)

    def open_debug(self):
        browser = viewport.get_cef_instance()
        if browser is not None:
            browser.ShowDevTools()


    def close_debug(self):
        browser = viewport.get_cef_instance()
        if browser is not None:
            browser.CloseDevTools()

    def py_quit(self):
        viewport.window.destroy()

    def py_exec_old(self, code: str):
        exec("global retVal\n" + code)
        global retVal
        out = None
        try:
            out = retVal
        except NameError:
            return None
        retVal = None
        return out

    def py_exec(self, code: str, args=None):
        if args is None:
            args = {}
        return af.func(tuple(args.keys()), code)(*tuple(args.values()))

    api.add_attr(pyprint, 'print')
    api.add_attr(open_debug)
    api.add_attr(close_debug)
    api.add_attr(py_quit, 'quit')
    api.add_attr(py_exec, 'exec')
    api.add_attr(py_exec_old, 'exec_old')

