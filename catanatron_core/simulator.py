from simulator_aux import play_batch
from catanatron_experimental.cli.cli_players import CLI_PLAYERS
from our_players import Magnate, Granjero, Napoleon
from catanatron.models.player import Color
from collections import defaultdict
import pandas as pd
import random


# Players List
# R - Random
# W - WeightedRandomPlayer
# VP - VictoryPointPlayer
# F - ValueFunctionPlayer
# 0 - BOT0
# 1 - BOT1
# N - Napoleon


if __name__ == '__main__':
    
    num = 500
    players_keys = ['N','0','1']
    players = []
    colors = [c for c in Color]
    for i, code in enumerate(players_keys):
        for cli_player in CLI_PLAYERS:
            if cli_player.code == code:
                player = cli_player.import_fn(*[colors[i]])
                players.append(player)
                break
        for bot_code, bot in [('0', Magnate), ('1', Granjero), ('N', Napoleon)]:
            if bot_code == code:
                players.append(bot(colors[i]))
                break
    final_df = play_batch(num, players, all_data=False)
    result = {
        p.color.value: {} for p in players
    }
    color_player = {
        p.color.value: type(p).__name__ for p in players
    }
    for color, name in color_player.items():
        final_df.loc[final_df['COLOR'] == color, 'COLOR'] = name
        final_df.loc[final_df['WINNER'] == color, 'WINNER'] = name
    
    # print(final_df)
    final_df.to_csv('botML_data_3players.csv', index=False)
        

    # for k, v in game_info.items():
    #     pos = k.find('_')
    #     color = k[:pos].split('.')[1]
    #     k1 = k[pos+1:]
    #     result[color][k1] = v

    # dfs = []
    # for color, name in color_player.items():
    #     df = pd.DataFrame(result[color])
    #     df['Player'] = name
    #     dfs.append(df)

    # dfs = []
    # for color, name in color_player.items():
    #     df = pd.DataFrame(result[color])
    #     df['Player'] = name
    #     dfs.append(df)
    # namefile = 'results' + ''.join(random.choices('0123456789', k=5)) + '.csv'
    # pd.concat(dfs, ignore_index=True).to_csv(namefile, index=False)

    
