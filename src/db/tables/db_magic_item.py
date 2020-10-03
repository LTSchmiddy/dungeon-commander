
from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db
from dungeonsheets import magic_items, stats


# JSON-based Data:
class DB_MagicItem(db.Base):
    __tablename__ = 'magic_item'
    # Item Common
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Armor")
    cost = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    description = Column(String, default="")
    rarity = Column(String, default="common")
    type = Column(String, default="Armor")

    ac_bonus = Column(Integer, default=0)
    needs_implementation = Column(Boolean, default=False)
    attunement = Column(String, default="")

    _original_json = Column(JSON, default={})


    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))

    @property
    def item_desc_html(self):
        return markdown2.markdown(self.description)

    def create_object(self):

        # except AttributeError:
        #     raise AttributeError(f'Weapon class "{weapon}" is not defined')
        item_ = magic_items.MagicItem()
        item_.load_dict(self._original_json)
        return item_

    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_MagicItem).filter(DB_MagicItem.id == json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_MagicItem()
            is_new = True

        this_item.id = json_data["id"]
        this_item.name = json_data["name"]
        this_item.cost = json_data["cost"]
        this_item.weight = json_data["weight"]
        this_item.description = json_data["description"]
        this_item.rarity = json_data["rarity"]
        this_item.type = json_data["type"]
        this_item.ac_bonus = json_data["ac_bonus"]
        this_item.needs_implementation = json_data["needs_implementation"]
        this_item.attunement = json_data["attunement"]

        this_item._original_json = json_data

        if is_new:
            db.Session.add(this_item)


#
# if not "cost" in json_data:
#     json_data["cost"] = "unknown"
#
# if not "weight" in json_data:
#     json_data["weight"] = 0
#
# if "requires-attunement" in json_data:
#     json_data['attunement'] = json_data['requires-attunement']
#     del json_data['requires-attunement']
# else:
#     json_data['attunement'] = False
#
# if not "ac_bonus" in json_data:
#     json_data["ac_bonus"] = 0
#
# if not "needs_implementation" in json_data:
#     json_data["needs_implementation"] = False