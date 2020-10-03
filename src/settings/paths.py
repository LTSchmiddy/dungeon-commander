import settings
# from settings import *

settings.load_settings()
# General

def get_campaign_path():
    return settings.current["game"]["campaign-dir-path"]

def get_global_py_addons_path():
    return settings.get_exec_path('addons/py')

def get_global_json_addons_path():
    return settings.get_exec_path('addons/json')