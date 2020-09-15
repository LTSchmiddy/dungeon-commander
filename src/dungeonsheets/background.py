from dungeonsheets import features as feats


class Background():
    name = "Generic background"
    owner = None
    skill_proficiencies = ()
    chosen_skill_proficiencies = ()
    weapon_proficiencies = ()
    proficiencies_text = ()
    skill_choices = ()
    num_skill_choices = 0
    features = ()
    languages = ()

    def __init__(self, owner=None):
        self.owner = owner
        cls = type(self)
        self.features = tuple([f(owner=self.owner) for f in cls.features])

    def __str__(self):
        return self.name


class Acolyte(Background):
    name = "Acolyte"
    skill_proficiencies = ('insight', 'religion')
    languages = ()
    features = (feats.ShelterOfTheFaithful, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class Charlatan(Background):
    name = "Charlatan"
    skill_proficiencies = ('deception', 'sleight of hand')
    features = (feats.FalseIdentity,)


class Criminal(Background):
    name = "Criminal"
    skill_proficiencies = ('deception', 'stealth')
    features = (feats.CriminalContact,)


class Spy(Criminal):
    name = "Spy"


class Entertainer(Background):
    name = "Entertainer"
    skill_proficiencies = ('acrobatics', 'performance')
    features = (feats.ByPopularDemand,)


class Gladiator(Entertainer):
    name = "Gladiator"


class FolkHero(Background):
    name = "Folk Hero"
    skill_proficiencies = ('animal handling', 'survival')
    features = (feats.RusticHospitality,)


class GuildArtisan(Background):
    name = "Guild Artisan"
    skill_proficiencies = ('insight', 'persuasion')
    languages = ()
    features = (feats.GuildMembership, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class GuildMerchant(GuildArtisan):
    name = "Guild Merchant"


class Hermit(Background):
    name = "Hermit"
    skill_proficiencies = ("medicine", "religion")
    languages = ()
    features = (feats.Discovery, feats.ExtraLanguage)


class Noble(Background):
    name = "Noble"
    skill_proficiencies = ("history", 'persuasion')
    languages = ()
    features = (feats.PositionOfPrivilege, feats.ExtraLanguage)


class Knight(Noble):
    name = "Knight"


class Outlander(Background):
    name = "Outlander"
    skill_proficiencies = ('athletics', 'survival')
    languages = ()
    features = (feats.Wanderer, feats.ExtraLanguage)


class Sage(Background):
    name = "Sage"
    skill_proficiencies = ('arcana', 'history')
    languages = ()
    features = (feats.Researcher, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class Sailor(Background):
    name = "Sailor"
    skill_proficiencies = ('athletics', 'perception')
    features = (feats.ShipsPassage,)


class Pirate(Sailor):
    name = "Pirate"


class Soldier(Background):
    name = "Soldier"
    skill_proficiencies = ('athletics', 'intimidation')
    features = (feats.MilitaryRank,)


class Urchin(Background):
    name = "Urchin"
    skill_proficiencies = ('sleight of hand', 'stealth')
    features = (feats.CitySecrets,)


# Sword's Coast Adventurers Guide
class CityWatch(Background):
    name = "City Watch"
    skill_proficiencies = ('athletics', 'insight')
    languages = ()
    features = (feats.WatchersEye,feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class ClanCrafter(Background):
    name = "Clan Crafter"
    skill_proficiencies = ('history', 'insight')
    languages = ('Dwarvish',)
    features = (feats.RespectOfTheStoutFolk,)


class CloisteredScholar(Background):
    name = "Cloistered Scholar"
    skill_proficiencies = ('history',)
    skill_choices = ('arcana', 'nature', 'religion')
    num_skill_choices = 1
    languages = ()
    features = (feats.LibraryAccess, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class Courtier(Background):
    name = "Courtier"
    skill_proficiencies = ("insight", 'persuasion')
    languages = ()
    features = (feats.CourtFunctionary, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class FactionAgent(Background):
    name = "Faction Agent"
    skill_proficiencies = ('insight',)
    skill_choices = ('animal handling', 'arcana', 'deception',
                     'history', 'intimidation', 'investigation',
                     'medicine', 'nature', 'perception', 'performance',
                     'persuasion', 'religion', 'survival')
    num_skill_choices = 1
    languages = ()
    features = (feats.SafeHaven, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class FarTraveler(Background):
    name = 'Far Traveler'
    skill_proficiencies = ('insight', 'perception')
    languages = ()
    features = (feats.AllEyesOnYou, feats.ExtraLanguage,)


class Inheritor(Background):
    name = "Inheritor"
    skill_proficiencies = ('survival',)
    skill_choices = ('arcana', 'history', 'religion')
    num_skill_choices = 1
    languages = ()
    features = (feats.Inheritance, feats.ExtraLanguage)


class KnightOfTheOrder(Background):
    name = "Knight of the Order"
    skill_proficiencies = ('persuasion',)
    skill_choices = ('arcana', 'history', 'nature', 'religion')
    num_skill_choices = 1
    languages = ()
    features = (feats.KnightlyRegard, feats.ExtraLanguage)


class MercenaryVeteran(Background):
    name = "Mercenary Veteran"
    skill_proficiencies = ('athletics', 'persuasion')
    features = (feats.MercenaryLife,)


class UrbanBountyHunter(Background):
    name = 'Urban Bounty Hunter'
    skill_proficiencies = ()
    skill_choices = ('Deception', 'Insight', 'Persuasion', 'Stealth')
    num_skill_choices = 2
    features = (feats.EarToTheGround,)


class UthgardtTribeMember(Background):
    name = "Uthgardt Tribe Member"
    skill_profifiencies = ('athletics', 'survival')
    languages = ()
    features = (feats.UthgardtHeritage, feats.ExtraLanguage)


class WaterdhavianNoble(Background):
    name = "Waterdhavian Noble"
    skill_proficiencies = ('history', 'persuasion')
    languages = ()
    features = (feats.KeptInStyle, feats.ExtraLanguage)


PHB_backgrounds = [Acolyte, Charlatan, Criminal, Spy, Entertainer,
                   Gladiator, FolkHero, GuildArtisan, GuildMerchant,
                   Hermit, Noble, Knight, Outlander, Sage, Sailor,
                   Pirate, Soldier, Urchin]

SCAG_backgrounds = [CityWatch, ClanCrafter, CloisteredScholar, Courtier,
                    FactionAgent, FarTraveler, Inheritor, KnightOfTheOrder,
                    MercenaryVeteran, UrbanBountyHunter, UthgardtTribeMember,
                    WaterdhavianNoble]

available_backgrounds = PHB_backgrounds + SCAG_backgrounds

__all__ = tuple([b.name for b in available_backgrounds]) + (
    'PHB_backgrounds', 'SCAG_backgrounds', 'available_backgrounds')
