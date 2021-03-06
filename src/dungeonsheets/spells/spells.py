import inspect
import markdown2

# from dungeonsheets.stats import AbilityScore


def create_spell(**params):
    """Create a new subclass of ``Spell`` with given default parameters.
    
    Useful for spells that haven't been entered into the ``spells.py``
    file yet.
    
    Parameters
    ----------
    params : optional
      Saved as attributes of the new class.
    
    Returns
    -------
    NewSpell
      New spell class, subclass of ``Spell``, with given params.
    """
    NewSpell = Spell
    NewSpell.name = params.get('name', 'Unknown Spell')
    NewSpell.level = params.get('level', 9)
    return NewSpell


class Spell():
    """A magical spell castable by a player character."""
    level = 0
    name = "Unknown spell"
    casting_time = "1 action"
    casting_range = "60 ft"
    components = ()
    materials = ""
    duration = "instantaneous"
    ritual = False
    _concentration = False
    magic_school = ""
    classes = ()

    casting_ability: (str, None) = None
    source_str: (str, None) = None
    owner = None
    is_instance = False
    
    def __str__(self):
        if len(self.components) == 0:
            s = self.get_id()
        else:
            s = self.get_id() + ' ({:s}) '.format(','.join(self.components))
        # Indicate if this is a ritual or a concentration
        indicators = [('R', self.ritual), ('C', self.concentration), ('$', self.special_material)]
        indicators = tuple(letter for letter, is_active in indicators if is_active)
        if len(indicators):
            s += f' ({", ".join(indicators)})'
        return s
    
    def __repr__(self):
        return "\"{:s}\"".format(self.get_id())
        # return "\"{:s}\"".format(self.name)

    def __eq__(self, other):
        return (self.name == other.name) and (self.level == other.level)

    def __hash__(self):
        return 0

    def __init__(self, casting_ability="", owner=None, source_str=""):
        self.is_instance = True
        self.casting_ability = casting_ability
        self.owner = owner
        self.source_str = source_str

    @classmethod
    def get_id(cls):
        return cls.__name__

    @classmethod
    def get_desc(cls):
        return inspect.getdoc(cls)

    @classmethod
    def get_desc_html(cls):
        return markdown2.markdown(inspect.getdoc(cls)).strip()

    @property
    def desc_html(self):
        return self.get_desc_html()

    @property
    def desc(self):
        return self.get_desc()

    @classmethod
    def get_component_string(cls):
        s = f'{", ".join(cls.components)}'
        if "M" in cls.components:
            s += f' ({cls.materials})'
        return s

    @classmethod
    def get_short_component_string(cls):
        return f'{", ".join(cls.components)}'

    @property
    def component_string(self):
        return self.get_component_string()

    @property
    def short_component_string(self):
        return self.get_short_component_string()

    @classmethod
    def get_concentration(cls):
        return ('concentration' in cls.duration.lower()) or cls._concentration

    @property
    def concentration(self):
        return ('concentration' in self.duration.lower()) or self._concentration

    @concentration.setter
    def concentration(self, val: bool):
        self._concentration = val

    @property
    def special_material(self):
        return ('worth at least' in self.materials.lower())

    @classmethod
    def get_db_spell(self):
        import db
        return db.Session.query(db.tables.DB_Spell).filter(db.tables.DB_Spell.id == self.get_id()).first()

    @property
    def get_spellcasting_ability_value(self):
        if self.owner is None or self.casting_ability is None:
            return None
        return self.owner.get_char_attr(self.casting_ability)

    @property
    def spell_save_dc(self):
        if self.owner is None:
            return None
        return 8 + self.get_spellcasting_ability_value.modifier + self.owner.proficiency_bonus

    @property
    def spell_attack_modifier(self):
        if self.owner is None:
            return None
        return self.get_spellcasting_ability_value.modifier + self.owner.proficiency_bonus
