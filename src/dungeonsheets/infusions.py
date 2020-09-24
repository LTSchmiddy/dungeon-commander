import inspect
from collections import namedtuple

import markdown2

class Infusion:
    name = "Unknown infusion"
    item = "Item to be infused"
    prerequisite = ""
    classes = ('Artificer',)

    def __str__(self):
        indicator = ('$', self.special_material)
        if indicator:
            return self.name + f' ({"".join(indicator)})'
        else:
            return self.name

    def __repr__(self):
        return "\"{:s}\"".format(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return 0

    @property
    def special_material(self):
        return 'worth at least' in self.item.lower()

    @classmethod
    def get_all(cls):
        return cls.__subclasses__()

    @property
    def desc(self):
        return self.get_desc()

    @classmethod
    def get_desc(cls):
        return inspect.getdoc(cls)

    @property
    def desc_html(self):
        return self.get_desc_html()

    @classmethod
    def get_desc_html(cls):
        return markdown2.markdown(cls.get_desc(), extras=['wiki-tables']).strip()

class BootsOfTheWindingPath(Infusion):
    """While wearing these boots, a creature can teleport up to 15 feet as a
    bonus action to an unoccupied space the creature can see. The creature
    must have occupied that space at some point during the current turn.
    """

    name = "Boots of the Winding Path"
    item = "A pair of boots (requires attunement"
    prerequisite = "6th-level artificer"


class EnhancedArcaneFocus(Infusion):
    """While holding this item, a creature gains a + 1 bonus to spell attack
    rolls. In addition, the creature ignores half cover when making a spell
    attack.

    The bonus increases to +2 when you reach 10th level in this class.
    """

    name = "Enhanced Arcane Focus"
    item = "A rod, staff, or wand (requires attunement)"


class EnhancedDefense(Infusion):
    """A creature gains a + 1 bonus to Armor Class while wearing (armor) or
    wielding (shield) the infused item.

    The bonus increases to +2 when you reach 10th level in this class.
    """

    name = "Enhanced Defense"
    item = "A suit of armor or shield"


class EnhancedWeapon(Infusion):
    """This magic weapon grants a +1 bonus to attack and damage rolls made with
    it.

    The bonus increases to +2 when you reach 10th level in this class.
    """

    name = "Enhanced Weapon"
    item = "A simple or martial weapon"


class HomunculusServant(Infusion):
    """You learn intricate methods for magically creating a special homunculus
    that serves you. The item you infuse serves as the creature's heart, around
    which the creature's body instantly forms.

    You determine the homunculus's appearance. Some artificers prefer
    mechanical-looking birds, whereas some like winged vials or miniature,
    animate cauldrons.

    The homunculus is friendly to you and your companions, and it obeys your
    commands. See this creature's game statistics in the Homunculus Servant
    stat block.

    In combat, the homunculus shares your initiative count, but it takes its
    turn immediately after yours. It can move and use its reaction on its own,
    but the only action it takes on its turn is the Dodge action, unless you
    take a bonus action on your turn to command it to take the action in its
    stat block or the Dash, Disengage, Help, Hide, or Search action.

    The homunculus regains 2d6 hit points if the *mending* spell is cast on it.
    If it dies, it vanishes, leaving its heart in its space.
    ---
    **Homunculus Servant**
    *Tiny construct, neutral*

    **Armor Class** 13 (natural armor)<br/>
   ** Hit Points** equal to homunculus's Constitution modifier + your Intelligence modifier + your level in this class<br/>
    **Speed **20 ft., fly 30 ft.<br/>
    **STR** 4 (−3) **DEX** 15 (+2) **CON** 12 (+1) **INT** 10 (+0) **WIS** 10 (+0) **CHA** 7 (−2)<br/>
    **Saving Throws** Dex +1<br/>
    **Skills** Perception +4, Stealth +4<br/>
    **Damage Immunities** poison<br/>
    **Condition Immunities** exhaustion, poisoned<br/>
    **Senses** darkvision 60 ft., passive Perception 14<br/>
    **Languages** understands the languages you speak<br/>

    **Evasion.** If the homunculus is subjected to an effect that allows it to make a Dexterity saving throw to take only
    half damage, it instead takes no damage if it succeeds on the saving throw, and only half damage if it fails. it
    can't use this trait if it's incapacitated

    **Might of the Master.** The following numbers increase by 1 when your proficiency bonus increases by 1: the
    homunculus’s skill and saving throw bonuses (above( and the bonuses to hit and damage of its attack (below).

    **Actions (Require Your Bonus Action)**
    Force Strike. Ranged Weapon Attack: +4 to hit, range 30 ft., one target you can see. Hit: 1d4 + 2 force damage.

    **Reactions**
    Channel Magic. The homunculus delivers a spell you cast that has a range of touch. The homunculus must be within
    120 feet of you.

    """

    name = "Homunculus Servant"
    item = "A gem worth at least 100gp or a dragonshard"
    prerequisite = "6th-level artificer"


class RadiantWeapon(Infusion):
    """This magic weapon grants a + 1 bonus to attack and damage rolls made
    with it. While holding it, the wielder can take a bonus action to cause it
    to shed bright light in a 30-foot radius and dim light for an additional 30
    feet. The wielder can extinguish the light as a bonus action.

    The weapon has 4 charges. As a reaction immediately after being hit by an
    attack, the wielder can expend 1 charge and cause the attacker to be
    blinded until the end of the attacker's next turn, unless the attacker
    succeeds on a Constitution saving throw against your spell save DC. The
    weapon regains ld4 expended charges daily at dawn.
    """

    name = "Radiant Weapon"
    item = "A simple or martial weapon (requires attunement)"
    prerequisite = "6th-level artificer"


class RepeatingShot(Infusion):
    """This magic weapon grants a + 1 bonus to attack and damage rolls made
    with it when it's used to make a ranged attack, and it ignores the loading
    property if it has it.

    If you load no ammunition in the weapon, it produces its own, automatically
    creating one piece of magic am­munition when you make a ranged attack with
    it. The ammunition created by the weapon vanishes the instant after it hits
    or misses a target.
    """

    name = "Repeating Shot"
    item = """A simple or martial weapon with the ammunition property (requires
              attunement)"""


class ReplicateMagicItem(Infusion):
    """
    Using this infusion, you replicate a particular magic item. You can
    learn this infusion multiple times; each time you do so, choose a magic
    item that you can make with it, picking from the Replicable Items tables
    below. A table's title tells you the level you must be in the class to
    choose an item from the table.

    In the tables, an item's entry tells you whether the item requires
    attunement. See the item's description in the *Dungeon Master's Guide* for
    more information about it, including the type of object required for its
    making. If you have *Xanathar's Guide to Everything*, you can choose from
    among the common magic items in that book when you pick a magic item you
    can replicate with this infusion.
    """
    RepItem = namedtuple('RepItem', ('name', 'attunement', 'level'))

    name = "Replicate Magic Item"
    item_table = {
        2: (
            RepItem(name='Alchemy jug', attunement='No', level=2),
            RepItem(name='Armblade (Eberron: Rising from the Last War)', attunement='Yes', level=2),
            RepItem(name='Bag of holding', attunement='No', level=2),
            RepItem(name='Cap of water breathing', attunement='No', level=2),
            RepItem(name='Goggles of night', attunement='No', level=2),
            RepItem(name='Prosthetic limb (Eberron: Rising from the Last War)', attunement='Yes', level=2),
            RepItem(name='Rope of climbing', attunement='No', level=2),
            RepItem(name='Sending stones', attunement='No', level=2),
            RepItem(name='Wand of magic detection', attunement='No', level=2),
            RepItem(name='Wand of secrets', attunement='No', level=2)
        ),
        6: (
            RepItem(name='Boots of elvenkind', attunement='No', level=6),
            RepItem(name='Cloak of elvenkind', attunement='No', level=6),
            RepItem(name='Cloak of the manta ray', attunement='No', level=6),
            RepItem(name='Eyes of charming', attunement='Yes', level=6),
            RepItem(name='Gloves of thievery', attunement='No', level=6),
            RepItem(name='Lantern of revealing', attunement='No', level=6),
            RepItem(name='Pipes of haunting', attunement='No', level=6),
            RepItem(name='Ring of water walking', attunement='No', level=6),
            RepItem(name='Wand sheath (Eberron: Rising from the Last War)', attunement='Yes', level=6)
        ),
        10: (
            RepItem(name='Boots of striding and springing', attunement='Yes', level=10),
            RepItem(name='Boots of the winterlands', attunement='Yes', level=10),
            RepItem(name='Bracers of archery', attunement='Yes', level=10),
            RepItem(name='Brooch of shielding', attunement='Yes', level=10),
            RepItem(name='Cloak of protection', attunement='Yes', level=10),
            RepItem(name='Eyes of the eagle', attunement='Yes', level=10),
            RepItem(name='Gauntlets of ogre power', attunement='Yes', level=10),
            RepItem(name='Gloves of missile snaring', attunement='Yes', level=10),
            RepItem(name='Gloves of swimming and climbing', attunement='Yes', level=10),
            RepItem(name='Hat of disguise', attunement='Yes', level=10),
            RepItem(name='Headband of intellect', attunement='Yes', level=10),
            RepItem(name='Helm of telepathy', attunement='Yes', level=10),
            RepItem(name='Medallion of thoughts', attunement='Yes', level=10),
            RepItem(name='Periapt of wound closure', attunement='Yes', level=10),
            RepItem(name='Pipes of the sewers', attunement='Yes', level=10),
            RepItem(name='Quiver of Ehlonna', attunement='No', level=10),
            RepItem(name='Ring of jumping', attunement='Yes', level=10),
            RepItem(name='Ring of mind shielding', attunement='Yes', level=10),
            RepItem(name='Slippers of spider climbing', attunement='Yes', level=10),
            RepItem(name='Ventilating lung (Eberron: Rising from the Last War)', attunement='Yes', level=10),
            RepItem(name='Winged boots', attunement='Yes', level=10)
        ),
        14: (
            RepItem(name='Amulet of health', attunement='Yes', level=14),
            RepItem(name='Arcane propulsion arm (Eberron: Rising from the Last War)', attunement='Yes', level=14),
            RepItem(name='Belt of hill giant strength', attunement='Yes', level=14),
            RepItem(name='Boots of levitation', attunement='Yes', level=14),
            RepItem(name='Boots of speed', attunement='Yes', level=14),
            RepItem(name='Bracers of defense', attunement='Yes', level=14),
            RepItem(name='Cloak of the bat', attunement='Yes', level=14),
            RepItem(name='Dimensional shackles', attunement='No', level=14),
            RepItem(name='Gem of seeing', attunement='Yes', level=14),
            RepItem(name='Horn of blasting', attunement='No', level=14),
            RepItem(name='Ring of free action', attunement='Yes', level=14),
            RepItem(name='Ring of protection', attunement='Yes', level=14),
            RepItem(name='Ring of the ram', attunement='Yes', level=14)
        )
    }


class RepulsionShield(Infusion):
    """A creature gains a + 1 bonus to Armor Class while wield­ing this shield.

    The shield has 4 charges. While holding it, the wielder can use a reaction
    immediately after being hit by a melee attack to expend 1 of the shield's
    charges and push the attacker up to 15 feet away. The shield regains ld4
    expended charges daily at dawn.
    """

    name = "Repulsion Shield"
    item = "A shield (requires attunement)"


class ResistantArmor(Infusion):
    """While wearing this armor, a creature has resistance to one of the
    following damage types, which you choose when you infuse the item: acid,
    cold, fire, force, light­ning, necrotic, poison, psychic, radiant, or
    thunder.
    """

    name = "Resistant Armor"
    item = "A suit of armor (requires attunement)"


class ReturningWeapon(Infusion):
    """This magic weapon grants a + 1 bonus to attack and damage rolls made
    with it, and it returns to the wielder's hand immediately after it is used
    to make a ranged attack.
    """

    name = "Returning Weapon"
    item = "A simple or martial weapon with the thrown property"
