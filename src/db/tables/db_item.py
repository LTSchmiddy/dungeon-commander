
from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db



# JSON-based Data:
class DB_Item(db.Base):
    __tablename__ = 'item'
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown DB_Item")
    item_desc = Column(String, default="Unknown DB_Item")
    rarity = Column(String, default="Standard")
    type = Column(String, default="Unknown")
    attunement = Column(String, default="")
    _original_json = Column(JSON, default={})


    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))

    @property
    def item_desc_html(self):
        return markdown2.markdown(self.item_desc)

    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_Item).filter(DB_Item.id == json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_Item()
            is_new = True

        this_item.id = json_data["id"]
        this_item.name = json_data["name"]
        this_item.item_desc = json_data["desc"]
        this_item.rarity = json_data["rarity"]
        this_item.type = json_data["type"]

        if "requires-attunement" in json_data:
            this_item.attunement = json_data["requires-attunement"]

        this_item._original_json = json_data

        if is_new:
            db.Session.add(this_item)

