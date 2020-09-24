from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db


class DB_Weapon(db.Base):
    __tablename__ = 'weapon'
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Weapon")
    weap_class = Column(String, default="Weapon")
    ability = Column(String, default="strength")
    attack_bonus = Column(Integer, default=0)
    base_damage = Column(String, default="1d4")
    cost = Column(String, default="10 gp")
    damage_bonus = Column(Integer, default=0)
    damage_type = Column(String, default="s")
    features_applied = Column(Boolean, default=False)
    is_finesse = Column(Boolean, default=False)
    properties = Column(String, default="")
    weight = Column(Integer, default=0)
    _original_json = Column(JSON, default={})

    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))


    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_Weapon).filter(DB_Weapon.id==json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_Weapon()
            is_new = True

        this_item.id = json_data["id"]
        this_item.name = json_data["name"]
        this_item.weap_class = json_data["class"]
        this_item.ability = json_data["ability"]
        this_item.attack_bonus = json_data["attack_bonus"]
        this_item.base_damage = json_data["base_damage"]
        this_item.cost = json_data["cost"]
        this_item.damage_bonus = json_data["damage_bonus"]
        this_item.damage_type = json_data["damage_type"]
        this_item.features_applied = json_data["features_applied"]
        this_item.is_finesse = json_data["is_finesse"]
        this_item.properties = json_data["properties"]
        this_item.weight = json_data["weight"]
        this_item._original_json = json_data

        if is_new:
            db.Session.add(this_item)