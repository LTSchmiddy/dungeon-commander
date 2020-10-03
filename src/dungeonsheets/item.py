from __future__ import annotations
from typing import List, Type

import dungeonsheets
import json_class

import db

class Item(json_class.JsonClass):
    id = "UnknownItem"
    name = "Unknown Item"
    cost = "0 gp"
    weight = 0
    type = "Unknown"
    rarity = "common"
    description = ""

    json_attributes = (
        "id",
        "name",
        "cost",
        "weight",
        "type",
        "rarity",
        "description"
    )
    # ['Dagger|BasicDagger']
    @staticmethod
    def related_db():
        return None

    @classmethod
    def get_from_db(cls, item_id: str):
        # print(cls.related_db())
        result: db.Base = db.Session.query(cls.related_db()).filter(
            cls.related_db().id == item_id).first()

        print(f"result = {result}")

        if result is None:
            db.Session.remove()
            return None

        if hasattr(result, 'create_object'):
            retVal = result.create_object()
            db.Session.remove()
            return retVal

        db.Session.remove()
        return None

    @classmethod
    def get_subtypes(cls) -> dict:
        retVal = {cls.__name__: cls}
        for i in cls.__subclasses__():
            retVal[str(i.__name__)] = i
            retVal.update(i.get_subtypes())
        return dict(retVal)

    @classmethod
    def save_item_list(cls, item_list: List[Item]):
        retVal = []
        for i in item_list:
            retVal.append(f"{type(i).__name__}|{i.id}")
        return retVal

    @classmethod
    def load_item_list(cls, item_list: List[str]):
        retVal = []
        type_list = cls.get_subtypes()
        for i in item_list:
            split_str = i.split('|')

            if len(split_str) < 2:
                continue

            type_str, item_id = split_str
            use_type: Type[Item] = type_list[type_str]
            # print(use_type)
            # print(item_id)

            item_obj = use_type.get_from_db(item_id)
            if item_obj is not None:
                retVal.append(item_obj)

        return retVal
