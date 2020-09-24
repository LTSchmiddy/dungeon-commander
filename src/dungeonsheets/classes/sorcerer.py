from collections import defaultdict

from dungeonsheets import features, weapons
from dungeonsheets.classes.classes import CharClass, SubClass


# PHB
class DraconicBloodline(SubClass):
    """Your innate magic comes from draconic magic that was mingled with your
    blood or that of your ancestors. Most often, sorcerers with this origin
    trace their descent back to a mighty sorcerer of ancient times who made a
    bargain with a dragon or who might even have claimed a dragon parent. Some
    of these bloodlines are well established in the world, but most are
    obscure. Any given sorcerer could be the first of a new bloodline, as a
    result of a pact or some other exceptional circumstance.

    """
    name = "Draconic Bloodline"
    languages = ('draconic',)
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.DragonAncestor,
                            features.DraconicResilience]
    features_by_level[6] = [features.ElementalAffinity]
    features_by_level[14] = [features.DragonWings]
    features_by_level[18] = [features.DraconicPresence]


class WildMagic(SubClass):
    """Your innate magic comes from the wild forces of chaos that underlie the
    order of creation. You might have endured exposure to some form o f raw
    magic, perhaps through a planar portal leading to Limbo, the Elemental
    Planes, or the mysterious Far Realm. Perhaps you were blessed by a powerful
    fey creature or marked by a demon. Or your magic could be a fluke of your
    birth, with no apparent cause or reason. However it came to be, this
    chaotic magic churns within you, waiting for any outlet.

    """
    name = "Wild Magic"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.WildMagicSurge, features.TidesOfChaos]
    features_by_level[6] = [features.BendLuck]
    features_by_level[14] = [features.ControlledChaos]
    features_by_level[18] = [features.SpellBombardment]


# XGTE
class DivineSoul(SubClass):
    """Sometimes the spark of magic that fuels a sorcerer comes from a divine
    source that glimmers within the soul. Having such a blessed soul is a sign
    that your innate magic might come from a distant but powerful familial
    connection to a divine being. Perhaps your ances- tor was an angel,
    transformed into a mortal and sent to fight in a god's name. Or your birth
    might align with an ancient prophecy, marking you as a servant of the gods
    or a chosen vessel of divine magic.

    A Divine Soul, with a natural magnetism, is seen as a threat by some
    religious hierarchies. As an outsider who commands sacred power, a Divine
    Soul can undermine an existing order by claiming a direct tie to the
    divine.

    In some cultures, only those who can claim the power of a Divine Soul may
    command religious power. In these lands, ecclesiastical positions are
    dominated by a few bloodlines and preserved over generations

    """
    name = "Divine Soul"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.DivineMagic, features.FavoredByTheGods]
    features_by_level[6] = [features.EmpoweredHealing]
    features_by_level[14] = [features.OtherworldlyWings]
    features_by_level[18] = [features.UnearthlyRecovery]


class ShadowMagic(SubClass):
    """You are a creature of shadow, for your innate magic comes from the
    Shadowfell itself. You might trace your lineage to an entity from that
    place, or perhaps you were exposed to its fell energy and transformed by
    it.

    The power of shadow magic casts a strange pall over your physical
    presence. The spark of life that sustains you is muffled, as if it
    struggles to remain viable against the dark energy that imbues your
    soul. At your option, you can pick from or roll on the Shadow Sorcerer
    Quirks table to create a quirk for your character

    """
    name = "Shadow Magic"
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.EyesOfTheDark,
                            features.SuperiorDarkvision,
                            features.StrengthOfTheGrave]
    features_by_level[6] = [features.HoundOfIllOmen]
    features_by_level[14] = [features.ShadowWalk]
    features_by_level[18] = [features.UmbralForm]


class StormSorcery(SubClass):
    """Your innate magic comes from the power of elemental air. Many with this
    power can trace their magic back to a near-death experience caused by the
    Great Rain, but perhaps you were born during a howling gale so powerful
    that folk still tell stories of it, or your lineage might include the
    influence of potent air creatures such as djinn. Whatever the case, the
    magic of the storm permeates your being.

    Storm sorcerers are invaluable members of a ship's crew. Their magic allows
    them to exert control over wind and weather in their immediate area. Their
    abilities also prove useful in repelling attacks by sahuagin, pirates,
    and other waterborne threats.

    """
    name = "Storm Sorcery"
    languages = ("primordial",)
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.TempestuousMagic]
    features_by_level[6] = [features.HeartOfTheStorm, features.StormGuide]
    features_by_level[14] = [features.StormsFury]
    features_by_level[18] = [features.WindSoul]


class Sorcerer(CharClass):
    """
    Sorcerers carry a magical birthright conferred upon them by an exotic bloodline, some otherworldly influence, or
    exposure to unknown cosmic forces. One can’t study sorcery as one learns a language, any more than one can learn to
    live a legendary life. No one chooses sorcery; the power chooses the sorcerer.

    # Raw Magic
    Magic is a part of every sorcerer, suffusing body, mind, and spirit with a latent power that waits to be tapped.
    Some sorcerers wield magic that springs from an ancient bloodline infused with the magic of dragons. Others carry
    a raw, uncontrolled magic within them, a chaotic storm that manifests in unexpected ways.

    The appearance of sorcerous powers is wildly unpredictable. Some draconic bloodlines produce exactly one sorcerer
    in every generation, but in other lines of descent every individual is a sorcerer. Most of the time, the talents of
    sorcery appear as apparent flukes. Some sorcerers can’t name the origin of their power, while others trace it to
    strange events in their own lives. The touch of a demon, the blessing of a dryad at a baby’s birth, or a taste of
    the water from a mysterious spring might spark the gift of sorcery. So too might the gift of a deity of magic,
    exposure to the elemental forces of the Inner Planes or the maddening chaos of Limbo, or a glimpse into the inner
    workings of reality.

    Sorcerers have no use for the spellbooks and ancient tomes of magic lore that wizards rely on, nor do they rely on a
    patron to grant their spells as warlocks do. By learning to harness and channel their own inborn magic, they can
    discover new and staggering ways to unleash that power.

    # Unexplained Powers
    Sorcerers are rare in the world, and it’s unusual to find a sorcerer who is not involved in the adventuring life in
    some way. People with magical power seething in their veins soon discover that the power doesn’t like to stay quiet.
    A sorcerer’s magic wants to be wielded, and it has a tendency to spill out in unpredictable ways if it isn’t called
    on.

    Sorcerers often have obscure or quixotic motivations driving them to adventure. Some seek a greater understanding of
    the magical force that infuses them, or the answer to the mystery of its origin. Others hope to find a way to get
    rid of it, or to unleash its full potential. Whatever their goals, sorcerers are every bit as useful to an
    adventuring party as wizards, making up for a comparative lack of breadth in their magical knowledge with enormous
    flexibility in using the spells they know.
    """
    name = 'Sorcerer'
    hit_dice_faces = 6
    subclass_select_level = 1
    saving_throw_proficiencies = ('constitution', 'charisma')
    primary_abilities = ('charisma',)
    _proficiencies_text = ('daggers', 'darts', 'slings',
                           'quarterstaffs', 'light crossbows')
    weapon_proficiencies = (weapons.Dagger, weapons.Dart,
                            weapons.Sling, weapons.Quarterstaff,
                            weapons.LightCrossbow)
    multiclass_weapon_proficiencies = ()
    _multiclass_proficiencies_text = ()
    class_skill_choices = ('Arcana', 'Deception', 'Insight',
                           'Intimidation', 'Persuasion', 'Religion')
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.SorcererAbilityScoreImprovement, features.SorcererSpellcasting]
    features_by_level[2] = [features.FontOfMagic]
    features_by_level[3] = [features.Metamagic]
    features_by_level[20] = [features.SorcerousRestoration]
    subclasses_available = (DraconicBloodline, WildMagic, DivineSoul,
                            ShadowMagic, StormSorcery)
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
        10: 11,
        11: 12,
        12: 12,
        13: 13,
        14: 13,
        15: 14,
        16: 14,
        17: 15,
        18: 15,
        19: 15,
        20: 15,
    }
    spell_slots_by_level = {
        # char_lvl: (cantrips, 1st, 2nd, 3rd, ...)
        1:  (4, 2, 0, 0, 0, 0, 0, 0, 0, 0),
        2:  (4, 3, 0, 0, 0, 0, 0, 0, 0, 0),
        3:  (4, 4, 2, 0, 0, 0, 0, 0, 0, 0),
        4:  (5, 4, 3, 0, 0, 0, 0, 0, 0, 0),
        5:  (5, 4, 3, 2, 0, 0, 0, 0, 0, 0),
        6:  (5, 4, 3, 3, 0, 0, 0, 0, 0, 0),
        7:  (5, 4, 3, 3, 1, 0, 0, 0, 0, 0),
        8:  (5, 4, 3, 3, 2, 0, 0, 0, 0, 0),
        9:  (5, 4, 3, 3, 3, 1, 0, 0, 0, 0),
        10: (6, 4, 3, 3, 3, 2, 0, 0, 0, 0),
        11: (6, 4, 3, 3, 3, 2, 1, 0, 0, 0),
        12: (6, 4, 3, 3, 3, 2, 1, 0, 0, 0),
        13: (6, 4, 3, 3, 3, 2, 1, 1, 0, 0),
        14: (6, 4, 3, 3, 3, 2, 1, 1, 0, 0),
        15: (6, 4, 3, 3, 3, 2, 1, 1, 1, 0),
        16: (6, 4, 3, 3, 3, 2, 1, 1, 1, 0),
        17: (6, 4, 3, 3, 3, 2, 1, 1, 1, 1),
        18: (6, 4, 3, 3, 3, 3, 1, 1, 1, 1),
        19: (6, 4, 3, 3, 3, 3, 2, 1, 1, 1),
        20: (6, 4, 3, 3, 3, 3, 2, 2, 1, 1),
    }
