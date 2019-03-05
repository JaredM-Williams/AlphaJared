import tree
from node import Node
import numpy as np

new_tree = tree.Tree()

def visit_count_test():
    while True:
        new_tree.iteration()
        for object in new_tree.root.children:
           print(object.visits),
        print()

def value_test():
    while True:
        new_tree.iteration()
        print(new_tree.root.children_value)

def node_count_test():
    while True:
        new_tree.iteration()
        print(Node.node_count)

def rollout_root():
    x = 0
    while True:
        new_tree.root.rollout()
        x += 1
        print(x)
#def win_loss_tie_test():
value_test()


#test = np.empty(5, dtype=Node)

#print(test[2])
print("done!")