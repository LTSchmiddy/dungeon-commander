from __future__ import annotations
from typing import List

import db
import dungeonsheets


class Campaign:
    campaign_path: str

    players: List[dungeonsheets.character.Character]
    npcs: List[dungeonsheets.character.Character]
