import inspect

import markdown2

from dungeonsheets import features as feats

class Background:
    """
    A generic background. A blank slate, as it were.
    """
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

    starting_equipment = ""
    characteristics = ()

    article_link = ""


    def __init__(self, owner=None):
        self.owner = owner
        cls = type(self)
        self.features = tuple([f(owner=self.owner) for f in cls.features])

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return self.get_id()

    @classmethod
    def get_id(cls):
        return cls.__name__

    @classmethod
    def get_desc(cls):
        return inspect.getdoc(cls)

    @classmethod
    def get_desc_html(cls):
        return markdown2.markdown(inspect.getdoc(cls)).strip()

    @property
    def desc_html(self):
        return self.get_desc_html()

    @property
    def desc(self):
        return self.get_desc()



class Acolyte(Background):
    """
    You have spent your life in the service of a temple to a specific god or pantheon of gods. You act as an
    intermediary between the realm of the holy and the mortal world, performing sacred rites and offering
    sacrifices in order to conduct worshipers into the presence of the divine. You are not necessarily a cleric –
    performing sacred rites is not the same thing as channeling divine power.

    Choose a god, a pantheon of gods, or some other quasi-divine being, and work with your DM to detail the nature of
    your religious service. Were you a lesser functionary in a temple, raised from childhood to assist the priests in
    the sacred rites? Or were you a high priest who suddenly experienced a call to serve your god in a different way?
    Perhaps you were the leader of a small cult outside of any established temple structure, or even an occult group
    that served a fiendish master that you now deny.

    Acolytes are shaped by their experience in temples or other religious communities. Their study of the history and
    tenets of their faith and their relationships to temples, shrines, or hierarchies affect their mannerisms and
    ideals. Their flaws might be some hidden hypocrisy or heretical idea, or an ideal or bond taken to an extreme.
    """
    name = "Acolyte"
    skill_proficiencies = ('insight', 'religion')
    languages = ()
    features = (feats.ShelterOfTheFaithful, feats.ExtraLanguage, feats.AdditionalExtraLanguage)
    starting_equipment = "A holy symbol (a gift to you when you entered the priesthood), a prayer book or prayer wheel," \
                         " 5 sticks of incense, vestments, a set of common clothes, and a belt pouch containing 15 gp"
    # article_link = "http://dnd5e.wikidot.com/background:acolyte"

class Charlatan(Background):
    """
    You have always had a way with people. You know what makes them tick, you can tease out their hearts' desires after
    a few minutes of conversation, and with a few leading questions you can read them like they were children's books.
    It's a useful talent, and one that you're perfectly willing to use for your advantage.

    You know what people want and you deliver, or rather, you promise to deliver. Common sense should steer people
    away from things that sound too good to be true, but common sense seems to be in short supply when you're around.
    The bottle of pink colored liquid will surely cure that unseemly rash, this ointment – nothing more than a bit of
    fat with a sprinkle of silver dust can restore youth and vigor, and there's a bridge in the city that just happens
    to be for sale. These marvels sound implausible, but you make them sound like the real deal.

    Charlatans are colorful characters who conceal their true selves behind the masks they construct. They reflect
    what people want to see, what they want to believe, and how they see the world. But their true selves are sometimes
    plagued by an uneasy conscience, an old enemy, or deep-seated trust issues.
    """
    name = "Charlatan"
    skill_proficiencies = ('deception', 'sleight of hand')
    proficiencies_text = ('Disguise kit', 'Forgery kit')
    starting_equipment = "A set of fine clothes, a disguise kit, tools of the con of your choice (ten stoppered bottles" \
                         " filled with colored liquid, a set of weighted dice, a deck of marked cards, or a signet ring " \
                         "of an imaginary duke), and a belt pouch containing 15 gp"
    features = (feats.FalseIdentity,)
    # article_link = "http://dnd5e.wikidot.com/background:charlatan"


class Criminal(Background):
    """
    You are an experienced criminal with a history of breaking the law. You have spent a lot of time among other
    criminals and still have contacts within the criminal underworld. You're far closer than most people to the
    world of murder, theft, and violence that pervades the underbelly of civilization, and you have survived up to
    this point by flouting the rules and regulations of society.

    Criminals might seem like villains on the surface, and many of them are villainous to the core. But some have an
    abundance of endearing, if not redeeming, characteristics. There might be honor among thieves, but criminals rarely
    show any respect for law or authority.
    """
    name = "Criminal"
    skill_proficiencies = ('deception', 'stealth')
    proficiencies_text = ("thieves' tools",)
    starting_equipment = "A crowbar, a set of dark common clothes including a hood, and a belt pouch containing 15 gp"
    features = (feats.CriminalContact, feats.GamingSetProficiency)


class Spy(Criminal):
    """
    Although your capabilities are not much different from those of a burglar or smuggler, you learned and practiced
    them in a very different context: as an espionage agent. You might have been an officially sanctioned agent of the
    crown, or perhaps you sold the secrets you uncovered to the highest bidder.

    Spies might seem like villains on the surface, and many of them are villainous to the core. But some have an
    abundance of endearing, if not redeeming, characteristics. There might be honor among thieves, but criminals rarely
    show any respect for law or authority.
    """
    name = "Spy"

class SpyRevised(Spy):
    name = "Spy Revised"
    skill_proficiencies = ('persuasion', 'stealth')
    features = (feats.CriminalContact, feats.ExtraToolProficiency)


class Entertainer(Background):
    """
    You thrive in front of an audience. You know how to entrance them, entertain them, and even inspire them.
    Your poetics can stir the hearts of those who hear you, awakening grief or joy, laughter or anger. Your music
    raises their spirits or captures their sorrow. Your dance steps captivate, your humor cuts to the quick. Whatever
    techniques you use, your art is your life.

    Successful entertainers have to be able to capture and hold an audience's attention, so they tend to have
    flamboyant or forceful personalities. They're inclined toward the romantic and often cling to high-minded ideals
    about the practice of art and the appreciation of beauty.
    """
    name = "Entertainer"
    skill_proficiencies = ('acrobatics', 'performance')
    proficiencies_text = ("Disguise kit",)
    starting_equipment = "A musical instrument (one of your choice), the favor of an admirer (love letter, lock of hair," \
                         " or trinket), a costume, and a belt pouch containing 15 gp"
    features = (feats.ByPopularDemand, feats.InstrumentProficiency)


class Gladiator(Entertainer):
    """
    A gladiator is as much an entertainer as any minstrel or circus performer trained to make the arts of combat into a
    spectacle the crowd can enjoy. This kind of flashy combat is your entertainer routine, though you might also have
    some skills as a tumbler or actor. Using your By Popular Demand feature, you can find a place to perform in any
    place that features combat for entertainment-perhaps a gladiatorial arena or secret pit fighting club. You can
    replace the musical instrument in your equipment package with an inexpensive but unusual weapon, such as a trident
    or net.

    Successful entertainers have to be able to capture and hold an audience's attention, so they tend to have
    flamboyant or forceful personalities. They're inclined toward the romantic and often cling to high-minded ideals
    about the practice of art and the appreciation of beauty.
    """
    name = "Gladiator"


class FolkHero(Background):
    """
    You come from a humble social rank, but you are destined for so much more. Already the people of your home village
    regard you as their champion, and your destiny calls you to stand against the tyrants and monsters that threaten
    the common folk everywhere.

    A folk hero is one of the common people, for better or for worse. Most folk heroes look on their humble origins as
    a virtue, not a shortcoming, and their home communities remain very important to them.
    """
    name = "Folk Hero"
    skill_proficiencies = ('animal handling', 'survival')
    proficiencies_text = ("vehicles (land)",)
    starting_equipment = "A set of artisan's tools (one of your choice), a shovel, an iron pot, a set of common " \
                         "clothes, and a belt pouch containing 10 gp"
    features = (feats.RusticHospitality, feats.ExtraToolProficiency)


class GuildArtisan(Background):
    """
    You are a member of an artisan's guild, skilled in a particular field and closely associated with other artisans.
    You are a well-established part of the mercantile world, freed by talent and wealth from the constraints of a feudal
    social order. You learned your skills as an apprentice to a master artisan, under the sponsorship of your guild,
    until you became a master in your own right.

    Guild artisans are among the most ordinary people in the world until they set down their tools and take up an
    adventuring career. They understand the value of hard work and the importance of community, but they're vulnerable
    to sins of greed and covetousness.
    """
    name = "Guild Artisan"
    skill_proficiencies = ('insight', 'persuasion')
    languages = ()
    starting_equipment = "A set of artisan's tools (one of your choice), a shovel, an iron pot, a set of common" \
                         " clothes, and a belt pouch containing 10 gp"
    features = (feats.GuildMembership, feats.ExtraLanguage, feats.ExtraToolProficiency)


class GuildMerchant(GuildArtisan):
    """
    Instead of an artisans' guild, you might belong to a guild of traders, caravan masters, or shopkeepers. You don't
    craft items yourself but earn a living by buying and selling the works of others (or the raw materials artisans
    need to practice their craft). Your guild might be a large merchant consortium (or family) with interests across
    the region. Perhaps you transported goods from one place to another, by ship, wagon, or caravan, or bought them
    from traveling traders and sold them in your own little shop. In some ways, the traveling merchant's life lends
    itself to adventure far more than the life of an artisan.

    Rather than proficiency with artisan's tools, you might be proficient with navigator's tools or an additional
    language. And instead of artisan's tools, you can start with a mule and a cart

    Guild artisans are among the most ordinary people in the world until they set down their tools and take up an
    adventuring career. They understand the value of hard work and the importance of community, but they're vulnerable
    to sins of greed and covetousness.
    """
    name = "Guild Merchant"

class GuildMerchantTwoLanguages(GuildMerchant):
    name = "Guild Merchant (Two Languages)"
    features = (feats.GuildMembership, feats.ExtraLanguage, feats.AdditionalExtraLanguage)

class Hermit(Background):
    """
    You lived in seclusion – either in a sheltered community such as a monastery, or entirely alone –
    for a formative part of your life. In your time apart from the clamor of society, you found quiet,
    solitude, and perhaps some of the answers you were looking for.

    Some hermits are well suited to a life of seclusion, whereas others chafe against it and long for company. Whether
    they embrace solitude or long to escape it, the solitary life shapes their attitudes and ideals. A few are driven
    slightly mad by their years apart from society.
    """
    name = "Hermit"
    skill_proficiencies = ("medicine", "religion")
    proficiencies_text = ("Herbalism kit",)
    languages = ()
    starting_equipment = "A scroll case stuffed full of notes from your studies or prayers, a winter blanket, a set " \
                         "of common clothes, an herbalism kit, and 5 gp"
    features = (feats.Discovery, feats.ExtraLanguage)


class Noble(Background):
    """
    You understand wealth, power, and privilege. You carry a noble title, and your family owns land, collects taxes,
    and wields significant political influence. You might be a pampered aristocrat unfamiliar with work or discomfort,
    a former merchant just elevated to the nobility, or a disinherited scoundrel with a disproportionate sense of
    entitlement. Or you could be an honest, hard-working landowner who cares deeply about the people who live and work
    on your land, keenly aware of your responsibility to them.

    Work with your DM to come up with an appropriate title and determine how much authority that title carries. A noble
    title doesn't stand on its own-it's connected to an entire family, and whatever title you hold, you will pass it
    down to your own children. Not only do you need to determine your noble title, but you should also work with the DM
    to describe your family and their influence on you.

    Is your family old and established, or was your title only recently bestowed? How much influence do they wield, and
    over what area? What kind of reputation does your family have among the other aristocrats of the region? How do the
    common people regard them?

    What's your position in the family? Are you the heir to the head of the family? Have you already inherited the
    title? How do you feel about that responsibility? Or are you so far down the line of inheritance that no one cares
    what you do, as long as you don't embarrass the family? How does the head of your family feel about your adventuring
    career? Are you in your family's good graces, or shunned by the rest of your family?

    Does your family have a coat of arms? An insignia you might wear on a signet ring? Particular colors you wear all
    the time? An animal you regard as a symbol of your line or even a spiritual member of the family?

    These details help establish your family and your title as features of the world of the campaign.

    Nobles are born and raised to a very different lifestyle than most people ever experience, and their personalities
    reflect that upbringing. A noble title comes with a plethora of bonds –responsibilities to family, to other nobles
    (including the sovereign), to the people entrusted to the family's care, or even to the title itself. But this
    responsibility is often a good way to undermine a noble.
    """
    name = "Noble"
    skill_proficiencies = ("history", 'persuasion')
    languages = ()
    starting_equipment = "A set of fine clothes, a signet ring, a scroll of pedigree, and a purse containing 25 gp"
    features = (feats.PositionOfPrivilege, feats.ExtraLanguage, feats.GamingSetProficiency)


class Knight(Noble):
    """
    A knighthood is among the lowest noble titles in most societies, but it can be a path to higher status. If you wish
    to be a knight, choose the Retainers feature below instead of the Position of Privilege feature. One of your
    commoner retainers is replaced by a noble who serves as your squire, aiding you in exchange for training on his or
    her own path to knighthood. Your two remaining retainers might include a groom to care for your horse and a servant
    who polishes your armor (and even helps you put it on).

    As an emblem of chivalry and the ideals of courtly love, you might include among your equipment a banner or other
    token from a noble lord or lady to whom you have given your heart – in a chaste sort of devotion. (This person
    could be your bond.)
    """
    name = "Knight"


class Outlander(Background):
    """
    You grew up in the wilds, far from civilization and the comforts of town and technology. You've witnessed the
    migration of herds larger than forests, survived weather more extreme than any city-dweller could comprehend, and
    enjoyed the solitude of being the only thinking creature for miles in any direction. The wilds are in your blood,
    whether you were a nomad, an explorer, a recluse, a hunter-gatherer, or even a marauder. Even in places where you
    don't know the specific features of the terrain, you know the ways of the wild.

    Often considered rude and uncouth among civilized folk, outlanders have little respect for the niceties of life in
    the cities. The ties of tribe, clan, family, and the natural world of which they are a part are the most important
    bonds to most outlanders.
    """
    name = "Outlander"
    skill_proficiencies = ('athletics', 'survival')
    languages = ()
    proficiencies_text = ()
    starting_equipment = "A staff, a hunting trap, a trophy from an animal you killed, a set of traveler's clothes, " \
                         "and a belt pouch containing 10 gp"
    features = (feats.Wanderer, feats.ExtraLanguage, feats.InstrumentProficiency)


class Sage(Background):
    """
    You spent years learning the lore of the multiverse. You scoured manuscripts, studied scrolls, and listened to the
    greatest experts on the subjects that interest you. Your efforts have made you a master in your fields of study.

    Sages arc defined by their extensive studies, and their characteristics reflect this life of study. Devoted to
    scholarly pursuits, a sage values knowledge highly – sometimes in its own right, sometimes as a means toward other
    ideals.
    """
    name = "Sage"
    skill_proficiencies = ('arcana', 'history')
    languages = ()
    starting_equipment = "A bottle of black ink, a quill, a small knife, a letter from a dead colleague posing a" \
                         " question you have not yet been able to answer, a set of common clothes, and a belt pouch containing 10 gp"
    features = (feats.Researcher, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class Sailor(Background):
    """
    You sailed on a seagoing vessel for years. In that time, you faced down mighty storms, monsters of the deep, and
    those who wanted to sink your craft to the bottomless depths. Your first love is the distant line of the horizon,
    but the time has come to try your hand at something new.

    Discuss the nature of the ship you previously sailed with your DM. Was it a merchant ship, a naval vessel, a ship
    of discovery, or a pirate ship? How famous (or infamous) is it? Is it widely traveled? Is it still sailing, or is
    it missing and presumed lost with all hands?

    What were your duties on board – boatswain, captain, navigator, cook, or some other position? Who were the captain
    and first mate? Did you leave your ship on good terms with your fellows, or on the run?

    Sailors can be a rough lot, but the responsibilities of life on a ship make them generally reliable as well. Life
    aboard a ship shapes their outlook and forms their most important attachments.
    """
    name = "Sailor"
    skill_proficiencies = ('athletics', 'perception')
    proficiencies_text = ("Navigator's tools", "Vehicles (Water)")
    starting_equipment = "A belaying pin (club), 50 feet of silk rope, a lucky charm such as a rabbit foot or a s" \
                         "mall stone with a hole in the center (or you may roll for a random trinket on the Trinkets " \
                         "table in chapter 5), a set of common clothes, and a belt pouch containing 10 gp"
    features = (feats.ShipsPassage,)


class Pirate(Sailor):
    """
    You spent your youth under the sway of a dread pirate, a ruthless cutthroat who taught you how to survive in a
    world of sharks and savages. You've indulged in larceny on the high seas and sent more than one deserving soul
    to a briny grave. Fear and bloodshed are no strangers to you, and you've garnered a somewhat unsavory reputation
    in many a port town.

    If you decide that your sailing career involved piracy, you can choose the Bad Reputation feature below instead of
    the Ship's Passage feature.
    """
    name = "Pirate"

class PirateBadReputation(Pirate):
    name = "Pirate (Bad Reputation)"
    features = (feats.BadReputation,)


class Soldier(Background):
    """
    War has been your life for as long as you care to remember. You trained as a youth, studied the use of weapon_list and
    armor, learned basic survival techniques, including how to stay alive on the battlefield. You might have been part
    of a standing national army or a mercenary company, or perhaps a member of a local militia who rose to prominence
    during a recent war.

    When you choose this background, work with your DM to determine which military organization you were a part of, how far
    through its ranks you progressed, and what kind of experiences you had during your military career. Was it a standing
    army, a town guard, or a village militia? Or it might have been a noble's or merchant's private army, or a mercenary
    company.

    The horrors of war combined with the rigid discipline of military service leave their mark on all soldiers,
    shaping their ideals, creating strong bonds, and often leaving them scarred and vulnerable to fear, shame,
    and hatred.
    """
    name = "Soldier"
    skill_proficiencies = ('athletics', 'intimidation')
    proficiencies_text = ('Vehicles (Land)',)
    features = (feats.MilitaryRank, feats.GamingSetProficiency)


class Urchin(Background):
    """
    You grew up on the streets alone, orphaned, and poor, You had no one to watch over you or to provide for you, so
    you learned to provide for yourself. You fought fiercely over food and kept a constant watch out for other
    desperate souls who might steal from you. You slept on rooftops and in alleyways, exposed to the elements, and
    endured sickness without the advantage of medicine or a place to recuperate. You've survived despite all odds,
    and did so through cunning, strength, speed, or some combination of each.

    You begin your adventuring career with enough money to live modestly but securely for at least ten days. How did
    you come by that money? What allowed you to break free of your desperate circumstances and embark on a better life?

    Urchins are shaped by lives of desperate poverty, for good and for ill. They tend to be driven either by a
    commitment to the people with whom they shared life on the street or by a burning desire to find a better life
    and maybe get some payback on all the rich people who treated them badly.
    """
    name = "Urchin"
    skill_proficiencies = ('sleight of hand', 'stealth')
    proficiencies_text = ("Disguise kit", "Thieves' tools")
    starting_equipment = "A small knife, a map of the city you grew up in, a pet mouse, a token to remember your " \
                         "parents by, a set of common clothes, and a belt pouch containing 10 gp"
    features = (feats.CitySecrets,)


# Sword's Coast Adventurers Guide
class CityWatch(Background):
    """
    You have served the community where you grew up, standing as its first line of defense against crime. You aren't
    a soldier, directing your gaze outward at possible enemies. Instead, your service to your hometown was to help
    police its populace, protecting the citizenry from lawbreakers and malefactors of every stripe.

    You might have been part of the City Watch of Waterdeep, the baton-wielding police force of the City of
    Splendors, protecting the common folk from thieves and rowdy nobility alike. Or you might have been one of the
    valiant defenders of Silverymoon, a member of the Silverwatch or even one of the magic-wielding Spellguard.

    Perhaps you hail from Neverwinter and have served as one of its Wintershield watchmen, the newly founded branch of
    guards who vow to keep safe the City of Skilled Hands.

    Even if you're not city-born or city-bred, this background can describe your early years as a member of law
    enforcement. Most settlements of any size have their own constables and police forces, and even smaller communities
    have sheriffs and bailiffs who stand ready to protect their community.
    """
    name = "City Watch"
    skill_proficiencies = ('athletics', 'insight')
    languages = ()
    starting_equipment = "A uniform in the style of your unit and indicative of your rank, a horn with which to " \
                         "summon help, a set of manacles, and a pouch containing 10 gp"
    features = (feats.WatchersEye, feats.ExtraLanguage, feats.AdditionalExtraLanguage)

class Investigator(CityWatch):
    """
    Rarer than watch or patrol members are a community's investigators, who are responsible for solving crimes after
    the fact. Though such folk are seldom found in rural areas, nearly every settlement of decent size has at least one
    or two watch members who have the skill to investigate crime scenes and track down criminals. If your prior
    experience is as an investigator, you have proficiency in Investigation rather than Athletics.

    Even if you're not city-born or city-bred, this background can describe your early years as a member of law
    enforcement. Most settlements of any size have their own constables and police forces, and even smaller communities
    have sheriffs and bailiffs who stand ready to protect their community.
    """
    name = "Investigator"
    skill_proficiencies = ('investigation', 'insight')

class ClanCrafter(Background):
    """
    The Stout Folk are well known for their artisanship and the worth of their handiworks, and you have been trained in
    that ancient tradition. For years you labored under a dwarf master of the craft, enduring long hours and dismissive,
     sour-tempered treatment in order to gain the fine skills you possess today.

    You are most likely a dwarf, but not necessarily- particularly in the North, the shield dwarf clans learned long ago
    that only proud fools who are more concerned for their egos than their craft turn away promising apprentices, even
    those of other races. If you aren't a dwarf, however, you have (likely) taken a solemn oath never to take on an apprentice in
    the craft: it is not for non-dwarves to pass on the skills of Moradin's favored children. You would have no difficulty,
    however, finding a dwarf master who was willing to receive potential apprentices who came with your recommendation.

    Use the tables for the guild artisan background as the basis for your traits and motivations, modifying the entries
    when appropriate to suit your identity. (For instance, consider the words "guild" and "clan" to be interchangeable.)

    Your bond is almost certainly related to the master or the clan that taught you, or else to the work that you
    produce. Your ideal might have to do with maintaining the high quality of your work or preserving the dwarven
    traditions of craftsmanship.
    """
    name = "Clan Crafter"
    skill_proficiencies = ('history', 'insight')
    languages = ('Dwarvish',)
    starting_equipment = "A set of artisan's tools with which you are proficient, a maker's mark chisel used to mark " \
                         "your handiwork with the symbol of the clan of crafters you learned your skill from, a " \
                         "set of traveler's clothes, and a pouch containing 5 gp and a gem worth 10 gp"
    features = (feats.RespectOfTheStoutFolk, feats.ExtraToolProficiency)


class CloisteredScholar(Background):
    """
    As a child, you were inquisitive when your playmates were possessive or raucous. In your formative years, you found
    your way to one of Faerûn's great institutes of learning , where you were apprenticed and taught that knowledge is
    a more valuable treasure than gold or gems. Now you are ready to leave your home – not to abandon it, but to quest
    for new lore to add to its storehouse of knowledge.

    The most well known of Faerûn's fonts of knowledge is Candlekeep. The great library is always in need of workers
    and attendants, some of whom rise through the ranks to assume roles of greater responsibility and prominence. You
    might be one of Candlekeep's own, dedicated to the curatorship of what is likely the most complete body of lore and
    history in all the world.

    Perhaps instead you were taken in by the scholars of the Vault of the Sages or the Map House in Silverymoon, and
    now you have struck out to increase your knowledge and to make yourself available to help those in other places who
    seek your expertise. You might be one of the few who aid Herald's Holdfast, helping to catalogue and maintain
    records of the information that arrives daily from across Faerûn.

    Your bond is almost certainly associated either with the place where you grew up or with the knowledge you hope to
    acquire through adventuring. Your ideal is no doubt related to how you view the quest for knowledge and truth –
    perhaps as a worthy goal in itself, or maybe as a means to a desirable end.
    """
    name = "Cloistered Scholar"
    skill_proficiencies = ('history',)
    skill_choices = ('arcana', 'nature', 'religion')
    num_skill_choices = 1
    languages = ()
    starting_equipment = "The scholar's robes of your cloister, a writing kit (small pouch with a quill, ink, " \
                         "folded parchment, and a small penknife), a borrowed book on the subject of your current " \
                         "study, and a pouch containing 10 gp"
    features = (feats.LibraryAccess, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class Courtier(Background):
    """
    In your earlier days, you were a personage of some significance in a noble court or a bureaucratic organization.
    You might or might not come from an upper-class family; your talents, rather than the circumstances of your birth,
    could have secured you this position.

    You might have been one of the many functionaries, attendants, and other hangers-on in the Court of Silverymoon, or
    perhaps you traveled in Waterdeep's baroque and sometimes cutthroat conglomeration of guilds, nobles, adventurers,
    and secret societies. You might have been one of the behind-the-scenes law-keepers or functionaries in Baldur's Gate
    or Neverwinter, or you might have grown up in and around the castle of Daggerford.

    Even if you are no longer a full-fledged member of the group that gave you your start in life, your relationships
    with your former fellows can be an advantage for you and your adventuring comrades. You might undertake missions
    with your new companions that further the interest of the organization that gave you your start in life. In any
    event, the abilities that you honed while serving as a courtier will stand you in good stead as an adventurer.

    The noble court or bureaucratic organization where you got your start is directly or indirectly associated with
    your bond (which could pertain to certain individuals in the group, such as your sponsor or mentor). Your ideal
    might be concerned with the prevailing philosophy of your court or organization.
    """
    name = "Courtier"
    skill_proficiencies = ("insight", 'persuasion')
    languages = ()
    starting_equipment = "A set of fine clothes and a pouch containing 5 gp."
    features = (feats.CourtFunctionary, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class FactionAgent(Background):
    """
    Many organizations active in the North and across the face of the world aren't bound by strictures of geography.
    These factions pursue their agendas without regard for political boundaries, and their members operate anywhere
    the organization deems necessary. These groups employ listeners, rumormongers, smugglers, sellswords, cache-holders
    (people who guard caches of wealth or magic for use by the faction's operatives), haven keepers, and message drop
    minders, to name a few. At the core of every faction are those who don't merely fulfill a small function for that
    organization, but who serve as its hands, head, and heart.

    As a prelude to your adventuring career (and in preparation for it), you served as an agent of a particular faction
    in Faerûn. You might have operated openly or secretly, depending on the faction and its goals, as well as how those
    goals mesh with your own. Becoming an adventurer doesn't necessarily require you to relinquish membership in your
    faction (though you can choose to do so), and it might enhance your status in the faction.

    Your bond might be associated with other members of your faction, or a location or an object that is important to
    your faction. The ideal you strive for is probably in keeping with the tenets and principles of your faction, but
    might be more personal in nature.
    """
    name = "Faction Agent"
    skill_proficiencies = ('insight',)
    skill_choices = ('animal handling', 'arcana', 'deception',
                     'history', 'intimidation', 'investigation',
                     'medicine', 'nature', 'perception', 'performance',
                     'persuasion', 'religion', 'survival')
    num_skill_choices = 1
    languages = ()
    starting_equipment = "Badge or emblem of your faction, a copy of a seminal faction text (or a code-book for a " \
                         "covert faction), a set of common clothes, and a pouch containing 15 gp."
    features = (feats.SafeHaven, feats.ExtraLanguage, feats.AdditionalExtraLanguage)


class FarTraveler(Background):
    """
    Almost all of the common people and other folk that one might encounter along the Sword Coast or in the North have
    one thing in common: they live out their lives without ever traveling more than a few miles from where they were
    born.

    You aren't one of those folk.

    You are from a distant place, one so remote that few of the common folk in the North realize that it exists, and
    chances are good that even if some people you meet have heard of your homeland, they know merely the name and
    perhaps a few outrageous stories. You have come to this part of the world for your own reasons, which you might or
    might not choose to share.

    Although you will undoubtedly find some of this land's ways to be strange and discomfiting, you can also be sure
    that some things its people take for granted will be to you new wonders that you've never laid eyes on before.
    By the same token, you're a person of interest, for good or ill, to those around you almost anywhere you go.

    A far traveler might have set out on a journey for one of a number of reasons, and the departure from his or her
    homeland could have been voluntary or involuntary.
    """
    name = 'Far Traveler'
    skill_proficiencies = ('insight', 'perception')
    languages = ()
    starting_equipment = "One set of traveler's clothes, any one musical instrument or gaming set you are proficient " \
                         "with, poorly wrought maps from your homeland that depict where you are in currently, " \
                         "a small piece of jewelry worth 10 gp in the style of your homeland's craftsmanship, and a " \
                         "pouch containing 5 gp"
    features = (feats.AllEyesOnYou, feats.ExtraLanguage, feats.InstrumentOrGamingSetProficiency)


class Inheritor(Background):
    """
    You are the heir to something of great value – not mere coin or wealth, but an object that has been entrusted to
    you and you alone. Your inheritance might have come directly to you from a member of your family, by right of
    birth, or it could have been left to you by a friend, a mentor, a teacher, or someone else important in your life.
    The revelation of your inheritance changed your life, and might have set you on the path to adventure, but it could
    also come with many dangers, including those who covet your gift and want to take it from you – by force, if need be.

    Your bond might be directly related to your inheritance, or to the person from whom you received it. Your ideal
    might be influenced by what you know about your inheritance, or by what you intend to do with your gift once you
    realize what it is capable of.
    """
    name = "Inheritor"
    skill_proficiencies = ('survival',)
    skill_choices = ('arcana', 'history', 'religion')
    num_skill_choices = 1
    languages = ()
    starting_equipment = "Your inheritance, a set of traveler's clothes, the tool you choose for this background’s " \
                         "tool proficiency, and a pouch containing 15 gp"
    features = (feats.Inheritance, feats.ExtraLanguage, feats.InstrumentOrGamingSetProficiency)


class KnightOfTheOrder(Background):
    """
    You belong to an order of knights who have sworn oaths to achieve a certain goal. The nature of this goal depends
    on the order you serve, but in your eyes it is without question a vital and honorable endeavor. Faerûn has a wide
    variety of knightly orders, all of which have a similar outlook concerning their actions and responsibilities.

    Though the term "knight" conjures ideas of mounted, heavily armored warriors of noble blood, many knightly orders
    in the world don't restrict their membership to such individuals. The goals and philosophies of the order are more
    important than the gear and fighting style of its members, and so most of these orders aren't limited to fighting
    types, but are open to all sorts of folk who are willing to battle and die for the order's cause.

    Many who rightfully call themselves "knight" earn that title as part of an order in service to a deity, such as
    Kelemvor's Eternal Order or Mystra's Knights of the Mystic Fire. Other knightly orders serve a government, royal
    family, or are the elite military of a feudal state, such as the brutal Warlock Knights of Vaasa. Other knighthoods
    are secular and non-governmental organizations of warriors who follow a particular philosophy, or consider
    themselves a kind of extended family, similar to an order of monks. Although there are organizations, such as the
    Knights of the Shield, that use the trappings of knighthood without necessarily being warriors, most folk of
    the world who hear the word "knight" think of a mounted warrior in armor beholden to a code.

    Your bond almost always involves the order to which you belong (or at least key members of it), and it is highly
    unusual for a knight's ideal not to reflect the agenda, sentiment, or philosophy of one's order.
    """
    name = "Knight of the Order"
    skill_proficiencies = ('persuasion',)
    skill_choices = ('arcana', 'history', 'nature', 'religion')
    num_skill_choices = 1
    languages = ()
    features = (feats.KnightlyRegard, feats.ExtraLanguage, feats.InstrumentOrGamingSetProficiency)


class MercenaryVeteran(Background):
    """
    As a sell-sword who fought battles for coin, you're well acquainted with risking life and limb for a chance at a
    share of treasure. Now, you look forward to fighting foes and reaping even greater rewards as an adventurer. Your
    experience makes you familiar with the ins and outs of mercenary life, and you likely have harrowing stories of
    events on the battlefield. You might have served with a large outfit such as the Zhentarim or the soldiers of
    Mintarn, or a smaller band of sell-swords, maybe even more than one. See the "Mercenaries of the North" section
    below for a collection of possibilities.

    Now you're looking for something else, perhaps greater reward for the risks you take, or the freedom to choose your
    own activities. For whatever reason, you're leaving behind the life of a soldier for hire, but your skills are
    undeniably suited for battle, so now you fight on in a different way.

    Countless mercenary companies operate all over the world. Most are small-scale operations that employ a dozen to a
    hundred folk who offer security services, hunt monsters and brigands, or go to war in exchange for gold. Some
    organizations, such as the Zhentarim, Flaming Fist, and the nation of Mintarn have hundreds or thousands of
    members and can provide private armies to those with enough funds.

    Your bond could be associated with the company you traveled with previously, or with some of the comrades you served
    with. The ideal you embrace largely depends on your worldview and your motivation for fighting.
    """
    name = "Mercenary Veteran"
    skill_proficiencies = ('athletics', 'persuasion')
    proficiencies_text = ('Vehicles (Land)',)
    starting_equipment = "A uniform of your company (traveler's clothes in quality), an insignia of your rank, a gaming " \
                         "set of your choice, and a pouch containing the remainder of your last wages (10 gp)"
    features = (feats.MercenaryLife, feats.GamingSetProficiency)


class UrbanBountyHunter(Background):
    """
    Before you became an adventurer, your life was already full of conflict and excitement, because you made a living
    tracking down people for pay. Unlike some people who collect bounties, though, you aren't a savage who follows
    quarry into or through the wilderness. You're involved in a lucrative trade, in the place where you live, that
    routinely tests your skills and survival instincts. What's more, you aren't alone, as a bounty hunter in the wild
    would be: you routinely interact with both the criminal subculture and other bounty hunters, maintaining contacts
    in both areas to help you succeed.

    You might be a cunning thief-catcher, prowling the rooftops to catch one of the myriad burglars of the city.
    Perhaps you are someone who has your ear to the street, aware of the doings of thieves' guilds and street gangs.
    You might be a "velvet mask" bounty hunter, one who blends in with high society and noble circles in order to catch
    the criminals that prey on the rich, whether pickpockets or con artists. The community where you plied your trade
    might have been one of Faenûn's great metropolises, such as Waterdeep or Baldur's Gate, or a less populous location,
    perhaps Luskan or Yartar – any place that's large enough to have a steady supply of potential quarries.

    As a member of an adventuring party, you might find it more difficult to pursue a personal agenda that doesn't fit
    with the group's objectives – but on the other hand, you can take down much more formidable targets with the help of
    your companions.

    Your bond might involve other bounty hunters or the organizations or individuals that employ you. Your ideal could
    be associated with your determination always to catch your quarry or your desire to maintain your reputation for
    being dependable.
    """
    name = 'Urban Bounty Hunter'
    skill_proficiencies = ()
    skill_choices = ('Deception', 'Insight', 'Persuasion', 'Stealth')
    num_skill_choices = 2
    starting_equipment = "A set of clothes appropriate to your duties and a pouch containing 20 gp."
    features = (feats.EarToTheGround, feats.UBHToolProficiencyBase)


class UthgardtTribeMember(Background):
    """
    Though you might have only recently arrived in civilized lands, you are no stranger to the values of cooperation
    and group effort when striving for supremacy. You learned these principles, and much more, as a member of an
    Uthgardt tribe.

    Your people have always tried to hold to the old ways. Tradition and taboo have kept the Uthgardt strong while the
    kingdoms of others have collapsed into chaos and ruin. But for the last few generations, some bands among the tribes
    were tempted to settle, make peace, trade, and even to build towns. Perhaps this is why Uthgar chose to raise up the
    totems among the people as living embodiments of his power. Perhaps they needed a reminder of who they were and from
    whence they came. The Chosen of Uthgar led bands back to the old ways, and most of your people abandoned the soft
    ways of civilization.

    You might have grown up in one of the tribes that had decided to settle down, and now that they have abandoned that
    path, you find yourself adrift. Or you might come from a segment of the Uthgardt that adheres to tradition, but you
    seek to bring glory to your tribe by achieving great things as a formidable adventurer.

    For most Uthgardt tribes, the only stability in their history is the site of their ancestral mound. Most of the
    Uthgardt holy sites have existed since antiquity, but the fortunes of the tribes that revere them have hardly been
    static.

    Even if you have left your tribe behind (at least for now), you hold to the traditions of your people. You will
    never cut down a still-living tree, and you may not countenance such an act being done in your presence. The
    Uthgardt ancestral mounds – great hills where the totem spirits were defeated by Uthgar and where the heroes of the
    tribes are interred – are sacred to you.

    Your bond is undoubtedly associated with your tribe or some aspect of Uthgardt philosophy or culture (perhaps even
    Uthgar himself). Your ideal is a personal choice that probably hews closely to the ethos of your people and
    certainly doesn't contradict or compromise what being an Uthgardt stands for.
    """
    name = "Uthgardt Tribe Member"
    skill_proficiencies = ('athletics', 'survival')
    languages = ()
    starting_equipment = "A hunting trap, a totemic token or set of tattoos marking your loyalty to Uthgar and your " \
                         "tribal totem, a set of traveler's clothes, and a pouch containing 10 gp"
    features = (feats.UthgardtHeritage, feats.ExtraLanguage, feats.InstrumentOrGamingSetProficiency)


class WaterdhavianNoble(Background):
    """
    You are a scion of one of the great noble families of Waterdeep. Human families who jealously guard their privilege
    and place in the City of Splendors, Waterdhavian nobles have a reputation across Faerûn for being eccentric,
    spoiled, venal, and, above all else, rich.

    Whether you are a shining example of the reason for this reputation or one who proves the rule by being an
    exception, people expect things of you when they know your surname and what it means. Your reasons for taking up
    adventuring likely involve your family in some way: Are you the family rebel, who prefers delving in filthy dungeons
    to sipping zzar at a ball? Or have you taken up sword or spell on your family's behalf, ensuring that they have
    someone of renown to see to their legacy?

    Work with your DM to come up with the family you are part of – there are around seventy-five lineages in Waterdeep,
    each with its own financial interests, specialties, and schemes. You might be part of the main line of your family,
    possibly in line to become its leader one day. Or you might be one of any number of cousins, with less prestige but
    also less responsibility.
    """
    name = "Waterdhavian Noble"
    skill_proficiencies = ('history', 'persuasion')
    languages = ()
    starting_equipment = "A set of fine clothes, a signet ring or brooch, a scroll of pedigree, a skin of fine " \
                         "zzar or wine, and a purse containing 20 gp"
    features = (feats.KeptInStyle, feats.ExtraLanguage)


PHB_backgrounds = [Acolyte, Charlatan, Criminal, Spy, SpyRevised, Entertainer,
                   Gladiator, FolkHero, GuildArtisan, GuildMerchant, GuildMerchantTwoLanguages,
                   Hermit, Noble, Knight, Outlander, Sage, Sailor,
                   Pirate, PirateBadReputation, Soldier, Urchin]

SCAG_backgrounds = [CityWatch, Investigator, ClanCrafter, CloisteredScholar, Courtier,
                    FactionAgent, FarTraveler, Inheritor, KnightOfTheOrder,
                    MercenaryVeteran, UrbanBountyHunter, UthgardtTribeMember,
                    WaterdhavianNoble]

available_backgrounds = PHB_backgrounds + SCAG_backgrounds

__all__ = tuple([b.name for b in available_backgrounds]) + (
    'PHB_backgrounds', 'SCAG_backgrounds', 'available_backgrounds')
