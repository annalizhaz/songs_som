class SOM:
    def __init__(self, x_len, y_len, n):
        self.x_len = x
        self.y_len = y
        self.n = n
        self.map = [[Node(i, j, self.n) for i in range(self.x_len)] for j in range(self.y_len)]