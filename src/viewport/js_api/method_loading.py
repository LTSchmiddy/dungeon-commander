import os
import json
import anon_func as af

from typing import Type
import game

# import viewport

from viewport.js_api import JsApi
from viewport import browser_python_env
import viewport

# "".is
from viewport.js_api.modules import file, std, mod_settings, campaign


def create_api_modules(api: Type[JsApi]):
    create_base_module(api)
    create_main_code_module(api)
    create_code_module(api)
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
        viewport.main_window.destroy()

    def py_exec(self, code: str, args=None, main_globals = True):
        if args is None:
            args = {}

        if main_globals:
            # return af.func(tuple(args.keys()), code, use_globals={'game': game}.update(browser_python_env.namespaces['main'].globals))(*tuple(args.values()))
            return af.func(
                tuple(args.keys()),
                code,
                __globals=browser_python_env.namespaces['main'].globals,
                __locals=browser_python_env.namespaces['main'].locals,
                collect_locals=False
            )(*tuple(args.values()))
        else:
            return af.func(tuple(args.keys()), code)(*tuple(args.values()))

    api.add_attr(pyprint, 'print')
    api.add_attr(open_debug)
    api.add_attr(close_debug)
    api.add_attr(py_quit, 'quit')
    api.add_attr(py_exec, 'exec')

def create_code_module(api: Type[JsApi]):

    def get_new_namespace_id(self):
        return browser_python_env.get_new_namespace_id()

    def create_new_namespace(self, name="", add_main = True, global_level = True):
        return browser_python_env.create_new_namespace(name, add_main, global_level)

    def create_namespace_if_dne(self, name, add_main = True, global_level = True):
        return browser_python_env.create_namespace_if_dne(name, add_main, global_level)

    def delete_namespace(self, name):
        browser_python_env.remove_namespace(name)

    def namespace_exists(self, name):
        browser_python_env.namespace_exists(name)

    def run(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].run(*args, **kwargs)

    def fexec(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].exec(*args, **kwargs)

    def call(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].call(*args, **kwargs)

    def get_var(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].get_var(*args, **kwargs)

    def set_var(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].set_var(*args, **kwargs)

    def has_var(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].has_var(*args, **kwargs)

    def del_var(self, namespace: str, *args, **kwargs):
        return browser_python_env.namespaces[namespace].del_var(*args, **kwargs)

    def get_globals(self, namespace: str, p_vars: (list, None)=None):
        if p_vars is None: # a bad idea, usually.
            return browser_python_env.namespaces[namespace].globals

        retVal = {}
        for key, value in browser_python_env.namespaces[namespace].globals:
            if key in p_vars:
                retVal[key] = value
        return retVal

    def get_locals(self, namespace: str, p_vars: (list, None)=None):
        if p_vars is None: # a bad idea, usually.
            return browser_python_env.namespaces[namespace].locals

        retVal = {}
        for key, value in browser_python_env.namespaces[namespace].locals:
            if key in p_vars:
                retVal[key] = value
        return retVal

    def set_globals(self, namespace: str, p_vars: list):
        browser_python_env.namespaces[namespace].globals.update(p_vars)

    def set_locals(self, namespace: str, p_vars: dict):
        browser_python_env.namespaces[namespace].locals.update(p_vars)

    def list_globals(self, namespace: str):
        return list(browser_python_env.namespaces[namespace].globals.keys())

    def list_locals(self, namespace: str):
        return list(browser_python_env.namespaces[namespace].locals.keys())

    def reset(self, namespace: str):
        browser_python_env.namespaces[namespace].reset()

    api.add_module_method_list("code", [
        get_new_namespace_id,
        create_new_namespace,
        create_namespace_if_dne,
        delete_namespace,
        namespace_exists,
        run,
        fexec,
        call,
        get_var,
        set_var,
        has_var,
        del_var,
        get_locals,
        get_globals,
        set_globals,
        set_locals,
        list_globals,
        list_locals,
        reset
    ])

# Create a separate module for the main namespace, for convenience.
def create_main_code_module(api: Type[JsApi]):

    def run(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].run(*args, **kwargs)

    def fexec(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].exec(*args, **kwargs)

    def call(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].call(*args, **kwargs)

    def get_var(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].get_var(*args, **kwargs)

    def set_var(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].set_var(*args, **kwargs)

    def has_var(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].has_var(*args, **kwargs)

    def del_var(self, *args, **kwargs):
        return browser_python_env.namespaces['main'].del_var(*args, **kwargs)

    def get_globals(self, p_vars: (list, None)=None):
        # if p_vars is None: # a bad idea, usually.
        #     return browser_python_env.namespaces['main'].globals

        retVal = {}
        for key, value in browser_python_env.namespaces['main'].globals:
            if key in p_vars:
                retVal[key] = value
        return retVal

    def get_locals(self, p_vars: (list, None)=None):
        # if p_vars is None: # a bad idea, usually.
        #     return browser_python_env.namespaces['main'].locals

        retVal = {}
        for key, value in browser_python_env.namespaces['main'].locals:
            if key in p_vars:
                retVal[key] = value
        return retVal

    def set_globals(self, p_vars: list):
        browser_python_env.namespaces['main'].globals.update(p_vars)

    def set_locals(self, p_vars: dict):
        browser_python_env.namespaces['main'].locals.update(p_vars)

    def list_globals(self):
        return list(browser_python_env.namespaces['main'].globals.keys())

    def list_locals(self):
        return list(browser_python_env.namespaces['main'].locals.keys())

    def reset(self):
        browser_python_env.namespaces['main'].reset()

    def global_reset(self):
        browser_python_env.global_reset()

    api.add_module_method_list("main", [
        run,
        fexec,
        call,
        get_var,
        set_var,
        has_var,
        del_var,
        get_locals,
        get_globals,
        set_globals,
        set_locals,
        list_globals,
        list_locals,
        reset,
        global_reset
    ])