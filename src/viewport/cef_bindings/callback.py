from __future__ import annotations
from cefpython3 import cefpython as cef
from viewport import browser_python_env


def cef_exec(code: str, args=None, callback: (cef.JavascriptCallback, None) = None, main_globals=True):
    if args is None:
        args = {}

    result = browser_python_env.namespaces['main'].exec(code, args, main_globals)

    if isinstance(callback, cef.JavascriptCallback):
        callback.Call(result)


def cef_ns_exec(namespace: str, code: str, args=None, callback: (cef.JavascriptCallback, None) = None,
                 main_globals=True):
    if args is None:
        args = {}

    result = browser_python_env.namespaces[namespace].exec(code, args, main_globals)

    if isinstance(callback, cef.JavascriptCallback):
        callback.Call(result)


def cef_run(code: str, p_return=None, args=None, callback: (cef.JavascriptCallback, None) = None):
    if args is None:
        args = {}

    result = browser_python_env.namespaces['main'].run(code, p_return, args)

    if isinstance(callback, cef.JavascriptCallback):
        callback.Call(result)


def cef_ns_run(namespace: str, code: str, p_return=None, args=None, callback: (cef.JavascriptCallback, None) = None):
    if args is None:
        args = {}

    result = browser_python_env.namespaces[namespace].run(code, p_return, args)

    if isinstance(callback, cef.JavascriptCallback):
        callback.Call(result)


def cef_call(attr, args=(), kwargs=None, callback: (cef.JavascriptCallback, None) = None):
    if args is None:
        args = {}

    result = browser_python_env.namespaces['main'].call(attr, args, kwargs, True)

    if isinstance(callback, cef.JavascriptCallback):
        callback.Call(result)

def cef_ns_call(namespace: str, attr, args=(), kwargs=None, callback: (cef.JavascriptCallback, None) = None):
    if args is None:
        args = {}

    result = browser_python_env.namespaces[namespace].call(attr, args, kwargs, True)

    if isinstance(callback, cef.JavascriptCallback):
        callback.Call(result)