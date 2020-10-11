from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db
from dungeonsheets import creatures
import json_class

monster_attributes = {
    'actions': list,
    'alignment': str,
    'armor_class': int,
    'armor_desc': str,
    'athletics': int,
    'challenge_rating': float,
    'charisma': int,
    'condition_immunities': str,
    'constitution': int,
    'dexterity': int,
    'hit_dice': str,
    'hit_points': int,
    'id': str,
    'intelligence': int,
    'intimidation': int,
    'languages': str,
    'legendary_actions': list,
    'legendary_desc': str,
    'name': str,
    'senses': str,
    'size': str,
    'special_abilities': list,
    'speed': str,
    'speed_json': dict,
    'strength': int,
    'subtype': str,
    'type': str,
    'wisdom': int,
    'constitution_save': int,
    'damage_immunities': str,
    'damage_resistances': str,
    'history': int,
    'intelligence_save': int,
    'perception': int,
    'reactions': list,
    'wisdom_save': int,
    'damage_vulnerabilities': str,
    'charisma_save': int,
    'deception': int,
    'dexterity_save': int,
    'performance': int,
    'persuasion': int,
    'stealth': int,
    'medicine': int,
    'religion': int,
    'spells': list,
    'group': str,
    'insight': int,
    'arcana': int,
    'nature': int,
    'strength_save': int,
    'acrobatics': int,
    'survival': int,
    'investigation': int,
    'vulnerable': str,
    'hand': int,
    'intimidate': int,
    'animal_handling': int,
    'sleight_of_hand': int,
    'handling': int,
    'ac': str,
}

# JSON-based Data:
class DB_Creature(db.Base, json_class.JsonClass):
    __tablename__ = "creature"
    id = Column(String, primary_key=True)
    # Attributes will be added at runtime.
    name = Column(String, default="")

    actions = Column(JSON, default=[])
    alignment = Column(String, default="")
    armor_class = Column(Integer, default=0)
    armor_desc = Column(String, default="")
    athletics = Column(Integer, default=0)
    challenge_rating = Column(Float, default=0.0)
    charisma = Column(Integer, default=0)
    condition_immunities = Column(String, default="")
    constitution = Column(Integer, default=0)
    dexterity = Column(Integer, default=0)
    hit_dice = Column(String, default="")
    hit_points = Column(Integer, default=0)
    intelligence = Column(Integer, default=0)
    intimidation = Column(Integer, default=0)
    languages = Column(String, default="")
    legendary_actions = Column(JSON, default=[])
    legendary_desc = Column(String, default="")
    senses = Column(String, default="")
    size = Column(String, default="")
    special_abilities = Column(JSON, default=[])
    speed = Column(String, default="")
    speed_json = Column(JSON, default={})
    strength = Column(Integer, default=0)
    subtype = Column(String, default="")
    type = Column(String, default="")
    wisdom = Column(Integer, default=0)
    constitution_save = Column(Integer, default=0)
    damage_immunities = Column(String, default="")
    damage_resistances = Column(String, default="")
    history = Column(Integer, default=0)
    intelligence_save = Column(Integer, default=0)
    perception = Column(Integer, default=0)
    reactions = Column(JSON, default=[])
    wisdom_save = Column(Integer, default=0)
    damage_vulnerabilities = Column(String, default="")
    charisma_save = Column(Integer, default=0)
    deception = Column(Integer, default=0)
    dexterity_save = Column(Integer, default=0)
    performance = Column(Integer, default=0)
    persuasion = Column(Integer, default=0)
    stealth = Column(Integer, default=0)
    medicine = Column(Integer, default=0)
    religion = Column(Integer, default=0)
    spells = Column(JSON, default=[])
    group = Column(String, default="")
    insight = Column(Integer, default=0)
    arcana = Column(Integer, default=0)
    nature = Column(Integer, default=0)
    strength_save = Column(Integer, default=0)
    acrobatics = Column(Integer, default=0)
    survival = Column(Integer, default=0)
    investigation = Column(Integer, default=0)
    vulnerable = Column(String, default="")
    hand = Column(Integer, default=0)
    intimidate = Column(Integer, default=0)
    animal_handling = Column(Integer, default=0)
    sleight_of_hand = Column(Integer, default=0)
    handling = Column(Integer, default=0)
    ac = Column(String, default="")


    @classmethod
    def generate_json_attr_tuple(cls, attr_dict):
        cls.json_attributes = tuple(attr_dict.keys())

    @classmethod
    def generate_table_definition(cls, attr_dict):
    # No longer needed, but I'll leave it here, JIC:
        for key, value in attr_dict.items():
            if key == 'id':
                continue
            setattr(cls, key, Column(db.db_type_conversions[value], primary_key=(key=='id'), default=value()))

    @staticmethod
    def add_json(json_data: dict):
        this_item = db.Session.query(DB_Creature).filter(DB_Creature.id == json_data["id"]).first()
        is_new = False

        if this_item is None:
            this_item = DB_Creature()
            is_new = True

        this_item.load_dict(json_data)

        if is_new:
            db.Session.add(this_item)

    @classmethod
    def make_instance_from_id(cls, cid:str) -> creatures.Creature:
        creature_entry: DB_Creature = db.Session.query(DB_Creature).filter(DB_Creature.id==cid).first()

        retVal = None
        if creature_entry is not None:
            retVal = creature_entry.make_instance()

        db.Session.remove()
        return retVal

    def make_instance(self) -> creatures.Creature:
        new_creature = creatures.Creature()
        new_creature.load_dict(self.save_dict())
        return new_creature


DB_Creature.generate_json_attr_tuple(monster_attributes)

