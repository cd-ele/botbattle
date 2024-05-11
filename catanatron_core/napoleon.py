import random
from catanatron.state_functions import (
    player_key,
    get_player_freqdeck
)


from catanatron.models.player import Player
from catanatron.game import Game
from catanatron.models.actions import ActionType


class Napoleon(Player):
    """
    Napoleon.
    """
    def decide(self, game: Game, playable_actions):

        def trade_or_use_for(game, clave, construccion, aux):
            print(f'Baraja Inicial {get_player_freqdeck(game.state, self.color)}')
            for action in aux[clave]:
                game_copy = game.copy()
                game_copy.execute(action)
                key = player_key(game_copy.state, self.color)
                

                if construccion == "city" and game_copy.state.player_state[f"{key}_WHEAT_IN_HAND"] >= 2 and game_copy.state.player_state[f"{key}_ORE_IN_HAND"] >= 3:
                    print(f'{clave} {get_player_freqdeck(game_copy.state, self.color)}, para ciudad', {action})
                    return action
                if construccion == "settlement" and game_copy.state.player_state[f"{key}_WOOD_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_BRICK_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_WHEAT_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_SHEEP_IN_HAND"] >= 1: 
                    print(f'{clave} {get_player_freqdeck(game_copy.state, self.color)}, para settlemente')
                    return action
                if construccion == "road" and game_copy.state.player_state[f"{key}_WOOD_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_BRICK_IN_HAND"] >= 1:
                    print(f'{clave} {get_player_freqdeck(game_copy.state, self.color)}, para road')
                    return action

        def create_auxdic():
            """
            aux will be a diccionary 
            key --> type action
            value --> list of those actions
            """
            aux = {}
            for action in playable_actions:
                if action.action_type not in aux:
                    aux[action.action_type] = [action]
                else:
                    aux[action.action_type].append(action)
            return aux
        


        if len(playable_actions) == 1:
            return playable_actions[0]

        aux = create_auxdic()
        key = player_key(game.state, self.color)

        if ActionType.PLAY_KNIGHT_CARD in aux:
            return aux[ActionType.PLAY_KNIGHT_CARD][0]
        
        if ActionType.BUILD_SETTLEMENT in aux:
            return aux[ActionType.BUILD_SETTLEMENT][0]
        if ActionType.MARITIME_TRADE in aux:
            can = self.trade_or_use_for(game,ActionType.MARITIME_TRADE,"settlement",aux)
            if can is not None: return can 

        if ActionType.BUILD_ROAD in aux:
            return aux[ActionType.BUILD_ROAD][0]
        if ActionType.MARITIME_TRADE in aux:
            can = self.trade_or_use_for(game,ActionType.MARITIME_TRADE,"road",aux)
            if can is not None: return can 

        num_sett_available = game.state.player_state[f'{key}_SETTLEMENTS_AVAILABLE']
        if num_sett_available <= 2:
            if ActionType.BUILD_CITY in aux:
                return aux[ActionType.BUILD_CITY][0]
            if ActionType.MARITIME_TRADE in aux:
                can = self.trade_or_use_for(game,ActionType.MARITIME_TRADE,"city",aux)
                if can is not None: return can 
        

        print(playable_actions)
        return random.choice(playable_actions)

