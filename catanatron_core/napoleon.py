import random
from catanatron.state_functions import (
    player_key,
)
from catanatron.models.player import Player
from catanatron.game import Game
from catanatron.models.actions import ActionType


class Napoleon(Player):
    """
    Napoleon.
    """
    def decide(self, game: Game, playable_actions):

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
        # anyadir trade

        if ActionType.BUILD_ROAD in aux:
            return aux[ActionType.BUILD_ROAD][0]
        # anyadir trade

        num_sett_available = game.state.player_state[f'{key}_SETTLEMENTS_AVAILABLE']
        if num_sett_available <= 2:
            if ActionType.BUILD_CITY in aux:
                return aux[ActionType.BUILD_CITY][0]
            # anyadir trades
        

        print(playable_actions)
        return random.choice(playable_actions)

