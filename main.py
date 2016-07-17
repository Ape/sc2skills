#!/usr/bin/env python3

import argparse
import collections
import enum
import trueskill

from ladder import Ladder

DRAW_PROBABILITY = 0.001
OPPONENT_SIGMA = 0.1

Result = enum.Enum("Result", "win loss")
Game = collections.namedtuple("Game", "result mmr label")

def load_games(games_file):
    games = []

    with open(games_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        result, mmr, label = line.strip().split()
        games.append(Game(Result[result], int(mmr), label))

    return games

def print_board(ladder, ratings):
    if len(ratings) == 0:
        print("No ratings.")
        return

    def sort_by_score(items):
        return reversed(sorted(items, key=lambda x: x[1].mu))

    def max_name_width(items):
        return max(len(x[0]) for x in items)

    items = ratings.items()
    items = sort_by_score(items)
    items = list(items)
    name_width = max_name_width(items)

    for name, rating in items:
        league = ladder.get_league(rating.mu)

        print("{name:{width}s} {mu:.0f} ± {sigma:.0f} ({league})"
              .format(name=name, width=name_width,
                      mu=rating.mu, sigma=2*rating.sigma,
                      league=league))

def rate(ladder, rating, game):
    opponent = trueskill.Rating(mu=game.mmr,
                                sigma=OPPONENT_SIGMA * ladder.sigma)

    if game.result is Result.win:
        return trueskill.rate_1vs1(rating, opponent)[0]
    else:
        return trueskill.rate_1vs1(opponent, rating)[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("region")
    parser.add_argument("games_file")
    args = parser.parse_args()

    try:
        ladder = Ladder(args.region)
    except KeyError:
        print("Error: Region '{}' not recognized".format(args.region))
        return

    trueskill.setup(mu=ladder.mu, sigma=ladder.sigma, beta=0.5 * ladder.sigma,
                    tau=0.01 * ladder.sigma, draw_probability=DRAW_PROBABILITY)

    ratings = collections.defaultdict(lambda: trueskill.Rating())

    try:
        games = load_games(args.games_file)
    except OSError as e:
        print("Error: Cannot read the provided games file:")
        print("  {}".format(e))
        return

    for game in games:
        ratings[game.label] = rate(ladder, ratings[game.label], game)

    print_board(ladder, ratings)

if __name__ == "__main__":
    main()
