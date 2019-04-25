import os
import numpy as np
import pickle
from res_net import Connect4Model
from play_nn_tree import data_gen
from keras.models import model_from_json
from game import Game
from nn_tree import Tree
import tensorflow as tf
from tensorflow import keras

def main():
    #    TESTING
    #data_gen(10)
    #test_individual_prediction()
    #make_new_nn()
    data_gen(10)
    #test_individual_prediction()
    #model = Connect4Model()
    #model.build()
    #model.predict()

def training_cycle():
    while True:
        data_gen(10)
        train_challenger()
        challenge()

def test_mass_predict():
    path = "/Users/jaredwilliams/Documents/AI/Reinforcement/connect4/"
    pickle_off = open(path + "data.pkl", "rb")
    array = pickle.load(pickle_off)
    board = array[0][0]
    print(board.shape)
    model = Connect4Model()
    model.build()
    board = np.reshape(board, (-1, 6, 7, 1))
    print(board.shape)
    prediction = model.model.predict(board, batch_size=9)
    print(len(prediction))
    print(len(prediction[0]))
    print(prediction[0])


def test_individual_prediction():
    list = []
    path = "/Users/jaredwilliams/Documents/AI/Reinforcement/connect4/"
    pickle_off = open(path + "data.pkl", "rb")
    array = pickle.load(pickle_off)
    board = array[0][0][0]
    print(board.shape)
    board = np.reshape(board, (-1, 6, 7, 1))
    model = Connect4Model()
    model.build()
    prediction = model.model.predict(board)
    print(len(prediction))
    print(prediction[0])
    print()
    print(prediction[0].shape)
    print(prediction[1])

def make_new_nn():
    model = Connect4Model()
    model.build()
    open('model.json', 'w')
    model.save_model("model.json", "champion.h5")


def train_challenger(data_path="data.pkl"):

    path = "/Users/jaredwilliams/Documents/AI/Reinforcement/connect4/"
    pickle_off = open(path + "data.pkl", "rb")
    unformatted_data = pickle.load(pickle_off)

    # format imported: list( tuples( array(boards), winner, array(predictions) ) ) )
    # format for training: array( array(board) )    array( list( array(predictions), winner ) )
    # board: numpy array (6,7)  predictions: numpy array (1, 7)
    board_list = []
    prediction_list = []
    winner_list = []

    for game in unformatted_data:  # game is a tuple
        boards = np.reshape(game[0], (-1, 6, 7, 3))
        for board in boards:  # boards is an array of boards
            board_list.append(board)
        for prediction in game[2]:  # game[2] is an array of predictions
            prediction_list.append(prediction[0])
        winner_list_temp = [game[1]] * game[2].shape[0]
        winner_list = winner_list + winner_list_temp

    board_array = np.array(board_list)
    prediction_array = np.array(prediction_list)
    winner_array = np.array(winner_list)

    print(board_array.shape)
    print(prediction_array.shape)
    print(winner_array.shape)

    json_file = open("model.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("champion.h5")

    tb_callback = keras.callbacks.TensorBoard(log_dir="./logs",
                                              histogram_freq=1, write_graph=True, write_images=True)

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss=['categorical_crossentropy', 'mean_squared_error'],
                  metrics=['accuracy'])

    model.summary()
    print(prediction_array.shape)
    print(winner_array.shape)

    # shuffle data

    #prediction_array = np.reshape(prediction_array, (-1, 7, 1))

    model.fit(board_array, {"value_out1":winner_array, "policy_out1":prediction_array}, epochs=3, callbacks=tb_callback)

    model.save_weights("challenger.h5")


def challenge():

    def challenge_game():
        game = Game()
        winner = 0
        while True:

            for y in range(100):
                challenger_tree.iteration()

            max_index = np.where(challenger_tree.root.children_visits == np.amax(challenger_tree.root.children_visits))[0][0]
            champion_tree.root = champion_tree.root.children[max_index]
            challenger_tree.root = challenger_tree.root.children[max_index]
            game.step(game.gameState.allowedActions[max_index])
            if game.gameState.isEndGame:
                if game.gameState.value[1] != 0:
                    winner = 1
                break

            for y in range(100):
                champion_tree.iteration()

            max_index = np.where(champion_tree.root.children_visits == np.amax(champion_tree.root.children_visits))[0][0]
            champion_tree.root = champion_tree.root.children[max_index]
            challenger_tree.root = challenger_tree.root.children[max_index]
            game.step(game.gameState.allowedActions[max_index])
            if game.gameState.isEndGame:
                if game.gameState.value[1] != 0:
                    winner = -1
                break
        return winner

    json_file = open("model.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    champ_model = model_from_json(loaded_model_json)
    chall_model = model_from_json(loaded_model_json)
    champ_model.load_weights("champion.h5")
    chall_model.load_weights("challenger.h5")
    champion_tree = Tree(champ_model)
    challenger_tree = Tree(chall_model)
    game_num = 1000
    winning_balance = 0
    for i in range(game_num):
        winning_balance += challenge_game()

    if winning_balance >= game_num * .05: # if the champion is 5% better
        # replace the champion
        os.remove("model.h5")
        os.rename("challenger.h5", "champion.h5")
        return True

    else:
        # delete the challenger
        os.remove("challenger.h5")
        return False




if __name__ == '__main__':
    main()
