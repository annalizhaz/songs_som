import csv
import random


class Node:

    def __init__(self, x, y, n, weights = None):
        '''
        x_len, y_len: grid size
        n: vectors length (i.e. number of attributes in dataset)
        weights: accept passed vector or initalize to random
        '''
        self.x = x
        self.y = y
        self.n = n
        if weights == None:
            self.weights = [random.random() for x in range(self.n)]
        else:
            self.weights = weights


    def update_weights(self, weights):
        self.weights = weights


    def calculate_distance(self, input_vector):
        ## Return Euclidean distance between node and input_vector
        distance = 0
        for i in range(self.n):
            distance += (input_vector[i] - self.weights[i]) ** 2
        return distance


    @staticmethod
    def get_map(file_name):
        ## Read grid from file; cast to floats
        with open(file_name) as map_file:
            reader = csv.reader(map_file)
            grid = list(reader)
            for i, row in enumerate(grid):
                for j, node in enumerate(row):
                    weights = [float(x) for x in node[1:-1].split(",")]
                    grid[i][j] = Node(i, j, len(weights), weights)
        return grid


    @staticmethod
    def compute_winning_vector(grid, input_vector):
        ## Initalize value, coordinates of BMU
        min_distance = grid[0][0].calculate_distance(input_vector)
        bmu = (0, 0)

        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                distance = node.calculate_distance(input_vector)
                ## Update BMU
                if min_distance > distance:
                    min_distance = distance
                    bmu = (i, j)
        return bmu


    def __repr__(self):
        return str(self.weights)