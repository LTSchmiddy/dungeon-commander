import dungeonsheets

from dungeonsheets.features import *

class ConstructedResilience(dungeonsheets.features.Feature):
    """
    You were created to have remarkable fortitude, represented by the following benefits:
    * You have advantage on saving throws against being poisoned, and you have resistance to poison damage.
    * You don’t need to eat, drink, or breathe.
    * You are immune to disease.
    * You don't need to sleep, and magic can't put you to sleep.
    * Warforged show no signs of deterioration due to age. You are immune to magical aging effects.
    """
    name = "Constructed Resilience"
    source = "Warforged"

class SentrysRest(dungeonsheets.features.Feature):
    """
    When you take a long rest, you must spend at least six hours in an inactive, motionless state,
    rather than sleeping. In this state, you appear inert, but it doesn’t render you unconscious,
    and you can see and hear as normal.
    """
    name = "Sentry's Rest"
    source = "Warforged"

class IntegratedProtection(dungeonsheets.features.Feature):
    """
    Sentry's Rest. When you take a long rest, you must spend at least six hours in an inactive,
    motionless state, rather than sleeping. In this state, you appear inert, but it doesn’t
    render you unconscious, and you can see and hear as normal.
    """
    name = "Integrated Protection"
    source = "Warforged"

class Warforged(dungeonsheets.race.Race):
    """
    The Warforged were built to fight in the Last War. The first Warforged were mindless automatons, but House
    Cannith devoted vast resources to improving these steel soldiers. An unexpected breakthrough produced fully
    sentient soldiers, blending organic and inorganic materials. Warforged are made from wood and metal, but they
    can feel pain and emotion. Built as weapon_list, they must now find a purpose beyond the war. A Warforged can be a
    steadfast ally, a cold-hearted killing machine, or a visionary in search of purpose and meaning.
    """
    name = "Warforged"
    size = "medium"
    speed = 30
    constitution_bonus = 2
    languages = ("Common",)
    features = (
        ExtraLanguageRace,
        ExtraToolProficiency,
        ExtraSkillRace,
        ConstructedResilience,
        SentrysRest,
        IntegratedProtection
    )

setattr(dungeonsheets.race, 'Warforged', Warforged)
dungeonsheets.race.available_races += (Warforged,)