from collections import defaultdict

from dungeonsheets import spells
from dungeonsheets import features
from dungeonsheets.features.artificer import _SpecialistSpells
from dungeonsheets.classes.classes import SubClass
from dungeonsheets.classes.artificer import Artificer


# addons.artificer_extended.additional_spells
# print(dir(addons.artificer_extended.additional_spells))

# Armorer Features:
class ArmorerToolProficiency(features.Feature):
    """When you adopt this specialization at 3rd level, you gain proficiency with heavy armor. You also gain proficiency
     with smith’s tools. If you already have this tool proficiency, you gain proficiency with one other type of
     artisan’s tools of your choice."""
    name = "Tool Proficiency"
    source = "Artificer (Armorer)"

class ArmorerSpells(_SpecialistSpells):
    """Starting at 3rd level, you always have certain spells prepared after you reach particular levels in this class,
    as shown in the Armorer Spells table. These spells count as artificer spells for you, but they don’t count against
    the number of artificer spells you prepare.
    """

    _name = "Armorer"
    # source = "Artificer (Armorer)"
    _specialist_spells = {
            3: [spells.MagicMissile, spells.Shield],
            5: [spells.MirrorImage, spells.Shatter],
            9: [spells.HypnoticPattern, spells.LightningBolt],
            13: [spells.FireShield, spells.GreaterInvisibility],
            17: [spells.Passwall, spells.WallOfForce]
            }


class PowerArmor(features.Feature):
    """Beginning at 3rd level, your metallurgical pursuits have led to you making armor a conduit for your artificer
    magic. As an action, you can turn a suit of heavy armor you are wearing into power armor, provided you have smith’s
    tools in hand. You gain the following benefits while wearing the power armor:

    * If the armor normally has a Strength requirement, the power armor lacks this requirement for you.
    * You can use the power armor as a spellcasting focus for your artificer spells.
    * The power armor attaches to you and can’t be removed against your will. It also expands to cover your entire body,
    and it replaces any missing limbs, functioning identically to a body part it is replacing.

    The armor continues to be power armor until you doff it, you don another suit of armor, or you die.

    **Armor Model**
    Beginning at 3rd level, you can customize your power armor. When you do so, choose one of the following armor
    models: guardian or infiltrator. The model you choose gives you special benefits while you wear it.

    Each model includes a special weapon. When you attack with that weapon, you can use your Intelligence modifier,
    instead of Strength or Dexterity, for the attack and damage rolls. You can change your power armor's model whenever
    you finish a short or long rest, provided you have smith's tools in hand.

    **Model: Guardian**
    You design your armor to be in the frontline of conflict. It has the following features:

    * *Thunder Gauntlets*. Your armored fists each count as a simple melee weapon, and each deals 1d8 thunder damage on a
    hit. A creature hit by the gauntlet has disadvantage on attack rolls against targets other than you until the start
    of your next turn, as the armor magically emits a distracting pulse when the creature attacks someone else.

    * *Defensive Field*. You gain a bonus action that you can use on each of your turns to gain temporary hit points equal
    to your level in this class, replacing any temporary hit points you already have. You lose these temporary hit
    points if you doff the armor.

    **Model: Infiltrator**
    You customize your armor for subtle undertakings. It has the following features:

    * *Lightning Launcher*. A gemlike node appears on one of your armored fists or on the chest (your choice). It counts as
    a simple ranged weapon, with a normal range of 90 feet and a long range of 300 feet, and it deals 1d6 lightning
    damage on a hit. Once on each of your turns when you hit a creature with it, you can deal an extra 1d6 lightning
    damage to that target.

    * *Powered Steps*. Your walking speed increases by 5 feet.

    * *Second Skin*. The armor’s weight is negligible, and it becomes formfitting and wearable under clothing. If the armor
    normally imposes disadvantage on Dexterity (Stealth) checks, the power armor doesn’t.
    """
    name = "Power Armor"
    source = "Artificer (Armorer)"


class ExtraAttackArmorer(features.Feature):
    """Starting at 5th level, you can attack twice, rather than once, whenever you take the Attack action on your turn."""
    name = "Extra Attack"
    source = "Artificer (Armorer)"

class ArmorModifications(features.Feature):
    """
    At 9th level, you learn how to use your artificer infusions to specially modify the armor enhanced by your Power
    Armor feature. That armor now counts as separate items for the purposes of your Infuse Items feature: armor (the
    chest piece), boots, bracers, and a weapon. Each of those items can bear one of your infusions. In addition, the
    maximum number of items you can infuse at once increases by 2, but those extra items must be part of your power
    armor.
    """
    name = "Armor Modifications"
    source = "Artificer (Armorer)"

class PerfectedArmor(features.Feature):
    """
    At 15th level, Your power armor gains additional benefits based on its model, as shown below.

    **Model: Guardian**. Tinkering with your armor's energy system leads you to discover a powerful pulling force. When a
    creature you can see ends its turn within 30 feet of you, you can use your reaction to force the creature to succeed
    on a Strength saving throw against your spell save DC or be pulled up to 30 feet toward you to an unoccupied space.
    If you pull the target to space within 5 feet of you, you can make a melee weapon attack against it as part of
    this reaction.

    You can use this reaction a number of times equal to your Intelligence modifier (minimum of once). You regain all
    expended uses of it when you finish a long rest.

    **Model: Infiltrator**. Any creature that takes lightning damage from your Lightning Launcher glimmers with light
    until the start of your next turn. The glimmering creature sheds dim light in a 5 foot radius, and the next attack
    roll against it by a creature other than you has advantage. If that attack hits, it deals an extra 1d6 lightning
    damage.
    """

# Armorer Subclass
class Armorer (SubClass):
    """An artificer who specializes as an Armorer modifies armor to function almost like a second skin.
    The armor is enhanced to hone the artificer’s magic, unleash potent attacks, and generate a formidable defense.
    The artificer bonds with this armor, becoming one with it even as they experiment with it and refine its magical
    capabilities.
    """

    name = "Armorer"
    features_by_level = defaultdict(list)
    features_by_level[3] = [ArmorerToolProficiency,
                            ArmorerSpells, PowerArmor]
    features_by_level[5] = [ExtraAttackArmorer]
    features_by_level[9] = [ArmorModifications]
    features_by_level[15] = [PerfectedArmor]


Artificer.subclasses_available += (Armorer,)