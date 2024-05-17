from catanatron import Game, Color
from our_players import Magnate, Granjero, Napoleon


# Play a simple 4v4 game
players = [
    Magnate(Color.RED),
    Granjero(Color.BLUE),
    Napoleon(Color.WHITE)
]
game = Game(players)
print(game.play())  # returns winning color
