# -*- coding: utf-8 -*-
""" Author: Jared Williams

This program defines a Tree, an object used to analyze the
possible playouts of a game.

"""

from node import Node
from game import Game
import numpy as np


class Tree:

    win_count = 0
    tie_count = 0

    def __init__(self, root=Node(Game().gameState, index=0)):
        self.root = root

    def iteration(self):
        visited = []   # keeps track of what has been visited
        current = self.root  # starts at the root
        leaf_bool = current.isLeaf()  #
        while not leaf_bool:
            #print("leaf_bool", leaf_bool)
            history = current
            current, index = current.select()
            visited.append([history, index])
            leaf_bool = current.isLeaf()
        new_node, index = current.select()
        visited.append([current, index])
        winning_player = new_node.rollout()
        if winning_player == 0:
            value_addition = 0
        elif winning_player == new_node.game_state.playerTurn:
            value_addition = 1
        else:
            value_addition = -1
        for visits_array in reversed(visited):
            visits_array[0].update_stats(visits_array[1], value_addition)
            value_addition = -value_addition



