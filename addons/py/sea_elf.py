import dungeonsheets

from dungeonsheets.features import Feature
from dungeonsheets.race import _Elf
from dungeonsheets.weapons import *


class FriendOfTheSea(Feature):
    """Using gestures and sounds, you can communicate simple ideas with any beast that has an innate swimming speed."""
    name = "Friend of the Sea"
    source = "Sea Elf"


class ChildOfTheSea(Feature):
    """You have a swimming speed of 30 feet, and you can breathe air and water."""
    name = "Child of the Sea"
    source = "Sea Elf"


class SeaElf(_Elf):
    """Sea elves fell in love with the wild beauty of the ocean in the earliest days of the multiverse. While other
    elves traveled from realm to realm, the sea elves navigated the deepest currents and explored the waters across a
    hundred worlds. Today, they live in small, hidden communities in the ocean shallows and on the Elemental Plane of
    Water"""
    name = "Sea Elf"
    constitution_bonus = 1
    weapon_proficiencies = (Spear, Trident, LightCrossbow, Net)
    languages = ("Common", "Elvish", "Aquan",)
    features = (FriendOfTheSea, ChildOfTheSea)

dungeonsheets.race.available_races += (SeaElf,)