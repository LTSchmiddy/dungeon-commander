import sys, os, json, inspect
from typing import Any

import db
import dungeonsheets

# Python-based Data:
def load_spells():
    spell_list = []

    for key, value in dungeonsheets.spells.__dict__.items():
        if not inspect.isclass(value):
            continue

        if issubclass(value, dungeonsheets.spells.spells.Spell):
            spell_list.append(value)

    for i in spell_list:
        # print (i.__doc__)
        db.tables.DB_Spell.add_spell_class(i)


    db.Session.commit()
    db.Session.remove()
    print(len(spell_list))


# JSON-based Data:
def _load_json_dir(read_dir: str, db_add_method: Any):
    for i in os.listdir(read_dir):
        scan_file = os.path.join(read_dir, i)

        json_in = json.load(open(scan_file, 'r', encoding='utf-8'))

        db_add_method(json_in)



def load_magic_items():
    read_dir = "./data/magicitems"

    _load_json_dir(read_dir, db.tables.DB_Item.add_json)

    db.Session.commit()
    db.Session.remove()


def load_weapons():
    read_dir = "./data/weapons"

    _load_json_dir(read_dir, db.tables.DB_Weapon.add_json)

    db.Session.commit()
    db.Session.remove()


# Other Utilities:
def dump_weapons():
    weapon_list = []
    out_dir = "./data/weapons"

    for key, value in dungeonsheets.weapons.__dict__.items():
        if not inspect.isclass(value):
            continue

        if issubclass(value, dungeonsheets.weapons.Weapon):
            weapon_list.append(value)

    weapon_list.sort(key=lambda x: x.__name__)
    for i in weapon_list:
        out_dict = i.to_base_dict()
        out_path = os.path.join(out_dir, out_dict['id'] + ".json")

        out_file = open(out_path, 'w')
        json.dump(out_dict, out_file, indent=4, sort_keys=True)
        out_file.close()

if __name__ == '__main__':
    # dump_weapons()
    load_magic_items()
    load_spells()
    load_weapons()