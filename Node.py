import random

class Node:
    def __init__(self, x, y, n, weights = None):
        self.x = x
        self.y = y
        self.n = n
        if weights == None:
            self.weights = [random.random() for x in range(self.n)]
        else:
            self.weights = weights
        self.weight_num = 0,
        self.weight_dem = 0
        self.u_val = 0

    def calculate_distance(self, input_vector):
        distance = 0
        for i in range(len(input_vector)):
            distance += (input_vector[i] - self.weights[i]) ** 2
        return distance

    def update_weights(self, weights):
        self.weights = weights
        '''
        self.weights = [x / self.weight_dem for x in self.weight_num]
        ## Clear weight ratios
        self.weight_num, self.weight_dem = 0
        '''

    def clear_weight_ratio(self):
        self.weight_num, self.weight_dem = 0

    def update_weight_ratio(self, weight_num, weight_dem):
        self.weight_num = weight_num + self.weight_num
        self.weight_dem = weight_dem + self.weight_dem

    def update_numerator(self, weight_num):
        print(type(weight_num))
        self.weight_num = weight_num + self.weight_num

    def update_denominator(self, weight_dem):
        self.weight_dem = weight_dem + self.weight_dem
    
    def __repr__(self):
        #return "({},{}): {}".format(self.x, self.y, self.weights)
        return str(self.weights)
    