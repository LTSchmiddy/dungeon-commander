from __future__ import annotations
from typing import List

import db
import dungeonsheets

from game.campaign import Campaign

current: Campaign = None

def start():
    global current
    current =  Campaign()

