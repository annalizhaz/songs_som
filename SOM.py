import random
import 

class SOM:
    def __init__(self, n, x_len = 10, y_len = 10, norm = 1, epochs = 1000):
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

    def train_map(self):
    	





