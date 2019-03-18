# -*- coding: utf-8 -*-
""" Author: Jared Williams

This program defines a Tree, an object used to analyze the
possible playouts of a game.

"""

from node import Node
from game import Game
import numpy as np


class Tree:

    def __init__(self, root=Node(Game().gameState, index=0, parent=Node(game_state=Game().gameState, index=None, parent=None))):
        self.root = root
        self.root.parent.children[0] = root

    def iteration(self):
        visited = [self.root]   # keeps track of what has been visited
        current = self.root  # starts at the root
        end = False
        while not end:
            current, end_val, end = current.select()
            visited.append(current)
        if end_val is None:
            rollout = current.rollout()
            matching = rollout == current.game_state.playerTurn
            tie = rollout == 0
        else:
            tie = end_val[1] == 0
            matching = True
        if not tie:
            if matching:
                value_addition = 1
            else:
                value_addition = -1
            for visits_array in reversed(visited):
                visits_array.update_stats(value_addition)
                value_addition = -value_addition


