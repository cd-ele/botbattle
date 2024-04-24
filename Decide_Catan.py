# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:46:45 2024

@author: alex2
"""

def decide(self, game, playable_actions):
    
   if player_can_play_dev(game.state, game.state.current_color, "KNIGHT"):
       return 'PLAY_KNIGHT_CARD'
    