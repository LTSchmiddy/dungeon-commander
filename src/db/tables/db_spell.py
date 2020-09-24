from __future__ import annotations

import os
from typing import Type

from sqlalchemy import *
from sqlalchemy.orm import relationship
import markdown2
import db

import dungeonsheets
import dungeonsheets.spells

# Python-based Data:
class DB_Spell(db.Base):
    __tablename__ = 'spell'
    """A magical spell castable by a player character."""
    id = Column(String, primary_key=True)
    level = Column(Integer, default=0)
    name = Column(String, default="Unknown spell")
    description = Column(String, default="Unknown spell")
    # higher_level = Column(String, default="")
    casting_time = Column(String, default="1 action")
    range = Column(String, default="60 ft")
    verbal = Column(Boolean, default=False)
    semantic = Column(Boolean, default=False)
    material = Column(Boolean, default=False)
    materials = Column(String, default="")
    duration = Column(String, default="instantaneous")
    ritual = Column(Boolean, default=False)
    concentration = Column(Boolean, default=False)
    school = Column(String, default="")
    classes = Column(String, default="")

    @property
    def components_string(self) -> str:
        retVal = ""

        if self.verbal:
            retVal += "Verbal"

        if self.semantic:
            if retVal != "":
                retVal += ", "
            retVal += "Semantic"

        if self.material:
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
        this_spell.description = cls.get_desc()

        this_spell.level = cls.level
        # this_spell.higher_level = ""

        this_spell.casting_time = cls.casting_time
        this_spell.range = cls.casting_range


        if "V" in cls.components:
            this_spell.verbal = True
        if "S" in cls.components:
            this_spell.semantic = True
        if "M" in cls.components:
            this_spell.material = True

        this_spell.materials = cls.materials

        this_spell.duration = cls.duration
        this_spell.ritual = cls.ritual
        this_spell.concentration = cls._concentration
        this_spell.school = cls.magic_school
        this_spell.classes = ",".join(cls.classes)

        if is_new:
            db.Session.add(this_spell)
