"""A collection of monsters. Also useful for building a list of wild
shape forms."""
from __future__ import annotations
import json

import json_class
import db
from db.tables.db_creature import *
from dungeonsheets.stats import CreatureSkill, CreatureAbility, SkillScore, AbilityScore
from dungeonsheets import char_key_order

file_extension = '.dc_creature'

type_conversions = {
    'bool': bool,
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'AbilityScore': int,
    'SkillScore': int
}

class Creature(json_class.JsonClass):
    """A monster that may be encountered when adventuring."""
    loaded_id = 0
    loaded_path = 0

    id: str = ""
    name: str = ""

    hit_dice: str = ""
    hp_current: int = 0

    strength = CreatureAbility(0)
    dexterity = CreatureAbility(0)
    constitution = CreatureAbility(0)
    intelligence = CreatureAbility(0)
    wisdom = CreatureAbility(0)
    charisma = CreatureAbility(0)

    strength_save: int = -1
    dexterity_save: int = -1
    constitution_save: int = -1
    intelligence_save: int = -1
    wisdom_save: int = -1
    charisma_save: int = -1

    acrobatics = CreatureSkill(ability='dexterity')
    animal_handling = CreatureSkill(ability='wisdom')
    arcana = CreatureSkill(ability='intelligence')
    athletics = CreatureSkill(ability='strength')
    deception = CreatureSkill(ability='charisma')
    history = CreatureSkill(ability='intelligence')
    insight = CreatureSkill(ability='wisdom')
    intimidation = CreatureSkill(ability='charisma')
    investigation = CreatureSkill(ability='intelligence')
    medicine = CreatureSkill(ability='wisdom')
    nature = CreatureSkill(ability='intelligence')
    perception = CreatureSkill(ability='wisdom')
    performance = CreatureSkill(ability='charisma')
    persuasion = CreatureSkill(ability='charisma')
    religion = CreatureSkill(ability='intelligence')
    sleight_of_hand = CreatureSkill(ability='dexterity')
    stealth = CreatureSkill(ability='dexterity')
    survival = CreatureSkill(ability='wisdom')

    actions: list = []
    alignment: str = ""
    armor_class: int = 0
    armor_desc: str = ""
    challenge_rating: float = 0.0
    condition_immunities: str = ""
    description = ""
    languages: str = ""
    senses: str = ""
    size: str = ""
    special_abilities: list = []
    speed: str = ""
    speed_json: dict = {}
    subtype: str = ""
    type: str = ""
    damage_immunities: str = ""
    damage_resistances: str = ""
    reactions: list = []
    damage_vulnerabilities: str = ""
    spells: list = []
    group: str = ""
    vulnerable: str = ""

    hand: int = 0
    intimidate: int = 0
    handling: int = 0
    ac: str = ""

    legendary_actions: list = []
    legendary_desc: str = ""

    # skills = "Perception +3, Stealth +4"
    # swim_speed = 0
    # fly_speed = 0
    # hp_max = 10

    def __init__(self):
        self.hp_current: int = 0

    @classmethod
    def load_by_id(cls, cid:str) -> Creature:
        return DB_Creature.make_instance_from_id(cid)

    @classmethod
    def generate_json_attr_tuple(cls, attr_dict):
        cls.json_attributes = tuple(attr_dict.keys()) + ("max_hp", "hp_current")

    @property
    def is_beast(self):
        is_beast = 'beast' in self.description.lower()
        return is_beast

    def load_json_viewer_dict(self, json_dict: dict, verbose=True) -> (None, Exception):
        char_props = {}

        for type_key, value in json_dict.items():
            use_type, key = type_key.split('-')[1:]
            if use_type in ('int', 'float') and value == "":
                char_props[key] = 0
            elif use_type in ('AbilityScore', 'SkillScore'):
                char_props[key] = type_conversions[use_type](value[1])
            else:
                char_props[key] = type_conversions[use_type](value)

        try:
            return self.load_dict(char_props)
        except Exception as e:
            return e

    def save_json_viewer_dict(self):
        attr_dict = self.save_dict()
        json_dict = {}

        for i in range(0, len(char_key_order.creature_order)):
            name = char_key_order.creature_order[i]
            type_key = f"{i}-{str(type(attr_dict[name]).__name__)}-{name}"

            if str(type(attr_dict[name]).__name__) in ('AbilityScore', 'SkillScore'):
                json_dict[type_key] = list(attr_dict[name])[:2]
            else:
                json_dict[type_key] = attr_dict[name]

        return json_dict


Creature.generate_json_attr_tuple(monster_attributes)
