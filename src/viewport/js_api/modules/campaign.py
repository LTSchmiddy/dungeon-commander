import os
import json

from typing import Type

# import viewport

from viewport.js_api import JsApi
import viewport
import json_class

from dungeonsheets.character import Character, de_stringify
from dungeonsheets import dice

import util
import game

def create_campaign_module(api: Type[JsApi]):
    create_character_module(api)

    def eval_dice(self, dice_string):
        return dice.eval_dice(dice_string)

    api.add_module_method_list("campaign", [
        eval_dice
    ])


def create_character_module(api: Type[JsApi]):
    def get_loaded_characters(self):
        return list(game.current.loaded_chars.keys())

    def char_id_exists(self, char_id):
        return int(char_id) in list(game.current.loaded_chars.keys())

    def new_character(self):
        return game.current.new_character()

    def load_character(self, filepath):
        return game.current.load_character(filepath)

    def unload_character(self, filepath):
        game.current.unload_character(filepath)

    def save_character(self, filepath):
        game.current.save_character(filepath)

    def is_character_edited(self, filepath):
        return game.current.loaded_chars[int(filepath)].has_been_edited

    def get_character_text(self, char_id):
        # print(char_id)
        return game.current.loaded_chars[int(char_id)].save_code()

    def get_character_json(self, char_id):
        # print(char_id)
        return game.current.loaded_chars[int(char_id)].save_json_dict()

    def apply_character_json(self, char_id, json_dict):
        # print(char_id)
        return game.current.loaded_chars[int(char_id)].load_info_json_dict(json_dict)

    def reload_character(self, char_id):
        game.current.save_character(char_id)

    def apply_character_text(self, char_id, char_code, verbose = True):
        char = game.current.loaded_chars[int(char_id)]
        result = char.load_into_from_code(char_code, verbose)

        if isinstance(result, SyntaxError):
            print("generating syntax error dict")

            retVal = {
                'error_type' : 'syntax_error'
            }
            retVal.update(json_class.make_dict(result, [
                'filename',
                'text',
                'args',
                'msg',
                'lineno',
                'msg',
                'offset'
            ]))
            return retVal

        elif isinstance(result, Exception):
            print("generating generic error dict")

            retVal = {
                'error_type': 'syntax_error'
            }
            retVal.update(json_class.make_dict(result, [
                'args',
                'msg',
            ]))
            return retVal
        else:
            return result

    def get_char_attr(self, char_id, attr_name):
        return game.current.loaded_chars[int(char_id)].get_char_attr(attr_name)


    def set_char_attr(self, char_id, attr_name, value, type_str: str):
        use_value = de_stringify(value, type_str)
        return game.current.loaded_chars[int(char_id)].set_attrs(**{attr_name: use_value})

    def set_char_attr_raw(self, char_id, attr_name, value, type_str: str):
        use_value = de_stringify(value, type_str)
        return setattr(game.current.loaded_chars[int(char_id)], attr_name, use_value)

    def call_char_method(self, char_id, method_name, *args):
        return game.current.loaded_chars[int(char_id)].get_char_attr(method_name)(*args)

    api.add_module_method_list("campaign__character", [
        get_loaded_characters,
        char_id_exists,
        new_character,
        load_character,
        unload_character,
        save_character,
        is_character_edited,
        get_character_text,
        get_character_json,
        reload_character,
        apply_character_text,
        apply_character_json,
        get_char_attr,
        set_char_attr,
        set_char_attr_raw,
        call_char_method
    ])