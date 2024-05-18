from catanatron_experimental import SimulationAccumulator, register_accumulator
import os, random
import pandas as pd
from catanatron.state_functions import player_key
from catanatron.models.enums import ActionType, SETTLEMENT
import networkx as nx
from collections import defaultdict

def clean_data(df, i):
    fixedCols = [
        'ID',
        'TURN',
        'REMAINING_TURNS',
        'NUM_PLAYERS',
        'MAX_VICTORY_POINTS',
        'MAX_PLAYED_KNIGHT',
        'MAX_LONGEST_ROAD_LENGTH',
        'MIN_VICTORY_POINTS',
        'MIN_PLAYED_KNIGHT',
        'MIN_LONGEST_ROAD_LENGTH',
        'MEAN_VICTORY_POINTS',
        'MEAN_PLAYED_KNIGHT',
        'MEAN_LONGEST_ROAD_LENGTH',
        'STD_VICTORY_POINTS',
        'STD_PLAYED_KNIGHT',
        'STD_LONGEST_ROAD_LENGTH',
        'MAX_WHEAT_PRODUCTION',
        'MAX_SHEEP_PRODUCTION',
        'MAX_BRICK_PRODUCTION',  
        'MAX_WOOD_PRODUCTION',   
        'MAX_ORE_PRODUCTION',
        'MIN_WHEAT_PRODUCTION',
        'MIN_SHEEP_PRODUCTION',
        'MIN_BRICK_PRODUCTION',  
        'MIN_WOOD_PRODUCTION',   
        'MIN_ORE_PRODUCTION',
        'MEAN_WHEAT_PRODUCTION',
        'MEAN_SHEEP_PRODUCTION',
        'MEAN_BRICK_PRODUCTION',  
        'MEAN_WOOD_PRODUCTION',   
        'MEAN_ORE_PRODUCTION',
        'STD_WHEAT_PRODUCTION',
        'STD_SHEEP_PRODUCTION',
        'STD_BRICK_PRODUCTION',  
        'STD_WOOD_PRODUCTION',   
        'STD_ORE_PRODUCTION',
        'MAX_DEV_CARDS',
        'MIN_DEV_CARDS',
        'MEAN_DEV_CARDS',
        'STD_DEV_CARDS',
        'WHEAT_PRODUCTION_MAP',
        'SHEEP_PRODUCTION_MAP',
        'BRICK_PRODUCTION_MAP',
        'WOOD_PRODUCTION_MAP',
        'ORE_PRODUCTION_MAP'
    ]

    # Creating remaining game features
    df['ID']                      = i
    df['REMAINING_TURNS']         = df['TURN'].iloc[-1] - df['TURN']
    df['MAX_PLAYED_KNIGHT']       = df.filter(regex='^P._PLAYED_KNIGHT$').max(axis=1)
    df['MAX_VICTORY_POINTS']      = df.filter(regex='^P._ACTUAL_VICTORY_POINTS$').max(axis=1)
    df['MAX_LONGEST_ROAD_LENGTH'] = df.filter(regex='^P._LONGEST_ROAD_LENGTH$').max(axis=1)
    df['MAX_WHEAT_PRODUCTION']    = df.filter(regex='^P._WHEAT_PRODUCTION$').max(axis=1)
    df['MAX_SHEEP_PRODUCTION']    = df.filter(regex='^P._SHEEP_PRODUCTION$').max(axis=1)
    df['MAX_BRICK_PRODUCTION']    = df.filter(regex='^P._BRICK_PRODUCTION$').max(axis=1)
    df['MAX_WOOD_PRODUCTION']     = df.filter(regex='^P._WOOD_PRODUCTION$').max(axis=1)
    df['MAX_ORE_PRODUCTION']      = df.filter(regex='^P._ORE_PRODUCTION$').max(axis=1)
    df['MIN_PLAYED_KNIGHT']       = df.filter(regex='^P._PLAYED_KNIGHT$').min(axis=1)
    df['MIN_VICTORY_POINTS']      = df.filter(regex='^P._ACTUAL_VICTORY_POINTS$').min(axis=1)
    df['MIN_LONGEST_ROAD_LENGTH'] = df.filter(regex='^P._LONGEST_ROAD_LENGTH$').min(axis=1)
    df['MIN_WHEAT_PRODUCTION']    = df.filter(regex='^P._WHEAT_PRODUCTION$').min(axis=1)
    df['MIN_SHEEP_PRODUCTION']    = df.filter(regex='^P._SHEEP_PRODUCTION$').min(axis=1)
    df['MIN_BRICK_PRODUCTION']    = df.filter(regex='^P._BRICK_PRODUCTION$').min(axis=1)
    df['MIN_WOOD_PRODUCTION']     = df.filter(regex='^P._WOOD_PRODUCTION$').min(axis=1)
    df['MIN_ORE_PRODUCTION']      = df.filter(regex='^P._ORE_PRODUCTION$').min(axis=1)
    df['MEAN_PLAYED_KNIGHT']       = df.filter(regex='^P._PLAYED_KNIGHT$').mean(axis=1).round(3)
    df['MEAN_VICTORY_POINTS']      = df.filter(regex='^P._ACTUAL_VICTORY_POINTS$').mean(axis=1).round(3)
    df['MEAN_LONGEST_ROAD_LENGTH'] = df.filter(regex='^P._LONGEST_ROAD_LENGTH$').mean(axis=1).round(3)
    df['MEAN_WHEAT_PRODUCTION']    = df.filter(regex='^P._WHEAT_PRODUCTION$').mean(axis=1).round(3)
    df['MEAN_SHEEP_PRODUCTION']    = df.filter(regex='^P._SHEEP_PRODUCTION$').mean(axis=1).round(3)
    df['MEAN_BRICK_PRODUCTION']    = df.filter(regex='^P._BRICK_PRODUCTION$').mean(axis=1).round(3)
    df['MEAN_WOOD_PRODUCTION']     = df.filter(regex='^P._WOOD_PRODUCTION$').mean(axis=1).round(3)
    df['MEAN_ORE_PRODUCTION']     = df.filter(regex='^P._ORE_PRODUCTION$').mean(axis=1).round(3)
    df['STD_PLAYED_KNIGHT']       = df.filter(regex='^P._PLAYED_KNIGHT$').std(axis=1).round(3)
    df['STD_VICTORY_POINTS']      = df.filter(regex='^P._ACTUAL_VICTORY_POINTS$').std(axis=1).round(3)
    df['STD_LONGEST_ROAD_LENGTH'] = df.filter(regex='^P._LONGEST_ROAD_LENGTH$').std(axis=1).round(3)
    df['STD_WHEAT_PRODUCTION']    = df.filter(regex='^P._WHEAT_PRODUCTION$').std(axis=1).round(3)
    df['STD_SHEEP_PRODUCTION']    = df.filter(regex='^P._SHEEP_PRODUCTION$').std(axis=1).round(3)
    df['STD_BRICK_PRODUCTION']    = df.filter(regex='^P._BRICK_PRODUCTION$').std(axis=1).round(3)
    df['STD_WOOD_PRODUCTION']     = df.filter(regex='^P._WOOD_PRODUCTION$').std(axis=1).round(3)
    df['STD_ORE_PRODUCTION']      = df.filter(regex='^P._ORE_PRODUCTION$').std(axis=1).round(3)
    df['MAX_DEV_CARDS']           = df.filter(regex='^P._(KNIGHT_IN_HAND|YEAR_OF_PLENTY_IN_HAND|MONOPOLY_IN_HAND|ROAD_BUILDING_IN_HAND|VICTORY_POINT_IN_HAND)$').max(axis=1)
    df['MIN_DEV_CARDS']           = df.filter(regex='^P._(KNIGHT_IN_HAND|YEAR_OF_PLENTY_IN_HAND|MONOPOLY_IN_HAND|ROAD_BUILDING_IN_HAND|VICTORY_POINT_IN_HAND)$').min(axis=1)
    df['MEAN_DEV_CARDS']          = df.filter(regex='^P._(KNIGHT_IN_HAND|YEAR_OF_PLENTY_IN_HAND|MONOPOLY_IN_HAND|ROAD_BUILDING_IN_HAND|VICTORY_POINT_IN_HAND)$').mean(axis=1).round(3)
    df['STD_DEV_CARDS']           = df.filter(regex='^P._(KNIGHT_IN_HAND|YEAR_OF_PLENTY_IN_HAND|MONOPOLY_IN_HAND|ROAD_BUILDING_IN_HAND|VICTORY_POINT_IN_HAND)$').std(axis=1).round(3)

    # Selecting game features by turn
    dfFixed = df[fixedCols]
    dfs = []
        
    # Processing game features by turn and player
    numPlayers = df['NUM_PLAYERS'][0]
    winner     = df['WINNER'][0]
    for j in range(numPlayers):
        dfPlayer = df.filter(regex=f'^P{j}').copy()
        dfPlayer.columns = [colname[3:] for colname in dfPlayer.columns]
        dfPlayer['ID_PLAYER'] = j
        dfPlayer['WINS'] = int(winner == j)
        dfs.append(pd.concat([dfFixed, dfPlayer], axis=1))
        
    return pd.concat(dfs, ignore_index=True)

MAP_FEATURES = [
    'WHEAT_PRODUCTION_MAP',
    'SHEEP_PRODUCTION_MAP',
    'BRICK_PRODUCTION_MAP',
    'WOOD_PRODUCTION_MAP',
    'ORE_PRODUCTION_MAP'
]

PROD_FEATURES = [
    'WHEAT_PRODUCTION',
    'SHEEP_PRODUCTION',
    'BRICK_PRODUCTION',
    'WOOD_PRODUCTION',
    'ORE_PRODUCTION'
]

OUTPUT = './batch' + ''.join(random.choices('0123456789', k=10))


class EvaluateBots(SimulationAccumulator):

    def before_all(self):
        self.ouput = OUTPUT
        self.production = None
        self.num_game = -1
        self.winner = []

    def before(self, game):
        self.flag = True
        if self.production is None:
            self.production = {c: {
                'WHEAT': [0],
                'SHEEP': [0],
                'BRICK': [0],
                'WOOD': [0],
                'ORE': [0],
            } for c in game.state.colors}
        else:
            for c in game.state.colors:
                for resource in ['WHEAT', 'SHEEP', 'BRICK', 'WOOD', 'ORE']:
                    self.production[c][resource].append(0)
        self.num_game += 1
        

    def step(self, game, action):
        if not game.state.is_initial_build_phase and self.flag:
            for node, (color, type) in game.state.board.buildings.items():
                if type == 'SETTLEMENT':
                    for resource, production in game.state.board.map.node_production[node].items():
                        self.production[color][resource][-1] += production
            self.flag = False
    def after(self, game):
        if game.winning_color() is not None: self.winner.append(game.winning_color().value)
        
    def after_all(self):
        dfs = []
        for color, production_dict in self.production.items():
            df = pd.DataFrame(production_dict)
            df['COLOR'] = color.value
            df['WINNER'] = self.winner
            df['WINS'] = [int(color.value == c) for c in self.winner]
            df['GAME'] = [i for i in range(len(self.winner))]
            dfs.append(df)
        self.final_df = pd.concat(dfs, ignore_index=True)

class CompletaAccumulator(SimulationAccumulator):
    def before_all(self):
        self.output = OUTPUT
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        self.num_game = 0

        
    def before(self, game):
        self.base_graph  = game.state.board.buildable_subgraph.copy()
        self.node_builds = set()
        self.node_by_color = {
            f"P{player_key(game.state, c)}": set()
            for c in game.state.colors
        }
        self.edges_by_color = {
            f"P{player_key(game.state, c)}": set()
            for c in game.state.colors
        }
        self.aux = {
            f"P{player_key(game.state, c)}": game.state.board.buildable_subgraph.copy()
            for c in game.state.colors
        }
        node_production = game.state.board.map.node_production
        map_info = {}
        for node, v in node_production.items():
            resources = [
                1 * v.get('WHEAT', 0),
                1 * v.get('SHEEP', 0),
                1 * v.get('BRICK', 0),
                1 * v.get('WOOD', 0),
                1 * v.get('ORE', 0)
                ]
            map_info[node] = [int(p*36) for p in resources]
        df = pd.DataFrame(map_info, index=['WHEAT', 'SHEEP', 'BRICK', 'WOOD', 'ORE'])
        suma_resources = df.sum(axis=0).tolist()
        self.game_info = {}
        for i, feat in enumerate(MAP_FEATURES):
            self.game_info[feat] = [suma_resources[i]]

        for k, v in game.state.player_state.items():
            self.game_info[k] = [int(v)]

        for c in game.state.colors:
            for v in PROD_FEATURES:
                k = f"{player_key(game.state, c)}_{v}"
                self.game_info[k] = [0]
            for v in range(6):
                k = f"{player_key(game.state, c)}_{v}"
                self.game_info[k] = [0] 


    def step(self, game, action):
        if action.action_type == ActionType.BUILD_SETTLEMENT:
            key = f"P{player_key(game.state, action.color)}"
            node = action.value
            self.node_builds.add(node)
            self.node_by_color[key].add(node)

        if action.action_type == ActionType.BUILD_ROAD:
            v, u = action.value
            for c in game.state.colors:
                key = f"P{player_key(game.state, c)}"
                if c != action.color:
                    self.aux[key].remove_edge(v, u)
                else:
                    self.edges_by_color[key].add(v)
                    self.edges_by_color[key].add(u)


        if action.action_type in [ActionType.BUILD_SETTLEMENT,
                                  ActionType.BUILD_ROAD]:
            buildables = [i for i in range(54)
                          if i not in self.node_builds and all([j not in self.node_builds
                                                                for j in self.base_graph.neighbors(i)])]
            for c in game.state.colors:
                key = f"P{player_key(game.state, c)}"
                dnodes = {i:float('inf') for i in range(54)}
                resul = {}
                for node_id in self.edges_by_color[key]:
                    G = self.aux[key]
                    shortets_path = nx.single_source_dijkstra_path_length(G, source=node_id)
                    for node, d in shortets_path.items():
                        if node in buildables and d <= dnodes[node]:
                            dnodes[node] = d
                for d in dnodes.values():
                    if d > 5:
                        d = 5
                    if d == float('inf'):
                        continue
                    if d not in resul:
                        resul[d] = 1
                    else:
                        resul[d] += 1
                for i in range(6):
                    if i not in resul:
                        resul[i] = 0
                for d, v in resul.items():
                    self.game_info[f"{player_key(game.state, c)}_{d}"].append(v)
        else:
            for c in game.state.colors:
                for v in range(6):
                    k = f"{player_key(game.state, c)}_{v}"
                    new_value = self.game_info[k][-1]
                    self.game_info[k].append(new_value)

        for k, v in game.state.player_state.items():
            self.game_info[k].append(int(v))

        for feat in MAP_FEATURES:
            self.game_info[feat].append(self.game_info[feat][-1])
        
        for c in game.state.colors:
            for v in PROD_FEATURES:
                k = f"{player_key(game.state, c)}_{v}"
                new_value = self.game_info[k][-1]
                if c == action.color and action.action_type in [
                    ActionType.BUILD_SETTLEMENT, ActionType.BUILD_CITY
                ]:
                    production = game.state.board.map.node_production[action.value]
                    resource = v.split('_')[0]
                    if resource in production:
                        new_value += int(production[resource] * 36)

                self.game_info[k].append(new_value)

        if action.action_type in [ActionType.MOVE_ROBBER,
                                  ActionType.BUILD_SETTLEMENT, 
                                  ActionType.BUILD_CITY]:
            coordinate_current = game.state.board.robber_coordinate
            if action.action_type == ActionType.MOVE_ROBBER:
                coordinate, _, _ = action.value
            else:
                coordinate = coordinate_current
                coordinate_current = None
            add_resources = {c:0 for c in game.state.colors}
            subtrack_resources = {c:0 for c in game.state.colors}
            last_resource = None
            new_resource = None
            i = 0
            for coord, tile in game.state.board.map.land_tiles.items():
                if coord == coordinate_current:
                    last_resource = tile.resource
                    if last_resource == None: 
                        i += 1
                        continue
                    for node_id in tile.nodes.values():
                        building = game.state.board.buildings.get(node_id, None)
                        if building is not None:
                            color = building[0]
                            type = building[1]
                            if type == SETTLEMENT:
                                add_resources[color] += 1
                            else:
                                add_resources[color] += 2
                    i += 1
                if coord == coordinate:
                    new_resource = tile.resource
                    if new_resource == None: i += 1; continue
                    if action.action_type == ActionType.MOVE_ROBBER:
                        for node_id in tile.nodes.values():
                            building = game.state.board.buildings.get(node_id, None)
                            if building is not None:
                                color = building[0]
                                type = building[1]
                                if type == SETTLEMENT:
                                    subtrack_resources[color] += 1
                                else:
                                    subtrack_resources[color] += 2
                    else:
                        node_id = action.value
                        if node_id in tile.nodes.values():
                            building = game.state.board.buildings.get(node_id, None)
                            if building is not None:
                                type = building[1]
                                if type == SETTLEMENT:
                                    subtrack_resources[action.color] += 1
                                else:
                                    subtrack_resources[action.color] += 2
                    i += 1
                if i == 2 or (i == 1 and coordinate_current == None):
                    break
            
            for c in game.state.colors:
                if last_resource != None:
                    k = f"{player_key(game.state, c)}_{last_resource}_PRODUCTION"
                    self.game_info[k][-1] += add_resources[c]
                if new_resource != None:
                    k = f"{player_key(game.state, c)}_{new_resource}_PRODUCTION"
                    self.game_info[k][-1] -= subtrack_resources[c]
            

    def after(self, game):
        for k, v in game.state.player_state.items():
            self.game_info[k].append(int(v))
        for feat in MAP_FEATURES:
            self.game_info[feat].append(self.game_info[feat][-1])
        for c in game.state.colors:
            for v in PROD_FEATURES:
                k = f"{player_key(game.state, c)}_{v}"
                new_value = self.game_info[k][-1]
                self.game_info[k].append(new_value)
            for v in range(6):
                k = f"{player_key(game.state, c)}_{v}"
                new_value = self.game_info[k][-1]
                self.game_info[k].append(new_value)

        df = pd.DataFrame(self.game_info)
        #print(game.winning_color())
        #print(player_key(game.state, game.winning_color()))
        winner = int(player_key(game.state, game.winning_color())[1])
        num_players = len(game.state.players)
        df['WINNER'] = winner
        df['NUM_PLAYERS'] = num_players
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'TURN'}, inplace=True)
        df_cleaned = clean_data(df, self.num_game)
        df_cleaned.to_csv(f"{self.output}/game_{game.id}.csv", index=False)  
        self.num_game += 1

    def after_all(self):
        dfs = []
        for file_name in os.listdir(self.output):
            if file_name.endswith('.csv'):
                df = pd.read_csv(os.path.join(self.output, file_name))
                dfs.append((df))

        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(f"{self.output}.csv", index=False)