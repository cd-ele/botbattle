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

        if ActionType.PLAY_KNIGHT_CARD in aux:
            print('HOLAAAAA')
        
        




        





            
            

