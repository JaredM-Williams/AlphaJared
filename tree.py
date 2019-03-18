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
        visited = [[self.root.parent, self.root.index]]   # keeps track of what has been visited
        current = self.root  # starts at the root
        leaf_bool = current.isLeaf()  # checks if the root is a leaf
        while not leaf_bool: # iterates until it finds a Node with no children
            history = current # stores the backstep node
            current, index = current.select() # finds the new node and its index in the backstep node
            visited.append([history, index])
            leaf_bool = current.isLeaf()
        new_node, index = current.select()
        if new_node is Node:
            visited.append([current, index])
            roll_num = new_node.rollout()
            if roll_num is new_node.game_state.playerTurn:
                value_addition = True
            else:
                value_addition = False
        else:
            if index is 1:
                value_addition = True
            else:
                value_addition = False

        for visits_array in reversed(visited):
            visits_array[0].update_stats(visits_array[1], value_addition)
            value_addition = not value_addition



