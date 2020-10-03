import sys, os, json, inspect

from typing import Any
import importlib
import importlib.util

import db
import dungeonsheets


# def load_python_addon_modules(p_name: str, p_code: str):
#     # create blank module
#     module = ModuleType(p_name)
#     # populate the module with code
#     try:
#         # module.__dict__.update({'dungeonsheets': dungeonsheets})
#         exec(p_code, module.__dict__)
#         setattr(dungeonsheets.addons, module.__name__, module)
#         return None
#     except Exception as e:
#         return e
#


# Python-based Data:
def load_spells():
    spell_list = []

    for i in dungeonsheets.spells.Spell.__subclasses__():
    # for key, value in dungeonsheets.spells.__dict__.items():
        if not inspect.isclass(i):
            continue

        if issubclass(i, dungeonsheets.spells.spells.Spell):
            spell_list.append(i)

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
        # print(scan_file)
        json_in = json.load(open(scan_file, 'r', encoding='utf-8'))

        db_add_method(json_in)



def load_magic_items():
    read_dir = "./data/magicitems"

    _load_json_dir(read_dir, db.tables.DB_MagicItem.add_json)

    db.Session.commit()
    db.Session.remove()


def load_weapons():
    read_dir = "./data/weapons"

    _load_json_dir(read_dir, db.tables.DB_Weapon.add_json)

    db.Session.commit()
    db.Session.remove()

def load_reference_sections():
    read_dir = "./data/sections"

    _load_json_dir(read_dir, db.tables.DB_ReferenceSection.add_json)
    db.tables.DB_ReferenceSection.generate_reference_structure()

    db.Session.commit()
    db.Session.remove()


def load_armor():
    read_dir = "./data/armor"

    _load_json_dir(read_dir, db.tables.DB_Armor.add_json)

    db.Session.commit()
    db.Session.remove()

def load_shields():
    read_dir = "./data/shields"

    _load_json_dir(read_dir, db.tables.DB_Shield.add_json)

    db.Session.commit()
    db.Session.remove()

# Other Utilities:
def dump_weapons():
    out_dir = "./data/weapons"

    for i in dungeonsheets.weapons.all_weapons:
        out_dict = i.to_base_dict()
        out_path = os.path.join(out_dir, out_dict['id'] + ".json")

        if "description" not in out_dict:
            out_dict["description"] = ""
        out_file = open(out_path, 'w')
        json.dump(out_dict, out_file, indent=4, sort_keys=True)
        out_file.close()

def dump_armor():
    out_dir = "./data/armor"

    for i in dungeonsheets.armor.all_armors + dungeonsheets.armor.armor_types:
        out_dict = i.to_base_dict()
        out_path = os.path.join(out_dir, out_dict['id'] + ".json")

        out_file = open(out_path, 'w')
        json.dump(out_dict, out_file, indent=4, sort_keys=True)
        out_file.close()


def dump_shields():
    out_dir = "./data/shields"

    for i in dungeonsheets.armor.all_shields:
        # print(i)
        out_dict = i.to_base_dict()
        # print(out_dict)
        out_path = os.path.join(out_dir, out_dict['id'] + ".json")

        out_file = open(out_path, 'w')
        json.dump(out_dict, out_file, indent=4, sort_keys=True)
        out_file.close()



def dump_magic_items():
    read_dir = "./old_info/magicitems_old2"
    write_dir = "./data/magicitems"

    _load_json_dir(read_dir, db.tables.DB_MagicItem.add_json)

    db.Session.commit()
    db.Session.remove()

    for i in db.Session.query(db.tables.DB_MagicItem).all():
        new_json: dict = i._original_json

        new_json['id'] = new_json['id'].replace("_", " ").title().replace(" ", "")
        new_json['cost'] = "0 gb"

        out_path = os.path.join(write_dir, new_json['id'] + ".json")
        out_file = open(out_path, 'w')
        json.dump(new_json, out_file, indent=4, sort_keys=True)
        out_file.close()


def load_all():
    load_magic_items()
    load_spells()
    load_weapons()
    load_armor()
    load_shields()
    load_reference_sections()

if __name__ == '__main__':
    db.init()
    dump_weapons()
    dump_armor()
    dump_shields()
    # dump_magic_items()
