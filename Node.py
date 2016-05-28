import random

class Node:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.weights = [random.random() for x in range(self.n)]

    def calculate_distance(input_vector):
        return sum([(attrb - self.weights[i])^2 for i, attrb in enumerate(input_vector)])

    def set_weights(weights):
        self.weights = weights