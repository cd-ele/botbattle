from simulator_aux import play_batch
from catanatron_experimental.cli.cli_players import CLI_PLAYERS
from our_players import Magnate, Granjero, Napoleon
from catanatron.models.player import Color
from collections import defaultdict
import pandas as pd
import random
import os
import itertools

# Players List
# R - Random
# W - WeightedRandomPlayer
# VP - VictoryPointPlayer
# F - ValueFunctionPlayer
# 0 - Magnate
# 1 - Granjero
# N - Napoleon


if __name__ == '__main__':
    
    nGames = 50
    nPlayers = 2
    players_keys = ['N','0','1','F']
    colors = [c for c in Color]
    dfs = []
    combinations = list(itertools.combinations([i for i in range(len(players_keys))], nPlayers))
    for comb in combinations:
        select_players = [players_keys[i] for i in comb]
        select_colors = [colors[i] for i in comb]
        players = []
        for i, code in enumerate(select_players):
            for cli_player in CLI_PLAYERS:
                if cli_player.code == code:
                    player = cli_player.import_fn(*[select_colors[i]])
                    players.append(player)
                    break
            for bot_code, bot in [('0', Magnate), ('1', Granjero), ('N', Napoleon)]:
                if bot_code == code:
                    players.append(bot(select_colors[i]))
                    break

        statistics_accumulator, vp_accumulator = play_batch(nGames, players, statistics=True, all_data=False)
        color_player = {
            p.color.value: type(p).__name__ for p in players
        }
        results = {}
        
        for player in players:
            vps = statistics_accumulator.results_by_player[player.color]
            avg_vps = sum(vps) / len(vps)
            avg_settlements = vp_accumulator.get_avg_settlements(player.color)
            avg_cities = vp_accumulator.get_avg_cities(player.color)
            avg_largest = vp_accumulator.get_avg_largest(player.color)
            avg_longest = vp_accumulator.get_avg_longest(player.color)
            avg_devvps = vp_accumulator.get_avg_devvps(player.color)
            name_player = [type(player).__name__] * len(vps)
            

    # directory = "resultados_liga"
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    # namefile = directory + '/results' + f'{nPlayers}Players' + ''.join(random.choices('0123456789', k=3)) + '.csv'
    # pd.concat(dfs, ignore_index=True).to_csv(namefile, index=False)

    