import settings
# from settings import *
import os


settings.load_settings()
# General

def get_campaign_path():
    return settings.current["game"]["campaign-dir-path"]