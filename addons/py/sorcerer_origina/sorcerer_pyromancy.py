from collections import defaultdict

from dungeonsheets.features import Feature
from dungeonsheets.classes.classes import SubClass
from dungeonsheets.classes.sorcerer import Sorcerer



class HeartOfFire(Feature):
    """At 1st level, whenever you start casting a spell of 1st level or higher that deals fire damage, fiery magic
    erupts from you. This eruption causes creatures of your choice that you can see within 10 feet of you to take fire
    damage equal to half your sorcerer level (minimum of 1)."""
    name = "Heart of Fire"
    source = "Sorcerer (Pyromancy)"


class FireInIheVeins(Feature):
    """At 6th level, you gain resistance to fire damage. In addition, spells you cast ignore resistance to fire damage."""
    name = "Fire In Ihe Veins"
    source = "Sorcerer (Pyromancy)"


class PyromancersFury(Feature):
    """Starting at 14th level, when you are hit by a melee attack, you can use your reaction to deal fire damage to the
    attacker. The damage equals your sorcerer level, and ignores resistance to fire damage."""
    name = "Pyromancer's Fury"
    source = "Sorcerer (Pyromancy)"


class FierySoul(Feature):
    """At 18th level, you gain immunity to fire damage. In addition, any spell or effect you create ignores resistance
    to fire damage and treats immunity to fire damage as resistance to fire damage."""
    name = "Fiery Soul"
    source = "Sorcerer (Pyromancy)"


class Pyromancy(SubClass):
    """Your innate magic manifests in fire. You are your fire, and your fire is you."""
    name = "Pyromancy"

    features_by_level = defaultdict(list)
    features_by_level[1] = [HeartOfFire]
    features_by_level[6] = [FireInIheVeins]
    features_by_level[14] = [PyromancersFury]
    features_by_level[18] = [FierySoul]

Sorcerer.subclasses_available += (Pyromancy,)