import random
from enum import Enum
import random
from catanatron.game import Game
from catanatron.models.enums import ActionType
from catanatron.models.actions import (
    road_building_possibilities
)
from catanatron.models.player import Player
from catanatron.state_functions import (
    player_key,
    get_player_freqdeck,
    get_player_buildings,
    player_can_afford_dev_card
    
)

def trade_or_use_for(game, clave, construccion, aux, color):
    # # print(f'Baraja Inicial {get_player_freqdeck(game.state, self.color)}')
    for action in aux[clave]:
        game_copy = game.copy()
        game_copy.execute(action)
        key = player_key(game_copy.state, color)
                

        if construccion == "city" and game_copy.state.player_state[f"{key}_WHEAT_IN_HAND"] >= 2 and game_copy.state.player_state[f"{key}_ORE_IN_HAND"] >= 3:
            # print(f'{clave} {get_player_freqdeck(game_copy.state, self.color)}, para ciudad', {action})
            return action
        if construccion == "settlement" and game_copy.state.player_state[f"{key}_WOOD_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_BRICK_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_WHEAT_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_SHEEP_IN_HAND"] >= 1: 
            # print(f'{clave} {get_player_freqdeck(game_copy.state, self.color)}, para settlemente')
            return action
        if construccion == "road" and game_copy.state.player_state[f"{key}_WOOD_IN_HAND"] >= 1 and game_copy.state.player_state[f"{key}_BRICK_IN_HAND"] >= 1:
            # print(f'{clave} {get_player_freqdeck(game_copy.state, self.color)}, para road')
            return action

def get_best_node(game, action_list, resources=[]):
        if len(action_list) == 1:
            return action_list[0]
        
        node_list = [action[2] for action in action_list]
        node_production = {node: d for node, d in game.state.board.map.node_production.items() 
                           if node in node_list}
        if resources:
            nodes = [node for node, d in node_production.items() if len(set(resources) & set(d.keys())) > 0]
            if nodes:
                total_production = [(production, node) for node in nodes 
                                    for resource, production in node_production[node].items() 
                                    if resource in resources]
                aux = {}
                for production, node in total_production:
                    if node in aux:
                        aux[node] += production
                    else:
                        aux[node] = production
                total_production = sorted([(production, node) for node, production in aux.items()])
                node_result = total_production[-1][1]
                for action in action_list:
                    if node_result == action[2]:
                        return action

        total_production = sorted([(sum(d.values()), node) for node, d in node_production.items()])
        best_node = total_production[-1][1]
        for action in action_list:
            if best_node == action[2]:
                return action
        return action_list[0]


class Magnate(Player):
    """Player that focuses on cities, ore and wheat"""
    def decide(self, game, playable_actions):
        if len(playable_actions) == 1:
            return playable_actions[0]
        # aux Diccionario De Todo Tipo de Jugadas por Tipo
        aux = {}
        for action in playable_actions:
            if action.action_type not in aux:
                aux[action.action_type] = [action]
            else:
                aux[action.action_type].append(action)
        ## print(list(aux.keys()))
        if ActionType.PLAY_KNIGHT_CARD in aux:
            return aux[ActionType.PLAY_KNIGHT_CARD][0]
        if ActionType.BUILD_CITY in aux:
            actions = aux[ActionType.BUILD_CITY]
            return get_best_node(game, actions, resources=[])
        
        #### TRADEAR PARA CIUDAD
        if ActionType.MARITIME_TRADE in aux: 
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"city",aux, self.color)
            if can is not None: return can
        #### HAS PLENTY CARD
        if ActionType.PLAY_YEAR_OF_PLENTY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_YEAR_OF_PLENTY,"city",aux, self.color)
            if can is not None: return can
        #### HAS MONOPOLY CARD
        if ActionType.PLAY_MONOPOLY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_MONOPOLY,"city",aux, self.color)
            if can is not None: return can

        if ActionType.BUILD_SETTLEMENT in aux:
            actions = aux[ActionType.BUILD_SETTLEMENT]
            return get_best_node(game, actions, resources=[])
        
        #### TRADEAR PARA Poblado
        if ActionType.MARITIME_TRADE in aux: 
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"settlement",aux, self.color)
            if can is not None: return can
        #### HAS PLENTY CARD
        if ActionType.PLAY_YEAR_OF_PLENTY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_YEAR_OF_PLENTY,"settlement",aux, self.color)
            if can is not None: return can
        #### HAS MONOPOLY CARD
        if ActionType.PLAY_MONOPOLY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_MONOPOLY,"settlement",aux, self.color)
            if can is not None: return can

        if ActionType.BUILD_ROAD in aux:
            return aux[ActionType.BUILD_ROAD][0]
        
        #### TRADEAR PARA ROAD
        if ActionType.MARITIME_TRADE in aux: 
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"road",aux, self.color)
            if can is not None: return can
        #### HAS PLENTY CARD
        if ActionType.PLAY_YEAR_OF_PLENTY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_YEAR_OF_PLENTY,"road",aux, self.color)
            if can is not None: return can
        #### HAS MONOPOLY CARD
        if ActionType.PLAY_MONOPOLY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_MONOPOLY,"road",aux, self.color)
            if can is not None: return can

        if ActionType.PLAY_KNIGHT_CARD not in aux or ActionType.PLAY_YEAR_OF_PLENTY not in aux or ActionType.PLAY_MONOPOLY not in aux or ActionType.PLAY_ROAD_BUILDING not in aux:
            if ActionType.BUY_DEVELOPMENT_CARD in aux:
                return aux[ActionType.BUY_DEVELOPMENT_CARD][0]
            
            ##### TRADE FOR DEV CARD
            if ActionType.MARITIME_TRADE in aux:
                for action in aux[ActionType.MARITIME_TRADE]:
                    game_copy = game.copy()
                    game_copy.execute(action)
                    if player_can_afford_dev_card(game_copy.state,self.color):
                        return action
            ##### PLENTY CARD FOR DEV CARD
            if ActionType.PLAY_YEAR_OF_PLENTY in aux:
                for action in aux[ActionType.PLAY_YEAR_OF_PLENTY]:
                    game_copy = game.copy()
                    game_copy.execute(action)
                    if player_can_afford_dev_card(game_copy.state,self.color):
                        return action
            ##### MONOPOLY FOR DEV CARD
            if ActionType.PLAY_MONOPOLY in aux:
                for action in aux[ActionType.PLAY_MONOPOLY]:
                    game_copy = game.copy()
                    game_copy.execute(action)
                    if player_can_afford_dev_card(game_copy.state,self.color):
                        return action               
        
        if ActionType.END_TURN in aux:
            return aux[ActionType.END_TURN][0]
        
        
        return random.choice(playable_actions)
    
class Granjero(Player):
    """Random AI player that selects an action randomly from the list of playable_actions"""

    def decide(self, game, playable_actions):
        if len(playable_actions) == 1:
            return playable_actions[0]
        # aux Diccionario De Todo Tipo de Jugadas por Tipo
        aux = {}
        for action in playable_actions:
            if action.action_type not in aux:
                aux[action.action_type] = [action]
            else:
                aux[action.action_type].append(action)
        #print(list(aux.keys()))
        #### HAVE KNIGHT CARD
        if ActionType.PLAY_KNIGHT_CARD in aux:
            return aux[ActionType.PLAY_KNIGHT_CARD][0]
        #### HAVE LESS THAN 2 CITIES
        if len(get_player_buildings(game.state,self.color,"CITY")) < 2:
            ##### CAN BUILD CITY
            if ActionType.BUILD_CITY in aux:
                actions = aux[ActionType.BUILD_CITY]
                return get_best_node(game, actions, resources=['SHEEP'])
            if get_player_freqdeck(game.state, self.color)[-2] < 2 or get_player_freqdeck(game.state, self.color)[-1] < 3:
                if ActionType.MARITIME_TRADE in aux: 
                    can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"city",aux, self.color)
                    if can is not None: return can
                #### HAS PLENTY CARD
                if ActionType.PLAY_YEAR_OF_PLENTY in aux:
                    can = trade_or_use_for(game,ActionType.PLAY_YEAR_OF_PLENTY,"city",aux, self.color)
                    if can is not None: return can
                #### HAS MONOPOLY CARD
                if ActionType.PLAY_MONOPOLY in aux:
                    can = trade_or_use_for(game,ActionType.PLAY_MONOPOLY,"city",aux, self.color)
                    if can is not None: return can
        if ActionType.BUY_DEVELOPMENT_CARD in aux:
            return aux[ActionType.BUY_DEVELOPMENT_CARD][0]
        ##### TRADE FOR DEV CARD
        if ActionType.MARITIME_TRADE in aux:
            for action in aux[ActionType.MARITIME_TRADE]:
                game_copy = game.copy()
                game_copy.execute(action)
                if player_can_afford_dev_card(game_copy.state,self.color):
                    return action
        ##### PLENTY CARD FOR DEV CARD
        if ActionType.PLAY_YEAR_OF_PLENTY in aux:
            for action in aux[ActionType.PLAY_YEAR_OF_PLENTY]:
                game_copy = game.copy()
                game_copy.execute(action)
                if player_can_afford_dev_card(game_copy.state,self.color):
                    return action
        ##### MONOPOLY FOR DEV CARD
        if ActionType.PLAY_MONOPOLY in aux:
            for action in aux[ActionType.PLAY_MONOPOLY]:
                game_copy = game.copy()
                game_copy.execute(action)
                if player_can_afford_dev_card(game_copy.state,self.color):
                    return action   
        #### CAN BUILD CITY
        if ActionType.BUILD_CITY in aux:
            actions = aux[ActionType.BUILD_CITY]
            return get_best_node(game, actions, resources=['SHEEP'])
        #### TRADEAR PARA Poblado
        if ActionType.MARITIME_TRADE in aux: 
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"city",aux, self.color)
            if can is not None: return can
        #### HAS PLENTY CARD
        if ActionType.PLAY_YEAR_OF_PLENTY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_YEAR_OF_PLENTY,"city",aux, self.color)
            if can is not None: return can
        #### HAS MONOPOLY CARD
        if ActionType.PLAY_MONOPOLY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_MONOPOLY,"city",aux, self.color)
            if can is not None: return can
        #### CAN BUILD A SETTLEMENTE

        if ActionType.BUILD_SETTLEMENT in aux:
            actions = aux[ActionType.BUILD_SETTLEMENT]
            return get_best_node(game, actions, resources=['SHEEP'])
                #### TRADEAR PARA Poblado
        if ActionType.MARITIME_TRADE in aux: 
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"settlement",aux, self.color)
            if can is not None: return can
        #### HAS PLENTY CARD
        if ActionType.PLAY_YEAR_OF_PLENTY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_YEAR_OF_PLENTY,"settlement",aux, self.color)
            if can is not None: return can
        #### HAS MONOPOLY CARD
        if ActionType.PLAY_MONOPOLY in aux:
            can = trade_or_use_for(game,ActionType.PLAY_MONOPOLY,"settlement",aux, self.color)
            if can is not None: return can
        #### CAN BUILD A SETTLEMENTE
        ##### HAS BUILDABLE NODES 

        if len(road_building_possibilities(game.state,self.color)) == 0:
            if ActionType.BUILD_ROAD in aux:
                return aux[ActionType.BUILD_ROAD][0]

        if ActionType.END_TURN in aux:
            return aux[ActionType.END_TURN][0]
        
        
        return random.choice(playable_actions)


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
            actions = aux[ActionType.BUILD_SETTLEMENT]
            return get_best_node(game, actions, resources=['BRICK', 'WOOD'])
        if ActionType.MARITIME_TRADE in aux:
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"settlement",aux, self.color)
            if can is not None: return can 

        if ActionType.BUILD_ROAD in aux:
            return aux[ActionType.BUILD_ROAD][0]
        if ActionType.MARITIME_TRADE in aux:
            can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"road",aux, self.color)
            if can is not None: return can 

        num_sett_available = game.state.player_state[f'{key}_SETTLEMENTS_AVAILABLE']
        if num_sett_available <= 2:
            if ActionType.BUILD_CITY in aux:
                actions = aux[ActionType.BUILD_CITY]
                return get_best_node(game, actions, resources=['BRICK', 'WOOD'])
            if ActionType.MARITIME_TRADE in aux:
                can = trade_or_use_for(game,ActionType.MARITIME_TRADE,"city",aux, self.color)
                if can is not None: return can 
        
        return random.choice(playable_actions)
