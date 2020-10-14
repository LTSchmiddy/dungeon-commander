import logging
import os
import platform

from webview.util import WebViewException

logger = logging.getLogger('pywebview')
guilib = None
forced_gui_ = None

def initialize(forced_gui=None):
    def import_tk_cef():
        global guilib

        try:
            import webview.platforms.tk_cef as guilib
            logger.debug('Using TK_CEF')
            print('Using TK_CEF')

            return True
        except (ImportError, ValueError) as e:
            logger.exception('TK_CEF cannot be loaded')
            print('TK_CEF cannot be loaded')

            return False

    def import_gtk():
        global guilib

        try:
            import webview.platforms.gtk as guilib
            logger.debug('Using GTK')
            print('Using GTK')

            return True
        except (ImportError, ValueError) as e:
            logger.exception('GTK cannot be loaded')
            print('GTK cannot be loaded')

            return False

    def import_qt():
        global guilib

        try:
            import webview.platforms.qt as guilib

            return True
        except ImportError as e:
            logger.exception('QT cannot be loaded')
            print('QT cannot be loaded')
            return False

    def import_cocoa():
        global guilib

        try:
            import webview.platforms.cocoa as guilib

            return True
        except ImportError:
            logger.exception('PyObjC cannot be loaded')

            return False

    def import_winforms():
        global guilib

        try:
            import webview.platforms.winforms as guilib
            return True
        except ImportError as e:
            logger.exception('pythonnet cannot be loaded')
            return False

    def try_import(guis):
        while guis:
            import_func = guis.pop(0)

            if import_func():
                return True

        return False

    global forced_gui_

    if not forced_gui:
        forced_gui = 'qt' if 'KDE_FULL_SESSION' in os.environ else None
        forced_gui = os.environ['PYWEBVIEW_GUI'].lower() \
            if 'PYWEBVIEW_GUI' in os.environ and os.environ['PYWEBVIEW_GUI'].lower() in ['qt', 'gtk', 'cef', 'mshtml'] \
            else None

    forced_gui_ = forced_gui

    if platform.system() == 'Darwin':
        if forced_gui == 'tk_cef':
            guis = [import_tk_cef, import_cocoa, import_qt]
        elif forced_gui == 'qt':
            guis = [import_qt, import_tk_cef, import_cocoa]
        else:
            guis = [import_cocoa, import_tk_cef, import_qt]

        if not try_import(guis):
            raise WebViewException('You must have cefpython3, PyObjC (for Cocoa support), or Qt with Python bindings installed in order to use pywebview.')

    elif platform.system() == 'Linux' or platform.system() == 'OpenBSD':
        if forced_gui == 'tk_cef':
            guis = [import_tk_cef, import_gtk, import_qt]
        elif forced_gui == 'qt':
            guis = [import_qt, import_tk_cef, import_gtk]
        else:
            guis = [import_gtk, import_tk_cef,import_qt]

        if not try_import(guis):
            raise WebViewException('You must have cefpython3, QT, or GTK with Python extensions installed in order to use pywebview.')

    elif platform.system() == 'Windows':
        if forced_gui == 'tk_cef':
            guis = [import_tk_cef, import_qt, import_winforms]
        elif forced_gui == 'qt':
            guis = [import_qt, import_winforms, import_tk_cef]
        else:
            guis = [import_winforms, import_tk_cef, import_qt]

        if not try_import(guis):
            raise WebViewException('You must have pythonnet, cefpython3, or QT installed in order to use pywebview.')
    else:
        raise WebViewException('Unsupported platform. Only Windows, Linux, OS X, OpenBSD are supported.')

    return guilib
