from collections import defaultdict

from dungeonsheets import features, weapons
from dungeonsheets.classes.classes import CharClass, SubClass


# Eberron Rising from the Last War
class Alchemist(SubClass):
    """An Alchemist is an expert at combining reagents to produce mystical
    effects. Alchemists use their creations to give life and to leech it away.
    Alchemy is the oldest of artificer traditions, and its versatility has
    long been valued during times of war and peace.
    """

    name = "Alchemist"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.AlchemistToolProficiency,
                            features.AlchemistSpells,
                            features.ExperimentalElixir]
    features_by_level[5] = [features.AlchemicalSavant]
    features_by_level[9] = [features.RestorativeReagents]
    features_by_level[15] = [features.ChemicalMastery]


class Artillerist(SubClass):
    """An Artillerist specializes in using magic to hurl energy, projectiles,
    and explosions on a battlefield. This destructive power was valued by all
    the armies of the Last War. Now that the war is over, some members of this
    specialization have sought to build a more peaceful world by using their
    powers to fight the resurgence of strife in Khorvaire. The gnome artificer
    Vi, an unlikely yet key member of House Cannith's warforged project, has
    been especially vocal about making things right: "It's about time we fixed
    things instead of blowing them all to hell."
    """

    name = "Artillerist"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.ArtilleristSpells,
                            features.ArtilleristToolProficiency,
                            features.EldritchCannon]
    features_by_level[5] = [features.ArcaneFirearm]
    features_by_level[9] = [features.ExplosiveCannon]
    features_by_level[15] = [features.FortifiedPosition]


class BattleSmith(SubClass):
    """Armies require protection, and someone has to put things back together
    if defenses fail. A combination of protector and medic, a Battle Smith is
    an expert at defending others and repairing both material and personnel.
    To aid in their work, Battle Smiths are usually accompanied by a steel
    defender, a protective companion of their own creation. Many soldiers tell
    stories of nearly dying before being saved by a Battle Smith and a steel
    defender.

    Battle Smiths played a key role in House Cannith's work on battle
    constructs and the original warforged, and after the Last War, these
    artificers led efforts to aid those who were injured in the war's horrific
    battles.
    """

    name = "Battle Smith"
    features_by_level = defaultdict(list)
    features_by_level[3] = [features.BattleSmithSpells,
                            features.BattleSmithToolProficiency,
                            features.BattleReady,
                            features.SteelDefender]
    features_by_level[5] = [features.ExtraAttackBattleSmith]
    features_by_level[9] = [features.ArcaneJolt]
    features_by_level[15] = [features.ImprovedDefender]


class Artificer(CharClass):
    """
    Masters of unlocking magic in everyday objects, 
    artificers are supreme inventors. They see magic
    as a complex system waiting to be decoded and
    controlled. Artificers use tools to channel arcane
    power, crafting temporary and permanent
    magical objects. To cast a spell, an artificer could
    use alchemist’s supplies to create a potent elixir,
    calligrapher’s supplies to inscribe a sigil of
    power on an ally’s armor, or tinker’s tools to
    craft a temporary charm. The magic of artificers
    is tied to their tools and their talents.
    
    # Arcane Science
    In the world of Eberron, arcane magic has been 
    harnessed as a form of science and deployed
    throughout society. Artificers reflect this
    development. Their knowledge of magical
    devices, and their ability to infuse mundane
    items with magical energy, allows the grand
    magical projects of Eberron to continue running.
    During the Last War, artificers were marshaled
    on a massive scale. Many lives were saved
    because of the inventions of brave artificers, but
    also countless lives were lost because of the
    mass destruction that artificers’ creations
    unleashed.

    # Seekers of New Lore
    Nothing excites an artificer quite like uncovering 
    a new metal or discovering a source of elemental
    energy. In artificer circles, new inventions and
    strange discoveries create the most excitement.
    Artificers who wish to make a mark must find
    something fresh, rather than uncover someone
    else’s work.
    This drive for novelty pushes artificers to
    become adventurers. Eberron’s main travel
    routes and populated regions have long since
    been explored. Thus, artificers take to the edge
    of civilization in hopes of making the next great
    discovery in arcane research.
    
    """
    name = "Artificer"
    hit_dice_faces = 8
    subclass_select_level = 3
    subclasses_available = (Alchemist, Artillerist, BattleSmith)
    saving_throw_proficiencies = ('intelligence', 'constitution')
    primary_abilities = ('intelligence',)
    _proficiencies_text = (
            'Light armor', 'Medium armor', 'Shields', 'Simple weapons',
            "Thieve's tools", "Tinker's tools",
            "One type of artisan's tools of your choice")
    _multiclass_proficiencies_text = (
            "Light armor", "Medium armor", "Shields",
            "Thieve's tools", "Tinker's tools")
    weapon_proficiencies = (weapons.SimpleWeapon,)
    infusions = []
    class_skill_choices = (
            'Arcana', 'History', 'Investigation',
            'Medicine', 'Nature', 'Perception', 'Sleight of Hand')
    features_by_level = defaultdict(list)
    features_by_level[1] = [features.MagicalTinkering,
                            features.FirearmProficiency,
                            features.ArtificerSpellcasting,
                            features.ArtificerRitualCasting]
    features_by_level[2] = [features.InfuseItem]
    features_by_level[3] = [features.TheRightToolForTheJob]
    features_by_level[6] = [features.ToolExpertise]
    features_by_level[7] = [features.FlashOfGenius]
    features_by_level[10] = [features.MagicItemAdept]
    features_by_level[11] = [features.SpellStoringItem]
    features_by_level[14] = [features.MagicItemSavant]
    features_by_level[18] = [features.MagicItemMaster]
    features_by_level[20] = [features.SoulOfArtifice]
    spellcasting_ability = 'intelligence'
    spell_slots_by_level = {
            1:  (2, 2, 0, 0, 0, 0, 0, 0, 0, 0),
            2:  (2, 2, 0, 0, 0, 0, 0, 0, 0, 0),
            3:  (2, 3, 0, 0, 0, 0, 0, 0, 0, 0),
            4:  (2, 3, 0, 0, 0, 0, 0, 0, 0, 0),
            5:  (2, 4, 2, 0, 0, 0, 0, 0, 0, 0),
            6:  (2, 4, 2, 0, 0, 0, 0, 0, 0, 0),
            7:  (2, 4, 3, 0, 0, 0, 0, 0, 0, 0),
            8:  (2, 4, 3, 0, 0, 0, 0, 0, 0, 0),
            9:  (2, 4, 3, 2, 0, 0, 0, 0, 0, 0),
            10: (3, 4, 3, 2, 0, 0, 0, 0, 0, 0),
            11: (3, 4, 3, 3, 0, 0, 0, 0, 0, 0),
            12: (3, 4, 3, 3, 0, 0, 0, 0, 0, 0),
            13: (3, 4, 3, 3, 1, 0, 0, 0, 0, 0),
            14: (4, 4, 3, 3, 1, 0, 0, 0, 0, 0),
            15: (4, 4, 3, 3, 2, 0, 0, 0, 0, 0),
            16: (4, 4, 3, 3, 2, 0, 0, 0, 0, 0),
            17: (4, 4, 3, 3, 3, 1, 0, 0, 0, 0),
            18: (4, 4, 3, 3, 3, 1, 0, 0, 0, 0),
            19: (4, 4, 3, 3, 3, 2, 0, 0, 0, 0),
            20: (4, 4, 3, 3, 3, 2, 0, 0, 0, 0)
            }
