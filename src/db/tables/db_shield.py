from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db

from dungeonsheets import armor, stats

class DB_Shield(db.Base):
    __tablename__ = 'shield'

    # Item Common
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Shield")
    cost = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    description = Column(String, default="")
    rarity = Column(String, default="common")
    base_class = Column(String, default="Shield")
    type = Column(String, default="Shield")

    # Armor
    base_armor_class = Column(Integer, default=0)
    improved = Column(Integer, default=0)

    _original_json = Column(JSON, default={})

    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))


    def create_object(self):
        # try:
        NewShieldClass = stats.findattr(armor, self.base_class)
        # except AttributeError:
        #     raise AttributeError(f'Weapon class "{weapon}" is not defined')
        armor_ = NewShieldClass()
        armor_.load_dict(self._original_json)
        return armor_

    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_Shield).filter(DB_Shield.id==json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_Shield()
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
        this_item.improved = json_data["improved"]

        this_item._original_json = json_data

        if is_new:
            db.Session.add(this_item)