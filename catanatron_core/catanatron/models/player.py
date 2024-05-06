import random
from enum import Enum
from catanatron.models.actions import ActionType
from catanatron.state_functions import player_key

class Color(Enum):
    """Enum to represent the colors in the game"""

    RED = "RED"
    BLUE = "BLUE"
    ORANGE = "ORANGE"
    WHITE = "WHITE"


class Player:
    """Interface to represent a player's decision logic.

    Formulated as a class (instead of a function) so that players
    can have an initialization that can later be serialized to
    the database via pickle.
    """

    def __init__(self, color, is_bot=True):
        """Initialize the player

        Args:
            color(Color): the color of the player
            is_bot(bool): whether the player is controlled by the computer
        """
        self.color = color
        self.is_bot = is_bot

    def decide(self, game, playable_actions):
        """Should return one of the playable_actions or
        an OFFER_TRADE action if its your turn and you have already rolled.

        Args:
            game (Game): complete game state. read-only.
            playable_actions (Iterable[Action]): options right now
        """
        raise NotImplementedError

    def reset_state(self):
        """Hook for resetting state between games"""
        pass

    def __repr__(self):
        return f"{type(self).__name__}:{self.color.value}"


class SimplePlayer(Player):
    """Simple AI player that always takes the first action in the list of playable_actions"""

    def decide(self, game, playable_actions):
        return playable_actions[0]


class HumanPlayer(Player):
    """Human player that selects which action to take using standard input"""

    def decide(self, game, playable_actions):
        for i, action in enumerate(playable_actions):
            print(f"{i}: {action.action_type} {action.value}")
        i = None
        while i is None or (i < 0 or i >= len(playable_actions)):
            print("Please enter a valid index:")
            try:
                x = input(">>> ")
                i = int(x)
            except ValueError:
                pass

        return playable_actions[i]


class RandomPlayer(Player):
    """Random AI player that selects an action randomly from the list of playable_actions"""

    
    def decide(self, game, playable_actions):

        def print_actions(actions):
            print('='*20)
            for a in actions:
                print(a)
            

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


        if ActionType.END_TURN in aux:
            return aux[ActionType.END_TURN][0]

        if ActionType.MOVE_ROBBER in aux:
            return aux[ActionType.MOVE_ROBBER][0]
        return random.choice(playable_actions)


          


class PlayerPrueba(Player):
    """
    Player that decides at random, but skews distribution
    to actions that are likely better (cities > settlements > dev cards).
    """

    def decide(self, game, playable_actions):

        WEIGHTS_BY_ACTION_TYPE = {
            ActionType.BUILD_CITY: 10000,
            ActionType.BUILD_SETTLEMENT: 1000,
            ActionType.BUY_DEVELOPMENT_CARD: 100}   

        bloated_actions = []
        for action in playable_actions:
            weight = WEIGHTS_BY_ACTION_TYPE.get(action.action_type, 1)
            bloated_actions.extend([action] * weight)

        return random.choice(bloated_actions)