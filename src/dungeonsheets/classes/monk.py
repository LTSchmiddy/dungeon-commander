__all__ = ('Monk')

from collections import defaultdict

from dungeonsheets import features, weapons
from dungeonsheets.classes.classes import CharClass, SubClass


# PHB
class OpenHandWay(SubClass):
    """Monks of the Way of the Open Hand are the ultimate masters of martial arts
    combat, whether armed or unarmed. They learn techniques to push and trip
    their opponents, manipulate ki to heal damage to their bodies, and practice
    advanced meditation that can protect them from harm.

    """
    name = "Way of the Open Hand"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.OpenHandTechnique]
    features_by_level[6] = [features.WholenessOfBody]
    features_by_level[11] = [features.Tranquility]
    features_by_level[17] = [features.QuiveringPalm]


class ShadowWay(SubClass):
    """Monks of the Way of Shadow follow a tradition that values stealth and
    subterfuge. These monks might be called ninjas or shadowdancers, and they
    serve as spies and assassins. Sometimes the members of a ninja monastery
    are family members, forming a clan sworn to secrecy about their arts and
    missions. Other monasteries are more like thieves' guilds, hiring out their
    services to nobles, rich merchants, or anyone else who can pay their
    fees. Regardless of their methods, the heads of these monasteries expect
    the unquestioning obedience of their students

    """
    name = "Way of Shadow"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.ShadowArts]
    features_by_level[6] = [features.ShadowStep]
    features_by_level[11] = [features.CloakOfShadows]
    features_by_level[17] = [features.Opportunist]


class FourElementsWay(SubClass):
    """You follow a monastic tradition that teaches you to harness the
    elements. When you focus your ki, you can align yourself with the forces of
    creation and bend the four elements to your will, using them as an
    extension of your body. Some members of this tradition dedicate themselves
    to a single element, but others weave the elements together.

    Many monks of this tradition tattoo their bodies with representations of
    their ki powers, commonly imagined as coiling dragons, but also as
    phoenixes, fish, plants, mountains, and cresting waves.

    """
    name = "Way of the Four Elements"
    spellcasting_ability = 'wisdom'
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.DiscipleOfTheElements,
                            features.ElementalAttunement]


# SCAG
class LongDeathWay(SubClass):
    """Monks of the Way of the Long Death are obsessed with the meaning and
    mechanics of dying. They capture creatures and prepare elaborate
    experiments to capture, record, and understand the moments of their
    demise. They then use this knowledge to guide their understanding of
    martial arts, yielding a deadly fighting style.

    """
    name = "Way of the Long Death"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.TouchOfDeath]
    features_by_level[6] = [features.HourOfReaping]
    features_by_level[11] = [features.MasteryOfDeath]
    features_by_level[17] = [features.TouchOfTheLongDeath]


class SunSoulWay(SubClass):
    """Monks of the Way of the Sun Soul learn to channel their own life energy
    into searing bolts of light. They teach that meditation can unlock the
    ability to unleash the indomitable light shed by the soul of every living
    creature

    """
    name = "Way of the Sun Soul"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.RadiantSunBolt]
    features_by_level[6] = [features.SearingArcStrike]
    features_by_level[11] = [features.SearingSunburst]
    features_by_level[17] = [features.SunShield]


# XGTE
class DrunkenMasterWay(SubClass):
    """The Way of the Drunken Master teaches its students to move with the jerky,
    unpredictable movements of a drunkard. A drunken master sways, tottering on
    unsteady feet, to present what seems like an incompetent combatant who
    proves frustrating to engage. The drunken master's erratic stumbles conceal
    a carefully executed dance of blocks, parries, advances, attacks, and
    retreats.

    A drunken master often enjoys playing the fool to bring gladness to the
    despondent or to demonstrate humility to the arrogant, but when battle is
    joined, the drunken master can be a maddening, masterful foe

    """
    name = "Way of the Drunken Master"
    _proficiencies_text = ("brewer's suplies",)
    skill_proficiencies = ("performance",)
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.DrunkenTechnique]
    features_by_level[6] = [features.TipsySway]
    features_by_level[11] = [features.DrunkardsLuck]
    features_by_level[17] = [features.IntoxicatedFrenzy]


class KenseiWay(SubClass):
    """Monks of the Way of the Kensei train relentlessly with their weapons, to
    the point where the weapon becomes an extension of the body. Founded on a
    mastery of sword fighting, the tradition has expanded to include many
    different weapons.

    A kensei sees a weapon in much the same way a calligrapher or painter
    regards a pen or brush. Whatever the weapon, the kensei views it as a tool
    used to express the beauty and precision of the martial arts. That such
    mastery makes a kensei a peerless warrior is but a side effect of intense
    devotion, practice, and study.

    """
    name = "Way of the Kensei"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.PathOfTheKensei]
    features_by_level[6] = [features.OneWithTheBlade]
    features_by_level[11] = [features.SharpenTheBlade]
    features_by_level[17] = [features.UnerringAccuracy]


class Monk(CharClass):
    """
    Whatever their discipline, monks are united in their ability to magically harness the energy that flows in their
    bodies. Whether channeled as a striking display of combat prowess or a subtler focus of defensive ability and speed,
    this energy infuses all that a monk does.

    # The Magic of Ki
    Monks make careful study of a magical energy that most monastic traditions call ki. This energy is an element of the
    magic that suffuses the multiverse—specifically, the element that flows through living bodies. Monks harness this
    power within themselves to create magical effects and exceed their bodies’ physical capabilities, and some of their
    special attacks can hinder the flow of ki in their opponents. Using this energy, monks channel uncanny speed and
    strength into their unarmed strikes. As they gain experience, their martial training and their mastery of ki gives
    them more power over their bodies and the bodies of their foes.

    # Training and Asceticism
    Small walled cloisters dot the landscapes of the worlds of D&D, tiny refuges from the flow of ordinary life, where
    time seems to stand still. The monks who live there seek personal perfection through contemplation and rigorous
    training. Many entered the monastery as children, sent to live there when their parents died, when food couldn’t be
    found to support them, or in return for some kindness that the monks had performed for their families.

    Some monks live entirely apart from the surrounding population, secluded from anything that might impede their
    spiritual progress. Others are sworn to isolation, emerging only to serve as spies or assassins at the command of
    their leader, a noble patron, or some other mortal or divine power.

    The majority of monks don’t shun their neighbors, making frequent visits to nearby towns or villages and exchanging
    their service for food and other goods. As versatile warriors, monks often end up protecting their neighbors from
    monsters or tyrants.

    For a monk, becoming an adventurer means leaving a structured, communal lifestyle to become a wanderer. This can be
    a harsh transition, and monks don’t undertake it lightly. Those who leave their cloisters take their work seriously,
    approaching their adventures as personal tests of their physical and spiritual growth. As a rule, monks care little
    for material wealth and are driven by a desire to accomplish a greater mission than merely slaying monsters and
    plundering their treasure.
    """
    name = 'Monk'
    hit_dice_faces = 8
    subclass_select_level = 3
    saving_throw_proficiencies = ('strength', 'dexterity')
    primary_abilities = ('dexterity', 'wisdom')
    _proficiencies_text = (
        'simple weapons', 'shortswords', 'unarmed',
        "one type of artisan's tools or one musical instrument")
    weapon_proficiencies = (weapons.Shortsword, weapons.Unarmed,
                            weapons.SimpleWeapon)
    multiclass_weapon_proficiencies = weapon_proficiencies
    _multiclass_proficiencies_text = ('simple weapons', 'shortswords',
                                      'unarmed')
    class_skill_choices = ('Acrobatics', 'Athletics', 'History', 'Insight',
                           'Religion', 'Stealth')
    subclasses_available = (OpenHandWay, ShadowWay,
                            FourElementsWay, SunSoulWay,
                            LongDeathWay, DrunkenMasterWay,
                            KenseiWay)
    features_by_level = defaultdict(list)
    features_by_level[1] = [
        features.MonkAbilityScoreImprovement,
        features.UnarmoredDefenseMonk,
        features.MartialArts
    ]
    features_by_level[2] = [features.Ki, features.FlurryOfBlows,
                            features.PatientDefense, features.StepOfTheWind,
                            features.UnarmoredMovement]
    features_by_level[3] = [features.DeflectMissiles]
    features_by_level[4] = [features.SlowFall]
    features_by_level[5] = [features.ExtraAttackMonk, features.StunningStrike]
    features_by_level[6] = [features.KiEmpoweredStrikes]
    features_by_level[7] = [features.Evasion, features.StillnessOfMind]
    features_by_level[10] = [features.PurityOfBody]
    features_by_level[13] = [features.TongueOfTheSunAndMoon]
    features_by_level[14] = [features.DiamondSoul]
    features_by_level[15] = [features.TimelessBody]
    features_by_level[18] = [features.EmptyBody]
    features_by_level[20] = [features.PerfectSelf]

    def __init__(self, level, subclass=None, **params):
        super().__init__(level, subclass=subclass, **params)
        for f in self.features_by_level[1]:
            if isinstance(f, features.MartialArts):
                f.level = self.level
