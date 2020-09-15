import inspect

from dungeonsheets.features.artificer import *
from dungeonsheets.features.backgrounds import *
from dungeonsheets.features.barbarian import *
from dungeonsheets.features.bard import *
from dungeonsheets.features.cleric import *
from dungeonsheets.features.druid import *
from dungeonsheets.features.feats import *
from dungeonsheets.features.features import Feature, create_feature
from dungeonsheets.features.fighter import *
from dungeonsheets.features.monk import *
from dungeonsheets.features.paladin import *
from dungeonsheets.features.races import *
from dungeonsheets.features.ranger import *
from dungeonsheets.features.rogue import *
from dungeonsheets.features.sorceror import *
from dungeonsheets.features.warlock import *
from dungeonsheets.features.wizard import *



class ExtraLanguageBase(Feature):
    """You know an additional language of your choice"""
    name = "Extra Language"
    source = "Background"
    # info_dict_key_mod = "1"
    languages = ("[Choose a language]",)

    def __init__(self, owner=None):
        super(ExtraLanguageBase, self).__init__()

        if hasattr(owner, 'info_dict'):
            if not self.info_dict_key() in owner.info_dict:
                owner.info_dict[self.info_dict_key()] = "[Choose a language]"

            self.languages = (owner.info_dict[self.info_dict_key()],)
            print("lang processed...")
            # print(owner.spells)
        else:
            print("lang not processed...")

    @property
    def desc(self):
        return inspect.getdoc(self) + f": **{self.languages[0]}**"

class ExtraLanguage(ExtraLanguageBase):
    """You know an additional language of your choice"""
    name = "Extra Language"
    source = "Background"
    # info_dict_key_mod = "2"

class AdditionalExtraLanguage(ExtraLanguageBase):
    """You know an additional language of your choice"""
    name = "Another Extra Language"
    source = "Background"
    # info_dict_key_mod = "2"


class ExtraLanguageRace(ExtraLanguageBase):
    """You know an additional language of your choice"""
    name = "Extra Language"
    source = "Race"
    # info_dict_key_mod = "Race"