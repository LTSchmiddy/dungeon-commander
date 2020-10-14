from typing import Dict

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

from webview.guilib import forced_gui_
from webview.serving import resolve_url
from webview.util import parse_api_js, interop_dll_path, parse_file_type, inject_base_uri, default_html, js_bridge_call
from webview.js import alert
from webview.js.css import disable_text_select
from webview.localization import localization
import webview as wv

WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Fix for PyCharm hints warnings
# from webview.platforms.tk_cef.browser_view import BrowserView
# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"
from . import browser_view

# def load_browser_view():
#     global BrowserView, BrowserViewCall
#
#     BrowserView = browser_view.BrowserView
#     BrowserViewCall = browser_view.BrowserViewCall

class CefFrame(tk.Frame):
    wv_browser: CEF.Browser
    browser: cef.PyBrowser
    master: browser_view.BrowserView

    def __init__(self, master):
        # self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        self.wv_browser = None
        tk.Frame.__init__(self, master)
        # self.mainframe: browser_view.BrowserView = master
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """
        self.focus_set()


    def embed_browser(self):
        # window_info = cef.WindowInfo()
        # rect = [0, 0, self.winfo_width(), self.winfo_height()]
        # window_info.SetAsChild(self.get_window_handle(), rect)
        # self.browser = cef.CreateBrowserSync(window_info,
        #                                      url="https://www.google.com/")
        self.wv_browser = CEF.create_browser_tk(self.master.window, self.get_window_handle(), None)
        self.browser = self.wv_browser.browser
        assert self.browser
        self.browser.SetClientHandler(LifespanHandler(self))
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if MAC:
            # Do not use self.winfo_id() on Mac, because of these issues:
            # 1. Window id sometimes has an invalid negative value (Issue #308).
            # 2. Even with valid window id it crashes during the call to NSView.setAutoresizingMask:
            #    https://github.com/cztomczak/cefpython/issues/309#issuecomment-661094466
            #
            # To fix it using PyObjC package to obtain window handle. If you change structure of windows then you
            # need to do modifications here as well.
            #
            # There is still one issue with this solution. Sometimes there is more than one window, for example when application
            # didn't close cleanly last time Python displays an NSAlert window asking whether to Reopen that window. In such
            # case app will crash and you will see in console:
            # > Fatal Python error: PyEval_RestoreThread: NULL tstate
            # > zsh: abort      python tkinter_.py
            # Error messages related to this: https://github.com/cztomczak/cefpython/issues/441
            #
            # There is yet another issue that might be related as well:
            # https://github.com/cztomczak/cefpython/issues/583

            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            logger.info("winfo_id={}".format(self.winfo_id()))
            # noinspection PyUnresolvedReferences
            content_view = objc.pyobjc_id(NSApp.windows()[-1].contentView())
            logger.info("content_view={}".format(content_view))
            return content_view
        elif self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        if self.master.is_alive:
            cef.MessageLoopWork()
            self.after(10, self.message_loop_work)

    def on_configure(self, _):
        pass
        # if not self.browser:
        #     self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logger.debug("CefFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logger.debug("CefFrame.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        logger.info("CefFrame.on_root_close")
        if self.browser:
            logger.debug("CloseBrowser")
            # self.browser.CloseBrowser(True)
            CEF.close_window(self.master.window.uid)
            self.clear_browser_references()
        else:
            logger.debug("tk.Frame.destroy")
            self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


class LifespanHandler(object):

    def __init__(self, tkFrame):
        self.tkFrame = tkFrame

    def OnBeforeClose(self, browser, **_):
        logger.debug("LifespanHandler.OnBeforeClose")
        self.tkFrame.quit()

class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        pass
        # if self.browser_frame.master.navigation_bar:
        #     self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())

class FocusHandler(object):
    """For focus problems see Issue #255 and Issue #535. """

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        if LINUX:
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        logger.debug("FocusHandler.OnGotFocus")
        if LINUX:
            self.browser_frame.focus_set()
