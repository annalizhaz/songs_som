import random
import math

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

    def train_map(self, input_vectors):
        ## Initalize time variable t
        t = 0
        for i in range(epochs):
            ## Set width exponential decay
            theta = self.theta_naught * ((theta_f / theta_naught) ^ (t / i))
            ## Initalize numerator and denominator in weight equation
            [[self.map(i, j).clear_weight_ratio() for i in range(self.x_len)] for j in range(self.y_len)]

            for input_vector in input_vectors:
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