from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db


class DB_Armor(db.Base):
    __tablename__ = 'armor'

    # Item Common
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Armor")
    cost = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    description = Column(String, default="")
    rarity = Column(String, default="common")
    type = Column(String, default="Armor")

    # Armor
    base_armor_class = Column(Integer, default=0)
    dexterity_mod_max = Column(Integer, default=None, nullable=True)
    strength_required = Column(Integer, default=None, nullable=True)
    stealth_disadvantage = Column(Boolean, default=False, nullable=False)


    _original_json = Column(JSON, default={})

    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))


    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_Armor).filter(DB_Armor.id==json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_Armor()
            is_new = True

        this_item.id = json_data["id"]
        this_item.name = json_data["name"]
        this_item.cost = json_data["cost"]
        this_item.weight = json_data["weight"]
        this_item.description = json_data["description"]
        this_item.rarity = json_data["rarity"]
        this_item.type = json_data["type"]

        this_item.base_class = json_data["base_class"]
        this_item.base_armor_class = json_data["base_armor_class"]
        this_item.dexterity_mod_max = json_data["dexterity_mod_max"]
        this_item.strength_required = json_data["strength_required"]
        this_item.stealth_disadvantage = json_data["stealth_disadvantage"]


        this_item._original_json = json_data

        if is_new:
            db.Session.add(this_item)