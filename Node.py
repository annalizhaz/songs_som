import random

class Node:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.weights = [random.random() for x in range(self.n)]
        self.weight_num = 0
        self.weight_dem = 0

    def calculate_distance(self, input_vector):
        return sum([(attrb - self.weights[i])^2 for i, attrb in enumerate(input_vector)])

    def update_weights(self, weights):
        self.weights = self.weight_num / self.weight_dem
        ## Clear weight ratios
        self.weight_num, self.weight_dem = 0

    def clear_weight_ratio(self):
        self.weight_num, self.weight_dem = 0

    def update_weight_ratio(self, weight_num, weight_dem):
        self.weight_num = weight_num + self.weight_num
        self.weight_dem = weight_dem + self.weight_dem