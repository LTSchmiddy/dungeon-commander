import dungeonsheets
import json_class

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