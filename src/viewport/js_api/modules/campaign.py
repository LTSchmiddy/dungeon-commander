import os
import json

from typing import Type

# import viewport

from viewport.js_api import JsApi
import viewport
import json_class

from dungeonsheets.character import Character
import game

def create_campaign_module(api: Type[JsApi]):
    create_character_module(api)


def create_character_module(api: Type[JsApi]):
    def get_loaded_characters(self):
        return list(game.current.loaded_chars.keys())

    def load_character(self, filepath):
        game.current.load_character(filepath)

    def unload_character(self, filepath):
        game.current.unload_character(filepath)

    def save_character(self, filepath):
        game.current.save_character(filepath)

    def get_character_text(self, char_id):
        print(char_id)
        return game.current.loaded_chars[int(char_id)].save_code()

    def get_character_json(self, char_id):
        print(char_id)
        return game.current.loaded_chars[int(char_id)].save_json_dict()

    def apply_character_json(self, char_id, json_dict):
        print(char_id)
        return game.current.loaded_chars[int(char_id)].load_info_json_dict(json_dict)

    def reload_character(self, char_id):
        game.current.save_character(char_id)

    def apply_character_text(self, char_id, char_code):
        char = game.current.loaded_chars[int(char_id)]
        result = char.load_into_from_code(char_code)

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

    api.add_module_method_list("campaign__character", [
        get_loaded_characters,
        load_character,
        unload_character,
        save_character,
        get_character_text,
        get_character_json,
        reload_character,
        apply_character_text,
        apply_character_json
    ])