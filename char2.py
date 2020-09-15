"""This file describes the heroic adventurer GuyMan.

Modify this file as you level up and then re-generate the character
sheet by running ``makesheets`` from the command line.

"""

dungeonsheets_version = "dc_1"

name = "GuyMan"
player_name = ""

# Be sure to list Primary class first
classes = ['Wizard']  # ex: ['Wizard'] or ['Rogue', 'Fighter']
levels = [5]  # ex: [10] or [3, 2]
subclasses = ["School of Evocation"]  # ex: ['Necromacy'] or ['Thief', None]
background = "Spy"
race = "High Elf"
alignment = "Neutral"

xp = 0
hp_max = 22
hp_current = 22
inspiration = False  # boolean inspiration value

# Ability Scores
strength = 8
dexterity = 14
constitution = 10
intelligence = 15
wisdom = 12
charisma = 10

# Select what skills you're proficient with
# ex: skill_proficiencies = ('athletics', 'acrobatics', 'arcana')
skill_proficiencies = []

# Any skills you have "expertise" (Bard/Rogue) in
skill_expertise = []

# Named features / feats that aren't part of your classes, race, or background.
# Also include Eldritch Invocations and features you make multiple selection of
# (like Maneuvers for Fighter, Metamagic for Sorcerors, Trick Shots for
# Gunslinger, etc.)
# Example:
# features = ('Tavern Brawler',) # take the optional Feat from PHB
features = []

# If selecting among multiple feature options: ex Fighting Style
# Example (Fighting Style):
# feature_choices = ('Archery',)
feature_choices = []

# Weapons/other proficiencies not given by class/race/background
weapon_proficiencies = ()
_proficiencies_text = []

# Proficiencies and languages
languages = """"""

# Inventory
# TODO: Get yourself some money
cp = 0
sp = 0
ep = 0
gp = 0
pp = 0

# TODO: Put your equipped weapons and armor here
weapons = ["PoopAxe"]  # Example: ('shortsword', 'longsword')
magic_items = ["bag_of_holding"]  # Example: ('ring of protection',)
armor = "None"  # Eg "leather armor"
shield = "None"  # Eg "shield"

equipment = """"""

attacks_and_spellcasting = """"""

# List of known spells
# Example: spells = ('magic missile', 'mage armor')
spells = ("Fire Bolt",)

# Which spells have been prepared (not including cantrips)
spells_prepared = []

# Wild shapes for Druid
wild_shapes = ()  # Ex: ('ape', 'wolf', 'ankylosaurus')

# Infusions for Artificer
infusions = () # Ex: ('repeating shot', 'replicate magic item')

# Backstory
# Describe your backstory here
personality_traits = """TODO: Describe how your character behaves, interacts with others"""

ideals = """TODO: Describe what values your character believes in."""

bonds = """TODO: Describe your character's commitments or ongoing quests."""

flaws = """TODO: Describe your character's interesting flaws."""

features_and_traits = """Describe any other features and abilities."""

info_dict = {'feature__ElfCantrip': 'Spell'}