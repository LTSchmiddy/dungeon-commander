from dungeonsheets import spells, features
from util import *
from anon_func import *

from enum import Enum


class SpellLearningType(Enum):
    KNOWN = 0
    PREPARED = 1
    WIZARD = 2


class SpellcastingAbility(features.Feature):
    spellcasting_ability = "intelligence"

    class SpellLearningType(Enum):
        KNOWN = "known"
        PREPARED = "prepared"
        WIZARD = "wizard"

    spell_learning_type = SpellLearningType.KNOWN

    # owning_class: (CharClass, SubClass, None) = None
    owning_class = None

    auto_load_info_dict = False

    _default_info_dict = {
        "spells_known": [],
        "spells_prepared": []
        # 'spell_learning_type': ""
    }

    @classmethod
    def get_default_info_dict(cls):
        out_dict = cls._default_info_dict.copy()
        if cls.spell_learning_type == cls.SpellLearningType.KNOWN:
            del out_dict["spells_prepared"]

        elif cls.spell_learning_type == cls.SpellLearningType.PREPARED:
            del out_dict["spells_known"]

        return out_dict

    def __init__(self, owner=None, owning_class=None):
        self.owning_class = owning_class
        super(SpellcastingAbility, self).__init__(owner=owner)
        self.owner.spellcasting[self.get_id()] = self
        self.load_info_dict()

    def load_info_dict(self):
        # self.my_info_dict['spell_learning_type'] = self.spell_learning_type.value
        self.spells_known = ()
        self.spells_prepared = ()
        # Load spells_known
        if self.spell_learning_type != self.SpellLearningType.PREPARED:
            for i in self.my_info_dict["spells_known"]:
                new_spell = self.get_spell(i)
                if new_spell is not None and not list_contains(
                    lambda x: x.get_id() == new_spell.get_id(), self.spells_known
                ):
                    self.spells_known += (new_spell,)

        if self.spell_learning_type != self.SpellLearningType.KNOWN:
            # Load spells_prepared
            for i in self.my_info_dict["spells_prepared"]:
                new_spell = self.get_spell(i)
                if new_spell is not None and not list_contains(
                    lambda x: x.get_id() == new_spell.get_id(), self.spells_prepared
                ):
                    self.spells_prepared += (new_spell,)

        if self.spell_learning_type == self.SpellLearningType.KNOWN:
            self.spells_prepared = self.spells_known

        elif self.spell_learning_type == self.SpellLearningType.PREPARED:
            self.spells_known = self.spells_prepared

    def get_spell(self, spell_id):
        from dungeonsheets.classes import CharClass
        from dungeonsheets.classes.classes import SubClass

        spell_class = list_get(
            lambda x: x.get_id() == spell_id, spells.Spell.__subclasses__()
        )
        if spell_class is None:
            print(f"'{spell_id}' is not a valid spell id...")
            return None

        if isinstance(self.owning_class, CharClass) or isinstance(
            self.owning_class, SubClass
        ):
            return spell_class(
                self.owning_class.spellcasting_ability,
                self.owner,
                self.owning_class.name,
            )

        return None

    def update_info_dict(self):
        self.my_info_dict = self.get_default_info_dict()

        # save spells_known
        if self.spell_learning_type != self.SpellLearningType.PREPARED:
            # i: spells.Spell = None
            for i in self.spells_known:
                if i.get_id() not in self.my_info_dict["spells_known"]:
                    self.my_info_dict["spells_known"].append(i.get_id())
            print(f"Spells Known: {len(self.spells_known)}")
            print(f"Spells Known Info: {len(self.my_info_dict['spells_known'])}")

        # save spells_prepared
        if self.spell_learning_type != self.SpellLearningType.KNOWN:
            # i: spells.Spell = None
            for i in self.spells_prepared:
                if i.get_id() not in self.my_info_dict["spells_prepared"]:
                    self.my_info_dict["spells_prepared"].append(i.get_id())
            print(f"Spells Prepared: {len(self.spells_prepared)}")
            print(f"Spells Prepared Info: {len(self.my_info_dict['spells_prepared'])}")

        # print(f"Spell Dict Total: {len(self.my_info_dict['spells_known']) + len(self.my_info_dict['spells_prepared'])}")
