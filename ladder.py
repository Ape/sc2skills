import collections
import math
import trueskill

LEAGUES = {
    "EU": collections.OrderedDict([
        ("master-1", 4919),
        ("master-2", 4719),
        ("master-3", 4520),
        ("diamond-1", 4227),
        ("diamond-2", 3933),
        ("diamond-3", 3640),
        ("platinum-1", 3520),
        ("platinum-2", 3400),
        ("platinum-3", 3280),
        ("gold-1", 3187),
        ("gold-2", 3093),
        ("gold-3", 3000),
        ("silver-1", 2813),
        ("silver-2", 2627),
        ("silver-3", 2440),
        ("bronze-1", 2241),
        ("bronze-2", 2041),
        ("bronze-3", -math.inf),
    ]),
    "NA": collections.OrderedDict([
        ("master-1", 5007),
        ("master-2", 4804),
        ("master-3", 4600),
        ("diamond-1", 4293),
        ("diamond-2", 3987),
        ("diamond-3", 3680),
        ("platinum-1", 3560),
        ("platinum-2", 3440),
        ("platinum-3", 3320),
        ("gold-1", 3213),
        ("gold-2", 3107),
        ("gold-3", 3000),
        ("silver-1", 2813),
        ("silver-2", 2627),
        ("silver-3", 2440),
        ("bronze-1", 2236),
        ("bronze-2", 2033),
        ("bronze-3", -math.inf),
    ])
}

class Ladder:
    def __init__(self, region):
        self.leagues = LEAGUES[region]

    @property
    def mu(self):
        # 50 % of the players are below platinum
        return self.leagues["platinum-3"]

    @property
    def sigma(self):
        # 73 % of the players are below diamond
        return ((self.leagues["diamond-3"] - self.mu)
                / trueskill.TrueSkill().ppf(0.73))

    def get_league(self, mmr):
        for league, min_mmr in self.leagues.items():
            if mmr >= min_mmr:
                return league
