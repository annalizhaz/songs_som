import random
import csv

class Node:
    def __init__(self, x, y, n, weights = None):
        '''
        x_len, y_len: size of grid
        n: size of vectors (number of attributes in data)
        u_val: value of Node in U-Matrix
        weights: Node weights - accept passed value of initalize to random values
        '''
        self.x = x
        self.y = y
        self.n = n
        self.u_val = 0
        if weights == None:
            self.weights = [random.random() for x in range(self.n)]
        else:
            self.weights = weights

    def calculate_distance(self, input_vector):
        ## Return Euclidean distance between Node and input_vector
        distance = 0
        for i in range(self.n):
            distance += (input_vector[i] - self.weights[i]) ** 2
        return distance

    def update_weights(self, weights):
        self.weights = weights

    @staticmethod
    def get_map(file_name):
        ## Read map from file
        with open(file_name) as map_file:
            reader = csv.reader(map_file)
            grid = list(reader)
            for i, row in enumerate(grid):
                for j, node in enumerate(row):
                    weights = [float(x) for x in node[1:-1].split(",")]
                    grid[i][j] = Node(i, j, len(weights), weights)
        return grid
    
    def __repr__(self):
        return str(self.weights)
    