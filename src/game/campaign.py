from __future__ import annotations

from collections import namedtuple
from typing import List, Dict
import os
import random

import settings
import db
import dungeonsheets
from dungeonsheets.character import Character

from json_class import JsonClass



class Campaign(JsonClass):
    json_data_filename = 'campaign.json'
    json_attributes = ['name', 'dir_path', 'max_loaded_chars']

    # Static Values:

    character_dir_name = "characters"
    player_dir_name = "characters/players"
    npc_dir_name = "characters/npcs"
    addon_dir_name = "addons"
    note_dir_name = "notes"

    # Instance Values:
    name: str
    dir_path: str
    # players: List[dungeonsheets.character.Character]
    # npcs: List[dungeonsheets.character.Character]

    max_loaded_chars = 1000
    loaded_chars: Dict[int, Character]

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

        for i in [self.player_dir_name, self.npc_dir_name, self.addon_dir_name, self.note_dir_name]:
            os.makedirs(self.get_path(i))

        self.save_json_file(self.json_data_path)

    def load_campaign(self, p_path: str = None):
        if p_path is not None:
            self.dir_path = p_path

        self.load_json_file(self.json_data_path)

    def save_campaign(self, p_path: str = None):
        if p_path is not None:
            self.dir_path = p_path

        self.save_json_file(self.json_data_path)

    @property
    def json_data_path(self):
        return self.get_path(self.json_data_filename)

    def get_path(self, p_path: str) -> str:
        return os.path.join(self.dir_path, p_path)

    def get_character_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.character_dir_name), p_path)

    def get_player_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.player_dir_name), p_path)

    def get_npc_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.player_dir_name), p_path)

    def get_addon_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.player_dir_name), p_path)

    def get_note_path(self, p_path: str) -> str:
        return os.path.join(self.get_path(self.player_dir_name), p_path)

    def get_new_ref_id(self):
        next_id = 0
        while True:
            next_id = random.randint(0, self.max_loaded_chars)
            if not next_id in self.loaded_chars:
                break
        return next_id

    def get_dir_tree(self, current_dir=None):
        if current_dir is None:
            current_dir = self.dir_path

        dir_cont = os.listdir(current_dir)

        dir_dict = {
            'path': current_dir,
            'dirs': {},
            'files': {}

        }

        for i in dir_cont:
            fullpath = os.path.join(current_dir, i).replace("\\", "/")
            # print(fullpath)

            if os.path.isfile(fullpath):
                dir_dict['files'][i] = fullpath

            elif os.path.isdir(fullpath):
                dir_dict['dirs'][i] = self.get_dir_tree(fullpath)


        return dir_dict

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
        new_id = self.get_new_ref_id()
        new_char.loaded_id = new_id

        self.loaded_chars[new_id] = new_char

    def unload_character(self, char):
        if isinstance(char, Character):
            del self.loaded_chars[char.loaded_id]
        if isinstance(char, int):
            del self.loaded_chars[char]

    def save_character(self, char, location=None):
        if isinstance(char, Character):
            char.save(char.loaded_path)

        if isinstance(char, int):
            char_obj = self.loaded_chars[char]
            char_obj.save(char_obj.loaded_path)