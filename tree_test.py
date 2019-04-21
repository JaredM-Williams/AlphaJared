from nn_tree import Tree
from game import Game
import numpy as np

new_tree = Tree("model.json", "champion.h5")

def children_test():
    while True:
        new_tree.iteration()
        print(new_tree.root.children)

def value_test():
    for x in range(10000):
        new_tree.iteration()
        print(new_tree.root.children_value)

def visit_count_test():
    while True:
        new_tree.iteration()
        print(new_tree.root.children_visits)

def rollout_root():
    x = 0
    while True:
        new_tree.root.rollout()
        x += 1
        print(x)

def gamestate_mutator_test():
    game = Game()
    state = game.gameState
    for x in range(7):
        actions = state.allowedActions
        a = actions[np.random.randint(len(actions))]
        state, value, done = state.takeAction(a)
    gamestate_mutator(state.board)

def gamestate_mutator(board):
    #final = np.array([6, 7, 3])
    final_one = np.reshape((board == 1).astype(int), (6,7))
    final_two = np.reshape((board == -1).astype(int), (6,7))
    final_three = np.zeros((6,7))
    final = np.array([final_one, final_two, final_three])

    print(final[0])
    print()
    print(final[1])
    print()
    print(final[2])
    print()
    print(final.shape)

visit_count_test()
print("done!")
