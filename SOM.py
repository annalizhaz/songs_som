import random
import math
from Node import *
from SOMMapper import *
import sys

class SOM:
    def __init__(self, n, x_len = 10, y_len = 10, norm = 1, epochs = 25, theta_naught = 10, theta_f = .2):
        '''
        x_len, y_len: size of grid
        n: size of vectors (number of attributes in data)
        '''
        self.x_len = x_len
        self.y_len = y_len
        self.n = n
        self.map = [[Node(i, j, self.n) for i in range(self.x_len)] for j in range(self.y_len)]
        self.norm = norm
        self.epochs = epochs
        self.theta_naught = theta_naught
        self.theta_f = theta_f


    def train_map(self, file_name):
        ## Initalize time variable t
        t = 0
        for i in range(self.epochs):
            ## Set width exponential decay
            theta = self.theta_naught * ((self.theta_f / self.theta_naught) ** (i / self.epochs))
            ## Initalize numerator and denominator in weight equation
            #[[self.map(i, j).clear_weight_ratio() for i in range(self.x_len)] for j in range(self.y_len)]

            compute_weights_job = SOMMapper(self.map, file_name)

        return self.map

        '''
            for song in input_vectors:
                key, input_vector = (song[0], song[1:])
                t += 1

                ## Find min distance over K nodes
                min_distance = self.map[0][0].calculate_distance(input_vector)
                bmu = (0, 0)
                for j in range(self.x_len):
                    for k in range(self.y_len):
                        distance = self.map[j][k].calculate_distance(input_vector)
                        ## Update best matching unit
                        if min_distance > distance:
                            min_distance = distance
                            bmu = (j, k)


                ## Accumulate numerator and denominator in weight equation over K nodes
                for j in range(self.x_len):
                    for k in range(self.y_len):
                        coor_distance = (j - bmu[0])^2 + (k - bmu[1])^2
                        neighborhood = math.exp(-coor_distance / theta^2)
                        self.map[i][j].update_weight_ratio([neighborhood * x for x in input_vector], neighborhood)

            ## Update weight vectors over K nodes
            [[self.map(i, j).set_weights() for i in range(self.x_len)] for j in range(self.y_len)]
        '''


if __name__ == "__main__":
    file_name = sys.argv[2]
    n = int(sys.argv[1])
    ## file in remaining parameters

    som_map = SOM(n)
    grid = som_map.train_map(file_name)