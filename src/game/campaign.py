from __future__ import annotations

from collections import namedtuple
from typing import List, Dict
import os
import random
from types import ModuleType
# import hashlib
# from tkinter import filedialog

import colors

import settings
import db
import dungeonsheets
from dungeonsheets import dice
from dungeonsheets.character import Character
from dungeonsheets.creatures import Creature

from json_class import JsonClass

import util


class Campaign(JsonClass):
    json_data_filename = 'campaign.json'
    json_attributes = ('name', 'dir_path', 'max_loaded_chars', 'is_dm', "addon_load_order")

    is_dm = False
    # Static Values:

    # character_dir_name = "characters"
    player_dir_name = "players"
    npc_dir_name = "npcs"
    py_addon_dir_name = "addons/py"
    json_addon_dir_name = "addons/json"
    note_dir_name = "notes"

    # Instance Values:
    name: str
    dir_path: str
    # players: List[dungeonsheets.character.Character]
    # npcs: List[dungeonsheets.character.Character]

    max_loaded_chars = 1000
    loaded_chars: Dict[int, Character]

    max_loaded_creatures = 1000
    loaded_creatures: Dict[int, Creature]

    addon_load_order: list

    # @property

    def __init__(self, p_path: str = ""):
        # Used to prevent auto-loading
        if p_path is None:
            return

        if p_path == "":
            p_path = settings.paths.get_campaign_path()

        self.dir_path = p_path

        self.name = "New Campaign"
        self.players = []
        self.npcs = []

        self.loaded_chars = {}
        self.loaded_creatures = {}

        self.addon_load_order = []

        self.start()

    def start(self):
        if not os.path.isfile(self.json_data_path):
            self.create_new_campaign()

        else:
            self.load_campaign()


    def create_new_campaign(self, p_path: str = None):
        if p_path is not None:
            self.dir_path = p_path

        if os.path.isdir(self.dir_path) and not len(os.listdir(self.dir_path)) == 0:
            print("ERROR: This directory is not empty.")

        os.makedirs(self.dir_path)

        self.construct_campaign_directories()
        self.save_json_file(self.json_data_path)

    def construct_campaign_directories(self):
        dirs = (
            self.player_dir_name,
            self.py_addon_dir_name,
            self.json_addon_dir_name,
            self.note_dir_name
        )
        if self.is_dm:
            dirs += (self.npc_dir_name,)

        for i in dirs:

            util.mkdir_if_missing(self.get_path(i))

    def load_campaign(self, p_path: str = None):
        if p_path is not None:
            self.dir_path = p_path

        self.construct_campaign_directories()

        self.load_json_file(self.json_data_path)


        # Load global addons:
        self.load_py_addon(settings.paths.get_global_py_addons_path(), settings.current["game"]["global_py_addon_load_order"])

        # Load campaign addons:
        self.load_py_addon(self.get_py_addon_path(''), self.addon_load_order)

    def load_py_addon(self, load_path: str, load_order_list: list):
        print(f"Scanning addons in '{load_path}' and determining load order...")
        settings.scan_addon_directory(load_path, load_order_list)
        print(f"Loading addons from '{load_path}'...")
        self.load_py_addon_dir(load_path, load_order_list, dungeonsheets.addons)


    def load_py_addon_dir(self, load_path: str, load_order_list: list, parent_module):
        for i in load_order_list:
            if isinstance(i, str):
                fullpath = os.path.join(load_path, i)
                result: (Exception, None) = self.create_py_addon_module(i.replace(".py", ""), open(fullpath, 'r', encoding='utf-8').read())
                if isinstance(result, ModuleType):
                    setattr(parent_module, result.__name__, result)

                    print(f"Addon '{fullpath}' loaded successfully")

                elif isinstance(result, Exception):
                    print(f"Error loading addon '{fullpath}': {result.args}")


            elif isinstance(i, dict) and ("name" in i) and ("contents" in i):
                fullpath = os.path.join(load_path, i['name'])

                result = ModuleType(i['name'])
                setattr(parent_module, result.__name__, result)
                print(f"Module '{result.__name__}' added to '{parent_module.__name__}'")
                self.load_py_addon_dir(fullpath, i['contents'], result)

                # if 'force_default_load_order' in i and i['force_default_load_order'] == True:
                #     del i['contents']



    @staticmethod
    def create_py_addon_module(p_name: str, p_code: str) -> (ModuleType, Exception):
        # create blank module
        module = ModuleType(p_name)
        # populate the module with code
        module.__dict__.update({"addons": dungeonsheets.addons})
        try:
            exec(p_code, module.__dict__)
            return module
        except Exception as e:
            return e

    def save_campaign(self, p_path: str = None):
        if p_path is not None:
            self.dir_path = p_path

        self.save_json_file(self.json_data_path)

    @property
    def json_data_path(self):
        return self.get_path(self.json_data_filename)

    def get_path(self, p_path: str) -> str:
        return os.path.join(self.dir_path, p_path)

    def get_player_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.player_dir_name), p_path)

    def get_npc_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.npc_dir_name), p_path)

    def get_py_addon_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.py_addon_dir_name), p_path)

    def get_json_addon_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.json_addon_dir_name), p_path)

    def get_note_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.player_dir_name), p_path)

    def get_new_char_ref_id(self):
        next_id = 0
        while True:
            next_id = random.randint(0, self.max_loaded_chars)
            if not next_id in self.loaded_chars:
                break
        return next_id

    def get_new_creature_ref_id(self):
        next_id = 0
        while True:
            next_id = random.randint(0, self.max_loaded_creatures)
            if not next_id in self.loaded_creatures:
                break
        return next_id

    # Character Management
    def new_character(self):
        new_char = Character()
        new_char.loaded_path = None
        new_id = self.get_new_char_ref_id()
        new_char.loaded_id = new_id

        new_char.update_props_hash()
        self.loaded_chars[new_id] = new_char
        return new_id

    def load_character(self, c_path: str):
        if not os.path.isfile(c_path):
            print(f"ERROR: File {c_path} does not exist.")
            return

        for key, value in self.loaded_chars.items():
            if c_path == value.loaded_path:
                return

        print(c_path)
        new_char = Character.load(c_path)
        new_char.loaded_path = c_path
        # new_char.loaded_path = os.path.abspath(c_path)
        new_id = self.get_new_char_ref_id()
        new_char.loaded_id = new_id

        new_char.update_props_hash()
        self.loaded_chars[new_id] = new_char
        return new_id

    def unload_character(self, char):
        if isinstance(char, Character):
            del self.loaded_chars[char.loaded_id]
        if isinstance(char, int):
            del self.loaded_chars[char]
        if isinstance(char, str):
            del self.loaded_chars[int(char)]

    def save_character(self, p_char, location=None):
        char = None
        if isinstance(p_char, Character):
            char = p_char

        if isinstance(p_char, int):
            char = self.loaded_chars[p_char]

        if isinstance(p_char, str):
            char = self.loaded_chars[int(p_char)]

        # print(os.path.abspath(self.dir_path))
        # file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
        import viewport, webview
        if char.loaded_path is None or char.loaded_path == "":
            char.loaded_path = viewport.main_window.create_file_dialog(
                dialog_type=webview.SAVE_DIALOG,
                directory=os.path.abspath(self.dir_path),
                save_filename=char.name + dungeonsheets.character.file_extension,
                file_types = (f"Character File (*{dungeonsheets.character.file_extension})",)
                # file_types = file_types
            )

            if char.loaded_path is None or char.loaded_path == "":
                print("File save cancelled.")
                return

            if not char.loaded_path.endswith(dungeonsheets.character.file_extension):
                char.loaded_path += dungeonsheets.character.file_extension

            # char.loaded_path = os.path.abspath(char.loaded_path)

        char.save(char.loaded_path)
        char.update_props_hash()


    def reload_character(self, char):
        my_char: Character = None

        result_message: (None, str) = None

        if isinstance(char, Character):
            my_char = self.loaded_chars[char.loaded_id]
        if isinstance(char, int):
            my_char = self.loaded_chars[char]
        if isinstance(char, str):
            my_char = self.loaded_chars[int(char)]

        if my_char is None:
            print(f"ERROR: {char} not loaded")
            return

        if isinstance(char.loaded_path, str) and os.path.isfile(char.loaded_path):

            result = my_char.load_into(char.loaded_path)
            if isinstance(result, Exception):
                result_message = f"ERROR: Can't import character attributes: {result.args}"

        else:
            result_message = f"ERROR: {char.loaded_path} does not exist."

        if result_message is not None:
            print(colors.color(result_message, fg='red'))

        return result_message


    # Creature Management:
    def spawn_creature(self, creature_id):
        loaded_creature = Creature.load_by_id(creature_id)

        if loaded_creature is None:
            print(f"No such creature as id: {creature_id}")
            return

        loaded_creature.loaded_path = None
        new_id = self.get_new_char_ref_id()
        loaded_creature.loaded_id = new_id
        loaded_creature.name += f" {new_id}"
        loaded_creature.hp_current = dice.eval_dice(loaded_creature.hit_dice)

        # loaded_creature.update_props_hash()
        self.loaded_creatures[new_id] = loaded_creature
        return new_id


    def load_creature(self, c_path: str):
        if not os.path.isfile(c_path):
            print(f"ERROR: File {c_path} does not exist.")
            return

        for key, value in self.loaded_creatures.items():
            if c_path == value.loaded_path:
                return

        print(c_path)
        loaded_creature = Creature()
        loaded_creature.load_json_file(c_path)
        loaded_creature.loaded_path = c_path
        # new_char.loaded_path = os.path.abspath(c_path)
        new_id = self.get_new_char_ref_id()
        loaded_creature.loaded_id = new_id

        # loaded_creature.update_props_hash()
        self.loaded_creatures[new_id] = loaded_creature
        return new_id


    def unload_creature(self, char):
        if isinstance(char, Creature):
            del self.loaded_creatures[char.loaded_id]
        if isinstance(char, int):
            del self.loaded_creatures[char]
        if isinstance(char, str):
            del self.loaded_creatures[int(char)]


    def save_creature(self, p_creature, location=None):
        creature = None
        if isinstance(p_creature, Creature):
            creature = p_creature

        if isinstance(p_creature, int):
            creature = self.loaded_creatures[p_creature]

        if isinstance(p_creature, str):
            creature = self.loaded_creatures[int(p_creature)]

        # print(os.path.abspath(self.dir_path))
        # file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
        import viewport, webview
        if creature.loaded_path is None or creature.loaded_path == "":
            creature.loaded_path = viewport.main_window.create_file_dialog(
                dialog_type=webview.SAVE_DIALOG,
                directory=os.path.abspath(self.dir_path),
                save_filename=creature.name + dungeonsheets.creatures.file_extension,
                file_types = (f"Character File (*{dungeonsheets.creatures.file_extension})",)
                # file_types = file_types
            )

            if creature.loaded_path is None or creature.loaded_path == "":
                print("File save cancelled.")
                return

            if not creature.loaded_path.endswith(dungeonsheets.character.file_extension):
                creature.loaded_path += dungeonsheets.character.file_extension

            # char.loaded_path = os.path.abspath(char.loaded_path)

        creature.save_json_file(creature.loaded_path)
        # creature.update_props_hash()