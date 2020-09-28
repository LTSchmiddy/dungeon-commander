import inspect

from dungeonsheets.features.features import Feature, create_feature

class ExtraToolProficiencyBase(Feature):
    """You are proficient in an additional artisan's tool of your choice"""
    name = "Extra Tool Proficiency"
    source = ""
    blank_message = "[Choose a tool]"
    proficiencies_text = (blank_message,)

    def __init__(self, owner=None):
        super(ExtraToolProficiencyBase, self).__init__(owner=None)

        if hasattr(owner, 'info_dict'):
            if not self.info_dict_key() in owner.info_dict:
                owner.info_dict[self.info_dict_key()] = self.blank_message

            self.proficiencies_text = (owner.info_dict[self.info_dict_key()],)

    @property
    def desc(self):
        return inspect.getdoc(self) + f": **{self.proficiencies_text[0]}**"

class ExtraToolProficiency(ExtraToolProficiencyBase):
    """You are proficient in an additional artisan's tool of your choice"""
    name = "Extra Tool Proficiency"
    source = "Background"

class AnotherExtraToolProficiency(ExtraToolProficiencyBase):
    """You are proficient in an additional artisan's tool of your choice"""
    name = "Another Extra Tool Proficiency"
    source = "Background"

class GamingSetProficiency(ExtraToolProficiencyBase):
    """You are proficient in an additional gaming set of your choice"""
    name = "Gaming Set Proficiency"
    source = "Background"
    blank_message = "[Choose a gaming set]"

class InstrumentProficiency(ExtraToolProficiencyBase):
    """You are proficient in a musical instrument of your choice"""
    name = "Musical Instrument Proficiency"
    source = "Background"
    blank_message = "[Choose an instrument]"

class PickTwoProficiencyBase(Feature):
    """Choose two from among one type of gaming set, one musical instrument, and an artisan's tools."""
    name = "Pick Two Tools Proficiency Base"
    source = ""
    blank_message = "[Choose one]"
    proficiencies_text = (blank_message,)

    def __init__(self, owner=None):
        super(PickTwoProficiencyBase, self).__init__(owner=None)

        if hasattr(owner, 'info_dict'):
            if not self.info_dict_key() in owner.info_dict:
                owner.info_dict[self.info_dict_key()] = [self.blank_message, self.blank_message]

            self.proficiencies_text = (
                owner.info_dict[self.info_dict_key()][0],
                owner.info_dict[self.info_dict_key()][1]
            )

    @property
    def desc(self):
        return inspect.getdoc(self) + f": **{self.proficiencies_text[0]}**"

class UBHToolProficiencyBase(PickTwoProficiencyBase):
    """Choose two from among one type of gaming set, one musical instrument, and an thieves' tools."""
    name = "Pick Two Tools Proficiency (UBH)"
    source = "Background"

class InstrumentOrGamingSetProficiency(ExtraToolProficiencyBase):
    """You are proficient in a musical instrument or gaming set of your choice"""
    name = "Musical Instrument or Gaming Set Proficiency"
    source = "Background"
    blank_message = "[Choose an instrument or gaming set]"

class ExtraLanguageBase(Feature):
    """You know an additional language of your choice"""
    name = "Extra Language"
    source = "Background"
    # info_dict_key_mod = "1"
    languages = ("[Choose a language]",)

    def __init__(self, owner=None):
        super(ExtraLanguageBase, self).__init__(owner=None)

        if hasattr(owner, 'info_dict'):
            if not self.info_dict_key() in owner.info_dict:
                owner.info_dict[self.info_dict_key()] = "[Choose a language]"

            self.languages = (owner.info_dict[self.info_dict_key()],)
            # print("lang processed...")
            # print(owner.spells)
        # else:
            # print("lang not processed...")

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

class ExtraSkillRace(Feature):
    """You have an additional skill proficiency of your choice"""
    name = "Extra Skill"
    source = "Race"
    # blank_message = "[Choose a Skill]"
    #
    # loaded_skill = blank_message
    #
    # def __init__(self, owner=None):
    #     super(ExtraSkillRace, self).__init__(owner=None)
    #
    #     if hasattr(owner, 'info_dict'):
    #         if not self.info_dict_key() in owner.info_dict:
    #             owner.info_dict[self.info_dict_key()] = self.blank_message
    #         self.loaded_skill = owner.info_dict[self.info_dict_key()]
    #         self.owner.skill_proficiencies = (self.loaded_skill,)
    #
    # @property
    # def desc(self):
    #     return inspect.getdoc(self) + f": **{self.loaded_skill}**"