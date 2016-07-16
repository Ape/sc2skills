import collections
import math
import scipy.stats

LEAGUES = {
    "EU": collections.OrderedDict([
        ("master-1", 5033),
        ("master-2", 4836),
        ("master-3", 4640),
        ("diamond-1", 4360),
        ("diamond-2", 4080),
        ("diamond-3", 3800),
        ("platinum-1", 3693),
        ("platinum-2", 3586),
        ("platinum-3", 3480),
        ("gold-1", 3373),
        ("gold-2", 3266),
        ("gold-3", 3160),
        ("silver-1", 2973),
        ("silver-2", 2786),
        ("silver-3", 2600),
        ("bronze-1", 2403),
        ("bronze-2", 2206),
        ("bronze-3", -math.inf),
    ]),
    "NA": collections.OrderedDict([
        ("master-1", 5032),
        ("master-2", 4834),
        ("master-3", 4640),
        ("diamond-1", 4373),
        ("diamond-2", 4106),
        ("diamond-3", 3840),
        ("platinum-1", 3720),
        ("platinum-2", 3600),
        ("platinum-3", 3480),
        ("gold-1", 3373),
        ("gold-2", 3266),
        ("gold-3", 3160),
        ("silver-1", 2973),
        ("silver-2", 2786),
        ("silver-3", 2600),
        ("bronze-1", 2406), # exact value unknown
        ("bronze-2", 2211),
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
                / scipy.stats.norm.ppf(0.73))

    def get_league(self, mmr):
        for league, min_mmr in self.leagues.items():
            if mmr >= min_mmr:
                return league
