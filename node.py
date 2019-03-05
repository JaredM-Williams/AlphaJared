# -*- coding: utf-8 -*-
""" Author: Jared Williams

This program defines a Node, an object used to construct a tree, and
used by the Tree class.

"""
from math import sqrt
from math import log
from random import *
import numpy as np


class Node:
    """a Node obejct, created to store in a Tree.

    One Node represents one possible state of a particular
    perfect information game, such as Chess or Connect4, to be
    used in a tree.

    Attributes:
        node_count: keeps track of how many nodes there are.
        """
    node_count = 0

    def __init__(self, game_state, index):
        """Inits a Node with a GameState.

        One Node is initialized with a unique GameState, and it doesn't
        change.

        Attributes:
            game_state: A GameState is a representation of the game board
                at a current point in the game, independent from the previous
                moves.
            value: The approximation on how good of a position it is.
            children: A list that stores the children Nodes.
            actions: The possible GameState objects that can be created
                from the current Node.
            visits: The count of how many times the Node has been visited.
            epsilon: The Multi Armed Bandit coefficient.
            """
        self.game_state = game_state
        self.index = index
        self.value = 0
        self.actions = game_state.allowedActions
        self.children = np.empty(len(self.actions), dtype=Node)
        self.children_value = np.zeros(len(self.actions))
        self.children_visits = np.zeros(len(self.actions))
        self.leaf = True
        self.epsilon = 1e-6

    def update_stats(self, index, value):
        """Updates the value and visits attributes, called by each visited Node
           during backpropagation.

           The visits attribute is updated by one, value is updated by a value
           determined by if that player in the tree won the game or not.

            Args:
                value: the addition to the value attribute.
            """
        self.children_value[index] += value
        self.children_visits[index] += 1

    def isLeaf(self):
        """Returns:
            A boolean of if the Node is a leaf, aka has no children.
            """
        return self.leaf

    def select(self):
        """Looks at the children nodes, and selects one based on the Upper Confidence
           Bound equation, which tries to balance exploration and exploitation, based
           on visits and value of the children Nodes.

            Returns:
                The selected Node and it's index to the parent.
            """
        best_value = - float("inf")
        selected_index = 0
        #print("children", self.children, len(self.children))
        for c in range(len(self.children)):
            uct_value = (self.children_value[c] /
                         (self.children_visits[c] + self.epsilon) +
                         sqrt(log(self.children_visits[c]+1) / (self.children_visits[c] + self.epsilon)) +
                         random() * self.epsilon)
            print(uct_value, " "),
            if uct_value > best_value:
                selected_index = c
                best_value = uct_value
        print()
        #print ("best value:", best_value)
        if self.children[selected_index] is None:
            self.leaf = False
            Node.node_count += 1
            action = self.game_state.allowedActions[selected_index]
            new_game_state = self.game_state.takeAction(action)[0]
            self.children[selected_index] = Node(new_game_state, selected_index)
        return self.children[selected_index], selected_index



    def rollout(self):
        """Does the following until the GameState is the end of the game:

           expands the current Node,
           selects a random child Node,
           makes that child the current Node,
           adds the child to a list of visited Nodes.

            Returns:
                The end state value, and the list of visited Nodes.
            """
        state = self.game_state
        while not state.isEndGame:
            actions = state.allowedActions
            a = actions[np.random.randint(len(actions))]
            state, value, done = state.takeAction(a)
        return state.value[2] * state.playerTurn
