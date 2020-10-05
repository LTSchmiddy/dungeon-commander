"""Tools for describing a player character."""
from __future__ import annotations
__all__ = ('Character',)

import hashlib
import importlib.util
import os
import re
import subprocess
import warnings
import math
import types
import json

from typing import Any, Dict

import markdown2
import jinja2

from enum import Enum


import dungeonsheets


from dungeonsheets import (armor, background, classes, exceptions, features,
                           infusions, magic_items, monsters, race, spells,
                           weapons, char_key_order)
from dungeonsheets.armor import Armor, NoArmor, NoShield, Shield

from dungeonsheets.classes import *

from dungeonsheets.dice import read_dice_str
from dungeonsheets.features import SpellcastingAbility
from dungeonsheets.item import Item
from dungeonsheets.stats import (Ability, ArmorClass, Initiative, Skill, Speed,
                                 findattr)
from dungeonsheets.weapons import Weapon

import colors

import black

import util

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import db

# __version__ = read('../VERSION').strip()
__version__ = "dc_1"


dice_re = re.compile('(\d+)d(\d+)')

__all__ = ('Artificer', 'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk',
           'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard', )

wallet_divisors = {
    'cp': 1,
    'sp': 10,
    'ep': 50,
    'gp': 100,
    'pp': 1000,
}

type_conversions = {
    'bool': bool,
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'tuple': tuple,
    'dict': dict
}

multiclass_spellslots_by_level = {
    # char_lvl: (cantrips, 1st, 2nd, 3rd, ...)
    1:  (0, 2, 0, 0, 0, 0, 0, 0, 0, 0),
    2:  (0, 3, 0, 0, 0, 0, 0, 0, 0, 0),
    3:  (0, 4, 2, 0, 0, 0, 0, 0, 0, 0),
    4:  (0, 4, 3, 0, 0, 0, 0, 0, 0, 0),
    5:  (0, 4, 3, 2, 0, 0, 0, 0, 0, 0),
    6:  (0, 4, 3, 3, 0, 0, 0, 0, 0, 0),
    7:  (0, 4, 3, 3, 1, 0, 0, 0, 0, 0),
    8:  (0, 4, 3, 3, 2, 0, 0, 0, 0, 0),
    9:  (0, 4, 3, 3, 3, 1, 0, 0, 0, 0),
    10: (0, 4, 3, 3, 3, 2, 0, 0, 0, 0),
    11: (0, 4, 3, 3, 3, 2, 1, 0, 0, 0),
    12: (0, 4, 3, 3, 3, 2, 1, 0, 0, 0),
    13: (0, 4, 3, 3, 3, 2, 1, 1, 0, 0),
    14: (0, 4, 3, 3, 3, 2, 1, 1, 0, 0),
    15: (0, 4, 3, 3, 3, 2, 1, 1, 1, 0),
    16: (0, 4, 3, 3, 3, 2, 1, 1, 1, 0),
    17: (0, 4, 3, 3, 3, 2, 1, 1, 1, 1),
    18: (0, 4, 3, 3, 3, 3, 1, 1, 1, 1),
    19: (0, 4, 3, 3, 3, 3, 2, 1, 1, 1),
    20: (0, 4, 3, 3, 3, 3, 2, 2, 1, 1),
}

blank_str_conversions = {
    bool: False,
    int: 0,
    float: 0.0,
}

def de_stringify(value, type_str: str) -> Any:
    if type_str == 'str' or type_str not in type_conversions.keys():
        return value

    use_type = type_conversions[type_str]

    if isinstance(value, str):
        if value == "":
            return blank_str_conversions[use_type]

        return use_type(value)

    return value

file_extension = ".dc_char"

class Character:
    """A generic player character.

    """
    # General attirubtes
    name = "New Character"
    player_name = ""
    alignment = "Neutral"
    dungeonsheets_version = __version__
    class_list = list()
    _race = None
    _background = None
    xp = 0
    # Hit points
    hp_max = None
    hp_current = None
    # hp_temp = None
    # Base stats (ability scores)
    strength = Ability()
    dexterity = Ability()
    constitution = Ability()
    intelligence = Ability()
    wisdom = Ability()
    charisma = Ability()
    armor_class = ArmorClass()
    initiative = Initiative()
    speed = Speed()
    inspiration = False
    _saving_throw_proficiencies = tuple()  # use to overwrite class proficiencies
    other_weapon_proficiencies = tuple()  # add to class/race proficiencies
    skill_proficiencies = list()
    skill_expertise = list()
    languages = ""
    # Skills
    acrobatics = Skill(ability='dexterity')
    animal_handling = Skill(ability='wisdom')
    arcana = Skill(ability='intelligence')
    athletics = Skill(ability='strength')
    deception = Skill(ability='charisma')
    history = Skill(ability='intelligence')
    insight = Skill(ability='wisdom')
    intimidation = Skill(ability='charisma')
    investigation = Skill(ability='intelligence')
    medicine = Skill(ability='wisdom')
    nature = Skill(ability='intelligence')
    perception = Skill(ability='wisdom')
    performance = Skill(ability='charisma')
    persuasion = Skill(ability='charisma')
    religion = Skill(ability='intelligence')
    sleight_of_hand = Skill(ability='dexterity')
    stealth = Skill(ability='dexterity')
    survival = Skill(ability='wisdom')
    # Characteristics
    attacks_and_spellcasting = ""
    personality_traits = "TODO: Describe how your character behaves, interacts with others"
    ideals = "TODO: Describe what values your character believes in."
    bonds = "TODO: Describe your character's commitments or ongoing quests."
    flaws = "TODO: Describe your character's interesting flaws."
    features_and_traits = "Describe any other features and abilities."
    # Inventory
    cp = 0
    sp = 0
    ep = 0
    gp = 0
    pp = 0
    equipment = ""
    weapon_list = list()
    magic_items = list()
    armor = None
    shield = None
    inventory = []
    _proficiencies_text = list()
    # Magic
    spellcasting_ability = None
    _spells = list()
    _spells_prepared = list()
    infusions = list()
    # Features IN MAJOR DEVELOPMENT
    custom_features = list()
    feature_choices = list()

    _current_spellslots = {
        '1': None,
        '2': None,
        '3': None,
        '4': None,
        '5': None,
        '6': None,
        '7': None,
        '8': None,
        '9': None
    }

    # _current_spellslots = {
    #     1: None,
    #     2: None,
    #     3: None,
    #     4: None,
    #     5: None,
    #     6: None,
    #     7: None,
    #     8: None,
    #     9: None
    # }

    unique = True

    spellcasting: Dict[str, SpellcastingAbility]

    info_dict: dict
    loaded_path: str
    props_hash: str = ""
    loaded_id: int

    # last_valid_dict: (dict, None) = None

    def __init__(self, **attrs):
        # if self.last_valid_dict is None:
        #     self.last_valid_dict = {}

        self.info_dict = {}
        self.spellcasting = {}

        if not hasattr(self, 'loaded_path'):
            self.loaded_path = ""

        if not hasattr(self, 'loaded_id'):
            self.loaded_id = 0

        if 'info_dict' in attrs:
            self.info_dict.clear()
            self.info_dict.update(attrs.pop('info_dict'))

        """Takes a bunch of attrs and passes them to ``set_attrs``"""
        self.clear()
        # make sure class, race, background are set first
        my_classes = attrs.pop('classes', [])
        my_levels = attrs.pop('levels', [])
        my_subclasses = attrs.pop('subclasses', [])
        # backwards compatability
        if len(my_classes) == 0:
            if 'class' in attrs:
                my_classes = [attrs.pop('class')]
                my_levels = [attrs.pop('level', 1)]
                my_subclasses = [attrs.pop('subclass', None)]
            else:  # if no classes or levels given, default to Lvl 1 Fighter
                my_classes = ['Fighter']
                my_levels = [1]
                my_subclasses = [None]
        # Generate the list of class objects
        self.add_classes(
            my_classes, my_levels, my_subclasses,
            feature_choices=attrs.get('feature_choices', []))
        # parse race and background
        self.race = attrs.pop('race', None)
        self.background = attrs.pop('background', None)
        # parse all other attributes


        self.set_attrs(**attrs)
        self.__set_max_hp(attrs.get('hp_max', None))

        if self.hp_current is None:
            self.hp_current = self.hp_max


        # self.last_valid_dict = attrs

        # db.Session.remove()

    def clear(self):
        # reset class-definied items
        self.class_list = list()
        self.weapon_list = list()
        self.magic_items = list()
        self._saving_throw_proficiencies = tuple()
        self.other_weapon_proficiencies = tuple()
        self.skill_proficiencies = list()
        self.skill_expertise = list()
        self._proficiencies_text = list()
        self._spells = list()
        self._spells_prepared = list()
        self.infusions = list()
        self.custom_features = list()
        self.feature_choices = list()
        self.armor = None
        self.shield = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.class_name}: {self.name}>"

    def add_class(self, cls: (classes.CharClass, type, str), level: (int, str),
                  subclass=None, feature_choices=[]):
        if isinstance(cls, str):
            cls = cls.strip().title().replace(' ', '')
            try:
                cls = getattr(classes, cls)
            except AttributeError:
                raise AttributeError(
                    'class was not recognized from classes.py: {:s}'.format(cls))
        if isinstance(level, str):
            level = int(level)
        self.class_list.append(cls(level, owner=self,
                                   subclass=subclass,
                                   feature_choices=feature_choices))

    def add_classes(self, classes_list=[], levels=[], subclasses=[],
                    feature_choices=[]):
        if isinstance(classes_list, str):
            classes_list = [classes_list]
        if isinstance(levels, int) or isinstance(levels, float) or isinstance(levels, str):
            levels = [levels]
        if len(levels) == 0:
            levels = [1]*len(classes_list)
        if isinstance(subclasses, str):
            subclasses = [subclasses]
        if len(subclasses) == 0:
            subclasses = [None]*len(classes_list)
        assert len(classes_list) == len(levels), (
            'the length of classes {:d} does not match length of '
            'levels {:d}'.format(len(classes), len(levels)))
        assert len(classes_list) == len(subclasses), (
            'the length of classes {:d} does not match length of '
            'subclasses {:d}'.format(len(classes_list), len(subclasses)))
        class_list = []
        for cls, lvl, sub in zip(classes_list, levels, subclasses):
            params = {}
            params['feature_choices'] = feature_choices
            self.add_class(cls=cls, level=lvl, subclass=sub,
                           **params)

    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, newrace):
        if isinstance(newrace, race.Race):
            self._race = newrace
            self._race.owner = self
        elif isinstance(newrace, type) and issubclass(newrace, race.Race):
            self._race = newrace(owner=self)
        elif isinstance(newrace, str):
            for i in race.available_races:
                # print(i)
                if newrace in (i.get_id(), i.name):
                    self._race = i(owner=self)
                    return
            # Let's try the old way:
            try:
                self._race = findattr(race, newrace)(owner=self)

            except AttributeError:
                msg = (f'Race "{newrace}" not defined. '
                       f'Please add it to ``race.py``')
                self._race = race.Race(owner=self)
                warnings.warn(msg)
        elif newrace is None:
            self._race = race.Race(owner=self)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, bg):
        if isinstance(bg, background.Background):
            self._background = bg
            self._background.owner = self
        elif isinstance(bg, type) and issubclass(bg, background.Background):
            self._background = bg(owner=self)
        elif isinstance(bg, str):
            find_bg = util.list_get(lambda x: x.get_id() == bg, background.available_backgrounds)

            if find_bg is not None:
                self._background = find_bg(owner=self)
            else:
                try:
                    self._background = findattr(background, bg)(owner=self)
                except AttributeError:
                    msg = (f'Background "{bg}" not defined. '
                           f'Please add it to ``background.py``')
                    self._background = background.Background(owner=self)
                    warnings.warn(msg)

    @property
    def class_name(self):
        if self.num_classes >= 1:
            return self.primary_class.name
        else:
            return ""

    @property
    def classes_and_levels(self):
        return ' / '.join([f'{c.long_name} {c.level}'
                           for c in self.class_list])

    @property
    def class_names(self):
        return [c.name for c in self.class_list]

    @property
    def levels(self):
        return [c.level for c in self.class_list]

    @property
    def subclasses(self):
        return list([c.subclass or '' for c in self.class_list])

    @property
    def level(self):
        return sum(c.level for c in self.class_list)

    @level.setter
    def level(self, new_level):
        self.primary_class.level = new_level
        if self.num_classes > 1:
            warnings.warn("Unable to tell which level to set. Updating "
                          "level of primary class {:s}".format(self.primary_class.name))

    @property
    def num_classes(self):
        return len(self.class_list)

    @property
    def has_class(self):
        return (self.num_classes > 0)

    @property
    def primary_class(self):
        # for now, assume first class given must be primary class
        if self.has_class:
            return self.class_list[0]
        else:
            return None

    def __set_max_hp(self, hp_max):
        """
        Set maximum HP based on value in charlist py or calc from classes
        """
        if hp_max:
            assert isinstance(hp_max, int)
            self.hp_max = hp_max
        else:
            const_mod = self.constitution.modifier
            level_one_hp = self.primary_class.hit_dice_faces + const_mod
            self.hp_max = level_one_hp
            for char_cls in self.class_list:
                hp_per_lvl = char_cls.hit_dice_faces/2 + 1 + const_mod
                levels = char_cls.level
                if char_cls == self.primary_class:
                    levels -= 1
                assert levels >= 0
                self.hp_max += int(hp_per_lvl * levels)

    def wallet_total(self, unit: str = 'gp'):
        cp_total = self.cp + (self.sp * 10) + (self.ep * 50) + (self.gp * 100) + (self.pp * 1000)
        return cp_total / wallet_divisors[unit]


    @property
    def all_skill_proficiencies(self):
        retVal = self.skill_proficiencies[:]
        if self.race is not None:
            retVal.extend(self.race.skill_proficiencies)
        if self.background is not None:
            retVal.extend(self.background.skill_proficiencies)
        return retVal


    @property
    def weapon_proficiencies(self):
        wp = set(self.other_weapon_proficiencies)
        if self.num_classes > 0:
            wp |= set(self.primary_class.weapon_proficiencies)
        if self.num_classes > 1:
            for c in self.class_list[1:]:
                wp |= set(c.multiclass_weapon_proficiencies)
        if self.race is not None:
            wp |= set(getattr(self.race, 'weapon_proficiencies', ()))
        if self.background is not None:
            wp |= set(getattr(self.background, 'weapon_proficiencies', ()))
        for i in self.features:
            wp |= set(getattr(i, 'weapon_proficiencies', ()))
        return tuple(wp)

    @weapon_proficiencies.setter
    def weapon_proficiencies(self, new_weapons):
        self.other_weapon_proficiencies = tuple(new_weapons)

    @property
    def other_weapon_proficiencies_text(self):
        return tuple(w.name for w in self.other_weapon_proficiencies)

    @property
    def features(self):
        fts = set(self.custom_features)
        fighting_style_defined = False
        set_of_fighting_styles = {
            "Fighting Style (Archery)",
            "Fighting Style (Defense)",
            "Fighting Style (Dueling)",
            "Fighting Style (Great Weapon Fighting)",
            "Fighting Style (Protection)",
            "Fighting Style (Two-Weapon Fighting)"
        }
        for temp_feature in fts:
            fighting_style_defined = (temp_feature.name in set_of_fighting_styles)
            if fighting_style_defined:
                break

        if not self.has_class:
            return fts
        for c in self.class_list:
            fts |= set(c.features)
            for feature in fts:
                if fighting_style_defined and feature.name == 'Fighting Style (Select One)':
                    temp_feature = feature
                    fts.remove(temp_feature)
                    break
        if self.race is not None:
            fts |= set(getattr(self.race, 'features', ()))
            # some races have level-based features (Ex: Aasimar)
            if hasattr(self.race, 'features_by_level'):
                for lvl in range(1, self.level+1):
                    fts |= set(self.race.features_by_level[lvl])
        if self.background is not None:
            fts |= set(getattr(self.background, 'features', ()))

        return sorted(tuple(fts), key=(lambda x: x.name))

    @property
    def all_languages(self):
        retVal = []
        retVal.extend(self.race.languages)
        retVal.extend(self.background.languages)
        for i in self.features:
            retVal.extend(i.languages)

        return retVal

    def update_feature_info_dicts(self):
        for f in self.features:
            f.update_info_dict()

    @property
    def custom_features_text(self):
        return tuple([f.name for f in self.custom_features])

    def has_feature(self, feat):
        return any([isinstance(f, feat) for f in self.features])

    @property
    def saving_throw_proficiencies(self):
        if self.primary_class is None:
            return self._saving_throw_proficiencies
        else:
            return (self._saving_throw_proficiencies or
                    self.primary_class.saving_throw_proficiencies)

    @saving_throw_proficiencies.setter
    def saving_throw_proficiencies(self, vals):
        self._saving_throw_proficiencies = vals

    @property
    def spellcasting_classes(self):
        return [c for c in self.class_list if c.is_spellcaster]

    @property
    def spellcasting_classes_excluding_warlock(self):
        return [c for c in self.spellcasting_classes if not type(c) == classes.Warlock]

    @property
    def is_spellcaster(self):
        return (len(self.spellcasting_classes) > 0)

    def spell_slots(self, spell_level):
        warlock_slots = 0
        for c in self.spellcasting_classes:
            if type(c) is classes.Warlock:
                warlock_slots = c.spell_slots(spell_level)
        if len(self.spellcasting_classes_excluding_warlock) == 0:
            return warlock_slots
        if len(self.spellcasting_classes_excluding_warlock) == 1:
            return self.spellcasting_classes_excluding_warlock[0].spell_slots(spell_level) + warlock_slots
        else:
            if spell_level == 0:
                return sum([c.spell_slots(0)
                            for c in self.spellcasting_classes])
            else:
                # compute effective level from PHB pg 164
                eff_level = 0
                for c in self.spellcasting_classes_excluding_warlock:
                    if type(c) in [classes.Bard, classes.Cleric, classes.Druid,
                                   classes.Sorcerer, classes.Wizard]:
                        eff_level += c.level
                    elif type(c) in [classes.Paladin, classes.Ranger]:
                        eff_level += c.level // 2
                    elif type(c) in [classes.Fighter, classes.Rogue]:
                        eff_level += c.level // 3
                    elif type(c) is classes.Artificer:
                        eff_level += math.ceil(c.level / 2)
                if eff_level == 0:
                    return warlock_slots
                else:
                    return multiclass_spellslots_by_level[eff_level][spell_level] + warlock_slots

    @property
    def current_spellslots(self):
        for key, value in self._current_spellslots.items():
            if value is None:
                self._current_spellslots[str(key)] = (self.spell_slots(int(key)))

        return self._current_spellslots

    @current_spellslots.setter
    def current_spellslots(self, value: dict):
        self._current_spellslots = value

    def get_current_spellslot(self, spell_level: str) -> int:
        retVal = self._current_spellslots[str(spell_level)]
        if isinstance(retVal, int):
            return retVal

        return self.spell_slots(int(spell_level))

    def set_current_spellslot(self, spell_level: str, value: int):
        self._current_spellslots[str(spell_level)] = value

    @property
    def spells(self):
        myspells = set(self._spells) | set(self._spells_prepared)
        for f in self.features:
            myspells |= set(f.spells_known) | set(f.spells_prepared)
        for f in self.race.features:
            myspells |= set(f.spells_known) | set(f.spells_prepared)
        for c in self.spellcasting_classes:
            myspells |= set(c.spells_known) | set(c.spells_prepared)
        if self.race is not None:
            myspells |= set(self.race.spells_known) | set(self.race.spells_prepared)
        return sorted(tuple(myspells), key=(lambda x: (x.name)))

    @property
    def spells_known(self):
        myspells = set(self._spells)
        for f in self.features:
            myspells |= set(f.spells_known)
        for f in self.race.features:
            myspells |= set(f.spells_known)
        for c in self.spellcasting_classes:
            myspells |= set(c.spells_known)
        if self.race is not None:
            myspells |= set(self.race.spells_known)
        return sorted(tuple(myspells), key=(lambda x: (x.name)))

    @property
    def spells_prepared(self):
        spells = set(self._spells_prepared)
        for f in self.features:
            spells |= set(f.spells_prepared)
        for c in self.spellcasting_classes:
            spells |= set(c.spells_prepared)
        if self.race is not None:
            spells |= set(self.race.spells_prepared)
        return sorted(tuple(spells), key=(lambda x: (x.name)))

    def set_attrs(self, **attrs):
        """
        Bulk setting of attributes
        Useful for loading a character from a dictionary
        """
        for attr, val in attrs.items():
            if attr == 'dungeonsheets_version':
                pass # Maybe we'll verify this later?
            elif attr == 'weapon_list':
                if isinstance(val, str):
                    val = [val]
                # Treat weapon_list specially
                for weap in val:
                    self.wield_weapon(weap)
            elif attr == 'magic_items':
                if isinstance(val, str):
                    val = [val]
                for mitem in val:
                    new_item = db.Session.query(db.tables.DB_MagicItem).filter(db.tables.DB_MagicItem.id == mitem).first()

                    if new_item is None:
                        msg = f'Magic Item "{mitem}" not defined. Please add it to the database.'
                        warnings.warn(msg)
                    else:
                        self.magic_items.append(new_item)
                    db.Session.remove()
                    # try:
                    #     self.magic_items.append(findattr(magic_items, mitem)(owner=self))
                    # except (AttributeError):
                    #     msg = (f'Magic DB_MagicItem "{mitem}" not defined. '
                    #            f'Please add it to ``magic_items.py``')
                    #     warnings.warn(msg)
            elif attr == 'weapon_proficiencies':
                self.other_weapon_proficiencies = ()
                wps = set([findattr(weapons, w) for w in val])
                wps -= set(self.weapon_proficiencies)
                self.other_weapon_proficiencies = list(wps)
            elif attr == 'armor':
                self.wear_armor(val)
            elif attr == 'shield':
                self.wield_shield(val)
            elif attr == 'circle':
                if hasattr(self, 'Druid'):
                    self.Druid.circle = val
            elif attr == 'features':
                if isinstance(val, str):
                    val = [val]
                _features = []
                for f in val:
                    feature_dict = features.Feature.get_subtypes()
                    if f in feature_dict:
                        _features.append(feature_dict[f])
                    else:
                        try:
                            _features.append(findattr(features, f))
                        except AttributeError:
                            msg = (f'Feature "{f}" not defined. '
                                   f'Please add it to ``features.py``')
                            # create temporary feature
                            _features.append(features.create_feature(
                                name=f, source='Unknown',
                                __doc__="""Unknown Feature. Add to features.py"""))
                            warnings.warn(msg)
                self.custom_features += tuple(F(owner=self) for F in _features)
            elif (attr == 'spells') or (attr == 'spells_prepared'):
                # Create a list of actual spell objects
                _spells = []
                for spell_name in val:
                    try:
                        _spells.append(findattr(spells, spell_name))
                    except AttributeError:
                        msg = (f'Spell "{spell_name}" not defined. '
                               f'Please add it to ``spells.py``')
                        warnings.warn(msg)
                        # Create temporary spell
                        _spells.append(spells.create_spell(name=spell_name, level=9))
                        # raise AttributeError(msg)
                # Sort by name
                _spells.sort(key=lambda spell: spell.name)
                # Save list of spells to character atribute
                if attr == 'spells':
                    # Instantiate them all for the spells list
                    self._spells = tuple(S() for S in _spells)
                else:
                    # Instantiate them all for the spells list
                    self._spells_prepared = tuple(S() for S in _spells)
            elif attr == 'infusions':
                if hasattr(self, 'Artificer'):
                    _infusions = []
                    for infusion_name in val:
                        try:
                            _infusions.append(findattr(infusions, infusion_name))
                        except AttributeError:
                            msg = (f'Infusion "{infusion_name}" not defined. '
                                   f'Please add it to ``infusions.py``')
                            warnings.warn(msg)
                    _infusions.sort(key=lambda infusion: infusion.name)
                    self.infusions = tuple(i() for i in _infusions)
            else:
                if not hasattr(self, attr):
                    warnings.warn(f"Setting unknown character attribute {attr}",
                                  RuntimeWarning)
                # Lookup general attributes
                setattr(self, attr, val)

    def get_char_attr(self, item: str):
        return getattr(self, item)

    def spell_save_dc(self, class_type):
        ability_mod = getattr(self, class_type.spellcasting_ability).modifier
        return (8 + self.proficiency_bonus + ability_mod)

    def spell_attack_bonus(self, class_type):
        ability_mod = getattr(self, class_type.spellcasting_ability).modifier
        return (self.proficiency_bonus + ability_mod)

    def is_proficient(self, weapon: Weapon):
        """Is the character proficient with this item?

        Considers class proficiencies and race proficiencies.

        Parameters
        ----------
        weapon
          The weapon to be tested for proficiency.

        Returns
        -------
        Boolean: is this character proficient with this weapon?

        """
        all_proficiencies = self.weapon_proficiencies
        is_proficient = any((isinstance(weapon, W) for W in all_proficiencies))
        return is_proficient

    @property
    def proficiencies_text(self):
        final_text = ""
        all_proficiencies = tuple(self._proficiencies_text)
        if self.has_class:
            all_proficiencies += tuple(self.primary_class._proficiencies_text)
        if self.num_classes > 1:
            for c in self.class_list[1:]:
                all_proficiencies += tuple(c._multiclass_proficiencies_text)
        if self.race is not None:
            all_proficiencies += tuple(self.race.proficiencies_text)
        if self.background is not None:
            all_proficiencies += tuple(self.background.proficiencies_text)
            for i in self.background.features:
                all_proficiencies += i.proficiencies_text
        # Create a single string out of all the proficiencies
        for txt in set(all_proficiencies):
            if not final_text:
                # Capitalize the first entry
                txt = txt.capitalize()
            else:
                # Put a comma first
                txt = ", " + txt
                # Add this item to the list text
            final_text += txt
        # Add a period at the end
        final_text += '.'
        return final_text

    @property
    def features_text(self):
        s = '\n\n--'.join([f.name + ("**" if f.needs_implementation else "")
                           for f in self.features])
        if s != '':
            s = '(See Features Page)\n\n--' + s
            s += '\n\n=================\n\n'
        return s

    @property
    def magic_items_text(self):
        s = ', '.join([f.name + ("**" if f.needs_implementation else "")
                        for f in sorted(self.magic_items, key=(lambda x: x.name))])
        if s:
            s += ', '
        return s

    def wear_armor(self, new_armor):
        """Accepts a string or Armor class and replaces the current armor.

        If a string is given, then a subclass of
        :py:class:`~dungeonsheets.armor.Armor` is retrived from the
        ``armor.py`` file. Otherwise, an subclass of
        :py:class:`~dungeonsheets.armor.Armor` can be provided
        directly.

        """
        db.Session.remove()
        if new_armor not in ('', 'None', None):
            if isinstance(new_armor, armor.Armor):
                self.armor = new_armor
            else:

                armor_data: db.tables.DB_Armor = db.Session.query(db.tables.DB_Armor).filter(
                    db.tables.DB_Armor.id == new_armor).first()
                if new_armor is None:
                    print(f'Armor "{new_armor}" is not defined')
                    db.Session.remove()
                    return
                self.armor = armor_data.create_object()
                db.Session.remove()




    def wield_shield(self, shield):
        """Accepts a string or Shield class and replaces the current armor.

        If a string is given, then a subclass of
        :py:class:`~dungeonsheets.armor.Shield` is retrived from the
        ``armor.py`` file. Otherwise, an subclass of
        :py:class:`~dungeonsheets.armor.Shield` can be provided
        directly.

        """
        db.Session.remove()
        if shield not in ('', 'None', None):
            # try:
            #     NewShield = findattr(armor, shield)
            # except AttributeError:
            #     # Not a string, so just treat it as Armor
            #     NewShield = shield
            if isinstance(shield, armor.Shield):
                self.shield = shield
            else:
                shield_data: db.tables.DB_Shield = db.Session.query(db.tables.DB_Shield).filter(
                    db.tables.DB_Shield.id == shield).first()
                if shield is None:
                    print(f'Armor "{shield}" is not defined')
                    db.Session.remove()
                    return
                NewShield = shield_data.create_object()
                db.Session.remove()
                self.shield = NewShield

    def wield_weapon(self, weapon: (str, Weapon)):
        """Accepts a string and adds it to the list of wielded weapon_list.

        Parameters
        ----------
        weapon : str
          Case-insensitive string with a name of the weapon.

        """


        if isinstance(weapon, str):
            weapon_data: db.tables.DB_Weapon = db.Session.query(db.tables.DB_Weapon).filter(db.tables.DB_Weapon.id==weapon).first()
            if weapon_data is None:
                print(f'Weapon "{weapon}" is not defined')
                db.Session.remove()
                return
            weapon_ = weapon_data.create_object(self)
            db.Session.remove()
            # print(f"loaded weapon from string {weapon_}")

        # Retrieve the weapon class from the weapon_list module
        elif isinstance(weapon, weapons.Weapon):
            weapon.wielder = self
            weapon_ = weapon

        elif issubclass(weapon, weapons.Weapon):
            weapon_ = weapon(wielder=self)

        else:
            raise AttributeError(f'Weapon "{weapon}" is not defined')
        # Save it to the array


        self.weapon_list.append(weapon_)

    @property
    def inventory_typedlist(self):
        return Item.save_item_list(self.inventory)

    @inventory_typedlist.setter
    def inventory_typedlist(self, value):
        self.inventory = Item.load_item_list(value)

    def equip_inv_item(self, index):
        item = self.inventory[index]

        if isinstance(item, Weapon):
            self.wield_weapon(item)
        if isinstance(item, Shield):
            self.wield_shield(item)
        if isinstance(item, Armor):
            self.wear_armor(item)

        self.inventory.remove(item)


    @property
    def hit_dice(self):
        """What type and how many dice to use for re-gaining hit points.

        To change, set hit_dice_num and hit_dice_faces."""
        return ' + '.join([f'{c.level}d{c.hit_dice_faces}'
                           for c in self.class_list])

    @property
    def hit_dice_faces(self):
        # Not a valid function if multiclass
        if self.num_classes > 1:
            warnings.warn("hit_dice_faces is not valid for multiclass characters")
        return self.primary_class.hit_dice_faces

    @hit_dice_faces.setter
    def hit_dice_faces(self, faces):
        self.primary_class.hit_dice_faces = faces

    @property
    def proficiency_bonus(self):
        if self.level < 5:
            prof = 2
        elif 5 <= self.level < 9:
            prof = 3
        elif 9 <= self.level < 13:
            prof = 4
        elif 13 <= self.level < 17:
            prof = 5
        elif 17 <= self.level:
            prof = 6
        return prof

    def can_assume_shape(self, shape: monsters.Monster):
        return hasattr(self, 'Druid') and self.Druid.can_assume_shape(shape)

    @property
    def all_wild_shapes(self):
        if hasattr(self, 'Druid'):
            return self.Druid.all_wild_shapes
        else:
            return ()

    @property
    def wild_shapes(self):
        if hasattr(self, 'Druid'):
            return self.Druid.wild_shapes
        else:
            return ()

    @wild_shapes.setter
    def wild_shapes(self, new_shapes):
        if hasattr(self, 'Druid'):
            self.Druid.wild_shapes = new_shapes

    @property
    def infusions_text(self):
        if hasattr(self, 'Artificer'):
            return tuple([i.name for i in self.infusions])
        else:
            return ()

    @classmethod
    def load_from_code(cls, char_string) -> (Character, Exception):
        char_props = read_character_code(char_string)
        if isinstance(char_props, Exception):
            return char_props
        else:
            return cls.load_from_dict(char_props)


    @classmethod
    def load(cls, character_file) -> (Character, Exception):
        # Create a character from the character definition
        char_props = read_character_file(character_file)
        if isinstance(char_props, Exception):
            return char_props
        else:
            return cls.load_from_dict(char_props)


    @classmethod
    def load_from_dict(cls, char_props) -> (Character, Exception):
        try:
            retVal: Character = cls._load_from_dict(char_props.copy())
            return retVal
        except Exception as e:
            print(colors.color(f"ERROR: Can't generate character from attributes: {e.args}", fg='red'))
            return e

    @classmethod
    def _load_from_dict(cls, char_props) -> Character:
        classes = char_props.get('classes', [])
        # backwards compatability
        if (len(classes) == 0) and ('character_class' in char_props):
            char_props['classes'] = [char_props.pop('character_class').lower().capitalize()]
            char_props['levels'] = [str(char_props.pop('level'))]
        # Create the character with loaded properties
        char = Character(**char_props)
        return char

    @property
    def current_props_hash(self) -> str:
        # return str(hashlib.md5(str(self.save_dict()).encode()).digest())
        return str(self.save_dict())

    def update_props_hash(self):
        # self.props_hash = str(hashlib.md5(str(self.save_dict()).encode()).digest())
        self.props_hash = str(self.save_dict())


    @property
    def has_been_edited(self) -> bool:
        return self.current_props_hash != self.props_hash

    def load_into_from_code(self, char_string, verbose = True) -> (None, Exception):
        char_props = read_character_code(char_string)
        if isinstance(char_props, Exception):
            return char_props
        else:
            return self.load_into_from_dict(char_props, verbose)


    def load_into(self, character_file) -> (None, Exception):
        # Create a character from the character definition
        char_props = read_character_file(character_file)
        if isinstance(char_props, Exception):
            return char_props
        else:
            self.load_into_from_dict(char_props)
            return None


    def load_into_from_dict(self, char_props, verbose = True) -> (None, Exception):
        last_valid_dict = self.save_dict()
        try:
            self._load_into_from_dict(char_props.copy())
            return None
        except Exception as e:
            if verbose:
                print(colors.color(f"ERROR: Can't import character attributes: {e.args}", fg='red'))

            if isinstance(last_valid_dict, dict) and len(last_valid_dict) > 0:
                self._load_into_from_dict(last_valid_dict.copy())

                if verbose:
                    print(colors.color(f"Reverted to last valid version of character.", fg='yellow'))
            return e

    def _load_into_from_dict(self, char_props):
        my_classes = char_props.get('classes', [])
        # backwards compatability
        if (len(my_classes) == 0) and ('character_class' in char_props):
            char_props['classes'] = [char_props.pop('character_class').lower().capitalize()]
            char_props['levels'] = [str(char_props.pop('level'))]
        # Create the character with loaded properties
        self.__init__(**char_props)

    def load_info_json_dict(self, json_dict: dict) -> (None, Exception):
        char_props = {}

        for type_key, value in json_dict.items():
            use_type, key = type_key.split('-')[1:]
            if use_type in ('int', 'float') and value == "":
                char_props[key] = 0
            else:
                char_props[key] = type_conversions[use_type](value)

        return self.load_into_from_dict(char_props)

    def load_info_from_json(self, json_str: str) -> (None, Exception):
        result = self.load_info_json_dict(json.loads(json_str))
        if isinstance(result, Exception):
            return result
        return None

    def save_code(self, template_file='character_template.txt') -> str:
        # self.update_feature_info_dicts()
        # Create the template context
        context = dict(
            char=self
        )
        # Render the template
        src_path = os.path.join(os.path.dirname(__file__), 'forms/')
        text = jinja2.Environment(
            loader=jinja2.FileSystemLoader(src_path or './')
        ).get_template(template_file).render(context)
        # Save the file

        # Format the code with Black:
        text = black.format_file_contents(text, fast=False, mode=black.FileMode())

        return text

    def save_dict(self):
        return read_character_code(self.save_code())

    def save_json_dict(self):
        attr_dict = self.save_dict()
        json_dict = {}
        # for key, value in attr_dict.items():
        #     type_key = f"{str(type(value).__name__)}-{key}"
        #     json_dict[type_key] = value

        for i in range(0, len(char_key_order.order)):
            name = char_key_order.order[i]
            type_key = f"{i}-{str(type(attr_dict[name]).__name__)}-{name}"
            json_dict[type_key] = attr_dict[name]

        return json_dict

    def save_json(self):
        return json.dumps(self.save_json_dict(), indent=4, sort_keys=True)

    def save(self, filename, template_file='character_template.txt'):
        text = self.save_code()
        with open(filename, mode='w') as f:
            f.write(text)

    def to_pdf(self, filename=None, **kwargs):
        if filename is None:
            filename = self.loaded_path

        from dungeonsheets.make_sheets import make_sheet
        if filename.endswith('.pdf'):
            filename = filename.replace('pdf', 'py')
        make_sheet(filename, character=self,
                   flatten=kwargs.get('flatten', True))


def read_character_code(p_code: str):
    # create blank module
    module = types.ModuleType('character_module')
    # populate the module with code
    try:
        exec(p_code, module.__dict__)
        return get_char_props_from_module(module)
    except Exception as e:
        return e

def read_character_file(filename):
    char_code = open(filename, 'r').read()
    return read_character_code(char_code)

'''
def read_character_file_old(filename):
    """Create a character object from the given definition file.

    The definition file should be an importable python file, filled
    with variables describing the character.

    Parameters
    ----------
    filename : str
      The path to the file that will be imported.

    """
    # Parse the file name
    dir_, fname = os.path.split(os.path.abspath(filename))
    module_name, ext = os.path.splitext(fname)
    # if ext != '.py':
    #     raise ValueError(f"Character definition {filename} is not a python file.")
    # Check if this file contains the version string
    # version_re = re.compile('dungeonsheets_version\s*=\s*[\'"]([0-9.]+)[\'"]')
    # with open(filename, mode='r') as f:
    #     version = None
    #     for line in f:
    #         match = version_re.match(line)
    #         if match:
    #             version = match.group(1)
    #             break
    #     if version is None:
    #         # Not a valid DND character file
    #         raise exceptions.CharacterFileFormatError(
    #             f"No ``dungeonsheets_version = `` entry in `{filename}`.")
    # Import the module to extract the information
    spec = importlib.util.spec_from_file_location('module', filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Prepare a list of properties for this character
    return get_char_props_from_module(module)
'''
def get_char_props_from_module(module) -> dict:
    char_props = {}
    for prop_name in dir(module):
        if prop_name[0:2] != '__':
            char_props[prop_name] = getattr(module, prop_name)
    return char_props


# Add backwards compatability for tests
class Artificer(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Artificer']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Barbarian(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Barbarian']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Bard(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Bard']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Cleric(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Cleric']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Druid(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Druid']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Fighter(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Fighter']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Monk(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Monk']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Paladin(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Paladin']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Ranger(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Ranger']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Rogue(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Rogue']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Sorceror(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Sorcerer']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Warlock(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Warlock']
        attrs['levels'] = [level]
        super().__init__(**attrs)


class Wizard(Character):
    def __init__(self, level=1, **attrs):
        attrs['classes'] = ['Wizard']
        attrs['levels'] = [level]
        super().__init__(**attrs)
