import dungeonsheets

class ArcaneClanCrafter(dungeonsheets.background.ClanCrafter):
    name = "Arcane Clan Crafter"
    skill_proficiencies = ('history', 'arcana')

dungeonsheets.background.available_backgrounds += (ArcaneClanCrafter,)