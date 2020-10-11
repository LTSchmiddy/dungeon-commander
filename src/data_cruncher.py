import sys, os, json, inspect

from typing import Any
import importlib
import importlib.util

import db
from db import db_type_conversions
import dungeonsheets
import anon_func as af

m_fields = {}
m_conflicts = []
m_conflict_entries = []
m_ik = set()

# JSON-based Data:
def _scan_json_dir(read_dir: str, db_add_method: Any):
    ticker = 0
    for i in os.listdir(read_dir):
        scan_file = os.path.join(read_dir, i)
        # print(scan_file)
        json_in = json.load(open(scan_file, "r", encoding="utf-8"))
        # print(scan_file)
        db_add_method(json_in)



        # the_void = json.dumps(json_in, indent=4, sort_keys=True)
        # print(the_void)
        # json.dump(json_in, open(scan_file, "w", encoding="utf-8"), indent=4, sort_keys=True)
        ticker += 1
    print (ticker)


def handle_monster(p_mon: dict):
    global m_fields
    # print(p_mon)
    for key, value in p_mon.items():
        if key not in m_fields:
            m_fields[key] = set()

        m_fields[key] |= {type(value)}


def show_conflicts(p_mon: dict):
    global m_fields, m_conflicts, m_conflict_entries
    for key, value in p_mon.items():
        if not key in m_conflicts:
            continue

        if isinstance(value, str):
            try:
                p_mon[key] = int(value)
            except Exception as e:
                print(e)



def clean_field_names(p_mon: dict):
    # global m_fields, m_conflicts, m_conflict_entries, m_ik
    clean_dict = dict()
    # key: str
    for key, _value in p_mon.items():
        new_key = key.lower().strip().replace(" ", "_")
        clean_dict[new_key] = _value
        if isinstance(_value, dict):
            homogenize_fields(_value)
        elif isinstance(_value, list):
            for i in _value:
                if isinstance(i, dict):
                    homogenize_fields(i)

    p_mon.clear()
    # print(clean_dict)
    p_mon.update(clean_dict)


def homogenize_fields(p_mon: dict):
    global m_fields, m_conflicts, m_conflict_entries, m_ik
    for key, value in m_fields.items():
        if key not in p_mon:
            p_mon[key] = value[0]()

def correct_challence_ratings(p_mon: dict):
    global m_fields, m_conflicts, m_conflict_entries, m_ik
    p_mon['challenge_rating'] = float(eval(p_mon['challenge_rating']))

def load_monsters():
    global m_fields, m_conflicts, m_conflict_entries, m_ik
    read_dir = "./data/monsters"

    _scan_json_dir(read_dir, correct_challence_ratings)

    _scan_json_dir(read_dir, clean_field_names)

    _scan_json_dir(read_dir, handle_monster)

    for key, value in m_fields.items():
        if len(value) > 1:
            m_conflicts.append(key)

    if len(m_conflicts) > 0:
        _scan_json_dir(read_dir, show_conflicts)

    print("\ndb_monsters def")
    for key, value in m_fields.items():
        if key == 'id':
            continue
        vtype = list(value)[0]
        # print(f"""{key} = {vtype() if vtype != str else '""' }""")
        print(f"""{key} = Column({db_type_conversions[vtype].__name__}, default={vtype() if vtype != str else '""' })""")


    print("\nmonsters def")
    for key, value in m_fields.items():
        vtype = list(value)[0]
        # print(f"'{key}': {str(list(value)[0].__name__)},")
        print(f"""{key}: {str(vtype.__name__)} = {vtype() if vtype != str else '""' }""")


if __name__ == '__main__':
    load_monsters()