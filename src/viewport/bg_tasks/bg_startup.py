import sys
import time
import os
import shutil
import hashlib

import std_handler
std_handler.init()

import settings
import settings.paths
import webview as wv
import interface_flask
import viewport


# Sub-Methods:
def mkdir_if_missing(dir_path: str):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


