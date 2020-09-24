import inspect

from dungeonsheets.features.features import Feature, create_feature
class BasicAbilityScoreImprovement(Feature):
    """
    When you reach 4th level, and again at 8th, 12th, 16th, and 19th level, you can increase one ability score of your
    choice by 2, or you can increase two ability scores of your choice by 1. As normal, you can’t increase an ability
    score above 20 using this feature.

    Using the optional feats rule, you can forgo taking this feature to take a feat of your choice instead.
    """
    name = "Ability Score Improvement"
    source = "Character"

from dungeonsheets.features.prof_choices import *

from dungeonsheets.features.artificer import *
from dungeonsheets.features.backgrounds import *
from dungeonsheets.features.barbarian import *
from dungeonsheets.features.bard import *
from dungeonsheets.features.cleric import *
from dungeonsheets.features.druid import *
from dungeonsheets.features.feats import *
from dungeonsheets.features.fighter import *
from dungeonsheets.features.monk import *
from dungeonsheets.features.paladin import *
from dungeonsheets.features.races import *
from dungeonsheets.features.ranger import *
from dungeonsheets.features.rogue import *
from dungeonsheets.features.sorceror import *
from dungeonsheets.features.warlock import *
from dungeonsheets.features.wizard import *

