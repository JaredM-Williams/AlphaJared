from game import Game
import random
from tree import Tree
import numpy as np

def tree_v_tree():
    # incomplete
    game = Game()


def person_v_tree():
    game = Game()
    first = random.randint(0,1)
    tree = Tree()
    while not game.gameState._checkForEndGame():
        print("root", tree.root)
        for x in range(50000):
            tree.iteration()
        print("iterated")
        max_index = np.where(tree.root.children_visits == np.amax(tree.root.children_visits))[0][0]
        #print(max_index)
        print("root children value", tree.root.children_value)
        tree.root.children[max_index].root_visits = tree.root.children_value[max_index]
        tree.root = tree.root.children[max_index]
        #print(move_node)
        game.step(game.gameState.allowedActions[max_index])
        game.gameState.print_render()
        print("checkDorEndGame: ", game.gameState._checkForEndGame())
        print("getValue: ", game.gameState._getValue())
        print("getScore: ", game.gameState._getScore())
        if game.gameState._checkForEndGame():
            print("GAME OVER!")
            break
        print(game.gameState.allowedActions)
        good_inputs = [x % 7 for x in game.gameState.allowedActions]
        print(good_inputs)
        inp = input("slot # of next move")
        while int(inp) not in good_inputs:
            inp = input("slot # of next move")
        game.step(game.gameState.allowedActions[good_inputs.index(int(inp))])

        game.gameState.print_render()
        print("checkDorEndGame: ", game.gameState._checkForEndGame())
        print("getValue: ", game.gameState._getValue())
        print("getScore: ", game.gameState._getScore())
    print("GAME OVER!")

person_v_tree()
