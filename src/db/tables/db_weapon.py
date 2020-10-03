from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db

from dungeonsheets import weapons, stats, character


class DB_Weapon(db.Base):
    __tablename__ = 'weapon'

    # Item Common
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Armor")
    cost = Column(Integer, default=0)
    weight = Column(Integer, default=0)
    description = Column(String, default="")
    rarity = Column(String, default="common")
    type = Column(String, default="Armor")

    base_class = Column(String, default="Weapon")
    improved = Column(Integer, default=0)
    ability = Column(String, default="strength")
    attack_bonus = Column(Integer, default=0)
    base_damage = Column(String, default="1d4")
    damage_bonus = Column(Integer, default=0)
    damage_type = Column(String, default="s")
    features_applied = Column(Boolean, default=False)
    is_finesse = Column(Boolean, default=False)
    properties = Column(String, default="")
    _original_json = Column(JSON, default={})

    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))


    def create_object(self, wielder: (character.Character, None) = None):
        # try:
        NewWeaponClass = stats.findattr(weapons, self.base_class)
        # except AttributeError:
        #     raise AttributeError(f'Weapon class "{weapon}" is not defined')
        weapon_ = NewWeaponClass(wielder=wielder)
        weapon_.load_dict(self._original_json)
        return weapon_

    
    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_Weapon).filter(DB_Weapon.id==json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_Weapon()
            is_new = True

        this_item.id = json_data["id"]
        this_item.name = json_data["name"]
        this_item.cost = json_data["cost"]
        this_item.weight = json_data["weight"]

        if "description" not in json_data:
            json_data["description"] = ""

        this_item.description = json_data["description"]
        this_item.rarity = json_data["rarity"]
        this_item.type = json_data["type"]

        this_item.base_class = json_data["base_class"]
        this_item.improved = json_data["improved"]
        this_item.ability = json_data["ability"]
        this_item.attack_bonus = json_data["attack_bonus"]
        this_item.base_damage = json_data["base_damage"]
        this_item.damage_bonus = json_data["damage_bonus"]
        this_item.damage_type = json_data["damage_type"]
        this_item.features_applied = json_data["features_applied"]
        this_item.is_finesse = json_data["is_finesse"]
        this_item.properties = json_data["properties"]
        this_item._original_json = json_data

        if is_new:
            db.Session.add(this_item)