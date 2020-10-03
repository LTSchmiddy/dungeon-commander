from collections import defaultdict

from dungeonsheets import features, spells, weapons
from dungeonsheets.classes.classes import CharClass, SubClass


# PHB
class Archfey(SubClass):
    """Your patron is a lord or lady of the fey, a creature of legend who holds
    secrets that were forgotten before the mortal races were born. This being's
    motivations are often inscrutable, and sometimes whimsical, and might
    involve a striving for greater magical power or the settling of age-old
    grudges. Beings of this sort include the Prince of Frost; the Queen of Air
    and Darkness, ruler of the Gloaming Court; Titania of the Summer Court; her
    consort Oberon, the Green Lord; Hyrsam, the Prince of Fools; and ancient
    hags

    """
    name = "The Archfey Patron"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.FeyPresence]
    features_by_level[6] = [features.MistyEscape]
    features_by_level[10] = [features.BeguilingDefenses]
    features_by_level[14] = [features.DarkDelirium]


class Fiend(SubClass):
    """You have made a pact with a fiend from the lower planes o f existence, a
    being whose aims are evil, even if you strive against those aims. Such
    beings desire the corruption or destruction of all things, ultimately
    including you. Fiends powerful enough to forge a pact include demon lords
    such as Demogorgon, Orcus, Fraz'Urb-luu, and Baphomet; archdevils such as
    Asmodeus, Dispater, Mephistopheles, and Belial; pit fiends and balors that
    are especially mighty; and ultroloths and other lords of the yugoloths

    """
    name = "The Fiend Patron"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.DarkOnesBlessing]
    features_by_level[6] = [features.DarkOnesOwnLuck]
    features_by_level[10] = [features.FiendishResilience]
    features_by_level[14] = [features.HurlThroughHell]


class GreatOldOne(SubClass):
    """Your patron is a mysterious entity whose nature is utterly foreign to the
    fabric of reality. It might come from the Far Realm, the space beyond
    reality, or it could be one of the elder gods known only in legends. Its
    motives are incomprehensible to mortals, and its knowledge so immense and
    ancient that even the greatest libraries pale in comparison to the vast
    secrets it holds. The Great Old One might be unaware of your existence or
    entirely indifferent to you, but the secrets you have learned allow you to
    draw your magic from it.

    Entities of this type include Ghaunadar, called That Which Lurks;
    Tharizdun, the Chained God; Dendar, the Night Serpent; Zargon, the
    Returner; Great Cthulhu; and other unfathomable beings.

    """
    name = "The Great Old One Patron"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.AwakenedMind]
    features_by_level[6] = [features.EntropicWard]
    features_by_level[10] = [features.ThoughtShield]
    features_by_level[14] = [features.CreateThrall]


# SCAG
class Undying(SubClass):
    """Death holds no sway over your patron, who has un- locked the secrets of
    everlasting life, although such a prize- like all power- comes at a
    price. Once mortal, the Undying has seen mortal lifetimes pass like the
    sea- sons, like the flicker of endless days and nights. It has the secrets
    of the ages to share, secrets of life and death. Beings of this sort
    include Vecna, Lord of the Hand and the Eye; the dread Iuz; the lich-queen
    Vol; the Undying Court of Aerenal; Vlaakith, lich-queen of the githyanki;
    and the deathless wizard Fistandantalus.

    In the Realms, Undying patrons include Larloch the Shadow King, legendary
    master of Warlock's Crypt, and Gilgeam, the God-King of Unther

    """
    name = "The Undying Patron"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.AmongTheDead]
    features_by_level[6] = [features.DefyDeath]
    features_by_level[10] = [features.UndyingNature]
    features_by_level[14] = [features.IndestructibleLife]


# XGTE
class Celestial(SubClass):
    """Your patron is a powerful being of the Upper Planes. You have bound yourself
    to an ancient empyrean, solar, ki-rin, unicorn, or other entity that
    resides in the planes of everlasting bliss. Your pact with that being
    allows you to experience the barest touch of the holy light that illuminates
    the multiverse.

    Being connected to such power can cause changes in your behavior and
    beliefs. You might find yourself driven to annihilate the undead, to defeat
    fiends, and to protect the innocent. At times, your heart might also be
    filled with a longing for the celestial realm of your patron, and a desire
    to wander that paradise for the rest of your days. But you know that your
    mission is among mortals for now, and that your pact binds you to bring
    light to the dark places of the world.

    """
    name = "The Celestial Patron"
    spells_known = spells_prepared = (spells.Light, spells.SacredFlame)
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.HealingLight]
    features_by_level[6] = [features.RadiantSoul]
    features_by_level[10] = [features.CelestialResilience]
    features_by_level[14] = [features.SearingVengeance]


class Hexblade(SubClass):
    """You have made your pact with a mysterious entity from the Shadowfell-a force
    that manifests in sentient magic weapon_list carved from the stuff of
    shadow. The mighty sword Blackrazor is the most notable of these weapon_list,
    which have been spread across the multiverse over the ages. The shadowy
    force behind these weapon_list can offer power to warlocks who form pacts with
    it. Many hexhlade warlocks create weapon_list that emulate those formed in the
    Shadowfell. Others forgo such arms, content to weave the dark magic of that
    plane into their spellcasting.

    Because the Raven Queen is known to have forged the first of these weapon_list,
    many sages speculate that she and the force are one and that the weapon_list,
    along with hexblade warlocks, are tools she uses to manipulate events on
    the Material Plane to her inscrutable ends

    """
    name = "Hexblade Patron"
    weapon_proficiencies = (weapons.MartialWeapon,)
    _proficiencies_text = ['martial weapon_list', 'medium armor', 'shields']
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.HexbladesCurse, features.HexWarrior]
    features_by_level[6] = [features.AccursedSpecter]
    features_by_level[10] = [features.ArmorOfHexes]
    features_by_level[14] = [features.MasterOfHexes]


class Warlock(CharClass):
    """
    Warlocks are seekers of the knowledge that lies hidden in the fabric of the multiverse. Through pacts made with
    mysterious beings of supernatural power, warlocks unlock magical effects both subtle and spectacular. Drawing on the
    ancient knowledge of beings such as fey nobles, demons, devils, hags, and alien entities of the Far Realm, warlocks
    piece together arcane secrets to bolster their own power.

    # Sworn and Beholden
    A warlock is defined by a pact with an otherworldly being. Sometimes the relationship between warlock and patron is
    like that of a cleric and a deity, though the beings that serve as patrons for warlocks are not gods. A warlock
    might lead a cult dedicated to a demon prince, an archdevil, or an utterly alien entity—beings not typically served
    by clerics. More often, though, the arrangement is similar to that between a master and an apprentice. The warlock
    learns and grows in power, at the cost of occasional services performed on the patron’s behalf.

    The magic bestowed on a warlock ranges from minor but lasting alterations to the warlock’s being (such as the
    ability to see in darkness or to read any language) to access to powerful spells. Unlike bookish wizards, warlocks
    supplement their magic with some facility at hand-to-hand combat. They are comfortable in light armor and know how
    to use simple weapon_list.

    # Delvers into Secrets
    Warlocks are driven by an insatiable need for knowledge and power, which compels them into their pacts and shapes
    their lives. This thirst drives warlocks into their pacts and shapes their later careers as well.

    Stories of warlocks binding themselves to fiends are widely known. But many warlocks serve patrons that are not
    fiendish. Sometimes a traveler in the wilds comes to a strangely beautiful tower, meets its fey lord or lady, and
    stumbles into a pact without being fully aware of it. And sometimes, while poring over tomes of forbidden lore, a
    brilliant but crazed student’s mind is opened to realities beyond the material world and to the alien beings that
    dwell in the outer void.

    Once a pact is made, a warlock’s thirst for knowledge and power can’t be slaked with mere study and research. No one
    makes a pact with such a mighty patron if he or she doesn’t intend to use the power thus gained. Rather, the vast
    majority of warlocks spend their days in active pursuit of their goals, which typically means some kind of
    adventuring. Furthermore, the demands of their patrons drive warlocks toward adventure.
    """
    name = 'Warlock'
    hit_dice_faces = 8
    subclass_select_level = 1
    saving_throw_proficiencies = ('wisdom', 'charisma')
    primary_abilities = ('charisma',)
    _proficiencies_text = ("light Armor", "simple weapon_list")
    class_skill_choices = ('Arcana', 'Deception', 'History',
                           'Intimidation', 'Investigation', 'Nature',
                           'Religion')
    weapon_proficiencies = (weapons.SimpleWeapon,)
    multiclass_weapon_proficiencies = weapon_proficiencies
    _multiclass_proficiencies_text = ('light armor', 'simple weapon_list')
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.WarlockAbilityScoreImprovement, features.OtherworldlyPatron]
    features_by_level[2] = [features.EldritchInvocation]
    features_by_level[3] = [features.PactBoon]
    features_by_level[11] = [features.MysticArcanum]
    features_by_level[20] = [features.EldritchMaster]
    subclasses_available = (Archfey, Fiend, GreatOldOne, Undying, Celestial,
                            Hexblade)
    spellcasting_ability = 'charisma'
    spells_known_by_level = {
        1: 2,
        2: 3,
        3: 4,
        4: 5,
        5: 6,
        6: 7,
        7: 8,
        8: 9,
        9: 10,
        10: 10,
        11: 11,
        12: 11,
        13: 12,
        14: 12,
        15: 13,
        16: 13,
        17: 14,
        18: 14,
        19: 15,
        20: 15,
    }
    spell_slots_by_level = {
        1:  (2, 1, 0, 0, 0, 0, 0, 0, 0, 0),
        2:  (2, 2, 0, 0, 0, 0, 0, 0, 0, 0),
        3:  (2, 0, 2, 0, 0, 0, 0, 0, 0, 0),
        4:  (3, 0, 2, 0, 0, 0, 0, 0, 0, 0),
        5:  (3, 0, 0, 3, 0, 0, 0, 0, 0, 0),
        6:  (3, 0, 0, 3, 0, 0, 0, 0, 0, 0),
        7:  (3, 0, 0, 0, 2, 0, 0, 0, 0, 0),
        8:  (3, 0, 0, 0, 2, 0, 0, 0, 0, 0),
        9:  (3, 0, 0, 0, 0, 2, 0, 0, 0, 0),
        10: (4, 0, 0, 0, 0, 2, 0, 0, 0, 0),
        11: (4, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        12: (4, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        13: (4, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        14: (4, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        15: (4, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        16: (4, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        17: (4, 0, 0, 0, 0, 4, 0, 0, 0, 0),
        18: (4, 0, 0, 0, 0, 4, 0, 0, 0, 0),
        19: (4, 0, 0, 0, 0, 4, 0, 0, 0, 0),
        20: (4, 0, 0, 0, 0, 4, 0, 0, 0, 0),
    }
