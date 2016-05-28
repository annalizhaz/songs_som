import random

class Node:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.weights = [random.random() for x in range(n)]
