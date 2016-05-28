class SOM:
    def __init__(self, x, y, n):
        self.map = [[Node(i, j, n) of i in range(x)] for j in range(y)]