from collections import defaultdict

from dungeonsheets import features, weapons
from dungeonsheets.classes.classes import CharClass, SubClass


# PHB
class BerserkerPath(SubClass):
    """For some barbarians, rage is a means to an end--that end being
    violence. The Path of the Berserker is a path of untrammeled fury, slick
    with blood. As you enter the berserker's rage, you thrill in the chaos of
    battle, heedless of your own health or well-being.

    """
    name = "Path of the Berserker"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.Frenzy]
    features_by_level[6] = [features.MindlessRage]
    features_by_level[10] = [features.IntimidatingPresence]
    features_by_level[14] = [features.Retaliation]


class TotemWarriorPath(SubClass):
    """The Path of the Totem Warrior is a spiritual journey, as the barbarian
    accepts a spirit animal as guide, protector, and inspiration. In battle,
    your totem spirit fills you with supernatural might, adding magical fuel to
    your barbarian rage.

    Most barbarian tribes consider a totem animal to be kin to a particular
    clan. In such cases, it is unusual for an individual to have more than one
    totem animal spirit, though exceptions exist.

    """
    name = "Path of the Totem Warrior"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.SpiritSeeker, features.TotemSpirit]
    features_by_level[6] = [features.BeastAspect]
    features_by_level[10] = [features.SpiritWalker]
    features_by_level[14] = [features.TotemicAttunement]


# SCAG
class BattleragerPath(SubClass):
    """Known as Kuldjargh (literally "axe idiot") in Dwarvish, battleragers are
    dwarf followers of the gods of war and take the Path of the
    Battlerager. They specialize in wearing bulky, spiked armor and throwing
    themselves into combat, striking with their body itself and giving
    themselves over to the fury of battle.

    """
    name = "Path of the Battlerager"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.BattleragerArmor]
    features_by_level[6] = [features.RecklessAbandon]
    features_by_level[10] = [features.BattleragerCharge]
    features_by_level[14] = [features.SpikedRetribution]


# XGTE
class AncestralGuardianPath(SubClass):
    """Some barbarians hail from cultures that revere their ancestors. These
    tribes teach that the warriors of the past linger in the world as mighty
    spirits, who can guide and protect the living. When a barbarian who follows
    this path rages, the barbarian contacts the spirit world and calls on these
    guardian spirits for aid.

    Barbarians who draw on their ancestral guardians can better fight to
    protect their tribes and their allies. In order to cement ties to their
    ancestral guardians, barbarians who follow this path cover themselves in
    elabo- rate tattoos that celebrate their ancestors' deeds. These tattoos
    tell sagas of victories against terrible monsters and other fearsome
    rivals.

    """
    name = "Path of the Ancestral Guardian"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.AncestralProtectors]
    features_by_level[6] = [features.SpiritShield]
    features_by_level[10] = [features.ConsultTheSpirits]
    features_by_level[14] = [features.VengefulAncestors]


class StormHeraldPath(SubClass):
    """All barbarians harbor a fury within. Their rage grants them superior
    strength, durability, and speed. Barbarians who follow the Path of the
    Storm Herald learn to transform that rage into a mantle of primal magic,
    which swirls around them. When in a fury, a barbarian ofthis path taps into
    the forces of nature to create powerful magical effects.

    Storm heralds are typically elite champions who train alongside druids,
    rangers, and others sworn to protect nature. Other storm heralds hone their
    craft in lodges in regions wracked by storms, in the frozen reaches at the
    world's end, or deep in the hottest deserts.

    """
    name = "Path of the Storm Herald"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.StormAura]
    features_by_level[6] = [features.StormSoul]
    features_by_level[10] = [features.ShieldingStorm]
    features_by_level[14] = [features.RagingStorm]


class ZealotPath(SubClass):
    """Some deities inspire their followers to pitch themselves into a ferocious
    battle fury. These barbarians are zealots-warriors who channel their rage
    into powerful disn plays of divine power.

    A variety of gods across the worlds of D&D inspire their followers to
    embrace this path. Tempus from the Forgotten Realms and Hextor and Erythnul
    of Greyhawk are all prime examples. In general, the gods who inspire
    zealots are deities of combat, destruction, and violence. Not all are evil,
    but few are good

    """
    name = "Path of the Zealot"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.DivineFury, features.WarriorOfTheGods]
    features_by_level[6] = [features.FanaticalFocus]
    features_by_level[10] = [features.ZealousPresence]
    features_by_level[14] = [features.RageBeyondDeath]


class Barbarian(CharClass):
    """
    Barbarians, different as they might be, are defined by their rage: unbridled, unquenchable, and unthinking fury.
    More than a mere emotion, their anger is the ferocity of a cornered predator, the unrelenting assault of a storm,
    the churning turmoil of the sea.

    For some, their rage springs from a communion with fierce animal spirits. Others draw from a roiling reservoir of
    anger at a world full of pain. For every barbarian, rage is a power that fuels not just a battle frenzy but also
    uncanny reflexes, resilience, and feats of strength.

    # Primal Instinct
    People of towns and cities take pride in how their civilized ways set them apart from animals, as if denying one’s
    own nature was a mark of superiority. To a barbarian, though, civilization is no virtue, but a sign of weakness.
    The strong embrace their animal nature—keen instincts, primal physicality, and ferocious rage. Barbarians are
    uncomfortable when hedged in by walls and crowds. They thrive in the wilds of their homelands: the tundra, jungle,
    or grasslands where their tribes live and hunt.

    Barbarians come alive in the chaos of combat. They can enter a berserk state where rage takes over, giving them
    superhuman strength and resilience. A barbarian can draw on this reservoir of fury only a few times without resting,
    but those few rages are usually sufficient to defeat whatever threats arise.

    # A Life of Danger
    Not every member of the tribes deemed “barbarians” by scions of civilized society has the barbarian class. A true
    barbarian among these people is as uncommon as a skilled fighter in a town, and he or she plays a similar role as a
    protector of the people and a leader in times of war. Life in the wild places of the world is fraught with peril:
    rival tribes, deadly weather, and terrifying monsters. Barbarians charge headlong into that danger so that their
    people don’t have to.

    Their courage in the face of danger makes barbarians perfectly suited for adventuring. Wandering is often a way of
    life for their native tribes, and the rootless life of the adventurer is little hardship for a barbarian. Some
    barbarians miss the close-knit family structures of the tribe, but eventually find them replaced by the bonds formed
    among the members of their adventuring parties.
    """
    name = 'Barbarian'
    hit_dice_faces = 12
    subclass_select_level = 3
    saving_throw_proficiencies = ('strength', 'constitution')
    primary_abilities = ('strength',)
    weapon_proficiencies = (weapons.SimpleWeapon, weapons.MartialWeapon)
    _proficiencies_text = ('light armor', 'medium armor', 'shields',
                           'simple weapon_list', 'martial weapon_list')
    multiclass_weapon_proficiencies = weapon_proficiencies
    _multiclass_proficiencies_text = ('shields', 'simple weapon_list',
                                      'martial weapon_list')
    class_skill_choices = ('Animal Handling', 'Athletics',
                           'Intimidation', 'Nature', 'Perception', 'Survival')
    subclasses_available = (BerserkerPath, TotemWarriorPath, BattleragerPath,
                            AncestralGuardianPath, StormHeraldPath, ZealotPath)
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.BarbarianAbilityScoreImprovement, features.Rage, features.UnarmoredDefenseBarbarian]
    features_by_level[2] = [features.RecklessAttack, features.DangerSense]
    features_by_level[5] = [features.ExtraAttackBarbarian,
                            features.FastMovement]
    features_by_level[7] = [features.FeralInstinct]
    features_by_level[9] = [features.BrutalCritical]
    features_by_level[11] = [features.RelentlessRage]
    features_by_level[15] = [features.PersistentRage]
    features_by_level[18] = [features.IndomitableMight]
    features_by_level[20] = [features.PrimalChampion]
