import inspect
import textwrap
from typing import Tuple

import markdown2

from dungeonsheets import weapons, spells
# from dungeonsheets.character import Character


def create_feature(**params):
    """Create a new subclass of ``Feature`` with given default parameters.

    Useful for features that haven't been entered into the ``features.py``
    file yet.

    Parameters
    ----------
    params : optional
      Saved as attributes of the new class.

    Returns
    -------
    NewFeature
      New feature class, subclass of ``Feature``, with given params.
    """
    NewFeature = type('UnknownFeature', (Feature,), params)
    return NewFeature


class Feature():
    """
    Provide full text of rules in documentation
    """
    name = "Generic Feature"
    owner = None
    source = ''  # race, class, background, etc.
    # skill_proficiencies = ()
    # skill_choices = ()
    # num_skill_choices = 0
    weapon_proficiencies = ()
    spells_known: (Tuple[spells.Spell], Tuple[str]) = ()
    spells_prepared: (Tuple[spells.Spell], Tuple[str]) = ()
    languages = ()
    proficiencies_text = ()
    needs_implementation = False  # Set to True if need to find way to compute stats
    info_dict_key_mod = ""
    child_features = ()

    _additional_html: (str, bool, None) = None

    auto_load_info_dict = True
    _default_info_dict = {}

    @classmethod
    def get_default_info_dict(cls):
        return cls._default_info_dict

    def __init__(self, owner=None):
        self.owner = owner
        self.spells_known = [S() for S in self.spells_known]
        self.spells_prepared = [S() for S in self.spells_prepared]
        if self.auto_load_info_dict:
            self.load_info_dict()

    def __eq__(self, other):
        return (self.name == other.name) and (self.source == other.source)

    def __hash__(self):
        return 0

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return "\"{:s}\"".format(self.get_id())

    @classmethod
    def get_id(cls):
        return cls.__name__

    @classmethod
    def get_subtypes(cls) -> dict:
        retVal = {cls.__name__: cls}
        for i in cls.__subclasses__():
            retVal[str(i.__name__)] = i
            retVal.update(i.get_subtypes())
        return dict(retVal)

    @property
    def desc(self):
        return self.get_desc()

    @classmethod
    def get_desc(cls):
        return textwrap.dedent(inspect.getdoc(cls))

    @property
    def desc_html(self):
        return markdown2.markdown(self.desc).strip()

    @property
    def additional_html(self):
        return self._additional_html

    @property
    def use_additional_html(self):
        return bool(self._additional_html)

    @classmethod
    def get_desc_html(cls):
        return markdown2.markdown(cls.get_desc(), extras=['cuddled-lists', 'wiki-tables']).strip()


    @classmethod
    def info_dict_key(cls) -> str:
        return "feature__" + cls.__name__ + cls.info_dict_key_mod

    def init_info_dict(self):
        if not hasattr(self.owner, 'info_dict'):
            setattr(self.owner, 'info_dict', {})

        if not self.info_dict_key() in self.owner.info_dict:
            self.owner.info_dict[self.info_dict_key()] = self.get_default_info_dict().copy()

    @property
    def my_info_dict(self):
        self.init_info_dict()

        return self.owner.info_dict[self.info_dict_key()]

    @my_info_dict.setter
    def my_info_dict(self, value):
        self.init_info_dict()

        self.owner.info_dict[self.info_dict_key()] = value

    def load_info_dict(self):
        pass

    def update_info_dict(self):
        pass

    def weapon_func(self, weapon: weapons.Weapon, **kwargs):
        """
        Updates weapon based on the Feature property

        Parameters
        ----------
        weapon
           The weapon to be tested for special bonuses
        kwargs
           Any other key-word arguments the function may require
        """
        pass


class FeatureSelector(Feature):
    """
    A feature with multiple possible choices.
    """
    options = dict()
    name = ''
    source = ''

    def __new__(t, owner, feature_choices=[]):
        # Look for matching feature_choices
        new_feat = Feature.__new__(Feature, owner=owner)
        new_feat.__doc__ = t.__doc__
        new_feat.name = t.name
        new_feat.source = t.source
        new_feat.needs_implementation = True
        for selection in feature_choices:
            if selection.lower() in t.options:
                feat_class = t.options[selection.lower()]
                if owner.has_feature(feat_class):
                    continue
                new_feat = feat_class(owner=owner)
                new_feat.source = t.source
        return new_feat

