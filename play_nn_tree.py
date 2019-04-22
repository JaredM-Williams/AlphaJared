from game import Game
from nn_tree import Tree
import numpy as np
import pickle


def main():
    data_gen(10)

def data_gen(number):
    tuple_list = []
    game_count = 0
    for y in range(number):
        state = Game().gameState
        states = []
        while not state.isEndGame:
            states.append(state)
            actions = state.allowedActions
            a = actions[np.random.randint(len(actions))]
            state, value, done = state.takeAction(a)
        rand_gamestate = states[np.random.randint(len(states))]
        tuple_list.append(tree_record(rand_gamestate))
        game_count += 1
        print("GAME:", game_count)
    with open("data.pkl", "wb") as file:
        pickle.dump(tuple_list, file)

def tree_record(gamestate):
    game = Game()
    game.gameState = gamestate
    tree = Tree("model.json", "champion.h5", gamestate_start=gamestate)
    game_list = []
    move_list = []
    winner = 0
    game_list.append(tree.root.proper_board)
    move_list.append(tree.root.nn_prediction[0])
    while True:
        for y in range(5):
            tree.iteration()
        max_index = np.where(tree.root.children_visits == np.amax(tree.root.children_visits))[0][0]
        game.step(tree.root.actions[max_index])
        tree.root = tree.root.children[max_index]
        if game.gameState.isEndGame:
            if game.gameState.value[1] != 0:
                winner = 1
            break
        else:
            game_list.append(tree.root.proper_board)
            move_list.append(tree.root.nn_prediction[0])

        max_index = np.where(tree.root.children_visits == np.amax(tree.root.children_visits))[0][0]
        game.step(tree.root.actions[max_index])
        tree.root = tree.root.children[max_index]
        if game.gameState.isEndGame:
            if game.gameState.value[1] != 0:
                winner = -1
            break
        else:
            game_list.append(tree.root.proper_board)
            move_list.append(tree.root.nn_prediction[0])
    full_tuple = (np.array(game_list), winner, np.array(move_list))
    return full_tuple

if __name__ == '__main__':
    main()
