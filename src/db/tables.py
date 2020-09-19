from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2

import db


# class Armor(db.Base):
#     __tablename__ = 'library'
#     get_id = Column(Integer, primary_key=True)

import dungeonsheets
import dungeonsheets.spells

# Python-based Data:
class DB_Spell(db.Base):
    __tablename__ = 'spell'
    """A magical spell castable by a player character."""
    id = Column(String, primary_key=True)
    level = Column(Integer, default=0)
    name = Column(String, default="Unknown spell")
    spell_desc = Column(String, default="Unknown spell")
    higher_level = Column(String, default="")
    casting_time = Column(String, default="1 action")
    casting_range = Column(String, default="60 ft")
    verbal_components = Column(Boolean, default=False)
    semantic_components = Column(Boolean, default=False)
    material_components = Column(Boolean, default=False)
    materials = Column(String, default="")
    duration = Column(String, default="instantaneous")
    ritual = Column(Boolean, default=False)
    concentration = Column(Boolean, default=False)
    magic_school = Column(String, default="")
    classes = Column(String, default="")

    @property
    def components_string(self) -> str:
        retVal = ""

        if self.verbal_components:
            retVal += "Verbal"

        if self.semantic_components:
            if retVal != "":
                retVal += ", "
            retVal += "Semantic"

        if self.material_components:
            if retVal != "":
                retVal += ", "
            retVal += "Material"

        return retVal

    @property
    def spell_object(self) -> dungeonsheets.spells.Spell:
        return dungeonsheets.spells.__dict__[self.id]

    @staticmethod
    def add_spell_class(cls: Type[dungeonsheets.spells.Spell]):

        this_spell = db.Session.query(DB_Spell).filter(DB_Spell.id == cls.get_id()).first()
        is_new = True

        if this_spell is None:
            this_spell = DB_Spell()
            this_spell.id = cls.get_id()
            is_new = True


        this_spell.name = cls.name
        this_spell.spell_desc = cls.get_desc()

        this_spell.level = cls.level
        this_spell.higher_level = ""

        this_spell.casting_time = cls.casting_time
        this_spell.casting_range = cls.casting_range


        if "V" in cls.components:
            this_spell.verbal_components = True
        if "S" in cls.components:
            this_spell.semantic_components = True
        if "M" in cls.components:
            this_spell.material_components = True

        this_spell.materials = cls.materials

        this_spell.duration = cls.duration
        this_spell.ritual = cls.ritual
        this_spell.concentration = cls._concentration
        this_spell.magic_school = cls.magic_school
        this_spell.classes = ",".join(cls.classes)

        if is_new:
            db.Session.add(this_spell)

# JSON-based Data:

class DB_Item(db.Base):
    __tablename__ = 'item'
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown DB_Item")
    item_desc = Column(String, default="Unknown DB_Item")
    rarity = Column(String, default="Standard")
    type = Column(String, default="Unknown")
    attunement = Column(String, default="")
    original_json = Column(JSON, default={})


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

        this_item.original_json = json_data

        if is_new:
            db.Session.add(this_item)


class DB_ReferenceSection(db.Base):
    __tablename__ = 'reference_section'
    id = Column(String, primary_key=True)
    name = Column(String, default="Unknown Section")
    parent = Column(String, default="Unknown Parent Section")
    index = Column(Integer, default=1)
    content = Column(String, default="CONTENT")

    original_json = Column(JSON, default={})

    manual_structure = {}

    def __str__(self):
        return self.id

    def __repr__(self):
        return '\"{:s}\"'.format(str(self))

    @property
    def content_html(self):
        out_content = self.content.replace("||", "||\n||").replace("|", "||")
        return markdown2.markdown(out_content, extras=['wiki-tables'])

    @staticmethod
    def add_json(json_data: dict):
        this_section=db.Session.query(DB_ReferenceSection).filter(DB_ReferenceSection.id == json_data["id"]).first()
        is_new = False

        if this_section is None:
            this_section = DB_ReferenceSection()
            is_new = True

        # print(json_data)

        this_section.id = json_data["id"]
        this_section.name = json_data["name"]
        this_section.parent = json_data["parent"]
        this_section.content = json_data["desc"]

        this_section.original_json = json_data

        if is_new:
            db.Session.add(this_section)

    @classmethod
    def generate_reference_structure(cls):
        for s in db.Session.query(DB_ReferenceSection).all():
            my_json = s.original_json.copy()
            my_json['desc'] = ""

            # Assume Top Level
            if s.parent not in cls.manual_structure:
                cls.manual_structure[s.parent] = {}

            index_val = len(cls.manual_structure[s.parent]) + 1
            if s.parent == s.name:
                index_val = 0

            cls.manual_structure[s.parent][f"{index_val}. {s.name}"] = my_json
            s.index = index_val

    @classmethod
    def get_sorted_reference(cls):
        return db.Session.query(DB_ReferenceSection).order_by(DB_ReferenceSection.parent, DB_ReferenceSection.index).all()




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
    original_json = Column(JSON, default={})

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
        this_item.original_json = json_data

        if is_new:
            db.Session.add(this_item)

'''
    @staticmethod
    def add_json(json_data):
        this_spell = db.Session.query(Spell).filter(Spell.get_id==json_data["get_id"]).first()
        is_new = False

        if this_spell is None:
            this_spell = Spell()
            is_new = True

        this_spell.get_id = json_data["get_id"]
        this_spell.name = json_data["name"]
        this_spell.spell_desc = json_data["get_desc"]

        this_spell.level = json_data["level_int"]
        if "higher_level" in json_data:
            this_spell.higher_level = json_data["higher_level"]

        this_spell.casting_time = json_data["casting_time"]
        this_spell.casting_range = json_data["range"]

        if "V" in json_data["components"]:
            this_spell.verbal_components = True
        if "S" in json_data["components"]:
            this_spell.semantic_components = True
        if "M" in json_data["components"]:
            this_spell.material_components = True

        if "material" in json_data:
            this_spell.materials = json_data["material"]

        this_spell.duration = json_data["duration"]
        this_spell.ritual = json_data["ritual"]
        this_spell.concentration = json_data["concentration"]
        this_spell.magic_school = json_data["school"]
        this_spell.classes = json_data["class"]

        this_spell.original_json = json_data

        if is_new:
            db.Session.add(this_spell)
'''