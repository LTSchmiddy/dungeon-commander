from __future__ import annotations

from collections import namedtuple
from types import FunctionType
from typing import Dict, Tuple, Any
from queue import Queue

from cefpython3 import cefpython as cef
import ctypes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import os
import platform
import logging as _logging
from webview.platforms import cef as CEF

import webview as wv

# To prevent import issues, we're going to declare this now, and define it later:
class BrowserView: pass

from webview.platforms.tk_cef.cef_frame import CefFrame

# Fix for PyCharm hints warnings

# Platforms
# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"


# BrowserViewCall = namedtuple('BrowserViewCall', ('func', 'args', 'kwargs'))
class BrowserViewCall:
    def __init__(self, func: Any, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}

        # We're holding the function in a tuple so that... HOPEFULLY, it won't get confused about what object it's attached to.
        self.func: Tuple[FunctionType] = (func,)
        self.args: tuple = args
        self.kwargs: dict = kwargs

        self.result = Queue(1)

    def call(self):
        results = self.func[0](*self.args, **self.kwargs)
        # print('call made')
        self.result.put(results)


class BrowserView(tk.Frame):
    instances: Dict[str, BrowserView] = {}
    window: wv.window.Window
    browser_frame: CefFrame
    root: tk.Tk

    call_queue: Queue

    def __init__(self, window, root):
        self.is_alive = True
        self.instances[window.uid] = self
        self.window = window

        self.browser_frame = None
        self.root = root
        self.root.resizable(True, True)

        # Root
        # root.geometry(f"{window.initial_width}x{window.initial_height}")
        geo_string = f"{window.initial_width}x{window.initial_height}"
        print(geo_string)
        root.geometry(geo_string)
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title(window.title)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.setup_icon()
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        # self.navigation_bar = NavigationBar(self)
        # self.navigation_bar.grid(row=0, column=0,
        #                          sticky=(tk.N + tk.S + tk.E + tk.W))
        # tk.Grid.rowconfigure(self, 0, weight=0)
        # tk.Grid.columnconfigure(self, 0, weight=0)

        # CefFrame
        self.browser_frame = CefFrame(self)
        self.browser_frame.grid(row=0, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

        self.call_queue = Queue()

        # Webview Setup:
        self.closed = window.closed
        self.closing = window.closing
        self.shown = window.shown
        self.loaded = window.loaded
        self.url = window.real_url
        self.text_select = window.text_select
        self.on_top = window.on_top

        self.was_maximized = False

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            # if self.navigation_bar:
            #     height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)


    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

    def on_close(self):
        self.is_alive = False
        if self.browser_frame:
            self.browser_frame.on_root_close()
            self.browser_frame = None
        else:
            self.master.destroy()

        # during tests windows is empty for some reason. no idea why.
        if self.window in wv.windows:
            wv.windows.remove(self.window)

        self.closed.set()


    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "tkinter" + IMAGE_EXT)
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            # noinspection PyProtectedMember
            self.master.call("wm", "iconphoto", self.master._w, self.icon)

    @property
    def fullscreen(self):
        return self.root.attributes("-fullscreen")

    @fullscreen.setter
    def fullscreen(self, value):
        self.root.attributes("-fullscreen", value)

    def get_fullscreen(self):
        return self.fullscreen


    def set_fullscreen(self, value):
        self.fullscreen = value


    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen



    def state(self, newState = None):
        return self.root.wm_state(newState)



    def main_thread_call(self, func: Any, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}

        new_call = BrowserViewCall(func, args, kwargs)
        self.call_queue.put(new_call)
        return new_call.result.get()


