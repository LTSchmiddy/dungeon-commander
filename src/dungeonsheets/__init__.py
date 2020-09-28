__all__ = ('__version__', 'Character', 'weapons', 'features',
           'character', 'race', 'background', 'spells', 'classes')

from dungeonsheets import background, features, race, spells, weapons, addons, armor, item, magic_items
from dungeonsheets.character import Character

import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


__version__ = "dc_1"
